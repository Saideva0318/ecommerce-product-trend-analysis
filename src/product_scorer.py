"""
Product Scorer Module
Composite product ranking using revenue, growth, and rating.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import logging

logger = logging.getLogger(__name__)


def score_products(df: pd.DataFrame, weights: dict = None) -> pd.DataFrame:
    """
    Compute a composite product score combining revenue, growth rate, and customer rating.
    
    Args:
        df: E-commerce orders DataFrame
        weights: Dict with keys 'revenue', 'growth', 'rating' summing to 1.0
    
    Returns:
        Ranked product DataFrame with composite scores
    """
    if weights is None:
        weights = {"revenue": 0.50, "growth": 0.30, "rating": 0.20}
    
    df["month"] = df["date"].dt.to_period("M").astype(str)
    
    agg = df.groupby(["product", "category"]).agg(
        total_revenue=("revenue", "sum"),
        avg_rating=("customer_rating", "mean"),
        total_orders=("order_id", "count")
    ).reset_index()
    
    # Growth: first half vs second half of year
    df["half"] = (df["date"].dt.month > 6).astype(int)
    h1 = df[df["half"] == 0].groupby("product")["revenue"].sum().rename("h1_rev")
    h2 = df[df["half"] == 1].groupby("product")["revenue"].sum().rename("h2_rev")
    growth = pd.concat([h1, h2], axis=1).fillna(0)
    growth["growth_rate"] = (growth["h2_rev"] - growth["h1_rev"]) / (growth["h1_rev"] + 1)
    agg = agg.merge(growth[["growth_rate"]], on="product", how="left").fillna(0)
    
    # Normalize to 0-1
    scaler = MinMaxScaler()
    agg[["rev_norm", "growth_norm", "rating_norm"]] = scaler.fit_transform(
        agg[["total_revenue", "growth_rate", "avg_rating"]]
    )
    
    agg["composite_score"] = (
        weights["revenue"] * agg["rev_norm"]
        + weights["growth"] * agg["growth_norm"]
        + weights["rating"] * agg["rating_norm"]
    ).round(4)
    
    ranked = agg.sort_values("composite_score", ascending=False).reset_index(drop=True)
    ranked.index += 1
    ranked.index.name = "rank"
    
    logger.info(f"Product scoring complete. Top product: {ranked.iloc[0]['product']} (score: {ranked.iloc[0]['composite_score']:.4f})")
    return ranked


if __name__ == "__main__":
    from data_generator import generate_ecommerce_data
    df = generate_ecommerce_data()
    ranked = score_products(df)
    print("\nTop 10 Ranked Products:")
    print(ranked[["product", "category", "total_revenue", "avg_rating", "composite_score"]].head(10).to_string())
