# CMP-01 — PRD and UX journeys

Status: DELTA CONVERSATIONAL-MVP v0.3 — CANDIDATE FOR CODEX REVIEW. DRAFT / NOT APPROVED / NOT READY FOR BUILD / NO BUILD-00 AUTHORIZATION. No tests executed. No staging. No Founder approval inferred. FDP-14 and FDP-15 remain pending. No voice provider is chosen or contracted.

This file is a proposed UX delta. It is not a recovered FDP-11. The gap is recorded in [CMP-06-TRACEABILITY-AND-IMPACT.md](CMP-06-TRACEABILITY-AND-IMPACT.md). It does not amend the v1.7 oracle table, the 41 F-stories, or the Round 10 parecer.

The addendum's phase table, which deferred voice, is superseded by the Founder decision. The addendum's other principles are kept: fact versus inference versus suggestion, Codex read-only, speech is not irreversible authorization, minimization, council as a workflow, and "show evidence" opens a real record.

## 1. Product outcome

On the first testable Forge version the Founder can enter STUDIO, start Jarvis by voice, talk to any registered conversational agent through the same composer, convene a Technical Council by voice, hear and read identified turns, question evidence, and end the session, with audit and hard gates still in force.

Uniform chrome is not uniform tool access. Jarvis does not raise anyone's privileges.

## 2. Entry and information architecture

Desktop ergonomics are the target (Tauri + React STUDIO already in the frozen stack). If a mobile frontend exists later, the same composer stacks vertically. This delta does not authorize a new mobile client.

STUDIO gains four tabs. Names are product labels, not a claim that the screens exist:

| Tab | Job |
|---|---|
| Conversar | Jarvis entry and 1:1 conversation |
| Conselho | Convene, follow, interrupt, minutes |
| Agentes | Registry of conversational agents and their capability summary |
| Evidências | Open a real evidence record, or an explicit absence |

Candidate layout inherited as a UX proposal from the addendum, not as an approved FDP-11 clause: one interlocutor menu, one composer bar.

The interlocutor menu lists only agents present in the conversational registry for this organization and project. The minimum roles named by the Founder are Coordinator, Builder, Architect, Security, Codex (audit read-only), and Jarvis. A role that is not registered is not shown. Adding an agent later requires a registry row; it does not require a second UI.

## 3. Universal composer

One component is reused in Conversar, Conselho, and Jarvis. It is specified here and bound to contracts in CMP-02.

Controls, all visible:

- text field;
- microphone button;
- audio output toggle;
- interrupt button, enabled while audio is playing or a provider call is in flight;
- live transcript;
- agent identity of the current speaker;
- "Mostrar fontes" / Show sources.

The microphone is push-to-talk or an explicit listen toggle. Always-on listening is not the default (AQ-08). Capture starts only after microphone consent (CMP-03).

### 3.1 UI states

| State | User sees | Audio | Next |
|---|---|---|---|
| IDLE | Composer ready. Agent name visible. | Silent | LISTENING or text submit |
| CONSENT_REQUIRED | Mic disabled. Text enabled. Consent action visible. | No capture | IDLE after grant, or stay in text |
| LISTENING | "Ouvindo" / Listening. Level meter. | Capture local only | TRANSCRIBING, IDLE on cancel |
| TRANSCRIBING | Partial or final transcript. | Local buffer until commit | THINKING or DEGRADED_TEXT |
| THINKING | Busy, named agent. Interrupt stays available. | Silent | SPEAKING, TEXT_READY, REFUSED, DEGRADED_TEXT |
| SPEAKING | Transcript in sync with playback. Speaker name before the words. | TTS of that turn only | IDLE, INTERRUPTED |
| TEXT_READY | Full transcript. Audio toggle off or TTS unavailable. | Silent | IDLE |
| INTERRUPTED | Prior turns kept. Playback stopped. | Stopped locally first | LISTENING or text |
| DEGRADED_TEXT | Banner with reason and Retry. Voice controls remain. | No claim that voice left the MVP | retry or text continue |
| REFUSED | Refusal reason in the transcript. No fake success. | Optional spoken refusal if TTS is up | IDLE |
| BUDGET_DENIED | 402 explanation. No invented balance beyond ledger fields the user may see. | No provider audio | IDLE |
| GATE_PREVIEW | Effect preview and a separate confirm control. Not part of the chat bubble. | Speech cannot press confirm | authenticated confirm or cancel |

