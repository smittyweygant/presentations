#!/usr/bin/env bash
# Starts, stops and checks the governance demo environment described in
# PRESENTER-RUNBOOK.md §2.1, §2.5 and §2.6.
#
#   ./demo-env.sh up [--pull]   stop everything, optionally fast-forward the repos, rebuild, start
#   ./demo-env.sh down          stop everything
#   ./demo-env.sh status        report what is answering
#   ./demo-env.sh snapshot      save the demo project's governance files as the baseline
#   ./demo-env.sh reset         restore the baseline, undoing Accept, Sign and survey answers
#
# Start order matters: workbench-svc before the console daemon (the console
# discovers it on start), the trace ledger after the daemon (it polls the daemon).
# The daemon keeps registered services in memory with no unregister, so `up`
# always stops and restarts it to drop services left over from other work.

set -uo pipefail

GOV="${GOV_REPO:-$HOME/akka/governance-explainability}"
CANVAS="${CANVAS_REPO:-$HOME/akka/akka-console-ai-canvas}"
AKKA="$CANVAS/akka-cli/build/akka"
OPT="$CANVAS/optimize-local"
LOGS="${DEMO_LOG_DIR:-/tmp/governance-demo-logs}"
# The Verify pages read and write this sample project: controls.yaml, survey.yaml and signed/.
PROJECT_GOV="$CANVAS/samples/loan-origination/governance"
BASELINE="${DEMO_BASELINE_DIR:-$HOME/.akka/demo-baseline/loan-origination-governance}"

# build-akka-with-console.sh calls bare `python`, which pyenv cannot resolve without a version.
export PYENV_VERSION="${PYENV_VERSION:-3.12.8}"
# `mvn compile exec:java` runs spotless, whose formatter fails on current JDKs.
export MAVEN_ARGS="${MAVEN_ARGS:--Dspotless.skip=true}"

mkdir -p "$LOGS"

say() { printf '\n== %s\n' "$*"; }

wait_http() { # url, tries, sleep-seconds, optional grep pattern
  local url=$1 tries=$2 pause=$3 pat=${4:-}
  for _ in $(seq 1 "$tries"); do
    if [ -n "$pat" ]; then
      curl -s -m 3 "$url" | grep -q "$pat" && return 0
    else
      [ "$(curl -s -o /dev/null -w '%{http_code}' -m 3 "$url")" = 200 ] && return 0
    fi
    sleep "$pause"
  done
  return 1
}

pull_repo() {
  local dir=$1
  say "pull $(basename "$dir")"
  git -C "$dir" fetch --quiet || { echo "fetch failed"; return 1; }
  if git -C "$dir" rev-parse '@{u}' >/dev/null 2>&1; then
    git -C "$dir" merge --ff-only '@{u}' | tail -1
  else
    echo "branch $(git -C "$dir" rev-parse --abbrev-ref HEAD) has no upstream, left as is"
  fi
}

down() {
  say "stop"
  pkill -f 'stack.py traffic' 2>/dev/null
  lsof -ti:8730 | xargs kill 2>/dev/null
  lsof -ti:9096 | xargs kill 2>/dev/null
  (cd "$OPT" && python3 stack.py services-direct-stop 2>&1 | tail -1)
  [ -x "$AKKA" ] && timeout 30 "$AKKA" local stop 2>&1 | tail -1
  sleep 3
}

up() {
  if [ "${1:-}" = "--pull" ]; then
    pull_repo "$GOV"
    pull_repo "$CANVAS"
  fi

  down

  say "build console and CLI"
  (cd "$CANVAS" && bash scripts/build-akka-with-console.sh > "$LOGS/console-build.log" 2>&1) \
    || { echo "build failed, see $LOGS/console-build.log"; exit 1; }

  say "workbench-svc :8730"
  (cd "$GOV" && PROJECT_ROOT=./demo REPO_ROOT=. nohup mvn -f services/workbench-svc/pom.xml -q compile exec:java \
    > "$LOGS/workbench.log" 2>&1 &)
  wait_http http://127.0.0.1:8730/api/overview 30 5 matrix_id \
    || { echo "workbench-svc not answering, see $LOGS/workbench.log"; exit 1; }

  say "console daemon :9889"
  (cd "$CANVAS" && nohup "$AKKA" local start > "$LOGS/daemon.log" 2>&1 &)
  wait_http http://localhost:9889/ 30 3 || { echo "console not answering, see $LOGS/daemon.log"; exit 1; }

  say "trace ledger :9096"
  (cd "$CANVAS/samples/trace-ledger" && nohup mvn -q compile exec:java > "$LOGS/trace-ledger.log" 2>&1 &)
  wait_http "http://127.0.0.1:9096/traces?limit=1" 36 5 \
    || { echo "trace ledger not answering, see $LOGS/trace-ledger.log"; exit 1; }

  say "optimize-local services (about 2 minutes cold)"
  (cd "$OPT" && python3 stack.py up > "$LOGS/optimize-stack.log" 2>&1)
  (cd "$OPT" && python3 stack.py services-direct 2>&1 | tee "$LOGS/optimize-services.log")
  (cd "$OPT" && nohup python3 stack.py traffic 3 > "$LOGS/optimize-traffic.log" 2>&1 &)

  status
}

status() {
  say "status"
  local rc=0
  chk() { # label, url, optional pattern
    if wait_http "$2" 1 0 "${3:-}"; then printf 'up    %s\n' "$1"; else printf 'DOWN  %s\n' "$1"; rc=1; fi
  }
  chk "console           :9889" http://localhost:9889/
  chk "workbench-svc     :8730" http://127.0.0.1:8730/api/overview matrix_id
  chk "trace ledger      :9096" "http://127.0.0.1:9096/traces?limit=1"
  (cd "$OPT" && python3 stack.py status 2>&1 | grep -E 'gateway-router|capture-refinery|portfolio|optimize  |trainer|registry')
  echo
  echo "Services registered with the console daemon:"
  timeout 15 "$AKKA" local status 2>&1 | sed -n '/Services/,$p'
  return $rc
}

snapshot() {
  mkdir -p "$BASELINE"
  rsync -a --delete "$PROJECT_GOV/" "$BASELINE/" && echo "baseline saved to $BASELINE"
}

reset() {
  [ -d "$BASELINE" ] || { echo "no baseline at $BASELINE; run '$0 snapshot' first"; exit 1; }
  echo "changes made to restore the baseline:"
  rsync -a --delete --itemize-changes "$BASELINE/" "$PROJECT_GOV/" | grep -v '^\.d' || true
  echo "done. Reload the console tab."
}

case "${1:-}" in
  up)     shift; up "$@" ;;
  down)   down ;;
  status) status ;;
  snapshot) snapshot ;;
  reset)  reset ;;
  *)      sed -n '2,9p' "$0"; exit 2 ;;
esac
