def compute_shortfall(stock: int, dtc_monthly_velocity: int, requested_quantity: int) -> int:
    """Units short after reserving one month of DTC demand plus the wholesale request.

    stock_shortfall = max(0, (dtc_monthly_velocity + requested_quantity) - stock)
    """
    return max(0, (dtc_monthly_velocity + requested_quantity) - stock)
