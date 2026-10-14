# Riscos — DELTA CONVERSATIONAL-MVP v0.1

**Estado:** DELTA CONVERSATIONAL-MVP v0.1 — CANDIDATE FOR CODEX REVIEW. DRAFT / NOT APPROVED / NOT READY FOR BUILD / NO BUILD-00 AUTHORIZATION. Registro de risco da especificação. Não é teste executado. Não autoriza BUILD-00.

| ID | Risco | Mitigação especificada | Residual |
|---|---|---|---|
| R-01 | Troca de interlocutor ou memória de sessão vaza outro projeto ou outra org | Context builder reconstruído a cada turno; oráculos CMP-O-06 e CMP-O-08 | Depende de AQ-02 não virar atalho de task compartilhada |
| R-02 | Conselho ou explicação do Jarvis contamina o revisor | Pack do Codex sem scratch do Builder; `review.sign` negado; parecer imutável por chat | Um parecer futuro mal armazenado ainda precisa do gate F-017, que este delta não substitui |
| R-03 | Fala “aprovo” vira deploy, gasto, segredo ou comando destrutivo | GATE_PREVIEW separado; oráculos CMP-O-22 a CMP-O-25 | O gate real continua sendo o da v1.7; este delta não o implementa |
| R-04 | Áudio gravado personifica o usuário | Sem biometria; user id é a sessão; AQ-11 | Ambiente físico não é controlado pela especificação |
| R-05 | Retry de STT/TTS ou Conselho chama o provider duas vezes | `operation_ref` por turno e capability; CMP-O-29 e CMP-O-31 | AQ-01 aberta: sem o comando de reserva, o risco é implementação furar o gateway |
| R-06 | Provider externo recebe áudio classificado ou guarda áudio sem consentimento | Consentimento antes da captura; default sem objeto de áudio; deny por classe | AQ-05: o enum ainda não está decidido |
| R-07 | Queda de áudio é usada para tirar voz do MVP | `voice_required` não volta a false; Retry; CMP-O-15 e CMP-O-16 | Sem vendor, o primeiro teste pode nascer degradado se ninguém contratar um adapter permitido |
| R-08 | Segundo ledger ou prova falada | Um protocolo, FDP-16A 8A–8A.3; adapter não é capturer | AQ-12: vendor sem recibo deixa reserva HELD de propósito |
| R-09 | Latência apresentada como SLA | Números só como planning default, no mesmo tipo de `session_max_age_ms` | Alguém pode citar 200 ms como medida; o texto proíbe isso |
| R-10 | Percentual ou custo inventado na UI | Ausência explícita; eventos sem corpo de prompt; nenhuma cifra medida neste pacote | Dashboard futuro fora deste delta |
| R-11 | FDP-11 citado como se existisse | Lacuna em CMP-06; snapshot histórico intocado | FDP-15 continua citando §161–165 que não estão na árvore; isso é dívida histórica, não corrigida aqui |
| R-12 | Acoplamento indevido ao Founder OS | Só referência de experiência; AQ-09 | Sem baseline compartilhada, dois UIs podem divergir |
| R-13 | LOW-01 corrigido “de carona” e a baseline auditada muda de byte | FDP-17 não foi editado | A frase “v1.6 matrix” continua no arquivo auditado até um commit editorial separado |
| R-14 | Model router manda dado interno ao OpenRouter | OpenRouter não é fallback implícito; classificação antes do fallback | AQ-04 aberta |
| R-15 | Consenso fabricado no Conselho | Divergência append-only; ata não pode dizer que houve acordo se a divergência existe | O modelo ainda pode falar “concordamos” na boca; a ata é que não pode gravar isso como fato |

Nenhum risco acima foi demonstrado em software. Nenhum foi fechado por teste.
