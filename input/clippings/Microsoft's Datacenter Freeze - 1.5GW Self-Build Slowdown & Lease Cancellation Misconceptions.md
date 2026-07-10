---
title: "Microsoft's Datacenter Freeze - 1.5GW Self-Build Slowdown & Lease Cancellation Misconceptions"
source: "https://newsletter.semianalysis.com/p/microsofts-datacenter-freeze"
author:
  - "[[DYLAN PATEL]]"
  - "[[JEREMIE ELIAHOU ONTIVEROS]]"
  - "[[MAYA BARKIN]]"
published: 2026-02-05
created: 2026-07-10
description: "OpenAI Shift, Oracle & Stargate Acceleration, Hyperscale Capex Implications, Vertiv's Impact Misunderstood, Copilot Weak Adoption"
tags:
  - "clippings"
---
Over the last few months, there have been a number of headlines raising concerns about Microsoft's reduction in datacenter leasing activities including a few datacenter leasing cancellations. [We called out Microsoft’s exit of multiple datacenter leasing contracts to our datacenter model clients on December 17th](https://semianalysis.com/datacenter-industry-model/) (two months before the Wall Street headlines). This story isn't as simple as it seems and there is a lot more nuance to Microsoft's actions.

The market has been focusing on "2GW of lease cancellations" which only **covers non-binding LOIs, not firm contracts**. This fails to mention that Microsoft has**~5GW of pre-leased capacity under binding contracts that will start operations between 2025 and 2028**.**In reality, Microsoft walked away from significantly more than 2GW of non-binding contracts** over the last 2 quarters. The firm was in discussion with virtually every single vendor for capacity in mid-2024 and has since completely frozen new leasing activity.

The chart below provides a perfect illustration. Microsoft singlehandedly drove the leasing market in 2023 and the first half of 2024. Not only was it aggressively signing deals, but it was also effectively “freezing” the market by locking up non-binding LOIs across the board. **Our estimates suggest Microsoft accounted for more than 60% of all new leased turnkey capacity from Q1 2023 through Q2 2024**. In June 2024, Microsoft's preleased capacity was larger than that of the four other major hyperscalers **combined**.

