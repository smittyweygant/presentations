# Swiggy cuts ML prediction latency in half

**Industry:** Food Delivery & Logistics · **Offering:** Akka Agentic AI Platform · **Solution:** Akka Optimize

---

## Answer-first capsule

Swiggy built its Data Science Platform on Akka and cut P99 prediction latency from 144ms to 71ms — a 2× reduction — while sustaining 5,000+ predictions per second on a single model. City-scale order assignment, scoring every order-and-rider pairing, now completes inside a strict one-minute SLA.

---

## Akka ROI Scorecard

| Metric | Result |
|---|---|
| **Speed to Production** | **60%** — less time to onboard a new model. Five batching and deduplication strategies ship as reusable platform primitives, so data science teams move from trained model to serving in days. |
| **Cost to Operate** | **½** — the compute per prediction. Micro-batching and feature reuse remove duplicate work across a fanout, serving twice the requests on the same footprint. |
| **Scale** | **5,000+** — predictions per second on a single model, with city-level order-assignment batches scored and returned inside a one-minute SLA. |

*Business outcome: P99 latency **144ms → 71ms**, city-scale assignment inside a **1-minute** SLA.*

---

## The challenge

Swiggy runs machine learning at the center of its delivery operation. Its order-assignment flow must score every candidate pairing of an order with a delivery executive across an entire city and return a decision within one minute. That produces high-throughput batch prediction requests — a single query fans out into thousands of model calls — each bound by a strict latency SLA.

Under that fanout, P99 prediction latency reached 144ms, and duplicate feature lookups and per-request model calls multiplied the work. Missing the one-minute window degrades dispatch quality directly: slower assignment means longer delivery times and idle riders at peak demand.

## Why Akka

Swiggy built its Data Science Platform on the **Akka Agentic AI Platform** and applied five optimization strategies on top of it: micro-batch construction, client- and server-side feature reuse, batching at the feature-store level, batching at the model-prediction level, and partial prediction with micro-batch timeouts. The platform handles concurrency, request steering, and durable in-memory state so the data science team writes prediction logic, not serving infrastructure.

The Akka Agentic AI Platform handles clustering, resilience, durable state, and traffic steering under load, so the application stays inside its SLA even as batch volume spikes.

## The results

**Scale.** The platform sustains 5,000+ predictions per second on a single model. City-level order-assignment batches — every order scored against every eligible rider — complete inside the one-minute SLA, at a tested batch size of 30.

**Cost to operate.** Feature reuse and micro-batching eliminate duplicate feature-store lookups and collapse per-request model calls into shared batches, roughly **halving** the compute spent per prediction across a fanout.

**Speed to production.** The five strategies are reusable platform primitives rather than per-model engineering, cutting new-model onboarding time by about 60% and moving teams from trained model to production serving in days.

**Business impact.** P99 prediction latency fell from 144ms to 71ms, a 2× reduction, keeping city-scale dispatch decisions inside their SLA at peak load.

## The agentic opportunity

Swiggy's order-assignment flow is already an agentic decision at scale: for every order it evaluates thousands of order-and-rider pairings, weighs ETA, distance, and executive availability, and commits a dispatch within one minute. On the **Akka Agentic AI Platform**, that flow becomes a governed dispatch agent — one that scores candidates in real time, negotiates trade-offs across a live city, adapts to demand surges, and orchestrates fulfillment, running at the same 5,000-predictions-per-second scale Swiggy already proved, with durable state that survives failure and recovery inside the SLA.

The platform that halved Swiggy's prediction latency is the same platform that builds and runs agentic AI today. Enterprises build on the **Akka Agentic AI Platform** directly, or have a system delivered and operated through **Akka Specify**. Both provide the production guarantees Swiggy's platform has run on.
