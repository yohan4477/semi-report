---
source: https://daily.semidoped.com/p/daily-update-june-16th-2026
title: Daily Update - June 16th, 2026
date: 2026-06-16
kind: clipping
genre: daily
audience: everyone
subtitle: VCSELs push into AI scale-up, AMD bets on flash-as-DRAM, TSMC goes glass, and Qualcomm is reportedly circling Tenstorrent
---
Today’s edition a bit longer because there’s a lot to pay attention to all at once. From VCSELs, to flash memory for AI, advanced packaging, and acqusition rumors. We are using Substack’s highlighting feature to help you scan quicker. Hope it helps!

Let’s get into it. _— Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

### **PicoJool Introduces 200G VCSELs for Scale Up AI Data Centers**

PicoJool, a Palo Alto optical connectivity startup, announced 200G VCSEL products with bandwidth above 37GHz, with chip-level samples starting next quarter and high-volume production expected in early 2027. The pitch is that VCSELs can now scale to AI data center bandwidth needs while staying close to copper on cost, with a roadmap toward 800G, 1.6T, and 3.2T. The company is working with hyperscalers and system startups on pluggable, NPO, and CPO designs.

The key angle is manufacturing rather than just the technology. PicoJool builds on a gallium arsenide supply chain through a partnership with WIN Semiconductor, which has shipped over a billion VCSEL chips for 3D sensing, so capacity is not the bottleneck that limits some competing laser approaches. Founder Al Yuen has a long VCSEL track record going back to gigabit Ethernet in 1996, and Pat Gelsinger of Playground Global framed the combination of record bandwidth plus existing production scale as a credible path from copper to optical at AI scale.

