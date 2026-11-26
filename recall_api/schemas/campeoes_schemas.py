from pydantic import BaseModel


class Passiva(BaseModel):
    name: str
    description: str
    imagem_url: str


class Habilidade(BaseModel):
    id: str
    name: str
    description: str
    cooldownBurn: str
    costBurn: str
    imagem_url: str


class Skin(BaseModel):
    num: int
    name: str
    splash_url: str


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
    splash_url: str
    passive: Passiva
    spells: list[Habilidade]
    skins: list[Skin]
