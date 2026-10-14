# CMP-FD-07 v0.3 — Histórias, fixtures e oráculos

**Estado:** especificação de teste futuro. **Nenhum caso foi executado.** Evidence ABSENT. NOT RUN. Não é PASS.
**Não é DoR cumprida.** Há papel proposto e processo de nomeação. Não há pessoa nomeada. Effort segue UNSTATED. DoR segue NOT MET.
**IDs:** CMP-FD-O01..O34 continuam. CMP-FD-O35..O40 são novos. Não colidem com CMP-O-01..36 nem com CMP-O-28.

## 1. Histórias — LOW-01 permanece aberto

Sete histórias. Nenhuma está pronta para implementação. O autor não inventa dono.

| ID | Título | Papel proposto | Pessoa | Effort | DoR |
|---|---|---|---|---|---|
| CMP-FD-S01 | Duplex universal, inclusive agente só de texto | Conversational Product Spec Owner | PENDING | UNSTATED | NOT MET |
| CMP-FD-S02 | Interrupção com cancel e custo preservado | Conversational Product Spec Owner | PENDING | UNSTATED | NOT MET |
| CMP-FD-S03 | Conselho com identidade e prioridade humana | Conversational Product Spec Owner | PENDING | UNSTATED | NOT MET |
| CMP-FD-S04 | Mic, retenção, classe e ledger único | Privacy Spec Owner | PENDING | UNSTATED | NOT MET |
| CMP-FD-S05 | Âncora, teto pai e reserva | Ledger Spec Owner | PENDING | UNSTATED | NOT MET |
| CMP-FD-S06 | Epoch de consentimento concorrente | Privacy Spec Owner | PENDING | UNSTATED | NOT MET |
| CMP-FD-S07 | Trust boundary e matriz das quatro classes | Policy Spec Owner | PENDING | UNSTATED | NOT MET |

Processo, ainda não executado:

1. Um ato humano posterior do Founder nomeia uma pessoa para o papel. Este pacote não é esse ato e não escolhe nome.
2. Essa pessoa registra effort como inteiro de planejamento. Enquanto isso não acontece, effort permanece UNSTATED.
3. DoR só poderia ser discutido como MET se, ao mesmo tempo, houvesse pessoa nomeada e effort registrado. Executar oráculo continua fora desta entrega. FDP-14, FDP-15, baseline e BUILD-00 continuam decisões separadas.
4. Checklist, toda desmarcada: owner humano, effort, dependência do schema v0.3, ausência de blocker de tenant e de teto, fixtures identificadas.
5. Sem os passos 1 e 2, DoR = NOT MET. Nomear o papel não completa a história.

## 2. Relógio da FX-01

Fixture `CMP-FD-FX-01`. Um processo. `clock_domain_id = fx01-single-process`. `overlap_epsilon_ns = 0`. Constante de fixture, não SLA.

Os intervalos são calculados dos eventos da seção 3:

- `output_playback_start` = menor `reproduced_at_ns` de `PLAYBACK_SPAN` = `100000000` (G0).
- `input_capture_start` = menor `captured_at_ns` de `INPUT_AUDIO_CHUNK` aceito = `300000000` (I0).
- `input_capture_end` = maior `captured_at_ns + duration_ns` de chunk aceito = `650000000 + 20000000` = `670000000` (I1).
- `output_playback_end` = maior `reproduced_at_ns` com `playback_state` `PLAYING` ou `DUCKED` = `880000000` (G2). Não há `STOPPED`.
- interseção = `[300000000, 670000000]`. O span de G1 em `400000000` cai dentro. O span de G0 abre o playback e fica antes da interseção.

## 3. Eventos imutáveis

Cada objeto inclui `event_digest` do algoritmo de CMP-FD-02, calculado sem esse campo. Recalcular e divergir falha a fixture antes do overlap. `OUTPUT_AUDIO_CHUNK` traz `reproduced_at_ns` null. A reprodução é o `PLAYBACK_SPAN` seguinte, com o mesmo `content_sha256` e `source_sequence`.

G0 OUTPUT

