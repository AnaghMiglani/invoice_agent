tools=[
    {
        "type": "function",
        "function": {
            "name": "get_invoice_details",
            "description": "Fetch invoice details using invoice ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "invoice_id": {
                        "type": "string",
                        "description": "Invoice ID like INV-100"
                    }
                },
                "required": ["invoice_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_client_contract",
            "description": "Fetch client contract details using client email",
            "parameters": {
                "type": "object",
                "properties": {
                    "client_email": {
                        "type": "string",
                        "description": "Client email address"
                    }
                },
                "required": ["client_email"]
            }
        }
    }
]