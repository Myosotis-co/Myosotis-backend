from sqlalchemy import (
    UniqueConstraint,
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
from app.message.models import Message


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    category_id = Column(
        Integer, ForeignKey("categories.id", ondelete="CASCADE"), nullable=False
    )
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    website_url = Column(String, nullable=False)
    application_name = Column(String, nullable=False)
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

    __table_args__ = (UniqueConstraint("category_id", "website_url"),)
