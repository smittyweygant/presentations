# Demo 3: drift in the ledger, then Replay

One control over time, then the session behind a verdict. Follows Slide 08. About 2 minutes.
Skip it when the session is running long. Speech: `SPEAKER-NOTES.md`, Slide 08, beats D3.1 to
D3.3.

## Start state

Console tab open on Canvas, nav collapsed.

## Before the take

The Replay and By control views need the trace ledger on `:9096` and the Optimize services
running. Run `../demo-env.sh status`. Then check the example once:

1. **Verify → Activity → Verdicts → By control** lists every control with its latest
   conclusion per environment, a **Trend** strip, and verdict counts. The certificate validity
   row shows Production **Breached**, 46 verdicts (42 upheld, 3 breached, 1 inconclusive), and
   a trend that is green until it turns red at the end. Clicking a row goes to
   **Controls → Bundle**, not to verdicts, so don't click it.
2. **All verdicts** → **All controls** filter → "Certificate validity is set per product…".
   The list shows 46 matching, newest first: Sep 29 and Sep 28 breached, Sep 27 back to Sep 20
   upheld, one inconclusive on Sep 25. Times are in the browser's local zone. Expand the
   newest row: "The certificate has 88 days of validity left, inside the 90-day renewal band,"
   with a days-remaining bar and a **simulated** badge.
3. Simulated verdicts can't be opened in Replay from the verdict. Open **Verify → Activity →
   Replay → Traces** and pick a trace that steps through cleanly. Write down which one.

## Click sheet

| Beat | Where | Do | Expect |
|---|---|---|---|
| D3.1 | Verify → Activity → Verdicts → By control, then All verdicts | Point at the certificate validity trend. Open **All verdicts**, set **All controls** to certificate validity | Trend ends red; list shows upheld for weeks, then two breached |
| D3.2 | All verdicts, filtered | Expand the newest row (click its caret) | "88 days of validity left, inside the 90-day renewal band"; days-remaining bar |
| D3.3 | Verify → Activity → Replay → Traces | Open a trace | A recorded history plays back |
| | Deck tab | Switch back. Continue to Slide 09 | |

The slide's own examples (a PII error "today," a storage limitation gate inconclusive) are
illustrative and not in the ledger. D3.1 says so. The ledger ends 30 September, so say "over
time," never "today."

## End state

Click **Canvas** in the left nav and collapse **Activity** and **Verify**.

## Fallback

Skip the demo. Read the Fallback line under Slide 08 in `SPEAKER-NOTES.md` and go to Slide 09.

## Reset

Nothing to reset. These pages only read.
