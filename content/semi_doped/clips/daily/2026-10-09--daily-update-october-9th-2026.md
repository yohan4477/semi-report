---
source: https://daily.semidoped.com/p/daily-update-october-9th-2026
title: Daily Update - October 9th, 2026
date: 2026-10-09
kind: clipping
genre: daily
audience: everyone
subtitle: OpenAI revenue near $50B vs. $100B+ assumptions hit CoreWeave -10%; GlobalFoundries signs $2B CoWoS interposer deal with TSMC; China commits $926M to Hua Hong; Kioxia LD4 QLC hits 30.72TB.
---
**Hello world, it’s Friday, October 9th.**

OpenAI’s annualized revenue is landing near $50 billion, well short of prior $100 billion-plus assumptions, dragging CoreWeave, Oracle, and Broadcom into a selloff. Elsewhere, TSMC and GlobalFoundries have signed a five-year, $2 billion deal for GlobalFoundries to supply silicon interposers for CoWoS advanced packaging out of its New York fabs, and Samsung has locked up roughly 80% of its 2027 memory output in long-term contracts with hyperscalers.

Let’s get into it. — _Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

#### Presented by Crusoe

Crusoe builds AI infrastructure from the ground up — power, data centers, and the cloud on top.

If you’re running open models — GLM, DeepSeek, Kimi, Qwen — Crusoe’s managed inference is fast: up to 9.9x faster time-to-first-token and 5x the throughput of vLLM, thanks to their MemoryAlloy caching layer and tokenizer fastokens. And it’s the easy kind of fast: pick a model, grab an API key and start inference. No GPUs to provision, no infrastructure or clusters to manage, and it’s pay per million tokens.

