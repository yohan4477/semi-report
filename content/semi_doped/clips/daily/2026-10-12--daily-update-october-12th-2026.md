---
source: https://daily.semidoped.com/p/daily-update-october-12th-2026
title: Daily Update - October 12th, 2026
date: 2026-10-12
kind: clipping
genre: daily
audience: everyone
subtitle: Amazon eyes Decart for $7B, TSMC cost hikes lift Intel CPU prices 20%, Vicor names 20 AI server makers in ITC complaint, Nvidia pursues Reflection AI deal.
---
**Hello world, it’s Monday, October 12th.**

Amazon is in talks to acquire Israeli AI startup Decart for around $7 billion to strengthen the software stack on its Trainium chips. Elsewhere, TSMC’s rising costs are pushing Intel CPU prices up as much as 20%, Vicor’s ITC complaint names roughly 20 AI server suppliers, and Nvidia is in early talks around Reflection AI and inference startup d-Matrix.

Let’s get into it. — _Austin & Vik_



 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

#### Presented by Crusoe

Crusoe builds AI infrastructure from the ground up — power, data centers, and the cloud on top.

If you’re running open models — GLM, DeepSeek, Kimi, Qwen — Crusoe’s managed inference is fast: up to 9.9x faster time-to-first-token and 5x the throughput of vLLM, thanks to their MemoryAlloy caching layer and tokenizer fastokens. And it’s the easy kind of fast: pick a model, grab an API key and start inference. No GPUs to provision, no infrastructure or clusters to manage, and it’s pay per million tokens.

