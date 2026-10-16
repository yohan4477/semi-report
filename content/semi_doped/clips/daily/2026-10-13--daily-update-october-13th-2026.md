---
source: https://daily.semidoped.com/p/daily-update-october-13th-2026
title: Daily Update - October 13th, 2026
date: 2026-10-13
kind: clipping
genre: daily
audience: everyone
subtitle: ASML unveils Hyper NA EUV for 5nm patterning, Microsoft Maia 300 targets Azure at multi-GW scale by 2027, CRDO adopts microVCSELs.
---
**Hello world, it’s Tuesday, October 13th.**

**We are at OCP this week, and there is so much excitement in the air. The conference is PACKED, with lines going out the door and into the street. Lots still going on in the world…**

ASML unveiled a Hyper NA EUV system targeting 5nm single-exposure patterning ahead of its earnings report this week. Elsewhere, Microsoft’s Maia 300 is headed for multi-gigawatt Azure deployments by 2027, China’s CXMT is claiming a denser 4F² DRAM cell architecture without EUV, and Applied Materials opened its $5 billion EPIC Center in Silicon Valley.

Let’s get into it. — _Austin & Vik_



 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

### Presented by Crusoe

Crusoe builds the full stack for AI, from power and data centers to the cloud. It can also help you tune a small model on your own data for just a few bucks.

For repeatable work like reports, an open model trained on your terminology and formats can match a frontier model, and it’s cheaper and faster to run.

Crusoe’s Serverless Fine-Tuning handles the training: upload your dataset, pick an open model like Llama, DeepSeek, or GLM, and pay per million tokens used, not per GPU hour. 

**About $2 buys roughly 5M training tokens on smaller models.**

Deploy on Crusoe Cloud in one click or download the weights and deploy on your own.

