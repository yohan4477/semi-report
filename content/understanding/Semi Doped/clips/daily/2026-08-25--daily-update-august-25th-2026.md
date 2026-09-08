---
source: https://daily.semidoped.com/p/daily-update-august-25th-2026
title: Daily Update - August 25th, 2026
date: 2026-08-25
kind: clipping
genre: daily
audience: everyone
subtitle: OpenAI's Jalapeño beats Blackwell on perf/W and matches Rubin in SemiAnalysis benchmarks; Nvidia's Groq 3 LPX enters mass production at Samsung; Anthropic builds a silicon team; Apple launches M6.
---
**Hello world, it’s Tuesday, August 25th.**

OpenAI’s Jalapeño inference chip went in front on a third-party benchmark and beat Blackwell on tokens per megawatt while running level with Vera Rubin, nine months after tapeout. Also today, Nvidia’s Groq 3 LPX inference rack entered mass production at Samsung Foundry, Anthropic is building a custom silicon team, and Apple launched the M6 and M5 Ultra as TSMC works through HBM packaging yields.

Let’s get into it. _— Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player_

 _Tell us how to make Semi Doped better![ Give us your feedback](http://semidoped.com/poll)! ❤️_

### OpenAI’s Jalapeño Beats Blackwell on Perf/W and Runs Level With Rubin, Nine Months After Tapeout

OpenAI put its first inference chip in front of a third-party benchmark. SemiAnalysis [ran its InferenceX suite on Jalapeño in OpenAI’s lab](https://newsletter.semianalysis.com/p/openai-jalapeno-better-than-nvidia) and reports the chip beats every Nvidia, AMD and Google part it has tested on tokens per megawatt, across nearly the whole latency curve, using single-token prediction with no speculative decoding and no prefill/decode disaggregation. On DeepSeek R1 it delivers more than 700 tokens per second per user at concurrency one. Kimi K2.5 and GPT-OSS ran at roughly 1,400. Against Vera Rubin, whose July figures used multi-token prediction, Jalapeño’s single-token throughput per MW still comes out ahead, and the two land roughly even on tokens per dollar.

Design began in mid-2024, the CoWoS tapeout was November 2025, and these results come from A0 silicon after about three months of bring-up. A B0 stepping is already in the fab with roughly 25% better performance per watt. B0 delivers 13.4 PFLOPs of MXFP4 on a single reticle-sized N3P die at 700 W, against 17.5 PFLOPs of dense NVFP4 for a Rubin compute die of similar size at 900 to 1,150 W. Memory is HBM4 at 15.4 TB/s per package, which implies 10 Gbps pin speeds versus the 9.6 Gbps Nvidia gets from HBM4 on Rubin, and SemiAnalysis believes the stacks come from Samsung. A rack holds 128 chips across 16 trays, scale-up reaches 2,048 chips over 16 racks on Tomahawk 6 switches, and a two-rack system draws about 160 kW. 

OpenAI [unveiled the program with Broadcom on June 24](https://openai.com/index/openai-broadcom-jalapeno-inference-chip/) and puts initial design to tape-out at nine months, with its own models accelerating parts of the design; SemiAnalysis counts about 16 months from team hiring, starting mid-2024. OpenAI says engineering samples are running GPT-5.3-Codex-Spark at production target frequency and power, and the kernels are written with Codex.

The caveats are real. Every number was supplied by OpenAI, verified in person but only on the 8k/1k workload, with no AgentX long-context results yet. OpenAI’s page says initial deployment by the end of 2026; SemiAnalysis has production ramping through 2027 with most volume at the end of next year. Either way Rubin ships to customers now while Jalapeño is engineering samples. SemiAnalysis’s read on the fallout is that Cerebras’s 1.25 GW option beyond OpenAI’s firm 750 MW commitment is now in question, and that AMD’s kernel team should be worried.

What people are saying:

  * **Gavin Baker:** “Impressive that Jalapeño outperforms the comparable TPU and is in the mix with Rubin. Credit where credit is due - first good ASIC outside of TPU/Trainium. However, will likely significantly underperform a disaggregated GPU/Trainium plus SRAM accelerator setup.” He added that the real comparison “will be with Rubin Ultra given Rubin shipping today,” and that Jalapeño “participated in a third party benchmark _before_ TPUs! Tells you a lot!” ([X](https://x.com/GavinSBaker/status/2092265540068966504))

  * **Jukan:** “As far as I know, Jalapeño uses Samsung’s HBM4 almost exclusively. It’s superior to Rubin.” ([X](https://x.com/jukan05/status/2092257540771917956)) And on volume: “OAI’s Jalapeño can’t scale to the same level as Rubin. If they source HBM4 exclusively from Samsung, there will be a limit to how far they can ramp.” ([X](https://x.com/jukan05/status/2092271778819375391))




> _**Vik:** Impressive achievement by OpenAI, and I am at Hot Chips where I will see this presentation live. I am surely it will be heavily attended. Two important things stand out to me already:_
> 
>   1. _**AI can significantly accelerate EDA for chip design**. A chip like this used to take 3-4 years, not 16 months. Getting it this competitive in first silicon pass is a big deal_
> 
>   2.  _HBM4 is used in Jalapeno even though many comparisons are made to Blackwell which uses HBM3e.**The memory bandwidth advantage is big, and points to where future optimizations will continue in HBM**. HBM5 is expected to have >23 Gbps/pin._
> 
> 

> 
> _**Austin:** Can’t wait to hear more. I’m very interested in how the OAI team frames the use of Jalapeño within it’s broader multi vendor inference portfolio._

### Nvidia Groq 3 LPX Enters Mass Production on Samsung Foundry

Nvidia has moved the [Groq 3 LPX inference rack into full production](https://nvidianews.nvidia.com/news/nvidia-groq-3-lpx-now-in-full-production-with-world-class-speed-for-agentic-ai), with Samsung Foundry handling manufacturing duties in what KED Global frames as a meaningful data point for the foundry’s recovery story. The rack integrates with the Vera Rubin NVL72 system and targets agentic long-context workloads, where, according to OpenRouter data cited by Nvidia, agents consume 15x more tokens than a standard chat request. Nvidia [claims 4x the throughput of Cerebras](https://the-decoder.com/nvidia-says-its-groq-3-lpx-is-four-times-faster-than-cerebras-but-the-math-is-more-complicated/) for those workloads, though The Decoder notes the comparison carries caveats. The production news arrives days before Nvidia’s Wednesday earnings call, giving the company a fresh revenue line to discuss. Samsung, still rebuilding its foundry credibility, earns a high-profile win.

> _**Vik:** Cool, but I still dislike Groq LPUs as a chip in itself. The expertise of the team they acquired will be more useful in building SRAM-based inference within their own products._
> 
> _**Austin:** This is Samsung Foundry’s 4nm process. If this was built on Intel 3, everyone would say “dude, this isn’t 18A, you can’t take a victory lap”. Same goes for Samsung Foundry, no?_

### Anthropic Builds Custom Silicon Team, Pressuring Merchant Chip Vendors

Anthropic is [accelerating development of proprietary AI training chips](https://www.digitimes.com/news/a20260825PD222/anthropic-asic-chips-silicon-design.html), a strategic turn that DigiTimes reports is already reshaping how the company places ASIC orders and threatening displacement of existing merchant-silicon and contract ASIC suppliers. The effort gained credibility when Anthropic hired the founder of Google’s TPU program, bringing rare in-house expertise for designing silicon at the scale Claude’s training demands. TSMC and advanced-packaging specialists stand to gain a substantial new customer as Anthropic moves toward committing custom training silicon to volume fabrication. The company is also navigating a broader competitive gap with OpenAI, with 36Kr noting Anthropic trails on infrastructure self-sufficiency even as it pursues what could be one of the largest IPOs in tech history.

> _**Vik:** Anthropic’s search for in-house hardware will step up now. They have hired some important people and rumors are that they are shopping around for someone to buy._
> 
> _**Austin:** Model labs + custom silicon teams is the trend here. OpenAI, Anthropic, Tesla, Waymo, Rivian … is it time merchant silicon vendors acquire model labs? Nvidia is doing as much with Poolside…_

### Apple Launches M6 and M5 Ultra as TSMC Wrestles With HBM Packaging Yields

Apple [introduced the M6 and M5 Ultra processors](https://www.businesswire.com/news/home/20260824417799/en/Apple-introduces-M6-and-M5-Ultra-for-a-big-leap-in-performance-and-AI-compute) Tuesday, pairing them with refreshed Mac mini and Mac Studio desktops in what the company called a major step forward in performance and AI compute. The M5 Ultra powers the Mac Studio, while the M6 anchors the new Mac mini. TSMC’s HBM packaging yield problems are drawing attention from analysts who say the difficulties benefit Intel’s packaging ambitions, according to EE Times. Those yield issues arrive at an awkward moment: TSMC is simultaneously ramping Apple’s most compute-intensive silicon to date, a combination that puts real pressure on the foundry’s advanced packaging capacity. Intel has been building out its own packaging capabilities and stands to attract customers if TSMC’s HBM problems persist.

> _**Vik:** If you are thinking you will buy an M5 Ultra and start inferencing at home, be prepared to sell your car. I do not thing this will be hobby-grade. It would be more like a DGX Spark. This is a good direction for Apple tbh, and would permanently knock out Windows/Windows-based ARM out of such workloads. Hint Snapdragon; see below._

### Sector Watch

#### Compute & Silicon

  * **Qualcomm** reveals its next Snapdragon flagship breaks the 5 GHz barrier with a new Oryon CPU core and FlexCache architecture. ([9to5Google](https://9to5google.com/2026/08/25/qualcomm-next-snapdragon-oryon-cpu/))

  * **AMD** details the MI400 Helios rack-scale AI infrastructure architecture at Hot Chips 2026, outlining system-level integration strategy. ([ServeTheHome](https://www.servethehome.com/amd-helios-mi400-system-architecture-at-hot-chips-2026/))

  * **Intel** presents Diamond Rapids, its 2027 Xeon server CPU with up to 256 cores per socket, and the Crescent Island GPU with up to 480 GB LPDDR5X at Hot Chips 2026. ([ServeTheHome](https://www.servethehome.com/intel-crescent-island-160gb-to-480gb-lpddr5x-ai-gpu-at-hot-chips-2026/))




#### Foundry & Packaging

  * **Japan** plans an additional 150 billion yen injection into Rapidus, pushing total state support higher as the 2nm foundry startup advances toward pilot production. ([Tech in Asia](https://www.techinasia.com/news/japan-plans-944m-chipmaker-rapidus))

  * **SK Hynix** publishes a detailed tech note on hybrid bonding as a foundational advanced-packaging technology, underscoring its roadmap leadership ahead of next-generation HBM generations. ([SK Hynix](https://news.skhynix.com/en/tech-note-series-ep2/))

  * **KCTech** wins a supply contract to provide CMP equipment and slurry for glass substrates to Absolics, supporting the SKC subsidiary’s 400 billion won capacity expansion. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13280))




#### Memory

  * **Enflame** , the Tencent-backed Chinese AI chipmaker, sets September 2 as its STAR Market IPO subscription date targeting roughly $900 million in proceeds. ([MEXC](https://www.mexc.com/crypto-pulse/article/enflame-ipo-date-set-141725))

  * **Hana Materials** faces a potential supply disruption after management imposed a lockout in response to a union strike, threatening silicon materials supply chains dependent on the Korean supplier. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13273))

  * **SK Hynix** union rejects a preliminary wage-hike agreement, prolonging labor negotiations at the world’s leading HBM supplier. ([Bloomberg](https://www.bloomberg.com/news/articles/2026-08-25/sk-hynix-union-rejects-preliminary-wage-hike-deal-yonhap-says))




#### Power

  * **Navitas Semiconductor** acquires Claros Technologies to add vertical power delivery (VPD) and integrated voltage regulator (IVR) technology for grid-to-xPU AI infrastructure applications. ([GlobeNewswire](https://www.globenewswire.com/news-release/2026/08/25/3350179/0/en/navitas-to-acquire-claros-advancing-ai-infrastructure-with-vpd-ivr-technology-for-grid-to-xpu.html))

  * **LS ELECTRIC** wins a $165.7 million power equipment order from a US Big Tech hyperscaler for an AI data center, its largest single overseas contract. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13270))

  * **NVent** pursues a $1.75 billion acquisition deal to expand its share of the AI data center thermal and power management market. ([Bloomberg](https://www.bloomberg.com/news/articles/2026-08-24/nvent-seeks-bigger-piece-of-ai-boom-with-1-75-billion-deal))




#### Policy & Trade

  * **US** government is reportedly considering pushing a near-total ban on ASML DUV sales and servicing to China, escalating semiconductor export restrictions. ([TrendForce](https://www.trendforce.com/news/2026/08/25/news-u-s-may-push-near-total-asml-china-ban-on-duv-sales-and-servicing-amid-chinas-domestic-lithography-push/))

  * **Tokyo Electron** delegation meets India Commerce Minister Piyush Goyal to discuss investment in the country’s emerging semiconductor ecosystem. ([thepublicworld.com](https://thepublicworld.com/archives/119426))

  * **Leeno Industrial** loses approximately 2 billion won per day as a prolonged worker strike redirects orders to Japanese and Taiwanese competitors. ([thelec.net](https://www.thelec.net/news/articleView.html?idxno=13322))




#### Data Centers

  * **Digital Realty** is selected to develop 50 MW of new AI-ready data center capacity on Singapore’s Jurong Island, expanding its Asia-Pacific footprint. ([Digital Realty](https://investor.digitalrealty.com/news-releases/news-release-details/digital-realty-selected-develop-50-megawatts-new-data-center))

  * **Lancium** announces a partnership with Nvidia to develop gigawatt-scale AI factory infrastructure across its 15-plus GW power portfolio. ([PR Newswire](https://www.prnewswire.com/news-releases/lancium-announces-partnership-with-nvidia-to-advance-gigawatt-scale-ai-factory-development-across-its-15-gw-portfolio-302858393.html))

  * **India** AI data center firm places an order for 9,000 Nvidia Vera Rubin systems, one of the largest single GPU procurement commitments outside the US hyperscalers. ([Bloomberg](https://www.bloomberg.com/news/articles/2026-08-25/india-ai-data-center-firm-orders-9-000-nvidia-vera-rubin-systems))




#### Optics & Networking

  * **Cisco** expands its Secure AI Factory with Nvidia for rack-scale AI infrastructure, adding validated full-stack architectures targeting enterprise AI deployment. ([Cisco](https://newsroom.cisco.com/c/r/newsroom/en/us/a/y2026/m08/cisco-secure-ai-factory-nvidia-rack-scale.html?source=rss))

  * **Eoptolink** is stockpiling optical components as AI-driven demand surges, positioning the Chinese transceiver maker to capture supply advantages over rivals. ([Briefs Finance](https://www.briefs.co/news/eoptolink-builds-up-component-reserves-as-ai-demand-soars-in/))

  * **Ciena** research finds service providers globally expect high-capacity AI services and multi-operator fiber networks to become primary revenue growth drivers. ([Business Wire](https://www.businesswire.com/news/home/20260825759712/en/New-Ciena-Research-Service-Providers-Expect-High-Capacity-AI-Services-and-MOFN-to-Fuel-Revenue-Growth-But-Network-Upgrades-are-Needed))




_Tell us how to make Semi Doped better![ Give us your feedback](http://semidoped.com/poll)! ❤️_

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-august-25th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
