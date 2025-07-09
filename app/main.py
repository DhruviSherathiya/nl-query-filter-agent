from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any, Dict
from app.agent import parse_query

app = FastAPI()

class FilterRequest(BaseModel):
    query: str

class FilterResponse(BaseModel):
    success: bool
    message: str
    data: Dict[str, Any]

@app.get("/", response_model=dict)
def root():
    """
    Health check endpoint to verify the API is running.
    """
    return {"message": "FastAPI is running"}

@app.post("/filter-metadata", response_model=FilterResponse)
async def filter_endpoint(request: FilterRequest):
    """
    Generate a Pinecone metadata filter from a natural language query.
    
    - **query**: The natural language query to convert into a metadata filter.
    - **Returns**: A JSON object containing the filter, a success flag, and a message.
    """
    result = parse_query(request.query)
    return {
        "success": True,
        "message": "Metadata filter generated successfully.",
        "data": result
    }