[![A bar chart illustrating the estimated datacenter pre-leased balance in megawatts for various companies, including Microsoft, Meta, Google, Amazon, and Oracle, over several quarters.](https://substackcdn.com/image/fetch/$s_!GCs6!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8ad3cca8-cf4b-456f-a4e5-81138a814bf5_1024x630.png)](https://semianalysis.com/datacenter-industry-model/)Source: [SemiAnalysis Datacenter Model](https://semianalysis.com/datacenter-industry-model/)

This happened at the same time as **Microsoft significantly ramped up its self-build efforts, acquiring tens of thousands of acres around the US and the globe, accelerating construction of existing sites and securing gigawatts of power for future sites**. Taken together, these moves signaled [Microsoft's preparation for what was the most ambitious infrastructure buildout in history.](https://semianalysis.com/2023/11/15/microsoft-infrastructure-ai-and-cpu/)

While the leasing slowdown is material, these changes are not material to the short and medium term and only impact 2027+. The more important slowdown of Microsoft's changes to their self-build datacenter plans. **Our research indicates that Microsoft is freezing 1.5GW of near term self-build datacenter projects - projects that were previously scheduled to go online in 2025 and 2026**.

Microsoft is freezing multiple (but not all) self-build projects across the globe with an immediate impact on capacity for 2025 and 2026 – [as highlighted earlier to our Datacenter Model clients](https://semianalysis.com/datacenter-industry-model/). Numerous multi-hundred-MW Microsoft campuses have shown underwhelming progress, despite our research indicating that these projects have secured energy and all necessary approvals. **This is a deliberate move by Microsoft to slow the expansion of its self-built capacity.**

The photos below illustrate the stalled development across several of its US datacenter projects - and there are many more. Slight progress is being made on the groundwork, but Microsoft has frozen construction of actual shells and delayed or cancelled orders for [cooling](https://semianalysis.com/2025/02/13/datacenter-anatomy-part-2-cooling-systems/) and [electrical](https://semianalysis.com/2024/10/14/datacenter-anatomy-part-1-electrical/) equipment. Progress is materially slower than the pace at which the firm had been developing self-build campuses in 2023 and 2024. Below we will make sense of Microsoft's strategic shift.

Microsoft’s capacity growth is misunderstood by the market, and the impact on equipment suppliers such as Vertiv is largely different from what has been suggested by analysts. Amateur confusion led a Wall Street analyst to forecast a material weakness in Vertiv's orders prior to Q1 25 earnings.

They misunderstood that a large portion of Microsoft's ~5GW preleased capacity is not yet in Vertiv's orderbook. And this is just one of many other major misconceptions - we explain the real impact on Vertiv at the end of this report.

What caused Microsoft's strategic shift, and what are the consequences to datacenter equipment suppliers like Vertiv, and the broader GPU and AI infra market ? Despite a 1.5GW self-build pause and a freezing of all new leasing activity, the implications are not as gloomy as it seems. We explain everything below.

## Microsoft's leasing and self-build exuberance

### Subscriber Content

Since early 2023, Microsoft has made an aggressive push to secure datacenter infrastructure as part of its response to surging demand for AI. The urgency of Microsoft’s strategy became apparent in the scale of its datacenter pre-leasing.

For context, hyperscaler datacenter capacity typically relies on both self-build and leasing. In the second scenario, a third party developer builds, owns and operates a datacenter, and the hyperscaler customer leases space and power to deploy IT equipment. Digital Realty, Equinix, QTS and NTT are some of the world's largest developers.

Pre-leasing is a standard practice in hyperscale datacenter (~50MW+) development, given the long construction timelines and high capital expenditure. These agreements allow companies to commit to leasing space in a facility that hasn't been completed yet. It is typical to outline key terms of an agreement with a non-binding Letter of Intent (LOI) before a final, binding contract is signed.

In 2023 and H1 2024, the scale of Microsoft’s leasing activity was staggering. The company contracted over 5GW of capacity, including **close to 2GW in CQ3 2023 alone**. To put this in perspective, the entire North American datacenter market grew by 2GW in full year 2022 – a record year back then! The scale of Microsoft’s leasing during this period is difficult to overstate.

[![A bar chart illustrating Microsoft's estimated datacenter pre-leased balance \(MW of IT capacity\) over several quarters, with distinct blue bars representing total pre-leasing and an orange line indicating quarter-over-quarter change.](https://substackcdn.com/image/fetch/$s_!20UE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F377534ab-91d0-49e6-a3f6-5e39a816bd73_2038x1280.png)](https://semianalysis.com/datacenter-industry-model/)Source: SemiAnalysis estimates and analysis of public filings

However, what the market may have overlooked is the sheer scale of Microsoft’s self-build acceleration. A simple look at the company's balance sheet reveals the magnitude of the company’s transformation: in FY24 (ending June 2024), Microsoft reported a $26B increase in building gross asset value and a 44% year-over-year surge in owned land. **Its forward-looking construction commitments tripled year-over-year to over ~35 billion USD.** [Our granular project-by-project analysis of Microsoft's growth plans depicts a similar story](https://semianalysis.com/datacenter-industry-model/).

[![Bar graph illustrating Microsoft datacenter-related balance sheet items in USD million from FY 2021 to FY 2024, showing buildings and improvements, committed construction, and land acquisitions.](https://substackcdn.com/image/fetch/$s_!xrW0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85f8a154-c3fa-45d4-8ab3-857bd8b7930c_2022x1276.png)](https://substackcdn.com/image/fetch/$s_!xrW0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F85f8a154-c3fa-45d4-8ab3-857bd8b7930c_2022x1276.png)Source: SemiAnalysis, Microsoft 10-K

## The OpenAI shift

Prior to the GenAI hype cycle, Azure was already growing at an astonishing pace. Microsoft's Cloud Computing arm has been consistently gaining share in the Public Cloud market. As a consequence, despite a vast infrastructure expansion (more than doubling electricity consumption from FY2020 to FY2023), Azure datacenter capacity constraints have long been a recurring topic.

[![Bar chart depicting Microsoft's electricity consumption in TWh from FY 2020 to FY 2023, showing an increase from 11 TWh in FY 2020 to 24 TWh in FY 2023. Semianalysis logo is present.](https://substackcdn.com/image/fetch/$s_!EaNg!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6085dea-70cf-449c-aff3-807bcf978f85_1878x1266.png)](https://substackcdn.com/image/fetch/$s_!EaNg!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff6085dea-70cf-449c-aff3-807bcf978f85_1878x1266.png)Source: Microsoft

OpenAI's ramp was fuel to the fire. Starting with a few tens of megawatts of AI hardware in 2022, [the firm kicked off a plan to expand capacity by orders of magnitude](https://semianalysis.com/2024/09/04/multi-datacenter-training-openais/#how-openai-and-microsoft-plan-to-beat-google) following ChatGPT's rise. Microsoft was on the front line as its primary partner - recall that, at the beginning of 2024, “Stargate” was largely a Microsoft/OpenAI project!

We believe that some cracks started to emerge in the spring / summer. [In September 2024, we highlighted the gigawatt-scale Crusoe/Oracle datacenter in Abilene, Texas as key to OpenAI’s training infrastructure](https://semianalysis.com/2024/09/04/multi-datacenter-training-openais/#how-openai-and-microsoft-plan-to-beat-google). We have been largely proven right, as the site is now [officially the first “Stargate” campus](https://semianalysis.com/2025/01/23/openai-stargate-joint-venture-demystified/) – and is developing extremely fast. Crusoe publicly announced a major expansion of the campus in March, targeting 1.2GW of total power by 2026. Ground has already been broken for future buildings.

[![Aerial view of a construction site with multiple large buildings in various stages of completion, surrounded by cleared land and vehicle tracks.](https://substackcdn.com/image/fetch/$s_!VAYS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F939ac1b8-91fb-42c2-8e04-85a958626674_2370x1358.png)](https://substackcdn.com/image/fetch/$s_!VAYS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F939ac1b8-91fb-42c2-8e04-85a958626674_2370x1358.png)Source: [SemiAnalysis Datacenter Model](https://semianalysis.com/datacenter-industry-model/)

The acceleration of this site materialized a shift in OpenAI’s spending strategy, with Oracle emerging as the winner and Microsoft on the losing side. We believe the primary factors behind this shift are poor execution and risk management, with Satya Nadella aiming to avoid overexposing Microsoft to AI training workloads.

One of Microsoft’s flagship AI sites, the Mount Pleasant datacenter, is feeling the impact. Our imagery reveals underwhelming development. While Phase 1 is impressive by its scale, it took longer than expected to fully develop due to its complex two-story structure, and Phase 2 has not shown any meaningful progress in the last six months. [Our analysis of the power infrastructure in the area reveals that construction could be further delayed.](https://semianalysis.com/datacenter-industry-model/)

[![Comparative satellite images of a Microsoft datacenter site showing progress from October 24, 2024, to March 25, 2025, highlighting construction development.](https://substackcdn.com/image/fetch/$s_!Vv5p!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F425d65dc-fd85-47b3-a9be-df67031138b3_1024x482.png)](https://substackcdn.com/image/fetch/$s_!Vv5p!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F425d65dc-fd85-47b3-a9be-df67031138b3_1024x482.png)Source: [SemiAnalysis Datacenter Model](https://semianalysis.com/datacenter-industry-model/)

In January 2025, the partial Microsoft/OpenAI breakup was made official. Their partnership is no longer exclusive, transitioning to a model where Microsoft now holds a right of first refusal (ROFR). While Microsoft still retains rights to OpenAI's intellectual property (including models and infrastructure) for integration into products like its Copilot platform, the reality is that Microsoft's hesitation to take on the financial risks of such investments is proving detrimental. Microsoft is losing both control and potential revenue as OpenAI moves toward new partnerships, with the [Stargate Joint Venture playing a central role in this shift](https://semianalysis.com/2025/01/23/openai-stargate-joint-venture-demystified/).

OpenAI has then further diversified its partners. In March 2025, it signed a USD $11.9 billion, five-year contract with CoreWeave. This included a USD $350 million equity investment in CoreWeave, deepening their strategic partnership. The deal has two impactful consequences:

  * **We believe that Coreweave GPUs are likely to serve OpenAI inference**. This would be a first, as Microsoft today serves 100% of OpenAI’s inference workloads.

  * **CoreWeave now has the ability to deal directly with OpenAI, and potentially take more share from Microsoft if it can deliver faster.** There is also higher price competition. Microsoft likely has to sacrifice some margin if it wants to win - [and there is a stark contrast relative to traditional Azure Cloud Computing margin profile](https://semianalysis.com/ai-cloud-tco-model/).




## Is Copilot filling the gap?

Beyond losing ground with OpenAI, we believe Microsoft is also encountering weaker-than-expected demand for its internal services. Progress on internal LLMs has been particularly underwhelming. Despite forming a dedicated AI team led by Mustafa Suleyman, Microsoft's internal LLM efforts lags behind top AI labs and even direct peers like Amazon's Nova models. As a result, the compute budget allocated to its internal GenAI research remains relatively modest and is not seeing significant growth.

But the key pillar of Microsoft’s internal AI strategy is Copilot - both as a consumer-facing product, but more importantly, an enterprise product. Starting with the consumer side, data from Google Trends reveals disappointing adoption compared to Google’s Gemini. While Copilot’s popularity aligns with Claude’s, the trend is concerning.**Interest in Copilot peaked last year and has since plateaued** , while Claude, Gemini and ChatGPT display a steady increase.

A large part of this could be due to Copilot still not including the best models from OpenAI.

[![Line graph comparing Google Trends data for Microsoft Copilot, Claude, and Google Gemini from February 2023 to February 2025, with a logo for 'semianalysis' in the top left corner.](https://substackcdn.com/image/fetch/$s_!jQod!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fefb9707a-acc0-4cba-83c6-808218cfd08f_1994x1276.png)](https://substackcdn.com/image/fetch/$s_!jQod!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fefb9707a-acc0-4cba-83c6-808218cfd08f_1994x1276.png)Source: Google Trends, SemiAnalysis

It is much harder to gauge adoption of the technology on the enterprise side. Anecdotal evidence points to somewhat lower than expected growth, and overall slow development and adoption of custom enterprise GenAI applications relative to initial expectations. In addition, analyzing RPO trends of Microsoft and Oracle reveals the former is losing market share, despite its status of the primary OpenAI provider! And we expect Oracle's RPO to surge by tens of billions of dollars in the coming quarters, as phase two of the Abilene, TX datacenter gets booked.

Even GCP's stable share relative to Microsoft is arguably disappointing, [given the scale of OpenAI's 2024 and 2025 deployments](https://semianalysis.com/datacenter-industry-model/) that are likely booked already for the most part. That combined with steady non-AI growth suggests relatively disappointing GenAI business growth (excluding OpenAI), relative to peers. We still expect steady RPO growth for Microsoft driven by OpenAI, as suggested by our bottom-up model and 2026+ deployments, but struggle to see evidence of meaningful Copilot enterprise adoption.

[![Chart comparing Oracle RPO, Microsoft RPO, and Google Cloud RPO in USD million, showing trends and percentage relationships over time.](https://substackcdn.com/image/fetch/$s_!F5hS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdbc3edbc-3428-4de0-8a59-aa880644aa27_1024x608.png)](https://substackcdn.com/image/fetch/$s_!F5hS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fdbc3edbc-3428-4de0-8a59-aa880644aa27_1024x608.png)Source: SemiAnalysis, company filings

## Market Implications – Microsoft CapEx, Hyperscaler trends, Vertiv, Neoclouds

Let’s evaluate one by one the consequences of Microsoft's self-build slowdown:

### **1\. Microsoft’s CapEx outlook:**

  
Tracking datacenter growth is a good forward-looking indicator to understand what is likely to happen in FY2026. [Our project-by-project tracker](https://semianalysis.com/datacenter-industry-model/) reveals that Microsoft will still significantly expand its total capacity next year. But there will be a meaningful change in asset purchase breakdown:

  * Right-of-use finance lease asset recognitions are likely to increase significantly. They are part of Microsoft’s “headline” CapEx but not PP&E CapEx. A good portion of the ~5GW pre-leased backlog is actively under construction and will meaningfully increase Microsoft’s capacity in 2025 and 2026.

  * PP&E long-lived assets are likely to be flat-to-down. This is directly related to the self-build pause. We expect the pause to continue, and hit international markets harder in calendar 2026, after being initially US-focused in 2025. Note that, while YoY self-build CapEx growth might be disappointing, it still contributes to Microsoft's capacity expansion. [While pausing on 1.5GW, Microsoft's pipeline is significantly higher](https://semianalysis.com/datacenter-industry-model/).

  * PP&E shorter-lived assets like [GPUs will go up significantly](https://semianalysis.com/accelerator-model/). Microsoft remains a key driver behind Nvidia’s revenue growth, largely driven by OpenAI’s inference and training workloads. While there is a partial breakup, the LLM leader will remain a key engine to Azure’s growth.

  * In conclusion, we still expect Microsoft to see YoY CapEx growth in FY26. However, we believe there are risks tied to economic conditions and overall GDP growth. Microsoft’s “non-OpenAI” revenue is arguably still in the proof-of-concept phase and remains cyclical, much like any other enterprise R&D budget.

  * Microsoft's self-build construction pause, while continuing early groundwork, highlights a desire to increase flexibility. The firm has the option to react fast to surges in demand. Tracking demand-side datapoints will be key.




### **2\. Vertiv and other datacenter equipment suppliers:**

  * As explained in great detail in our [Cooling ](https://semianalysis.com/2025/02/13/datacenter-anatomy-part-2-cooling-systems/)and [Electrical ](https://semianalysis.com/2024/10/14/datacenter-anatomy-part-1-electrical/)deep-dive articles, Vertiv’s content/MW is much lower for self-build compared to colocation datacenters - and varies by hyperscaler. The Microsoft pause is a negative, but not as bad as feared by the market and uninformed Wall Street analysts.

  * Microsoft’s non-binding LOI cuts do not impact Vertiv’s near term order trends, for the most part. There is a lead time mismatch, as **Vertiv’s top selling product do not have particularly long lead times**. The total hyperscaler pre-leasing balance keeps growing and suggests accelerated growth for Vertiv going forward. But **leasing trends remain a key item to watch for total pipeline beyond orders**.

  * Our supply-demand analysis of IT power enables us to identify hyperscalers in need for more power, and likely to rely more on leasing. We expect more leasing activity to come, but a changing customer mix.




### **3\. Ex-Microsoft Cloud CapEx and growth trends**

  * We expect Oracle’s RPO to surge again, driven by their Gigawatt win. The deal alone will trigger a double digit increase to Oracle’s RPO – and CapEx will be impacted accordingly.

  * Some specific hyperscalers are highly power-constrained and actively looking for solutions. We expect Coreweave, Oracle, and other Neoclouds like Nebius or Lambda to benefit – as hyperscalers are reluctant to work with a direct competitor.

  * We think the story on AWS’ datacenter cancellations is clickbait. Although the company has pulled out from specific deals in Europe, this does not reflect a material change in strategy – as opposed to Microsoft. In APAC and LATAM, the [AI Diffusion Export Controls ](https://semianalysis.com/2025/01/15/2025-ai-diffusion-export-controls-microsoft-regulatory-capture-oracle-tears/)have tempered market growth forecasts and increased uncertainty – as we expected, but is nothing new.




Our institutional clients have the full detail hyperscaler-by-hypescaler of real time changes in strategy.
