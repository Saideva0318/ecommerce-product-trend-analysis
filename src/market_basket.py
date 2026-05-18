"""
Market Basket Analysis Module
Apriori algorithm for product association rules.
"""

import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def build_basket(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build basket (one-hot encoded transaction matrix) per customer.
    Groups by customer_id: all products purchased by each customer.
    """
    basket = df.groupby("customer_id")["product"].apply(list).reset_index()
    te = TransactionEncoder()
    te_array = te.fit_transform(basket["product"])
    basket_df = pd.DataFrame(te_array, columns=te.columns_)
    return basket_df


def run_apriori(basket_df: pd.DataFrame, min_support: float = 0.02, min_confidence: float = 0.3) -> pd.DataFrame:
    """
    Run Apriori and return association rules sorted by lift.
    
    Args:
        basket_df: One-hot encoded basket DataFrame
        min_support: Minimum support threshold
        min_confidence: Minimum confidence threshold
    
    Returns:
        DataFrame of association rules with support, confidence, and lift
    """
    freq_items = apriori(basket_df, min_support=min_support, use_colnames=True)
    rules = association_rules(freq_items, metric="confidence", min_threshold=min_confidence)
    rules = rules.sort_values("lift", ascending=False)
    rules["antecedents"] = rules["antecedents"].apply(lambda x: ", ".join(sorted(x)))
    rules["consequents"] = rules["consequents"].apply(lambda x: ", ".join(sorted(x)))
    
    logger.info(f"Found {len(rules)} association rules (min_support={min_support}, min_confidence={min_confidence})")
    return rules[["antecedents", "consequents", "support", "confidence", "lift"]]


if __name__ == "__main__":
    from data_generator import generate_ecommerce_data
    df = generate_ecommerce_data()
    basket_df = build_basket(df)
    rules = run_apriori(basket_df)
    print(f"\nTop 10 Association Rules:")
    print(rules.head(10).to_string(index=False))
