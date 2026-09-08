---
source: https://daily.semidoped.com/p/daily-update-june-18th-2026
title: Daily Update - June 18th, 2026
date: 2026-06-18
kind: clipping
genre: daily
audience: everyone
subtitle: SML on Terafab, NOR/SLC prices double, HBM4E samples out, Samsung absorbs TSMC overflow, and Broadcom's AI upside case gets bigger.
---
Another day, another example of the AI buildout pressuring every layer of the supply chain. ASML’s CEO says Terafab would be the ultimate test; meanwhile, NOR Flash and SLC NAND are already up 100%+ as suppliers chase HBM and advanced NAND instead. SK Hynix is shipping fast 12-layer HBM4E samples, Samsung is taking TSMC overflow orders from Google and AMD, and Broadcom’s AI revenue could triple by FY28 if Anthropic’s financing comes together. 

Plus: why the Mythos shutdown is another data point for owning your models, not renting them.

Let’s get into it. _—Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

* * *

### ASML CEO Calls Terafab Supply-Chain Test

ASML CEO Christophe Fouquet said Elon Musk’s proposed “Terafab” semiconductor project would be a test for the industry’s supply lines, in comments to Bloomberg. The Dutch lithography maker is the sole supplier of EUV scanners required for leading-edge chip production, and a fab targeting wafer volumes an order of magnitude above today’s largest facilities would strain tool output, materials, and skilled labor. Separately, ASML shares rose as analysts pointed to EUV capacity expansion and the company’s installed-base service revenue as drivers beyond near-term AI capex. ([Bloomberg Tech](https://www.bloomberg.com/news/articles/2026-06-17/asml-ceo-warns-of-possible-supply-constraints-on-musk-s-terafab))

> _**Vik:** If Terafab comes online, we ain’t seen nothin’ yet regarding supply chain shortages. Big boost for Semicap names would ensue though!_

* * *

### NOR Flash, SLC NAND Prices Surge Over 100% in 1H26

NOR Flash and SLC NAND contract prices increased over 100% in the first half of 2026, according to TrendForce. This surge is attributed to major memory suppliers prioritizing higher-value products like HBM and advanced-layer 3D NAND, which has constrained mature-node capacity for NOR Flash and SLC NAND. TrendForce projects continued price increases in 2H26, with high-density NOR Flash potentially rising 60–65% and SLC NAND 70–75%, due to sustained demand from automotive, industrial, and AI applications amid limited capacity expansion. ([trendforce.com](https://www.trendforce.com/presscenter/news/20260616-13102.html))

> _**Vik:** Kioxia for example phased out SLC NAND in favor of higher density options like TLC/QLC. But there is still demand for SLC, especially because it has lower latency which is useful for KV cache applications. Now limited capacity = higher prices. Go figure._
> 
> _**Austin:** Supply mix changes to chase AI, and then “legacy” product has supply tightness and price increases too. Super interesting. _

### Companies must own intelligence, not rent it, for business control

The shutdown of Mythos highlights the risk of building a business on intelligence not directly controlled by the company. While frontier APIs offer powerful capabilities, relying on them exposes companies to external decisions, such as price changes or platform access revocation. Companies can achieve control by starting with open models, post-training them on proprietary data and workflows, and relentlessly evaluating them against frontier models. ([lqiao](https://x.com/lqiao/status/2066403957824688462))

> _**Vik:** Is the Fable/Mythos saga the final tipping point for edge AI? “Right-sized-intelligence” that does one task well but runs on company premises is much more logical for companies to deploy._
> 
> _**Austin:** Yet another reason to buy vs rent... I think at a minimum it makes the argument for having control over your own models, even if you deploy on cloud infra. But might as well use your own token generators if possible_

### SK hynix ships 12-layer HBM4E samples

SK hynix said Thursday it has shipped 12-layer HBM4E samples to major customers, an Nvidia supplier moving its next-generation high-bandwidth memory toward qualification. The Seoul-based company said the chips reach a maximum speed of 16 Gbps per pin and use its Advanced MR-MUF packaging process, which it said reduces heat resistance by 17% while improving stability. SK hynix did not name the recipients of the samples. ([SK Hynix](https://news.skhynix.com/12-layer-hbm4e-sample/))

> _**Vik:** 12 hi stack, 48 GB, with 16 Gbps per pin on TSMC 3nm for base die. Leading edge for base die really kicks up pin speeds a notch!_
> 
> _**Austin:** How much of the speed gains are due to the 3nm node process? If that’s the major contributor, seems like every memory company will follow suit. Crazy how far past JEDEC spec things are getting. Wonder what memory controller IP Hynix uses here._

### Samsung Gains Chip Orders as AI Strains TSMC Capacity

BYD, Google, and AMD are increasingly seeking contract chipmaking services from Samsung Electronics. This shift is occurring as surging demand for AI infrastructure strains the advanced chipmaking capacity of market leader TSMC. ([asia.nikkei.com](https://asia.nikkei.com/business/tech/semiconductors/samsung-sees-rising-chip-production-requests-from-byd-google-amd-sources))

> _**Vik:** Many folks were of the opinion around TSMC’s $56B capex spend that it was not enough, but then capacity takes years to come online. TMSC’s conservatism might be their own Achilles heel in the time of exponential growth. It’s quite natural for chip makers to turn to other alternatives if they the yield/performance exists._

### Aehr secures follow-on order for AI data center optical interconnect

Aehr Test Systems received a follow-on production order for a fully automated FOX-XP wafer-level burn-in (WLBI) system. This system, configured to test nine wafers in parallel, includes a WaferPak Auto Aligner and FOX WaferPak Contactors, with delivery expected within six months. The customer, a global leader in networking products, plans to use the system for advanced silicon photonics-based transceivers for hyperscale AI and cloud data centers. ([aehr.com](https://www.aehr.com/2026/06/aehr-receives-follow-on-order-from-major-silicon-photonics-customer-for-fully-automated-wafer-level-burn-in-system-for-hyperscale-data-center-optical-interconnect/))

> _**Vik:** Any guesses who this “customer” is? This is a “follow on” order mind you — [the first one was in April](https://www.aehr.com/2026/04/aehr-receives-record-41-million-production-order-from-lead-hyperscale-ai-customer-second-half-bookings-exceed-92-million/) for $41M. I’ll just say Broadcom. If you disagree, leave a comment below._

### Broadcom’s AI Revenue Could Triple by FY28 with Anthropic Financing

Broadcom’s AI XPU volume could triple to 15GW by FY28, driving $250-300 billion in FY28 XPU revenue, if the Apollo/Blackstone XPV financing vehicle for Anthropic’s FY26 Broadcom purchases is fully funded. Wolfe Research stated that if full XPV financing comes together, FY27 guidance will no longer be a concern. Bullish views on [AVGO 0.00%↑](https://substack.com/search/%24AVGO) ([@ScroogeCap](https://x.com/ScroogeCap/status/2067220322349134122?s=20))

[Scrooge McDuck@ScroogeCap$JPM has dug to the bottom of this $AVGO TPU debacle and are saying everything is hunky dory. See note below. There are no delays, and no cancellations. Wolfe is out positive too on AVGO today: We followed up with management to discuss the Apollo/Blackstone XPV financing 12:18 PM · Jun 17, 2026 · 10.2K Views

* * *

3 Replies · 8 Reposts · 97 Likes](https://x.com/ScroogeCap/status/2067220322349134122?s=20)

>  _**Vik:** Lots of bullish news for Broadcom despite their recent dips post earnings. News is that TPU v9 is not delayed, but the detailed note does explain how Google’s CoT might be 18 months behind. _
> 
> _**Austin:** We need retail investors to invest in Anthropic and OpenAI IPOs like they did for SpaceX, so the model labs can take those dollars and send them to the semiconductor supply chain. _😁

## Quick Takes

  * **CoreWeave** details infrastructure innovations behind being the first cloud provider to bring up and validate Nvidia’s Vera Rubin NVL72 platform. ([CoreWeave](https://wf.coreweave.com/blog/a-deep-dive-on-coreweave-innovations-for-nvidia-vera-rubin-nvl72))

  * **China** highlights five AI models trained entirely on domestic chips as Beijing pushes alternatives to Nvidia hardware amid US export curbs. ([SCMP](https://www.scmp.com/tech/tech-trends/article/3357391/can-chinese-silicon-replace-nvidia-here-are-5-ai-models-trained-local-chips?utm_source=rss_feed))

  * **Infineon** Malaysia draws more than 1,000 applicants in a 2km queue for production jobs starting at roughly $1,100 monthly. ([The Straits Times](https://news.google.com/rss/articles/CBMi0gFBVV95cUxPckJ3YnlVWmJvQjBMSHFkVFk5VG5qZTJXRmxzZEFiZXd0RWVBU21BNkJFc2lRay1ISXp6SmhJMk1MeFZUWGp4WHl1Qkd2WDN1ZEY3bXRJZlhuZnR3ckRYa3lXdWhWSGVXRFF1U2FhR3dkdlYzSUVyT0xlOTAwbWY1eFhlSnNhVktXLURIV0R6cnY0cnY4Qk1jZEhsSUlERFloUjFxMVhvd0N0WlpuMl9uV1I5ZGdIUE5RN01CUGNHNTdDSHl0NUJXZTFLOU5jMWpMaWc?oc=5))




### Worth a Look

[Intel’s Lip Bu Tan on “The Long View”](https://www.troweprice.com/en/us/insights/the-long-view-intel) — good conversation with T. Rowe Price.
