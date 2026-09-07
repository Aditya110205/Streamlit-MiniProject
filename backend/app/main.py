from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.schemas import PipelineRequest, PipelineResponse
from app.services import analyze_pipeline


app = FastAPI(
    title="Pipeline Health Monitor API",
    version="1.0.0"
)


# Allow Streamlit frontend to communicate with API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Pipeline Health Monitor API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post(
    "/api/v1/analyze",
    response_model=PipelineResponse
)
def analyze_pipeline_health(
    data: PipelineRequest
):
    try:
        return analyze_pipeline(data)

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc)
        )