```json
{
  "schema_id": "cmp.media.duplex.v1",
  "contract_version": "cmp.media.duplex.v1",
  "event_type": "OUTPUT_AUDIO_CHUNK",
  "event_id": "e1000000-0000-4000-8000-0000000000a1",
  "organization_id": "11111111-1111-4111-8111-111111111101",
  "project_id": "11111111-1111-4111-8111-111111111102",
  "session_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1",
  "stream_id": "22222222-2222-4222-8222-222222222222",
  "sequence": 1,
  "sequence_scope": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1/22222222-2222-4222-8222-222222222222",
  "direction": "OUTPUT",
  "ack_of_sequence": null,
  "gap_policy": "REJECT_GAP",
  "participant_id": "ffffffff-ffff-4fff-8fff-fffffffffff2",
  "turn_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbb2",
  "invocation_id": "cccccccc-cccc-4ccc-8ccc-ccccccccccc2",
  "speaker_agent_id": "dddddddd-dddd-4ddd-8ddd-ddddddddddd1",
  "origin": "AGENT",
  "source_turn_ids": [],
  "evidence_refs": [],
  "epistemic_label": null,
  "media_plane": "LOCAL_PIPELINE",
  "consent_ref": "99999999-9999-4999-8999-999999999999",
  "consent_grant_epoch": 1,
  "capture_generation": 1,
  "data_classification": "INTERNAL",
  "execution_location": "LOCAL",
  "trust_boundary": "GATEWAY",
  "operation_ref": "cmp:bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbb2:speech.synthesize",
  "is_final": false,
  "stream_end": false,
  "discontinuity": false,
  "payload": {
    "media_encoding": "PCM_S16LE",
    "audio_mime": "audio/wav",
    "sample_rate_hz": 16000,
    "channels": 1,
    "duration_ns": 20000000,
    "payload_mode": "CONTENT_REF",
    "payload_bytes": null,
    "content_ref": "ephemeral:fx01:g0",
    "content_sha256": "a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0",
    "content_size_bytes": 640
  },
  "observation": {
    "clock_domain_id": "fx01-single-process",
    "generated_at_ns": 40000000,
    "generated_observer": "TTS_ADAPTER",
    "received_at_ns": 80000000,
    "received_observer": "GATEWAY",
    "reproduced_at_ns": null,
    "reproduced_observer": null,
    "captured_at_ns": null,
    "captured_observer": null,
    "gateway_accepted_at_ns": null,
    "gateway_accepted_observer": null,
    "stt_forward_at_ns": null,
    "stt_forward_observer": null
  },
  "event_digest": "850ed372de0f47d47d40b777274dc6eddcb6ab2989a36801d159b1d1871cd04c"
}
```

G0 SPAN

```json
{
  "schema_id": "cmp.media.duplex.v1",
  "contract_version": "cmp.media.duplex.v1",
  "event_type": "PLAYBACK_SPAN",
  "event_id": "e1000000-0000-4000-8000-0000000000a2",
  "organization_id": "11111111-1111-4111-8111-111111111101",
  "project_id": "11111111-1111-4111-8111-111111111102",
  "session_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1",
  "stream_id": "22222222-2222-4222-8222-222222222222",
  "sequence": 2,
  "sequence_scope": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1/22222222-2222-4222-8222-222222222222",
  "direction": "OUTPUT",
  "ack_of_sequence": null,
  "gap_policy": "REJECT_GAP",
  "participant_id": "ffffffff-ffff-4fff-8fff-fffffffffff2",
  "turn_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbb2",
  "invocation_id": "cccccccc-cccc-4ccc-8ccc-ccccccccccc2",
  "speaker_agent_id": "dddddddd-dddd-4ddd-8ddd-ddddddddddd1",
  "origin": "AGENT",
  "source_turn_ids": [],
  "evidence_refs": [],
  "epistemic_label": null,
  "media_plane": "LOCAL_PIPELINE",
  "consent_ref": "99999999-9999-4999-8999-999999999999",
  "consent_grant_epoch": 1,
  "capture_generation": 1,
  "data_classification": "INTERNAL",
  "execution_location": "LOCAL",
  "trust_boundary": "GATEWAY",
  "operation_ref": "cmp:bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbb2:speech.synthesize",
  "is_final": false,
  "stream_end": false,
  "discontinuity": false,
  "payload": {
    "span_role": "CHUNK",
    "playback_state": "PLAYING",
    "content_sha256": "a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0a0",
    "source_sequence": 1
  },
  "observation": {
    "clock_domain_id": "fx01-single-process",
    "generated_at_ns": null,
    "generated_observer": null,
    "received_at_ns": null,
    "received_observer": null,
    "reproduced_at_ns": 100000000,
    "reproduced_observer": "PLAYBACK_SINK",
    "captured_at_ns": null,
    "captured_observer": null,
    "gateway_accepted_at_ns": null,
    "gateway_accepted_observer": null,
    "stt_forward_at_ns": null,
    "stt_forward_observer": null
  },
  "event_digest": "bd56e4057353a017c34dcd24a95e627460edd78f73c8ab4ebb792706e340c140"
}
```

I0 INPUT

