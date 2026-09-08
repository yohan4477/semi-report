---
source: https://daily.semidoped.com/p/daily-update-may-11th-2026
title: Daily Update - May 11th, 2026
date: 2026-05-11
kind: clipping
genre: daily
audience: everyone
subtitle: OpenAI-Broadcom, AMD MI350P, Sony image sensors.
---
It’s all about the CEREBRAS IPO this week, and we will definitely cover it on the Semi Doped podcast. Stay tuned!

Updates on OpenAI-Broadcom chip deal, AMD Instinct MI350, and Sony’s ‘fab-lite’ approach to image sensors. Let’s dive in!

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Follow the Semi Doped podcast on[YouTube](https://www.youtube.com/@semidoped), or any podcast streaming platform of your choice. Weekly discussions on semiconductor technology that will keep you sharp and informed!_

* * *

### **OpenAI’s Broadcom chip deal hits financing snag**

[The Information](https://www.theinformation.com/articles/openais-ai-chip-deal-broadcom-hits-18-billion-financing-snag?rc=ij60ts) reported that OpenAI and Broadcom are negotiating an agreement under which Broadcom would finance the first phase of OpenAI’s custom chip program at roughly $18 billion in chip production cost. There’s a catch though. Broadcom will only finance phase 1 if Microsoft commits to buying roughly 40% of the chips, which Microsoft would install in its data centers and rent back to OpenAI; Microsoft has not committed. According to The Information, an internal OpenAI memo characterized “the persistent programmatic risk” as “that Microsoft does not ultimately come through”. 

> _**Austin:** The custom silicon caught my eye, but actually this is a credit story. Broadcom isn’t refusing to build the chips, but Hock is refusing to be the bag-holder. He wants Satya on the hook because Microsoft is extremely credit worth (AAA-rated), whereas OpenAI is a private company burning money._
> 
> _The problem is that the Microsoft-OpenAI relationship has cooled. Satya isn’t incentivized to say yes to everything Sam asks for anymore, and the recent restructuring ended Microsoft’s revenue-share payments to OpenAI. There’s also an infrastructure impedance mismatch of sorts; OpenAI wants data centers purpose-built for its custom silicon, Microsoft only wants silicon that fits into the broader Azure portfolio. Backstopping $7B+ of chips that go into bespoke facilities is exactly the kind of CapEx Satya has been publicly against._
> 
> _Hock can hold the line because he doesn’t need this deal. On the last earnings call he was explicit that OpenAI is Broadcom’s sixth and newest XPU customer; so not its largest or most critical. Google’s Ironwood ramp and the other strategic accounts carry the $100B Broadcom 2027 AI revenue story without the OAI deal (“Project Nexus”)._
> 
> _The fix is OpenAI’s upcoming IPO. A $50–100B equity raise is the headline, but the more important unlock is access to investment-grade and convertible debt markets. These instruments can directly finance custom silicon buildouts. That graduates OpenAI from begger to chooser; less time begging hyperscalers to underwrite the roadmap, more control over its own destiny. It’s also better for Broadcom too. A public OpenAI with audited financials and capital-markets access is a far more legitimate counterparty than the current cash-burning private company._
> 
> _The problem, of course, is timing. Project Nexus Phase 1 needs to be financed now, not in 2027. So either Microsoft foots the bill (seems unlikely), OpenAI finds alternate buyers (Broadcom has reportedly floated this as an option), or the project slips while OpenAI’s credit profile catches up to its compute ambitions. Maybe the latter?_

### **AMD ships Instinct MI350P, the only current-gen server-grade AI PCIe card on the market**

AMD launched the [Instinct MI350P](https://www.amd.com/en/products/accelerators/instinct/mi350/mi350p.html), its first Instinct PCIe card since the 2022 MI210, bringing CDNA 4 to a 600W FHFL dual-slot board. 

[](https://substackcdn.com/image/fetch/$s_!juUs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe5a6aa78-e54a-47c9-9754-4ed550027803_1200x675.jpeg)

The chip is purpose-built rather than salvaged from MI350X silicon: a single I/O die with four XCDs (half the MI350X’s compute), 144GB HBM3E, 4TB/sec memory bandwidth, and 2.3 PFLOPS at MXFP8. AMD offers an optional 450W TBP mode for older racks that can’t handle the full PCIe CEM 600W. Up to eight cards fit in a single server tray. The biggest tradeoff versus the modular MI350X is that AMD does not expose Infinity Fabric on the card, so multi-card scale-up runs over PCIe Gen5 x16 only — per [ServeTheHome](https://www.servethehome.com/amd-intros-instinct-mi350p-accelerator-cdna-4-comes-to-pcie-cards/), “an 8-card setup is a better fit for running 8 models than it is for one large model spread over 8 GPUs.” AMD also published both peak and delivered performance figures, which ServeTheHome called “welcome” disclosure. Strategic context: NVIDIA has no current-gen PCIe server GPU and has signaled none is coming, leaving AMD as the sole vendor offering current-generation server-grade accelerators in PCIe form factor.

### **Sony takes steps toward becoming “fab-light”**

Per [Bloomberg](https://www.bloomberg.com/news/articles/2026-05-08/tsmc-and-sony-to-form-joint-venture-on-image-sensors), Sony and TSMC announced a Kumamoto-based image sensor joint venture that Sony CEO Hiroki Totoki framed as the company’s pivot to a fab-light model on Friday’s post-earnings call: “The joint venture with TSMC will be our first step to becoming fab-light. Until now, we have handled everything in-house, from R&D to manufacturing, but going forward, we hope to advance manufacturing not only on our own but also by bringing in partners.” 

> _**Vik** : TSMC’s CMOS image sensor business has been around for >20 years, and so its not just leading edge silicon and advanced packaging with them. This business accounts for a small fraction of revenue, but they still do it. In comparison, they stopped doing GaN last year. Wonder if that’s a wise move for the future of power semis._

### Quick Hits

  * **AI-driven semiconductor demand** surge fuels divergent economic growth dynamics in Korea and Taiwan, lifting regional market valuations. ([Bloomberg Tech](https://www.bloomberg.com/news/articles/2026-05-11/goldman-sees-rates-pressure-as-ai-fuels-k-shaped-korea-taiwan))

  * **Arista Networks** disclosed an $8.9 billion inventory pile-up that has unsettled investors despite the company posting record quarterly results. ([AD HOC NEWS](https://www.ad-hoc-news.de/boerse/news/ueberblick/arista-networks-8-9-billion-procurement-pile-up-spooks-investors-despite/69302260))

  * **Lumentum Holdings** , a supplier of optical modules and photonics components, has been added to the Nasdaq-100 Index.

  * **nLIGHT** reported first-quarter earnings and revenue that both exceeded Wall Street expectations, driven by unusually strong demand from its defense customer base. [LASR 0.00%↑](https://substack.com/search/%24LASR)

  * **Cyient Semiconductors** Launches India’s First GaN Power IC Family Leveraging Navitas Technology ([PRS newswire](https://www.prnewswire.com/in/news-releases/cyient-semiconductors-launches-indias-first-gan-power-ic-family-leveraging-navitas-technology-302768122.html))




### Key Data

[Wall St Engine@wallstengineCEREBRAS UPSIZES IPO TO $4.8B AFTER 20X DEMAND $CRBS filed to sell 30M shares at $150-$160 each, up from 28M shares at $115-$125. At the top of the new range, the AI chipmaker would raise roughly $4.8B, compared with $3.5B under the prior terms. Reuters says the IPO drew 12:26 PM · May 11, 2026 · 69.2K Views

* * *

17 Replies · 49 Reposts · 296 Likes](https://x.com/wallstengine/status/2053813969039822855?s=20)

### Etcetera

  * **Nvidia** CEO Jensen Huang delivers keynote commencement address outlining career opportunities emerging from AI infrastructure revolution. ([Nvidia News](https://blogs.nvidia.com/blog/your-career-starts-at-the-beginning-of-the-ai-revolution-nvidia-ceo-tells-graduates/))

  * **Samsung** faces substantial $15 million lawsuit from music artist Dua Lipa alleging product defect in television device. ([The Korea Herald](https://news.google.com/rss/articles/CBMiV0FVX3lxTE45emdSMDY2YTRmMFIzSlA1TUh2bWFtVXlVaHd1UUo1bVprUEZWUnhuMk9keEZnY3NzS0tiOUVkbUdXbUhvYWlrNzl5RkxlaS1JN2puaE5rRQ?oc=5))




Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-may-11th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
