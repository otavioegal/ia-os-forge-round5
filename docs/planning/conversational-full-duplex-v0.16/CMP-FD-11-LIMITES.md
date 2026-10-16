# CMP-FD-11 v0.16 — Limites

**Estado:** CANDIDATE FOR CODEX REVIEW. Não é PASS.

## O que este pacote faz

Traduz decisões já tomadas para jornadas, estados, falhas e um roteiro que o Founder consegue ler. Marca proposta onde o mecanismo ainda era detalhe de revisão.

## O que este pacote não faz

- Não altera arquivo anterior.
- Não reescreve a v0.15 nem o SHA `f016b1a4a32b460ee9948c2dc71f171a9146e61a`.
- Não reescreve o CMP v0.3, a baseline v1.7, atas, ADRs nem pareceres.
- Não escolhe fornecedor, modelo, SDK nem preço. AQ-04 continua diferida.
- Não liga o Forge ao Founder OS. AQ-09 continua diferida, com a guarda de não compartilhar banco, código, sessão nem memória.
- Não inventa recibo de custo. AQ-12 continua diferida. Incerteza de gasto continua sem recibo fictício.
- Não executa código de produto, teste, PostgreSQL, migration, deploy, provider, gasto nem BUILD-00.
- Não mede latência nem qualidade de voz.
- Não fecha finding e não declara cobertura de produto.
- Não transforma ACE-01..14 em oráculo executado.
- Não promove o parecer v0.2 a VERIFIED e não preenche `chosen_verdict`.
- Não recupera os prompts ausentes da v0.6 e da v0.7. Ausência legítima permanece ausência.
- Não usa 480/2239 nem 508/2443 como prova de uso.

## Como o Codex deve ler uma tensão antiga

O CMP-01 da v0.3 ainda diz que meia-duplex com botão bastava, e que o microfone padrão era apertar para falar. Isso é fotografia daquela versão. O ADR posterior rejeitou a meia-duplex. A v0.3 de UX do full-duplex já tinha proposto escuta e fala ao mesmo tempo dentro da sessão ativa. Esta v0.16 repete esse resultado em linguagem de uso e não afrouxa: o botão de interromper pode existir, mas não é o único modo.

## Questões que continuam abertas

LOW-01, NEW-GOV-01, HIGH-03, FD07-07, O92, O93, NEW-MEDIUM-09, FDP-14, FDP-15, baseline, BUILD-00, AQ-04, AQ-09, AQ-12, errata humana do parecer v0.2, e a ratificação da referência semântica. Nenhuma delas é transferida ao Founder como escolha de mecanismo desta jornada.

O Founder não é chamado a decidir fornecedor, milissegundos, limiar de ruído, nome interno de evento nem formato de banco.
