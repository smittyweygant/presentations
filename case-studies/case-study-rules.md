# Akka Case Study — Writing Rules

Governing rules for rewriting akka.io customer stories to enforce Akka positioning. Every case study must pass every rule below. Reference implementation: `verizon.md` / `verizon.html`.

---

## 1. Voice — direct statements of fact, no quips

State what happened and what it means. Nothing else. If a sentence is doing anything other than delivering a fact, cut it.

**Banned — quips, flourishes, and AI-tell wording:**
- No "throughline," "at its core," "in its purest form," "the answer that," "this is where," "make no mistake," "it's worth noting," "testament to," "at the end of the day."
- No "isn't just X — it's Y" reveals. No colon-drama ("This is the real story: …"). No rhetorical questions.
- No hype verbs: "unlock," "supercharge," "leverage" (as a flourish), "harness" (as a flourish), "empower," "revolutionize," "seamless," "game-changer," "journey," "delve," "tapestry," "fast-paced world."
- No em-dash used as a dramatic punchline. Em-dash is allowed only to attach a clarifying clause.
- No adjectives standing in for numbers ("blazing-fast," "massive," "incredible"). Use the number.
- No aspirational "together" or unity tag: not "Growing X — Together," "build the future together," "let's do this together," "X, together." It is empty warmth. State what happens, and cut "together."
- No "X, not Y" antithesis or abstract negation for rhythm ("a partnership, not a handoff"; "we don't bet the plant, we grow it"; "the gap is not the product"). State the fact once, plainly and positively.
- No rhythmic triads assembled for cadence ("protect the standard, keep the crew, and grow the business"). List only what carries information.
- No aspirational abstractions ("the reputation the business runs on," "share in what it earns next," "a modern, credible front door") and no reassurance tags ("without compromising the standard," "stays exactly as it is"). Say the concrete thing.
- No flippant or presumptuous colloquial closers ("tell me if you want in," "let's do this," "sound good?," "here's the deal"). They read as glib or condescending. End on a fact or a plain, respectful ask.
- No stilted, bookish phrasing no one says out loud ("price is not the first of them," "not the least of which," "chief among them," "therein lies"). Read every sentence aloud; if you would not say it in conversation, rewrite it.
- No decorative numbered markers (01 / 02 / 03) on cards, boxes, tiles, or sections that are not an actual ordered sequence. Numbering is allowed only when the order carries real meaning (a true process or ranked steps).
- No clipped, telegraphic object-lists no one would say out loud, and never treat people or values as things you "keep," "hold," or "retain" ("I keep the standard and the crew," "we retain quality and talent"). Say what actually happens to the work and to the people.
- Don't tack a benefit, payoff, reassurance, or invitation onto the end of a statement or paragraph ("...so you win too," "I'd rather you tell me where I'm wrong now than later," "and that's how we all succeed"). State the point and stop. The last sentence has to be content, not a closer.
- Don't editorialize or over-emphasize a point ("This is the big one," "This is key," "what really matters is," "make no mistake"). State it plainly and move on; emphasis comes from order or a number, not narration.
- No empty intensifiers used for emphasis: "real" ("a real website," "a real stake," "real money"), "actually," "truly," "genuine." Name the thing plainly.
- No "the shape of X" and no "X-shaped" as a descriptor ("the shape of the obligations," "the shape of the problem," "the shape of the claim," "an LLM-shaped task"). It is AI speak; no one says it out loud. Name the property you mean — the size, the structure, the split, the category — or state the thing itself.

**Required instead:** subject–verb–fact. "Throughput rose from 1,600 to 12,000 orders per minute." Lead every paragraph with the fact; explain after. If you would not say it to a skeptical engineer across a table, do not write it.

The test: read any sentence and ask "is this a fact or a flourish?" Flourishes get deleted, not softened.

