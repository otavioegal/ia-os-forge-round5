# CMP-02 — System architecture

Status: DELTA CONVERSATIONAL-MVP v0.2 — CANDIDATE FOR CODEX REVIEW. DRAFT / NOT APPROVED / NOT READY FOR BUILD / NO BUILD-00 AUTHORIZATION. No tests executed. No staging. No Founder approval inferred. FDP-14 and FDP-15 remain pending. No voice provider is chosen or contracted.

This document is an implementation proposal plus normative references. It does not edit FDP-16, FDP-16A v1.7, or FDP-15 v1.0. Where a v1.7 rule would have to change, the change is an open question in [CMP-OPEN-QUESTIONS.md](CMP-OPEN-QUESTIONS.md), not a silent amendment.

## 1. What is inherited unchanged

- Stack stays frozen: Tauri 2, React/TypeScript/Vite, Node sidecar, tldraw, Supabase Postgres/Auth/RLS/Storage, PGMQ, Git worktrees, Fastify, Cloud Run, OpenTelemetry, n8n. Codex and Claude Code remain the MVP coding engines. Grok and OpenRouter stay prepared P1 on that engine allowlist until a grant says otherwise (FDP-16 v1.7 §1). A conversational model route is not that grant.
- Task states stay exactly: QUEUED, READY, RUNNING, WAITING, RETRYING, HANDOFF, REVIEWING, BLOCKED, COMPLETED, FAILED, CANCELLED.
- Identity rule stays: table PK is `id`. Alias columns equal `id`. `operation_ref` is not an alias of `operation.id`.
- Money stays int64 minor units, USD for the MVP ledger. Invariant `spent + reserved <= limit`. One monetary movement per operation. Lock order unchanged. `ProviderEffectProof` captured only by `forge.provider_ingest`. Late evidence after a movement stays the v1.7 rule. This delta does not restate those algorithms in order to vary them.
- Adapter shape inherited from the unapproved FDP-15 draft, as a constraint this proposal will not break: ForgeContract → Adapter → Provider; callers ask for a capability, not a vendor; common methods `describe`, `health`, `invoke`, `cancel`.
- Coding-engine `InvokeCapability` remains `coding_engine via gateway`. This delta does not retarget that row.

## 2. Components

| Component | Owns | Must not own |
|---|---|---|
| Universal composer (CMP-01) | Capture, playback, transcript view, interrupt button | Policy, money, parecer writes |
| Session service | `conversation_session`, turns, council records | Budget mutation |
| Context builder | Authorized pack for one agent on one turn | Cross-project memory, secrets |
| Conversation router | Mode DIRECT, COUNCIL, or JARVIS; next speaker | Tool grants, review signatures |
| Speech boundary | STT/TTS capability calls | The model prompt of a text-only agent |
| Model router | `conversation.respond` only, deny-by-default | Coding-engine selection |
| Existing tool gateway and ledger | Reserve, dispatch, receipt, release | A special voice exception |
| Evidence read | Real bundle or ABSENCE | Invented status |
| Policy service | Consent, classification, capability, gates | Spoken override |

Direction of authority stays the FDP-16 rule: human policy, then Policy Service, then Gateway, then Adapter. The router is not above policy.

## 3. Modes

`session.mode` is exactly one of `DIRECT`, `COUNCIL`, `JARVIS`.

- DIRECT: one `active_agent_id`. Replies come from that agent.
- COUNCIL: two or more participants. The router assigns `next_speaker_agent_id`. Users may pin the next speaker.
- JARVIS: Jarvis may answer, invite, or transfer. A transferred answer is not a Jarvis turn.

## 4. Proposed records

These tables do not exist in v1.7. They are a proposal. RLS on `organization_id` and application checks on project membership are mandatory, same as every other tenant table. Names are not created by this document.

Identity proposal, copying the v1.7 rule rather than inventing a second key: `session_id` generated equal to `conversation_session.id`; `turn_id` generated equal to `conversation_turn.id`.

### 4.1 conversation_session

