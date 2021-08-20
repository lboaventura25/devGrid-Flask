from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import now
from database.db import db


Base = declarative_base()

class Weather(Base):
    __tablename__ = 'weather'

    id = Column(Integer, primary_key=True)
    city_name = Column(String(50), nullable=False)
    temperature = Column(String(10), nullable=False)
    description = Column(String(30))
    created_date = Column(DateTime,
                          server_default=now(),
                          nullable=False)

    def __init__(self, city_name, temperature, description, created_date=None):
        self.city_name = city_name
        self.temperature = temperature
        self.description = description
        self.created_date = created_date

    def to_dict(self):
        weather = {
            'id': self.id,
            'city_name': self.city_name,
            'temperature': self.temperature,
            'description': self.description,
            'created_date': self.created_date
        }

        return weather


Base.metadata.create_all(db)