**Never expose the author's chain of thought or a figure's provenance.** The paper is the customer's story, not a record of how it was written.
- No editorial annotations, ever: no "(invented)," "(invented, defensible)," "illustrative estimate," "Akka estimate," "figures are illustrative," "for illustration," "not reported metrics," "reflects capabilities described in the source."
- No hedges that signal a number isn't real: not "an estimated 60% lower," just "60% lower." Invented figures (allowed — see rule 6) are stated cleanly as fact, with no tell that they were invented.
- A customer's *own* forward-looking estimate is fine as narrative ("a four-to-six-month plan," "the industry loses an estimated $7B a year") — that is the customer's number, not a disclaimer about ours.

## 2. Runtime internals

- Actors and actor-based concurrency are allowed. That restriction was lifted 2026-08-02,
  matching the same removal from the HubSpot content rules on 2026-07-27.
- Still out: garbage collection, JVM heap sizes, and naming a specific competing framework
  being replaced (e.g. Spring Boot).
- Speak only at the umbrella level: the **Akka Agentic AI Platform** or **Akka Specify**.
- Keep customer-visible outcomes (hardware halved, TCO cut in half, latency, throughput). Drop the implementation mechanism that reveals the library era.
- Naming the customer's *former* vendor (Oracle, etc.) is fine — that is their incumbent, not an Akka library.

## 3. Always extrapolate an AI use case

Every story ends by extrapolating a concrete agentic-AI use case from the work that was actually done, framed under the **Akka Agentic AI Platform** and/or **Akka Specify** umbrella.

- Extrapolate honestly from real facts (channels, volumes, workloads the customer already had). Do not assert the customer deployed agents they did not.
- Name specific AI agent behavior the work implies (e.g. an agent that takes an order, personalizes an offer, runs eligibility/fraud checks, orchestrates fulfillment).
- Close by naming both paths onto the platform: build it on the **Akka Agentic AI Platform**, or have it delivered and operated through **Akka Specify**.

## 4. The ROI Scorecard — the same three metrics every time

Every case study reports a scorecard with these three metrics, each with the customer's real number:

| Metric | Measures | Primarily proves |
|---|---|---|
| **Speed to Production** | Time from requirement to live system, and change velocity after | Akka Specify + spec-driven development |
| **Cost to Operate** | Infrastructure + operational TCO for the same volume | The platform's shared-compute efficiency |
| **Scale** | Throughput / concurrency sustained at production reliability | The platform's runtime guarantees |

Business outcomes (revenue, conversion) are reported as a supporting line under the scorecard, not as a fourth metric — not every customer discloses them.

## 5. Structure — the eight sections

1. **Headline** — outcome, direct.
2. **Meta line** — Industry · Offering (Akka Agentic AI Platform / Akka Specify). No date.
3. **Answer-first capsule** — 40–60 words, carries the headline numbers (AEO/GEO extractable).
4. **Akka ROI Scorecard** — the three metrics above + supporting outcome line.
5. **The challenge** — the business problem, in facts.
6. **Why Akka** — the decision and the platform capability it maps to.
7. **The results** — quantified, grouped under the three ROI metrics.
8. **The agentic opportunity** — the AI extrapolation (rule 3). This is the last section; the CTA band follows.

**No Sources section, and no dates about when the paper was made.** Do not publish a citation, a source link, or a "Reviewed / drafted / as of" date — users don't need to see where the content came from or when it was written. (Customer-history dates that are part of the story — "acquired in 2019," "built in 2003" — are fine.)

## 6. Evidence (research, not published citations)

- Do the sourcing research to get real numbers — the akka.io story, or the archived Lightbend original for revived logos — but **do not surface the source in the paper.** No Sources block, no "attributed to X as reported," no archive URL.
- Use primary-source figures over any internal restatement. (Verizon: use 1,600 → 12,000 orders/min = 7.5×, from the case study.)
- Inventing ROI figures is allowed where the source lacks them (see rule 1): state them cleanly as fact, never flagged as invented.

## 7. Format / brand (HTML)

- Each page links the shared `case-study.css`; do not inline a `<style>` block.
- Match the akka.io case-study template: dark hero (eyebrow → headline → subtitle → meta), white article body, dark "Let's Build Trust Together" CTA band.
- Type: Instrument Sans (display) + Roboto (body). Accent: **#FFCE4A**. Black `#0B0B0C`.
- Real HTML tables/text, never images of data. If adding JSON-LD, use `Organization` only — no date fields.
