---
source: https://daily.semidoped.com/p/daily-update-august-26th-2026
title: Daily Update - August 26th, 2026
date: 2026-08-26
kind: clipping
genre: daily
audience: everyone
subtitle: OpenAI Jalapeño ASIC outperforms Nvidia GB300, Meta MTIA 300 moves fabric on-chip, d-Matrix & SambaNova, YMTC targets Samsung NAND share by 2027 with $5B IPO, CXMT qualifies LPDDR6 for Xiaomi.
---
**Hello world, it’s Wednesday, August 26th.**

OpenAI brought its first custom inference chip, the Jalapeño, to Hot Chips 2026, claiming it beats the Nvidia GB300. Meta and Google were also at Hot Chips showing off the MTIA 300 and TPU v10, while SambaNova and d-Matrix presented memory-compute fusion work moving closer to production silicon. On the memory side, YMTC is gunning for Samsung and SK Hynix in NAND share by 2027, tied to a US$5 billion IPO from its parent company.

Let’s get into it. _— Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

_Tell us how to make Semi Doped better![ Give us your feedback](http://semidoped.com/poll)! ❤️_

### OpenAI Jalapeño ASIC Claims Performance Edge Over Nvidia GB300

OpenAI took its first custom inference chip, the Jalapeño, to [Hot Chips 2026](https://www.servethehome.com/openai-jalapeno-asic-at-hot-chips-2026/), where the company presented a deep-dive on an ASIC it built rapidly to compete directly with merchant silicon. OpenAI claims the Jalapeño beats the Nvidia GB300 on both performance-per-watt and inference speed, the two metrics data-center operators weight most heavily when choosing accelerators. The chip is designed to let OpenAI customers select models optimized for either lower cost or faster responses, according to Bloomberg. CNBC framed the debut as a fresh threat to Nvidia’s data-center gross margins as [custom silicon moves from roadmap to production hardware](https://openai.com/index/the-full-stack-behind-abundant-intelligence/). OpenAI attributed all performance figures itself; independent verification has not been published.

> _**Austin:** Vik and I just recorded a pod on this topic, will post within the next day or two. Incredible first at bat from OpenAI. Amazing example of how AI-enabled RTL design enables a small, talented team to punch way above its weight._
> 
> _Note that comparing the HBM4-equipped Jalapeño to HBM3E-era Nvidia Blackwell and AMD MI355X is a bit unfair; looking forward to the Vera Rubin and Helios comparisons._
> 
> _Also, although the talk emphasized the importance of a large KV cache and designing Jalapeño to minimize KV cache movement and HBM contention, the Jalapeño benchmarks used very small context (8K input sequence length, 1K output). Running SemiAnalysis’ AgentX multi-turn agentic coding benchmark with 1M sequence length with Jalapeño would be the gold standard._

### Meta MTIA 300 and Google TPU v10 Push Custom Silicon Into Distributed Training

Meta presented the MTIA 300 at Hot Chips 2026 with an architecture that [moves the network fabric onto the chip itself](https://www.servethehome.com/metas-mtia-custom-ai-silicon-at-hot-chips-2026/), a design choice that addresses where distributed training stalls at scale rather than simply adding more compute. The on-chip network integration is a direct response to the communication bottlenecks that emerge when thousands of accelerators coordinate gradient updates across a training cluster. Google’s TPU v10, meanwhile, goes multi-vendor for the first time, deepening [MediaTek’s role as an ASIC partner](https://www.digitimes.com/news/a20260826PD218/google-mediatek-tpu-supply-chain-design.html) in a supply arrangement that distributes production risk and expands Google’s fabrication options beyond a single source. Both programs were disclosed at the same Hot Chips 2026 conference, placing two of the largest ad-funded AI spenders on the same stage with silicon designed to reduce reliance on merchant GPU allocations.

> _**Austin:** MTIA 300 is a great example of Meta co-designing an AI accelerator for it’s own workloads, namely recommendation models, which is incredibly important for it’s core ads business. Yes, Meta Superintelligence Labs gets all the attention, and the rest of the MTIA roadmap better addresses GenAI workloads, but don’t forget what pays the bills (recommendation systems). I learned a lot on this topic from Meta VP Matt Steiner if you haven’t watched yet:_

### SambaNova and d-Matrix Show Memory-Compute Fusion Moving from Lab to Silicon

At Hot Chips 2026, SambaNova unveiled the SN50 with an architecture that [overlaps HBM access and compute](https://www.servethehome.com/sambanovas-sn50-rdu-for-ai-at-hot-chips-2026/sambanova-sn50-hot-chips-2026-hbm-and-compute-overlap/) to attack the bandwidth wall directly, while d-Matrix showed its Raptor card taking a more radical approach. D-Matrix bonds a TSMC 4nm compute die face-to-face onto a custom-designed DRAM die at a [36-micron pitch, delivering 100 TB/s of memory bandwidth per card](https://www.tomshardware.com/tech-industry/semiconductors/d-matrix-stacks-its-ai-accelerator-directly-on-custom-dram-for-100-tbs-per-card). That figure dwarfs what conventional HBM stacks connected via interposer can offer today. SambaNova’s method keeps a more traditional package geometry but schedules memory traffic to hide latency rather than brute-force it. Both presentations arrived as working silicon, not architecture studies, which puts concrete pressure on HBM suppliers and GPU memory subsystem vendors who have so far owned this tier of the market.

> _**Austin:**_****_Lots of hype for D-Matrix, catch up on them from Vik below. We should have them on the pod sometime, SambaNova too._
> 
> [ Vikram Sekar@vikramskr3D DRAM is a strong approach for inference architecture. I have covered d-Matrix in quite some detail on my Substack before... With all the heat from Hot Chips regarding the @dMatrix_AI talk, now might be a good time to read my earlier post. [open.substack.com/pub/viksnewsle…](https://open.substack.com/pub/viksnewsletter/p/d-matrix-in-memory-compute?r=222kot&utm_campaign=post-expanded-share&utm_medium=web)Gavin Baker @GavinSBakerEvery accelerator company, and I mean every accelerator company, is likely going to do some variant of 3D DRAM or the “zHBM” which were both discussed at HotChips today. The larger companies will probably run (are running) parallel programs, but these two memory variants4:46 AM · Aug 24, 2026 · 13.1K Views
> 
> * * *
> 
> 5 Replies · 9 Reposts · 85 Likes](https://x.com/vikramskr/status/2091748920703725995)

### YMTC Pushes for NAND Top Spot as CXMT Qualifies LPDDR6 for Xiaomi

YMTC has [set an explicit goal to surpass Samsung and SK Hynix in global NAND market share by 2027](https://www.digitimes.com/news/a20260826VL222/ymtc-nand-2027-ipo-shipments.html), a target timed to coincide with a US$5 billion IPO by its parent company. Barron’s notes that Micron and SK Hynix face unequal exposure to this pressure, with one better positioned to absorb the competitive hit. On the DRAM side, CXMT has [qualified LPDDR6 memory for Xiaomi’s flagship SoC](https://www.koreaherald.com/article/10852961), entering direct competition with SK Hynix for that supply contract.매일경제 reports CXMT is expected to cover 50% of Xiaomi’s DRAM demand. Domestic saturation is driving CXMT toward its production limits, per economy.ac, even as questions about proprietary process know-how complicate any broader global push.

### Sector Watch

#### Foundry & Packaging

  * **TSMC** packaging reallocation could boost AMD’s CoWoS share while trimming Nvidia’s allocation, per DigiTimes, with direct implications for H2 AI accelerator shipment mix. ([digitimes](https://www.digitimes.com/news/a20260826PD243/amd-cowos-tsmc-nvidia-demand.html))

  * **Powertech Technology** targets FOPLP mass production by mid-2027, marking a concrete timeline for fan-out panel-level packaging at volume scale. ([Taiwan News](https://www.taiwannews.com.tw/en/news/6428264))

  * **Nordson Electronics Solutions** launches the ASYMTEK Vantage XL fluid dispensing system for panel-level packaging, debuting at SEMICON Taiwan 2026. ([Nordson](https://www.eagletribune.com/region/nordson-electronics-solutions-launches-the-new-asymtek-vantage-xl-fluid-dispensing-system-for-panel-level/article_1fc52f2c-df64-5a7c-b907-338eddebcadc.html))




#### Memory

  * **Micron** announces leadership appointments aimed at accelerating innovation and growth, signaling internal reorganization ahead of next HBM and DRAM product cycles. ([Micron Investor Relations](https://investors.micron.com/news/press-release/2026/Micron-Announces-Leadership-Appointments-to-Accelerate-Innovation-and-Growth/default.aspx))

  * **SIMMTECH** announces a dedicated SOCAMM module plant in Ochang, committing capacity to the next-generation AI memory module standard ahead of anticipated hyperscaler demand. ([thelec.net](https://www.thelec.net/news/articleView.html?idxno=13335))

  * **XCENA** details its MX1 architecture integrating memory expansion and near-memory computing at Hot Chips 2026, targeting inference bandwidth constraints. ([Business Wire](https://www.businesswire.com/news/home/20260825275952/en/XCENA-Details-MX1-Architecture-Integrating-Memory-Expansion-and-Near-Memory-Computing-at-Hot-Chips-2026))




#### Policy & Trade

  * **Taiwan** indicts nine people, including staff from Nvidia and Super Micro, over alleged illegal exports of AI servers to China. ([TechRepublic](https://www.techrepublic.com/article/news-taiwan-nvidia-supermicro-ai-server-smuggling-china-apac/))

  * **Huawei** submits a formal proposal to Egypt to build AI data centers for military and public-sector use, prompting US officials to weigh a counter-offer. ([Bloomberg.com](https://www.bloomberg.com/news/articles/2026-08-26/huawei-egypt-ai-ascend-chips-test-us-tech-diplomacy-nvidia-amd-microsoft))

  * **Naura** reports 25% revenue growth but sees margins squeezed by rising R&D spending, as China’s domestic equipment buildout intensifies. ([digitimes](https://www.digitimes.com/news/a20260826VL215/naura-technology-ic-manufacturing-equipment-growth-revenue-profit.html))




#### Compute & Edge

  * **Nvidia** announces Jetson Orin Nano 2, a new entry-level edge AI robotics computer targeting cost-sensitive physical-AI deployments. ([Nvidia News](https://nvidianews.nvidia.com/news/nvidia-announces-jetson-orin-nano-2-robotics-computer-to-redefine-entry-level-edge-ai))

  * **AMD** presents Versal Premium Gen2 at Hot Chips 2026, targeting edge and physical AI use cases with an updated adaptive SoC architecture. ([ServeTheHome](https://www.servethehome.com/amd-versal-premium-gen2-at-hot-chips-2026/))

  * **SpaceXAI** will deploy Nvidia chips in its orbital AI data center program, with significant-scale operations targeted for 2028. ([Light Reading](https://www.lightreading.com/satellite/with-nvidia-on-board-spacex-orbital-data-centers-to-hit-significant-scale-in-2028))




#### Optics & Networking

  * **Advantest** launches an integrated test cell for high-volume silicon photonics production, targeting AI optical interconnect manufacturing scale-up. ([thelec.net](https://www.thelec.net/news/articleView.html?idxno=13353))

  * **Fujikura** raises its full-year earnings forecast for the second time, citing accelerating AI-driven demand for optical fiber and interconnect products. ([Fujikura](https://www.ad-hoc-news.de/boerse/news/unternehmensnachrichten/fujikura-s-ai-fiber-engine-revs-higher-as-forecasts-get-a-second-major/70000375))

  * **FST** adds a Canatu CNT reactor to expand pellicle production capacity, supporting EUV photomask supply for leading-edge nodes. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13332))




#### PCB & Components

  * **Samsung** and **LG Innotek** are accelerating FC-BGA substrate production to address an AI-driven supply shortage, per Chosunbiz reporting. ([조선일보](https://www.chosun.com/english/industry-en/2026/08/26/XGBNER6IO5BGJIVE5BMVVHMPKM/))

  * **MLCC** global inventories have dropped to record lows as AI server demand surges, triggering supply tightness for the component dubbed the rice of electronics. ([SCMP](https://www.scmp.com/tech/tech-trends/article/3365353/ai-server-boom-fuels-record-supply-crunch-rice-electronics?utm_source=rss_feed))

  * **SIMMTECH** announces a dedicated SOCAMM module plant in Ochang to build capacity for the next-generation AI memory module standard ahead of hyperscaler demand. ([Chosunbiz](https://biz.chosun.com/en/en-finance/2026/08/26/GISMSBG5E5DCHD4EW4SJE5NQQY/?outputType=amp))




#### Data Centers

  * **Google** breaks ground on a $2 billion data center and cloud region in Malaysia, its largest infrastructure commitment in the country. ([blog.google](https://blog.google/intl/ms-my/company-news/inside-google/2024_10_google-breaks-ground-on-us2-billion/))

  * **Nscale** closes $790 million in project financing for its Norway data center, one of the largest such raises for a European AI infrastructure facility. ([Legal Desire](https://legaldesire.com/latham-advises-on-nscales-us790-million-norway-data-center-financing/))

  * **Emerald AI** raises $150 million Series A at a $1.05 billion valuation to scale power-flexible AI data centers across the United States. ([Business Wire](https://www.businesswire.com/news/home/20260825127649/en/Emerald-AI-Raises-%24150-Million-Series-A-at-%241.05-Billion-Valuation-to-Scale-Power-Flexible-AI-Data-Centers))




#### Earnings & EDA

  * **Photronics** reported Q3 fiscal 2026 results for the quarter ended August 2, 2026. ([Photronics](https://photronicsinc.gcs-web.com/news-releases/news-release-details/photronics-reports-third-quarter-2026-results))

  * **Alchip Technologies** reports Q2 2026 financial results, providing a read on ASIC design-services demand from hyperscaler custom silicon programs. ([The Manila Times](https://www.manilatimes.net/2026/08/26/tmt-newswire/globenewswire/alchip-technologies-reports-2026-second-quarter-financial-results/2412638))

  * **Monolithic Power Systems** tops Q2 earnings consensus, with results reinforcing strong AI power-management demand and raising full-year targets. ([StockStory](https://stockstory.org/us/stocks/nasdaq/mpwr/news/earnings/q2-analog-semiconductors-earnings-review-first-prize-goes-to-monolithic-power-systems-nasdaqmpwr))




_Tell us how to make Semi Doped better![ Give us your feedback](http://semidoped.com/poll)! ❤️_

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-august-26th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
