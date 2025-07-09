import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Any, Dict, List
from app.agent import parse_query
from app.eval_pipeline import load_dataset, evaluate

app = FastAPI()

class FilterRequest(BaseModel):
    query: str

class FilterResponse(BaseModel):
    success: bool
    message: str
    data: Dict[str, Any]

class FailureCase(BaseModel):
    query: str
    expected: Dict[str, Any]
    predicted: Dict[str, Any]

class EvalResult(BaseModel):
    total: int
    fuzzy: int
    failed: int
    failures: List[FailureCase]

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

@app.get("/run-eval", response_model=EvalResult, tags=["Evaluation"])
def run_eval():
    """
    Run the evaluation pipeline on the synthetic eval dataset.
    Returns a summary of exact, fuzzy, and failed matches, along with sample failed cases.
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, "data/synthetic_eval_data.json")
    dataset = load_dataset(dataset_path)
    results = evaluate(dataset)
    return results