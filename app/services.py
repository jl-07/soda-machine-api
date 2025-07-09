from sqlmodel import Session, select
from .models import Soda, Transaction
from .instructor_utils import parse_message
from datetime import datetime

def initialize_stock(session: Session):
    initial_sodas = [
        Soda(name="coke", stock=10),
        Soda(name="pepsi", stock=10),
        Soda(name="fanta", stock=10)
    ]
    for soda in initial_sodas:
        existing_soda = session.exec(select(Soda).where(Soda.name == soda.name)).first()
        if not existing_soda:
            session.add(soda)
    session.commit()

def handle_purchase(message: str, session: Session):
    parsed_command = parse_message(message)

    if parsed_command.intent != "comprar":
        return {"status": "error", "message": "Intenção não reconhecida para compra."}

    soda_name = parsed_command.soda_type.lower()
    quantity_to_buy = parsed_command.quantity

    soda = session.exec(select(Soda).where(Soda.name == soda_name)).first()

    if not soda or soda.stock < quantity_to_buy:
        return {"status": "error", "message": f"Refrigerante '{soda_name}' indisponível ou estoque insuficiente. Temos apenas {soda.stock}."}

    soda.stock -= quantity_to_buy
    session.add(soda)

    transaction = Transaction(
        soda_id=soda.id,
        quantity=quantity_to_buy,
        timestamp=datetime.utcnow()
    )
    session.add(transaction)

    session.commit()
    session.refresh(soda)

    return {
        "status": "success",
        "message": f"Compra de {quantity_to_buy} {soda_name} realizada. Estoque restante: {soda.stock}."
    }