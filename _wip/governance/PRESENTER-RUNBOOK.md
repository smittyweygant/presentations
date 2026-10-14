# AI Governance Demo — Presenter Runbook

*The demo environment and the deck build: what to run, what to open, and how to recover.
Companion to `README.md` (spec), `SPEAKER-NOTES.md` (talk-track), `teleprompter/` (the script
text alone, generated from the notes; load `governance-smitty.textream` in Textream), and
`demos/` (click sheets, checks, and resets for each demo).*

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

While editing slides, run `node dev-server.mjs` instead. It serves the deck at
`http://127.0.0.1:8765/index.html`, rebuilds when anything under `slides/`, `shell/`,
`builder/` or `presenters/` changes, and reloads open pages. Options: `--port`,
`--presenter` (default `smitty`), `--mode`. It refuses to start if the port is taken.

---

## 1. Desktop layout — what to have open when the session starts

Arrange these BEFORE joining the call. Use ⌘⇥ / Mission Control to move between:

| # | Window | State | Position |
|---|---|---|---|
| **1** | **Chrome — deck tab** at `file:///.../_wip/governance/generated/overview/index.html` | Fullscreen (F key) | Primary display |
| **2** | **Chrome — Console tab** at `http://localhost:9889`, on **Canvas with the left nav collapsed**. This one tab carries all four demos (`demos/`). | Regular tab | Same window as (1) |
| **3** | **Terminal — service logs** (workbench-svc on `:8730`, the trace ledger on `:9096`), or `/tmp/governance-demo-logs/` when started with `demo-env.sh`. | 40-col wide, visible | Second display (or hidden until needed) |
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

### 2.1 Start workbench-svc

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
live** — see §4.1 recovery. Nothing is ever presented at `127.0.0.1:8730` directly. Start it
*before* §2.5 so the console daemon discovers it and lists it under Services. The Verify pages
read the `loan-origination` sample project instead (see `demos/README.md`).

### 2.2 Smoke-test the demos

Each demo has its own smoke test in `demos/`. Run `demos/01-lifecycle.md` (2 min) before
dial-in; it covers the Verify pages every demo uses. Any FAIL means escalate before dial-in.
**Every Accept and Sign click is a persistent write**, so smoke tests never click them.

### 2.3 Stage the console tab

Chrome tab 2 starts every demo on **Canvas with the left nav collapsed**. Each demo file in
`demos/` names its end state, which is the next demo's start state.

### 2.4 Load the deck fullscreen

Open **Chrome tab 1** at
`file:///Users/smittyweygant/akka/presentations/_wip/governance/generated/overview/index.html`.
Press **F** (or ⌃⌘F) for fullscreen. Verify the title slide lands cleanly with your
name/title.

### 2.5 Start the local console (Specify / Verify / Optimize / Canvas)

