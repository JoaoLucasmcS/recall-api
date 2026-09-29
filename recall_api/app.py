from fastapi import FastAPI

from recall_api.routers.campeoes_router import router as campeoes_router

app = FastAPI()
app.include_router(campeoes_router)


@app.get("/")
def helth_check():
    return {"message": "Tá rodano!"}
