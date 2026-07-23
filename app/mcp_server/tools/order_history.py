import json
import os
import re

ORDERS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "mock_orders.json")

def lookup_order_history(company_id: str) -> list:
    """Look up order history for a specific company ID.
    
    Args:
        company_id: The unique ID of the company, e.g., COMP-001.
        
    Returns:
        A list of past orders for the given company.
    """
    if not re.match(r"^COMP-\d{3}$", company_id):
        raise ValueError(f"Invalid company ID format: '{company_id}'. Expected format is 'COMP-XXX' where X are digits.")

    if not os.path.exists(ORDERS_PATH):
        return []

    with open(ORDERS_PATH, "r") as f:
        orders = json.load(f)

    return [o for o in orders if o["company_id"] == company_id]


def get_dtc_monthly_velocity(product_id: str) -> dict:
    """Get the recent direct-to-consumer (DTC) monthly order velocity for a product.
    
    Args:
        product_id: The unique product identifier, e.g., PROD-A.
        
    Returns:
        A dictionary with the product ID and the monthly DTC velocity.
    """
    if not re.match(r"^PROD-[A-Z]$", product_id):
        raise ValueError(f"Invalid product ID format: '{product_id}'. Expected format is 'PROD-X' where X is a letter.")
        
    inventory_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "mock_inventory.json")
    if not os.path.exists(inventory_path):
        return {"product_id": product_id, "dtc_monthly_velocity": 0}

    with open(inventory_path, "r") as f:
        inventory = json.load(f)

    for item in inventory:
        if item["product_id"] == product_id:
            return {
                "product_id": product_id,
                "dtc_monthly_velocity": item["dtc_monthly_velocity"]
            }

    return {"product_id": product_id, "dtc_monthly_velocity": 0}
