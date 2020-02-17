from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///newspaper.db')  # nuestro motor

Session = sessionmaker(bind=engine)  # al objeto sessionmaker le pasamos el motor

Base = declarative_base()  # se van a extender todos nuestro modelos
