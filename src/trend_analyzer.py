"""Product Trend Analysis Engine."""

import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import warnings
import os
import logging

warnings.filterwarnings('ignore')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class TrendAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['year_month'] = self.df['date'].dt.to_period('M').astype(str)
        self.df['week'] = self.df['date'].dt.isocalendar().week.astype(int)
        self.df['month'] = self.df['date'].dt.month
        self.df['year'] = self.df['date'].dt.year

    def monthly_product_revenue(self) -> pd.DataFrame:
        return self.df.groupby(['year_month', 'product_name', 'category']).agg(
            revenue=('total_price', 'sum'),
            orders=('order_id', 'count'),
            avg_rating=('rating', 'mean')
        ).reset_index()

    def compute_momentum_scores(self) -> pd.DataFrame:
        """Score products by recent 30-day vs prior 60-day revenue growth."""
        max_date = self.df['date'].max()
        recent = self.df[self.df['date'] >= max_date - pd.Timedelta(days=30)]
        prior = self.df[(self.df['date'] >= max_date - pd.Timedelta(days=90)) &
                        (self.df['date'] < max_date - pd.Timedelta(days=30))]

        r_rev = recent.groupby('product_name')['total_price'].sum().rename('recent_revenue')
        p_rev = prior.groupby('product_name')['total_price'].sum().rename('prior_revenue')
        avg_rat = self.df.groupby('product_name')['rating'].mean().rename('avg_rating')

        momentum = pd.concat([r_rev, p_rev, avg_rat], axis=1).dropna()
        momentum['momentum_score'] = ((momentum['recent_revenue'] - momentum['prior_revenue'])
                                       / (momentum['prior_revenue'] + 1) * 100).round(2)
        momentum['trend'] = momentum['momentum_score'].apply(
            lambda x: '📈 Rising' if x > 10 else ('📉 Declining' if x < -10 else '➡️ Stable')
        )
        return momentum.sort_values('momentum_score', ascending=False).reset_index()

    def seasonal_analysis(self, product_name: str) -> pd.DataFrame:
        """Return monthly seasonality index for a product."""
        prod_df = self.df[self.df['product_name'] == product_name].copy()
        monthly = prod_df.groupby('month')['total_price'].mean()
        monthly_idx = (monthly / monthly.mean() * 100).round(2)
        return monthly_idx.reset_index().rename(columns={'total_price': 'seasonality_index'})

    def pareto_analysis(self) -> pd.DataFrame:
        """80/20 revenue concentration analysis."""
        prod_rev = self.df.groupby('product_name')['total_price'].sum().sort_values(ascending=False).reset_index()
        prod_rev['cumulative_pct'] = prod_rev['total_price'].cumsum() / prod_rev['total_price'].sum() * 100
        prod_rev['revenue_pct'] = prod_rev['total_price'] / prod_rev['total_price'].sum() * 100
        return prod_rev

    def generate_report(self, output_dir: str = 'outputs/reports') -> None:
        os.makedirs(output_dir, exist_ok=True)
        momentum = self.compute_momentum_scores()
        pareto = self.pareto_analysis()
        momentum.to_csv(f'{output_dir}/product_momentum.csv', index=False)
        pareto.to_csv(f'{output_dir}/pareto_analysis.csv', index=False)
        logger.info(f"Reports saved to {output_dir}/")
        print("\n=== Top 5 Rising Products ===")
        print(momentum[momentum['trend'] == '📈 Rising'][['product_name', 'momentum_score', 'avg_rating']].head())


if __name__ == '__main__':
    df = pd.read_csv('data/raw/ecommerce_orders.csv', parse_dates=['date'])
    analyzer = TrendAnalyzer(df)
    analyzer.generate_report()
    print("\n✅ Trend analysis complete!")
