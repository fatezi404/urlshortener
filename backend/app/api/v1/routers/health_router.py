from fastapi import APIRouter, status


router = APIRouter()


@router.get('/healthcheck', status_code=status.HTTP_200_OK, tags=['healthcheck'])
async def get_health():
    return {'status': '200 OK'}