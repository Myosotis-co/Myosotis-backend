from venv import create
from sqlalchemy import Boolean, Column, Integer, String, Float, DateTime, ForeignKey,MetaData, TIMESTAMP, text
from sqlalchemy.orm import relationship
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    # temp_email_id = Column(Integer, ForeignKey("temp_emails.id"))
    category_name = Column(String)
    deletion_date = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))