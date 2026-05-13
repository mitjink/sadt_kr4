from fastapi import FastAPI, HTTPException, status
from typing import List
from app.schemas import UserCreate, UserResponse, DeleteResponse

app = FastAPI()

fake_db: dict[int, dict] = {}
next_id = 1


def get_next_id() -> int:
    global next_id
    current = next_id
    next_id += 1
    return current


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    
    for existing in fake_db.values():
        if existing["username"] == user.username:
            raise HTTPException(status_code=400, detail=f"Username '{user.username}' already taken")
    
    user_id = get_next_id()
    fake_db[user_id] = {
        "id": user_id,
        "username": user.username,
        "age": user.age,
        "email": user.email
    }
    return UserResponse(**fake_db[user_id])


@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return UserResponse(**fake_db[user_id])


@app.delete("/users/{user_id}", response_model=DeleteResponse)
async def delete_user(user_id: int):
    
    if user_id not in fake_db:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    
    deleted = fake_db.pop(user_id)
    return DeleteResponse(message="User deleted", deleted_id=user_id)


@app.get("/users", response_model=List[UserResponse])
async def get_all_users():
    return list(fake_db.values())