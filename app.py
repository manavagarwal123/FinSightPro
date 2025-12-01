# app.py - FinSight Pro (Final: single global year filter in TOP BAR)
import streamlit as st
import pandas as pd
import pdfplumber
import re
import plotly.express as px
import numpy as np
from io import BytesIO

# ML imports
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Optional PDF generation (reportlab)
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import mm
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False

st.set_page_config(page_title="FinSight Pro", layout="wide")

# ------------------------- Clean Corporate Header -------------------------
st.markdown(
    """
    <style>
        .header-container {
            padding: 24px 28px;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 14px;
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            box-shadow: 0 4px 20px rgba(0,0,0,0.35);
            margin-bottom: 12px;
        }
        .header-title {
            font-size: 26px;
            font-weight: 700;
            letter-spacing: -0.3px;
            color: #ffffff;
        }
        .header-subtitle {
            font-size: 14px;
            color: rgba(255,255,255,0.65);
            margin-top: 4px;
        }
        .header-tag {
            background: rgba(255,255,255,0.08);
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 12px;
            color: rgba(255,255,255,0.75);
            border: 1px solid rgba(255,255,255,0.1);
        }
        .glass { background: rgba(255,255,255,0.03); padding: 10px; border-radius: 12px; margin-bottom: 12px; }
        .glass-sm { background: rgba(255,255,255,0.02); padding: 8px; border-radius: 10px; }
        .metric { font-size:20px; font-weight:700; color:#fff; margin-top:6px; }
        .small { color:rgba(255,255,255,0.8); font-size:12px; }
        .muted { color:rgba(255,255,255,0.6); font-size:12px; }
    </style>
    <div class="header-container">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <div>
                <div class="header-title">FinSight Pro</div>
                <div class="header-subtitle">AI-Powered Finance Analytics Platform</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# ------------------------- Utilities -------------------------
def extract_transactions_from_pdf(file):
    transactions = []
    pattern = re.compile(r"(\d{1,3}(?:,\d{3})*(?:\.\d{2})|\d+(?:\.\d{2}))")
    try:
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text:
                    continue
                for line in text.split("\n"):
                    parts = line.split()
                    if len(parts) < 2:
                        continue
                    m = pattern.search(line.replace("■", ""))
                    if not m:
                        continue
                    amt_str = m.group(1).replace(",", "")
                    try:
                        amount = float(amt_str)
                    except:
                        continue
                    date_match = re.search(r"(20\d{2}-\d{2}-\d{2})", line) \
                                 or re.search(r"(\d{2}/\d{2}/20\d{2})", line) \
                                 or re.search(r"(\d{2}-\d{2}-20\d{2})", line)
                    if not date_match:
                        continue
                    date_raw = date_match.group(1)
                    try:
                        date = pd.to_datetime(date_raw, dayfirst=False, errors='coerce')
                        if pd.isna(date):
                            date = pd.to_datetime(date_raw, dayfirst=True, errors='coerce')
                    except:
                        date = None
                    if date is None or pd.isna(date):
                        continue
                    date = date.strftime("%Y-%m-%d")
                    category = parts[-1] if len(parts) >= 2 else "Uncategorized"
                    desc = " ".join(parts[1:-1]) if len(parts) > 2 else ""
                    transactions.append({"date": date, "description": desc, "amount": amount, "category": category})
    except Exception as e:
        st.error("PDF parsing error: " + str(e))
    return pd.DataFrame(transactions)


def process_uploaded_file(file):
    fname = file.name.lower()
    if fname.endswith(".csv"):
        df = pd.read_csv(file)
    elif fname.endswith(".xlsx") or fname.endswith(".xls"):
        df = pd.read_excel(file)
    elif fname.endswith(".pdf"):
        df = extract_transactions_from_pdf(file)
    else:
        st.error("Unsupported file type.")
        return None

    df.columns = df.columns.str.lower().str.strip()
    date_cols = ["date", "transaction_date", "timestamp", "time"]
    amt_cols = ["amount", "amt", "value", "txn_amount", "debit", "credit"]
    desc_cols = ["description", "details", "remark", "narration", "desc"]
    cat_cols = ["category", "type", "label", "tag"]

    def find_col(possible):
        for c in df.columns:
            if c in possible:
                return c
        return None

    dcol = find_col(date_cols)
    acol = find_col(amt_cols)
    scol = find_col(desc_cols)
    ccol = find_col(cat_cols)

    if dcol is None or acol is None:
        st.error("Couldn't detect required columns (date/amount). Use a CSV/XLSX with 'date' and 'amount' or upload a statement PDF.")
        return None

    out = pd.DataFrame()
    out["date"] = pd.to_datetime(df[dcol], errors="coerce")
    out["amount"] = pd.to_numeric(df[acol].astype(str).str.replace(",", ""), errors="coerce")
    out["description"] = df[scol].astype(str) if scol else "N/A"
    out["category"] = df[ccol].astype(str) if ccol else "Uncategorized"
    out = out.dropna(subset=["date", "amount"])
    out["month"] = out["date"].dt.to_period("M")
    out["year"] = out["date"].dt.year
    return out.reset_index(drop=True)


# ------------------------- Transaction Classification -------------------------
def classify_transactions(df):
    income_keywords = [
        "salary", "income", "refund", "profit", "credit",
        "interest", "cashback", "deposit", "received"
    ]

    df = df.copy()
    df['desc_clean'] = df['description'].astype(str).str.lower()
    df['cat_clean']  = df['category'].astype(str).str.lower()

    df['is_income'] = df['desc_clean'].apply(lambda x: any(k in x for k in income_keywords)) | \
                      df['cat_clean'].apply(lambda x: any(k in x for k in income_keywords))

    def compute_actual_amount(row):
        amt = row['amount']
        if pd.isna(amt):
            return 0.0
        if row['is_income']:
            return abs(amt)
        return -abs(amt)

    df['actual_amount'] = df.apply(compute_actual_amount, axis=1)
    return df


def df_to_csv_bytes(df):
    b = BytesIO()
    df.to_csv(b, index=False)
    return b.getvalue()


def df_to_excel_bytes(sheets: dict):
    b = BytesIO()
    try:
        with pd.ExcelWriter(b, engine="xlsxwriter") as writer:
            for name, df in sheets.items():
                df.to_excel(writer, sheet_name=name[:31], index=False)
        b.seek(0)
        return b.getvalue()
    except Exception:
        return None


# ------------------------- File Upload UI -------------------------
with st.container():
    st.markdown("<div class='glass-sm' style='margin-top:12px;padding:12px;'>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload bank statement (PDF / CSV / XLSX)", type=["pdf", "csv", "xlsx"])
    st.markdown("</div>", unsafe_allow_html=True)

if not uploaded:
    st.info("Upload a file to start. Use the sample dataset if you want to test quickly.")
    st.stop()

df = process_uploaded_file(uploaded)
if df is None or df.empty:
    st.error("No transactions detected. Check file format or column names.")
    st.stop()

df = classify_transactions(df)

# ensure month/year
if "month" not in df.columns:
    df["month"] = df["date"].dt.to_period("M")
if "year" not in df.columns:
    df["year"] = df["date"].dt.year

# ------------------------- years available (for global filter) -------------------------
years_available = sorted(df["year"].dropna().unique().tolist())

# ------------------------- Session-state initialization -------------------------
if "compare_active" not in st.session_state:
    st.session_state.compare_active = False
if "bestworst_active" not in st.session_state:
    st.session_state.bestworst_active = False
if "ai_active" not in st.session_state:
    st.session_state.ai_active = False
if "iso_contamination" not in st.session_state:
    st.session_state.iso_contamination = 0.05
if "iso_use_abs" not in st.session_state:
    st.session_state.iso_use_abs = True
if "n_clusters_txn" not in st.session_state:
    st.session_state.n_clusters_txn = 3
if "n_clusters_months" not in st.session_state:
    st.session_state.n_clusters_months = 3
if "compare_months_selection" not in st.session_state:
    st.session_state.compare_months_selection = []
# Global year memory
if "global_year" not in st.session_state:
    st.session_state.global_year = "All"

# ------------------------- Top row controls (with GLOBAL YEAR SELECT) -------------------------
st.markdown("<div class='glass' style='margin-top:12px;'>", unsafe_allow_html=True)
cols = st.columns([1,1,1,1,1,1,1,1,1])  # last column reserved for global year select
show_overview = cols[0].button("📊 Overview")
show_monthly = cols[1].button("📈 Monthly Trend")
show_yearly = cols[2].button("📅 Yearly Trend")
show_categories = cols[3].button("🏷️ Categories")
show_bestworst = cols[4].button("⭐ Best/Worst")
show_ai = cols[5].button("🤖 AI Intelligence")
show_compare_btn = cols[6].button("📊 Compare Months")
show_txns = cols[7].button("📋 Transactions")

# Global year select appears in last column of the top bar (option A requested)
years_options = ["All"] + [str(y) for y in years_available]
# Maintain previously selected value if present
selected_global_year = cols[8].selectbox("Year filter (global)", options=years_options, index=years_options.index(str(st.session_state.global_year)) if str(st.session_state.global_year) in years_options else len(years_options)-1, key="global_year_select")
st.markdown("</div>", unsafe_allow_html=True)

# persist buttons state -> we toggle flags
if show_overview:
    st.session_state.compare_active = False
    st.session_state.bestworst_active = False
    st.session_state.ai_active = False
if show_monthly:
    st.session_state.compare_active = False
    st.session_state.bestworst_active = False
    st.session_state.ai_active = False
if show_yearly:
    st.session_state.compare_active = False
    st.session_state.bestworst_active = False
    st.session_state.ai_active = False
if show_categories:
    st.session_state.compare_active = False
    st.session_state.bestworst_active = False
    st.session_state.ai_active = False
if show_bestworst:
    st.session_state.bestworst_active = True
    st.session_state.compare_active = False
    st.session_state.ai_active = False
if show_ai:
    st.session_state.ai_active = True
    st.session_state.compare_active = False
    st.session_state.bestworst_active = False
if show_compare_btn:
    st.session_state.compare_active = True
    st.session_state.ai_active = False
    st.session_state.bestworst_active = False
if show_txns:
    st.session_state.compare_active = False
    st.session_state.bestworst_active = False
    st.session_state.ai_active = False

# store global year in session state
st.session_state.global_year = selected_global_year

# ------------------------- Build df_view based on global year -------------------------
if st.session_state.global_year == "All":
    df_view = df.copy()
else:
    try:
        gy = int(st.session_state.global_year)
        df_view = df[df["year"] == gy].copy()
    except Exception:
        df_view = df.copy()

# if filtered view becomes empty, warn but continue (so UI doesn't crash)
if df_view.empty:
    st.warning("No data for the selected year. The dashboard will show empty/zeroed views for that year.")

# ------------------------- Derived Stats (based on df_view) -------------------------
# Use 'actual_amount' for calculations (income positive, expense negative)
if "actual_amount" not in df_view.columns:
    st.error("The dataset doesn't contain 'actual_amount' after classification. Aborting.")
    st.stop()

total_income = df_view[df_view['actual_amount'] > 0]['actual_amount'].sum()
total_expense = df_view[df_view['actual_amount'] < 0]['actual_amount'].abs().sum()
current_balance_lifetime = total_income - total_expense

# Monthly breakdowns (period index)
monthly_income = df_view[df_view['actual_amount'] > 0].groupby('month')['actual_amount'].sum()
monthly_expense = df_view[df_view['actual_amount'] < 0]['actual_amount'].abs().groupby(df_view['month']).sum()

all_months = sorted(set(monthly_income.index.tolist() + monthly_expense.index.tolist()))
monthly_income = monthly_income.reindex(all_months, fill_value=0)
monthly_expense = monthly_expense.reindex(all_months, fill_value=0)
monthly_savings = monthly_income - monthly_expense

if len(all_months) == 0:
    current_month = "N/A"
    previous_month = None
    current_month_savings = 0
    previous_month_savings = 0
else:
    current_month = all_months[-1]
    previous_month = all_months[-2] if len(all_months) > 1 else None
    current_month_savings = monthly_savings.loc[current_month] if current_month in monthly_savings.index else 0
    previous_month_savings = monthly_savings.loc[previous_month] if (previous_month and previous_month in monthly_savings.index) else 0

# Yearly breakdowns (from full df aggregated by year but still we show "selected year" YTD)
yearly_income_full = df[df['actual_amount'] > 0].groupby('year')['actual_amount'].sum()
yearly_expense_full = df[df['actual_amount'] < 0]['actual_amount'].abs().groupby(df['year']).sum()
years_union_full = sorted(set(list(yearly_income_full.index) + list(yearly_expense_full.index)))
yearly_income_full = yearly_income_full.reindex(years_union_full, fill_value=0)
yearly_expense_full = yearly_expense_full.reindex(years_union_full, fill_value=0)
yearly_net_full = yearly_income_full - yearly_expense_full
yearly_full = yearly_net_full.reindex(sorted(yearly_net_full.index.tolist()), fill_value=0)

def pct_change_str(curr, prev):
    try:
        if prev == 0:
            return "N/A"
        return f"{round(((curr - prev) / prev) * 100, 2)}%"
    except Exception:
        return "N/A"

# ------------------------- Other derived helpers (based on df_view) -------------------------
cat_full = df_view.groupby(["month", "category"])["actual_amount"].sum().reset_index()
total_by_cat = cat_full.groupby("category")["actual_amount"].sum().sort_values(ascending=False)
top_category = total_by_cat.index[0] if len(total_by_cat) > 0 else "N/A"
top_cat_total = total_by_cat.iloc[0] if len(total_by_cat) > 0 else 0
months_with_top_cat = cat_full[cat_full['category'] == top_category].sort_values(by='actual_amount', ascending=False)
top_month_for_cat = months_with_top_cat.iloc[0]['month'] if not months_with_top_cat.empty else "N/A"

monthly_total_amount = df_view.groupby("month")["actual_amount"].sum().reindex(all_months, fill_value=0)

# ------------------------- Conditional sidebar when comparing -------------------------
selected_view_year_sidebar = "All"
year_a = "Select"
year_b = "Select"
compare_years_btn = False
if st.session_state.compare_active:
    st.sidebar.header("View & Compare (Year)")
    st.sidebar.write("This is separate from the global Year filter.")
    selected_view_year_sidebar = st.sidebar.selectbox("Select year (affects only this compare widget)", ["All"] + [str(y) for y in years_available], index=len(years_available))
    st.sidebar.markdown("### Year Comparison")
    year_a = st.sidebar.selectbox("Year A", options=["Select"] + [str(y) for y in years_available])
    year_b = st.sidebar.selectbox("Year B", options=["Select"] + [str(y) for y in years_available])
    compare_years_btn = st.sidebar.button("Compare Years")
# ------------------------- Overview -------------------------
if (not st.session_state.compare_active) and (show_overview or (not any([show_overview, show_monthly, show_yearly, show_categories, show_bestworst, show_ai, show_txns]) and not st.session_state.ai_active and not st.session_state.bestworst_active)):

    st.markdown('<div class="glass" style="margin-top:18px;padding:18px 22px 22px 22px;">', unsafe_allow_html=True)
    st.markdown(
        "<div style='display:flex;justify-content:space-between;align-items:center;'>"
        "<div><h2 style='margin:0px'>🌐 Executive Financial Overview</h2>"
        f"<div class='muted' style='margin-top:4px;'>A concise executive snapshot (Year filter: <b>{st.session_state.global_year}</b>).</div></div>"
        "</div>", 
        unsafe_allow_html=True
    )

    # ---------------- FILTER YEAR FOR OVERVIEW ----------------
    if st.session_state.global_year != "All":
        df_view = df[df["year"] == int(st.session_state.global_year)]
    else:
        df_view = df.copy()

    # ---- LIFETIME & INCOME/EXPENSE CALCULATIONS (FILTERED) ----
    lifetime_income = df_view[df_view['actual_amount'] > 0]['actual_amount'].sum()
    lifetime_expense = df_view[df_view['actual_amount'] < 0]['actual_amount'].abs().sum()
    lifetime_net = lifetime_income - lifetime_expense

    # ---- YTD NET ----
    if st.session_state.global_year != "All":
        vy = int(st.session_state.global_year)
        y_income = yearly_income_full.loc[vy] if vy in yearly_income_full.index else 0
        y_expense = yearly_expense_full.loc[vy] if vy in yearly_expense_full.index else 0
        y_net = y_income - y_expense
        prev_y_net = (yearly_full.loc[vy-1] if (vy-1) in yearly_full.index else 0)
        y_yoy = pct_change_str(y_net, prev_y_net)
    else:
        y_net = yearly_full.sum() if len(yearly_full) > 0 else 0
        y_yoy = "N/A"

    # ---- MOM CHANGE ----
    mom_change = pct_change_str(current_month_savings, previous_month_savings) if previous_month is not None else "N/A"

    # ---- METRICS ----
    c1, c2, c3, c4 = st.columns(4)

    # lifetime
    with c1:
        st.markdown(f"""
        <div class='glass-sm' style='padding:16px;'>
            <div class='small'>💳 Lifetime Net Balance</div>
            <div class='metric'>₹{lifetime_net:,.2f}</div>
            <div class='muted'>Income − Expense across selected data</div>
        </div>
        """, unsafe_allow_html=True)

    # this month
    with c2:
        st.markdown(f"""
        <div class='glass-sm' style='padding:16px;'>
            <div class='small'>📅 This Month Net ({current_month})</div>
            <div class='metric'>₹{current_month_savings:,.2f}</div>
            <div class='muted'>MoM change vs previous month: <b>{mom_change}</b></div>
        </div>
        """, unsafe_allow_html=True)

    # YTD
    with c3:
        st.markdown(f"""
        <div class='glass-sm' style='padding:16px;'>
            <div class='small'>📈 YTD Net ({st.session_state.global_year})</div>
            <div class='metric'>₹{y_net:,.2f}</div>
            <div class='muted'>YoY: <b>{y_yoy}</b></div>
        </div>
        """, unsafe_allow_html=True)

    # top category
    with c4:
        st.markdown(f"""
        <div class='glass-sm' style='padding:16px;'>
            <div class='small'>🏷️ Top Category</div>
            <div class='metric'>{top_category}</div>
            <div class='muted'>Total: ₹{top_cat_total:,.2f} — Peak: {top_month_for_cat}</div>
        </div>
        """, unsafe_allow_html=True)

    # explanation
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class='muted' style='line-height:1.5'>
    <b>What this overview shows</b><br>
    • Filter applies globally: <b>{st.session_state.global_year}</b>.<br>
    • Lifetime Net, This Month Net and YTD all use filtered data.<br>
    </div>
    """, unsafe_allow_html=True)

    # download snapshot
    snapshot_df = pd.DataFrame({
        "metric": ["lifetime_net", "current_month_net", "ytd_net", "top_category"],
        "value": [lifetime_net, current_month_savings, y_net, top_category]
    })
    st.download_button("Download overview snapshot (CSV)", snapshot_df.to_csv(index=False).encode(), file_name="overview_snapshot.csv")

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------- Monthly Trend -------------------------
# Show Monthly Trend ONLY when user clicks the button
if show_monthly and not st.session_state.compare_active:
    st.markdown('<div class="glass" style="margin-top:12px;">', unsafe_allow_html=True)
    st.header(f"📈 Monthly Expense Trend (Year filter: {st.session_state.global_year})")
    try:
        x = [str(m) for m in all_months]
        y = monthly_total_amount.values if len(monthly_total_amount) == len(all_months) else monthly_total_amount.reindex(all_months, fill_value=0).values
        fig = px.line(x=x, y=y, markers=True, title="Monthly Net Amounts (income positive, expense negative)")
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", xaxis_title="Month", yaxis_title="Amount (₹)")
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error("Unable to render monthly trend: " + str(e))
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------- Yearly Trend -------------------------
if (not st.session_state.compare_active) and show_yearly:
    st.markdown('<div class="glass" style="margin-top:12px;">', unsafe_allow_html=True)
    st.header("📅 Yearly Expense Trend (ALL data)")
    try:
        year_index = sorted(set(list(yearly_income_full.index) + list(yearly_expense_full.index)))
        y_vals = [(yearly_income_full.loc[y] if y in yearly_income_full.index else 0) - (yearly_expense_full.loc[y] if y in yearly_expense_full.index else 0) for y in year_index]
        fig2 = px.bar(x=[str(y) for y in year_index], y=y_vals, title="Yearly Net (Income − Expense)")
        fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", xaxis_title="Year", yaxis_title="Net (₹)")
        st.plotly_chart(fig2, use_container_width=True)
    except Exception as e:
        st.error("Unable to render yearly trend: " + str(e))
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------- Categories -------------------------
if (not st.session_state.compare_active) and show_categories:
    st.markdown('<div class="glass" style="margin-top:12px;padding-bottom:12px;">', unsafe_allow_html=True)
    st.header(f"🏷️ Category-wise Spending (Year filter: {st.session_state.global_year})")
    try:
        df_view_local = df_view.copy()
        cat = (
            df_view_local
            .assign(amount_positive = df_view_local["actual_amount"].abs())
            .groupby("category")["amount_positive"]
            .sum()
            .sort_values(ascending=False)
        )
        fig3 = px.pie(cat, names=cat.index, values=cat.values, hole=0.45, title="Category Split (net)")
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("#### Category totals")
        st.dataframe(cat.reset_index().rename(columns={'actual_amount':'total'}), use_container_width=True)
        csv_bytes = df_view_local.groupby("category")["actual_amount"].sum().reset_index().to_csv(index=False).encode()
        st.download_button("Download category totals (CSV)", csv_bytes, file_name="category_totals.csv")
    except Exception as e:
        st.error("Unable to render categories: " + str(e))
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------- Best/Worst (Deep) -------------------------
if st.session_state.bestworst_active:
    st.markdown('<div class="glass" style="margin-top:12px;padding-bottom:12px;">', unsafe_allow_html=True)
    st.header(f"⭐ Financial Highlights — Deep Analysis (Year filter: {st.session_state.global_year})")
    try:
        monthly_expense_local = df_view[df_view['actual_amount'] < 0].groupby('month')['actual_amount'].sum().abs()
        monthly_income_local = df_view[df_view['actual_amount'] > 0].groupby('month')['actual_amount'].sum()
        months_index = sorted(set(monthly_expense_local.index.tolist() + monthly_income_local.index.tolist()))
        monthly_expense_local = monthly_expense_local.reindex(months_index, fill_value=0)
        monthly_income_local = monthly_income_local.reindex(months_index, fill_value=0)
        monthly_savings_local = (monthly_income_local - monthly_expense_local).rename('savings')

        summary_df = pd.DataFrame({'expense': monthly_expense_local, 'income': monthly_income_local, 'savings': monthly_savings_local})
        summary_df['expense_diff'] = summary_df['expense'].diff().fillna(0)
        summary_df['expense_pct_change'] = (summary_df['expense'].pct_change().fillna(0) * 100).round(2)
        summary_df['savings_diff'] = summary_df['savings'].diff().fillna(0)
        summary_df['savings_pct_change'] = (summary_df['savings'].pct_change().fillna(0) * 100).round(2)

        worst_spend_month = summary_df['expense'].idxmax() if not summary_df['expense'].empty else "N/A"
        worst_spend_val = summary_df['expense'].max() if not summary_df['expense'].empty else 0
        best_spend_month = summary_df['expense'].idxmin() if not summary_df['expense'].empty else "N/A"
        best_spend_val = summary_df['expense'].min() if not summary_df['expense'].empty else 0
        best_saving_month = summary_df['savings'].idxmax() if not summary_df['savings'].empty else "N/A"
        best_saving_val = summary_df['savings'].max() if not summary_df['savings'].empty else 0
        worst_saving_month = summary_df['savings'].idxmin() if not summary_df['savings'].empty else "N/A"
        worst_saving_val = summary_df['savings'].min() if not summary_df['savings'].empty else 0

        c1,c2,c3,c4 = st.columns(4)
        c1.markdown(f"**🔴 Worst Spend Month**\n\n{worst_spend_month} — ₹{worst_spend_val:,.2f}")
        c2.markdown(f"**🟢 Best (Lowest) Spend Month**\n\n{best_spend_month} — ₹{best_spend_val:,.2f}")
        c3.markdown(f"**💰 Best Saving Month**\n\n{best_saving_month} — ₹{best_saving_val:,.2f}")
        c4.markdown(f"**⚠️ Worst Saving Month**\n\n{worst_saving_month} — ₹{worst_saving_val:,.2f}")

        st.markdown("---")
        display_df = summary_df.copy()
        display_df.index = display_df.index.astype(str)
        display_df_display = display_df.reset_index().rename(columns={'index':'month'})
        display_df_display['expense'] = display_df_display['expense'].map(lambda x: f"₹{x:,.2f}")
        display_df_display['income'] = display_df_display['income'].map(lambda x: f"₹{x:,.2f}")
        display_df_display['savings'] = display_df_display['savings'].map(lambda x: f"₹{x:,.2f}")
        display_df_display['expense_diff'] = display_df_display['expense_diff'].map(lambda x: f"₹{x:,.2f}")
        display_df_display['expense_pct_change'] = display_df_display['expense_pct_change'].map(lambda x: f"{x}%")
        display_df_display['savings_diff'] = display_df_display['savings_diff'].map(lambda x: f"₹{x:,.2f}")
        display_df_display['savings_pct_change'] = display_df_display['savings_pct_change'].map(lambda x: f"{x}%")

        st.markdown("### 📅 Month-by-Month Financial Summary")
        st.dataframe(display_df_display.set_index('month'), use_container_width=True)
        st.download_button("Download monthly summary (CSV)", df_to_csv_bytes(display_df.reset_index()), file_name="monthly_summary.csv")

        # Compare months
        st.markdown("---")
        st.markdown("📊 **Compare Multiple Months** (pick 2 or more)")

        month_list = sorted(df_view["month"].astype(str).unique())

        sel_months = st.multiselect(
            "Select months (order will be chronological)",
            month_list,
            default=[],   # start empty so user must actively choose
            key="compare_months_selector_local"
        )
        st.session_state.compare_months_selection = sel_months

        if len(sel_months) >= 2:
            sel_idx = pd.PeriodIndex(sel_months, freq="M")
            comp = df_view[df_view["month"].astype(str).isin(sel_months)].groupby("month")["actual_amount"].sum().reindex(sel_idx).sort_index()
            st.markdown("#### 📅 Monthly Spending Summary")
            st.dataframe(comp.to_frame("Total Net (₹)"))
            diffs = comp.diff().fillna(0)
            diff_df = pd.DataFrame({"Month": comp.index.astype(str), "Net": comp.values, "Diff From Prev": diffs.values})
            st.markdown("#### 🔍 Month-to-Month Gain/Loss")
            st.dataframe(diff_df)
            st.markdown("#### 📈 Trend")
            fig_c = px.line(x=comp.index.astype(str), y=comp.values, markers=True)
            st.plotly_chart(fig_c, use_container_width=True)

            compare_export_df = comp.reset_index().rename(columns={"month":"month","actual_amount":"amount"})
            st.download_button("Download compared months (CSV)", compare_export_df.to_csv(index=False).encode(), file_name="compared_months.csv")
        else:
            st.info("Select at least 2 months to compare.")

        # per-month category drilldown
        st.markdown("---")
        st.markdown("### 🏷️ Explore a month's category breakdown")
        month_to_explore = st.selectbox("Select month for category drilldown", display_df.index.astype(str).tolist(), key="drilldown_month")
        if month_to_explore:
            month_df = df_view[df_view['month'].astype(str) == month_to_explore]
            cat_break = (
                month_df.assign(amount_positive = month_df["actual_amount"].abs())
                        .groupby("category")["amount_positive"]
                        .sum()
                        .sort_values(ascending=False)
            )
            st.dataframe(cat_break.reset_index().rename(columns={'actual_amount':'total'}), use_container_width=True)
            
            fig_cat = px.pie(
                cat_break,
                names=cat_break.index,
                values=cat_break.values,
                hole=0.45,
                title="Category Split (positive totals)"
            )
            st.plotly_chart(fig_cat, use_container_width=True)

        st.markdown("---")
        overall_trend = summary_df['expense'].iloc[-1] - summary_df['expense'].iloc[0] if len(summary_df) > 1 else 0
        if overall_trend > 0:
            st.warning("Overall expenses increased across the period. Consider targeting top categories.")
        else:
            st.success("Overall expenses decreased — good job managing spend.")
    except Exception as e:
        st.error("Unable to compute Best/Worst analysis: " + str(e))
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------- AI Intelligence -------------------------
if st.session_state.ai_active:
    st.markdown('<div class="glass" style="margin-top:12px;padding-bottom:12px;">', unsafe_allow_html=True)
    st.header(f"🤖 AI Intelligence (Year filter: {st.session_state.global_year})")

    tab1, tab2, tab3 = st.tabs(["🔍 Anomalies", "🧩 Clusters", "💡 AI Insights"])

    # ----------------- Anomalies -----------------
    with tab1:
        st.subheader("Anomaly Detection — Isolation Forest")
        cont = st.slider("Contamination (expected proportion of anomalies)", min_value=0.001, max_value=0.2, value=st.session_state.iso_contamination, step=0.001, format="%.3f", key="iso_cont_slider")
        st.session_state.iso_contamination = cont
        use_abs_amount = st.checkbox("Use absolute amounts (treat large incomes/spends equally)", value=st.session_state.iso_use_abs, key="iso_use_abs_checkbox")
        st.session_state.iso_use_abs = use_abs_amount

        df_ml = df_view.copy().reset_index(drop=True)
        df_ml['day'] = df_ml['date'].dt.day
        df_ml['month_num'] = df_ml['date'].dt.month
        df_ml['amt_feat'] = df_ml['actual_amount'].abs() if use_abs_amount else df_ml['actual_amount']

        top_n = 8
        top_cats = df_ml['category'].value_counts().nlargest(top_n).index.tolist()
        df_ml['category_trim'] = df_ml['category'].where(df_ml['category'].isin(top_cats), other='__other__')
        cat_dummies = pd.get_dummies(df_ml['category_trim'], prefix='cat')

        features = pd.concat([df_ml[['amt_feat', 'day', 'month_num']], cat_dummies], axis=1)

        if len(features) < 5:
            st.info("Not enough data to run anomaly detection reliably (need at least ~5 transactions).")
        else:
            scaler = StandardScaler()
            X = scaler.fit_transform(features)

            iso = IsolationForest(contamination=float(cont), random_state=42)
            iso.fit(X)
            preds = iso.predict(X)
            scores = iso.decision_function(X)

            df_ml['anomaly'] = preds
            df_ml['anomaly_score'] = scores
            anomalies = df_ml[df_ml['anomaly'] == -1].sort_values(by='anomaly_score')

            st.markdown(f"Detected **{len(anomalies)}** anomalies (contamination={cont}).")
            ts = df_ml.groupby('date')['actual_amount'].sum().reset_index()
            anom_dates = anomalies['date'].unique().tolist()
            ts['is_anom'] = ts['date'].isin(anom_dates)
            fig_ts = px.line(ts, x='date', y='actual_amount', title="Net amount over time (anomalies highlighted)", markers=True)
            if len(anomalies) > 0:
                anom_points = anomalies.groupby('date')['actual_amount'].sum().reset_index()
                fig_ts.add_scatter(x=anom_points['date'].astype(str), y=anom_points['actual_amount'], mode='markers', marker=dict(color='red', size=8), name="Anomaly")
            st.plotly_chart(fig_ts, use_container_width=True)

            st.markdown("### ⚠️ Anomaly Table (top anomalies)")
            display_anom = anomalies[['date', 'description', 'actual_amount', 'category', 'anomaly_score']].copy()
            display_anom = display_anom.sort_values(by='anomaly_score')
            st.dataframe(display_anom.reset_index(drop=True), use_container_width=True)
            st.download_button("Download anomalies (CSV)", display_anom.to_csv(index=False).encode(), file_name="anomalies.csv")

    # ----------------- Clustering -----------------
    with tab2:
        st.subheader("Spending Clusters — K-Means")
        cluster_type = st.radio("Cluster by:", options=["Transactions (each txn)", "Monthly totals"], index=0, key="cluster_type_radio")
        if cluster_type == "Transactions (each txn)":
            n_clusters = st.slider("Number of clusters", 2, 6, value=st.session_state.n_clusters_txn, key="n_clusters_txn_slider")
            st.session_state.n_clusters_txn = n_clusters

            tx_df = df_view.copy().reset_index(drop=True)
            tx_df['day'] = tx_df['date'].dt.day
            tx_df['month_num'] = tx_df['date'].dt.month
            tx_df['amt_feat'] = tx_df['actual_amount'].abs()

            top_n = 6
            top_cats = tx_df['category'].value_counts().nlargest(top_n).index.tolist()
            tx_df['category_trim'] = tx_df['category'].where(tx_df['category'].isin(top_cats), other='__other__')
            cat_dummies = pd.get_dummies(tx_df['category_trim'], prefix='cat')
            feats = pd.concat([tx_df[['amt_feat', 'day', 'month_num']], cat_dummies], axis=1)

            if len(feats) < n_clusters:
                st.info("Not enough distinct data to form that many clusters. Lower the number of clusters.")
            else:
                scaler = StandardScaler()
                X = scaler.fit_transform(feats)
                km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                labels = km.fit_predict(X)
                tx_df['cluster'] = labels

                cluster_summary = tx_df.groupby('cluster')['amt_feat'].agg(['count', 'mean', 'sum']).sort_values(by='mean', ascending=False).reset_index()
                cluster_summary['mean'] = cluster_summary['mean'].map(lambda x: f"₹{x:,.2f}")

                st.markdown("### Cluster Summary (transactions)")
                st.dataframe(cluster_summary, use_container_width=True)

                scatter_df = tx_df.copy()
                scatter_df['amount_signed'] = scatter_df['actual_amount']
                fig_sc = px.scatter(scatter_df, x='date', y='amount_signed', color=scatter_df['cluster'].astype(str),
                                    title="Transactions colored by cluster", hover_data=['description', 'category'])
                st.plotly_chart(fig_sc, use_container_width=True)

                st.markdown("### Sample transactions per cluster")
                for c in sorted(tx_df['cluster'].unique()):
                    st.markdown(f"**Cluster {c} — sample (top 5 by amount)**")
                    st.dataframe(tx_df[tx_df['cluster'] == c].sort_values(by='amt_feat', ascending=False)[['date', 'description', 'actual_amount', 'category']].head(5), use_container_width=True)

                st.download_button("Download clustered transactions (CSV)", tx_df.to_csv(index=False).encode(), file_name="clustered_transactions.csv")
        else:
            n_clusters = st.slider("Number of clusters (months)", 2, 6, value=st.session_state.n_clusters_months, key="n_clusters_months_slider")
            st.session_state.n_clusters_months = n_clusters

            month_tot = df_view.groupby('month')['actual_amount'].sum().reset_index()
            if month_tot.empty:
                st.info("Not enough monthly data to cluster.")
            else:
                month_tot['month_num'] = month_tot['month'].dt.month
                month_tot['amt_abs'] = month_tot['actual_amount'].abs()
                feats = month_tot[['amt_abs', 'month_num']]
                if len(month_tot) < n_clusters:
                    st.info("Not enough months to form that many clusters. Lower the number of clusters.")
                else:
                    scaler = StandardScaler()
                    X = scaler.fit_transform(feats)
                    km = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
                    month_tot['cluster'] = km.fit_predict(X)
                    st.markdown("### Monthly Cluster Assignments")
                    st.dataframe(month_tot[['month', 'actual_amount', 'cluster']].sort_values(by='month'), use_container_width=True)
                    fig_m = px.line(month_tot.sort_values(by='month')['month'].astype(str), y=month_tot.sort_values(by='month')['actual_amount'],
                                    title="Monthly totals (clusters shown as markers)")
                    st.plotly_chart(fig_m, use_container_width=True)
                    st.download_button("Download monthly clusters (CSV)", month_tot.to_csv(index=False).encode(), file_name="monthly_clusters.csv")

    # ----------------- AI Insights -----------------
    with tab3:
        st.subheader("AI Insights — Summary Table")
        cm_str = str(current_month)
        pm_str = str(previous_month) if previous_month is not None else "N/A"
        selected_view_year_display = st.session_state.global_year  # use global year here
        if selected_view_year_display != "All":
            vy = int(selected_view_year_display)
            y_income_ins = yearly_income_full.loc[vy] if vy in yearly_income_full.index else 0
            y_expense_ins = yearly_expense_full.loc[vy] if vy in yearly_expense_full.index else 0
            y_net_ins = y_income_ins - y_expense_ins
            prev_y_net_ins = (yearly_income_full.loc[vy-1] if (vy-1) in yearly_income_full.index else 0) - (yearly_expense_full.loc[vy-1] if (vy-1) in yearly_expense_full.index else 0)
            y_yoy_ins = pct_change_str(y_net_ins, prev_y_net_ins)
        else:
            y_net_ins = yearly_full.sum() if len(yearly_full) > 0 else 0
            y_yoy_ins = "N/A"

        insights_table = pd.DataFrame([
            ["Current Month (net)", cm_str, f"₹{current_month_savings:,.2f}"],
            ["Previous Month (net)", pm_str, f"₹{previous_month_savings:,.2f}"],
            ["Month-over-Month Change (savings)", "-", pct_change_str(current_month_savings, previous_month_savings) if previous_month is not None else "N/A"],
            ["Selected Year (YTD net)", selected_view_year_display, f"₹{y_net_ins:,.2f}"],
            ["Year-over-Year Change (YTD)", "-", y_yoy_ins],
            ["Top Category (net)", top_category, f"₹{top_cat_total:,.2f}"],
            ["Peak Month for Top Category", str(top_month_for_cat), "-"],
            ["Total Transactions (in view)", len(df_view), "-"]
        ], columns=["Insight", "Detail", "Value"])
        st.table(insights_table.astype(str))
        st.download_button("Download insights (CSV)", insights_table.to_csv(index=False).encode(), file_name="insights_table.csv")

    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------- Transactions view -------------------------
