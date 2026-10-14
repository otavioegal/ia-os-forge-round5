# Tabela executiva — decisões do Founder ainda abertas

**Estado:** DELTA CONVERSATIONAL-MVP v0.3 — CANDIDATE FOR CODEX REVIEW. DRAFT / NOT APPROVED / NOT READY FOR BUILD / NO BUILD-00 AUTHORIZATION.
**Esta tabela não é decisão.** Nenhuma linha está aprovada, recusada ou adiada pelo Founder. A coluna “proposta” é recomendação do pacote para deliberação. Silêncio não é aceite.

O parecer Codex da v0.2 pediu decisão humana expressa nas nove AQ abaixo antes de integrar o delta à baseline. AQ-04, AQ-09 e AQ-12 podem continuar diferidas só com as guardas já escritas. Fornecedor de voz não é escolhido aqui.

## Nove decisões pedidas antes da integração

| AQ | Proposta / default deste pacote | Risco se a integração ignorar | Consequência da escolha | Estado |
|---|---|---|---|---|
| AQ-01 | Ator `conversation_router` e um comando cujo efeito de reserva é o da transação já existente. O roteador não finge ser `coding_engine`. | Gasto fora do gateway ou um segundo ledger. | Sem isso, implementação de voz que gasta não pode chamar provider. | ABERTO — NÃO DECIDIDO |
| AQ-02 | Uma Task âncora por sessão, fora do DAG de build, sem deploy, terminal ou vault. `task_id` continua NOT NULL. | Conversa misturada ao build, ou operação sem task. | A âncora não vira READY_FOR_HUMAN_TEST e não recebe ferramentas de código. | ABERTO — NÃO DECIDIDO |
| AQ-03 | `speech.transcribe` e `speech.synthesize` como capabilities TOOL, junto com a deliberação de FDP-15. Sem quarta família. | Contradição com as três famílias do rascunho ainda não aprovado. | Trocar de fornecedor não muda o contrato `cmp.speech.v0`. | ABERTO — NÃO DECIDIDO |
| AQ-05 | Rótulos PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED. Conteúdo de projeto não é PUBLIC até decisão contrária. CONFIDENTIAL e RESTRICTED não saem para speech externo. | Áudio classificado enviado a provider externo. | O enum continua proposta. Não é cláusula histórica. | ABERTO — NÃO DECIDIDO |
| AQ-06 | Áudio bruto `DO_NOT_STORE`, salvo opt-in futuro. Transcrição conforme política da organização. Sem prazo eterno e sem número de dias. | Áudio retido sem regra, ou retenção tratada como já medida. | Text-only continua legal com consentimento de microfone NOT_GRANTED. | ABERTO — NÃO DECIDIDO |
| AQ-07 | Meia-duplex com STT/TTS e barge-in local satisfaz “áudio de baixa latência” neste delta. Full-duplex não está contratado. 200 ms, 15 s e 800 ms são default de planejamento, não SLA. | Voz adiada de novo, ou um número citado como medida. | Confirmar ou exigir full-duplex é ato do Founder. A voz não sai do MVP em nenhum dos dois casos. | ABERTO — NÃO DECIDIDO |
| AQ-08 | Ativação explícita ou push-to-talk. Escuta contínua não é o default. | Microfone sempre ligado sem consentimento. | Always-on, se um dia for pedido, continua sujeito a consentimento e classificação. | ABERTO — NÃO DECIDIDO |
| AQ-10 | O teto é o ledger existente, `spent + reserved <= limit`. Sem envelope paralelo e sem preço de sessão. | Tarifa oculta de Conselho ou dupla cobrança. | Não cria segundo protocolo de dinheiro. | ABERTO — NÃO DECIDIDO |
| AQ-11 | Biometria fora do MVP. Gravação não autentica e não renova assurance. | Áudio tratado como identidade. | Confirmar a exclusão evita um fornecedor de voz como fator de login. | ABERTO — NÃO DECIDIDO |

## Três questões que podem esperar

| AQ | Guarda que permanece vinculante | O que não está decidido | Estado |
|---|---|---|---|
| AQ-04 | Deny-by-default. Grok e OpenRouter não entram na allowlist de engines de código por causa da conversa. | Qual modelo responde. Nenhum vendor foi escolhido. | ABERTO — DIFERÍVEL, NÃO DECIDIDO |
| AQ-09 | Sem banco, sessão ou código compartilhado com Founder OS. | Se um dia haverá baseline visual comum. | ABERTO — DIFERÍVEL, NÃO DECIDIDO |
| AQ-12 | Sem prova ingerível por `forge.provider_ingest`, a reserva fica HELD. Não se inventa recibo. | Qual vendor de voz terá atestação. | ABERTO — DIFERÍVEL, NÃO DECIDIDO |

Nenhuma célula acima é resposta do Founder. FDP-14, FDP-15, a integração do delta e BUILD-00 continuam pendentes e separados desta tabela.
