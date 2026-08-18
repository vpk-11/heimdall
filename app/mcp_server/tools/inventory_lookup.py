import os

from app.mcp_server.tools._shared import load_json, validate_product_id

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "mock_inventory.json")

def lookup_inventory(product_id: str) -> dict:
    """Look up current stock level and details for a given product.

    Args:
        product_id: The unique product identifier, e.g., PROD-A.

    Returns:
        A dictionary containing inventory details, or an error dictionary.
    """
    validate_product_id(product_id)

    if not os.path.exists(DATA_PATH):
        return {"error": "Inventory database not initialized."}

    inventory = load_json(DATA_PATH)

    for item in inventory:
        if item["product_id"] == product_id:
            return item

    return {"error": f"Product '{product_id}' not found."}
