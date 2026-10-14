# Demo 4: Optimize

Spend, then a cost question in Canvas. Follows Slide 10. About 2 minutes.
Speech: `SPEAKER-NOTES.md`, Slide 10, beats D4.1 to D4.2.

## Preconditions

The `optimize-local` stack is up and has run traffic long enough to show spend. Check:

```bash
cd ~/akka/akka-console-ai-canvas/optimize-local && python3 stack.py status
```

Then open **Optimize → Spend**, set the Period to 7 or 30 days, and confirm it shows a non-zero
spend and exchange count. Those periods come from `python3 seed.py history`, so they are full
without waiting. Today's traffic shows only after it completes a conversation (five idle
minutes) and crosses into the next whole UTC hour. A period that overlaps live days may read
"incomplete"; the figures still show.

`python3 check.py` in the same folder reports one failure at the time of writing:
`models attestations list frontier-large` returns 404. The CLI calls a route the optimize service
lacks. It does not affect Spend, the only Optimize page this demo opens.

This console build has four Optimize views: Spend, Routing, Models and Training. Spend carries
five tabs: Breakdown, Tokens, Compare, Savings and Prices. The Efficiency, Use cases, Changes and
Budgets views are not in it, so the demo does not open them.

Spend's other tabs hold data but are not part of the click sheet (Breakdown is the page that carries the dollar figures):

- **Compare** reads "decrease of 54.5%". The current week holds only the days since traffic
  restarted, so the drop is an artifact of the data. Don't open it unprompted.
- **Savings** shows provider caching ($0.36 over the week) but no routing savings, because live
  traffic carries no use case.
- **Prices** shows catalog version 3 in force, the two earlier versions and the rate changes.
  It is safe to open if asked about prices.

## Click sheet

| Beat | Where | Do | Expect |
|---|---|---|---|
| D4.1 | Optimize → Spend → Tokens | Click **Optimize**, **Spend**, then the **Tokens** tab | Tokens by class, by model, and by use case (point at Tokens by use case). Some use cases show as short hex ids and one as "No use case". "Incomplete" badges show on some figures |
| D4.2 | Canvas | Click **Canvas**. Click "Which models are we paying for?". Wait for the answer | About 20 seconds. Eight registered models, a Spend by model chart for the last 7 days, and a price table |
| | Deck tab | Switch back. Continue to the thank-you slide | |

The "Incomplete" badge and the Missing traffic panel (unreadable capture files, hours with no
report) come from days the stack ran before the capture paths were fixed. They clear as those days
leave the period. Say the figures are preliminary if asked. Canvas may show a stale red
"claude exited" line from an earlier question until the next one runs.

If the **Environment** dropdown (top right) shows a hosted cluster profile and Optimize errors
with a token message, switch it to `optimize-local`.

## End state

Console tab left on Canvas. Deck tab in front for the close.

## Fallback

If Spend shows no usage or Optimize errors, don't narrate an empty page. Switch to the deck and
read the Fallback line under Slide 10 in `SPEAKER-NOTES.md`.

## Reset

Nothing to reset. Spend only reads.
