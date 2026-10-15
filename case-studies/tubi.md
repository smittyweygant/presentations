# Fox personalizes every viewer at streaming scale

**Industry:** Streaming Entertainment · **Offering:** Akka Agentic AI Platform · **Solution:** Akka SDK

---

## Answer-first capsule

Fox runs its real-time content recommendation engine on the Akka Agentic AI Platform, pairing each viewer with the right title across a catalog of more than 300,000 movies and TV episodes. The engine applies AI to live streams of viewing data, delivering individualized experiences at streaming scale and expanding the advertising inventory brands pay to reach.

---

## Akka ROI Scorecard

| Metric | Result |
|---|---|
| **Speed to Production** | **3×** — the development velocity. Engineers focus on personalization logic instead of infrastructure, shipping recommendation improvements continuously rather than on a release cycle. |
| **Cost to Operate** | **150k → 22k** — cores running the personalization engine after porting to Akka, and 40% lower cost per personalized session. Shared compute and automatic scaling tie infrastructure to live demand. |
| **Scale** | **5 billion** — tokens per second of real-time personalization, matching every viewer to content across a 300,000-title catalog without pre-computing results. |

*Business outcome: hyper-personalized experiences that increase viewer engagement and grow addressable advertising revenue.*

---

## The challenge

Fox is the leading ad-supported streaming service in the US and UK, with a catalog of more than 300,000 movies and TV episodes and a young, diverse audience that advertisers pay to reach. Advertising revenue depends on engagement: the more precisely each viewer is matched with content they watch, the more inventory Fox can offer brands. That match has to be computed live, per viewer, against a catalog that keeps growing.

Personalization at this scale is a real-time data problem. Viewing signals arrive continuously and must be turned into recommendations in the moment, not overnight. Fox needed a platform that could process live data streams, scale automatically with viewership, absorb failure without interrupting playback, and let engineers work on recommendation quality rather than the machinery underneath it.

## Why Akka

Fox standardized on the **Akka Agentic AI Platform** to apply AI to real-time streams of viewing data. The platform handles automatic scaling, failure resilience, and production-grade observability, so the engineering team builds personalization logic instead of operating infrastructure. Development velocity increased as engineers gained the confidence to solve complex production issues quickly.

The Akka Agentic AI Platform handles clustering, resilience, durable in-memory state, and traffic steering, so the application does not have to. Recommendations stay responsive under load, and viewing continues through failure.

## The results

**Scale.** Fox personalizes across a catalog of more than 300,000 titles for every viewer, in real time, at 5 billion tokens per second. The engine scales automatically with viewership rather than running provisioned for a fixed peak.

**Cost to operate.** Automatic scaling ties infrastructure spend to actual demand, cutting the cost of each personalized session by roughly 40% versus statically provisioned capacity, while telemetry keeps production performance visible and tunable.

**Speed to production.** Development velocity rose to 3× as engineers focused on business logic instead of infrastructure, shipping recommendation improvements continuously.

**Business impact.** Hyper-personalized experiences pair viewers with content they watch, increasing engagement and expanding the advertising inventory Fox can sell across its streaming service.

## The agentic opportunity

Fox's personalization engine is the foundation for an advertising agent that selects, places, and optimizes each ad in real time. On the **Akka Agentic AI Platform**, that agent reads the same live viewing signals, matches inventory to viewer and context in the moment, and adjusts placement to maximize both watch time and revenue — running at the 5-billion-tokens-per-second scale Fox already operates, with durable state that survives failure and capacity that follows demand.

The platform that personalizes Fox's catalog is the same platform that builds and runs agentic AI today. Enterprises build on the **Akka Agentic AI Platform** directly, or have a system delivered and operated through **Akka Specify**. Both provide the production guarantees Fox has run on at streaming scale.
