# Parecer independente pós-correções Round 3

**Veredito: FAIL**

As correções restauraram vários elementos literais, mas o conjunto ainda não constitui baseline implementável. Permanecem falhas de fidelidade semântica, contradições normativas, traceability incompleta, contratos de execução insuficientes e runbooks não testáveis.

Nenhum teste ou procedimento foi executado. Nenhuma autorização de BUILD-00, build ou produção decorre deste parecer.

## Resultado dos itens solicitados

| Item | Resultado | Conclusão |
|---|---|---|
| Enum literal de `Task` | **SANADO** | Os 11 estados de FDP-12 foram reproduzidos corretamente em [FDP-16:17](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-16-v1.0-AIOX-EXECUTION-ENGINES-REVISED.md:17>), correspondendo à fonte em [FDP-12:1134](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/source-material/chat-extracts/FDP-12-v1.0__msg074.md:1134>). |
| 17 casos P0 | **PARCIAL** | Os 17 IDs aparecem na extensão da matriz, mas `AUTHZ-01` e `SEC-01` tiveram sua semântica alterada. |
| SPIKE-01..09 | **SANADO COM RESSALVA** | Títulos e tópicos agora correspondem a FDP-10 e receberam hipóteses, fixtures, oráculos e outputs. O texto ainda os chama de descrições provisórias “a reconciliar”. |
| Frozen stack | **PARCIAL** | FDP-20 está fiel; FDP-18 continua omitindo quatro componentes congelados e toda a classificação P1/deferred, exceto Temporal. |
| `COST-01` | **NÃO SANADO** | Foi acrescentada uma associação a F-015, mas F-015 não contém controle de orçamento e a tabela anterior conflitante continua normativa. |
| Wrappers FDP-12/13 | **SANADO** | Ambos apontam para os extratos literais preservados. |
| Contratos implementáveis | **NÃO SANADO** | FDP-16 permanece um outline arquitetural, sem schemas e protocolos suficientes para implementação inequívoca. |
| Traceability completa | **NÃO SANADO** | A matriz não cobre todas as histórias nem todos os testes suplementares e contém linhas contraditórias. |
| Runbooks testáveis | **NÃO SANADO** | São templates narrativos; faltam valores, comandos, precondições e procedimentos reproduzíveis. |

## Falhas residuais

### HIGH — Semântica de casos P0 não preservada

A fonte define:

- `AUTHZ-01 org isolation` em [FDP-13:2273](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/source-material/chat-extracts/FDP-13-v1.0__msg077.md:2273>);
- `SEC-01 secrets not logged` em [FDP-13:2279](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/source-material/chat-extracts/FDP-13-v1.0__msg077.md:2279>).

Os documentos corrigidos redefinem:

- `AUTHZ-01` como autorização de role/capability em [FDP-17:11](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-17-v1.0-TESTING-STRATEGY-REVISED.md:11>) e [Matriz:44](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-TRACEABILITY-MATRIX-v1.0.md:44>);
- `SEC-01` como acesso não autorizado ao vault em [FDP-17:17](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-17-v1.0-TESTING-STRATEGY-REVISED.md:17>) e [Matriz:46](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-TRACEABILITY-MATRIX-v1.0.md:46>).

Ter o ID presente não basta: os dois oráculos literais originais continuam sem preservação inequívoca.

### HIGH — `COST-01` continua inconsistente e sem deliverable implementável

A fonte exige `hard budget blocks spend` em [FDP-13:2287](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/source-material/chat-extracts/FDP-13-v1.0__msg077.md:2287>).

Há duas associações conflitantes:

- tabela original: somente `F-021`, S01, em [Matriz:14](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-TRACEABILITY-MATRIX-v1.0.md:14>);
- extensão: `F-015, F-021`, S01/S06, em [Matriz:59](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-TRACEABILITY-MATRIX-v1.0.md:59>).

Entretanto:

