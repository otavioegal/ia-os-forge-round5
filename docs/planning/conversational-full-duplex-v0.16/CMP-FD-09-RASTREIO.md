# CMP-FD-09 v0.16 — Rastreio

**Estado:** CANDIDATE FOR CODEX REVIEW. Não é PASS. Nenhuma linha foi executada.

Legenda de estado do requisito: PROPOSTA, salvo quando a linha diz que o comportamento em si já está aprovado e só a forma é proposta.

| Requisito | Cumpre | Onde | Não é |
|---|---|---|---|
| REQ-IND-01 | DEC-IND, DEC-SESSAO | CMP-FD-02 | Concessão de poder |
| REQ-IND-02 | DEC-IND, DEC-COERENTE | CMP-FD-02 | Texto como sucata da voz |
| REQ-IND-03 | DEC-VOZ, DEC-TEXTO | CMP-FD-02 | Voz obrigatória em toda frase |
| REQ-IND-04 | DEC-COERENTE | CMP-FD-02 | Medição de latência |
| REQ-IND-05 | DEC-IND, DEC-COERENTE | CMP-FD-02 | Jarvis fantasiando outro papel |
| REQ-IND-06 | DEC-IND | CMP-FD-02 | Lista inventada |
| REQ-IND-07 | DEC-COERENTE | CMP-FD-02 | Uma tela diferente por agente |
| REQ-SALA-01 | DEC-SALA, DEC-COERENTE | CMP-FD-03 | Acordo automático |
| REQ-SALA-02 | DEC-SALA | CMP-FD-03 | Sala anônima |
| REQ-SALA-03 | DEC-SALA, identificação do ADR | CMP-FD-03 | Várias vozes juntas |
| REQ-SALA-04 | ADR, não fabricar acordo | CMP-FD-03 | Ata que apaga divergência |
| REQ-SALA-05 | DEC-DUPLEX; pedido nominal é proposta | CMP-FD-03 | Turno obrigatório |
| REQ-SALA-06 | DEC-CODEX | CMP-FD-03 | Decisão do Founder ou parecer |
| REQ-SALA-07 | ADR, sem fan-out pago | CMP-FD-03 | Taxa escondida |
| REQ-SALA-08 | DEC-CODEX | CMP-FD-03 | Revisão formal pelo chat |
| REQ-NAT-01 | DEC-DUPLEX | CMP-FD-04 | Meia-duplex |
| REQ-NAT-02 | DEC-FORGE, AQ-09 guarda | CMP-FD-04 | Memória do outro sistema |
| REQ-NAT-03 | DEC-DUPLEX | CMP-FD-04 | Recomeçar do zero |
| REQ-NAT-04 | Identificação aprovada | CMP-FD-04 | Cor ou biometria |
| REQ-NAT-05 | Jornada antiga, rótulo visível | CMP-FD-04 | Informação só no áudio |
| REQ-NAT-06 | DEC-DUPLEX | CMP-FD-04 | SLA em milissegundos |
| REQ-CORTE-01 | DEC-DUPLEX | CMP-FD-05 | Esperar o fim da frase |
| REQ-CORTE-02 | DEC-DUPLEX | CMP-FD-05 | Apagar o já dito |
| REQ-CORTE-03 | DEC-DUPLEX | CMP-FD-05 | Sessão nova a cada corte |
| REQ-CORTE-04 | Proposta de eco | CMP-FD-05 | Autointerrupção pelo alto-falante |
| REQ-CORTE-05 | Proposta de ruído | CMP-FD-05 | Limiar escolhido pelo Founder |
| REQ-CORTE-06 | DEC-TETO | CMP-FD-05 | Estorno fingido |
| REQ-CORTE-07 | DEC-DUPLEX e acessibilidade | CMP-FD-05 | Botão como único modo |
| REQ-PASSA-01 | DEC-IND | CMP-FD-06 | Troca muda |
| REQ-PASSA-02 | Contexto autorizado | CMP-FD-06 | Copiar tudo |
| REQ-PASSA-03 | DEC-SIGILO, DEC-FORGE | CMP-FD-06 | Founder OS |
| REQ-PASSA-04 | Proposta de resumo | CMP-FD-06 | Notas escondidas |
| REQ-PASSA-05 | DEC-GASTO | CMP-FD-06 | Privilégio emprestado |
| REQ-PASSA-06 | DEC-IND | CMP-FD-06 | Convite no lugar da resposta |
| REQ-PASSA-07 | DEC-CODEX | CMP-FD-06 | Frase atribuída ao Codex |
| REQ-TELA-01 | Proposta de lugares | CMP-FD-07 | Tela já construída |
| REQ-TELA-02 | DEC-DUPLEX | CMP-FD-07 | Um spinner único |
| REQ-TELA-03 | DEC-SESSAO, DEC-TEXTO | CMP-FD-07 | Voz retirada |
| REQ-TELA-04 | DEC-TEXTO | CMP-FD-07 | Provider escondido |
| REQ-TELA-05 | Proposta de queda de rede | CMP-FD-07 | Resposta inventada |
| REQ-TELA-06 | DEC-SIGILO | CMP-FD-07 | Voz externa de confidencial |
| REQ-TELA-07 | DEC-AUDIO | CMP-FD-07 | Gravação prometida |
| REQ-TELA-08 | Jornada de fontes | CMP-FD-07 | Porcentagem decorativa |
| REQ-TELA-09 | DEC-GRAVE | CMP-FD-07 | "Eu aprovo" falado |
| REQ-TELA-10 | DEC-SESSAO | CMP-FD-07 | Escuta de fundo |
| REQ-TELA-11 | DEC-TETO | CMP-FD-07 | Saldo inventado |
| REQ-TELA-12 | Recusa visível | CMP-FD-07 | Sucesso falso |
| ACE-01 | REQ-IND-01, REQ-IND-02, REQ-IND-03 | CMP-FD-08 | Teste executado |
| ACE-02 | REQ-IND-05, REQ-IND-07 | CMP-FD-08 | Jarvis assinando outro agente |
| ACE-03 | REQ-SALA-01, REQ-SALA-02, REQ-SALA-03 | CMP-FD-08 | Sala sem nomes |
| ACE-04 | REQ-SALA-04 | CMP-FD-08 | Acordo fabricado |
| ACE-05 | REQ-CORTE-01, REQ-CORTE-02, REQ-CORTE-03 | CMP-FD-08 | Meia-duplex |
| ACE-06 | REQ-NAT-02, REQ-NAT-03, REQ-PASSA-03 | CMP-FD-08 | Memória de outro projeto |
| ACE-07 | REQ-PASSA-01, REQ-PASSA-04, REQ-PASSA-05 | CMP-FD-08 | Privilégio emprestado |
| ACE-08 | REQ-TELA-03, DEC-TEXTO | CMP-FD-08 | Voz retirada do produto |
| ACE-09 | REQ-TELA-04 | CMP-FD-08 | Provider escondido |
| ACE-10 | REQ-TELA-05 | CMP-FD-08 | Prova de rede |
| ACE-11 | REQ-TELA-09, DEC-GRAVE | CMP-FD-08 | Frase falada como botão |
| ACE-12 | REQ-TELA-10, DEC-SESSAO | CMP-FD-08 | Escuta de fundo |
| ACE-13 | REQ-TELA-08 | CMP-FD-08 | Status inventado |
| ACE-14 | REQ-TELA-06, DEC-SIGILO | CMP-FD-08 | Prova de egress |

Fontes que este pacote não altera:

- `docs/governance/ATA-FOUNDER-AQS-CONVERSATIONAL-2026-10-13.md`
- `docs/governance/ADR-FDR-AQ07-FULL-DUPLEX-MVP-2026-10-13.md`
- `docs/planning/conversational-mvp-v0.3/CMP-01-PRD-UX-JOURNEYS.md` (fotografia; ainda fala em meia-duplex)
- `docs/planning/conversational-full-duplex-v0.3/CMP-FD-05-UX.md` (escuta e fala juntas já propostas)
- `docs/planning/conversational-full-duplex/CMP-FD-01-FULL-DUPLEX-ARCHITECTURE.md`
- Pacote v0.15 `f016b1a4a32b460ee9948c2dc71f171a9146e61a`

A v0.16 não entra no manifesto histórico da v0.15. Incluí-la lá reescreveria pacote publicado.
