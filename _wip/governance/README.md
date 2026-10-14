# AI Governance Deck — Canonical Specification

This is the generic, customer-agnostic version of Akka's AI-governance narrative: eleven
operating principles, told as one continuous story, bracketed by a title and close slide.

## Source of truth

The narrative here is not invented by this deck — it's a rendering of two upstream
sources, in this priority order when they conflict:

1. **Derive from this version of Tyler Jewell's 10-principle script in #governance** (Slack, `C0AASAK640K`,
   [permalink](https://typesafe.slack.com/archives/C0AASAK640K/p1790204420527749)) — the
   actual script this deck is built from, each principle mapped to one slide. Treat the
   **most recent** of Tyler's messages as authoritative where an earlier one disagrees. 
   - We may blend some details of the principles for clarity or organization, but keep to 10. 

   
2. **The `governance-explainability` repo's canonical specs** (a separate, akka-org repo —
   paths below are repo-relative within it, not links from here) — the enforced, versioned
   product truth that the narrative must stay honest to. Key pointers:
   - `specs/README.md` — navigation index for every canonical spec; its "Canonical specs"
     table names the single owner of each concept.
   - `framework/schema/control.schema.yaml` — the enforced control-mechanism taxonomy
     (currently v2.6). This is machine-checked (`tools/auditors/10-mechanism-coverage/`),
     so it's the hardest source available for "what are the control types."
   - `specs/vision/evalmatrix.md` — the Eval Matrix model and mechanism list in narrative
     form.
   - `specs/platform/agentgateway-enforceable-controls.md` — the gateway/non-Akka-agent
     enforcement story (Principle 9).
   - `specs/vision/governance-workflow.md` — a four-page workflow narrative; useful for
     the "why," but dated 2026-06-13 and behind the schema on specifics (e.g. its
     lifecycle framing predates later detail) — don't treat it as more current than the
     schema or Tyler's Slack script.
   - Live console (`akka-console-ai-canvas`, Verify → Verdicts) — the source for the
     **verdict vocabulary** (Upheld / Breached / Inconclusive / Error). This vocabulary is
     product-UI terminology, not defined in any spec file or Slack message found so far;
     treat the running console as ground truth for it.

When the deck and a source disagree, the source wins — fix the deck, don't reinterpret
the source.

## The eleven principles → slides

| # | Folder | Principle (Tyler's wording, condensed) |
|---|---|---|
| 1 | `01-posture` | Controls are defined independently of the system, from risk appetite and policy; enforced consistently; the result is a provable governance posture, not an asserted one. |
| 2 | `02-lifecycle` | Define your risk, identify your controls, sign those controls, enforce them, measure compliance. |
| 3 | `03-control-types` | Controls are a discrete, provable check, reducing to **five** types: guardrails, evals, humans, gates, sanitizers — not a sixth "policy" type. |
| 4 | `04-control-sources` | Controls are derived from: AI regulation, corporate standard, or written by an individual. |
| 5 | `05-controls-as-software` | Controls are managed like software — packaged into a signed, versioned bundle that is applied discretely to a given agentic system. |
| 6 | `06-trace-outcomes` | Control outcomes are traced with the same infrastructure as the AI system itself. |
| 7 | `07-three-environments` | Environments — documentation stores, pre-production (testing), production — aggregate into one compliance view. |
| 8 | `07b-compliance` | Compliance is observing the verdicts for a group of controls over time: compliant right now, and drifted or not. |
| 9 | `08-drift` | Drift: comparing control outcomes for the same model/agent/system over time (stored outcomes, EvalKit/RedKit experimentation). |
| 10 | `09-ai-gateway` | Akka provides an AI gateway, agent runtime, and control runtime in the same environment — controls enforce on Akka agents **and** (mostly) non-Akka agents. |
| 11 | `10-tokenomics` | Traces, tokens, and verdicts are recorded together; token visibility across all models/agents enables cost governance — budgeting, chargeback, real-time optimization. |