```json
{
  "schema_id": "cmp.media.duplex.v1",
  "contract_version": "cmp.media.duplex.v1",
  "event_type": "INPUT_AUDIO_CHUNK",
  "event_id": "e1000000-0000-4000-8000-0000000000b1",
  "organization_id": "11111111-1111-4111-8111-111111111101",
  "project_id": "11111111-1111-4111-8111-111111111102",
  "session_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1",
  "stream_id": "11111111-1111-4111-8111-111111111111",
  "sequence": 1,
  "sequence_scope": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1/11111111-1111-4111-8111-111111111111",
  "direction": "INPUT",
  "ack_of_sequence": null,
  "gap_policy": "REJECT_GAP",
  "participant_id": "ffffffff-ffff-4fff-8fff-fffffffffff1",
  "turn_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbb1",
  "invocation_id": "cccccccc-cccc-4ccc-8ccc-ccccccccccc1",
  "speaker_agent_id": null,
  "origin": "HUMAN",
  "source_turn_ids": [],
  "evidence_refs": [],
  "epistemic_label": null,
  "media_plane": "LOCAL_PIPELINE",
  "consent_ref": "99999999-9999-4999-8999-999999999999",
  "consent_grant_epoch": 1,
  "capture_generation": 1,
  "data_classification": "INTERNAL",
  "execution_location": "LOCAL",
  "trust_boundary": "DEVICE",
  "operation_ref": "cmp:bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbb1:speech.transcribe",
  "is_final": false,
  "stream_end": false,
  "discontinuity": false,
  "payload": {
    "media_encoding": "PCM_S16LE",
    "audio_mime": "audio/wav",
    "sample_rate_hz": 16000,
    "channels": 1,
    "duration_ns": 20000000,
    "payload_mode": "CONTENT_REF",
    "payload_bytes": null,
    "content_ref": "ephemeral:fx01:i0",
    "content_sha256": "c2c2c2c2c2c2c2c2c2c2c2c2c2c2c2c2c2c2c2c2c2c2c2c2c2c2c2c2c2c2c2c2",
    "content_size_bytes": 640
  },
  "observation": {
    "clock_domain_id": "fx01-single-process",
    "generated_at_ns": null,
    "generated_observer": null,
    "received_at_ns": null,
    "received_observer": null,
    "reproduced_at_ns": null,
    "reproduced_observer": null,
    "captured_at_ns": 300000000,
    "captured_observer": "DEVICE",
    "gateway_accepted_at_ns": 310000000,
    "gateway_accepted_observer": "GATEWAY",
    "stt_forward_at_ns": 320000000,
    "stt_forward_observer": "STT_ADAPTER"
  },
  "event_digest": "8348bfbffe533905987410923dafe416db167efc3f1cda59c59fecf8193293ca"
}
```

G1 OUTPUT

```json
{
  "schema_id": "cmp.media.duplex.v1",
  "contract_version": "cmp.media.duplex.v1",
  "event_type": "OUTPUT_AUDIO_CHUNK",
  "event_id": "e1000000-0000-4000-8000-0000000000a3",
  "organization_id": "11111111-1111-4111-8111-111111111101",
  "project_id": "11111111-1111-4111-8111-111111111102",
  "session_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1",
  "stream_id": "22222222-2222-4222-8222-222222222222",
  "sequence": 3,
  "sequence_scope": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1/22222222-2222-4222-8222-222222222222",
  "direction": "OUTPUT",
  "ack_of_sequence": null,
  "gap_policy": "REJECT_GAP",
  "participant_id": "ffffffff-ffff-4fff-8fff-fffffffffff2",
  "turn_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbb2",
  "invocation_id": "cccccccc-cccc-4ccc-8ccc-ccccccccccc2",
  "speaker_agent_id": "dddddddd-dddd-4ddd-8ddd-ddddddddddd1",
  "origin": "AGENT",
  "source_turn_ids": [],
  "evidence_refs": [],
  "epistemic_label": null,
  "media_plane": "LOCAL_PIPELINE",
  "consent_ref": "99999999-9999-4999-8999-999999999999",
  "consent_grant_epoch": 1,
  "capture_generation": 1,
  "data_classification": "INTERNAL",
  "execution_location": "LOCAL",
  "trust_boundary": "GATEWAY",
  "operation_ref": "cmp:bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbb2:speech.synthesize",
  "is_final": false,
  "stream_end": false,
  "discontinuity": false,
  "payload": {
    "media_encoding": "PCM_S16LE",
    "audio_mime": "audio/wav",
    "sample_rate_hz": 16000,
    "channels": 1,
    "duration_ns": 20000000,
    "payload_mode": "CONTENT_REF",
    "payload_bytes": null,
    "content_ref": "ephemeral:fx01:g1",
    "content_sha256": "b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1",
    "content_size_bytes": 640
  },
  "observation": {
    "clock_domain_id": "fx01-single-process",
    "generated_at_ns": 200000000,
    "generated_observer": "TTS_ADAPTER",
    "received_at_ns": 360000000,
    "received_observer": "GATEWAY",
    "reproduced_at_ns": null,
    "reproduced_observer": null,
    "captured_at_ns": null,
    "captured_observer": null,
    "gateway_accepted_at_ns": null,
    "gateway_accepted_observer": null,
    "stt_forward_at_ns": null,
    "stt_forward_observer": null
  },
  "event_digest": "93700e9614a1d89006646c6a9a32f3ed44281c01480f85ca9a54e59068ea2a02"
}
```

