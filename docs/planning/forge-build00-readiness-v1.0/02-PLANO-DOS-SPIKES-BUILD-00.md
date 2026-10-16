# Proposta de alocação e esforço — spikes BUILD-00

Claude Code é o Builder responsável. O papel AIOX indicado executa a investigação. Codex revisa a evidência ao final de cada spike. Todas as provas usam fixtures ou ambiente isolado; nenhuma integração real é acionada nesta etapa de planejamento.

| Spike | Função AIOX responsável | Esforço inicial | Resultado esperado já definido no FDP-20 |
|---|---|---:|---|
| SPIKE-01 — Tauri / stream do sidecar Node | Desktop | 4–8 h | Frames de fixture ordenados; preview sem IPC privilegiado |
| SPIKE-02 — adaptador Codex | Integration | 4–8 h | describe, invoke, cancel e status numa tarefa sintética |
| SPIKE-03 — adaptador Claude Code | Integration | 4–8 h | Mesmo contrato; segredo resolvido ausente dos logs |
| SPIKE-04 — handoff do envelope | Orchestration | 4–8 h | Mesmo task id, novo attempt, mesmo operation_ref, sem execução adicional |
| SPIKE-05 — dois worktrees | Desktop | 4–8 h | Escrita isolada por tarefa e conflito detectado |
| SPIKE-06 — impacto no Project Graph | Data | 3–6 h | Mesmo conjunto de nós na mesma revisão; projeto alheio excluído |
| SPIKE-07 — sincronização tldraw | UX | 4–8 h | Round trip preserva node ids; edge ilegal é rejeitada |
| SPIKE-08 — PGMQ | Backend | 4–8 h | Uma vencedora entre duas claims; epoch antigo é negado |
| SPIKE-09 — escopo do shell | Security | 4–8 h | Comando allowlisted funciona dentro da raiz; traversal e comando fora da lista falham |

**Esforço estimado dos nove spikes:** 35–70 horas ativas. Não somar este valor às 552–1.104 horas das histórias: alguns resultados dos spikes podem ser reutilizados no trabalho posterior.

**Timebox:** o limite superior da faixa de cada linha é o máximo inicial de horas ativas daquele spike. Encerrar quando houver o pass/fail e os artefatos previstos. Se o limite for alcançado sem evidência conclusiva, pausar e reestimar; não dispensar o spike nem convertê-lo em PASS. Esta proposta não agenda data de calendário.