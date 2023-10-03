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
from sqlalchemy.ext.declarative import declarative_base
from app.models import Message


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
