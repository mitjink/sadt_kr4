from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    username: str
    age: int = Field(ge=18, description="Age must be 18 or older")
    email: str


class UserResponse(BaseModel):
    id: int
    username: str
    age: int
    email: str


class DeleteResponse(BaseModel):
    message: str
    deleted_id: int