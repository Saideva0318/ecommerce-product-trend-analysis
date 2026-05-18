"""
api_client.py - Sample API Integration Module
Fetches product trend data from a public REST API (Open Food Facts / FakeStore API)
Demonstrates: requests, retry logic, exception handling, structured logging
Author: Saideva0318
"""

import logging
import time
from typing import Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ---------------------------------------------------------------
# Configure logging
# ---------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/api_client.log", mode="a"),
    ],
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------
# Constants
# ---------------------------------------------------------------
FAKE_STORE_BASE_URL = "https://fakestoreapi.com"
OPEN_FOOD_BASE_URL = "https://world.openfoodfacts.org/cgi/search.pl"
REQUEST_TIMEOUT = 10  # seconds
MAX_RETRIES = 3
BACKOFF_FACTOR = 0.5


# ---------------------------------------------------------------
# HTTP Session with retry logic
# ---------------------------------------------------------------
def create_session(max_retries: int = MAX_RETRIES) -> requests.Session:
    """Create a requests Session with automatic retry on transient failures."""
    session = requests.Session()
    retry = Retry(
        total=max_retries,
        backoff_factor=BACKOFF_FACTOR,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    logger.info("HTTP session created with retry policy (max_retries=%d)", max_retries)
    return session


# ---------------------------------------------------------------
# FakeStore API - Product Catalog
# ---------------------------------------------------------------
class FakeStoreAPIClient:
    """Client to fetch product data from FakeStore API (simulates e-commerce catalog)."""

    def __init__(self):
        self.base_url = FAKE_STORE_BASE_URL
        self.session = create_session()

    def get_all_products(self) -> list:
        """Fetch all products from the FakeStore API."""
        endpoint = f"{self.base_url}/products"
        logger.info("Fetching all products from FakeStore API: %s", endpoint)
        try:
            response = self.session.get(endpoint, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            products = response.json()
            logger.info("Successfully fetched %d products.", len(products))
            return products
        except requests.exceptions.HTTPError as e:
            logger.error("HTTP error while fetching products: %s", e)
            raise
        except requests.exceptions.ConnectionError as e:
            logger.error("Connection error: %s", e)
            raise
        except requests.exceptions.Timeout:
            logger.error("Request timed out after %ds", REQUEST_TIMEOUT)
            raise
        except requests.exceptions.RequestException as e:
            logger.error("Unexpected request error: %s", e)
            raise

    def get_products_by_category(self, category: str) -> list:
        """Fetch products filtered by category."""
        endpoint = f"{self.base_url}/products/category/{category}"
        logger.info("Fetching products for category '%s'", category)
        try:
            response = self.session.get(endpoint, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("Failed to fetch category '%s': %s", category, e)
            return []

    def get_all_categories(self) -> list:
        """Fetch all available product categories."""
        endpoint = f"{self.base_url}/products/categories"
        try:
            response = self.session.get(endpoint, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            categories = response.json()
            logger.info("Available categories: %s", categories)
            return categories
        except requests.exceptions.RequestException as e:
            logger.error("Failed to fetch categories: %s", e)
            return []


# ---------------------------------------------------------------
# Open Food Facts API - Real Product Data
# ---------------------------------------------------------------
class OpenFoodFactsClient:
    """Client to fetch real product trend data from Open Food Facts (open source)."""

    def __init__(self):
        self.base_url = OPEN_FOOD_BASE_URL
        self.session = create_session()

    def search_products(
        self,
        search_term: str,
        page_size: int = 20,
        page: int = 1,
        fields: Optional[str] = None,
    ) -> dict:
        """
        Search for products by keyword.

        Args:
            search_term: Product name or keyword to search
            page_size: Number of results per page (default 20)
            page: Page number (default 1)
            fields: Comma-separated field names to return

        Returns:
            dict with 'products' list and 'count' total
        """
        if fields is None:
            fields = "product_name,categories,brands,nutriment,ecoscore_grade"

        params = {
            "search_terms": search_term,
            "search_simple": 1,
            "action": "process",
            "json": 1,
            "page_size": page_size,
            "page": page,
            "fields": fields,
        }

        logger.info("Searching Open Food Facts for: '%s' (page %d)", search_term, page)
        try:
            response = self.session.get(
                self.base_url, params=params, timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            count = data.get("count", 0)
            products = data.get("products", [])
            logger.info("Found %d total results, returned %d products.", count, len(products))
            return {"count": count, "products": products}
        except requests.exceptions.RequestException as e:
            logger.error("Open Food Facts search failed: %s", e)
            return {"count": 0, "products": []}


# ---------------------------------------------------------------
# Helper: Rate-limited batch fetcher
# ---------------------------------------------------------------
def fetch_categories_with_rate_limit(
    client: FakeStoreAPIClient,
    delay_seconds: float = 0.5,
) -> dict:
    """
    Fetch products for all categories with rate limiting.

    Args:
        client: FakeStoreAPIClient instance
        delay_seconds: Delay between API calls (respects rate limits)

    Returns:
        dict mapping category name -> list of products
    """
    categories = client.get_all_categories()
    results = {}

    for category in categories:
        logger.info("Fetching category: %s", category)
        products = client.get_products_by_category(category)
        results[category] = products
        time.sleep(delay_seconds)  # Respect API rate limits

    logger.info("Completed fetching %d categories.", len(results))
    return results


# ---------------------------------------------------------------
# Main - Demo execution
# ---------------------------------------------------------------
if __name__ == "__main__":
    import json
    import os

    os.makedirs("logs", exist_ok=True)
    os.makedirs("data/raw", exist_ok=True)

    # Demo 1: FakeStore API
    logger.info("=" * 60)
    logger.info("Demo: FakeStore API Product Catalog")
    logger.info("=" * 60)
    fakestore = FakeStoreAPIClient()
    all_products = fakestore.get_all_products()
    with open("data/raw/fakestore_products.json", "w") as f:
        json.dump(all_products, f, indent=2)
    logger.info("Saved %d products to data/raw/fakestore_products.json", len(all_products))

    # Demo 2: Open Food Facts
    logger.info("=" * 60)
    logger.info("Demo: Open Food Facts Product Search")
    logger.info("=" * 60)
    food_client = OpenFoodFactsClient()
    results = food_client.search_products("organic coffee", page_size=10)
    logger.info("Open Food Facts returned %d results", results["count"])
