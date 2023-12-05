import sqlalchemy as sa
from db import Base


class Order(Base):
    __tablename__ = "orders"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True, unique=True)
    username = sa.Column(sa.String, sa.ForeignKey("users.username"), nullable=False)
    product_name = sa.Column(sa.String, sa.ForeignKey("products.name"), nullable=False)

    def __repr__(self):
        return f"Заказ: {self.id}\n" \
               f"Покупатель: @{self.username}\n" \
               f"Товар: {self.product_name}\n"
