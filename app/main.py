import os

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.agent import parse_query
from app.eval_pipeline import load_dataset, evaluate

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI is running"}

@app.post("/filter-metadata")
async def filter_endpoint(request: Request):
    data = await request.json()
    nl_query = data.get("query", "")
    result = parse_query(nl_query)
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": "Metadata filter generated successfully.",
            "data": result
        }
    )

@app.get("/run-eval")
def run_eval():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(base_dir, "data/synthetic_eval_data.json")
    dataset = load_dataset(dataset_path)
    results = evaluate(dataset)
    return JSONResponse(content=results)