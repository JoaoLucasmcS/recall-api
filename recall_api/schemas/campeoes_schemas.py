from pydantic import BaseModel


class CampeaoResumo(BaseModel):
    id: str
    name: str
    title: str
    tags: list[str]
    imagem_url: str


class CampeaoDetalhe(CampeaoResumo):
    info: dict
    lore: str
    blurb: str
    allytips: list[str]
    enemytips: list[str]
    partype: str
    stats: dict
