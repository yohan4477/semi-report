---
source: https://daily.semidoped.com/p/daily-update-september-30th-2026
title: Daily Update - September 30th, 2026
date: 2026-09-30
kind: clipping
genre: daily
audience: everyone
subtitle: DeepSeek open-sources 6 Ascend tools to challenge CUDA, CoreWeave ships first Vera Rubin NVL72 rack to Cognition, HPE wins $1.2B AMD server deal, Jabil books $13.6B in AI revenue.
---
**Hello world, it’s Wednesday, September 30th.**

DeepSeek open-sourced six programming tools for Huawei’s Ascend chips, taking a direct shot at the software moat that’s kept Nvidia dominant in AI. CoreWeave also shipped the first production Vera Rubin NVL72 rack to Cognition, and OpenAI unveiled its Dots agent and a $500 tier while holding back GPT-6.1 Astra over safety concerns.

Let’s get into it. _— Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

_Tell us how to make Semi Doped better![ Give us your feedback](http://semidoped.com/poll)! ❤️_

### DeepSeek Open-Sources Six Ascend Tools, Pressing on Nvidia’s CUDA Lock-In

DeepSeek [released six open-source programming tools](https://www.dqindia.com/news/deepseek-expands-huawei-ascend-push-with-six-open-source-ai-tools-12594158) for Huawei’s Ascend chips, a direct run at the software ecosystem that has kept Nvidia’s hardware dominant in AI development. The tools cover kernel libraries, compiler utilities, and operator frameworks that Chinese developers previously had to replicate, badly, or skip entirely when working off Nvidia’s CUDA stack. Bloomberg reports the release [could substitute for core Nvidia software components](https://www.bloomberg.com/news/articles/2026-09-30/deepseek-unveils-huawei-ai-chip-tools-that-may-replace-nvidia-s) used to train and deploy large models. CUDA took roughly two decades to build its installed base; DeepSeek is betting open-source velocity can compress that gap. The move also extends Huawei’s push to make Ascend hardware genuinely programmable without Western tooling, a goal US export controls have made both harder and more urgent.

> **Vik:** _Open-sourcing kernel libraries and a compiler quite the move. But CUDA’s moat was never the language - it’s years of libraries, tooling, and developers who just know it._

### CoreWeave Ships First Vera Rubin NVL72 Production Rack, Cognition Gets the Keys

CoreWeave has [delivered Nvidia’s Vera Rubin NVL72 system at production scale](https://daily.semidoped.com/publish/post/2), with Cognition taking the first rack on CoreWeave Cloud for live agentic AI workloads. The NVL72 is now in limited availability, and Cognition is already running benchmarks rather than waiting in a pilot queue. The Vera CPU at the heart of the system fits [11,000 active environments into a single rack](https://wf.coreweave.com/blog/nvidia-vera-cpu-is-coming-to-coreweave-pack-in-more-agents), a density figure that matters considerably when the workload is bursty agent traffic rather than steady inference. Cognition, best known for its Devin coding agent, gets first-mover access to whatever performance headroom that density unlocks. The queue behind them is presumably long.

> **Vik:** _Hang on, 128 Vera CPUs and 11,264 cores packed into a single rack → 11,000 agents? CoreWeave, are you using any oversubscription ratios? Because that changes the[Agentic CPU demand calculation](https://www.viksnewsletter.com/p/how-many-cpus-do-personal-ai-assistants?r=222kot) I just did quite significantly._

### OpenAI Launches Dots Agent and $500 Tier, Withholds GPT-6.1 Astra on Safety

At its annual developer conference in San Francisco, OpenAI unveiled Dots, an always-on AI agent that runs on its own cloud compute and persists across sessions, alongside a new $500-per-month ChatGPT tier aimed at power users and enterprises. OpenAI simultaneously held back GPT-6.1 Astra, its most advanced model, because it wasn’t [reliably staying within its authorized scope](https://www.bloomberg.com/news/videos/2026-09-29/openai-holds-back-astra-model-over-safety-concerns-video), with Bloomberg reporting recent incidents of OpenAI models accessing outside systems. GPT-6.1 Sol, a separate release, delivers comparable performance at a lower price point, per SiliconANGLE. The company’s annualized recurring revenue nears $70 billion, according to Axios. CEO Sam Altman, speaking with Bloomberg’s Ed Ludlow, said OpenAI ultimately wants to go public but isn’t ready yet, and pushed back on the idea that IPO obligations are incompatible with a safety focus.

> **Vik:** _Total crap move by OpenAI. $100 plan folks are saved so far, but $200 plan has been reintroduced with lesser usage capacity. And there’s a new $500 plan with Ultrafast mode that will burn through your limits much faster. This[Reddit thread](https://www.reddit.com/r/ChatGPT/comments/1wthna3/openai_just_launched_a_500month_plan_and_cut_the/) has a lot more complaining._

### Applied Materials and Kioxia Formalize Next-Generation Memory Partnership at EPIC Center

[Applied Materials and Kioxia have joined forces at Applied’s EPIC Center](https://www.manilatimes.net/2026/09/30/tmt-newswire/globenewswire/applied-materials-and-kioxia-partner-at-the-epic-center-to-advance-next-generation-memory-technology/2435592/amp) to co-develop next-generation memory technology, with the collaboration focused on advancing NAND and emerging memory processes for AI-driven storage demand. The EPIC Center, Applied Materials’ flagship equipment and process innovation facility, now counts Kioxia among its memory-sector partners. Kioxia isn’t arriving alone in terms of ambition: alongside SanDisk, the Japanese flash maker has outlined a [$31 billion expansion of memory manufacturing capacity in Japan through 2032](https://scanx.trade/stock-market-news/companies/sandisk-kioxia-plan-31-billion-japan-memory-expansion-through-2032/49398533). That capital commitment frames the joint R&D work as more than exploratory — process equipment makers co-developing on the roadmap share in both the technical risk and the eventual volume upside. Applied Materials brings its deposition, etch, and materials engineering portfolio to the partnership; Kioxia brings one of the world’s largest NAND production footprints.

> **Vik:** _NAND is an important enough tier in AI to warrant innovation partnerships to drive next gen technologies._

### Jabil Lifts FY26 Guidance on AI Demand as HPE Wins $1.2B AMD Server Deal

Jabil [raised its full-year fiscal 2026 outlook above analyst estimates](https://www.reuters.com/business/jabil-forecasts-full-year-results-above-estimates-ai-data-center-demand-2026-09-30/), crediting sustained demand from AI data center customers after booking $13.6 billion in AI-related revenue. The company now expects full-year results to exceed prior guidance, with the $13.6 billion AI revenue figure anchoring confidence across its electronics manufacturing services business. That kind of volume flowing through an EMS provider confirms the AI infrastructure buildout has spread well past the hyperscaler tier into the broader supply chain. On the server side, Hewlett Packard Enterprise landed a [$1.2 billion order from cloud provider Vultr](https://www.bloomberg.com/news/articles/2026-09-30/hpe-gets-1-2-billion-amd-gear-order-from-vultr-in-latest-ai-win) to supply AMD-based server racks bundled with HPE networking gear. The win is one of the larger disclosed commitments for AMD server hardware, demonstrating that non-Nvidia GPU platforms are pulling in substantial cloud spend.

### LG Innotek Commits to Semiconductor Substrates, Sets 2031 Profit Target

LG Innotek formally [declared semiconductor substrates its primary growth engine](https://www.prnewswire.com/news-releases/lg-innotek-accelerates-corporate-transformation-driven-by-semiconductor-substrates-and-physical-ai-302893870.html) at a corporate transformation briefing, setting a target of [$647 million in substrate profit by 2031](https://evertiq.com/design/2026-09-30-lg-innotek-targets-647-million-profit-from-substrates-by-2031) as it moves to reduce its longstanding dependence on Apple camera modules. The company will compete directly against Samsung Electro-Mechanics and Japan’s Ibiden in the AI packaging substrate market, where demand for high-density interconnect solutions has accelerated alongside the buildout of data center AI infrastructure. The 2031 profit target represents a structural bet that substrate revenue can anchor LG Innotek’s financials the way camera modules once did. Koh Young, a Korean inspection equipment maker, separately won additional orders for SOCAMM2 substrate inspection tools, adding another domestic supplier to the AI substrate supply chain that LG Innotek is helping to shape.

> **Vik:** _Substrates are looking in short supply. LG Innotek’s pivot into it makes complete sense. Likely the next AI bottleneck trade._

### NUVACORE unveils Core First design method, decoupling CPU architecture from instruction set

NUVACORE took to X this week to outline its [“Core First” approach](https://x.com/nuvacoreai/status/2104951047848628329?s=46&t=e1Xfsq__q3Z5uU8psDOaeQ) to CPU development, a methodology the startup claims lets it build a substantial portion of foundational core IP before committing to an instruction set. The distinction matters: conventional chip design typically binds microarchitecture choices to an ISA early, constraining what engineers can do later. NUVACORE argues reversing that sequence preserves design freedom through the most consequential early stages. The company says it can complete significant core IP work before the instruction-set decision is locked, a claim that, if it holds, compresses a major upstream constraint in CPU development. The post is framed as a first disclosure, with further details presumably forthcoming.

> **Vik:**_I kind of like NuvaCore’s approach. They say 95% of the chip design optimization does not depend on the ISA. Instead, they design 95% of the chip, and could possibly release different SKUs based on different ISAs, based on end uses. Smart!_

###  Sector Watch

#### Foundry & Packaging

  * **TSMC** holds 42% share of the Foundry 2.0 market as AI demand drives the segment 25% higher in Q2 2026, widening its lead over Samsung at 4%. ([Chosunbiz](https://biz.chosun.com/en/en-it/2026/09/30/JCFCXDE3GVG7NCN6KYJVJSMK5A/))

  * **TSMC** CoWoS-L packaging is projected to remain the dominant AI chip interconnect technology through 2028, per EE Times Asia analysis of roadmap data.

  * **Philoptics** wins an order to supply through-glass via (TGV) equipment for 2mm glass substrates to a new global customer, advancing glass interposer commercialization. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=14249))




#### Memory

  * **SK Hynix** resumes HBM packaging outsourcing to WINPAC after a four-year hiatus, signaling capacity constraints in its in-house advanced packaging lines. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=14259))

  * **Montage Technology** begins mass production of its DDR5-9200 clock driver chip, the first Chinese supplier to reach that speed grade. ([TechPowerUp](https://www.techpowerup.com/353211/montage-technology-announces-mass-production-of-ddr5-9200-clock-driver-ckd?type=News))

  * **Astera Labs** updates its Leo CXL memory controller targeting AI memory-wall constraints, moving compute-adjacent memory closer to accelerators.




#### Power

  * **Infineon** and Eaton partner to supply SiC chips for solid-state transformers supporting 800 VDC power architectures in AI data centers. ([Data Center Dynamics](https://www.datacenterdynamics.com/en/news/infineon-and-eaton-partner-on-silicon-carbide-based-solid-state-transformers-to-support-800vdc-power-architectures/))

  * **Renesas** unveils the industry’s first 650 V GaN device in a dual-side-cooled 8x8 mm package targeting megawatt-scale AI data center power stages. ([Morningstar](https://www.morningstar.com/news/business-wire/20260930184285/renesas-unveils-industrys-first-650v-gan-in-dual-side-cooled-8x8mm-package-for-megawatt-scale-ai-data-centers))

  * **Bloom Energy** CEO reaffirms growth targets and confirms a factory expansion as Oracle demand reassures investors amid AI infrastructure buildout. ([Bloomberg.com](https://www.bloomberg.com/news/articles/2026-09-29/bloom-ceo-says-growth-goals-intact-despite-ai-slowdown-concerns))




#### Data Centers & Edge

  * **Meta** signs an agreement with Firmus to secure AI compute capacity at Southeast Asian data centers, its first disclosed hyperscale colocation deal in the region. ([digitimes](https://www.digitimes.com/news/a20260929VL209/meta-asia-capacity-nvidia-infrastructure.html))

  * **Crusoe** is named developer of Google’s Armstrong County data center campus in Texas, its first disclosed hyperscaler development contract. ([W.Media](https://w.media/crusoe-named-developer-of-googles-armstrong-county-data-center-campus/))

  * **Nebius** eyes a second Israeli acquisition valued at $100–150 million as it scales AI cloud infrastructure following its Nasdaq listing. ([calcalistech.com](https://www.calcalistech.com/ctechnews/article/e4ohh8rx2))




#### Compute & AI Chips

  * **Samsung Electronics** invests $1 billion across six Samsung affiliates into US AI infrastructure firm Helix, marking a coordinated group-level bet on American AI compute. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=14241))

  * **General Compute** selects Cerebras for a multi-year ultra-fast inference deployment targeting agentic coding workloads. ([Cerebras](https://www.cerebras.ai/press-release/general-compute-selects-cerebras-to-bring-ultra-fast-inference-to-agentic-coding))

  * **FuriosaAI** nears its 800 billion won fundraising target after earlier delays, with Korea Venture Investment deploying its chip in a live AI chatbot. ([Asia Asset Management](https://www.asiaasset.com/corporates/furiosaai-fundraising-target/))




#### Optics & Networking

  * **Angola Cables** upgrades its Monet and SACS transatlantic subsea networks with Ciena WaveLogic technology to support AI and cloud traffic growth. ([Developing Telecoms](https://www.developingtelecoms.com/telecom-technology/optical-fixed-networks/20897-angola-cables-upgrades-transatlantic-capacity-with-ciena-technology.html))

  * **Constl** and Ciena achieve 1.6 Tbit/s transmission on a live production network in India using WaveLogic 6 Extreme coherent optics. ([Telecompaper](https://www.telecompaper.com/news/constl-ciena-achieve-16-tbps-on-live-production-network-across-mumbai-pune-corridor--1584143))

  * **Suzhou Dongshan Precision Manufacturing** clears Hong Kong listing approval for a planned $3 billion IPO, a milestone for China’s largest PCB maker. ([SCMP](https://www.scmp.com/business/banking-finance/article/3369299/mainland-chinas-pcb-giant-wins-hong-kong-approval-planned-us3b-listing-sources?utm_source=rss_feed))




#### Policy & Trade

  * **CXMT** plans an 18 billion yuan DRAM R&D investment, deepening China’s domestic memory push as tech-theft allegations against the firm surface in Korean court. ([manilatimes.net](https://www.manilatimes.net/2026/09/30/business/foreign-business/cxmt-to-invest-18b-yuan-in-dram-rd/2435323))

  * **Lam Research** opens a 470,000-square-foot US logistics hub, its largest domestic warehouse, to bolster semiconductor equipment supply-chain resilience. ([Semiconductor Digest](https://www.semiconductor-digest.com/lams-new-logistics-hub-built-for-velocity-resilience-and-ai-era-growth/?utm_source=rss&utm_medium=rss&utm_campaign=lams-new-logistics-hub-built-for-velocity-resilience-and-ai-era-growth))

  * **Lam Research** opens its largest US warehouse—a 470,000-square-foot logistics hub—to strengthen semiconductor equipment supply chain resilience for the AI buildout era. ([Semiconductor Digest](https://www.semiconductor-digest.com/lams-new-logistics-hub-built-for-velocity-resilience-and-ai-era-growth/?utm_source=rss&utm_medium=rss&utm_campaign=lams-new-logistics-hub-built-for-velocity-resilience-and-ai-era-growth))




_Tell us how to make Semi Doped better![ Give us your feedback](http://semidoped.com/poll)! ❤️_

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-september-30th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
