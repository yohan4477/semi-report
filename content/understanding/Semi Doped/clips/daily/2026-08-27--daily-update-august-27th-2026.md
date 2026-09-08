---
source: https://daily.semidoped.com/p/daily-update-august-27th-2026
title: Daily Update - August 27th, 2026
date: 2026-08-27
kind: clipping
genre: daily
audience: everyone
subtitle: Nvidia guides 70% growth, agrees to buy Hugging Face for $12.9B, adds NVHBM to NVLink Fusion; AWS adds 2M GPUs for 2027-28; Kioxia and SanDisk commit $31B to NAND.
---
**Hello world, it’s Thursday, August 27th.**

Nvidia, Nvidia, Nvidia. 

Nvidia reported fiscal Q2 results Wednesday and guided for roughly 70% revenue growth, with AI spending visibility stretching through 2028. Nvidia allegedly agreed to buy Hugging Face for $12.9 billion, per The Information. Also, Nvidia added NVHBM to NVLink Fusion, a custom HBM that moves the memory controller into the base die, with Amazon’s Annapurna first in line. 

On the supply side, AWS and Nvidia are committing 2 million additional GPUs to data centers in 2027 and 2028, Anthropic locked in a six-year $45 billion deal alongside that, and Kioxia and SanDisk announced a joint $31 billion NAND expansion in Japan.

Let’s get into it. _— Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

