from extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

class User(db.Model):
    __tablename__ = 'users_1'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))

    def __repr__(self):
        return f"User({self.name}, {self.password}, {self.email})"