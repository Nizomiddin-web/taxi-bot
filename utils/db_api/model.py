from sqlalchemy import Column, Integer, String, Table, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# engine = create_engine('mysql+pymysql://nizom:nizom0299@localhost:3306/nizom', echo=True)
from data.config import DB_CONNECT_URL


engine = create_engine(DB_CONNECT_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
    __tablename__ = 'users_lang'
    telegram_id = Column(String, primary_key=True)
    lang = Column(String, nullable=True)


class DemoData(Base):
    __tablename__ = 'demo_datas'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    country_code = Column(String)
    phone_number = Column(String, unique=True)


Base.metadata.create_all(engine)
