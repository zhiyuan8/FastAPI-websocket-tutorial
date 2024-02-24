from .database import Base, SessionLocal
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
"""
Inheriting from Base in SQLAlchemy is crucial for several reasons, 
particularly when defining your models like Users and Todos in an ORM (Object-Relational Mapping) approach. 
"""

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)


class Todos(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id")) # describes the relationship between the Todos and Users table