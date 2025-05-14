from sqlalchemy import (
    Column,
    String,
    DateTime,
    Boolean,
    Integer
)
from sqlalchemy import func
from app.db.session import Base


class URLModel(Base):
    __tablename__ = 'urls'
    
    url_id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String(2048), nullable=False)
    short_url = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())