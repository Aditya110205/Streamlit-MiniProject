from pydantic import BaseModel, Field


class PipelineRequest(BaseModel):
    pipeline_name: str = Field(
        min_length=1,
        max_length=100
    )

    records_processed: int = Field(
        ge=0
    )

    failed_records: int = Field(
        ge=0
    )

    null_percentage: float = Field(
        ge=0,
        le=100
    )

    duplicate_percentage: float = Field(
        ge=0,
        le=100
    )

    processing_time: float = Field(
        ge=0
    )


class PipelineResponse(BaseModel):
    pipeline_name: str
    status: str
    success_rate: float
    quality_score: float
    processing_time: float
    recommendations: list[str]