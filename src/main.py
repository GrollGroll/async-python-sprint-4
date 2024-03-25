import logging
import sys
from pydantic import BaseModel
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api.handlers import *
from core.config import AppSettings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

app = FastAPI(title=AppSettings().PROJECT_NAME, default_response_class=ORJSONResponse)

app.add_middleware(IPMiddleware)

# Получить сокращённый вариант переданного URL
@app.post('/', status_code=201)
async def handle_get_short_url(url: str):
    return await get_short_url(url)

# Передача ссылок пачками (batch upload) (доп.задание)
class BatchUpload(BaseModel):
    urls: list[str]

@app.post('/batch/', status_code=201)
async def handle_batch_upload_url(batch: BatchUpload):
    return await batch_upload_url(batch)

# Вернуть оригинальный URL
@app.get('/{url_id}', status_code=307)
async def handle_get_original_url(url_id: str):
    return await get_original_url(url_id)

# Вернуть статус использования URL
@app.get('/status/{url_id}')
async def handle_get_status(url_id: str):
    return await get_status(url_id)

if __name__ == '__main__':
    uvicorn.run(
        'main:app', 
        host=AppSettings().PROJECT_HOST, 
        port=AppSettings().PROJECT_PORT,
        reload=True,
    )
