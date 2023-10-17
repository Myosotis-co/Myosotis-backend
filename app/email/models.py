from sqlalchemy import (
    Column,
    Integer,
    String,
    TIMESTAMP,
    text,
)
from sqlalchemy.orm import relationship

from app.database import Base


class TempEmail(Base):
    __tablename__ = "temp_emails"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    access_token = Column(String, unique=True, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    category = relationship(
        "Category", back_populates="temp_email", passive_deletes=True
    )
