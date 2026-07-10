---
title: "AMD 2.0 - New Sense of Urgency | MI450X Chance to Beat Nvidia | Nvidia's New Moat"
source: "https://newsletter.semianalysis.com/p/amd-2-0-new-sense-of-urgency-mi450x-chance-to-beat-nvidia-nvidias-new-moat"
author:
  - "[[DYLAN PATEL]]"
  - "[[KIMBO CHEN]]"
  - "[[DANIEL NISHBALL]]"
published: 2026-02-05
created: 2026-07-10
description: "Rapid Improvements, Developers First Approach, Low AMD AI Software Engineer Pay, Python DSL, UALink Disaster, MI325x, MI355x, MI430X UL4, MI450X Architecture, IF64/IF128, Flexible IO, UALink, IFoE"
tags:
  - "clippings"
---
_SemiAnalysis is expanding the AI engineering team! If you have an experience in PyTorch, training, inferencing, system modelling, SLURM/Kubernetes, send us your resume and 5 bullet points demonstrating your engineering excellence to[ letsgo@semianalysis.com](mailto:letsgo@semianalysis.com)._

Ever since [SemiAnalysis published an article in December 2024 detailing mediocre AMD software and the lack of usability](https://semianalysis.com/2024/12/22/mi300x-vs-h100-vs-h200-benchmark-part-1-training/), AMD has kicked into a higher gear and has made rapid progress in the past four months on many items we laid out. We view AMD’s new sense of urgency as a massive positive in its journey to catch up to Nvidia. AMD is now in a wartime stance, but there are still many battles ahead of it.

In this report, we will discuss the many positive changes AMD has made. They are on the right track but need to increase the R&D budget for GPU hours and make further investments in AI talent. We will provide additional recommendations and elaborate on AMD management’s blind spot: how they are uncompetitive in the race for AI Software Engineers due to compensation structure benchmarking to the wrong set of companies.

We will also discuss how AMD’s product launch cadence has put their current generation products against Nvidia’s next-gen products. Launching the MI325X at the same time as B200 has led to mediocre customer interest. Customers are now comparing the 8-GPU MI355X to the rack-scale 72-GPU GB200 NVL72 solution. [Our demand view in the Accelerator Model tracked Microsoft’s disappointment early in 2024 and lack of follow-on orders for AMD GPUs](https://semianalysis.com/accelerator-industry-model/).

We now believe that, there is renewed interest in AMD GPUs from [OpenAI via Oracle ](https://semianalysis.com/accelerator-industry-model/)and [a few other major customers](https://semianalysis.com/accelerator-industry-model/), but still not Microsoft, on the condition that they reach a sweet-heart pricing with AMD. **We will also outline how AMD’s window for fully catching up to NVIDIA could open in H2 2026, when AMD will finally bring a rack-scale solution to production. These SKUs, the MI450X IF64 and MI450X IF128, could be competitive to NVIDIA’s H2 2026 production rack-scale solution (VR200 NVL144).**

SemiAnalysis is actively working with NVIDIA and AMD on inference benchmarking on Hopper and CDNA3 class GPUs and will publish an article on comprehensive benchmarks and comparisons within the upcoming months.

## Executive Summary

  1. We met with Lisa Su to present our findings from the [December AMD article](https://semianalysis.com/2024/12/22/mi300x-vs-h100-vs-h200-benchmark-part-1-training) and she acknowledged the many gaps in the ROCm software stack & expressed a strong desire to improve.

  2. Over the past four months, AMD has made rapid progress on its AI software stack.

  3. In January 2025, AMD launched its developer relations (devrel) function, mainly led by Anush Elangovan, AMD’s AI Software Czar. His focus is interacting with external developers on Tech Twitter and In Real Life events.

  4. In January 2025, AMD recognized that external developers community are what made CUDA great and has since adopted a Developer First strategy.

  5. Before SemiAnalysis published our AMD article in December, [AMD had zero MI300X in PyTorch Continuous Integration/Continuous Delivery (CI/CD)](https://x.com/AnushElangovan/status/1877342554842345479). AMD has since added MI300 into PyTorch CI/CD. AMD has made great progress over the past four months on CI/CD.

  6. AMD plans to take a page out of [Google’s TPU Research Cloud (TRC) book](https://sites.research.google/trc/about/) and launch a developer cloud at their upcoming Advancing AI event in June. The metric for success is if an [GPT-J moment](https://arankomatsuzaki.wordpress.com/2021/06/04/gpt-j/) happens on their AMD’s community developer cloud. 

  7. AI Software Engineering compensation is AMD’s management’s blind spot. Their total compensation is significantly worse than companies that are great at AI software, such as NVIDIA and AI Labs.

  8. AMD's internal development clusters have seen significant improvements over the past four months, yet these enhancements still fall short of what is needed to compete effectively in the long-term GPU development landscape. 

  9. AMD should considerably increase & prioritize allocations of its investments into R+D CapEx and OpEx initiatives to give their teams significantly more GPU resources for software development. The current short-sighted focus on quarterly earnings compromises its capacity for long-term competitiveness. AMD needs to invest significantly more GPUs, they have less than 1/20th of Nvidia's total GPU count.

  10. Making the entire Cuda ecosystem first class on Python has been a top priority for Jensen. NVIDIA now has a pythonic interface at every level of the stack. ROCm does not have this. This is a serious threat to AMD's usability long term with developers.

  11. Although RCCL has made some decent progress, the delta between NCCL and RCCL continues to significantly widen due to the [new NCCL improvements and features announced at GTC 2025](https://www.nvidia.com/en-us/on-demand/session/gtc25-s72583/).

  12. AMD has made some progress in the last four months on its software infrastructure layer (i.e., Kubernetes, SDC detectors, health checks, SLURM, Docker, metrics exporters), but its rate of progress is nowhere near keeping up with the rate of progress of AMD’s ML libraries.

  13. AMD is currently lacking support for many inference features, such as good support for disaggregated prefill, Smart Routing, and NVMe KV Cache Tiering. NVIDIA [open-sourced Dynamo](https://github.com/ai-dynamo/dynamo), a distributed inference framework, further democratizing disaggregated serving for NVIDIA GPUs.

  14. The MI355X is still not competitive with NVIDIA’s rack scale GB200 NVL72 solution. Instead, AMD is pitching MI355X as being competitive to NVIDIA’s air-cooled HGX solutions, but this is not the purchasing comparison most customers are making.

  15. By 2H 2026, AMD’s MI450X rack-scale solution, if executed properly, could be competitive against Nvidia’s VR200 NVL144.

  16. SemiAnalysis is expanding the AI engineering team! If you have an experience in PyTorch, training, inferencing, system modelling, SLURM/Kubernetes, send us your resume and 5 bullet points demonstrating your engineering excellence to [letsgo@semianalysis.com](mailto:letsgo@semianalysis.com).

  17. AMD is hiring engineers across the whole software stack. Drop Anush a note at [anush+letsgo@amd.com](mailto:anush+letsgo@amd.com).




## What’s New Since our December AMD Article?

Hours after we dropped the AMD article, Lisa Su reached out to us to arrange a call with our engineering team to discuss in detail each of our findings and recommendations. The [very next day at 7am PT](https://x.com/dylan522p/status/1871287937268383867), we presented our findings to Lisa and walked her through our experience during the prior five months working with the AMD team to try to fix their software to carry out various workload benchmarks.

We showed her dozens of bug reports our team submitted to our AMD engineering contacts. She was sympathetic to end users facing an unpleasant experience on ROCm and acknowledged the many gaps in the ROCm software stack. Furthermore, Lisa Su and her team expressed a strong desire for AMD to do better. To this end, for the next hour and a half, Lisa asked her engineering team and our engineers numerous detailed questions regarding our experience and our key recommendations.

[![](https://substackcdn.com/image/fetch/$s_!J7vr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcea36a0e-95e6-4689-add4-a09080b760ac_952x1024.png)](https://substackcdn.com/image/fetch/$s_!J7vr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcea36a0e-95e6-4689-add4-a09080b760ac_952x1024.png)Source: X

This tone shift from the top has resonated across the organization. **AMD is now in wartime mode** , it is addressing software gaps and is working hard on closing them. This is a huge change from when AMD’s PR department in 2024 _would not publicly acknowledge_ any major issues with software.

In 2025 thus far, AMD has acknowledged that their software has way more bugs are than Nvidia currently but are rapidly improving and are engaging the community to bring ROCm to parity. In particular, Anush Elangovan, the AMD AI Software Tzar, has been active in tackling the issues at AMD.

[![](https://substackcdn.com/image/fetch/$s_!Ovsn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F80d0fd27-c2ac-4831-89ad-f63cbce159ad_1024x632.png)](https://substackcdn.com/image/fetch/$s_!Ovsn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F80d0fd27-c2ac-4831-89ad-f63cbce159ad_1024x632.png)Source: X

## AMD’s Culture Shift – A Renewed Sense of Urgency

Acceptance is the final stage of grief. AMD has finally accepted its massive software gap and can now address its issues for its chance to beat NVIDIA in the software and hardware game. AMD has caught a second wind, [but Nvidia is still at an all-out sprint](https://nypost.com/2024/08/26/business/nvidia-employees-can-work-7-days-a-week-until-2-a-m-but-few-leave-because-of-ai-chip-giants-lavish-pay-report/), and AMD must match them and even outpace them to catch up. Nvidia’s staff clearly recognize that sometimes [extra hours are needed for Nvidia](https://nypost.com/2024/08/26/business/nvidia-employees-can-work-7-days-a-week-until-2-a-m-but-few-leave-because-of-ai-chip-giants-lavish-pay-report/) to continue to be a leader in a competitive market. For AMD to win, it needs to work at least as hard and smart as Nvidia if not harder and smarter. We see clear signs of this starting to happen.

[![](https://substackcdn.com/image/fetch/$s_!hkel!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F55518b58-c994-4df1-a886-b1a9d1dced75_1024x929.png)](https://substackcdn.com/image/fetch/$s_!hkel!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F55518b58-c994-4df1-a886-b1a9d1dced75_1024x929.png)Source: X

There plenty of examples of the focused and hungry teams catching up. xAI vs OpenAI is an example of how a shift in culture to adopt a sense of urgency and take a wartime stance can lead to a company catching up with the competition at a ludicrous speed.

[![](https://substackcdn.com/image/fetch/$s_!laUI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c90564f-6e0e-43ee-b752-5e554d659e3a_1024x530.png)](https://substackcdn.com/image/fetch/$s_!laUI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c90564f-6e0e-43ee-b752-5e554d659e3a_1024x530.png)Source: xAI

We see many concrete examples that show this dynamic starting to play out at AMD. One area where AMD was executing is their product roadmap to achieve parity with Nvidia on rack-scale solutions. We explain our estimates of their rack-scale MI450X solution later in the article.

Another example is AMD’s rapid progress on its AI software stack over the past four months. They have been showing significant improvements in both their [training](https://rocm.blogs.amd.com/artificial-intelligence/training_rocm_pt/README.html) and [inference performance](https://rocm.blogs.amd.com/artificial-intelligence/DeepSeekR1_Perf/README.html), as well as their out-of-the-box experience. [They even adopted SemiAnalysis code for their training benchmark](https://www.linkedin.com/feed/update/urn:li:activity:7292299941761187840).

In January 2025, AMD launched its developer relations (devrel) function as it has finally understood that developers are what made Nvidia’s CUDA great and now acknowledges that winning over developers will be critical to the success of ROCm. Currently, the developer relations team is led by Anush Elangovan, who is acting as the sole devrel for AMD at in-person events as well as on [social media forums such as Tech Twitter](https://x.com/AnushElangovan).

AMD is going even further on the developer front. In June, AMD will launch a developer cloud focused on engaging with the overarching community. This is a direct result of SemiAnalysis’s suggestion for AMD to close the gap.

[![](https://substackcdn.com/image/fetch/$s_!enEr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe11cfc7e-8974-4304-ac05-e0f9300e7f09_1024x396.png)](https://substackcdn.com/image/fetch/$s_!enEr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe11cfc7e-8974-4304-ac05-e0f9300e7f09_1024x396.png)Source: SemiAnalysis, AMD

AMD now beats Nvidia in the reproducibility of benchmarks and performance claims. AMD has started posting easy-to-follow instructions that allow users and developers to replicate their benchmarking runs instead of publishing unrealistic or biased performance claims that can’t be verified. A great example is how [AMD published a great blog on how to reproduce their MLPerf Inference 5.0 submission](https://rocm.blogs.amd.com/artificial-intelligence/reproducing-amd-mlperf-inference-submission/README.html). NVIDIA did not provide such instructions as part of the latest MLPerf exercise.

## What Makes CUDA Great?

CUDA’s greatest advantage isn’t just its internal software developers but also the ecosystem that includes 4 million external developers building on the CUDA platform, thousands of enterprises, and numerous AI Labs and startups. This creates a self‑reinforcing flywheel of tools, tutorials, and ready‑made kernels that lowers the barrier to adoption for every newcomer and keeps veterans moving fast. Due to this massive developer base, tribal knowledge is quickly shared with newcomers.

The result of this thriving ecosystem is that breakthrough ideas—whether new attention algorithms, state‑space models or high‑throughput serving engines—almost always appear on CUDA first, receive feedback sooner and get tuned harder on CUDA, which in turn attracts the next wave of developers.

The pay‑off from that collective energy is clear: when researchers publish a game‑changing kernel, the CUDA version typically launches day‑one. Tri Dao’s FlashAttention shipped reference CUDA code, and it took multiple quarters for ROCm to implement their own optimized attention. The selective‑state‑space model was the same, the authors only released a CUDA implementation but the authors themselves did not support or port it over to ROCm. The port of ROCm mamba was from AMD internal engineers and not the original authors. On the serving side, UC Berkeley’s vLLM and SGLang have their maintainers develop mainly on NVIDIA GPUs, and only after the CUDA path is stable do the maintainers then help AMD internal developers port to ROCm.

Another example is how bugs are discovered and patched faster thanks to the millions of external CUDA ecosystem developers. In contrast, on ROCm, it may take months before a bug is discovered, such as was the case with numerous bugs we discovered and reported last year. For example, ROCm’s torch.scaled_dot_product_attention API in 2024. Attention is the most important layer in start of the art transformer models.

## Developers, Developers, Developers

Since January 2025 AMD has been vocal about a developers first approach, echoing Steve Ballmer’s famous mantra and mirroring Jensen’s approach too. At [TensorWave’s “Beyond CUDA 2025” summit](https://www.youtube.com/watch?v=RAK3Ce0RXgM&ab_channel=TensorWave), Anush, AMD’s AI Software Tzar, framed ROCm’s future with three words—“**[developers, developers, developers”](https://www.youtube.com/watch?v=Vhh_GeBPOhs&ab_channel=MrWueb007)** We believe this developers-first approach and messaging will be amplified on a broader stage at AMD’s June keynote event. AMD has finally understood that what made CUDA unbeatable was not just great silicon but a swarm of external developers. We feel extremely positive about AMD’s new developers-first approach.

[![](https://substackcdn.com/image/fetch/$s_!4tT8!,w_1456,c_limit,f_auto,q_auto:good,fl_lossy/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3db26059-86f9-4fb7-87a6-d0139522cd42_240x180.gif)](https://substackcdn.com/image/fetch/$s_!4tT8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3db26059-86f9-4fb7-87a6-d0139522cd42_240x180.gif)Source: [Microsoft](https://www.youtube.com/watch?v=8fcSviC7cRM)

In January 2025, Anush took this developers-first approach by engaging with external ROCm developers on Tech Twitter & GitHub collecting feedback, being customer support whenever ROCm craps out (which is often), and personally answering questions. This hands‑on engagement is real progress, but AMD’s developer relations still runs on a skeleton crew; aside from Anush, AMD has basically zero full‑time dev‑rel engineers. AMD has started hiring [full time developer relations engineers](https://careers.amd.com/careers-home/jobs/63017?lang=en-us), but to close the gap with NVIDIA’s army of evangelists, the company will need at least 20+ devrel engineers that host regular in‑person hackathons and meetups.

NVIDIA’s annual GTC developer conference, _“Super Bowl of AI”_ packs more than 500 developer focused deep‑dive sessions and hands‑on labs into a single week. Those tracks—covering every layer of the stack from PyTorch to JAX to CUTLASS to CUDA C++ to Assembly to profiling tools —give external developers a reliable place to learn and push the frontier.

AMD, by contrast, still lacks a GTC style developer conference that has many developer focused sessions. The company’s June “Advancing AI” event will be great for roadmap reveals, but the event is essentially a few product keynotes plus a handful of prerecorded talks—nowhere near the multi‑track developer sessions, code‑lab depth developers get at GTC. If AMD is serious about its new developer‑first stance, it should launch an annual, in‑person ROCm Developer Conference: three to four days of parallel tracks that cover kernel authoring, graph compilers, HIP/Triton migration, MI300 cluster tuning, and real‑time debugging with the ROCm toolchain. Pair those talks with on‑site hackathons run by a beefed‑up (20‑plus‑strong) devrel team and follow‑up regional roadshows, and ROCm users would finally have a venue to share war stories, surface blocking bugs, and build the social fabric that made GTC indispensable to the CUDA community.

[![](https://substackcdn.com/image/fetch/$s_!WOCH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F72b092ea-fde3-4ba6-b237-1e7a7ae556b8_1024x562.png)](https://substackcdn.com/image/fetch/$s_!WOCH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F72b092ea-fde3-4ba6-b237-1e7a7ae556b8_1024x562.png)Source: NVIDIA

Although George Hotz could have settled for AMD’s earlier offer of cloud‑hosted MI300X systems with full BMC access, he insisted on physical hardware so he could _“hack the metal”_ directly. AMD initially balked—even though Hotz’s goal was to help open‑source tooling on their GPUs. The stalemate turned into a public spectacle when the widely respected PyTorch co‑creator, Soumith Chintala, tweeted in support of Geohotz receiving the physical boxes.

[![](https://substackcdn.com/image/fetch/$s_!VGzI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F049c7cb0-0422-45a0-beb7-a508493ebad5_1024x519.png)](https://substackcdn.com/image/fetch/$s_!VGzI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F049c7cb0-0422-45a0-beb7-a508493ebad5_1024x519.png)Source: X

We believe that this nudge worked, and a [Geohotz March 8 blog](https://geohot.github.io/blog/jekyll/update/2025/03/08/AMD-YOLO.html) revealed that AMD had relented, sending him the two MI300X boxes. With this, AMD finally passed _Geohotz’s “cultural test.”_ For AMD, this is arguably a bigger reputational coup than a technical one—shipping real silicon to a high‑profile hacker signals a newfound, developer‑first ethos that marketing dollars alone can’t buy, and it finally turns a bruising Twitter saga into a story demonstrating AMD’s new developer-first ethos.

In addition to sending Geohotz boxes, we believe that AMD can also score another easy reputation and marketing win by donating physical AMD GPU boxes to academic labs. [Jensen & Ian Buck has had a long history of donating GPUs to academics labs even going back as far as 2014](https://x.com/haozhangml/status/1914439713332863348?s=46). This year, Jensen continues to supporting academics labs such as [CMU’s Catalyst Labs](https://x.com/scsatcmu/status/1912910889566490821?s=46), [Berekely’s Sky labs](https://x.com/vllm_project/status/1893001644037566610), [UCSD’s HaoAI Lab](https://x.com/haoailab) and others for some time by donating physical gold plated B200 boxes to them in addition to providing free cloud access to NVIDIA GPUs.

![](https://substackcdn.com/image/fetch/$s_!jQ85!,w_474,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1e60ef98-391a-4d5a-a079-0fd11d14c4cc_1020x932.webp)![](https://substackcdn.com/image/fetch/$s_!0jHh!,w_474,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe56b3e58-d828-425f-8c3f-a49b35f57c6c_1024x1014.webp)![](https://substackcdn.com/image/fetch/$s_!kSeX!,w_474,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b0f75de-9411-4f09-bd45-9df07037cde6_947x1024.webp)

Source: X

## Continuous Integration / Continuous Deployment (CI/CD)

Before SemiAnalysis published the AMD article in December, [AMD had zero MI300X participating in PyTorch CI/CD](https://x.com/AnushElangovan/status/1877342554842345479). AMD has since added MI300 into PyTorch CI/CD. AMD had been well known for providing buggy software – adding MI300 into PyTorch CI will go a long way towards this effort of continuing to rid AMD’s software of bugs!

Previously, AMD’s did not want to spend money on investing in CI/CD resources, but we believe that this stance has changed over the past four months. At the ROCm SF developer meetup events, an AMD software engineer walked up to us, thanked us, and told us that they now have CI resources due to our efforts.

In addition to unit test CI, AMD has also enabled MI300X on TorchInductor Performance CI such that [performance is tracked in inductor /torch.compile commit](https://x.com/AnushElangovan/status/1884727132477382915). [According to a Meta CI engineer](https://x.com/_seemethere/status/1924526179463397425), AMD provided the MI300X nodes, while NVIDIA hasn't provided any resources, so Meta pays for all of the A100 and H100 capacity. For this specific compile CI, AMD is ahead of NVIDIA. However – there is still much progress to be had as AMD’s dynamic shapes torch.compile is only at a 77% pass rate compared to Nvidia’s 90%+.

[![](https://substackcdn.com/image/fetch/$s_!n9Zz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5c173e03-c664-47d1-a6ea-48bdc3c64918_1024x559.png)](https://substackcdn.com/image/fetch/$s_!n9Zz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5c173e03-c664-47d1-a6ea-48bdc3c64918_1024x559.png)Source: PyTorch

AMD should build on this progress by open sourcing and making all of their CI/CD and dashboards publicly accessible such that anyone can see the pass rate of AMD’s software across all ROCm libraries (HipBLASLt, Sglang, vLLM,TransformerEngine, etc). [Currently, the only publicly accessible ROCm CI for their ML libraries is PyTorch](https://hud.pytorch.org/benchmark/compilers).

## Upcoming Community Developer Cloud

One of the reasons that Google’s TPU was able to gain external developer adoption was due to TPU’s free Colab access and because it provided large cluster access via [TPU Research Cloud](https://sites.research.google/trc/about/) (TRC). This allowed the community quick and free access, enabling many interesting projects as shown in [TRC’s spotlight](https://sites.research.google/trc/spotlight/) and [the many papers published as part of TRC](https://sites.research.google/trc/publications/). In fact, in 2020, well before the ChatGPT moment, a high schooler was able to train a model that was competitive with GPT-2 on a relatively giant TPU pod for free. In addition to providing plenty of smaller 8-16 chip pods, TRC also regularly provides free 1-2-week access to 1000+ chip pods to researchers.

The [famous open source GPT-J model](https://arankomatsuzaki.wordpress.com/2021/06/04/gpt-j/) was also trained on TPUs for free leading to an complete open repo about how to use TPUs with JAX and furthering external community adoption of TPUs. TRC has been wildly successful at promoting the TPU and supporting the open-source community.

AMD’s developer cloud plans essentially take a page out of Google’s book. We believe that if AMD properly invests in enough GPUs for this developer cloud program such that its GPUs easily and freely accessible, AMD’s developer cloud will be able to help it broaden adoption of its GPUs. This is a key battle AMD must win in its race against NVIDIA.

**The metric for success is if an GPT-J moment happens on their AMD’s community developer cloud.**

[![](https://substackcdn.com/image/fetch/$s_!zzze!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3f186274-2562-43aa-b31e-5bb1f03e0fcf_1024x396.png)](https://substackcdn.com/image/fetch/$s_!zzze!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3f186274-2562-43aa-b31e-5bb1f03e0fcf_1024x396.png) Source: SemiAnalysis, AMD

## AMD Management’s Blind Spot – AMD AI Software Engineer Compensation

AMD faces a critical challenge in its AI software division due to non-competitive compensation, significantly impacting its ability to attract and retain top talent. Other companies that are known for developing great AI software pay significantly better than AMD.

While compensation isn't everything, it remains a significant factor influencing engineers' decisions. Engineers often evaluate career opportunities based on multiple factors, including technical challenges, workplace culture, and growth opportunities. However, competitive compensation remains critical, particularly in highly specialized fields such as AI software engineering.

It is well known amongst AI engineers that the total compensation packages at AMD, which include base salary, RSUs (Restricted Stock Units), and bonuses, lag considerably behind competitors like NVIDIA, Tesla Dojo, [OpenAI Chip Team](https://openai.com/careers/hardwaresoftware-co-design-engineer/), Google TPU, and xAI, etc.

In conversations with top AI software engineers about why they chose not to join AMD, many highlighted that working at AMD software feels like working on porting features that NVIDIA engineers developed two years earlier. In contrast, NVIDIA provides engineers with the opportunity to work on cutting-edge software and to build software for chips used in state-of-the-art models like o3, for both training and inference.

Additionally, engineers attracted to the "David" in a "David vs Goliath" scenario often choose Google TPU or the [OpenAI Chip team](https://openai.com/careers/hardwaresoftware-co-design-engineer/) over AMD. These teams offer significantly better compensation and arguably have a higher probability of success in competing against NVIDIA due to those companies having giant volume of internal workloads to be their own customers. This makes them more appealing options for ambitious engineers.

AMD's internal benchmarking of their compensation structure appears to cherry pick comparable companies. By benchmarking against semiconductor companies that aren't known for great software such as Juniper Networks, Cisco, and ARM, AMD may mistakenly perceive their compensation as competitive. However, when correctly benchmarked against companies renowned for AI software such as GPU kernels, GEMMs, PyTorch internals, distributed training infrastructure, and inference engines—the gap in pay becomes glaringly apparent.

When conducting a proper apples-to-apples comparison, for example, comparing an NVIDIA PyTorch Lead to AMD's PyTorch Lead or NVIDIA's NCCL engineers to AMD's RCCL engineers, NVIDIA pays significantly better and thus is able to attract and retain top talent.

This issue represents a critical blind spot in AMD management's strategy. We think that AMD understands how essential software engineers are to AMD’s long-term competitiveness and innovation and wants to place them at the core of their strategy, but we think the blind spot comes from inaccurate benchmarking and attempting to make comparisons in broad strokes – a fog of war, as it were. This unfortunately has resulted in a persistent undervaluation of software which risks further exacerbating the company's weaker software capabilities relative to its direct competitors.

AMD should keep AI software engineering base salaries stable but implement substantial increases in RSUs. By tying engineer compensation more closely to AMD’s future growth and, the company can more directly align the interests of their top talent with long-term organizational performance.

Given AMD’s financial position with over $5 billion in cash reserves, the company possesses ample capacity to invest strategically in software talent. Leadership must now decide to prioritize retaining and attracting high-caliber engineers through meaningful compensation enhancements. Without taking such action, AMD risks perpetuating its lag behind NVIDIA, undermining its progress in the rapidly evolving AI market.

## Internal Development Clusters Needs More Budget

AMD's internal development clusters have seen significant improvements over the past four months, yet these enhancements still fall short of what is needed to compete effectively in the long-term GPU development landscape.

Currently, AMD claims to have rented an aggregate capacity of ~8,000 MI300 GPUs from CSPs distributed across several clusters and it claims that among this, the largest single cluster contains about 2,000 MI300 GPUs. However, deeper examination suggests the realistic consistent availability may be closer to 3,000 to 4,000 GPUs in aggregate across the whole company as AMD internally operates on a burst model. Internal developers now have adequate access to single-node development resources, but multi-node and comprehensive cluster development remain constrained. This limitation severely impacts larger-scale projects and collaborative development efforts, and there is still a need for a substantial increase in absolute quantity and consistency of GPU availability.

Moreover, with the new industry-standard approach of datacenter-scale disaggregated prefill optimization for inferencing, even developing inference solutions now requires resources at the cluster scale. AMD’s current limited cluster level resources for individual internal developers further complicates its ability to effectively innovate and compete in this evolving landscape.

A major impediment to further expansion and innovation at AMD is the short-term, burst-oriented model for procurement of clusters for internal use, with most contracts lasting less than a year. This contrasts starkly with NVIDIA's strategy, which employs persistent, multi-year cluster deployments, giving engineers greater freedom to pursue creative and high-risk projects without continuous oversight from financial controllers. NVIDIA, for example, operates extensive internal GPU resources including the A100 Selene cluster with thousands of GPUs, two EOS clusters (one with 4,600 H100 GPUs and another with 11,000 H100 GPUs) alongside dozens of smaller 64-1024 sized H100/H200 clusters located both on-premises and rented from cloud providers such as OCI, Azure, CoreWeave, and Nebius, etc. The massive scale of the GB200 clusters they will get this year. The above numbers also exclude the billions of dollars of clusters for DGX Cloud that they have.

AMD's current setup, where each GPU hour effectively carries a direct profit-and-loss consideration, discourages essential exploratory projects and strategic long-term developments.

AMD must urgently pivot from its current sub-year cluster strategy toward signing long-term, multi-year commitments, and it should specifically invest in a substantial cluster of 10,000+ flagship class GPUs. Such a commitment would demonstrate AMD's dedication to each GPU generation, like NVIDIA’s robust, long-term software and hardware support spanning multiple years for every GPU generation. The existing burst model is significantly damaging AMD’s internal development efforts and limiting innovation potential. Transitioning to a sustained, multi-year investment approach will enable AMD to pursue strategic innovation and competitive advantage effectively.

With over $5 billion in available cash reserves, AMD clearly has the financial flexibility to shift toward a more strategic, long-term investment approach. The current short-sighted focus on quarterly earnings compromises AMD’s capacity for future innovation and development leadership. Adopting a multi-year commitment to GPU generations would significantly enhance long-term support, aligning AMD’s internal capabilities more closely with customer expectations. This strategic adjustment would also reassure customers regarding AMD’s commitment to sustained support and innovation, thereby strengthening market confidence and long-term partnerships.

## ROCm’s Lack of First-Class Python Support

Making the entire CUDA ecosystem a first-class experience on Python has been a top priority for NVIDIA for the past 12 months. None other than Jensen himself is personally looped in and managing this effort. In the 2010s, Jensen was the first to understand that investing into making CUDA software great for AI would pay dividends. In 2025, Jensen’s key insight is to now understand that the de facto language of AI is Python, and that supporting every layer of NVIDIA’s current C++ CUDA stack into the Python world will yield a high return on investment. AT GTC this year, NVIDIA released dozens of Python libraries from GEMM libraries like nvmath-python libraries to cuda.binding cuBLASLt bindings to kernel DSLs like cuTile, Warp, Triton, CuTe Python. Unfortunately, ROCm libraries support in Python is nowhere near what NVIDIA has. **NVIDIA has a python interface at every layer of the stack. AMD does not offer this.**

[![](https://substackcdn.com/image/fetch/$s_!EF_p!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feddb5bf0-2350-4224-9805-270fd7257b65_1024x557.png)](https://substackcdn.com/image/fetch/$s_!EF_p!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feddb5bf0-2350-4224-9805-270fd7257b65_1024x557.png) Source: NVIDIA

By supporting Python first class in CUDA, end users can spend less time to get the same performance or spend the same amount of time to get even better performance. CUDA Python effectively shifts the pareto frontier curve on “Performance of Application versus Time Spent Optimizing”

[![](https://substackcdn.com/image/fetch/$s_!PyIa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F632dac3f-4f52-4e0f-8ef6-86146a0046f5_1024x596.png)](https://substackcdn.com/image/fetch/$s_!PyIa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F632dac3f-4f52-4e0f-8ef6-86146a0046f5_1024x596.png)Source: NVIDIA

To use a simple example, previously if a developer wanted to call cuBLASLt with a custom epilogue, they would need to write a C++ extension and then Pybind it to Python which is a bit convolved and adds another layer of indirection that an ML engineer needs to worry about. Now with nvmath-python, the same task can now be carried out and automatically tuned with just 3 python lines**. The task is now turned from a 30-minute task to a 2-minute one.** These NVIDIA Python libraries aren’t just half-baked bindings, they are first-class implementations with performance top of mind.

[![](https://substackcdn.com/image/fetch/$s_!josI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbcb30bba-d5bd-4708-b3f3-c7afaecec424_1024x547.png)](https://substackcdn.com/image/fetch/$s_!josI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbcb30bba-d5bd-4708-b3f3-c7afaecec424_1024x547.png)Source: NVIDIA

In another example, with the cuda.cooperative device side library, one can now access speed of light CUDA prebuilt algorithms such as block reduce through a python interface. This level of performance was previously only available in C++ CUDA through [CUB](https://docs.nvidia.com/cuda/cub/index.html).

[![](https://substackcdn.com/image/fetch/$s_!voSq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52432d38-3103-4617-ab33-b1f06c0c23c6_1024x559.png)](https://substackcdn.com/image/fetch/$s_!voSq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F52432d38-3103-4617-ab33-b1f06c0c23c6_1024x559.png)Source: NVIDIA

For end users that want 1:1 Python bindings instead of higher order Pythonic libraries, NVIDIA also offers this through cuda.binding and cuda.core. **NVIDIA has a python interface at every layer of the stack. AMD does not offer this.**

[![](https://substackcdn.com/image/fetch/$s_!va6V!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92ec8da0-6bde-48e4-9f8a-f3e04cc848b9_1024x614.png)](https://substackcdn.com/image/fetch/$s_!va6V!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F92ec8da0-6bde-48e4-9f8a-f3e04cc848b9_1024x614.png) Source: NVIDIA

AMD has launched recently python interfaces for [AITER](https://github.com/ROCm/aiter) which is the equivalent of cuDNN-python and supports OAI triton for kernel authoring but the rest of the layers of the stack, ROCm has no comparable product and they aren’t even thinking about supporting a first-class python experience yet.

## Python GPU Kernel Authoring DSLs

At GTC 2025, in addition to debuting the overall Python CUDA libraries, NVIDIA also announced Python kernel authoring DSLs - namely Python CuTe 4.0, cuTile Python and Warp. And this is on top of Nvidia’s existing Triton DSL support! **AMD is lacking and uncompetitive in the Python Kernel DSLs space to the extent that Nvidia teams are now competing against each other with multiple different NVIDIA DSLs now publicly launched**. There are currently five different NVIDIA python DSLs (OAI Triton, CuTe Python, cuTile Python, Numba, Warp), with many more that are internally in the works that they haven’t announced publicly yet. 

Python kernel DSLs can be categorized into two types based on the abstraction unit. Programmers describe single-thread behaviors in thread-based languages, while in tile-based languages, they describe operations on partitions of matrices.

CuTe Python is NVIDIA’s recommended path for writing speed-of-light kernels in for thread-based Python kernel DSLs. It provides low-level primitives as building blocks for custom kernels, and it uses a powerful abstraction cuTe (CUDA Tensor) to describe data and thread layouts. CUTLASS Python’s API design is based on CUTLASS, so new users can leverage CUTLASS’s extensive documentation of concepts and usage to get up to speed. While AMD has a CUTLASS-analogous C++ library CK (Composable Kernel), its documentation on concepts and usage is comparatively sparse and unclear. CK Python interface is coming for their high-level interfaces but none in the works for their CuTe-analogous atom layer.

**More importantly, AMD in general currently has no Python DSLs for thread-based kernel programming which is needed for speed of light.**

[![](https://substackcdn.com/image/fetch/$s_!kIU8!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9f42354a-d080-4dc1-8112-433fd04cfdbc_1024x400.png)](https://substackcdn.com/image/fetch/$s_!kIU8!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9f42354a-d080-4dc1-8112-433fd04cfdbc_1024x400.png) Source: NVIDIA

For Tile Based and SIMT based as well as hybrid Tile/SIMT mixed based kernel authoring Python DSLs, NVIDIA announced cuTile at GTC 2025. cuTile is not meant for 100% speed of light performance but is meant for 98% speed of light performance at 10% the time to write the kernel. It is relatively easy to write kernels in cuTile**. Unfortunately, AMD has no offering for hybrid SIMT/Tile based python kernels DSLs.**

[![](https://substackcdn.com/image/fetch/$s_!_duY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f6b19e6-4f67-43a6-a1fa-d8c5dacb3927_1024x542.png)](https://substackcdn.com/image/fetch/$s_!_duY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6f6b19e6-4f67-43a6-a1fa-d8c5dacb3927_1024x542.png) Source: NVIDIA

Triton popularized tile-based programming models in the age of tensor cores where the effective abstraction is at the layer of a Tile instead of on a per thread basis. Nvidia will continue to fully support Triton’s Tile based DSLs in addition to cuTile Tile based DSLs.

[![](https://substackcdn.com/image/fetch/$s_!3VZH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3fc3d1cd-10f9-462e-9f5b-1651f860952b_1024x637.png)](https://substackcdn.com/image/fetch/$s_!3VZH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3fc3d1cd-10f9-462e-9f5b-1651f860952b_1024x637.png)Source: Nvidia

For differential simulation AI, NVIDIA announced Warp Python DSLs. Warp is a hybrid tile and SIMT based programming model useful for writing simulations and geometry processing. The great benefit of Warp over cuTile is that Warp is automatically differentiable which is extremely useful in simulation to automatically generate the backward pass. **AMD has no offering for this hybrid SIMT/Tile based differentiable Python kernels DSLs either.**

Nvidia continues to fully support OpenAI Triton Python DSL in addition to all their newly announced Python DSLs. The primarily maintainer of Triton is OpenAI whose mission is to build safe AGI. Indeed, at [the SemiAnalysis Blackwell PTX Hackathon 2025](https://semianalysis.com/2025-hackathon-eol/), **Phil Tilet, lead OpenAI maintainer of Triton, has even said that “AGI won’t come from 10% faster matrix multiplications”,** & this is the ethos surrounding what features Triton will prioritize. Thus Triton isn’t the platform AI chip vendors should solely support if they want to have the fastest AI chip. We believe that AI chip vendors should still fully support Triton in addition to other Python DSLs.

[![](https://substackcdn.com/image/fetch/$s_!MnHX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5ef71117-a094-4525-94b4-047e37aa43a1_1024x196.png)](https://substackcdn.com/image/fetch/$s_!MnHX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5ef71117-a094-4525-94b4-047e37aa43a1_1024x196.png)Source: OpenAI, [SemiAnalysis Blackwell PTX Hackathon](https://semianalysis.com/2025-hackathon-eol/)

This stance has led to a misalignment of objectives where OpenAI Triton does not care about getting absolute speed of light peak performance while AI Chip vendors like Nvidia, MTIA, MAIA, AMD care a lot about getting peak performance in their kernel language.

Nvidia’s Triton performance isn’t close to speed of light while AMD’s Triton performance is even further away from speed of light. AMD needs to heavily hire and invest into making Triton performance much stronger in addition to supporting/inventing in other python kernel DSLs.

AMD has an experimental kernel language called [wave](https://github.com/iree-org/iree-turbine/tree/main/iree/turbine/kernel/wave) that uses a warp based programming model but it seems to be still very early stage and doesn’t have the full backing of the company. This is a far cry from cuTile, CuTe, Warp, all of which have the full backing of Jensen and Nvidia, who are all in on making CUDA Python great. Furthermore, it is questionable if warp-based kernel DSLs add the right abstraction layer considering the industry is moving towards warp-group based MMAs hardware & 2-CTA MMAs hardware instead of warp based MMAs.

## The Widening Gap Between AMD RCCL and NVIDIA NCCL

Collective communication libraries are extremely important for AI training and inference as these libraries let multiple GPUs work on the same workload. Nvidia’s collective communication library is called NCCL. AMD’s library is a “ctrl+c, ctrl+v” fork of NCCL and it is called RCCL. Ever since we shared our thoughts on RCCL in [our December 2024 article](https://semianalysis.com/2024/12/22/mi300x-vs-h100-vs-h200-benchmark-part-1-training/), RCCL team has made some decent progress. More than a year after the MI300X went into production, the RCCL team has now finally supported the [LL128 protocol](https://github.com/ROCm/rccl/pull/1549) on MI300X. This is a great improvement but by comparison, Blackwell on day one already supports all three collective protocols (SIMPLE, LL, LL128).

Furthermore, RCCL finally supports rail optimized trees which improves networking performance by reducing traffic away from spine switches, leading to fewer path collisions. This feature has been supported by NCCL by countless years already.

[![](https://substackcdn.com/image/fetch/$s_!Iwpm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fac743225-694a-4afe-b80b-51d61dc9f491_861x1024.png)](https://substackcdn.com/image/fetch/$s_!Iwpm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fac743225-694a-4afe-b80b-51d61dc9f491_861x1024.png)Source: Github

**Although RCCL has made some decent progress, the delta between NCCL and RCCL continues to significantly widen due to the[new NCCL improvements and features announced at GTC 2025](https://www.nvidia.com/en-us/on-demand/session/gtc25-s72583/). **TheRCCL team will need more access to proper resources like large compute clusters to catch up with NCCL. They should be given exclusive access to a persistent cluster of at least 1,024 MI300 class GPUs. Furthermore, AMD leadership needs to invest into massively increasing RCCL engineer RSUs compensation in order to attract and retain key talent in what is one of the most mission critical software libraries.

Because AMD’s RCCL library is a carbon copy fork of Nvidia’s NCCL, NCCL 2.27 and 2.28 massive refactor will continue expanding the CUDA moat and will force AMD’s RCCL team to expend thousands of engineering hours to sync Nvidia’s major refactor into RCCL. While AMD’s engineering team is bogged down having to spend thousands of engineering hours to sync the changes, Nvidia will be using that time instead to continue advancing the frontier of collective communications software stack and algorithms. This dynamic makes it virtually impossible for AMD to sustain RCCL’s existing development efforts while working towards achieving parity with NCCL, let alone surpassing NCCL.

AMD has indicated that they are currently in the planning phase of rewriting RCCL from scratch to stop being a fork of NCCL.

At his GTC 2025 talk, as a joke, we asked NCCL chief Sylvain Jeaugey, if in the spirit of open-source development, he would lend a helping hand to RCCL as its currently mostly a copy paste library.

He rebuffed our suggestion:  
  
_SemiAnalysis: Will Nvidia provide support to the AMD team's RCCL fork due to this big of a refactor in the upcoming 2.28?  
Sylvain: Are we going to also help RCCL move to that? I don't think so - usually we don't really take part in that development.  
Source: [Nvidia](https://www.nvidia.com/en-us/on-demand/session/gtc25-s72583/?start=2025) – timestamp 33:48_

During this talk, Sylvain also announced many new NCCL features in the upcoming massive refactor. These new features include supporting symmetric memory natively in NCCL as well as new algorithms that run much faster and use fewer SMs thus allowing more SMs for compute.

[![](https://substackcdn.com/image/fetch/$s_!TvBY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F54bd2315-6097-424a-b08f-ae4242ef30a0_1024x609.png)](https://substackcdn.com/image/fetch/$s_!TvBY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F54bd2315-6097-424a-b08f-ae4242ef30a0_1024x609.png)Source: NVIDIA

[PyTorch introduced SymmetricMemory API](https://dev-discuss.pytorch.org/t/pytorch-symmetricmemory-harnessing-nvlink-programmability-with-ease/2798) that enable users to harness multi-GPU scale up programmability with ease and [write collectives or fused compute/communication kernels in CUDA or Triton](https://github.com/yifuwang/symm-mem-recipes). Previously, writing multi-GPU fused compute/communication kernels required a ton of work, but the work needed has been reduced considerably with the use of PyTorch SymMem. Performant inference kernels like one-shot and two-shot collectives as well as all gather fused matmul kernels can be written in SymmetricMemory easily.

[![](https://substackcdn.com/image/fetch/$s_!tRJY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e1f7b17-388f-49bc-8739-54be3d68c5ed_1024x567.jpeg)](https://substackcdn.com/image/fetch/$s_!tRJY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5e1f7b17-388f-49bc-8739-54be3d68c5ed_1024x567.jpeg)Source: PyTorch

This feature has been available on NVIDIA GPUs for the past 8 months while AMD GPUs still don’t support it. AMD has indicated that they will land initial support for PyTorch SymmetricMemory API in Q2 2025.

[![](https://substackcdn.com/image/fetch/$s_!x4as!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc5748b2c-13ab-4f69-83b1-fc230f3f14b0_831x1024.png)](https://substackcdn.com/image/fetch/$s_!x4as!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc5748b2c-13ab-4f69-83b1-fc230f3f14b0_831x1024.png)Source: PyTorch, YiFu

In the upcoming 2.27 release, allreduce achieves a 4x lower reduction at the same message size and attains the same algorithm bandwidth at 4x smaller message sizes.

[![](https://substackcdn.com/image/fetch/$s_!sgsA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd54dcf51-7427-410a-8708-9f57626d7447_1024x620.png)](https://substackcdn.com/image/fetch/$s_!sgsA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd54dcf51-7427-410a-8708-9f57626d7447_1024x620.png)Source: NVIDIA

In the upcoming 2.28 release, NCCL offers device-side APIs allowing end users to easily write custom communication/compute fusion kernels.

[![](https://substackcdn.com/image/fetch/$s_!CVOk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc51b21f2-0ab0-461c-8dee-0b91070ab7f8_1024x619.png)](https://substackcdn.com/image/fetch/$s_!CVOk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc51b21f2-0ab0-461c-8dee-0b91070ab7f8_1024x619.png)Source: NVIDIA

The upcoming NCCL 2.28 release will also support [GPUDirect Async](https://developer.nvidia.com/blog/improving-network-performance-of-hpc-systems-using-nvidia-magnum-io-nvshmem-and-gpudirect-async/) (IBGDA) on both InfiniBand and RoCEv2 Ethernet. Currently, in NCCL and RCCL, a CPU proxy is used to control flow for scale-out communication. Although the dataflow doesn’t go through the CPU, sending the control flow through the CPU still limits the real world achieved performance. With NVIDIA NCCL’s 2.28 integration with IBGDA – supported in both RoCEv2 and InfiniBand - the control flow is initialized by the GPU and does not go through the CPU, leading to better performance on all2all and all2all based algorithms across small and medium message sizes.

Another feature that is currently only available on Nvidia is user buffer registration. This feature avoids creating extra copies between the user’s tensor and NCCL’s internal buffers. This helps with reducing the number of collective SMs needed and with alleviating memory pressure, leading a 5-20% end to end training improvement.

[![](https://substackcdn.com/image/fetch/$s_!sLMH!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5329093c-48c5-485e-8f1e-1370e09cfb23_1024x576.png)](https://substackcdn.com/image/fetch/$s_!sLMH!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5329093c-48c5-485e-8f1e-1370e09cfb23_1024x576.png)Source: NVIDIA

Most experienced ML engineers have seen the dreaded NCCL_TIMEOUT/RCCL_TIMEOUT or NCCL/RCCL stalling. NVIDIA NCCL supports [ncclras](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/troubleshooting/ras.html), which simplifies debugging these issues. Unfortunately, RCCL does not currently include any features to help with debugging.

[![](https://substackcdn.com/image/fetch/$s_!ahBk!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7fa2ea5c-a6ee-4a40-93b2-fc5089973420_1024x571.png)](https://substackcdn.com/image/fetch/$s_!ahBk!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7fa2ea5c-a6ee-4a40-93b2-fc5089973420_1024x571.png)Source: NVIDIA

## Infrastructure Software Progress Not As Fast

AMD’s has made meaningful progress in the last four months on its software infrastructure layer (i.e. kubernetes, SDC detectors, health checks, SLURM, docker, metrics exporters), but the rate of progress is nowhere near keeping up with the rate of progress of AMD’s ML libraries.

Until seven months ago, AMD had no GPU metrics export function at all, meaning that cluster operators had no way to gain observability into their GPUs. Although ROCm claimed to be an open-source ecosystem, AMD’s GPU metrics exporter was not open source until SemiAnalysis took this point up with AMD executives, advocating for them to adopt a sense of urgency for AMD to live by the ethos of their claimed commitment to the “open source” ecosystem.

Fortunately, after many follow-ups, AMD has finally open sourced their GPU exporter. Note that their GPU exporter is still a work in progress and many features are still missing and are not at parity with NVIDIA’s GPU open-source metrics exporter yet. For example, AMD’s GPU exporter currently has still does not support the metric for matrix core activity, CU occupancy or CU active. These are extremely important metrics to proxy how workloads are performing. The only current utilization metric available in AMD’s GPU exporter is GPU_UTIL which, as most experienced [ML engineers know, doesn’t actually measure util at all for both Nvidia and AMD GPUs](https://x.com/memorypaladin/status/1817689501113979357).

[As mentioned in our December AMD article](https://semianalysis.com/2024/12/22/mi300x-vs-h100-vs-h200-benchmark-part-1-training/#amd%e2%80%99s-forked-libraries), the AMD Docker UX is extremely poor compared to Nvidia’s UX. AMD has acknowledged this shortcoming and has mentioned to us that they are working on this. They have indicated that they will announce a roadmap for this later this quarter.

[![](https://substackcdn.com/image/fetch/$s_!KKN_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F936ac9c8-0ea8-4b8a-a7bf-a6197eaafdbd_1024x377.png)](https://substackcdn.com/image/fetch/$s_!KKN_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F936ac9c8-0ea8-4b8a-a7bf-a6197eaafdbd_1024x377.png)Source: SemiAnalysis

Unlike on Nvidia’s stack, the current state of Slurm+Container on AMD’s stack is disappointing. [On Nvidia with open source pyxis Slurm](https://github.com/NVIDIA/pyxis), launching container through Slurm is as easy as running “srun –container-name=pytorch”. In contrast, when working on AMD, one must through an extremely convolved process that requires the use of lots of indirections.

When considering how all AMD’s internal AI engineers use SLURM with containers, it is distressing to see the amount of indirection that are needed and how poor the current AMD Slurm+Container UX is.

[![](https://substackcdn.com/image/fetch/$s_!gpNJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F61e5a9a2-e3e6-4c85-8417-44ecb1f7d863_1024x575.png)](https://substackcdn.com/image/fetch/$s_!gpNJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F61e5a9a2-e3e6-4c85-8417-44ecb1f7d863_1024x575.png)[Source: GitHub, AMD](https://github.com/AMD-AIG-AIMA/InstellaVL/blob/9e143b50378cbbaea7784d6da0058c78d2e01352/scripts/1B_release/sbatch_instellavl_mlp_warmup.sh#L133-L142)

We have recommended on multiple occasions that AMD prioritize fixing this and focus on supporting a first-class Slurm+Containers experience by putting some money to work and paying for SchmedMD’s (the maintainers of Slurm) consulting services. We have yet to see any concrete timelines or roadmap on when AMD plans to fix this issue.

Moreover, Nvidia’s datacenter-manager tool (DCGM) has directly integrated NVVS (Nvidia Validation suite) such that running diagnostics is as simple as running “sudo dcgmi diag -r <diag_level>”. In contrast, on AMD, the RVVS (ROCm validation Suite) is separate from their Datacenter tool (RDC), forcing the end user to download yet another library. We recommend that AMD integrate RVVS into RDC to make the user experience as simple as that of Nvidia’s DCGM.

Also, AMD’s UX and validation coverage is not as good as DCGM’s. [Nvidia’s DCGM utilizes notation denoting different levels (r1,r2,r3,r4)](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html#run-levels-and-tests) while AMD’s NVVS does not use any such notation.

[![](https://substackcdn.com/image/fetch/$s_!4w3i!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa8ee03d-de4a-4608-a916-8aec310a78fb_1024x504.png)](https://substackcdn.com/image/fetch/$s_!4w3i!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa8ee03d-de4a-4608-a916-8aec310a78fb_1024x504.png)Source: NVIDIA

## AMD’s Lack of Disaggregated Prefill Inferencing and NVMe KV Cache Tiering

AMD is currently lacking support for many inference features such as disaggregated prefill, Smart Routing, and NVMe KV Cache Tiering. Disaggregated serving has been an industry standard for year, and last month NVIDIA [open-sourced Dynamo](https://github.com/ai-dynamo/dynamo), a distributed inference framework, further democratizing disaggregated serving. Disaggregated prefill splits the prefill stage and decode stage into different GPUs. Even Google has launched their own [disaggregated inferencing framework](https://cloud.google.com/ai-hypercomputer/docs/workloads/pathways-on-cloud/multihost-inference#disaggregated_inference).

[![](https://substackcdn.com/image/fetch/$s_!_fVY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff4244b1a-2acc-4edb-9ee8-c041950ae28a_1024x649.png)](https://substackcdn.com/image/fetch/$s_!_fVY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff4244b1a-2acc-4edb-9ee8-c041950ae28a_1024x649.png)Source: Peking University

NVIDIA’s Dynamo Smart Router intelligently routes each token in a multi-GPU inference deployment to both available instances. For the prefill phase – this means ensuring that incoming tokens are equally distributed to the different GPUs serving prefill to avoid bottlenecks on any given experts in the prefill phase.

Similarly – in the decode phase – it is important to ensure sequence lengths and requests are well distributed and balanced across GPUs serving decode. Some experts that are more heavily trafficked can be replicated as well by the GPU Planner provided by Dynamo to help keep the load balanced. 

The router also load balances across each replica serving the model which is something AMD’s vLLM and many other inference engines do not support.

[![](https://substackcdn.com/image/fetch/$s_!oslW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F77ae5735-0828-4180-93c9-312b9d8c3b22_1024x611.png)](https://substackcdn.com/image/fetch/$s_!oslW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F77ae5735-0828-4180-93c9-312b9d8c3b22_1024x611.png)Source: NVIDIA

Dynamo’s GPU Planner is an autoscaler of both prefill and decode nodes, spinning up additional nodes with fluctuations in demand that are natural over the course of the day. It can implement a degree of load balancing among many experts in an MoE model in both prefill and decode nodes. The GPU planner spins up additional GPUs to provide additional compute to high-load experts. It can also dynamically reallocate nodes between prefill and decode nodes as needed, further maximizing resource utilization. 

This additionally supports changing the ratio of GPUs used for decoding and for prefill – this is especially useful for cases like Deep Research, where more prefill is required as opposed to decoding, as these applications need to review a huge amount of context but only generate a comparatively small amount.

[![](https://substackcdn.com/image/fetch/$s_!51t_!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0cf5891f-e6cd-4808-a98d-69d46d8ae7f9_1024x554.png)](https://substackcdn.com/image/fetch/$s_!51t_!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0cf5891f-e6cd-4808-a98d-69d46d8ae7f9_1024x554.png)Source: NVIDIA

NVIDIA Dynamo’ KV-Cache Offload Manager allows more efficient overall execution of prefill overall by saving the KVCache from prior user conversations in NVMe storage rather than discarding it. 

When a user engages in an ongoing multi response conversation with an LLM, the LLM needs to factor in the prior questions and responses earlier in the conversation, taking these as input tokens as well. In the naïve implementation, the inference system will have discarded the KV Cache originally used for generating those earlier questions and responses, meaning that the KV Cache will have to be computed again, repeating the same set of calculations.

Instead, with Dynamo’s NVMe KVCache offload feature, when a user steps away, the KVCache can be offloaded to an NVMe storage system until the user returns to the conversation. When the user asks a subsequent question in the conversation, the KVCache can be quickly retrieved from the NVMe storage system, obviating the need to calculate the KVCache again.

This frees up capacity on the prefill nodes to handle more incoming volume, or alternative could reduce the size of the prefill deployment needed. The user will also have a much better experience with faster time to first token as there is now much less time needed to retrieve the KV Cache vs computing it. 

[![](https://substackcdn.com/image/fetch/$s_!KFxZ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdb44fab1-aabf-4e48-b3fd-8be71401570d_1014x683.png)](https://substackcdn.com/image/fetch/$s_!KFxZ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdb44fab1-aabf-4e48-b3fd-8be71401570d_1014x683.png)Source: NVIDIA

These features for KVCache offload will matter more and more as RLVR and multi-agent systems with tool use become more common.

## Summary of Recommendations to AMD

**We genuinely want to see another effective competitor to Nvidia and want to help AMD get to that spot**. AMD has made great progress over the past four months but there are still a lot of changes that AMD needs to make to be competitive with Nvidia. Earlier in the article, we have outlined in detail our recommendations to Lisa Su and the AMD Leadership Team, and we provide a summary here:

  1. AMD needs to maintain (if not intensify) their sense of urgency to even have a chance at being on par with NVIDIA.

  2. AMD leadership team’s biggest blind spot is low total compensation (base + RSU + bonus) for their AI software engineers due to incorrect compensation structure benchmarking to semiconductor companies instead of companies that are great at AI software. We have discussed how our recommendation will help strengthen the alignment of engineers’ compensation to AMD’s success (or failure). **We strongly believe that if AMD does not significantly increase their AI Software Engineer pay, AMD will continue losing to Nvidia.**

  3. We recommend that AMD invest heavily in Python interfaces at every layer of the ROCm stack, and not just in Python Kernel Authoring DSLs.

  4. AMD needs to invest heavily in a team of 20+ developer relations engineers hosting In Real Life events and interacting with the community at a deeper level.

  5. Unlike NVIDIA GTC, AMD doesn’t hold any developer-focused conferences and only holds product launch keynote events, for instance _“Advancing AI”._ We recommend that AMD host an in‑person “ROCm Developer Conference”.

  6. NVIDIA has launched their [Dynamo disaggregated prefill inference framework called](https://github.com/ai-dynamo/dynamo) and [their NIXL inference KV cache tiering library](https://github.com/ai-dynamo/nixl). AMD does not have first-class support for disaggregated prefill or NVMe KVCache tiering. They need to rapidly make progress on this, or they will fall behind on inference.

  7. AMD should give ROCm collective engineers a persistent cluster of at least 1,024 MI300 class GPUs that are for the exclusive of this team. This will go a long way towards helping RCCL catch up to NCCL.

  8. Nvidia overstates TFLOP/s in their chip specifications, but AMD overstates TFLOP/s specifications even more. [Even in AMD’s own blog, they have admitted to a significantly larger gap between their marketed TFLOP/s and what is achievable](https://rocm.blogs.amd.com/software-tools-optimization/Understanding_Peak_and_Max-Achievable_FLOPS/README.html) than users might experience with NVIDIA.

  9. AMD should state their Model FLOPS Utilization (MFU) and TFLOP/s/GPU whenever they publicly announce a new in-house model training run. [AMD does not currently do this](https://rocm.blogs.amd.com/artificial-intelligence/introducing-instella-3B/README.html). We have asked AMD repeatedly about their MFU but so far, we have not received a satisfactory answer. This could lead one to assume their MFU is quite low.

  10. In contrast to [Nvidia’s Pyxis solution](https://github.com/NVIDIA/pyxis), first-class support for AMD SLURM for containers is non-existent. AMD’s should invest in [SchedMD (maintainers of SLURM)](https://www.schedmd.com/) consulting to help get containers in AMD SLURM to be on par with NVIDIA.

  11. AMD should open source and make all of their CI/CD and dashboards publicly accessible across all ROCm libraries (HipBLASLt, Sglang, vLLM,TransformerEngine, etc). [Currently, the only publicly accessible ROCm CI for their ML libraries is PyTorch](https://hud.pytorch.org/benchmark/compilers).

  12. Currently AMD has internal clusters on a short-term basis on a burst model. But since demand for compute matches the available supply of compute, that means that there is a lot of development projects and efforts that can’t be carried out. This happens often when engineers are not able to convince capacity gatekeepers to provide burst compute capacity to carry out this research. The roadblock is the fact that there is an effective P&L attached to every GPU hour. The situation at Nvidia is completely different as their internal clusters are persistent and multi-year. This gives Nvidia’s engineers a large degree of freedom to be creative and work on higher risk projects on spare capacity on the cluster without an accountant hovering over them. **AMD has over 5 billion dollars of cash on hand, and has the financial ability to invest more heavily into internal clusters**.

  13. Most of AMD’s internal cluster are rented for sub-1 year basis. This means that their customers will still be using MI300 in 2027 at which point AMD’s internal MI300 volume will be very low given contract expiries, leading to poor long-term support for “vintage” generations of GPUs. AMD should change their internal cluster procurement strategy to commit to multi-year procurement so as to enable long-term support of each GPU generation. **If AMD internal clusters aren’t even committing multiple years to each GPU generation, why should their customers commit to long-term ownership of AMD GPUs?**

  14. AMD’s software infrastructure layer (i.e. Kubernetes, SDC detectors, health checks, SLURM, docker, metrics exporters) has made some progress over the past four months but the rate of progress is much slower than the rate of progress of AMD’s ML libraries. We recommend AMD executives investigate investing more engineering resources into AMD’s AI software infrastructure layer.

  15. Jensen has been donating DGX B200 boxes to academic labs like [Berkeley Sky lab](https://x.com/vllm_project/status/1893001644037566610), [CMU Catalyst Research Group](https://x.com/scsatcmu/status/1912910889566490821?s=46) and [many other university labs](https://x.com/haoailab/status/1914402516420440072). We recommend that AMD also support the academic ecosystem. It is incredibly easy win for AMD marketing to ship boxes and post photos with PhD students grinning next to a shiny AMD box.




## Recommendations to NVIDIA

For the past couple of years, NVIDIA leadership has internally viewed [Huawei](https://semianalysis.com/2025/04/16/huawei-ai-cloudmatrix-384-chinas-answer-to-nvidia-gb200-nvl72/) as the company with the [highest probability of being competitive with NVIDIA](https://semianalysis.com/2025/04/16/huawei-ai-cloudmatrix-384-chinas-answer-to-nvidia-gb200-nvl72/). Due to the rapid improvement and sense of urgency from AMD, we believe that NVIDIA should instead think of AMD as their main competitor as well. We make the following recommendations to Jensen if they want to continue being the market leader:

  1. Continue to rapidly expand the API surface area with useful new features. If NVIDIA expands their API surface area faster than AMD can copy/port to make it ROCm compatible, NVIDIA will continue to be the market leader. Recent launches across the CUDA Python stack was a great example of NVIDIA massively increasing its API surface area with useful new features.

  2. For many developers, working on Nvidia consumer GPUs is a gateway to working on the broader CUDA ecosystem. Unfortunately, due to NVIDIA consumer EULA, PyTorch and most other ML libraries are unable to host consumer NVIDIA GPUs in their CI/CD, leading to a suboptimal experience on NVIDIA GPUs. We recommend that NVIDIA explore a strategy to get NVIDIA consumer GPUs into PyTorch CI/CD.

  3. [NCCL User Buffer Registration](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/bufferreg.html) reduces memory pressure which allows for larger batch sizes and less activation recomputation leading to ~5-10% increase in performance. Although [basic integration with low level PyTorch APIs](https://github.com/pytorch/pytorch/pull/133603) is supported, there is currently no integration into the common APIs such as DistributedDataParallel (DDP), DTensors, or FullySharedDataParallel (FSDP). We recommend that NVIDIA integrates the user buffer registration feature across the whole PyTorch stack.

  4. Although NVIDIA’s out of box experience is better than AMD, there is still room for improvement. [For example, for developer to get optimal performance for RMSNorm, they need to use NVIDIA/apex library instead of having it out of the box in PyTorch](https://github.com/pytorch/pytorch/pull/146388). RMSNorm is an extremely common layer in SOTA LLMs. We recommend NVIDIA work with the Meta PyTorch team on figuring out a strategy to integrate fast RMSNorm kernels and other cuDNN kernels directly into PyTorch.

  5. NVIDIA needs to pay for additional CI H100s so that PyTorch can enable H100 for their [TorchInductor Benchmark CI](https://hud.pytorch.org/benchmark/compilers). Even AMD has enabled already MI300 for this Benchmark CI.

  6. Over the past four months, AMD has done a great job making most of their benchmarks easily reproducible by the community. For example, [AMD wrote a great blog on how to reproduce their MLPerf Inference 5.0 submission](https://rocm.blogs.amd.com/artificial-intelligence/reproducing-amd-mlperf-inference-submission/README.html). If NVIDIA wants the ML community to have confidence in the benchmarks that NVIDIA posts, we recommend that NVIDIA provide reproducible instructions and an explanatory blog post whenever they post benchmark results.

  7. A meaningful number of NVIDIA’s open source libraries are very poor at following the “open source” ethos and do code dumps at every release. Examples include NCCL and CUTLASS. We have seen progress in some open-source libraries such as [trt-llm when they moved towards a Github first approach](https://github.com/NVIDIA/TensorRT-LLM/pull/2980). We recommend that NVIDIA embrace the open-source ethos across all the open libraries.

  8. Stop promoting [marketing Jensen Math 2:4 sparsity FLOPs specifications, curtail the unannounced use of bi-directional bandwidth conventions so as to reduce confusion across the whole ecosystem](https://semianalysis.com/2025/03/19/nvidia-gtc-2025-built-for-reasoning-vera-rubin-kyber-cpo-dynamo-inference-jensen-math-feynman/#jensen-math-changes-every-year). Avoid overstating dense FLOP/s specifications and instead move to publishing a FLOP/s metric that reflects what is achievable for a real-world normal input distribution rather than for an [unrealistic [-4, 4] uniform discrete integer distribution.](https://github.com/NVIDIA/cutlass/blob/main/media/images/cutlass-3.8-blackwell-gemm-peak-performance.svg)

  9. Look into hiring AMD’s engineers that contribute to libraries such as [RCCL](https://github.com/ROCm/rccl/graphs/contributors), [ComposableKernels](https://github.com/ROCm/composable_kernel/graphs/contributors), [hipBLASLt](https://github.com/ROCm/hipBLASLt/graphs/contributors), [ROCm/PyTorch](https://github.com/pytorch/pytorch/pulls?q=is%3Apr+is%3Aopen+%5BROCm%5D), etc. by [looking the contributor tab on Github](https://github.com/ROCm/rccl/graphs/contributors) and searching on the ["[ROCm]" PR tag on Github](https://github.com/pytorch/pytorch/pulls?q=is%3Apr+is%3Aopen+%5BROCm%5D).




## MI325X and MI355X Customer Interest

There has been a [lack of interest from customers in purchasing the MI325X as we've been saying for a year.](https://semianalysis.com/accelerator-industry-model/) It was supposed to be a competitor to H200, but the MI325X started shipment in Q2 2025, about three quarters after the H200 and at the exact same time as Blackwell mass production. The obvious customer choice has been the much lower cost per performance Blackwell and so the release of the MI325X was too little too late and AMD was only able to sell minimal volumes of the MI325.

[Our demand view in the Accelerator Model tracked Microsoft’s disappointment early in 2024 and lack of follow on orders throughout the rest of 2024](https://semianalysis.com/accelerator-industry-model/). We believe that there is renewed interest in AMD GPUs from [OpenAI via Oracle ](https://semianalysis.com/accelerator-industry-model/)and [a few other major customers](https://semianalysis.com/accelerator-industry-model/), but still not Microsoft, on the condition that they reach a sweet-heart pricing with AMD. To be clear, MI355X is still not competitive with NVIDIA’s rack scale GB200 NVL72 solution because the MI355X’s scale-up world size is still only 8 GPUs while for NVIDIA’s GB200 NVL72 the world size is 72 GPUs.

AMD’s pitch on the competitiveness of MI355X centers around the fact that it doesn’t require direct to chip liquid cooling (DLC). There certainly is merit to some point, but there is a degree of irony to the fact that AMD is still pitching the next gen MI355X as a competitor to Nvidia’s last-gen economy-class products. AMD’s MI355X cannot compete head on with NVIDIA’s flagship GB200 NVL72 for frontier reasoning inferencing due to the smaller scale-up world size mentioned above, so it is instead positioned to compete with the air-cooled HGX B200 NVL8 and the air-cooled HGX B300 NVL16.

With that said, [this product segment will ship meaningful volumes](https://semianalysis.com/accelerator-industry-model/) and depending on the MI355X’s software quality and the price that AMD is willing to sell at, the MI355X could be decently competitive on performance per TCO basis when compared to NVIDIA’s HGX. This is particularly true for small to medium models that do not benefit from large scale-up world sizes. However, we believe that GB200 NVL72 will win on performance and perf per TCO when it comes to reasoning models and frontier inferencing that do benefit from large disaggregated deployments or mixture of experts that best harness large scale-up networks.

Below, we will discuss what we see on MI355X, MI420X, MI450X, UALink, Infinity Fabric over Ethernet, and pricing.

### Subscriber Content

## The MI355X Microarchitecture (CDNA4) – SemiAnalysis Estimates

The MI355 microarchitecture (CDNA4) will feature a Hopper SM90 style microarchitecture with Thread Block cluster, Tensor Memory Accelerator (TMA), TMA multicasting, wgmma and async data movements and async mma. We believe that CDNA4’s TMA equivalent will be called ROCm Memory Accelerator (RMA). This will allow CDNA4 to have more efficient data movements compared to CDNA3 but unfortunately picoJoules per bit & picoJoules per FLOP will still be higher than Blackwell’s SM100 uarch. This is due to CDNA4 not having tensor memory, 2 CTA mma, or preferred thread block cluster size.

Like the MI300X and the MI325X, the MI355X also wastes too much silicon area on FP64 cores which are never used in AI. The reason AMD hasn’t been able to bring itself to pare down silicon usage on FP64 cores is that that AMD has historically done well in greybeard High-Performance Computing (HPC) applications that require FP64. The problem is that catering to this now small segment of HPC customers is now holding AMD back from capturing the now far larger AI customer segment that prefers to use number formats such as MX4/6/8, FP4/FP8 or FP16.

NVIDIA is pursuing a different strategy. When moving to Blackwell from Hopper, Nvidia has reduced the number of FP64 tensor cores by 50% and are instead using software emulation with 7-8 INT8 tensor core operations to still achieve decent FP64 performance. This silicon is then re-allocated to tensor cores for MX4 tensor cores which are far more desirable to AI Lab customers. The below table illustrates how cuBLAS FP64 emulation nonetheless delivers meaningful TFLOP improvements for the B200 over the H200 in FP64.

[![](https://substackcdn.com/image/fetch/$s_!W5x1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b68b22d-8f7d-41cb-b10a-a52184edd425_1024x578.png)](https://substackcdn.com/image/fetch/$s_!W5x1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7b68b22d-8f7d-41cb-b10a-a52184edd425_1024x578.png)Source: NVIDIA

This emulation works decently well that we in fact believe that NVIDIA will remove FP64 tensor cores almost entirely in the future and shift to only using software emulation to provide FP64.

## MI400 Series Flexible IO

AMD's learned from their mistake on MI300 with regard to infinity fabric being much worse than NVLink while also recognizing they don't have the hardware talent to actually execute on an NVSwitch equivalent. Furthermore, they don't want to encroach on the industry ecosystem and verticalize. As such they have gone with the shotgun approach of supporting everything under the sun.

In come flexible IO lanes. Instead of having seperate SerDes and IO paths for each different type of IO such as PCIe and Scale Up, AMD has gone with having 144 lanes of IO that can support many different standards. They can support PCIe 6.0, Infinity Fabric at 64G, UALink at 128G, xGMI 4 at 128G which is somewhat of a superset of UALink, and Infinity Fabric over Ethernet at 212G. This enables AMD silicon team to have maximum flexibility for various different use cases.

AMD with this can do scale up UALink or Ethernet. They can do SSDs directly attached to the GPU. They can have Infinity fabric directly connected to GPUs. They can have NICs attached via UALink. The possibilities are almost endless. It is an incredibly large array of permutations for systems and a lot of changes can happen.

As such there are a number of different racks AMD is considering from Torus fabrics with UALink to up to 256 GPU Ethernet based fabrics. We will detail the most likely current racks below, but its over a year from mass production and customers are still discussing their options. This incredible flexibility comes at a cost though.

With different forms of IO, the silicon engineering is not easy. AMD has to make SerDes and data paths that work with all of these different permutations. This is an incredibly hard engineering path fraught with engineering risk.

## MI430X UL4 – SemiAnalysis Estimates

Due to AMD’s accelerated roadmap, we believe that they are skipping MI375X (CDNA4 refresh) and going straight to their CDNA-NEXT generation of chips.

For AMD’s CDNA-NEXT generation of chips, we believe that AMD will release two SKUs - one targeted at FP64 boomer HPC workloads and another targeted at AI workloads that will not have many FP64 tensor cores. They both consist of 2 IO dies, 2 base active interposers, and 4 compute dies 3D stacked.

We believe that MI430X UL4 will be their HPC focused CDNA-NEXT chip. Since this is an HPC focused chip, the MI430X UL4 will have plenty of FP64 tensor cores. Because there will be zero UALink switches available for a while to come, the MI430X will only connect between 4 GPUs in a point-to-point mesh topology hence the “4” in UL4. This is the current limitation of UALink deployments that are available today – in the absence of a UALink switch taped out from Astera Lab, Enfabrica, XConn, or Auradine, UALink can only connect a low number of GPUs together. While they can do torus or mesh topologies, AMD doesn't have the design or software resources to do both hence prioritizing only ethernet for scale up.

The concept of UALink sounds amazing in theory, where there is an open standard for scale up. The unfortunate truth is that for some open standards, progress is very slow due to the numerous amount of committee meetings. Furthermore, AMD does not currently have their own internal UALink switching group which means they must rely on Astera Lab or Broadcom. We believe that from Broadcom perspective, UALink switches will be lower volume than Ethernet switches thus they are not investing enough resources to make the switch come to market quicker.

To be clear, Ultra Ethernet for scale out open standards is going great & will be widely adopted & UEC ready switches are already on market.

[![](https://substackcdn.com/image/fetch/$s_!-pE5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbb389b0f-76e2-40d3-9cc3-80dc3c9e16b1_845x1024.png)](https://substackcdn.com/image/fetch/$s_!-pE5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fbb389b0f-76e2-40d3-9cc3-80dc3c9e16b1_845x1024.png)Source: SemiAnalysis Estimates

There is a possibility from the hardware perspective for MI430X and MI455X to do a larger point to point network with some sort of Torus like Google TPUs, or other topology, but AMD isn't investing the resources to enable that. Previously Alibaba wanted UALink Scale Up, but with the newest bans, we believe this will no longer be prioritized.

In the next section, we will talk about the CDNA-NEXT generation SKU that is targeted for AI workload - MI450X.

## MI450X Infinity Fabric over Ethernet (IFoE) IFoE64 & MI450X IFoE128 – SemiAnalysis Estimates

As we have written about many times, when it comes to AI compute, [systems matter more than chip level performance](https://semianalysis.com/2023/04/12/google-ai-infrastructure-supremacy/).

While ASIC competitors, Nvidia, and even [Huawei](https://semianalysis.com/2025/04/16/huawei-ai-cloudmatrix-384-chinas-answer-to-nvidia-gb200-nvl72/) have offered their AI hardware in rack level scale-up form factor, AMD customers have thus far been stuck with a smaller and thus inferior scale up domain of only 8 accelerators versus the 72 offered for Nvidia to cite one example.

The pressure has been on for AMD to come up with its own rack-scale solution. However, Taiwanese ODMs, namely Quanta and Foxconn, have been focusing most of their engineering resources on supporting Nvidia, particularly with the well-known ongoing issues with GB200 NVL72 racks. Meanwhile, smaller ODMs are also busy as they are very focused on ASIC customers like Google, AWS, and OpenAI.

This leaves very little spare capacity or incentive for ODM partners to develop rack scale solution for AMD. [AMD’s solution to this problem was to acquire ZT Systems, a US based ODM, for $4.9 billion USD in March 2025.](https://www.amd.com/en/newsroom/press-releases/2025-3-31-amd-completes-acquisition-of-zt-systems.html) After the acquisition the engineering team at [ZT will focus completely on developing the rack scale solution for AMD, dropping most of their work on Nvidia systems.](https://x.com/LisaSu/status/1910131191946121533) There are some smaller efforts from Celestica and Lenovo, but primarily it is AMD / ZT.

That said, AMD will not have their rack scale solution ready until the release of the MI450X, which is scheduled to launch in 2H26. This launch comes around the same time as Rubin, which will be offered in the Oberon (NVL144) form factor. In the sections below we will detail the concept of the MI450X rack scale solution and explain why it could be a competitive product to Rubin NVL144 when it launches.

First, we show the compute tray concept:

[![](https://substackcdn.com/image/fetch/$s_!d7ca!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F613334a5-b5d3-4d2f-81ab-4fed545fbed7_1024x743.png)](https://substackcdn.com/image/fetch/$s_!d7ca!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F613334a5-b5d3-4d2f-81ab-4fed545fbed7_1024x743.png)Source: SemiAnalysis Estimates

We believe that four MI450X OAM modules will be socketed onto one compute board for serviceability and repairability. It is a reasonable assumption that there are four MI450X GPUs and one Venice CPUs per compute tray as x86 EPYC CPU is more powerful than Nvidia’s arm-based CPU. Furthermore, x86 CPU enables more seamline software integrations. MI450X’s TDP will be between 1600W and 2000W. Its FLOPS will be competitive to Rubin based going by the expected TDP.

The MI450X GPU will have direct access to three different levels of memory, which indicates that the rack solution will be optimized for inference workloads as the availability of multiple memory tiers enables more efficient KVCaching. It is also interesting to see a direct PCIe channel between GPU and SSD, whereas for the GB200, the GPU still accesses NVMe storage via the Grace CPU. The four tiers of memory:

  1. In-package HBM (288GB/432GB, 18TB/s)

  2. Direct GPU Attached LPDDR5X through custom HBM (819GB/s)

  3. Direct attached PCIe linked SSD

  4. CPU MR DIMM DDR5 over 16 lanes of 64G Infinity Fabric




The Direct GPU attached LPDDR5X is similar to the architecture of Rubin Ultra. The Direct attached PCIe linked SSD similar to NVIDIA HGX’s local NVMe GPUDirect Storage.

The UAlink scale up switch will not be ready by 2H26, hence the scale up protocol of MI450X will be the ethernet based - Infinity Fabric over Ethernet (IFoE) T**he IFoE scale up bandwidth of MI450X is at least 1.8TB/s uni-di = 72 lanes of 200Gbit/s. This will be competitive with Rubin.**

Overall, we believe there will be three different SKUs of the MI450X - each with a different backend network configuration:

  1. Three AMD 800GbE ethernet NICs per GPU (shown in the chart above)

     1. UALink protocol between the GPU and the NIC

     1. 2.4Tbit/s per GPU

     1. The most aggressive SKU in terms of scale out bandwidth.

  2. Two AMD 800GbE ethernet NICs per GPU

     1. UALink protocol between the GPU and the NIC

     1. 1.6Tbit/s per GPU

     1. Less aggressive scale out option.

  3. Two custom PCIe 6.0 800GbE ethernet NICs per GPU

     1. PCIe 6.0 protocol between the GPU and the NIC

     1. 1.6Tbit/s per GPU

     1. Allow the customers to choose non-AMD NIC.




Customers that choose AMD’s NIC will have 1.5x more scale out bandwidth per GPU compared to a non-AMD NIC.

At the compute tray level, we believe that AMD’s solution will be competitive on paper to NVIDIA’s H2 2026 VR200 NVL144 solution. Next, let’s look at the scale-up network and architecture in more detail.

[![](https://substackcdn.com/image/fetch/$s_!QRWO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0bcea4ce-d53c-48d7-819a-f8df6679c405_708x1024.png)](https://substackcdn.com/image/fetch/$s_!QRWO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0bcea4ce-d53c-48d7-819a-f8df6679c405_708x1024.png)Source: SemiAnalysis Estimates

We believe AMD’s MI450X IFoE rack will have switch trays between the compute trays using the ORV3 rack, much like Nvidia’s Oberon platform. There will be 8 compute trays at the top of each rack, 9 switch trays in the middle, and 8 compute trays at the bottom of each rack. The key difference between the AMD IFoE64 rack and the Nvidia GB200 NVL72 is that there are 10 compute trays at the top of Nvidia’s rack while AMD’s will only have 8 compute trays above the switch trays. This brings the total scale up world size for AMD’s MI450x IFoE to 64 GPUs, which is 8 less than Nvidia’s. [We have explained why Nvidia chose to go with 72 scale up world size instead of 64 before.](https://semianalysis.com/2024/08/04/nvidias-blackwell-reworked-shipment/) To recap, 64 is the most efficient scale-up domain size to run AI workloads on but having a set of 8 extra GPUs in the scale up domain allows a degree of flexibility should compute nodes fail while carrying out workloads. The scale up size of the MI450X is not yet finalized, but we still believe customers prefer a 72-GPU scale up domain size.

[![](https://substackcdn.com/image/fetch/$s_!Erjq!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff9d050c7-74e4-4311-a062-2dae7a2d22b7_1024x591.png)](https://substackcdn.com/image/fetch/$s_!Erjq!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff9d050c7-74e4-4311-a062-2dae7a2d22b7_1024x591.png)Source: SemiAnalysis Estimates

The IFoE scale up domain will use an all to all topology. Each switch tray will contain two 51.2T switches, meaning that the aggregate scale up bandwidth of MI450 IFoE64 will be 921.6 Tbit/s of uni-directional bandwidth. For scale-up connectivity, each GPU will utilize 72 lanes of 200G ethernet connecting 18 switches. This works out to 4 lanes of 200G ethernet or 800Gbit/s of uni-directional (uni-di) bandwidth between each GPU and each Switch ASIC. There will be a total of 9,216 DAC cables in the copper backplane, more than Nvidia’s 5,184 DAC cable in the GB200 copper backplane.

[![](https://substackcdn.com/image/fetch/$s_!XaXK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd90cd3de-bc8c-4d55-af6f-3946df69087f_1024x652.png)](https://substackcdn.com/image/fetch/$s_!XaXK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd90cd3de-bc8c-4d55-af6f-3946df69087f_1024x652.png)Source: SemiAnalysis Estimates

Interestingly, we believe that AMD will also launch a more aggressive rack scale architecture of MI450X IFoE128, which basically combines two MI450X IFoE64 racks into one scale up domain. MI450X IFoE128 will have the same 1.8TByte/s scaleup bandwidth per GPU as MI450X IFoE64. While Nvidia has taken a similar approach in joining two physical racks into one scale up domain in its NVL36x2 concept, AMD’s concept utilizes a different cable solution. Nvidia’s attempt of NVL36x2 was short lived and never saw the light of day due to issues with the ACC cables that connect the two NVL36 racks via the front of the rack using the NVSwitch trays. Instead of using ACCs, we believe that AMD will attempt to connect the two racks with DAC cables via a massive copper backplane that spans across two racks.

[![](https://substackcdn.com/image/fetch/$s_!dwsY!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa084c9e-421c-4ae5-bbe3-09abaa51264a_1024x923.png)](https://substackcdn.com/image/fetch/$s_!dwsY!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa084c9e-421c-4ae5-bbe3-09abaa51264a_1024x923.png)Source: SemiAnalysis Estimates

We believe that the DAC backplane approach of AMD provides two advantages over the ACC approach that Nvidia tried with.  
  
First, with Nvidia’s approach, each cross-rack link between GPUs requires two hops. AMD’s DAC backplane solves this problem as all the hops are still one hops.

Second, as the interconnect does not go through the front of the rack, the switch ASICs can be place closer to the backplane connector reducing the distance between each link.

With benefits comes challenges. In order to double the scale up domain from 64 to 128 while maintain 1.8TByte/s per GPU, the uni-di scale up bandwidth between each GPU and each Switch will be halved to be 2 lanes of 212G ethernet SerDes or 400Gbit/s. Cable management would present a significant challenge, as there would even more cables, a total of 18,432 DAC cables with half the cable from each rack going across to the other rack. The longer distance of the cross-rack cables also poses a significant challenge for execution as it becomes harder to maintain signal integrity over longer distances on DAC cables.

Overall, we believe that AMD will make significant progress with rack scale solution post acquisition of ZT System to remain competitive on the hardware level. With the Kyber architecture of Nvidia scheduled to be launched in 2H27, this presents an opportunity for AMD to catch up with Nvidia on rack scale solution in 2H26 against 2H26 Rubin Oberon form factor.

[![](https://substackcdn.com/image/fetch/$s_!dhzI!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe5517317-bd56-4701-8b67-ecc91cb2176c_1024x424.png)](https://substackcdn.com/image/fetch/$s_!dhzI!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe5517317-bd56-4701-8b67-ecc91cb2176c_1024x424.png)Source: SemiAnalysis Estimates, Nvidia

We believe the MI450X IFoE64 architecture will be competitive with 2H 2026’s Rubin Vera NVL144 as they have the same scale up bandwidth per GPU @1.8TByte/s and competitive FLOPs. There is a chance that AMD even one up Nvidia with the MI450X IFoE128 solution which almost doubles the scale up domain of Rubin Vera NVL144.

[![](https://substackcdn.com/image/fetch/$s_!d_tX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F182cc746-78e3-44ae-8662-0205652ff644_1024x346.png)](https://substackcdn.com/image/fetch/$s_!d_tX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F182cc746-78e3-44ae-8662-0205652ff644_1024x346.png)Source: SemiAnalysis Estimates, Nvidia

They have a 256 GPU DAC backplane approach in design too.

## MI300X, MI325X, MI355X Pricing & TCO

As discussed earlier, AMD’s launch timing means that its current generation products have been facing off against Nvidia’s next generation products. We have already observed price cuts in the MI300X into late 2024 as we have gotten closer to the first shipment dates for Blackwell systems. In 2025 thus far, the MI325X has been competing with Nvidia’s Blackwell for customer orders. With AMD’s GPUs seeing less than ideal traction, we see a round of price cuts coming to the MI325X and MI355X in the second half of the year just to stay competitive with the B200 1000W and B300A NVL16. And this is even before we consider how AMD’s current products stack against the GB200 NVL72 and its intimidating inference performance that is enhanced even further with the release of Dynamo.

AMD’s MI300X and MI325X server level cost and total cluster upfront costs are 20-30% lower than Nvidia’s H100 due to lower chip pricing as well as the availability of less expensive Ethernet networking switches and the use of transceivers from vendors other than Nvidia.

[![](https://substackcdn.com/image/fetch/$s_!G0AD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4cec9a11-b035-4c3f-a1d7-1d5912f298c7_1024x580.png)](https://substackcdn.com/image/fetch/$s_!G0AD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4cec9a11-b035-4c3f-a1d7-1d5912f298c7_1024x580.png)Source: SemiAnalysis

Operating costs for AMD’s servers are similar to Nvidia’s servers as they generally have comparable TDPs and most operating costs scale with respect to IT power requirements.

[![](https://substackcdn.com/image/fetch/$s_!gcMX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8fb4214d-9cc6-4105-8b50-2418932ac8c4_1024x556.png)](https://substackcdn.com/image/fetch/$s_!gcMX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8fb4214d-9cc6-4105-8b50-2418932ac8c4_1024x556.png)Source: SemiAnalysis

However, with leading edge GPUs, the Capital Cost generally dominates and so AMD’s total cost of ownership is noticeably below that of Nvidia, with the MI300X coming in at a TCO of $1.37 per hour per GPU vs Nvidia’s H100 at $1.62 per hour per GPU. Note that the below graph is based on theoretical 8 bit FLOP/s and not realistic FLOP/s. [As discussed earlier, AMD as owned to overstate their theoretical FLOP/s](https://rocm.blogs.amd.com/software-tools-optimization/Understanding_Peak_and_Max-Achievable_FLOPS/README.html)

[![](https://substackcdn.com/image/fetch/$s_!DwY9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F24184829-157e-4500-9633-591e7562d40d_1024x375.png)](https://substackcdn.com/image/fetch/$s_!DwY9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F24184829-157e-4500-9633-591e7562d40d_1024x375.png)Source: SemiAnalysis
