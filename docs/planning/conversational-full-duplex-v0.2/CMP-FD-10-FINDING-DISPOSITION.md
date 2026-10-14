# CMP-FD-10 v0.2 — Disposição dos findings

**Regra:** o autor não fecha finding. A coluna final é sempre aberta para o Codex.

| ID | O que o parecer exigiu | Onde está o material | Autodeclaração |
|---|---|---|---|
| HIGH-01 | Delta de schema, enum, comando, caller/callee, grants, transação, erros, dedupe, âncora com `build_id` NOT NULL fora do DAG, órfãs, proibição de deploy/terminal/vault | CMP-FD-01 | NÃO FECHADO |
| HIGH-02 | Fixture com relógio, dois fluxos, interseção positiva, chunks nos dois sentidos, playback depois do primeiro input, negativo de pause-before-capture, gerado versus reproduzido | CMP-FD-07 §2–§4, O01, O13, O14 | NÃO FECHADO |
| HIGH-03 | Schema tipado e crosswalk com `cmp.speech.v0` | CMP-FD-02 | NÃO FECHADO |
| MEDIUM-01 | Máquinas separadas, duck ≠ stop ≠ cancel, retry sem redespacho incerto | CMP-FD-03 | NÃO FECHADO |
| MEDIUM-02 | Epoch, corte concorrente, quatro pontos de observação | CMP-FD-04 §1–§3, O19–O22 | NÃO FECHADO |
| MEDIUM-03 | Trust validado pelo registry, rechecagem em todo egress, matriz das quatro classes | CMP-FD-04 §4–§5, O23–O26 | NÃO FECHADO |
| MEDIUM-04 | `turn_id`, speaker, sources, evidence, rótulos, Codex read-only, CMP-O-28 preservado | CMP-FD-05, O12, O27 | NÃO FECHADO |
| MEDIUM-05 | Pontos de medida agora; limiares pendentes de calibração | CMP-FD-06, O29 | NÃO FECHADO |
| LOW-01 | Fixtures exatas; histórias sem fingir DoR | CMP-FD-07 | NÃO FECHADO |

O FAIL v0.1 continua sendo o veredito daquele SHA. Este arquivo não o revoga.

Independência: CMP-FD-O12 referencia CMP-O-28 e declara que não o substitui. CMP-O-28 segue NOT RUN.

Gates que o parecer listou e que este pacote não cumpre sozinho:

1. O Codex ainda precisa aceitar ou recusar HIGH-01, HIGH-02 e HIGH-03.
2. O delta de FDP-16A/FDP-15 está proposto, não incorporado aos arquivos históricos.
3. FDP-14 sem deliberação.
4. FDP-15 sem deliberação.
5. Baseline consolidada sem aprovação.
6. Owner, effort e DoR das histórias continuam pendentes de propósito.
7. Os oráculos CMP-FD não foram executados.
8. Os 36 CMP-O não foram executados.
9. Os 91 oráculos v1.7 não foram executados nesta revisão.
10. BUILD-00 não foi autorizado.
