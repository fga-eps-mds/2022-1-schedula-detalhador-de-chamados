from operator import truediv
from unicodedata import name
from sqlalchemy import Column, Integer, String
from database import Base

class Chamado(Base):

    __tablename__ = "categoria"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)#n sei como seria no caso de TEXT#

    __tablename__ = "problem"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)

    