| Field | Type | Null | Constraint |
|---|---|---|---|
| id | uuid | no | PK |
| organization_id | uuid | no | RLS |
| project_id | uuid | no | same org |
| mode | enum | no | DIRECT, COUNCIL, JARVIS |
| opened_by | uuid | no | authenticated user |
| active_agent_id | uuid | yes | required for DIRECT and JARVIS |
| status | enum | no | OPEN, DEGRADED_TEXT, CLOSED |
| voice_required | bool | no | true for every session this delta allows; never cleared by a provider failure |
| microphone_consent_state | enum | no | exactly NOT_GRANTED, GRANTED, DENIED, or REVOKED |
| microphone_consent_id | uuid | yes | null if and only if state is NOT_GRANTED; otherwise FK to microphone_consent |
| retention_policy_id | uuid | no | org retention policy; required for text-only and for voice; not a microphone grant |
| ledger_anchor_task_id | uuid | yes | see AQ-02; null until that decision |
| created_at | date-time | no | UTC |

`voice_required` is set true at insert and is not updated to false. DEGRADED_TEXT is availability, not scope.

LOW-01 model, chosen in v0.2 so a text-only open does not invent a microphone grant. `retention_policy_id` and microphone consent are different fields.

| microphone_consent_state | microphone_consent_id | Capture and STT |
|---|---|---|
| NOT_GRANTED | null. No decision row is required. This is the legal text-only open. | zero audio bytes, zero STT |
| DENIED | required. The row's decision is DENIED, not a grant. | zero audio bytes, zero STT |
| REVOKED | required. The row records the prior grant now revoked. | zero audio bytes, zero STT |
| GRANTED | required. Same user, same org, scope `microphone`, decision GRANTED. | STT may be attempted, still subject to classification and the ledger |

A session insert that needs a synthetic UUID in `microphone_consent_id` in order to open text-only is illegal. Text submit stays legal in every non-GRANTED state. Voice controls stay on screen. `voice_required` stays true.

### 4.2 conversation_turn

| Field | Type | Null | Constraint |
|---|---|---|---|
| id | uuid | no | PK |
| session_id | uuid | no | FK |
| sequence | int64 | no | unique per session, starts at 1 |
| speaker_kind | enum | no | HUMAN, AGENT |
| speaker_agent_id | uuid | yes | required when AGENT |
| speaker_user_id | uuid | yes | required when HUMAN; the authenticated user, never a voiceprint |
| input_mode | enum | no | TEXT, VOICE, NONE |
| output_mode | enum | no | TEXT, VOICE, NONE |
| origin | enum | no | HUMAN_INPUT, DIRECT_AGENT, STT_THEN_TEXT_AGENT, TTS_OF_TEXT, JARVIS_SYNTHESIS, HANDOFF, EVIDENCE_LOOKUP, REFUSAL |
| answered_by_agent_id | uuid | yes | agent that produced the words; required for agent content |
| claim_class | enum | no | FACT, INFERENCE, SUGGESTION, ABSENCE |
| evidence_refs | uuid[] | no | empty allowed |
| source_turn_ids | uuid[] | no | required non-empty for JARVIS_SYNTHESIS |
| operation_refs | string[] | no | ledger keys for this turn's provider calls; empty if none |
| status | enum | no | COMPLETED, INTERRUPTED, FAILED, REFUSED |
| refusal_reason | string | yes | required when REFUSED |
| interrupted_from_turn_id | uuid | yes | |
| created_at | date-time | no | |

Unique `(session_id, sequence)`. Turns are append-only. Interrupt does not delete earlier rows.

### 4.3 Council extras

`council_participant(session_id, agent_id, role)` with at least two agents before status can leave convening.

`council_divergence(id, session_id, topic, turn_ids[])` append-only. Deleting a divergence is forbidden.

`conversation_minutes(id, session_id, authored_turn_id, source_turn_ids[], evidence_refs[], divergence_ids[], claim_class)`. `claim_class` cannot be FACT if any source claim is not FACT or if any evidence ref is missing. A minutes row that says the council agreed while a divergence row exists for that agenda item is illegal.

