from app.agent.invoice_chat.main import invoice_agent
from app.agent.guardrails.main import guardrail_llm
import json

user_prompt="Hi, I am Daniel from Acme Corp. Why is invoice INV-100 for $500? We have overages waived on our Pro plan, My email is hello@acmecorp.com"

GUARDRAIL_MESSAGE="""
Your request has been flagged and could not be processed due to security or policy validation checks.

If you believe this was flagged in error, please contact the finance support team with your original request for manual review.

Best Regards,
iion automated finance team
"""
reply=GUARDRAIL_MESSAGE
run_info={}
raw_run_info={}

raw_run_info["USER_PROMPT"]=user_prompt
run_info["USER_PROMPT"]=user_prompt
print("USER PROMPT: ",user_prompt)

approve=guardrail_llm(user_prompt,raw_run_info)

if not approve:
    print(GUARDRAIL_MESSAGE)
else:
    reply=invoice_agent(user_prompt,raw_run_info)
    print(reply)

raw_run_info["Final Message"]=reply
# print(raw_run_info)
with open("raw_message_history.json","w") as f:
    json.dump(raw_run_info, f, indent=4, default=str)
