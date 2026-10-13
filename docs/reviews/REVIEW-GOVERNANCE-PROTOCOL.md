# Protocolo de governanca das revisoes — IA OS Forge

Status: REGISTRO OPERACIONAL. Nao altera nem aprova a baseline tecnica.

O repositorio `otavioegal/ia-os-forge-round5` e o registro compartilhado das revisoes documentais do IA OS Forge a partir da quinta rodada. Cada rodada concluida deve registrar: (1) baseline documental entregue pelo Builder, identificada por numero e versao; (2) parecer integral independente do Codex, sem edicao de seu conteudo; (3) findings com severidade, evidencias e situacao; (4) correcoes com rastreabilidade e changelog; (5) resultados da checagem documental, separados de testes de software; (6) historico integral imutavel das rodadas anteriores; (7) indice da rodada e pendencias de Founder/BUILD/staging.

Fluxo: Grok entrega alteracoes em uma nova versao candidata -> organizacao incorpora os artefatos em commit identificavel -> Codex revisa a versao fixada pelo commit -> parecer e registrado sem substituir originais -> findings abertos voltam ao Grok para a proxima rodada. Repetir ate nao haver findings documentais impeditivos. Findings que dependam de software ou staging ficam explicitamente em gates posteriores, sem serem considerados testes executados.

Regras: nao usar push --force, reset destrutivo nem sobrescrever pareceres/historicos; conferir git status, commit hash e integridade antes de anunciar sucesso. Repositorio e fonte de registro das revisoes, nao banco de dados de producao. Nenhum parecer autoriza BUILD-00 nem substitui aprovacao expressa do Founder. Esta rotina sera aplicada quando as proximas entregas estiverem disponiveis e a coordenacao for acionada; nao pressupoe acesso autonomo continuo ao Grok.

Round 5: `docs/reviews/PARECER-CODEX-ROUND5-2026-10-13.md` — FAIL documental, 6 HIGH e 5 MEDIUM. O parecer foi produzido em checkout read-only isolado; arquivo preservado integralmente.