### 4.4 Conversational registry

`conversational_agent(id, organization_id, agent_key, display_name, role, accepts_audio, capability_allow[], capability_deny[], voice_label)`.

`accepts_audio` false means the speech boundary runs STT and forwards text, then TTS of the text reply. The menu still offers voice. `capability_allow` never includes `deploy.release`, raw `vault.read`, destructive terminal capabilities, `ledger.reconcile`, `ledger.proof_ingest`, or `review.sign`.

Codex's conversational registry row, when offered, is `codex_conversational` only. Its allow list is limited to `conversation.respond` and `conversation.show_evidence` over already stored review artifacts. Deny includes `review.sign`, `review.edit`, and `review.execute`. That row is not the formal review executor in CMP-03 §8. InviteAgent and TransferTurn cannot start a formal review.

Jarvis allow: `conversation.respond`, `conversation.invite`, `conversation.transfer`, `conversation.show_evidence`, `conversation.issue_minutes`. Deny includes every coding, deploy, vault, and review-sign capability.

`voice_label` is a stable role string ("Architect"), not a vendor voice name.

## 5. Context builder

On every model call the builder assembles a new pack. It does not reuse the previous agent's pack by pointer.

Included only when all of these pass:

- same `organization_id`;
- project membership of the user and of the agent;
- data classification allowed for the selected model route;
- the agent's allow list;
- evidence refs the agent may read.

Excluded always:

- other projects and other orgs;
- resolved secrets and the canary class of secret material;
- raw audio bytes;
- another agent's hidden prompt or scratchpad;
- parecer edit tokens.

A switch or a handoff may attach one filtered summary. The summary is INFERENCE, carries the ids it was built from, and is rebuilt if the target agent differs. ENG-02's rule ("handoff keeps same scope") is the ceiling: a conversational handoff must not grow capabilities. It may shrink the pack.

This is the same least-memory idea as F-036. It does not amend F-036.

## 6. Router and council orchestration

Commands below are proposals. They are not rows of the v1.7 command catalog.

| Proposed command | Actor | Effect | Denial |
|---|---|---|---|
| OpenSession | authenticated human | insert session, voice_required true | 401 AUTH_REQUIRED; 403 AUTHZ_PROJECT; 403 AUTHZ_FOREIGN_ORG |
| SubmitText | same human | append HUMAN turn, then route | 409 SESSION_CLOSED; 403 |
| CommitUtterance | same human | append HUMAN voice turn after local capture | 403 CONSENT_REQUIRED; 409 SESSION_CLOSED |
| InterruptPlayback | same human | stop local audio; mark in-flight playback INTERRUPTED; keep session | 409 NOT_SPEAKING |
| SwitchAgent | same human | rebuild pack; set active agent | 403 AGENT_NOT_REGISTERED; 403 AGENT_SCOPE |
| ConveneCouncil | same human | participants >= 2, agenda turn | 422 COUNCIL_TOO_SMALL |
| PinSpeaker | same human | next turn only | 403 NOT_IN_COUNCIL |
| InviteAgent | Jarvis via router | participant row, no answer yet | 403 AGENT_NOT_REGISTERED |
| TransferTurn | Jarvis via router | next answer must be the named agent | 403 AGENT_NOT_REGISTERED |
| IssueMinutes | router | minutes row from stored turns | 409 DIVERGENCE_UNSTATED; 422 NO_TURNS |
| ShowEvidence | router read | bundle or ABSENCE | 403 AUTHZ_PROJECT |

No command in this list moves money. Provider calls go through section 7.

Council turn order is explicit: pinned speaker if set, otherwise the next participant in registry order, one agent per turn. The router does not ask all models in parallel and then hide the calls. Parallel fan-out is forbidden in v0.2 because it spends without a visible speaker and complicates cancel.

User interrupt during another agent's speech inserts a HUMAN turn and clears the pin only if the user then selects a different agent. It does not erase the interrupted turn's partial transcript if one was already shown; that turn stays INTERRUPTED.

## 7. Speech and model contracts