G1 SPAN

```json
{
  "schema_id": "cmp.media.duplex.v1",
  "contract_version": "cmp.media.duplex.v1",
  "event_type": "PLAYBACK_SPAN",
  "event_id": "e1000000-0000-4000-8000-0000000000a4",
  "organization_id": "11111111-1111-4111-8111-111111111101",
  "project_id": "11111111-1111-4111-8111-111111111102",
  "session_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1",
  "stream_id": "22222222-2222-4222-8222-222222222222",
  "sequence": 4,
  "sequence_scope": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1/22222222-2222-4222-8222-222222222222",
  "direction": "OUTPUT",
  "ack_of_sequence": null,
  "gap_policy": "REJECT_GAP",
  "participant_id": "ffffffff-ffff-4fff-8fff-fffffffffff2",
  "turn_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbb2",
  "invocation_id": "cccccccc-cccc-4ccc-8ccc-ccccccccccc2",
  "speaker_agent_id": "dddddddd-dddd-4ddd-8ddd-ddddddddddd1",
  "origin": "AGENT",
  "source_turn_ids": [],
  "evidence_refs": [],
  "epistemic_label": null,
  "media_plane": "LOCAL_PIPELINE",
  "consent_ref": "99999999-9999-4999-8999-999999999999",
  "consent_grant_epoch": 1,
  "capture_generation": 1,
  "data_classification": "INTERNAL",
  "execution_location": "LOCAL",
  "trust_boundary": "GATEWAY",
  "operation_ref": "cmp:bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbb2:speech.synthesize",
  "is_final": false,
  "stream_end": false,
  "discontinuity": false,
  "payload": {
    "span_role": "CHUNK",
    "playback_state": "PLAYING",
    "content_sha256": "b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1b1",
    "source_sequence": 3
  },
  "observation": {
    "clock_domain_id": "fx01-single-process",
    "generated_at_ns": null,
    "generated_observer": null,
    "received_at_ns": null,
    "received_observer": null,
    "reproduced_at_ns": 400000000,
    "reproduced_observer": "PLAYBACK_SINK",
    "captured_at_ns": null,
    "captured_observer": null,
    "gateway_accepted_at_ns": null,
    "gateway_accepted_observer": null,
    "stt_forward_at_ns": null,
    "stt_forward_observer": null
  },
  "event_digest": "2f146eb304051b712297d0dbb93d411194cc8c53fee9a2546bd158e6152b4de3"
}
```

I1 INPUT

```json
{
  "schema_id": "cmp.media.duplex.v1",
  "contract_version": "cmp.media.duplex.v1",
  "event_type": "INPUT_AUDIO_CHUNK",
  "event_id": "e1000000-0000-4000-8000-0000000000b2",
  "organization_id": "11111111-1111-4111-8111-111111111101",
  "project_id": "11111111-1111-4111-8111-111111111102",
  "session_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1",
  "stream_id": "11111111-1111-4111-8111-111111111111",
  "sequence": 2,
  "sequence_scope": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1/11111111-1111-4111-8111-111111111111",
  "direction": "INPUT",
  "ack_of_sequence": null,
  "gap_policy": "REJECT_GAP",
  "participant_id": "ffffffff-ffff-4fff-8fff-fffffffffff1",
  "turn_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbb1",
  "invocation_id": "cccccccc-cccc-4ccc-8ccc-ccccccccccc1",
  "speaker_agent_id": null,
  "origin": "HUMAN",
  "source_turn_ids": [],
  "evidence_refs": [],
  "epistemic_label": null,
  "media_plane": "LOCAL_PIPELINE",
  "consent_ref": "99999999-9999-4999-8999-999999999999",
  "consent_grant_epoch": 1,
  "capture_generation": 1,
  "data_classification": "INTERNAL",
  "execution_location": "LOCAL",
  "trust_boundary": "DEVICE",
  "operation_ref": "cmp:bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbb1:speech.transcribe",
  "is_final": false,
  "stream_end": false,
  "discontinuity": false,
  "payload": {
    "media_encoding": "PCM_S16LE",
    "audio_mime": "audio/wav",
    "sample_rate_hz": 16000,
    "channels": 1,
    "duration_ns": 20000000,
    "payload_mode": "CONTENT_REF",
    "payload_bytes": null,
    "content_ref": "ephemeral:fx01:i1",
    "content_sha256": "d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3d3",
    "content_size_bytes": 640
  },
  "observation": {
    "clock_domain_id": "fx01-single-process",
    "generated_at_ns": null,
    "generated_observer": null,
    "received_at_ns": null,
    "received_observer": null,
    "reproduced_at_ns": null,
    "reproduced_observer": null,
    "captured_at_ns": 650000000,
    "captured_observer": "DEVICE",
    "gateway_accepted_at_ns": 660000000,
    "gateway_accepted_observer": "GATEWAY",
    "stt_forward_at_ns": 670000000,
    "stt_forward_observer": "STT_ADAPTER"
  },
  "event_digest": "25eaa9fb47868cf3992c029dcd6d045fdf817323281090e90d9f3a4ff352c244"
}
```

