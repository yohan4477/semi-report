---
source: https://daily.semidoped.com/p/daily-update-august-10th-2026
title: Daily Update - August 10th, 2026
date: 2026-08-10
kind: clipping
genre: daily
audience: everyone
subtitle: Apple tests Chinese DRAM, Anthropic builds its own chip team, and TSMC's 2nm books are full through 2028 at $30,000 a wafer.
---
**Hello world, it’s Monday, August 10th.**

Apple is reportedly testing CXMT memory chips for iPhones and MacBooks, which would mark a significant milestone for Chinese DRAM clearing US performance benchmarks. Anthropic is building its own chip team with Samsung eyed as foundry partner, and TSMC’s 2nm capacity is already sold out through 2028 at $30,000 a wafer.

Let’s get into it. _— Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

### Apple Tests CXMT Chips for iPhones as Chinese DRAM Clears Speed Benchmarks

Apple is [testing memory chips from China’s ChangXin Memory Technologies for use in iPhones and MacBooks](https://www.reuters.com/business/retail-consumer/apple-tests-chinas-cxmt-memory-chips-iphones-macbooks-wsj-reports-2026-08-09/), according to a Wall Street Journal report, even as US regulatory pressure complicates any formal supply agreement. The outreach comes amid a broader tightening in global DRAM supply driven by AI demand, and CXMT has reportedly declined to offer the kind of pricing concessions Apple typically extracts from suppliers. US export-control rules currently block CXMT from supplying Apple with the custom-designed chips the iPhone requires, meaning standard DRAM modules are what’s actually under evaluation.

On the performance side, CXMT chips [hit DDR5-8800 MT/s on AMD’s AM5 platform](https://www.tomshardware.com/pc-components/ram/chinas-memory-making-champion-smashes-ddr5-8800-barrier-on-amd-platform-cxmt-chips-close-the-gap-with-sk-hynix), matching speeds associated with SK Hynix’s top-tier modules. That result, demonstrated on the X870E chipset, puts a Chinese vendor on competitive footing with established Korean suppliers for the first time in the high-speed desktop segment. Tuttle Capital’s HBMX ETF recently [added CXMT exposure](https://www.newsfilecorp.com/release/308651/Tuttle-Capitals-Concentrated-Memory-Stack-ETF-HBMX-Adds-Exposure-to-CXMT-the-488-Billion-Chinese-Memory-Maker-Many-U.S.-Investors-Cant-Access-Directly), calling it a [$488 billion company](https://www.newsfilecorp.com/release/308651/Tuttle-Capitals-Concentrated-Memory-Stack-ETF-HBMX-Adds-Exposure-to-CXMT-the-488-Billion-Chinese-Memory-Maker-Many-U.S.-Investors-Cant-Access-Directly) that most US investors cannot access directly. CXMT also secured [entry into the MSCI China index](https://www.scmp.com/business/china-business/article/3363490/how-china-dram-champion-cxmts-msci-entry-could-lure-fund-inflows-cement-its-top-ranking), a move that may draw additional institutional fund inflows.

> _**Vik** : Regardless of whether they get to use Chinese memory supply or not, Apple 18 Pro models are estimated to have a higher selling price [according to TrendForce](https://www.trendforce.com/presscenter/news/20260810-13172.html)._
> 
> [](https://substackcdn.com/image/fetch/$s_!tk7F!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa3213e91-794f-4c6b-9316-1fdd5ef693c9_1080x560.jpeg)
> 
> _**Austin:** Bold move by CXMT to reportedly hold the line on pricing. At first blush it seems the wrong move; wouldn’t you want to make friends with Apple now by giving them a little discount when times are hard, and trust the good relationship would pay back over time? Except, that’s not how Apple works. I don’t think CXMT favors now would result in any extra business whatsoever from Apple in the future. And if you believe that, you might as well charge them a pretty penny for today’s dance._
> 
> _Also — dang, 42% of BOM for memory in that cart. OUCH._

### Anthropic Forms Chip Team; Willing to pay $$$ to Teach Chip Design to AI

Anthropic is assembling a dedicated silicon design group to build custom inference chips for its Claude models, with Samsung [reported as the likely manufacturing partner](https://www.tomshardware.com/tech-industry/anthropic-to-build-its-own-co-designed-custom-ai-accelerator-for-inferencing-workloads-samsung-reported-to-be-partnering-with-the-claude-ai-maker-for-manufacturing). The move follows a pattern set by Google with its TPUs and Amazon with Trainium: as inference workloads scale, buying compute from Nvidia becomes a margin problem, and owning the silicon solves it. 

Anthropic is paying engineers focused on teaching AI models to assist with chip design [close to $1 million annually](https://wccftech.com/anthropic-is-paying-nearly-a-million-dollars-per-year-to-the-engineers-teaching-its-ai-models-to-design-a-chip-but-just-320000-485000-to-those-actually-building-its-first-asic/), while those building the first ASIC directly earn between $320,000 and $485,000. The salary gap reflects how much the company is betting on AI-assisted design workflows, not just conventional hardware engineering. [Claude demand straining its existing compute strategy](https://mlq.ai/news/anthropic-is-building-a-chip-design-team-as-claude-demand-strains-its-compute-strategy/) is the pressure driving the timeline. Custom silicon takes years to tape out and qualify, so the team Anthropic is hiring now is building toward a future where the company isn’t entirely dependent on GPU allocations it cannot control.

> _**Vik** : I can’t believe teaching AI to design chips has a 3x factor over designing the chip yourself in terms of leverage. This actually does make sense because you teach AI to design a chip once and reap the benefits forever going forward. Human capital does not have the same leverage. Regardless, this kind of stuff is crazy, and I have seen nothing like it in the 15 years I worked in the semi world._
> 
> _**Austin:**_ _Lesson for current undergrads? Take both. ML and EE, not just one. Learn to train models. Learn to design chips too. Actually, zoom out. The move is to pair AI training with any domain, and you can train AI to do that domain’s work._

### TSMC Capacity Sells Out at Every Node as AI Locks Bookings Through 2028

TSMC’s [2nm wafers are priced at $30,000 each](https://tech-insider.org/ca/tsmc-2nm-wafer-price-2026/) with capacity already committed through 2028, and that’s before the company has finished building everything it’s planning to sell. The foundry [accelerated 3nm output ahead of schedule](https://www.techtimes.com/articles/323627/20260808/tsmc-accelerates-3nm-output-months-early-14nm-factory-beats-schedule.htm) and has secured land in Taiwan for [two 1.4nm fabrication plants](https://wccftech.com/tsmc-1-4nm-fabs-longtan-expansion-landowner-reversal/), a site acquisition that moved only after landowners calculated what they’d be leaving on the table by refusing. Monthly sales [rose 45%](https://www.bloomberg.com/news/articles/2026-08-10/tsmc-sales-rise-45-after-ai-spending-roars-on-despite-jitters) as AI hardware spending held firm through broader market jitters, and full-year capital expenditure is tracking toward [$64 billion](https://tech-insider.org/tsmc-earnings-capex-arizona-2026/).

The CoWoS advanced packaging hub at Longtan is [sold out globally](https://www.techtimes.com/articles/323679/20260809/tsmc-revives-longtan-14nm-fabs-cowos-hub-both-sell-out-globally.htm), with TSMC reviving that site to serve both 1.4nm production and the packaging demand that AI chip builders cannot satisfy elsewhere. Not everything in the expansion is logic-focused: per TrendForce, TSMC and Sony are reportedly planning a [JPY 1 trillion joint venture](https://www.trendforce.com/news/2026/08/10/news-tsmc-sony-reportedly-plan-jpy-1-trillion-jv-for-image-sensors-in-kumamoto-eye-2029-mass-production/) in Kumamoto to manufacture image sensors, with Reuters pegging the [investment at $6.3 billion](https://www.reuters.com/world/asia-pacific/sony-tsmc-spend-63-billion-jointly-make-image-sensors-nikkei-says-2026-08-10/) and mass production targeting 2029. The deal extends TSMC’s Japan footprint, already being analyzed by Digitimes as an [advanced packaging push](https://www.digitimes.com/news/a20260807VL221/tsmc-japan-kumamoto-3nm-fab-packaging.html) beyond the company’s original Kumamoto wafer fab.

> _**Austin:**_****_TSMC continues to be such an interesting company given the market dynamics right now. And just they released July’s monthly revenue, which is also one-of-a-kind. 5.6% MoM, 44.7% YoY._
> 
> [](https://substackcdn.com/image/fetch/$s_!IygF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd970086c-5e1b-4d95-b485-8e298389a97c_682x159.jpeg)

### Key Data

Nice chart from [Ben Bajarin](https://open.substack.com/users/21971657-ben-bajarin?utm_source=mentions) from Creative Strategies that shows why it’s different this time.

[](https://substackcdn.com/image/fetch/$s_!G53P!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd8c8e704-dd97-4d75-b225-54882c8471e4_2630x1972.jpeg)

### Sector Watch

#### Memory

  * **SK Hynix** board formally approves $38 billion investment split across Yongin and Cheongju fabs, with additional shareholder-return measures promised in Q3. ([Reuters](https://www.reuters.com/world/asia-pacific/sk-hynix-announce-additional-shareholder-return-measures-third-quarter-2026-08-07/))

  * **SK Hynix** mulls strategic options for its Chongqing, China facility, including bringing in an outside investor to accelerate an exit. ([Bloomberg Tech](https://www.bloomberg.com/news/articles/2026-08-07/sk-hynix-is-said-to-mull-options-for-3-billion-chongqing-assets))

  * **SK Hynix** and SanDisk unveil the first HBF standard specification, positioning High Bandwidth Flash as a new memory tier for AI infrastructure. ([EE News Europe](https://www.eenewseurope.com/en/sk-hynix-sets-first-hbf-standard-for-ai-memory/))




#### Compute

  * **Moore Threads** files for a Hong Kong listing after reporting 147% first-half revenue growth, seeking public capital to fund AI GPU expansion. ([Bloomberg.com](https://www.bloomberg.com/news/articles/2026-08-09/china-ai-chip-designer-moore-threads-plans-hong-kong-listing))

  * **Cambricon** reports 6 billion yuan in H1 revenue and 2.3 billion yuan net profit, doubling year-on-year as China AI chip demand surges. ([digitimes](https://www.digitimes.com/news/a20260810VL203/cambricon-ai-chip-revenue-capacity-demand.html))

  * **Intel** appoints Dean Jarnac as executive vice president and chief sales officer to strengthen customer engagement and accelerate revenue growth. ([Intel Newsroom](https://newsroom.intel.com/corporate/intel-announces-leadership-appointment-to-strengthen-customer-engagement-and-accelerate-growth))




#### Foundry & EDA

  * **Siemens** agrees to acquire EDA software firm Precision Innovations, extending its electronic design automation portfolio. ([Evertiq](https://evertiq.com/news/2026-08-07-siemens-to-acquire-eda-software-firm-precision-innovations))

  * **Synopsys** demonstrates CXL 4.0 IP running at 128 GT/s, claiming 3-6x KV cache offload improvement over SSDs for AI inference workloads. ([StorageReview.com](https://www.storagereview.com/news/synopsys-cxl-4-0-ip-hits-128-gt-s-claims-3-6x-kv-cache-offload-over-ssds))




#### Packaging

  * **ACM Research** receives its first production and evaluation orders for the Ultra ECP ap-p horizontal panel electroplating tool, advancing large-panel advanced packaging toward volume manufacturing. ([ACM Research](https://ir.acmr.com/news-releases/news-release-details/acm-researchs-ultra-ecp-ap-p-horizontal-panel-electroplating))

  * **Ibiden** raises its full-year profit forecast as demand for AI server substrates and ABF buildup substrates strengthens across hyperscaler customers. ([digitimes](https://www.digitimes.com/news/a20260805PD228/ibiden-demand-profit-forecast-2026.html))

  * **Ajinomoto** reports surging demand for its ABF substrate materials, riding the advanced packaging boom driven by AI chip production ramp. ([digitimes.com](https://www.digitimes.com/news/a20260807VL222/demand-packaging-forecast-business-sales.html))




#### Optics & Networking

  * **Zhongji InnoLight** seeks a $7 billion Hong Kong listing focused on AI data center optical interconnect products amid booming transceiver demand. ([Indiatimes](https://datacenters.economictimes.indiatimes.com/news/ai-compute-infrastructure/zhongji-innolight-seeks-7-billion-hong-kong-listing-for-ai-data-centre-focus/133082914))

  * **Kioxia** demonstrates a GP1 enterprise NVMe SSD hitting 10 million IOPS at FMS 2026, targeting AI and cloud storage infrastructure deployments. ([ServeTheHome](https://www.servethehome.com/a-10m-iops-kioxia-gp1-ssd-shown-running-at-fms-2026/))




#### Edge & Automotive

  * **LX Semicon** begins mass production of South Korea’s first domestically developed automotive MCU, supplying Hyundai and Kia in a semiconductor localization milestone. ([The Korea Times](https://www.koreatimes.co.kr/business/tech-science/20260810/lx-semicon-supplies-automotive-semiconductor-to-hyundai-kia))

  * **MediaTek** is committing $5 billion to Intel Foundry for advanced chip manufacturing, a significant vote of confidence in Intel’s foundry ambitions. ([天下雜誌](https://english.cw.com.tw/article/article.action?id=4932))

  * **STMicroelectronics** launches the ST54M secure element with hardware-based post-quantum cryptography, targeting IoT and edge device security.




#### Policy & Trade

  * **US government** reviews offshore access to Nvidia chips after AI capability gains by Chinese entities using third-country procurement routes. ([Bloomberg.com](https://www.bloomberg.com/news/articles/2026-08-07/us-reviews-china-s-offshore-access-to-nvidia-chips-after-ai-breakthroughs))

  * **India** plans polysilicon production incentives to reduce its dependence on Chinese supply in the solar and semiconductor materials chain. ([Reuters](https://www.reuters.com/world/china/india-plans-polysilicon-incentives-reduce-reliance-china-2026-08-07/))

  * **South Korea** sentences a former SK Hynix employee to prison for leaking proprietary chip technology to a Chinese firm, per Yonhap. ([Reuters](https://www.reuters.com/legal/litigation/former-sk-hynix-employee-jailed-leaking-information-chinese-firm-yonhap-reports-2026-08-09/))

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-august-10th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
