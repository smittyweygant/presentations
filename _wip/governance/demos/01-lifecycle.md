# Demo 1: the lifecycle in the console

Define Risk, Identify Controls, Sign, Enforce, Measure. Follows Slide 02. About 6 minutes.
Speech: `SPEAKER-NOTES.md`, Slide 02, beats D1.1 to D1.8.

## Why it runs first

The audience sees each step happen by name before Slide 03 onward defines it. Slides 03 to 05
recap what was just watched. Don't use control vocabulary ahead of this demo.

## Start state

Console tab on **Canvas**, left nav collapsed to its top-level names. Don't pre-open Verify;
opening it on camera is beat D1.2.

## Smoke test (2 minutes, before dial-in)

Read-only, except where noted. Loading Verify pages bumps revision counters; that is expected.

1. **Verify → Risk** loads with a risk survey and at least one answered question.
2. **Verify → Controls → Corpus**: the tiles show 226 regulations and 1369 controls. Filter
   **In this project → Applies**, expand a row. A citation panel opens.
3. **Verify → Controls → Bundle**: the **Candidates** and **In the bundle** tabs render with
   Accept, Waive, and Remove buttons. Do **not** click Accept. Accept and Sign are persistent
   writes; save them for the take.
4. **Verify → Controls → Sign**: the collapsed **What signing does and does not attest**
   section opens and lists what signing does not show. The **Signed bundles** table has rows
   with a version in force.
5. **Verify → Activity → Verdicts** lists verdicts, newest first, with a mix of Upheld,
   Breached, and Error conclusions.
6. **Verify → Compliance** loads with a summary line and a week-by-week view.

Any failure: do not present the demo live. Use the fallback below.

## Click sheet

| Beat | Where | Do | Expect |
|---|---|---|---|
| D1.1 | Console tab, Canvas | Switch to the tab. Point down the collapsed nav: Specify, Verify, Optimize | Nav shows top-level names only |
| D1.2 | Verify → Risk | Click Verify, then Risk. Answer one unanswered question. Don't reset the survey | Question count moves; survey stays partway through |
| D1.3 | Verify → Controls → Corpus | Filter **In this project → Applies**. Expand one row. Read its framework line | Citation panel opens; tiles read 226 and 1369 |
| D1.4 | Verify → Controls → Bundle | Point at **Candidates** and **In the bundle**. Click **Accept** on one candidate | Accepted counter ticks up |
| D1.5 | Verify → Controls → Sign | Optionally open **What signing does and does not attest**. Click **Sign as v…** | New row in **Signed bundles**; version in force advances |
| D1.6 | Verify → Activity → Verdicts | Leave filters alone. Point at one **Breached** row and one **Error** row | Newest first; mixed conclusions visible |
| D1.7 | Verify → Compliance | Point at the summary line and the week-by-week view | Summary names failing, unresolved, stale, and no-evidence counts |
| D1.8 | Deck tab | Switch back. Continue to Slide 03 | |

## End state

Leave the deck tab in front. Before Demo 2, in the console tab click **Canvas** and collapse
**Verify**, so the nav shows top-level names only.

## Fallback

If the smoke test fails or the console stops responding mid-take, don't attempt any part live.
Read the Fallback paragraph under Slide 02 in `SPEAKER-NOTES.md` and go to Slide 03.

## Reset

Accept and Sign write to `samples/loan-origination/governance/` in the
`akka-console-ai-canvas` checkout: edits to `controls.yaml` and `survey.yaml`, and a new file
under `signed/`. Run `../demo-env.sh reset` between takes.

## Confirm in the room before relying on it

- The Specify description in D1.1 ("specs, docs, and exit conditions"): open Specify once
  and check the labels.
- The seven survey sections named in D1.2 (Purpose, Data, Decisions, Failure, Oversight,
  Operations, Compliance) are what the Risk page shows for the full survey.
- The Sign button's label includes the next version number (for example "Sign as v7").
