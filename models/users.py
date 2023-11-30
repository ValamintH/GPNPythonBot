import sqlalchemy as sa
from db import Base


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=False, unique=True)
    is_admin = sa.Column(sa.Boolean, default=False)
    first_name = sa.Column(sa.String)
    last_name = sa.Column(sa.String, nullable=True)
    username = sa.Column(sa.String)
    barrels = sa.Column(sa.Integer, default=0)

    def __repr__(self):
        return f"Пользователь: {self.first_name} {self.last_name}\n" \
               f"ID: {self.id}\n" \
               f"Юзернейм: {self.username}\n" \
               f"Количество баррелек: {self.barrels}\n" \
               f"Администратор: {self.is_admin}\n"
