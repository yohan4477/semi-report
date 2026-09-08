---
source: https://daily.semidoped.com/p/daily-update-may-8th-2026
title: Daily Update - May 8th, 2026
date: 2026-05-08
kind: clipping
genre: daily
audience: everyone
subtitle: ams OSRAM and optical interconnects, will supply chain limit Arm? Memory tax validated, a story of Mr. Clean.
---
Lots of players are getting into the “wide-but-slow” business in optical interconnects. Arm has serious AI CPU demand, but can they build chips fast enough? And other easy reading bits and bobs.

Let’s hit it.

_Thanks for being one of our first fans! We’re up to 750!_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

* * *

### ams OSRAM bets on “slow and wide” parallel optics for the AI rack

[ams OSRAM](https://ams-osram.com/) signed a development agreement with a “leading AI data center infrastructure partner” to commercialize what the company calls “slow and wide” optical interconnects: highly parallel micro-emitter arrays running at 8 gigabit per channel across hundreds of parallel channels.

Most optical interconnects are “fast and narrow” and accelerated by power-hungry serializers and deserializers. It seems Osram is building the inverse: drop the SerDes, replace serial speed with parallel channels, and transmit light pulses at chip speed across an emitter array. CFO Rainer Irle said the initial focus is on shorter-distance scale-out interconnects (rack to rack), then scale-up within racks replacing copper over distances up to several tens of meters, and eventually chip-to-chip connections between GPUs and HBM.

[](https://substackcdn.com/image/fetch/$s_!Be36!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F78dc74db-7003-4344-bd6d-2b77e74617ac_1344x738.png)

[](https://substackcdn.com/image/fetch/$s_!4Qe0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5c8b1e1a-6caa-48fc-983e-74f6c54f2a49_1340x748.png)

ams OSRAM gave specific power numbers for the alternatives. Today’s pluggable transceivers and active optical cables consume up to 30 picojoules per bit. Near-port optics gets to 5 to 10 pJ/bit. Co-packaged optics targets 1 to 5 pJ/bit. The slow-and-wide approach achieves low pJ/bit not by moving the engine closer to the ASIC but by removing the power-hungry SerDes entirely.

The other claimed advantage is inherent redundancy: with hundreds of parallel channels, single-emitter failures degrade gracefully rather than knocking a link offline, which matters for hyperscaler uptime SLAs.

The partner is not exclusive. Rebel: _“It’s not only on a similar integration level that we are speaking, but basically we’re speaking with everyone.”_

On revenue: Osram said the AI-datacenter opportunity is _“a EUR 3-digit million opportunity in 2030 and beyond, with a gradual ramp”_ if the company supplies just emitters, and could be _“obviously a much higher number”_ if the program expands to photodiodes, drivers, and amplifiers. First revenue is targeted for _“before 2030, hopefully before 2029.”_

>  _**Austin:**_ _When I hear “slow and wide” I think of microLEDs, like[Avicena](https://avicena.tech/) or [Credo (Hyperlume)](https://investors.credosemi.com/news-events/news/news-details/2025/Credo-to-Acquire-Hyperlume-Inc-/default.aspx). _
> 
> _But then I though maybe this based on VCSEL arrays? ams OSRAM’s VCSEL business runs back through the OSRAM Opto Semiconductors side, including Apple Face ID dot projector, smartphone proximity sensors, automotive LiDAR sources, and datacom transceiver lasers. Touched on this the other day at Chipstrat:_
> 
> [ ChipstratVCSELs + 200G Wall In AI Datacenters?Coherent has lately been talking about parallel-pathing the light source for 1.6T transceivers, developing solutions based on SiPh (silicon photonics), EMLs (electro-absorption-modulated lasers), and VCSELs (vertical-cavity surface-emitting lasers). From the recent earnings call…Read more4 months ago · 12 likes · Austin Lyons](https://www.chipstrat.com/p/vcsels-200g-wall-in-ai-datacenters?utm_source=substack&utm_campaign=post_embed&utm_medium=web)
> 
>  _And ams OSRAM management used “microLED” elsewhere on the same call when describing smart-glasses displays, but deliberately switched to “micro-emitter array” for this AI program… so maybe VCSELs?_
> 
> _But then a friend looked at the image in the slides and said it looked like uLEDs:_
> 
> [](https://substackcdn.com/image/fetch/$s_!8FqF!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8fb0058f-ff5c-4d87-91b0-adc14ed62b02_2118x1158.png)
> 
> _That’s surprising. ams OSRAM is already the[high-volume manufacturing partner for Avicena’s GaN MicroLEDs](https://avicena.tech/avicena-partners-with-ams-osram-to-enable-high-volume-future-production-of-ultra-low-energy-chip-to-chip-interconnects/). Does this have anything to do with Avicena, or is it a completely different thing, with the hyperscaler working directly with ams?_
> 
> _**Vik**_ : _InP lasers for shorter reach is overkill, and supply chain is F-ed. Lots of reasons to go either microLED or VCSEL arrays. Question is which one?_

### Arm Has the Demand. Does The Supply Chain?

Per Arm’s recent earnings call, AGI CPU customer demand has more than doubled since the launch six weeks ago. Yet Arm is keeping the FY26 revenue outlook flat while it secures the supply needed to fulfill the new pipeline.

> **Jason Child, CFO:** _“As Rene mentioned, customer demand for the Arm AGI CPU is very strong. We now have line of sight to more than $2 billion of demand across fiscal ‘27 and ‘28. However, we are maintaining our outlook of $1 billion while we pursue supply chain capacity, and we still expect the first revenues from production chip sales to land in the fourth quarter of this fiscal year.”_

Can Arm actually build the chips in time? It’s “working around the clock” to pull it off:

> **Rene Haas:** _“The number that we talked about at end of March was supply in place to support $1 billion of demand, and that includes memory, that includes wafers, that includes packaging, that includes access to test equipment. So for the $2 billion, we are now in the process of securing supply to support that. And the teams are working around the clock to make sure we can find the right answers for our customers.”_

Building chips has much lower margins than selling IP… but if you build the IP already, it might not be as expensive as you’d think for Arm to take CSS to final taped out chip: 

> **Jason Child:** _“The most expensive part of developing a chip is really the compute die, which really is effectively kind of the CSS. So we’re able to leverage that, and that automatically makes this business much more profitable as a stand-alone chip business given that we get that work as part of our IP business already. So the incremental costs and OpEx that we’re having to add to the chip business is not that significant.**It’s a team that’s in the dozens of people, not hundreds.** And so you can assume that it’s operating profit positive next year.”_

Dozens of people, not hundreds!

> _**Austin:**_****_The existing IP business is paying a large portion of the chip development cost, that’s pretty sweet. Or you could look at it from the inverse angle: the chip business is funded by licensing its internal IP to external customers too._

### Key Data

We covered the “memory tax” on a Semi Doped episode. This chart shows just how true it is.

#### [🎧 CapEx is just Memory Tax Now, Deepseek V4 NAND impact[Semi Doped](https://substack.com/profile/500274950-semi-doped)·May 4[Read full story](https://www.semidoped.com/p/capex-is-just-memory-tax-now-deepseek)](https://www.semidoped.com/p/capex-is-just-memory-tax-now-deepseek)

[](https://substackcdn.com/image/fetch/$s_!oBDh!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc1322070-66be-4ca9-87b4-45e786ded12d_1920x1240.png)

### Eye Candy

These things are beautiful to look at. See the honking black cables between racks? That’s scale out. Anyway, this is Meta Catalina from a year ago, Custom build based on GB200. It uses a 1:1 CPU:GPU ratio. 

[](https://substackcdn.com/image/fetch/$s_!u11z!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F18d6ca22-fccf-4b40-8a4e-e5874c0537f4_1783x1003.jpeg)Courtesy: Dr. Ian Cutress on X.

For more images, see [here](https://x.com/IanCutress/status/2052363398029926726?s=20) and [here](https://x.com/IanCutress/status/2052363859428581603?s=20).

### TIL: The Semiconductor Industry Exists Because One Guy Got Annoyed by Dust

Everyone knows the transistor, but almost nobody knows the environment required to build one. Before 1960, “clean rooms” were a disaster. Even the most advanced labs were filled with over 1,000,000 particles of dust per cubic foot - a literal minefield for microscopic circuitry.

Enter [Willis Whitfield](https://en.wikipedia.org/wiki/Willis_Whitfield) (fondly called Mr. Clean), a physicist and son of cotton farmers who learned engineering by fixing farm equipment. While working at Sandia National Laboratories, Whitfield realized the industry’s fatal flaw: they were trying to trap dust instead of removing it.

His “Aha!” moment came on an airplane, where he sketched a solution in five minutes: Laminar Flow. His insight was brilliantly simple: stop fighting the particles and instead “let the air be the janitor.” By blowing a constant, ultra-filtered curtain of air from the ceiling to the floor, he effectively swept the room clean every few seconds.

The results were so radical they were scary. His prototype brought the particle count from 1,000,000 down to 750. It was so clean that fellow scientists initially thought his measuring instruments were broken!

Despite enabling a global industry now worth hundreds of billions, Whitfield never got rich. Because the U.S. government placed the patent in the public domain. He later helped NASA sterilize spacecrafts, but his true legacy is the “invisible infrastructure” of the modern world. From TSMC’s fabs to your phone’s OLED display, we are all living in a reality made possible by a five-minute sketch and a man who hated dust.

[](https://substackcdn.com/image/fetch/$s_!Ha9I!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F60cf450f-4214-4720-848f-126890498bd0_2560x1700.jpeg)Willis Whitfield, aka, Mr. Clean. Source: Sandia Labs.

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-may-8th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
