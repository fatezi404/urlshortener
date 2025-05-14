from typing import Annotated
from fastapi import APIRouter, Depends, status, HTTPException, Query, Response

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.schemas.url_schema import URLLong, URLShort, URLResponse, URLUpdate
from app.utils.uuid import generate_short_id
from app.models.url_model import URLModel


router = APIRouter()


@router.post('/url-shortener', response_model=URLResponse, tags=['shortener'])
async def create_url(url: URLLong, db: AsyncSession = Depends(get_db)):
    '''Generate short ID, which is UUID + base64, create a database 
    record with long_url and short_url (which is basically a short ID).'''
    query = select(URLModel).filter(URLModel.long_url == str(url.long_url))
    response = await db.execute(query)
    exist_in_db = response.one_or_none()
    if exist_in_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='URL already exists')
    short_url = generate_short_id()
    db_url = URLModel(
        long_url = str(url.long_url),
        short_url = short_url
    )
    db.add(db_url)
    await db.commit()
    await db.refresh(db_url)
    return db_url


@router.get('/url-shortener', response_model=URLResponse, tags=['shortener'])
async def read_from_short_url(short_url: Annotated[URLShort, Query()], db: AsyncSession = Depends(get_db)):
    '''Get all data from short_url.'''
    query = select(URLModel).filter(
        URLModel.short_url == str(short_url.short_url), URLModel.is_active == True
        )
    response = await db.execute(query)
    result = response.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='URL not found')
    return result


@router.patch('/url-shortener/update_url', response_model=URLResponse, tags=['shortener'])
async def update_url(short_url: Annotated[URLShort, Query()],  db: AsyncSession = Depends(get_db)):
    '''Update URL'''
    query = select(URLModel).filter(URLModel.short_url == short_url.short_url)
    response = await db.execute(query)
    result = response.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='URL not found')
    result.is_active = not result.is_active
    await db.commit()
    await db.refresh(result)
    return result


@router.delete('/url-shortener', tags=['shortener'])
async def delete_url(short_url: Annotated[URLShort, Query()], db: AsyncSession = Depends(get_db)):
    query = select(URLModel).filter(URLModel.short_url == short_url.short_url)
    response = await db.execute(query)
    result = response.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='URL not found')
    await db.delete(result)
    await db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)