import os

from app.mcp_server.tools._shared import load_json, validate_company_id

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "mock_customers.json")

def lookup_customer(company_id: str) -> dict:
    """Look up a B2B customer in the mock CRM.

    Args:
        company_id: The unique ID of the company, e.g., COMP-001.

    Returns:
        A dictionary containing company information, or an error dictionary.
    """
    validate_company_id(company_id)

    if not os.path.exists(DATA_PATH):
        return {"error": "Database not initialized."}

    customers = load_json(DATA_PATH)

    for customer in customers:
        if customer["company_id"] == company_id:
            return customer

    return {"error": f"Company ID '{company_id}' not found."}
