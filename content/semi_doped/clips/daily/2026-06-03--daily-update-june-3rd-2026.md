---
source: https://daily.semidoped.com/p/daily-update-june-3rd-2026
title: Daily Update - June 3rd, 2026
date: 2026-06-03
kind: clipping
genre: daily
audience: everyone
subtitle: Nvidia opens the rack to photons, crams a petaflop into a laptop, and Alphabet passes the $80B hat.
---
Big day for the photons. Nvidia cracks NVLink Fusion open to Lightmatter and Ayar Labs, optical names rip, and Jensen reminds everyone that copper still has a job for as long as we can imagine. Microsoft and Nvidia stuff a petaflop into a thin-and-light and call it RTX Spark. And Alphabet passes the hat for $80 billion with Berkshire chipping in. Plus: Chinese NAND closes the gap, CoreWeave taps the junk market, and Astera plants a bigger flag in Taiwan. Let’s dig in. 👇

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

* * *

## **Nvidia opens NVLink Fusion to photonics partners**

Nvidia announced at GTC Taipei 2026 that its NVLink Fusion ecosystem will extend to photonic interconnects, with Lightmatter and Ayar Labs joining as co-packaged optics partners. Lightmatter is contributing its Passage photonic interconnects and Guide laser sources, while Ayar Labs is making its CPO products optically and electrically compatible with Nvidia’s optical and SerDes technologies for rack-scale AI infrastructure. ([Ayar](https://ayarlabs.com/news/ayar-labs-joins-nvidia-nvlink-fusion-ecosystem-to-bring-co-packaged-optics-to-rack-scale-ai-infrastructure/), [Lightmatter](https://lightmatter.co/blog/scale-up-is-a-problem-made-for-photonics/)) 

Shares of optical suppliers Lumentum, Coherent, and Corning rose sharply following CEO Jensen Huang’s remarks:

> _**Jensen:** We should use copper as much as we can, for as long as we can, but copper has its limits. The right strategy is to scale up with copper as long as you can. After that you scale up further with optics, you scale out with optics and you scale across with optics. So you use optics wherever you must, you use copper wherever you can._

My take:

> _**Austin:**_ _Nothing new was said. A near-term interpretation of Jensen’s comments: scale-up inside the rack using copper, extended scale up between neighbor racks using optics, scale out and across with optics. Where the scale up TAM truly grows for optical names is when scale up inside the same rack moves optical. That will come, but not nearly as soon as the rhetoric makes it seem.[Read more about timing here](https://www.chipstrat.com/p/inside-the-800g-16t-32t-race). _

## Windows laptop with beefy GPU

Microsoft and Nvidia introduced RTX Spark, an Nvidia processor for thin-and-light Windows PCs with 1 petaflop of AI performance, up to 6,144 Blackwell RTX cores, up to 20 Arm CPU cores, and up to 128GB of unified memory. The pitch is the on-device agents: 128GB of unified memory runs frontier-class models and agent tools locally (GitHub Copilot, Claude Code, Cursor, ComfyUI, TensorRT), with a new Windows OpenShell runtime to sandbox them. Beyond the laptop, the two scaled Windows to the DGX Station deskside box (GB300 Grace Blackwell Ultra, 748GB coherent memory, 20 petaflops FP4, trillion-parameter models), due later in 2026. First laptops to ship this fall include the Surface Laptop Ultra, ASUS ProArt P16, Dell XPS 16 Creator Edition, HP OmniBook, Lenovo Yoga Pro 9n, and MSI Prestige. ([Microsoft Build](https://blogs.nvidia.com/blog/microsoft-build-windows-local-cloud-devices/), [Windows](https://blogs.windows.com/windowsexperience/2026/05/31/introducing-a-powerful-new-chapter-for-windows-pcs-accelerated-by-nvidia-rtx-spark/)). 

> _**Austin:** I’m actively migrating some of my own workloads to my local token generator, a Framework AMD Ryzen Max+ 395. It’s my always-on agent computer on my desk. Note that it has 128 GB of memory too, which is actually enough in my experience for many of my simple agentic tasks. Sure, there’s a cap to context length and token generation speed. But I have a lot of background tasks where that’s just fine. The memory and compute won’t be the barrier to local agentic AI imo, rather the user experience and consumer awareness will be. That’s where Microsoft has a big opportunity to help. _

## Alphabet wants $80 billion

**Alphabet** is raising $80 billion in equity to fund AI compute: about $30 billion underwritten, $40 billion via an at-the-market program, and a $10 billion private placement from Berkshire Hathaway. The reaction was muted, down about 2% premarket, partly because nearly 40% of the raise is earmarked for employee equity-tax obligations rather than direct capex. ([WSJ](https://www.wsj.com/tech/ai/google-seeks-to-raise-80-billion-for-ai-infrastructure-05a379be))

> _**Austin:**_ _Ben Thompson has a good read on this here:[The Google Capital Company](https://stratechery.com/2026/the-google-capital-company/)_

### Quick Hits

**Semicap**

  * **Koh Young Technology** said its semiconductor packaging inspection equipment sales jumped 79%, driven by surging demand from AI server packaging programs. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=10969))




**Storage**

  * **Chinese NAND makers** have reached market share comparable to Micron and SanDisk, narrowing the gap with traditional incumbents, per market data shared by analysts. ([@jukan05)](https://x.com/jukan05/status/2062014627521986600)

  * **Sandisk** announced a plan to shield budget consumers from the broad memory price surge by offering value-tier storage products despite rising NAND and DRAM costs. ([bgr.com](https://news.google.com/rss/articles/CBMicEFVX3lxTFBKSG5MaE5QTXktNmQtV1BJZFVLUTVIRFRzRG5ncUZCNzNUZkw2RHQzSXExa1c4cWcwVHFWQnlPWjdWcnAzUlBYaWQ2aWZKejJxZDVoRXFmdF9TNEU0WmMzS29NWTVQLVRQd2hmVUJIWWQ?oc=5))




**Infrastructure**

  * A **CoreWeave** -tied data center entity raised $900 million via a junk-bond sale, adding to financing stacks supporting continued GPU-cloud capacity expansion. ([Bloomberg.com](https://news.google.com/rss/articles/CBMitAFBVV95cUxPZ29yLUFkOTdlcEMxUFVnWjJqZGtlRHFwMmkzejhhMGp3MjdIVUxweEV0UFNkbnhSWkhfMExPZ0xDZ2ZpX0g1U2ttRUlTMFRFRFpxQ3BUaFkzRnlnRGZ4YjMzR1FmbEdBMkNvb3YySmp0V2JEUmNuUks1bHBDd01QRU5YX2Uwdm9KTmpLRU5zR0ZCOWtZclRuOFJnSERmQUN2WmlLYkhqYWxZNHEwcHhkOW53OW4?oc=5))




**Networking**

  * **Astera Labs** is expanding its Taiwan operations to accelerate global AI infrastructure buildout, deepening its presence in the island’s hardware design and supply ecosystem. ([GlobeNewswire](https://news.google.com/rss/articles/CBMi7gFBVV95cUxQc2pqZDlzX1NrZnBnd2FmMi1Jb05ZRTc1aDhFbUhhcmJweFNXUlZSS05qR2tqYjBybURlTk1kS1ozamFueUE2YkpycFR0eWxLZEdORTNicEF1Z1lYeEpQczAxc1NSMUFfRmttdEVQRkZSa1NhMlBsbkVuSWF6U0ZxSW9pV2xvc0JIVDNXRjFrQzVLVWNxMzZhTHlCanFHNUt2VlFTWVprNjZ3TzBfWHhwdUt4RGtrUVB3ckRQaDg5bHJRNTExSHBhTE5rTnJHRHhEQWQ2SkNXVV9YTS04ZGFjOEFoV1lOdXMzQVlsNUdR?oc=5), [Stock Titan](https://news.google.com/rss/articles/CBMitwFBVV95cUxOc0JiTURPQ0t0OTBQbHA1eVhNUTRsRGtTVjNrX3FXQmVQaC1nOEJxZUkwQWZsbGdCY3NfVU5ZTm5vOHFURW9pWEtWMlVQUTNjRXU0bDhJdU9VamZqMDlFQkNOTXA3SjdrWVBRWENnaDVLSFUzVkJFeEttbHZhX081aVBuQXFIQ0pxNWxiSm80MzlfUmVXVWFFbm1oRUZFUFNXVjl2WjdfaUlXVk1zZTlQaThsZVRuYVU?oc=5))




### Cool Stuff

Fourty minute video from TechInsights on 18A, per [Alex_Intel_](https://open.substack.com/users/264958805-alex_intel_?utm_source=mentions) on X.

[](https://substackcdn.com/image/fetch/$s_!BPYF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe60c4760-2832-4280-871c-bfaf113cfd1d_1206x1174.png)[Source](https://x.com/alex_intel_/status/2062258748929061254?s=51)

That’s it for today. Austin’s on his way home from Computex; flight through Toyko was cancelled due to Typhoon Jangmi, hope our Japanese friends are all doing ok!

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-june-3rd-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
