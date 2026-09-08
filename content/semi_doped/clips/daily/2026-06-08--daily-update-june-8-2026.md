---
source: https://daily.semidoped.com/p/daily-update-june-8-2026
title: Daily Update - June 8, 2026
date: 2026-06-08
kind: clipping
genre: daily
audience: everyone
subtitle: Market slumps last week, memory demand is strong, Rubin SOCAMM scare, NPO scale-up, power delivery startup Lotus Microsystems
---
Austin and Vik are back from Computex 2026. Incredible show, but very tiring. Chip markets turn around, and lots of talk about memory and near packaged optics. 

Lets get to it!

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

* * *

### **Chip slump erases $1.3 trillion in value**

A broad selloff in semiconductor stocks late last week wiped roughly **$1.3 trillion** from market value, with memory names Micron and Sandisk among the steepest decliners as traders rotated out of high-flying AI plays. Friday's selloff added to losses on Thursday after **Broadcom’s earning calls showed that demand for their custom ASICs fell short of expectations**.

Micron and Sandisk, which had rallied on AI-driven memory demand, gave back gains as investors trimmed exposure to the year’s best-performing chip trades. Nvidia, AMD, and Broadcom also closed lower in the session. Jensen calls this a great buying opportunity.

(via [Reuters](https://www.reuters.com/business/media-telecom/chip-selloff-erases-over-1-trillion-stock-market-value-2026-06-05/))

> _**Vik:** It looks the market’s exuberance is finally cooling off, but such short drawdowns are not indicative of anything long term. There is some concern that companies are getting sticker shock at their AI bills. We will have to wait and see if this materially affects token spend, whether Anthropic’s steep ARR ascent will be curtailed, and CapEx spending levels off. Those are signs to watch for._
> 
> _**Austin:**_****_Not investment advice; agree that this feels like one of those opportunities where nothing has materially changed about AI infra demand or supply._

### **Nvidia, SK Hynix Sign Multi-Year Memory Pact**

SK hynix and Nvidia announced a multi-year technology partnership to co-develop next-generation memory for Nvidia’s AI platforms, unveiled in Seoul by SK Group Chairman Chey Tae-won and Nvidia CEO Jensen Huang. The agreement covers memory for Nvidia’s Vera Rubin, Vera CPU, RTX Spark, and Jetson Thor platforms, and includes SK hynix adopting Nvidia’s Omniverse and CUDA-X software across its fabs. The announcement did not specify HBM allocation, exclusivity terms, or supply commitments. Huang separately flagged a prolonged chip shortage during the briefing.

(via [Nvidia news](https://nvidianews.nvidia.com/news/sk-hynix-ai-factory))

> _**Vik:** I personally do not see the demand for memory leveling off. Co-development efforts are strong signals that memory remains an important part of AI. There is no alternative in the near horizon given how AI works._
> 
> _**Austin:** Edge is going to continue to demand more memory too. I’m convinced local token generators will be necessary, yet the biggest complaint is that local machines (whether laptop, desktop, or even air-cooled on-premises AI racks) don’t have enough memory to support useful models with big enough context. I think interesting research with memory tiers, more efficient KV caches, and so on could impact edge device memory demand as much as datacenter. _

### **The SoCAMM Rubin Scare**

Memory stocks sold off sharply after reports that NVIDIA would halve CPU-side SOCAMM (LPDDR5X) DRAM in Vera Rubin NVL72 racks—from ~55TB to ~28TB per rack—by shipping most systems with 96GB modules instead of 192GB ones. The story originated from SemiAnalysis’s institutional research note, which was widely excerpted on social media and triggered fears of weakening AI memory demand. Founder Dylan Patel quickly clarified that the note had been taken out of context, noting most people “leave out most of the content”. 

The full analysis presented the change as a deliberate optimization, not a demand warning. Analysts view the move as bullish for DRAM overall. With LPDDR5X supply still extremely tight, NVIDIA’s right-sized configs ease bottlenecks, cut ~$800K per-rack costs, improve TCO, and allow more Rubin systems to ship—reflecting smart supply-chain management amid strong AI-driven demand.

> _**Vik:** This is not the first time social media has taken institutional reports out of context, but this is also the danger of providing info to a select few. PSA to think carefully about what you’re looking at and asking “why?”_
> 
>  _**Austin:** This is the SemiAnalysis business model working as designed. Sell market-moving research to a select few, and snippets will leak and lose their context on the way out the door. Sell-side notes do the same thing. There are fixes, but none are as profitable or scalable as the current approach, so it will keep happening. _
> 
> _Funny enough, that asymmetry is really the product: if you paid for the whole note, everyone else’s out-of-context panic is your edge. You read the full thing, retail got it wrong, the dip is a buying opportunity._

### **The Rubin Ultra NPO Shift**

Reports revealed NVIDIA’s Rubin Ultra NVL576 platform would use Near-Package Optics (NPO) for inter-rack scale-up—nearly doubling optical-engine content per GPU from ~2.25 to ~4.0 (+78%) and implying ~12M units of demand. 

The story originated from FundaAI’s institutional weekly research note, which was widely circulated on social media and forums. FundaAI presented the shift as a deliberate supply-chain decision favoring modular NPO over full CPO internalization. Analysts view it as bullish for the broader optics ecosystem. 

NPO preserves and expands value for specialized optical-engine makers, lasers, DSPs, and SiPh foundries—accelerating AI networking deployment and capturing more content amid exploding Rubin Ultra demand—without handing the entire interconnect stack to vertically integrated chip giants.

> _**Vik:** I personally think that NPO is a very practical near term approach. The Rubin Ultra mid-plane PCB is a monstrosity prone to problems, and going direct to co-packaged optics has its challenges at scale. There are lots of unsolved problems. NPO is the “goldilocks zone.”_
> 
>  _**Austin:** Vik [tweeted](https://x.com/vikramskr/status/2063618075409477719) about this and it got >120K views! (Tweeted… posted… whatever)_

### Startup News

#### **Power Goes Vertical: Lotus Microsystems Launches vStrata**

Copenhagen startup [Lotus Microsystems has launched vStrata](https://www.globenewswire.com/news-release/2026/06/08/3308071/0/en/lotus-microsystems-launches-first-vstrata-module-a-vertical-power-delivery-platform-designed-to-break-through-power-and-thermal-limits-in-ai-infrastructure.html), a vertical power delivery platform that moves power conversion directly beneath the processor while managing heat at the same location.

The first module, LSC0580, has taped out for unnamed “leading xPU and AI infrastructure” partners, with engineering samples scheduled to ship in Q3 2026.

Built on the company’s silicon Power Interposer Technology, Lotus claims vStrata:

  * Cuts power conversion losses by more than 50%

  * Achieves up to 96% point-of-load efficiency

  * Handles kiloampere-class loads and transients above 10 A/ns without external capacitors

  * Lowers operating temperatures by up to 25°C

  * Has a roadmap to sub-1 mm thickness




The company says it is working with Tier-1 hyperscalers through an Early Access Program and will demonstrate the module at PCIM Europe (June 9-11).

> _**Austin:** I just wrote about power delivery, [check it out here](https://www.chipstrat.com/p/power-moves-into-the-package-empower) to get up to speed. The space is heating up._

### Key Data

We love this chart. Notice how much of _both_ optics and copper are in there?

[](https://substackcdn.com/image/fetch/$s_!gYjo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4faa3ff5-c329-4064-b97d-06b467e3ca0e_1079x410.jpeg)

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-june-8-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