- F-015 é apenas “Tool Gateway authorization/dedupe” e nem lista `COST-01`: [FDP-19:21](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-19-v1.0-PRODUCT-BACKLOG-REVISED.md:21>);
- F-021 continua P2, “dashboard and alerts”: [FDP-19:27](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-19-v1.0-PRODUCT-BACKLOG-REVISED.md:27>).

Portanto, não existe história P0 que especifique ledger atômico, reserva de orçamento, decisão deny-before-spend e comportamento concorrente do hard cap.

### HIGH — Frozen stack ainda inconsistente entre FDP-18 e FDP-20

A fonte congelada inclui Git/worktrees, n8n e Codex + Claude Code em [FDP-10:2177](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/source-material/chat-extracts/FDP-10-v1.0__msg068.md:2177>).

FDP-20 reproduz corretamente frozen/P1/deferred em [FDP-20:37](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-20-v1.0-SPRINT-IMPLEMENTATION-PLAN-REVISED.md:37>).

FDP-18, porém, omite Git/worktrees, n8n e Codex + Claude Code da lista congelada, além de não reproduzir Grok/OpenRouter/workers como P1 nem Neo4j/Redis/Kafka/Kubernetes como deferred: [FDP-18:4](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-18-v1.0-DEPLOYMENT-ROLLBACK-REVISED.md:4>).

Dois documentos normativos continuam descrevendo baselines diferentes.

### HIGH — Contratos de execução ainda não são implementáveis

FDP-16 enumera campos de Build, Task, Attempt e Operation em [FDP-16:9](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-16-v1.0-AIOX-EXECUTION-ENGINES-REVISED.md:9>), mas não define:

- tipos, obrigatoriedade, constraints e versionamento dos schemas;
- matriz completa `estado atual × comando → novo estado`;
- payload e versionamento de comandos/eventos;
- efeitos transacionais e outbox por transição;
- protocolo concreto de claim/heartbeat/lease/fencing;
- taxonomia de erro e política de retry por classe;
- resolução de operação `IN_FLIGHT/UNKNOWN` após falha;
- contratos de API entre Controller, Task Service e Attempt Manager.

O próprio texto posterga normalização para ADR futuro em [FDP-16:18](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-16-v1.0-AIOX-EXECUTION-ENGINES-REVISED.md:18>). Isso impede tratar o documento como contrato pronto para implementação.

### HIGH — Traceability não cobre o backlog nem os próprios acceptance contracts

A matriz não possui linha própria para numerosas histórias, incluindo F-003, F-004, F-005, F-008–010, F-012–014, F-017–019, F-022–025, F-032 e F-038.

Também faltam linhas verificáveis para vários testes declarados obrigatórios por FDP-17: `SECRET-01`, `ENV-01`, `DEPLOY-03`, `SAFE-01`, `QUEUE-01`, `SUPPLY-01`, `KILL-01`, `WATCH-01` e `DONE-01`, listados em [FDP-17:36](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-17-v1.0-TESTING-STRATEGY-REVISED.md:36>).

Isso contradiz a afirmação de FDP-16 de que cada acceptance contract possui evidência na matriz: [FDP-16:37](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-16-v1.0-AIOX-EXECUTION-ENGINES-REVISED.md:37>).

As referências também permanecem aproximadas — “section 191, around line 2269” — em [Matriz:40](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-TRACEABILITY-MATRIX-v1.0.md:40>), não requisito-a-requisito.

### HIGH — Runbooks não são procedimentos testáveis

Os cinco cenários operacionais existem em [FDP-18:16](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-18-v1.0-DEPLOYMENT-ROLLBACK-REVISED.md:16>), mas continuam sem:

- thresholds e observation windows concretos;
- origem/query de cada sinal;
- identificadores reais de serviço, release e backup;
- comandos ou chamadas autorizadas;
- precondições e permissões por etapa;
- passos numerados e critérios de abort;
- on-call routing configurado;
- RPO/RTO medidos;
- resultado de restore/rollback drill.

