from sqlalchemy import create_engine, Column, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import List
import os

load_dotenv()
mysql_password = os.getenv('MYSQL_PASSWORD')
DATABASE_URL = f"mysql+pymysql://root:{mysql_password}@49.247.34.221/woodeco"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class User(Base):
    __tablename__ = "user"

    user_id = Column(String(255), primary_key=True, index=True)
    birth = Column(String(12))
    sex = Column(String(8))
    tastes = Column(String(140))

class UserCreate(BaseModel):
    user_id: str
    birth: str
    sex: bool
    tastes: List[bool]