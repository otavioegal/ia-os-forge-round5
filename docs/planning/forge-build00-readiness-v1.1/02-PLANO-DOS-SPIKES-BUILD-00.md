# Proposta de função e esforço — spikes BUILD-00

**Estado:** proposta candidata. Não aprovada. Não executada. Não autoriza BUILD-00.

Claude Code é o Builder proposto, não um Builder já aprovado. A função da tabela é o papel de execução proposto para a investigação. Codex é o revisor proposto da evidência, ao final de cada spike. Quem investiga não aprova o próprio resultado. Nenhuma prova real está autorizada por este texto. O resultado esperado continua sendo o do FDP-20, inclusive a coluna de falha; a tabela abaixo não a substitui.

O texto histórico do FDP-20 ainda diz que papel e timebox de cada spike estão pendentes. Esse arquivo não foi reescrito. Atribuir uma função aqui não nomeia uma pessoa e não calibra o esforço.

| Spike | Função proposta | Estimativa inicial | Por que esta função | Resultado que o FDP-20 já define |
|---|---|---:|---|---|
| SPIKE-01 — Tauri / stream do sidecar Node | Desktop | 4–8 h | Faixa S já definida | Frames de fixture ordenados; preview sem IPC privilegiado |
| SPIKE-02 — adaptador Codex | Integration | 4–8 h | Faixa S já definida | describe, invoke, cancel e status numa tarefa sintética |
| SPIKE-03 — adaptador Claude Code | Integration | 4–8 h | Faixa S já definida | Mesmo contrato; segredo resolvido ausente dos logs |
| SPIKE-04 — handoff do envelope | Orchestration | 4–8 h | Faixa S já definida | Mesmo task id, novo attempt, mesmo operation_ref, sem execução adicional |
| SPIKE-05 — dois worktrees | Desktop | 4–8 h | Faixa S já definida | Escrita isolada por tarefa e conflito detectado |
| SPIKE-06 — impacto no Project Graph | Backend | 4–8 h | Mesmo papel de F-003, que é Backend. A faixa de 3–6 h da v1.0 não existia na tabela; passa a usar S, a menor faixa já definida | Mesmo conjunto de nós na mesma revisão; projeto alheio excluído |
| SPIKE-07 — sincronização tldraw | UX | 4–8 h | Faixa S já definida | Round trip preserva node ids; edge ilegal é rejeitada |
| SPIKE-08 — PGMQ | Backend | 4–8 h | Faixa S já definida | Uma vencedora entre duas claims; epoch antigo é negado |
| SPIKE-09 — escopo do shell | Desktop | 4–8 h | Mesmo papel de F-007, que é Desktop e cobre a allowlist de comandos | Comando allowlisted funciona dentro da raiz; traversal e comando fora da lista falham |

**Estimativa dos nove spikes:** 36–72 horas ativas. A v1.0 somava 35–70 porque o SPIKE-06 estava em 3–6. Essa faixa foi retirada. Nove vezes 4–8 horas dá 36–72. Não somar este valor às horas das histórias: um resultado de spike pode ser reaproveitado depois, e esta proposta não calcula essa sobreposição.

**Limite de cada faixa:** o número de cima é o máximo inicial de horas ativas daquele spike. Não é data. Se o limite chegar sem evidência conclusiva, pausar e reestimar. Não dispensar o spike e não convertê-lo em PASS. Nenhuma data de calendário é criada aqui.

A divergência entre o Builder proposto e o caminho AIOX, descrita no modelo, também fica pendente para estes spikes. Este plano não escolhe qual dos dois prevalece.
