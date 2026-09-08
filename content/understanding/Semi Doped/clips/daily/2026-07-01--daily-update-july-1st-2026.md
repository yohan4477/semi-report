---
source: https://daily.semidoped.com/p/daily-update-july-1st-2026
title: Daily Update - July 1st, 2026
date: 2026-07-01
kind: clipping
genre: daily
audience: everyone
subtitle: New announcements from Etched, ASM $400M High-NA EUV machine, steel-can batteries, ++
---
Etched has emerged from stealth with over $1 billion in customer contracts, indicating significant early market validation for its AI chip technology. ASML’s $400 million High-NA EUV machine has achieved 8nm resolution, a critical advancement for next-generation chip manufacturing. 

Lighter on takes today since Austin is on vacation (he still got a take in!) and Vik is battling a cold.

Let’s get into it. _— Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

### Etched Emerges from Stealth with $1B+ Customer Contracts

Etched came out of stealth with a successful A0 tapeout, more than $1 billion in customer contracts, and $800 million raised, and says its first racks ship this summer after early tests showed state-of-the-art throughput, latency, and power efficiency. The round drew Jane Street (over $100 million on its own), HRT, Two Sigma, Jump, and a strategic investment from TSMC’s VentureTech Alliance, alongside a 400+ team pulled from Nvidia, Google’s TPU group, Broadcom, SK Hynix, and TSMC and angels including Geoffrey Hinton, Peter Thiel, Andrej Karpathy, and Fei-Fei Li.

