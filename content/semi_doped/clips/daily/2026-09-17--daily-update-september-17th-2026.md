---
source: https://daily.semidoped.com/p/daily-update-september-17th-2026
title: Daily Update - September 17th, 2026
date: 2026-09-17
kind: clipping
genre: daily
audience: everyone
subtitle: Huawei pulls Ascend 960DT to Q1 2027 and claims million-processor clusters, CoreWeave raises $3B in notes, Generac locks $2.4B Amazon generator deal, MediaTek's 2nm Dimensity 9600 Pro at $220.
---
**Hello world, it’s Thursday, September 17th.**

Huawei pulled the Ascend 960DT’s launch forward nine months to Q1 2027 and claimed its UnifiedBus interconnect can bind a million processors into one logical computer. CoreWeave raised $3 billion in convertible notes as its Nvidia Vera Rubin clusters went live, Generac surged 33% premarket on a $2.4 billion generator deal with Amazon, and MediaTek’s 2nm Dimensity 9600 Pro landed at a reported $220.

Let’s get into it. — _Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

_Tell us how to make Semi Doped better![ Give us your feedback](http://semidoped.com/poll)! ❤️_

#### Presented by G2i

> You track the chips. G2i works the layer above them: the human data and RL environments that decide whether a model trained on all that silicon is actually good.
> 
> G2i spent over a decade placing engineers at other companies, from startups to FAANG. Two years ago, they built their own bench to do that work directly for frontier AI labs, with engineers who’ve shipped production code themselves.
> 
> Building or scaling that kind of work? [See how G2i does it, and book a call when you’re ready.](https://fandf.co/4wZvKHS)

### Huawei Pulls Ascend 960 Launch Forward, Claims Million-Processor Cluster

Huawei [moved the Ascend 960DT training chip’s release to Q1 2027](https://www.scmp.com/tech/big-tech/article/3367832/huawei-quickens-ai-chip-pace-promises-next-entrant-3-quarters-early?utm_source=rss_feed), nine months ahead of its original schedule, with rotating chairman David Wang Tao telling the Huawei Connect 2026 conference in Shanghai that the chip delivers doubled performance over its predecessor. Demand already outstrips supply on current Ascend hardware, according to Reuters. 

The bigger architectural news came alongside the chip timing: [the Peerium Computing Architecture’s UnifiedBus interconnect can bind up to one million processors](https://www.scmp.com/tech/big-tech/article/3367882/how-huawei-plans-bypass-us-chip-curbs-its-new-unifiedbus-technology?utm_source=rss_feed) into a single logical computer, using nested parallelism, unified memory addressing, and peer-to-peer fabric connecting processors, memory, and storage. Huawei also introduced near-packaged optics in its Atlas 960 SuperPoD cluster, promising higher speeds and lower energy consumption. Chairman Guo Ping has stated the company aims to become the Nvidia of ICT.

> **Austin:**_From Huawei directly, this is what caught my eye:**NPO!**  
>   
>  “SuperPoDs are designed to coordinate multiple NPUs through interconnect,” continued Wang. “**We have developed a next-generation optical interconnect product based on near-packaged optics (NPO):** the High-density Optical-interconnect-Node Engine (Hi-ONE).” Built on Huawei’s proprietary technologies, Hi-ONE has a multi-physics design for balancing optical, mechanical, electrical, electromagnetic, and thermal performance, realizing a transmission capacity of **7.2 Tbit/s per single engine.**_
> 
> _**“This is the industry’s first NPO product ready for mass production,** delivering the largest transmission capacity. It is also the industry’s **first NPO product with a built-in light source**.”_
> 
>  _Some big claims, we’ll have to dig in more here!_
> 
> **Vik:**_Unified Bus Architecture was part of the Tau Scaling concept, where all the devices on the bus speak the same language, thus saving any delays that arise from translations. And yes, SuperPODs are entirely optical scale up with NPO. That’s whats amazing about it._

### Generac Locks $2.4 Billion Amazon Generator Pact as Data-Center Power Crunch Deepens

Generac shares surged 33% premarket after the company announced a $2.4 billion long-term generator supply agreement with Amazon, covering backup power infrastructure for Amazon’s expanding data-center portfolio. Reuters confirmed the deal’s value at $2.4 billion, though Bloomberg put the figure at [$8 billion](https://www.bloomberg.com/news/articles/2026-09-16/generac-shares-jump-on-8-billion-amazon-data-center-supply-pact), and the discrepancy between sources hasn’t been resolved. 

The contract reflects a broader shift among hyperscalers toward multi-year, committed power procurement rather than spot purchasing. On-site generation is now treated as core infrastructure. Google, Nvidia, and Emerald AI separately founded the AI Energy Management Alliance to advance grid demand-response capabilities across data centers, addressing the grid-side constraint that makes firm backup generation so attractive to operators in the first place.

> **Vik:**_The grid connection being so constrained has opened up an entire market for behind-the-meter power generation with Bloom Energy at the helm. With demand still outpacing grid-supply, BTM power is set to continue to grow!_

### SK Hynix Lays Out HBM4 and CXL Roadmap for Hyperscale Customers

SK Hynix used the three-day [AI Infra Summit 2026 in Santa Clara](https://news.skhynix.com/en/ai-infra-summit-2026/) to present what it called a “new spectrum” for AI infrastructure, walking hyperscale customers through its HBM4 and CXL memory roadmap across sessions spanning compute, data movement, and AI data center architectures. The summit ran September 15-17, drawing global big tech firms competing for advanced memory allocation through 2027. 

> _**Austin:**[Chosun Daily](https://www.chosun.com/english/industry-en/2026/09/17/DPBT3YGLRJEXVHCBEOSVQ3GZNI/) has an interesting quote from the AI infra summit regarding CXL:_
> 
> _“However, Daniel Morris, a researcher responsible for AI accelerator design at OpenAI, stated during a panel discussion, “**From the perspective of actually operating AI models, I cannot find a use case for CXL**.” He added, “If I were to assign a role to CXL, it would be to store inactive data that is rarely used in large AI models. Unlike expectations, I have yet to see practical applications specialized for model operation.”_

### Georgia Tech Open-Sources a 2nm GAA Nanosheet PDK

Georgia Tech researchers [released GT2N](https://github.com/azadnaeemi/GT2N), an open-source process design kit for a 2nm-class gate-all-around nanosheet node with backside power delivery, under a BSD-3 license. The kit ships 72 standard cells, thermal-calibrated GAAFET SPICE models, DRC/LVS rulesets, and library collateral across three process corners, with flows for Synopsys Custom Compiler and the open-source OpenROAD toolchain. Real leading-edge PDKs live behind foundry NDAs, so an open kit at these design rules gives universities and startups a way to research, prototype, and teach angstrom-era design without a foundry agreement.

> **Vik:**_I have a whole post on how you can play around with Open Source EDA Tools from last year!_
> 
> [ Vik's NewsletterHow to Learn Chip Design With Open-Source EDA ToolsHey Vikram here! 👋🏽 This newsletter now has lower price options for students and people in lower income regions to establish Purchasing Power Parity (PPP…Read morea year ago · 34 likes · 4 comments · Vikram Sekar](https://www.viksnewsletter.com/p/how-to-learn-chip-design-with-foss-eda?utm_source=substack&utm_campaign=post_embed&utm_medium=web&embedding_publication_id=8781267)

[phase interpolator@phasentrpolatorInsane work, open source GAA nanosheet 2nm PDK just dropped. github.comGitHub - azadnaeemi/GT2N: PDK for 2nm Technology Node10:22 PM · Sep 16, 2026 · 36.3K Views

* * *

4 Replies · 29 Reposts · 178 Likes](https://x.com/phasentrpolator/status/2100349628445024576)

[](https://substackcdn.com/image/fetch/$s_!MMoA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F57a7f832-a51e-4786-be12-ac570619fcc6_400x574.gif)

### Sector Watch

#### Optics & Networking

  * **Tower Semiconductor** and **NewPhotonics** begin high-volume shipments of laser-integrated, serviceable optical engine PICs targeting scale-out and scale-up AI interconnect. ([Tower Semiconductor](https://towersemi.com/2026/09/17/09172026/))

  * **Lightmatter** joins the Open CPX MSA and introduces the industry’s first bidirectional CPX optical engine, advancing co-packaged photonics standards for AI switch fabrics. ([PR Newswire](https://www.prnewswire.com/news-releases/lightmatter-joins-open-cpx-msa-introduces-the-industrys-first-bidirectional-cpx-optical-engine-302881786.html))

  * **GlobalFoundries** and **Marvell** expand their collaboration for next-generation optical connectivity silicon, deepening the GF silicon-photonics roadmap for AI networking. ([Globe Newswire](https://www.globenewswire.com/news-release/2026/09/17/3364000/0/en/globalfoundries-and-marvell-expand-collaboration-for-next-generation-optical-connectivity.html))




#### Memory

  * **Kioxia** halts NAND flash price hikes to protect demand, stepping back from further increases after signs of customer resistance, Chosunbiz reports. ([조선일보](https://www.chosun.com/english/industry-en/2026/09/17/SZNE3OEUSZD3XPLRUVEPEBVC3A/))

  * **CXMT** wins share among Chinese smartphone brands as domestic buyers shift DRAM sourcing away from Samsung and SK Hynix, South China Morning Post reports. ([South China Morning Post](https://www.scmp.com/tech/big-tech/article/3367853/once-reliant-samsung-and-sk-hynix-chinese-smartphone-makers-are-turning-cxmt))

  * **CXMT** capitalizes on the global DRAM shortage to expand revenue and discloses plans to enter the HBM market, DigiTimes reports. ([digitimes](https://www.digitimes.com/news/a20260917VL219/cxmt-dram-hbm-supply-chain-emerging-memory.html))




#### Compute

  * **Rebellions** will supply AI inference racks to Japan’s ai& data center, the Korean AI chip startup’s first confirmed commercial deployment outside its home market. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13963))

  * **Apple** is weighing Nvidia server technology for a potential return to the server market, according to The Information via Reuters. ([Reuters](https://www.reuters.com/technology/apple-considers-nvidia-tech-return-server-market-information-reports-2026-09-16/))

  * **Analog Devices** adopts the Cadence Tensilica DSP architecture for its next-generation automotive signal processors, EE Times Asia reports. ([EE Times Asia](https://www.eetasia.com/adi-adopts-cadence-tensilica-architecture-for-next-gen-automotive-dsps/))




#### Power

  * **onsemi** unveils its Embedded Power Platform at investor day, targeting high-density power delivery for AI racks, automotive, and industrial systems. ([ServeTheHome](https://www.servethehome.com/onsemi-embedded-power-platform-announced/))

  * **Bloom Energy** launches an 800V DC power architecture for AI data centers, claiming meaningful cost reductions versus standard AC-coupled designs. ([Fuel Cells Works](https://fuelcellsworks.com/2026/09/16/clean-energy/bloom-energy-s-800v-dc-native-power-can-cut-billions-from-ai-data-center-costs-reduce-power-use-and-eliminate-need-for-transformers))

  * **ROHM** secures a flagship EV design win, supplying silicon carbide power devices for BMW’s Neue Klasse electric vehicle powertrain architecture. ([presseagentur.com](https://www.presseagentur.com/rohm/detail.php?pr_id=7801&lang=en))




#### Data Centers

  * **Anthropic** signs its first Australian data center lease with Zerra DC for a 2.16 GW Queensland facility, marking the AI lab’s first owned inference infrastructure outside North America. ([Reuters](https://www.reuters.com/world/asia-pacific/anthropic-signs-first-australia-data-centre-agreement-2026-09-16/))

  * **LIAN Group** is weighing a US IPO targeting $500 million to fund AI and computing data center infrastructure development, Bloomberg reports. ([Bloomberg Tech](https://www.bloomberg.com/news/articles/2026-09-17/ai-data-center-developer-lian-mulls-ipo-to-raise-500-million))

  * **Goodman** raises $455 million for the mechanical and electrical fit-out of its HK10 data center in Tsuen Wan, Hong Kong, Light Reading reports. ([Light Reading](https://www.lightreading.com/finance/goodman-pulls-in-455m-for-hong-kong-data-center-push))




#### Foundry & Packaging

  * **ClassOne Technology** receives multi-system follow-on production orders from two leading photonics manufacturers for 6-inch InP gold-plating tools. ([Semiconductor Digest](https://www.semiconductor-digest.com/classone-technology-secures-multi-system-follow-on-orders-from-top-photonics-manufacturers-for-high-volume-6-inch-inp-gold-plating/?utm_source=rss&utm_medium=rss&utm_campaign=classone-technology-secures-multi-system-follow-on-orders-from-top-photonics-manufacturers-for-high-volume-6-inch-inp-gold-plating))

  * **Japan and the US** are discussing semiconductor factory construction as part of a broader $550 billion bilateral investment package, Nikkei reports via Reuters. ([Reuters](https://www.reuters.com/world/asia-pacific/japan-us-discussing-chip-factory-construction-part-550-billion-investment-talks-2026-09-17/))

  * Banks arrange a **$22 billion chip-industry loan** tied to Blackstone and Alphabet, one of the largest single financing packages for semiconductor infrastructure, Bloomberg reports. ([Bloomberg.com](https://www.bloomberg.com/news/articles/2026-09-16/banks-line-up-22-billion-chip-loan-tied-to-blackstone-alphabet))




#### Policy & Trade

  * The **US House** advances its first bill addressing the economic impact of the data center boom, establishing an initial legislative framework for the sector, Reuters reports. ([Reuters](https://www.reuters.com/world/us-house-advances-first-bill-addressing-economic-impacts-data-center-boom-2026-09-16/))

  * **Prime Minister Modi** draws pledges from US chip industry leaders at Semicon India for a $30 billion national chipmaking investment push, Bloomberg reports. ([Bloomberg Tech](https://www.bloomberg.com/news/articles/2026-09-17/modi-courts-investors-with-india-s-30-billion-chipmaking-bet))

  * **South Korea’s judiciary** draws industry alarm after handing lighter sentences in technology-secrets theft cases, heightening IP-protection concerns for chipmakers. ([조선일보](https://www.chosun.com/english/national-en/2026/09/17/4L4J3RLS4ZFKXOEQZ63SGECCGA/))




_Tell us how to make Semi Doped better![ Give us your feedback](http://semidoped.com/poll)! ❤️_

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-september-17th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
