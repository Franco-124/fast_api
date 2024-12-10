from typing import Annotated
from fastapi import Depends,status, FastAPI, HTTPException, Request
from datetime import datetime
import time
import zoneinfo

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from db import SessionDep,create_all_tables
from sqlmodel import select
from app.routers import customers,transactions,invoices,plans

app=FastAPI()
app.include_router(customers.router)  
app.include_router(transactions.router)
app.include_router(plans.router)

@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.url} completed in {process_time:.4f} seconds")
    return response

@app.middleware("http") 
async def log_request_headers(request: Request, call_next):
    
    print("Request Headers:")
    for header, value in request.headers.items():
        print(f"{header}: {value}")

    response = await call_next(request) 

    return response

@app.on_event("startup")
def on_startup():
    create_all_tables()

security = HTTPBasic()
@app.get("/")
async def root(credentials : Annotated[HTTPBasicCredentials,Depends(security)]):
    print(credentials)
    if credentials.username == "johan" and credentials.password == "1234":
         return {"message":f"hola {credentials.username}!"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

country_timezones = {
    "US": "America/New_York",
    "UK": "Europe/London",
    "DE": "Europe/Berlin",
    "FR": "Europe/Paris",
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
}




@app.get("/time/{iso_code}")
async def get_time_by_iso_code(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    now = datetime.now(tz)
    return {"hora":  now.strftime("%H:%M:%S")}














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



