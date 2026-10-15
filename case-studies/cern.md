# CERN keeps the world's largest machine running on 2.5 million signals a day

**Industry:** Scientific research / high-energy physics · **Offering:** Akka Agentic AI Platform

---

## Answer-first capsule

CERN gathers, stores, and analyzes more than 2.5 million signals a day — about 3.5 TB — from the operational devices that run its seven particle accelerators, including the 27-kilometer Large Hadron Collider and its 10,000+ superconducting magnets. That telemetry keeps the accelerators reliable for a scientific community of more than 12,000 researchers, with virtually no data loss.

---

## Akka ROI Scorecard

| Metric | Result |
|---|---|
| **Speed to Production** | **weeks** — to stand up a fault-tolerant acquisition service, not quarters. New data subscriptions are added non-disruptively, with no stop to acquisition from other devices. |
| **Cost to Operate** | **0** — data loss during infrastructure maintenance. The cluster shuts itself down and fully recreates itself when the network returns, with no operator intervention. |
| **Scale** | **2.5M+** — signals gathered, stored, and analyzed every day — roughly 3.5 TB — across seven accelerators, and built to grow with HL-LHC data volumes. |

*Business outcome: near-zero data loss on a mission-critical acquisition layer, running for **months** without a break.*

---

## The challenge

CERN operates seven large particle accelerators, including the Large Hadron Collider — with a circumference of 27 kilometers, the largest machine ever constructed, holding more than 10,000 superconducting magnets to accelerate and steer beams of subatomic particles. Keeping them reliable means capturing how hundreds of sub-systems and tens of thousands of devices behave, along with the shape and intensity of the particle beam itself.

CERN's earlier relational acquisition system, built in the early 2000s, had scaled well since 2003 but could not keep pace with the need for more complex, long-running analyses. The next-generation system demanded exceptional fault-tolerance to survive process failures with no data loss, even load-balancing of data subscriptions across processes, and the ability to add resources rapidly as new sources of data came online.

## Why Akka

CERN built its next-generation acquisition layer on Akka. The system spreads workload horizontally across nodes, adds resources dynamically, detects and reports failures, and persists the state of the distributed system to external storage so nothing is lost when a process goes down. It processes on the order of 100,000 messages per second across roughly 90,000 subscriptions, and isolates any device that suddenly sends excessive data onto its own worker so the wider acquisition layer stays stable.

The Akka Agentic AI Platform handles clustering, resilience, durable state, and workload distribution, so the application does not have to.

## The results

**Scale.** The acquisition system handles more than 2.5 million signals a day — about 3.5 TB — across seven accelerators, processing roughly 100,000 messages per second, and is built to grow with the fast-rising data volumes expected when HL-LHC comes online.

**Cost to operate.** During broader infrastructure maintenance the cluster shuts itself down and fully recreates itself when the network is restored, **with no loss of data** and no manual recovery — cutting the operational overhead of running a system that generates data continuously.

**Speed to production.** New data subscriptions are added **non-disruptively** whenever a new system is commissioned or a new mode of operation begins, without stopping acquisition from other devices — so the team keeps pace with the accelerators instead of scheduling around them.

**Business impact.** The acquisition layer is the go-to service for monitoring beam quality and troubleshooting accelerator equipment, with virtually no data loss — supporting some of the world's leading research into fundamental physics.

## The agentic opportunity

The same 2.5-million-signal-a-day telemetry that CERN already captures is exactly what an AI agent needs to act. On the **Akka Agentic AI Platform**, a monitoring agent reads those signals in real time, predicts when a device, magnet, or sub-system is drifting toward failure, and recommends corrective action before a fault interrupts a run — protecting beam time that is measured in months of continuous operation. The agent runs on the same fault-tolerant substrate CERN's acquisition layer already proved: durable state that survives failure, self-healing recovery, and horizontal scale to match rising data volumes.

The platform that acquires the telemetry is the same platform that builds and runs agentic AI on top of it. Organizations build on the **Akka Agentic AI Platform** directly, or have a system delivered and operated through **Akka Specify**. Both provide the production guarantees a mission-critical acquisition layer has always required.