$5 in free credits to try it. [Send your first request today →](https://semidoped.com/crusoe-daily)

### OpenAI Revenue Miss Drags CoreWeave, Oracle, Broadcom Into Selloff

Bloomberg placed OpenAI’s [current annualized revenue near $50 billion](https://www.bloomberg.com/news/articles/2026-10-08/openai-s-annualized-revenue-nears-50-billion-ft-says), well short of the $100 billion-plus figures circulating in prior market assumptions, sending CoreWeave shares down roughly 10%, Oracle lower, and Broadcom dipping toward $350. The gap matters because GPU-cloud valuations had been priced against a faster monetization curve. Broadcom compounds the tension from its own angle: the company is [seeking more than $50 billion](https://ca.finance.yahoo.com/news/broadcom-seeks-more-50-billion-140200618.html) in financing to fund custom AI silicon for OpenAI, a capital raise that lands now in a market suddenly reassessing how much debt the AI infrastructure stack can carry.

> **Vik:** _So much discussion about what the ARR actually is, and when the turn around is coming. When it does, the drop is going to be a long way down._
> 
> **Austin:** _$35B closed for Anthropic in June, $60B more for Anthropic last week, and now $50B+ for OpenAI. That’s $145B+ of financing around two customers…_

### TSMC Signs GlobalFoundries to Five-Year CoWoS Interposer Deal

Under a [five-year, $2 billion supply agreement](https://www.reuters.com/world/asia-pacific/globalfoundries-make-key-ai-chip-component-tsmc-2026-10-08/), GlobalFoundries will manufacture silicon interposers for TSMC’s CoWoS advanced-packaging process at its fabrication facilities in New York. The interposer is the passive silicon layer that stitches together chiplets and high-bandwidth memory in AI accelerators, and TSMC has faced persistent capacity pressure on that component as CoWoS demand has surged. Producing them domestically at GlobalFoundries’ Malta, New York fabs addresses US-content requirements that have grown harder to ignore given CHIPS Act dynamics. GFS shares [jumped roughly 4%](https://www.streetinsider.com/General+News/TSMC+taps+GlobalFoundries+in+%242B+U.S.+chip+deal%3B+GFS+shares+jump+4%25/27164482.html) on the news. The arrangement effectively recruits a direct competitor into a supplier role, dedicating a slice of GlobalFoundries’ 300mm capacity to TSMC’s packaging roadmap through the end of the decade.

> **Vik:** _Note this is CoWoS-S only, the monolithic silicon interposer that runs into reticle limits. Open question is whether GF ever gets into CoWoS-L. Smart to hand the reticle-capped part to a subcontractor and keep the hard packaging in house. GF ramps in New York first half of 2028. US footprint box ticked too._
> 
> **Austin:** _GF has published papers mentioning silicon interposers and TSVs before, so clearly they have the know-how.[This paper](https://ieeexplore.ieee.org/document/10565181) used a 65nm process for the interposer._

### Samsung Locks Up 80% of 2027 Memory Output in Long-Term Deals

Samsung Electronics has [secured long-term supply commitments covering roughly 80% of its 2027 memory output](https://www.kedglobal.com/korean-chipmakers/newsView/ked202610090002), shifting the bulk of its DRAM and NAND allocation away from spot markets and into multi-year contracts with hyperscaler customers. The move follows a quarter in which Samsung posted [107.4 trillion won in operating profit](https://www.thelec.net/news/articleView.html?idxno=14487), its first result above 100 trillion won and a fourth consecutive record. That financial backdrop gives Samsung little reason to leave capacity uncommitted. Spot availability will tighten as a result, with a shrinking share of output reaching open-market buyers. The contracts cover production scheduled for next year, locking in pricing and volume well ahead of delivery.

> **Vik:** _If all the memory is already spoken for in LTAs, what is left for the spot market? The supply squeeze continues into 2028 for sure, possibly through the end of the decade._
> 
> **Austin:** _No wonder Lisa Su was in Seoul this week asking for three to five year plans. If ~80% of 2027 is already spoken for, what’s left for everyone who isn’t a hyperscaler?_

### China State Funds Pour $926M Into Hua Hong for Legacy Node Capacity

Chinese state funds have committed [$926 million to Hua Hong Semiconductor](https://www.scmp.com/tech/big-tech/article/3370297/china-state-funds-double-down-hua-hong-legacy-chip-push), backing an expansion of the foundry’s mature-node capacity as Beijing continues to funnel capital into the lower end of the process-node spectrum. Hua Hong, which operates fabs in Shanghai and Wuxi, serves as a key domestic supplier for analog, power management, and other legacy chips that Chinese device makers have historically sourced abroad. The injection doubles down on a strategy of shoring up that supply base with state backing rather than market financing alone. Separately from that vote of confidence, CXMT shares posted their [worst single-day decline since the memory maker’s July IPO](https://www.caixinglobal.com/2026-10-09/cxmt-shares-suffer-biggest-drop-since-july-ipo-102491581.html), a reminder that not every corner of Beijing’s chip build-out is running smoothly. The two moves sit inside the same broad push, but the capital flowing to Hua Hong carries none of CXMT’s price-discovery turbulence.

> **Vik:** _Not everything is AI related. There is still a major demand for legacy node chips for automotive, IoT, etc. China can lock up all this supply while western companies are laser focused on AI datacenters. All without EUV._

### Nvidia-Backed Firmus Scraps $5 Billion Australia IPO, Seeks Private Capital

Firmus, the Australian data-center operator backed by Nvidia, [scrapped its $5 billion IPO](https://www.reuters.com/world/asia-pacific/australian-nvidia-backed-ai-data-centre-operator-firmus-shelves-ipo-2026-10-08/) after demand cratered under investor scrutiny of AI infrastructure valuations. The company is now exploring a private funding round of as much as $3 billion to plug the financing gap left by the collapse. Public-market investors balked at the price, according to Bloomberg, with concerns about pure-play AI data-center operators drawing a valuation discount that the private route may sidestep. The fallout reaches beyond Firmus: Bloomberg reports the misfire has cast a shadow over a pipeline of comparable data-center listings, with DayOne’s $500 million bond talks also [caught in the turbulence](https://www.bloomberg.com/news/articles/2026-10-08/firmus-misfire-casts-shadow-on-data-center-ipos-in-the-pipeline).

> **Austin:** _Public markets blinked on a pure-play AI data center operator. Going private sidesteps price discovery, for now. Compute’s still short so the asset isn’t worthless - but every pulled listing like this feeds the crowd hunting for the peak._

### Kioxia Brings QLC Flash to E1.L Form Factor for AI Storage

Kioxia has announced the LD4, its [first E1.L QLC NVMe SSD built for hyperscale workloads](https://www.storagereview.com/news/kioxia-ld4-qlc-e1-l-ssd-1u-servers-30-72tb-122-88tb), currently sampling at 30.72TB with a roadmap extending to 122.88TB. The E1.L form factor fits two drives in a standard 1U server slot, making density the obvious pitch. QLC’s cost-per-terabyte advantage over TLC has long been offset by endurance concerns, but Kioxia is betting hyperscale read-heavy AI storage shifts that calculus in QLC’s favor. At the OCP Global Summit, the company is going to demo a [GPU-focused variant exceeding 20 million IOPS](https://xenospectrum.com/en/kioxia-gen3-gpu-ssd-demo/), targeting inference workloads where throughput competes with capacity for attention. Hyperscale qualifications haven’t closed yet, so the LD4’s commercial impact hinges on what those processes return.

> **Vik:** _I really think endurance can be amortized over an array of QLC drives by intelligently writing to them. We have discussed this idea with Val Bercovici from Weka on the Semi Doped podcast._

###  Sector Watch

#### Compute & AI Silicon

  * **Astera Labs** announces Aries 7, the industry’s first PCIe 7 signal-conditioning portfolio — smart retimers, redrivers, and cable modules, for copper and optics — targeting next-generation AI systems. ([Astera Labs](https://www.asteralabs.com/news/astera-labs-announces-aries-7-industrys-first-pcie-7-signal-conditioning-portfolio-across-copper-and-optical-interconnects/))

  * **Nvidia** invests in AI inference chip startup d-Matrix, choosing partnership over competition as rival silicon developers consolidate around the GPU leader. ([Breakingthenews.net](https://breakingthenews.net/Article/Nvidia-said-to-invest-in-chip-developer-d-Matrix/67263116))

  * Former **Groq** engineers sue the board over the $20B Nvidia acquisition, alleging the deal structured billions away from minority shareholders. ([Tom’s Hardware](https://www.tomshardware.com/tech-industry/semiconductors/former-groq-engineers-sue-board-over-usd20-billion-nvidia-deal-saying-it-handed-nvidia-the-lpu-and-the-team-that-built-it-plaintiffs-allege-the-board-kept-billions-from-other-shareholders))




#### Foundry & Packaging

  * **Applied Materials** and **Besi** expand their strategic packaging partnership to accelerate next-generation hybrid-bonding and advanced interconnect for AI scaling. ([DQ](https://www.dqindia.com/semiconductors/applied-materials-and-besi-expand-strategic-partnership-to-advance-next-gen-packaging-for-ai-scaling-12622576))

  * **Lam Research** ships its 15,000th semiconductor equipment chamber in South Korea, marking 15 years of cumulative manufacturing support for local fabs. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=14496))

  * **A*STAR** and **Synopsys** launch trial EDA licenses for advanced packaging design, opening Singapore’s research institutions to chiplet integration toolflows. ([Tech Wire Asia](https://techwireasia.com/2026/10/astar-synopsys-advanced-packaging-consortium-licence-terms/))




#### Optics & Networking

  * **Lumentum** (Nvidia-backed) reports opto-electronic component capacity sold out through 2029, **the most bullish supply timeline yet** disclosed for optical AI-interconnect parts. ([Bloomberg.com](https://www.bloomberg.com/news/articles/2026-10-09/nvidia-backed-lumentum-sees-opto-parts-capacity-sold-out-to-2029))

  * **FS** launches the D5130 Optical Circuit Switch for reconfigurable AI-factory networks, the company’s first OCS product targeting large-scale GPU interconnect. ([Business Wire](https://www.businesswire.com/news/home/20261008186405/en/FS-D5130-Optical-Circuit-Switch-Enables-Reconfigurable-Optical-Networks-for-AI-Factories))

  * **Arista Networks** unveils an ESUN-based rack-scale architecture expanding its open Ethernet AI-infrastructure portfolio for high-density GPU clusters. ([SDxCentral](https://www.sdxcentral.com/news/arista-networks-unleashes-esun-based-rack-scale-architecture-targeting-ai-infra/))




#### Power

  * **VEIR** raises $110M Series C to commercialize superconducting power-delivery cables purpose-built for AI data-center load densities. ([Business Wire](https://www.businesswire.com/news/home/20261008239548/en/VEIR-Raises-%24110-Million-Series-C-to-Accelerate-Commercialization-of-Superconducting-Power-Delivery-Technology-for-AI-Data-Centers))

  * South Korea’s **power semiconductor industry** launches a coordinated data-center efficiency research initiative targeting power supply improvements for AI infrastructure. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=14493))

  * **Atlas Atomics** , nuclear startup co-founded by Vivek Ramaswamy, raises capital at a $1.9 billion valuation to advance its small modular reactor program. ([Bloomberg Tech](https://www.bloomberg.com/news/articles/2026-10-08/vivek-ramaswamy-s-nuclear-startup-raises-at-1-9-billion-value))




#### Data Centers

  * **Micron Technology** commits up to $50M over five years to the White House Genesis Mission graduate fellowship and national-laboratory research program. ([Semiconductor Digest](https://www.semiconductor-digest.com/micron-plans-to-invest-up-to-50-million-to-support-genesis-mission-graduate-fellowship-and-national-laboratory-research/?utm_source=rss&utm_medium=rss&utm_campaign=micron-plans-to-invest-up-to-50-million-to-support-genesis-mission-graduate-fellowship-and-national-laboratory-research))

  * **DayOne Data Centers** enters preliminary talks with banks on a $500M bond offering, weeks after filing for a US IPO as a Singapore-headquartered operator. ([Bloomberg Tech](https://www.bloomberg.com/news/articles/2026-10-09/dayone-in-early-talks-with-banks-for-potential-500-million-bond))

  * **Claro Argentina** and **Oracle** agree to launch a locally operated hyperscale cloud, extending Oracle’s infrastructure footprint into South America. ([Telecompaper](https://www.telecompaper.com/news/claro-argentina-and-oracle-to-launch-locally-operated-hyperscale-cloud--1585070))




#### EDA

  * **Synopsys** seeks partnerships with Chinese AI labs to accelerate chip design workflows, a move carrying significant export-control implications for US EDA vendors. ([Nikkei Asia](https://asia.nikkei.com/business/tech/semiconductors/synopsys-looks-to-work-with-chinese-ai-labs-to-speed-up-chip-design))




#### Edge & Telecom

  * **Qualcomm** launches Snapdragon 8 Gen 6 at IMC 2026, with Motorola, Xiaomi, and iQOO confirming upcoming phones on the new agentic-AI mobile chip. ([BW Businessworld](https://www.businessworld.in/article/imc-2026-qualcomm-pushes-agentic-ai-onto-the-mobile-phone-with-snapdragon-8-gen-6-chips-627731))

  * **Telstra** activates the Perth-Sydney segment of its Aura Network backbone, pulling ahead on Australia’s national terrestrial fiber upgrade toward a 2028 finish. ([Light Reading](https://www.lightreading.com/cable-technology/telstra-activates-perth-sydney-route-aura-network-65-complete-ahead-of-2028-target))

  * **Arelion** and **Nokia** complete a live 500km Amsterdam-to-London field trial on Nokia’s open line system, validating expanded optical backbone spectrum capacity. ([Light Reading](https://www.lightreading.com/private-networks/arelion-partners-with-nokia-on-live-network-field-trial))




_Tell us how to make Semi Doped better![ Give us your feedback](http://semidoped.com/poll)! ❤️_

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-october-9th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
