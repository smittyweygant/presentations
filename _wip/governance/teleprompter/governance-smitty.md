# governance — Teleprompter (smitty)
Generated from `SPEAKER-NOTES.md` by `tools/teleprompter/build.py`. Edit the notes, not this file.

---

## Slide 00 — Title

Hello, everyone. I'm Smitty, Field CTO at Akka.

Today I'm going to walk you through how Akka approaches AI governance. This is an operating model, not a product tour. We'll break the governance problem into its elements, build it back up one principle at a time, and then show you what it looks like running.

---

## Slide 00b — AI regulations

Why this matters now. Regulations are multiplying, and the penalties are large. Under the EU AI Act, a prohibited practice carries a fine of up to thirty-five million euros or seven percent of global annual turnover, whichever is higher.

Take social scoring, which the Act prohibits. Imagine a lender whose AI lowers a customer's credit limit because of what that customer posts on social media. That's a risk score built from social behavior, used against the customer to assess their credit risk. That practice warrants the top penalty tier.

The Act also requires providers of high-risk systems to keep technical documentation for ten years.

At the same time, most governance tools monitor AI systems from the outside. They report after something has happened. They can't enforce at the point where an agent calls a model or a tool.

So the questions are where enforcement lives, and how you prove it worked. The rest of this session answers both.

---

## Slide 01 — You define your AI risk posture as sets of controls

The first principle. You define your AI risk posture as a set of controls.

Every business already has a risk posture. It has regulatory duties, and it has corporate policy. Akka doesn't supply those. You decide them.

What Akka does is turn those decisions into controls. A control is a discrete, enforceable check. You define controls independently of any one AI system, so governance and the agentic system are defined separately and managed separately.

Once you have a set of controls, Akka enforces them consistently. The result is a posture you can measure.

---

## Slide 02 — Postures have a lifecycle

The second principle. A posture has a lifecycle, and Akka manages it like software. It has versions, it has releases, and it has history.

It starts with a risk profile, which we capture in a risk survey. The survey asks four kinds of questions.

Intent: what is this system for, and who is accountable. Autonomy: what can it decide on its own, and when must a human step in. Boundaries: who can it affect, and what data and dependencies shape it. And Evidence: which regulations govern it, what evidence it must produce, and who attests to it.

Your answers map to controls. Those controls are collected into a control matrix. The matrix is enforced on test systems and production systems. Then you measure how the posture is performing, and the verdicts and drift you find feed the next cycle.

That's a loop, not a checklist. Rather than keep describing it, let me show it to you.

---

[>>> DEMO 1 — Identify Risk <<<]

[D1.1 · Console tab]

This is the Akka Console. It provides a unified view of your agentic system, including the governance for this project.

The left nav has three sections. Specify is where a system's specs, docs, and exit conditions live. Verify is where risk, controls, and every enforcement outcome are tracked, and that's most of what we'll use. Optimize is cost and models, and we'll get to it later.

---

[D1.2 · Verify > Risk]

Verify opens into Risk, Controls, Evaluations, Human, Activity, and Compliance. We start at Risk.

This is the live risk survey for this system. It's partway through, which is the honest state of an intake in flight. The console groups the questions into seven sections. They're aligned to the four areas from the slide, in finer detail.

[Answer one question]

I'll change one of the jurisdictions. [REMOVE UK]

That's step one, Define Risk. One answer, and controls are derived from it, each tied to an article in the regulatory corpus.

---

[D1.3 · Controls > Corpus. Filter Applies. Expand a row]

Step two, Identify Controls. This is the corpus: two hundred twenty-six regulations and thirteen hundred sixty-nine controls. [Click Applies filter] The filter shows the ones that apply to this system, based on the answer I just gave.

Every control carries the exact citation it comes from.

Let's look at one from the EU

[Open first EU control, read the citation]

The corpus is versioned and published my Akka, so when it is updated, we know exactly which controls to re-verify, because the citation is live data.

---

[D1.4 · Bundle tab. Accept one]

The console calls the set of controls in force a bundle. Technically we refer to it as the control matrix. It's the same thing.

Candidates is everything that could apply. In the bundle is what a decision maker agreed is in scope. I'll accept one.

That's Identify Controls: You determine what's in scope based on the business' ability to apply the controls.

---

[D1.5 · Sign tab]

Step three, Sign. Signing records which controls were accepted or waived, the survey they came from, and the corpus version. The result is a new version: a permanent record of exactly which controls were in scope.

[Click Sign]

There's the new version. One caveat, which the page states itself. Signing records scope. It doesn't test the controls, and it isn't an approval by a regulator or an auditor.

---

[D1.6 · Activity > Verdicts]

[Verdicts] Step four, Enforce. Every control in the bundle that applies at runtime is enforced on the requests it covers, and each execution lands here as a verdict, newest first.

Most are upheld, and a few are violations.

[Filter on Errors]

