from pydantic import BaseModel, EmailStr, field_validator
from sqlmodel import Relationship, SQLModel, Field, Session, select
from typing import List, Optional
from enum import Enum
from db import engine


class StatusEnum(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class CustomerPlan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    plan_id: Optional[int] = Field(default=None, foreign_key="plan.id")
    customer_id: Optional[int] = Field(default=None, foreign_key="customer.id")
    status:StatusEnum = Field(default=StatusEnum.ACTIVE)

class Plan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    price: int
    description: Optional[str] = None
    customers: List['Customer'] = Relationship(
        back_populates="plans",
        link_model=CustomerPlan
    )
    

class CustomerBase(SQLModel):
    name: str = Field(default=None)
    description: Optional[str] | None = Field(default=None)
    email: EmailStr  = Field(default=None)
    age: int = Field(default=None)
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        session = Session(engine)
        query = select(Customer).where(Customer.email == value)
        result = session.exec(query).first()
        if result:
            raise ValueError("Email already exists")
        return value
    
    @field_validator("age")
    @classmethod
    def validate_age(cls, value):
        if value < 18:
            raise ValueError("Must be 18 years old")
        return value
        

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    transactions: List["Transaction"] = Relationship(back_populates="customer")
    plans: List[Plan] = Relationship(
        back_populates="customers", link_model=CustomerPlan
    )

class TransactionBase(SQLModel):
    amount: int
    description: Optional[str] = None

class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: Optional[int] = Field(default=None, foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="transactions")

class TransactionCreate(TransactionBase):
    customer_id: int

class Invoice(BaseModel):
    id: int = Field(default=None)
    customer: Customer = Field(default=None)
    transactions: List[Transaction] = Field(default=None)
    total: int = Field(default=None)
    
    @property
    def amount_total(self):
        return sum(transaction.amount for transaction in self.transactions)