Contract version proposed: `cmp.speech.v0`. Not implemented. No provider binding.

Capabilities, asked by name, never by vendor:

| Capability | Family proposal | side_effects | Timeout class |
|---|---|---|---|
| speech.transcribe | TOOL (AQ-03) | EXTERNAL | INTERACTIVE |
| speech.synthesize | TOOL (AQ-03) | EXTERNAL | INTERACTIVE |
| conversation.respond | MODEL | EXTERNAL | INTERACTIVE |
| conversation.show_evidence | TOOL | NONE | INTERACTIVE |
| conversation.invite | internal router | NONE | none |
| conversation.issue_minutes | internal router | INTERNAL | STANDARD |

Family TOOL is a proposal so the unapproved FDP-15 sentence "three families" is not silently extended. See AQ-03.

Adapter descriptor adds nothing that weakens FDP-15: `describe`, `health`, `invoke`, `cancel`, plus `receipt_query` = SUPPORTED or ABSENT, and `data_access` classes. An undeclared field takes the stricter policy. `cancel` must be real. Silent success without cancel support is forbidden while a playback or stream is advertised.

Streaming partial transcripts and streaming TTS bytes are optional on the same capabilities when `describe` says `streaming: true`. Half-duplex with local barge-in is sufficient for v0.2 if interrupt meets CMP-01. A full-duplex media vendor is not selected (AQ-07).

Unknown fields are rejected (`422 VALIDATION`). A missing required field is the same error. No vendor name is part of the contract.

### 7.2 `cmp.speech.v0` schemas

This section is the minimum versioned contract for MEDIUM-01. It binds no provider. `contract_version` on every speech request and every speech result is the literal string `cmp.speech.v0`.

`describe` lists `contract_versions`. If that list does not contain `cmp.speech.v0`, the router does not call `invoke` and does not send audio bytes. The error is `SPEECH_UNSUPPORTED_VERSION`. There is no silent downgrade and no second version negotiated in the same call.

Audio encoding enum for both capabilities: `PCM_S16LE`, `OPUS`, `FLAC`. Any other value is `SPEECH_UNSUPPORTED_ENCODING`. `audio_mime` must match: `audio/wav` for `PCM_S16LE`, `audio/ogg` for `OPUS`, `audio/flac` for `FLAC`. A mismatch is `SPEECH_BAD_AUDIO`.

#### speech.transcribe request

| Field | Type | Null | Purpose |
|---|---|---|---|
| invocation_id | uuid | no | one invocation; the cancel target |
| operation_ref | string | no | ledger key `cmp:{turn_id}:speech.transcribe` |
| contract_version | string | no | exactly `cmp.speech.v0` |
| audio | bytes | no | utterance payload; never copied into an audit event |
| audio_encoding | enum | no | PCM_S16LE, OPUS, or FLAC |
| audio_mime | string | no | mime that matches encoding |
| sample_rate_hz | int | yes | required when encoding is PCM_S16LE; otherwise omitted |
| channels | int | no | 1 for this contract |
| language | string | yes | BCP-47 hint; the adapter may ignore it only if describe says language detection is automatic |
| streaming | bool | no | true only when describe.streaming is true; otherwise 422 |
| data_classification | string | no | policy input before any byte leaves the process |
| organization_id | uuid | no | tenant |
| project_id | uuid | no | project |
| timeout_ms | int | no | planning bound, not a measured SLO |

#### speech.transcribe result

| Field | Type | Null | Purpose |
|---|---|---|---|
| contract_version | string | no | exactly `cmp.speech.v0` |
| invocation_id | uuid | no | echoes the request |
| transcript_text | string | no | text of this result |
| transcript_state | enum | no | PARTIAL or FINAL |
| is_final | bool | no | true if and only if transcript_state is FINAL |
| language_detected | string | yes | BCP-47 when the adapter detected one |
| provider_id | string | no | adapter descriptor id, not a secret and not a vendor selection |
| model_id | string | yes | present when the adapter has a model dimension; otherwise null and the attribution key is the capability |

