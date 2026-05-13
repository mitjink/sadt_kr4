from pydantic import BaseModel, EmailStr, conint, constr, Field
from typing import Optional

class UserRegistration(BaseModel):
    username: str
    age: int = Field(gt=18)
    email: EmailStr
    password:  str = Field(min_length=8, max_length=16)
    phone: Optional[str] = "Unknown"
    
class UserResponse(BaseModel):
    message: str
    user_id: int
    username: str
    email: str
    
class ValidationErrorDetail(BaseModel):
    field: str
    value: str
    message: str
    error_type: str
    
class ValidationErrorResponse(BaseModel):
    status_code: int
    error_type: str
    message: str
    errors: list[ValidationErrorDetail]