G2 OUTPUT

```json
{
  "schema_id": "cmp.media.duplex.v1",
  "contract_version": "cmp.media.duplex.v1",
  "event_type": "OUTPUT_AUDIO_CHUNK",
  "event_id": "e1000000-0000-4000-8000-0000000000a5",
  "organization_id": "11111111-1111-4111-8111-111111111101",
  "project_id": "11111111-1111-4111-8111-111111111102",
  "session_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1",
  "stream_id": "22222222-2222-4222-8222-222222222222",
  "sequence": 5,
  "sequence_scope": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1/22222222-2222-4222-8222-222222222222",
  "direction": "OUTPUT",
  "ack_of_sequence": null,
  "gap_policy": "REJECT_GAP",
  "participant_id": "ffffffff-ffff-4fff-8fff-fffffffffff2",
  "turn_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbb2",
  "invocation_id": "cccccccc-cccc-4ccc-8ccc-ccccccccccc2",
  "speaker_agent_id": "dddddddd-dddd-4ddd-8ddd-ddddddddddd1",
  "origin": "AGENT",
  "source_turn_ids": [],
  "evidence_refs": [],
  "epistemic_label": null,
  "media_plane": "LOCAL_PIPELINE",
  "consent_ref": "99999999-9999-4999-8999-999999999999",
  "consent_grant_epoch": 1,
  "capture_generation": 1,
  "data_classification": "INTERNAL",
  "execution_location": "LOCAL",
  "trust_boundary": "GATEWAY",
  "operation_ref": "cmp:bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbb2:speech.synthesize",
  "is_final": false,
  "stream_end": false,
  "discontinuity": false,
  "payload": {
    "media_encoding": "PCM_S16LE",
    "audio_mime": "audio/wav",
    "sample_rate_hz": 16000,
    "channels": 1,
    "duration_ns": 20000000,
    "payload_mode": "CONTENT_REF",
    "payload_bytes": null,
    "content_ref": "ephemeral:fx01:g2",
    "content_sha256": "e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4",
    "content_size_bytes": 640
  },
  "observation": {
    "clock_domain_id": "fx01-single-process",
    "generated_at_ns": 500000000,
    "generated_observer": "TTS_ADAPTER",
    "received_at_ns": 800000000,
    "received_observer": "GATEWAY",
    "reproduced_at_ns": null,
    "reproduced_observer": null,
    "captured_at_ns": null,
    "captured_observer": null,
    "gateway_accepted_at_ns": null,
    "gateway_accepted_observer": null,
    "stt_forward_at_ns": null,
    "stt_forward_observer": null
  },
  "event_digest": "b91ce3a655afd359eed1f5cc4fc5f711673ff8d9a3062f0784cbcccf80c50cbc"
}
```

G2 SPAN

