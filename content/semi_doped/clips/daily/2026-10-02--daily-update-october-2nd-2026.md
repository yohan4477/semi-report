---
source: https://daily.semidoped.com/p/daily-update-october-2nd-2026
title: Daily Update - October 2nd, 2026
date: 2026-10-02
kind: clipping
genre: daily
audience: everyone
subtitle: Broadcom assembles $60B debt for Anthropic chips, DRAM DDR4 8Gb contract price hits $26, Micron says NVHBM will improve profitability.
---
**Hello world, it’s Friday, October 2nd.**

Broadcom is assembling $60 billion in debt to finance chip leases for Anthropic, the largest single AI infrastructure financing disclosed to date. Memory markets are also moving, with DRAM’s mainstream 8-gigabit DDR4 contract price up 4% month-on-month to $26, and Qualcomm’s Snapdragon X2 benchmarks are putting real pressure on Intel in premium laptops.

Let’s get into it. _— Austin & Vik_



 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

#### Presented by Crusoe

Crusoe builds AI infrastructure from the ground up — power, data centers, and the cloud on top.

If you’re running open models — GLM, DeepSeek, Kimi, Qwen — Crusoe’s managed inference is fast: up to 9.9x faster time-to-first-token and 5x the throughput of vLLM, thanks to their MemoryAlloy caching layer and tokenizer fastokens. And it’s the easy kind of fast: pick a model, grab an API key and start inference. No GPUs to provision, no infrastructure or clusters to manage, and it’s pay per million tokens.

