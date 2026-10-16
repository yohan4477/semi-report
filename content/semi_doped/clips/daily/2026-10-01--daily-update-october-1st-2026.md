---
source: https://daily.semidoped.com/p/daily-update-october-1st-2026
title: Daily Update - October 1st, 2026
date: 2026-10-01
kind: clipping
genre: daily
audience: everyone
subtitle: Micron posts record FY2026 revenue, Synopsys signs $1B Amazon IP pact, Nebius acquires Inferize for up to $150M with 50 MW capacity, Huawei launches Kirin 9050 Pro across five Mate 90 models.
---
**Hello world, it’s Thursday, October 1st.**

Micron posted record fiscal fourth-quarter and full-year 2026 results, with current-quarter revenue guidance topping analyst estimates as AI memory demand continues to outstrip supply. Synopsys had a big day too, signing a multi-year silicon IP deal worth over $1 billion with Amazon while separately announcing a partnership with OpenAI to build GPT-Synopsys, a frontier model for AI-native chip design. Google also shipped Gemini 4 Argon, targeting enterprise and cybersecurity workflows, though Bloomberg is reporting internal skepticism about the model’s performance.

Let’s get into it. _— Austin & Vik_



 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

#### Presented by Crusoe

Crusoe builds AI infrastructure from the ground up — power, data centers, and the cloud on top.

If you’re running open models — GLM, DeepSeek, Kimi, Qwen — Crusoe’s managed inference is fast: up to 9.9x faster time-to-first-token and 5x the throughput of vLLM, thanks to their MemoryAlloy caching layer and tokenizer fastokens. And it’s the easy kind of fast: pick a model, grab an API key and start inference. No GPUs to provision, no infrastructure or clusters to manage, and it’s pay per million tokens.

