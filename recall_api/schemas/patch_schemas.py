from pydantic import BaseModel


class Patch(BaseModel):
    versao: str