Listening, speaking, and busy are distinct. A spinner alone is not an identity.

### 3.2 Claim labels

Every agent bubble shows one of: FACT, INFERENCE, SUGGESTION, ABSENCE. The label is the turn's `claim_class`. A spoken answer uses the same label on screen. Audio must not be the only place a refusal or an absence exists.

## 4. Journey A — Jarvis by voice (FD-1)

1. Authenticated user opens Conversar inside a project they belong to.
2. Jarvis is the default interlocutor only after an explicit activation control. Activation is not a grant.
3. User grants microphone consent if it is not already stored for this org policy.
4. User speaks a question about real project data, or types it.
5. Transcript of the user turn appears before the model reply is trusted.
6. Jarvis answers in voice when the audio toggle is on and TTS is available, and always in text on screen.
7. User may interrupt playback. Prior turns remain. The next utterance continues the same `session_id`.
8. "Show sources" runs Journey E. It does not invent a status.

Context resume means the same open session replays its own authorized turns. It does not import another project's memory.

## 5. Journey B — any registered agent, voice and text (FD-2)

1. User opens the interlocutor menu and selects one registered agent by name and role.
2. The composer does not change. STT/TTS stay at the UI boundary when that agent cannot accept audio itself.
3. A spoken question and a typed question are both first-class. Neither is a fallback that deletes the other.
4. The reply's `speaker_agent_id` is that agent. Jarvis is not credited for a direct 1:1 answer.
5. Switching agent is Journey D, not a hidden merge of prompts.

There is no "text-only because it was easier" path for a registered conversational agent. An agent absent from the registry is out of the menu rather than silently downgraded.

## 6. Journey C — Technical Council (FD-3)

Council is an orchestration workflow. It is not several models agreeing by themselves.

1. User selects at least two registered agents, writes or speaks an agenda, and convenes.
2. The room shows the agenda, the participant list, and whose turn it is.
3. Each turn has one speaker. The screen prints the role name. Audio, when on, speaks a short identity preface from the same string ("Architect.") before the content. Acoustic similarity is not identity.
4. Divergences are stored as their own records. The UI lists them. It does not collapse them into "the council agrees".
5. The user may interrupt playback, speak or type, ask one named agent for the next turn, or request minutes.
6. Minutes (ata) quote `turn_id`s and evidence refs. Where a claim has no evidence, the minutes say ABSENCE. Minutes are SUGGESTION unless every quoted claim is FACT with a ref. They do not replace a human decision or a Codex parecer.

A council that produces one unlabeled paragraph fails the journey.

## 7. Journey D — switch interlocutor (AC-2)

1. From an open session the user picks another registered agent.
2. The UI names the switch and the new speaker.
3. The context builder drops anything the new agent may not read: other projects, other orgs, secrets, and the previous agent's unshared scratchpad.
4. A short handoff note is shown only if it survived that filter. The user can see that the note is a filtered summary, class INFERENCE, not a copy of the other agent's hidden prompt.
5. Conversation continues in the same session id only when the switch is in-session. The authorized pack is still rebuilt. Same session id is not permission to keep the old pack.

## 8. Journey E — Jarvis summons or transfers (FD-4, AC-4)

1. User asks Jarvis, by voice or text, to bring a named specialist.
2. Jarvis may invite that agent or transfer the next turn. The invite itself is not the answer.
3. The specialist's reply is a new turn whose `answered_by_agent_id` is the specialist.
4. If Jarvis then summarizes, the summary turn lists the source `turn_id`s. It must not attribute to Codex a conclusion Codex's turn did not contain, and it must not write or sign a parecer.

