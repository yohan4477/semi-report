---
source: https://daily.semidoped.com/p/daily-update-july-24th-2026
title: Daily Update - July 24th, 2026
date: 2026-07-24
kind: clipping
genre: daily
audience: everyone
subtitle: AMD unveils MI455X and Helios rack, Anthropic commits $5B on MI450, Intel short on chips through Q4 2026 despite $20B+ CapEx, Nvidia prepays Amkor $1.5B for Arizona packaging.
---
**Good morning, it’s July 24th, 2026.**

$1.5B from Nvidia to Amkor locks in domestic advanced packaging capacity in Arizona for multiple years. Intel, meanwhile, will be short on chips through Q4 2026 even with 2026 CapEx lifted above $20 billion. Elsewhere, AMD unveiled the MI455X, ROCm.ai, and Helios Rack at its Advancing AI 2026 event, extending its full-stack push against Nvidia across training, inference, and deployment.

Let’s get into it. _— Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

**Presented by …** _(this spot is open: reply to this email to talk sponsorship)_

### AMD Launches MI455X, ROCm.ai, and Helios Rack to Broaden AI Stack

AMD’s Advancing AI 2026 event — held after the previously reported Anthropic $5B investment / 2 GW MI450 compute deal — unveiled a full-stack platform spanning new silicon, software, and infrastructure partnerships targeting Nvidia across training, inference, and deployment. The breadth signals AMD is competing on ecosystem lock-in, not chip specs alone.

  * MI455X targets large-scale AI factories; MI430X targets sovereign AI and HPC — two distinct SKUs from the Instinct MI400 series, both built on TSMC 2nm with CoWoS-L packaging ([TrendForce](https://www.trendforce.com/news/2026/07/24/news-amd-unveils-mi455x-targeting-nvidia-rubin-tsmc-2nm-cowos-l-demand-seen-rising/)).

  * [ROCm.ai](https://www.amd.com/en/products/software/rocm.html?utm_campaign=domain&utm_medium=redirect&utm_source=301&utm_term=rocm.ai) launched as an AI-native dev platform with automated optimization, claiming up to 3.3x inference gains — AMD’s direct answer to CUDA’s software moat.

  * Helios rack-scale system pairs MI455X GPUs with 6th-gen EPYC Venice CPUs and open Ethernet networking.

  * [Cerebras WSE](https://www.cerebras.ai/press-release/amd-and-cerebras-announce-industry-leading-ultra-low-latency-and-high-throughput-ai-inference) integrated into Helios for inference, claiming 5x tokens-per-second-per-watt versus alternatives — great for low latency inference.




> **Vik:** _At their Advancing AI event, AMD announced a whole gamut of hardware upgrades that puts them head-to-head with Nvidia. AMD, with their ROCm.ai software stack, intends to compete with CUDA head on. In the era where AI writes code, a good software stack coupled with coding agents should in theory break the CUDA moat. AMD Venice CPUs are getting into production too, with 256c/512t performance. Noticeably, they announced multiple SKUs to match CPU performance to head-node versus agentic applications. I predicted this in my[CPU post in February](https://www.viksnewsletter.com/p/the-cpu-bottleneck-in-agentic-ai) this year; good to see it come to fruition. _
> 
> **Austin:** _One can argue the GPU silicon marketplace didn’t have true competition yet given that only Nvidia had a 72-GPU scale up domain. Now AMD has the hardware to match. But software was the next challenge; how much time would it take to port a workload to ROCm, and would the software prevent the full expression of the hardware? But OpenAI and Anthropic both said ROCm is no longer a huge barrier. So, then, come late 2026 and 2027, there will be actual competition._

### Intel Beats Q2 Estimates; AI Data Center Demand Lifts Sales Forecast

Intel’s second-quarter 2026 results topped analyst expectations, and the company’s forward sales guidance cleared estimates by a wide margin, sending shares sharply higher after market close. ([Reuters](https://www.reuters.com/business/intel-forecasts-upbeat-quarterly-revenue-profit-strong-ai-driven-server-chip-2026-07-23/)) The stock’s move surprised analysts who had argued that even strong results might not be enough to reverse Intel’s July slide. ([Bloomberg Tech](https://www.bloomberg.com/news/articles/2026-07-23/intel-needs-more-than-blowout-earnings-as-chips-rally-falters))

CEO Lip-Bu Tan and CFO Dave Zinsner attributed the outperformance to the AI data center boom, which is now visibly pulling demand for Intel chips across hyperscaler and cloud customers. The earnings call gave investors the first detailed look at the recovery’s composition. ([Intel Newsroom](https://newsroom.intel.com/corporate/intel-reports-second-quarter-2026-financial-results))

SK Hynix is in talks with Intel to **jointly operate** Intel’s semiconductor fabrication facility in Ohio — a structure that stops short of an outright acquisition. The discussions followed a Semafor report on **July 22** that Intel is actively seeking a partner to run the plant, citing people familiar with the matter. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=12480))

> **Vik:** _Intel has a strong recovery story really, and my guess is that the story is only going to get better due to 3 reasons: CPU demand, advanced packaging, and 18A becoming a widely used node._
> 
> **Austin:** _14A is a go! HVM 2028!_
> 
> _LBT: “I'm pleased to see the increasing momentum on customer engagements for Intel 14A, and I'm increasingly confident that the 14A will be highly competitive process offering across key vectors of performance, power, density, cost, and schedule._
> 
> _With encouraging external customer progress and increased demand for our internal products, we remain on track for 14A risk production for our internal products in the second half of 2027, and we make the decision in Q2 to fully commit to high volume ramp in 2028.”_

### Nvidia Commits $1.5B to Amkor for Domestic Advanced Packaging

Nvidia has signed a $1.5 billion multi-year prepayment agreement with Amkor Technology (Nasdaq: AMKR) for advanced packaging and test technologies supporting next-generation AI infrastructure. ([Amkor Technology](https://ir.amkor.com/news-releases/news-release-details/amkor-technology-announces-strategic-partnership-nvidia-expand)) The deal formalizes a long-term collaboration on packaging for AI and accelerated computing platforms.

Capital from the agreement will fund expansion of Amkor’s **Arizona** facilities, targeting **high-density interconnect** and heterogeneous integration capabilities — the package-level technologies central to assembling large-scale AI accelerators.

> **Vik:** _Advanced packaging is very important, and NVIDIA securing supply by dropping a few “bils” is a strong signal. They have done this already with many companies in the supply chain._

### Etched Raises $300M at $10.3B Valuation for Inference Silicon

Etched has closed a **$300M funding round at a $10.3B valuation** , led by Sequoia Capital, to build what it describes as Gigawatt-scale inference infrastructure for frontier AI models. ([etched.com](https://www.etched.com/progress))

The company is positioning its product not as a standalone chip but as a full-stack inference cluster — co-designed silicon, packaging, PCBs, cold plates, and interconnects — on the premise that the most capable models cannot be served efficiently on general-purpose hardware.

> **Vik** : _Good for Etched and great to see new solutions come to market. Inference hardware is amorphous and many shapes can solve problems in new ways. We are just getting started on inference, and it is here to stay. Any long arc of technology will see different solutions come to market: some will fail, some will succeed. Only time will tell._

## Quick Hits

  * **IBM** acquires HRL Laboratories, adding silicon-spin qubit and quantum sensing expertise to extend its quantum computing roadmap beyond superconducting architectures. ([IBM](https://newsroom.ibm.com/2026-07-23-ibm-to-acquire-hrl-laboratories-to-power-the-future-of-quantum))

  * **SK Hynix** pulls Cheongju P&T7 HBM advanced packaging cleanroom opening forward by three months, accelerating capacity essential to HBM4 supply for next-generation AI accelerators. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=12485))

  * **SK Telecom** commits ₩750B ($510M) to newly established subsidiary SK Hyper to build dedicated AI data center infrastructure serving Korean hyperscale compute demand. ([Light Reading](https://www.lightreading.com/data-centers/sk-telecom-commits-510m-to-new-ai-data-center-subsidiary))

  * **PsiQuantum** secures a $125M DARPA contract, its largest US government award, advancing photonic quantum computing development on a government-backed timeline. ([EE News Europe](https://www.eenewseurope.com/en/psiquantum-lands-125m-darpa-quantum-deal/))

  * **Anthropic** is considering requiring all employees, not just executives, to sell post-IPO shares via preset 10b5-1 plans to limit insider-trading risk and manage selling pressure after its valuation hit $965 billion. ([x.com](https://x.com/wallstengine/status/2080290328670875951?s=20))




### Key Data

Google’s cash flow is negative?! They’re REALLY spending on this AI infra buildout. As the saying goes — if you see a bubble, run towards it. Bullish AI.

[](https://substackcdn.com/image/fetch/$s_!33JE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fce83adb7-d7c7-4b86-8e94-baff2b8d1e6c_1023x1023.jpeg)

### Funny

LOL

[](https://substackcdn.com/image/fetch/$s_!-gJx!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85910a43-b29f-48b0-adcc-7b1292e611e0_1125x840.png)LOL. From SemiAnalysis

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-july-24th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
