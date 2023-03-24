from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./app/database.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://ehab:OyhKPPw4p1eRyXeL6NicjgRCLyg9qBNF@dpg-cgeqsje4dadd1mng6o3g-a.oregon-postgres.render.com/ehab"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
# engine = create_engine(SQLALCHEMY_DATABASE_URL, isolation_level="AUTOCOMMIT")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()