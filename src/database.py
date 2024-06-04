from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.config import setup_env, get_env_value


# load (cached) env variables
setup_env()


DB_HOST = get_env_value("DB_HOST")
DB_USER = get_env_value("DB_USER")
DB_PASSWORD = get_env_value("DB_PASSWORD")
DB_PORT = get_env_value("DB_PORT")
DB_NAME = get_env_value("DB_NAME")


SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# export database connection
Base = declarative_base()


def init_tables():
    """
    Initializes database tables from imported/available models.
    """
    # import models so that it is detected by sqlalchemy to export to table
    # added models to be exported to table should be imported below
    from src.auth.models import User
    # creates table
    Base.metadata.create_all(engine)


def get_db():
    """
    Dependency to initialize database connections.
    Closes connection after finishing queries.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
