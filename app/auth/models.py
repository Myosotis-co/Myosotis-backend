from app.database import Base

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseOAuthAccountTable
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    TIMESTAMP,
    ForeignKey,
    JSON,
    Boolean,
    MetaData,
    text,
)
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.ext.declarative import declared_attr


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)

    users = relationship("User", backref="users", passive_deletes=True)


# Needed for linkage autherization through 3rd party apps
class OAuthAccount(SQLAlchemyBaseOAuthAccountTable[int], Base):
    __tablename__ = "oauth_accounts"
    id = Column(Integer, primary_key=True)

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return Column(
            Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
        )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    role_id = Column(
        Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False
    )
    name = Column(
        String,
        nullable=False,
    )
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    oauth_accounts = relationship("OAuthAccount", lazy="joined")
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    categories = relationship(
        "Category",
        backref="categories",
        passive_deletes=True,
        cascade="all, delete",
    )

    # ignoring the fastapi_users columns
    def is_active(self):
        pass

    def is_superuser(self):
        pass
