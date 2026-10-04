from pydantic import BaseModel, Field


class BenchmarkPackRequest(BaseModel):
    query: str = Field(..., description="User query for Benchmark Pack")
    context: dict | None = None


class BenchmarkPackResponse(BaseModel):
    result: str
    confidence: float = 0.0
    metadata: dict = Field(default_factory=dict)
