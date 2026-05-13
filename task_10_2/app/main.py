from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from datetime import datetime

from app.schemas import (
    UserRegistration, 
    UserResponse, 
    ValidationErrorResponse, 
    ValidationErrorDetail
)

app = FastAPI()

fake_users_db = []
next_user_id = 1

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    formatted_errors = []
    for error in exc.errors():
        field = error["loc"][-1] if error["loc"] else "unknown"

        user_value = error.get("input", "N/A")
        
        formatted_errors.append(
            ValidationErrorDetail(
                field=str(field),
                value=str(user_value),
                message=error["msg"],
                error_type=error["type"]
            )
        )
    
    response = ValidationErrorResponse(
        status_code=422,
        error_type="VALIDATION_ERROR",
        message="Invalid input data. Please check your request.",
        errors=formatted_errors,
        timestamp=datetime.now().isoformat()
    )
    
    return JSONResponse(
        status_code=422,
        content=response.dict()
    )


@app.post(
    "/register/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Creates a new user with validation. Age must be > 18, email valid, password 8-16 chars."
)
async def register_user(user_data: UserRegistration):
    global next_user_id
    
    for existing_user in fake_users_db:
        if existing_user["username"] == user_data.username:
            from fastapi import HTTPException
            raise HTTPException(
                status_code=400,
                detail=f"Username '{user_data.username}' is already taken"
            )

    user_id = next_user_id
    fake_users_db.append({
        "id": user_id,
        "username": user_data.username,
        "email": user_data.email,
        "age": user_data.age,
        "phone": user_data.phone
    })
    next_user_id += 1
    
    return UserResponse(
        message="User registered successfully",
        user_id=user_id,
        username=user_data.username,
        email=user_data.email
    )