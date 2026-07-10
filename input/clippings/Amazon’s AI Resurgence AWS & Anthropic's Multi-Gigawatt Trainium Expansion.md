---
title: "Amazon’s AI Resurgence: AWS & Anthropic's Multi-Gigawatt Trainium Expansion"
source: "https://newsletter.semianalysis.com/p/amazons-ai-resurgence-aws-anthropics-multi-gigawatt-trainium-expansion"
author:
  - "[[JEREMIE ELIAHOU ONTIVEROS]]"
  - "[[DYLAN PATEL]]"
  - "[[AJ]]"
  - "[[MYRON XIE]]"
published: 2026-02-05
created: 2026-07-10
description: "Anthropic multi-gigawatt clusters, Trainium ramp, best TCO per memory bandwidth, system-level roadmap, Bedrock and internal models"
tags:
  - "clippings"
---
[Two-and-a-half years ago, we flagged a looming “cloud crisis” at AWS](https://semianalysis.com/2023/03/20/amazons-cloud-crisis-how-aws-will/). Today, the evidence has mounted. AWS is the crown jewel of the Amazon empire, generating ~60% of group profits, and dominating the lucrative Cloud Computing market. But it struggles to translate this strength into the new GPU/XPU Cloud era.

Microsoft Azure now leads the market on quarterly new cloud revenue, and the gap between Google Cloud and AWS has materially narrowed especially with [Google's big moves on the TPU that we've been posting about for over a month](https://semianalysis.com/accelerator-model/). Markets have noticed. Year-to-date, Amazon is the clear laggard among the four tech-and-AI titans as investors mark down the company most for losing momentum in AI.

[![](https://substackcdn.com/image/fetch/$s_!AEa_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6227dc41-f0ed-4125-87c2-b52961d1b42c_1024x606.png)](https://substackcdn.com/image/fetch/$s_!AEa_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6227dc41-f0ed-4125-87c2-b52961d1b42c_1024x606.png)Source: [SemiAnalysis Core Research](https://semianalysis.com/core-research/), company filings

Today, SemiAnalysis is back with another out-of-consensus call. While the market overplays the Cloud Crisis theme, we call for an AWS AI Resurgence. We laid out our thesis a month ago to our [Core Research subscribers](https://semianalysis.com/core-research/), forecasting an upcoming acceleration beyond 20% year-over-year growth by the end of 2025.

[![](https://substackcdn.com/image/fetch/$s_!HfDU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F414c071a-3f68-4268-8f7c-94ba79182635_1024x509.png)](https://substackcdn.com/image/fetch/$s_!HfDU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F414c071a-3f68-4268-8f7c-94ba79182635_1024x509.png)Source: [SemiAnalysis Core Research](https://semianalysis.com/core-research/)

Amazon’s savior has a name: Anthropic. The startup has been the clear outperformer in the GenAI market in 2025, multiplying revenue fivefold year-to-date to reach $5B annualized.

[![](https://substackcdn.com/image/fetch/$s_!lqu2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F01c05a64-a990-4506-9f1d-d0690410b13a_1024x547.png)](https://substackcdn.com/image/fetch/$s_!lqu2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F01c05a64-a990-4506-9f1d-d0690410b13a_1024x547.png)Source: The Information, Reuters, Bloomberg, [SemiAnalysis Core Research](https://semianalysis.com/core-research/)

To keep that trajectory, Anthropic is betting hard on [Scaling Laws](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/). While Dario’s startup draws fewer headlines than OpenAI, xAI and [Meta Superintelligence](https://semianalysis.com/2025/07/11/meta-superintelligence-leadership-compute-talent-and-data/), it isn’t shy about investment. AWS has **well over a gigawatt of datacenter capacity in final stages of construction** for its anchor customer. AWS is building datacenters faster than it ever has in its entire history. And there’s **much more on the horizon**.

[![](https://substackcdn.com/image/fetch/$s_!ZPks!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F348cc316-30b7-41e3-a083-911df1ae1a33_1024x576.png)](https://substackcdn.com/image/fetch/$s_!ZPks!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F348cc316-30b7-41e3-a083-911df1ae1a33_1024x576.png)Source[: SemiAnalysis Datacenter Industry Model](https://www.semianalysis.com/p/datacenter-model)

To understand and forecast GPU/XPU power capacity by AI Lab broken down by Cloud Provider, we rely on our proprietary [Datacenter Industry Model](https://www.semianalysis.com/p/datacenter-model) powered by real-time satellite imagery. Trusted by all hyperscalers, AI labs, and the world’s largest investors, it _provides a**quarterly building-by-building datacenter forecast** for OpenAI, Anthropic, xAI, Meta Superintelligence, Google DeepMind, and more. [Contact us for more information](Sales@SemiAnalysis.com)._

## Trainium vs GPUs

While Amazon’s AI Datacenters are impressive in scale and speed, the design of individual building is unremarkable. [Hyper-optimized for air-cooling](https://semianalysis.com/2025/02/13/datacenter-anatomy-part-2-cooling-systems/#google-datacenters-%e2%80%93-energy-for-water-tradeoff), this blueprint is identical to 5-year-old traditional AWS Cloud datacenters.

What makes these facilities unique is their inside: they’ll host the **world’s largest cluster of non-Nvidia AI chips, with just under a million Trainium2 in the largest campus**. To understand everything about the Trainium2 system, read [our December 2024 technical deep dive](https://semianalysis.com/2024/12/03/amazons-ai-self-sufficiency-trainium2-architecture-networking/).

Trainium2 lags Nvidia’s systems in many ways, but it was pivotal to the [multi-gigawatt AWS/Anthropic deal](https://www.semianalysis.com/p/datacenter-model). Its memory bandwidth per TCO advantage perfectly fits into Anthropic’s [aggressive Reinforcement Learning roadmap](https://semianalysis.com/2025/06/08/scaling-reinforcement-learning-environments-reward-hacking-agents-scaling-data/). Dario Amodei’s startup was heavily involved in the design process, and its influence on the Trainium roadmap only grows from here.

Put plainly: Trainium2 is converging toward an **Anthropic custom-silicon program**. This will enable Anthropic to be, alongside Google DeepMind, the only AI labs benefiting from **tight hardware–software co-design** in the near horizon.

[![](https://substackcdn.com/image/fetch/$s_!Euws!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F377f07d4-2e4e-4833-afc7-dd75f876c777_1024x357.png)](https://substackcdn.com/image/fetch/$s_!Euws!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F377f07d4-2e4e-4833-afc7-dd75f876c777_1024x357.png)Source: [AI Cloud TCO Model](https://semianalysis.com/ai-cloud-tco-model/)

This report will dig into all aspects of Amazon’s AI resurgence: the Anthropic partnership, datacenters, and Trainium. At the end of the report, we provide a longer-term outlook on Anthropic, AWS Bedrock and internal models, and explain why everything isn’t rosy.

First, a step back on why AWS has underperformed rival AI Clouds to date.

## AWS GenAI underperformance

To understand the causes of Amazon’s underperformance in the GenAI era, we can analyze drivers of success in the GPU/XPU cloud market. In the most simplistic way, we see two primary customer groups for GPU/XPU capacity:

  * Wholesale bare metal users: large-scale customers like OpenAI, Anthropic, ByteDance, and other hyperscalers.

  * Managed SLURM/Kubernetes: Smaller customers such as startups, research institutes, and enterprise pilot projects.




### Cloud Crisis and ClusterMAX underperformance

In the second category, our [ClusterMax AI cloud rating](https://semianalysis.com/2025/03/26/the-gpu-cloud-clustermax-rating-system-how-to-rent-gpus/) is the best way to compare relative strengths and weaknesses. Platinum and gold-rated AI Clouds have seen more traction than others and boast higher-than-average pricing power. As such, the likes of CoreWeave, Oracle, Nebius, Crusoe and Azure have outperformed the market for multitenant GPU clusters – which require high performance and advanced software layers.

[![](https://substackcdn.com/image/fetch/$s_!yi5j!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdbf0fa08-c2d5-42ef-a937-665ed42e6ce3_1024x615.png)](https://substackcdn.com/image/fetch/$s_!yi5j!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdbf0fa08-c2d5-42ef-a937-665ed42e6ce3_1024x615.png)Source: [SemiAnalysis ClusterMAX GPU Cloud Rating](https://semianalysis.com/2025/03/26/the-gpu-cloud-clustermax-rating-system-how-to-rent-gpus/)

[As predicted two years ago](https://semianalysis.com/2023/03/20/amazons-cloud-crisis-how-aws-will/), key to Amazon’s underperformance is the use of custom networking fabric EFA. AWS's success with ENA on the frontend network has not yet translated to EFA on the backend. EFA still lags behind other networking options on performance: NVIDIA's InfiniBand and Spectrum-X, as well as RoCEv2 options from Cisco, Arista, and Juniper. Raw performance isnt the only metric, the user experience of EFA isn't as good as InfiniBand & RoCEv2 either. That being said, with Amazon's newest EFAv4 performance at real world msg sizes is improving, albeit still behind the competiton.

Amazon's custom networking also [reduces their time-to-market due to customization requirements of Nvidia systems](https://x.com/SemiAnalysis_/status/1959758467402784855). Other items like advanced passive and active automated weekly scheduled health check strategies aren’t as solid as gold & platinum-rated clouds.

Our upcoming ClusterMAXv2 rating will provide an update on all major cloud providers based on our proprietary testing. Stay tuned!

### Searching for an anchor customer

More important to AWS’ XPU business growth is the ability to **secure anchor customers – the market-makers in this first wave of GenAI demand**. Scale, time-to-market, deep partnerships, and pricing are key to winning these accounts, more so than advanced software layers.

No firm better illustrates this than Microsoft. Azure’s AI outperformance over peers is entirely driven by its OpenAI partnership. As of Q2 2025 (June 2025), all of OpenAI’s >$10B cloud spending is booked by Azure.

[![](https://substackcdn.com/image/fetch/$s_!Zcru!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7cf42542-67fc-456a-bc11-41ca08f65139_1024x508.png)](https://substackcdn.com/image/fetch/$s_!Zcru!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7cf42542-67fc-456a-bc11-41ca08f65139_1024x508.png)Source: [SemiAnalysis Datacenter Industry Model](https://semianalysis.com/datacenter-industry-model/)

Amazon understood early on the need for an anchor customer and [invested $1.25B, expandable to $4B in Anthropic in September 2023](https://semianalysis.com/2023/10/02/amazon-anthropic-poison-pill-or-empire/). The partnership expanded in March 2024 [with Anthropic committing to use Tranium and Inferentia chips](https://www.aboutamazon.com/news/company-news/amazon-anthropic-ai-investment). In November 2024[, Amazon invested an additional $4B into Anthropic,](https://www.aboutamazon.com/news/aws/amazon-invests-additional-4-billion-anthropic-ai) [with the latter naming AWS as its primary LLM training partner](https://www.aboutamazon.com/news/aws/amazon-invests-additional-4-billion-anthropic-ai).

### Anthropic’s outperformance, AWS underperformance?

Amazon’s bet has been the right one. Anthropic is the clear outperformer in 2025 in the GenAI market, with revenue surging from $1B to $5B annualized. In this context, AWS’ underperformance understandably frustrates investors, but they’re misunderstanding the composition of Anthropic’s spending on training and inference.

[![](https://substackcdn.com/image/fetch/$s_!Pi7B!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb77d4f69-7460-45f7-9709-b281de0a926c_1024x547.png)](https://substackcdn.com/image/fetch/$s_!Pi7B!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb77d4f69-7460-45f7-9709-b281de0a926c_1024x547.png)Source: [SemiAnalysis Tokenomics](https://semianalysis.com/tokenomics-model/)

There **are two clear reasons explaining why Amazon isn’t yet truly benefiting** from its relationship with Anthropic:

  1. As of Q2 2025, Anthropic’s cloud spending is over 2x smaller than that of OpenAI.

  2. A large share of Anthropic’s spending is going to Google Cloud – one of Anthropic’s first major investors ($300M round late-2022) and preferred cloud partner in 2023 and 2024, before the expanded AWS deal.




[![](https://substackcdn.com/image/fetch/$s_!HERL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F315d7305-7da2-407b-a362-97b5a08962d3_1024x507.png)](https://substackcdn.com/image/fetch/$s_!HERL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F315d7305-7da2-407b-a362-97b5a08962d3_1024x507.png)Source: [SemiAnalysis Datacenter Industry Model](https://semianalysis.com/datacenter-industry-model/)

## Anthropic & AWS multi-gigawatt AI Training infrastructure

In particular, we believe that most of Anthropic’s skyrocketing inference needs are served by Google Cloud. Having the world’s best inference system (TPU) is a key competitive advantage.

The AWS infrastructure buildout is aimed at taking a chunk of this for its key customer will also focusing on **training**. While Anthropic makes less headlines than peers like OpenAI, xAI and Meta, is it all-in on the AGI race and isn’t planning to be shy on training spending. Anthropic leadership truly believes in [Scaling for RL](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/).

Their belief will materialize as early as this year. We show below three AWS campuses in final stages of construction, boasting over 1.3GW of IT capacity for the **sole purpose of serving Anthropic’s training needs**. The speed of construction is remarkable.

[![](https://substackcdn.com/image/fetch/$s_!J-9v!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feed0550a-e73f-4693-991e-fc95b5f6fc7a_1024x576.png)](https://substackcdn.com/image/fetch/$s_!J-9v!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feed0550a-e73f-4693-991e-fc95b5f6fc7a_1024x576.png)Source[: SemiAnalysis Datacenter Industry Model](https://www.semianalysis.com/p/datacenter-model)

While these datacenters look built from the skies, we don’t think they are generating any meaningful revenue yet. Trainium has faced some yield issues on the assembly phase – fairly standard for a new system. We think the three large AWS campuses will meaningfully contribute to AWS’ top line by the end of 2025 and jack up growth above the 20% YoY threshold.

[![](https://substackcdn.com/image/fetch/$s_!0ahn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2757411e-3e3d-465b-aa82-b637633ee401_1024x509.png)](https://substackcdn.com/image/fetch/$s_!0ahn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2757411e-3e3d-465b-aa82-b637633ee401_1024x509.png)Source: [SemiAnalysis Core Research](https://semianalysis.com/core-research/) \- _[Core Research](https://semianalysis.com/core-research/) is our institutional research service trusted by most of the world’s largest hedge funds and investors. [Contact us](Sales@SemiAnalysis.com) to get the industry’s most granular insights on AI hardware, software and infrastructure._

Anthropic isn’t stopping there. Its ~$13B funding round at a $183B valuation will provide capital to sign additional deals with AWS, Google, and others. AWS isn’t waiting standing still – they're already breaking ground on upcoming GW-scale datacenters to capture this growth.

[![](https://substackcdn.com/image/fetch/$s_!BRbQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F58e99612-92fc-46a8-a6c1-1b97237f9b05_1024x553.png)](https://substackcdn.com/image/fetch/$s_!BRbQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F58e99612-92fc-46a8-a6c1-1b97237f9b05_1024x553.png)Source: [SemiAnalysis Datacenter Industry Model](https://www.semianalysis.com/p/datacenter-model)

As explained earlier, these datacenters will primarily be filled with AWS’ custom chip [Trainium](https://semianalysis.com/2024/12/03/amazons-ai-self-sufficiency-trainium2-architecture-networking/). Given the sheer scale, we **can’t understate how bold Anthropic’s bet is**. Not only are they committing to spending tens of billions of dollars, they're doing it on a largely unproven chip!

Let’s try to make some sense of their bet by digging into Trainium’s TCO and roadmap.

## Trainium2 TCO analysis – how Anthropic’s big bet could pay off

Trainium2 supply chain signals are currently extremely strong. Our industry-leading [AI Accelerator Model](https://semianalysis.com/accelerator-industry-model/) track both the package shipments and the system/rack shipments and they’ve surged since the beginning of the year. It _provides quarterly volume forecasts for the 10+ SKUs comprising the Trainium2 and Trainium3 product family and calls out suppliers set to disproportionately benefit from specific SKUs.[Contact us for more information](Sales@SemiAnalysis.com)._

[![](https://substackcdn.com/image/fetch/$s_!iQ0J!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd5e4a6cb-ee16-49ea-ad64-5288333af03c_1024x552.png)](https://substackcdn.com/image/fetch/$s_!iQ0J!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd5e4a6cb-ee16-49ea-ad64-5288333af03c_1024x552.png)Source: [SemiAnalysis Accelerator and HBM Model](https://semianalysis.com/accelerator-hbm-model/)

Note this is chip production, rack production is lagged, but we also track it.

Competing with Nvidia and Google’s TPU is, of course, no small feat. While Google is rolling out its seventh generation TPU, Ironwood, Trainim2 is only Amazon’s third-generation AI Accelerator.

### Chip specifications: Trainium2 inferior on all fronts, but…

A simple look at chip specifications shows Trainium as a clear laggard relative to Nvidia:

  * Nvidia’s GB200 has a **3.85x FP16 FLOPs advantage** , at 2500 TFLOP/s/chip vs Trainium2’s 667 TFLOP/s/chip. Note that spec sheet numbers are inflated compared to actual achievable FLOPs.

  * In terms of **Memory bandwidth, the gap narrows to 2.75x** , at 8000GB/s/GPU vs 2900GB/s/Trn2




[![](https://substackcdn.com/image/fetch/$s_!_gU7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Febe72b52-b6a4-4b23-8c3b-a85a6399d12d_1024x553.png)](https://substackcdn.com/image/fetch/$s_!_gU7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Febe72b52-b6a4-4b23-8c3b-a85a6399d12d_1024x553.png)Source: Amazon, [SemiAnalysis](https://semianalysis.com/2024/12/03/amazons-ai-self-sufficiency-trainium2-architecture-networking/#aws-trainium2-specifications-overview)

Evaluating scale-up network bandwidth is another key item. We’ve explained several times the [importance of scale-up networks for reasoning model inference](https://semianalysis.com/2024/12/25/nvidias-christmas-present-gb300-b300-reasoning-inference-amazon-memory-supply-chain/#built-for-reasoning-model-inference). Our [deep-dive on Reinforcement Learning](https://semianalysis.com/2025/06/08/scaling-reinforcement-learning-environments-reward-hacking-agents-scaling-data/) highlighted the similarities of RL with inference workloads, making memory bandwidth a crucial item to scale post-training.

  * Nvidia’s GB200 NVL72 boasts an aggregate 576TB/s memory bandwidth across World Size.

  * This is a **3.1x advantage relative to Trainium2’s** (Teton2-PD-Ultra-3L SKU) 186 TB/s – with the caveat that it varies across SKUs.




While Trainium appears materially behind, the picture changes once we factor-in Total Cost of Ownership.

### Trainium’s memory bandwidth per TCO advantage

In the table below, we incorporate TCO into our comparison. While Nvidia has a material head on a TCO per effective training PFLOP, Trainium2 is highly competitive on a TCO per million Tokens and TCO per TB/s of memory bandwidth.

[![](https://substackcdn.com/image/fetch/$s_!9MQi!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3fa83400-60da-4742-8b8b-131e439ac2b7_1024x357.png)](https://substackcdn.com/image/fetch/$s_!9MQi!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3fa83400-60da-4742-8b8b-131e439ac2b7_1024x357.png)Source: [AI Cloud TCO Model](https://semianalysis.com/ai-cloud-tco-model/)

And we don’t see Nvidia’s upcoming VR200 NVL144 change the picture relative to AWS’ Trainium3. To be clear, TCO has many other moving parts. AWS has other system-level architecture deployments that better fit some use cases. Later down the road, [Nvidia’s Kyber rack will boast the world’s most advanced scale-up network architecture](https://semianalysis.com/2025/03/19/nvidia-gtc-2025-built-for-reasoning-vera-rubin-kyber-cpo-dynamo-inference-jensen-math-feynman/#kyber-rack-architecture).

For a full understanding of the TCO of 50+ Nvidia SKU and a detailed TCO comparison with all AMD, Trainium and TPU SKUs, [check out our AI Cloud TCO Model](https://semianalysis.com/ai-cloud-tco-model/). The largest hyperscalers, Neoclouds and their financial sponsors rely on our model to time their investment decisions.

### Anthropic is betting on hardware-software codesign

Trainium2’s memory bandwidth per TCO advantage is key to understanding Anthropic’s choice. While Nvidia’s chips and systems are better on most fronts, Trainium2 fits perfectly into Anthropic’s roadmap. They’re the most aggressive AI Lab on [scaling post-training techniques like Reinforcement Learning](https://semianalysis.com/2025/06/08/scaling-reinforcement-learning-environments-reward-hacking-agents-scaling-data/). Their roadmap is more memory-bandwidth-bound than FLOPs bound. Our recent HBM report explains in-depth which AI workloads tend to be memory-bound.

Anthropic’s ramp will make it not only the only large external end-user of Trainium2, it’ll also be materially larger than Amazon’s internal needs (e.g. Bedrock, Alexa, etc). They’re now heavily involved in all Trainium design decisions and, essentially, use Amazon’s Annapurna Labs as a custom silicon partner! **This makes Anthropic the only AI lab, alongside Google DeepMind, benefiting from tight hardware-software codesign**.

### Trainium’s roadmap: doubling down on systems

Amazon is rolling out a new system-level architecture for its anchor customer. Currently, the two systems deployed by AWS are Teton PD and Teton PD Ultra. Next year, the new Teton PDS and Teton Max are set to ship in large volumes. [Our AI Accelerator Model provides the exact volumes and SKU-by-SKU breakdown on a quarterly basis](https://semianalysis.com/accelerator-industry-model/).

[![](https://substackcdn.com/image/fetch/$s_!mPc4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4bfcf56c-0eb5-4cdc-9c3c-593978efdf66_1024x517.png)](https://substackcdn.com/image/fetch/$s_!mPc4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4bfcf56c-0eb5-4cdc-9c3c-593978efdf66_1024x517.png)Source: [SemiAnalysis Accelerator Industry Model](https://semianalysis.com/accelerator-hbm-model/), AWS

The key difference **is the introduction of an all-to-all scale-up network dubbed NeuronLinkv3.** Trainium’s architecture is thus converging towards Nvidia’s NVL72 NVLink.

**Four NeuronLinkv3 switch trays** will be placed in the middle of the rack with 16 compute trays above and below split evenly. [Certain supply chain vendors are set to benefit disproportionately, as highlighted two months ago on Core Research](https://semianalysis.com/core-research/) – our institutional research service trusted by the world’s largest hedge funds. That vendor is up 73% since our post. We see the introduction of PDS as an intermediate step in Trainium’s path to catch up with Nvidia. We also believe that Anthropic was heavily involved in the launch of this new system-level architecture.

[![](https://substackcdn.com/image/fetch/$s_!vYuT!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf62f51b-0cdc-4e58-80e0-ea8828c9d9ba_1024x292.png)](https://substackcdn.com/image/fetch/$s_!vYuT!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faf62f51b-0cdc-4e58-80e0-ea8828c9d9ba_1024x292.png)Source: [SemiAnalysis Accelerator Industry Model](https://semianalysis.com/accelerator-hbm-model/), AWS

Anthropic’s increased involvement in design decisions bodes well for future volumes. But they’re not giving up on TPUs and Nvidia GPUs either. Our [Accelerator Model ](https://semianalysis.com/accelerator-industry-model/)forecasts Amazon and Google Cloud’s chip purchases broken down by precise SKU, and our [Datacenter model](https://www.semianalysis.com/p/datacenter-model) to understand which datacenter and cloud partners support Anthropic’s ramp. The [TPU ramp for Anthropic in 2026 is huge, and their are unique aspects to their deal as we have been posting about for over a month.](https://semianalysis.com/core-research/google-selling-tpu-systems-externally-further-tpu-revisions/)

Let’s now take a longer-term view and evaluate what the future of AWS might look like. Behind paywall, we discuss the following items:

  * The outlook for Amazon’s key customer: Anthropic.

  * Amazon’s GenAI business beyond Anthropic: Bedrock and internal LLM efforts.

  * The Trainium ramp in 2026 & 2027, potential new external customers, and how it might impact Amazon’s financial profile in future years.




## Subscriber Content

## Anthropic outlook: full steam ahead

Our positive stance on AWS not only stands from their 2025 and early 2026 datacenter ramp. We think scoring Anthropic as a key customer will result in a highly lucrative long-term partnership. We show below our Anthropic revenue forecast, based on the [SemiAnalysis Tokenomics](https://semianalysis.com/tokenomics-model/) model.

[![](https://substackcdn.com/image/fetch/$s_!061i!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F22a04000-f387-4e32-8305-075af6f0f3a2_1024x511.png)](https://substackcdn.com/image/fetch/$s_!061i!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F22a04000-f387-4e32-8305-075af6f0f3a2_1024x511.png)Source: [SemiAnalysis Tokenomics](https://semianalysis.com/tokenomics-model/)

While OpenAI dominates the consumer market with ChatGPT, Anthropic is the API market king.

[![](https://substackcdn.com/image/fetch/$s_!Z9F_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c0b0f93-0241-4fad-932c-6bd001a3a403_1024x543.png)](https://substackcdn.com/image/fetch/$s_!Z9F_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0c0b0f93-0241-4fad-932c-6bd001a3a403_1024x543.png)Source: Menlo Ventures

Coding is their crown jewel, and the end market is surging. The speed at which Cursor (and similar coding solutions like Claude Code) is being adopted and crossing ARR milestones is astonishing. While getting to $100M ARR took Cursor 750 days, it broke the $250M mark in barely 45 days and $500M in 15 days.

[![](https://substackcdn.com/image/fetch/$s_!tptU!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F70e1a5e3-eaef-483a-8b15-062203fc9de6_1024x623.png)](https://substackcdn.com/image/fetch/$s_!tptU!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F70e1a5e3-eaef-483a-8b15-062203fc9de6_1024x623.png)Source: [SemiAnalysis Tokenomics](https://semianalysis.com/tokenomics-model/)

### State-of-the-art over GPT-5

We think the outlook is bright for Anthropic. Their models are state of the art. Claude Opus 4.1 leads on coding-related benchmarks like SWE-Bench, and we expect more updates before the end of 2025 to further improve the model through RL. The launch of Amazon’s large-scale training clusters towards the end of 2025 bodes well for Anthropic’s progress in 2026.

OpenAI has tried hard to unseat Anthropic from being the best coding model through GPT-5, but we understand Anthropic remains the top model in Cursor and isn’t losing traction. We see Cursor as the ultimate indicator of which model nails the balance between capability and usability, and it remains to be Claude 4 Sonnet.

Anthropic has long had a singular focus on developer coding capabilities and a deep understanding of their userbase. As an example, when Anthropic introduced reasoning, it was through a hybrid model in Claude 3.7. This suited developer workloads better than o3, which was in some cases a more capable model on cursor but was a pure reasoner and often took too long to reply.

[![](https://substackcdn.com/image/fetch/$s_!_c0D!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a371247-3789-43ec-9b23-8b946c4af083_1024x497.jpeg)](https://substackcdn.com/image/fetch/$s_!_c0D!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4a371247-3789-43ec-9b23-8b946c4af083_1024x497.jpeg)Source: [SemiAnalysis Tokenomics](https://semianalysis.com/tokenomics-model/)

[GPT-5 tried to change this by switching to a “hybrid reasoning” system](https://semianalysis.com/2025/08/13/gpt-5-ad-monetization-and-the-superapp/), but they are playing catch up. In addition, Anthropic’s top position in coding through Cursor and Claude Code is creating a data moat and a flywheel effect. On the other hand, OpenAI has historically placed a deeper focus on **competitive coding** capabilities and somewhat overlooked developer experiences. While they dominate GitHub Copilot, they don’t benefit from the same data/experience moat given tighter privacy policies.

And Anthropic’s models aren’t just good at coding, they’re leading on many other domains. There is also mounting evidence that strong coding abilities yields benefits to other seemingly unrelated use cases, such as Agentic tasks. As such, we’re optimistic on Anthropic’s future. The main risk comes from lower network effects and entry barriers compared to ChatGPT’s consumer moat.

If anything, that likely makes Anthropic more paranoid than any other lab. Developing state-of-the-art models is existential to the company’s existence. That bodes well for AWS, given an overexposure to Anthropic training.

## Trainium ramps and for the future of AWS

This makes us optimistic about the future of AWS’ Trainium program volume-wise. However, while Trainium shipments closely match our forecast Anthropic IT Capacity (excl. TPU & Nvidia) in 2025 and 2026, we see a gap in 2027.

Said differently, Anthropic will be essentially the sole customer for Trainium2+ in 2025 and 2026 but isn’t large enough to absorb the volumes AWS currently aims to produce in 2027.

The risk for Amazon is a repeat of the Trainium1 and Inferentia2 situation. We believe they haven’t found any sizeable external customers. While they are used in some internal use-cases, the return on invested capital likely isn’t up to AWS’ standards. Given the sheer size of our 2027 forecasted spending, the risk is a more visible degradation of AWS’ ROIC profile.

[![](https://substackcdn.com/image/fetch/$s_!BURS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5347e70e-8ea0-456f-9749-35efc062e64b_1024x587.png)](https://substackcdn.com/image/fetch/$s_!BURS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5347e70e-8ea0-456f-9749-35efc062e64b_1024x587.png)Source: [SemiAnalysis Datacenter Industry Model](https://semianalysis.com/datacenter-industry-model/)

AWS likely wants to apply the AWS Cloud playbook into the AI era: differentiate on cost. We’ve witnessed this already with the Trainium/Annapurna/Alchip/Marvell drama saga:

  * To build Trainium, AWS didn’t opt for the world’s best custom silicon partner – Broadcom who has mopped up almost all of the major AI ASIC sockets. It has chosen Marvell and Alchip as design partners who are somewhat weaker technology partners but offer much more attractive pricing than Broadcom. Amazon also derives significant savings by directly procuring their HBM needs, instead of having it run through their design partners’ balance sheet who then stack additional margin on HBM, which is the case for Google going through Broadcom.

  * After running a competitive bake off between Alchip and Marvell for who wins this multi-billion dollar socket, Annapurna is taking it further by focusing more on Alchip for future generations. Alchip offers little in the way of silicon IP but on the other hand is significantly cheaper than Marvell. This will help AWS system cost come closer to actual BOM cost by reducing margin for the design middleman.




The next phase of Amazon’s GenAI cost-optimization playbook is Bedrock + Trainium.

## Beyond Anthropic – Bedrock, internal models

Bedrock is Amazon’s inference-as-a-service platform. It provides a fully managed unified API to call a wide range of models and offers additional security and compliance layers to make integration seamless for enterprises. [The market is highly competitive](https://semianalysis.com/2023/12/18/inference-race-to-the-bottom-make/), but AWS boasts the advantage of a unique full Claude integration – similar to Microsoft’s integration of OpenAI’s closed source models.

Given Bedrock abstracts the hardware from the customer, AWS’ plan is to differentiate on cost (relative to Nvidia-dependent Neoclouds & hyperscalers) via custom silicon. All ASIC programs have the goal of beating Nvidia GPUs on performance relative to TCO, and the focus for AWS is to reduce the TCO part.

However, current signals point to Bedrock facing several issues. Given strong competition and how fast-moving the industry is, this suggests the AWS AI Cloud Crisis isn’t over.

### Rate limits

Bedrock’s rate limits are a huge blocker for production deployments. Many developers have avoided using Bedrock for their API, even though it served Claude 4 Sonnet, due to overly tight rate limits. New accounts automatically get 2 requests per minute (RPM) for Claude Opus, for example, while the advertised amount is 50. While accounts can request a rate limit raise, this process is generally laborious and not guaranteed.

Anthropic, on the other hand, automatically assigns rate limits of 50 RPM and 4,000 RPM for Tier 4 customers. Enterprise customers can get access to even higher rates.

This constraint is so limiting that deploying Claude Code using the Bedrock API can cause Claude Code to crash and operate unexpectedly.

[![](https://substackcdn.com/image/fetch/$s_!WYr5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F949bc1f6-1339-4fba-a382-3a6f07616ed3_1024x670.jpeg)](https://substackcdn.com/image/fetch/$s_!WYr5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F949bc1f6-1339-4fba-a382-3a6f07616ed3_1024x670.jpeg)Source: Anthropic

### Bedrock and open models

Bedrock doesn’t just offer Claude; their range of models is quite large. Like other inference end points, Bedrock readily implemented GPT-OSS. However, upon closer inspection, it seems that the implementation is botched. Some users reported that the system prompt the model sees while deployed was changed in random and incoherent ways. This leads the model performance to be rather dysfunctional in a chat capacity.

[![](https://substackcdn.com/image/fetch/$s_!2bO3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e2b538d-706c-4864-8030-6973b7fa1aad_975x292.png)](https://substackcdn.com/image/fetch/$s_!2bO3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6e2b538d-706c-4864-8030-6973b7fa1aad_975x292.png)Source: [Benjamin Anderson](https://benanderson.work/blog/bedrock-gpt-oss/)

Independent testing conducted by Artificial Analysis also revealed that the deployment of GPT-OSS on Amazon Bedrock also resulted in considerably worse performance relative to the average across different end points. GPT-OSS deployed on Bedrock **scored 13% lower** than most of the other inference endpoints like Fireworks and even Azure. The Bedrock team is still struggling to independently deploying a model at full capability, despite their experience.

[![](https://substackcdn.com/image/fetch/$s_!dbJ7!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F115e5093-ea9f-462e-adaf-cd4cb7026d41_1024x503.jpeg)](https://substackcdn.com/image/fetch/$s_!dbJ7!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F115e5093-ea9f-462e-adaf-cd4cb7026d41_1024x503.jpeg)Source: Artificial Analysis

### Amazon’s Titan and Nova internal models

The last major piece of Amazon’s GenAI strategy is their internal models. Amazon Nova is a series of models by Amazon which showcases multimodal capabilities. However, the models, across the board, perform poorly. Released in December of ’24, the models were lagging behind even at that time. As an example, Nova Pro was released 8 months after GPT-4o yet still showcased worse performance.

The more interesting part is that there have been little to no updates to the model since release. In general, Amazon is not dedicating a huge amount of effort to their internal models. It opts for Claude’s technology instead. For example, shortly after the release of Nova, [Claude was integrated into Alexa](https://www.anthropic.com/news/claude-and-alexa-plus). We expect that Amazon will continue to integrate Claude, not Nova, into their products.

Amazon does not possess the required talent to produce a strong model. And with the tight partnership with Anthropic, they do not really need to, at least when it comes to text and multimodal capabilities.

When it comes to image generation, though, we do not expect Anthropic to bail Amazon out. Anthropic has no plans to release an image generation model and Amazon’s model in this domain, Titan, is also lacking in performance.

Titan, which saw its latest version put out last year, is still served on Bedrock. However, due to how behind it is on capabilities, it is unlikely Amazon will release a new version. For Amazon’s use cases, there is only a small need for image generation models anyway. This is not true for companies like Google, ByteDance, and Meta which have large consumer facing apps that can leverage image generation models more effectively.