```json
{
  "schema_id": "cmp.media.duplex.v1",
  "contract_version": "cmp.media.duplex.v1",
  "event_type": "PLAYBACK_SPAN",
  "event_id": "e1000000-0000-4000-8000-0000000000a6",
  "organization_id": "11111111-1111-4111-8111-111111111101",
  "project_id": "11111111-1111-4111-8111-111111111102",
  "session_id": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1",
  "stream_id": "22222222-2222-4222-8222-222222222222",
  "sequence": 6,
  "sequence_scope": "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaa1/22222222-2222-4222-8222-222222222222",
  "direction": "OUTPUT",
  "ack_of_sequence": null,
  "gap_policy": "REJECT_GAP",
  "participant_id": "ffffffff-ffff-4fff-8fff-fffffffffff2",
  "turn_id": "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbb2",
  "invocation_id": "cccccccc-cccc-4ccc-8ccc-ccccccccccc2",
  "speaker_agent_id": "dddddddd-dddd-4ddd-8ddd-ddddddddddd1",
  "origin": "AGENT",
  "source_turn_ids": [],
  "evidence_refs": [],
  "epistemic_label": null,
  "media_plane": "LOCAL_PIPELINE",
  "consent_ref": "99999999-9999-4999-8999-999999999999",
  "consent_grant_epoch": 1,
  "capture_generation": 1,
  "data_classification": "INTERNAL",
  "execution_location": "LOCAL",
  "trust_boundary": "GATEWAY",
  "operation_ref": "cmp:bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbb2:speech.synthesize",
  "is_final": false,
  "stream_end": false,
  "discontinuity": false,
  "payload": {
    "span_role": "CHUNK",
    "playback_state": "PLAYING",
    "content_sha256": "e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4e4",
    "source_sequence": 5
  },
  "observation": {
    "clock_domain_id": "fx01-single-process",
    "generated_at_ns": null,
    "generated_observer": null,
    "received_at_ns": null,
    "received_observer": null,
    "reproduced_at_ns": 880000000,
    "reproduced_observer": "PLAYBACK_SINK",
    "captured_at_ns": null,
    "captured_observer": null,
    "gateway_accepted_at_ns": null,
    "gateway_accepted_observer": null,
    "stt_forward_at_ns": null,
    "stt_forward_observer": null
  },
  "event_digest": "872bd9d774cac70f0e4045b0626f42203bb4ce78aad797ce2404c17d2de83a7a"
}
```

## 4. Predicado de full-duplex real

Todas as linhas, senão FAIL:

1. Existe `PLAYBACK_SPAN` com `reproduced_at_ns` anterior a `stt_forward_at_ns` de I0 e `playback_state` `PLAYING` ou `DUCKED`. Na FX-01 esse span é G0, `100000000` < `320000000`.
2. I0 tem `captured_at_ns`, `gateway_accepted_at_ns` e `stt_forward_at_ns` não nulos, no mesmo `clock_domain_id` dos spans.
3. Existe `PLAYBACK_SPAN` cujo `reproduced_at_ns` está na interseção e é maior que `captured_at_ns` de I0. Na FX-01: G1, `400000000`.
4. Esse span correlaciona com um `OUTPUT_AUDIO_CHUNK` por `content_sha256` e `source_sequence`, e nesse chunk `reproduced_at_ns` é null.
5. Não há `PLAYBACK_SPAN` `STOPPED` nem pause com carimbo menor ou igual a `stt_forward_at_ns` de I0.
6. A sessão não entra em modo exclusivo de entrada para poder aceitar I0.
7. `generated_at_ns` ou `received_at_ns` sozinhos não satisfazem a linha 3.

Contadores do PASS futuro: `input_chunks_accepted_during_playback = 2` (I0 e I1), `output_chunks_reproduced_during_capture = 1` (só G1), `exclusive_input_mode_entered = false`.

Domínios de relógio diferentes tornam o predicado `NOT_EVALUABLE`. Isso não é PASS.

## 5. O01, O02, O13, O14

### CMP-FD-O01

- Fixture: os oito eventos da seção 3, nesta ordem de emissão.
- PASS: predicado da seção 4.
- FAIL: STT só abre depois do playback parar; ou o harness usa um fim lógico sem `PLAYBACK_SPAN`; ou aceita evento que o schema rejeitaria.
- NOT RUN. Evidence ABSENT.

### CMP-FD-O02

- Os mesmos eventos, `media_plane=LOCAL_PIPELINE`, agente com `accepts_audio=false`.
- PASS: predicado da seção 4; o processo do agente não recebe sample; recebe o texto do `STT_FINAL`; a synthesize usa o `voice_label` desse agente.
- FAIL: downgrade a turn-taking, ou sample entregue ao agente.
- NOT RUN.

### CMP-FD-O13 — pause-before-STT

- Anti-fixture: os mesmos relógios de I0, mais um `PLAYBACK_SPAN` com `playback_state=STOPPED` e `reproduced_at_ns=240000000`, anterior ao `stt_forward_at_ns` `320000000`. Um fim lógico artificial de `900000000` não conta.
- O oráculo passa somente se O01 é reprovado nesse roteiro.
- FAIL do oráculo: marcar O01 PASS. Esse é o half-duplex com barge-in.
- NOT RUN.

### CMP-FD-O14 — gerado não é reproduzido

