# CMP-FD-05 v0.4 — UX e proveniência

**Estado:** PROPOSTA. Não é PASS. Não reescreve CMP-01 v0.3.
**MEDIUM-04** permanece fechado pelo Codex. Os campos abaixo continuam obrigatórios.

Em `ACTIVE_DUPLEX`, escuta e fala podem ser verdadeiras juntas. Não há botão de turno como único modo. Texto permanece visível. `voice_required` não vira false quando a voz cai.

Saída de agente: `turn_id`, `speaker_agent_id`, `origin`, `source_turn_ids` não vazio na síntese de Jarvis, `evidence_refs` quando o rótulo é `FACT`, `epistemic_label` em `FACT`, `INFERENCE`, `SUGGESTION` ou `ABSENCE`. Um speaker por turno. Preâmbulo de áudio igual ao nome da tela.

Conselho não fabrica acordo se há divergência. Codex de sala não inicia review formal. CMP-O-28 não é substituído por CMP-FD-O27 nem por CMP-FD-O28.

AQ-08: abertura expressa, grant separado da âncora financeira, escuta contínua só na sessão ativa, indicador desligado fora dela.
