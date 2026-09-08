---
source: https://daily.semidoped.com/p/daily-update-july-21st-2026
title: Daily Update - July 21st, 2026
date: 2026-07-21
kind: clipping
genre: daily
audience: everyone
subtitle: AMD's Helios lands Azure, China's 1GW domestic stack goes optical, Etched eyes $20B, and OpenRouter draws suitors
---
**Good morning, it’s July 21st, 2026.**

AMD is making a grand entrance into rack-level hardware with their Microsoft deal, China is deploying some large scale-up domains in GW-scale datacenters, Etched reaching $20B valuations, ASML employees get €20,000 but vests by 2030, and potential interest in an acquisition of OpenRouter.

Let’s get into it. _— Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

### **Presented by …** _(this spot is open: reply to this email to talk sponsorship)_

### AMD Wins Azure Helios Deal as Nvidia’s Rack Monopoly Faces First Real Test

**Microsoft will deploy AMD’s Helios rack-scale AI system** on Azure to support **frontier model inference** , per a joint announcement timed ahead of AMD’s [Advancing AI 2026 event on July 22](https://www.digitimes.com/news/a20260721VL200/amd-microsoft-azure-partnership-infrastructure.html). The deal pairs Helios with **6th-gen EPYC processors** and marks the first credible hyperscale commitment to an alternative rack-scale architecture — directly targeting Nvidia’s end-to-end infrastructure dominance in inference workloads ([CNBC](https://www.cnbc.com/2026/07/20/amd-helios-microsoft-ai-nvidia.html), [Data Center Dynamics](https://www.datacenterdynamics.com/en/news/microsoft-to-deploy-amd-helios-rackscale-solution-to-support-inference-workloads-and-azure-services/)).

  * **Helios** is AMD’s first rack-scale AI system, purpose-built to rival Nvidia’s NVL rack configurations at the infrastructure layer.

  * Deployment scope covers **Microsoft’s own frontier models, Azure AI services, and enterprise customers** — not a limited pilot.

  * **Anthropic** is reportedly evaluating AMD as a second source, which would extend pressure on Nvidia beyond Microsoft ([The Decoder](https://the-decoder.com/nvidias-grip-on-ai-chips-weakens-as-microsoft-turns-to-amd-and-anthropic-may-follow/)).

  * AMD’s **Advancing AI 2026 event opens July 22** — the concrete next checkpoint for Helios specs, pricing, and any additional customer disclosures that validate whether this deal is replicable at scale.




> **Vik:** _Nvidia currently controls 95% of the datacenter GPU market, and the Helios can change that. Look at what AMD did to take back market share from Intel in server CPUs… AMD commands about 35% of the market share, from nearly 0% a decade ago. We can expect something similar to happen with AMD taking Nvidia market share. I’d bet it would happen a lot faster as customers are eager to suck up compute supply. Diversifying away from Nvidia is a bonus._
> 
> **Austin:** _Helios is the first time AMD shows up as a rack: MI455X + EPYC Venice + Pensando + ROCm, shipping 2H26. This is what the 2024 ZT Systems acquisition was for. AMD’s 2H26 looking great; OpenAI (first 1GW) and Oracle (50K MI450s from Q3) and now Microsoft Azure. Per Jean Hu and Matt Ramsay at BofA conference, customers are already running full Helios racks on production workloads in their own datacenters, with a concentrated ODM set at launch and revenue step-ups in Q4 and Q1._
> 
> _Of course, don’t forget CPUs! AMD’s Q1 CPU revenue +50%, Q2 guided +70% YoY, and two-thirds of that is units, not price. Traditional cloud is only ~$25–30B; AMD says head nodes plus agentic racks are another ~$100B! Venice at 256 cores on 2nm is built around “concurrent agents per rack per megawatt”. Note there’s a real constraint in wafer supply. TSMC is tight, and AMD claims it pre-booked ‘26/’27 and is negotiating ‘28. I’m watching tomorrow for more MI500 news, hoping for more customer announcements, and want to see Pensando get more airtime._

### Nvidia Stakes Nebius, Hut 8 and IREN Lock Multibillion-Dollar AI Cloud Deals

Nvidia has disclosed a **9.3% stake in Nebius** — which simultaneously closed **$775M in secured debt financing** — while Hut 8 signed a **$9.8B data-center lease** and IREN added **$2.8B in new contracts** , raising its 2026 ARR target to **over $4B** ([CNBC](https://www.cnbc.com/2026/07/21/nebius-stock-nvidia-stake-neocloud.html), [Data Center Dynamics](https://www.datacenterdynamics.com/en/news/nebius-secures-775m-in-debt-financing/), [Reuters](https://www.reuters.com/technology/hut-8-signs-98-billion-ai-data-center-lease-fully-commercializes-texas-campus-2026-07-20/), [IREN](https://irisenergy.gcs-web.com/news-releases/news-release-details/iren-signs-28bn-new-customer-contracts-leading-ai-developers)).

  * **~85%** of IREN’s **$4B+** ARR target is now under contract ([IREN](https://irisenergy.gcs-web.com/news-releases/news-release-details/iren-signs-28bn-new-customer-contracts-leading-ai-developers), [Pulse 2.0](https://pulse2.com/iren-signs-2-8-billion-in-ai-cloud-contracts-and-raises-2026-arr-target-to-over-4-billion/)).

  * Nebius’s **$775M** facility is its first secured debt raise; Nvidia’s equity stake follows a prior **$2B** GPU commitment ([Data Center Dynamics](https://www.datacenterdynamics.com/en/news/nebius-secures-775m-in-debt-financing/), [The Tech Buzz](https://www.techbuzz.ai/articles/nvidia-takes-9-3-stake-in-nebius-after-2b-cloud-bet)).

  * Nvidia taking equity in its own customers structurally entrenches the neocloud layer.




### China’s Domestic AI Stack Closes Around Optics, Supernodes, and 1GW Silicon

Z.AI’s **1GW data center running entirely on domestic chips** is now in partial operation ([DigiTimes](https://www.digitimes.com/news/a20260721VL204/z.ai-chips-data-center-bloomberg-nvidia.html)), while WAIC 2025 surfaced competing supernode architectures — Huawei’s **Ascend 950 linking 1,024 NPUs** , Biren’s **1,024-GPU optical supernode** ([DigiTimes](https://www.digitimes.com/news/a20260720VL218/china-ai-chips-hardware-optics-packaging.html), [Caixin Global](https://www.caixinglobal.com/2026-07-21/biren-unveils-1024-gpu-optical-super-node-architecture-102466336.html)), and Moore Threads’ **MTT C256 at 256 GPUs** ([TechNode](https://technode.com/2026/07/21/moore-threads-packs-256-gpus-into-its-mtt-c256-system/)) — as China’s stack consolidates beyond individual accelerators.

  * **SMIC N+3 Kirin 9030** hits **~32.5nm minimum metal pitch** , 10% tighter than the 36nm minimum metal pitch found in Intel's Panther Lake CPUs on 18A, though **efficiency gaps persist** ([DigiTimes](https://www.digitimes.com/news/a20260721PD236/huawei-kirin-efficiency-7nm-smic.html), teardown by SemiAnalysis)

  * Beijing is weighing **export controls on domestic AI models and chips** ([Reuters](https://www.reuters.com/world/asia-pacific/china-considers-tighter-export-controls-ai-models-chips-ft-reports-2026-07-21/)), which would formalize the stack as a sovereign asset




> **Vik:** _SMIC N+3 uses a ton of transistor optimizations that still only use DUV — like two fins per transistor, contacts over active gate, and single diffusions between cells. They may be able to get a better metal pitch, but power and performance are still lacking. Future Kirin chips are expected to have 3D LogicFolding that will boost transistor performance._
> 
> _Also, those 1GW chips running large scale-up domains? They heavily use near-packaged optics (NPO). It tells you where interconnects are going for scale-up._

### Etched Targets $20 Billion Valuation in Dual-Round Fundraise Led by Jane Street

Etched, a San Jose-based AI inference chip startup founded in 2022, is in talks to raise capital at a $20 billion valuation in a round led by Jane Street, according to people familiar with the matter. The company says it is testing its initial chip design and working to validate its first product against $1 billion in customer demand. 

**Sources:** [wsj.com](https://www.wsj.com/tech/ai/ai-chip-startup-etched-is-in-talks-for-20-billion-valuation-caf1787d?st=CkQqC5&reflink=article_copyURL_share)

> **Vik:**_Etched came out with a bang recently, with a ton of customer demand. A $20B valuation round would put Etched in the same weight class as Groq, for which NVIDIA paid $20B._
> 
> **Austin:**_Could Etched be the[next trillion-dollar chip company](https://www.chipstrat.com/p/the-next-trillion-dollar-chip-company)? _

### OpenRouter Fields Multibillion-Dollar Takeover Interest After Revenue Surges Fivefold

OpenRouter, a startup that provides API access to more than 400 proprietary and open-source AI models, has held discussions about a potential acquisition at a valuation of several billion dollars, according to people familiar with the matter. 

The company raised $113 million in May in a round led by Alphabet’s CapitalG, with prior backing from Andreessen Horowitz and Menlo Ventures. Annualized revenue reached $50 million in April, up fivefold since October 2024, and token processing through its API has grown tenfold since the start of 2025 to more than 60 trillion tokens. Potential buyers were not identified.

**Sources:** [theinformation.com](https://www.theinformation.com/articles/startup-openrouter-fields-multi-billion-dollar-takeover-interest?rc=ij60ts&shared=33ff386039a8785f)

> **Vik:**_Who would want to buy OpenRouter? Looking at the investor list: Nvidia’s NVentures, Snowflake and Databricks Ventures, among others, Nvidia might be interested to actual own a diversified model layer and get actual insights into inference side token demand. Databricks and Snowflake have a ton of data already; perhaps it makes sense to bring AI models to the data. Just my guesses._

### ASML Offers €20,000 Share Bonus to All 45,000 Global Employees

ASML will grant each of its approximately 45,000 global employees a one-time €20,000 ($22,862) share award on January 1, vesting at the start of 2030 for staff who remain with the company through that period. The announcement follows ASML raising its annual sales forecast for the second time this year and expanding production capacity to meet AI-driven demand. The bonus mirrors moves by chipmaker customers including Samsung and SK Hynix, which have also offered payouts to employees as AI infrastructure spending fuels record revenues. TSMC in May committed to raising profit-sharing payments by more than 30% on average this year.

**Sources:** [bloomberg.com](https://www.bloomberg.com/news/articles/2026-07-17/asml-to-pay-one-time-20-000-bonus-to-staff-as-ai-propels-demand)

> **Vik:**_Passing along some AI-fueled growth along to hardworking employees. Nice! But fully vesting in 2030?! Those are some long term golden handcuffs._
> 
> **Austin:**_ASML has to be the most interesting place to work in the Netherlands if you’re a local, and probably all of Europe for that matter, so golden handcuffs look a lot different than SF where you can walk down the street to another interesting employer. That said, they probably have a global workforce who might get poached by memory companies etc. Regardless, good for ASML to reward and retain employees._

## Quick Hits

**Compute**

  * **Google** is reportedly developing ‘Frozen v2’, a Gemini-optimized inference chip built with Samsung to boost model efficiency. ([CNBC](https://www.cnbc.com/2026/07/20/alphabet-googl-stock-ai-chip-report.html), [The Information](https://www.theinformation.com/articles/google-plans-new-frozen-chip-run-ai-models-efficiently), [Bloomberg.com](https://www.bloomberg.com/news/articles/2026-07-20/google-plans-new-chip-to-boost-ai-efficiency-information-says))

  * **Bristol Myers Squibb** is building a life-science AI factory on Nvidia’s Vera Rubin platform for drug research. ([Nvidia News](https://blogs.nvidia.com/blog/bristol-myers-squibb-building-life-science-industrys-most-advanced-ai-factory-on-nvidia-vera-rubin/), [Reuters](https://www.reuters.com/legal/litigation/bristol-myers-buys-nvidias-latest-ai-computing-system-drug-research-2026-07-20/), [Bloomberg.com](https://www.bloomberg.com/news/articles/2026-07-20/bristol-partners-with-nvidia-on-ai-factory-for-drug-development))




**Memory**

  * **Samsung** and **SK Hynix** are prioritizing server DDR5 as margins approach HBM levels, while DDR5 spot prices hit record highs. ([DigiTimes](https://www.digitimes.com/news/a20260720VL213/samsung-hbm-sk-hynix-ddr5-dram.html?chid=10), [The Korea Herald](https://www.koreaherald.com/article/10813898))

  * **DigiTimes/Micron** analysts warn the memory shortage could flip to a glut by 2028 as chipmakers expand capacity aggressively. ([DigiTimes](https://www.digitimes.com/news/a20260720VL223/2028-dram-hbm-demand-sk-hynix.html))




**Foundry & Packaging**

  * **Siemens EDA** agreed to acquire Precision Innovations to add AI-powered SoC design planning and optimization to its toolchain. ([Siemens Newsroom](https://news.siemens.com/en-us/siemens-to-acquire-precision-innovations/), [Design News](https://www.designnews.com/electronics/siemens-acquires-precision-innovations-to-add-ai-chip-planning-to-eda), [Star Local Media](https://starlocalmedia.com/planocourier/news/siemens-to-acquire-chip-design-firm-precision-innovations/article_548bbb42-b13b-482e-bbf8-301b328d971a.html))

  * **TSMC** disclosed plans to raise chipmaking prices by up to 10% in 2027, per Nikkei, to offset US expansion costs. ([Bloomberg Tech](https://www.bloomberg.com/news/articles/2026-07-21/tsmc-in-talks-to-raise-prices-by-up-to-10-in-2027-nikkei-says), [DigiTimes](https://www.digitimes.com/news/a20260721PD217/tsmc-expansion-demand-investment-arizona.html))




**Networking & Optics**

  * **Innolight** (Zhongji) plans an ~$8 billion Hong Kong listing backed by BlackRock, Hillhouse and Temasek amid an optical-transceiver boom. ([Bloomberg.com](https://www.bloomberg.com/news/articles/2026-07-20/zhongji-innolight-starts-gauging-interest-for-hong-kong-listing), [Smartkarma](https://www.smartkarma.com/insights/zhongji-innolight-a-h-pre-ipo-early-thoughts), [The Standard (HK)](https://www.thestandard.com.hk/finance/article/337778/Chinas-Zhongji-Innolight-to-raise-US8-billion-in-Hong-Kong-listing-sources-say))




**Robotics**

  * **Samsung** created a standalone robotics division, hiring an ex-Boston Dynamics/Hyundai executive to lead humanoid strategy. ([Bloomberg Tech](https://www.bloomberg.com/news/articles/2026-07-21/samsung-hires-ex-boston-dynamics-executive-in-robotics-push), [Reuters](https://www.reuters.com/world/asia-pacific/samsung-electronics-creates-robotics-division-key-part-growth-strategy-2026-07-21/), [Silicon Republic](https://www.siliconrepublic.com/machines/samsungs-new-robotics-division-appoints-former-boston-dynamics-lead))




**Presented by …** _(this spot is open: reply to this email to talk sponsorship)_

### Key Data

Similar colors in the chart below means that models give similar responses. It makes sense that each model gives similar responses to itself — there for the diagonal is all blue. Interesting to note:

  * Moonshot Kimi K3 is similar to Fable and Opus

  * GLM 5.2 is similar to Gemini




This is leading to believe that Chinese models are distilled from frontier US models. 

[](https://substackcdn.com/image/fetch/$s_!sd18!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05267ca8-840f-469f-b97e-ff5993474d44_864x741.png)

### Interesting

Watch the full teardown video from SemiAnalysis.

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-july-21st-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
