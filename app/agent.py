import json

from app.client import MODEL_NAME, client
from app.prompt import get_prompt

def parse_query(nl_input: str) -> dict:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": get_prompt(nl_input)
            }
        ],
        response_format={"type": "json_object"},
        max_tokens=500,
    )
    content = response.choices[0].message.content
    if content is None:
        return {}
    return json.loads(content)