PARTIAL is not a committed user turn and is not input to `conversation.respond`. Only a FINAL result may become the committed transcript. A stream of PARTIAL results followed by one FINAL result is one operation and one reservation, not one spend per partial. A second FINAL for the same invocation is a contract error and must not start a second provider execution.

#### speech.synthesize request

| Field | Type | Null | Purpose |
|---|---|---|---|
| invocation_id | uuid | no | cancel target |
| operation_ref | string | no | ledger key `cmp:{turn_id}:speech.synthesize` |
| contract_version | string | no | exactly `cmp.speech.v0` |
| text | string | no | reply text already produced by the agent turn |
| voice_label | string | no | role label from the registry, not a vendor voice name |
| audio_encoding | enum | no | requested encoding |
| audio_mime | string | no | requested mime matching encoding |
| language | string | yes | BCP-47 |
| streaming | bool | no | same rule as transcribe |
| data_classification | string | no | policy input |
| organization_id | uuid | no | tenant |
| project_id | uuid | no | project |
| timeout_ms | int | no | planning bound, not a measured SLO |

#### speech.synthesize result

| Field | Type | Null | Purpose |
|---|---|---|---|
| contract_version | string | no | exactly `cmp.speech.v0` |
| invocation_id | uuid | no | echoes the request |
| audio | bytes | no | playback bytes; never an audit payload |
| audio_encoding | enum | no | actual encoding |
| audio_mime | string | no | actual mime |
| is_final | bool | no | true only on the completed clip or the stream end |
| provider_id | string | no | descriptor id |
| model_id | string | yes | same attribution rule as transcribe |

Streaming TTS chunks before `is_final` true are playback only. They are not a second operation. Interrupt stops local playback without waiting for this result.

#### Error object

| Field | Type | Null | Purpose |
|---|---|---|---|
| error_code | string | no | one code from the taxonomy below |
| retryable | bool | no | true only when the taxonomy row says retryable |
| terminal | bool | no | true only when the taxonomy row says terminal |
| provider_code | string | yes | opaque provider symbol; redacted if it contains secret-like material |
| message_redacted | string | no | no audio, no transcript body, no secret |

| Code | retryable | terminal | When it is used |
|---|---|---|---|
| SPEECH_UNAVAILABLE | yes | no | adapter unhealthy or connection failed before a conclusive provider effect |
| SPEECH_TIMEOUT | yes | no | timer fired; does not by itself prove the provider never received the call |
| SPEECH_RATE_LIMITED | yes | no | provider asked for backoff before a conclusive effect |
| SPEECH_BAD_AUDIO | no | yes | empty audio, bad mime, or encoding mismatch |
| SPEECH_UNSUPPORTED_VERSION | no | yes | contract_version is not `cmp.speech.v0` |
| SPEECH_UNSUPPORTED_ENCODING | no | yes | encoding outside the enum |
| SPEECH_CLASSIFICATION_DENY | no | yes | policy refused egress; no provider payload |
| SPEECH_CONSENT_REQUIRED | no | yes | microphone state is not GRANTED; no STT |
| SPEECH_CANCELLED | no | yes | cancel_state CONFIRMED for this invocation |
| SPEECH_CANCEL_UNCONFIRMED | no | no | cancel was requested and the provider did not confirm |
| SPEECH_PROVIDER_REJECTED | no | yes | provider refused the payload |

`SPEECH_CANCEL_UNCONFIRMED` is the only code with both flags false. The invocation is not a confirmed completion, and it still must not be redispatched. Every other code has exactly one of the two flags true. A result whose flags disagree with this table is a contract violation and is treated as non-redispatchable.

`retryable: true` is not permission to dispatch again. Section 9 decides that from ledger state. A retryable code after dispatch still forbids redispatch.

#### Cancel

`cancel(invocation_id)` returns `cancel_state` exactly `CONFIRMED` or `UNCONFIRMED`.

