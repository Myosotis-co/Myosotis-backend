from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    MetaData,
    TIMESTAMP,
    text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from app.database import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    application_id = Column(
        Integer, ForeignKey("applications.id", ondelete="CASCADE"), nullable=False
    )
    message_type_id = Column(Integer, ForeignKey("message_types.id"), nullable=False)
    topic = Column(String, nullable=False)
    message_text = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )


class Message_Type(Base):
    __tablename__ = "message_types"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)

    messages = relationship(Message, backref="messages", passive_deletes=True)
