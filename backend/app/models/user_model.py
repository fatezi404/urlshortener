from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    Integer
)
from sqlalchemy import func
from app.db.session import Base


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    hashed_pass = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())