- CONFIRMED maps to `SPEECH_CANCELLED`. This invocation is finished. It does not create a new operation.
- UNCONFIRMED maps to `SPEECH_CANCEL_UNCONFIRMED`. The operation stays uncertain. Redispatch is forbidden.
- Local barge-in does not wait for either result.
- Neither result invents a `ProviderEffectProof`. Money after cancel stays section 8 and FDP-16A. If there was no dispatch, there is no reservation. If dispatch happened and no conclusive proof exists, the reservation stays HELD and the UI shows reconciliation.

Invocation envelope reuses the FDP-15 shape: `invocation_id`, `operation_ref`, `capability`, validated `input`, `organization_id`, `project_id`, `task_id` when the anchor exists, `data_classification`, `timeout_class`, trace context. The envelope never carries a secret value. Audio bytes are the STT input only after CMP-03 classification allows that adapter. They are not copied into the model prompt when the agent is text-backed; the transcript is.

`operation_ref` for one committed attempt is `cmp:{turn_id}:{capability}` and must fit 1..128 characters. `normalized_input_digest` is SHA-256 of the canonical input: UTF-8 transcript for `conversation.respond`, audio bytes for `speech.transcribe`, UTF-8 text plus `voice_label` for `speech.synthesize`.

Planning timeouts, not measured SLOs and not SLAs:

- `forge.conversation.barge_in_stop_ms` planning default 200, local playback stop only;
- `forge.conversation.stt_timeout_ms` planning default 15000;
- `forge.conversation.tts_first_byte_target_ms` planning default 800.

These numbers are configuration proposals in the same sense as `forge.ledger.session_max_age_ms` = 900000. They are not measurements. No percentile is claimed.

### 7.1 Text-backed agents

If `accepts_audio` is false:

1. `speech.transcribe` produces text;
2. `conversation.respond` receives that text under the agent's own allow list;
3. `speech.synthesize` speaks the reply text with that agent's `voice_label`.

The agent process never receives microphone samples. It also never receives another agent's tools.

## 8. Money path

There is one money protocol: FDP-16A v1.7 sections 8A through 8A.3. This delta does not create `conversation_ledger`, does not assign `pending_actual_minor`, and does not insert `pending_provider_cost` by a new rule.

Proposed binding, blocked on AQ-01 and AQ-02:

- Each external speech or model call reserves with the same transaction effect as `InvokeCapability`: one operation row, `reserved` increased by the estimate, no provider call inside that transaction. Denials stay 402 BUDGET_EXCEEDED, 403 CAPABILITY_NOT_GRANTED, 409 STOP_LATCH, 409 RECONCILIATION_REQUIRED, 409 SAFE_MODE.
- The actor must not be `coding_engine`. v1.7 only allows `coding_engine via gateway` on `InvokeCapability`. Until the Founder accepts a `conversation_router` actor and a command whose effect is defined as that same reservation, no implementation may call a provider by bypassing the gateway, and no implementation may pretend the router is a coding engine.
- `operation.task_id` is NOT NULL in v1.7. This delta does not null it. The proposed anchor is one system Task per session that cannot enter the build DAG and cannot hold deploy, terminal, or vault capabilities (AQ-02).
- Dispatch happens only after the utterance is committed (text submit or end of an explicit listen). Local capture and local barge-in before commit create no operation. That avoids a pre-dispatch release, which v1.7 cannot do without a conclusive NO_EFFECT proof.
- Settlement and release stay `RecordReceipt` and `ReleaseReservation` under existing proof rules. The speech adapter is an adapter, so it cannot capture a `ProviderEffectProof`. Only `forge.provider_ingest` can. A human sentence, a transcript, or a WAV file is not a proof.
- If the chosen adapter's `receipt_query` is ABSENT and no attestation exists, the operation follows section 8C: BLOCKED_RECONCILIATION, reservation HELD, no invented receipt, no write-off. A voice vendor that cannot be ingested is not given a lighter rule (AQ-12).
- Replay of the same `(project_id, task_id, operation_ref, capability, normalized_input_digest)` does not dispatch a second provider call. This is the IDEM-01 shape applied to speech. It does not edit IDEM-01.
- A council turn per agent is its own `conversation.respond` and, when audio is on, its own `speech.synthesize`. N speakers are N model operations, not one blended call.
- Late conflicting receipts, if a provider later attests a different amount, stay on the v1.7 late-evidence rule. This package does not reopen it.

