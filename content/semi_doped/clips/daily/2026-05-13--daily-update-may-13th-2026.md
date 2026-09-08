---
source: https://daily.semidoped.com/p/daily-update-may-13th-2026
title: Daily Update - May 13th, 2026
date: 2026-05-13
kind: clipping
genre: daily
audience: everyone
subtitle: Cowboy Space datacenters in space, Camtek, Infineon, and Gimlet Labs.
---
Cerebras IPO prices today, and trading will begin tomorrow May 14th, under ticker CRBS. Vik has a [deep dive piece](https://www.viksnewsletter.com/p/cerebras-ipo-and-the-scaling-bottlenecks) on Cerebras in case you haven’t seen it. Some scattered semi news we found interesting today, including datacenters in space, Camtek, power silicon on d-Matrix, and the Semi Doped podcast with Gimlet Labs.

Let’s check it out.

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

* * *

### Cowboy Space Raises $275M to build data centers in orbit

Cowboy Space is a startup by the billionaire founder of Robinhood, Baiju Bhatt, and recently rebranded from [Aetherflux](https://www.aetherflux.com/). They raised $275M with Index Ventures leading the funding, and the startup is valued at $2B. They want to use their own rockets to put datacenters into orbit, in a bid to compete with Space X. Targeting first rocket launch in 2028. ([Bloomberg](https://www.bloomberg.com/news/articles/2026-05-11/robinhood-billionaire-bhatt-s-cowboy-space-raises-275-million?cmpid=tech-in-depth&utm_campaign=tech-in-depth&utm_medium=email&utm_source=newsletter&utm_term=260512&utm_content=4371))

> _**Vik:**_****_Launching stuff into space is incredibly cool. The upper stage of the Cowboy Space rocket is the datacenter itself that will go into LEO. It will be power by solar. Wonder if their name is based on one of my favorite shows — Cowboy Bebop, which is entirely set in space?_
> 
> _**Austin:** I’m keeping tabs on this datacenter in space stuff, but am personally more interested in datacenters on Earth. Training clusters have to be fairly centralized, but what might it look like to distribute inference datacenters? Think [Cloudflare AI workers](https://www.cloudflare.com/products/workers-ai/), see this [video](https://www.nvidia.com/en-us/on-demand/session/gtc24-expt63299/)._

Watch their [cool video on X](https://x.com/CowboySpaceCorp/status/2053822995257348450?s=20). Doesn’t show any datacenter stuff, but like to see rocket 🔥.

### Camtek -15% on Q1: H2 ramp is the thesis, and the market isn’t buying it

[Camtek](https://www.camtek.com/) (CAMT) makes optical inspection and 3D metrology tools for advanced semiconductor packaging (HBM stacks, CoWoS interposers, OSAT process steps), competing with KLA and Onto Innovation. Management claims market leadership in 3D metrology and is gaining share in 2D inspection.

Q1 2026 revenue came in at $121.7M (slightly above Q1 2025) with gross margin holding at 51% and operating margin of 25.5%, down from 31.5% a year earlier. EPS landed at $0.70 vs $0.79. Q2 guidance is $129–131M (only ~7% sequential), with H2 2026 guided 25%+ higher than H1 and revenue from Eagle G5 and Hawk (30% of 2025 mix) guided to double in 2026. Two HBM customers have already placed orders and forecasts representing $260M+ for 2026 and 2027. 

> _**Austin:** Camtek’s stock is down 15% after the earnings call. Market not happy. Q2 guide of $129–131M is only ~7% sequential from Q1, which means H2 needs a 21%+ Q3 step to clear the “25%+ above H1” guidance._
> 
> [](https://substackcdn.com/image/fetch/$s_!kODt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe208544c-7b3c-457c-9f05-305e897e8b0a_1122x1118.png)

### Infineon collaborates with d-Matrix on Power Optimization

d-Matrix’s current inference accelerator — Corsair — uses Infineon OptiMOS TDM2254xx dual-phase power modules, which actually deliver power vertically (vertical power delivery - VPD) from under the compute die, rather than off to the side. This is a design win disclosure dressed up as a partnership announcement. Infineon gets to point at an inference customer. d-Matrix gets to signal that its board has serious power infrastructure behind it.

The VPD angle is the interesting part. Lateral power delivery breaks down once you push past roughly 1000A into a single package, because PCB trace resistance dominates and you waste too much in IR drop. Putting the VR module directly under the die solves that. Nvidia GB200/GB300 already does this with Vicor and MPS parts. Now d-Matrix is doing it with Infineon.

> _**Vik**_ : _This is incremental evidence that Infineon is building a credible AI power franchise thesis. The more interesting investor question is whether Infineon's TDM family is winning enough sockets across the inference ASIC universe to threaten MPS's dominant position in datacenter voltage regulators._

(via [Infineon](https://www.infineon.com/market-news/2026/infpss202605-087))

### Optimally splitting workloads across AI silicon

If you’ve been watching inference shift from one-size-fits-all GPUs to multi-vendor, multi-silicon data centers, this one is worth your time. 

Austin sat down with [Gimlet Labs](https://gimletlabs.ai/) co-founder Natalie Serrino and Beltir Caglar Dayanik to talk about what they’re building:

> _**Austin:** Really clever technology and business model to go with it. Watch it, listen, or just skim it here: [Gimlet Labs Interview](https://www.chipstrat.com/p/an-interview-with-the-gimlet-labs)._

### Quick Hits

  * **AWS** introduces Redshift “RG” instances powered by Graviton processors that allows running data warehousing workloads fasters, at lower price. ([AWS Blogs](https://aws.amazon.com/blogs/aws/amazon-redshift-introduces-aws-graviton-based-rg-instances-with-an-integrated-data-lake-query-engine/))

  * **Nebius** has broken ground on a gigawatt-scale AI data center on a 45-acre site in Independence, Missouri. The facility is expected to create 1,300 jobs during construction and operational phases. The project marks Nebius’s expansion into the North American market. ([Nebius](https://nebius.com/newsroom/nebius-breaks-ground-on-gigawatt-scale-ai-factory-in-independence-missouri))

  * **NVIDIA** Vera CPU collecting customers like Pokemon: CoreWeave, Meta, Oracle and Alibaba, are all signed up as early buyers according to [jukan05 on X](https://x.com/jukan05/status/2054089107878617189?s=20).




### Key Data

[Cignal AI predicts](https://cignal.ai/2026/05/elsfp-module-market-to-exceed-1-5-billion-by-2030/) that “this time feels different” when it comes to co-packaged optics (CPO). The projected demand for external laser sources for CPO (ELSFPs) from Nvidia indicates that either CPO has finally arrived, or there are going to be a lot of unused ELSFPs that you can hang from your keychains.

[](https://substackcdn.com/image/fetch/$s_!N_Kg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F45baf765-0072-42de-acd5-858576855d44_1280x720.jpeg)

### For Fun

This AI generated video of Jensen going to China last minute by [@CuiMao on X](https://x.com/CuiMao/status/2054407640198041720?s=20) is hilarious. 🤣

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-may-13th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