FDP-18 reconhece que esses valores ainda deverão ser registrados e medidos: [FDP-18:29](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-18-v1.0-DEPLOYMENT-ROLLBACK-REVISED.md:29>). Logo, são especificações de futuros runbooks, não runbooks executáveis.

### MEDIUM — Backlog promete DoR que as linhas não contêm

FDP-19 afirma que cada história possui fonte, aceitação positiva/negativa, evidência, risco e esforço em [FDP-19:3](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-19-v1.0-PRODUCT-BACKLOG-REVISED.md:3>).

As linhas F-001..F-041, porém, trazem somente prioridade, resumo, owner, dependência e teste, por exemplo [FDP-19:7](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-19-v1.0-PRODUCT-BACKLOG-REVISED.md:7>). A alegação de DoR completo não é sustentada pelo documento.

### MEDIUM — Spikes corrigidos, mas ainda declarados provisórios

Os nove tópicos agora correspondem literalmente à fonte FDP-10: [FDP-10:2046](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/source-material/chat-extracts/FDP-10-v1.0__msg068.md:2046>) e [FDP-20:21](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-20-v1.0-SPRINT-IMPLEMENTATION-PLAN-REVISED.md:21>).

Os contratos adicionais em [FDP-20:50](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-20-v1.0-SPRINT-IMPLEMENTATION-PLAN-REVISED.md:50>) são adequados como especificação de planejamento. Contudo, [FDP-20:18](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/planning/FDP-20-v1.0-SPRINT-IMPLEMENTATION-PLAN-REVISED.md:18>) ainda afirma que precisam ser reconciliados e são descrições de trabalho “to confirm”. Essa ressalva deve ser removida ou convertida em confirmação explícita da reconciliação já realizada.

## Itens efetivamente sanados

- Enum Task literal completo.
- Tópicos literais dos nove spikes e contratos mínimos de avaliação.
- Inclusão nominal dos 17 IDs P0.
- Separação dos cinco KPIs/evals na extensão da matriz.
- Wrappers FDP-12 e FDP-13 agora apontam para as fontes preservadas: [FDP-12 wrapper:5](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/architecture/FDP-12-DATA-ARCHITECTURE.md:5>) e [FDP-13 wrapper:5](</C:/Users/User/Desktop/Otávio Rodrigues Digital Group/AI OS Forge/docs/security/FDP-13-SECURITY-ARCHITECTURE.md:5>).
- Frozen stack completo em FDP-20.
- Todos os casos continuam corretamente marcados `NOT RUN`.

## Próximos passos obrigatórios

1. Corrigir `AUTHZ-01` e `SEC-01` para preservar os oráculos literais; criar novos IDs para capability authorization e vault access.
2. Criar um deliverable P0 explícito para hard budget enforcement e eliminar as duas linhas conflitantes de `COST-01`.
3. Reproduzir em FDP-18 a mesma classificação frozen/P1/deferred de FDP-10 e FDP-20.
4. Produzir schemas versionados e contratos completos de comando, evento, transição, lease, fencing, retry e recovery.
5. Consolidar a matriz em uma única tabela normativa, cobrindo F-001..F-041 e todos os testes obrigatórios, com referência exata à fonte.
6. Transformar cada história em registro DoR/DoD verificável ou remover a alegação de que esses campos já existem.
7. Converter RB-APP/RB-SCHEMA/RB-RUNNER/RB-DESKTOP/RB-SECRET em procedimentos versionados, reproduzíveis e ensaiados em staging.
8. Registrar thresholds, windows, on-call, RPO/RTO e resultados dos drills antes de qualquer certificação de release readiness.
9. Manter FDP-14 sujeito à confirmação do Founder e FDP-15 pendente de aprovação.
10. Submeter nova auditoria independente após as correções; não declarar `READY FOR BUILD` ou autorizar BUILD-00 antes disso.