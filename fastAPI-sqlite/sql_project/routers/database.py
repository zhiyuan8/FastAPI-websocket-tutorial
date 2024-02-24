from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'

# The engine is created to manage the database connection.
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# SessionLocal is configured to handle transactions and operations in the database through a session. 
# It's the way you interact with the database in a more Pythonic way instead of writing raw SQL.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is used to define models (database tables in ORM), which SQLAlchemy uses to create or interact with the database schema.
Base = declarative_base()