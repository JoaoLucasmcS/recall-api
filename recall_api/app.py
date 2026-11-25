from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from recall_api.core.settings import get_settings
from recall_api.routers.campeoes_router import router as campeoes_router
from recall_api.schemas.message_schemas import Message

settings = get_settings()
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=[settings.frontend_url], allow_methods=['GET'])

app.include_router(campeoes_router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def health_check():
    return {'message': 'Tá rodano!'}
