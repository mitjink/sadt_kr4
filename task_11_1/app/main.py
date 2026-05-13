from fastapi import FastAPI, HTTPException, status
from typing import Dict, List
from app.schemas import UserCreate, UserResponse, DeleteResponse

app = FastAPI()

fake_db: Dict[int, dict] = {}
next_id = 1


def get_next_id() -> int:
    global next_id
    current = next_id
    next_id += 1
    return current

@app.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Creates a user and returns the created user with ID"
)
async def create_user(user: UserCreate):
    for existing_user in fake_db.values():
        if existing_user["username"] == user.username:
            raise HTTPException(
                status_code=400,
                detail=f"Username '{user.username}' is already taken"
            )
    
    user_id = get_next_id()
    fake_db[user_id] = {
        "id": user_id,
        "username": user.username,
        "age": user.age,
        "email": user.email
    }
    
    return UserResponse(**fake_db[user_id])

@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Returns user data if found"
)
async def get_user(user_id: int):
    
    if user_id not in fake_db:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} not found"
        )
    
    return UserResponse(**fake_db[user_id])

@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete user by ID",
    description="Removes user from the database"
)
async def delete_user(user_id: int):
    
    if user_id not in fake_db:
        raise HTTPException(
            status_code=404,
            detail=f"User with id {user_id} not found"
        )
    
    deleted_user = fake_db.pop(user_id)
    
    return DeleteResponse(
        message="User deleted successfully",
        deleted_id=user_id
    )

@app.get(
    "/users",
    response_model=List[UserResponse],
    summary="Get all users",
    description="Returns list of all users"
)
async def get_all_users():
    return list(fake_db.values())