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
from app.database import Base
from app.auth.user import User
from sqlalchemy.ext.declarative import declarative_base


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


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    category_id = Column(
        Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    website_url = Column(String, nullable=False)
    deletion_date = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    received_messages = relationship(
        Message,
        backref="received_messages",
        passive_deletes=True,
        cascade="all, delete",
    )

