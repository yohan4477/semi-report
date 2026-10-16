---
source: https://daily.semidoped.com/p/til-in-1979-82-chip-designs-went
title: TIL: In 1979, 82 chip designs went from the ARPANET to packaged silicon in 29 days
date: 2026-09-19
kind: clipping
genre: til
audience: everyone
subtitle: Most of the people who drew them had been learning chip design for about three months. 
---
At ten in the morning on December 5, 1979, someone from Xerox PARC carried a set of merged mask data to a shop called Micro Mask, Inc.

The deadline had been five o’clock the previous afternoon. The file held 82 separate chip designs by 124 designers, packed into 12 die types across two wafer types, gathered over the [ARPANET](https://en.wikipedia.org/wiki/ARPANET). Students at MIT, Caltech, Stanford, Illinois and Rochester had spent six or seven weeks learning how to design silicon and six or seven more actually doing it. Faculty and research staff at Berkeley, CMU, Yale, Washington, Colorado Springs and Bristol threw in bigger projects. [Alan Bell ](https://en.wikipedia.org/wiki/Alan_E._Bell)put them all together.

[![](<../_img/2026-09-19--til-in-1979-82-chip-designs-went/001_a582c8d7-3ac6-4910-921e-c71057714674_2509x2454.jpeg> "https://substackcdn.com/image/fetch/$s_!oWIr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa582c8d7-3ac6-4910-921e-c71057714674_2509x2454.jpeg")](https://substackcdn.com/image/fetch/$s_!oWIr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa582c8d7-3ac6-4910-921e-c71057714674_2509x2454.jpeg)The VLSI Technology VL82C486 Single Chip 486 System Controller incorporates several devices essential to the implementation of a intel 486 based PC/AT-compatible computer system. By Antoinebercovici - Own work, CC BY-SA 3.0, https://commons.wikimedia.org/w/index.php?curid=29023368. 

Micro Mask wrote the patterns with an electron beam. The first mask of each set reached Hewlett-Packard’s Integrated Circuit Processing Laboratory at five in the afternoon on December 6, by which point HP had already started running wafers. Then a poly-deposition system failed, costing about eight days of repairs, and Christmas cost more. One wafer set came out December 28, the other December 31. Packaged chips, wire-bonded individually for every project, shipped January 2, 1980.

Twenty-nine days.

If a design fit its space allocation, had syntactically correct code, and was submitted as finished before the cutoff, it went on the wafer. If you look closely at the bonding maps PARC sent back, you can find where somebody made a last-minute change and broke their own chip. Conway’s own documentation calls them glorious disasters. 

To understand why this was heresy, you have to remember what chip design looked like before. You cut your circuit into red Rubylith film with an X-Acto knife, and the whole time you were thinking about doping profiles and electron mobility and whether the lithography could actually resolve the thing you had just drawn. Design and manufacturing were the same job, held by the same small priesthood. That group of hallowed priests controlled who got to build anything.

[Carver Mead](https://en.wikipedia.org/wiki/Carver_Mead) at Caltech and [Lynn Conway](https://en.wikipedia.org/wiki/Lynn_Conway), who ran the LSI Systems group at [PARC](https://en.wikipedia.org/wiki/PARC_\(company\)), spent the mid-1970s saw a wall approaching. If chips kept getting denser, drawing them by hand while worrying about physics would eventually choke Moore’s Law to death. They figured the only way out was abstraction, where you had to start treating it like software. Their answer was to throw out the physics and keep the geometry. Conway’s design rules were dimensionless, scaled by a single variable called lambda. Draw rectangles, obey the ratios, and the chip works. Nobody had to explain a lithography tool to a computer science graduate student ever again.

[![](<../_img/2026-09-19--til-in-1979-82-chip-designs-went/002_166b99e5-9824-49c1-9859-b38b605c6d66_751x1000.jpeg> "https://substackcdn.com/image/fetch/$s_!lbB1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F166b99e5-9824-49c1-9859-b38b605c6d66_751x1000.jpeg")](https://substackcdn.com/image/fetch/$s_!lbB1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F166b99e5-9824-49c1-9859-b38b605c6d66_751x1000.jpeg)By Charles Rogers - http://ai.eecs.umich.edu/people/conway/LynnPhotos/Lynn2006.jpg, CC BY-SA 2.5, https://commons.wikimedia.org/w/index.php?curid=4100989

The reaction inside the industry was roughly what you would expect. Conway's own notes record the push-back against what critics were calling toy methods, and some of it came from inside PARC.

Then came the next big problem: designing chips is cheap; fab-ing them costs a fortune. So Conway sucked all 82 student designs back across the ARPANET, compiled them into one massive master file, and crammed them onto a shared piece of silicon — the multi-project wafer (MPW).

She taught it anyway during the Fall of 1978, as a visiting associate professor at MIT, from a near-finished draft of the textbook. That December the class sent 19 projects to PARC over the network and got packaged silicon back on January 18. Then she went bigger. In spring 1979 she specified what amounted to an operating system for the whole pipeline: take design files from remote users, juggle space allocation, drive mask-making and fab and packaging against a deadline. Bell and [Martin Newell ](https://en.wikipedia.org/wiki/Martin_Newell_\(computer_scientist\))architected it over the summer and coded it that fall. MPC79 was the load test, four times the projects, on a broken fab, over a holiday.

When it held, the system moved to USC’s Information Sciences Institute and became MOSIS in 1981. _[Introduction to VLSI Systems](https://en.wikipedia.org/wiki/Mead%E2%80%93Conway_VLSI_chip_design_revolution)_ was in use at nearly 120 universities by 1983. Stanford’s[ James Gibbons](https://en.wikipedia.org/wiki/James_F._Gibbons) later wrote that Conway was the singular force behind the entire foundry development that followed.

The MPC79 run birthed the fabless silicon industry, and Carver Mead became a Silicon Valley legend. But Lynn Conway did not become a household name alongside Wozniak or Torvalds. 

To understand why, you have to look at what happened eleven years earlier at IBM.

In 1968, Conway was a rising star in IBM’s secret Advanced Computing Systems division. She was the primary architect of a concept called dynamic instruction scheduling. It is a trick that allows a computer to execute commands out of order to save time. In fact, every modern laptop and smartphone on earth still relies on it.

The Computer History Museum says ACS appears to have been the first superscalar design. It was also secret, and then cancelled. [Robert Tomasulo](https://en.wikipedia.org/wiki/Robert_Tomasulo)’s single-issue scheme, published in 1967, got the textbook name and an Eckert-Mauchly Award. Conway’s work sat in classified memos for decades.

She had resumed hormone therapy in 1967 under [Harry Benjamin](https://en.wikipedia.org/wiki/Harry_Benjamin)’s care. In early 1968 she told a supervisor. Then IBM fired her.

They erased her name from the history of computer architecture. She lost her career, her security clearance, and her social support network in a single afternoon.

_Aside: There are some stories that suggest that her direct managers wanted to keep her and worked out a plan where she would take leave, finish transitioning, and come back as a new employee under a new name. Then IBM’s corporate medical director found out and alerted Thomas J. Watson Jr. In August 1968, in Gene Amdahl’s office in Sunnyvale, she was fired. She and her wife divorced that year, and under the_ _custody law of the time she was denied access to their two daughters._

Conway had to start over from absolute zero and started with a low-level contract programming job under her new name. She lived in deep stealth, terrified that if anyone looked too closely at her background, she would be outed and fired again.

Thanks for reading! Subscribe for free to receive new posts and support our work.


Historians did not find her. She retired and learned that a Clemson professor named [Mark Smotherman](https://mark.people.clemson.edu/homepage.html) was reconstructing the ACS story and would publish it, and decided to tell it first. She came out in 1999 and put the whole thing on her own website.

IBM apologised in 2020, at a public event, with a lifetime achievement award attached. She was 82. It had only taken them 52 years.

Thanks for reading! This post is public so feel free to share it.

[Share](https://daily.semidoped.com/p/til-in-1979-82-chip-designs-went?utm_source=substack&utm_medium=email&utm_content=share&action=share)
