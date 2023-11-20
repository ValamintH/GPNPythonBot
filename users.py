import sqlalchemy as sa
from db import Base


class User(Base):
    __tablename__ = "users"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=False, unique=True)
    first_name = sa.Column(sa.String)
    last_name = sa.Column(sa.String, nullable=True)
    username = sa.Column(sa.String)
    barrels = sa.Column(sa.Integer, default=0)

    def __repr__(self):
        return "<User {}>".format(self.username)
