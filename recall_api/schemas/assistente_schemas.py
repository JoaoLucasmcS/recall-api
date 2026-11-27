from enum import StrEnum

from pydantic import BaseModel


class RolesPermitidasNasMensagens(StrEnum):
    USER = 'user'
    ASSISTANT = 'assistant'


class Mensagem(BaseModel):
    role: RolesPermitidasNasMensagens
    content: str


class PerguntaAssistente(BaseModel):
    mensagens: list[Mensagem]


class RespostaAssistente(BaseModel):
    resposta: str