**$5 in free credits to try it.[Send your first request today →](https://semidoped.com/crusoe-daily)**

### Amazon Pursues $7 Billion Decart Deal to Strengthen Trainium Software Stack

Amazon is [in talks to acquire Israeli AI startup Decart for around $7 billion](https://www.reuters.com/business/retail-consumer/amazon-talks-buy-ai-startup-decart-around-7-billion-wsj-reports-2026-10-11/), according to a Wall Street Journal report cited by Reuters. Decart, founded in Tel Aviv, has built model-optimization software that runs on Amazon’s proprietary Trainium training chips, making it a close technical fit for AWS’s push to compete with Nvidia’s end-to-end hardware-software stack. The reported price would rank among the largest acquisitions in Israeli tech history. CTech draws a parallel to Amazon’s 2023 investment in Anthropic, framing the Decart talks as part of a broader effort to deepen AWS’s position in the AI training supply chain rather than rely on third-party optimization tooling.

> **Austin:** _Anthropic walked away from Decart at about $6B just last month, after due diligence. Now Amazon is reportedly in at $7B. Seems this is entirely about “how to get more tokens out of Trainium”… i.e. better software to improve utilization._
> 
> **Vik:**_Hesitation in acquiring Decart is costing them $1B. Nuts._

### TSMC Cost Increases Push Intel CPU Prices Up 20%, Others Follow

TSMC’s rising wafer and advanced packaging costs are now landing directly on chip buyers, with [Intel reportedly raising prices as much as 20%](https://www.trendforce.com/news/2026/10/12/news-cpu-price-hike-wave-intel-reportedly-up-to-20-qualcomm-10-amd-may-join-as-tsmc-costs-climb/) and Qualcomm close behind at roughly 10%, according to TrendForce. AMD hasn’t moved yet but is expected to follow, making this the first coordinated CPU price-hike wave tied explicitly to foundry cost pass-through. The pressure point is TSMC’s advanced packaging capacity, which remains tight and expensive. OEMs and system builders absorbing these increases face compressed margins at a moment when AI server demand is already straining component budgets. TSMC’s [wafer and CoWoS packaging costs](https://www.trendforce.com/news/2026/10/12/news-tsmcs-2b-silicon-interposer-deal-with-gf-could-fast-track-u-s-packaging-to-1h28-free-up-fab-capacity/) have climbed steadily as the company invests in both overseas fabs and next-generation interconnect technology.

> **Vik:** _The 20% lands on Panther Lake parts with high-end GPU tiles built on TSMC N3E - Intel’s own 18A compute tile isn’t driving it.[TSMC has full pricing power across mobile and AI now](https://www.viksnewsletter.com/p/high-stakes-advanced-node-poker-tsmc-intel), and it flows straight to buyers. Everyone downstream eats it._
> 
> **Austin:**_TSMC is charging for it’s value. As they should!_
> 
> [![tsmc-gm-vs-gross-profit-dollars.png](<../_img/2026-10-12--daily-update-october-12th-2026/001_79964020-cf70-4657-bce3-6f03dcb24bf5_2100x1280.png> "https://substackcdn.com/image/fetch/$s_!aB9W!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F79964020-cf70-4657-bce3-6f03dcb24bf5_2100x1280.png")](https://substackcdn.com/image/fetch/$s_!aB9W!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F79964020-cf70-4657-bce3-6f03dcb24bf5_2100x1280.png)[Source](https://newsletter.chipstrat.com/p/tsmc-could-spend-10b-more-on-n2-capacity)

### Vicor ITC Section 337 Filing Pulls 20 AI Server Makers Into Patent Fight

Vicor has expanded its ITC Section 337 complaint to [name roughly 20 respondents](https://thenextweb.com/news/us-probes-foxconn-luxshare-and-18-others-over-ai-server-power-patents), including Foxconn, Luxshare, Quanta, Delta, and a broad swath of the AI server supply chain, seeking import bans on power hardware it says infringes its patents. The timing is pointed: hyperscalers are racing to lock in rack-scale AI server procurement just as this probe could disrupt the very manufacturers filling those orders. Luxshare, an Apple supplier also deep in data-center work, said in a [Saturday filing](https://www.bloomberg.com/news/articles/2026-10-11/apple-supplier-luxshare-expects-no-material-impact-from-us-probe) it expects no material impact. Quanta, meanwhile, has seen its stock price target revised to TWD 427.84 following the probe’s disclosure. The ITC’s formal investigation is now open.

> **Vik:** _The patents cover feeding power to the chip from directly underneath - vertical power delivery, the exact thing pushing advanced packaging right now. Vicor’s named basically the whole AI power chain, Infineon and MPS included. Luxshare says their parts aren’t in mass production yet, so limited near term bite. An import ban would get messy though._
> 
> **Austin:** _Maybe an opportunity for IVR startups like PowerLattice or Ferric? Or ADI’s Empower?_

### Nvidia Pursues Reflection AI Deal While Moving on Inference Chip Startup d-Matrix

Nvidia is in early-stage talks to acquire or deepen its investment in Reflection AI, an American open-weight model developer, the [Financial Times reported](https://www.bloomberg.com/news/articles/2026-10-10/nvidia-is-in-talks-to-acquire-reflection-ai-the-ft-reports), with Bloomberg adding that discussions include a broader computing arrangement. The company is separately weighing a [stake in d-Matrix](https://www.datacenterdynamics.com/en/news/report-nvidia-plans-to-invest-in-inference-chip-startup-d-matrix/), a startup building inference-focused silicon that competes in territory Nvidia has long dominated. Both moves arrive together, which is not a coincidence: Nvidia appears to be deploying its balance sheet to keep emerging inference competitors close rather than let them mature at arm’s length. Reflection AI is still a young outfit. d-Matrix is further along in silicon development. Nvidia isn’t slowing down.

> **Austin:** _Nvidia investing in open-weight models is very strategically sound[as I laid out here recently.](https://newsletter.chipstrat.com/p/open-weights-and-american-diffusion) _
> 
> **Vik:** _Same NVLink Fusion playbook here - keep the inference rivals plugged into the rack instead of letting them build their own. d-Matrix already said they’d hook Raptor up through it. Nvidia went from dismissing custom silicon in 2025 to hosting it. Reflection’s a model team though, that one’s probably an acqui-hire.[I have covered d-Matrix in depth on my newsletter befor](https://open.substack.com/pub/viksnewsletter/p/d-matrix-in-memory-compute?r=89umme&utm_campaign=post-expanded-share&utm_medium=web)e. Upcoming Semi Doped podcast with d-Matrix Sudeep Bhoja too._

### Super Micro Contractor Pleads Guilty in $2.5B AI Chip Diversion Case

A contractor described as a “fixer” in the Super Micro export-control investigation has pleaded guilty in a U.S. federal court, becoming the [first person formally convicted](https://thenextweb.com/news/super-micro-case-fixer-pleads-guilty-to-sending-ai-servers-to-china) in the alleged $2.5 billion scheme to divert Nvidia-powered AI servers to China. The broker admitted breaking export control rules by routing shipments through third-party intermediaries to obscure their ultimate destination. Super Micro co-founder Charles Liang has denied related charges, and the company itself has not been convicted of any crime. The guilty plea converts what was previously a set of allegations into a criminal record, sharpening legal exposure for others named in the case and drawing fresh regulatory attention to AI server supply chains that passed through China-linked buyers.

> **Vik:** _First actual conviction in the whole Super Micro saga. Co-founder’s trial is still ahead, November 2nd._

### Penguin Solutions Posts Record Quarter as AI Memory Orders Accelerate

Penguin Solutions raised its outlook on the strength of sustained AI memory system deployments. The results sent shares climbing sharply, with demand for purpose-built memory infrastructure outpacing the broader enterprise AI adoption curve that most analysts had penciled in. Bank of America, which [initiated coverage with a Buy rating](https://www.proactiveinvestors.com/companies/news/1099916/penguin-solutions-initiated-with-a-buy-from-bank-of-america-on-ai-memory-demand-1099916.html) citing AI memory demand, sees further upside tied to agentic AI workloads driving persistent procurement cycles. CEO and CFO commentary pointed to customers pulling forward large-scale memory system orders rather than waiting on general IT budget cycles, a pattern that management expects to continue through the coming fiscal year.

> **Vik:** _Penguin solutions[PENG 0.00%↑](https://substack.com/search/%24PENG) does memory testing at the module level, and their recent earnings are entirely memory price driven. Interesting to watch how this goes._

### Sector Watch

#### Foundry & Compute

  * **Rapidus** launches the CORE global ecosystem with 17 design-firm partners to secure customer commitments for its 2nm foundry service ahead of production. ([Semiconductor Digest](https://www.semiconductor-digest.com/rapidus-launches-core-ecosystem-to-support-2nm-chip-development-and-manufacturing/?utm_source=rss&utm_medium=rss&utm_campaign=rapidus-launches-core-ecosystem-to-support-2nm-chip-development-and-manufacturing))

  * **ASML** plans to raise prices on lithography spare parts, adding another cost vector to chipmakers already absorbing wafer-price increases. ([THE ELEC, Korea Electronics Industry Media](https://www.thelec.net/news/articleView.html?idxno=14518))

  * **Rapidus** partner **MediaTek** launches Dimensity 9600 Pro on 2nm process, with OPPO Find X10 Pro Max confirmed as global debut device. ([DagangNews](https://www.dagangnews.com/article/english/oppo-find-x10-pro-max-debut-globally-mediateks-2nm-flagship-dimensity-9600-pro-75544))




#### Power

  * **Infineon** unveils a 27 kW three-phase PSU reference design targeting next-generation AI server rack power architectures above 800 VDC. ([Semiconductor Digest](https://www.semiconductor-digest.com/infineon-unveils-27-kw-power-supply-for-next-generation-ai-servers/?utm_source=rss&utm_medium=rss&utm_campaign=infineon-unveils-27-kw-power-supply-for-next-generation-ai-servers))

  * **SolarEdge** and **Infineon** extend partnership to co-develop solid-state circuit breakers for 800 VDC AI data-center power systems. ([Energies Media](https://energiesmedia.com/solaredge-infineon-sscb-development-energy/))




#### PCB & Components

  * **Murata** completes inductor plant expansion in Dong Nai, Vietnam, adding production capacity to meet AI-server passive-component demand. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=14519))

  * **Samsung Electro-Mechanics** signs an AI server component supply deal, marking a new design-win in the high-density server substrate market. ([Samsung Electro-Mechanics](https://www.ad-hoc-news.de/boerse/news/corporate-news/samsung-electro-signs-ai-server-deal-samsung-electro-stock-sits-38-48/70299133))

  * **Unimicron** acquires Hukou industrial sites to expand PCB substrate capacity ahead of the TPCA Show, where its chair will deliver the keynote. ([Unimicron](https://www.ad-hoc-news.de/boerse/news/corporate-news/unimicron-bought-hukou-sites-unimicron-stock-sits-11-62-percent-below-its/70298283))




#### Memory

  * **CXMT** reports key progress on 4F² DRAM cell architecture, a structural breakthrough that could enable competitive server-class memory density. ([CNBC](https://www.cnbc.com/2026/10/11/this-chinese-memory-chip-maker-has-global-potential.html))

  * **TDK** is weighing a sale of its hard-drive head unit, a move that could reshape HDD supply chains and potentially eliminate a third major disk maker. ([Nikkei Asia](https://asia.nikkei.com/business/business-deals/tdk-weighs-sale-of-hard-drive-head-unit-but-regulatory-ok-uncertain))

  * **SK Group** chairman Chey Tae-won pledges to accelerate construction of a new semiconductor cluster in Gwangju, South Korea, as soon as possible. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=14517))




#### Optics & Networking

  * **Nokia** launches a flexible 50G/25G/10GPON line card enabling operators to evolve fiber networks incrementally toward AI-ready broadband without forklift upgrades. ([Nokia](https://www.nokia.com/newsroom/nokia-launches-flexible-50g25g10gpon-solution-to-accelerate-ai-ready-fiber-broadband/))

  * **Openreach** deploys Ciena WaveLogic 6 technology to deliver 1.6 Tbps wholesale optical services across its UK network infrastructure. ([Konsulteer](https://www.konsulteer.com/article/openreach-deploys-ciena-wavelogic-6-technology-for-1-6tbps-wholesale-optical-services))

  * **Nokia** launches GPU-accelerated AI-RAN with multiple operators beginning trial deployments this quarter, though industry experts remain divided on benefits. ([Light Reading](https://www.lightreading.com/5g/nokia-to-start-dealing-out-gpus-in-high-stakes-ai-ran-gamble))




#### Packaging

  * **Tata Electronics** and **Besi** announce a partnership to develop advanced semiconductor packaging capabilities in India, the first such named OEM-equipment deal for the country.

  * **TeraView** begins proof-of-concept validation of terahertz inspection equipment for through-glass vias in advanced glass substrates. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=14504))

  * **Nordson Electronics Solutions** launches ASYMTEK Vantage XL fluid-dispensing system targeting panel-level packaging production applications. ([DQ](https://www.dqindia.com/semiconductors/nordson-electronics-solutions-launches-asymtek-vantage-xl-fluid-dispensing-system-for-panel-level-packaging-12666723))




#### Data Centers & Edge

  * **Tencent** tells bond investors its planned $5 billion debt offering will fund AI-related CapEx, confirming the company as a major independent GPU demand center. ([Bloomberg Tech](https://www.bloomberg.com/news/articles/2026-10-12/tencent-tells-investors-its-5-billion-bond-mainly-for-ai-capex))

  * **Bain Capital** -owned Bridge Data Centres seeks to upsize an existing loan to $6.6 billion to fund continued Asia-Pacific data-center expansion. ([Bloomberg Tech](https://www.bloomberg.com/news/articles/2026-10-12/bain-s-bridge-data-centres-seeks-to-upsize-loan-to-6-6-billion))

  * **Nebius** acquires inference startup Inferize to expand its Token Factory inference platform as the company scales GPU cloud capacity. ([Pulse 2.0](https://pulse2.com/nebius-acquires-inferize-to-expand-token-factory-inference-platform/))




#### Policy & Trade

  * **Broadcom** CEO states the biggest constraint on AI-fuelled tech growth is capital availability, not memory chip supply — a direct counter-narrative to prevailing HBM bottleneck framing. ([Reuters](https://www.reuters.com/world/asia-pacific/broadcom-ceo-says-biggest-hurdle-ai-fuelled-tech-growth-is-capital-not-memory-2026-10-12/))

  * **Qualcomm** and **Arm** jury deliberations extend into next week in the contract-breach dispute that could affect Arm’s licensing model industry-wide. ([Reuters](https://www.reuters.com/business/media-telecom/qualcomm-arm-set-jury-verdict-contract-breach-feud-2026-10-09/))

  * **Suzhou Dongshan Precision** gauges investor appetite for a Hong Kong listing of up to $3 billion, testing capital markets for PCB makers. ([Bloomberg Tech](https://www.bloomberg.com/news/articles/2026-10-12/dongshan-said-to-gauge-demand-for-up-to-3-billion-hk-listing))




_Tell us how to make Semi Doped better![ Give us your feedback](<../_img/2026-10-12--daily-update-october-12th-2026/002_poll> "http://semidoped.com/poll")! ❤️_

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-october-12th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
