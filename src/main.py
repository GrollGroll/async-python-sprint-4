import secrets
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from core import config
from core.logger import LOGGING
from db.db import get_session
from models.entity import Entity

BLACK_LIST = [
    # "127.0.0.1",
    "56.24.15.106"
]

app = FastAPI(title=config.PROJECT_NAME, default_response_class=ORJSONResponse)

# Middleware для проверки IP-адреса (доп.задание)
def is_ip_banned(headers):
    try:
        real_ip = headers['host'][:-5]
        print(real_ip)
        return real_ip in BLACK_LIST
    except KeyError:
        print('IP header not found')
        return True

class IPMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if is_ip_banned(request.headers):
            return JSONResponse(status_code=403, content={'message': 'Forbidden'})
        response = await call_next(request)
        return response
    
app.add_middleware(IPMiddleware)

# Получить сокращённый вариант переданного URL
@app.post('/', status_code=201)
async def get_short_url(url: str):
    session = await get_session()
    url_id = secrets.token_urlsafe(5)
    short_url = f'http://{url_id}'
    entity = Entity(id=url_id, original_url=url, shortened_url=short_url, num_of_visit=0)
    session.add(entity)
    await session.commit()
    return short_url

# Передача ссылок пачками (batch upload) (доп.задание)
class BatchUpload(BaseModel):
    urls: list[str]

@app.post('/batch/', status_code=201)
async def batch_upload_url(batch: BatchUpload):
    for url in batch.urls:
        await get_short_url(url)

# Вернуть оригинальный URL
@app.get('/{url_id}', status_code=307)
async def get_original_url(url_id: str):
    session = await get_session()
    query = await session.get(Entity, url_id)
    if query:
        original_url = query.original_url
        query.num_of_visit += 1
        await session.commit()
        return original_url
    else:
        raise HTTPException(status_code=404, detail='Not found')

# Вернуть статус использования URL
@app.get('/status/{url_id}')
async def get_status(url_id: str):
    session = await get_session()
    query = await session.get(Entity, url_id)
    if query:
        status = query.num_of_visit
        return f'Number of visit: {status}'
    else:
        raise HTTPException(status_code=404, detail='Not found')

if __name__ == '__main__':
    uvicorn.run(
        'main:app', 
        host=config.PROJECT_HOST, 
        port=config.PROJECT_PORT,
        reload=True,
    )