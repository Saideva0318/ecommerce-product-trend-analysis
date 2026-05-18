"""Synthetic E-commerce Dataset Generator."""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SEED = 42
N_ORDERS = 15000
N_USERS = 3000
START_DATE = datetime(2022, 1, 1)
END_DATE = datetime(2023, 12, 31)

PRODUCT_CATALOG = {
    'P001': {'name': 'Wireless Headphones', 'category': 'Electronics', 'base_price': 79.99, 'trend': 'rising'},
    'P002': {'name': 'Running Sneakers', 'category': 'Footwear', 'base_price': 89.99, 'trend': 'stable'},
    'P003': {'name': 'Yoga Mat Premium', 'category': 'Sports', 'base_price': 34.99, 'trend': 'rising'},
    'P004': {'name': 'Coffee Grinder', 'category': 'Kitchen', 'base_price': 49.99, 'trend': 'stable'},
    'P005': {'name': 'Skincare Serum', 'category': 'Beauty', 'base_price': 39.99, 'trend': 'rising'},
    'P006': {'name': 'Smart Watch Lite', 'category': 'Electronics', 'base_price': 129.99, 'trend': 'rising'},
    'P007': {'name': 'Protein Powder', 'category': 'Health', 'base_price': 44.99, 'trend': 'stable'},
    'P008': {'name': 'Desk Organizer', 'category': 'Office', 'base_price': 24.99, 'trend': 'declining'},
    'P009': {'name': 'Sunglasses UV400', 'category': 'Accessories', 'base_price': 29.99, 'trend': 'seasonal'},
    'P010': {'name': 'Portable Charger', 'category': 'Electronics', 'base_price': 39.99, 'trend': 'rising'},
    'P011': {'name': 'Cooking Apron', 'category': 'Kitchen', 'base_price': 19.99, 'trend': 'declining'},
    'P012': {'name': 'Resistance Bands Set', 'category': 'Sports', 'base_price': 22.99, 'trend': 'rising'},
    'P013': {'name': 'Moisturizer SPF50', 'category': 'Beauty', 'base_price': 32.99, 'trend': 'stable'},
    'P014': {'name': 'Laptop Stand', 'category': 'Office', 'base_price': 45.99, 'trend': 'rising'},
    'P015': {'name': 'Winter Jacket', 'category': 'Apparel', 'base_price': 99.99, 'trend': 'seasonal'},
}


def generate_orders(n: int = N_ORDERS) -> pd.DataFrame:
    np.random.seed(SEED)
    logger.info(f"Generating {n} orders...")

    product_ids = list(PRODUCT_CATALOG.keys())
    product_weights = [0.12, 0.08, 0.09, 0.06, 0.08, 0.10, 0.07, 0.04, 0.06, 0.09, 0.03, 0.07, 0.05, 0.08, 0.08]

    date_range = (END_DATE - START_DATE).days
    dates = [START_DATE + timedelta(days=int(np.random.randint(0, date_range))) for _ in range(n)]
    products_chosen = np.random.choice(product_ids, n, p=product_weights)

    quantities = np.random.randint(1, 5, n)
    user_ids = np.random.randint(1, N_USERS + 1, n)
    ratings = np.random.choice([1, 2, 3, 4, 5], n, p=[0.03, 0.07, 0.15, 0.40, 0.35])
    returned = np.random.choice([0, 1], n, p=[0.92, 0.08])

    records = []
    for i, (date, pid, qty) in enumerate(zip(dates, products_chosen, quantities)):
        product = PRODUCT_CATALOG[pid]
        # Seasonal price variation
        month = date.month
        seasonal_factor = 1.2 if month in [11, 12] else (0.9 if month in [6, 7] else 1.0)
        # Trend factor
        days_from_start = (date - START_DATE).days
        trend_map = {'rising': 1 + 0.0005 * days_from_start,
                     'declining': max(0.7, 1 - 0.0003 * days_from_start),
                     'stable': 1.0,
                     'seasonal': seasonal_factor}
        trend_f = trend_map[product['trend']]
        unit_price = round(product['base_price'] * seasonal_factor * trend_f * np.random.uniform(0.95, 1.05), 2)
        total = round(unit_price * qty, 2)

        records.append({
            'order_id': f'ORD-{str(i+1).zfill(6)}',
            'user_id': f'USR-{str(user_ids[i]).zfill(4)}',
            'product_id': pid,
            'product_name': product['name'],
            'category': product['category'],
            'trend_type': product['trend'],
            'date': date,
            'quantity': qty,
            'unit_price': unit_price,
            'total_price': total,
            'rating': ratings[i],
            'returned': returned[i]
        })

    df = pd.DataFrame(records).sort_values('date').reset_index(drop=True)
    logger.info(f"Generated {len(df)} orders. Revenue: ${df['total_price'].sum():,.2f}")
    return df


if __name__ == '__main__':
    df = generate_orders()
    os.makedirs('data/raw', exist_ok=True)
    df.to_csv('data/raw/ecommerce_orders.csv', index=False)

    catalog_df = pd.DataFrame(PRODUCT_CATALOG).T.reset_index()
    catalog_df.columns = ['product_id', 'product_name', 'category', 'base_price', 'trend']
    catalog_df.to_csv('data/raw/product_catalog.csv', index=False)

    print(f"\n✅ Orders saved. Shape: {df.shape}")
    print(df.groupby('category')['total_price'].sum().sort_values(ascending=False))
