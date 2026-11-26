from contextlib import asynccontextmanager
from http import HTTPStatus

import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from recall_api.core.cache import CacheCampeoes, CacheVersao
from recall_api.core.exceptions import DataDragonIndisponivelError
from recall_api.core.settings import get_settings
from recall_api.routers.campeoes_router import router as campeoes_router
from recall_api.routers.patch_router import router as patch_router
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
app.include_router(patch_router)


# O Data Dragon pode falhar dentro de uma dependência (ex.: ao buscar a versão atual),
# antes de a rota rodar; por isso este erro é tratado aqui, para a API inteira.
@app.exception_handler(DataDragonIndisponivelError)
async def data_dragon_indisponivel(request: Request, erro: DataDragonIndisponivelError):
    return JSONResponse(
        status_code=HTTPStatus.SERVICE_UNAVAILABLE,
        content={'detail': 'Data Dragon indisponível no momento'},
    )


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def health_check():
    return {'message': 'Tá rodano!'}
