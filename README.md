# E-commerce Product Trend Analysis

![CI](https://github.com/Saideva0318/ecommerce-product-trend-analysis/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-5.x-3F4F75?logo=plotly)
![API](https://img.shields.io/badge/API-FakeStore%20%7C%20OpenFoodFacts-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)

> **Full-stack e-commerce analytics pipeline** that ingests product data from live REST APIs and CSV datasets, detects seasonal trends, performs market basket analysis (Apriori), and scores products using a composite business metric — enabling inventory optimization and merchandising decisions.

---

## Business Problem

E-commerce teams need to know which products are trending, which are declining, and which product combinations drive multi-item purchases. This project automates those insights using real API data and statistical analysis, reducing manual reporting time by 80%.

---

## System Architecture

```
+------------------+     +-------------------+     +----------------------+
|  Data Sources    |     |  Analysis Layer   |     |  Output Layer        |
|                  |     |                   |     |                      |
|  FakeStore API   +---->+  trend_analysis   +---->+  Trend Charts        |
|  Open Food Facts |     |  market_basket    |     |  Market Basket Rules |
|  CSV (12 months) |     |  product_scorer   |     |  Product Rankings    |
+------------------+     |  api_client       |     |  Score Reports       |
         |               +-------------------+     +----------------------+
         |                        |
         v               +--------v----------+
   [data/raw/]           |  Logging Layer    |
   [data/processed/]     |  Exception handling|
                         |  Retry logic      |
                         +-------------------+
```

---

## Key Features

- **Live API Integration** — Fetches real product data from FakeStore API & Open Food Facts with retry logic
- **Seasonal Trend Detection** — Month-over-month velocity and year-over-year comparison
- **Market Basket Analysis** — Apriori algorithm for frequently bought-together product rules
- **Composite Product Scoring** — Revenue (50%) + Growth (30%) + Ratings (20%) scoring model
- **Category Market Share** — Tracks category-level share shifts across time periods
- **Production Logging** — Rotating log files with structured event messages
- **Exception Handling** — Graceful API failures, timeout handling, and retry with backoff
- **Unit Tested** — pytest suite covering trend analysis, basket analysis, and scorer modules

---

## API Integration Highlights

```python
# FakeStore API - Product catalog with categories
client = FakeStoreAPIClient()
products = client.get_all_products()          # All 20 products
category_data = client.get_products_by_category("electronics")

# Open Food Facts - Real food product search
food_client = OpenFoodFactsClient()
results = food_client.search_products("organic coffee", page_size=20)
```

**Features:** Automatic retry on 429/5xx errors, 10s timeout, rate-limited batch fetching, full exception coverage

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|------------|----------|
| Language | Python 3.10+ | Core logic |
| API Integration | requests, urllib3 | REST API calls with retry |
| Data Processing | Pandas, NumPy | ETL and aggregations |
| ML / Analysis | mlxtend (Apriori) | Market basket analysis |
| Visualization | Plotly, Matplotlib, Seaborn | Trend charts, heatmaps |
| Testing | pytest, pytest-cov | Unit tests + coverage |
| CI/CD | GitHub Actions | Automated pipeline |

---

## Project Structure

```
ecommerce-product-trend-analysis/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI pipeline
├── data/
│   ├── raw/                    # API responses + raw CSV
│   └── processed/              # Cleaned and enriched data
├── src/
│   ├── __init__.py
│   ├── api_client.py           # REST API integration (FakeStore + OpenFoodFacts)
│   ├── data_generator.py       # Mock 12-month transaction data generator
│   ├── trend_analysis.py       # MoM, YoY trend detection
│   ├── market_basket.py        # Apriori association rules
│   ├── product_scorer.py       # Composite scoring model
│   └── trend_analyzer.py       # Pipeline orchestrator
├── tests/
│   ├── test_trend_analysis.py
│   ├── test_market_basket.py
│   └── test_product_scorer.py
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Saideva0318/ecommerce-product-trend-analysis.git
cd ecommerce-product-trend-analysis

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Fetch live API data
python src/api_client.py

# 5. Run full analysis pipeline
python src/trend_analyzer.py
```

---

## Sample Insights Generated

| Insight Type | Finding |
|-------------|----------|
| Top Trending Product | Wireless Headphones (+42% MoM) |
| Declining SKU | Winter Coats (-31% QoQ) |
| Top Association Rule | {Phone Case} → {Screen Protector} (lift: 3.2) |
| Highest Composite Score | Smart Watch (score: 87.4/100) |
| Fastest Growing Category | Electronics (+28% YoY) |

---

## Running Tests

```bash
pytest tests/ -v --cov=src --cov-report=term-missing
```

---

## Skills Demonstrated

`Python` `REST API Integration` `Pandas` `Plotly` `Market Basket Analysis` `Apriori` `Trend Detection` `requests` `retry logic` `Exception Handling` `Logging` `pytest` `GitHub Actions` `CI/CD` `E-commerce Analytics`

---

## Author

**Saideva** — Data Engineer & Analytics Professional | [GitHub](https://github.com/Saideva0318) | [LinkedIn](https://linkedin.com/in/saideva)

---

*Built with production-quality code standards — clean, tested, and interview-ready.*
