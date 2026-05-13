from pydantic import BaseModel
from typing import Optional, List

class ProductResponse (BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool

class ErrorDetail(BaseModel):
    field: Optional[str] = None
    message: str
    error_code: str
    
class ErrorResponse(BaseModel):
    status_code: int
    error_type: str
    message: str
    details: List[ErrorDetail]
    timestamp: str