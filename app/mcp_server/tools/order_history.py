import os

from app.mcp_server.tools._shared import load_json, validate_company_id
from app.mcp_server.tools.inventory_lookup import lookup_inventory

ORDERS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "mock_orders.json")

def lookup_order_history(company_id: str) -> list:
    """Look up order history for a specific company ID.

    Args:
        company_id: The unique ID of the company, e.g., COMP-001.

    Returns:
        A list of past orders for the given company.
    """
    validate_company_id(company_id)

    if not os.path.exists(ORDERS_PATH):
        return []

    orders = load_json(ORDERS_PATH)

    return [o for o in orders if o["company_id"] == company_id]


def get_dtc_monthly_velocity(product_id: str) -> dict:
    """Get the recent direct-to-consumer (DTC) monthly order velocity for a product.

    Args:
        product_id: The unique product identifier, e.g., PROD-A.

    Returns:
        A dictionary with the product ID and the monthly DTC velocity.
    """
    item = lookup_inventory(product_id)
    if "error" in item:
        return {"product_id": product_id, "dtc_monthly_velocity": 0}

    return {
        "product_id": product_id,
        "dtc_monthly_velocity": item["dtc_monthly_velocity"]
    }
