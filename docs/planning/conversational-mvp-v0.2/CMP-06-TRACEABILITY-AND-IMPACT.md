# CMP-06 — Traceability and impact

Status: DELTA CONVERSATIONAL-MVP v0.2 — CANDIDATE FOR CODEX REVIEW. DRAFT / NOT APPROVED / NOT READY FOR BUILD / NO BUILD-00 AUTHORIZATION. No tests executed. No staging. No Founder approval inferred. FDP-14 and FDP-15 remain pending. No voice provider is chosen or contracted.

This file classifies impact. It does not amend v1.7 and it does not invent historical clauses. Codex PASS of v1.7 at `0c42373d583dec420348efd7bc0b8c6228a66f47` is not a PASS of this delta.

## 1. Source inventory

| Source | What was found | How this delta uses it |
|---|---|---|
| `docs/governance/FOUNDER-DECISION-JARVIS-VOICE-ALL-AGENTS-MVP-2026-10-13.md` | Functional decision, 2026-10-13. Voice is mandatory in the first testable version. | Binding for scope. Not an FDP approval and not BUILD-00. |
| `docs/governance/ADDENDUM-CONVERSATIONAL-COUNCIL-JARVIS-2026-10-13.md` | Principles plus a phase table that deferred voice. | Principles kept. Phase table and the open voice question are superseded by the Founder decision. |
| `docs/governance/IMPACT-ASSESSMENT-CONVERSATIONAL-MVP-2026-10-13.md` | Impact inventory. States it is not a new approved baseline. | Used as the delivery checklist. Not treated as normative. |
| `docs/reviews/PARECER-CODEX-ROUND10-2026-10-13.md` | Documentary PASS of v1.7 only. NEW-MEDIUM-12 closed. FDP-14, FDP-15, Founder approval, and BUILD-00 still pending. | Left byte-stable. Not reopened. |
| FDP-16, FDP-16A, FDP-17, FDP-19, FDP-19A, matrix, all v1.7 | Closed baseline candidate, Codex documentary PASS at the SHA above. | Cited, not edited. |
| `historical/round4/.../FDP-13-v1.0__msg077.md` | Security extract. §191 lines 2272–2288 are the 17 P0. §216 is the frozen-decision list. §25 names policy inputs including data_classification. | Inherited constraints. Extract is not a signature page. |
| `historical/round4/.../FDP-14-v1.0__msg080.md` | Observability extract. §6 OpenTelemetry. §8 correlation. §207 decisions, including no fake percentages and no indiscriminate prompt collection. | Inherited constraints. Founder confirmation still pending. |
| `historical/round4/docs/planning/FDP-15-v1.0-INTEGRATION-ADAPTER-SPECIFICATION.md` | Draft → review. ForgeContract → Adapter → Provider. Three families. Idempotency, privacy-before-fallback, OpenRouter optional. | Inherited as a draft constraint. Not approved. Not edited. |

## 2. FDP-11 gap

Searched the tree for an isolated FDP-11 specification.

- No file name contains a normative FDP-11 document.
- `historical/round4/docs/source-material/chat-extracts/FDP-10-v1.0__msg068.md` lines 2234–2258 are the end of FDP-10. They announce the next step titled "FDP-11 — FRONTEND / UX TECHNICAL SPECIFICATION" and list topics: layout, navigation, STUDIO, sidebar, Project Orchestrator, Decision Center, Build screen, Test screen, Operations, Simple/Expert View, component hierarchy, frontend state, events, empty/loading/error states, interactions, accessibility, responsive behavior, tldraw integration, design tokens, prototype flows. There are no numbered clauses under that title. It is not a specification body.
- FDP-12, FDP-13, and FDP-14 extracts contain sequence lines of the form "FDP-11 ✅". Those lines do not include the text.
- FDP-15 v1.0 line 1058 says contact points were foreseen in "FDP-11 (§161–165)" for Engine Setup, Engine Health, and Secrets UX. Those section numbers are not present in this repository. The citation is not treated as recovered normative text.

The historical snapshot was not edited. CMP-01 is a proposed delta for the conversational surfaces only. It does not claim to be FDP-11 §161 or any other missing paragraph. Screens outside conversation (Build, Test, tldraw, Decision Center) are not respecified here.

## 3. Impact by document

| Document | Impact | Edit in this delta |
|---|---|---|
| FDP-11 | Gap. Proposed journeys live in CMP-01. | none, because there is no file to edit |
| FDP-13 | Conversational consent, classification, verbal injection, and gate refusal reference the extract. The 17 P0 sentences stay on their current stories. | no edit |
| FDP-14 | CMP-04 proposes session_id, turn_id, conversational events, and minimization. It does not confirm the extract and it does not publish a metric value. | no edit |
| FDP-15 | Speech capabilities are proposed as TOOL-family contracts, provider-agnostic. Vendor not chosen. | no edit |
| FDP-16 / FDP-16A v1.7 | Router and turns are specified beside the ledger. Money, proofs, Task states, and InvokeCapability's coding_engine actor are unchanged. AQ-01 and AQ-02 block a future schema change. | no edit |
| FDP-17 v1.7 | Method of fixture, steps, positive rule, negative rule, NOT RUN is reused for CMP-O. The sentence at line 31 that says "v1.6 matrix" is LOW-01. It is intentionally not corrected here, so the audited SHA's file stays byte-stable. | no edit |
| FDP-19 / FDP-19A v1.7 | 41 stories stay the backlog index. CMP-S01..CMP-S13 are only in CMP-05. | no edit |
| Matrix v1.7 | 91 oracles remain the only normative baseline table. | no edit |
| Round 10 parecer and historical snapshots | Closed record. | no edit |

