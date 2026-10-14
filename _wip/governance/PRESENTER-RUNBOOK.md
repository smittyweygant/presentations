# AI Governance Demo — Presenter Runbook

*Desktop / browser instructions for driving the deck + demos as if presenting live.
Companion to `README.md` (spec), `SPEAKER-NOTES.md` (talk-track), and `teleprompter/`
(the script text alone, generated from the notes; load `governance-smitty.textream` in Textream).*

Duration budget: ~45 min presentation + ~15 min Q&A (adjust to slot).

For a customer-specific session, work from that customer's own copy of this file at
`~/akka/customers/<name>/PRESENTER-RUNBOOK.md` if one exists — it may carry
engagement-specific timing, blockers, or asks on top of the mechanics below.

---

## 0. Pre-flight — the day before

### 0.1 Machine + software checklist

- [ ] macOS with JDK ≥ 21 (JDK 27 works — cross-compile is fine).
- [ ] Maven 3.9+.
- [ ] `~/.m2/settings.xml` has the Akka token (`https://repo.akka.io/maven/` server +
  repository blocks per `account.akka.io/token`).
- [ ] `chmod 600 ~/.m2/settings.xml` — tighten permissions.
- [ ] Chrome (any recent version) as the presentation browser.
- [ ] Slack + Gmail closed or muted (Do Not Disturb on).
- [ ] External display cable / adapter in bag. Test HDMI/USB-C output at least once.

### 0.2 Warm the Maven cache (do this once, day-of setup is faster)

```bash
cd ~/akka/governance-explainability
mvn -f services/workbench-svc/pom.xml -q -DskipTests dependency:resolve
```

Expected: exit 0, ~5 min first time, seconds thereafter.

### 0.3 Build the deck

```bash
cd ~/akka/presentations/_wip/governance
python3 builder/build.py --mode overview --presenter <name>
```

Output: `generated/overview/index.html` (~60 KB).

---

## 1. Desktop layout — what to have open when the session starts

Arrange these BEFORE joining the call. Use ⌘⇥ / Mission Control to move between:

