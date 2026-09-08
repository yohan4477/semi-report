---
source: https://daily.semidoped.com/p/daily-update-may-1st-2026
title: Daily Update - May 1st, 2026
date: 2026-05-01
kind: clipping
genre: daily
audience: everyone
subtitle: Intel EMIB yields, Qualcomm teases hyperscaler custom silicon design win, DeepSeek V4's SSD KV cache slashes inference cost
---
Competitors enter the fray. Intel’s EMIB is a legit alternative to CoWoS. Qualcomm throws it’s hat in the custom ASIC ring. _But which ring? Not sure exactly what custom ASIC means here…_ And SSDs in DeepSeek V4 are seriously driving down inference cost. Let’s get into it.

Subscribe

>  _**Vik:** I finished up at QCOM a week ago. Went on vacation this week. During the vacation, QCOM stock skyrocketed. Maybe I’m a market mover, but in the most embarrassing way. LOL._
> 
> _**Austin:** I don’t know man…. maybe you should take more vacations!_

* * *

### Intel EMIB yield reportedly >90%

Intel’s EMIB advanced-packaging yields are reportedly above 90%, per GF Securities analyst [Jeff Pu](https://x.com/sssjeffpu/status/2049864883450380768?s=46&t=e1Xfsq__q3Z5uU8psDOaeQ) in a note out of MediaTek’s earnings.

Embedded Multi-die Interconnect Bridge (EMIB) is Intel’s [advanced packaging](https://www.viksnewsletter.com/p/a-comprehensive-primer-on-advanced-packaging) alternative to TSMC’s CoWoS. It lets you interconnect multiple die at the silicon level rather than through an interposer.

EMIB ships in two flavors:

  * EMIB-T, with through-silicon vias (TSVs)

  * EMIB-M, with metal-insulator-metal (MIM) capacitors, useful for power connections through the EMIB die that need a bypass capacitor




Today EMIB scales to 8x reticle size. Intel’s roadmap targets 12x by 2028, matching what TSMC has guided for CoWoS. Google, NVIDIA, and Meta are all likely EMIB customers.

[](https://substackcdn.com/image/fetch/$s_!m8DK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8b37bbf7-b000-4278-97b2-d3cc230165d9_2560x1440.jpeg)

> _**Austin:** EMIB isn’t new by any means. For example, here’s a [2016 EMIB paper](https://ieeexplore.ieee.org/abstract/document/7545486) from Intel. It’s long been in production inside Intel server CPUs, GPUs, FPGAs. _
> 
> _So why the hype now? First, hyperscalers want a CoWoS alternative, and they want it yesterday. And EMIB-T and EMIB-M are genuinely useful. EMIB-T solves vertical power delivery necessary for EMIB to power HBM4, while EMIB-M improves local decoupling and signal integrity for UCIe-A-class high-speed die-to-die interfaces.  
>   
>  Also, Vik, not sure if you saw it on vacation, but $INTC went to the moon 🚀_

### Qualcomm hinted they’re in the custom ASIC game

In [yesterday’s daily update](https://www.semidoped.com/p/daily-update-april-30th-2026), we covered Qualcomm’s auto strength. 

The other earnings call moment worth flagging was the tease of custom silicon. CEO Cristiano Amon said, “We're also entering the custom silicon space, beginning our ramp with a leading hyperscaler, and we expect initial shipments in the December quarter”.

What form that design win takes is anyone’s guess. Amon kept fairly mum, other than to say more to come at the [Qualcomm Investor Day](https://investor.qualcomm.com/overview/default.aspx) on June 24, 2026.

> _**Vik:** AI200/250 got a similar stock pop with limited detail attached. I’d want to see more substance before drawing conclusions. _
> 
> _**Austin:** Qualcomm CEO [Cristiano Amon is giving a Computex Keynote](https://events.computextaipei.com.tw/en/KeynoteDetail01.aspx) on June 1. Between that and the investor day on June 24, I expect we’ll learn a lot more about Qualcomm’s datacenter and custom ASIC aspirations._

Subscribe

### Deepseek V4: KV cache compression and cost

Quote from [FundaAI](https://fundaai.substack.com/p/deepdeepseek-v4-the-inflection-point) (from free part of post):

> DeepSeek’s accumulated engineering work on SSD-based KV cache, which together migrate KV cache from expensive, capacity-limited DRAM / HBM onto larger and cheaper SSD at scale. We believe DeepSeek V4’s cache-hit repricing implies upside for SSD, with NAND demand set to grow exponentially.

This is the importance of context storage systems in inference. It is always better to store large amounts of KV matrices in SSDs and achieve a massive reduction in cost due to a high cache hit rate. DRAM does not provide that kind of capacity/cost ratio. Vik covered this extensively in his deep dive on context storage. Now we are seeing it play out in action in Deepseek v4 with 95%+ cache hit rates. 

From the [original post](https://open.substack.com/pub/viksnewsletter/p/context-memory-storage-tokenomics?utm_campaign=post-expanded-share&utm_medium=web) in Jan 2026:

> In short, context storage systems when deployed fully will drive down the cost of inference significantly, especially for long context cases. 

DeepSeek V4 is proof. Cost of tokens with cache hits have now fallen dramatically.

[](https://substackcdn.com/image/fetch/$s_!2gYp!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F98e80262-ee1c-4796-8e5a-00e09753f69e_1106x1040.png)

> _**Austin:** Vik, dude, you could have taken more of a victory lap on this one. Regardless, great topic, we should keep digging into SSDs and the impact on tokenomics._

_That’s it for today!_

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-may-1st-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
