---
source: https://daily.semidoped.com/p/daily-update-june-22nd-2026
title: Daily Update - June 22nd, 2026
date: 2026-06-22
kind: clipping
genre: daily
audience: everyone
subtitle: Amazon selling Trainium externally, memory bottleneck optimizations, SSDs, floating datacenters, and cool optics data.
---
Google and Amazon are now both selling AI chips directly to data center operators. _Not just cloud rental. The hardware itself._ Who buys, and is “neocloud” still the right term for what comes next?

Also today: HBM test bottlenecks, floating datacenters, Hyundai absorbing Boston Dynamics, and really interesting data about the optics market. 

Let’s get into it. _— Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player._

* * *

### Amazon to sell Trainium chips externally

Amazon plans to sell its in-house Trainium AI chips directly to data center operators, joining Google, which announced a similar move in April, in offering custom silicon outside their own cloud platforms. The shift positions both hyperscalers as direct alternatives to Nvidia, whose chip business is valued at roughly $5 trillion and which counts Amazon and Google among its largest customers. EE Times reported the development, noting it marks a departure from the prior model in which hyperscaler-designed accelerators were available only through AWS and Google Cloud rentals. ([EE Times](https://www.eetimes.com/amazon-newest-gambit-selling-ai-chips/))

> _**Vik:** First Google started selling externally, and now Amazon. Their CUDA equivalent is called Neuron, and the software ecosystem is just as important. It is inevitable that companies making AI chips will feed themselves first, and then start selling to others. Competition is good._
> 
> _**Austin:** Who will be buying these TPUs and Trainiums? Surely neoclouds. And the obvious end customers renting those chips will be AI labs. But I’ll be super interested to understand which enterprise end customers sign up. According to the [WSJ](https://www.wsj.com/tech/ai/google-is-using-nvidias-playbook-to-build-a-rival-ai-chip-business-1eac86f9),_
> 
> _“Among them is Citadel Securities, a longtime Google Cloud customer that recently began using TPUs for some of its research software workloads. Josh Woods, the firm’s chief technology officer, said the company can run key workloads at a 30% lower cost and up to four times as fast with TPUs.”_
> 
>  _Relatedly, neocloud originally referred to “new GPU-only cloud” players like CoreWeave, and was meant to differentiate from traditional cloud service providers that also rent CPU, storage, etc like Amazon Web Services, Microsoft Azure, and Google Cloud. Will the term neocloud now also encompass XPUs or more broadly, any AI accelerator? I’d expect said neoclouds to eventually also stand up racks of AI accelerators from startups._
> 
> _Of course, if customers are demanding XPUs, one has to stop and ask why AWS and GCP don’t just expand their own fleet of XPU rentals and are instead selling them? Some reasons come to mind. The hardware rental business has a longer time-to-payback for the CapEx investment, plus it requires more datacenter buildouts and access to power. Selling the XPUs is a lot simpler and banks a quick ROI…_

* * *

### MangoBoost moves from DPU chips to server racks

[MangoBoost](https://www.mangoboost.io/), an AI data center DPU startup, is expanding from chip sales into complete server rack systems, CEO of MangoBoost Korea Kim Jang-woo said on June 19. The company is betting that customers increasingly prefer turnkey AI infrastructure over assembling servers themselves. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=11505))

Bold claim by MangoBoost: “**Outside of Nvidia, MangoBoost is the only company capable of delivering everything from chips to software as a unified offering.** ”

>  _**Vik:** Delivering optimized hardware is a much bigger deal than people think. MangoBoost’s software platform is called LLM Boost, and they integrate networking, storage, CPUs, and GPUs (from AMD) into racks providing turnkey solutions to deploy AI hardware._
> 
> _**Austin:** SemiAnalysis had a [nice post](https://newsletter.semianalysis.com/i/194395279/the-grand-unifying-theory-of-goodput) discussing the idea of “goodput”, namely: _
> 
> _“In the context of training,**goodput** is defined as the amount of useful work users can perform on their cluster. Goodput plays on the term throughput to mean that not all throughput is “good”. Lots of training throughput can be “bad” if a GPU fell of the bus, NCCL is stalling, or there is an OOM hiding around the corner during the next checkpoint save.”_
> 
>  _While that definition discusses training, obviously there’s tons of money on the table if inference isn’t fully optimized either. DPUs play an underappreciated role in offloading networking tasks from host CPUs and enabling high-throughput data access for KV caches, for example in[Nvidia’s STX](https://www.nvidia.com/en-us/data-center/ai-storage/stx/) platform:_
> 
> [](https://substackcdn.com/image/fetch/$s_!b9yZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fafa918a7-cc02-428b-9de6-a4687f6ac115_1580x1126.png)
> 
> _If MangoBoost is good at leveraging DPUs, they should be able squeeze more tokens out of the same hardware._
> 
> _I wonder what they can do with AMD’s[MI455X Helios](https://www.amd.com/en/blogs/2025/amd-helios-ai-rack-built-on-metas-2025-ocp-design.html) platform, which also has a Pensando DPU in it:_
> 
> [](https://substackcdn.com/image/fetch/$s_!taXU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdc8ef2c6-a7f0-4f9a-a714-e0495ee60d9b_960x538.jpeg)
> 
> _If MangoBoost can squeeze more tokens out of Helios than AMD… well then, they ought to be a great acquisition target._

* * *

### TSE builds HBM test handler doubling throughput

South Korean semiconductor test component maker TSE is developing a next-generation test handler aimed at doubling inspection throughput for high-bandwidth memory devices, the company said. The handler targets HBM production lines, where rising stack heights and tighter quality requirements have stretched test times and created a bottleneck for memory makers including SK Hynix, Samsung, and Micron. TSE, which supplies probe cards and test sockets to the major DRAM producers, said the new equipment is intended to improve manufacturing efficiency as HBM volumes scale to meet AI accelerator demand. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=11502))

> _**Austin:** The article says the engineering development will be done in 9 months from now or so:_
> 
> _“The companies plan to complete development of both the handler and die socket by March 2027. Once commercialized, the system is expected to alleviate testing bottlenecks that currently constrain throughput in HBM manufacturing lines.”_
> 
>  _But when will it actually be deployed at the big three and actually move the needle on amount of tested wafers per hour? Not until 2028 or later?_

* * *

### Imec details ferroelectric memory advances at VLSI Symposium

Belgian research institute imec presented two ferroelectric memory developments at the 2026 IEEE/JSAP Symposium on VLSI Technology & Circuits, targeting capacity, bandwidth, and energy-efficiency constraints in AI memory systems. The work covers low-voltage ferroelectric capacitors and vertically stacked ferroelectric field-effect transistors (FeFETs), positioned as alternatives to conventional DRAM and SRAM for high-density applications. Imec framed the research as a response to AI workloads pushing existing memory architectures beyond their limits. ([EE News Europe](https://www.eenewseurope.com/en/imec-unveils-ferroelectric-memory-breakthroughs-for-next-generation-ai-systems/))

> _**Vik:** New memory technologies are one of the long term escape hatches from our current memory shortage predicament. We need a breakthrough now, more than ever._
> 
> _**Austin:** imec is so cool. Vik we need to get there and talk to folks. It’s one of the most interesting R&D labs in the world._

* * *

### Phison Demos 28GB/s Pascari Gen6 SSD

Phison demonstrated a PCIe Gen6 Pascari SSD reaching 28GB/s sequential throughput at Computex 2026, alongside new additions to its Pascari enterprise lineup. The demo doubles the bandwidth of current Gen5 enterprise drives and positions Phison among the first controller vendors to publicly show working Gen6 silicon. The expanded Pascari portfolio targets AI training, inference, and high-capacity storage tiers in data center deployments. ([The SSD Review](https://news.google.com/rss/articles/CBMi6AFBVV95cUxNRndJRVZ2TXV2TDEycjl2UHVEbkQ4WjkxYjVCWVBPNi1XRlp3VHpUMllKaWgwOVI0ZVFSVVhIY3BGcVdCOHFEdWVzNC1CMzlfUG40Tk9XSGQ0SjhWRDhZMkNSWEJxdFRJTVZZRjRWRTdjd1NWVG13bWd1Uk9kVUl3d3J4YmZ1V0E0RzljTGhtZVVONlRVdndUQUVLdm9NTnZXWnJ0ckx5c05Ed0VOc0JUbHhhU21UVVl0bkhuZ1dEenlJM3pBOWFFZW5VQVFGR2toX2RtdUc0MEVNdFE4aEZiRHpKRDRSM2VT?oc=5))

* * *

### Samsung Heavy, Supermicro plan floating AI data centers

Samsung Heavy Industries has partnered with Supermicro and a Greek shipowner to develop 50MW floating AI data centers, according to Hydrogen Central. The vessels are designed to be powered by solid oxide fuel cells running on liquefied natural gas. Samsung Heavy will lead the shipbuilding, while Supermicro supplies the compute infrastructure housed onboard. ([Hydrogen Central](https://news.google.com/rss/articles/CBMivgJBVV95cUxPZGhaMG0xTWtfZ1V3bmZ3Yjh6d1diWlZIYURMaGl1WHY2TU1SR28xWnYwY1lLejFIbTdHaWtMSUhFeldkUWdvbTliUy1wbWpITHF5NUZodm5FcmFIbUlZbkFnOUx1aU9oMnJjZDM3aUdpY0wwU20ybkd0VzU4NV8yMXBXN2tySF9zZWpBdk91VTdZUEFrOXJ0NkxTdkRIR1l4NC1pSG54dWZKWGItRklHWnBvWk5vR1F6bjBLaTBKajJTWmw3cExOQTRXMjBNLXlnV1EzZG9KRHh4ZlRGeUp4allPZmFvQjYyZ29jbkxyYUNmT214X0s0R0llRWM4WnVjSEFRNElLVGhuaDBYUWtUVWhyMVB1V21XcW9qTFprUHQ1aDB5T2QxWVBlRHBvRUd6VzJ2bGh0aHowaGF2R0E?oc=5))

> _**Vik:** Ha! First we want to chuck data centers in space, now we want to bob them on the oceans. I bet they could double as AI powered weather stations making sea-faring even safer. Also, [BE 0.00%↑](https://substack.com/search/%24BE) for floating data centers? _

* * *

### Hyundai acquires Boston Dynamics, plans 25,000 Atlas robots for factories

Hyundai Motor Group is paying $325 million to acquire SoftBank’s remaining stake in Boston Dynamics, bringing its ownership to 100%. Hyundai plans to deploy over 25,000 Atlas robots across its global plants, starting with its Metaplant near Savannah, Georgia, by 2028. A dedicated humanoid factory is targeting 10,000 to 30,000 units annually by around 2030. ([finance.yahoo.com](https://finance.yahoo.com/technology/ai/articles/softbank-walks-away-boston-dynamics-173021881.html))

> _**Austin:**_ _Well, we lost Boston Dynamics from America’s grip, but at least we’ll see some deployment and operation know-how reside in America. Savannah Bananas home game in 2028 + a Metaplant visit? Hyundai call us!_

* * *

### SK Hynix surpasses Samsung as South Korea’s most valuable company

SK Hynix’s market capitalization reached $1.362 trillion, overtaking Samsung Electronics. This occurred as SK Hynix shares closed 5.6% higher on Monday, lifting its market capitalization to 2.080 quadrillion won. Samsung shares ended 0.1% lower, taking its market value to 2.067 quadrillion won. ([wsj.com](https://www.wsj.com/tech/sk-hynix-tops-samsung-to-become-south-koreas-most-valuable-company-279419a0))

* * *

### Key Data #1

A single AI training cluster now requires more optical and photonic components than the entire worldwide volume of such components in 2008. (via [jwt0625](https://x.com/jwt0625/status/2068729190011322775))

[](https://substackcdn.com/image/fetch/$s_!nZLr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9277300a-32ac-42f6-9b85-9532f38ed450_2258x2129.jpeg)

* * *

### Key Data #2

According to Goldman Sachs, here is the breakdown of the BoM of a CPO switch. (via [omercheema](https://x.com/omercheema/status/2067327524544094510))

[](https://substackcdn.com/image/fetch/$s_!b1Ze!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff2be81fa-ebde-4140-add8-8f922b7a6bc9_804x517.jpeg)

* * *

## Supply Chain Insight

So. Many. Companies.

[Dan Nystedt@dnystedtStory includes list of suppliers to TSMC's CoPoS pilot line. Really outstanding article. (AI helped, company names confirmed): Breakdown of TSMC’s CoPoS Equipment List 1\. Lithography and Coating TSMC has introduced a highly comprehensive lineup for exposure and coating12:58 AM · Jun 22, 2026 · 8.86K Views

* * *

2 Replies · 8 Reposts · 43 Likes](https://x.com/dnystedt/status/2068861242761241062?s=20)

* * *

## Worth a Watch

How AI interconnects are built — a nice video by Lightmatter.

* * *

## Worth a Read

[FADU’s blog post](https://blogs.fadu.io/cmx-ssd-for-ai-inference/) on CMX using SSDs is highly informative. The table below explains how the needs for Agentic AI differs from traditional storage.

[](https://substackcdn.com/image/fetch/$s_!dISo!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F705a75f5-b516-4284-94f0-72a5616acac9_1576x824.png)

* * *

## Sector Watch

#### Foundry & Logic

  * **Intel and Apple** Intel shares rose ~9% after Trump announced Apple agreed to design and manufacture chips in the U.S. with Intel, shifting significant volume from TSMC and validating Intel’s foundry strategy with a lighthouse customer. ([TechMeme](https://www.techmeme.com/260618/p14#a260618p14))

  * **Samsung and AMD** Samsung leveraging excess fab capacity to secure AMD as advanced node customer, carving supply share from TSMC and testing pricing power in the foundry oligopoly. ([com.tw](https://www.ctee.com.tw/news/20260618700154-430501))




#### Advanced Packaging

  * **TSMC** Advancing CoPoS panel-level packaging with glass substrates to replace CoWoS silicon interposers, targeting mass production Q4 2028 or Q1 2029 to align with Nvidia’s next-gen accelerators. ([com.tw](https://www.ctee.com.tw/news/20260620700209-430501))

  * **MPI Corporation** Weighing prepayment mechanism to secure probe card capacity amid AI-driven supply constraints, highlighting test infrastructure as binding constraint on accelerator throughput. ([DigiTimes](https://www.digitimes.com/news/a20260618PD208/mpi-ai-chip-probe-card-test-interface-demand.html))




#### Networking

  * **Nvidia and optical interconnects** Acceleration to 1.6T and 3.2T standards exposing copper limits, driving structural shift toward silicon photonics and MicroLED in Taiwan supply chain. ([DigiTimes](https://www.digitimes.com/news/a20260617PD211/microled-siph-cpo-optical-communications-supply-chain-taiwan.html))

  * **Arista Networks** Deploying 1.6T Ethernet switches for AI cluster interconnects, challenging Nvidia’s NVLink dominance with open, disaggregated alternative for hyperscale datacenters. ([eenewseurope.com](https://www.eenewseurope.com/en/arista-rolls-out-1-6t-networking-switches-for-ai-fabrics/))




#### Optics & CPO

  * **JX Nippon** Expanding Indium Phosphide substrate capacity to meet rising demand for optical interconnects in datacenters, supporting transition toward optical I/O as critical bottleneck for hyperscale AI. ([Semiconductor Today](https://semiconductor-today.com/news_items/2026/jun/jx-170626.shtml))




#### Power

  * **BWX Technologies** Licensed small modular reactor design following activist pressure; NRC reforming licensing framework to accelerate nuclear plant approvals for AI datacenter energy demand. ([Bloomberg Tech](https://www.bloomberg.com/news/articles/2026-06-17/bwx-agrees-to-license-nuclear-reactor-design-after-activist-push))




#### Components

  * **MLCC shortage** AI accelerator density driving structural shortage in multi-layer ceramic capacitors, forcing hyperscalers to secure long-term supply contracts before chip deliveries. ([South China Morning Post](https://www.scmp.com/tech/article/3357603/tiny-capacitor-huge-demand-ai-frenzy-driving-mlcc-prices-higher))




Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-june-22nd-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
