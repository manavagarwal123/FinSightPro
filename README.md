# FinSight Pro 💰

<div align="center">

![FinSight Pro](https://img.shields.io/badge/FinSight-Pro-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=for-the-badge&logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**AI-Powered Financial Analytics Dashboard for Enterprise Use**

[Features](#-key-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Why FinSight Pro?](#-why-finsight-pro)
- [Tech Stack & Libraries](#-tech-stack--libraries)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Detailed Setup Guide](#-detailed-setup-guide)
- [Usage Guide](#-usage-guide)
- [Machine Learning Algorithms](#-machine-learning-algorithms)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**FinSight Pro** is an enterprise-grade, AI-powered financial analytics dashboard designed for automated bank-statement analysis, anomaly detection, month-to-month comparisons, yearly summaries, category insights, and executive financial reporting.

### What Makes It Special?

✅ **Zero Manual Data Entry** - Automatically extracts data from PDF, CSV, or Excel files  
✅ **AI-Powered Insights** - Machine learning algorithms detect anomalies and patterns  
✅ **Executive-Ready Reports** - Professional dashboards suitable for C-suite presentations  
✅ **Interactive Visualizations** - Real-time, interactive charts and graphs  
✅ **Export Capabilities** - Download reports in CSV or Excel format  
✅ **Scalable Architecture** - Handles small to enterprise-level transaction volumes  

### Business Value

- **Time Savings**: Reduce manual financial analysis time by 80%
- **Fraud Detection**: Identify suspicious transactions automatically
- **Data-Driven Decisions**: Make informed financial decisions with AI insights
- **Compliance Ready**: Generate audit-ready financial reports
- **Cost Effective**: Open-source solution with no licensing fees

---

## 🚀 Key Features

### 📄 Smart File Extraction

- Upload bank statements in **PDF**, **CSV**, or **Excel** formats
- Automatic parsing using advanced PDF extraction
- Intelligent column detection (date, amount, category, description)
- Handles messy and inconsistent formats automatically
- Supports multiple date formats and currency notations

### 🧠 AI Intelligence Layer

#### 🔍 Anomaly Detection (Isolation Forest)

- Detects unusual transactions based on amount, category, and timing patterns
- Identifies potentially fraudulent or suspicious activities
- Highlights anomaly dates on interactive time series charts
- Configurable sensitivity (contamination parameter)
- Export detailed anomaly reports as CSV

#### 🧩 Spending Clusters (K-Means)

- Clusters transactions by similarity patterns
- Understand spending behaviors and trends
- Monthly or transaction-level clustering modes
- Helps identify hidden spending patterns
- Visual cluster analysis with scatter plots

### 📊 Executive Financial Dashboard

- **Real-time Metrics**:
  - Lifetime net balance
  - Current month net savings
  - Year-to-date (YTD) net performance
  - Month-over-month percentage changes
  - Top spending categories
  
- **Professional UI**: Clean glassmorphism design suitable for corporate presentations
- **Interactive Charts**: Fully interactive Plotly visualizations with zoom, pan, and hover

### 📅 Month & Year Comparison Tools

#### Month Comparison
- Select and compare multiple months simultaneously
- Analyze spending changes over time
- Calculate month-to-month gain/loss
- Visual trend analysis
- Category breakdown for any selected month

#### Year Comparison
- Compare Year A vs Year B side-by-side
- Category-wise bar chart comparisons
- Year-over-year (YoY) performance metrics
- Export comparison reports as CSV or Excel

### ⭐ Best/Worst Insights (Deep Analysis)

- **Best saving month** - Identify peak savings periods
- **Worst saving month** - Highlight areas needing attention
- **Highest spend month** - Track maximum expenditure
- **Lowest spend month** - Recognize cost-saving periods
- **Detailed financial table** - Month-by-month comprehensive breakdown

### 🏷️ Category Analytics

- Interactive pie charts for category splits
- Download category totals and summaries
- Per-month category drilldown analysis
- Identify dominant spending areas
- Category trend visualization

### 📋 Transaction Management

- Clean, sortable table view for transaction inspection
- Advanced filtering capabilities
- Bulk export in CSV & Excel formats
- Search and filter by date, amount, category
- Transaction-level anomaly flags

---

## 💡 Why FinSight Pro?

### For Financial Analysts
- **Automated Analysis**: Eliminate manual spreadsheet work
- **Pattern Recognition**: AI identifies trends humans might miss
- **Time Efficiency**: Analyze months of data in minutes

### For Business Executives
- **Executive Dashboards**: High-level insights for strategic decisions
- **Risk Management**: Early detection of financial anomalies
- **Performance Tracking**: Clear YoY and MoM comparisons

### For Accountants
- **Audit Trail**: Export detailed reports for compliance
- **Category Management**: Automatic transaction categorization
- **Reconciliation**: Quick month-end and year-end summaries

### For Data Scientists
- **ML Integration**: Built-in anomaly detection and clustering
- **Extensible**: Easy to add custom ML models
- **Data Export**: Export processed data for further analysis

---

## 🏗️ Tech Stack & Libraries

### Why Each Library?

#### **Core Framework**

##### 🎨 [Streamlit](https://streamlit.io/) `>=1.28.0`
**Why we use it:**
- **Rapid Development**: Build interactive web apps in pure Python without HTML/CSS/JS
- **Built-in Components**: Pre-built widgets (file uploaders, charts, tables) reduce development time
- **Session State Management**: Handles user interactions and state persistence automatically
- **Deployment Ready**: One-command deployment to Streamlit Cloud
- **Enterprise Adoption**: Used by Fortune 500 companies for internal dashboards

**Installation:**
```bash
pip install streamlit>=1.28.0
```

---

#### **Data Processing**

##### 📊 [Pandas](https://pandas.pydata.org/) `>=2.0.0`
**Why we use it:**
- **Data Manipulation**: Industry-standard library for data cleaning and transformation
- **Time Series Support**: Built-in date/time handling for financial data
- **Performance**: Optimized C implementations for fast processing
- **Excel Integration**: Native support for reading/writing Excel files
- **DataFrames**: Intuitive tabular data structure for transaction data

**Installation:**
```bash
pip install pandas>=2.0.0
```

##### 🔢 [NumPy](https://numpy.org/) `>=1.24.0`
**Why we use it:**
- **Numerical Computing**: Fast array operations for ML algorithms
- **Mathematical Operations**: Efficient calculations on large datasets
- **ML Foundation**: Required by scikit-learn for feature processing
- **Performance**: Vectorized operations are 10-100x faster than Python loops
- **Memory Efficiency**: Optimized memory usage for large transaction datasets

**Installation:**
```bash
pip install numpy>=1.24.0
```

---

#### **PDF Processing**

##### 📄 [pdfplumber](https://github.com/jsvine/pdfplumber) `>=0.10.0`
**Why we use it:**
- **Bank Statement Extraction**: Specialized for extracting text from PDF bank statements
- **Layout Preservation**: Maintains table structure and formatting
- **Reliable Parsing**: Handles complex PDF layouts better than basic PDF readers
- **Text Extraction**: Accurate extraction of dates, amounts, and descriptions
- **Active Maintenance**: Regularly updated to handle new PDF formats

**Installation:**
```bash
pip install pdfplumber>=0.10.0
```

**Note:** pdfplumber requires system dependencies. On Linux:
```bash
sudo apt-get install python3-dev python3-pip libffi-dev
```

---

#### **Visualization**

##### 📈 [Plotly](https://plotly.com/python/) `>=5.17.0`
**Why we use it:**
- **Interactive Charts**: Zoom, pan, hover, and click interactions
- **Professional Quality**: Publication-ready visualizations
- **Multiple Chart Types**: Line, bar, pie, scatter plots for different analyses
- **Export Options**: Save charts as PNG, PDF, or HTML
- **Responsive Design**: Charts adapt to different screen sizes
- **Enterprise Standard**: Used by major financial institutions

**Installation:**
```bash
pip install plotly>=5.17.0
```

---

#### **Machine Learning**

##### 🤖 [scikit-learn](https://scikit-learn.org/) `>=1.3.0`
**Why we use it:**
- **Isolation Forest**: Industry-standard algorithm for anomaly detection
- **K-Means Clustering**: Proven algorithm for pattern recognition
- **Feature Scaling**: StandardScaler for normalizing financial data
- **Production Ready**: Battle-tested library used in production ML systems
- **Well Documented**: Extensive documentation and examples
- **Performance**: Optimized Cython implementations

**Installation:**
```bash
pip install scikit-learn>=1.3.0
```

**Key Algorithms Used:**
- `IsolationForest`: Detects unusual transactions
- `KMeans`: Groups similar transactions/months
- `StandardScaler`: Normalizes features for ML models

---

#### **Excel Support**

##### 📗 [XlsxWriter](https://xlsxwriter.readthedocs.io/) `>=3.1.0`
**Why we use it:**
- **Excel Export**: Create professional Excel files with formatting
- **Multiple Sheets**: Export multiple data views to different sheets
- **Formatting Control**: Customize fonts, colors, and cell styles
- **Large Files**: Efficiently handles large datasets
- **No Excel Required**: Pure Python implementation, no Microsoft Excel needed

**Installation:**
```bash
pip install xlsxwriter>=3.1.0
```

##### 📘 [openpyxl](https://openpyxl.readthedocs.io/) `>=3.1.0`
**Why we use it:**
- **Excel Reading**: Read existing Excel files uploaded by users
- **Format Preservation**: Maintains formatting when reading files
- **Compatibility**: Works with .xlsx files (Excel 2007+)
- **Pandas Integration**: Seamless integration with pandas DataFrame

**Installation:**
```bash
pip install openpyxl>=3.1.0
```

---

#### **Optional: PDF Generation**

##### 📑 [ReportLab](https://www.reportlab.com/) `>=4.0.0`
**Why we use it (Optional):**
- **PDF Reports**: Generate professional PDF financial reports
- **Custom Layouts**: Full control over report design
- **Charts Integration**: Embed charts and graphs in PDFs
- **Enterprise Reports**: Create executive-ready PDF summaries

**Installation:**
```bash
pip install reportlab>=4.0.0
```

**Note:** This is optional. The app works without it, but PDF export features will be disabled.

---

### Standard Library (No Installation Required)

- **`re`**: Regular expressions for pattern matching in PDF text extraction
- **`io.BytesIO`**: In-memory file handling for Excel/CSV exports

---

## 📦 Installation

### Prerequisites

- **Python 3.8 or higher** (Python 3.10+ recommended)
- **pip** package manager (comes with Python)
- **Git** (for cloning the repository)

### System Requirements

- **RAM**: Minimum 4GB (8GB+ recommended for large datasets)
- **Storage**: 500MB free space
- **OS**: Windows, macOS, or Linux

### Step-by-Step Installation

#### 1. Clone the Repository

```bash
# Using HTTPS
git clone https://github.com/manavagarwal123/FinSightPro.git

# Or using SSH
git clone git@github.com:manavagarwal123/FinSightPro.git

# Navigate to project directory
cd FinSightPro
```

#### 2. Create Virtual Environment (Recommended)

**Why use a virtual environment?**
- Isolates project dependencies
- Prevents conflicts with other Python projects
- Ensures consistent environment across team members

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

#### 3. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list
```

#### 4. Verify Installation

```bash
# Check Python version (should be 3.8+)
python --version

# Check Streamlit installation
streamlit --version

# Test import of key libraries
python -c "import streamlit, pandas, plotly, sklearn; print('All libraries installed successfully!')"
```

---

## 🚀 Quick Start

### Running the Application

```bash
# Make sure you're in the project directory
cd FinSightPro

# Activate virtual environment (if using one)
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Run the Streamlit app
streamlit run app.py
```

The application will:
1. Start the Streamlit server
2. Automatically open your default browser
3. Navigate to `http://localhost:8501`

### First-Time Usage

1. **Upload a File**
   - Click "Upload bank statement"
   - Select a PDF, CSV, or Excel file
   - Wait for automatic parsing

2. **Explore the Dashboard**
   - Start with the **Overview** tab
   - Try different views (Monthly Trend, Categories, etc.)
   - Use the global year filter to focus on specific periods

3. **Test AI Features**
   - Navigate to **AI Intelligence** tab
   - Try anomaly detection with default settings
   - Explore transaction clustering

---

## 📖 Detailed Setup Guide

### For Development

#### Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/manavagarwal123/FinSightPro.git
cd FinSightPro

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies (optional)
pip install pytest black flake8  # For testing and code formatting
```

#### Running in Development Mode

```bash
# Run with auto-reload on file changes
streamlit run app.py --server.runOnSave true

# Run on custom port
streamlit run app.py --server.port 8502
```

### For Production Deployment

#### Option 1: Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy with one click

#### Option 2: Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:
```bash
docker build -t finsight-pro .
docker run -p 8501:8501 finsight-pro
```

#### Option 3: Traditional Server

```bash
# Install dependencies
pip install -r requirements.txt

# Run as a service (using systemd on Linux)
# Create /etc/systemd/system/finsight.service
```

---

## 📖 Usage Guide

### Getting Started

#### 1. Upload Your Data

**Supported Formats:**
- **PDF**: Bank statements (automatically parsed)
- **CSV**: Transaction files with columns: date, amount, description, category
- **Excel**: .xlsx or .xls files with same structure as CSV

**File Requirements:**
- **Date Column**: Should be named `date`, `transaction_date`, `timestamp`, or `time`
- **Amount Column**: Should be named `amount`, `amt`, `value`, `txn_amount`, `debit`, or `credit`
- **Description Column** (optional): `description`, `details`, `remark`, `narration`, or `desc`
- **Category Column** (optional): `category`, `type`, `label`, or `tag`

#### 2. Navigate the Dashboard

**Available Views:**

| View | Icon | Description |
|------|------|-------------|
| Overview | 📊 | Executive summary with key financial metrics |
| Monthly Trend | 📈 | Line chart showing monthly net amounts |
| Yearly Trend | 📅 | Bar chart comparing years |
| Categories | 🏷️ | Pie chart and table of category spending |
| Best/Worst | ⭐ | Deep analysis of best/worst months |
| AI Intelligence | 🤖 | Anomaly detection and clustering |
| Compare Months | 📊 | Side-by-side month comparison |
| Transactions | 📋 | Full transaction table |

#### 3. Use the Global Year Filter

- Located in the top navigation bar
- Select "All" to see all years
- Select a specific year to filter all views
- Filter persists across view changes

### Advanced Features

#### Anomaly Detection

1. Navigate to **AI Intelligence** → **Anomalies** tab
2. Adjust **Contamination** slider (0.001 to 0.2)
   - Lower = fewer anomalies detected (more strict)
   - Higher = more anomalies detected (more sensitive)
3. Toggle **Use absolute amounts** checkbox
   - Checked: Treats large incomes and expenses equally
   - Unchecked: Distinguishes between income and expense anomalies
4. Review highlighted anomalies on the time series chart
5. Export anomaly report as CSV

#### Clustering Analysis

1. Navigate to **AI Intelligence** → **Clusters** tab
2. Choose clustering mode:
   - **Transactions**: Groups individual transactions
   - **Monthly totals**: Groups months by spending patterns
3. Adjust number of clusters (2-6)
4. Review cluster summaries and visualizations
5. Export clustered data as CSV

#### Month Comparison

1. Navigate to **Best/Worst** view
2. Scroll to "Compare Multiple Months" section
3. Select 2 or more months from the dropdown
4. View:
   - Monthly spending summary
   - Month-to-month gain/loss
   - Trend visualization
5. Export comparison as CSV

#### Year Comparison

1. Click **Compare Months** button
2. In the sidebar, select:
   - Year A
   - Year B
3. Click **Compare Years** button
4. View:
   - Side-by-side totals
   - Category-wise comparison
   - Year-over-year percentage change
5. Export comparison as CSV or Excel

---

## 🔧 Machine Learning Algorithms

### 1. Isolation Forest - Anomaly Detection

**Algorithm:** Isolation Forest (Unsupervised Learning)

**How It Works:**
1. Randomly selects features (amount, day, month, category)
2. Randomly splits data points
3. Anomalies are isolated in fewer splits (easier to separate)
4. Assigns anomaly scores based on isolation depth

**Features Used:**
- Transaction amount (absolute or signed)
- Day of month (1-31)
- Month number (1-12)
- Category encoding (one-hot encoded top categories)

**Parameters:**
- `contamination`: Expected proportion of anomalies (0.001 to 0.2)
- `random_state`: Ensures reproducible results

**Use Cases:**
- Fraud detection
- Unusual spending identification
- Data quality checks

**References:**
- [Isolation Forest Paper](https://cs.nju.edu.cn/zhouzh/zhouzh.files/publication/icdm08b.pdf)
- [scikit-learn Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.IsolationForest.html)

### 2. K-Means Clustering - Pattern Detection

**Algorithm:** K-Means Clustering (Unsupervised Learning)

**How It Works:**
1. Initializes K cluster centers randomly
2. Assigns each data point to nearest cluster
3. Updates cluster centers to mean of assigned points
4. Repeats until convergence

**Modes:**

**A. Transaction-Level Clustering:**
- Features: Amount, day, month, category
- Groups similar transactions together
- Identifies spending patterns

**B. Monthly Clustering:**
- Features: Monthly total amount, month number
- Groups similar months together
- Identifies seasonal patterns

**Parameters:**
- `n_clusters`: Number of clusters (2-6)
- `random_state`: Ensures reproducible results
- `n_init`: Number of initializations (10)

**Use Cases:**
- Spending pattern recognition
- Seasonal trend identification
- Budget category optimization

**References:**
- [K-Means Algorithm](https://en.wikipedia.org/wiki/K-means_clustering)
- [scikit-learn Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html)

### 3. StandardScaler - Feature Normalization

**Why Normalization?**
- ML algorithms are sensitive to feature scales
- Amounts (₹1000-₹100000) vs. days (1-31) have different scales
- Normalization ensures all features contribute equally

**How It Works:**
- Transforms features to have mean=0 and std=1
- Formula: `(x - mean) / std`

**Applied To:**
- All numerical features before ML algorithms
- Ensures fair comparison across features

---

## 📚 API Reference

### Key Functions

#### `extract_transactions_from_pdf(file)`

Extracts transactions from PDF bank statements.

**Parameters:**
- `file`: File object (uploaded PDF)

**Returns:**
- `pd.DataFrame`: DataFrame with columns: date, description, amount, category

**Example:**
```python
with open("statement.pdf", "rb") as f:
    df = extract_transactions_from_pdf(f)
```

#### `process_uploaded_file(file)`

Processes uploaded CSV, Excel, or PDF files.

**Parameters:**
- `file`: File object (uploaded file)

**Returns:**
- `pd.DataFrame`: Standardized DataFrame with date, amount, description, category, month, year

**Example:**
```python
df = process_uploaded_file(uploaded_file)
```

#### `classify_transactions(df)`

Classifies transactions as income or expense.

**Parameters:**
- `df`: DataFrame with transaction data

**Returns:**
- `pd.DataFrame`: DataFrame with added `is_income` and `actual_amount` columns

**Example:**
```python
df_classified = classify_transactions(df)
```

#### `df_to_csv_bytes(df)`

Converts DataFrame to CSV bytes for download.

**Parameters:**
- `df`: DataFrame to convert

**Returns:**
- `bytes`: CSV file as bytes

#### `df_to_excel_bytes(sheets)`

Converts multiple DataFrames to Excel bytes.

**Parameters:**
- `sheets`: Dictionary of {sheet_name: DataFrame}

**Returns:**
- `bytes`: Excel file as bytes

---

## 🔍 Troubleshooting

### Common Issues

#### 1. Import Errors

**Problem:** `ModuleNotFoundError` when running the app

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Verify installation
pip list | grep streamlit
```

#### 2. PDF Parsing Fails

**Problem:** PDF upload doesn't extract transactions

**Solutions:**
- Ensure PDF is not password-protected
- Check if PDF contains text (not just images)
- Try converting PDF to CSV/Excel manually
- Check PDF format matches expected bank statement layout

#### 3. Port Already in Use

**Problem:** `Port 8501 is already in use`

**Solution:**
```bash
# Use a different port
streamlit run app.py --server.port 8502

# Or kill the process using port 8501
# On Linux/Mac:
lsof -ti:8501 | xargs kill
# On Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

#### 4. Memory Issues with Large Files

**Problem:** App crashes or runs slowly with large datasets

**Solutions:**
- Process files in chunks
- Increase system RAM
- Filter data by year before processing
- Use more efficient data types (e.g., `category` dtype for categories)

#### 5. Date Parsing Errors

**Problem:** Dates not recognized correctly

**Solution:**
- Ensure dates are in format: YYYY-MM-DD, DD/MM/YYYY, or DD-MM-YYYY
- Check CSV/Excel date column format
- Manually convert dates to standard format before upload

#### 6. Anomaly Detection Shows No Results

**Problem:** No anomalies detected

**Solutions:**
- Increase contamination parameter (try 0.1 or 0.2)
- Uncheck "Use absolute amounts" if checked
- Ensure dataset has sufficient variation
- Check if dataset is too small (< 10 transactions)

### Getting Help

1. **Check Issues**: Search [GitHub Issues](https://github.com/manavagarwal123/FinSightPro/issues)
2. **Create Issue**: Open a new issue with:
   - Error message
   - Steps to reproduce
   - Python version
   - Operating system
3. **Review Documentation**: Check this README and code comments

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### How to Contribute

1. **Fork the Repository**
   ```bash
   git fork https://github.com/manavagarwal123/FinSightPro.git
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Follow PEP 8 style guide
   - Add comments for complex logic
   - Update documentation if needed

4. **Test Your Changes**
   ```bash
   streamlit run app.py
   # Test all features
   ```

5. **Commit and Push**
   ```bash
   git add .
   git commit -m "Add: Description of your changes"
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Go to GitHub repository
   - Click "New Pull Request"
   - Describe your changes

### Contribution Guidelines

- **Code Style**: Follow PEP 8
- **Documentation**: Update README for new features
- **Testing**: Test your changes thoroughly
- **Commits**: Write clear, descriptive commit messages

### Areas for Contribution

- [ ] Additional ML models (forecasting, classification)
- [ ] Support for more file formats
- [ ] Enhanced PDF parsing for different banks
- [ ] UI/UX improvements
- [ ] Performance optimizations
- [ ] Documentation improvements
- [ ] Unit tests
- [ ] Docker configuration
- [ ] CI/CD pipeline

---

## 📝 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 Manav Agarwal

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

### Built With

- **[Streamlit](https://streamlit.io/)** - Rapid web app development framework
- **[Plotly](https://plotly.com/python/)** - Interactive visualization library
- **[scikit-learn](https://scikit-learn.org/)** - Machine learning algorithms
- **[pdfplumber](https://github.com/jsvine/pdfplumber)** - PDF text extraction
- **[Pandas](https://pandas.pydata.org/)** - Data manipulation and analysis
- **[NumPy](https://numpy.org/)** - Numerical computing foundation

### Inspiration

This project was inspired by the need for automated financial analysis tools that combine the power of machine learning with user-friendly interfaces.

### Contributors

- **Manav Agarwal** - Creator and Maintainer

---

## 📞 Support & Contact

- **GitHub Issues**: [Report bugs or request features](https://github.com/manavagarwal123/FinSightPro/issues)
- **Repository**: [https://github.com/manavagarwal123/FinSightPro](https://github.com/manavagarwal123/FinSightPro)

---

<div align="center">

**Made with ❤️ for better financial insights**

⭐ **Star this repo if you find it useful!**

[⬆ Back to Top](#finsight-pro-)

</div>
