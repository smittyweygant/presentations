# 1M+ healthcare providers rely on Doctolib for secure messaging

**Industry:** Healthcare · **Offering:** Akka Agentic AI Platform

---

## Answer-first capsule

Doctolib built a distributed, encrypted messaging system that 1M+ healthcare providers rely on to track patient care, handle referrals, and exchange medical expertise. It sustains 2,500 patient data messages per second at peak, holds 99.9999% availability, and was delivered in three months by two engineers — with no external cache or message queue to operate.

---

## Akka ROI Scorecard

| Metric | Result |
|---|---|
| **Speed to Production** | **3 mo** — from start to production, built by two engineers. Secure inter-server messaging shipped without stitching together an external cache or message queue. |
| **Cost to Operate** | **2** — engineers run the entire backend. Sharding, clustering, and replication are handled by the platform, removing the infrastructure Doctolib would otherwise staff and pay for. |
| **Scale** | **1M+** — healthcare providers served, with thousands of new users added every month and 2,500 patient messages per second sustained at peak traffic. |

*Business outcome: **99.9999%** service availability for sensitive patient data.*

---

## The challenge

Doctolib needed to modernize how healthcare providers track patient care, handle referrals, and exchange medical expertise. The messaging that carries this work moves sensitive patient data, so it had to be encrypted end to end, provably reliable, and compliant with European health-data regulation. Any interruption or data loss would put both patient care and regulatory standing at risk.

Meeting those requirements the conventional way meant assembling and operating an external cache and a message queue, then securing every hop between servers. That infrastructure carries a standing operational cost and a large compliance surface — precisely what a small engineering team cannot afford to run around the clock.

## Why Akka

Doctolib built its messaging on the **Akka Agentic AI Platform**, using sharding, pub/sub messaging, clustering, and replication to move encrypted messages between servers without an external cache or message queue. Removing those dependencies cut both the operational load and the compliance surface, which is why two engineers can run the entire backend.

The Akka Agentic AI Platform handles clustering, resilience, durable in-memory state, and traffic steering, so the application does not have to. Jasper Aarts, Senior Staff Engineer at Doctolib, put it directly: "What's great about Akka is that it just works. It's saved us a lot of hours in terms of setup, and we are able to run our entire backend system with just two engineers."

## The results

**Scale.** 1M+ healthcare providers rely on the messaging system, and thousands of new users join every month. At peak traffic it sustains 2,500 patient data messages per second.

**Cost to operate.** Two engineers run the entire backend. Because sharding, clustering, and replication are handled by the platform — and no external cache or message queue has to be maintained — Doctolib carries far less infrastructure and compliance overhead than a system of this scale usually demands.

**Speed to production.** The system went from start to production in three months with two engineers, delivering encrypted inter-server messaging without custom infrastructure to build first.

**Business impact.** Service availability reached 99.9999%, the level required to carry sensitive patient data for referrals, care tracking, and clinical exchange across a national provider base.

## The agentic opportunity

The same secure messaging fabric now enables agentic AI on the clinical surface. On the **Akka Agentic AI Platform**, an AI agent can triage inbound patient messages, schedule appointments, and route clinical requests to the right provider — reading and writing across the encrypted channels Doctolib already runs. Because governance, encryption, and durable state are properties of the platform, agent actions on patient data stay inside the same HIPAA- and GDPR-grade controls that carry the 2,500 messages per second today, with a full audit trail of every routing and scheduling decision.

The platform that scaled Doctolib's messaging to 1M+ providers is the same platform that builds and runs agentic AI today. Enterprises build on the **Akka Agentic AI Platform** directly, or have a system delivered and operated through **Akka Specify**. Both provide the production guarantees Doctolib has run its patient data on at 99.9999% availability.
