# 🛍️ E-commerce Product Trend Analysis

## Problem Statement
E-commerce businesses need to understand which products are trending, when demand peaks, and how buying patterns evolve to optimize inventory, marketing, and pricing strategies.

## Approach
1. **Data Generation** — Synthetic online retail transactions dataset (orders, products, users)
2. **EDA** — Sales velocity, product lifecycle analysis, category performance
3. **Trend Detection** — Moving averages, seasonal decomposition, growth rates
4. **Market Basket Analysis** — Association rules (Apriori) for cross-sell recommendations
5. **Product Ranking** — Composite scoring by revenue, growth, and reviews
6. **Visualization** — Interactive trend dashboards, heatmaps, product scorecards

## Tech Stack
| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| Pandas / NumPy | Data manipulation |
| Plotly / Dash | Interactive visualizations |
| MLxtend | Apriori & association rules |
| Statsmodels | Seasonal decomposition |
| Matplotlib / Seaborn | Static charts |
| Jupyter Notebook | Analysis notebooks |

## Project Structure
```
ecommerce-product-trend-analysis/
├── data/
│   ├── raw/                    # Raw order/product data
│   └── processed/              # Feature-engineered data
├── notebooks/
│   ├── 01_eda_trends.ipynb     # EDA & trend exploration
│   └── 02_market_basket.ipynb  # Market basket analysis
├── src/
│   ├── data_generator.py       # Synthetic data creation
│   ├── trend_analyzer.py       # Trend detection & scoring
│   ├── market_basket.py        # Apriori association rules
│   └── visualizations.py       # Chart generation
├── outputs/
│   └── reports/                # Generated reports
├── requirements.txt
└── README.md
```

## Getting Started
```bash
git clone https://github.com/Saideva0318/ecommerce-product-trend-analysis.git
cd ecommerce-product-trend-analysis
pip install -r requirements.txt

python src/data_generator.py
python src/trend_analyzer.py
python src/market_basket.py
```

## Key Insights Delivered
- Top trending products (30-day momentum)
- Seasonal demand patterns per category
- Product association rules ("customers who bought X also bought Y")
- Revenue concentration (top 20% of products = 80% revenue)
