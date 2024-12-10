from sqlmodel import Session

from db import engine
from models import Customer, Transaction

session = Session(engine)

customer = Customer(
    name = "John Doe",
    description="John Doe description",
    email="johan@gmail.com",
    age=20
)
session.add(customer)
session.commit()

for _ in  range(100):
    session.add(Transaction(
        customer_id=customer.id,
        descripción=f"Test number {_}",
        amount=10 * _
    ))
session.commit()