We see an error - PII Redaction at model boundary. This error threw at the time of the call, and the PII data was protected from being sent to an LLM. The details show this was in production and the notice writer agent was blocked.

We'll come back to this ledger in detail later.

---

[D1.7 · Compliance]

Step five, Measure. Compliance reads those same verdicts and asks whether the controls in force are satisfied, now and over time.

This project isn't fully compliant today, and the page says exactly which controls and why. That's the honest position, and it's what a measured posture looks like.

The ledger concretely describes our governance posture and state of compliance over time. We can describe how it is Enforced, measured, and provable.

[D1.8 · Deck tab]

---

## Slide 03 — There are only five types of controls

The third principle is that there are five types of controls.

You just watched a control get defined, signed, and enforced.

A control is a discrete, provable check. It holds or it doesn't, and evidence supporting each event and verdict can be produced.

Every obligation you have reduces to one of these types:

A guardrail blocks or allows a call at a runtime boundary: before or after a model, a tool, an agent, or a memory call. For example, stopping a wire transfer that lacks dual sign-off.

An evaluation measures and scores behavior that isn't deterministic. It runs against live agents or in test. For example, scoring responses weekly for parity drift.

A human control covers the human-in-the-loop moments: approvals, halts, feedback and drift review. For example, a loan officer approves an adverse-action notice before it goes out.

A gate is a release activity. It runs against documents or in pre-production to confirm a system is ready. For example, blocking a deploy that lacks a current bias-audit attestation.

And a sanitizer redacts, masks, or strips data before it moves on. For example, removing an applicant's Social Security number before the model sees it.

---

## Slide 04 — Controls are created in three ways

The fourth principle. Controls are created in three ways.

First, Akka ships a corpus of two hundred twenty-six AI regulations, mapped to thirteen hundred sixty-nine controls. It covers the EU AI Act, SOC 2, GDPR, and the NIST AI Risk Management Framework, among others. Your risk survey answers select the controls that apply, and you can browse the corpus directly.

Second, corporate policy. These are rules your enterprise has already written down, for example, no agent approves a refund over five hundred dollars without review. Corporate controls are inherited by every project, and you decide whether each one is required or optional.

Third, a project can write its own, for a risk unique to that system, for example, this underwriting agent may never see an applicant's Social Security number.

Once a control is accepted in the bundle, it is uniformly enforced.

---

## Slide 05 — Groups of controls are placed into signed bundles

The fifth principle. Groups of controls are placed into a signed bundle. We call that bundle the control matrix.

For each corporate or custom control, you explicitly accept it, waive it, or remove it. When the mapping is clean, you sign. Signing records which controls were accepted or waived, the survey they came from, and the corpus version. That creates a version: a permanent record of exactly which controls make up that scope of checks.

In this simple example, the loan origination assistant launches with the ability to answer borrower questions. The risk is disclosure accuracy, and version one carries twelve controls. It gains judgment and starts recommending approve or deny. Fair lending becomes a real risk, and version two carries thirty-four controls. Then it gains authority to initiate the wire transfer. Dual control becomes a risk, and version three carries fifty-one.

Every version is kept, and you can compare any two to see how your posture changed. A change creates a new version.

Signing records what is in scope. It doesn't test the controls, and it isn't an approval by a regulator or an auditor.

When you deploy the bundle, the Akka runtime finds every place a control has to run and applies it. Your developers don't write extra code for it.

---

## Slide 06 — Every control execution produces a verdict

The sixth principle. Every time a control executes, it produces a verdict. The control was upheld, it was violated, the result was inconclusive, or it errored.

Verdicts are written to an immutable store. It's the same store that holds the traces of the AI system itself: the conversations, the model calls, the tool calls. So controls and behavior sit side by side, and nothing is self-reported.

Let me ask the console what is true of this system.

---

[>>> DEMO 2 — Canvas <<<]

[D2.1 · Console tab > Canvas]

Instead of a static dashboard, we ask the platform directly, and it builds the view.

---

[D2.2 · First starter question]

I'll start with a plain question: which controls apply to this system.

[Type the follow-up]

Now the one that matters. Which of those have been violated.

---

[D2.3 · Point at a violation]

There's a live violation, with its control, its environment, and the date it happened.

[Deck tab]

[>>> BACK TO DECK <<<]

---

## Slide 07 — Controls can execute in pre-production or production

The seventh principle. Controls can execute in pre-production or in production, and some conduct checks on documents.

Production is where Akka enforces guardrails, human-in-the-loop controls, sanitizers, and evals against running systems.

Pre-production is where you run tests, evaluations, model analysis, and red teaming before a change goes live. Akka gives you test, eval, and red-team kits for this, and they produce verdicts the same way production does.

How much you retest depends on the change. A model swap, an architecture change, a new data source, or a new jurisdiction calls for a full retest. A prompt or parameter change, a retrain, or vendor model drift calls for a targeted one. A bug fix, an ownership transfer, or a lapsed attestation needs a records update only.