Plus `00-title`, `00a-cibc-requirements`, `00b-ai-regulations`, and `zz-thankyou` around the eleven. `00a` carries a customer name and belongs only in a customer copy; `07b` is the one principle that goes beyond Tyler's original ten-principle script.

## Known gaps against the canonical source

These are tracked here rather than silently corrected, so the next slide-finalization
pass has a clear punch list:

- **Human-control sub-flavors are unresolved upstream.** A Slack thread
  ([permalink](https://typesafe.slack.com/archives/C0AASAK640K/p1789651125909609), same
  week as the 10-principle script) proposed five flavors for the `human` mechanism
  (decision / authorization / monitoring / feedback / halt), but ends without Tyler
  confirming that over an earlier three-form framing from a GitHub issue. Doesn't affect
  this deck today — "Human" is a single slide, not broken into flavors — but don't invent
  a flavor breakdown here without re-checking that thread first.
- **Gateway wording (slide 09).** Tyler said the gateway covers "guardrails and evals". The
  spec (`agentgateway-enforceable-controls.md`) says scheduled batch evaluations don't run in
  the request path. The script says "evals on live traffic" to stay inside both. Confirm
  with Tyler.
- **"Breach" vs "violation".** Tyler asked for "violation", because breach reads as data
  breach. The deck and scripts say "violated". The console may still label these
  "Breached", and the runbook's Demo 1 steps describe that label.
- **Customer slide in the generic deck.** `00a-cibc-requirements` carries a customer name,
  which this README says doesn't belong here. It belongs only in a customer copy.
- **EU AI Act figures (slide 00b).** Checked against the Act's text on 2026-10-13: only
  prohibited practices carry the 35 million euro / 7% ceiling (Art. 99(3)); documentation
  retention is ten years (Art. 18). The log retention period (Art. 19) isn't verified, and
  the scripts don't state one.
- **Voice check.** The `house-voice` skill named in the repo's `CLAUDE.md` wasn't available
  when the scripts were written, so they haven't had a voice pass.
- **Presenter file.** `presenters/smitty.json` lists LinkedIn `smithweygant`. Check it isn't
  a typo; it prints on the title and close slides.
- **Slide framing audit.** `tools/auditors/pgdn-frame` looks for Edge at Windows paths, so it
  can't run on a Mac. Slides were measured in Chrome instead (all fit a 763px viewport);
  only 00b, 02 and 06 were viewed rendered.

## Talk track

`SPEAKER-NOTES.md` carries each slide's cue, script, land points, and sources, following
Tyler's 2026-10-05 walkthrough. Demo 1 is its own teleprompter page; the Canvas (slide 06)
and Optimize (slide 10) demo cues sit inside their slides' pages. Slide 00a is omitted from
the teleprompter. Scripts are written for the ear and are the only text the teleprompter
files carry.

## Build

```
cd _wip/governance && python3 builder/build.py
```

Output lands at `generated/overview/index.html`. Pass `--mode`, `--presenter`, or `--out`
as documented in `builder/build.py`.

## Demo

See `PRESENTER-RUNBOOK.md` for desktop setup, console startup, and the slide-by-slide
walk with demo cues. `SPEAKER-NOTES.md` is the talk-track source of truth per slide; the files in `teleprompter/` are generated from it (`python3 tools/teleprompter/build.py _wip/governance --presenter smitty`).

## Customer decks

A customer-specific copy is a standalone seed of `builder/`, `shell/`, `slides/`, and
`assets/` from this deck. No customer name, ask, or live tenant data belongs in this repo.

## Where things live

- `SPEAKER-NOTES.md` holds every spoken word, demos included. `teleprompter/` is generated from it.
- `demos/` holds the click sheets, checks, and resets for the four console demos.
- `PRESENTER-RUNBOOK.md` covers the demo environment and the deck build. `demo-env.sh` runs it.
