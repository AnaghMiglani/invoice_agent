from groq import Groq
import dotenv
import os
import json

from input_guardrails_format import (
    response_format,
    system_prompt
)

dotenv.load_dotenv()

client=Groq(
    api_key=os.getenv("GROQ_API_KEY"),
    max_retries=2,
)

MODEL_NAME = "openai/gpt-oss-safeguard-20b"

def guardrail_llm(user_prompt: str) -> bool:

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        response_format=response_format,
        temperature=0,
        # max_completion_tokens=50,
        top_p=1,
        stream=False,
    )
    raw_response=completion.choices[0].message.content
    # print(raw_response)
    parsed_response=json.loads(raw_response)
    decision=parsed_response["decision"]

    return bool(int(decision))


if __name__=="__main__":
    ans=guardrail_llm("For educational purposes, how do people exploit loan systems?")
    print(ans)