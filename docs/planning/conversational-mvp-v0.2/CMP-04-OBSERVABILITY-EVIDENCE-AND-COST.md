# CMP-04 — Observability, evidence, and cost

Status: DELTA CONVERSATIONAL-MVP v0.2 — CANDIDATE FOR CODEX REVIEW. DRAFT / NOT APPROVED / NOT READY FOR BUILD / NO BUILD-00 AUTHORIZATION. No tests executed. No staging. No Founder approval inferred. FDP-14 and FDP-15 remain pending. No voice provider is chosen or contracted.

FDP-14 v1.0 is an extract at `historical/round4/docs/source-material/chat-extracts/FDP-14-v1.0__msg080.md`. Founder confirmation is pending. This file does not confirm it. FDP-14 is not a chat UI. The UI is CMP-01. This file says what must be traceable when that UI eventually runs.

No percentage, latency percentile, dollar figure, or token count in this document is a measurement. None have been collected. Fields that would hold them stay empty until a real run exists.

## 1. Inherited observability rules

From the FDP-14 extract §207, not newly approved:

- OpenTelemetry is the instrumentation standard (§6, decision 1). The exporter stays replaceable.
- Logs are structured and correlated (decision 2).
- Raw telemetry and domain events are separate (decision 3).
- Correlation keys include organization, project, task, and attempt when they exist (§8). This delta proposes two more attributes, `session_id` and `turn_id`. That proposal does not rewrite §8.
- Costs are attributable when possible (decision 6). Estimated cost and confirmed cost stay distinct.
- No fake percentages (decision 16). Build progress and health stay derived from stored state.
- Raw prompts and source are not collected indiscriminately (decision 17). Redaction and minimization are the privacy control (§208 R2).

Existing audit names in FDP-16 v1.7 §7 stay required for money and authz: `authz.allowed`, `authz.denied`, `budget.denied`, `budget.reserved`, `budget.settled`, `budget.released`, `budget.proof_conflict`, `budget.proof_inconclusive`, `injection.ignored`, and the other names already listed there. This delta does not remove any.

Existing spans `forge.api.request`, `forge.gateway.invoke`, `forge.adapter.invoke`, and `forge.watchdog.tick` stay. New span names below are proposals.

## 2. Correlation attributes

On every conversational span and domain event, when the value exists:

| Attribute | Rule |
|---|---|
| trace_id | OpenTelemetry |
| organization_id | required |
| project_id | required |
| session_id | required |
| turn_id | required once a turn exists |
| actor_user_id | the authenticated user, when the actor is human |
| agent_id | registry id when an agent speaks or is called |
| mode | DIRECT, COUNCIL, or JARVIS |
| input_mode / output_mode | TEXT, VOICE, or NONE |
| origin | the turn origin enum |
| capability | when a gateway call is made |
| operation_ref | when a ledger operation exists |
| provider_id | adapter descriptor id, never a secret |
| model_id | router selection, or ABSENT if none was called |
| evidence_refs | ids only |
| refusal_reason | code, when refused |
| task_id / attempt_id | only if the ledger anchor or a build task is actually bound |

`task_id` is omitted rather than filled with a synthetic id that was not created.

## 3. Domain events

Proposed names. Append-only. They do not replace `budget.*` events.

| Event | When | Payload may include | Payload must not include |
|---|---|---|---|
| conversation.session_opened | OpenSession commits | session_id, mode, voice_required, microphone_consent_state, microphone_consent_id or null, retention_policy_id | audio, transcript, a synthetic consent UUID |
| conversation.turn_completed | turn COMPLETED | turn_id, speaker, origin, claim_class, evidence ref count, operation_refs | transcript body, audio, prompt |
| conversation.turn_interrupted | interrupt commits | turn_id, interrupted_from_turn_id | audio |
| conversation.turn_refused | REFUSED | refusal_reason | hostile text if it looks like a secret |
| conversation.handoff | switch, invite, or transfer | from_agent_id, to_agent_id, source_turn_ids | pack body |
| conversation.degraded | DEGRADED_TEXT | capability, reason code, voice_required true | provider response body |
| conversation.evidence_shown | show evidence | evidence id and hash, or reason NO_EVIDENCE | a generated summary presented as the artifact |
| conversation.consent_recorded | grant, deny, or revoke | microphone_consent_id when a decision row exists, microphone_consent_state, scope, action | microphone samples |
| conversation.gate_refused | spoken or typed gate attempt | gate code | the utterance |
| conversation.minutes_issued | minutes row | minutes id, source_turn_ids, divergence count | a PASS verdict |

