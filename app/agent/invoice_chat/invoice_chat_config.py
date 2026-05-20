from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)

DEFAULT_SYSTEM_PROMPT="""
You are an invoice reconciliation assistant.

Your job:
1. Read customer invoice complaints.
2. Use tools whenever needed.
3. Compare invoice data with contract data.
4. Explain discrepancies clearly.
5. Draft a professional email reply.

Rules:
- Always verify invoice details before responding.
- Always verify contract details before responding.
- If a tool returns an error, explain the issue politely.
- Keep responses concise and professional.
"""

system_prompt=DEFAULT_SYSTEM_PROMPT

current_file=Path(__file__)
agent_path=current_file.parent.parent
target=agent_path.parent/"prompts"/"invoice.md"

try:
    with open(target,"r") as f:
        system_prompt=f.read()
    logging.info("Loaded system prompt for invoice agent successfully.")
except FileNotFoundError:
    logging.warning("invoice.md not found. Using default system prompt.")

except Exception as e:
    logging.exception(f"Unexpected error while loading system prompt for the invoice: {e}")