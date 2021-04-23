"""Data base app."""
from os import environ

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URI = (
    'postgresql+psycopg2://postgres:{password}@{db}/postgres'.format(
        db=environ.get('DB'),
        password=environ.get('DB_PASSWORD')
    )
) if environ.get('DB') else 'sqlite:///foo.db'

engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
