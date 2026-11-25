from http import HTTPStatus

from fastapi import FastAPI

from recall_api.routers.campeoes_router import router as campeoes_router
from recall_api.schemas.message_schemas import Message

app = FastAPI()

app.include_router(campeoes_router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
async def health_check():
    return {'message': 'Tá rodano!'}
