import secrets
import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from core import config
from core.logger import LOGGING
from db.db import get_session
from models.entity import Entity
app = FastAPI(title=config.PROJECT_NAME, default_response_class=ORJSONResponse)

@app.post('/short')
async def shorten_url(url: str):
    session = get_session()
    url_id = secrets.token_urlsafe(5)
    short_url = f"http://example.com/{url_id}"
    entity = Entity(id=url_id, original_url=url, shortened_url=short_url)
    session.add(entity)
    session.commit()
    session.close()
    return short_url
    
if __name__ == '__main__':
    uvicorn.run(
        'main:app', 
        host=config.PROJECT_HOST, 
        port=config.PROJECT_PORT,
    )