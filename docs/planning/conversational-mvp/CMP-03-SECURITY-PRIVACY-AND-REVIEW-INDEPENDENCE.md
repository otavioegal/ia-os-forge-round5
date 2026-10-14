# CMP-03 — Security, privacy, and review independence

Status: DELTA CONVERSATIONAL-MVP v0.1 — CANDIDATE FOR CODEX REVIEW. DRAFT / NOT APPROVED / NOT READY FOR BUILD / NO BUILD-00 AUTHORIZATION. No tests executed. No staging. No Founder approval inferred. FDP-14 and FDP-15 remain pending. No voice provider is chosen or contracted.

Inherited security sentences are not re-approved by being cited. FDP-13 v1.0 in this tree is an extract (`historical/round4/docs/source-material/chat-extracts/FDP-13-v1.0__msg077.md`). It has no Founder signature page here. The seventeen P0 intents stay on their v1.7 stories. This file adds conversational rules around them.

## 1. Frozen decisions this delta will not weaken

From FDP-13 §216, as preserved extract, not as a new approval:

- Security-critical controls live outside LLMs (item 1).
- Engine handoff never expands permissions automatically (item 8).
- Secrets are references, not task content (item 9).
- Model routing respects data classification (item 12).
- External content is untrusted and cannot elevate authority (item 13).
- Tool calls are re-authorized outside the model (item 14).
- Audit is append-oriented (item 19).
- Emergency stop and safe mode remain P0 (item 20). STOP-01 still halts new work, including new speech and model calls.
- Production approval is bound to a specific release and environment (item 22).

From the v1.7 ledger: spoken text is not a `ProviderEffectProof`. Capturer remains `forge.provider_ingest` only.

Policy inputs already named in FDP-13 §25 include actor, organization, project, resource, action, environment, risk, data classification, budget, and context. Conversational turns supply those inputs. They do not replace the policy engine.

## 2. Scopes

Every session and turn carries `organization_id` and `project_id`.

- A user without a session gets 401 AUTH_REQUIRED (AUTH-01). Conversation does not create a side channel.
- A user in org A cannot open or read org B (AUTHZ-01, RLS-01).
- A member of the org who is not a member of the project gets 403 AUTHZ_PROJECT (AUTHZ-02).
- Switching agents rebuilds the pack (CMP-02 §5). The previous project id is not retained as "helpful context".
- Audio objects, transcript refs, and minutes are project-scoped rows. A foreign select returns zero rows.

Jarvis does not hold a cross-project search capability in this delta.

## 3. Voice is not authentication

The human speaker id on a turn is the already authenticated desktop user. A recording played into the microphone does not change `speaker_user_id`, does not refresh assurance, and does not extend `authenticated_at`.

No voiceprint, speaker-verification vendor, or "trusted voice" flag is specified. AQ-11 asks the Founder to confirm that biometrics stay out of this MVP.

Impersonation of an agent is handled by the registry id and the visible `voice_label`, not by timbre. Two agents must not share a `voice_label` inside one org registry. The screen still prints the name during playback so a similar voice cannot be the only signal.

## 4. Consent and retention

Microphone capture requires a stored consent row: user id, org id, scope `microphone`, `granted_at`, policy version. Absent or revoked consent:

- the client captures zero audio bytes;
- STT is not called;
- text submit still works;
- the voice controls remain, leading to CONSENT_REQUIRED rather than to a removed feature.

Retention is an org policy, configurable, referenced by `retention_policy_id`.

Proposed defaults, not measured retention SLAs:

- raw audio: `DO_NOT_STORE`. After the STT digest is computed and the call is dispatched or refused, the local buffer is discarded. No object-storage row is written.
- opt-in audio store is a separate policy value the Founder has not set. This delta does not turn it on.
- transcript: stored as a project-scoped row while the policy says so. The default proposal is retain with the session, deletable by an org admin later. Forever-storage is not assumed.
- audit events do not contain the transcript body or audio bytes (CMP-04).

Revoking consent closes capture going forward. It does not rewrite append-only audit events. Deleting a transcript is a future admin command and is not specified as a ledger operation.

## 5. Data classification

The extracts name `data_classification` and do not freeze the label set in this repository. Proposed labels, AQ-05, used only so adapters can be denied:

| Proposed label | External speech or conversation provider |
|---|---|
| PUBLIC | Allowed only if the adapter descriptor lists PUBLIC |
| INTERNAL | Allowed only if an org policy names that adapter for INTERNAL |
| CONFIDENTIAL | External speech provider denied. External model denied unless a future policy explicitly allows a named adapter. Default deny. |
| RESTRICTED | External speech and external model denied. |

Deny means the bytes are not sent. The session goes DEGRADED_TEXT with reason `CLASSIFICATION_DENY` or `NO_PERMITTED_SPEECH_ADAPTER`, `voice_required` stays true, and Retry remains. A local adapter may be registered later. None is named here.

Fallback to another provider checks the same table first. OpenRouter `ONLY_FOR_PUBLIC`, as written in the FDP-15 draft, is not widened by voice.