- Remover o `PLAYBACK_SPAN` de G1. O `OUTPUT` de G1 continua com `generated_at_ns=200000000` e `received_at_ns=360000000`, `reproduced_at_ns` null. O último span real antes da captura é G0, em `100000000`.
- O oráculo passa somente se O01 falha.
- FAIL do oráculo: O01 passa usando `generated_at_ns` ou `received_at_ns`.
- NOT RUN.

## 6. Eco e VAD — CMP-FD-O28 refeito

Fixture `CMP-FD-FX-AEC-01`. O componente não recebe campo `echo`, booleano ou rótulo. Entrada que traga `echo=true` invalida a fixture. Esse resultado não pode ser PASS.

Entrada, `PCM_S16LE`, 48000 Hz, um canal:

- `reference_pcm`: 960 amostras. A amostra `i` vale `8000` se `(i // 40) % 2 == 0`, senão `-8000`.
- `mic_pcm`: 1440 amostras, inicializadas em 0. Para `i` de 480 a 1439, `mic[i] = reference[i-480] // 2`. Em seguida, para `i` de 1000 a 1199, `mic[i] = 16000`. Esse trecho é a fala humana sintética e não é cópia da referência.
- Atraso: 480 amostras. Constante de fixture, não SLA.

Saída observada, produzida pelo componente e não escrita como premissa: `forwarded_pcm` e `aec_decision` em `ECHO_ONLY`, `MIXED`, `HUMAN_ONLY` ou `DROPPED`.

PASS futuro, todas as linhas:

1. `mic_open` permanece true. O AEC não incrementa `capture_generation`.
2. No `forwarded_pcm`, cada amostra de 1000 a 1199 difere de `16000` em no máximo `1000`. A fala humana permanece.
3. Fora desse trecho, onde só havia eco, cada amostra difere de `0` em no máximo `400`.
4. O STT recebe `forwarded_pcm`, não o `mic_pcm` bruto e não um frame vazio.
5. `aec_decision` é saída. `MIXED` ou `HUMAN_ONLY` podem aparecer. Não vêm na entrada.

FAIL: `DROPPED`, frame vazio ou `mic_open=false` (falso positivo que apaga a fala); `forwarded_pcm` igual ao `mic_pcm` (eco conservado); entrada com `echo=true`.

Os limites `1000` e `400` são `FIXTURE_CONSTANT` desta forma de onda. Não são aceite de produto. NOT RUN.

## 7. Ledger

Build pai do projeto, teto escrito só por `AuthorizeConversationalBudget` de um humano: `budget_limit_minor = 100`, `spent = 0`, `reserved = 0`, uma autorização `ACTIVE`. `OpenConversationalAnchor` não envia teto.

### CMP-FD-O35 — dois gastos distintos

- A: `operation_ref` `cmp:turn-a:speech.transcribe`, estimate `60`, `expected_build_version = 1`, `expected_task_version = 1`.
- B: outro `operation_ref`, estimate `60`, as mesmas versions esperadas.
- Os dois passam a fase A. Só quem obtém primeiro o `SELECT build FOR UPDATE` pode comprometer.
- Depois do vencedor: `reserved = 60`, `build.version = 2`, `spent = 0`.
- O perdedor lê headroom `40` só depois do lock. `60 > 40`. `402 BUDGET_EXCEEDED`. `reserved` fica `60`. Zero segunda reservation.
- FAIL: `reserved = 120`, ou headroom lido antes do lock.
- NOT RUN.

### CMP-FD-O36 — duas sessões não fazem 2X

- Teto `100`.
- Open A pede fatia `80` e manda `budget_authorization_ref` da autorização `ACTIVE`. Sucesso: soma das fatias `80`, limit continua `100`, um único Build.
- Open B pede fatia `80`. Depois do mesmo lock a soma seria `160`. `409 SLICE_CEILING`. Soma fica `80`. Nenhum Build novo.
- Opens concorrentes: a serialização no Build pai deixa um sucesso só.
- FAIL: dois Builds, ou dois limits `80`, ou headroom agregado `160` sem autorização humana nova.
- NOT RUN.

### CMP-FD-O40 — teto autodeclarado

- Open com `budget_limit_minor = 1000000`.
- `422 UNKNOWN_FIELD` na fase A, antes de lock monetário.
- Zero task nova. `budget_limit_minor` inalterado.
- NOT RUN.

### CMP-FD-O37 — cross-tenant