_Tell us how to make Semi Doped better![ Give us your feedback](http://semidoped.com/poll)! ❤️_

### Nvidia Projects 70% Revenue Growth, Sees AI Spending Running Through 2028

Nvidia’s fiscal second-quarter results, released Wednesday, came with a forward-revenue forecast that stopped the duration debate cold. The company [guided for roughly 70% sales growth](https://www.reuters.com/business/media-telecom/nvidia-forecasts-quarterly-revenue-above-estimates-2026-08-26/) in fiscal 2027 and told investors the AI spending surge extends into 2028, giving hyperscalers and sovereign buyers no credible off-ramp. Shares dipped briefly after the print before recovering, with Nasdaq futures turning higher as the guidance rippled through markets. Mizuho analyst Vijay Rakesh said Wall Street is now [drilling into Nvidia’s own capital spending](https://www.bloomberg.com/news/articles/2026-08-26/mizuho-s-rakesh-sees-wall-street-drilling-in-on-nvidia-spending) as a proxy for conviction in that timeline. Every supplier in the compute, memory, and networking stack is repricing capacity against a longer build cycle than most had modeled.

> _**Austin:**_ _Rubin is probably going to be the fastest revenue ramp in history. And full-stack Vera Rubin is $40B/GW according to Jensen on the call, so that clearly helps. Also interesting to hear CPUs is a $20B/yr business; some of that is as a host CPU, the rest is standalone Vera racks. Don’t forget that enterprise GenAI is still growing (although its a bit fuzzy as it’s wrapped into ACIE with neoclouds). And robotics/autonomous vehicles still have plenty of growth ahead. Nvidia is doing just fine._

### AWS Adds 2 Million Nvidia GPUs for 2027-2028; Anthropic Signs $45 Billion Nscale Deal

AWS will [deploy 2 million additional Nvidia GPUs](https://nvidianews.nvidia.com/news/aws-and-nvidia-to-deliver-2-million-additional-gpus-and-next-generation-infrastructure-for-agentic-and-physical-ai) across its global infrastructure in 2027 and 2028, on top of the more than 1 million it already planned to add starting in 2026. The new capacity spans Blackwell Ultra, Rubin, and Rubin Ultra GPUs, plus Vera CPU-based infrastructure, and 100,000 of the GPUs go into secure U.S. government infrastructure for federal and national-security workloads. Nvidia’s release also confirms AWS will adopt NVLink Fusion with Nvidia’s new NVHBM custom high-bandwidth memory (next story). Next door, Anthropic has signed a [six-year, $45 billion compute contract with Nscale](https://www.bloomberg.com/news/articles/2026-08-26/anthropic-to-pay-nscale-45-billion-for-ai-computing-power), committing to a non-hyperscaler AI infrastructure provider at a price that dwarfs most cloud deals on record. Together the two deals shift GPU acquisition from opportunistic spot purchasing toward multi-year infrastructure commitments, raising baseline utilization floors for the entire GPU cloud market.

> **Austin:**_Obviously the zero-sum GPU vs XPU mindset is wrong. AWS deployed over one million Tranium 2s, and Trainium3 is shipping and Trainium4 is on the roadmap. Yet AWS still bought *checks notes* a couple million more Nvidia GPUs._

### Nvidia Moves the HBM Controller Into the Base Die With NVHBM; Amazon’s Annapurna Is First

Nvidia [expanded NVLink Fusion with NVHBM](https://blogs.nvidia.com/blog/nvlink-fusion-nvhbm-custom-high-bandwidth-memory/), a high-bandwidth memory variant that puts Nvidia’s custom memory controller into the HBM base die instead of on the XPU. Nvidia claims up to 30% more memory bandwidth, 15% lower HBM power, and up to 25% more free area on the XPU compute die versus standard HBM4E, using the same technology it will use in its own future GPUs. Nvidia is defining a standard NVHBM implementation to be validated and sold by multiple memory vendors, so NVLink Fusion customers qualify one memory design across suppliers. Amazon’s Annapurna Labs is the first partner, and will support NVLink Fusion on Trainium starting with Trainium4 so Amazon chips and Nvidia GPUs share a rack-scale architecture. “NVHBM represents a new architectural approach to advancing high-bandwidth memory performance and efficiency,” said Nafea Bshara, vice president of Annapurna Labs.

> _**Austin:** The HBM4 custom base die is yet another opportunity for Nvidia to sell a little bit more content. _

### Kioxia and SanDisk Commit $31 Billion to Kitakami NAND Expansion Amid YMTC Push

Kioxia and SanDisk have [announced a joint investment exceeding $31 billion](https://www.wsj.com/tech/kioxia-sandisk-to-invest-more-than-31-billion-in-memory-chips-bb6bddbf) in NAND flash memory production in Japan, centered on a new Fab3 facility at Kioxia’s Kitakami plant in Iwate Prefecture. Kioxia’s own announcement describes Fab3 as an expansion of its [3D flash memory production capacity](https://www.businesswire.com/news/home/20260827613046/en/Kioxia-to-Expand-3D-Flash-Memory-Production-Capacity-with-the-New-Fab3-at-Kitakami-Plant) at Kitakami, adding a third building to a complex that already houses two operating fabs. The scale of the commitment reflects mounting pressure from YMTC, the Chinese state-backed chipmaker that has publicly targeted surpassing Samsung and SK Hynix in NAND by 2027, according to The Korea Herald. Seoul Economic Daily frames the investment explicitly as a response to Kioxia falling behind YMTC on capacity. Digitimes notes YMTC faces its own hurdles, including equipment access constraints tied to U.S. export controls, though the Chinese firm’s domestic market share has grown steadily regardless.

### Synopsys Raises Full-Year Outlook After Q3 Revenue Tops $2.47 Billion

Synopsys reported [third-quarter revenue of $2.477 billion with GAAP EPS of $2.84](https://www.quiverquant.com/news/Synopsys+Q3+Revenue+Reaches+%242.477+Billion+as+GAAP+EPS+Hits+%242.84), beating analyst expectations and prompting management to lift its full-year 2026 guidance. The results arrived against a backdrop of accelerating custom ASIC development by hyperscalers and rapid chiplet adoption, both of which require intensive front-end EDA work before a single wafer is started. Synopsys raised its full-year outlook on the strength of what executives described on the earnings call as sustained demand for AI chip design tools. EDA vendors sit unusually early in the semiconductor supply chain: tool spending precedes tape-out by months, giving Synopsys relatively durable revenue visibility even as broader chip-market cycles remain uneven. Design complexity at advanced nodes keeps that demand compounding.

> _**Austin:** OpenAI’s Jalapeño is the existence proof that GenAI for EDA is real and transformative._

### Nvidia Agrees to Buy Hugging Face for $12.9 Billion

Nvidia has _allegedly_ agreed to [buy Hugging Face for $12.9 billion](https://www.theinformation.com/articles/nvidia-agrees-buy-open-source-model-repository-hugging-face-12-9-billion), according to The Information, citing a person with knowledge of the agreement. Hugging Face was recently generating about $150 million in annualized revenue, up from roughly $100 million a couple of months earlier, so Nvidia is paying about 80 times forward revenue. Google, Microsoft, Amazon, and Nvidia had all previously invested in the company, and talks began after interest from another suitor; Salesforce was among the investors with interest. The Information’s read is that Nvidia wants a plethora of successful open models as a counterweight to closed-model labs building their own chips, the same logic behind its Nemotron open-model program, its $6 billion Poolside license deal last week, and this summer’s Kumo AI and Essential AI acquisitions. Nvidia disclosed Wednesday that it holds $99 billion in equity investments with another $25 billion committed as of the end of July. Business Insider had earlier reported the two were in talks.

### Nvidia Ships First H200 Processors to China Under US Export License

Nvidia has [confirmed its first H200 data-centre chip shipments to China](https://www.scmp.com/tech/big-tech/article/3365383/nvidia-ships-first-h200s-china-forecasts-no-data-centre-computing-revenue?utm_source=rss_feed) under a licensing framework Washington approved in January, ending a stretch in which the company reported zero Hopper-architecture deliveries to the country. The sales were not nothing, but they were close: revenue came in at under 1 percent of Nvidia’s $89 billion data-centre total for the fiscal second quarter ended July 26. Nvidia offered no forecast for data-centre compute revenue from China going forward, a caveat that puts a hard ceiling on how much weight investors can assign to the resumption. The previous quarter had shown a clean zero for Hopper shipments to China, making even a sub-1-percent figure a directional change worth marking.

### Sector Watch

#### Compute & Custom Silicon

  * **Meta** unveils MTIA 400 at Hot Chips 2026 with a dual-purpose architecture serving both AI model training and ad-ranking inference, the first MTIA generation to target training workloads. ([The Register](https://www.theregister.com/systems/2026/08/26/metas-new-mtia-400-chip-has-a-split-personality-training-ai-and-serving-ads/5292727))

  * **Microsoft** presents Maia 200, its second-generation server AI inference processor, at Hot Chips 2026 with new architectural details. ([ServeTheHome](https://www.servethehome.com/microsofts-maia-200-accelerator-at-hot-chips-2026/))

  * **BOS Semiconductors** showcases its Eagle-N AI accelerator at Hot Chips 2026, marking a public debut for the Korean chip startup’s inference silicon. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13382))




#### Foundry & Packaging

  * **AMD** and **Broadcom** have booked most of Powertech’s FOPLP capacity ahead of the 2027 production ramp, per DigiTimes, locking in early slots for panel-level packaging. ([digitimes](https://www.digitimes.com/news/a20260827PD215/foplp-powertech-capacity-2027-amd.html))

  * **JCET** South Korean factory deepens its Samsung supply partnership as the Chinese OSAT expands advanced packaging ties with leading memory makers, per 36Kr. ([36 Kr](https://eu.36kr.com/en/p/3957224303934595))




#### Memory

  * **SK Hynix** breaks ground on its Indiana fab, a landmark step for the company’s US HBM and DRAM manufacturing footprint. ([SK Hynix](https://news.skhynix.com/en/indiana-fab-groundbreaking/))

  * **CXMT** DDR5 closes to within 1% of SK Hynix at 8,000 MT/s on third-party benchmarks, a significant milestone for China’s leading DRAM challenger. ([digitimes](https://www.digitimes.com/news/a20260827VL209/cxmt-ddr5-sk-hynix-memory-chips-performance.html))

  * **Qualcomm** says Samsung and SK Hynix are backing development of its High-Bandwidth Cache standard alongside HBM, broadening the memory ecosystem around mobile and edge AI chips. ([thelec.net](https://www.thelec.net/news/articleView.html?idxno=13402))




#### Power

  * **LS ELECTRIC** and **GE Vernova** announce a joint venture to develop voltage-source converter HVDC systems, combining Korean grid expertise with GE’s power infrastructure platform. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13342))

  * **Iron Device** presents an ultra-compact GaN power IC at PCIM Asia 2026 in Shenzhen, targeting high-density power conversion for AI and industrial applications. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13383))

  * **Bloom Energy** reports record revenue and raises full-year guidance, citing accelerating AI data-center demand for its solid-oxide fuel-cell power systems. ([Bloom Energy](https://www.ad-hoc-news.de/boerse/news/unternehmensnachrichten/bloom-energy-s-ai-fueled-ascent-record-revenue-raised-guidance-and-a/70008803))




#### Optics & Networking

  * **Innolight** raises an additional $7.94 billion via greenshoe option following its Hong Kong listing, capitalizing on surging AI-driven transceiver demand. ([The Standard (HK)](https://www.thestandard.com.hk/finance/article/341097/Chinese-optical-part-maker-Zhongji-Innolight-raises-extra-794b-via-greenshoe-option))

  * **Japan** secures global ITU-T Y.3335 standard for all-photonics networks, a joint effort by KDDI, NTT, Rakuten Mobile and four other Japanese carriers. ([Light Reading](https://www.lightreading.com/optical-networking/japan-secures-global-itu-t-standard-for-all-photonics-networks))

  * **Lumen** expands cloud networking access to more than 10 million US business locations, extending AI and cloud connectivity reach across its enterprise fiber footprint. ([Light Reading](https://www.lightreading.com/ai-machine-learning/lumen-expands-cloud-networking-access-to-more-than-10m-u-s-business-locations))




#### Edge & Robotics

  * **Renesas** opens a Physical AI & Robotics Lab in Beijing targeting next-generation robotics SoC co-development with Chinese ecosystem partners. ([Business Wire](https://www.businesswire.com/news/home/20260826040795/en/Renesas-Establishes-Physical-AI-Robotics-Lab-in-Beijing-to-Accelerate-Next-Generation-Robotics-Innovation))

  * **Geniatech** expands its edge AI portfolio with a new Renesas RZ/V2N OSM-M module targeting thermally constrained vision applications. ([The Manila Times](https://www.manilatimes.net/2026/08/26/tmt-newswire/plentisoft/geniatech-expands-edge-ai-portfolio-with-new-renesas-rzv2n-osm-m-module-for-thermally-constrained-vision-applications/2412691))

  * **LetinAR** is expanding optical module production capacity fivefold in preparation for an anticipated AI glasses market opening, per The Elec. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13379))




#### Data Centers

  * **SK Telecom** launches AI data center infrastructure spinout ‘SK Horizon’ with anchor investments from KKR and IMM, creating a dedicated vehicle to monetize Korea’s AI buildout. ([PR Newswire](https://www.prnewswire.com/news-releases/sk-telecom-launches-ai-data-center-infrastructure-company-sk-horizon-and-secures-investments-from-kkr-and-imm-302861694.html))

  * **Alibaba** launches its first data centers in South America with a Brazil deployment, marking the Chinese cloud giant’s entry into the Latin American AI infrastructure market. ([SCMP](https://www.scmp.com/tech/big-tech/article/3365491/alibaba-pushes-south-americas-ai-market-launch-brazil-data-centres?utm_source=rss_feed))

  * **Core Scientific** adds $600 million in new credit facilities to accelerate its AI data center buildout as demand for dedicated GPU infrastructure intensifies. ([TheEnergyMag](https://theenergymag.com/news/market-news/core-scientific-600-million-credit-ai-infrastructure))




#### Policy & Trade

  * **Z.ai** shares surge 8% after releasing a new AI model running entirely on Chinese chips, signaling commercial viability of domestic silicon for frontier inference. ([CNBC](https://www.cnbc.com/2026/08/27/zai-shares-surge-new-ai-model-using-chinese-chips.html))

  * **YMTC** ‘s Wuhan semiconductor ecosystem expands with 17 new companies and RMB 6 billion in committed projects, deepening the supply chain around China’s leading NAND maker. ([TechNode](https://technode.com/2026/08/27/yangtze-memorys-wuhan-semiconductor-ecosystem-expands-with-17-companies-and-rmb6-billion-in-projects/))

  * **IBM** completes acquisition of HRL Laboratories, adding silicon-spin qubit technology and advanced research capabilities to its quantum computing program. ([EE News Europe](https://www.eenewseurope.com/en/ibm-acquires-hrl-laboratories-to-boost-quantum-technologies/))




_Tell us how to make Semi Doped better![ Give us your feedback](http://semidoped.com/poll)! ❤️_

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-august-27th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
