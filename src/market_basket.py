"""Market Basket Analysis using Apriori Algorithm."""

import pandas as pd
import numpy as np
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class MarketBasketAnalyzer:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.basket_matrix = None
        self.frequent_itemsets = None
        self.rules = None

    def build_basket_matrix(self) -> 'MarketBasketAnalyzer':
        logger.info("Building basket matrix...")
        # Group by user_id to simulate session baskets
        baskets = self.df.groupby('user_id')['product_name'].apply(list).reset_index()
        baskets = baskets[baskets['product_name'].apply(len) > 1]  # Multi-item sessions

        te = TransactionEncoder()
        te_array = te.fit_transform(baskets['product_name'].tolist())
        self.basket_matrix = pd.DataFrame(te_array, columns=te.columns_)
        logger.info(f"Basket matrix shape: {self.basket_matrix.shape}")
        return self

    def find_frequent_itemsets(self, min_support: float = 0.02) -> 'MarketBasketAnalyzer':
        logger.info(f"Finding frequent itemsets (min_support={min_support})...")
        self.frequent_itemsets = apriori(self.basket_matrix, min_support=min_support, use_colnames=True)
        logger.info(f"Found {len(self.frequent_itemsets)} frequent itemsets")
        return self

    def generate_rules(self, min_confidence: float = 0.3, min_lift: float = 1.0) -> 'MarketBasketAnalyzer':
        logger.info("Generating association rules...")
        self.rules = association_rules(
            self.frequent_itemsets, metric='confidence', min_threshold=min_confidence
        )
        self.rules = self.rules[self.rules['lift'] >= min_lift]
        self.rules = self.rules.sort_values('lift', ascending=False)
        logger.info(f"Generated {len(self.rules)} rules")
        return self

    def get_recommendations(self, product: str, top_n: int = 5) -> pd.DataFrame:
        """Get top N product recommendations for a given product."""
        relevant = self.rules[self.rules['antecedents'].apply(lambda x: product in x)]
        if relevant.empty:
            return pd.DataFrame({'message': [f'No associations found for {product}']})
        recs = relevant.head(top_n)[['antecedents', 'consequents', 'support', 'confidence', 'lift']]
        recs['antecedents'] = recs['antecedents'].apply(lambda x: ', '.join(x))
        recs['consequents'] = recs['consequents'].apply(lambda x: ', '.join(x))
        return recs

    def save_rules(self, output_dir: str = 'outputs/reports') -> None:
        os.makedirs(output_dir, exist_ok=True)
        if self.rules is not None:
            output = self.rules.copy()
            output['antecedents'] = output['antecedents'].apply(lambda x: ', '.join(x))
            output['consequents'] = output['consequents'].apply(lambda x: ', '.join(x))
            output.to_csv(f'{output_dir}/association_rules.csv', index=False)
            logger.info(f"Rules saved to {output_dir}/association_rules.csv")


if __name__ == '__main__':
    df = pd.read_csv('data/raw/ecommerce_orders.csv')
    analyzer = MarketBasketAnalyzer(df)
    analyzer.build_basket_matrix().find_frequent_itemsets().generate_rules().save_rules()

    print("\n=== Top Association Rules ===")
    if analyzer.rules is not None and len(analyzer.rules) > 0:
        display_rules = analyzer.rules.head(10).copy()
        display_rules['antecedents'] = display_rules['antecedents'].apply(lambda x: ', '.join(x))
        display_rules['consequents'] = display_rules['consequents'].apply(lambda x: ', '.join(x))
        print(display_rules[['antecedents', 'consequents', 'confidence', 'lift']].to_string(index=False))

    print("\n✅ Market basket analysis complete!")
