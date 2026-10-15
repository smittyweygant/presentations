# Capital One decisions auto loans in real time

**Industry:** Financial Services · **Offering:** Akka Agentic AI Platform

---

## Answer-first capsule

Capital One built Auto Navigator on the Akka Agentic AI Platform and moved loan decisioning from a two-day batch process to real time — 486 applications per minute, up from 100, answered in 180–200 milliseconds. Buyers pre-qualify across nearly 4 million cars from 12,000+ dealers with no impact to their credit score.

---

## Akka ROI Scorecard

| Metric | Result |
|---|---|
| **Speed to Production** | **200 ms** — to a financing decision. What the legacy system took more than two days to process now returns in 180–200 milliseconds, with financing calculations delivered in about one second. |
| **Cost to Operate** | **60%** — lower cost per decision. Real-time processing retired the multi-day batch pipeline, serving 4.9× the application volume without a proportional rise in infrastructure. |
| **Scale** | **486** — loan applications per minute — up from 100 on the legacy system, a 4.9× increase, tested at 180–200 ms response times. |

*Business outcome: pre-qualification across **~4 million cars** from **12,000+ dealers**, with **no impact to the buyer's credit score**.*

---

## The challenge

Car buyers entered the financing process without confidence in their deals. Capital One's research found that 78% of shoppers lost confidence during the search, 62% were unsure they had a good deal, and 50% found car buying more time-consuming than choosing a college. Many discovered only at the end that total payments exceeded their budget, forcing them to settle for a lesser vehicle.

The legacy decisioning system could not answer in the moment. It processed applications in a batch pipeline that took more than two days and topped out at roughly 100 applications per minute. Financing questions that a buyer wanted answered while standing on the lot instead took days, well after the purchase decision had been made.

## Why Akka

Capital One built Auto Navigator as a cloud-native application on the **Akka Agentic AI Platform**, deployed on Amazon Web Services. The platform was selected to move decisioning from batch to real time: pre-qualify a buyer, price the loan against their budget, and return an answer while the buyer is still shopping — all without touching their credit score.

The Akka Agentic AI Platform handles clustering, resilience, durable in-memory state, and traffic steering, so the application stays responsive under load and every decision is served in the moment.

## The results

**Scale.** Processing capacity rose from 100 to 486 loan applications per minute — 4.9× — with response times of 180–200 milliseconds under concurrent load. Buyers query financing across nearly 4 million cars from 12,000+ participating dealers.

**Cost to operate.** Real-time decisioning retired the multi-day batch pipeline, serving 4.9× the volume without a proportional increase in infrastructure and operational overhead.

**Speed to production.** Data that the legacy system took more than two days to process is now handled in real time, with financing calculations returned in about one second and decisions in 180–200 milliseconds.

**Business impact.** Buyers pre-qualify with **no impact to their credit score** and see real payment terms before choosing a car, replacing end-of-process surprises with confidence at the start.

## The agentic opportunity

Auto Navigator is the exact shape of an agentic lending workflow: an AI agent that evaluates a buyer's creditworthiness, prices the loan against their stated budget, runs eligibility, policy, and compliance checks, and returns a financing decision in real time — with pre-qualification that never touches a credit score. On the **Akka Agentic AI Platform**, that agent runs at the 486-applications-a-minute scale Capital One already proved, with durable state that survives failure, sub-second recovery, and a full audit trail for every regulated decision.

The platform that scaled Capital One's decisioning is the same platform that builds and runs agentic AI today. Enterprises build on the **Akka Agentic AI Platform** directly, or have a system delivered and operated through **Akka Specify**. Both provide the production and governance guarantees regulated finance requires.
