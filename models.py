from sqlalchemy import Integer, Column, String
from db import Base
class User(Base):
    __tablename__ = "users"

    id = Column(Integer,primary_key=True, index=True)
    name = Column(String, nullable= False)
    email = Column(String, nullable= False, unique= True)
    age = Column (Integer, nullable= False)