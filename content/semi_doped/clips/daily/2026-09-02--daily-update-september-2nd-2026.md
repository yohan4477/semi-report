---
source: https://daily.semidoped.com/p/daily-update-september-2nd-2026
title: Daily Update - September 2nd, 2026
date: 2026-09-02
kind: clipping
genre: daily
audience: everyone
subtitle: OpenAI's 'Compilers 2.0' AI-written kernels, Nvidia nears $14B Hugging Face deal, SK Group eyes Japan fab tied to Kioxia, TSMC tool procurement nearly doubles.
---
**Hello world, it’s Wednesday, September 2nd.**

An OpenAI engineer’s deep dive on AI-written kernels has stirred up real debate about where low-level compiler expertise fits going forward, while Nvidia is reportedly closing in on a roughly $14 billion deal to acquire Hugging Face that could wrap up this week. Elsewhere, SK Group’s chairman confirmed the conglomerate is reviewing Japan as a chip production site tied to a potential Kioxia partnership, and TSMC’s quarterly tool procurement nearly doubled.

Let’s get into it. _— Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

_Tell us how to make Semi Doped better![ Give us your feedback](http://semidoped.com/poll)! ❤️_

### OpenAI’s “Compilers 2.0”: AI as a stochastic optimizer for kernels

Chris Leary — who started Google’s XLA compiler and now works on OpenAI’s hardware team — [posted a deep dive](https://x.com/cdleary/status/2094878051238887834) on how AI wrote the Jalapeño MLA kernel shown at HotChips. He frames AI as a “stochastic optimizer”: traditional compilers improve programs through local dataflow rules and heuristics, while an LLM proposes optimizations more like an expert human performance engineer — unconstrained by a fixed rule set and taking many shots on goal. 

The lineage runs back to 2013’s STOKE paper, which randomly tweaked programs in search of the optimal one; swap the random tweaks for LLM reasoning and the walk through program space gains human-like traction per unit time. Conceptually, the AI takes the place of the “emitter” in a compiler like XLA — it lowers a numpy-level spec into optimized code, and because output kernels are verified for semantic equivalence against that spec, nobody needs to read them line by line, any more than you read the assembly that C++ at -O3 produces. Start from something “not very far from the numpy,” wait 48 hours, and out comes an optimized kernel — often climbing past ones OpenAI’s human experts had considered well tuned.

[@cdleary@cdleary"openai engineer explains /why/ he didn't need to understand the kernel line by line" 🙃 we're doing compilers 2.0 https://t.co/LAqjaXsnlk8:00 PM · Sep 1, 2026 · 91.9K Views

* * *

19 Replies · 62 Reposts · 512 Likes](https://x.com/cdleary/status/2094878051238887834)

[](https://substackcdn.com/image/fetch/$s_!MHHk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7329a2e7-0dc7-470d-b81c-5016b9d62e9d_1190x1418.png)

> **Vik:**_Worth a read! The paradigms of software for hardware design are changing._

### Nvidia Closes In on $14 Billion Hugging Face Acquisition

[Nvidia is nearing a deal to acquire Hugging Face at a roughly $14 billion valuation](https://www.bloomberg.com/news/articles/2026-09-02/nvidia-nears-14-billion-hugging-face-deal-this-week), with Bloomberg reporting the transaction could close this week. Hugging Face operates the dominant open-model repository, hosting hundreds of thousands of models and datasets that developers across the industry rely on daily. A purchase at that price would rank among the largest AI software acquisitions on record. 

Sara Araghi, senior vice president and portfolio manager at Franklin Templeton, told Bloomberg Surveillance that Nvidia has been using its financial strength to support the broader AI ecosystem, arguing the company needs to backstop demand and monetization across that ecosystem. Owning Hugging Face would fold model distribution directly into Nvidia’s stack, sitting alongside its silicon, software libraries, and cloud partnerships.

> **Vik** : _Nvidia’s commitment to open source is only getting stronger as frontier model builders diversify away from Nvidia hardware by either building their own silicon, or look to use alternative suppliers and custom ASICs. $14B is a lot of money!_

### SK Chairman Floats Japan Chip Plant Tied to Kioxia Partnership

SK Group Chairman Chey Tae-won confirmed the conglomerate is [reviewing Japan as a potential overseas semiconductor production site](https://www.thelec.net/news/articleView.html?idxno=13509), telling reporters the group “will make an announcement once discussions are completed.” The disclosure is notable for what Chey attached to it: an explicit overture toward cooperation with Kioxia, the Japanese NAND flash maker in which SK Hynix already holds a roughly 18.6 percent stake following its participation in a 2021 consortium investment. Chey framed the Japan facility and the Kioxia tie-up as linked considerations, not separate tracks, according to Chosunbiz and Seoul Economic Daily. A formal partnership, if it materializes, would give SK Hynix deeper operational reach into Japan while potentially aligning the two largest NAND producers outside Samsung under a closer manufacturing arrangement.

### TSMC Tool Procurement Nearly Doubles as Big Tech Courts Intel Packaging

TSMC’s quarterly chipmaking equipment needs [almost doubled this year](https://www.bloomberg.com/news/articles/2026-09-02/tsmc-s-quarterly-chipmaking-tool-needs-almost-doubled-this-year), a pace that reflects sustained demand pressure rather than a one-time surge in orders. With that backlog stretching lead times, major technology companies are actively shifting advanced packaging work toward Intel Foundry, where capacity remains more accessible. 

The [pivot to Intel packaging](https://biz.chosun.com/en/en-it/2026/09/02/VC6WHF4WNBFM5CNWWY6KJKGNME/) comes at a useful moment for Intel’s foundry ambitions, which have absorbed considerable investment without proportional revenue to show for it. Korean suppliers are also diversifying customer exposure in response to the same bottleneck. TSMC continues expanding aggressively, but equipment procurement at that velocity takes quarters to translate into usable capacity.

### Sector Watch

#### Foundry & Packaging

  * **UMC** commits $6.4 billion to a new Singapore fab, its largest-ever overseas investment, targeting AI-driven mature-node demand growth. ([The Straits Times](https://www.straitstimes.com/business/economy/semiconductor-firm-umc-spends-6-4m-on-new-singapore-fab-to-claim-a-stake-in-ai-boom))

  * **ASML** expects its High-NA EUV tool to reach production-grade availability by year-end 2026, accelerating next-node ramp timelines. ([Bits&Chips](https://bits-chips.com/article/asml-expects-high-na-euv-to-reach-production-grade-availability-by-year-end/))

  * **Camtek** secures a $31 million advanced-packaging inspection order from an OSAT customer, reflecting continued back-end capacity expansion. ([openpr.com](https://www.openpr.com/news/4619935/camtek-secures-31-million-osat-order-as-advanced-packaging))




#### PCB & Components

  * **Samsung Electro-Mechanics** CEO Jang Deokhyun visits key supplier partners in Yangsan, pledging deeper ties to meet surging AI parts demand. ([Seoul Economic Daily](https://en.sedaily.com/finance/2026/09/02/samsung-electro-mechanics-ceo-pledges-deeper-supplier-ties))

  * **HanWool Semiconductor** launches AI-based visual inspection equipment capable of screening 13,000 MLCCs per minute, targeting AI server component quality. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13516))

  * **GlobalFoundries** and **RAAAM Memory Technologies** announce a partnership, per a joint press release, targeting embedded memory solutions. ([GlobeNewswire](https://www.globenewswire.com/news-release/2026/09/02/3355121/0/en/globalfoundries-and-raaam-memory-technologies-announce-the-joint-development-of-next-generation-gcram-technology-and-test-chip-on-fdx-platform.html))




#### Power

  * **Infineon** and Skeleton Technologies announce a collaboration to develop high-resilience power solutions engineered for AI data center applications. ([Compound Semiconductor](https://compoundsemiconductor.net/article/125287/Infineon_and_Skeleton_to_collaborate_on_AI_power))

  * **Eaton** announces a $242 million investment in a new Arkansas facility to expand manufacturing of modular electrical enclosures for critical infrastructure. ([Voice of Alexandria](https://www.voiceofalexandria.com/news/national_business_news/eaton-expands-manufacturing-for-modular-electrical-enclosures-with-242-million-investment-in-new-arkansas-facility/article_8910f5a1-fc4f-5682-9e29-3e7418aa897b.html))

  * **SB Energy** (SoftBank-backed, Nvidia- and OpenAI-affiliated) files for IPO, disclosing substantial dependence on OpenAI as its anchor data center customer. ([CNBC](https://www.cnbc.com/2026/09/01/sb-energy-ipo-softbank-open-ai-nvidia.html))




#### Optics & Networking

  * **iPronics** raises $125 million led by Nvidia and others to scale programmable optical networking chips for AI data centers. ([GlobeNewswire](https://www.globenewswire.com/news-release/2026/09/02/3355203/0/en/ipronics-raises-125-million-to-scale-programmable-optical-networking-for-ai-data-centers.html))

  * **RAONTECH** will supply spatial light modulator backplanes for optical communications equipment used in Nvidia AI data centers, per The Elec. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13504))

  * **Keppel DC REIT** acquires majority stakes in two hyperscale Tokyo data centers as Singtel and KKR close their $5.2 billion Singapore transaction. ([Light Reading](https://www.lightreading.com/data-centers/keppel-dc-reit-expands-japan-assets-as-singtel-kkr-close-5-2b-stt-gdc-deal))




#### China Domestic Chip

  * **AMEC** unveils six new chip-making machines in a single day, accelerating China’s domestic semiconductor equipment self-sufficiency push. ([South China Morning Post](https://www.scmp.com/tech/big-tech/article/3366079/chinas-amec-unveils-6-chip-making-machines-one-day-speed-self-reliance))

  * **Hua Hong Grace** invests $2 billion in a Phase III Wuxi fab expansion adding 55,000 wafers-per-month of capacity to meet AI-driven mature-node demand. ([South China Morning Post](https://amp.scmp.com/tech/big-tech/article/3366104/chinas-no-2-foundry-hua-hong-invests-us2b-new-fab-meet-surging-ai-driven-demand))

  * **Enflame** prices its Shanghai IPO at roughly $900 million after drawing 6,109 times online demand, marking a landmark Chinese AI chip public listing. ([Reuters](https://www.reuters.com/world/china/tencent-backed-enflame-ipo-draws-6109-times-online-demand-2026-09-02/))




#### Edge & Compute

  * **Qualcomm** and HUMAIN unveil the Horizon Ultra AI PC at LEAP 2026, the first commercial device built around Snapdragon’s on-device AI platform. ([IT Brief UK](https://itbrief.co.uk/story/humain-and-qualcomm-launch-the-horizon-ultra-ai-pc))

  * **Cerebras** and Compute Nordic Finland announce a 165 MW AI data center in Mikkeli with the first 50 MW already under construction. ([W.Media](https://w.media/cerebras-and-compute-nordic-finland-announce-new-165-mw-ai-data-center-in-mikkeli/))

  * **Google** accelerates its in-house chip rollout cadence, with its technology chief signaling faster generational cycles to sustain AI leadership, per Nikkei. ([Nikkei Asia](https://asia.nikkei.com/business/technology/artificial-intelligence/google-to-speed-up-chip-rollout-to-stay-ahead-in-ai-technology-chief-says))




_Tell us how to make Semi Doped better![ Give us your feedback](http://semidoped.com/poll)! ❤️_

[Share](https://daily.semidoped.com/p/daily-update-september-2nd-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-september-2nd-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
