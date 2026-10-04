from pydantic import BaseModel, Field


class SynthesizedPackRequest(BaseModel):
    query: str = Field(..., description="User query for Synthesized Pack")
    context: dict | None = None


class SynthesizedPackResponse(BaseModel):
    result: str
    confidence: float = 0.0
    metadata: dict = Field(default_factory=dict)
