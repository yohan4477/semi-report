---
source: https://daily.semidoped.com/p/daily-update-may-15th-2026
title: Daily Update - May 15th, 2026
date: 2026-05-15
kind: clipping
genre: daily
audience: everyone
subtitle: CRBS IPO pops, Fractile gets funds, Rivian's Robotics play. Also, notes on Cisco, Qualcomm. 
---
Cerebras just made a lot of people a $#it ton of money. Inference accelerator builders like Fractile are raising money. Robotics is a growing theme in Rivian.

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player! We have an upcoming episode entirely dedicated to Cerebras!_

* * *

### Cerebras IPO

Although the Cerebras IPO was priced at $185 per share, the trading day opened up at $350 per share and closed 68% up at $311. This values the company closer to the $100B mark. There’s no doubt this is a fantastic chip, and we have an upcoming Semi Doped podcast episode that goes into quite some depth. We’re excited to see where this goes in the future.

This AI IPO is a big data point that sets precedent of what to expect in the future. Now the SRAM inference accelerator startup race is on, and we’re going to see a lot more of this. This is great news for anyone working on inference hardware. Congrats to Cerebras and everybody who bought at pre-IPO prices.

[Morning Brew ☕️@MorningBrewCerebras, by the numbers: IPO: • Price: $185 • Shares: 30 million • Raise: $5.55 billion • Valuation: $56.4 billion At the open: • Price: $350 (+89%) • Valuation: $100+ billion It's the largest U.S. tech IPO since Uber in 2019 6:33 PM · May 14, 2026 · 39.6K Views

* * *

7 Replies · 20 Reposts · 409 Likes](https://x.com/MorningBrew/status/2054993468586426734?s=20)

>  _**Austin:** We’ll cover this more on this week’s pod coming ASAP. But I’ve always been bearish on the pre-ChatGPT-era AI accelerators like Groq and Cerebras. They made their architectural calls before anyone understood how much memory frontier models would chew through for weights and KV cache to do intelligent, long-context work. Yes, SRAM-only accelerators can fire off tokens at incredibly low latency, but only for small-to-medium models at low batch sizes, meaning a handful of concurrent users. Is that a $100B market cap business?_
> 
> _What I underappreciated was the “any X is a good X right now, because supply is so tight” dynamic. Any CPU, any SRAM accelerator, anything. Bonus points if X doesn’t lean on leading-edge TSMC capacity. And hey, who cares about DRAM shortages and price hikes if you don’t use any of that?_
> 
> _So[Nvidia scooped Groq](https://x.com/semidoped/status/2008298610706772309) (that was the surprise), and that opened the lane for Cerebras. OpenAI partnered up, and now Cerebras is heading to IPO. But the question in the back of my mind is what happens to Cerebras when competitors actually design their systems for frontier MoE models with massive context?_
> 
> _Chips are coming that mix memory hierarchies (SRAM + HBM + DRAM), use lower-precision numerics, and so on.[MatX](https://www.chipstrat.com/p/an-interview-with-matx-ceo-reiner), Etched, SambaNova, d-Matrix, Fracticle, and on and on. _
> 
> _And the XPU roadmaps are moving fast and thinking hard about exactly these constraints too. Google’s[TPU v8i](https://www.semidoped.com/p/googles-networking-innovations) made the tradeoffs and even built the interconnect around MoE inference. [Microsoft’s Maia](https://www.chipstrat.com/p/an-interview-with-microsofts-saurabh), Trainium, and [Meta’s MTIA](https://www.chipstrat.com/p/metas-mtia-roadmap) (four inference-optimized chips in two years!) aren’t sitting still either._
> 
> _Can Cerebras fend off all of it?_

### Fractile raises $220M for inference silicon that ditches HBM and SRAM

The Wall Street Journal reported that UK chip startup Fractile, founded in 2022 by Oxford-trained engineer Walter Goodwin, closed a $220M Series B led by Factorial Funds, Accel, and Peter Thiel’s Founders Fund. Fractile builds inference-specific silicon and is targeting latency, the time it takes a frontier model to produce useful responses, as the binding constraint as agentic workloads push token budgets per task into the tens of millions. Goodwin told the Journal Fractile has designed both a logic chip and a rack-level architecture for attaching memory that he says will “help AI companies maximize bandwidth without sacrificing speed.” Fractile explicitly does not use high-bandwidth memory or on-chip SRAM, the two dominant memory paths in AI accelerators today. The company declined to disclose technical specifications, and Goodwin framed the target simply: “fast and cheap.” The Information has separately reported Anthropic has discussed purchasing Fractile silicon.

**Sources:** [WSJ](https://www.wsj.com/tech/ai/chips-startup-fractile-raises-220-million-to-speed-up-ai-queries-c8681944)

>  _**Austin:** No SRAM? Did the WSJ get that right? _
> 
> _Seems to be a processing-in-memory play. From an[Andes Tech press release](https://www.andestech.com/en/2024/10/22/fractile-licenses-andes-technologys-risc-v-vector-processor-as-it-builds-radical-new-chip-to-accelerate-ai-inference/) detailing a partnership with Fractile:_
> 
> _“**Fractile’s uses novel circuits to execute 99.99% of the operations needed to run model inference in on-chip memory.** This removes the need to shuttle model parameters to and from processor chips, instead baking computational operations into memory directly. This architecture drives both much higher energy efficiency (TOPS/W) as well as dramatically improved latency on inference tasks (tokens per second per user in an LLM context, for instance). The company has been betting on inference scaling – leveraging more inference time-compute to improve AI performance – as the next frontier of AI scaling. The AI world seems to agree, with OpenAI recently releasing their latest LLM, o1, which requires orders of magnitude more inference compute than previous LLMs. Fractile’s hardware and software stack is built to take models that can still take many seconds to produce an answer on current hardware, and make this instantaneous._
> 
> _As part of the collaboration,**Fractile will integrate Andes Technology’s high-performance RISC-V vector processor with its own groundbreaking in-memory computing architecture** via ACE. Fractile’s architecture leverages the strengths of both companies, aiming to deliver an exceptionally fast and cost-effective AI inference system that overcomes the limitations of conventional computing methods – blasting through the memory bottleneck.”_

### Rivian spinoff Mind Robotics raises another $400M, two months after a $500M round

[Mind Robotics](https://www.mindrobotics.com/) is the industrial-robotics company Rivian spun out in 2025. Rivian’s CEO RJ Scaringe chairs it, and pitched the thesis to TechCrunch in March: existing robotics startups are not equipped to fully automate industrial work, so Mind Robotics is going after “robotics with human-like skills” for factory operations. The company first raised $115M from Eclipse at founding, then $500M two months ago, and is now adding another $400M led by Kleiner Perkins, with the venture arms of Volkswagen (Rivian’s software JV partner) and Salesforce also in. Total raised is now north of $1B at a >$3B valuation per WSJ. 

**Sources:** [WSJ](https://www.wsj.com/business/autos/rivian-ceos-robotics-spinoff-raises-400-million-4c54a9a0), [TechCrunch](https://techcrunch.com/2026/05/13/rivian-spinoff-mind-robotics-raises-another-400m/)

>  _**Austin:** Great anchor customer for Mind. Rivian co-designs and buys. A ton of conceptually similarities to mindmeld on too; Rivian’s EVs and autonomy already tackle perception plus motion in the physical world. The downstream story is great too. If Mind nails factory robotics automation, Rivian builds beautiful EVs at lower cost, funds more capacity, orders more robots. Tesla obviously pioneering this flywheel approach with Optimus too. Hope they both get it right._

### Quick Hits

  * **Cisco’s** networking segment was up 15% YoY in Q1 FY26 with Silicon One landing at four hyperscalers at triple-digit growth; management cited Acacia as the optics lever and disclosed Q1 hyperscale AI orders of $1.3B. Will also eliminate 4,000 jobs, or 5% of workforce. Investments in AI use among cited reasons. ([Cisco](https://blogs.cisco.com/news/our-path-forward))

  * **MediaTek** explores alternatives to TSMC CoWoS as Google pushes supplier diversification. ([digitimes](https://www.digitimes.com/news/a20260514PD217/mediatek-intel-asic-cowos-emib.html))

  * [FundaAI](https://open.substack.com/users/282947998-fundaai?utm_source=mentions) estimates that Qualcomm will start shipping LPU-like AI ASIC to a Chinese CSP by end of 2026. ASP $4,000, 1 million units, CPUs expected H2 2027. 




### Must Read

A nice interview with [Irrational Analysis](https://open.substack.com/users/135313705-irrational-analysis?utm_source=mentions) — with thoughts on various aspects of the AI supply chain.

[Chris Barber@chrisbarberhttps://t.co/Z5V4Li4QFE4:43 PM · May 14, 2026 · 292K Views

* * *

16 Replies · 79 Reposts · 648 Likes](https://x.com/chrisbarber/status/2054965791901319621?s=20)

## TIL: Gordon Teal was semiconductors greatest showman

In 1954, early transistors made of germanium were notoriously fragile and would stop working if they got too hot - around 75°C. The IRE conference in May 1954 in Dayton, Ohio, was basically a “Germanium Fan Club” meeting. The industry heavyweights onstage confidently explained that silicon is a pipe dream - too hard to work with, too expensive, and at least a decade away.

Gordon Teal, a recent Bell Labs defector who had moved home to work for a then-obscure Texas Instruments, had heard enough. He stood up for his talk and deadpanned: _“Contrary to what my colleagues have told you... I happen to have a few silicon transistors in my pocket.”_

Teal set up a record player and a beaker of hot/boiling oil (or glycerin - the accounts vary). He chose glycerin because it’s clear - he wanted the engineers to actually see the “impossible” happen. He fired up Artie Shaw’s jazz hit “Summit Ridge Drive” through a germanium amp and dunked it. The music instantly cut to static. Then came the flex: he swapped in his silicon transistors and plunged them into the beaker.

The music never missed a beat.

Then, madness ensued. When Teal mentioned he had mimeographed copies of his research at the back of the hall, the crowd triggered a literal stampede. Legend has it that a panicked competitor was heard screaming into a lobby payphone: _“They’ve got the silicon transistor down in Texas!”_ while the final speaker - Victor Moore of Raytheon - presented to a room of empty chairs.

While Bell Labs had shelved the tech as “commercially unattractive,” Teal rushed them to market for **$120 a pop** (about 50x the price of germanium) according to legend. That’s how you mic drop in physics.

[](https://substackcdn.com/image/fetch/$s_!fL19!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74791892-4a8b-4aae-8a87-242bc8ba79c4_197x255.png)Source: Bloomberg

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-may-15th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
