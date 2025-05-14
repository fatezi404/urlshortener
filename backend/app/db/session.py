from sqlalchemy.orm import declarative_base 
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.core.config import settings

engine = create_async_engine(settings.DATABASE_URL)

Session = async_sessionmaker(engine)

Base = declarative_base()

async def get_db():
    db = Session()
    try:
        yield db
    finally:
        await db.close()