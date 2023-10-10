from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create database URL for SQLAlchemy
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Smileok21@localhost/fastapi"

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

# Create a Base class
Base = declarative_base()

# Create Dependency: creat new session that will be used in a single request and 
# then close it once the request is finished. 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()