**[Get $5 in credit to start →](https://semidoped.com/crusoe-daily)**

### ASML Reveals Hyper NA EUV System Capable of 5nm Single-Exposure Patterning

ASML has [unveiled a Hyper NA EUV lithography system](https://www.digitimes.com/news/a20261013PD234/asml-euv-5nm-high-na-euv-commercial.html) targeting 5nm single-exposure patterning, extending the company’s roadmap beyond its current High-NA platform. Single-exposure capability at that resolution removes the need for multi-patterning workarounds that add cost and process complexity at leading-edge nodes. The disclosure sets a technical anchor for sub-2nm scaling across the industry. Timing is deliberate: ASML reports earnings this week, and according to Bloomberg, [guidance on capacity buildout](https://www.bloomberg.com/news/articles/2026-10-13/asml-s-guidance-key-to-instill-confidence-in-fragile-chip-trade) has become a central test for investors already nervous about the chip sector’s unsteady rally. The Hyper NA announcement gives ASML something concrete to stand behind when those questions arrive.

### Microsoft Maia 300 Multichiplet Chip Targets Gigawatt-Scale Nvidia Displacement

Microsoft has unveiled the Maia 300, a multichiplet inference accelerator it [plans to deploy at multi-gigawatt scale across Azure data centers by 2027](https://www.bloomberg.com/news/articles/2026-10-12/microsoft-prepares-to-put-gigawatts-of-its-chips-in-data-centers), with cost reduction cited as the explicit mandate behind the program. The chip uses a multichiplet architecture, a departure from the monolithic die approach that has defined GPU design, and targets roughly 40% more tokens per second than its predecessor. Reuters reported the rollout is framed internally as a structural move to reduce dependence on outside semiconductor suppliers, Nvidia chief among them. Microsoft expects to stock multiple gigawatts worth of Maia 300 capacity, a deployment scale that would represent one of the largest commitments to proprietary inference silicon any hyperscaler has announced. Axios noted that the announcement effectively makes every major Nvidia customer a potential competitor, as hyperscalers now have a concrete reference point for vertical silicon integration at cloud scale.

> **Vik:** _Whoever wins the compute race, SK Hynix already[locked the memory on the whole Maia fleet](https://www.viksnewsletter.com/p/twic-maia-200-h200-in-china-microns) back at Maia 200. The memory trade doesn’t care which ASIC wins. And 7x rack throughput over Maia 200 on N2P is a real jump._
> 
> **Austin:** _Multi-GW sounds like a lot until you put it next to the 38 GW Microsoft is targeting by 2032. There’s plenty of room for both Maia and Nvidia in that._

### CXMT Claims Denser DRAM Cell Architecture, Rattling Samsung and SK Hynix

China’s largest memory maker CXMT says it has shifted to a 4F² cell architecture for DRAM, a denser layout it adopted specifically because EUV lithography remains out of reach, according to [reporting by Bloomberg](https://www.bloomberg.com/news/articles/2026-10-13/china-s-cxmt-claims-memory-breakthrough-ahead-of-samsung-hynix). The design reportedly lets CXMT pack more cells per wafer without EUV, and the company is targeting server DDR5 as its next commercial milestone, putting it on a collision course with Samsung and SK Hynix in one of memory’s highest-margin segments. Shares of both Korean chipmakers fell on the news, Seoul Economic Daily reported, while Micron also dropped. CXMT is funding the push partly through a large domestic IPO and captive Chinese demand, with economy.ac noting that [leaked Korean process knowledge](https://economy.ac/news/2026/10/202610295832) has accelerated the timeline. Wall Street is divided on how deep the threat runs, with some analysts treating the selloff as overdone.

> **Austin:** _Announced, not shipping. But with Samsung reportedly ~80% sold out for 2027, does CXMT even need great yields to find server DDR5 buyers in China?_

### OCP Summit Brings Vera Rubin Specs and AMD Helion Racks Into the Open

At the OCP Global Summit in San Jose, [Nvidia opened its Vera Rubin architecture](https://blogs.nvidia.com/blog/ocp-global-summit-vera-rubin-scale-ai-factories/) to the broader ecosystem, publishing specifications intended to help partners build interoperable AI factory infrastructure at gigawatt scale. AMD simultaneously debuted Helion at full rack scale, targeting agentic AI workloads. ODM partners moved fast: Wiwynn arrived on the show floor with physical Vera Rubin NVL72 and AMD Helion rack systems already built. Cisco and Nvidia jointly introduced a new pluggable optics form factor, with [Cisco President Jeetu Patel arguing](https://www.bloomberg.com/news/videos/2026-10-12/cisco-nvidia-tackle-ai-s-growing-data-center-bottleneck-video) that AI agents will consume far more network bandwidth than humans running equivalent tasks. Meta disclosed IcePack liquid-cooled network racks, the 102.4T IceCube switch platform, and the MetaRoCE open-source transport protocol, while also launching the Open Switch Platform Architecture initiative inside OCP.

> **Vik:**_The new pluggable form factor from Nvidia + Cisco is interesting: USFP. Here is a comparison to XPO I posted on X._
> 
> [![X avatar for @vikramskr](<../_img/2026-10-13--daily-update-october-13th-2026/001_Rf_mIEz0.jpg> "https://substackcdn.com/image/fetch/$s_!TWOG!,w_40,h_40,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fpbs.substack.com%2Fprofile_images%2F1864653638054105088%2FRf_mIEz0.jpg") Vikram Sekar ✈️ OCP@vikramskrNVIDIA and Cisco’s USFP and Arista’s XPO are taking different routes to higher-density pluggable optics. USFP puts 16 electrical lanes at 400G into an OSFP-sized footprint using a new connector. That gets you 6.4T, with a path to 12.8T. XPO starts with 64 lanes at 200G for …![](<../_img/2026-10-13--daily-update-october-13th-2026/002_HUcYIBOaoAA1TVl.jpg> "https://pbs.substack.com/media/HUcYIBOaoAA1TVl.jpg")4:24 PM · Oct 12, 2026 · 6.13K Views
> 
> * * *
> 
> 6 Replies · 3 Reposts · 56 Likes](https://x.com/vikramskr/status/2109681504226033908?s=20)

### Applied Materials Opens $5 Billion EPIC Center to Speed AI-Era Chip Development

Applied Materials has unveiled its [Equipment and Process Innovation and Commercialization Center](https://www.globenewswire.com/news-release/2026/10/12/3379252/0/en/applied-materials-unveils-5-billion-epic-center-in-silicon-valley-to-accelerate-semiconductor-innovation-for-the-ai-era.html) in Silicon Valley, a $5 billion capital commitment the company describes as its largest ever. The facility is billed as the world’s largest dedicated to collaborative semiconductor process technology and manufacturing equipment R&D, designed to seat chipmakers, systems companies, equipment partners, and university researchers alongside Applied’s own engineers. CEO Gary Dickerson frames the initiative as a direct response to AI driving demand for faster innovation cycles, where speed now rivals raw technological capability. Bloomberg reports that Applied targets [doubling sales without a proportional increase in headcount](https://www.bloomberg.com/news/articles/2026-10-12/applied-materials-will-double-sales-not-headcount-thanks-to-ai), treating the EPIC Center as the infrastructure that makes that ratio plausible as AI-driven wafer demand climbs.

### Credo Launches 1.6T ZeroFlap Cable and SRMO Optical Standard for AI Racks

Credo Technology has simultaneously released its [1.6T ZeroFlap Active Light Cable](https://investors.credosemi.com/news-events/news/news-details/2026/Credo-Unveils-1-6T-ZeroFlap-Active-Light-Cable-Industrys-First-Row-Scale-Wide-Parallel-Optical-Interconnect-for-AI-Data-Centers/default.aspx) and initiated a Short-Reach Micro-Emitter Optics standardization workstream under the Open Compute Project, with ams OSRAM, Lumentum, Corning, and Astera Labs joining as founding contributors. The ZeroFlap cable is billed as the industry’s first row-scale, wide-parallel optical interconnect, targeting AI data center scale-up and scale-out applications, with customer shipments expected in 2027. The SRMO initiative aims to define a common specification for micro-emitter-based optical links inside AI racks, covering both intra-rack and rack-to-rack distances. Lumentum, Corning, and Astera Labs are separately [planning a live demonstration](https://investor.lumentum.com/financial-news-releases/news-details/2026/Lumentum-Astera-Labs-and-Corning-to-Demonstrate-1060-nm-VCSEL-Based-PCIe-over-Optics-for-AI-Rack-Scale-Connectivity-at-the-2026-OCP-Global-Summit/default.aspx) of 1060 nm VCSEL-based PCIe-over-optics at the 2026 OCP Global Summit, a data point that puts the supplier ecosystem’s hardware commitments on a visible timeline.

> **Vik:** _Micro-emitters are the wide-but-slow play - lots of emitters in parallel at modest speeds instead of flogging a few channels. This is exactly the mid reach gap I[flagged for active copper](https://www.viksnewsletter.com/p/how-rack-power-density-is-opening-acc-market), now going optical, with 50m reach closing the copper to pluggable hole. SRMO as an OCP standard means Credo wants an ecosystem, not a one off cable._
> 
> **Austin:** _Fast. Credo only closed the Hyperlume (microLED) acquisition a year ago, but seem to have pivoted to microVCSELs. MicroLEDs are falling behind._

###  Sector Watch

#### Compute & Edge

  * **d-Matrix** announces Squadron multi-rack AI inference clusters at data-center scale, days after reports Nvidia is set to invest in the startup at a $5 billion valuation. ([PR Newswire](https://www.prnewswire.com/news-releases/d-matrix-announces-squadron-compute-clusters-for-ai-inference-at-data-center-scale-302906041.html))

  * **Marvell** unveils second-generation Structera X CXL 3.2 memory expanders — the industry’s first six-channel design — targeting AI inference memory bandwidth bottlenecks. ([Marvell](https://investor.marvell.com/news-events/press-releases/detail/1037/adding-and-replacing-marvell-unveils-second-generation-structera-x-industry-first-six-channel-cxl-3-2-memory-expanders-for-ai-inference))

  * **Intel** officially names its Crescent Island data-center AI inference GPU the GPU D-Series, releasing full performance specifications ahead of launch. ([ServeTheHome](https://www.servethehome.com/intels-crescent-island-ai-server-gpu-gets-a-name-and-specs-meet-the-intel-gpu-d-series/))




#### Memory & Storage

  * **SK Hynix** discloses the H-TPU controller architecture featuring over 100 small processors, targeting in-memory transaction processing for AI workloads. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=14536))

  * **Kioxia** launches the CM9-DLC enterprise SSD with direct liquid cooling support, targeting AI data-center thermal demands in dual-port E3.S form factor up to 30.72 TB. ([TechPowerUp](https://www.techpowerup.com/353631/kioxia-introduces-direct-liquid-cooling-support-for-enterprise-ssds?amp))

  * **Reuters** reports global smartphone shipments recorded their worst third quarter in 14 years, with a memory shortage cited as a primary constraint on device supply. ([Reuters](https://www.reuters.com/business/retail-consumer/global-smartphone-shipments-record-worst-third-quarter-14-years-amid-memory-2026-10-12/))




#### Foundry & Packaging

  * **Hua Hong** deepens partnerships with domestic Chinese equipment suppliers and sets a target to strengthen its specialty foundry market share by 2030. ([digitimes](https://www.digitimes.com/news/a20261013VL216/equipment-2030-production-wafer-manufacturing.html))

  * **ERS electronic** launches a fully automated panel-level packaging system for 310×310 mm substrates, integrating temporary bonding and debonding in one platform. ([Semiconductor Digest](https://www.semiconductor-digest.com/ers-introduces-automated-310mm-panel-level-packaging-system/?utm_source=rss&utm_medium=rss&utm_campaign=ers-introduces-automated-310mm-panel-level-packaging-system))




#### Power

  * **Bloom Energy / LS Electric** — LS Electric wins a $138 million order from Bloom Energy for U.S. data-center power systems, pushing cumulative LS Electric orders from Bloom above $500 million; LS Materials adds a separate $51.5 million ultracapacitor order from the same program. ([Bloom Energy](https://www.ad-hoc-news.de/boerse/news/corporate-news/ls-electric-signs-usd-138-46-million-deal-bloom-energy-stock-sits-25-34/70312626))

  * **Wolfspeed** receives a conditional commitment for up to $1.5 billion in U.S. Department of War loan funding to bolster domestic wide-bandgap semiconductor supply chain. ([Charged EVs](https://chargedevs.com/newswire/wolfspeed-gets-conditional-commitment-for-up-to-1-5-billion-us-department-of-war-loan/))

  * **Infineon** introduces the XDP8HD40S-1 high-voltage hot-swap controller extending its power portfolio from grid to core for 800 VDC AI server architectures. ([Infineon](https://www.ad-hoc-news.de/boerse/news/vorboerse/infineon-introduces-high-voltage-controller-for-ai-servers-stock/70310447))




#### Optics & Networking

  * **Celestica** introduces the DS6005 data-center switch with co-packaged optics, targeting power-efficient AI fabric interconnects at hyperscale. ([GlobeNewswire](https://www.globenewswire.com/news-release/2026/10/12/3378829/0/en/celestica-introduces-the-ds6005-data-center-switch-with-co-packaged-optics-to-enable-power-efficient-ai-fabrics.html))

  * **Qualcomm** unveils four AI broadband Dragonwing platforms at Network X 2026, while gFiber, Gemtek, and Qualcomm jointly debut an AI-native Wi-Fi 8 broadband gateway. ([Light Reading](https://www.lightreading.com/broadband/gfiber-teams-with-gemtek-and-qualcomm-on-wi-fi-8-router))

  * **Global Technology** and **ADST** partner to localize UV light sources used in co-packaged optics alignment equipment, reducing Korean CPO supply-chain dependency. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=14526))




#### PCB & Components

  * **Murata** is weighing additional investment to expand MLCC production capacity as AI server demand for multilayer ceramic capacitors continues to outpace supply. ([Bloomberg Tech](https://www.bloomberg.com/news/articles/2026-10-13/murata-weighs-further-capacity-expansion-to-meet-huge-ai-demand))

  * **HanWool Semiconductor** wins a contract from a Japanese MLCC maker to supply upgraded inspection equipment, the company’s latest design-win in passive-component quality control. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=14523))

  * **Intekplus** signs a 30.9 billion won contract to supply semiconductor substrate inspection equipment, its largest single order on record. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=14525))




#### Policy & Trade

  * **nLIGHT** will report its Q3 2026 financial results on November 5th. ([nLIGHT](https://investors.nlight.net/news-releases/news-details/2026/nLIGHT-to-Announce-Third-Quarter-2026-Financial-Results-on-November-5th/default.aspx))

  * **Tower Semiconductor** will release its Q3 2026 earnings on November 2, 2026, followed by a conference call for investors and analysts. ([Tower Semiconductor](https://towersemi.com/2026/10/12/10132026/))

  * **Nokia** signs a definitive agreement to sell its Enterprise Campus Edge business to AURELIUS, sharpening its strategic focus on AI-RAN and core network infrastructure.




_Tell us how to make Semi Doped better![ Give us your feedback](<../_img/2026-10-13--daily-update-october-13th-2026/003_poll> "http://semidoped.com/poll")! ❤️_Story 1

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-october-13th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
