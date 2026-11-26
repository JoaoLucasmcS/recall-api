# Recall API

API BFF da biblioteca de campeões do League of Legends. Consome o Data Dragon (CDN da Riot), trata os dados e entrega no formato que o front ([recall-web](https://github.com/JoaoLucasmcS/recall-web)) precisa.

## Como rodar

```bash
cp .env.example .env.dev   # ajuste os valores se precisar
poetry install
poetry run task run        # sobe em http://127.0.0.1:8000 (docs em /docs)
poetry run task test       # lint + testes + cobertura
```

## Endpoints

| Método | Rota | Descrição |
|---|---|---|
| GET | `/` | Health check |
| GET | `/patch/` | Versão atual do Data Dragon |
| GET | `/campeoes/` | Lista resumida (id, nome, título, classes, imagem) |
| GET | `/campeoes/{campeao_id}` | Detalhe: história, atributos, dicas, passiva, habilidades, skins e splash |

Erros: `404` para campeão inexistente; `503` quando o Data Dragon não responde.

## Decisões de Arquitetura (ADR) — Recall API V1

### 1. Arquitetura BFF (rota → service → client)
- Decisão: Foi decidido construir uma API BFF.
- Por quê: Pois os dados que vou consumir são estáticos (CDN) fornecido pela Data Dragon. Dessa forma o backend faz a gestão da consulta dos dados e tratamento e disponibilização dos dados, via API, para deixar no formato esperado pelo front. 
- Trade-off: Como estou adicionando  uma camada no meio do DataDragon e do front, perdemos em latência.
- Reavaliar quando: Não pretendo reavaliar pois o BFF é a fundação dessa V1.

### 2. Sem banco de dados na V1
- Decisão: Não adotei um banco de dados próprio para aplicação.
- Por quê: Pois os arquivos JSON com os dados necessários já estão sendo disponibilizados via CDN e os dados não mudam dentro do mesmo patch, ou seja, taxa de atualização baixa e volume baixo então não se faz necessário guardarmos esses dados novamente em algum lugar.  
- Trade-off: Perdemos no poder de consulta, pois as consultas em um banco bem modelado ganha "processamento" e recurso do que fazer todo o tratamento na "mão".
- Reavaliar quando: Na V2 quando for necessário guardar informações até quando o processo "morrer", ou seja, quando a aplicação restartar.

### 3. Cache em memória (dicionário no processo)
- Decisão: Adotei a estrutura de guardar os dados em cache - memória. 
- Por quê: Para não sobrecarregar em processamento minha aplicação, seria inviável se a cada requisição ele fosse baixar os dados no CDN, tratasse e devolvesse. Para isso adotamos o cache guardado em memória. Descartei o uso de redis, pois não precisamos guardar caches de múltiplas instâncias.
- Trade-off: Quando a aplicação restartar, o que acontece nos deploys grátis (free tier) os dados guardados na memória do backend são perdidos, dessa forma no cold start (primeira requisição pós reset) tende a demorar mais tempo, já que nessa primeira requisição vão ser baixado os dados novamente e guardados em cache (dicts em memória). Por não usar o Redis se minha aplicação tiver duas ou mais instâncias, cada instância vai ter seu próprio cache em memória.
- Reavaliar quando: Talvez na v2 quando precisarmos guardar algum dado que não pode sumir pós reset, ou até quando os dados forem de tamanho elevado a ponto de atrasar muito pós reset. Caso minha API escale para múltiplas instâncias é válido considerar o uso de Redis
- Implementação: os caches (`core/cache.py`) e um único `httpx.AsyncClient` são criados uma vez no `lifespan` da aplicação e guardados no `app.state`, então vivem enquanto a API estiver de pé e são compartilhados por todas as requisições. O client compartilhado também reaproveita as conexões com o Data Dragon (keep-alive), evitando um handshake TLS a cada requisição.
- Limitação conhecida: logo após a API subir, duas requisições simultâneas podem encontrar o cache vazio e baixar o mesmo arquivo (cache stampede). Para o volume do Recall é irrelevante; se virar problema, resolve com um `asyncio.Lock` por chave.

### 4. Dois caches com invalidação diferente
- Decisão: Os dados a respeito dos campeões são invalidados por patch, ou seja, se tiver um patch mais atualizado ele vai realizar a consulta novamente. Já a lista dos patchs consultamos de 6 em 6h.
- Por quê: Pois precisamos consultar a lista dos patchs para saber se tem algum mais atualizado, a fim de atualizar os dados dos campeões como consequência. 
- Trade-off: Para o cache de campeões não temos perda pois os dados dentro dos patchs são imutáveis. Já para o cache das versões, temos um atraso de até 6h, pois é o tempo que demora para verificar se possui algum patch mais atualizado. 
- Reavaliar quando: Se caso a aplicação escalar em um nível onde o uso passar a exigir dado no minuto do lançamento, nesse caso 6h seria muito tempo para ter os dados desatualizados. 
- Implementação: `CacheVersao` guarda a versão mais recente e o momento da busca (`time.monotonic()`, que não sofre com ajustes no relógio do servidor) e só consulta o `versions.json` de novo depois de 6h. `CacheCampeoes` guarda os JSONs por chave (`lista:{idioma}`, `detalhe:{idioma}:{id}`) junto com a versão a que pertencem; quando a versão atual muda, ele se esvazia. Respostas de erro (404/503) não são guardadas, porque a exceção interrompe antes de o valor ser salvo.

### 5. Exceções próprias no client, tradução para HTTP na borda
- Decisão: O `DataDragonClient` levanta exceções do projeto (`CampeaoNaoEncontradoError`, `DataDragonIndisponivelError`) e quem as traduz para respostas HTTP (404, 503) é a camada web: o router, para o 404, e um `exception_handler` global no `app.py`, para o 503.
- Por quê: O client é meu, então sou eu quem define o que ele comunica para cima. Se ele levantasse `HTTPException` estaria acoplado ao HTTP do front, e na V2 o mesmo client vai ser usado por um servidor MCP, que não fala HTTP. O 503 fica num handler global porque o Data Dragon pode falhar dentro de uma dependência (ao buscar a versão atual), antes de a rota rodar, onde o `try/except` do router não alcança.
- Trade-off: Duas classes de exceção a mais para manter e dois lugares onde a tradução acontece (router e handler).
- Reavaliar quando: Se surgirem muitos tipos de erro, vale centralizar toda a tradução em handlers globais.

### 6. Settings estrito
- Decisão: O `Settings` (pydantic-settings) não usa `extra='ignore'`: qualquer variável no arquivo `.env` que não exista na classe impede a API de subir.
- Por quê: Pega sobras e erros de digitação na hora (foi assim que o antigo `VERSAO` esquecido no `.env.dev` apareceu), em vez de serem ignorados em silêncio.
- Trade-off: Ao remover uma configuração do código é preciso lembrar de removê-la também dos `.env` locais. Só vale para o arquivo `.env`; variáveis de ambiente do sistema que não estão na classe continuam sendo ignoradas.
- Reavaliar quando: Se o mesmo `.env` passar a ser compartilhado com outras ferramentas.

## Testes

Os testes (`tests/`) usam um Data Dragon falso (`httpx.MockTransport`, em `conftest.py`) que responde como a CDN real e registra cada URL pedida. Assim dá para testar os endpoints, os erros 404/503 e o comportamento dos caches (quantas vezes cada arquivo foi baixado) sem depender da rede.

---

Recall não é endossado pela Riot Games e não reflete as opiniões da Riot Games nem de ninguém oficialmente envolvido na produção ou gestão de League of Legends. League of Legends e Riot Games são marcas comerciais ou marcas registradas da Riot Games, Inc. League of Legends © Riot Games, Inc.
