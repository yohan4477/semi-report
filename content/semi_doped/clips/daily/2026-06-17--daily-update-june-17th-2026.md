---
source: https://daily.semidoped.com/p/daily-update-june-17th-2026
title: Daily Update - June 17th, 2026
date: 2026-06-17
kind: clipping
genre: daily
audience: everyone
subtitle: Intel 18A-P risk production, TSMC's glass CoWoS bet, Amkor 10-year US packaging pact, AR optics, more
---
This week, we’re diving deep into advanced packaging, with TSMC making a big move by opting for glass substrates in their CoWoS packaging for next-gen AI chips, while also locking in a decade-long US packaging commitment with Amkor. Meanwhile, Intel’s 18A-P process is hitting risk production, and Applied Materials is teaming up with EssilorLuxottica to push the boundaries of AR optics. Lots of interesting developments across the stack!

Let’s get into it. _—Austin & Vik_

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Subscribe

 _Be sure to check out the[Semi Doped podcast](https://www.youtube.com/@semidoped) on YouTube or your favorite podcast player!_

### Intel 18A-P Enters Risk Production

Intel Foundry told the 2026 VLSI Symposium in Santa Clara on June 16 that Intel 18A-P, the first performance enhancement in the Intel 18A family, has entered risk production on schedule, hitting the timeline Intel gave customers and partners last year. The company also outlined longer-term process roadmap milestones and continued investment in future node innovation. ([Intel Newsroom](https://newsroom.intel.com/intel-foundry/intel-foundry-details-process-milestones-future-innovation-at-vlsi-symposium))

> _**Vik:** Always good to hear progress on the Intel 18A front. It’s EMIB packaging story is very strong, and the world needs an alternative to TSMC’s 2nm/3nm which is vastly oversubscribed. Chips makers will jump at the opportunity._
> 
> _**Austin:** 18A-P shows Intel listening to customers. New transistor width options for power-sensitive circuits, a fifth VT, and the Power Boost dual contact on the widest transistors where it matters most on a critical path. Each one is a new knob. More ways to trade power for performance, more flexibility to hit a PPA target without starting over. That’s how mature foundry PDKs work._
> 
> _The thermal improvements were co-developed with EDA vendors, so they land inside existing design flows rather than requiring new tooling. Again, good sign of Foundry maturity and another strong signal from EDA partners that they believe 18A-P customers are coming._

### TSMC picks glass CoWoS over panel for largest AI chips

TSMC said wafer-level CoWoS packaging will remain its preferred path for the largest AI processors, with panel-level packaging unlikely to replace it in the near term. The foundry pointed to CoWoS scaling to as many as 58 dies in a single package, and flagged glass substrates as the next step because their thermal behavior more closely matches silicon than organic substrates do. Mass production of glass-based CoWoS remains some distance away, with TSMC continuing to lean on existing wafer-level processes to serve customers including Nvidia, AMD, and Broadcom while panel packaging stays positioned for smaller, lower-end chips. ([Wccftech](https://news.google.com/rss/articles/CBMi1AFBVV95cUxObXZocE9jTVFuWHlnbXBlclpsRlNzTnUweDNGM1ItS0VDQ1ZkM1NKRUJjVTRnbU9TTUNqc2V6Ulo1bDJ4M1doVDM2RXpjcWI5UmJXUDFBNlpzR2tqNG9ac2ZfTWxaQUJJN2NJd0RJMVI4THVhNnJZampDLUlaWEoycDJwR3k5T0oxcEdxV05HaXZLbl9QOUNRQnVfcjJ3YzUyTDZ0R0Z5VDNrQm90R2FhMGdrenhlUnZSQmJEX1NIS3RYa0ZHTnNGMHVOY2twNWRPWTRuMtIB2gFBVV95cUxOZF83eU9IZ2tWa2xzZnduOGZDcHVJbG1RN1Y5RTVXeEprVzEyNktfRmRKbU9lT1hrNTZfOEoxbk15Y3ladURBbk9kMTFkdnJkVzNhRlFqM3ZvY2I0Ukt1eVFPTVllQm1hVURyaGhuUlF1anFteUhyblkzb2tpWEFQdVFvMmNUenBaaXlNcTFWa1BKOTgtVkZFa1Z3YjBwN2FQR1hoLUd3RWVKdmtocWRaYlZVQkJrRVVVSjV4a3lTLUtmelUyYnJLcXFibnpNa1YwUTN4WHowMWxaUQ?oc=5), [Tom’s Hardware](https://news.google.com/rss/articles/CBMiuAJBVV95cUxQRFZGVWZjek51em5mRDVSMGZfZ0J2TzV2UGpBUmpUNUU0aGJhR01DblZCem9aS0J0Z0tQaE5GUld0UzR5ZllsOG1vZDBNT1BXTV9WdElOVlZEbE4tbGJiMktVN0x6aml3WGRJZ3gyQUxpQ0k1aHFqejRaU1hndElSemdTNzI4SGJWTUl5a1FLNzlhVjZTVnQyN1VSaGFzaU5LajRDSjgzRmNBdUhGci02aWJuUDJ4WDBOVTdpUWVzZEJLOGFpWHdLRUhnaXhlRGdlZUNVWmVKTV9oaHB1dkk1LUQ5RzVEUW84RG9yU3Jkc0JfU05jckZySVd4Sjk3U2V3UVNyZThPN1E5aktDZTNvTEVrY3pOUUduRnVNdGlzakZNalBtTGx4WEgwLS1VTkhVVnQxTklNS1Q?oc=5), [Let’s Data Science](https://news.google.com/rss/articles/CBMipAFBVV95cUxORjNwMzBuVXA4MmtqUm9KaW1LdlVXcUtCRE1wTks0emt5ZEotS05mUlBxaF9FY2lnUFRxVXBPVHhiUmt2NXR6dGRNWEpDZ2JGazBxZ194WTlWa0FnbmxxUkRlMHU2Z0RpU0xYZGJMbnFRUUwwWE1VTkpKY2VudHphempaOFJrRlZuM0lhV1lwS1V5WjAwa3ozdEg1LWVzQ2tZaXhBNA?oc=5))

> _**Vik:** Wait, what? Ok, I do agree that CoWoS may have some more time overall given that Rubin still only requires 5.5x reticle size packages, but does TSMC really think CoWoS will actually scale to 14x reticle size? I don’t buy it. They’re going to have to go to glass panels. They’re undermining the fact that Intel EMIB already is on rectangular panels, which is a massive advantage going forward._

### TSMC, Amkor ink 10-year US packaging pact

TSMC and Amkor Technology announced a 10-year partnership to expand advanced semiconductor packaging and test capacity in the United States. The agreement, disclosed jointly from Hsinchu and Tempe, Arizona, is aimed at building out domestic back-end capabilities to complement TSMC’s Arizona fab investments. Financial terms were not disclosed. ([Amkor Technology](https://ir.amkor.com/news-releases/news-release-details/tsmc-and-amkor-technology-announce-long-term-partnership), [Semiecosystem](https://news.google.com/rss/articles/CBMiggFBVV95cUxQN3pSV3gyVXpSc2dYc0EzeWRrN2oza0Vqam96cHN4dG05VENIWERkdUd3VXhJejZYUFgtWkxpM1NfdkVOelRtX1laQmJMdmplREdoZEVMbnphVi0wSGh3cmctMXVyaDZfWEl2R2w1Uk50YkwwQVBjUnVKczlwcWFtODh3?oc=5))

> _**Vik:** Amkor is the arms dealer for advanced packaging here. They have partnerships with both TSMC for CoWoS and Intel for EMIB. I have a [full deep dive](https://open.substack.com/pub/viksnewsletter/p/battle-for-advanced-packaging-tsmc-intel-amkor?r=222kot&utm_campaign=post-expanded-share&utm_medium=post%20viewer) on this dynamic, if you’re interested._

### AttoTude raises $52M Series C

[AttoTude](https://www.attotude.com/) raised $52 million in a Series C round to scale its terahertz interconnect technology for AI infrastructure. The company is developing connectivity solutions aimed at addressing bandwidth bottlenecks in AI data centers. ([Pulse 2.0](https://news.google.com/rss/articles/CBMiogFBVV95cUxPUHEtdEdhTWZ4VnE2dGllVEdjdzYxUTd1RnMyeTRJcG5oYnRmX3V6QVhranBuQ1A1RFU2ZkliZ0UweXdNYkVLbG03VGdQOGI4aXV0TjFxeThjY2NuVlltYUtoMWVfbHRQalJRQ1AzdTlXYU8xb2VoOGt6QlBvcG9XdVJta0dETVk4ZFBHUUIwdmJHNWE2SVl4MHVURzRuNTk3SGfSAaIBQVVfeXFMT1BxLXRHYU1meFZxNnRpZVRHY3c2MVE3dUZzMnk0SXBuaGJ0Zl91ekFYa2pwbkNQNURVNmZJYmdFMHl3TWJFS2xtN1RnUDhiOGl1dE4xcXk4Y2NjblZZbWFLaDFlX2x0UGpSUUNQM3U5V2FPMW9laDhrekJQb3BvV3VSbWtHRE1ZOGRQR1FCMHZiRzVhNklZeDB1VEc0bjU5N0hn?oc=5), [citybiz](https://news.google.com/rss/articles/CBMivgFBVV95cUxQajhsQlJJWXhkRDNCMnF4dWR4SzZha1RqUGhxcmJMcFNuVDJNVGJyODYtVjZPVzlKeDM3aXVPSi1jenRLWnc5NHBLci1iNUlVcE9Vc2s0ajNmWEhsYTkzZzVKLXNUS1lFeXVGMmdzV05Ndkp1bDhhREFhQmwwY1JTLTctVlQ2R2tQNnBsT1B0b2lFSjV2OEVpOHFLcFFDNS1hT0RaZFBtZGEydmpad0xYN1JIQ3dkWGRjLWp6eDVn?oc=5))

> _**Vik:** This company is using THz RF for datacenter interconnects. I saw their CEO Keynote at IMS 2025. The search for InP alternatives for scale-up interconnect continues. We heard news about VCSELs, MicroLEDs. RF is just another way._

### Nokia Doubles Pennsylvania Chip Packaging Footprint

Nokia announced an expansion of its advanced test and packaging operations in Allentown, Pennsylvania, aimed at increasing domestic production of optical networking components used in AI infrastructure. The company said the investment will nearly double its Pennsylvania workforce to more than 500 engineering, manufacturing, and R&D jobs, with a projected economic impact exceeding $500 million over five years. Nokia noted that less than two percent of global semiconductor advanced test and packaging currently takes place in the United States. ([Nokia](https://www.nokia.com/newsroom/nokia-announces-major-expansion-of-us-semiconductor-advanced-test-and-packaging-in-pennsylvania-to-bolster-ai-growth/))

> _**Vik:** Nokia expanding optical packaging facility is a good sign for the company. The AI optical race places a lot of business squarely in their realm of expertise._
> 
> _**Austin:** Nokia! _
> 
> [](https://substackcdn.com/image/fetch/$s_!AqTu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feedc9c8e-572e-4dce-b514-341ee340ab8f_960x1280.jpeg)

### Applied Materials, EssilorLuxottica partner on AR optics

Applied Materials and EssilorLuxottica signed a joint development agreement to advance optical systems for smart eyewear and augmented reality lens stacks. The partnership pairs Applied Materials’ materials engineering capabilities with EssilorLuxottica’s expertise in lenses and smart eyewear, targeting lightweight next-generation AR optics. The companies said the collaboration aims to accelerate commercialization of intelligent optical platforms for the smart glasses category. ([Applied Materials](https://ir.appliedmaterials.com/news-releases/news-release-details/essilorluxottica-and-applied-materials-join-forces-advance))

> _**Vik:** I don’t think these smart glasses will catch on. Sorry. Have you seen [SNAP’s recent announcement for smart eyewear](https://newsroom.snap.com/introducing-specs-augmented-reality-glasses)? They’re UGLY AF. I wear glasses and won’t be caught dead wearing them. I’m not even style conscious._
> 
> _**Austin:** LOL. I’m gonna get some to troll you on the podcast. _

### Stock Movers (June 16)

**Up:** CRWV +9.7%, WDC +4.2%, NBIS +1.9%  
**Down:** MRVL -9.8%, MU -6.2%

## **Worth a Watch**

**[This Perfectly Silent Fan Took 300 Years to Make](https://www.youtube.com/watch?v=Q9FiuoXzEEA)** — Linus Tech Tips

Linus Tech Tips visits [Ventiva](https://ventiva.com/), a company commercializing an ionic wind cooling module that moves air silently with no moving parts. The video walks through how the 300‑year‑old physics works, demonstrates a fanless AMD Strix Halo laptop reference design running at 28 watts, and explains why the real value isn’t just silence — it’s the board space and PCB cost savings that ionic coolers unlock for next‑gen SOCs with large local memory.

[Watch on YouTube](https://www.youtube.com/watch?v=Q9FiuoXzEEA) ·[ Transcript on Chipstrat](https://www.chipstrat.com/p/this-perfectly-silent-fan-took-300)

## Quick Hits

  * **Coherent** announced a CHIPS Letter of Intent for $50 Million to expand its manufacturing facility for AI infrastructure. ([Coherent IR](https://www.coherent.com/news/press-releases/a-chip-letter-of-intent-for-50m-to-expand-world-leading-manufacturing-facility-for-ai-infrastructure))

  * **Vertiv** completed the acquisition of ThermoKey, expanding its heat rejection portfolio for AI data centers. ([Vertiv IR](https://www.vertiv.com/en-us/about/news-and-events/corporate-news/2026/vertiv-completes-acquisition-of-thermokey-expanding-heat-rejection-portfolio-for-ai-data-centers/))

  * **Nvidia** explores a compute futures market. ([Bloomberg Tech](https://www.bloomberg.com/news/videos/2026-06-15/the-race-to-build-a-compute-market-bigger-than-oil-video))

  * **SK Hynix** expands HBM4 packaging, potentially with Nvidia. ([DigiTimes](https://www.digitimes.com/news/a20260615VL201/sk-hynix-nvidia-hbm4-demand-packaging-equipment.html))

  * **Omdia** reports the semiconductor market surpassed $300B in 1Q26. ([Semiconductor Digest](https://www.semiconductor-digest.com/omdia-semiconductor-market-surpasses-300b-quarterly-revenue-in-1q26-as-memory-market-shifts-historical-patterns/?utm_source=rss&utm_medium=rss&utm_campaign=omdia-semiconductor-market-surpasses-300b-quarterly-revenue-in-1q26-as-memory-market-shifts-historical-patterns))




Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/daily-update-june-17th-2026?utm_source=substack&utm_medium=email&utm_content=share&action=share)
