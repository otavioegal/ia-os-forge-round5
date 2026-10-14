# Riscos — DELTA CONVERSATIONAL-MVP v0.3

**Estado:** DELTA CONVERSATIONAL-MVP v0.3 — CANDIDATE FOR CODEX REVIEW. DRAFT / NOT APPROVED / NOT READY FOR BUILD / NO BUILD-00 AUTHORIZATION. Registro de risco da especificação. Não é teste executado. Não autoriza BUILD-00.

| ID | Risco | Mitigação especificada | Residual |
|---|---|---|---|
| R-01 | Troca de interlocutor ou memória de sessão vaza outro projeto ou outra org | Context builder reconstruído a cada turno; oráculos CMP-O-06 e CMP-O-08 | Depende de AQ-02 não virar atalho de task compartilhada |
| R-02 | Conselho, Jarvis ou review formal reutiliza processo, runtime, instância ou credencial do Builder | Contrato CMP-03 inalterado; CMP-O-28 da v0.3 exige ids host-attested distintos e falha mesmo com principal nominal codex_reviewer | F-017 da v1.7 não foi emendado; o oráculo ainda está NOT RUN |
| R-03 | Fala “aprovo” vira deploy, gasto, segredo ou comando destrutivo | GATE_PREVIEW separado; oráculos CMP-O-22 a CMP-O-25 | O gate real continua sendo o da v1.7; este delta não o implementa |
| R-04 | Áudio gravado personifica o usuário | Sem biometria; user id é a sessão; AQ-11 | Ambiente físico não é controlado pela especificação |
| R-05 | Retry depois do dispatch chama o provider outra vez | Tabela CMP-02 §9; CMP-O-15, CMP-O-16, CMP-O-29 e CMP-O-35 | AQ-01 aberta: sem o comando de reserva, o risco é implementação furar o gateway |
| R-06 | Provider externo recebe áudio classificado ou guarda áudio sem consentimento | Consentimento antes da captura; default sem objeto de áudio; deny por classe | AQ-05: o enum ainda não está decidido |
| R-07 | Queda de áudio é usada para tirar voz do MVP | `voice_required` não volta a false; Retry; CMP-O-15 e CMP-O-16 | Sem vendor, o primeiro teste pode nascer degradado se ninguém contratar um adapter permitido |
| R-08 | Segundo ledger ou prova falada | Um protocolo, FDP-16A 8A–8A.3; adapter não é capturer | AQ-12: vendor sem recibo deixa reserva HELD de propósito |
| R-09 | Latência apresentada como SLA | Números só como planning default, no mesmo tipo de `session_max_age_ms` | Alguém pode citar 200 ms como medida; o texto proíbe isso |
| R-10 | Percentual ou custo inventado na UI | Ausência explícita; eventos sem corpo de prompt; nenhuma cifra medida neste pacote | Dashboard futuro fora deste delta |
| R-11 | FDP-11 citado como se existisse | Lacuna em CMP-06; snapshot histórico intocado | FDP-15 continua citando §161–165 que não estão na árvore; isso é dívida histórica, não corrigida aqui |
| R-12 | Acoplamento indevido ao Founder OS | Só referência de experiência; AQ-09 | Sem baseline compartilhada, dois UIs podem divergir |
| R-13 | LOW-01 editorial do Round 10, em FDP-17:31, corrigido de carona | FDP-17 não foi editado | A frase “v1.6 matrix” continua no arquivo auditado até um commit editorial separado. Não confundir com o LOW-01 de consentimento do parecer CMP v0.1, tratado na v0.2 |
| R-14 | Model router manda dado interno ao OpenRouter | OpenRouter não é fallback implícito; classificação antes do fallback | AQ-04 aberta |
| R-15 | Consenso fabricado no Conselho | Divergência append-only; ata não pode dizer que houve acordo se a divergência existe | O modelo ainda pode falar “concordamos” na boca; a ata é que não pode gravar isso como fato |

Nenhum risco acima foi demonstrado em software. Nenhum foi fechado por teste.
