class CampeaoNaoEncontradoError(Exception):
    """Levantada quando o id não corresponde a nenhum campeão do Data Dragon"""


class DataDragonIndisponivelError(Exception):
    """Levantada quando o Data Dragon não responde ou responde com erro"""


class LLMIndisponivelError(Exception):
    """Levantada quando o provedor de IA não responde ou responde com erro"""
