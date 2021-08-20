import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import logger


db_url = os.environ.get("SQLALCHEMY_DB_URL")
db = create_engine(db_url, echo=True)

Session = sessionmaker(db)
session = Session()


# INSERT INTO weather (city_name, temperature, description) 
# VALUES ('paris', 18.13, 'clean sky') 
def insert_one(element):
    try:
        session.add(element)
        session.commit()

        return "Weather created successfully!", 201
    except Exception as error:
        logger.error(error)
        session.rollback()

        return 'Something went wrong', 500


# SELECT * FROM weather w ORDER BY w.created_date DESC LIMIT 5
def get_all(model, max_number):
    try:
        data = session.query(model) \
            .order_by(model.created_date.desc()) \
            .limit(max_number) \
            .all()

        return data, 200
    except Exception as error:
        logger.error(error)
        session.rollback()

        return 'Something went wrong', 500


 # SELECT * FROM weather w WHERE w.city_name = "paris"
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


# UPDATE weather 
# SET temperature = 20.90, description = 'clean sky' 
# WHERE city_name = 'paris'
def update(model, identifier, params):
    try:
        data = session.query(model).filter_by(city_name=identifier).first()
        session.commit()

        if data:
            for param in params:
                setattr(data, param, params[param])
        
            session.commit()
            return data, 200

        return "Not Found!", 404
    except Exception as error:
        logger.error(error)
        session.rollback()

        return 'Something went wrong', 500


# DELETE FROM weather w WHERE w.city_name = "paris"
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
