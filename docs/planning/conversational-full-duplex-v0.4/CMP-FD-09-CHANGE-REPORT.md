# CMP-FD-09 v0.4 — Change report

**Estado:** PROPOSTA. Não é PASS. Nenhum arquivo fora de `docs/planning/conversational-full-duplex-v0.4/` foi alterado por esta rodada.

## Adicionado

Pasta nova, com os dezoito caminhos do índice CMP-FD-00. O contrato financeiro que a v0.3 deixou só no estimate passa a ter checagem de fatia no settlement. A Reservation passa a carregar org e projeto. O replay de comando passa a ser lookup durável antes do CAS. O preâmbulo deixa de ter um único `HELLO_ACK`. Os oito eventos da FX-01 saem do Markdown e vão para JSON com vetor de digest. O microfone da fixture de AEC passa a ser soma com saturação. A sessão aberta deixa de ser única só pelo UUID.

## Não alterado

- FDP-16A v1.7, inclusive o trecho `:322-324`. O delta conversacional é só nesta pasta.
- FDP-15 histórico. Sem quarta família de adapter.
- CMP v0.3 e `cmp.speech.v0`. O crosswalk está em CMP-FD-02:138-151 e não substitui o contrato de fala.
- `docs/planning/conversational-full-duplex/`, `...-v0.2/` e `...-v0.3/`.
- Ata, ADR AQ-07 e todos os pareceres.
- Nenhuma migration foi aplicada. CMP-FD-13 é especificação.
- Nenhum provider foi chamado. Nenhum segredo foi mudado. BUILD-00 não começou.

## Flag

`forge.conversation.delta.v3` nasce desligada. `forge.conversation.delta.v2` não é ligada e não é integrada. O Codex pediu para não integrar a v2; esta pasta não a promove.

## Decisões que o texto novo toma, e que o Codex pode recusar

1. `held` da fórmula inclui o estimate corrente. A conta subtrai E uma vez.
2. Se a fatia não comporta e o root comporta, a razão do pending é `SESSION_SLICE`, não `OVER_ESTIMATE`.
3. Se os dois não comportam, a razão é só `OVER_ESTIMATE`.
4. Elevar a fatia é `AmendSessionSlice`, humano, e não liquida.
5. Sessão com pending não vai a `SESSION_CLOSED`; fica `ORPHAN_HELD` ou `CLOSING`, e a fatia continua na soma.
6. `command_digest` inclui as versions esperadas do comando. Replay byte a byte continua válido depois que o banco andou.
7. `consent_stop_deadline_ns` e `observation_tolerance_ns` ficam fora do envelope. A outra opção do prompt, colocá-los no schema, não foi a escolhida.
8. `overlap_epsilon_ns = 0` continua constante da FX-01, não a chave de configuração.
9. Limites 1000 e 400 do AEC são `FIXTURE_CONSTANT`, não SLA.

Nenhuma dessas nove é fechamento de finding. São o texto candidato.
