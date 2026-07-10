---
title: "Huawei AI CloudMatrix 384 – China's Answer to Nvidia GB200 NVL72"
source: "https://newsletter.semianalysis.com/p/huawei-ai-cloudmatrix-384-chinas-answer-to-nvidia-gb200-nvl72"
author:
  - "[[DYLAN PATEL]]"
  - "[[DANIEL NISHBALL]]"
  - "[[MYRON XIE]]"
published: 2026-02-05
created: 2026-07-10
description: "China Abundance of Power, 100% Optics, 0% Copper, Power Inefficiency, 2.6x lower FLOP per Watt, 14 Transceivers per Chip, Linear Pluggable Optics"
tags:
  - "clippings"
---
Huawei is making waves with its new AI accelerator and rack scale architecture. Meet China’s newest and most powerful Chinese domestic solution, the CloudMatrix 384 built using the Ascend 910C. This solution competes directly with the GB200 NVL72, and in some metrics is more advanced than Nvidia’s rack scale solution. The engineering advantage is at the system level, not just at the chip level, with innovation at the networking, optics, and software layers.

[![](https://substackcdn.com/image/fetch/$s_!5dtP!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc395d1e6-7a89-4eb5-b54d-10a13df2347e_1080x524.png)](https://substackcdn.com/image/fetch/$s_!5dtP!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc395d1e6-7a89-4eb5-b54d-10a13df2347e_1080x524.png)Source: Huawei

The Huawei Ascend chip is not new to SemiAnalysis, but in a [world where systems matter more than microarchitecture](https://semianalysis.com/2023/04/12/google-ai-infrastructure-supremacy/), Huawei is pushing the limits of AI system performance. There are trade-offs, but given export controls and lackluster domestic yields, it’s clear that there are further loopholes in the Chinese export controls.

While the Ascend chip _can be_ fabricated at SMIC, we note that this is a global chip that has [HBM from Korea](https://www.semianalysis.com/p/accelerator-model), [primary wafer production from TSMC](https://semianalysis.com/accelerator-industry-model/), and is fabricated by [10s of billions of wafer fabrication equipment from the US, Netherlands, and Japan](https://semianalysis.com/wafer-fab-model/). We do a deep dive into what is possible for domestic Chinese production what is an aggressive skirting of the export controls, and why the US government needs to focus on these key new areas to limit China’s AI capabilities.

Huawei is a generation behind in chips, but its scale-up solution is arguably a generation ahead of Nvidia and AMD’s current products on the market. So what would be the specifications for Huawei’s CloudMatrix 384 (CM384)?

The CloudMatrix 384 consists of 384 Ascend 910C chips connected through an all-to-all topology. The tradeoff is simple: having five times as many Ascends more than offsets each GPU being only one-third the performance of an Nvidia Blackwell.

[![](https://substackcdn.com/image/fetch/$s_!h7gO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec70db4a-8695-4864-a756-e740da2fece7_794x528.png)](https://substackcdn.com/image/fetch/$s_!h7gO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fec70db4a-8695-4864-a756-e740da2fece7_794x528.png)Source: SemiAnalysis, Nvidia, Huawei

A full CloudMatrix system can now deliver **300 PFLOPs of dense BF16 compute, almost double that of the GB200 NVL72**. With more than **3.6x aggregate memory capacity** and **2.1x more memory bandwidth** , Huawei and China now have AI system capabilities that can beat Nvidia’s.

What’s more, is the CM384 is uniquely suited to China’s strengths, which is domestic networking production, infrastructure software to prevent network failures, and with further yield improvements, an ability to scale up to even larger domains.

The drawback here is that it takes **4.** 1**x the power of a GB200 NVL72** , with **2.5x worse power per FLOP** , 1.9x worse power per TB/s memory bandwidth, and 1.2x worse power per TB HBM memory capacity.

**The deficiencies in power are relevant but not a limiting factor in China.**

## China has No Power Constraints, just Silicon Constraints

The common refrain in the West is that [AI is power-limited](https://www.semianalysis.com/p/datacenter-model), but in China, this is the opposite. The West has spent the last decade shifting a primarily coal-based power infrastructure to greener natural gas and renewable power generation paired with more efficient energy usage on a per capita basis. This is the opposite in China, where rising lifestyles and continued heavy investment mean massive power generation demand.

[![](https://substackcdn.com/image/fetch/$s_!eloJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b977aa8-9e8b-4996-ac88-6a67c69953c7_1855x598.png)](https://substackcdn.com/image/fetch/$s_!eloJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b977aa8-9e8b-4996-ac88-6a67c69953c7_1855x598.png)[Source: SemiAnalysis Datacenter Model](https://semianalysis.com/datacenter-industry-model/)

Most of this has been powered by coal, but China also has the largest install bases of solar, hydro, wind, and now is the leader in deploying nuclear. The United States just maintains the nuclear power deployed in the 1970s. Put simply, upgrading and adding capacity to the US energy grid is a lost muscle, meanwhile in China they have added an entire US grid of capacity since 2011, or approximately the last 10 years.

If you do not have a power constraint because of your relative power abundance, it makes sense to forgo power density and increase scale-up, including optics in the design. The CM384 design considers system-level constraints even outside of the rack, and we believe that it’s not just the relative power availability that constrains China’s AI ambitions. We think that there are multiple ways for continued scaling for Huawei’s solution.

## How Many Ascend 910C and CloudMatrix 384 Can China Make?

One common misconception is that Huawei’s 910C is made in China. It is entirely designed there, but China still relies heavily on foreign production. Whether it be HBM from Samsung, wafers from TSMC, or equipment from America, Netherlands, and Japan, there is a big reliance on foreign industry.

While SMIC, the largest foundry in China, does have 7nm, the vast majority of Ascend 910B and 910C are made with TSMC’s 7nm. In fact, the US Government, TechInsights, and others have acquired Ascend 910B and 910C and every single one used TSMC dies. Huawei was able to circumvent the sanctions on them against TSMC by purchasing ~$500 million of 7nm wafers through another company, Sophgo.

[![](https://substackcdn.com/image/fetch/$s_!YTAd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa1896a04-96ed-4eaa-a0a2-d0a8d818d5c6_927x590.png)](https://substackcdn.com/image/fetch/$s_!YTAd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa1896a04-96ed-4eaa-a0a2-d0a8d818d5c6_927x590.png)[Source: SemiAnalysis Datacenter Model](https://semianalysis.com/datacenter-industry-model/)

[TSMC is being fined $1 billion for this blatant sanctions violation](https://www.reuters.com/technology/tsmc-could-face-1-billion-or-more-fine-us-probe-sources-say-2025-04-08/), only 2x what they profited. It is rumored Huawei continues to receive wafers from TSMC via another 3rd party firm, but we cannot verify this rumor.

## Huawei’s HBM Access

Leading edge foreign reliance is part of the equation here, but China is even more reliant on HBM. China is not able to manufacture this reliably with CXMT still a year away from ramping any reasonable volume. Luckily Samsung has come to the rescue, having been the number one supplier of HBM to China through which Huawei has been able to stockpile a total of 13 million HBM stacks which can be used for 1.6 million Ascend 910C packages before any HBM bans.

Furthermore, this banned HBM is still being re-exported to China. The HBM export ban is specifically for raw HBM packages. Chips with HBM can still be shipped as long as they don’t exceed the FLOPS regulations. CoAsia Electronics is the sole distributor of HBM for Samsung in Greater China and they have been shipping HBM2E that is to ASIC design service company Faraday who gets SPIL to “package” it alongside of a cheap 16nm logic die.

Faraday then ships this system in package to China, which is technically allowed, but Chinese companies can then recover the HBM by desoldering. We think they employ techniques to make it very easy for the HBM to be extracted from the package, like using very weak low-temperature solder bumps, so when we say it is “packaged,” we mean this in the loosest way possible.

[![](https://substackcdn.com/image/fetch/$s_!36WI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F73215cc0-7d0f-4900-a0a8-69818f3b5a3e_1648x978.png)](https://substackcdn.com/image/fetch/$s_!36WI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F73215cc0-7d0f-4900-a0a8-69818f3b5a3e_1648x978.png)Source: CoAsia Electronics

It is no coincidence that CoAsia’s revenue has exploded since 2025, right after these export controls came into force.

## Chinese Domestic Foundry Can Still Ramp

Foreign production is still required, but China’s domestic semiconductor supply chain capability has rapidly improved and is still underestimated. We’ve been consistently sounding the alarm on SMIC and CXMT’s fabrication abilities. Yield and throughput are still issues but the question is what happens longer term with China’s GPU production ramp.

Both SMIC and CXMT have received [tens of billions of dollars worth of tools](https://semianalysis.com/2024/10/28/fab-whack-a-mole-chinese-companies/), and they still receive [significant volumes of sole sourced chemicals and materials](https://semianalysis.com/2024/10/28/fab-whack-a-mole-chinese-companies/) from foreign countries despite sanctions.

[![](https://substackcdn.com/image/fetch/$s_!BBsn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0abc690-f0d0-4459-8b4a-298f89941032_1294x433.png)](https://substackcdn.com/image/fetch/$s_!BBsn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd0abc690-f0d0-4459-8b4a-298f89941032_1294x433.png)Source: SemiAnalysis

SMIC is adding capacity in Shanghai, Shenzhen, and Beijing for advanced node capacity. They will have nearly 50,000 wafers per month of capacity this year, and they continue to expand due to continued access to foreign tools and the lack of effective sanctions and enforcement. If they increase their yield, they can reach serious numbers on Huawei Ascend 910C packages.

While TSMC has provided 2.9 million dies which is enough for 800 thousand Ascend 910B’s and 1.05 million Ascend 910C’s across 2024 and 2025, the SMIC production has the potential to massively grow the capacity if HBM, wafer fabrication tools, tool servicing, and chemicals such as photoresist are not effectively controlled.

## CloudMatrix 384 System Architecture

Next let’s dive into the CloudMatrix 384 architecture, scale up networking, scale-out networking, power budget, and cost.

A full CloudMatrix system is spread across 16 racks, with each of the 12 compute rack containing 32 GPUs. In the middle of these 16 racks is 4 racks of scale up switches. To bring up world size, Huawei is scaling up across multiple racks and to do that Huawei has had to use optics. Getting to 100s of GPUs in an all-to-all scale up like Huawei is not an easy feat.

[![](https://substackcdn.com/image/fetch/$s_!2-06!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F44796b8e-8a32-4b20-ae39-c4c0f50cefec_2560x884.png)](https://substackcdn.com/image/fetch/$s_!2-06!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F44796b8e-8a32-4b20-ae39-c4c0f50cefec_2560x884.png)Source: SemiAnalysis

## Similarities to DGX H100 NVL256 “Ranger”

[Back in 2022, Nvidia had announced DGX H100 NVL256 “Ranger” Platform](https://pytorchtoatoms.substack.com/p/why-dgx-h100-nvl256-never-shipped), but decided to not bring it to production due to it being prohibitively expensive, power hungry, and unreliable due to all the optical transceivers required and the two tiers of network. The CloudMatrix Pod requires an incredible 6,912 400G LPO transceivers for networking, the vast majority of which are for the scaleup network.

[![](https://substackcdn.com/image/fetch/$s_!yKSN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F803dd96a-d9ca-41d4-8de8-871ac8a3ab03_1430x804.png)](https://substackcdn.com/image/fetch/$s_!yKSN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F803dd96a-d9ca-41d4-8de8-871ac8a3ab03_1430x804.png)[Source: Nvidia HotChips](https://pytorchtoatoms.substack.com/p/why-dgx-h100-nvl256-never-shipped)

## CloudMatrix384 Scale-Up Topology Estimates

The following section will explain in depth the rack architecture of their scale up NVLink competitor between 384 chips, their scale out networking, power budget break down for the entire system and implications on the massive number of optics and lack of copper cables.

### Subscriber Content

Each Huawei Ascend 910C GPU has 2,800Gbit/s of uni-directional scale-up bandwidth. This is in the same order of magnitude as the Nvidia GB200 NVL72’s 7,200 Gb/s of scale-up bandwidth per GPU. While the NVL72’s scale-up network is carried over direct drive copper with a comparatively compact connector footprint, Huawei takes a brute force approach, simply using 7 units of 400G transceivers per GPU to provide the 2,800 Gbit/s of scale-up networking.

This solution is more expensive, consumes much more power, and raises questions regarding airflow, ease of installation and servicing, but it gets the job done.

A single-layer network is used to connect all the GPUs together in the scale-up network. Although each GPU is connected to the network with an immense amount of aggregate bandwidth. We believe that for scale up, it will connect into 4 CloudEngine 16800 modular switches in a 1-tier flat topology. Note these switches utilize line cards and fabric planes from Huawei that do cell spraying which is similar to Broadcom’s Jericho3 line cards + Ramon3 fabric cards inside of Arista modular switches.

[![](https://substackcdn.com/image/fetch/$s_!6aud!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9261dd9e-66a7-4459-9b8c-382345a2ffe0_2560x757.png)](https://substackcdn.com/image/fetch/$s_!6aud!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9261dd9e-66a7-4459-9b8c-382345a2ffe0_2560x757.png)Source: SemiAnalysis, Huawei

## Scale Up Optics and No Copper

Having 5k transceivers for scale up also raises questions around reliability, and high quality fault tolerance training software will be needed to account for this many transceivers.

Each CloudMatrix 384 pod has 6,912 400G optical modules / transceivers – 5,376 for scale-up and 1,536 scale-out.

Each pod includes 384 Ascend 910C chips, each offering 2.8 Tbps of interconnect bandwidth for scale-up communication. Therefore, each chip requires 7 transceivers at 400G, and across 384 GPUs, that’s 384 × 7 = 2,688 total transceivers. Since this is a flat 1-layer topology, the switch side matches the GPU side with another 2,688 transceivers. Altogether, the scale-up network uses 5,376 400G transceivers.

For optical transceivers, there are two potantial options: 400G SR8 multimode transceivers and 400G LPO transceivers. We expect the SR8 option to be much more likely adopted, with pricing under $100 per unit. The total cost of ownership (TCO) for scaling up a supernode network with SR8 transceivers is approximately 2.2 times that of an NVL72 rack, while its power consumption exceeds 10 times that of NVL72. However, on a per-GPU basis, the TCO is only 40% of NVL72’s, with power consumption about 1.7 times higher.

[![](https://substackcdn.com/image/fetch/$s_!mpBZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5545fd91-5a1a-41db-a9f0-f08a44416406_1030x504.png)](https://substackcdn.com/image/fetch/$s_!mpBZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5545fd91-5a1a-41db-a9f0-f08a44416406_1030x504.png)Source: SemiAnalysis

## CloudMatrix 384 Scale Out Topology Estimates

CloudMatrix 384 adopts a two-tier 8-rail optimized topology. Each scale-out CloudEngine modular switch has 768 ports at 400G, with 384 ports facing downward to connect to 384 GPUs, and 384 ports facing upward. Since there are 384 GPUs in the pod, each paired with a 400G NIC, at least 1 leaf switch is needed to accommodate them in addition to 0.5 spine switch.

[![](https://substackcdn.com/image/fetch/$s_!qRA8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F51d948ff-2f8e-4ec4-99df-f9d3e969ee25_2560x1166.png)](https://substackcdn.com/image/fetch/$s_!qRA8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F51d948ff-2f8e-4ec4-99df-f9d3e969ee25_2560x1166.png)Source: SemiAnalysis

Calculating the number of transceivers needed is simpler. On the GPU side, we need 384 400G transceivers – one per GPU. On the leaf layer, we need double the number of transceivers because we allocate half the ports downward to connect to GPUs and half upwards to connect to spine switches. Finally, we need another 384 400G switches on the spine layer to match the aggregate upward bandwidth from the leaf layer. Altogether, this results in 384 × 4 = 1,536 transceivers at 400G for the scale-out.

## Chip Level

Huawei’s Ascend 910B and 910C accelerators are the best of China’s domestic GPU efforts. Considering the constraints they have faced they deliver excellent performance. On a chip basis, they are still not as good as Nvidia’s.

[![](https://substackcdn.com/image/fetch/$s_!_zS6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffdbb0cfc-c363-472a-bcfe-bed0504c9fd3_972x862.png)](https://substackcdn.com/image/fetch/$s_!_zS6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ffdbb0cfc-c363-472a-bcfe-bed0504c9fd3_972x862.png)Source: SemiAnalysis

The Huawei Ascend 910C is the follow on to the 910B and is effectively 2x 910B interposers placed on a single substrate: doubling compute and memory performance per chip.

[![](https://substackcdn.com/image/fetch/$s_!OyVb!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc47e3bcf-7936-4cb4-83cd-5cada0bca770_1784x1552.png)](https://substackcdn.com/image/fetch/$s_!OyVb!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc47e3bcf-7936-4cb4-83cd-5cada0bca770_1784x1552.png)Source: SemiAnalysis

## System-level Power Budget

Due to the extensive use of optical transceivers in both scale-up and scale-out network, this 384-GPU cluster is very power hungry. We estimate that one CM384 supernode draws close to 600kW of power – more than 4 times that of Nvidia’s GB200 NVL72 rack, which consumes about 145kW.

[![](https://substackcdn.com/image/fetch/$s_!3Isd!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d5c7557-19bc-4dcc-a180-21e73d394910_710x816.png)](https://substackcdn.com/image/fetch/$s_!3Isd!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d5c7557-19bc-4dcc-a180-21e73d394910_710x816.png)Source: SemiAnalysis

On a per-GPU basis, however, each Huawei GPU uses about 75-80% the all-in power of a B200 GPU within NVL72. Overall, the Huawei supernode delivers 70% more FLOPS than the NVL72, but its architecture design ultimately leads to 2.5x worse power per FLOP, 1.9x worse power per TB/s memory bandwidth, and 1.2x worse power per TB HBM memory capacity.

[![](https://substackcdn.com/image/fetch/$s_!jW36!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd99d9a03-0e2c-4c54-9e87-dba0a9040846_802x530.png)](https://substackcdn.com/image/fetch/$s_!jW36!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd99d9a03-0e2c-4c54-9e87-dba0a9040846_802x530.png)Source: SemiAnalysis, Nvidia, Huawei

However, the additional expense and power are just a necessary cost which China can swallow to match the compute capabilities of the West. As mentioned, with energy being as abundant as it is in China, the cost is relatively low giv­en the national security importance. China’s energy advantage will be a key asset in enabling the scaling up of its data centers in terms of scale and speed.
