from pydantic import BaseModel,Field
from typing import List,Any,Dict


## Query Request

class QueryRequest(BaseModel):
    question: str = Field(..., example="What is refund policy")
    user_id: str = Field(..., example="Amit_123")

## Response schema for query

class QueryResponse(BaseModel):
    status:str
    messages:dict


## Response schema for file upload

class UploadResponse(BaseModel):
    status:str
    messages:str
    