from sqlalchemy import create_engine,MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

SQL_URL = "mysql://root:%s@localhost:3306/practica"% quote_plus("pass@word")
engine = create_engine(SQL_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata_obj = MetaData(bind=engine)
Base = declarative_base(metadata=metadata_obj)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
