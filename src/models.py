import enum

from sqlalchemy import (TIMESTAMP, Boolean, Column, Enum, ForeignKey, Integer,
                        String, Table, Text)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class EnumStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    not_solved = "not_solved"
    outsourced = "outsourced"
    solved = "solved"


class EnumPriority(str, enum.Enum):
    low = "low"
    normal = "normal"
    high = "high"
    urgent = "urgent"


has = Table(
    "has",
    Base.metadata,
    Column("problem_id", Integer, ForeignKey("problem.id")),
    Column("request_id", Integer, ForeignKey("request.id")),
    Column("category_id", Integer, nullable=False),
    Column("is_event", Boolean, nullable=True),
    Column("event_date", TIMESTAMP, nullable=True),
    Column(
        "request_status",
        Enum(EnumStatus),
        default=EnumStatus.pending,
        nullable=False,
    ),
    Column(
        "priority",
        Enum(EnumPriority),
        default=EnumPriority.normal,
        nullable=False,
    ),
)


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    active = Column(Boolean, default=True)
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )


class Problem(Base):
    __tablename__ = "problem"
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=True)
    active = Column(Boolean, nullable=False, default=True)
    updated_at = Column(
        TIMESTAMP,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
    category_id = Column(Integer, ForeignKey(Category.id))
    requests = relationship(
        "Request", secondary=has, back_populates="problems"
    )


class Request(Base):
    __tablename__ = "request"
    id = Column(Integer, primary_key=True)
    attendant_name = Column(String(250), nullable=False)
    applicant_name = Column(String(250), nullable=False)
    applicant_phone = Column(String(20), nullable=True)
    place = Column(String(250), nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    workstation_id = Column(Integer, nullable=False)
    problems = relationship(
        "Problem", secondary=has, back_populates="requests"
    )