**Sources** : [Businesswire](https://www.businesswire.com/news/home/20260615089975/en/PicoJool-Introduces-200G-VCSELs-and-MicroVCSELs-for-Scale-Up-AI-Data-Centers)

>  _**Vik:** An important thing about VCSELs: they are based on GaAs, not InP. They are not subject to the same supply chain constraints as other optics tech today. If this actually works for scale up, it can basically seize the massive TAM. Lots of skepticism about VCSELs, but every major optics player including market heartthrobs like LITE are looking into it. Do not discount it just yet. If it has reach, data rate, and capacity, the tech in IN._
> 
> _**Austin:** VCSELs are a tried and true technology and work for short reach interconnects. Yes, it requires PAM4 + DSPs at 200G/lane, but you can nix the DSP and just do slow and wide to increase bandwidth, i.e. instead of 8x 200G/lane you can do 32x 50G/lane NRZ. _

### **AMD Acquires MEXT to Advance Memory Optimization**

MEXT has developed innovative AI-powered predictive memory technology designed to make flash behave more like DRAM, helping expand usable memory capacity while maintaining performance and efficiency. This approach has the potential to reduce infrastructure costs, improve resource utilization, and help customers more effectively scale general-purpose and AI workloads. 

The acquisition adds to AMD’s ability to deliver differentiated, full-stack compute and AI solutions. By integrating MEXT’s technology across the AMD data center portfolio, AMD expects to help enterprise customers unlock greater value from their infrastructure investments while accelerating AI deployment.

**Source** : [AMD](https://www.amd.com/en/blogs/2026/amd-acquires-mext-for-memory-optimization.html)

>  _**Vik:** Flash is becoming an increasingly important theme as DRAM’s price and lack of capacity fundamentally limits long-running agentic AI workloads. The sauce lies in understanding how to make NAND flash behave like DRAM and unlock the secrets of the agentic AI universe _😃
> 
>  _**Austin:** MEXT is software-only memory tiering that makes DRAM + flash look like a single, large, fast memory pool to applications, with no OS or app changes required._
> 
> _The core loop is basically_
> 
>  _1\. Classify — MEXT monitors which DRAM pages are hot (actively used) vs. cold (idle).  
>  2\. Offload — Cold pages are evicted to flash, which is 20x cheaper than DRAM.  
> 3\. Predict — AI predicts which flash-resident pages the application will request next.  
> 4\. Prefetch — Those pages are pulled back into DRAM before the application asks for them, so from the app’s perspective, the data was never gone._
> 
> _I met[MEXT CEO and Founder Gary Smerdon](https://www.linkedin.com/in/garysmerdon/) at an industry event last year and I remember thinking “This pitch sounds amazing, is it too good to be true?”_
> 
>  _AMD says nope, it’s real!_

### **TSMC Partners With Ibiden, Innolux On Glass Substrates**

TSMC is working with Japanese substrate maker Ibiden and Taiwanese display panel maker Innolux to develop chip-on-panel-on-substrate (CoPoS) packaging using glass substrates, according to a Digitimes report. The collaboration pairs Ibiden’s substrate expertise with Innolux’s panel-level manufacturing capabilities to advance CoPoS, a next-generation advanced packaging format that uses rectangular panels rather than the round wafers used in current CoWoS production. Glass substrates are being explored across the industry as a potential alternative to organic substrates for high-performance chips, offering improved dimensional stability and the ability to support larger package sizes.

**Sources:** [digitimes](https://www.digitimes.com/news/a20260616PD217/tsmc-innolux-ibiden-packaging-cowos.html)

>  _**Vik:** Glass panels for advanced packaging is becoming increasingly important as chip sizes for frontier accelerator chips get massive. This is however a 2028/29 story at the earliest before we see glass panels in production. CC Wei has said so quite clearly. But the suppliers to this tech will start showing profits much earlier. Watch for Ibiden and Innolux._

### **Qualcomm in talks to acquire Tenstorrent**

Qualcomm is in talks to acquire AI chip startup Tenstorrent, The Information reported, according to Reuters. Terms of the potential deal were not disclosed. Tenstorrent, led by chip designer Jim Keller, develops RISC-V-based AI processors and has raised funding from backers including Jeff Bezos and Samsung. Neither Qualcomm nor Tenstorrent has publicly commented on the report.

**Sources:** [The Information](https://www.theinformation.com/articles/qualcomm-talks-buy-tenstorrent-expand-ai-chip-capabilities)

>  _**Vik:** Why buy Tenstorrent when you’re building your own accelerator? Or is that not going too well?_
> 
> _**Austin:** Wouldn’t you want to acquihire Jim Keller? Engineers want to work with him. Qualcomm is known for having hardcore engineers as CEOs and leaders… I think Jim Keller would fit right in. _

### **TechInsights confirms SMIC N+3 node in Kirin 9030**

TechInsights has confirmed that Huawei’s Kirin 9030 processor is fabricated on SMIC’s N+3 process, according to a teardown analysis of the chip. The finding marks SMIC’s third-generation advancement of its 7nm-class node, narrowing the gap with TSMC’s 5nm technology despite US export controls that have blocked the Chinese foundry from accessing EUV lithography equipment. The Kirin 9030 powers Huawei’s latest smartphone lineup and represents the most advanced silicon produced domestically in China to date.

**Sources:** [TechInsights](https://www.techinsights.com/blog/smic-n3-confirmed-kirin-9030-analysis-reveals-how-close-smic-5nm)

>  _**Vik:** If SMIC N+3 node is almost like TSMC N5, I wonder what Tau Folding can do for transistor density going forward. It is amazing how much China is able to squeeze out of non-EUV nodes because they have no other choice._

### **Applied Materials launches 3D chip tools**

Applied Materials introduced two new systems aimed at manufacturing high-aspect-ratio 3D logic and memory chips. The Centris Spectral SiN ALD uses microwave plasma technology to deposit uniform silicon nitride films inside complex 3D structures, while the Producer Selectra Mo Etch performs selective molybdenum removal in tight geometries. Both tools target precision materials engineering challenges that emerge as logic transistors and memory cells move to vertically stacked architectures.

**Sources:** [Applied Materials](https://ir.appliedmaterials.com/news-releases/news-release-details/applied-materials-unveils-deposition-and-selective-etch-systems)

### **TSMC CoWoS shortfall seen halving by end-2026**

TSMC’s chip-on-wafer-on-substrate (CoWoS) advanced packaging supply-demand gap is projected to narrow from roughly 20% to 10% by the end of 2026, according to a TrendForce report. The tightening reflects ongoing capacity expansion at TSMC, which has been ramping CoWoS output to serve AI accelerator demand from customers including Nvidia, AMD, and Broadcom. CoWoS has been a persistent bottleneck for high-bandwidth memory integration on leading-edge AI chips since 2023.

**Sources:** [TrendForce](https://www.trendforce.com/news/2026/06/15/news-tsmc-cowos-supply-demand-gap-reportedly-seen-narrowing-from-20-to-10-by-end-2026-as-capacity-expands/)

>  _**Vik:** Good to have CoWoS expand capacity at a time when people are increasingly looking to going to Intel EMIB due to shortages._

### Stock Movers (June 15)

**WDC** ▲ +16.1%, **MRAM** ▲ +14.1%, **AAOI** ▲ +13.3%, **NBIS** ▲ +11.9%, **POET** ▲ +11.2%

## Quick Hits

  * **IQE** and **Tower Semiconductor** signed a multi-year supply agreement for indium phosphide epiwafers supporting Tower’s planned growth in InP silicon photonics. ([Tower Semiconductor](https://towersemi.com/2026/06/15/06152026/))

  * **GigaVis** signed a 7.2 billion-won contract to supply semiconductor substrate inspection equipment to an unnamed Chinese substrate maker, per The Elec. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=11347))

  * **AWS** officially launched Amazon EC2 M9g and M9gd instances powered by its in-house low-power Graviton5 CPU for general-purpose workloads. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=11329))

  * **Samsung Electro-Mechanics** is in talks with multiple global big tech companies to supply silicon capacitors for AI servers, expanding beyond its core MLCC business. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=11314))

  * **Ericsson** defended its purpose-built 5G chip strategy after Nvidia’s plans to build radio unit chips rattled investors and raised questions about telco economics. ([Light Reading](https://www.lightreading.com/5g/ericsson-defends-chip-strategy-as-nvidia-plan-rattles-investors)) 




### Key Data

NVIDIA is still KING! From “The Information”.

[](https://substackcdn.com/image/fetch/$s_!n5M0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c083773-849e-4535-ba24-af96edb4589f_1712x1136.jpeg)

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-june-16th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
