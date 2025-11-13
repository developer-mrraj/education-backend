from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
import app.models.payment as payment_models
import app.schemas.payment as payment_schemas

router = APIRouter(
    prefix="/payments",
    tags=["Payments"]
)

# CREATE PAYMENT
@router.post("/", response_model=payment_schemas.PaymentResponse)
def create_payment(payment: payment_schemas.PaymentCreate, db: Session = Depends(get_db)):
    db_payment = payment_models.Payment(
        user_id=payment.user_id,
        test_id=payment.test_id,
        amount=payment.amount,
        payment_status=payment.payment_status,
        payment_mode=payment.payment_mode,
        transaction_id=payment.transaction_id
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

# GET PAYMENT BY ID
@router.get("/{payment_id}", response_model=payment_schemas.PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(payment_models.Payment).filter(payment_models.Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

# UPDATE PAYMENT
@router.put("/{payment_id}", response_model=payment_schemas.PaymentResponse)
def update_payment(payment_id: int, payment_update: payment_schemas.PaymentUpdate, db: Session = Depends(get_db)):
    payment = db.query(payment_models.Payment).filter(payment_models.Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    for field, value in payment_update.dict(exclude_unset=True).items():
        setattr(payment, field, value)
    db.commit()
    db.refresh(payment)
    return payment

# DELETE PAYMENT
@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(payment_models.Payment).filter(payment_models.Payment.payment_id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(payment)
    db.commit()
    return {"detail": f"Payment with id {payment_id} deleted successfully"}
