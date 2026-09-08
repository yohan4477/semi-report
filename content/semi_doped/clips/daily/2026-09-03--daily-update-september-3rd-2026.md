---
source: https://daily.semidoped.com/p/daily-update-september-3rd-2026
title: Daily Update - September 3rd, 2026
date: 2026-09-03
kind: clipping
genre: daily
audience: everyone
subtitle: Nvidia acquires Hugging Face for $12.93B, Broadcom targets $30/share by FY2028, TSMC defers hybrid bonding HBM CapEx, Phison warns 2027 NAND shortage worst ever.
---
**Hello world, it’s Thursday, September 3rd.**

Nvidia is acquiring Hugging Face for $12.93 billion, with Jensen Huang framing the deal as a move to scale the platform’s infrastructure and expand developer access to AI. Broadcom is forecasting a surge in AI chip sales and now expects to top $30 a share in earnings by fiscal 2028, while TSMC is holding off on hybrid bonding CapEx for HBM and Samsung is pushing into vertically stacked memory architectures.

Let’s get into it. _— Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

_Tell us how to make Semi Doped better![ Give us your feedback](http://semidoped.com/poll)! ❤️_

### Nvidia Acquires Hugging Face for $12.93 Billion, Retention Package Included

[Nvidia confirmed it will acquire Hugging Face](https://blogs.nvidia.com/blog/nvidia-to-acquire-hugging-face/) for $12,930,300,000, with Jensen Huang framing the deal as a move to scale the platform’s infrastructure and expand developer access to AI. Bloomberg reports the transaction includes up to $1 billion in equity-based retention for Hugging Face employees who join Nvidia, on top of the roughly $13 billion headline price. The figure is a step down from the $14 billion Bloomberg had cited when reporting advanced talks earlier this year. Hugging Face co-founders Clément Delangre, Julien Chaumond, and Thomas Wolf built the platform into the dominant hub for open model sharing, a position that now sits inside Nvidia’s stack. The deal is subject to regulatory review.

> _**Austin:** Nvidia is buying access to developers while ensuring open model distribution. The former reminds me of Microsoft buying Github. _
> 
> _**Vik:** Definitely Microsoft+Github vibes here. Open models means that more people have something they can tinker with, and it will eventually need compute — which feeds into NVIDIA. This feels like a good move to foster this developer ecosystem._

### Broadcom’s AI Chip Forecast Clouds Over Google Defection Fears

Broadcom [predicted a surge in AI chip sales over the next two years](https://theedgemalaysia.com/node/816660), telling investors the company is on track to top $30 a share in earnings by fiscal 2028, ahead of Wall Street estimates, according to Bloomberg Intelligence analyst Matt Bloxham. The stock fell anyway. Google’s reported shift toward fully in-house TPU silicon, including a fourfold acceleration in TPU rollout cadence, has investors questioning how much of Broadcom’s AI revenue depends on a single hyperscaler relationship that may be shrinking. Broadcom’s custom ASIC business counts Google among its most significant partners, making the concentration risk harder to dismiss against an otherwise [bullish two-year forecast](https://www.bloomberg.com/news/videos/2026-09-03/broadcom-forecasts-boom-in-ai-chip-sales-video).

> _**Austin:** Hock says his XPUs less than half the cost per GW as an Nvidia GPU, and are more performant for the LLM workloads they are designed for. That explains the wild forecast of “$115 billion of chips to these guys in fiscal 2027, another $230 billion in 2028”. Second-sourcing and CoT are price negotiations; no one in the race to deploy inference compute is walking away from Broadcom._
> 
> _**Vik:** Never bet against Hock on maximizing shareholder value! But yeah, Google’s massive TPU, part of which is being eaten by MediaTek, is giving investors the jitters. OpenAI’s Jalapeno’s quick turnaround is actually testament to Broadcom’s ASIC design prowess, come to think of it. Still not betting against Hock._

### TSMC Holds at Microbumps for HBM, Deferring Hybrid Bonding CapEx

TSMC [currently sits at 6-micron hybrid bonding pitch](https://www.tomshardware.com/tech-industry/semiconductors/hybrid-bonding-roadmap-examined) for its advanced packaging work, and the company has decided against committing capital to hybrid bonding for HBM production in the near term, sticking instead with microbump interconnects while yield on the newer approach matures. The pause hands Samsung and SK Hynix a window to push hybrid bonding into HBM roadmaps first, a reversal of the sequence most of the industry had assumed. Yield concerns are real: hybrid bonding at scale demands defect rates that microbumps, however unglamorous, already deliver reliably. Pressure arrives from another direction too, as [Intel’s EMIB-T is gaining traction as a CoWoS alternative](https://www.chosun.com/english/industry-en/2026/09/03/6NI4ACJCABBTTDJ45DF35PYWLM/), putting TSMC’s advanced-packaging revenue under scrutiny from customers with options.

> _**Vik:** I am bearish hybrid bonding at least for HBM applications. High stacks are too expensive, and hardware makers won’t bite into it. They will find other ways to work around the need for high capacity HBM. Bandwidth is more important! I wrote about this on [Vik’s Newsletter](https://www.viksnewsletter.com/p/how-custom-base-die-drives-hbm-bandwidth?r=89umme&utm_campaign=post&utm_medium=web) this week._

### Samsung Pushes HBM Into Vertical Territory With New Stacked Architecture

At the center of Samsung’s disclosure is an architecture that vertically stacks memory and computing devices to sharply increase capacity within the same footprint while cutting data-transfer distances. The move targets what Samsung frames as fundamental limits on planar memory scaling in the AI era, with [3D-stacked HBM](https://www.thelec.net/news/articleView.html?idxno=13541) positioned as the path forward beyond current generation designs. Vertical integration depth, rather than spreading transistors across a wider die, becomes the primary lever for density gains. Samsung hasn’t named a specific product generation or ship date, but the disclosure itself is a public staking of ground in a market where SK Hynix currently holds the lead on advanced HBM supply to major AI customers.

> _**Vik:** I do like the idea of zHBM inherently. Stacking DRAM on top of logic is … logical, but hard to do because of thermal issues. Samsung is saying HBM5 will use hybrid bonding though. My feeling is that its going to be a while._

### Phison Warns 2027 NAND Shortage Worst Ever as SK Courts Kioxia

Phison Electronics [told Bloomberg](https://www.bloomberg.com/news/videos/2026-09-02/phison-electronics-sees-worst-nand-shortage-in-2027-video) that 2027 will bring the worst NAND shortage the industry has yet seen, a forecast that gives SK Group Chairman Chey Tae-won’s courtship of Kioxia some urgency. Chey, in a September 2 interview with Japan’s Asahi Shimbun, [called joint production with Kioxia “one option”](https://www.thelec.net/news/articleView.html?idxno=13593), adding that the Japanese chipmaker “has many strengths.” He has also said a decision on an overseas plant, likely in Japan, could come this year. Kioxia is separately planning a new Japanese fab to serve AI memory demand, though how that interacts with any SK tie-up remains unsettled. The existing Kioxia-SanDisk combination, valued at roughly $31 billion, doesn’t resolve the timeline.

> _**Vik:** The worst NAND shortage in 2027?! The Phison CEO has been saying this for a while actually. For a guy building memory controllers, the messaging seems bearish, to be honest. We will wait and see!_

### Sector Watch

#### Data Centers

  * **Dell** lifts its annual sales forecast by $25 billion for the fifth straight quarter on sustained AI and traditional server demand. ([Bloomberg Tech](https://www.bloomberg.com/news/videos/2026-09-02/dell-rises-on-sales-outlook-boost-video))

  * **ByteDance** secures a $29.6 billion loan — Asia’s second-largest this year — and plans to expand its AI data center cluster in Inner Mongolia to sustain compute buildout. ([Bloomberg Tech](https://www.bloomberg.com/news/articles/2026-09-03/bytedance-gets-30-billion-loan-asia-s-second-largest-this-year))

  * **Fluidstack** reaches an $18 billion valuation building AI compute infrastructure for Google and Anthropic, emerging as a major hyperscaler supply-chain partner. ([Forbes](https://www.forbes.com/sites/iainmartin/2026/09/03/a-tiny-startup-helping-google-take-on-nvidia-is-now-worth-18-billion/))




#### Foundry & Packaging

  * **Simmtech** plans a 400 billion won capacity expansion targeting AI package substrates, responding to accelerating advanced-packaging demand from TSMC and OSAT customers. ([thelec.net](https://www.thelec.net/news/articleView.html?idxno=13591))

  * **Hanmi Semiconductor** unveils new 2.5D AI chip packaging equipment at SEMICON Taiwan 2026, targeting advanced heterogeneous integration assembly for next-generation AI processors. ([mbiz.heraldcorp.com](https://mbiz.heraldcorp.com/article/10860306))

  * **Onto Innovation** unveils the Dragonfly G5 advanced-packaging inspection system at SEMICON Taiwan 2026, extending its metrology portfolio for heterogeneous integration. ([Yahoo! Finance Canada](https://ca.finance.yahoo.com/news/onto-innovation-onto-unveiled-dragonfly-150737061.html))




#### Power

  * **Hitachi** and **Bloom Energy** announce a collaboration to deploy on-site fuel-cell power solutions in Japan, addressing grid constraints at AI data center campuses. ([ESG News](https://esgnews.com/hitachi-bloom-energy-target-japans-data-center-power-gap/))

  * **LS Cable & System** targets AI data center power delivery with superconductor cable technology, expanding its infrastructure business for hyperscale campuses. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13537))

  * **Gaon Cable** , an LS Cable subsidiary, extends its low-friction power distribution cables into AI data center deployments, broadening use beyond industrial facilities. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13555))




#### Compute & Edge

  * **Qualcomm** unveils Dragonwing Q-2390 and IQ-2390 processors, new infrastructure-grade chips expanding its portfolio beyond mobile into network and industrial AI applications. ([thelec.net](https://www.thelec.net/news/articleView.html?idxno=13559))

  * **RISC-V** RVA23 is confirmed as the new industry standard at Hot Chips 2026, with broad silicon and software ecosystem uptake across compute tiers. ([ServeTheHome](https://www.servethehome.com/update-on-risc-v-standards-and-adoption-at-hot-chips-2026/))

  * **Microchip Technology** and **Marelli** announce an open-standard display connectivity solution for software-defined vehicles, enabling multi-display architectures without proprietary interface lock-in. ([Microchip](https://ir.microchip.com/news-events/press-releases/detail/1412/microchip-and-marelli-pioneer-open-standard-display-connectivity-solution-for-software-defined-vehicles))




#### Optics & Networking

  * **Ericsson** demonstrates AI-RAN and Integrated Sensing and Communication at its Korea Innovation Day 2026, showcasing 6G base-station drone-detection as a commercial-path capability. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13551))

  * **Qualcomm** executives say 6G will directly intersect with AI inference and sensing use cases, positioning the next standard beyond pure connectivity. ([Light Reading](https://www.lightreading.com/6g/6g-and-ai-are-on-a-collision-course))

  * **Nokia** signs a commercial deal with BeeHealthy to integrate its Network as Code APIs into digital healthcare verification services. ([Nokia](https://www.nokia.com/newsroom/nokia-and-beehealthy-bring-network-based-verification-to-digital-healthcare/))




#### Policy & Trade

  * **Korea Science Ministry** sets a 9.4 trillion won AI budget for 2027, with roughly half earmarked for compute infrastructure, marking a major step-up in state AI investment. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=13544))

  * **China** releases a new private 5G industrial deployment plan but omits spectrum allocation, leaving the initiative short of regulatory clarity needed to proceed. ([Light Reading](https://www.lightreading.com/private-networks/china-makes-another-run-at-deregulating-private-5g))

  * **US export controls** have concentrated China’s tech IPO pipeline in semiconductor and AI chokepoint sectors as companies prioritize areas Beijing is racing to indigenize. ([SCMP](https://www.scmp.com/tech/tech-trends/article/3366164/us-export-curbs-have-reshaped-chinas-tech-scene-around-chokepoints-report?utm_source=rss_feed))




_Tell us how to make Semi Doped better![ Give us your feedback](http://semidoped.com/poll)! ❤️_

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-september-3rd-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
