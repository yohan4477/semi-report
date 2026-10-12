---
source: https://daily.semidoped.com/p/daily-update-october-5th-2026
title: Daily Update - October 5th, 2026
date: 2026-10-05
kind: clipping
genre: daily
audience: everyone
subtitle: Ex-Groq engineers sue Nvidia over the $20B license-and-hire deal, Cloudflare ships Jev-compatible Clef, TSMC in early Terafab talks, Schneider buys PTC for $22.6B, Foxconn Q3 tops NT$1.15T.
---
**Hello world, it’s Monday, October 5th.**

Former Groq engineers are suing Nvidia over its $20 billion license-and-hire deal, claiming the structure left them holding equity in an empty shell. Cloudflare shipped Clef, an open-source decision model that is Jev-API compatible just weeks after Typesafe created the category. Elsewhere, Elon Musk confirmed TSMC is in early talks on Terafab, Schneider Electric is buying PTC for $22.6 billion, and Foxconn’s Q3 cumulative sales topped NT$1.15 trillion on AI server demand.

Let’s get into it. — _Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

#### Presented by Crusoe

Crusoe builds AI infrastructure from the ground up — power, data centers, and the cloud on top.

If you’re running open models — GLM, DeepSeek, Kimi, Qwen — Crusoe’s managed inference is fast: up to 9.9x faster time-to-first-token and 5x the throughput of vLLM, thanks to their MemoryAlloy caching layer and tokenizer fastokens. And it’s the easy kind of fast: pick a model, grab an API key and start inference. No GPUs to provision, no infrastructure or clusters to manage, and it’s pay per million tokens.