No numeric session price cap is set here. The hard ceiling is the existing budget invariant. A duplicate call is prevented by the idempotency key, not by an invented percentage.

## 9. Fallback and retry after dispatch

Speech failure still degrades to text, still offers a visible recovery control, and still leaves `voice_required` true. The control does not always resubmit the same `operation_ref`. v0.1 said both "retry the same key" and "do not execute again after dispatch". v0.2 replaces that pair with the table below. The table does not add a ledger, does not release a reservation without a conclusive NO_EFFECT proof, and does not invent a receipt.

| Ledger / proof situation | Recovery control | New turn or operation_ref | Provider call |
|---|---|---|---|
| Before dispatch. Operation is absent, or RESERVED, and `DispatchOperation` has not committed. | RETRY_SAME_OPERATION. The same `operation_ref` and digest may proceed to one dispatch. | No | At most one |
| Provider received the request, or the result is unknown. Status DISPATCHED and no conclusive proof. | RECONCILIATION_REQUIRED. Do not redispatch. Do not start another vendor. | No | Zero additional |
| Conclusive NO_EFFECT, or a conclusive failure with a NO_EFFECT proof and no RECEIPT. Includes ReleaseReservation that already committed under FDP-16A. | NEW_ATTEMPT. The old key only replays the stored no-effect result. A real new try is a new turn and a new `operation_ref`. | Yes, only if the user asks for a new attempt | One call, only on the new key, still through the gateway |
| HELD pending reconciliation. BLOCKED_RECONCILIATION, reservation HELD, `receipt_query` ABSENT, or proof inconclusive. | RECONCILIATION_REQUIRED. Same as the unknown-result row. | No | Zero additional. No invented receipt and no write-off |
| Conclusive effect. SETTLED, or a conclusive RECEIPT. | REPLAY_RESULT. Return the stored result. | No | Zero additional |

A changed utterance is always a new turn, including when the previous operation never dispatched. Retry of identical bytes after audio discard uses the stored digest; it does not require the raw audio to be kept.

Health-down before any dispatch uses `SPEECH_UNAVAILABLE` or `NO_PERMITTED_SPEECH_ADAPTER` and the first row, or no operation at all if policy denies the call before reserve. That banner is not a reason to redispatch an older uncertain operation.

Order around the table:

1. Classify the existing operation with the table. Do this before any adapter invoke.
2. If the table says zero additional calls, the client shows the named control and does not call a provider.
3. A fallback adapter is eligible only for a NEW_ATTEMPT or a not-yet-dispatched operation, and only when Policy allows it for the same data classification (FDP-15 draft §23, privacy before fallback). Otherwise the reason is `NO_PERMITTED_SPEECH_ADAPTER`.
4. OpenRouter is not an implicit speech or conversation fallback. It remains optional and is not on the coding-engine MVP allowlist.

Text entry stays available in every row. Offering text is not removal of voice from the MVP.

## 10. Interrupt

Local playback stops first, within the planning barge-in bound, without waiting for the provider. Then `adapter.cancel` is invoked if a stream is open. Money after cancel follows section 8. If the provider already has a conclusive receipt, late evidence applies and spent is not rewritten by the interrupt. If there was no dispatch yet, there is no reservation to release.

Session context after interrupt is the append-only turn list. Resume uses that list through the context builder, not a private cache on the client.

## 11. Evidence read

`conversation.show_evidence` loads `evidence_bundle` by id within org and project. Hit: return id and content hash. Miss: `{ status: ABSENCE, reason: NO_EVIDENCE }`. The handler does not create a bundle, does not call a model, and does not fill test or percent fields.

## 12. Deliberate non-changes

- No edit to FDP-16A command catalog, proof schema, or Task enum.
- No new P0 id.
- No second budget currency.
- No provider name, endpoint, or price.
- No claim that streaming latency has been measured.
