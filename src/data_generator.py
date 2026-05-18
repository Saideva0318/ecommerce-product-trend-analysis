"""
Data Generator Module
Generates realistic mock e-commerce transaction data.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def generate_ecommerce_data(n_orders: int = 8000, seed: int = 42) -> pd.DataFrame:
    """
    Generate mock e-commerce order transaction data with seasonal patterns.
    
    Args:
        n_orders: Number of order records
        seed: Random seed
    
    Returns:
        DataFrame with order-level transaction data
    """
    np.random.seed(seed)
    
    categories = ["Electronics", "Fashion", "Home Decor", "Sports & Fitness", "Beauty"]
    products = {
        "Electronics": ["Wireless Earbuds", "Smart Watch", "Portable Charger", "Bluetooth Speaker", "USB Hub"],
        "Fashion": ["Denim Jacket", "Sneakers", "Hoodie", "Sunglasses", "Backpack"],
        "Home Decor": ["LED Fairy Lights", "Throw Pillow", "Scented Candle", "Wall Clock", "Plant Stand"],
        "Sports & Fitness": ["Resistance Bands", "Yoga Mat", "Water Bottle", "Jump Rope", "Foam Roller"],
        "Beauty": ["Face Serum", "Lip Balm Set", "Eye Cream", "Sunscreen SPF50", "Hair Mask"]
    }
    
    # Seasonal multipliers by month (index 0 = January)
    seasonal_weights = {
        "Electronics": [0.8, 0.7, 0.9, 0.9, 1.0, 1.0, 1.0, 1.0, 1.1, 1.2, 1.5, 1.8],
        "Fashion": [0.7, 0.8, 1.1, 1.2, 1.3, 1.0, 0.9, 1.0, 1.1, 1.0, 1.2, 1.1],
        "Home Decor": [1.0, 0.9, 1.0, 1.2, 1.3, 0.9, 0.8, 0.9, 1.0, 1.1, 1.3, 1.5],
        "Sports & Fitness": [1.4, 1.3, 1.2, 1.0, 1.0, 0.9, 0.9, 0.9, 0.8, 0.9, 1.0, 0.9],
        "Beauty": [1.0, 1.1, 1.0, 1.1, 1.2, 0.9, 0.9, 0.9, 1.0, 1.0, 1.2, 1.3]
    }
    
    dates = pd.date_range(start="2023-01-01", end="2023-12-31", periods=n_orders)
    months = pd.Series(dates).dt.month.values
    
    cat_choices, product_choices = [], []
    for m in months:
        weights = np.array([seasonal_weights[c][m - 1] for c in categories])
        weights /= weights.sum()
        cat = np.random.choice(categories, p=weights)
        cat_choices.append(cat)
        product_choices.append(np.random.choice(products[cat]))
    
    price_ranges = {
        "Electronics": (25, 200), "Fashion": (15, 120), "Home Decor": (10, 80),
        "Sports & Fitness": (8, 90), "Beauty": (10, 60)
    }
    unit_prices = np.array([np.random.uniform(*price_ranges[c]) for c in cat_choices]).round(2)
    quantities = np.random.randint(1, 5, n_orders)
    ratings = np.random.choice([3, 4, 5], n_orders, p=[0.1, 0.45, 0.45]).astype(float)
    ratings += np.random.normal(0, 0.2, n_orders)
    ratings = ratings.clip(1, 5).round(1)
    
    df = pd.DataFrame({
        "order_id": [f"ORD_{i:07d}" for i in range(1, n_orders + 1)],
        "date": dates,
        "category": cat_choices,
        "product": product_choices,
        "unit_price": unit_prices,
        "quantity": quantities,
        "revenue": (unit_prices * quantities).round(2),
        "customer_rating": ratings,
        "customer_id": [f"CUST_{np.random.randint(1, 3000):05d}" for _ in range(n_orders)]
    })
    
    logger.info(f"Generated {n_orders} e-commerce orders for 2023")
    return df


if __name__ == "__main__":
    df = generate_ecommerce_data()
    path = Path("data/raw/ecommerce_orders.csv")
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(df.head())
    print(f"\nRevenue by Category:\n{df.groupby('category')['revenue'].sum().sort_values(ascending=False)}")
