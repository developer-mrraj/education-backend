from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# --- Create Payment ---
class PaymentCreate(BaseModel):
    user_id: int
    test_id: int
    amount: float
    payment_mode: str
    transaction_id: str
    payment_status: Optional[str] = "Pending" 

# --- Update Payment ---
class PaymentUpdate(BaseModel):
    user_id: Optional[int] = None
    test_id: Optional[int] = None
    amount: Optional[float] = None
    payment_status: Optional[str] = None  # e.g., "success", "failed"
    payment_mode: Optional[str] = None
    transaction_id: Optional[str] = None

# --- Response Schema ---
class PaymentResponse(BaseModel):
    payment_id: int
    user_id: int
    test_id: int
    amount: float
    payment_status: str
    payment_mode: str
    transaction_id: str
    created_at: datetime

    class Config:
        orm_mode = True
