from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database import Base


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    active = Column(Boolean, default=True)
    # relacionado a server default (server_default=)
    updated_at = Column(DateTime(timezone=True))
    #@TODO: conferir se tá certo
    categoria = relationship("problem", back_populates="category")


class Problem(Base):
    __tablename__ = "problem"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    # como inclui o current timestamp como default?
    updated_at = Column(DateTime(timezone=True))
    category_id = Column(Integer, ForeignKey(Category.id), primary_key=True)
    # has = relationship() #https://docs.sqlalchemy.org/en/14/orm/basic_relationships.html
    # category =
