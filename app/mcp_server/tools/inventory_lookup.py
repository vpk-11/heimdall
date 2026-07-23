import json
import os
import re

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "mock_inventory.json")

def lookup_inventory(product_id: str) -> dict:
    """Look up current stock level and details for a given product.
    
    Args:
        product_id: The unique product identifier, e.g., PROD-A.
        
    Returns:
        A dictionary containing inventory details, or an error dictionary.
    """
    if not re.match(r"^PROD-[A-Z]$", product_id):
        raise ValueError(f"Invalid product ID format: '{product_id}'. Expected format is 'PROD-X' where X is a letter.")

    if not os.path.exists(DATA_PATH):
        return {"error": "Inventory database not initialized."}

    with open(DATA_PATH, "r") as f:
        inventory = json.load(f)

    for item in inventory:
        if item["product_id"] == product_id:
            return item

    return {"error": f"Product '{product_id}' not found."}
