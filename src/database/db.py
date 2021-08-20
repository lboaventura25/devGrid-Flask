import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import logger


db_url = os.environ.get("SQLALCHEMY_DB_URL")
db = create_engine(db_url, echo=True)

Session = sessionmaker(db)
session = Session()


def insert_one(element):
    try:
        # INSERT INTO weather (city_name, temperature, description) 
        # VALUES ('paris', 18.13, 'clean sky') 
        session.add(element)
        session.commit()

        return "Weather created successfully!", 201
    except Exception as error:
        logger.error(error)
        session.rollback()

        return 'Something went wrong', 500


def get_all(model, max_number):
    try:
        # SELECT * FROM weather w ORDER BY w.created_date DESC LIMIT 5
        data = session.query(model) \
            .order_by(model.created_date.desc()) \
            .limit(max_number) \
            .all()

        return data, 200
    except Exception as error:
        logger.error(error)
        session.rollback()

        return 'Something went wrong', 500


def get_one(model, identifier):
    try:
        # SELECT * FROM weather w WHERE w.city_name = "paris"
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
        # DELETE FROM weather w WHERE w.city_name = "paris"
        data = session.query(model).filter_by(city_name=identifier).first()
        session.delete(data)
        session.commit()

        return "User deleted successfully!", 200
    except Exception as error:
        logger.error(error)
        session.rollback()

        return "Weather not found!", 404
