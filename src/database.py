from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import parse_env_value


DB_HOST = parse_env_value("DB_HOST")
DB_USER = parse_env_value("DB_USER")
DB_PASSWORD = parse_env_value("DB_PASSWORD")
DB_PORT = parse_env_value("DB_PORT")
DB_NAME = parse_env_value("DB_NAME")


SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# export database connection
Base = declarative_base()
