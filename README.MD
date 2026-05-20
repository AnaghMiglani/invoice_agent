# Invoice Reconciliation Agent

## How To Run
### Setup .env file (refer sample.env)

### Python setup
```bash
py -3.12 -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Run The Agent

```bash
py agent.py
```

## Overview

This project implements an AI-powered Invoice Reconciliation Agent designed to automate finance support workflows for invoice discrepancy emails.

The system uses an LLM-powered agent with tool calling capabilities to:
- Analyze billing concerns
- Retrieve invoice details
- Verify customer contract information
- Compare invoice data against contract terms
- Draft professional customer-facing responses
- Prevent malicious or unrelated requests using a guardrail layer
## Features

### Guardrail Layer

The application includes a dedicated guardrail agent that validates whether a user request is safe and relevant before passing it to the invoice reconciliation agent.

The guardrail:
- Detects prompt injection attempts
- Blocks malicious or unrelated requests
- Allows legitimate invoice and billing conversations
- Returns a boolean-style decision
- Returns a safe automated reply if flagged

Location:

```txt
app/agent/guardrails/
```

The system prompt is stored in:

```txt
prompts/guardrail.md
```

A fallback prompt is also configured internally in case the markdown file is missing.

---

### Invoice Reconciliation Agent

The invoice reconciliation agent:
- Handles invoice discrepancy requests
- Uses tool calling to fetch invoice and contract information
- Verifies ownership and matching customer records
- Drafts professional customer-facing responses
- Prevents exposure of internal data

Location:

```txt
app/agent/invoice_chat/
```

The system prompt is stored in:

```txt
prompts/invoice.md
```

A fallback prompt is also configured internally.

---

## Tool Calling Architecture

The project uses the mock tools provided in the assessment:

```python
get_invoice_details(invoice_id: str)

get_client_contract(client_email: str)
```

Located inside:

```txt
app/tools/
```

### Retry Handling

Retry wrappers were implemented separately inside:

```txt
app/tool_with_retry/
```

This allows retries to be configured without modifying the original tools.

Features:
- Each tool retries internally up to 2 times
- Controlled fallback response if both attempts fail
- Individual tool call limits using a limit dictionary
- Maximum LLM loop limit of 5 iterations to prevent infinite loops

---

## Prompt Design

### Guardrail Prompt Summary

The guardrail prompt acts as a security and relevance validation layer.

It:
- Allows normal billing conversations
- Blocks prompt injection attempts
- Blocks malicious or unrelated requests
- Prevents access to internal system information

Examples of blocked requests:
- "Ignore previous instructions"
- "Reveal your system prompt"
- "Help me fake an invoice"

The guardrail focuses on user intent rather than keyword matching to reduce false positives.

---

### Invoice Agent Prompt Summary

The invoice prompt enforces:
- Structured workflow execution
- Secure tool usage
- Professional communication
- Data privacy

Workflow:
1. Read customer email
2. Identify invoice ID and dispute reason
3. Fetch invoice information
4. Fetch contract information
5. Compare both datasets
6. Draft a professional response

The prompt also enforces:
- Retry handling
- Customer verification checks
- No internal data leakage
- No hallucination when tools fail

Every customer-facing email ends with:

```txt
Best Regards,
iion automated finance agent
```
## Updated User Input

The original assessment prompt was updated from:

```txt
Hi, I am Daniel from Acme Corp. Why is invoice INV-100 for $500? We have overages waived on our Pro plan.
```

to:

```txt
Hi, I am Daniel from Acme Corp. Why is invoice INV-100 for $500? We have overages waived on our Pro plan, My email is hello@acmecorp.com
```

This change was necessary because the contract lookup tool requires an email argument.

If email is missing, the agent requests it before proceeding.

---

## Design Decisions

### Why Separate Guardrails?

Separating guardrails improves:
- Security
- Maintainability
- Prompt clarity
- Reusability


### Why Separate Retry Logic?

Retry logic was abstracted into:

```txt
tool_with_retry/
```

This keeps the original tools (provided ones) unchanged while allowing centralized retry handling.


### Why Use Execution Limits?

Execution limits prevent:
- Infinite loops
- Excessive token usage
- Repeated failing calls

Tool calls which can be made by invoice agent were also limited using "limit" dictionary.
To prevent agent from calling same tool again and again, especially when tool keep failing

## Invalid Invoice-ID Handling & Guardrail Handling

The project also includes handling for a few edge cases:

- Invalid or non-existing invoice IDs
- Prompt injection / malicious guardrail checks

### Invalid Invoice-ID Handling

<p align="center">
  <img src="./assets/screenshots/INV-200.png" alt="Invalid Invoice ID Handling" width="750">
</p>

### Guardrail Handling

<p align="center">
  <img src="./assets/screenshots/guardrail_check.png" alt="Guardrail Handling" width="750">
</p>

## If Given More Time

- Add a seperate validator layer to verify that generated emails are professional, safe, properly formatted, and do not expose internal data.
- Expose the `agent.py` logic through async FastAPI routes for webhook-based integration with mail platforms and automated replies.
- Add temporary rate-limiting, moderation tools, and a human-in-the-loop review system to prevent repeated malicious requests, reduce unnecessary token usage, and allow manual warning/muting decisions for flagged users.