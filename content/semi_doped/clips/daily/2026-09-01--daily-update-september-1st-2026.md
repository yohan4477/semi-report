---
source: https://daily.semidoped.com/p/daily-update-september-1st-2026
title: Daily Update - September 1st, 2026
date: 2026-09-01
kind: clipping
genre: daily
audience: everyone
subtitle: CXMT enters HBM3E risk production, ASML High-NA EUV hits volume logic, Samsung Electro-Mechanics wins $780M MLCC deal, Kioxia and SanDisk commit $31B to Japan NAND.
---
**Hello world, it’s Tuesday, September 1st.**

China’s CXMT has begun small-batch HBM3E production with a 2027 mass-output target, making it the first Chinese manufacturer to reach even trial-stage output of the memory that powers AI accelerators. ASML’s High-NA EUV tool has entered high-volume logic production for the first time, and Kioxia and SanDisk are committing a joint $31 billion to expand NAND capacity in Japan.

Let’s get into it. _— Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

_Tell us how to make Semi Doped better![ Give us your feedback](http://semidoped.com/poll)! ❤️_

### China’s CXMT Enters HBM3E Risk Production With 2027 Mass-Output Target

Chang Xin Memory Technologies has begun small-batch production of HBM3E chips, according to reporting from Seoul Economic Daily and Korea JoongAng Daily, marking the first time a Chinese manufacturer has reached even trial-stage output of the high-bandwidth memory that powers AI accelerators. Alibaba is [reportedly in early testing of the chips](https://en.sedaily.com/international/2026/09/01/chinas-cxmt-starts-small-scale-hbm3e-output-alibaba-seen), making it the first named customer for a Chinese-made HBM product. SK Hynix, Samsung, and Micron currently hold the entire commercial market. Tom’s Hardware [puts a mass-production timeline at 2027](https://www.tomshardware.com/pc-components/dram/cxmt-reportedly-begins-risk-production-of-hbm3e-memory-in-breakthrough-for-chinese-dram-production-company-could-be-in-mass-production-in-2027), a date that would give CXMT roughly two years to close a yield and stacking-process gap that took Korean firms years to narrow. Risk production means usable parts come out, not that the economics work yet.

> **Vik** : _The Information reported that CXMT might be 3-5 years away from have HBM3e ready for mass market. China does not pose a threat to HBM any time soon. In the era of custom base die, the gap gets even wider if China does not access to EUV-class logic nodes._

### Architect Labs Claims AI-Designed Accelerator Beats Jetson Orin Nano 3.4x on Performance Per Watt

Architect Labs has published a paper describing Redwood, an AI accelerator it says was designed, verified, and deployed end-to-end by an AI system from a high-level specification provided by two human architects. The system autonomously generated RTL, UVM environments, formal proofs, firmware, and compute kernels in under two weeks, with every block reaching 95% coverage. Redwood Nano, the FPGA variant running on an AMD Versal VPK180 at 250 MHz, ran Qwen3-0.6B inference and, when projected onto Samsung 8 nm, is claimed to deliver 1.75x the decode throughput at 1.9x lower power than a measured Nvidia Jetson Orin Nano baseline, a 3.4x performance-per-watt gain. The paper also notes that Qwen running on Redwood was used to help design the next-generation Redwood, which the team describes as an early step toward recursive self-improvement.

[](https://substackcdn.com/image/fetch/$s_!yxE-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb57c42b1-f397-47d5-870b-36d41af9cdfa_922x924.png)

**Sources:** [architectlabs.com](https://architectlabs.com/architect-labs-redwood.pdf)

> **Austin:**_A proof-of-concept running on an FPGA, but still the fact this was designed in two weeks with only the specs and guidance from the architects is incredible._
> 
> _**Vik:** Everybody be vibe codin chips these days. Never would have thought this would have ever been possible 10 years ago. Great times we live in._

### ASML High-NA EUV Enters High-Volume Logic Production for First Time

ASML confirmed that its High-NA EUV lithography tool has [reached its first high-volume logic product](https://www.digitimes.com/news/a20260901VL216/asml-euv-taiwan-performance-wafer.html), marking the technology’s transition from development and early qualification into full production deployment. The milestone validates the manufacturing path chipmakers have mapped toward sub-2nm process nodes, where High-NA’s tighter numerical aperture enables the finer patterning that conventional EUV cannot achieve at scale. The gap this creates looks durable: UBS Group analysts [predict China is unlikely to develop a viable alternative](https://www.bloomberg.com/news/articles/2026-09-01/china-unlikely-to-match-asml-s-top-tool-in-next-decade-ubs-says) to ASML’s top lithography tool within the next decade, citing the depth of engineering complexity involved. That’s a long runway for chipmakers already running the machines.

> **Vik:**_Who’s buying these things that cost $400M? TSMC has been against high-NA EUV if I remember right, because they consider it too expensive. I’m guessing Intel then; they won’t want to miss this bus like they missed the EUV bus at 10nm._

### Samsung Electro-Mechanics Lands $780 Million MLCC Deal for AI Servers

Samsung Electro-Mechanics disclosed a [1.07 trillion won MLCC supply contract](https://www.thelec.net/news/articleView.html?idxno=13508) with a global customer, a figure Korea Times converts to roughly $780 million, making it the largest single passive-component order the company has publicly reported. The buyer hasn’t been named, but multiple Korean outlets describe the counterparty as a major global tech company with AI server procurement at the center of the deal. MLCCs, the small ceramic capacitors that filter power across every circuit board in a server rack, typically attract none of the attention lavished on GPUs or HBM, yet this contract lands at a scale that sits comfortably alongside significant logic and memory supply agreements. 매일경제 identifies Samsung Electro-Mechanics as [the leading MLCC supplier for AI server applications](https://www.mk.co.kr/en/business/12141548), a position this contract would reinforce considerably.

> **Vik:**_MLCC is a classic bottleneck trade. Nobody ever cared for these small capacitors on boards. All of a sudden everybody wants it to power their GPU boards. Hilarious!_

### Kioxia and SanDisk Commit $31 Billion to Expand Japan NAND Capacity

Kioxia and SanDisk have [announced a joint $31 billion investment](https://www.eetasia.com/kioxia-and-sandisk-plan-31b-japan-investment-to-expand-nand-capacity/) in Japan to expand NAND flash memory production, one of the largest single capacity commitments the sector has seen. The two companies, long-standing partners in Yokkaichi and Kitakami fab operations, plan to channel the funds into building out manufacturing capacity at those sites. The scale of the spend reflects sustained confidence in storage demand, particularly from AI infrastructure buildout, where data centers require ever-larger volumes of NAND for both training and inference workloads. Together the partners control a substantial share of global NAND supply, so output from this expansion will carry real weight when it hits the market.

> **Vik** : _NAND will continue to be important in the age of AI. Everything just cannot live on DRAM, and[we know of ways to make NAND fast](https://semidoped.com/episodes/weka-s-val-bercovici-kv-cache-deepseek-v4-hbf-slc-vs-qlc-nand-cxl-nvlink-tokenomics/)._

### Sector Watch

#### Foundry & Packaging

  * **TSMC** 1.4nm fab expansion in Taichung is running ahead of schedule, accelerating the N14 node ramp toward volume production. ([Taiwan News](https://www.taiwannews.com.tw/en/news/6431272))

  * **JCET** raises its 2026 capital expenditure plan to CNY10 billion (~$1.4B) as AI advanced-packaging demand outpaces earlier forecasts, per DigiTimes. ([digitimes](https://www.digitimes.com/news/a20260901VL201/packaging-demand-jcet-2026-capex.html))

  * **LG Electronics** taps Samsung Foundry for AI home chips through a CoAsia SEMI-led consortium under South Korea’s K-On-Device AI program. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13484))




#### Memory

  * **SK Hynix** $4 billion U.S. HBM advanced-packaging facility advances as the company targets domestic production of high-bandwidth memory for American customers. ([EE Times](https://www.eetimes.com/sk-hynixs-4b-hbm-project-targets-u-s-chipmaking-gap/))

  * **Micron** Taiwan factory unions threaten strike over unresolved bonus dispute, raising near-term supply-continuity risk at a key DRAM site. ([Reuters](https://www.reuters.com/business/world-at-work/microns-taiwan-unions-threaten-strike-over-bonus-dispute-2026-09-01/))

  * **OpenAI** compresses its Jalapeno custom-chip design cycle to just nine months, signaling an aggressive push toward proprietary AI silicon. ([digitimes](https://www.digitimes.com/news/a20260831PD212/openai-design-performance-2026-ai-chip.html))




#### Data Centers & Cloud

  * **Nscale** closes approximately $3 billion in debt financing for two US AI campuses in Texas and North Carolina totaling up to 315 MW of capacity. ([PR Newswire UK](https://www.prnewswire.co.uk/news-releases/nscale-closes-approximately-3-billion-in-financing-for-both-ward-county-texas-and-madison-county-north-carolina-ai-deployments-302865202.html))

  * **Microsoft Azure** and **AWS** launch Azure Multicloud Interconnect, a direct cross-cloud networking link marking the first formal hyperscaler interconnect between the two largest cloud platforms. ([Microsoft Azure](https://azure.microsoft.com/en-us/blog/introducing-azure-multicloud-interconnect-for-aws/))

  * **Anthropic** signs a reported $35 billion multi-year cloud infrastructure agreement with Nvidia-backed Lambda, anchoring capacity at Hut 8’s 1 GW Beacon Point campus in Texas. ([Data Center Dynamics](https://www.datacenterdynamics.com/en/news/anthropic-signs-35bn-cloud-agreement-with-lambda-report/))




#### Compute & Edge

  * **AWS** launches EC2 R9g and R9gd instances powered by Graviton5, its first memory-optimized instances on the new in-house Arm processor. ([AWS Blogs](https://aws.amazon.com/blogs/aws/amazon-ec2-r9g-and-r9gd-instances-powered-by-aws-graviton5-processors-are-now-generally-available/))

  * **Qualcomm** raises chip prices starting September 1, a broad-based increase affecting Snapdragon and related product lines across mobile and edge markets. ([MacRumors](https://www.macrumors.com/2026/08/31/qualcomm-chip-price-increase/))

  * **Renesas** joins the Autoware Foundation to bring open-source end-to-end AI software to its ADAS and autonomous-driving silicon platforms. ([PR Newswire](https://www.prnewswire.com/news-releases/autoware-foundation-partners-with-renesas-to-accelerate-production-ready-end-to-end-ai-for-adas-and-autonomous-driving-302866054.html))




#### Optics & Networking

  * **THine** launches new VCSEL drivers and TIAs targeting ultra-low-latency, high-density scale-up networks for next-generation large-scale AI data centers. ([Business Wire](https://www.businesswire.com/news/home/20260831397063/en/THine-Announces-New-VCSEL-Drivers-and-TIAs-for-Ultra-Low-Latency-Lower-Power-High-Density-and-Cost-Effective-Scale-Up-Networks-to-Enable-Next-Generation-Large-Scale-AI-Datacenters))

  * **EV Group** releases a process solution addressing critical wafer-bonding and lithography manufacturing challenges specific to co-packaged optics production. ([PR Newswire](https://www.prnewswire.com/news-releases/ev-group-addresses-critical-manufacturing-challenges-for-next-generation-co-packaged-optics-302865636.html))

  * **Credo Technology** Toucan PCIe 6.x retimer achieves PCI-SIG compliance and joins the official PCIe 6.x Integrators List, clearing the path to data-center deployment. ([Investor Relations](https://investors.credosemi.com/news-events/news/news-details/2026/Credos-Toucan-PCIe-Retimer-Achieves-PCI-Express-Compliance-and-Joins-PCI-Express-6-x-Integrators-List/default.aspx))




#### Power

  * **GE Vernova** launches a medium-voltage UPS system engineered for AI data centers and other energy-intensive facilities requiring stable power protection. ([energiesmedia.com](https://energiesmedia.com/ge-vernova-mv-ups-ai-data-centers/))

  * **Fervo Energy** signs a record 396 MW geothermal power deal with **Google** for a Utah data center campus targeting a 2028 launch. ([Bloomberg Tech](https://www.bloomberg.com/news/articles/2026-09-01/fervo-signs-geothermal-power-deal-with-google-for-2028-launch))

  * **Diodes Incorporated** completes its $250 million all-cash acquisition of ElevATE Semiconductor, expanding its power and analog product portfolio. ([bisinfotech.com](https://www.bisinfotech.com/diodes-incorporated-completes-250-million-all-cash-acquisition-of-elevate-semiconductor/))




_Tell us how to make Semi Doped better![ Give us your feedback](http://semidoped.com/poll)! ❤️_

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-september-1st-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
