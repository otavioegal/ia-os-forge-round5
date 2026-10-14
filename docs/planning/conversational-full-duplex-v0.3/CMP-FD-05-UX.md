# CMP-FD-05 v0.3 — UX full-duplex e proveniência

**Estado:** PROPOSTA. Não substitui CMP-01 v0.3. Onde o CMP v0.3 ainda descreve push-to-talk como experiência suficiente, a ata e o ADR AQ-07 prevalecem para a decisão humana, sem reescrever o CMP v0.3.
**Achado:** MEDIUM-04 foi marcado CLOSED documentalmente pelo Codex na v0.2. As regras abaixo são as mesmas. O autor não declara fechamento.
**Campos de proveniência** estão também no envelope tipado de CMP-FD-02 v0.3.


## 1. O que a pessoa vê durante o simultâneo

Estados de CMP-01 §3.1 que deixam de ser mutuamente exclusivos no áudio:

- `LISTENING` e `SPEAKING` podem ser verdadeiros juntos enquanto a sessão está `ACTIVE_DUPLEX`.
- O compositor mostra os dois indicadores: captura ligada **dentro da sessão** e playback do agente.
- Não há botão de turno obrigatório. O botão de interrupção da v0.3 pode existir como acessibilidade, mas o MVP falha se ele for o único modo (CMP-FD-O11).
- Texto continua sempre visível. Voz indisponível degrada para texto com `voice_required` verdadeiro.

Identidade, herdada e tornada campo de contrato:

- Um speaker por turno de saída.
- Nome do papel na tela antes das palavras.
- Preâmbulo de áudio com a mesma string (“Architect.”), não semelhança acústica.
- `speaker_agent_id` obrigatório no envelope de saída (CMP-FD-02).
- `turn_id` obrigatório fora do handshake e do `START_SESSION`.

Conselho:

- Lista de participantes e de quem fala agora.
- Divergência é registro próprio. A UI não escreve “o conselho concorda” se existe divergência.
- Intervenção humana tem prioridade: `USER_SPEECH_START` durante fala de agente entra na máquina CMP-FD-03 sem esperar o fim da frase.
- Paralelismo de mídia não dispara N modelos de uma vez.

Codex na sala fala como participante read-only. A UI não oferece “pedir parecer formal” nesse turno. Review formal continua outro principal, outro processo, outra credencial, CMP-O-28.

## 2. Proveniência que a v0.1 tinha enfraquecido

Estes campos voltam a ser obrigatórios na saída de agente, não só `speaker_agent_id`:

| Campo | Regra herdada |
|---|---|
| turn_id | um por turno |
| speaker_agent_id | o agente que fala, não Jarvis por omissão |
| origin | `AGENT` ou `CODEX_READ_ONLY` ou `SYSTEM` |
| source_turn_ids | não vazio na síntese de Jarvis (CMP-02 v0.3) |
| evidence_refs | obrigatório se o rótulo é `FACT` |
| epistemic_label | `FACT`, `INFERENCE`, `SUGGESTION` ou `ABSENCE` |

Minuta de conselho continua `conversation_minutes(id, session_id, authored_turn_id, source_turn_ids[], evidence_refs[], divergence_ids[], claim_class)`. `FACT` é ilegal se alguma fonte não é `FACT` ou se falta ref. Divergência não pode ser apagada por uma ata de acordo.

Síntese de Jarvis não atribui ao Codex frase que o turno `CODEX_READ_ONLY` não contém. Isso é CMP-FD-O27. Não é o CMP-O-28.

Troca de interlocutor continua a jornada D: pack reconstruído, nota de handoff é `INFERENCE`, capabilities não crescem.

## 3. Ativação

AQ-08 aprovada depois do texto da v0.3:

1. Ação expressa abre a sessão.
2. Grant de microfone é separado da abertura da âncora financeira.
3. Escuta contínua só em `ACTIVE_DUPLEX` com generation corrente.
4. Fora disso o indicador está desligado, inclusive com o microfone do sistema operacional aberto para outro aplicativo (CMP-FD-O06).

## 4. Acessibilidade

Texto permanece alternativa. Falha de voz mostra erro recuperável. Não remove full-duplex do contrato do MVP e não declara o modo turn-taking como equivalente.
