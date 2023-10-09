from sqlalchemy import create_engine, Integer, Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import geocoding_API

engine = create_engine('postgresql+psycopg2://postgres:12345@localhost:5432/postgres')
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
    fk_location_id = Column(Integer)


class Location(Base):
    __tablename__ = 'locations'

    location_id = Column(Integer, primary_key=True)
    city = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def set_location(chat_id, country, city):
    coord = geocoding_API.get_city_latitude(country, city)
    session = Session()

    if (session.query(Location).filter(Location.latitude == coord['lat'], Location.longitude == coord['lng'])
            .first() is None):
        location = Location(city=city, latitude=coord['lat'], longitude=coord['lng'])
        session.add(location)
        session.commit()

    fk_location_id = session.query(Location).filter(Location.latitude == coord['lat'],
                                                    Location.longitude == coord['lng']).first()
    fk_location_id = fk_location_id.location_id

    if session.query(User).filter(User.chat_id == chat_id).first() is None:
        user = User(chat_id=chat_id, fk_location_id=fk_location_id)
        session.add(user)
    else:
        a = session.query(User).filter(User.chat_id == chat_id).first()
        a.fk_location_id = fk_location_id

    session.commit()


def get_location(chat_id):
    session = Session()
    if session.query(User).filter(User.chat_id == chat_id).first() is None:
        return "Input your location (/set_location)"
    else:
        fk_location_id = session.query(User).filter(User.chat_id == chat_id).first().fk_location_id
        location = session.query(Location).filter(Location.location_id == fk_location_id).first()
        coord = {'lat': location.latitude, 'lng': location.longitude}
        return coord
