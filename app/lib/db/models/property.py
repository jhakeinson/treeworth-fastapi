from decimal import Decimal
import uuid
from sqlmodel import Field, Relationship, SQLModel

class Street(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    category: str = Field(index=True)
    tree_median_height: float
    properties: list["Property"] = Relationship(back_populates="street")


class Property(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    full_address: str = Field(index=True)
    price: Decimal = Field(default=0, max_digits=14, decimal_places=2)
    street_id: uuid.UUID = Field(default_factory=uuid.uuid4, foreign_key="street.id")
    street: Street = Relationship(back_populates="properties")
    date_of_sale: str