from sqlalchemy import create_engine, Integer, Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import geocoding_API

engine = create_engine('postgresql+psycopg2://qplogdvyiaaymv:e3b6b3ce79fccbfeb8e7c5f716ae4f19da165e9a9441c3d0d649c1c3c'
                       'af0fdf0@ec2-52-19-164-214.eu-west-1.compute.amazonaws.com/d8mmdsqobd7qjg')
connection = engine.connect()


# def set_location(chat_id, country, state, city):
#     coord = geocoding_API.get_city_latitude(country, state, city)
#     connection.execute("INSERT INTO users(user_city, city_latitude, city_longitude, chat_id)"
#                        f" VALUES ('{city}', {coord['lat']}, {coord['lng']}, {chat_id})")
#

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    chat_id = Column(Integer)
    user_city = Column(String)
    city_latitude = Column(Float)
    city_longitude = Column(Float)



Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def set_location(chat_id, country, state, city):
    coord = geocoding_API.get_city_latitude(country, state, city)
    session = Session()
    user = User(user_city=city, city_latitude=coord['lat'], city_longitude=coord['lng'], chat_id=chat_id)
    session.add(user)
    session.commit()
