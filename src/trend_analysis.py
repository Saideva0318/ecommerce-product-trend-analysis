"""
Trend Analysis Module
Detects seasonal patterns, MoM growth, and product velocity.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def load_or_generate_data() -> pd.DataFrame:
    """Load existing data or generate fresh mock data."""
    from data_generator import generate_ecommerce_data
    path = Path("data/raw/ecommerce_orders.csv")
    if path.exists():
        return pd.read_csv(path, parse_dates=["date"])
    df = generate_ecommerce_data()
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df


def monthly_category_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute monthly revenue and order counts per category.
    Also calculates MoM growth rate per category.
    """
    df["month"] = df["date"].dt.to_period("M")
    monthly = (
        df.groupby(["month", "category"])
        .agg(revenue=("revenue", "sum"), orders=("order_id", "count"), avg_rating=("customer_rating", "mean"))
        .reset_index()
    )
    monthly["month_str"] = monthly["month"].astype(str)
    
    # MoM growth rate
    monthly = monthly.sort_values(["category", "month"])
    monthly["mom_growth_pct"] = monthly.groupby("category")["revenue"].pct_change() * 100
    monthly["mom_growth_pct"] = monthly["mom_growth_pct"].round(2)
    
    return monthly


def product_velocity(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Identify products with fastest recent growth.
    Uses Q3 vs Q4 revenue comparison as velocity proxy.
    """
    df["quarter"] = df["date"].dt.quarter
    q3 = df[df["quarter"] == 3].groupby("product")["revenue"].sum().rename("q3_revenue")
    q4 = df[df["quarter"] == 4].groupby("product")["revenue"].sum().rename("q4_revenue")
    
    velocity_df = pd.concat([q3, q4], axis=1).fillna(0).reset_index()
    velocity_df["growth_pct"] = ((velocity_df["q4_revenue"] - velocity_df["q3_revenue"]) / (velocity_df["q3_revenue"] + 1) * 100).round(2)
    velocity_df = velocity_df.sort_values("growth_pct", ascending=False).head(top_n)
    
    logger.info(f"Top velocity product: {velocity_df.iloc[0]['product']} ({velocity_df.iloc[0]['growth_pct']:+.1f}% Q3→Q4)")
    return velocity_df


def category_market_share(df: pd.DataFrame) -> pd.DataFrame:
    """Compute monthly category market share as % of total revenue."""
    df["month"] = df["date"].dt.to_period("M").astype(str)
    monthly_cat = df.groupby(["month", "category"])["revenue"].sum().reset_index()
    monthly_total = monthly_cat.groupby("month")["revenue"].sum().rename("total_revenue")
    result = monthly_cat.merge(monthly_total, on="month")
    result["market_share_pct"] = (result["revenue"] / result["total_revenue"] * 100).round(2)
    return result


if __name__ == "__main__":
    df = load_or_generate_data()
    trends = monthly_category_trends(df)
    velocity = product_velocity(df)
    share = category_market_share(df)
    
    print("\n=== Monthly Trends (first 10 rows) ===")
    print(trends.head(10).to_string(index=False))
    print("\n=== Top 10 Product Velocity (Q3 → Q4) ===")
    print(velocity.to_string(index=False))
    print("\n=== Category Market Share Sample ===")
    print(share.head(10).to_string(index=False))