| # | Window | State | Position |
|---|---|---|---|
| **1** | **Chrome — deck tab** at `file:///.../_wip/governance/generated/overview/index.html` | Fullscreen (F key) | Primary display |
| **2** | **Chrome — Console tab** at `http://127.0.0.1:9889` — pre-loaded to **Canvas, left-nav sections collapsed** (the audience's first view of the console — see §4.1 beat 1). **This one tab carries the entire console track**: Demo 1 (Verify → Risk/Controls/Verdicts, after Slide 02) and the Canvas/Verdicts-Replay/Optimize walkthroughs later. There's no separate workbench-svc tab — `workbench-svc` is a service this console discovers and surfaces natively, not a page of its own. | Regular tab | Same window as (1) |
| **3** | **Terminal — service log** running the workbench-svc (see §2.1) — still a separate process on port 8730; the console discovers and displays it, but it must be running | 40-col wide, visible | Second display (or hidden until needed) |
| **4** | **VS Code / editor** with `SPEAKER-NOTES.md` open | Second display or ⌘⇥ target | Secondary display |

Rule of thumb: **only the deck tab is ever shared to the room**. The console gets its own
tab switches (Chrome tab bar visible for a moment is fine — just don't linger). Terminal
and notes never make the shared feed.

---

## 2. Environment setup — the 10 minutes before you dial in

### 2.0 One command

`./demo-env.sh up --pull` runs §2.1, §2.5 and §2.6 in order: it fast-forwards
`governance-explainability` and `akka-console-ai-canvas`, stops everything, rebuilds the
console, and starts workbench-svc, the console daemon, the trace ledger and the Optimize
services. `./demo-env.sh status` reports what is answering and `./demo-env.sh down` stops it
all. Logs go to `/tmp/governance-demo-logs/`. Allow about 8 minutes cold. The sections below
are the manual steps it replaces.

### 2.1 Start the Demo 1 backing service (workbench-svc)

**Terminal window 3** (long-running):

```bash
cd ~/akka/governance-explainability
PROJECT_ROOT=./demo REPO_ROOT=. mvn -f services/workbench-svc/pom.xml -q compile exec:java
```

Wait ~33 seconds. When you see logs steady, verify:

```bash
# separate terminal
curl -s http://127.0.0.1:8730/api/overview | python3 -m json.tool | head -20
```

Should print JSON with a `matrix_id` and control counts. **If it doesn't, do NOT go
live** — see §5.1 recovery. Nothing is ever presented at `127.0.0.1:8730` directly — this
process just has to be up before the console starts (§2.5) so the console can discover it
and serve its data under Verify → Risk/Controls/Verdicts. Start this *before* §2.5.

### 2.2 Smoke-test Demo 1 in the console (2 min)

Open **Chrome tab 2** at `http://127.0.0.1:9889` (console must be running — §2.5). Click
through each of these once, all inside the console:

1. **Verify → Risk.** Page loads with a risk survey for the loaded project. **PASS if it
   loads immediately with no error banner** and at least one question already has an
   answer (confirms demo content is loaded, not a blank project).
2. Answer one unanswered question. **PASS if the "answered" counter above the survey tabs
   increments.**
3. **Verify → Controls → Corpus.** Filter the **In this project → Applies** facet (left
   rail). Expand any row's caret. **PASS if a citation panel opens** showing the source
   framework/article text.
4. **Verify → Controls → Bundle.** Confirm the **Candidates / In the bundle** tab split
   renders and an "accepted" counter is visible. Do **not** click Accept during this smoke
   test — every click is a real, persistent write against the demo project; save
   Accept/Sign actions for the dry run or the live session, not a repeatable smoke test.
5. **Verify → Controls → Sign.** Confirm the "Signing does not attest to any of the
   following" list renders and the **Signed bundles** table below has at least one row.
6. **Verify → Verdicts.** Confirm the ledger loads with verdicts, newest first, and a mix
   of **Upheld / Breached / Error** conclusions is visible without changing filters. (The
   console may still label violations "Breached"; say "violation" aloud.)

*Any FAIL = escalate before dial-in; do not present Demo 1 broken.* **Every Accept/Sign
click in the real session is a live, persistent write** — counters will read one higher
after every rehearsal and after the real thing. Re-pull live numbers before quoting any
count out loud; don't trust what's written in this runbook or the slides.

### 2.3 Stage Chrome tab 2 on Canvas, nav collapsed

Demo 1 and the Canvas/Verdicts-Replay/Optimize track share one tab and one smoke test
(§2.2 covers both), but the audience's first view of this tab matters — they've never seen
the console before. After §2.2 finishes (it leaves the tab on whatever Verify page was
tested last), navigate back to **Canvas** and collapse the **Specify** / **Verify** /
**Optimize** nav sections if any are expanded, so the left nav shows only its top-level
section names. That's the frame Demo 1's beat 1 (§4.1) opens on and narrates live — don't
pre-open Verify or pre-click into Risk ahead of time, the whole point of beat 1 is the
presenter doing that expansion on camera while explaining it.

### 2.4 Load the deck fullscreen

Open **Chrome tab 1** at
`file:///Users/smittyweygant/akka/presentations/_wip/governance/generated/overview/index.html`.
Press **F** (or ⌃⌘F) for fullscreen. Verify the title slide lands cleanly with your
name/title.

### 2.5 Start the local console (Specify / Verify / Optimize / Canvas)

The console lives in `~/akka/akka-console-ai-canvas` (Tyler's repo) and drives a complete
local Akka console — Specify, Verify (Controls/Risk/Traces/Replay/Verdicts), Optimize, and
the **Canvas** NL-question flow that backs the live-query demo beat.

**One-time machine setup** (skip once already done on a given machine):

1. Repos nested inside `~/akka/akka-console-ai-canvas/`: `kalix-console`
   (branch `ai-canvas-prototype`), `akka-cli` (branch `console-companion`), `nexus`
   (branch `local/trace-hooks`, with `migration/nexus-local-config.patch` applied).
   Restore from `migration/README.md` if these ever need re-cloning on another machine.
2. `~/.akka/local/canvas/profiles.json` — machine-specific paths (this machine's
   explainability checkout, `ask.cwd`, `projects.roots`, etc). Copy
   `canvas-bridge/profiles.example.json` and fill in per `docs/setup.md` §2 if missing.
3. `python3 -m pip install --user PyYAML` — the governance adapter's only Python
   dependency.
4. Toolchain: Node 22+, pnpm 10+ (`npm install -g pnpm@10.24.0`), Go 1.24+, protoc
   (`brew install protobuf`), jq.
5. One-time builds:
   ```bash
   cd ~/akka/akka-console-ai-canvas/akka-cli
   make generate-proto PROTOC_GEN_GO="$(go tool -n protoc-gen-go)" \
     PROTOC_GEN_GO_GRPC="$(go tool -n protoc-gen-go-grpc)"
   make download-local-console-assets build-reliability-dashboard
   cd ../kalix-console && pnpm install
   cd ../nexus && go -C cli build -o target/akka-optimize ./cmd/akka-optimize
   ```

**Every time you want to run it** — rebuild the embedded console + CLI (picks up any new
commits) and start the daemon:

```bash
cd ~/akka/akka-console-ai-canvas
bash scripts/build-akka-with-console.sh
akka-cli/build/akka local stop        # no-op if not running
akka-cli/build/akka local start       # backgrounds itself; daemonizes
akka-cli/build/akka local status      # confirm: HTTP localhost:9889
```

`build-akka-with-console.sh` calls bare `python`. If pyenv has no global version it fails
with `pyenv: python: command not found`; prefix the call with `PYENV_VERSION=3.12.8`.

The daemon keeps registered services in memory and has no unregister. A service started
from another project (for example a customer demo) stays listed as Unavailable until the
daemon restarts, which is why the `akka local stop` above is not optional.

Open **`http://localhost:9889`**. Left nav: Dashboard / **Canvas** / Services / Specify
(Specs, Docs, Auditors, Exit conditions) / Verify (Risk, Controls, Evaluations, Red
teaming, Traces, Replay, Verdicts, Compliance). Canvas ships starter questions — good for
a first smoke test.

**`optimize-local` synthetic stack** backs the Optimize pages. Bring it up from a cold
machine:

```bash
cd ~/akka/akka-console-ai-canvas/nexus
mvn -pl .,optimize,portfolio,trainer,registry,gateway-router,capture-refinery \
  -am install -DskipTests -Dnon-akka-service=true -Dspotless.skip=true
```

`-Dspotless.skip=true` works around a real bug, not a preference: the repo's formatting
check reflects into javac internals that newer JDKs removed, so a couple of services fail
to build without it.

```bash
cd ~/akka/akka-console-ai-canvas/optimize-local
python3 stack.py up                       # stub backends + agentgateway
python3 stack.py services-direct --discover   # 6 services, ~1-2 min cold
python3 seed.py all                       # catalog, routing, training, ~7 min
```

Then restart `gateway-router` **without** discovery (discovery-on grows its H2 file fast
and is only needed for the seed's `discovery`/`manifest`/`traffic` steps):

```bash
python3 -c "import json; p=json.load(open('data/pids.json')); \
import os,signal; os.kill(p.pop('svc-gateway-router'),signal.SIGTERM); \
json.dump(p, open('data/pids.json','w'))"
python3 stack.py services-direct          # no --discover; only relaunches gateway-router
```

`stack.py services-direct` runs `mvn compile exec:java` without the spotless skip, so on a
current JDK each service fails with a `palantir-java-format` error. Export
`MAVEN_ARGS=-Dspotless.skip=true` before running it.

```bash
python3 stack.py traffic 3                # ongoing traffic, 3 conversations/min
python3 check.py                          # verify — every Optimize-page command, one line each
```

Spend pages read "Not measured" / 0 exchanges until traffic has run long enough to
complete a conversation (5 idle minutes) and cross into the next whole UTC hour — this is
expected, not a failure.

**If the Optimize page shows a JWT / token-validation error**: the tab's Environment
dropdown (top right, next to Period) is on a real hosted cluster profile instead of
`optimize-local`. Switch it via that dropdown. `profiles.json` should list
`optimize-local` first among any "optimize"-named keys
(`curl -s http://localhost:9889/api/companion/profiles`).

### 2.6 Start the trace ledger (Verify → Traces/Replay backing service)

`samples/trace-ledger` is a separate Akka service — the simulated trace and
human-oversight store behind Verify → Traces, Replay, and the Agents directory. It is
not started by `akka local start` and not covered anywhere else in this runbook; miss
it and Traces/Replay fail with `dial tcp 127.0.0.1:9096: connect: connection refused`.
Its poller reads from the running console, so start it *after* §2.5, console already up:

```bash
cd ~/akka/akka-console-ai-canvas/samples/trace-ledger
mvn -q compile exec:java
```

First run compiles from cold — allow ~60-90s. Confirm it's up:

```bash
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:9096/traces?limit=1   # expect 200
```

Long-running, same pattern as workbench-svc (§2.1) — leave it in its own terminal window
or backgrounded for the session; stop it with `lsof -ti:9096 | xargs kill`.

### 2.7 Deck navigation controls

Deck is driven by keyboard — never the mouse, never a clicker unless tested against this
deck's key bindings.

| Action | Keys |
|---|---|
| Next slide | **PgDn**, **→**, **↓**, or **Space** |
| Previous slide | **PgUp**, **←**, or **↑** |
| Jump to title | scroll to top (⌘↑) |

`shell/nav.js` handles PgDn with smooth scroll to the next registered wrapper — do NOT
resize the window mid-deck; layout shifts break the section rail's active-slide
detection. **Keep this file's `views` list in sync with `builder/slide-registry.json` by
hand any time slides are added, removed, or renamed** — `getElementById` silently drops a
stale id instead of erroring, so the symptom of drift is "arrow keys jump past slides,"
not a build failure.

---

## 3. Slide-by-slide walk

Read talk-tracks from `teleprompter/governance-<presenter>.textream` (cue, land, and sources are in `SPEAKER-NOTES.md`).
This table is just cues + timing. Word budgets are enforced (≤70 words visible per slide) so
the audience has time to look at *you*, not the screen. Slide numbers below are the folder
numbers in `slides/`, which the demo beats in §4 also use.

| # | Slide title | Time | Key cue / action |
|---|---|---|---|
| 00 | Title | 1 min | Operating model, not a product tour. |
| 00a | Customer requirements | 2 min | Summarize the asks in order; promise to point back. Customer copy only. |
| 00b | AI regulations | 1 min | Why now: top penalty tier is for prohibited practices (social scoring example), outside-in tools. |
| 01 | You define your AI risk posture as sets of controls | 2 min | Decide / Define / Enforce rows. |
| 02 | Postures have a lifecycle | 3 min | Trace the categorization grid and the lifecycle boxes. Then go straight into Demo 1 (§4.1) — **name each step as the console does it.** |
| 03 | There are only five types of controls | 3 min | Recap, not a cold definition — "you just watched these." One example per type. No new demo. |
| 04 | Controls are created in three ways | 2 min | Corpus (226 regulations, 1,369 controls), corporate, project. |
| 05 | Groups of controls are placed into signed bundles | 3 min | Control matrix 12 → 34 → 51. Signing is versioning, not human sign-off; roll forward only. |
| 06 | Every control execution produces a verdict | 3 min | Upheld / violated / inconclusive / error, tamper-evident store. Canvas walkthrough live (§4.2). |
| 07 | Controls can execute in pre-production or production | 3 min | Documents, pre-production (full / targeted / records only), production. Engineers learn early. |
| 07b | Compliance is observing the verdicts… | 1 min | By control, regulation, bundle. A violation is not automatic non-compliance. |
| 08 | Drift is a pattern change in the verdict ledger | 2 min | Same control, two times. Verdicts/Replay live if time allows (§4.3). |
| 09 | Controls can be enforced on 3rd party agents | 2 min | Gateway; be precise: "most controls," not all. Human-in-the-loop needs agent changes. |
| 10 | Traces, tokens, and verdicts are recorded together | 2 min | Observe / Scrutinize / Compare. Optimize walkthrough live (§4.4). |
| zz | Thank you | 1 min | Recap in slide order; open the floor. |

**Total**: ~31 min speaking, plus the demo beats in §4 (Canvas and Optimize target ~3 and
~2 min; Demo 1 per §4.1). Fits a 45-min slot with ~10 min for Q&A.

The appendix demo slide is no longer in the build.

---

## 4. Demo runbooks

### 4.1 Demo 1 — the lifecycle, live, entirely in the console: Define Risk → Identify
Controls → Sign → Enforce → Measure *(after Slide 02)*

**Reworked 2026-10-01**: this demo used to run against a standalone `workbench-svc`
browser tab (`127.0.0.1:8730`) for steps 1–3, then tab-switched to the console for a
15-second glimpse of steps 4–5. That standalone tab is gone — the same risk-survey and
control data now live natively inside the console itself (Verify → Risk/Controls/
Verdicts), because `workbench-svc` is a discovered service the console surfaces directly.
**All five steps now run in one tab, as one continuous left-nav walk** — no tab-switch
mid-demo, just clicks down the Verify section. The backing process (§2.1) still has to be
running; it just isn't presented on its own anymore.

**Why this beat exists**: Slide 02 shows the lifecycle abstractly. This demo is
where the audience sees each step happen on a real system, by name, before any later slide
formalizes it — Slide 03 onward recap and define what was just watched, they don't
introduce it cold. Don't skip ahead to "control" vocabulary before this beat runs.

**Precondition**: workbench-svc up (§2.1), console up (§2.5), §2.2 smoke test passed. Tab 2
reachable — leave it wherever §2.3 left it (Canvas, nav collapsed); this beat starts with
an explicit nav-driven landing, not a pre-scrolled frame.

**Beats (target ~6 min)**:

1. **Tab-switch to Tab 2 (console).** Lands on **Canvas**, left-nav sections collapsed —
   the audience has not seen this screen before, so orient them to the chrome itself before
   doing anything with it. Say: "This is the Akka console — the actual governance system
   running this project, not a slide about it." Point down the collapsed left nav without
   opening anything yet: "Three sections: **Specify** is where the specs, docs, and exit
   conditions for this system live; **Verify** is where risk, controls, and every
   enforcement outcome get tracked — that's most of what we'll use; **Optimize** is cost
   and model management, for later." Don't linger on Canvas itself — that walkthrough is
   its own beat later (§4.2); this is purely "here's the map" before stepping into Verify.
2. **Click to open Verify, then click Risk.** Narrate the click itself, since this is the
   first time the audience sees the nav expand: "Verify" — click — "opens into Risk,
   Controls, Evaluations, Red teaming, Traces, Replay, Verdicts, Compliance. We start at the
   top." Click **Risk**. Say: "This is the live risk survey for this system." Point at the
   survey progress indicator — don't reset or restart it, just note it's mid-flight, which
   is the honest state of an in-flight intake. **Answer one unanswered question.** **Name
   the step**: "That's step one — Define Risk. One answer, controls auto-derived, sourced
   by article from the regulatory corpus."
3. **Click Verify → Controls → Corpus.** Point at the summary tiles (controls in corpus,
   regulations, controls for this system). Filter the **Applies** facet under **In this
   project** in the left filter rail. Expand any row's caret. **Name the step**: "Step two
   — Identify Controls. Every one of these carries the exact citation it derives from" —
   read the framework line aloud. "When the corpus rolls, we know exactly which controls to
   re-verify, because the citation is live, not a comment someone wrote once."
4. **Click Verify → Controls → Bundle.** Point at the **Candidates / In the bundle** tab
   split and the accepted/waived/removed counters. **Click Accept on one candidate row.** A
   confirmation toast fires and the counters tick up live. **Name the step**: "Still step
   two — this is an officer deciding what's actually in scope, not everything the corpus
   could apply."
5. **Click Verify → Controls → Sign.** Read (or closely paraphrase) the **"Signing does not
   attest to any of the following"** list on-screen. **Click Sign bundle.** A new row lands
   in the **Signed bundles** table below and the signed-off counters tick up. **Name the
   step**: "Step three — Sign. A content-addressed, versioned record of exactly what was in
   scope, at this revision — not a crypto attestation, and the page just told you that
   itself."
6. **Click Verify → Verdicts, ~15 sec.** Point at the ledger — newest first — and the
   **Conclusion** column showing a mix of **Upheld** rows and at least one **Breached** or
   **Error** row in view. **Name the step**: "Step four — Enforce. Every one of those
   controls now runs on every request this system handles — not sampled, not quarterly.
   We'll come back here in detail with Canvas in a few minutes." Glimpse only — don't
   linger, that payoff belongs to §4.2.
7. **Stay on Verdicts, ~15 sec.** Point at a **Breached** or **Error** row if one is
   visible. **Name the step**: "Step five — Measure. That's drift showing up in the ledger
   itself — we'll go deep on it later." Glimpse only — full payoff is §4.3. **Close the loop
   to Slide 01**: "That ledger — enforced, measured, provable — is the governance posture
   Slide 01 promised. Nothing here was asserted; it was proven."
8. **Tab-switch back to the deck.** Continue to Slide 03 as a recap, not a new topic.

**Fallback (if workbench-svc / the console doesn't respond)**: skip live, describe
verbally, reference a pre-seeded bundle under `demo/governance/signed/` — open in a text
editor if pressed. Because this demo no longer has a separate tab for steps 1–3, a console
outage now takes down the *whole* beat — if the console smoke test (§2.2) fails, do not
attempt any part of Demo 1 live; narrate all five steps verbally against the slide and move
straight to Slide 03.

### 4.2–4.4 Console demo track — one running console, three cues

All three demo beats below use the same running console at `http://127.0.0.1:9889`
(build/start steps: §2.5) — the same tab Demo 1 (§4.1) already ran in — different pages,
different points in the deck.

#### 4.2 Canvas walkthrough *(after Slide 06)*

**Precondition**: Console running, left nav on **Canvas**, starter questions smoke-tested
this session.

**Beats (target ~3 min)**:

1. **Tab-switch to the console, Canvas.** Say: "Instead of a static dashboard, we ask the
   platform directly — it generates the view."
2. **Ask a starter question** (or a pre-tested ad-hoc one) that touches controls or
   evidence.
3. **Confirm a live policy violation is visible** somewhere in the result or a follow-up
   question — this is the key thing to show, not optional flavor.
4. **Tab-switch back to the deck.** Continue to Slide 07.

#### 4.3 Verdicts/Replay walkthrough (drift) *(after Slide 08)*

Query the same control live in **Verify → Verdicts** across two time points, then open
**Verify → Replay** on the session behind an anomalous verdict to show *why* it happened,
not just that it did.

#### 4.4 Optimize walkthrough (cost) *(after Slide 10)*

**Precondition**: `optimize-local` synthetic stack running AND seeded with traffic —
check `cd ~/akka/akka-console-ai-canvas/optimize-local && python3 stack.py status` for
service health, then confirm the Spend page shows non-zero exchanges before the session.

**Beats (target ~2 min)**:

1. **Tab-switch to the console, Optimize → Spend.** Say: "Every token, every model,
   tagged by business construct — department, use case, region."
2. **Ask Canvas a cost question live** — pre-test any variant before relying on it in the
   room.
3. **Tab-switch back to the deck** for the close.

**Fallback (no seeded traffic, or Optimize errors)**: narrate the page structure without a
live number, and land the cost-governance point verbally on Slide 10 using the
Observe/Scrutinize/Compare framing already in the slide copy.

---

## 5. Recovery from common failure modes

### 5.1 Workbench-svc won't start (symptom: Verify → Risk/Controls is empty or errors in the console)

Demo 1 has no separate tab of its own, so a dead `workbench-svc` shows up as the console's
Verify pages failing to load, not as a "Connecting…" banner on a standalone page.

```bash
# 1. Is port 8730 already bound?
lsof -ti:8730

# 2. If yes, whose PID? (probably a stale Java from earlier)
ps -o pid,command -p $(lsof -ti:8730)

# 3. Kill it and retry
lsof -ti:8730 | xargs kill
```

If Maven can't resolve dependencies — verify `~/.m2/settings.xml` still has the akka-repo
token and try `mvn -q -DskipTests dependency:resolve` alone before `exec:java`. After
restarting `workbench-svc`, reload the console tab (⌘R) — it discovers the service on load,
not continuously.

### 5.2 Deck won't build

`python3 builder/build.py --mode overview 2>&1 | tail -20` — if a slide's `meta.json` is
malformed, the traceback names the file.

### 5.3 A slide lands with content clipped

Every slide is designed to fit at 860px usable height. If content still clips in your
projector's resolution, that's a projector aspect ratio mismatch — press **⌘0** to reset
zoom, or **F** to toggle fullscreen off/on. Do NOT edit CSS live.

### 5.4 You lose the deck to a screen sleep / lock

`⌘⇧F` toggles fullscreen back. `⌘R` reloads without losing progress (deck is stateless —
starts at the title slide again; PgDn until you're back).

### 5.5 A demo hangs mid-click

Never wait longer than 5 seconds. Say the punchline verbally and move on. The audience
will forgive a slow tab far less than a silent presenter watching a spinner.

---

## 6. Post-session cleanup

```bash
# 1. Stop the workbench-svc
lsof -ti:8730 | xargs kill 2>/dev/null

# 2. Any test .gcc bundles produced during the demo
cd ~/akka/governance-explainability
git status demo/governance/signed/
# If new bundles are demo artifacts you don't want to commit:
#   git checkout -- demo/governance/signed/       # discards them

# 3. Close Chrome tabs.
```

---

## 7. One-page cheat sheet (print or keep on a phone)

```
ENVIRONMENT      cd ~/akka/presentations/_wip/governance && ./demo-env.sh up --pull   (also: down, status)
DECK             file:///Users/smittyweygant/akka/presentations/_wip/governance/generated/overview/index.html
CONSOLE (ALL)    http://localhost:9889  (land on Canvas, nav collapsed — Dashboard/Verify/Optimize also in left nav)
                 Demo 1 (after Slide 02): Verify > Risk > Controls (Corpus/Bundle/Sign) > Verdicts
                 Canvas / Verdicts-Replay / Optimize walkthroughs come later (§4.2-4.4)
DEMO 1 BACKEND   workbench-svc must be running — not presented directly, console discovers it
                 cd ~/akka/governance-explainability
                 PROJECT_ROOT=./demo REPO_ROOT=. mvn -f services/workbench-svc/pom.xml -q compile exec:java
DEMO 1 BACKEND STOP  lsof -ti:8730 | xargs kill
TRACE LEDGER     cd ~/akka/akka-console-ai-canvas/samples/trace-ledger && mvn -q compile exec:java
                 (start after CONSOLE START — backs Verify > Traces/Replay, port 9096)
TRACE LEDGER STOP  lsof -ti:9096 | xargs kill
CONSOLE START    cd ~/akka/akka-console-ai-canvas && bash scripts/build-akka-with-console.sh \
                 && akka-cli/build/akka local stop; akka-cli/build/akka local start
CONSOLE STOP     cd ~/akka/akka-console-ai-canvas && akka-cli/build/akka local stop
OPTIMIZE STATUS  cd ~/akka/akka-console-ai-canvas/optimize-local && python3 stack.py status
OPTIMIZE RESTART cd ~/akka/akka-console-ai-canvas/optimize-local && python3 stack.py up \
                 && python3 stack.py services-direct && python3 stack.py traffic 3
OPTIMIZE STOP    cd ~/akka/akka-console-ai-canvas/optimize-local && python3 stack.py down \
                 && python3 stack.py services-direct-stop
NEXT SLIDE       PgDn / → / Space
PREV SLIDE       PgUp / ←
FULLSCREEN       F  (⌘⇧F to toggle)
BUILD DECK       cd ~/akka/presentations/_wip/governance && python3 builder/build.py --mode overview
```

---

*Reconstituted 2026-10-01 as the generic companion to `README.md`, split out of the
customer-specific runbook so every customer deck has a presenter runbook to start from.
Demo 1 reworked 2026-10-01 to run entirely inside the console (no more standalone
`127.0.0.1:8730` tab) — see §4.1; backported from the CIBC Mellon customer runbook, where
this was originally caught and fixed, per this repo's rule that generic mechanics belong
here first. Living doc.*
