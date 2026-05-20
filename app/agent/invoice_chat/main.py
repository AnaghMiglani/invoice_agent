import pprint
from groq import Groq
import dotenv
import os
import json

import logging
logging.basicConfig(level=logging.INFO)

from app.agent.invoice_chat.invoice_chat_config import system_prompt
from app.tool_with_retry.invoice_tool_retries import get_invoice_details,get_client_contract
from app.agent.invoice_chat.function_tools import tools
# from groq.types.chat import (
#     ChatCompletionSystemMessageParam,
#     ChatCompletionUserMessageParam,
#     ChatCompletionAssistantMessageParam,
#     ChatCompletionToolMessageParam
# )

def invoice_agent(user_prompt:str):
    # USER_PROMPT="Hi, I am Daniel from Acme Corp. Why is invoice INV-100 for $500? We have overages waived on our Pro plan, My email is hello@acmecorp.com"
    #added user's email as get_client_contract tool expects it, if no email provided :- asks for email to confirm

    limit={ #maximum tool calls allowed (default 2)
        "get_invoice_details": 2,
        "get_client_contract": 2,
    }

    current={ #current number of tool calls
        "get_invoice_details": 0,
        "get_client_contract": 0,
    }

    dotenv.load_dotenv()

    client=Groq(
        api_key=os.getenv("GROQ_API_KEY"),
        max_retries=2,
    )

    MODEL_NAME="openai/gpt-oss-120b"

    available_functions={
        "get_invoice_details": get_invoice_details,
        "get_client_contract": get_client_contract
    }

    messages=[
        {
            "role": "system",
            "content": system_prompt,
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]

    MAX_ITERATIONS=5

    for iteration in range(MAX_ITERATIONS):
        resp=client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.2
        )
        message=resp.choices[0].message
        # pprint.pprint(message)
        messages.append(message)

        if not message.tool_calls:
            return (message.content)
            break

        for tool_call in message.tool_calls:

            function_name=tool_call.function.name
            function_args=json.loads(tool_call.function.arguments)

            try:
                if current.get(function_name): #count of how many times current function has been called
                    current[function_name]+=1
                else:
                    current[function_name]=1

                function_limit=limit.get(function_name)
                if not function_limit:
                    function_limit=2 #setting limit of tool call to 2 (default)

                if current[function_name] >= function_limit:
                    logging.exception("Exceeded tool call limit")
                    return """
                    Thank you for contacting us, we will contact you soon!
                    Best Regards,
                    iion automated finance agent
                    """

                function_to_call=available_functions[function_name]
                function_response=function_to_call(**function_args)

            except Exception as e:
                function_response={
                    "error": str(e)
                }

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": json.dumps(function_response)
            })
    return """
        Thank you for contacting us, we will contact you soon!
        Best Regards,
        iion automated finance agent
        """