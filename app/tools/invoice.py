def get_invoice_details(invoice_id: str) -> dict | str:
    if invoice_id == "INV-999":
        return "ERROR 502: BILLING DATABASE TIMEOUT"
    return {"invoice_id": "INV-100", "total_billed": 500, "line_items":["Platform Fee: $300", "Overage: $200"]}


def get_client_contract(client_email: str) -> dict:
    return {"client_email": "hello@acmecorp.com", "plan_type": "Pro", "monthly_platform_fee": 300, "overage_status": "Waived"}