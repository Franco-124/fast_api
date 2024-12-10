from fastapi import APIRouter

from models import Invoice


router = APIRouter()


@router.post('/invoices')
async def create_customer(invoice_data: Invoice):
    return invoice_data
