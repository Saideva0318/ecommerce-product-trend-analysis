# 🛒 E-commerce Product Trend Analysis

## Problem Statement
E-commerce companies need to understand which products are trending, identify seasonal demand patterns, and optimize inventory. This project analyzes product performance trends across categories, time periods, and customer segments.

## Approach
1. **Data Simulation** – 12 months of transaction data across 5 product categories
2. **Market Basket Analysis** – Apriori algorithm to find frequently co-purchased items
3. **Trend Detection** – Rolling averages, seasonal decomposition (STL), MoM velocity
4. **Product Scoring** – Composite score: revenue + growth rate + review rating
5. **Visualization** – Trend dashboards, heatmaps, category comparisons

## Tech Stack
| Layer | Technology |
|-------|------------|
| Language | Python 3.10+ |
| Data Processing | Pandas, NumPy |
| Statistical Analysis | SciPy, statsmodels |
| Market Basket | mlxtend (Apriori, AssociationRules) |
| Visualization | Plotly, Seaborn, Matplotlib |

## Project Structure
```
ecommerce-product-trend-analysis/
├── data/
│   ├── raw/                     # Raw transaction data
│   └── processed/               # Aggregated & encoded data
├── notebooks/
│   └── trend_analysis.ipynb
├── src/
│   ├── __init__.py
│   ├── data_generator.py         # Mock transaction data
│   ├── trend_analysis.py         # Trend detection logic
│   ├── market_basket.py          # Apriori association rules
│   └── product_scorer.py         # Composite product ranking
├── tests/
│   └── test_trends.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Getting Started
```bash
git clone https://github.com/Saideva0318/ecommerce-product-trend-analysis.git
cd ecommerce-product-trend-analysis
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run full analysis
python src/trend_analysis.py
python src/market_basket.py
python src/product_scorer.py
```

## Key Analyses
- **Seasonal Trends**: Identify holiday spikes and off-season dips per category
- **Market Basket**: "Customers who bought X also bought Y" associations
- **Velocity Tracking**: Products with fastest MoM revenue growth
- **Category Share**: Market share shifts over time
- **Product Scoring**: Data-driven ranking to prioritize inventory & promotions

## License
MIT