$5 in free credits to try it. [Send your first request today →](https://semidoped.com/crusoe-daily)

### Former Groq Engineers Sue Over Nvidia’s $20 Billion Licensing Deal

A group of former Groq engineers has filed suit against Nvidia over its [$20 billion license-and-hire agreement](https://www.ft.com/content/93ee425d-9ac7-4543-8cc9-fef2e0670787?syn-25a6b1a6=1) with Groq, claiming the deal was structured to cut them out of any compensation. The plaintiffs allege that Nvidia effectively acquired Groq’s inference chip intellectual property and key personnel while leaving behind a hollowed-out company with no assets to satisfy employee equity claims. The transaction, one of the largest AI chip IP deals on record, saw Nvidia license Groq’s architecture and bring aboard critical engineering staff. Groq’s remaining entity, the engineers argue, [amounts to an empty shell](https://app.dealroom.co/news/note/former-groq-engineers-sue-over-nvidia-s-20b-licence-and-hire-deal-saying-it-left-a-hollowed-out-shell) incapable of honoring prior financial obligations to them.

> **Austin:** _The structure dodged merger review, but can it dodge employee equity claims? Didn’t see that coming but it makes sense. Whatever the courts decide here reads straight across to Microsoft + Inflection and Google + Character.AI… again, those guys set the precedent here._

### Cloudflare launches Clef, open-source AI decision model platform

Cloudflare has released Clef, an open-source platform pairing decision models with a reinforcement learning fine-tuning layer aimed at producing bounded structured outputs cheaply and consistently inside automated workflows. The project enters a small but active category seeded by Typesafe AI’s Jev System One, which introduced the decision model concept to a wider audience in recent weeks. Where traditional classifiers return a label, decision models are designed to slot directly into a workflow at the point where a choice must be made, returning structured outputs with enough speed and cost efficiency to run inline rather than as a batch afterthought. Clef’s RL fine-tuning component lets teams adapt those models to their own decision criteria without rebuilding from scratch.

> **Austin:** _That was fast. Jev-API compatible and Apache 2.0, weeks after Jev introduced the category. Cloudflare hosting it on Workers AI puts it right next to where the action runs. What’s Typesafe’s moat now? BTW I wrote about the usefulness of these models and their impact on the AI infra buildout[here on Chipstrat](https://www.chipstrat.com/p/ai-with-no-decode-jev-and-what-it) _

### Musk Confirms TSMC Talks for Terafab

Elon Musk has publicly confirmed that [TSMC is in early discussions](https://www.thehindubusinessline.com/info-tech/tsmc-in-talks-with-musk-over-potential-role-in-texas-terafab-discussions-at-early-stage/article71545751.ece) to play a role in Terafab, the $119 billion fab project slated to serve Tesla, SpaceX, and xAI exclusively, with Intel named as the only other partner in the venture. No deal is in place, according to tbreak.com, and the talks remain at a preliminary stage. Korean MCE firms have already secured a major stake in the project. Intel stock fell on the news, per qz.com, as investors weighed whether a TSMC-Musk alignment would pull leading-edge US fab investment away from Intel Foundry. TSMC shares gained 1.13 percent on the day. TrendForce lists the Terafab talks as one of five key themes heading into TSMC’s next earnings call.

### Schneider Electric’s $22.6B PTC Deal Reshapes Industrial Software Stack

Schneider Electric has agreed to [acquire PTC for $22.6 billion](https://www.channelnewsasia.com/business/schneider-electric-buy-us-software-firm-ptc-in-226-billion-deal-6432401), folding the Boston-based maker of Windchill PLM and ThingWorx IIoT software into a company whose core business is power distribution hardware for factories and data centers. The combined entity would span physical infrastructure and the software layer that manages it, a pairing Schneider is positioning directly at AI data center buildouts and smart manufacturing customers. Schneider shares fell on the announcement, an unusual market verdict on a deal the company framed as strategically essential. Siemens and Rockwell Automation both compete across segments the merged company would now cover end-to-end, leaving neither rival with an obvious clean response.

### Foxconn Q3 Revenue Hits Record as AI Server Assembly Drives Demand

Foxconn posted third-quarter revenue that beat market forecasts on surging AI server assembly demand, with the company recording its first-ever monthly figure above NT$1.15 trillion. Hon Hai Precision, Foxconn’s listed entity, saw cumulative Q3 sales top NT$1.15 trillion, driven by hyperscaler orders flowing through its AI server integration lines. Bloomberg reported the results as a beat on sales estimates, attributing the outperformance to what it called an [AI frenzy among Nvidia’s supply chain partners](https://www.bloomberg.com/news/articles/2026-10-05/nvidia-partner-hon-hai-beats-sales-estimates-due-to-ai-frenzy). The record monthly threshold, crossed for the first time in the company’s history according to Taiwan News, lifted guidance expectations across the broader electronics manufacturing services sector for the quarter ahead.

> **Austin:** _Foxconn’s an ODM, so this is a good a read on hyperscaler order flow. Up and to the right._

### Scale AI’s Muse opens ESP32 firmware to third-party hardware makers

Alexandr Wang announced Muse Gadgets, releasing an [open-source ESP32 firmware and Linux SDK](https://x.com/alexandr_wang/status/2106113742266089526?s=46) so any developer can build hardware that connects to the Muse AI platform. Scale AI is also shipping its own first-party device under the initiative: Muse Home Link, designed to let Muse interact with consumer smart-home equipment including TVs. The move follows a pattern familiar from voice-assistant ecosystems, where a platform owner publishes a hardware abstraction layer and then seeds the market with a reference product. Releasing on ESP32, the low-cost Espressif microcontroller that already powers millions of IoT devices worldwide, keeps the barrier to entry low for independent makers.

[](https://substackcdn.com/image/fetch/$s_!VtfD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5c43ad81-a6b2-491b-91b4-2bf3efd176af_2366x724.png)

> **Austin:**_Dude, agentic IoT? Amazing. This is huge. Qualcomm bought Arduino, they should jump on getting Muse on Arduino!_
> 
> _And this suggests easier agentic physical AI more broadly?_

### Nathan Lambert launches Trillium Labs to open-source frontier AI research

Nathan Lambert, announcing via X, [unveiled Trillium Labs](https://x.com/), a new non-profit organization aimed at fostering open science around frontier artificial intelligence. The lab’s initial focus sits on building open post-training recipes, with plans to expand into open infrastructure for studying recursive self-improvement, reward hacking, and multi-agent systems. Lambert, known for his work on reinforcement learning from human feedback, described the effort as built around open principles from the ground up. The organization operates under the handle @trillium_labs. No funding figures or institutional backers were disclosed in the announcement, though the non-profit structure distinguishes it from the commercial AI labs whose closed development practices it implicitly pushes back against.

> **Austin:** _A non-profit for open frontier AI, starting with open post-training recipes and later open infra for things like reward hacking and multi-agent systems. This is good for the ecosystem and especially for academia._

###  Sector Watch

#### Foundry & Packaging

  * **Rapidus** forms a 17-company alliance to build chip design support services around its 2nm platform in Japan, broadening its ecosystem ahead of pilot production. ([nhk.or.jp](https://www3.nhk.or.jp/nhkworld/news/20261005de54872/))

  * **JSR** completes a new South Korea plant dedicated to next-generation EUV photoresist, adding domestic supply capacity for advanced lithography nodes. ([streamlinefeed.co.ke](https://streamlinefeed.co.ke/news/jsr-korea-ochang-euv-mor-plant-completion))

  * **Samsung Electronics** begins mass production of Exynos 2700 at 10% higher volume than its predecessor, targeting the Galaxy S27 series and signaling renewed confidence in its in-house AP roadmap. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=14397))




#### Compute

  * **Microchip Technology** completes acquisition of edge AI chip startup Hailo, adding dedicated neural-network inference silicon to its embedded microcontroller and networking portfolio. ([Hailo](https://www.ad-hoc-news.de/boerse/news/corporate-news/microchip-technology-completes-hailo-acquisition-as-microchip-technology/70227232))

  * **CoreWeave** deploys liquid-cooled switching for Nvidia Vera Rubin NVL72 racks, delivering 100% higher switching performance at 1.64 Pb/s per rack — first disclosed deployment at this scale. ([CoreWeave](https://wf.coreweave.com/blog/liquid-cooled-switching-doubles-ai-network-bandwidth-per-rack))

  * **Intel** ships Xeon 6+ Clearwater Forest CPUs in volume, with ServeTheHome publishing a full SKU list and value analysis of the wide-core lineup. ([ServeTheHome](https://www.servethehome.com/intel-xeon-6-sku-list-and-value-analysis-clearwater-forest-runs-wide/))




#### Memory

  * **Micron** files suit against YMTC alleging theft of 3D NAND technology, escalating IP litigation between the US and China’s leading flash memory producer. ([winbuzzer.com](https://winbuzzer.com/2026/10/05/micron-sues-memory-rival-ymtc-patent-ownership-xcxwbn/))

  * **Kioxia** and SanDisk offer a close-up look at BiCS NAND Gen 10 1Tb TLC die, providing the industry’s first public detail on the latest generation flash cell. ([ServeTheHome](https://www.servethehome.com/this-is-bics-nand-close-up-from-kioxia-and-sandisk/))

  * **Infineon** doubles AI revenue to $1.6 billion and divests its NOR Flash and F-RAM business to Winbond for $1.12 billion, sharpening focus on power semiconductors for AI data centers. ([Infineon](https://www.ad-hoc-news.de/boerse/news/unternehmensnachrichten/infineon-doubles-ai-revenue-to-1-6-billion-as-thai-backend-plant-and/70233211))




#### Power & Energy

  * **Vicor** raises Q3 FY26 revenue guidance above $186 million, representing over 30% growth, driven by AI data center power delivery demand. ([Vicor](https://www.ad-hoc-news.de/boerse/news/corporate-news/vicor-stock-enters-october-with-q3-guidance-above-30-percent/70228188))

  * **Renesas** develops a high-voltage GaN transistor targeting AI data center power conversion, expanding its wide-bandgap power device portfolio. ([Bisinfotech](https://www.bisinfotech.com/renesas-debuts-dual-side-cooled-650v-gan-device-to-power-megawatt-scale-ai-data-centers/))

  * **Eaton** acquires COL Group to expand manufacturing capacity for data center and utility power infrastructure across the EMEA region. ([Process and Control Today](https://www.pandct.com/news/eaton-acquires-col-group-expanding-manufacturing-capacity-and-capabilities-for-data-center-and-utility-markets-in-emea))




#### Optics & Networking

  * **Corning** signs a fiber supply deal worth over $3 billion with AT&T, one of the largest optical fiber agreements disclosed this year. ([Corning](https://www.ad-hoc-news.de/boerse/news/corporate-news/corning-agrees-to-more-than-3-billion-at-and-t-deal-what-it-means-for/70220136))

  * **Molex** introduces VersaBeam Mini, a 16-fiber expanded-beam optical connector designed for high-density AI and hyperscale data center connectivity. ([EE News Europe](https://www.eenewseurope.com/en/molex-unveils-versabeam-mini-for-high-density-ai-connectivity/))

  * **Ciena** achieves 1.6 Tbps transmission on a live Indian long-distance network with Constl across the Mumbai-Pune corridor, validating its AI optical platform at scale. ([SMEStreet](https://smestreet.in/technology/constl-achieves-16-tbps-transmission-on-live-nld-network-with-ciena-across-mumbaipune-corridor-12619514))




#### Policy & Trade

  * **Qualcomm** and Huawei sign a multi-year patent licensing deal covering 5G and AI, the first time Qualcomm has paid to license Huawei IP. ([Qualcomm](https://www.ad-hoc-news.de/boerse/news/corporate-news/qualcomm-signs-huawei-patent-deal-qualcomm-stock-gains-1-53-percent/70233308))

  * **Qualcomm** and Arm return to trial in Q4 2026 over royalties and alleged contract breach, with potentially enormous damages at stake. ([Reuters](https://www.reuters.com/business/media-telecom/qualcomm-arm-head-trial-again-potential-huge-damages-focus-2026-10-05/))

  * **OpenAI** , Blackstone, and SoftBank form the American Infrastructure Alliance, a lobbying group whose immediate mandate is blocking state-level restrictions on AI data center construction. ([TechRadar](https://www.techradar.com/pro/openai-blackstone-softbank-form-us-data-center-lobbying-group-american-infrastructure-alliances-first-job-is-stop-states-from-blocking-ai-data-center))




#### Edge

  * **Nscale** hires longtime Meta executive Justin Osofsky as COO as the Nvidia-backed neocloud prepares for an IPO, even as its UK supercomputer campus faces multi-year power grid delays. ([bloomberg.com](https://www.bloomberg.com/news/articles/2026-10-02/nscale-hires-meta-s-justin-osofsky-to-be-coo-ahead-of-ipo?srnd=homepage-americas))

  * **Arm Holdings** will release its fiscal Q2 2027 financial results on November 4, 2026, after market close, followed by a webcast at 14:00 PT. ([Arm Newsroom](https://newsroom.arm.com/news/arm-announces-earnings-release-date-for-second-quarter-fiscal-year-ending-2027))

  * **General Compute** signs a multi-year agreement with Cerebras to deploy Cerebras silicon across its compute infrastructure, according to Data Center Dynamics. ([Data Center Dynamics](https://www.datacenterdynamics.com/en/news/general-compute-signs-multi-year-agreement-with-cerebras/))




_Tell us how to make Semi Doped better![ Give us your feedback](http://semidoped.com/poll)! ❤️_

[Share](https://daily.semidoped.com/p/daily-update-october-5th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-october-5th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