**$5 in free credits** to try it. [Send your first request today →](https://console.crusoecloud.com/request-foundry?utm_source=podcast_host&utm_medium=audio&utm_campaign=pdsp_mi_su_semidoped-podcast)

### Broadcom Assembles $60 Billion Debt Pile to Finance Anthropic Chip Buildout

Bloomberg reports that Broadcom has begun [assembling $60 billion in debt financing](https://www.bloomberg.com/news/articles/2026-10-02/broadcom-starts-amassing-60-billion-to-fund-chips-for-anthropic) to fund chip leases for Anthropic, the largest single AI infrastructure financing disclosed to date. The structure, detailed in an SEC filing, has Broadcom lending Anthropic [up to $42 billion](https://www.reuters.com/business/broadcom-lend-anthropic-up-42-billion-lease-its-chips-filing-says-2026-10-01/) specifically to lease chips, with Anthropic issuing convertible notes in return. The chips in question include Google TPUs, creating a circular arrangement where Google’s hardware flows through Broadcom’s balance sheet to Anthropic. Anthropic’s own ten-year infrastructure ambitions run to $518 billion. A pre-IPO investor day is set for October 14, according to Bloomberg, adding immediate pressure to get the capital structure settled before that meeting.

> **Vik:** _Lending a customer up to $42 billion to lease chips you co-designed is circular financing in a bow - I tagged circular deals as[one of the horsemen that pops this buildout](https://www.viksnewsletter.com/p/the-four-horsemen-of-ai-infra). Anthropic’s own filing flags the conflict. But I don’t bet against Hock, and his ASIC book is what pays for all of it._

### DRAM and NAND Spot Prices Hit Records as Micron Touts NVHBM Margin Gains

[DRAM and NAND flash prices both reached record highs in September](https://www.thelec.net/news/articleView.html?idxno=14329), with TrendForce’s DRAMeXchange showing the mainstream 8-Gb DDR4 contract price climbing 4% month-on-month to $26, though the pace of gains eased from prior months. NAND posted a parallel move. Micron’s Scott J. DeBoer, president and chief technology officer, confirmed that NVHBM, the company’s custom high-bandwidth memory product developed for Nvidia, [will improve profitability even though the base die is manufactured externally](https://www.thelec.net/news/articleView.html?idxno=14372) rather than in-house. That admission is notable because outsourcing the base die to TSMC was the obvious cost pressure point critics flagged. Micron posted record annual results alongside the disclosure, with full-year DRAM revenue crossing $100 billion for the first time and operating margin exceeding 70% for the year.

> **Vik:** _You know why this is Micron cope?  
>   
>  A base die designed by NVIDIA, manufactured by TSMC, is somehow more profitable to Micron? If that's the case, profitable to whom? To Nvidia? It's NVLink fusion and their custom base die design, over their NVHBM IP. How much of this custom HBM value now flows to NVIDIA?  
>   
> I anticipated this cope a while ago on my Substack. Here's the whole thing:_
> 
> [![](<../_img/2026-10-02--daily-update-october-2nd-2026/001_a409d69d-ca10-4bfe-a1fc-f8d291690566_185x185.png> "https://substackcdn.com/image/fetch/$s_!9JlA!,w_56,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa409d69d-ca10-4bfe-a1fc-f8d291690566_185x185.png")Vik's NewsletterHow Custom Base Die Drives HBM Bandwidth, and Who Stands to BenefitA recent notable trend is that HBM performance is decoupling from stack height. Reports over the last month that Rubin Ultra drops HBM from 12-high to 8-high have been read as a supply/cost-driven downgrade, which is true. But the larger shift is that bandwidth, not capacity, is becoming the metric that matters in HBM. What sets HBM apart going forward is bandwidth performance via the custom base die, and value accrues to whoever designs it…Read morea month ago · 52 likes · Vikram Sekar](https://www.viksnewsletter.com/p/how-custom-base-die-drives-hbm-bandwidth?utm_source=substack&utm_campaign=post_embed&utm_medium=web&embedding_publication_id=8781267)

### Qualcomm Snapdragon X2 Benchmarks Pressure Intel in Premium Laptops

Qualcomm’s Snapdragon X2 generation arrived at the Snapdragon Summit 2026 in Maui with benchmark results that [outpace Intel’s Core Ultra](https://daily.semidoped.com/publish/post/1) at comparable or lower price points, putting direct pressure on Intel’s hold over premium Windows laptops heading into the 2027 refresh cycle. The X2 Elite and X2 Plus chips anchor a growing device lineup documented by Ultrabookreview, with OEM partners already committing hardware across multiple form factors. Qualcomm separately released a [Linux upstream preview for the X2 platform](https://www.infoq.com/news/2026/10/snapdragon-x2-linux/), a move aimed at ARM laptop developers who have long waited for mainline kernel support. The Apple licensing renewal provides Qualcomm near-term revenue stability even as iPhone chip volumes soften, freeing the company to sustain PC investment. Tirias Research analysts McGregor and Sideco, present at the Summit, called agentic AI the defining theme of the platform.

> **Vik:** _Funny we didn’t hear more BS about AI PCs. It’s all about Agents now. For now, Qualcomm might be right about edge devices becoming the central interface to AI. I still don’t buy that we will run any meaningful LLMs on the end. Maybe only to collect some data and send a “smarter” version to the cloud. Interesting that Apple renewed their licensing deal though — quite the lifeline for the moment._

### Amazon Moves to Securitize $8B in Nvidia Chips While Paying Communities to Accept Data Centers

Amazon is working to [offload roughly $8 billion worth of Nvidia chips](https://www.reuters.com/business/retail-consumer/amazon-seeks-offload-8-billion-nvidia-chips-investors-ft-reports-2026-10-02/) to outside investors, according to the Financial Times, a move that would shift the GPU inventory off its balance sheet as capital costs mount across its AI buildout. The structure would effectively convert hardware holdings into a financing arrangement with third parties. On the community side, AWS separately announced [“Built Together,” a five-year, $1 billion program](https://www.unite.ai/amazon-announces-built-together-program-for-data-center-communities/) committing funds to infrastructure, workforce training, and local grants in towns hosting data centers, after facing mounting permitting resistance and public opposition to new facilities. Amazon has also published blog posts warning communities that blocking data centers carries economic consequences.

> **Vik:** _The $1 billion community fund and the doom blog about moratoriums are the same move. Permitting and local pushback are now a real brake on the buildout, which I flagged as one of the ways this thing pops. Over 100 moratoriums being considered says it isn’t small._

### Huawei Claims Ascend Passed Nvidia in China as DeepSeek Tools Widen Moat

Huawei rotating chairman Ken Hu [told an audience that Ascend has surpassed Nvidia in China AI chip market share](https://www.geopolitechs.org/p/huawei-rotating-chairman-ascend-has), a claim the company did not quantify but delivered with evident confidence. The software wall around that position got thicker this week when DeepSeek and Huawei jointly [released open-source compute and communication libraries plus TileLang support for Ascend](https://www.tomshardware.com/tech-industry/artificial-intelligence/deepseek-and-huawei-release-open-source-ascend-ai-programming-tools-to-reduce-reliance-on-nvidia-ecosystem-tools-include-compute-and-communication-libraries-as-well-as-ascend-support-for-tilelang), giving developers a credible CUDA alternative without Nvidia’s toolchain. That combination, a domestic chip now claiming share leadership and an open-source developer ecosystem building around it, raises the switching cost for any hardware rival trying to re-enter the Chinese market. On the silicon side, Huawei’s Kirin 9050 Pro uses a LogicFolding architecture that stacks transistors vertically rather than shrinking them, sidestepping the process-node constraints that U.S. export controls were designed to exploit.

> **Vik:** _Nvidia’s China market share is already very low, which is why Jensen has been trying to get sales up in China, or at least saying that cutting off China from chips is a bad idea. You can see his point now though. Huawei is building chips rapidly, and China is building their own ecosystem which will be hard to penetrate later._

### Tavus launches Griffin model claiming first video Turing test pass

Tavus has unveiled Griffin, a real-time video AI model the company is calling the first Human Interaction Model, or HIM. In live testing, [48% of people who conversed with Griffin believed they were talking to a real human](https://x.com/tavus/status/2105704169009246248?s=46&t=e1Xfsq__q3Z5uU8psDOaeQ), compared to a pass rate below 3% for previous systems. The jump is stark: prior full-duplex video AI hadn’t come close to fooling a majority, or even a meaningful minority, of live participants. Tavus also claims Griffin ranks first on Nvidia’s benchmark for full-duplex AI video. The model targets conversational video applications where latency and natural cadence determine whether an interaction reads as human or machine.

> **Vik:**_See the AI talking in this tweet, it is quite believable actually._
> 
> [![X avatar for @tavus](<../_img/2026-10-02--daily-update-october-2nd-2026/002_ZFG0msxY.jpg> "https://substackcdn.com/image/fetch/$s_!sZ29!,w_40,h_40,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fpbs.substack.com%2Fprofile_images%2F1974200616399593472%2FZFG0msxY.jpg") Tavus@tavusIntroducing Griffin, the first model to pass the video Turing test. 48% of people who talked to it live thought it was a real human. Previous systems have had a pass rate <3%. It is #1 on NVIDIA's benchmark for full-duplex AI video. It’s the first Human Interaction Model (HIM). ![](<../_img/2026-10-02--daily-update-october-2nd-2026/003___ss-rehost__tw-video-preview-13_2105703934073683968.jpg> "https://substackcdn.com/image/fetch/$s_!AE1p!,w_1028,c_limit,f_auto,q_auto:best,fl_progressive:steep/l_play_button_usfui2,w_88,e_colorize:0/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F__ss-rehost__tw-video-preview-13_2105703934073683968.jpg")4:59 PM · Oct 1, 2026 · 12.4M Views
> 
> * * *
> 
> 2.24K Replies · 3.28K Reposts · 30.5K Likes](https://x.com/tavus/status/2105704169009246248?s=46&t=e1Xfsq__q3Z5uU8psDOaeQ)

### Sector Watch

#### Compute & Edge

  * **Nvidia** expands DGX Spark to a 64 GB unified-memory configuration, giving developers more headroom for local AI model development and scaling. ([Nvidia News](https://blogs.nvidia.com/blog/local-ai-dgx-spark-64gb-sync/))

  * **Tenstorrent** adds Smallest.ai as a partner to bring on-premises voice agents to its hardware platform, opening a new edge AI deployment path. ([Unite.AI](https://www.unite.ai/on-prem-voice-agents-get-new-hardware-path-as-smallest-ai-joins-tenstorrent/))

  * **Exascale** and Compal sign an agreement to jointly develop a platform for next-generation GPU systems, combining compute expertise with ODM manufacturing scale. ([Evertiq](https://evertiq.com/design/2026-10-02-exascale-compal-to-develop-platform-for-next-gen-gpu-systems))




#### Optics & Networking

  * **CtrlS** and Ciena partner to build 100 Tb/s metro optical networks across five Indian cities, targeting surging AI and cloud traffic demand. ([Prop News Time](https://propnewstime.com/latestnewsstories/Mzc1MjM=/ctrls-and-ciena-to-build-100-tb-s-metro-networks-across-five-indian-cities))

  * **AT &T**, T-Mobile, and Verizon launch a joint venture to close coverage gaps using satellite-enabled connectivity, naming Paul Roth interim CEO. ([Light Reading](https://www.lightreading.com/satellite/at-t-t-mobile-and-verizon-launch-joint-venture-that-helps-end-dead-zones-name-paul-roth-interim-ceo))




#### Data Centers

  * **Crusoe** files permits for a $4.8 billion data center campus in Jayton, Texas, its largest disclosed development footprint to date. ([Data Center Dynamics](https://www.datacenterdynamics.com/en/news/crusoe-files-for-48bn-data-center-campus-in-jayton-texas/))

  * **Core Scientific** terminates its $9 billion merger agreement with CoreWeave, ending one of the sector’s most closely watched consolidation bids. ([app.dealroom.co](https://app.dealroom.co/news/note/core-scientific-terminates-9b-merger-agreement-with-coreweave)) → This is kind of a big deal, no?




#### Policy & Trade

  * **MaxLinear** will report Q3 2026 financial results on October 22, hosting a conference call at 1:30 p.m. PT. ([MaxLinear](https://investors.maxlinear.com/news/detail/626/maxlinear-inc-announces-conference-call-to-review-third-quarter-2026-financial-results-thursday-oct-22-2026-at-1-30-p-m-pacific-time-4-30-p-m-eastern-time))

  * **US federal prosecutors** arrest a California man on charges of smuggling $300 million worth of Nvidia chip servers to China, exposing gaps in export-control enforcement. ([Bloomberg Tech](https://www.bloomberg.com/news/articles/2026-10-02/man-charged-by-us-with-illegally-shipping-nvidia-chips-to-china)) — Question: how did California man get Nvidia chips to begin with?

  * **China** stockpiles hundreds of ASML immersion lithography machines worth billions, intensifying US congressional calls for a complete tool export ban. ([SCMP](https://www.scmp.com/tech/tech-war/article/3369557/china-stockpiles-asml-lithography-tools-spurring-us-calls-complete-export-ban?utm_source=rss_feed))




_Tell us how to make Semi Doped better![ Give us your feedback](<../_img/2026-10-02--daily-update-october-2nd-2026/004_poll> "http://semidoped.com/poll")! ❤️_

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-october-2nd-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
