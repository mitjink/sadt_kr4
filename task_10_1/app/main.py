from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from datetime import datetime

from app.schemas import ProductResponse, ErrorDetail, ErrorResponse
from app.exceptions import ItemNotFoundException, OutOfStockException

app = FastAPI()

products_db = {
    1: {"id": 1, "name": "Ноутбук", "price": 50000, "in_stock": True},
    2: {"id": 2, "name": "Наушники", "price": 4500, "in_stock": True},
    3: {"id": 3, "name": "Клавиатура", "price": 3000, "in_stock": False},  # нет в наличии
}

@app.exception_handler(ItemNotFoundException)
async def handle_item_not_found(request: Request, exc: ItemNotFoundException):
    error_response = ErrorResponse(
        status_code=exc.status_code,
        error_type=exc.error_type,
        message="The requested product could not be found",
        details=[
            ErrorDetail(
                field="item_id",
                message=exc.detail,
                error_code="NOT_FOUND"
            )
        ],
        timestamp=datetime.now().isoformat()
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict()
    )
    
@app.exception_handler(OutOfStockException)
async def handle_out_of_stock(request: Request, exc: OutOfStockException):
    error_response = ErrorResponse(
        status_code=exc.status_code,
        error_type=exc.error_type,
        message="Product is not available for purchase",
        details=[
            ErrorDetail(
                field="quantity",
                message=f"Requested: {exc.requested}, Available: {exc.available}",
                error_code="OUT_OF_STOCK"
            ),
            ErrorDetail(
                field="item_id",
                message=f"Product ID {exc.item_id} has insufficient stock",
                error_code="INSUFFICIENT_STOCK"
            )
        ],
        timestamp=datetime.now().isoformat()
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content=error_response.dict()
    )
    
@app.get("/products/{item_id}", response_model=ProductResponse)
async def get_product(item_id: int):
    if item_id not in products_db:
        raise ItemNotFoundException(item_id=item_id)
    product = products_db[item_id]
    return ProductResponse(**product)

@app.post("/products/{item_id}/order")
async def order_product(item_id: int, quantity: int = 1):
    if item_id not in products_db:
        raise ItemNotFoundException(item_id=item_id)
    product = products_db[item_id]
    if not product["in_stock"]:
        raise OutOfStockException(
            item_id=item_id,
            requested=quantity,
            available=0
        )
    return {"message": f"Ordered {quantity} of {product['name']}", "status": "success"}

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    error_response = ErrorResponse(
        status_code=500,
        error_type="INTERNAL_SERVER_ERROR",
        message="An unexpected error occurred. Please try again later.",
        details=[
            ErrorDetail(
                field=None,
                message=str(exc) if app.debug else "Internal server error",
                error_code="INTERNAL_ERROR"
            )
        ],
        timestamp=datetime.now().isoformat()
    )
    return JSONResponse(
        status_code=500,
        content=error_response.dict()
    )