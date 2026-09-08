---
source: https://daily.semidoped.com/p/daily-update-june-30th-2026
title: Daily Update - June 30th, 2026
date: 2026-06-30
kind: clipping
genre: daily
audience: everyone
subtitle: Anthropic Claude on Azure, Taiwan raids Super Micro, Digital Realty acquires Blackstone stake, Bolt Graphics video, Meituan open-sources trillion-parameter model
---
News is a bit light today. We could use some days like this where not too much happens. It’s good when the “news of the day” is a Chinese food delivery company training trillion parameter frontier-class models. 

Or did we just miss something important? FOMO is real. Let us know in the comments.

Let’s get into it. _— Austin & Vik_

* * *

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast playe_

### Anthropic Claude Reaches General Availability on Azure

Anthropic’s Claude models are now generally available on Microsoft Azure via Microsoft Foundry, running on NVIDIA GB300 Blackwell Ultra GPUs. The deployment targets enterprise customers building agentic AI applications and domain-specific agents within Azure-native environments. ([Nvidia News](https://blogs.nvidia.com/blog/anthropic-nvidia-gb300-blackwell-ultra-microsoft-azure/))

> _**Austin:** Anthropic is a new TAM for Nvidia here… used to only be on Trainium._

### Taiwan Raids Super Micro in Nvidia GPU Export Probe

Taiwan authorities raided Super Micro’s offices as part of an investigation into alleged smuggling of Nvidia GPUs to China in violation of U.S. export controls. The probe is part of a broader Taiwan crackdown on chip export circumvention. Super Micro said it is cooperating with authorities. SMCI shares fell roughly 7% on the news. ([Bloomberg.com](https://www.bloomberg.com/news/articles/2026-06-29/super-micro-office-raided-as-taiwan-expands-chip-smuggling-probe), [Stocktwits](https://stocktwits.com/news-articles/markets/equity/smci-stock-taiwan-raids-super-micro-offices-ai-chip-export-probe/cZ19jVKR7LS))

> _**Vik:** This was a whole thing in late March of this year, where NVIDIA GPUs were smuggled into China by swapping shipping labels on rack servers. The CEO later [issued a letter](https://ir.supermicro.com/news/news-details/2026/A-Letter-From-CEO-Charles-Liang-2026-LfRyW8BDwq/default.aspx) saying that this was not Super Micro’s intention, and that the “three individuals” responsible for this violation have been “taken action against.” _

### Meituan Open-Sources Trillion-Parameter Model Trained on Chinese Chips

Meituan has open-sourced LongCat-2.0, a 1.6 trillion-parameter large language model with a 1 million-token context window, trained entirely on domestic Chinese chips. The Beijing-based food delivery company claims it is China’s first trillion-parameter model trained on home-grown hardware rather than imported GPUs, placing it on par with DeepSeek’s latest flagship by parameter count. ([SCMP](https://www.scmp.com/tech/tech-trends/article/3358854/china-debuts-biggest-ai-model-trained-local-chips-meituan-releases-longcat-20?utm_source=rss_feed))

> _**Vik:** Food delivery companies in China are now training AI models? Who is delivering food then? Apparently its near frontier performance from 50k Chinese accelerators._
> 
> _**Austin:** Food delivery used to be the side hustle. Now training AI models is._

### Palantir, NVIDIA Integrate Nemotron Models Into Sovereign AI Platform for US Agencies

Palantir and NVIDIA have expanded their AI partnership, integrating NVIDIA’s Nemotron open models into Palantir’s Sovereign AI Operating System. The system targets US government agencies and critical infrastructure operators that require on-premises deployment, allowing them to train and run models without transferring sensitive data to public cloud environments. ([EE News Europe](https://www.eenewseurope.com/en/palantir-nvidia-ai-us-agencies/))

> _**Vik:** Keeping sensitive data close to the chest is going to become more and more important in the world of AI. There is too much risk of info leak or distillation if AI is used by high profile organizations on the open internet. _
> 
> _**Austin:** My ears perk up anytime I see mention of Nemotron. As a merchant silicon vendor making training systems, it makes sense to train your own models to deeply understand your customers and test your systems. But deploying them? After you’ve invested all the depreciation and OpEx for training Nemotron, might as well get some use out of it! Not sure if Nvidia makes any money directly sharing Nemotron, but surely brand goodwill at a minimum._

### Samsung Electro-Mechanics Expands AI Server Substrate Capacity in Busan

Samsung Electro-Mechanics will expand flip chip ball grid array (FC-BGA) substrate production at its Busan facility to meet AI server demand, with a further capacity increase at its Sejong plant also expected. Samsung Electronics Executive Chairman 

### Digital Realty Acquires Blackstone’s Stake in Three Northern Virginia Data Centers

Digital Realty (NYSE: DLR) agreed to purchase Blackstone’s interest in three fully-leased hyperscale data centers in Northern Virginia, increasing its ownership in assets in the top U.S. data center market. To fund the acquisition, Digital Realty priced an underwritten secondary offering of approximately 12.31 million shares of common stock. ([Digital Realty](https://investor.digitalrealty.com/news-releases/news-release-details/digital-realty-prices-secondary-offering-common-stock-blackstone))

> _**Austin:** Stock down on the news._

## Worth a Watch

**[Bolt Graphics’ GPU Architecture and Plan to Challenge Nvidia with Founder Darwesh Singh](https://www.youtube.com/watch?v=-fZM9wOvbh0)** — Gamers Nexus

Gamers Nexus sat down with Bolt Graphics founder Darwesh Singh, a US startup taking a genuinely strange swing at the GPU market. Bolt’s card is RISC-V and chiplet-based, with user-expandable memory (two standard DDR5 SODIMM slots, so you choose your own 8 to 48GB DIMMs), dual PCIe, and an onboard Ethernet jack. 

The plan is to go where Nvidia is pulling back, winning over creative pros first and gamers later, and to prioritize path tracing over rasterization instead of chasing raw frame rates. Singh walks the roadmap (FPGA prototype today, 5nm tapeout by year end, mass production end of next year) and is candid that the hardest part is the same one Intel is still fighting: drivers and software.

> _**Austin:** It’s natural for the world’s largest accelerator companies to focus on datacenter AI and toward the future Physical AI S-curve. It’s also expected for startups to move in for a foothold where attention has waned. Bolt is bringing more acceleration to the workstation for creative professionals, simulations, high-performance, etc. You like FP64? _

[Transcript on Chipstrat](https://www.chipstrat.com/p/bolt-graphics-gpu-architecture-and-d03)

## Sector Watch

### AI & Compute

  * **Meta** deployed a custom CXL ASIC to pool memory from decommissioned servers, bypassing HBM supply constraints for inference workloads. ([The Register](https://www.theregister.com/systems/2026/06/29/zuck-saves-meta-bucks-by-reusing-memory-from-old-servers-with-a-custom-cxl-asic/5263483))

  * **Global AI sales** reached $25B in Q1 2026, exceeding $21B in data center depreciation costs but leaving margins critically thin. ([TechMeme](https://www.techmeme.com/260625/p21#a260625p21))




### Memory

  * **SEMI** projects 300mm memory equipment spending to exceed $50B in 2026, driven by HBM and DRAM capacity expansion for AI workloads. ([semi.org](https://www.semi.org/en/semi-press-release/semi-projects-300mm-memory-equipment-investment-to-surpass-50-billion-dollars-in-2026))




### China & Policy

  * **CXMT** secured ~$3B three-year server DRAM supply agreement with Tencent, with SemiAnalysis projecting $55B revenue this year at 75%+ gross margins ahead of IPO. ([TechMeme](https://www.techmeme.com/260629/p12#a260629p12))

  * **CXMT** signed 20B yuan supply deal with Tencent while in talks with Alibaba Cloud, ByteDance, and Xiaomi; Apple sources CXMT DRAM exclusively for Chinese market. ([chosun.com](https://www.chosun.com/english/industry-en/2026/06/28/WYWWI4BNHRCZPBOLA46CCN6G24/))

  * **Baidu’s Kunlunxin** seeks $50B Hong Kong IPO valuation while requiring investors to commit to purchasing its AI chips. ([DigiTimes](https://www.digitimes.com/news/a20260629VL214/chips-baidu-ipo-subsidiary-market.html))




### Foundry & Logic

  * **South Korea** unveiled $880B AI and semiconductor investment megaproject led by Samsung and SK Hynix to cement memory and logic market dominance. ([Bloomberg Tech](https://www.bloomberg.com/news/videos/2026-06-29/samsung-sk-hynix-at-center-of-south-korea-s-ai-drive-video))

  * **Apple** to launch first touch-screen MacBook with M5 Pro and M5 Max silicon, skipping M6 generation entirely and jumping to M7 for 2027 models. ([co.uk](https://www.silicon.co.uk/workspace/mac/apple-skip-m6-630501))Jay Y. 




## Stock Movers

 _At close on June 29th, 2026._

  * **ALAB** ▲ +16.4% — Astera Labs debuted in the Nasdaq-100 index, triggering mandatory buying from passive funds benchmarked to the index.

  * **ALGM** ▲ +14.7% — Mizuho raised Allegro MicroSystems’ price target citing AI data center demand, pushing shares to a new all-time high.

  * **ACMR** ▲ +13.8% — Morgan Stanley maintained its Overweight rating on ACM Research, catalyzing a sharp single-session surge in the semiconductor equipment maker.

  * **MXL** ▲ +12.3% — _no clear catalyst from public sources_

  * **KLAC** ▲ +12.0% — _no clear catalyst from public sources_

  * **WDC** ▲ +11.2% — Micron fell 5% and SanDisk dropped 7% while Western Digital outperformed, as investors favored its diversified storage business over pure-play NAND peers.




### Press Releases

  * **Google** Gemini can now take notes in Google Meet for Google AI Pro and Ultra subscribers. ([Google IR, June 28](https://blog.google/products-and-platforms/products/workspace/take-notes-for-me/))




Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-june-30th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
