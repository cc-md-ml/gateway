from sqlalchemy import Column, String, Integer

from src.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(32), unique=True, index=True)
    password = Column(String(64))
    