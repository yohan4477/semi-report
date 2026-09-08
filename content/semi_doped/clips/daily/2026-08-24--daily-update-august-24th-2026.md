---
source: https://daily.semidoped.com/p/daily-update-august-24th-2026
title: Daily Update - August 24th, 2026
date: 2026-08-24
kind: clipping
genre: daily
audience: everyone
subtitle: Cerebras CS-4 and d-Matrix Raptor target GPU clusters at Hot Chips 2026, Xiaomi Xring O3 hits TSMC 3nm with LPDDR6, Infineon buys C2i Semiconductors, Amazon raises hardware prices up to 60%.
---
**Hello world, it’s Monday, August 24th.**

Cerebras and d-Matrix both took the stage at Hot Chips 2026 to pitch purpose-built inference chips as direct replacements for GPU clusters, with Cerebras claiming its CS-4 runs AI inference 30x faster than GPUs. Xiaomi’s Xring O3 landed on TSMC’s 3nm process as the first mobile chip with LPDDR6 support, Samsung approved a record 90-to-110-trillion-won shareholder return that somehow sent its shares lower, Infineon snapped up Bangalore AI power startup C2i Semiconductors, and Amazon raised prices on Echo, Fire TV, Kindle, and eero hardware by up to 60%, blaming memory costs.

Let’s get into it. _— Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