To push the pareto curve on many-trillion-parameter MoEs, long context, and agentic workloads, Etched co-designed the whole cluster “from the transistor to the token” around two ideas. Low-Voltage Inference (LVI) runs its math blocks at under half the voltage of most AI chips, which today downclock as FLOPs utilization rises and often sustain under half their peak FLOPs; Etched claims 80%+ of peak on trillion-parameter sparse MoEs without thermal throttling. Cluster-Scale Memory (CSM) pools low-latency memory across the entire scale-up domain over a proprietary interconnect, pairing HBM and SRAM to reach SRAM-level decode speed without the capacity, cost, and yield tradeoffs of SRAM-only or 3D DRAM designs. Etched also built a 2MW datacenter in its office and opened a Taiwan factory, with performance and roadmap details due this summer. ([@Etched](https://x.com/Etched/status/2071972062202343590), [Bloomberg](https://www.bloomberg.com/news/articles/2026-06-30/ai-chip-startup-etched-says-jane-street-tsmc-linked-vc-invested))

> _**Vik:** Etched seems to have designed a lot more than just the silicon. They seem to have designed the whole rack, including PCBs, liquid cooling, and network “connections” (whatever that means). Underclocking compute seems to help thermals, and they appear to treat all memory in the Etched cluster as “one.” Pretty smart stuff. Excited for more!_
> 
> _**Austin:** A lot has been announced recently in the AI ASIC startup space. I’ll write about it soon, probably right after the 4th of July holiday._

[](https://substackcdn.com/image/fetch/$s_!J3s_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff68db590-876d-4024-b710-adcec83aa18e_1735x2200.webp)Source: Etched

### ASML’s $400M High-NA EUV Machine Achieves 8nm Resolution

ASML started shipping its high-NA EUV lithography machine, a $400 million, 150-ton system the size of a double-decker bus that patterns chip features down to 8 nanometers, versus 13nm on the prior EUV generation. High-NA is evolutionary rather than a new source of light: ASML raised the numerical aperture from 0.33 to 0.55, which cuts transistor size by nearly half and roughly triples density, and lets chipmakers single-pattern layers that today need slower, costlier multi-patterning. 

Intel bought the very first high-NA machine and is testing it in Oregon, hoping first-mover access gives its foundry an edge on TSMC and Samsung. TSMC is holding back, calling high-NA only 30 to 50% better and not obviously worth $400 million, and may not run it in volume until the 2030s. The duopoly is also drawing challengers doing end runs around EUV: China is pouring billions into its own extreme-ultraviolet program, San Francisco’s Substrate is chasing x-ray lithography from a compact particle accelerator (targeting $10,000 wafers and its own fab by 2030), and Norway’s Lace Lithography is firing helium-atom beams at 0.1nm precision (2029 to 2030). ASML’s Jos Benschop doubts any of them scale to volume, and is already sketching a hyper-NA successor (0.55 to 0.75, roughly 6nm) for the second half of the 2030s. ([technologyreview.com](https://www.technologyreview.com/2026/06/23/1138837/asml-400-million-dollar-machine-powering-future-of-chipmaking/))

> _**Vik:** Where lithography goes from here is anyone’s guess, but its great to see so many options emerging._

### Meta develops ultra-narrow steel-can batteries for AI glasses

Meta engineers developed steel-can battery technology with widths as narrow as 7mm for AI glasses like Ray-Ban Meta and Oakley Meta Vanguards. This involved replacing traditional wound “jelly roll” electrode material with die-cut stacked layers to achieve lower impedance. The Gen 1 Meta Ray-Ban’s cell capacity grew from 160 mAh to 210 mAh, and the Meta Ray-Ban Display glasses feature a 248 mAh steel-can cell. ([engineering.fb.com](https://engineering.fb.com/2026/06/23/production-engineering/how-meta-built-ultra-narrow-batteries-for-ai-glasses-meta-tech-podcast/))

> _**Vik:** Like a AAA battery but way smaller?_

[](https://substackcdn.com/image/fetch/$s_!jQHz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd2c7941e-2872-4150-8376-e2c77f85e1b1_1376x768.png)Source: Meta

### TSMC Accelerates CoPoS Optical Packaging Under Supply Chain Silence

TSMC is fast-tracking development of Co-Packaged Optics on Substrate (CoPoS), an advanced optical packaging technology that integrates photonics directly with chips at the substrate level. The company has placed its entire supply chain under a non-disclosure agreement, barring partners and vendors from discussing the program publicly. CoPoS is aimed at data center interconnect applications where electrical signaling faces bandwidth and power limits at scale. ([digitimes](https://www.digitimes.com/news/a20260630PD239/tsmc-supply-chain-cowos-packaging-equipment.html))

> _**Vik:** CoPoS is an open secret now, and lots of people can guess who Taiwanese suppliers are._
> 
> _From Pres. Bill Chiu: “TSMC will need to expand domestic procurement, since only**local suppliers can respond quickly enough to keep pace with R &D needs** — meaning Taiwan-based equipment and materials makers in the first wave of CoPoS suppliers stand to benefit.”_

## Sector Watch

  * **TSMC** Q2 gross margins near 70% on insatiable 3nm and 5nm demand; Q3 revenue projected to grow over 10% sequentially. ([TrendForce](https://www.trendforce.com/news/2026/06/29/news-tsmcs-2q-margins-reportedly-near-70-as-ai-demand-strengthens-3q-revenue-seen-growing-over-10-sequentially/))

  * **Anthropic** receives US government approval to expand Mythos 5 model access, removing regulatory bottleneck for commercial deployment. ([Bloomberg Tech](https://www.bloomberg.com/news/videos/2026-06-29/anthropic-s-mythos-5-cleared-by-us-for-wider-use-video))

  * **ByteDance** advances in-house CPU design for 2027 deployment, reinforcing vertical AI stack trend among Chinese tech giants. ([SCMP Tech](https://www.scmp.com/tech/tech-trends/article/3358777/bytedance-targets-early-next-year-new-cpu-power-own-ai-infrastructure-sources?utm_source=rss_feed))

  * **Nvidia Research** publishes a self-evolving AI agent framework for hardware design that treats RTL development as repository-level code evolution. ([Semiconductor Engineering](https://semiengineering.com/a-self-evolving-agent-framework-that-treats-hardware-design-as-repository-level-code-evolution-nvidia-research/))




### By the Numbers

Closing moves, 2026-06-30:

  * **AMBA** ▲ +28.0% — Rosenblatt labeled Ambarella a ‘Physical AI Pure Play’ and set a $120 price target, sparking the 28% surge.

  * **MXL** ▲ +18.0% — Stifel raised MaxLinear’s price target to $110, maintaining Buy on AI infrastructure end-market strength.

  * **FORM** ▲ +10.9% — _no clear catalyst from public sources_

  * **SNDK** ▲ +10.9% — Analysts flagged a record-breaking quarter and projected another large jump, driving Sandisk’s 10.9% gain. 

  * **CRDO** ▲ +10.7% — Strong Q4 results and analyst upgrades drove Credo Technology shares up ~11%.

  * **IMOS** ▲ +10.2% — Post-dividend selling pressure faded for ChipMOS, allowing shares to recover ~10% as the dividend hangover cleared. 




**Down:** CLSK -5.3%, HPQ -3.1%, SKYT -2.2%, QCOM -2.1%, WDC -2.0%

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-july-1st-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
