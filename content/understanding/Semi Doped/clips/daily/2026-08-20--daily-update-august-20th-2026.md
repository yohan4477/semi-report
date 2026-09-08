---
source: https://daily.semidoped.com/p/daily-update-august-20th-2026
title: Daily Update - August 20th, 2026
date: 2026-08-20
kind: clipping
genre: daily
audience: everyone
subtitle: SK Hynix published a CPO roadmap in Nature Electronics, Waymo built a custom robotaxi chip, Micron plans a $10B Boise AI memory campus, and Alibaba Cloud grew 45% as CapEx hit $10B.
---
**Hello world, it’s Thursday, August 20th.**

SK Hynix published a co-packaged optics roadmap in Nature Electronics, mapping the path from memory bandwidth to optical interconnect. Waymo has built a custom chip for its robotaxi fleet. Micron is committing $10 billion to a new AI memory research campus in Boise, and Alibaba Cloud grew 45% while profit cratered as CapEx hit $10 billion.

Let’s get into it. _— Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

_Tell us how to make Semi Doped better![ Give us your feedback](http://semidoped.com/poll)! ❤️_

### SK Hynix Maps CPO Path From Memory Bandwidth to Optical Interconnect

SK Hynix published a co-packaged optics roadmap in Nature Electronics on Aug. 20, framing CPO as the answer to bandwidth and energy bottlenecks that conventional electrical interconnects can no longer solve at AI-scale. The paper, titled [“Co-packaged optics for high-performance computing and artificial intelligence,”](https://news.skhynix.com/en/cpo-in-nature-electronics/) lays out how photonic integration with memory packages becomes the next systems-level contest as the industry works through the HBM4 and HBM5 generations. That timing collides with a parallel question the industry is still working out: HBM4 introduces a [customizable base die](https://semiengineering.com/how-will-the-custom-hbm-business-work/), and as Semiconductor Engineering reports, the scarce resource in those custom projects isn’t supply but design teams and tooling. Packaging, interconnect architecture, and supplier relationships are all in play at once. Light, it turns out, is the easy part.

> _**Austin:** The memory pooling is interesting. Why limit the amount of HBM to what can be physically packaged with your SOC? Why not just have a local memory pool you can connect to via optics? This gives XPU makers the ability to decide compute:memory ratios at design time. Or easily have a prefill chip with less pooled memory and a decode chip with more. _
> 
> [](https://substackcdn.com/image/fetch/$s_!6cLf!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F53573463-7efa-420f-a439-5beb6ffae663_1600x900.jpeg)
> 
> _Note that we’ve seen ideas like this_ _elsewhere, e.g.[Marvell/Celestial AI](https://www.marvell.com/blogs/photonic-fabric-technology-optical-connectivity-ai-infrastructure.html)._

### Waymo Builds Custom Robotaxi Chip as Automotive Silicon Splits

Alphabet’s Waymo has [built a purpose-designed chip](https://www.bloomberg.com/news/articles/2026-08-20/google-s-waymo-has-built-a-custom-chip-for-its-robotaxis) for its robotaxi fleet, stepping into the custom silicon business that its hyperscale parent knows well and that rivals like Tesla have already staked out. The move puts Waymo in direct control of its own perception hardware rather than buying off-the-shelf solutions from traditional automotive suppliers. Separately, Renesas has struck a deal with Japan’s Tier IV to run the open-source Autoware stack on [R-Car Gen 5 automotive SoCs](https://www.prnewswire.com/news-releases/tier-iv-collaborates-with-renesas-to-build-an-open-ai-native-computing-platform-for-sdvs-integrating-r-car-gen-5-automotive-socs-with-autoware-and-reference-ai-models-302855856.html), pairing the forthcoming processor with Tier IV’s reference AI models for software-defined vehicles. The Renesas arrangement targets the broader OEM market that won’t build its own silicon, offering an integrated platform for automakers that want Autoware without assembling the stack themselves from scratch.

> _**Austin:**_ _Waymo had a bit to say, with more details at Hot Chips! The important value prop is the ability to co-design the end-to-end system and reduce “pixels-to-actuation” latency:_
> 
> [](https://substackcdn.com/image/fetch/$s_!62zb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fff602a6a-c668-4280-91d9-03e32eb4c007_1914x1264.png)
> 
> _Relatedly, see my conversation with Rivian’s VP of ASIC Design about their custom silicon chip to learn more about custom silicon for autonomous vehicles:[An Interview with Rivian’s Mukund Chavan About RAP1](https://www.chipstrat.com/p/an-interview-with-rivians-mukund)_

### Micron Bets $10 Billion on Boise as AI Memory Race Tightens

Micron has [unveiled a $10 billion AI memory research campus in Boise](https://investors.micron.com/news/press-release/2026/Micron-Unveils-Micron-Research-Labs-a-U-S--Based-Long-Horizon-Innovation-Hub-to-Shape-the-Future-of-Memory-and-AI/default.aspx), planting a flag in the high-stakes competition to supply the memory stacks that power large-scale AI infrastructure. The investment targets Micron’s persistent gap with SK Hynix in high-bandwidth memory, where Hynix currently holds a commanding lead in HBM3E supply to Nvidia. Boise now enters the conversation alongside Icheon and Hiroshima as a serious advanced-memory R&D address. Micron has simultaneously overtaken Kioxia for third place in global NAND market share, according to reporting on [Kioxia’s 2026 capacity outlook](https://www.ad-hoc-news.de/boerse/news/unternehmensnachrichten/kioxia-s-2026-output-is-already-spoken-for-even-as-micron-steals-its/69977292). Kioxia, for its part, has its 2026 output already contracted, suggesting the competitive pressure is real but the displaced company isn’t exactly scrambling.

> _**Austin:** Love to see it. More investment in memory R&D is essential to keep up with the insane demands of AI. Also on a personal level, this is awesome for EE/Materials Science/etc PhDs. One of the sharpest people in my grad school research group went to Micron after finishing his PhD. Others went to Intel Foundry, a great spot for R&D too. _

### Alibaba Cloud Jumps 45% but Profit Craters as CapEx Hits $10 Billion

Alibaba’s cloud and AI division [grew 45% in the June quarter](https://www.scmp.com/tech/big-tech/article/3364705/alibabas-ai-cloud-growth-surge-drives-earnings-despite-soaring-tech-spending?utm_source=rss_feed), pushing overall revenue up 9% and delivering adjusted profit of 27.3 billion yuan, better than analysts expected. The cost of that growth is hard to miss. [Quarterly capital expenditure hit nearly $10 billion and net profit fell](https://www.bloomberg.com/news/articles/2026-08-20/alibaba-s-revenue-climbs-9-in-testament-to-china-s-ai-boom) as the company poured cash into AI infrastructure. Executives told investors on the earnings call that AI computing investments would break even within three years, or possibly two if gross margins kept climbing. Alibaba has outpaced Chinese tech peers this quarter on renewed AI enthusiasm, but the arithmetic for now runs in one direction: revenue accelerating, profits absorbing the blow.

### Cerebras Posts Q2 Loss, Raises Full-Year Guidance After CS-4 Launch

Cerebras Systems delivered its first earnings report as a public company with a swing to a second-quarter loss, even as management [raised its full-year outlook](https://www.wsj.com/business/earnings/cerebras-swings-to-second-quarter-loss-lifts-full-year-outlook-ed83550a) following the launch of the CS-4 wafer-scale chip. The loss reflects the company’s heavy infrastructure spending as it scales to meet demand, a pattern common in capital-intensive AI hardware builds. Cathie Wood’s ARK Invest moved in the other direction from sellers, [purchasing $8.84 million of Cerebras shares](https://app.dealroom.co/news/note/cathie-wood-buys-8-84m-of-cerebras-after-29-post-ipo-slide) after the stock slid roughly 29% from its IPO price. The Callosum partnership, announced around the same period, extends Cerebras inference capacity through third-party API access, adding a distribution channel without requiring additional fab investment. Revenue growth absorbing investment costs remains the core financial story here, and the raised guide suggests management sees that trajectory holding through year-end.

### Sector Watch

#### Compute

  * **Nvidia** plans to ship a new China-compliant AI chip by year-end, according to The Information, marking its first export-rule-cleared product since the H20 ban. ([Reuters](https://www.reuters.com/world/china/nvidia-ship-ai-chip-china-by-year-end-information-reports-2026-08-20/))




#### Foundry & Packaging

  * **JCET** reports 79.4% year-on-year growth in H1 2026 net profit and accelerates its advanced packaging expansion in a PR Newswire release. ([PR Newswire](https://www.prnewswire.com/news-releases/jcet-reports-79-4-yoy-growth-in-h1-2026-net-profit-attributable-to-shareholders-accelerates-advanced-packaging-expansion-302856590.html))

  * **Synopsys** validates a PCIe 6.0 PHY inside a face-to-face 3D stack at 64 GT/s, the first disclosed demonstration of the interconnect standard in a stacked die configuration. ([Tom’s Hardware](https://www.tomshardware.com/tech-industry/semiconductors/synopsys-validates-a-pcie-6-phy-inside-a-face-to-face-3d-stack))

  * **ASML** faces a potential US-directed Dutch ban on selling its DUV tools to China, as Washington prepares to pressure the Netherlands for a broader export restriction. ([NL Times](https://nltimes.nl/2026/08/20/us-preparing-force-netherlands-ban-asml-selling-china))




#### Memory

  * **Samsung** and **SK Hynix** are preparing shareholder return programs exceeding $72 billion combined, the largest in Korean semiconductor history. ([Bloomberg](https://www.eenewseurope.com/en/sk-hynix-launches-28bn-share-buyback/))

  * **YMTC** clears IPO counseling acceptance on the Shanghai exchange, advancing the sanctioned NAND maker’s push toward a domestic listing as its global market share reaches 14%. ([digitimes](https://www.digitimes.com/news/a20260819VL211/ymtc-ipo-nand-flash-market.html))

  * **ENF Technology** will build a 450 billion won semiconductor materials campus in Yesan, South Chungcheong Province, targeting advanced memory supply chains. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13187))

  * **Soulbrain** files plans for an $85.8 million semiconductor-materials plant in Taylor, Texas, deepening its supply position for Samsung’s US fab. ([Energies Media](https://energiesmedia.com/soulbrain-texas-semiconductor-factory/))




#### Data Centers

  * **CoreWeave** and Hudson River Trading sign a multibillion-dollar multiyear deal to power HRT’s AI trading research on Nvidia Vera Rubin hardware. ([CoreWeave](https://www.roi-nj.com/2026/08/20/tech/coreweave-signs-ai-cloud-deal-with-hudson-river-trading-for-research-platform/))

  * **Nebius** prices $5 billion in convertible notes to fund AI data center expansion, its largest single debt raise and part of more than $11 billion raised in under a year. ([Blockspace Media](https://blockspace.media/insight/nebius-prices-convertible-notes-ai-infrastructure/))

  * **Bloom Energy** launches a new rapid-deployment platform to cut time-to-power for data center operators, targeting faster fuel-cell installations at AI campuses. ([Data Center Dynamics](https://www.datacenterdynamics.com/en/news/bloom-launches-new-deployment-platform-to-expedite-time-to-power-for-data-center-operators/))




#### Optics & Networking

  * **Zayo** expands its long-term fiber supply agreement with **Corning** to underpin a 15,000-route-mile AI network buildout across the US. ([Broadband Breakfast](https://broadbandbreakfast.com/zayo-reaches-fiber-reserve-deal-with-corning/))

  * **Relativity Networks** raises $22 million and secures a $40 million hyperscaler contract for its hollow-core fiber technology targeting AI interconnect. ([Light Reading](https://www.lightreading.com/ai-machine-learning/relativity-raises-22m-scores-40m-hyperscaler-deal))

  * **Charter** closes its merger with Cox to create the world’s largest cable operator, passing more than 70 million locations under the Spectrum brand. ([Light Reading](https://www.lightreading.com/cable-technology/charter-cox-deal-is-a-wrap-with-spectrum-brand-to-take-over-within-a-year))




#### Power

  * **Nordson** posted record Q3 fiscal 2026 results and raised its full-year guidance. ([Nordson](https://investors.nordson.com/news/news-details/2026/Nordson-Corporation-Reports-Record-Third-Quarter-Fiscal-2026-Results-and-Increases-Full-Year-Guidance/default.aspx))

  * **GlobalFoundries** details its 48V power architecture strategy, targeting automotive, industrial, and AI infrastructure customers with its specialized process portfolio. ([GlobalFoundries](https://gf.com/news-and-events/blog/powering-the-next-architecture-shift-inside-gfs-approach-to-48v/))

  * **Gaon Cable** wins a 200 billion won busduct supply contract for a US AI cloud data center, marking a major infrastructure component win for the LS Cable subsidiary. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13224))




#### PCB & Components

  * **GIS** will build a dedicated MLCC equipment base in Gumi, South Korea, expanding domestic passive component manufacturing capacity for AI and automotive demand. ([thelec.net](https://www.thelec.net/news/articleView.html?idxno=13198))

  * **Taesung** supplies PCB wet-process equipment to Austria’s AT&S, extending Korean equipment makers’ reach into high-end substrate board manufacturing. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13199))

  * **Wolfspeed** reports fiscal Q4 2026 financial results as the SiC power device maker navigates capacity ramp and restructuring amid strong EV and industrial demand. ([Wolfspeed](https://daily.semidoped.com/files/doc_earnings/2026/q4/earnings-result/Wolfspeed_Q4_2026_Earnings_Release.pdf))




Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-august-20th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
