import json
import re

COMPANY_ID_PATTERN = re.compile(r"^COMP-\d{3}$")
PRODUCT_ID_PATTERN = re.compile(r"^PROD-[A-Z]$")


def load_json(path: str):
    """Loads a JSON fixture file. Shared by every tool reading app/mcp_server/data/*.json."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_company_id(company_id: str) -> None:
    if not COMPANY_ID_PATTERN.match(company_id):
        raise ValueError(
            f"Invalid company ID format: '{company_id}'. Expected format is 'COMP-XXX' where X are digits."
        )


def validate_product_id(product_id: str) -> None:
    if not PRODUCT_ID_PATTERN.match(product_id):
        raise ValueError(
            f"Invalid product ID format: '{product_id}'. Expected format is 'PROD-X' where X is a letter."
        )
