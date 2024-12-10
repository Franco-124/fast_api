from models import Customer, Transaction
from fastapi import APIRouter,HTTPException, Query, status
from models import Transaction, TransactionCreate
from db import SessionDep
from sqlmodel import select
router = APIRouter()

@router.post('/transactions',status_code=status.HTTP_201_CREATED, tags=["transactions"])
async def create_customer(
    transaction_data: TransactionCreate, 
    session: SessionDep
     ):
    transaction_data_dict = transaction_data.model_dump()
    customer = session.get(Customer, transaction_data_dict["customer_id"]) 

    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    transaction_db = Transaction.model_validate(transaction_data_dict)
    session.add()
    session.commit()
    session.refresh()
    return transaction_db




@router.get('/transactions', tags=["transactions"])
async def list_transaction(session: SessionDep , skip: int = Query(0, description="Registros a omitir"),
                    limit:int = Query(2, description="Numero de registros a mostrar")):
   query = select(Transaction).offset(skip).limit(limit)
   transactions = session.exec(query).all()
   
   return transactions