## 4. Founder item to future evidence

Each functional item has a flow, a contract, a policy, at least one oracle, and a future evidence pointer. Evidence files are ABSENT. Oracles are NOT RUN.

| ID | Founder item | Flow | Contract | Policy | Oracle | Future evidence |
|---|---|---|---|---|---|---|
| FD-1 | Jarvis by voice on the first testable version, with text, transcript, interrupt, resume, real project data | CMP-01 §4 | CMP-02 §4 and §7 | CMP-03 §4 consent | CMP-O-01, CMP-O-02, CMP-O-33 | CMP-04 `conversation.turn_completed` |
| FD-2 | Voice and text for every registered agent; same UI, not same tools | CMP-01 §5 | CMP-02 §7.1 | CMP-03 §2 and §6 | CMP-O-03, CMP-O-04, CMP-O-05 | CMP-04 `forge.adapter.invoke` per capability |
| FD-3 | Council by text and voice, identity, interrupt, minutes, divergences | CMP-01 §6 | CMP-02 §4.3 and §6 | CMP-03 §8 no fake verdict | CMP-O-09, CMP-O-10, CMP-O-11, CMP-O-12 | CMP-04 `conversation.minutes_issued` |
| FD-4 | Jarvis as universal entry: find, invite, transfer, synthesize without stealing a reviewer's conclusion | CMP-01 §8 | CMP-02 InviteAgent and TransferTurn | CMP-03 §8 | CMP-O-13, CMP-O-14 | CMP-04 `conversation.handoff` |
| FD-5 | One composer, desktop first, responsive only if a mobile frontend exists | CMP-01 §2 and §3 and §12 | CMP-02 §2 | CMP-03 §3 identity is not timbre | CMP-O-05, CMP-O-34 | CMP-04 session_opened mode attribute |
| AC-1 | Select any registered agent; ask by voice and by text | CMP-01 §5 | CMP-02 §7.1 | CMP-03 §6 tools unchanged | CMP-O-03, CMP-O-04 | CMP-04 turn origin |
| AC-2 | Switch agent; keep only role, org, and project context | CMP-01 §7 | CMP-02 §5 | CMP-03 §2 | CMP-O-06, CMP-O-07, CMP-O-08 | CMP-04 handoff without pack body |
| AC-3 | Council of at least two, identity, user interrupt, minutes with sources | CMP-01 §6 | CMP-02 §6 | CMP-03 §8 | CMP-O-09, CMP-O-10, CMP-O-11, CMP-O-12 | CMP-04 minutes event |
| AC-4 | Jarvis transfers to the named agent; origin is auditable | CMP-01 §8 | CMP-02 §4.2 origin | CMP-03 §8 | CMP-O-13, CMP-O-14 | CMP-04 handoff event |
| AC-5 | STT or TTS failure degrades to text and offers retry; voice stays in scope | CMP-01 §10 | CMP-02 §7.2 and §9 | CMP-03 §5 deny is not a scope cut | CMP-O-15, CMP-O-16, CMP-O-35, CMP-O-36 | CMP-04 `conversation.degraded` |
| AC-6 | Show evidence returns a real artifact or says none | CMP-01 §9 | CMP-02 §11 | CMP-04 §6 | CMP-O-17, CMP-O-18 | CMP-04 `conversation.evidence_shown` |
| AC-7 | Mic consent, configurable retention, least access, classification for voice vendors | CMP-01 §3 | CMP-02 §4.1 microphone_consent_state separate from retention_policy_id | CMP-03 §4 and §5 | CMP-O-19, CMP-O-20, CMP-O-21 | CMP-04 `conversation.consent_recorded` |
| AC-8 | Spoken "I approve" does not clear spend, deploy, credentials, destructive ops, or sensitive data | CMP-01 §11 | CMP-02 §8 no money from speech | CMP-03 §7 | CMP-O-22, CMP-O-23, CMP-O-24, CMP-O-25 | CMP-04 `conversation.gate_refused` |
| AC-9 | Codex may explain; cannot be led to sign against the stored analysis; formal review does not reuse Builder state | CMP-01 §6 and §8 | CMP-02 registry deny review.sign; CMP-03 §8.2 review_run_id | CMP-03 §8 | CMP-O-26, CMP-O-27, CMP-O-28 | parecer hash unchanged; review_run_id not the Builder actor |
| AC-10 | Voice and council cost per session, model, and provider; limits; no duplicate calls | CMP-01 state BUDGET_DENIED | CMP-02 §8 and §9 | CMP-03 §7 COST-01 | CMP-O-29, CMP-O-30, CMP-O-31, CMP-O-35 | CMP-04 cost attributes; no measured amount in this package |