$5 in free credits to try it. [Send your first request today →](https://console.crusoecloud.com/request-foundry?utm_source=newsletter_sponsor&utm_medium=newsletter&utm_campaign=nl_mi_su_semidoped-podcast)

### Micron Posts Record Results as AI Memory Demand Outstrips Supply

Micron reported [record fiscal fourth-quarter and full-year 2026 results](https://investors.micron.com/news/press-release/2026/Micron-Technology-Inc--Reports-Record-Fiscal-Fourth-Quarter-and-Full-Year-2026-Results/), with revenue forecasts for the current quarter blowing past analyst estimates as AI infrastructure buildouts drove demand the company says has outrun available supply. Backlog has swelled to levels Micron hasn’t seen before, and the queue isn’t shrinking. DRAM now [commands a 54% price premium over TSMC 2nm silicon](https://shattered.io/dram-more-expensive-than-tsmc-2nm-chips-2026/), a comparison that captures just how thoroughly memory pricing has decoupled from conventional chip economics. HBM and high-density DRAM capacity remains constrained, keeping average selling prices on an upward path; Reuters notes the supply gap is structural, not cyclical. 

> **Vik:** _This is the structural demand side playing out, not a normal cycle. Fabs keep steering wafer starts to HBM, which sells around 5x the per-bit price of DDR5, so commodity DDR5 tightens right alongside it. Investors keep hunting for the peak though. I don’t see it yet. I wrote about this several times on my Substack:[here](https://www.viksnewsletter.com/p/how-ai-demand-is-driving-a-memory-supercycle?utm_source=publication-search), [here](https://www.viksnewsletter.com/p/evaluating-memory-hog-cycles-in-the-ai-era?utm_source=publication-search), and [here](https://www.viksnewsletter.com/p/hbm-is-the-ugly-baby-what-now?utm_source=publication-search)._
> 
> **Austin:** _DRAM priced 50% above TSMC 2nm silicon!? Wild. Memory has the pricing power in semis right now, that’s for sure, hence Micron’s 87% margins._

### Synopsys Lands $1B Amazon IP Pact, OpenAI Chip-Design Partnership

Synopsys has signed a [multi-year silicon IP agreement worth over $1 billion with Amazon](https://www.datacenterdynamics.com/en/news/synopsys-and-amazon-sign-1bn-multi-year-ip-agreement-for-custom-chip-development/) to support the tech giant’s custom chip development programs. The company simultaneously announced GPT-Synopsys, a jointly developed model built with OpenAI under a [revenue-sharing arrangement](https://news.synopsys.com/2026-09-30-OpenAI-and-Synopsys-Announce-GPT-Synopsys-Frontier-Intelligence-to-Revolutionize-Chip-Design) in which Synopsys compensates OpenAI based on results rather than a flat fee, a structure designed to ease customer concerns about AI-generated design work. GPT-Synopsys is intended to perform chip design tasks at the level of an experienced engineer, spanning RTL generation through physical implementation. The two deals arrived together at Synopsys’s 2026 Investor Day, where the company also outlined its long-term financial model. Cadence, Synopsys’s closest EDA rival, has no announced equivalent to either agreement.

> **Vik:** _The rise of AI-driven EDA is a big deal actually. A lot of chip design is based on repetitive tasks, and takes up a lot of human labor. This means that a lot of work gets offshored to design houses. If chip design companies can make AI deliver all this, they will be inclined to keep their designs within country borders and push efficiency with AI. Bad for offshore design houses. Expect layoffs sadly._
> 
> **Austin:** _I was there! Stay tuned for the Semi Doped podcast early next week that I recorded live from Investor Day. Very interesting implications from the news._

### Google Ships Gemini 4 as TPU Revenue Recognition Begins Against $513.9B Cloud Backlog

Google released Gemini 4 Argon after months of delays, and the timing is awkward: [Bloomberg reports active internal skepticism](https://www.bloomberg.com/news/articles/2026-09-30/google-grapples-with-employee-skepticism-about-new-gemini-model) about the model’s performance in coding and other key areas, a candid admission for a flagship launch. AI chip capacity tied to the rollout has already sold out. That scarcity matters because Alphabet simultaneously began recognizing revenue from TPU systems against a [Cloud backlog of $513.9 billion](https://www.tokenpost.com/news/technology/25900), shifting the business from infrastructure build-out toward actual returns. The combination of sold-out chip capacity and unresolved model-quality concerns from within Google’s own ranks puts real pressure on Gemini 4 to deliver before competitors close any remaining gap.

> **Vik:** _Google gives the vibes of playing catch up here. Can we believe that this is truly a good model based on “trust me bro” benchmarks? I’m getting model fatigue. I’m already jumping between AI agents trying to test them all out. I think I am happy with my high tier Anthropic and OpenAI subscriptions. Will have to pass on Gemini 4._
> 
> **Austin:** _I’ll be kicking the tires on Argon regardless, every new frontier model so far has unlocked more productivity for me._

### Nebius Buys Inferize, Locks Up 50 MW of Southeast US Capacity

Nebius has [acquired Inferize](https://www.businesswire.com/news/home/20261001221757/en/Nebius-acquires-Inferize-to-strengthen-Nebius-Token-Factorys-production-inference-stack) to bolster the inference stack inside its Token Factory platform, paying somewhere between $100 million and $150 million (_unconfirmed_) for a startup that was only ten months old and operating in stealth. The Tel Aviv-founded team built software targeting production inference efficiency, giving Nebius a deeper chip-level optimization layer for the AI cloud service it competes on. AIB Data Centers separately signed a 12-year binding agreement to supply Nebius with [50 MW of capacity](https://www.quiverquant.com/news/AIB+Data+Centers+Announces+50+MW+Binding+Agreement+with+Nebius+for+AI+Data+Center+Capacity+in+the+Southeastern+U.S.) at a southeastern US data center site. That contract cements a physical expansion footprint to match the software acquisition, with long-tenor committed power suggesting Nebius is building for sustained, large-scale GPU cloud demand rather than short-cycle spot capacity.

> **Vik:** _Increasing hardware utilization is extremely important as we stay short of compute. More neo-clouds will try to extract the best out of their hardware. It translates into direct revenue._

### Huawei Mates Kirin 9050 Pro to Tau Logic-Folding in Five-Phone Lineup

Huawei launched the [Mate 90 series across five models](https://www.androidheadlines.com/2026/10/huawei-mate-90-lineup-gets-five-phones-and-one-very-serious-camera-add-on.html), each carrying a Kirin processor built on the company’s Tau Scaling Law architecture, with the flagship Kirin 9050 Pro deploying logic-folding technology to extract more compute density without requiring access to leading-edge fabrication nodes. The Tau chip approach, which Huawei says partially compensates for US export restrictions on advanced process equipment, is rolling out broadly enough that the Mate XT 2 is tracking toward [1 million pre-orders](https://www.scmp.com/tech/big-tech/article/3369400/huawei-steps-tau-chip-roll-out-mate-xt-2-track-1-million-sales?utm_source=rss_feed). The standard Mate 90 and Mate 90 Pro step down to the Kirin 9035, while the Pro Max carries the 9050 Pro and has already posted Geekbench 7 scores. Huawei also flagged further smartphone price increases tied to a tightening memory supply.

> **Vik:** _Logic folding sounds exotic, but[it’s really a hybrid bonding bet](https://www.viksnewsletter.com/p/huaweis-tau-scaling-is-really-hybrid-bonding-bet) \- stack a SMIC 7nm-class die on itself and you double density by burning twice the silicon, not the same as EUV making denser transistors. It is still incredible to see that phones are shipping in volume using this._

### Sector Watch

#### Compute

  * **AMD** publishes pricing and full specs for its 31-processor EPYC 9006 “Venice” family, with Zen 6 cores scaling to 256 cores from $700. ([EE News Europe](https://www.eenewseurope.com/en/amd-epyc-9006-lineup-700-256-cores/))

  * **Vicor** grants a VPD power-delivery license to an unnamed AI OEM, lifting shares 15% and raising its Q3 outlook on AI licensing momentum. ([quiverquant.com](https://www.quiverquant.com/news/Vicor+gains+as+raised+Q3+outlook+and+AI+licensing+momentum+lift+sentiment))




#### Foundry & Packaging

  * **Infineon** opens a $1.4 billion backend manufacturing hub in Samut Prakan, Thailand, expanding power and automotive chip assembly capacity. ([Nation Thailand](https://www.nationthailand.com/business/tech/40071760))

  * **Unimicron** secures a NT$10 billion land deal in Hukou to expand ABF substrate capacity for AI chip packaging demand. ([digitimes](https://www.digitimes.com/news/a20261001PD200/unimicron-capacity-abf-substrate-taiwan-demand.html))




#### Memory

  * **YMTC** wins Munich court injunctions against Micron over two 3D NAND utility models; Micron countersues alleging YMTC recruited its engineers and then patented stolen technology. ([Tom’s Hardware](https://www.tomshardware.com/pc-components/ssds/micron-lawsuit-claims-chinese-memory-maker-ymtc-poached-its-engineers-then-sued-it-using-its-own-stolen-tech-ex-employees-hid-roles-on-linkedin-patented-micron-tech-and-won-a-german-injunction))

  * **Koh Young Technology** wins additional orders for SOCAMM2 inspection equipment, extending its lead in next-generation memory module quality control. ([디지털투데이](https://www.digitaltoday.co.kr/en/view/108934/koh-young-technology-wins-additional-orders-for-socamm2-inspection-equipment))

  * **Sandisk** schedules its fiscal Q1 2027 results for October 29, 2026, the first standalone earnings report since its separation from Western Digital. ([Business Wire](https://www.businesswire.com/news/home/20260929992289/en/Sandisk-to-Report-First-Quarter-Fiscal-Year-2027-Results-on-October-29-2026))




#### Power

  * **Amazon** signs a 20-year, 690 MW power purchase agreement with Constellation Energy to support the Calvert Cliffs nuclear plant expansion in Maryland, committing ~$3B in infrastructure backing. ([Bloomberg Tech](https://www.bloomberg.com/news/articles/2026-09-30/amazon-nuclear-deal-to-help-expand-constellation-s-maryland-site))

  * **Bloom Energy** leases a Fremont facility for manufacturing expansion as CEO reaffirms record revenue and raised 2026 guidance driven by AI data center demand. ([The Business Journals](https://www.bizjournals.com/sanjose/news/2026/09/30/bloom-energy-fremont-manufacturing-expansion.html))

  * **GE Vernova Ventures** is seeking to upsize its venture fund to $250 million, targeting energy-technology startups supporting the AI infrastructure buildout. ([Axios](https://www.axios.com/pro/climate-deals/2026/09/30/ge-vernova-ventures-funding-energy-data-centers))




#### PCB & Components

  * **Samsung Electro-Mechanics** secures 3.6 trillion won in new supply contracts and confirms $1.85 billion in customer-funded Vietnam substrate expansion. ([조선일보](https://www.chosun.com/english/industry-en/2026/10/01/FYISMCFE2NDHPHXU4XA3N2WHXY/))

  * **Kolon Life Science** will expand PPO production capacity at its Gimcheon plant, targeting semiconductor material demand for advanced-node processes. ([The Elec](https://www.thelec.net/news/articleView.html?idxno=14321))

  * **Simmtech** advances its SOCAMM substrate line with Taesung entering talks to supply copper plating equipment, deepening Korea’s AI memory packaging supply chain.




#### Data Centers & Cloud

  * **CoreWeave** launches Forge, an integrated AI development environment connecting training, inference, evaluation and agent workflows, while also announcing availability of the Nvidia Vera CPU with 11,264 cores across its cloud. ([CoreWeave](https://www.coreweave.com/news/coreweave-forge-launches-turning-the-ai-loop-production-run-into-a-better-model-and-agent))

  * **Globe Telecom** commits at least $1 billion to data center investment as the Philippines positions to capture hyperscale AI infrastructure demand. ([Light Reading](https://www.lightreading.com/data-centers/globe-telecom-bets-1b-on-data-centers-as-the-philippines-positions-for-hyperscale-boom))




#### Optics & Networking

  * **Ciena** launches a $200 million venture fund focused on AI networking startups as optical interconnect demand accelerates across hyperscaler customers. ([rcrwireless.com](https://rcrwireless.com/20260930/ai-infrastructure/ciena-venture-ai-networking))

  * **Nokia** and ICEYE partner to develop secure, sovereign low-orbit satellite communications systems for government and defense customers. ([Nokia](https://www.nokia.com/newsroom/iceye-and-nokia-partner-to-launch-secure-and-sovereign-satellite-communications-for-governments-and-defense-customers/))

  * **Inseego** completes its acquisition of Nokia’s Fixed Wireless Access business, consolidating the FWA product line under a dedicated operator. ([Nokia](https://www.nokia.com/newsroom/inseego-completes-acquisition-of-nokias-fixed-wireless-access-business/))




_Tell us how to make Semi Doped better![ Give us your feedback](<../_img/2026-10-01--daily-update-october-1st-2026/001_poll> "http://semidoped.com/poll")! ❤️_

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-october-1st-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