The console lives in `~/akka/akka-console-ai-canvas` (Tyler's repo) and drives a complete
local Akka console — Specify, Verify (Controls/Risk/Traces/Replay/Verdicts), Optimize (Spend with Breakdown, Tokens, Compare, Savings and Prices tabs; Routing; Models; Training), and
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

Open **`http://localhost:9889`**. Left nav: Dashboard / **Canvas** / Services / Agents / Specify / Verify (Risk, Controls,
Evaluations, Human, Activity with Traces, Conversations, Verdicts and Replay, Compliance) /
Optimize. Canvas ships starter questions — good for a first smoke test.

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
python3 seed.py history                   # 35 days of past usage, so 7- and 30-day Spend fills at once
```

`history` needs nexus on branch `local/trace-hooks-new` (the import route is not on
`local/trace-hooks`) and a portfolio store whose `catalog-v1` is dated 36 days back. If it stops
and says the price catalog starts too late, stop portfolio, delete `data/db/portfolio-db.mv.db`,
restart it, and run `python3 seed.py catalog-v1` before `history`.

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
complete a conversation (5 idle minutes) and cross into the next whole UTC hour. Live traffic is
expected to wait; the `history` step above fills the 7- and 30-day periods straight away, so set
the Period to 7 or 30 days for the demo. A period that overlaps days the stack ran live reads
"incomplete" and shows its figures anyway.

If Spend stays empty after the hour, check `logs/capture-refinery.log` for
`is not in bucket gateway-router-capture; recording the hole`. That means gateway-router and
capture-refinery are writing to different folders. Both take the folder from
`OPTIMIZE_LOCAL_DATA`, which `stack.py` sets; a conf file with a hard-coded path breaks it.

**If the Optimize page shows a JWT / token-validation error**: the tab's Environment
dropdown (top right, next to Period) is on a real hosted cluster profile instead of
`optimize-local`. Switch it via that dropdown. `profiles.json` should list
`optimize-local` first among any "optimize"-named keys
(`curl -s http://localhost:9889/api/companion/profiles`).

### 2.6 Start the trace ledger (Verify → Activity backing service)

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

## 3. Demos and run of show

The slide-by-slide run of show, timings, click sheets, and per-demo fallbacks are in
`demos/README.md`. The words are in `SPEAKER-NOTES.md` and on the prompter.

---

## 4. Recovery from common failure modes

### 4.1 Workbench-svc won't start (symptom: `workbench-svc` missing or Unavailable under Services)

Workbench-svc has no tab of its own. A dead one shows as a missing or Unavailable entry under
Services in the console, and `curl http://127.0.0.1:8730/api/overview` fails.

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
restarting `workbench-svc`, reload the console tab (⌘R). A service another project left
registered stays listed as Unavailable until the daemon restarts (`demo-env.sh up`).

### 4.2 Deck won't build

`python3 builder/build.py --mode overview 2>&1 | tail -20` — if a slide's `meta.json` is
malformed, the traceback names the file.

### 4.3 A slide lands with content clipped

Every slide is designed to fit at 860px usable height. If content still clips in your
projector's resolution, that's a projector aspect ratio mismatch — press **⌘0** to reset
zoom, or **F** to toggle fullscreen off/on. Do NOT edit CSS live.

### 4.4 You lose the deck to a screen sleep / lock

`⌘⇧F` toggles fullscreen back. `⌘R` reloads without losing progress (deck is stateless —
starts at the title slide again; PgDn until you're back).

### 4.5 A demo hangs mid-click

Never wait longer than 5 seconds. Say the punchline verbally and move on. The audience
will forgive a slow tab far less than a silent presenter watching a spinner.

---

## 5. Post-session cleanup

```bash
# 1. Stop the environment
./demo-env.sh down

# 2. Accept and Sign wrote to the demo project: controls.yaml, survey.yaml, and a new file
#    under signed/. Restore the saved baseline, or review the changes first.
cd ~/akka/akka-console-ai-canvas
git status samples/loan-origination/governance/
cd ~/akka/presentations/_wip/governance && ./demo-env.sh reset

# 3. Close Chrome tabs.
```

---

## 6. One-page cheat sheet (print or keep on a phone)

```
ENVIRONMENT      cd ~/akka/presentations/_wip/governance && ./demo-env.sh up --pull   (also: down, status)
DECK             file:///Users/smittyweygant/akka/presentations/_wip/governance/generated/overview/index.html
CONSOLE (ALL)    http://localhost:9889  (land on Canvas, nav collapsed). Click sheets: demos/
DEMO PROJECT     ./demo-env.sh snapshot (save baseline)   ./demo-env.sh reset (restore it)
DEMO 1 BACKEND   workbench-svc must be running — not presented directly, console discovers it
                 cd ~/akka/governance-explainability
                 PROJECT_ROOT=./demo REPO_ROOT=. mvn -f services/workbench-svc/pom.xml -q compile exec:java
DEMO 1 BACKEND STOP  lsof -ti:8730 | xargs kill
TRACE LEDGER     cd ~/akka/akka-console-ai-canvas/samples/trace-ledger && mvn -q compile exec:java
                 (start after CONSOLE START — backs Verify > Activity: Traces, Replay; port 9096)
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
DEV SERVER       cd ~/akka/presentations/_wip/governance && node dev-server.mjs   (live reload, :8765)
```

---

*Reconstituted 2026-10-01 as the generic companion to `README.md`, split out of the
customer-specific runbook so every customer deck has a presenter runbook to start from.
Demos moved to `demos/` 2026-10-14; this file now covers the environment and the deck build.
Living doc.*