- Canal: organização `11111111-1111-4111-8111-111111111101`, projeto `11111111-1111-4111-8111-111111111102`.
- `task_id` existente só em outra organização. UUID bem formado.
- A consulta com org e projeto do canal devolve zero linhas.
- Corpo: `{"error_code":"NOT_FOUND","retryable":false,"terminal":true}`.
- Sem id estrangeiro, sem saldo, sem Operation, sem Reservation. Contadores do outro Build inalterados.
- FAIL: código que confirme a existência no outro tenant, ou qualquer débito lá.
- NOT RUN.

### CMP-FD-O38 — CAS

- Depois do lock, `task.version = 2` e o comando trouxe `expected_task_version = 1`.
- `409 VERSION_CONFLICT`, `mismatch_aggregate = task`. Rollback. `reserved` igual. Zero Operation nova.
- `command_id` que já tinha commit: `200 IDEMPOTENT_REPLAY`, sem segunda reserva.
- Campo `expected_version` da v0.2, presente ou null: `422`, sem reserva.
- NOT RUN.

### CMP-FD-O15, O16, O17, O18, O30, O31

Sentido preservado, agora sobre o Build pai:

- O15: `coding_engine` na reserva conversacional, ou `InvokeCapability` pelo roteador, deixa `reserved` inalterado.
- O16: task sem `build_id` não insere. A coluna continua NOT NULL.
- O17: segunda reserva da mesma chave não soma o estimate outra vez.
- O18: task de produto na reserva conversacional → `409 NOT_SESSION_ANCHOR`. Task de sessão na lista de dependência de produto → `409 DAG_KIND_MIX`.
- O30: sweep com operation `DISPATCHED` põe `ORPHAN_HELD` e não chama `ReleaseReservation`.
- O31: `deploy.release`, `terminal.exec` e `vault.read` → `403` antes de reservar.

Todos NOT RUN. Evidence ABSENT.

### CMP-FD-O39 — mesmo event_id, outro payload

- Reenviar o `event_id` de I0 com outro `content_sha256`.
- O digest muda. `409 EVENT_ID_REUSED`. Sessão e `reserved` não mudam.
- Mesmos bytes e mesmo digest: replay, zero efeito novo.
- NOT RUN.

## 8. Demais oráculos

O03 a O12, O19 a O27, O29, O32, O33 e O34 continuam NOT RUN, evidence ABSENT. O critério da v0.2 vale, com uma substituição: carimbo de reprodução lê-se em `PLAYBACK_SPAN.observation.reproduced_at_ns`, não num campo reescrito do chunk.

| ID | PASS futuro | FAIL |
|---|---|---|
| O03 | playback para; ACK `UNCONFIRMED` não zera custo nem redespacha | `NO_EFFECT` sem prova |
| O04 | speaker, turn, ata e divergência; sem review formal | consenso fabricado ou review iniciado |
| O05 | chunk de epoch velho rejeitado | chunk tardio transcrito |
| O06 | DEVICE, TRANSPORT, STT e BUFFER fechados fora de sessão | frame do Forge aceito |
| O07 | `CONFIDENTIAL` não sai para speech externo | um byte no provider |
| O08 | dedupe com HELD, sem segunda reserva | segundo débito |
| O09 | fala de deploy não chama `DeployRelease` | efeito de deploy |
| O10 | troca de projeto reconstrói o pack e recheca a classe | tool do outro projeto |
| O11 | adapter half-duplex não marca o MVP pronto | banner de PASS |
| O12 | aponta para CMP-O-28 e não o executa | usar O12 como prova de independência |
| O19 | epoch antigo rejeitado de modo atômico | aceite depois do corte |
| O20 | os quatro pontos observados em separado | só um agregado “zero STT” |
| O21 | crash ou background deixa `mic_open=false` | reabertura automática |
| O22 | reconnect recusa generation velha | merge de buffer |
| O23 | divergência registry/adapter nega | confiar no auto-relato |
| O24 | matriz das quatro classes | `EXTERNAL` em `RESTRICTED` |
| O25 | subida para `CONFIDENTIAL` trava o egress seguinte | buffer antigo enviado |
| O26 | fallback local para externo é decisão nova | herdar permissão |
| O27 | síntese não atribui frase ausente do turno Codex | falsa atribuição |
| O29 | campos de latência existem e os aceites seguem null | SLA numérico inventado |
| O32 | os dois planos emitem os mesmos `event_type` | contrato diferente por plano |
| O33 | lacuna vira `STREAM_GAP`, sem sample inventado | áudio fabricado |
| O34 | `discontinuity=true` só no chunk depois da lacuna | buraco silencioso |

CMP-O-28 continua NOT RUN. CMP-FD-O28 é eco e VAD. CMP-FD-O27 também não substitui CMP-O-28.

## 9. O que este arquivo não é

Não é relatório de execução. Não há run id, host, artefato nem exit code. A existência da fixture não é PASS.
