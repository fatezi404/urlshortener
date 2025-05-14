from fastapi import FastAPI

from app.api.v1.routers import health_router, url_router, redirect_router


app = FastAPI(docs_url='/api/v1/docs')


app.include_router(
    router=health_router.router,
    prefix='/api/v1',
    tags=['healthcheck']
)

app.include_router(
    router=url_router.router,
    prefix='/api/v1',
    tags=['shortener']
)

app.include_router(
    router=redirect_router.router,
    tags=['redirect']
)

print('Routers included')

@app.get('/')
async def root():
    return {'message': 'Root page'}