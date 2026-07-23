import json
import os
import re

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "mock_customers.json")

def lookup_customer(company_id: str) -> dict:
    """Look up a B2B customer in the mock CRM.
    
    Args:
        company_id: The unique ID of the company, e.g., COMP-001.
        
    Returns:
        A dictionary containing company information, or an error dictionary.
    """
    if not re.match(r"^COMP-\d{3}$", company_id):
        raise ValueError(f"Invalid company ID format: '{company_id}'. Expected format is 'COMP-XXX' where X are digits.")
        
    if not os.path.exists(DATA_PATH):
        return {"error": "Database not initialized."}
        
    with open(DATA_PATH, "r") as f:
        customers = json.load(f)
        
    for customer in customers:
        if customer["company_id"] == company_id:
            return customer
            
    return {"error": f"Company ID '{company_id}' not found."}
