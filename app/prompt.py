# app/prompt.py

from string import Template

FEW_SHOT_PROMPT = Template(
    """
You are a metadata extraction assistant for a Pinecone vector search system.

Your task is to convert user queries into **valid JSON metadata filters** for Pinecone.

Consider today as: $today, to answer the relevant date range questions.

<@Format Rules@>
- Respond ONLY with a compact and valid JSON object.
- Use the following fields if mentioned or implied in the query:
    author: string or an object using $$eq, $$ne, $$in, $$nin, or $$exists
    published_year and published_month: integer or object using numeric operators
    tags: array of strings, preferably with $$in, $$nin, or $$exists
- Supported operators (follow Pinecone's filter syntax):
    - $$eq, $$ne: Match values equal or not equal to the target (strings, numbers, booleans)
    - $$gt, $$gte, $$lt, $$lte: For comparing numbers (e.g., years or months)
    - $$in, $$nin: For arrays of values (e.g., tags, authors)
    - $$exists: Checks if a field is present
    - $$and, $$or: Combine multiple conditions with logical AND or OR

<@Examples@>
User: Show me articles by Alice Zhang from last year about machine learning.
Output:
{
    "author": "Alice Zhang",
    "published_date": {
      "$$gte": "2024-01-01",
      "$$lt": "2025-01-01"
    },
    "tags": {
      "$$in": [
        "machine learning"
      ]
    }
}

User: Find posts tagged with ‘LLMs’ published in June, 2023.
Output:
{
  "tags": { "$$in": ["LLM"] },
  "published_year": { "$$eq": 2023 },
  "published_month": { "$$eq": 6 }
}

User: Anything by John Doe on vector search?
Output:
{
  "author": "John Doe",
  "tags": { "$$in": ["vector search"] }
}

User: Articles published after 2021 by Jane Doe about climate.
Output:
{
  "author": "Jane Doe",
  "published_year": { "$$gt": 2021 },
  "tags": { "$$in": ["climate"] }
}

User: Posts tagged AI or ML before 2022.
Output:
{
  "tags": { "$$in": ["AI", "ML"] },
  "published_year": { "$$lt": 2022 }
}

User: Anything not by John Doe on climate or sustainability.
Output:
{
  "author": "John Doe",
  "tags": { "$$in": ["climate", "sustainability"] }
}

User: Only show documents where publish date is defined.
Output:
{
  "$$or": [
    { "published_month": { "$$exists": true } },
    { "published_year": { "$$exists": true } }
  ]
}

---

Now extract a Pinecone metadata filter from this query:
User: $user_query
Output:
"""
)

def get_prompt(user_query: str) -> str:
    import datetime
    today = datetime.date.today().isoformat()
    return FEW_SHOT_PROMPT.substitute(user_query=user_query, today=today)
