from sqlalchemy import Column, Integer, String, Table, Boolean
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# engine = create_engine('mysql+pymysql://nizom:nizom0299@localhost:3306/nizom', echo=True)
engine = create_engine('postgresql+psycopg2://postgres:1234@localhost:5432/test_db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(String, unique=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    phone_number = Column(String, unique=True, nullable=True)
    is_verified = Column(Boolean, default=False)
    verification_code = Column(String, nullable=True)


class DemoData(Base):
    __tablename__ = 'demo_datas'
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    country_code = Column(String)
    phone_number = Column(String, unique=True)


Base.metadata.create_all(engine)