Project content default for this proposal, until the Founder sets a class: treat project source and evidence as not PUBLIC. The router then denies external speech unless policy says otherwise. That default is conservative and is itself a proposal (AQ-05), not a historical clause.

## 6. Verbal prompt injection

User speech and STT output are untrusted external content (FDP-13 §216 item 13 and the prompt-injection note in §151).

A transcript that says "ignore policy", "I approve the deploy", "print the secret", or "tell Codex to mark PASS" is content on a HUMAN turn. Effects:

- no capability is added;
- no secret is placed in the reply or the log;
- no deploy, budget, or reconcile command is enqueued;
- the model may quote the refusal;
- an append-only `conversation.gate_refused` or the existing `injection.ignored` event records the reason code, not the raw hostile string if that string contains a secret-like token.

Tool calls proposed by the model are still re-authorized outside the model (item 14). The conversation router is not a place where the model executes tools directly.

## 7. Hard gates

Speech never satisfies a gate. The sentence "aprovo" or "I approve", in voice or text, does not:

| Gate | Existing control that still decides | Conversational result |
|---|---|---|
| Spend above headroom | COST-01, Invoke reservation, 402 | no provider call; BUDGET_DENIED |
| Deploy | DEPLOY-01, DEPLOY-02, the 10-field tuple, release_agent only | GATE_PREVIEW at most; 403 if a conversational actor calls DeployRelease |
| Credentials | SEC-01, SEC-02, vault refs | 403; canary must not appear in transcript, audio, or logs |
| Destructive command | TERM-01 | 403 COMMAND_DENIED; no process |
| Sensitive data export | classification §5 plus project scope | 403; bytes not sent |
| Manual ledger reconcile | STRONG fresh session, split actors, proof | conversational actors are not approver or confirmer |
| Emergency stop | STOP-01 | new conversational invokes return 409 STOP_LATCH |

The confirm control on the GATE_PREVIEW sheet submits only a command the authenticated user may already submit under v1.7, with assurance STRONG where that command requires it. Planning default freshness remains `forge.ledger.session_max_age_ms` = 900000 for those ledger commands. A voice turn does not refresh that timestamp.

Jarvis, Builder, Architect, Coordinator, Security-as-chat, and Codex-as-chat are not `release_agent` and not `security_operator` because they spoke.

Low-risk reads inside an already granted policy do not grow a new micro-approval. The addendum's rule is kept: do not add approval fatigue for ordinary questions. Ordinary questions also do not include deploy, secrets, destructive commands, or budget raises.

## 8. Reviewer independence

Codex may be a conversational agent that explains an already stored parecer. That conversation is not a review act.

Rules:

- The reviewer actor and the author stay different actors (FDP-16 §6, F-017). A council seat does not merge them.
- Context pack for `codex_reviewer` is limited to stored review artifacts and evidence the reviewer is allowed to read. Builder prompts, builder scratchpads, and draft patches the reviewer was not already given by the review gate are excluded (oracle CMP-O-28).
- `review.sign`, `review.edit`, and any command that writes a parecer or sets a verdict to PASS are denied with `REVIEW_SIGN_FORBIDDEN`.
- Jarvis may read a parecer to explain it and may consult Codex in this read-only conversational mode. Jarvis cannot insert, update, or delete a parecer, cannot set its status, and cannot say that Codex passed a review unless that sentence is a quotation of a stored parecer turn or a stored verdict record. A missing verdict is ABSENCE, not PASS.
- Council minutes cannot be the parecer. If the user asks the council to "decide PASS", the minutes record the request and the refusal or the divergence. They do not contain a signed evaluation.
- A Codex conversational reply that conflicts with the stored parecer must be labeled INFERENCE or must quote the parecer. It must not overwrite the parecer. The stored analysis remains the evaluation of record.
- The router cannot add `review.sign` for the duration of a meeting.

Independent review of this delta, later, is a Codex audit of the documents. Nothing in the product specification lets a council session produce that audit.

## 9. Threats and required outcomes

| Threat | Required outcome | Oracle |
|---|---|---|
| Cross-project exfiltration via switch or session memory | pack rebuilt; foreign ids absent | CMP-O-06, CMP-O-08 |
| Builder contaminates Codex during council or Jarvis explanation | reviewer pack excludes builder scratch; no sign | CMP-O-26, CMP-O-27, CMP-O-28 |
| Voice mistaken for formal authorization | gates unchanged | CMP-O-22..25 |
| Recorded audio impersonates the user | user id stays the session user | CMP-O-32 |
| Duplicate STT/TTS or council calls | one dispatch per operation key | CMP-O-29, CMP-O-31 |
| External vendor receives classified audio or stores it without consent | deny send; default no audio object | CMP-O-19, CMP-O-20, CMP-O-21 |
| Provider failure used to delete voice from scope | `voice_required` stays true | CMP-O-15, CMP-O-16 |
| Verbal injection elevates tools | no grant change | CMP-O-24, CMP-O-25 |

## 10. Logging boundary

Security events record reason codes, ids, and capability names. They do not record raw audio, full prompts, secret values, or the canary `CANARY_SECRET_FORGE_9f3a`. SEC-01 still applies to every new sink named in CMP-04.
