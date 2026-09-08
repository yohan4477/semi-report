---
source: https://daily.semidoped.com/p/daily-update-august-5th-2026
title: Daily Update - August 5th, 2026
date: 2026-08-05
kind: clipping
genre: daily
audience: everyone
subtitle: AMD Q2 beat offset by weak AI outlook, Anthropic commits $10B to Volta Infrastructure, CoreWeave plans 360 MW in Indonesia, Kioxia and Samsung push NAND density at FMS 2026.
---
**Good morning, it’s Wednesday, August 5.**

AMD’s stock slid after its Q2 earnings call, where a weak forward AI sales outlook overshadowed a headline revenue beat. Anthropic also made waves with a $10 billion compute commitment to Volta Infrastructure, a cloud startup that barely existed six months ago, and the Trump administration is drafting a ban on Chinese data center component imports, sending optical stocks swinging.

Let’s get into it. _— Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

### US Drafts Ban on Chinese Data Center Imports, Optical Stocks Whipsaw

The Trump administration is [drafting a ban on imports of certain Chinese data center components](https://www.reuters.com/world/trump-administration-drafting-ban-chinese-data-center-devices-sources-say-2026-08-04/), targeting AI infrastructure supply chains in a move that landed with particular awkwardness for Innolight. The optical transceiver maker had completed a [$6.81 billion Hong Kong IPO](https://xenospectrum.com/en/fcc-innolight-optical-transceiver-ban/) just five days before Reuters broke the story. Innolight holds a significant share of the global optical transceiver market, and its shares led a broad selloff in Chinese optical names after the report hit.

Western rivals moved the opposite direction: Lumentum, Corning, and Marvell [surged on the news](https://www.barrons.com/articles/marvell-stock-price-corning-lumentum-china-ban-97074aa8) as investors priced in a substitution trade toward non-Chinese suppliers. The FCC is separately weighing its own restrictions on China-sourced optical transceivers, adding a second regulatory front. Bloomberg reported that the ban is [unlikely to hurt China’s overall export engine](https://www.bloomberg.com/news/articles/2026-08-05/china-s-official-newspaper-warns-us-over-expanding-tech-curbs), but the People’s Daily warned Washington against [expanding tech curbs](https://www.bloomberg.com/news/articles/2026-08-05/china-s-official-newspaper-warns-us-over-expanding-tech-curbs), a sign the measure is already generating diplomatic friction. The draft arrives while a fragile US-China trade truce remains in place, and Beijing’s state press rarely issues that kind of warning quietly.

Ripples from the debut:

  * Coherent, often named a primary beneficiary, may face its own [supply-chain complications](https://xenospectrum.com/en/fcc-innolight-optical-transceiver-ban/) given residual China manufacturing exposure, per XenoSpectrum.

  * Chinese optical makers including [Zhongji Innolight slumped](https://www.bloomberg.com/news/articles/2026-08-05/chinese-optical-stocks-slide-on-report-of-proposed-us-import-ban) in Hong Kong and mainland trading after the Reuters report.




> _**Vik:** This news hit the industry like a tsunami because building optical transceivers is low-margin business that is dominated by Chinese companies. If optical transceivers stop, the AI buildout stops. Period. There are several complications regarding what constitutes a Chinese sourced optical transceiver, and a lot of it is not clear. Here are some links to excellent coverage on this: [Cignal AI](https://cignal.ai/2026/08/fcc-ban-on-new-chinese-optical-modules/), [Funda AI](https://fundaai.substack.com/p/researchoptics-fcc-curbs-on-chinese)._
> 
> _**Austin**_**:** _I’m trying to understand the how a transceiver can be a security risk when it never touches the packets, and when the module makers are buying the components (DSPs, TIA, driver, laser, etc) inside the transceiver from American companies (Broadcom, Marvell, Lumentum, etc)._
> 
> _It seems a high-speed pluggable runs vendor firmware on its own MCU, and the CMIS spec has carried a standard firmware-download command since 2019. Here’s OIF (Optical Internetworking Forum)[webinar slides on the topic](https://www.oiforum.com/wp-content/uploads/OIF_CMIS_CDB_Seminar_Final_April_3rd_2024.pdf). Slide 27 says the spec deliberately leaves file signatures, security, and encryption to the vendor, and slide 38 notes many modules won’t let you read the image back out at all. _
> 
> _Hence, the trust model is “trust the module vendor”. I couldn’t find published examples of a compromised module. That doesn’t mean it’s not possible, of course._
> 
> _What’s interesting about policy decisions like this is the blast radius. The expensive silicon in an Innolight 800G module is usually a Broadcom or Marvell DSP. Ban the module and you impact Broadcom and Marvell volume too. And it’s not possible to just immediately ramp non-Chinese optical packaging and alignment capacity and labor…_

### AMD Beats on Revenue but Forward AI Guidance Leaves Investors Cold

AMD [tumbled in early trading](https://www.bloomberg.com/news/articles/2026-08-04/amd-sales-outlook-disappoints-investors-after-ai-fueled-rally) after its second-quarter earnings call, as an underwhelming sales outlook overshadowed a headline beat on current revenue. Shareholders had priced in faster momentum from the global AI data-center build-out, and the guidance didn’t clear that bar. AMD’s AI-powered revenue forecast failed to impress investors who had driven the stock up sharply on expectations of accelerating share gains against Nvidia.

The gap between what AMD delivered and what the market wanted centers less on today’s numbers than on the pace of displacement in hyperscaler accounts. For now, the sales outlook disappointed a market that had run hard into the print.

In related news:

  * AMD’s [Q2 financial results](https://ir.amd.com/news-events/press-releases/detail/1295/amd-reports-second-quarter-2026-financial-results) were reported as a beat on current-period revenue, per the company’s own release.

  * [Reuters coverage](https://www.reuters.com/business/amd-forecasts-upbeat-revenue-ai-data-center-demand-beats-quarterly-estimates-2026-08-04/) framed the AI forecast miss as the central story, noting the contrast with investor expectations built during the recent AI-fueled stock rally.




> _**Vik** : AMD posted 107% YoY growth in revenue in the datacenter market, but somehow failed to meet Wall Street expectations. It’s becoming a recurring trend in the AI hardware space where companies beat their guidance but still end up with tumbling stock prices. [Beyond the Hype has some great observations](https://open.substack.com/pub/enertuition/p/amd-firing-on-all-cylinders-but-lisa?r=222kot&utm_campaign=post-expanded-share&utm_medium=post%20viewer) about Lisa Su’s guidance style._
> 
> _**Austin:** I wouldn’t overthink the “stock dropped afterhours” bit. Shares rose 7% on the day and 13% on the week heading into the print, so measured from where that run started, the stock isn’t down much. _
> 
> _The quarter was good. Record $11.5bn, up 50%, data center now 58% of the company, and AMD telling analysts their 2027 estimates were too low. Su called the demand “unforecastable”. Though notice the supply constraint she described is CPU servers, which is a different story than GPU scarcity._
> 
> _It’s super encouraging that AMD’s revenue is now majority datacenter. Of course, a $6.7bn a quarter against Nvidia’s $75bn makes it clear no one is Nvidia, but a credible rackscale second supplier exists now, which wasn’t true a year ago._
> 
> _Yet its also interesting to see how “robbing Peter to pay Paul” is playing out, as datacenter is taxing AMD’s other half (consumer). Memory is getting pulled into AI, laptop prices are up, and AMD as a result expects the PC market to shrink this half._
> 
> _AI silicon also carries lower margins than the rest of AMD, so faster growth drags the blended number down. IMO this is fine, as incremental margin dollars pay the bills, not margin percentages._
> 
> _The next three to four quarters are arguably the most important of Lisa Su and Mark Papermaster’s entire AMD tenure. 2027 rests on the delivery of Helios, with first units shipping at the end of this quarter. Go make it happen!_

### Anthropic’s $10B Volta Pact Puts AI Chip Risk on New Lenders

Anthropic has committed [$10 billion in compute purchases](https://www.bloomberg.com/news/articles/2026-08-04/anthropic-inks-10-billion-computing-deal-with-new-cloud-startup) to [Volta Infrastructure](https://volta.com/), a London-based cloud startup that did not exist six months ago and carries a [$2.4 billion valuation backed by Nvidia and Dell](https://www.bloomberg.com/news/articles/2026-08-04/nvidia-dell-back-ai-cloud-startup-volta-at-2-4-billion-value). The deal hands Volta an anchor customer before the company has operated at any meaningful scale, which is either a vote of confidence in third-party infrastructure models or a sign that Anthropic simply needed somewhere to park its chip appetite. JPMorgan is providing a [credit backstop for Nvidia’s ecosystem](https://www.techtimes.com/articles/323047/20260804/anthropics-10b-norway-compute-deal-gives-nvidias-ecosystem-its-first-jpmorgan-credit-backstop.htm) tied to the arrangement, adding a layer of structured finance that earlier AI compute deals lacked. Volta’s data centers are slated for Norway, and the compute commitments are denominated in both dollars and euros, with the euro figure reported at [€8.6 billion](https://www.eu-startups.com/2026/08/london-ai-cloud-startup-volta-exits-stealth-at-2-4-billion-valuation-lands-e8-6-billion-compute-deal-reportedly-with-anthropic/).

> _**Vik:** A 6-month old startup has a $10B commitment? Do companies even do any due diligence anymore? I tried looking up this Volta Infra company, and found a [confusingly similar company doing a similar thing out of Singapore](https://www.voltainfra.com/). People don’t have time to come up with discrete names before Anthropic comes dropping compute dollars. SMH._

### FMS 2026: Kioxia, Samsung, SK Hynix Push NAND Density to AI-Era Limits

FMS 2026 in Santa Clara produced a concentrated set of memory advances aimed at AI inference workloads through 2027 and 2028. Kioxia and SanDisk jointly demonstrated [332-layer QLC NAND](https://www.businesswire.com/news/home/20260804147821/en/New-3D-Flash-Memory-Technology-from-Kioxia-and-Sandisk-Achieves-Industrys-Highest-Bit-Density-for-QLC-NAND) running at a [4,800 MT/s interface](https://www.tomshardware.com/pc-components/ssds/kioxia-and-sandisk-demonstrate-the-worlds-highest-density-3d-nand-flash-332-active-layers-and-up-to-4-800-mt-s-interface), which the companies claim represents the highest bit density achieved in 3D NAND flash. The tenth-generation design pairs the layer count with the faster interface to address the throughput gap that large-scale inference creates for flash storage. Kioxia’s [GP1 Series SSD](https://www.eagletribune.com/region/kioxia-announces-kioxia-gp1-series-super-high-iops-ssds-for-ai-applications/article_eb07259d-71ab-57e3-982c-9b7a3348efe4.html), built for high-IOPS AI applications, took Best of Show at the event..\

Samsung arrived with concept models rather than shipping silicon, introducing [zHBM and zNAND-O](https://news.samsungsemiconductor.com/global/samsung-unveils-next-gen-3d-memory-vision-at-fms-2026-charting-the-future-of-ai-infrastructure/?utm_source=rss&utm_medium=direct) as its vision for next-generation 3D memory architecture serving HPC and AI infrastructure. Bloomberg reported that Samsung framed the disclosures as part of a broader [3D-memory roadmap bid](https://www.bloomberg.com/news/articles/2026-08-04/samsung-reveals-new-3d-memory-roadmap-in-bid-for-ai-tech-lead) for AI technology leadership. SK Hynix and SanDisk separately unveiled the [industry’s first High Bandwidth Flash standard](https://www.thelec.net/news/articleView.html?idxno=12793) on August 4, specifying support for up to 512 GB capacity, six months after the underlying HBF technology was launched. The HBF specification is a joint effort designed to deliver both high capacity and high bandwidth from a single device class.

More from FMS 2026:

  * Silicon Motion showed storage controller solutions at [booth 315](https://siliconmotiontechnologycorporation.gcs-web.com/news-releases/news-release-details/huirongkejiliangxiang-fms-2026zhanshimianxiang-agentic-ai) targeting AI factory, edge AI, and physical AI workloads, with a focus on KV cache and agentic AI latency requirements.

  * Marvell [advanced its AI memory infrastructure portfolio](https://investor.marvell.com/news-events/press-releases/detail/1030/marvell-advances-ai-memory-infrastructure-portfolio-to-accelerate-agentic-ai-inference) at FMS to accelerate agentic AI inference.

  * Rambus introduced a [DDR5 RDIMM server chipset](https://www.allaboutcircuits.com/news/rambus-serves-up-ddr5-rdimm-server-chipset-for-next-gen-ai-data-centers/) aimed at next-generation AI data center deployments.




> _**Vik:** High Bandwidth Flash is seeming making progress and even big players like Google seem to be eager to lap up anything that does not involve DRAM in this memory crisis. CXL is another high signal option to watch out for; I am not at FMS, but I’ve heard from those who are that there is a lot of interest._

### Sector Watch

#### Foundry & Packaging

  * **Tower Semiconductor** posted Q2 2026 revenue of $460 million, up 24% year over year, and guided Q3 to $520 million, a 31% increase. ([Tower Semiconductor](https://towersemi.com/2026/08/04/08042026/))

  * **TSMC** resumes full operations at its Kumamoto fab after an earthquake-related shutdown, keeping Japan capacity on track. ([thelec.net](https://www.thelec.net/news/articleView.html?idxno=12826))

  * **Eugene Technology** completes development of a TiN ALD tool for sub-10nm DRAM, expanding Korea’s domestic process-equipment capability. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=12801))




#### Memory

  * **Entegris** posted Q2 2026 net sales of $883 million, up from $792 million a year earlier, with non-GAAP diluted EPS of $0.93. ([Entegris](https://investor.entegris.com/news/news-details/2026/Entegris-Reports-Results-for-Second-Quarter-of-2026/default.aspx))

  * **Everspin Technologies** and **MaxLinear** partner to develop persistent MRAM for metadata, log data, write buffering and cache in AI servers. ([Everspin](https://investor.everspin.com/news-releases/news-release-details/everspin-technologies-and-maxlinear-collaborate-advance-memory))

  * **LB Semicon** wins Qualcomm production approval and begins mass production of Qualcomm power management ICs this month. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=12785))




#### Optics & Networking

  * **Furukawa Electric** plans $635 million in optical fiber and cable capacity expansion across Japan, US, Brazil, and India to meet surging AI data center demand. ([Nikkei Asia](https://asia.nikkei.com/business/technology/artificial-intelligence/furukawa-electric-to-spend-635m-in-japan-us-brazil-india-amid-ai-boom))

  * **Ciena** , Quantum Corridor and Toshiba complete the world’s first 1.6 Tb/s quantum-safe optical encryption milestone on a live commercial network. ([Ciena](https://investor.ciena.com/news/news-details/2026/Quantum-Corridor-Ciena-and-Toshiba-Complete-Worlds-First-1-6-Tbs-Quantum-Safe-Optical-Encryption-Milestone-on-Live-Commercial-Network/default.aspx))

  * **Aehr Test Systems** receives a follow-on production order from its lead silicon photonics customer, extending its series-production momentum in that segment. ([Aehr Test Systems](https://www.aehr.com/2026/08/aehr-test-systems-expands-silicon-photonics-production-momentum-with-follow-on-production-order-from-lead-customer/))




#### Compute

  * **Lattice Semiconductor** posted record Q2 2026 revenue up 62% year-over-year, driven by record Compute & Communications revenue and the closed AMI acquisition. ([Lattice Semiconductor](https://ir.latticesemi.com/news-releases/news-release-details/lattice-semiconductor-reports-record-2q26-revenue-62-yoy))

  * **Microchip Technology** and **Micron** jointly demonstrate a high-performance PCIe Gen 6 storage architecture targeting AI and data center infrastructure. ([Microchip](https://ir.microchip.com/news-events/press-releases/detail/1407/microchip-technology-in-collaboration-with-micron-technology-demonstrates-high-performance-pcie-gen-6-storage-architecture-for-ai-and-data-center-infrastructure))




#### Edge

  * **FuriosaAI** will deploy 7,000–8,800 RNGD NPU accelerators at a new 15 MW Swedish data center, marking the Korean AI chip startup’s first major European footprint. ([Chosunbiz](https://biz.chosun.com/en/en-it/2026/08/05/E5BOKAKASJH35JMBNXGVF7DTNI/))

  * **Nvidia** makes its Alpamayo 2 Super frontier open model for robotaxis and autonomous vehicles available for commercial use. ([Nvidia News](https://blogs.nvidia.com/blog/alpamayo-2-super-open-model-now-available/))




#### Policy & Trade

  * **Reuters** reports the US is weighing a polysilicon price floor and new tariffs to counter Chinese dominance in solar and semiconductor-grade polysilicon supply. ([Reuters](https://www.reuters.com/world/china/us-weighs-polysilicon-price-floor-tariffs-counter-china-solar-chips-2026-08-04/))

  * **Samsung** and **SK Hynix** are reportedly evaluating Chinese chip equipment as a hedge against escalating US export-control risk on foreign tools. ([slguardian.org](https://slguardian.org/samsung-and-sk-hynix-evaluate-chinese-chip-equipment-as-us-export-controls-loom/))

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-august-5th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
