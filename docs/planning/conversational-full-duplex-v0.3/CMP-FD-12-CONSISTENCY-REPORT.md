# CMP-FD-12 v0.3 — Relatório de consistência do autor

**Checagem estática de texto. Não é teste de software. Não é PASS. Não substitui o Codex.**

| Checagem | Resultado no momento da redação |
|---|---|
| Ata: nove AQ aprovadas e três não decididas | reproduzidas no índice e na rastreabilidade |
| `OpenConversationalAnchor` não aceita `budget_limit_minor` | campo desconhecido na fase A; O40 |
| Headroom só depois de `SELECT build FOR UPDATE` | CMP-FD-01 fase D, passo 5, depois de C1 |
| Dois estimates distintos serializam no mesmo Build | O35 |
| Soma de fatias não excede o teto pai | invariante 3 e O36 |
| `expected_task_version` e `expected_build_version` não nulos | fase A, passo 7; O38 |
| `404` de escopo sem corpo que vaze o outro tenant | fase B; O37 |
| Seis timestamps são campos de `observation` | CMP-FD-02 seção 7 |
| `OUTPUT` não carrega `reproduced_at_ns`; quem carrega é `PLAYBACK_SPAN` | matriz de nulabilidade e FX-01 |
| `HELLO` tem schema de preâmbulo | CMP-FD-02 seção 2 |
| `echo=true` não é entrada de O28 | FX-AEC-01 |
| Histórias com pessoa PENDING e DoR NOT MET | CMP-FD-07 seção 1 |
| CMP-O-28 distinto de CMP-FD-O28 | rastreabilidade |
| 91, 36 e 40 oráculos de full-duplex (O01–O40) NOT RUN | este pacote não traz evidência |
| MEDIUM-01..05 sem afrouxar duck/cancel, epoch, trust, proveniência ou SLA | CMP-FD-03..06 |
| Rollback não apaga movement, prova, outbox nem audit | CMP-FD-13 |
| Nenhum arquivo fora de `conversational-full-duplex-v0.3/` é proposto para edição | relatório de mudança |
| BUILD-00, FDP-14, FDP-15, baseline | pendentes |

Contradição procurada e evitada: a v0.2 lia headroom na mesma lista em que ainda não tinha o lock. A v0.3 separa as fases. Se algum leitor achar uma frase residual mandando ler saldo antes de C1, essa frase perde para a seção 4 de CMP-FD-01.

Contradição procurada e evitada: fixture com carimbo que o schema rejeita. G1 como `OUTPUT` tem `reproduced_at_ns` null. A reprodução está no `PLAYBACK_SPAN`.

Não foi executado: parser de schema, teste de concorrência, migration, suíte de oráculos, build, provider.
