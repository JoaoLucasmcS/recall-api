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

### 4. Dois caches com invalidação diferente
- Decisão: Os dados a respeito dos campeões são invalidados por patch, ou seja, se tiver um patch mais atualizado ele vai realizar a consulta novamente. Já a lista dos patchs consultamos de 6 em 6h.
- Por quê: Pois precisamos consultar a lista dos patchs para saber se tem algum mais atualizado, a fim de atualizar os dados dos campeões como consequência. 
- Trade-off: Para o cache de campeões não temos perda pois os dados dentro dos patchs são imutáveis. Já para o cache das versões, temos um atraso de até 6h, pois é o tempo que demora para verificar se possui algum patch mais atualizado. 
- Reavaliar quando: Se caso a aplicação escalar em um nível onde o uso passar a exigir dado no minuto do lançamento, nesse caso 6h seria muito tempo para ter os dados desatualizados. 
