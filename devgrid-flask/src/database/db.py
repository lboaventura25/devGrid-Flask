import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import select

from settings import logger


db_url = os.environ.get("SQLALCHEMY_DB_URL")
db = create_engine(db_url, echo=True)

Session = sessionmaker(db)
session = Session()


def insert_one(element):
    try:
        session.add(element)
        session.commit()

        return "Weather created successfully!", 201
    except Exception as error:
        logger.error(error)
        session.rollback()

        return 'Something went wrong', 500


def get_all(model, max_number):
    try:
        data = session.query(model).limit(max(max_number, 5)).all()

        return data, 200
    except Exception as error:
        logger.error(error)
        session.rollback()

        return 'Something went wrong', 500


def get_one(model, identifier):
    try:
        data = session.query(model).filter_by(city_name=identifier).first()

        if data:
            return data, 200

        return 'Not Found!', 404
    except Exception as error:
        logger.error(error)
        session.rollback()

        return 'Something went wrong', 500


def delete(model, identifier):
    try:
        data = session.query(model).filter_by(city_name=identifier).first()
        session.delete(data)
        session.commit()

        return "User deleted successfully!", 200
    except Exception as error:
        logger.error(error)
        session.rollback()

        return "Weather not found!", 404
