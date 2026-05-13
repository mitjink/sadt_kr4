from fastapi import HTTPException

class ItemNotFoundException(HTTPException):
    def __init__(self, item_id: int):
        super().__init__(
            status_code=404,
            detail=f"Item with id {item_id} not found"
        )
        
        self.item_id = item_id
        self.error_type = "ITEM_NOT_FOUND"
        
class OutOfStockException(HTTPException):
    def __init__(self, item_id: int, requested: int, available: int):
        detail_message = f"Item {item_id} is put of stock. Requested: {requested}, Available: {available}"
        super().__init__(
            status_code=400,
            detail=detail_message
        )
        
        self.item_id = item_id
        self.requested = requested
        self.available = available
        self.error_type = "OUT_OF_STOCK"
        