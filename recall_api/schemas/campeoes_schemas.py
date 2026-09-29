from pydantic import BaseModel


class Image(BaseModel):
    full: str


class CampeaoResumo(BaseModel):
    id: str
    name: str
    title: str
    image: Image


class CampeaoDetalhe(CampeaoResumo):
    info: str
    blurb: str
    tags: str
    partype: str
