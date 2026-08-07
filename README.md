# Airbnb Market Intelligence Platform

A production-quality end-to-end data engineering and analytics project analyzing 109,000+ Airbnb listings across Bangkok, London, and Sydney.

---

## Project Overview

This project simulates the kind of market intelligence platform a real analytics team at Airbnb, Booking.com, or Expedia would build — covering the full data pipeline from raw data ingestion to interactive Power BI dashboards.

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| Data Collection | Python, Inside Airbnb (public dataset) |
| Data Cleaning | Python, Pandas |
| Database | SQLite, SQLAlchemy |
| Analysis | SQL, Pandas |
| Visualization | Power BI Desktop |
| Version Control | Git, GitHub |

---

## Architecture
Raw Data (.csv.gz)
↓
Python ETL Pipeline (loader.py + cleaner.py)
↓
SQLite Database (4 normalized tables)
↓
EDA & SQL Analysis (eda.py)
↓
CSV Export (export.py)
↓
Power BI Dashboards

---

## Dataset

- **Source:** [Inside Airbnb](http://insideairbnb.com/get-the-data)
- **Cities:** Bangkok 🇹🇭 | London 🇬🇧 | Sydney 🇦🇺
- **Total Listings:** 109,000+
- **Note:** All prices normalized to USD for cross-city comparison

---

## Database Schema

Four normalized tables following 3NF:

- **hosts** — unique host records with superhost status
- **neighbourhoods** — unique neighbourhood per city
- **listings** — core listing data with foreign keys
- **reviews** — review scores per listing

---

## Dashboards

### Executive Dashboard
High-level KPIs and city comparisons for quick market overview.

### Neighbourhood & Host Dashboard
Neighbourhood-level analysis with listing distribution map and superhost performance metrics.

### Property Type Dashboard
Room type breakdown including Value Score and Demand Ratio analysis.

### Investment Dashboard
ROI-focused analysis including estimated monthly revenue, occupancy rates, and price vs occupancy scatter plot by neighbourhood.

---

## Key Insights

- London has the most listings (62K) but Bangkok commands higher average prices in local currency
- Superhosts maintain a consistent 4.86 avg rating across all three cities
- Sydney leads occupancy rate at 45.5% vs London 40.8% and Bangkok 21.2%
- Private room offers the best balance of Value Score and Demand Ratio for investors
- Woollahra and Waverley (Sydney) top estimated monthly revenue among all neighbourhoods

---

## Project Structure

airbnb-market-intelligence/
├── data/
│ ├── raw/ # Raw .csv.gz files (gitignored)
│ └── cleaned/ # Cleaned CSVs for Power BI
├── scraper/
│ ├── config.py # Project-wide settings
│ ├── loader.py # Data loader
│ └── cleaner.py # Cleaning pipeline
├── database/
│ ├── schema.sql # Database schema
│ ├── load_data.py # DB loader
│ └── export.py # CSV exporter
├── notebooks/
│ └── eda.py # Exploratory data analysis
├── dashboard/
│ └── Airbnb_Dashboard.pbix
└── README.md

---

## How to Run

```bash
# 1. Clone the repo
git clone https://github.com/nayr02/airbnb-market-intelligence.git
cd airbnb-market-intelligence

# 2. Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # Windows
source venv/bin/activate       # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download data from insideairbnb.com and place in data/raw/

# 5. Run the pipeline
python -m notebooks.test_loader     # Load and clean data
python -m database.load_data        # Build database
python -m database.export           # Export for Power BI
python -m notebooks.eda             # Run analysis

# 6. Open dashboard/Airbnb_Dashboard.pbix in Power BI Desktop
```

---

## Author

**Ryan Seguiro**
[LinkedIn](linkedin.com/in/ryanseguiro) • [GitHub](https://github.com/nayR02)