Documents are the third place. A gate can check that a required attestation is on file and still fresh.

Consider what this does for your engineering teams. They can find out whether a system will pass governance while they are building it. Today, most systems can only be validated after it is built and sent for a review. Some controls such as a human escalation can only be verified in production, but you can test the functionality in pre-production too.

Verdicts from all three places are merged into one view.

---

## Slide 07b — Compliance is observing the verdicts for a group of controls over time

The eighth principle. Compliance is observing the verdicts for a group of controls over time.

We've talked about controls and risk profiles. Compliance is the question you ask of them. Is my AI system compliant right now? And has it drifted over time?

You can look at it by control, by regulation, or by bundle. How well do I satisfy this regulation? How have all the controls in my bundle done?

A violation tells you something happened. It doesn't by itself mean you're out of compliance. What matters is that you can see it and act on it. And everything here can be exported as OpenTelemetry spans, so your alerts and dashboards can live in the observability tools you already run.

---

## Slide 08 — Drift is a pattern change in the verdict ledger

The ninth principle. Drift is a pattern change in the verdict ledger.

You don't need a separate drift detector. Take a single control and watch its verdicts over time. If it behaves differently, that's drift.

Here, the PII redaction guardrail was upheld three weeks ago. Today it returns an error, because the classifier score fell outside its valid range and the control failed closed. The storage limitation gate was upheld, and today it's inconclusive, because its retention schedule aged past its freshness window.

Same control, same system. Only time changed.

The verdict shows me what changed. Replay lets me open the session behind it and see why.

[>>> DEMO 3 — Ledger / Drift / Replay <<<]

---

[D3.1 · Verdicts > By control. Point at the Certificate validity trend]

The numbers on the slide were illustrative. Here is a real verdict from this ledger: a control that checks how much validity is left on a certificate.

Each bar in the trend is a verdict. Green is upheld, and at the end it turns red.

[All verdicts. Filter to Certificate validity]

Filtered to that one control, newest first: upheld for weeks, then violations on the last two days.

---

[D3.2 · Open the latest breached verdict]

The newest says the certificate has eighty-eight days of validity left, inside the ninety-day renewal band. Same control, same system. Only time changed.

That's drift, and it's in the ledger with its reason. No separate detector.

---

[D3.3 · Replay > Traces. Open a trace]

The verdict shows what changed. Replay is how I get from a record to the session behind it: I can step through what the agent did, and where.

[Deck tab]

---

## Slide 09 — Controls can be enforced on third-party agents

The tenth principle. Controls can be enforced on third-party agents.

So far we could have been talking about agents that run on Akka. Many of the agents you run don't. Akka's AI gateway routes inference traffic and optimizes it. If you steer a third-party agent's model and tool requests through the gateway, we can identify that agent and enforce controls on it directly.

That covers most of what you need from guardrails, sanitizers, and evals on live traffic. Some controls, a human-in-the-loop escalation for example, need changes inside the third-party agent itself. For those, the agent sends its traces to Akka's ledger, so its behavior still lands in the same record as everything else.

For an agent built on Akka, the controls run natively in the runtime, and the platform governs the rest, human escalation included.

---

## Slide 10 — Traces, tokens, and verdicts are recorded together

The eleventh principle. Traces, tokens, and verdicts are recorded together.

Every call is measured, by team, use case, and system. Whether an agent runs on Akka or its traffic comes through the gateway, the trace carries its token usage, its cost, and the verdicts that fired. It all lands in one data warehouse.

Because it's all correlated, you can replay history, and you can see cost, performance, budget, and spend in the same place as governance.

That gives you three things. Observe: every model call is measured. Scrutinize: each team sees its own system's spend, and you can set thresholds so a crossed line becomes an action. Compare: you can keep testing models against each other on cost and performance, against a registry of known models and their prices.

Let me show you.

[>>> DEMO 4 — Optimize: spend, question in Canvas <<<]

---

[D4.1 · Optimize > Spend > Tokens]

Every token and every model, divided by use case, tag, and caller. This is cost, in the same console as governance.

---

[D4.2 · Canvas. Ask which models we pay for]

And I don't have to build a report. I ask: which models are we paying for.

[Wait for the answer]

That's the same record we've been reading all session, now showing cost beside the verdicts.

[Deck tab]

---

## Slide zz — Thank you

In summary, that's the operating model. You define your posture as controls, and you manage it as software. There are five types of controls, from three sources, packaged in signed bundles. Verdicts record every execution across pre-production and production, and compliance and drift are read from those verdicts. The same controls reach third-party agents through the gateway, and traces, tokens, and verdicts land together.

Akka is one platform for your developers, your AI risk and security teams, your machine learning engineers, and your infrastructure engineers to build agentic systems.

Thank you.

---

Spoken words: about 2641 (2641 on slides, 0 in demos). At 150 words a minute that is about 17 minutes on slides and 0 in demos, plus time spent clicking.
