import sqlalchemy as sa
from sqlalchemy.orm import relationship
from db import Base
from models.orders import Order # noqa


class Product(Base):
    __tablename__ = "products"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)
    name = sa.Column(sa.String, nullable=False, unique=True)
    description = sa.Column(sa.String)
    price = sa.Column(sa.Integer, default=0)
    image = sa.Column(sa.String)

    order = relationship("Order")

    def __repr__(self):
        return f"Товар: {self.name}\n" \
               f"ID: {self.id}\n" \
               f"Описание: {self.description}\n" \
               f"Цена: {self.price}\n"
