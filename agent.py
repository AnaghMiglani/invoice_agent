from app.agent.invoice_chat.main import invoice_agent
from app.agent.guardrails.main import guardrail_llm

user_prompt="Hi, I am Daniel from Acme Corp. Why is invoice INV-100 for $500? We have overages waived on our Pro plan, My email is hello@acmecorp.com"

GUARDRAIL_MESSAGE="""
Your request has been flagged and could not be processed due to security or policy validation checks.

If you believe this was flagged in error, please contact the finance support team with your original request for manual review.

Best Regards,
iion automated finance team
"""

approve=guardrail_llm(user_prompt)
if not approve:
    print(GUARDRAIL_MESSAGE)
else:
    print(invoice_agent(user_prompt))