from sqlalchemy import (
    create_engine,
)
from sqlalchemy.engine import URL
import os
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base, sessionmaker


load_dotenv()
url = os.environ["DATABASE_URL"] + "?sslmode=disable"

engine = create_engine(url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
