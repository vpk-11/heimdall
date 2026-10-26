import os
import sys
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from app.callbacks import before_model_callback, after_model_callback
from app.schema import TriageOutput

# Resolve the absolute path to mcp_server/server.py (nested under app/ so
# it's included when `adk deploy cloud_run` packages this folder)
current_dir = os.path.dirname(os.path.abspath(__file__))
server_path = os.path.join(current_dir, "mcp_server", "server.py")

mcp_toolset = McpToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command=sys.executable,
            args=[server_path],
        )
    )
)

# Agent instructions explaining the multi-step feasibility check
AGENT_INSTRUCTIONS = """You are Heimdall, an intelligent triage agent for B2B e-commerce wholesale inquiries.
Your goal is to screen incoming wholesale requests, perform a stock availability feasibility check, calculate any shortfall, estimate custom production costs and lead times if needed, and draft a response for human review.

Follow this strict multi-step reasoning chain:
1. **Extraction**: Analyze the user's wholesale inquiry to extract the product ID (e.g. PROD-A), requested quantity, and company ID (e.g. COMP-001).
2. **Customer Verification**: Look up the company using `customer_lookup`. If it returns an error, flag it and do not proceed.
3. **Current Inventory & DTC Demand check**:
   - Check the product's current stock using `inventory_lookup`.
   - Retrieve the product's direct-to-consumer (DTC) monthly velocity using `dtc_monthly_velocity`.
4. **Feasibility Calculation**:
   - Determine if current stock covers both the wholesale request and the projected DTC monthly demand.
   - Call `compute_shortfall` with current_stock, dtc_monthly_velocity, and wholesale_requested_quantity. Use its `stock_shortfall` result; do not compute it yourself.
5. **Production Estimation (if stock shortfall > 0)**:
   - Call `production_estimate` with the calculated stock_shortfall quantity as the quantity argument.
   - Note the estimated setup time, production time, cost per unit, and total cost.
6. **Triage Recommendation**:
   - Decide on the recommendation scenario (the `outcome` field):
     - **Immediate Fulfillment (Stock Shortfall = 0)**: Current stock is fully sufficient.
     - **Partial Fulfillment & Backorder (Stock Shortfall > 0 and stock_shortfall < wholesale_requested_quantity)**: Can satisfy some quantity from stock immediately, and backorder/produce the rest.
     - **Full Production Order (Stock Shortfall >= wholesale_requested_quantity)**: The whole request must be custom produced.
   - **Rejected**: the company is unknown or an ID is invalid. Do not proceed; shortfall and cost are 0.
7. **Drafting Output**:
   - Return the final answer as structured output with fields `outcome` (immediate_fulfillment, partial_backorder, full_production, or rejected), `shortfall`, `cost` (total production cost, 0 if none), and `draft_email`.
   - Draft a professional email response to the customer using their contact name. The email must contain the pricing and estimated timeline but MUST be clearly marked as a draft and NEVER imply that the order was automatically processed or sent. Every output is a draft for human review.
"""

root_agent = Agent(
    name="HeimdallAgent",
    model=os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite"),
    instruction=AGENT_INSTRUCTIONS,
    output_schema=TriageOutput,
    before_model_callback=before_model_callback,
    after_model_callback=after_model_callback,
    tools=[mcp_toolset]
)