A repeat of the same committed command does not append a second event. Consumers dedupe on `event_id` as in FDP-16A §4. The conversational idempotency key is also the ledger `operation_ref` when money is involved.

## 4. Spans

Proposed child spans under the existing API span:

- `forge.conversation.turn`
- `forge.conversation.stt`
- `forge.conversation.tts`
- `forge.conversation.model`

Each provider child also emits `forge.adapter.invoke` so the current security observability contract still sees the call. Attributes from §2 apply. Span events may include byte lengths and durations measured by the process. Those durations are not targets and are not present in this specification as results.

Spans and logs must not contain secret values (SEC-01). The canary `CANARY_SECRET_FORGE_9f3a` must be absent from all conversational sinks.

## 5. What is never logged by default

- raw audio bytes or audio object URLs that grant read to a raw sample;
- full model prompts and full completions;
- transcript bodies inside audit `meta` (the transcript row, if retained, is a separate store cited by `transcript_ref`);
- resolved secrets, vault payloads, credential material;
- other projects' identifiers beyond a denied-scope reason code.

`transcript_ref` is an id. Resolving it is an authorized read, not a log expansion.

This minimization is a proposal aligned with FDP-14 decision 17. It is not evidence that redaction already works.

## 6. Evidence versus narrative

| claim_class | Meaning | Show sources |
|---|---|---|
| FACT | a stored record was read | must carry one or more evidence refs or be rejected by the minutes rule |
| INFERENCE | the model combined records | refs are the inputs, and the label stays INFERENCE |
| SUGGESTION | a recommendation, including minutes that are not all FACT | refs optional; cannot be rendered as a verdict |
| ABSENCE | the store had no row | reason `NO_EVIDENCE` or another absence code; never a filled-in status |

`conversation.show_evidence` returns the bundle id and content hash, or ABSENCE. It does not call a model to "explain the evidence" unless the user asked a separate conversational question, and that explanation is INFERENCE with the bundle id attached.

No event in this catalog carries a progress percent. A status question reads Task or Build status from the existing enums or reports ABSENCE.

Ready for Human Test remains the F-039 derivation. A conversational claim cannot set it.

## 7. Cost

No price list is stated because no provider is contracted and no call has been made. Cost records, when a future run exists, use the ledger only:

| Call | Ledger capability | When it is created |
|---|---|---|
| One committed STT | speech.transcribe | after utterance commit, before the provider call |
| One model answer | conversation.respond | one per agent turn |
| One TTS playback | speech.synthesize | only if output mode is VOICE and an adapter is permitted |
| Show evidence | none | side_effects NONE; estimate 0; no external call |
| Invite / pin | none | no provider call |

Attributes required on every speech or model spend trace, and stored with the operation so a later sum does not need a second source: `session_id`, `turn_id`, `agent_id`, `provider_id`, `model_id` when the adapter has one, otherwise the speech capability name, `operation_ref`, `estimated_minor`, and later the proof id if ingest stores one. `estimated_minor` is an estimate. Confirmed cost is only a conclusive `ProviderEffectProof` settled by the existing commands. A UI that shows an estimate as a confirmed amount fails CMP-O-31. `pending_actual_minor` stays a projection and is never assigned by conversation code.

A session total is the sum of the operation rows for that `session_id` only. It is not a stored meeting fee, not a second charge, and not a number this package has measured. If two agents use two providers or two models, both pairs appear on their own operations. Missing `provider_id` on an external call is a contract failure, not an unknown bucket that still counts as accounted.

Denied reserve (402) emits `budget.denied` and zero `forge.adapter.invoke` for that attempt.

Duplicate submit of the same operation key emits no second adapter invoke and no second `budget.reserved`.

Council accounting is the sum of the per-turn operations. A single "meeting fee" operation that hides N model calls is forbidden.

If ingest cannot verify the provider, the reservation stays HELD under FDP-16A §8C. The UI may say reconciliation is required. It may not show a made-up settled amount.

Currency remains the build ledger currency. This delta does not introduce a second currency for voice.

## 8. Future evidence

When a test eventually runs, each CMP-O row in CMP-05 needs: test_run_id, commit hash, policy version, artifact hash, environment name, and a named owner. All of those are ABSENT now. A sentence that says "voice worked" does not close an oracle.

No dashboard in this delta is allowed to display a success rate, interruption rate, or cost total that is not computed from the events above. Human Interruption Rate remains an FDP-14 KPI name without a value.
