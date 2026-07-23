import json
import os
import math

CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "production_config.json")

def estimate_production(quantity: int) -> dict:
    """Calculate lead time and cost estimates for producing a specified quantity of shortfall units.
    
    Args:
        quantity: The quantity needed to produce, e.g., 300.
        
    Returns:
        A dictionary containing production estimates:
        - quantity: the requested quantity
        - cost_per_unit: unit cost based on quantity pricing tier
        - total_cost: total production cost
        - lead_time_days: total lead time including setup and production
    """
    if quantity <= 0:
        raise ValueError(f"Quantity must be a positive integer. Got: {quantity}")

    if not os.path.exists(CONFIG_PATH):
        return {"error": "Production configuration not initialized."}

    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)

    production_rate = config["production_rate_units_per_day"]
    setup_lead_time = config["setup_lead_time_days"]
    cost_tiers = config["cost_tiers"]

    # Determine cost per unit based on tiers
    cost_per_unit = None
    for tier in cost_tiers:
        min_q = tier["min_quantity"]
        max_q = tier["max_quantity"]
        if quantity >= min_q and (max_q is None or quantity <= max_q):
            cost_per_unit = tier["cost_per_unit"]
            break

    if cost_per_unit is None:
        # Fallback to the last tier's price if not matched
        cost_per_unit = cost_tiers[-1]["cost_per_unit"]

    total_cost = quantity * cost_per_unit
    production_days = quantity / production_rate
    total_lead_time_days = math.ceil(setup_lead_time + production_days)

    return {
        "quantity": quantity,
        "cost_per_unit": cost_per_unit,
        "total_cost": total_cost,
        "lead_time_days": total_lead_time_days,
        "setup_lead_time_days": setup_lead_time,
        "production_days": production_days
    }
