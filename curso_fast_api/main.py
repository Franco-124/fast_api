from fastapi import FastAPI, HTTPException,status
from datetime import datetime
import zoneinfo
from models import Customer,Transaction,Invoice, CustomerCreate
from db import SessionDep,create_all_tables
from sqlmodel import select

app=FastAPI()


@app.on_event("startup")
def on_startup():
    create_all_tables()


@app.get("/")
async def root():
    return {"message":"hola Johan "}


country_timezones = {
    "US": "America/New_York",
    "UK": "Europe/London",
    "DE": "Europe/Berlin",
    "FR": "Europe/Paris",
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
}




@app.get("/time/{iso_code}")
async def time(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    now = datetime.now(tz)
    return {"hora":  now.strftime("%H:%M:%S")}





@app.post('/customers', response_model=Customer)
async def create_customer(customer_data: CustomerCreate , session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@app.get("/customers/{customer_id}", response_model=Customer)
async def read_customer(customer_id:int, session:SessionDep):
    customer_db=session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer no encontrado")
    return customer_db


@app.delete("/customers/{customer_id}")
async def delete_customer(customer_id:int, session:SessionDep):
    customer_db=session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer no encontrado")
    session.delete(customer_db)
    session.commit()
    return {"detail :" "ok"}


@app.get("/customers")
async def list_customer( session: SessionDep):
    return session.exec(select(Customer)).all()
    


"""@app.get("/customers/{customer_id}", response_model = Customer)
async def get_customer(customer_id:int):
    customer = next((customer for customer in db_customers if customer["id"] == customer_id), None)
    if customer is not None:
       return customer
    raise HTTPException(status_code=404, detail="customer_not_found")
"""


"""#OBTENER CUSTOMER SEGUN ID USANDO SESSION
@app.get("/customers/{id}", response_model=Customer | None)
async def get_customer(id: int, session: SessionDep):
    if not session.exec(select(Customer)).all():
        return {'messsage':'Cliente no encontrado'}
    for i in session.exec(select(Customer)).all():
        if i.id == id:
            return i
"""



@app.post('/transactions')
async def create_customer(transaction_data: Transaction):
    return transaction_data

@app.post('/invoices')
async def create_customer(invoice_data: Invoice):
    return invoice_data
