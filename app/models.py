from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime

class Soda(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    stock: int

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    soda_id: int = Field(foreign_key="soda.id")
    quantity: int
    timestamp: datetime = Field(default_factory=datetime.utcnow)