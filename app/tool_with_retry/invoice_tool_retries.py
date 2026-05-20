from app.tools.invoice import (
    get_invoice_details as get_invoice_details_base,
    get_client_contract as get_client_contract_base,
)

MAX_TOOL_RETRIES=2

def get_invoice_details(invoice_id:str) -> dict:
    ans="Unknown Error"
    for _ in range(MAX_TOOL_RETRIES):
        ans=get_invoice_details_base(invoice_id)
        if not isinstance(ans,str):
            return ans
    return {
        "STATUS": "FAILED",
        "ERROR": ans
    }


def get_client_contract(client_email:str) -> dict:
    ans="Unknown Error"
    for _ in range(MAX_TOOL_RETRIES):
        ans=get_client_contract_base(client_email)
        if not isinstance(ans,str):
            return ans
    return {
        "STATUS": "FAILED",
        "ERROR": ans
    }