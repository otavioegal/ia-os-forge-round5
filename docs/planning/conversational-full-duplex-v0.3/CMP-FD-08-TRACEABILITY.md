# CMP-FD-08 v0.3 — Rastreabilidade

**Estado:** índice. Não é parecer e não é PASS. Nenhum oráculo foi executado.

## Decisões

| ID | Estado | Onde a v0.3 obedece |
|---|---|---|
| AQ-01 | APPROVED | comando próprio do `conversation_router`, sem impersonar `coding_engine` |
| AQ-02 | APPROVED | uma task por sessão, `build_id` NOT NULL, fora do DAG, sem deploy/terminal/vault |
| AQ-03 | APPROVED | TOOL e MODEL nas três famílias; sem quarta família |
| AQ-05 | APPROVED | quatro classes; default de projeto não é PUBLIC |
| AQ-06 | APPROVED | áudio `DO_NOT_STORE`; prazo de transcrição não inventado |
| AQ-07 | APPROVED | overlap físico; half-duplex não passa |
| AQ-08 | APPROVED | mic só na sessão; epoch e generation |
| AQ-10 | APPROVED | um teto pai, mesmo ledger, sem segundo débito |
| AQ-11 | APPROVED | voz não passa hard gate |
| AQ-04, AQ-09, AQ-12 | UNDECIDED | sem fornecedor, sem Founder OS, sem recibo fictício |

## Findings do Codex sobre a v0.2

| Finding | Onde a proposta responde | Fechado pelo autor? |
|---|---|---|
| HIGH-01 parcial | CMP-FD-01, CMP-FD-13 | não |
| HIGH-02 parcial | CMP-FD-02 seção 7, CMP-FD-07 seções 3–5 | não |
| HIGH-03 parcial | CMP-FD-02 seções 2–6 e 11 | não |
| LOW-01 parcial | CMP-FD-07 seção 1 | não |
| NEW-HIGH-01 | CMP-FD-01 seções 2–5, oráculo O36 | não |
| NEW-HIGH-02 | CMP-FD-01 seção 4, oráculo O35 | não |
| NEW-HIGH-03 | CMP-FD-01 fase B, oráculo O37 | não |
| NEW-MEDIUM-01 | `expected_task_version` e `expected_build_version`, O38 | não |
| NEW-MEDIUM-02 | timestamps dentro de `observation`, O01 | não |
| NEW-MEDIUM-03 | FX-AEC-01, O28 | não |
| MEDIUM-01..05 | CMP-FD-03 a CMP-FD-06, preservados | já estavam CLOSED pelo Codex; o autor não os usa como prova |

## Oráculos

| Conjunto | Estado nesta entrega |
|---|---|
| 91 oráculos v1.7 | não executados |
| CMP-O-01..36, inclusive CMP-O-28 | NOT RUN, evidence ABSENT |
| CMP-FD-O01..O34 | NOT RUN, evidence ABSENT |
| CMP-FD-O35..O40 | NOT RUN, evidence ABSENT |

CMP-FD-O28 é eco/VAD. CMP-O-28 é independência do review. Nomes parecidos, objetos diferentes. Nenhum dos dois substitui o outro.

## Gates

FDP-14 PENDING. FDP-15 PENDING. Consolidação da baseline PENDING. BUILD-00 não autorizado.
