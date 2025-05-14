from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import RedirectResponse

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db.session import get_db
from app.models.url_model import URLModel


router = APIRouter()


@router.get('/{short_url}', response_class=RedirectResponse, tags=['redirect'])
async def redirect_to_url(short_url: str, db: AsyncSession = Depends(get_db)):
    '''Redirect to long_url through short_url.'''
    query = select(URLModel).filter(URLModel.short_url == short_url, URLModel.is_active == True)
    response = await db.execute(query)
    result = response.scalar_one_or_none()
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='URL not found')
    return result.long_url