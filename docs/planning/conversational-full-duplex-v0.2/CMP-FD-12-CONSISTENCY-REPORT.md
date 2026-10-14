# CMP-FD-12 v0.2 — Relatório de consistência do autor

**Isto não é parecer Codex e não é PASS.** É a checagem que o autor fez antes de pedir auditoria. Nenhum teste de software foi executado.

| Checagem | Resultado do autor |
|---|---|
| Nove AQ aprovadas tratadas como APPROVED e não reabertas | sim, CMP-FD-00 e CMP-FD-08 |
| AQ-04, AQ-09, AQ-12 tratadas como UNDECIDED | sim |
| FDP-14, FDP-15, baseline, BUILD-00 pendentes | sim |
| Arquivos v1.7, v0.3, v0.1, pareceres e ata não editados por este pacote | sim, só o diretório novo |
| `build_id` e `task_id` continuam NOT NULL na proposta | sim, CMP-FD-01 §3 |
| `InvokeCapability` histórico não é dado ao roteador | sim, comando separado |
| Impersonação de `coding_engine` recusada | sim, O15 |
| Mesmo lock order e mesma prova `forge.provider_ingest` | sim |
| Sem segundo ledger e sem recibo fictício | sim |
| Sem quarta família de adapter | sim |
| `cmp.speech.v0` referenciado, não sobrescrito | sim, crosswalk |
| Half-duplex não é fallback silencioso | sim, handshake |
| Overlap exige interseção e chunk reproduzido, não fim lógico | sim, predicado §4 e O13 |
| Duck, stop local e cancel são distintos | sim, CMP-FD-03 |
| Epoch concorrente e quatro pontos de corte | sim |
| Registry manda no trust, não o adapter | sim |
| Proveniência da v0.3 restaurada no contrato de saída | sim |
| CMP-O-28 referenciado e não substituído | sim, O12 e O27 |
| 12 oráculos antigos conservados; novos começam em O13 | sim, até O34 |
| 36 CMP-O e 91 oráculos v1.7 permanecem NOT RUN | sim |
| Limiares de latência não numéricos | sim, O29 |
| Histórias com owner PENDING e DoR NOT MET | sim |
| Nenhum finding marcado fechado | sim, CMP-FD-10 |
| Nenhum fornecedor nomeado | sim |
| Nenhum gasto, staging ou BUILD-00 | sim |

## Tensões deixadas visíveis de propósito

1. A v0.3 ainda descreve half-duplex como suficiente para a versão dela. Este pacote não a reescreve. A decisão posterior do Founder está no ADR e na ata. Um leitor que leia só a v0.3 verá o texto antigo. Isso é correto.
2. O ADR AQ-07, no momento em que foi escrito, ainda listava as outras AQ como pendentes. A ata posterior aprovou oito. Os dois documentos históricos ficam como estão.
3. O status `SESSION_ACTIVE` não existe no arquivo FDP-16A. Existe como proposta. Tratar a proposta como se o check histórico já a aceitasse seria inconsistente. O texto diz o contrário.
4. Liberar reservation antes do dispatch, quando não há prova de não-chamada, continua bloqueado pela v1.7. O pacote prefere HELD a inventar `NO_EFFECT`. Isso pode segurar orçamento de uma sessão cancelada cedo. É a guarda de AQ-12, não um furo esquecido.
5. A matriz nega modelo externo para CONFIDENTIAL e RESTRICTED embora a ata tenha nomeado speech externo. A extensão é deny-by-default para não abrir desvio. Não é escolha de vendor. O Codex pode discordar da extensão; ela está explícita.

Se qualquer linha da primeira tabela estiver errada no texto, o veredito continua com o revisor. O autor não converte esta página em PASS.
