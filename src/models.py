from datetime import timezone
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from database import Base


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    active = Column(Boolean, default=True)
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        server_onupdate=func.current_timestamp(timezone.utc)
    )


class Problem(Base):
    __tablename__ = "problem"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        server_onupdate=func.current_timestamp(timezone.utc)
    )
    category_id = Column(Integer, ForeignKey(Category.id), primary_key=True)