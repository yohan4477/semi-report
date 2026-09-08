---
source: https://daily.semidoped.com/p/daily-update-may-14th-2026
title: Daily Update - May 14th, 2026
date: 2026-05-14
kind: clipping
genre: daily
audience: everyone
subtitle: Cerebras IPO, OpenAI-MRC, Samsung Strike, TSEM results, Wolfspeed SiC, plus a special story about Trilogy Systems -- the Cerebras of the 1980s.
---
The much awaited Cerebras IPO is here, and is priced at $185/share. Trading begins today. Also in this daily update, we see why Ethernet is winning on frontier training, why Samsung employees have stopped working, how Tower Semi is posting monstrous results, and the revival of Wolfspeed.

Plus, **a special story dedicated to Trilogy Systems** — who wanted to be where Cerebras is today, but were hit by the curse of the Pharoahs.

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

* * *

### Cerebras Systems announces IPO

The much sought after IPO is here, and is priced even higher than some earlier estimates. [Cerebras Systems priced its initial public offering](https://www.cerebras.ai/press-release/cerebras-systems-announces-pricing-of-initial-public-offering) at $185 per share on the evening of May 13, 2026, significantly above its revised range of $150-$160. The AI accelerator company sold 30 million shares to raise $5.55B, implying a market capitalization of approximately $39.8B and a fully diluted valuation of over $56B. The offering, which was reportedly >20x oversubscribed, will see shares begin trading on the Nasdaq on May 14 under the ticker “CBRS”. As [Bloomberg](https://www.bloomberg.com/news/articles/2026-05-13/arm-softbank-said-to-have-tried-to-buy-cerebras-in-11th-hour') reports, Arm and Softbank made 11th hour bids to buy Cerebras, in a classic eBay style snipe that did not work.

Don’t miss the Trilogy Systems story at the end of this post — its a story worth knowing.

### Tower Semiconductor Posts Massive Results

[TSEM 0.00%↑](https://substack.com/search/%24TSEM) guided Q2 2026 to be the highest revenue quarter in company history ($455M mid-range), significantly exceeding historical levels. This 22% YoY projected growth, paired with a commitment to sequential revenue and margin expansion throughout 2026, signals a major inflection point in scaling operations and profitability.

Tower also announced $1.3B contractual commitments for 2027, which is a massive jump from $230M in 2025, with unprecedented visibility. There is $290M of cash prepayments, which derisks future expansion and confirms Tower’s leadership in the optical interconnect market. 

> _**Vik** : Tower is in a strong position in the optical interconnect market. This is an amazing turnaround in the AI era for them. For years, they have made do with being a “specialty analog foundry” but when optics showed up, they snatched the opportunity right up! Kudos!_
> 
> _**Austin:** NEVER FORGET INTEL TRIED TO BUY TOWER! See this [Feb 2022 Intel Press Release.](https://www.intc.com/news-events/press-releases/detail/1527/intel-to-acquire-tower-semiconductor-for-5-4-billion) Imagine if Tower was part of Intel Foundry right now!_

### OpenAI ships MRC: Ethernet winning on frontier training

OpenAI [published](https://www.opencompute.org/documents/ocp-mrc-1-0-pdf) the design behind **MRC (Multipath Reliable Connection)** , a new RDMA transport protocol co-developed with AMD, Broadcom, Intel, Microsoft, and NVIDIA, and released through the Open Compute Project ([OpenAI](https://openai.com/index/mrc-supercomputer-networking/)). MRC is built into 800Gb/s NICs and targets tail latency under failure, not peak bandwidth.

MRC sprays a single transfer across hundreds of paths (”packet spraying”) instead of pinning flows to one route, pairs with multi-plane Clos topologies for 100K+ GPU scaling, and replaces dynamic routing with static source routing via SRv6 — the transport layer owns resilience instead of the fabric. MRC is already in production across OpenAI’s largest Microsoft training clusters and is the networking foundation for the Stargate cluster in Abilene, Texas, on Oracle Cloud Infrastructure.

[](https://substackcdn.com/image/fetch/$s_!QXK4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd87caa9e-06fe-4844-aa38-337acb738968_802x435.svg)

[](https://substackcdn.com/image/fetch/$s_!ML8l!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe7325514-9bee-4c13-ba64-a6482abcc50e_808x393.svg)

> _**Austin:**_****_The[MRC paper](https://cdn.openai.com/pdf/resilient-ai-supercomputer-networking-using-mrc-and-srv6.pdf) mentions that the NIC/DPUs are the star of the show:  
>   
> “We implemented MRC in 400 and 800Gb/s RDMA NICs: NVIDIA ConnectX-8, AMD Pollara and Vulcano, and Broadcom Thor Ultra. We also implemented support for SRv6 in NVIDIA Spectrum-4 and 5 switches running both Cumulus and SONiC, and collaborated with Arista to implement it in EOS on Broadcom Tomahawk 5 switches. MRC is in large-scale production use in multiple very large AI training clusters, where it has been used to train frontier large language models (LLMs) for ChatGPT and Codex._
> 
> _Training has already been moving from Infiniband toward Ethernet, and now it seems the important silicon isn’t simply the switch but increasingly the DPU._
> 
> _**Vik:** DPUs / NICs are interesting because they straddle the line between networking and compute. They are critical to tying massive compute clusters together, and are often the unsung heros of the AI expansion._

### Samsung chip workers threaten 18-day strike over AI windfall bonuses

Samsung’s chip-division union is reportedly preparing for an **18-day strike** over AI windfall bonuses and annual payouts after pay-deal talks broke down ([Bloomberg](https://www.bloomberg.com/news/articles/2026-05-12/samsung-fails-to-reach-labor-deal-yonhap-says-as-strike-looms)). The union is demanding a share of memory-cycle profits, which printed up **~48x year-over-year** in Q1. SK hynix’s union is reportedly considering parallel action.

> _**Austin:**_****_The union wants management to allocate 15% of its operating profit to worker bonuses. That would truly be an incentive alignment between employees and employer. Now is obviously the right time for unions to make demands — Samsung can’t afford to miss a single day of memory production._
> 
> _**Vik:** Seems fair for the workers to want a piece of the AI upside I guess. But I know nothing about worker unions, corporations, let alone in South Korea. But hey, I agree, 18-days of not making memory affects the company and workers alike._

### Wolfspeed Garners Analyst Upgrades on SiC Strategy

Following positive investor signals regarding its silicon carbide (SiC) strategy for AI and industrial power markets, [WOLF 0.00%↑](https://substack.com/search/%24WOLF) saw upward revisions of 90% in price targets as analysts gained confidence in the company’s long-term growth and restructuring efforts. Stock to a new 52-week high on May 12.

> _**Vik:** The positive analyst revisions suggest growing conviction in Wolfspeed’s SiC pure-play strategy, particularly its leverage to the power-hungry AI datacenter market. This is a turnaround from a company that was in serious financial trouble up until recently._
> 
> _**Austin:** I can’t find a pulse…. oh wait…. its alive!_
> 
> [](https://substackcdn.com/image/fetch/$s_!8qJJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe302b719-6996-43c2-87f6-f7fba5ccd1b3_1134x934.png)

### Quick Hits

  * **[Google’s Googlebook](https://googlebook.google/)** sounds amazing, and **[Qualcomm](https://x.com/Qualcomm/status/2054547344020918503?s=20)**[ seems to have something to do with it](https://x.com/Qualcomm/status/2054547344020918503?s=20) (Snapdragon?).



  * **Micron samples 256GB DDR5 RDIMM** on 1-gamma DRAM at 9,200 MT/s, 40%+ faster and 40%+ more power-efficient than current production modules ([Micron IR](https://investors.micron.com/news-releases/news-release-details/micron-redefines-ai-performance-sampling-256gb-ddr5-server)). Highest-capacity DRAM module yet for AI training and HPC servers.

  * **TSMC posts third 2026 monthly revenue record** — April revenue +22.4% YoY. Analyst @lithos_graphein argues TSMC is converting AI demand into margin, not volume — pricing over capacity addition, the Morris Chang playbook running unchanged ([@lithos_graphein](https://x.com/lithos_graphein/status/2054203064878350739) on X).

  * **TSMC board approves ~$31.3B capex appropriation plus a $20B Arizona top-up** at the May 12 meeting ([TSMC](https://pr.tsmc.com/english/news/3311)). The Arizona injection materially deepens TSMC’s US footprint for AI accelerator customers.

  * **AMAT EPIC Center** in Silicon Valley names TSMC inaugural foundry partner with ASU, RPI, Stanford as university partners ([Semiconductor Today](https://semiconductor-today.com/news_items/2026/may/appliedmaterials-tsmc-120526.shtml)). AMAT reports Thursday.

  * **Veeco** booked $250M+ in InP-laser tool orders for 800G/1.6T transceiver capacity ramping 2027 ([Semiconductor Today](https://semiconductor-today.com/news_items/2026/may/veeco-060526.shtml)).

  * **Half-wavelength-pitch optical phased arrays land in Nature.** New silicon-photonics grating antenna design cuts inter-antenna coupling from 100% to 1%, enabling the first wide-field-of-view, grating-lobe-free integrated OPA ([Nature Communications](https://www.nature.com/articles/s41467-026-71832-y)). Removes a fundamental FOV limit on chip-scale beam steering for LiDAR, free-space optical interconnects, and CPO.




### TIL: The Cursed Story of Trilogy Systems — the Cerebras of the 1980s

The story of Trilogy Systems is a tech-noir saga for Silicon Valley. In 1980, Gene Amdahl raised a record-breaking $230 million - nearly $880 million in 2026 money - to build a computer on a single 2.5-inch silicon wafer. The ambition was way ahead of its time. They wanted to route around defects just like Cerebras does today. But the yields on 2.5” wafers in the ‘80s were just simply too low. The manufacturing processes were simply not good enough to solve yield at wafer scale.

Then, started the curse of the Pharoahs. The 1982 Pineapple Express storms flooded their $33 million factory; water seeped into the air-conditioning bearings, causing them to rust and blow microscopic dust into the cleanroom - a sabotage by nature that took months to diagnose. Desperately burning through capital while trying to fix this contamination, Trilogy launched a hail Mary IPO in 1983, raising an additional $60 million without a product in hand. However, as months passed without a working wafer, the public market panicked. The stock, which debuted at $12 per share, plummeted to just $2.44 by mid-1984.

The human toll felt equally hexed. Amdahl was sidelined by the legal and emotional fallout of a fatal accident involving his forest-green Rolls Royce, while the company’s finance and administrative guy, Clifford Madden, died of a brain tumor at the height of the crisis. In June 1984, facing a completely depleted runway, Amdahl announced a brutal restructuring, laying off roughly 15% of the workforce to slow the bleeding.

In July 1984, they abandoned[ ](https://en.wikipedia.org/wiki/Trilogy_Systems)the dream of building an IBM-compatible supercomputer. By late 1984, Trilogy had vaporized its mountain of cash without shipping a single product. They cratered and took down the product roadmaps of giants like DEC and Sperry, who had staked their futures on Trilogy’s success. With wafer-scale technology dead, the company sold off its advanced cooling components to salvage capital. Amdahl then used Trilogy’s remaining $70 million in cash reserves to acquire minicomputer startup Elxsi, pivoting the business into a financial shell. However, the merged entity failed to achieve profitability, prompting a defeated Amdahl to officially step down and exit the company in 1989.

While modern firms like Cerebras (IPO pricing) have finally realized the wafer-scale dream, Trilogy remains the ultimate warning that even a genius cannot force the future into existence before the manufacturing yields - and the stars - align.

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-may-14th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
