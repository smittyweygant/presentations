# Governance demos

Everything needed to run the four console demos. The words are in `../SPEAKER-NOTES.md`
(beat IDs D1.1 to D4.2) and on the prompter. These files hold the clicks, the checks, and the
resets. Environment setup and recovery are in `../PRESENTER-RUNBOOK.md`.

| File | Demo | Follows slide | Beats |
|---|---|---|---|
| `01-lifecycle.md` | Define Risk, Identify Controls, Sign, Enforce, Measure | 02 | D1.1 to D1.8 |
| `02-canvas.md` | Canvas: which controls apply, which were violated | 06 | D2.1 to D2.3 |
| `03-drift-replay.md` | One control over time, then Replay | 08 | D3.1 to D3.3 |
| `04-optimize.md` | Optimize Spend, then a cost question in Canvas | 10 | D4.1 to D4.2 |

All four run in one console tab (`http://localhost:9889`), tab 2 of the desktop layout. Each
demo starts and ends on **Canvas with the left nav collapsed**, so the next one begins from a
known frame.

## Run of show

Times are estimates carried over from the earlier runbook. Replace them with timings from a
recorded run. Prompter totals: about 1,890 spoken words on slides and 670 in demos
(`teleprompter/governance-smitty.md` footer), roughly 12 and 4 minutes at 150 words a minute,
before clicking and pauses.

| Slide | Title | Min | Cue |
|---|---|---|---|
| 00 | Title | 1 | Operating model, not a product tour. |
| 00a | Customer requirements | 2 | Summarize the asks in order. Customer copy only. |
| 00b | AI regulations | 1 | Why now: top penalty tier is for prohibited practices; outside-in tools. |
| 01 | You define your AI risk posture as sets of controls | 2 | Decide, Define, Enforce rows. |
| 02 | Postures have a lifecycle | 3 | Trace the grid and the lifecycle boxes. **Demo 1.** |
| 03 | There are only five types of controls | 3 | Recap, not a cold definition. One example per type. |
| 04 | Controls are created in three ways | 2 | Corpus, corporate, project. |
| 05 | Groups of controls are placed into signed bundles | 3 | Signing is versioning, not human sign-off. Roll forward only. |
| 06 | Every control execution produces a verdict | 3 | Verdicts in a tamper-evident store. **Demo 2.** |
| 07 | Controls can execute in pre-production or production | 3 | Documents, pre-production, production. |
| 07b | Compliance is observing the verdicts… | 1 | By control, regulation, bundle. |
| 08 | Drift is a pattern change in the verdict ledger | 2 | Same control, two times. **Demo 3**, skipped if short. |
| 09 | Controls can be enforced on third-party agents | 2 | Gateway. Say "most controls," not all. |
| 10 | Traces, tokens, and verdicts are recorded together | 2 | Observe, Scrutinize, Compare. **Demo 4.** |
| zz | Thank you | 1 | Recap in slide order; open the floor. |

## Live data to know about

The Verify pages read the `loan-origination` sample project in
`~/akka/akka-console-ai-canvas/samples/loan-origination/`, not the project served by
workbench-svc on `:8730`. Accept and Sign write there, and so does loading a Verify page: the
revision counters on Risk and Controls move on every load.

- The verdict ledger holds about 2,000 verdicts, dated 2 June to 30 September. Nothing is
  recent, so never ask Canvas for "this week" or "today."
- Every verdict is simulated except seven imported from real eval and red-team runs. The
  runtime can't record verdicts yet, and the console marks each verdict's source. D1.6 says
  so aloud.
- The console labels violations **Breached**. The script says "violation."
- Control counts differ from Slide 05's 12, 34, 51. Don't read counts aloud in Demo 1. The
  corpus figures (226 regulations, 1,369 controls) match Slide 04.
- Compliance reports the project as not compliant. Demo 1 uses that as the honest position.

## Before each take

```bash
../demo-env.sh status      # everything answering
../demo-env.sh reset       # demo project back to the saved baseline
```

`reset` restores the baseline saved with `../demo-env.sh snapshot`. Take the snapshot once,
when the demo project is in the state you want to start every take from.
