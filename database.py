from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

sqlalchemy_database_url = "postgresql://postgres:"password"@localhost:5432/fastapi" #<-password should inser here
engine = create_engine(sqlalchemy_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

Base.metadata.create_all(bind=engine) # recreate tables with new columns


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
