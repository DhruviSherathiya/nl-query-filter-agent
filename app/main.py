from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.agent import parse_query

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