CMP-O-32 (recorded audio is not authentication) supports AC-8 and CMP-03 §3. It is not a separate Founder sentence; it is the impersonation threat from the impact assessment, specified so it is testable.

## 5. Classification

### Inherited, not newly approved

- v1.7 ledger, proof capturer `forge.provider_ingest`, one movement, late evidence, 11 Task states, 17 P0, 41 stories, 91 oracles.
- FDP-13 extract controls listed in CMP-03 §1.
- FDP-14 extract rules listed in CMP-04 §1, still pending Founder confirmation.
- FDP-15 draft rules: capability not vendor, three families, idempotency, privacy before fallback, OpenRouter optional, still pending Founder approval.
- Addendum principles other than the superseded phase table.
- Codex documentary PASS of v1.7 only.

### Newly approved functional decision

Only what the Founder decision states: Jarvis voice in the first testable version; voice and text for every offered agent; council by voice and text; Jarvis as entry and handoff; one UX pattern; the acceptance lines FD/AC above. Approval of that scope is not approval of a schema, a vendor, FDP-14, FDP-15, or BUILD-00.

### Implementation proposal, not approved

- Record shapes in CMP-02 §4.
- TOOL-family speech capabilities and contract version `cmp.speech.v0`, including the v0.2 request, result, error, and cancel schemas.
- Half-duplex streaming with local barge-in as the way to meet low-latency audio (AQ-07).
- Explicit activation instead of always-on mic (AQ-08).
- Classification labels PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED and the default that project content is not PUBLIC (AQ-05).
- Raw audio default DO_NOT_STORE (AQ-06).
- Split `microphone_consent_state` and `retention_policy_id`, with a null consent id when state is NOT_GRANTED (LOW-01).
- `conversation_router` actor and a reservation command whose effect matches InvokeCapability without using the coding_engine actor (AQ-01).
- One ledger-anchor Task per session (AQ-02).
- Planning timeouts in CMP-02 §7. They are not measurements.
- Event names in CMP-04 §3.
- Thirteen CMP stories and thirty-six CMP oracles. The two ids added in v0.2 are CMP-O-35 and CMP-O-36.
- Formal-review record `review_run_id` (HIGH-01). It does not edit F-017.

## 6. Conflicts and gaps marked for the Founder

| Topic | Classification | Why it is not silently resolved |
|---|---|---|
| Addendum phases deferred voice | Resolved by the Founder decision's precedence statement | Not left open. This delta follows the decision. |
| FDP-11 body missing, while FDP-15 cites §161–165 | Gap | Sections were not invented. CMP-01 does not pretend to be those sections. |
| Speech versus FDP-15's three adapter families | Open AQ-03 | A fourth family would contradict a draft frozen sentence. TOOL is the proposal. |
| Who may reserve conversational spend | Open AQ-01 | v1.7 InvokeCapability is coding_engine via gateway. The router must not impersonate a coding engine. |
| operation.task_id is NOT NULL | Open AQ-02 | A conversation is not a build task. A second money table is rejected by this proposal. |
| Which model may answer | Open AQ-04 | Must not be read as adding Grok or OpenRouter to the FDP-16 coding-engine MVP allowlist. |
| Classification enum | Open AQ-05 | The field exists in extracts; the label set does not, in this tree. |
| Low-latency audio means full-duplex or half-duplex | Open AQ-07 | The decision asks for low-latency audio contracts. This package proposes half-duplex plus local interrupt and does not buy a realtime vendor. |
| Round 10 editorial LOW-01, "v1.6 matrix" in FDP-17 line 31 | Left unchanged | The editorial note says to fix it only in an authorized editorial commit. Doing it here would change a byte of the audited baseline. This is not the CMP consent finding. |
| CMP v0.1 LOW-01, `consent_id` required on text-only open | Corrected in this v0.2 proposal | `microphone_consent_id` is null when state is NOT_GRANTED. `retention_policy_id` stays required. Not a Founder approval of the schema. |

No closed Round 10 finding is reopened. No regression against LEDGER-17 or LEDGER-18 is asserted, and none was introduced, because those files were not modified.

## 7. What a later Codex review of this delta can check

- v1.7 bytes unchanged relative to `0c42373d583dec420348efd7bc0b8c6228a66f47` for the normative planning set.
- Every FD and AC row in §4 has a flow, a contract, a policy, an oracle, and a future evidence name.
- Every CMP-O is NOT RUN and is absent from the v1.7 matrix.
- No vendor, no measured cost, no measured percentile, no BUILD-00 grant, no self-issued PASS.
- Speech does not create a second ledger or a proof capturer other than `forge.provider_ingest`.
