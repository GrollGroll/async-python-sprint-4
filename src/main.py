import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api import handlers
from core.config import app_settings

app = FastAPI(title=app_settings.project_name, default_response_class=ORJSONResponse)

app.add_middleware(handlers.IPMiddleware)

app.include_router(handlers.router, prefix='/api')

if __name__ == '__main__':
    uvicorn.run(
        'main:app', 
        host=app_settings.project_host, 
        port=app_settings.project_port,
        reload=True,
    )
