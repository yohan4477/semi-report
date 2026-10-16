---
source: https://daily.semidoped.com/p/daily-update-september-10th-2026
title: Daily Update - September 10th, 2026
date: 2026-09-10
kind: clipping
genre: daily
audience: everyone
subtitle: Groq-Nvidia hit by DoJ investigation, d-Matrix Raptor + Nvidia, DeepSeek improvements, OpenAI AI intern, Kepler Compute.
---
**Hello world, it’s Thursday, September 10th.**

DOJ is looking into Nvidia-Groq deal, d-Matrix Raptor chips to work alongside NVIDIA racks, DeepSeek gets way way cheaper, OpenAI makes research intern → goes for researcher’s job next, and a real mysterious memory company.

Let’s get into it. _— Austin & Vik_



 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

_Tell us how to make Semi Doped better![ Give us your feedback](<../_img/2026-09-10--daily-update-september-10th-2026/001_poll> "http://semidoped.com/poll")! ❤️_

### DOJ Probes Whether Nvidia Structured Groq Deal to Skirt Merger Review

The Justice Department has opened an antitrust investigation into Nvidia’s licensing deal with AI chip startup Groq, according to reporting cited by [Reuters](https://www.reuters.com/legal/litigation/us-doj-probes-nvidias-licensing-deal-with-ai-startup-groq-nyt-reports-2026-09-10/). The probe centers on whether Nvidia deliberately framed the arrangement as a licence rather than an acquisition to stay below thresholds that would trigger mandatory merger review. The deal is valued at roughly $17 billion to $20 billion, depending on the source, making it substantial enough that its structure, not just its size, drew federal attention. Nvidia’s stock dipped on the news. The DOJ has not filed any action, and neither company has publicly commented on the investigation’s scope.

> **Vik:**_The acqui-hire deal was exactly supposed to avoid an anti-trust, but DoJ hot on Nvidia’s case after all. Guess the plan didn’t work out as expected? Let’s see how it goes._
> 
> **Austin:**_To be fair, there was precedent before Nvidia. Remember[Microsoft + Inflection, Google + Character.AI](https://www.cnbc.com/2024/08/30/how-google-microsoft-and-amazon-are-raiding-ai-startups-for-talent.html)? _

### d-Matrix Ties Raptor XPU to NVLink Fusion and Nvidia MGX Rack Standard

Inference chipmaker d-Matrix [announced it will connect its next-generation Raptor XPUs to Nvidia’s AI infrastructure](https://www.prnewswire.com/news-releases/d-matrix-adopts-nvidia-nvlink-fusion-rackscale-infrastructure-for-ultra-low-latency-ai-inference-302875104.html) through NVLink Fusion, integrating with both NVLink scale-up networking and the Spectrum-X scale-out fabric. The company also adopts the Nvidia MGX rack architecture, meaning its hardware ships inside a chassis designed to Nvidia’s own mechanical and electrical spec. d-Matrix is joining what Nvidia describes as a growing roster of ecosystem partners, a list that now spans custom silicon startups willing to wire their products into Nvidia’s interconnect stack rather than build independent rack topologies. 

> **Austin:**_If you’re an AI accelerator startup you COULD build everything — compute, scale-up, cooling, rack design, etc… or you could partner with Nvidia and use their scale-up networking, cooling etc which is already deployed in production worldwide…_
> 
> **Vik** : _Raptor gains access to Nvidia AI factory deployments, and Nvidia gains another accelerator vendor whose product only fully performs inside its own infrastructure. This is good news for d-Matrix whose 3D DRAM approach I personally like a lot for AI inference. It’s a challenging engineering problem, but even Qualcomm’s HBC is along the same vein._

### DeepSeek’s V4.1 Flash Model Prices Inference at Fractions of a Cent

DeepSeek released V4.1 Flash on Thursday, built on a 552-billion-parameter Mixture-of-Experts architecture using what the company calls a [“Causal-Encoder-Decoder” design](https://www.scmp.com/tech/big-tech/article/3367051/deepseek-says-new-flash-ai-model-beats-kimi-k3-cyber-coding-benchmarks?utm_source=rss_feed). The model charges [as little as a fraction of a cent per million tokens](https://www.bloomberg.com/news/articles/2026-09-10/deepseek-s-new-low-cost-model-deals-a-fresh-blow-to-openai-z-ai), undercutting rivals including Anthropic, OpenAI, and Z.AI. DeepSeek also claims V4.1 Flash beats Kimi K3 on cybersecurity and coding benchmarks while running faster than its previous flagship. The pricing isn’t accidental; each successive DeepSeek release has arrived cheaper and more capable, compressing the global floor for inference. Hyperscalers that built CapEx cases around premium model pricing now face a competitor content to charge almost nothing.

> **Vik:**_DeepSeek has been continuously improving on how they compress KV cache, which means they need to use even lesser SSD offload. The progress is actually impressive. zephyr_z9 on X posted a good picture of this._
> 
> [![X avatar for @zephyr_z9](<../_img/2026-09-10--daily-update-september-10th-2026/002_Jk4w7gjp.jpg> "https://substackcdn.com/image/fetch/$s_!X8j6!,w_40,h_40,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fpbs.substack.com%2Fprofile_images%2F1837802996723597312%2FJk4w7gjp.jpg") Zephyr@zephyr_z9Deepseek has compressed KV cache size per token by 54x in the last 9 months ![](<../_img/2026-09-10--daily-update-september-10th-2026/003_HR1k2r2bQAA3bek.png> "https://pbs.substack.com/media/HR1k2r2bQAA3bek.png")7:03 AM · Sep 10, 2026 · 95.1K Views
> 
> * * *
> 
> 14 Replies · 67 Reposts · 683 Likes](https://x.com/zephyr_z9/status/2097943984425545755?s=20)

### OpenAI Reports Automated Research Intern Goal Met, Targets Full AI Researcher by 2028

[OpenAI published internal metrics](https://openai.com/index/research-acceleration-view-inside-openai/) on September 6, 2026 showing its research organization now uses 3.1 agent-workdays of effort for every workday of human labor, up from below parity before June 2026. The company states it has met its previously announced goal of building an automated research intern by September 2026, defined as a system that can complete well-defined tasks under human direction that would take a skilled researcher a few days. The company says it is targeting an automated AI researcher by March 2028 and plans to continue public reporting on its progress toward recursive self-improvement.

> **Vik: ✅** _AI intern check, 📌 AI researcher. 3.1 agent workdays / 1 human workday - so thats the metric here, and its rapidly accelerating. By the end of the year, we should easily have a 10x employee that never tires. Is any job safe now?_
> 
> **Austin:**_Vik, when are you creating a Semi Doped intern for us?_

### Wafer Launches AI Performance Engineering Series Starting with Prefill vs Decode

Wafer announced the launch of what it describes as the most comprehensive AI performance engineering repository, followed by a deep-dive series covering each resource. The series begins with Part 1 on prefill vs decode.

**Sources:** [@wafer_ai](https://x.com/wafer_ai/status/2096104842712469923?s=46)

[![X avatar for @wafer_ai](<../_img/2026-09-10--daily-update-september-10th-2026/004_dx5Anxe6.png> "https://substackcdn.com/image/fetch/$s_!ghF1!,w_40,h_40,c_fill,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fpbs.substack.com%2Fprofile_images%2F2002108104599642112%2Fdx5Anxe6.png")wafer@wafer_aiWafer AI Performance Engineering Repo: github.comGitHub - wafer-ai/gpu-perf-engineering-resources: A curated resource list for learning AI performance engineering, from GPU fundamentals to production inference.![](https://substackcdn.com/image/fetch/$s_!PKhN!,w_64,h_64,c_fill,f_auto,q_auto:good,fl_progressive:steep,g_auto/https%3A%2F%2Fpbs.substack.com%2Fnews_img%2F2096836802917330944%2FeZfhw3lN%3Fformat%3Djpg%26name%3Dorig)5:15 AM · Sep 5, 2026 · 894 Views

* * *

1 Reply · 11 Likes](https://x.com/wafer_ai/status/2096104842712469923)

> **Vik:**_Great learning resource, highly recommend._

### 👀 Look at this mysterious memory company

[![](<../_img/2026-09-10--daily-update-september-10th-2026/006_8bd3a8ea-c227-4967-adb0-ed7fba4cba66_1377x875.png> "https://substackcdn.com/image/fetch/$s_!CsYw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8bd3a8ea-c227-4967-adb0-ed7fba4cba66_1377x875.png")](https://substackcdn.com/image/fetch/$s_!CsYw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8bd3a8ea-c227-4967-adb0-ed7fba4cba66_1377x875.png)

See more at [keplercompute.com](https://keplercompute.com/).

### Sector Watch

#### Foundry & Packaging

  * **GlobalFoundries** and **Monolithic Power Systems** sign a long-term manufacturing agreement to produce advanced power solutions at GF’s Singapore fab. ([quiverquant.com](https://www.quiverquant.com/news/GlobalFoundries+and+Monolithic+Power+Systems+Announce+Long-Term+Manufacturing+Agreement+for+Advanced+Power+Solutions+in+Singapore))

  * **Samsung Foundry** and **Cadence** expand their AI design ecosystem partnership to cover next-generation AI infrastructure and physical AI process nodes. ([Samsung Semiconductor](https://semiconductor.samsung.com/news-events/tech-blog/samsung-foundry-and-cadence-expand-ai-design-ecosystem-for-next-generation-ai-infrastructure-and-physical-ai/))

  * **Taiyo Holdings** launches the FPIM Series packaging material, achieving a three-layer RDL formation with 700 nm critical dimensions on 12-inch wafers for advanced semiconductor packaging. ([PR Newswire](https://www.prnewswire.com/news-releases/taiyo-holdings-launches-next-generation-semiconductor-packaging-material-fpim-series-achieving-its-first-three-layer-rdl-formation-with-700-nm-cd-on-12-inch-wafers-302874600.html))




#### Memory

  * **UMC** reports August revenue up 30%, as mature-node demand tightens. ([inkl](https://www.inkl.com/news/united-microelectronics-sales-jump-30-in-august-umc-stock-has-more-room-to-run))

  * **Huawei** raises the price of its Ascend 950DT AI accelerator by 60% over three months; **Cambricon** also lifts prices as domestic HBM supply remains critically short. ([Bloomberg.com](https://www.bloomberg.com/news/articles/2026-09-10/huawei-lifted-prices-for-its-best-ai-chip-by-60-this-summer))

  * **Simmtech** unveils a next-generation AI semiconductor substrate technology aimed at advanced packaging demand from high-bandwidth memory stacks. ([아시아경제](https://www.asiae.co.kr/en/article/stock-disclosure/2026090909090728203))




#### Compute & Edge

  * **AMD** ships 50,000 MI450 GPUs from its Helios generation to Oracle, marking the first large-scale deployment of the new accelerator. ([shattered.io](https://shattered.io/amd-helios-mi450-oracle-50000-gpus-2026/))

  * **Qualcomm** details its next Snapdragon flagship with an upgraded Hexagon NPU capable of running 30-billion-parameter on-device AI models. ([ServeTheHome](https://www.servethehome.com/qualcomm-details-next-gen-oryon-cpu-adreno-gpu-and-hexagon-npu/))

  * **Renesas** launches the 64-bit RZ/G3L and RZ/G3SE MPUs targeting HMI and IoT edge designs with a unified development environment. ([EE News Europe](https://www.eenewseurope.com/en/renesas-rz-g3-mpus-target-hmi-and-iot-edge-designs/))




#### China Chip Industry

  * **Enflame** debuts on the Hong Kong Stock Exchange following its $913 million IPO, completing China’s ‘four-dragons’ domestic GPU public listings. ([digitimes](https://www.digitimes.com/news/a20260910PD222/gpu-revenue-ai-chip-2026-2025.html))

  * **Loongson** raises $340 million to expand homegrown CPU and GPU development as AI inference demand boosts domestic chip plans. ([digitimes](https://www.digitimes.com/news/a20260910PD216/loongson-cpu-gpu-development-technology.html))

  * **SMIC** posts quarterly revenue above $3 billion for the first time, narrowing the gap with Samsung Foundry to roughly $250 million. ([XenoSpectrum](https://xenospectrum.com/en/smic-q2-2026-growth-gap/))




#### Power

  * **DB HiTek** completes reliability qualification for its 8-inch, 1,200V SiC MOSFET process and targets mass production in 2027, claiming the world’s first 8-inch SiC foundry line. ([Chosunbiz](https://biz.chosun.com/en/en-it/2026/09/09/PRZYMOGPAVAEHNJJ4HTKIQKSAM/?outputType=amp))

  * **Infineon** and **SolarEdge** extend their partnership to deliver solid-state DC fault protection for 800 VDC AI data-center power architectures. ([Energetica India Magazine](https://www.energetica-india.net/news/infineon-and-solaredge-expand-800-vdc-data-centre-power-protection-collaboration))

  * **ASML** and **Xanadu** announce a collaboration to optimize lithography processes for ultra-low-loss quantum photonic hardware. ([Quantum Zeitgeist](https://quantumzeitgeist.com/asml-xanadu-collaboration-photonics-quantum/))




#### Data Centers & Infrastructure

  * **Wistron** and **Wiwynn** both hit record August revenues; Wiwynn says AI server shipments will overtake general-purpose servers in Q3 2026 and is adding a 120 MW power plant for its Socorro factories. ([digitimes](https://www.digitimes.com/news/a20260909PD250/wistron-revenue-wiwynn-2026-expansion.html))

  * **Nvidia** announces a major expansion of data-center capacity in Australia, partnering with local operators to meet surging AI compute demand. ([Nvidia News](https://nvidianews.nvidia.com/news/nvidia-expands-ai-infrastructure-capacity-in-partnership-with-australias-data-center-ecosystem))

  * **Crux AI** , the Google-Blackstone TPU neocloud venture, formally launches and hires Meta’s former data-center engineering head Alan Duong. ([Data Center Dynamics](https://www.datacenterdynamics.com/en/news/google-blackstones-tpu-neocloud-named-crux-ai-hires-metas-data-center-engineering-head-alan-duong/))




#### Optics & Networking

  * **Huawei** unveils a new high-speed optical module and proprietary optical interconnect standard positioned as a direct challenge to Nvidia and Broadcom in AI infrastructure. ([Nikkei Asia](https://asia.nikkei.com/business/technology/artificial-intelligence/huawei-unveils-new-optical-tech-standard-in-challenge-to-nvidia-broadcom))

  * **Singtel** and **Gulf Development** forge a strategic partnership to build a new subsea cable link between Singapore and Thailand. ([Light Reading](https://www.lightreading.com/cable-technology/singtel-and-gulf-development-to-invest-in-singapore-thailand-cable-link))

  * **Spark Wholesale** launches a dedicated data-centre interconnect service in Auckland built on **Ciena** optical transport equipment. ([reseller.co.nz](https://www.reseller.co.nz/article/4220411/spark-launches-dedicated-data-centre-interconnect-service-with-ciena.html))




_Tell us how to make Semi Doped better![ Give us your feedback](<../_img/2026-09-10--daily-update-september-10th-2026/007_poll> "http://semidoped.com/poll")! ❤️_

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-september-10th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
