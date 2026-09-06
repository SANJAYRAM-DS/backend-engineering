from typing import Generic, TypeVar, Optional, Any, List
from pydantic import BaseModel, Field

DataT = TypeVar("DataT")

class ErrorDetail(BaseModel):
    field: Optional[str] = None
    issue: str

class ErrorPayload(BaseModel):
    code: str
    message: str
    details: List[ErrorDetail] = Field(default_factory=list)

class ErrorEnvelope(BaseModel):
    success: bool = False
    error: ErrorPayload

class SuccessEnvelope(BaseModel, Generic[DataT]):
    success: bool = True
    data: DataT
    meta: Optional[dict[str, Any]] = None
