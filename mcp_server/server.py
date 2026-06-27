import os
import sys

# When run as a subprocess via StdioConnectionParams, sys.path won't include the
# project root. Insert it so mcp_server.tools.* imports resolve correctly.
_project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from mcp.server.fastmcp import FastMCP
from mcp_server.tools.customer_lookup import lookup_customer
from mcp_server.tools.order_history import lookup_order_history, get_dtc_monthly_velocity
from mcp_server.tools.inventory_lookup import lookup_inventory
from mcp_server.tools.production_estimate import estimate_production

mcp = FastMCP("HeimdallServer")

@mcp.tool()
def customer_lookup(company_id: str) -> dict:
    """Look up a B2B customer in the CRM by their company ID (COMP-XXX format).
    
    Args:
        company_id: The unique ID of the company, e.g., COMP-001.
    """
    return lookup_customer(company_id)

@mcp.tool()
def order_history(company_id: str) -> list:
    """Retrieve B2B order history for a customer.
    
    Args:
        company_id: The unique ID of the company, e.g., COMP-001.
    """
    return lookup_order_history(company_id)

@mcp.tool()
def dtc_monthly_velocity(product_id: str) -> dict:
    """Retrieve the recent monthly direct-to-consumer (DTC) velocity for a product.
    
    Args:
        product_id: The unique product identifier, e.g., PROD-A.
    """
    return get_dtc_monthly_velocity(product_id)

@mcp.tool()
def inventory_lookup(product_id: str) -> dict:
    """Look up current stock levels and details for a product.
    
    Args:
        product_id: The unique product identifier, e.g., PROD-A.
    """
    return lookup_inventory(product_id)

@mcp.tool()
def production_estimate(quantity: int) -> dict:
    """Estimate lead time and pricing tiers for producing a given unit shortfall quantity.
    
    Args:
        quantity: The quantity needed to produce.
    """
    return estimate_production(quantity)

if __name__ == "__main__":
    mcp.run()
