---
source: https://daily.semidoped.com/p/daily-update-july-13th-2026
title: Daily Update - July 13th, 2026
date: 2026-07-13
kind: clipping
genre: daily
audience: everyone
subtitle: Memory supercycle update, money flows into packaging, and custom accelerators are redrawing the foundry map.
---
We’re trying out a new format for daily updates where we cluster news and spot directional trends instead of just adding takes on individual news items. We will have fewer but hopefully more measured takes that are focused on info density. Comment and let us know what you think.

Today, we touch up on the memory supercycle, advanced packaging buildout, and where custom silicon is going.

Let’s get into it. _— Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

### The memory supercycle is now a capital markets event

SK Hynix raised $26.5 billion in its Nasdaq debut, the largest US share sale by a foreign company, with ADRs opening at $170, 14% above the $149 offer price ([Quartz](https://qz.com/sk-hynix-nasdaq-adr-debut-stock-071026)). Seoul-listed shares have pulled back roughly 25% from their late-June record as investors booked profits, and the listing is widely framed as a test of the Korea discount ([TradingKey](https://www.tradingkey.com/analysis/stocks/more/262022878-sk-hynix-debuts-nasdaq-with-record-26-5b-offering-tradingkey)). Chairman Chey Tae-won said US investment plans will far exceed the $35 billion already committed ([CNBC](https://www.cnbc.com/2026/07/10/sk-hynix-skhy-stock-nasdaq.html)).

The capital is chasing a supply gap that keeps widening; supply is coming online, but demand is growing even faster. To keep up, Samsung pulled the first fab at its Yongin cluster forward to 2029, one to two years earlier than planned ([Korea Times](https://www.koreatimes.co.kr/business/companies/20260712/samsung-electronics-to-bring-forward-opening-of-1st-yongin-chip-plant-to-2029)). 

On pricing, HBM4 is expected to roughly double from about $2 per Gb in 2H26 to $4-5 in 2027, driven by Rubin demand, long-term agreements, and HBM consuming about 3x the wafer capacity of DDR5 ([digitimes](https://www.digitimes.com/news/a20260710PD216/hbm-2027-demand-hbm4-capacity.html), [Investing.com](https://www.investing.com/news/stock-market-news/hbm-prices-could-double-by-2027-on-surging-ai-demand-digitimes-reports-4786153)).

Memory bandwidth is the constraint in AI compute economics, and long-term contracts are converting a cyclical business into contracted revenue.

> _**Vik:** What the memory saga has taught us all is that LLMs are useful, but its requirement for memory is a fatal flaw, not a feature. There is simply no way that people are going to blindly keep adding RAM. They. will. make. tradeoffs. It can be in terms of acceptable latency, token throughput, or model quality. A new technique that is less memory hungry will flip the world over — but it does not exist yet. Or so I think._
> 
> _**Austin:** LLMs with significant memory/context is super useful, but blindly using expensive HBM or SRAM is the flaw imo. Hopefully this pushes for continued innovations to use cheaper flavors of DRAM and even use flash storage as a tier for KV Cache offloading, as well as algorithmic and KV cache compression improvements like sparse attention._

### Packaging is where the money is landing

TSMC’s June revenue hit NT$442.68 billion, up 67.9% from June 2025, taking first-half revenue to NT$2.4 trillion, up 35.6% YoY ([TSMC press release](https://pr.tsmc.com/english/news/3323)). Q2 came in around $39.6 billion, a 36% YoY rise that edged past guidance ahead of Thursday’s full report ([Bloomberg](https://www.bloomberg.com/news/articles/2026-07-13/tsmc-sales-surge-36-in-fresh-sign-of-ai-spending-momentum)).

The growth is pulling investment into packaging. 

  * TSMC is expanding the Chiayi Science Park into a dedicated packaging hub: two Phase I plants are in or entering mass production, and Phase II broke ground this weekend with additional fabs planned ([Reuters](https://finance.yahoo.com/technology/articles/tsmc-add-2-advanced-chip-034251078.html), [Focus Taiwan](https://focustaiwan.tw/business/202607120005)). 

  * Alongside the CoWoS ramp toward 200K wafers monthly in 2027, KYEC and JCET are each committing $1.4 billion to new fabs

  * ASE posted record Q2 revenue on AI packaging, and Liteon grew 37% YoY on AI server power ([digitimes](https://www.digitimes.com/news/a20260710PD202/revenue-demand-ai-server-2026-high-end.html)). 




Supply constraints are easing, but demand is strong enough to hold pricing power for packaging and test suppliers.

> _**Vik:** Although there is a lot of capital being deployed to packaging, I’d be really interested to see where Intel’s advanced packaging revenue lands next quarter. Earnings is reported on Thursday, July 23rd, and I know I’ll be listening in. There was also some news that TSMC’s panel level packaging for large substrates won’t use glass in the initial stages. This actually makes sense to me because there is a lot of trouble in handling glass to produce high yield. There is a learning curve to scale there for the industry._
> 
> _**Austin:** Amkor is a few days later on July 27th and is an OSAT moving into advanced packaging worth following._

### Custom silicon is redrawing the foundry map

**Meta’s** custom inference chip Iris enters production in September, fabbed at TSMC, targeting recommendation and ranking workloads across Facebook and Instagram as part of the MTIA program ([Lumien](https://lumienai.com/news/meta-iris-ai-chip-production-september-2026-mtia)).

**Samsung** landed an important win. A Samsung Foundry engineer disclosed on LinkedIn that Tesla’s AI5 has completed tape-out and will be produced on Samsung’s 2nm process at Taylor, Texas ([Korea Times](https://www.koreatimes.co.kr/business/tech-science/20260713/samsung-taylor-fab-enters-production-phase-for-teslas-ai5-chip)). Tesla splits AI5 between Samsung and TSMC, with Samsung reportedly taking AI6 and TSMC handling AI6.5 ([TrendForce](https://www.trendforce.com/news/2026/04/16/news-tesla-ai5-reportedly-uses-sk-hynix-memory-samsung-lpddr5x-samsung-sf2t-process-applied-ahead-of-ai6/)). Running AI5 on 2nm at Taylor implies Samsung’s 2nm yields have crossed the viability threshold, and a successful ramp is the recovery path for a foundry business still in the red ([Electrek](https://electrek.co/2026/07/13/samsung-taylor-fab-tesla-ai5-chip-2nm/)).

**Apple** is rebuilding its Mac silicon roadmap around AI: a base M6 later this year, no M6 Pro/Max/Ultra, an AI-focused M7 family through 2027-28 with the M7 Ultra supporting up to 1.5TB of memory for Apple’s AI servers, and an M8 on a 1.4nm process in 2028 ([Bloomberg](https://www.bloomberg.com/news/newsletters/2026-07-12/apple-s-chip-plans-m6-m7-pro-m7-max-m7-ultra-m8-details-touch-macbook-pro)). 

**Intel** , meanwhile, announced a €5 billion ($5.7B) investment at Leixlip, Ireland, upgrading existing fabs to expand Intel 3 output for Xeon 6 and next-gen Xeon ([Intel](https://newsroom.intel.com/intel-foundry/intel-invests-5-billion-euro-to-expand-manufacturing-in-europe), [Bloomberg](https://www.bloomberg.com/news/articles/2026-07-13/intel-invests-5-billion-in-irish-hub-to-keep-up-in-ai-chip-race)). With Magdeburg cancelled last year, Leixlip is Intel’s only leading-edge site outside the US and Israel.

> _**Austin:** Meta is a Samsung story too. Meta will be ramping rack scale MTIA 400 later this year, and MI450 is supposed to be only 6 months behind that. It was recently reported by the [Seoul Economic Daily](https://en.sedaily.com/finance/2026/07/03/samsung-foundry-emerges-as-ai-chip-powerhouse-wooing) that Meta is considering building MTIA with Samsung Foundry:_
> 
> _“Meta’s proprietary AI accelerator, the ‘MTIA,’ was produced by TSMC through its first and second generations, but the third generation unveiled this year has designated Samsung Foundry as its partner. In particular, the MTIA third generation is set to apply Samsung Foundry’s most advanced 2-nanometer process and be mass-produced on a scale of hundreds of thousands of units. A Samsung Electronics official said, “Nothing has been finalized yet.”_
> 
>  _TSMC capacity can only grow so fast. Samsung Foundry and Intel Foundry are picking up the excess. This isn’t bearish TSMC, but it’ll be interesting to see how it impacts future TSMC expansion plans. Although it could be tempting for TSMC to increase capacity as a competitive response, I don’t think they will, and I think that’s wise. Let Samsung and Intel rise up and offtake the excess demand. The hard questions: how much should TSMC’s capacity expand and how quickly? Well, quickly enough to retain customers, satisfy as much of their growth as possible, and maintain margins._
> 
> _Easier said than done._

## _K_ ey Data

zephyr_z9 on X has an excellent article that explains how there will be a 24% shortfall in DRAM supply even in 2030. He counts the various buildouts and how much capacity they are adding, and sizes that up against expected DRAM demand.

[](https://substackcdn.com/image/fetch/$s_!zb6i!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F34f02661-a6aa-4024-a404-2e7c9a6d033a_1448x1086.jpeg)

Read the whole post.

[Zephyr@zephyr_z9https://t.co/dAoQkZrPBS12:57 PM · Jul 13, 2026 · 58.7K Views

* * *

27 Replies · 27 Reposts · 164 Likes](https://x.com/zephyr_z9/status/2076652343307964879?s=20)

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-july-13th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
