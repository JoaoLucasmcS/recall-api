from pydantic import BaseModel


class Image(BaseModel):
    full: str


class CampeaoResumo(BaseModel):
    id: str
    name: str
    title: str
    image: Image


class CampeaoDetalhe(CampeaoResumo):
    info: dict
    lore: str
    blurb: str
    allytips: list[str]
    enemytips: list[str]
    tags: list[str]
    partype: str
    stats: dict
