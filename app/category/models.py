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

from app.application.models import Application


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    temp_email_id = Column(Integer, ForeignKey("temp_emails.id"), nullable=False)
    category_name = Column(String, nullable=False)
    deletion_date = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    applications = relationship(
        Application,
        backref="applications",
        passive_deletes=True,
        cascade="all, delete",
    )
    temp_email = relationship(
        "TempEmail", back_populates="category", passive_deletes=True
    )
