# AI Governance Demo — Speaker Notes

One section per slide, in delivery order.

Each section carries:
- **Cue** — the visual/staging moment: what's on screen, when to tab-switch, when to click.
- **Script** — the exact words to say, written for a teleprompter: plain sentences, numbers
  spelled as spoken, no stage directions inside the prose. A line of the form `>>> ... <<<`
  marks a demo handoff. `TELEPROMPTER.md` is generated from these blocks
  (`python3 builder/teleprompter.py`); edit the script here, never there.
- **Land** — the key points this slide must land, for a presenter who wants to speak more
  freely than the script and still hit everything required.
- **Sources** — where the copy is drawn from, so a future rev can trace it.

Presenter mechanics (tab-switching, build status, fallbacks) live in `PRESENTER-RUNBOOK.md`.

Voice follows Tyler's walkthrough of 2026-10-05 (Obsidian: `Projects/Governance/Governance
walkthrough 2026-10-05.md`). That file is a speech-to-text transcript with recognition
errors ("ACA" is Akka), so wording here is paraphrased from it, never quoted.

---

## Slide 00 — Title

- **Cue**: title on screen; presenter introduces themselves.
- **Script**:

    Hello, everyone. I'm Smitty, Field CTO for the Americas at Akka.

    Today I'm going to walk you through how Akka approaches AI governance. This is an operating model, not a product tour. We'll break the governance problem into its elements, build it back up one principle at a time, and then show you what it looks like running.

    Questions are welcome at any point. If I'm midway through a thought I may ask you to hold one for a moment, but please don't sit on it.

- **Land**: operating model, not a feature tour; principles first, then the running system;
  questions welcome throughout.
- **Sources**: —

---

## Slide 00a — Customer requirements

- **Cue**: five asks on screen, text verbatim from the customer. Don't read them word for
  word; summarize in order. This slide carries a customer name and belongs in the
  customer-specific copy of the deck, not the generic one.
- **Script**:

    Before the principles, I want to put your requirements on the screen, because everything that follows is organized around them.

    You asked us to show how governance applies to AI agents built outside your platform, such as Copilot or Appian.

    You asked how your internal policies become controls a machine can enforce, and what happens when one is violated.

    You asked how an application stays compliant over time, through runtime guardrails, prompt changes, newly connected tools, and risk reassessment.

    You asked for financial governance, with AI spend visible by department, use case, application, and owner.

    And you asked how a new AI use case moves from intake through risk assessment, approval, deployment, monitoring, and retirement.

    I'll point back to this slide as we go. I'll also be plain about what Akka does today and what we would configure with you.

- **Land**: each ask maps to later principles — outside agents to 10, policies and violations
  to 3 through 6, continuous compliance and drift to 7 through 9, FinOps to 11, intake and
  lifecycle to 2 and 5 (risk survey, versioned bundles, approval hooks); be honest about the
  intake workflow: today it is the risk survey plus hooks into the customer's issue system.
- **Sources**: customer requirements slide, text verbatim; Tyler's walkthrough (hooks into
  JIRA/SDLC for approvals).

---

## Slide 00b — AI regulations

- **Cue**: three stats on screen.
- **Script**:

    Why this matters now. Regulations are multiplying. The EU AI Act allows penalties of up to seven percent of global turnover for the most serious violations, and it requires providers to keep technical documentation for ten years.

    At the same time, most governance tools look at AI systems from the outside. They report after something has happened. They can't enforce at the point where an agent calls a model or a tool.

    So the questions are where enforcement lives, and how you prove it worked. The rest of this session answers both.

- **Land**: penalties are real; outside-in tools report after the fact; enforcement at the
  agent boundary is the gap.
- **Sources**: EU AI Act penalty and documentation-retention provisions.
- **Slide text to fix**: the slide says "Art. 72 requires petabyte-scale, tamper-proof audit
  retention" and "7% … for non-compliant agents". As I read the Act, Art. 72 covers
  post-market monitoring; the ten-year duty is documentation (Art. 18); 7% applies to the
  most serious violations only; "petabyte-scale" is not in the Act. Verify against the
  regulation text before the slide is used with a regulator-literate audience. The script
  above is worded to stay true either way.

---

## Slide 01 — You define your AI risk posture as sets of controls

- **Cue**: Decide / Define / Enforce rows on screen.
- **Script**:

    The first principle. You define your AI risk posture as a set of controls.

    Every business already has a risk appetite. It has regulatory duties, and it has corporate policy. Akka doesn't supply those. You decide them.

    What Akka does is turn those decisions into controls. A control is a discrete, enforceable check. You define controls independently of any one AI system, so governance and the agentic system are defined separately and managed separately.

    Once you have a set of controls, Akka enforces them consistently. The result is a posture you can measure.

- **Land**: risk appetite, regulatory duties, and policy already exist, Akka doesn't
  introduce them; they become controls; controls are independent of the AI system and
  managed separately from it; enforcement is consistent; the posture is measurable.
- **Sources**: Tyler's walkthrough; `governance-explainability` glossary (Governance
  Posture); `_wip/governance/research/posture-terminology-brief.md`.

---

## Slide 02 — Postures have a lifecycle

- **Cue**: categorization grid (Intent / Autonomy / Boundaries / Evidence) fades in, then
  the four lifecycle boxes with arrows. Trace both halves with the cursor. After the last
  line, cue Demo 1 (`PRESENTER-RUNBOOK.md` §4.1), which walks the loop in the console.
- **Script**:

    The second principle. A posture has a lifecycle, and Akka manages it like software. It has versions, it has releases, and it has history.

    It starts with a risk profile, which we capture in a risk survey. The survey asks four kinds of questions.

    Intent: what is this system for, and who is accountable. Autonomy: what can it decide on its own, and when must a human step in. Boundaries: who can it affect, and what data and dependencies shape it. And evidence: which regulations govern it, what evidence it must produce, and who attests to it.

    Your answers map to controls. Those controls are collected into a control matrix. The matrix is enforced on test systems and production systems. Then you measure how the posture is performing, and the verdicts and drift you find feed the next cycle.

    That's a loop, not a checklist. Rather than keep describing it, let me show it to you.

    >>> DEMO 1 — console: Define Risk, Identify Controls, Sign, Enforce, Measure <<<

- **Land**: posture is managed as software — versions, releases, history; four risk-profile
  categories; answers map to controls, controls form the control matrix, the matrix is
  enforced and measured; verdicts and drift restart the loop; hands off directly into
  Demo 1, so don't let this stand as a diagram.
- **Sources**: Tyler's walkthrough; console Verify → Risk survey (69 questions, seven
  categories, plain language); lifecycle graphic.

---

## Slide 03 — There are only five types of controls

- **Cue**: recap sentence, then the five rows, one example each. No new demo; this names
  what Demo 1 just showed.
- **Script**:

    You just watched a control get defined, signed, and enforced. Now let me name what a control is.

    A control is a discrete, provable check. It holds or it doesn't, and the outcome can be shown.

    There are only five types of controls, and every obligation you have reduces to one of them.

    A guardrail blocks or allows a call at a runtime boundary: before or after a model, a tool, an agent, or a memory call. For example, stopping a wire transfer that lacks dual sign-off.

    An evaluation measures and scores behavior that isn't deterministic. It runs against live agents or in test. For example, scoring responses weekly for parity drift.

    A human control covers the human-in-the-loop moments: approvals, halts, feedback and drift review. For example, a loan officer approves an adverse-action notice before it goes out.

    A gate is a release activity. It runs against documents or in pre-production to confirm a system is ready. For example, blocking a deploy that lacks a current bias-audit attestation.

    And a sanitizer redacts, masks, or strips data before it moves on. For example, removing an applicant's Social Security number before the model sees it.

    Policy isn't a sixth type. Policy decides which of the five apply.

- **Land**: a control is one discrete, provable requirement; exactly five types — guardrail,
  evaluation, human, gate, sanitizer; one grounded example each; gates run once before
  release or periodically; sanitizers can act before a tool call, a model call, or the
  verdict log; policy selects among the five and is not a type.
- **Sources**: Tyler's walkthrough; Tyler's pinned 10-principle script, #governance
  (`C0AASAK640K/p1790204420527749`); `framework/schema/control.schema.yaml`.

---

## Slide 04 — Controls are created in three ways

- **Cue**: corpus panel with the regulation badges and the 226 / 1,369 figure, then the
  corporate and project panels.
- **Script**:

    The fourth principle. Controls are created in three ways.

    First, Akka ships a corpus of two hundred twenty-six AI regulations, mapped to thirteen hundred sixty-nine controls. It covers the EU AI Act, SOC 2, GDPR, and the NIST AI Risk Management Framework, among others. Your risk survey answers select the controls that apply, and you can browse the corpus directly.

    Second, corporate policy. These are rules your enterprise has already written down, for example, no agent approves a refund over five hundred dollars without review. Corporate controls are inherited by every project, and you decide whether each one is required or optional.

    Third, a project can write its own, for a risk unique to that system, for example, this underwriting agent may never see an applicant's Social Security number.

    Once a control is in the bundle, it is enforced the same way, wherever it came from.

- **Land**: three sources — Akka corpus, corporate policy, project; corpus is 226
  regulations and 1,369 controls; each control traces to the exact requirement in the
  regulation, with effective dates and trigger conditions; corporate controls inherit
  automatically, required or optional; enforced identically regardless of origin.
- **Sources**: Tyler's walkthrough (corpus version 0.9: 226 regulations, 1,369 controls;
  the earlier "225" in the transcript is a slip); console Verify → Controls → Corpus.
  Re-pull live counts per engagement.

---

## Slide 05 — Groups of controls are placed into signed bundles

- **Cue**: three-stop timeline — Launches / Gains judgment / Gains authority — with the
  control count growing at each stop.
- **Script**:

    The fifth principle. Groups of controls are placed into a signed bundle. We call that bundle the control matrix.

    For each corporate or custom control, you explicitly accept it, waive it, or remove it. When the mapping is clean, you sign. Signing creates a version: a record of exactly which controls make up that scope of checks.

    Look at the example. The loan origination assistant launches answering borrower questions. The risk is disclosure accuracy, and version one carries twelve controls. It gains judgment and starts recommending approve or deny. Fair lending becomes a real risk, and version two carries thirty-four controls. Then it gains authority to initiate the wire transfer. Dual control becomes a risk, and version three carries fifty-one.

    Every version is kept, and you can compare any two to see how your posture changed. You roll forward. You don't roll back. A change creates a new version.

    One clarification. This signature is Akka versioning the set of controls. It isn't a human sign-off. If you want people to approve which controls go in, or to attest to a document, we connect that to your issue-tracking and development systems through hooks.

    When you deploy the bundle, the Akka runtime finds every place a control has to run and applies it. Your developers don't write extra code for it.

- **Land**: bundle equals control matrix; accept, waive, or remove each non-corpus control
  before signing; signing creates a version; capability growth drives risk growth drives
  matrix growth (12 → 34 → 51); versions are compared, rolled forward only, never erased;
  signing is not human approval — human review attaches through hooks; Akka is the runtime
  for both the AI system and the controls, so it injects controls without developer work.
- **Sources**: Tyler's walkthrough; `BundleSigner.java:48-110`; `demo/governance/signed/`.
- **Do NOT claim**: cryptographic attestation, RFC 3161 trusted timestamping, or a
  tamper-evident hash chain for bundles. Signing anchors a digest and creates a version.
  A hash chain exists for runtime audit events (`specs/corpus/aud-taxonomy.yaml:84-86`);
  don't conflate the two.
- **Do NOT promise**: a built-in human approval workflow. The hooks are implemented per
  customer. Tyler also named a real gap: authority to choose which controls enter a bundle
  is a different thing from a control that needs human attestation, and neither is built
  into signing today.

---

## Slide 06 — Every control execution produces a verdict

- **Cue**: verdict tiles and mini table on screen, then tab-switch to the console, Canvas
  (`PRESENTER-RUNBOOK.md` §4.2). Tile numbers are illustrative.
- **Script**:

    The sixth principle. Every time a control executes, it produces a verdict. The control was upheld, it was violated, the result was inconclusive, or it errored.

    Verdicts are written to a tamper-evident store. It's the same store that holds the traces of the AI system itself: the conversations, the model calls, the tool calls. So controls and behavior sit side by side, and nothing is self-reported.

    Let me ask the console what is true of this system right now.

    >>> DEMO — Canvas: ask which controls apply and whether they held this week <<<

    That answer isn't a canned report. It was generated from the same ledger an examiner would query. And every verdict carries its control, its execution, and its evidence, so I can go one level down on any of them and see why it landed where it did.

- **Land**: verdict = outcome of one control execution — upheld, violated, inconclusive, or
  error; stored tamper-evidently, co-resident with the AI system's own traces; Canvas answer
  is generated live; one live violation must be visible on screen.
- **Sources**: Tyler's walkthrough; console Verify → Verdicts.
- **Slide text to fix**: Tyler asked for "violation" in place of "breach," because breach
  reads as data breach. The slide still says "breached" in the subtitle and "Breached /
  error" on the tile, and the console may still show Breached. The script says "violated"
  to follow Tyler; confirm the console label before presenting.

---

## Slide 07 — Controls can execute in pre-production or production

- **Cue**: three columns — Documents, Pre-production, Production — and the retest table
  (full / targeted / records only).
- **Script**:

    The seventh principle. Controls can execute in pre-production or in production, and some are checks on documents.

    Production is where Akka enforces guardrails, human-in-the-loop controls, sanitizers, and evals against running systems.

    Pre-production is where you run tests, evaluations, model analysis, and red teaming before a change goes live. Akka gives you test, eval, and red-team kits for this, and they produce verdicts the same way production does.

    How much you retest depends on the change. A model swap, an architecture change, a new data source, or a new jurisdiction calls for a full retest. A prompt or parameter change, a retrain, or vendor model drift calls for a targeted one. A bug fix, an ownership transfer, or a lapsed attestation needs a records update only.

    Documents are the third place. A gate can check that a required attestation is on file and still fresh.

    Notice what this does for your engineering teams. They can find out whether a system will pass governance while they are building it, not after it's built and sent to a review. Some controls can only be verified in production, a human escalation for example, but you can test those behaviors in pre-production too.

    Verdicts from all three places are merged into one view.

- **Land**: three places; production enforces guardrails, human, sanitizers, and evals;
  pre-production runs tests, evals, model analysis, and red teaming, triggered by change
  (full / targeted / records-only); documents check attestations are present and fresh; kits
  produce verdicts like production does; shift-left — engineering learns during the build
  whether it passes, with no late compliance refactor; verdicts from all three merge into
  one view.
- **Sources**: Tyler's walkthrough (TestKit, EvalKit, RedKit); console Verify → Verdicts
  `Environment` facet (Production, Pre-production, Documents).
- **Open item**: Tyler flagged "pre-production" as a placeholder name earlier because it
  reads as release gating. The slide now frames it as change-triggered, which matches him.

---

## Slide 07b — Compliance is observing the verdicts for a group of controls over time

- **Cue**: two-line question slide. Optionally cut to the console compliance view (by
  bundle, by control).
- **Script**:

    The eighth principle. Compliance is observing the verdicts for a group of controls over time.

    We've talked about controls and risk profiles. Compliance is the question you ask of them. Is my AI system compliant right now? And has it drifted over time?

    You can look at it by control, by regulation, or by bundle. How well do I satisfy this regulation? How have all the controls in my bundle done?

    A violation tells you something happened. It doesn't by itself mean you're out of compliance. What matters is that you can see it and act on it. And everything here can be exported as OpenTelemetry spans, so your alerts and dashboards can live in the observability tools you already run.

- **Land**: compliance is a read of verdicts over time, not a separate measurement; views by
  control, regulation, and bundle; a violation is information to act on, not automatic
  non-compliance; OpenTelemetry export for alerts and dashboards.
- **Sources**: Tyler's walkthrough.

---

## Slide 08 — Drift is a pattern change in the verdict ledger

- **Cue**: query at the top, then two controls compared at two times. If time allows, run
  the same query live in Verify → Verdicts and open Replay (`PRESENTER-RUNBOOK.md` §4.3).
- **Script**:

    The ninth principle. Drift is a pattern change in the verdict ledger.

    You don't need a separate drift detector. Take a single control and watch its verdicts over time. If it behaves differently, that's drift.

    Here, the PII redaction guardrail was upheld three weeks ago. Today it returns an error, because the classifier score fell outside its valid range and the control failed closed. The storage limitation gate was upheld, and today it's inconclusive, because its retention schedule aged past its freshness window.

    Same control, same system. Only time changed.

    The verdict shows me what changed. Replay lets me open the session behind it and see why.

- **Land**: drift = a change in one control's verdicts over time; same ledger, no separate
  detector; verdicts show what, Replay shows why; the change is a prompt to investigate.
- **Sources**: Tyler's walkthrough; console Verify → Verdicts and Replay. Grounding
  examples: "PII redaction at model boundary" (Error, "score outside 0 to 1… failed
  closed"); "Storage limitation" (Inconclusive, "retention schedule is 410 days old, past
  its 365-day freshness window").

---

## Slide 09 — Controls can be enforced on third-party agents

- **Cue**: two rows — Built on Akka / Everything else — plus the in-agent note.
- **Script**:

    The tenth principle. Controls can be enforced on third-party agents.

    So far we could have been talking about agents that run on Akka. Many of the agents you run don't. Akka's AI gateway routes inference traffic and optimizes it. If you steer a third-party agent's model and tool requests through the gateway, we can identify that agent and enforce controls on it directly.

    That covers most of what you need from guardrails, sanitizers, and evals on live traffic. Some controls, a human-in-the-loop escalation for example, need changes inside the third-party agent itself. For those, the agent sends its traces to Akka's ledger, so its behavior still lands in the same record as everything else.

    For an agent built on Akka, the controls run natively in the runtime.

- **Land**: gateway routes inference and optimizes; routing a third-party agent's model and
  tool calls through it lets Akka identify the agent and enforce controls; most guardrails,
  sanitizers, and evals work in-path; human-in-the-loop controls need work in the agent;
  traces still go to the ledger; Akka agents get controls natively.
- **Sources**: Tyler's walkthrough; Tyler's pinned 10-principle script, Principle 9
  (`p1790204420527749`); `governance-explainability`
  `specs/platform/agentgateway-enforceable-controls.md` (for an agent you don't own, the
  gateway reaches 198 of 210 in-path-addressable controls; 1,159 of 1,369 corpus controls
  sit outside any data plane).
- **Do NOT claim**: the gateway enforces every control on a non-Akka agent; that it inspects
  multimodal content (text only); or that it sees in-process tool calls of an agent you
  don't run.
- **Check with Tyler**: he said the gateway covers "guardrails and evals." The spec says
  scheduled batch evaluations don't live in the request path. The script says "evals on live
  traffic" to stay inside both.

---

## Slide 10 — Traces, tokens, and verdicts are recorded together

- **Cue**: Observe / Scrutinize / Compare, then tab-switch to the console, Optimize →
  Spend (`PRESENTER-RUNBOOK.md` §4.4). Fall back to narrating the page if the stack isn't
  seeded.
- **Script**:

    The eleventh principle. Traces, tokens, and verdicts are recorded together.

    Every call is measured, by team, use case, and system. Whether an agent runs on Akka or its traffic comes through the gateway, the trace carries its token usage, its cost, and the verdicts that fired. It all lands in one data warehouse.

    Because it's all correlated, you can replay history, and you can see cost, performance, budget, and spend in the same place as governance.

    That gives you three things. Observe: every model call is measured. Scrutinize: each team sees its own system's spend, and you can set thresholds so a crossed line becomes an action. Compare: you can keep testing models against each other on cost and performance, against a registry of known models and their prices.

    Let me show you.

    >>> DEMO — Optimize → Spend: ask Canvas a cost question <<<

- **Land**: one data warehouse for traces, tokens, and verdicts; spend sliceable by team,
  department, use case, system; thresholds make spend actionable; periods can be compared,
  including savings after a change; model registry with input, output, and cache prices;
  continuous comparison of models on cost and performance.
- **Sources**: Tyler's walkthrough; console Optimize → Spend;
  `enablement/03-solution-akka-optimize.md:62-71`.
- **Dependency**: a live query needs the `optimize-local` synthetic stack seeded with
  traffic.

---

## Slide zz — Thank you

- **Cue**: close.
- **Script**:

    That's the operating model. You define your posture as controls, and you manage it as software. There are five types of controls, from three sources, packaged in signed bundles. Verdicts record every execution across pre-production and production, and compliance and drift are read from those verdicts. The same controls reach third-party agents through the gateway, and traces, tokens, and verdicts land together.

    Akka is one platform for your developers, your AI risk and security teams, your machine learning engineers, and your infrastructure engineers.

    I'll take questions now.

- **Land**: recap in slide order; one platform for developers, risk, security, ML, and
  infrastructure teams; open the floor.
- **Sources**: Tyler's walkthrough (closing exchange on who the platform is for).