_Tell us how to make Semi Doped better![ Give us your feedback](http://semidoped.com/poll)! ❤️_

### Cerebras CS-4 and d-Matrix Raptor Challenge GPU Clusters at Hot Chips 2026

Back-to-back disclosures at Hot Chips 2026 put two purpose-built inference chips in direct competition with GPU clusters for production deployment. Cerebras unveiled the CS-4, claiming [30x faster AI inference than GPUs](https://tech-insider.org/cerebras-cs-4-ai-accelerator-launch-2026/) on the same wafer-scale architecture that defined its earlier systems, with the company saying internal benchmarks show double the performance of the CS-3 on identical silicon. d-Matrix’s Raptor, meanwhile, recorded 105 TB/s of memory bandwidth in real-silicon testing using [1Hi 32GB 3D-DRAM stacks](https://www.servethehome.com/meta-3d-dram-based-accelerator-for-genai-slide-12/), enough capacity to fit frontier large language models inside a single Raptor rack. XenoSpectrum notes that d-Matrix positions the 3D-DRAM as a complement to HBM rather than a replacement. Both announcements arrived at the same conference, letting the hardware speak for itself.

> _**Vik:** We saw Cerebras announce CS-4 at their SuperNova event just before Hot Chips. It’s just same chip from before but with three WSEs in one rack compared to two earlier. d-Matrix showed promising results on 3D-DRAM tech, and it is very promising indeed. The company is generating a lot of excitement on X. I have covered this company on my newsletter before → [read it here](https://open.substack.com/pub/viksnewsletter/p/d-matrix-in-memory-compute?r=89umme&utm_campaign=post-expanded-share&utm_medium=web)._

### Amazon Pins Hardware Price Hikes Up to 60% on Memory Cost Surge

Amazon has [raised prices across its Echo, Fire TV, Kindle, and eero lineups by as much as 60%](https://www.techspot.com/news/113584-amazon-raises-echo-kindle-fire-tv-eero-prices.html), citing what it calls “significant increases” in memory costs. The move covers the company’s entire consumer hardware portfolio, touching everything from entry-level Kindles to mesh Wi-Fi systems. It isn’t subtle: some products cost well over half again what they did before. The hikes land against a backdrop of broad silicon wafer price inflation driven by what analysts are calling “chipflation,” with costs rising across wafer sizes industry-wide. Micron, for its part, [presented evolving memory packaging architectures at Hot Chips 2026](https://www.servethehome.com/micron-evolving-memory-architectures-for-ai-at-hot-chips-2026/) aimed at AI workloads, a roadmap that speaks to where memory investment is flowing. Consumers, it turns out, are covering some of that tab now.

> _**Vik:** At Hot Chips, where I am writing this from, there was a lot of talk that we won’t continue to see memory makers charge like crazy. This cycle is due to change, and soon. There are people looking at alternative architectures. In any case, you can read my free report on memory from the big-3 at Hot Chips. [Read it here](https://www.viksnewsletter.com/p/hot-chips-2026-tuning-into-memory)._

### Samsung’s Record Return Plan Sends Shares Skidding as Exynos Benchmarks Impress

Samsung Electronics’ board approved a [shareholder return plan of 90 trillion to 110 trillion won](https://www.thelec.net/news/articleView.html?idxno=13262) for 2026, the largest such commitment ever by a Korean company, yet the announcement triggered a sell-off rather than a rally. Seoul stocks closed over 3% lower on the news, with investors apparently unconvinced the cash will materialize given the company’s recent execution struggles. Samsung’s internally run benchmarks claim the Exynos 2700 outperforms Qualcomm’s forthcoming Snapdragon 8 Elite Gen 6 Pro, according to Seoul Economic Daily. Qualcomm’s stock held steady on the claim, which has not been independently verified. At Hot Chips 2026, Samsung separately [presented plans to evolve the HBM base die](https://www.servethehome.com/samsung-evolving-hbm-base-die-at-hot-chips-2026/) to free up package area for more efficient compute.

> _**Austin:** Samsung’s zHBM is a hot topic too_
> 
> [](https://substackcdn.com/image/fetch/$s_!hGrH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c4ee497-06eb-43f7-a9c4-042f572a18dc_800x450.jpeg)
> 
> [Gavin Baker@GavinSBakerEvery accelerator company, and I mean every accelerator company, is likely going to do some variant of 3D DRAM or the “zHBM” which were both discussed at HotChips today. The larger companies will probably run (are running) parallel programs, but these two memory variants8:08 PM · Aug 23, 2026 · 286K Views
> 
> * * *
> 
> 101 Replies · 103 Reposts · 1.76K Likes](https://x.com/GavinSBaker/status/2091618684603105717)

### Infineon Acquires Bangalore AI Power Firm C2i Semiconductors

Infineon Technologies has [acquired C2i Semiconductors](https://www.prnewswire.com/in/news-releases/infineon-acquires-c2i-semiconductors-to-expand-its-innovation-capabilities-in-ai-data-center-power-management-solutions-302858343.html), a Bangalore-based startup specializing in AI data-center power management, to extend its position in high-density GPU rack power delivery. The deal adds C2i’s engineering team and intellectual property directly into Infineon’s power systems portfolio. Infineon stock held above €56 following the announcement, with the company issuing [record Q3 2026 guidance](https://www.ad-hoc-news.de/boerse/news/corporate-news/infineon-stock-holds-above-56-on-record-q3-guidance/69991346) alongside the deal disclosure. C2i’s focus on granular power management for AI accelerator clusters fits a supply chain increasingly strained by rack densities that conventional voltage regulator architectures weren’t designed to handle. Terms of the acquisition were not disclosed.

> _**Vik:** C2i seems to have IP on substrate integrated voltage regulators (SIVRs). That would fit nicely into Infineon’s power portfolio I would say._

### Xiaomi Xring O3 Arrives on TSMC 3nm, Squeezing Qualcomm and MediaTek

Xiaomi’s Xring O3 is [fabbed at TSMC on a 3nm process](https://www.reuters.com/world/china/xiaomi-launches-new-xring-chip-partners-with-tsmc-production-sources-say-2026-08-24/) and carries the distinction of being the world’s first mobile chip to support LPDDR6 memory, according to Huawei Central. The chip posted an AnTuTu score [above 5.2 million](https://nokiapoweruser.com/xiaomi-xring-o3-chip-specs-benchmarks/), a figure that puts it ahead of Apple’s A19 Pro on latency by that benchmark’s measure. Xiaomi plans to ship the Xring O3 inside the Xiaomi 18 Fold in September, giving the chip its commercial debut in the premium foldable segment where Qualcomm and MediaTek currently hold the floor. 

### Sector Watch

#### Compute & AI Silicon

  * **Intel** outlines three agentic AI architectures at Hot Chips 2026 combining Diamond Rapids processor, Crescent Island GPU, and Wildcat Lake SoC for enterprise-scale workloads. ([Intel Newsroom](https://newsroom.intel.com/client-computing/intel-outlines-architectures-for-agentic-ai-at-hot-chips-2026))

  * **IBM** unveils a next-generation dual-architecture processor for IBM Z and LinuxONE, bringing Arm-native application support to flagship mainframes. ([IBM](https://newsroom.ibm.com/2026-08-24-ibm-unveils-next-generation-dual-architecture-processor-for-ibm-z-and-linuxone))

  * **Anthropic** hires Amir Salek, founder of Google’s TPU program, as it accelerates a push into custom in-house AI silicon. ([Business Standard](https://www.business-standard.com/technology/tech-news/anthropic-taps-google-chip-veteran-amir-salek-as-part-of-push-into-hardware-126082200097_1.html))




#### Foundry & Packaging

  * **Absolics** (SKC subsidiary) launches a 400 billion won rights issue to fund its glass substrate business expansion. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13254))

  * **Socionext** advances SoC development on Intel 18A-P process, marking a new external customer commitment to Intel’s leading-edge node. ([Bisinfotech](https://www.bisinfotech.com/socionext-advances-soc-development-with-intel-18a-p/))

  * **Kools** unveils SPEA bottom-up plating technology for through-glass vias, targeting next-generation glass-substrate advanced packaging. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13257))




#### Memory

  * **YMTC** parent CCSH files for a $4.9 billion STAR Market IPO,. ([Reuters](https://www.reuters.com/world/asia-pacific/chinese-flash-memory-chipmaker-ymtc-plans-raise-49-billion-shanghai-ipo-2026-08-21/))

  * **CXMT** relied on leaked Samsung technology to skip years of DRAM R&D, court testimony claims, deepening IP concerns around China’s memory expansion. ([TechSpot](https://www.techspot.com/news/113568-chinese-memory-firm-cxmt-relied-leaked-samsung-technology.html))

  * **LG Innotek** pivots its business toward AI substrates as its primary growth engine, flagging potential for operating profit to exceed 1 trillion won this year. ([매일경제](https://www.mk.co.kr/en/business/12135234))




#### Optics & Networking

  * **Quintessent** raises $40 million Series A and begins sampling its first product for AI optical interconnects. ([Business Wire](https://www.businesswire.com/news/home/20260824525357/en/Quintessent-Raises-%2440-Million-Series-A-and-Begins-Sampling-First-Product-for-AI-Optical-Interconnects))

  * **Innolight** reports H1 2026 net profit surging 2.4 times to 13 billion yuan, driven by surging overseas demand for optical transceivers. ([The Standard (HK)](https://www.thestandard.com.hk/finance/article/340637/Zhongji-Innolights-H1-2026-net-profit-surges-24-times-to-13-bln-yuan-on-growing-overseas-demand))

  * **Zayo** signs a long-term fiber supply agreement with Corning to secure capacity for AI network expansion. ([ET Datacenters](https://datacenters.economictimes.indiatimes.com/news/cloud-colocation-connectivity/zayo-secures-corning-fiber-capacity-for-ai-network-expansion/133416566))




#### Power & Energy

  * **GE Vernova** introduces a medium-voltage UPS system purpose-built for AI factories and energy-intensive industries, and wins a new AI data center power contract. ([GE Vernova](https://www.ad-hoc-news.de/boerse/news/corporate-news/ge-vernova-stock-holds-firm-after-a-new-ai-data-center-contract/69993256))

  * **IBM** and Together AI sign a $240 million multi-year deal to deploy a large-scale Nvidia B300 AI inference cluster. ([Pulse 2.0](https://pulse2.com/ibm-and-together-ai-sign-240-million-multi-year-deal-for-large-scale-nvidia-b300-ai-inference-cluster/))

  * **Wiwynn** announces a $275 million investment to build a second server manufacturing factory in Socorro, Texas, targeting 2,000 total jobs by 2027. ([Connect CRE](https://www.connectcre.com/stories/ai-supplier-building-275m-el-paso-area-factory/))




#### Data Centers

  * **Nscale** targets a $3 billion US IPO as the AI-focused data center builder looks to capitalize on surging GPU cloud demand. ([NAI500](https://nai500.com/blog/2026/08/ai-data-center-newcomer-nscale-eyes-u-s-stock-market-aims-to-raise-3-billion/))

  * **Nebius** raises $5 billion via a pair of upsized convertible bonds to fund its AI infrastructure expansion. ([Global Capital](https://www.globalcapital.com/article/2gsito4mrkjj5pw2d6134/equity/nebius-raises-5bn-with-pair-of-upsized-convertible-bonds))

  * **Meta** has emerged as one of Microsoft Azure’s largest AI customers, with a multi-million-dollar cloud infrastructure agreement now confirmed. ([Bloomberg Tech](https://www.bloomberg.com/news/newsletters/2026-08-24/microsoft-ai-business-is-concentrated-with-openai-tiktok-meta))




#### Policy & Trade

  * **ASML** and Tata sign an MoU to strengthen India’s semiconductor ecosystem, with Prime Minister Modi calling it a significant step for domestic chip ambitions. ([News On AIR](https://newsonair.gov.in/asml-tata-mou-marks-significant-step-in-strengthening-indias-semiconductor-ecosystem-pm-modi/))

  * **MediaTek** wins Google’s next TPU silicon contract on three competitive strengths, per DigiTimes, deepening the Taiwan fabless firm’s hyperscaler ASIC footprint. ([digitimes](https://www.digitimes.com/news/a20260821PD220/taiwan-mediatek-ic-design-revenue-2026.html))

  * **Nexperia** ‘s China unit announces a full pivot to domestic 12-inch silicon wafers, targeting 100 percent supply-chain independence from Western sources. ([SCMP](https://www.scmp.com/tech/tech-war/article/3365049/nexperias-china-unit-pivots-domestic-12-inch-wafers-pursuit-100-independence?utm_source=rss_feed))




Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-august-24th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