if show_txns:
    st.markdown('<div class="glass" style="margin-top:12px;padding-bottom:12px;">', unsafe_allow_html=True)
    st.header(f"📋 All Transactions (Year filter: {st.session_state.global_year})")
    st.dataframe(df_view.sort_values(by="date", ascending=False).reset_index(drop=True), use_container_width=True)
    st.download_button("Download transactions (CSV)", df_view.to_csv(index=False).encode(), file_name="transactions.csv")
    excel_txn = df_to_excel_bytes({"transactions": df_view})
    if excel_txn:
        st.download_button("Download transactions (Excel)", excel_txn, file_name="transactions.xlsx")
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------------- Year Compare (sidebar triggered) -------------------------
if st.session_state.compare_active and compare_years_btn:
    if year_a == "Select" or year_b == "Select":
        st.sidebar.error("Choose both Year A and Year B to compare.")
    else:
        try:
            ya = int(year_a)
            yb = int(year_b)
            total_a = (yearly_income_full.loc[ya] if ya in yearly_income_full.index else 0) - (yearly_expense_full.loc[ya] if ya in yearly_expense_full.index else 0)
            total_b = (yearly_income_full.loc[yb] if yb in yearly_income_full.index else 0) - (yearly_expense_full.loc[yb] if yb in yearly_expense_full.index else 0)
            pctc = pct_change_str(total_b, total_a) if total_a != 0 else "N/A"

            st.markdown('<div class="glass" style="margin-top:12px;padding-bottom:12px;">', unsafe_allow_html=True)
            st.header(f"📊 Year Comparison — {ya} vs {yb}")
            ca, cb, cc = st.columns(3)
            ca.metric(f"Total {ya}", f"₹{total_a:,.2f}")
            cb.metric(f"Total {yb}", f"₹{total_b:,.2f}", pctc)
            cc.markdown(f"**Difference:** ₹{(total_b - total_a):,.2f}")

            cat_a = df[df["year"] == ya].groupby("category")["actual_amount"].sum()
            cat_b = df[df["year"] == yb].groupby("category")["actual_amount"].sum()
            comp_cat = pd.concat([cat_a, cat_b], axis=1).fillna(0)
            comp_cat.columns = [str(ya), str(yb)]
            st.markdown("### 🏷️ Category Comparison")
            st.dataframe(comp_cat)
            comp_cat_plot = comp_cat.reset_index().melt(id_vars='category', value_name='amount')
            figy = px.bar(comp_cat_plot, x='category', y='amount', color='variable', barmode='group')
            st.plotly_chart(figy, use_container_width=True)

            year_compare_df = comp_cat.reset_index()
            st.download_button("Download year compare (CSV)", year_compare_df.to_csv(index=False).encode(), file_name=f"year_compare_{ya}_vs_{yb}.csv")
            excel_compare_bytes = df_to_excel_bytes({f"{ya}_vs_{yb}": year_compare_df})
            if excel_compare_bytes:
                st.download_button("Download year compare (Excel)", excel_compare_bytes, file_name="year_compare_{ya}_vs_{yb}.xlsx")
            st.markdown("</div>", unsafe_allow_html=True)
        except Exception as e:
            st.error("Year compare failed: " + str(e))

# ------------------------- Footer -------------------------
st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)