from contextlib import asynccontextmanager
from http import HTTPStatus

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from recall_api.core.cache import CacheCampeoes, CacheVersao
from recall_api.core.settings import get_settings
from recall_api.routers.campeoes_router import router as campeoes_router
from recall_api.schemas.message_schemas import Message


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient(timeout=10.0) as http_client:
        app.state.http_client = http_client
        app.state.cache_versao = CacheVersao(ttl_segundos=6 * 60 * 60)
        app.state.cache_campeoes = CacheCampeoes()
        yield


settings = get_settings()
app = FastAPI(lifespan=lifespan)

app.add_middleware(CORSMiddleware, allow_origins=[settings.frontend_url], allow_methods=['GET'])

app.include_router(campeoes_router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def health_check():
    return {'message': 'Tá rodano!'}
