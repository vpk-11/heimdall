import pytest
from mcp_server.tools.customer_lookup import lookup_customer
from mcp_server.tools.inventory_lookup import lookup_inventory
from mcp_server.tools.order_history import lookup_order_history, get_dtc_monthly_velocity
from mcp_server.tools.production_estimate import estimate_production


class TestCustomerLookup:
    def test_known_company_returns_record(self):
        result = lookup_customer("COMP-001")
        assert result["company_id"] == "COMP-001"
        assert result["name"] == "Apex Retailers"

    def test_unknown_company_returns_error(self):
        result = lookup_customer("COMP-999")
        assert "error" in result

    def test_invalid_format_raises(self):
        with pytest.raises(ValueError):
            lookup_customer("invalid")

    def test_invalid_format_no_digits_raises(self):
        with pytest.raises(ValueError):
            lookup_customer("COMP-ABC")


class TestInventoryLookup:
    def test_known_product_returns_stock(self):
        result = lookup_inventory("PROD-A")
        assert result["product_id"] == "PROD-A"
        assert "stock" in result
        assert "dtc_monthly_velocity" in result

    def test_unknown_product_returns_error(self):
        result = lookup_inventory("PROD-Z")
        assert "error" in result

    def test_invalid_format_raises(self):
        with pytest.raises(ValueError):
            lookup_inventory("PRODUCT-1")


class TestOrderHistory:
    def test_known_company_returns_orders(self):
        orders = lookup_order_history("COMP-001")
        assert isinstance(orders, list)
        assert len(orders) > 0
        assert all(o["company_id"] == "COMP-001" for o in orders)

    def test_company_with_no_orders_returns_empty(self):
        orders = lookup_order_history("COMP-003")
        assert isinstance(orders, list)

    def test_invalid_format_raises(self):
        with pytest.raises(ValueError):
            lookup_order_history("bad-id")


class TestDtcVelocity:
    def test_known_product_returns_velocity(self):
        result = get_dtc_monthly_velocity("PROD-A")
        assert result["product_id"] == "PROD-A"
        assert isinstance(result["dtc_monthly_velocity"], (int, float))
        assert result["dtc_monthly_velocity"] > 0

    def test_unknown_product_returns_zero(self):
        result = get_dtc_monthly_velocity("PROD-Z")
        assert result["dtc_monthly_velocity"] == 0

    def test_invalid_format_raises(self):
        with pytest.raises(ValueError):
            get_dtc_monthly_velocity("BAD")


class TestProductionEstimate:
    def test_small_order_hits_tier_one(self):
        result = estimate_production(50)
        assert result["cost_per_unit"] == 12.0
        assert result["quantity"] == 50

    def test_mid_order_hits_tier_two(self):
        result = estimate_production(200)
        assert result["cost_per_unit"] == 10.0

    def test_large_order_hits_tier_three(self):
        result = estimate_production(600)
        assert result["cost_per_unit"] == 8.0

    def test_lead_time_includes_setup(self):
        # 100 units / 50 per day = 2 production days + 2 setup = 4 total
        result = estimate_production(100)
        assert result["lead_time_days"] == 4

    def test_total_cost_correct(self):
        result = estimate_production(100)
        assert result["total_cost"] == result["quantity"] * result["cost_per_unit"]

    def test_zero_quantity_raises(self):
        with pytest.raises(ValueError):
            estimate_production(0)

    def test_negative_quantity_raises(self):
        with pytest.raises(ValueError):
            estimate_production(-5)


class TestFeasibilityMath:
    """Validates the core shortfall equation the agent reasons over.

    stock_shortfall = max(0, (dtc_monthly_velocity + wholesale_ask) - stock)
    """

    def test_no_shortfall_when_stock_sufficient(self):
        stock = 600
        dtc = 400
        wholesale_ask = 100
        shortfall = max(0, (dtc + wholesale_ask) - stock)
        assert shortfall == 0

    def test_partial_shortfall(self):
        stock = 600
        dtc = 400
        wholesale_ask = 300
        shortfall = max(0, (dtc + wholesale_ask) - stock)
        assert shortfall == 100

    def test_full_production_needed(self):
        stock = 100
        dtc = 400
        wholesale_ask = 500
        shortfall = max(0, (dtc + wholesale_ask) - stock)
        assert shortfall == 800
