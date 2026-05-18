"""
Unit Tests — Trend Analysis
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_generator import generate_ecommerce_data
from trend_analysis import monthly_category_trends, product_velocity, category_market_share
from product_scorer import score_products


@pytest.fixture
def df():
    return generate_ecommerce_data(n_orders=1000)


def test_data_shape(df):
    assert df.shape[0] == 1000
    assert "revenue" in df.columns


def test_monthly_trends_has_mom(df):
    trends = monthly_category_trends(df)
    assert "mom_growth_pct" in trends.columns


def test_product_velocity_returns_top_n(df):
    velocity = product_velocity(df, top_n=5)
    assert len(velocity) <= 5


def test_market_share_sums_to_100(df):
    share = category_market_share(df)
    monthly_totals = share.groupby("month")["market_share_pct"].sum()
    assert (monthly_totals.round(0) == 100).all()


def test_product_scorer_has_score(df):
    ranked = score_products(df)
    assert "composite_score" in ranked.columns
    assert (ranked["composite_score"] >= 0).all()
    assert (ranked["composite_score"] <= 1).all()