## 9. Journey F — show evidence (AC-6)

1. User activates Show sources on a turn, or asks "mostrar evidência".
2. The client calls the evidence read for that turn's refs.
3. If a bundle exists, the Evidências tab opens that record: id, hash, timestamps, project. It does not open a generated lookalike.
4. If none exists, the transcript row is ABSENCE with reason `NO_EVIDENCE`. No percentage, test result, or status is filled in.

"Qual o status?" reads stored state. It does not compute a decorative percent.

## 10. Journey G — speech failure (AC-5)

STT down, TTS down, or no classification-compatible adapter:

- the thread remains usable in text;
- a banner names the failing capability and offers Retry;
- the microphone and speaker controls stay on screen;
- session and product flags do not change from "voice required" to "voice removed";
- no second hidden provider is called by the client.

Retry is not one button with one meaning. The label follows CMP-02 §9:

- RETRY_SAME_OPERATION only when that speech operation has not been dispatched;
- RECONCILIATION_REQUIRED when the provider result is unknown or the reservation is HELD, and that control does not call a provider again;
- NEW_ATTEMPT only after a conclusive NO_EFFECT, and only as a new turn with a new `operation_ref`;
- REPLAY_RESULT when a conclusive receipt already exists, returning the stored result and not calling the provider again.

A changed utterance is a new turn. Identical bytes after audio discard use the stored digest. Details are CMP-02 §7.2 and §9, and CMP-04.

Degraded mode is an availability error. It is not a scope cut.

## 11. Journey H — governed action preview (AC-8)

Talking about deploy, spend, credentials, destructive commands, or sensitive data may produce a GATE_PREVIEW sheet:

- what would change;
- which existing gate applies (CMP-03);
- a confirm control that is not the microphone and not the sentence "aprovo" / "I approve".

The chat transcript may record that a preview was shown. The preview's confirm control is the only UI that can submit the already-specified authenticated command, and only when that command's actor and assurance rules already allow this user. Jarvis cannot press it.

## 12. Accessibility

Proposed requirements, not a certification and not a measured score:

- every control has a name, including mic, interrupt, audio toggle, agent menu, and Show sources;
- transcript is a live region, so a screen reader hears turns without relying on TTS;
- interrupt is a keyboard-operable button, not only a spoken barge-in;
- focus order is composer, then latest turn, then evidence;
- color is not the only speaker indicator; the name is text;
- audio toggle off still completes the task in text;
- `prefers-reduced-motion` disables non-essential animation and does not block playback the user explicitly started;
- captions are the transcript itself, visible during SPEAKING.

No information that the Founder needs for a decision is audio-only.

## 13. Failure and empty copy

| Condition | Copy rule |
|---|---|
| No agents registered | Empty Agentes tab. Do not invent a roster. |
| No project membership | 403 state. Do not open a session. |
| No evidence | ABSENCE / `NO_EVIDENCE`. |
| Provider down | DEGRADED_TEXT plus Retry. |
| Budget deny | BUDGET_DENIED. Do not show a fabricated remaining percent. |
| Reviewer asked to sign | REFUSED / `REVIEW_SIGN_FORBIDDEN`. |
| Consent missing | CONSENT_REQUIRED. Text still works. |

## 14. Non-goals of this UX

- Always-listening wake word as a default.
- Voice biometrics or "sounds like the Founder".
- A second design system cloned from Founder OS. Visual reuse is allowed only as reference until a shared baseline is approved (AQ-09).
- Mobile-only flows.
- Treating a council transcript as a Codex verdict.

## 15. Binding

Journeys A–H are the flows cited from CMP-06. Screen behavior that spends money, stores audio, or calls a model is illegal unless CMP-02 and CMP-03 allow it. Oracles CMP-O-01 through CMP-O-36 exercise this file. None have been run.
