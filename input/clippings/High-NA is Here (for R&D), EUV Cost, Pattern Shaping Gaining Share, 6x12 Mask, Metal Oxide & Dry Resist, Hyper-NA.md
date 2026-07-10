---
title: "High-NA is Here (for R&D), EUV Cost, Pattern Shaping Gaining Share, 6x12" Mask, Metal Oxide & Dry Resist, Hyper-NA"
source: "https://newsletter.semianalysis.com/p/spie2025"
author:
  - "[[DYLAN PATEL]]"
  - "[[JEFF KOCH]]"
published: 2026-02-05
created: 2026-07-10
description: "SPIE Advanced Litho & Patterning 2025 Round-Up"
tags:
  - "clippings"
---
 _“Lithos Graphein” is back as a guest contributor to this report. Follow him on twitter[ @lithos_graphein](https://twitter.com/lithos_graphein)_

If TSMC is “the most important company in the world,” according to President Trump, then EUV lithography tools are surely “the most important machines in the world.” Does that make SPIE Advanced Lithography & Patterning the most important conference in the world? Not exactly, but it’s at least a good opportunity to see the latest progress in EUV and advanced logic.

In this report we’ll cover the technology highlights and market implications from this year’s conference. High-NA was a main topic as real wafer volumes are being run on customer (Intel) tools. Complementary patterning techniques such as pattern shaping (AMAT Sculpta and TEL Acrevia) and directed self-assembly are picking up steam. And ASML itself is already on to the next topic: hyper-NA for the CFET era.

[![](https://substackcdn.com/image/fetch/$s_!FwD5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb68f3690-ee2a-4c9a-bdc5-d14924f1d188_828x458.webp)](https://substackcdn.com/image/fetch/$s_!FwD5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb68f3690-ee2a-4c9a-bdc5-d14924f1d188_828x458.webp)Source: imec

## **Manufacturing Readiness of High-NA EUV**

The highlight keynote was delivered by Steve Carson of Intel on the manufacturing readiness for their two fully installed high-NA EUV tools.  As a recap, Intel has gone all in on high-NA EUV, installing the first shipped tool, the EXE:5000, over a year ago and accepting a second shipment shortly after to get early learnings ahead of the competition.

Intel clearly views high-NA EUV as being a critical part of their product strategy for launching their 14A node, although they have said 14A is _possible_ with only low-NA. With a total of 30,000 wafers now exposed across two fully installed tools, they are in the best position to assess the viability of the new scanner in a manufacturing environment. The stated goal was to bring up a development pilot line with the new high-NA EUV system in record time, avoiding the slow ramp that plagued low-NA EUV.

[![](https://substackcdn.com/image/fetch/$s_!a-X0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F583a5911-29a9-40e6-9b6b-db44a7543999_1024x627.png)](https://substackcdn.com/image/fetch/$s_!a-X0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F583a5911-29a9-40e6-9b6b-db44a7543999_1024x627.png)Source: Intel

Several first-of-a-kinds for a new scanner technology were undertaken by Intel and ASML. The normal scanner build process is to assemble it at the ASML Veldhoven factory, where the fully assembled tool is tested to customer’s and ASML’s agreed specifications. The machine is then disassembled and shipped to the customer’s fab for install and reassembly. For the first high-NA tool, the factory integration and test were skipped. Instead, the first fully built tool testing was done directly at Intel.

This has not been done before and is unheard of for the first unit of a new scanner technology – the high-NA scanner is substantially different than low-NA. ASML and Intel collaborated on this process closely as much of procedures and methods for bringing up a tool and making it reliable were being learned for the first time.

However, a functional scanner alone is only a piece of the high-NA puzzle. The pilot line also required process, reticles (masks), and Optical Proximity Correction (OPC) to be ready on the aggressive 14A timeline. This is especially difficult as all 4 elements are interdependent, which means development must be done serially. This is where Intel was forced to innovate and parallelize as much as possible.

The process portion includes photoresist, where Intel used both low-NA NXE systems and Berkeley’s Microfield Exposure Tool to characterize and down-select the photoresist to be used with high-NA. The etch process for transferring the pattern from the resist down into the underlying materials stack is also normally decided at this point.

OPC is a complex software suite that is used to convert a chip design into complex shapes on a lithography mask. Typically, an OPC model would be calibrated using the actual scanner and POR (process of record) resist and etch to print real wafers. OPC models for device masks, often referred to as a “keyword”, require many of the process details to be known. They contain an etch bias table, thus, the etch process must have first been developed and characterized. The thru-pitch bias for a given illumination pupil, unique to the new scanner is also characterized for the new resist.

But at this point the high-NA scanner was not available. So Intel developed a novel method of calibrating OPC models without true wafer data. Instead, they used a combination of simulation and low-NA exposures that was extrapolated and used to tune a high-NA OPC model. This isn’t normally done as OPC models will have poor accuracy without calibration on wafer data, but Intel proved that it is possible.

[![](https://substackcdn.com/image/fetch/$s_!u9D1!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F38951c91-73a6-4cf0-855b-c006d10221f7_1024x643.png)](https://substackcdn.com/image/fetch/$s_!u9D1!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F38951c91-73a6-4cf0-855b-c006d10221f7_1024x643.png)Source: Intel

The OPC model was necessary to make high-NA reticles, which have smaller features and the new anamorphic setup versus low-NA. With OPC taken off the critical path, the reticles could be produced in time to meet scanner qualification and run the pilot line almost immediately. Traditionally this process takes many months after scanner acceptance – here Intel and ASML reduced it to nearly zero. A bring-up time this short on a brand new scanner technology is unprecedented.

## **High-NA Imaging Results**

With the scanner installed and masks in hand, Intel could characterize the tool. The basic metrics of source power and reliability were vastly exceeding targets for a new scanner system. Source power was 110% of the target, the first time a new EUV system has exceeded the initial target. For comparison the NXE:3300 development tool was just 15% and the NXE:3400B production system 50% of their target source powers at first shipment. ASML has actually gotten ahead of their source roadmap. Reliability was at 85%, which was also significantly better than any prior systems at this point in development.

Overlay performance was impressive – 0.6nm aligned to a low-NA tool. This exceptional performance across multiple tools is often taken for granted but is part of what makes ASML singular. It gives chipmakers flexibility to mix and match toolsets with good results, rather than limiting critical layers to the same tool or even same wafer chuck. Competitors are miles (nanometers) behind on this.

This overlay result was sufficient for Intel and ASML to declare that high-NA has no penalty for stitched fields. This has been a big concern as the high-NA optics limit field size, so stitching is required for large dies such as a GPU. Despite their declaration, it’s still an open question if fabless customers will accept a stitched die. Likely there will be design rule limitations in the stitching areas at the very least.

The consensus on photoresist thickness is that high-NA lithography will require significantly thinner film coatings which impacts the required optical depth-of-focus. Intel was able to make an assessment on this crucial process parameter that impacts manufacturability. Focus control for the new high-NA tools outperformed the low-NA NXE system which meets the target specifications.

Along with the core lithography performance, Intel shared early device data for metal and contact hole layers. Both are critical layers at 14A where high-NA EUV could tip the yield scales. For metal, the comparison used a single high-NA exposure to replace an existing metallization scheme comprising three low-NA exposures and more than 40 process steps in total.

It should be noted that the low-NA process uses pitch splitting with self-aligned double patterning (SADP) to shrink beyond low-NA EUV single-exposure limits. Intel refers to this as self-aligned litho-etch litho-etch (SALELE). SADP requires many process steps as it relies on ALD and a series of etches to split the metal pitch down to the desired geometry. The other two EUV exposures are used for cut masks that trim the lines from pitch splitting and also pattern the larger pitch metal features. High-NA replaces all this with a single exposure and many fewer process steps.

[![](https://substackcdn.com/image/fetch/$s_!sdAe!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2e1f253-4667-4808-88d8-e3727513d873_1024x589.jpeg)](https://substackcdn.com/image/fetch/$s_!sdAe!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fc2e1f253-4667-4808-88d8-e3727513d873_1024x589.jpeg)High-NA single exposure SEM images, post pattern transfer, for 1x metal routing. Source: Intel

For the contact-hole (CH) layer, Intel shared yield data showing similar yield with high-NA to an existing low-NA multi-patterning (LELE) process. For context, the early masks used to measure the health of a layer are notoriously bad at delivering promising results. Typically, a number of iterations of OPC and mask spins are required to get a live yield signal. So comparable yield between high-NA and the mature process is impressive at this stage.

They did not share the number of low-NA mask steps, nor the total number of process steps (more on this later). Our assumption is that this would be two passes of low-NA memorized into a hard mask prior to final etch transfer and metallization.

[![](https://substackcdn.com/image/fetch/$s_!fbyS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6ccd457-4257-402c-be4b-30bc2460c925_1024x541.jpeg)](https://substackcdn.com/image/fetch/$s_!fbyS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb6ccd457-4257-402c-be4b-30bc2460c925_1024x541.jpeg)Source: Intel

Last, Intel finished with a call to action on new mask infrastructure (more on this in the cost analysis section below) and a bold declaration that both of their high-NA EUV systems were now “in production.” This term means running test wafers on a proven process, not that high-NA scanners are running commercial products.

Likely the proven process used here is 18A, as it will be in the final stages of development and taping out mask sets with prospective customers, with the process steps mostly frozen. This serves as a convenient baseline for experimentation by swapping in high-NA for one or more critical layers. Comparison with the low-NA POR for 18A, well characterized at this point, gives valuable feedback towards 14A development.

This same concept is used to test many new technologies to vet them prior to production. In the case of low-NA EUV at 7nm, it was used to generate yield learnings before the cost made sense. The initial source power at that time was too low to make EUV competitive with DUV quadruple patterning.

## **High-NA Cost**

ASML’s latest high-NA system, the EXE:5000, weighs an astounding 150 metric tons and has a comparable price tag of nearly $400 million. It’s close to twice the price of a low-NA system, which directly translates to a higher cost of operation and ultimately wafer cost.

As we’ve discussed in our report on high-NA vs. low-NA multipatterning, equipment decisions are based on cost. While reducing complexity is good, it is not cheaper in every case. This is what was missing from Intel’s talk. Is it cheaper than low-NA LELE or SALELE?

Given they are “in production” with branch high-NA run paths comparing directly to these alternatives, they must know the answer. Intel along with imec and IBM are all pushing for high-NA to be adopted at the 14A node; however, being too early with a fleet of scanners to run your production line—at a price tag in the billions—could be just as detrimental as being too late with a new enabling technology.

SPIE organizers have a habit of placing the most important talks on Thursday afternoon, and one of them was by Luciana Meli from IBM, who presented the only talk addressing the 150-ton elephant in the room—is high-NA cost-effective?

IBM presented several key findings based on simulation and their work at the Veldhoven high-NA EUV lab. First, they determined the 14A layers with largest potential benefit from replacing multiple low-NA exposures with a single high-NA pass:

[![](https://substackcdn.com/image/fetch/$s_!7ojz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c44c075-ba74-40d9-b038-6858adeea0c8_562x188.png)](https://substackcdn.com/image/fetch/$s_!7ojz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F6c44c075-ba74-40d9-b038-6858adeea0c8_562x188.png)Source: IBM, SemiAnalysis

Their cost analysis focused on SALELE as it offers the highest cost savings potential, replacing three or four low-NA exposures with one high-NA. Details here filled in a few key items left out of Intel’s talks. First, the number of process steps in SALELE is roughly twice those needed for a high-NA single exposure. Recall that Intel indicated SALELE was approximately 40 process steps for their three mask process; thus, the number of steps in a high-NA module is still significant. For cost, IBM claims a four mask SALELE process is 1.7-2.1x more than a single high-NA pass. Not a surprising result but a good data point on cost – it was expected that high-NA single exposure would be cheaper than triple or quadruple low-NA exposures.

However, IBM also helped confirm our modeling on high-NA versus low-NA double patterning, suggesting that the low-NA option is cheaper. Their data shows a single high-NA exposure costs roughly 2.5x a single low-NA exposure. This strongly suggests that any cost-per-pass benefits for high-NA wouldn’t kick in unless three low-NA masks are reduced to a single high-NA.

Another interesting finding from IBM’s presentation was that a high-NA single exposure for a metal process might have trouble meeting the metal tip-to-tip design targets. Note that a low-NA SALELE process excels here with a dedicated cut mask defining the tip-to-tip features. IBM suggests that directional etch process technology, such as Applied Materials Sculpta tool, would be needed to augment this shortcoming – more on pattern shaping in a few sections.

## **High-NA 6 x 12” Mask**

The last slide of Intel’s plenary talk included a call to action for large high-NA masks. They’ve been beating this drum for a while but for good reason: a 6 x 12” mask, twice the 6 x 6” that has long been industry standard, would improve the scanner productivity by 23-50%.

[![](https://substackcdn.com/image/fetch/$s_!8bQj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fafa92cc5-4670-490b-bf53-d7ab67d6cbab_1024x567.png)](https://substackcdn.com/image/fetch/$s_!8bQj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fafa92cc5-4670-490b-bf53-d7ab67d6cbab_1024x567.png)A 6 x 12” mask improves throughput and eliminates the high-NA field stitching problem. Source: Intel

It enables full-field exposures, eliminating the stitching issue along with the throughput gains. Assuming a reasonable increase in scanner cost, this would swing the economics of critical layers to clearly favor high-NA.

[![](https://substackcdn.com/image/fetch/$s_!kHjE!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb582e243-e7e5-41c8-9ef4-c7fe08b128e4_1024x518.png)](https://substackcdn.com/image/fetch/$s_!kHjE!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb582e243-e7e5-41c8-9ef4-c7fe08b128e4_1024x518.png)Intel’s call-to-action for larger high-NA masks to improve productivity and reduce costs. Source: Intel

While Intel and others say the mask ecosystem sees no major showstoppers for large mask, the tipping point really depends on ASML. While the CEO Christophe Fouquet’s plenary at SPIE EUV last year was positive towards large masks, it wasn’t on the roadmap and the company didn’t formally state they can or will develop the capability. This year, ASML’s plenary talk went further, stating that the larger “ecosystem is progressing,” “impact studies were ongoing” and that it may be introduced sometime “early in the next decade.”

[![](https://substackcdn.com/image/fetch/$s_!VPBR!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1632cdf8-48a6-4e4c-a140-487c5ae60c59_1024x607.png)](https://substackcdn.com/image/fetch/$s_!VPBR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F1632cdf8-48a6-4e4c-a140-487c5ae60c59_1024x607.png)ASML acknowledged the possibility of large masks. Source: ASML

This is not a minor change. The 6 x 6” mask size has been standard since the start of projection lithography in the 1980s. All the tooling: blank manufacturing, resist coating, e-beam writing, mask cleaning, fab handling, etc. must be rebuilt for the new mask size. It’s the equivalent of moving from 200mm to 300mm wafers (recall that an attempted move to 450mm failed a decade ago). The timeline is surely beyond the ramp for the 14A node.

For ASML, the 6x12” mask is at odds with their core EUV systems strategy where they desire to make the NXE, EXE, and future hyper-NA systems on a common platform to streamline their production, one of which is the reticle stage and handling system. A large mask would require significant changes to these modules and probably disrupt the commonality.

[![](https://substackcdn.com/image/fetch/$s_!iDS9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F733977c4-c55b-4001-94a7-ecc63a927a14_1024x538.png)](https://substackcdn.com/image/fetch/$s_!iDS9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F733977c4-c55b-4001-94a7-ecc63a927a14_1024x538.png)Future EUV scanners will move to a common platform. Source: ASML

A large mask is also not directly in ASML’s economic interests. If the choice is between two regular mask high-NA scanners or a single large mask tool, selling two complete scanners is probably 200-300M more revenue for ASML. Developing a large mask tool would be extremely customer-friendly.

## **High-NA EUV: Insertion at 14A or 10A?**

At 14A, high-NA only offers a cost advantage in a few metal layers where it would replace three masks in Intel’s process. Note that TSMC is not necessarily using triple EUV exposures in its A14 process, this is specific to Intel. In other layers, Intel notes, it offers design flexibility and process simplification – advantages that are tangential to cost.

Is cost reduction on just three layers worth the risk of early insertion for a new technology? The reduction is real but small as a percentage of the overall chip process that is on the order of 100 layers. Intel itself has even said publicly that 14A is feasible _without_ high-NA, especially if customers were to demand it. But most signs so far point towards Intel adopting high-NA in critical layers at 14A. The inertia in the organization is probably too strong to change course now. And should the 6 x 12” mask be ready for a potential 10A process, making the economics very favorable, Intel would potentially benefit from early adoption. Its learnings and expertise on high-NA at this point are far ahead of competitors.

## **Metal Oxide Resist**

Metal-oxide resist (MOR) has been the “next up” EUV photoresist platform for a few years now. MOR resists offer much better Resolution-LER-Sensitivity (RLS) performance versus the mature organic chemically amplified resists (CAR). Sensitivity and line width roughness, or CD variance, are especially important for EUV because it’s photon limited. At the 13.5nm wavelength, relatively few photons are emitted by the source, but they are much higher power relative to DUV wavelengths. Small improvements in dose sensitivity can have a big impact on throughput and therefore operational costs.

However, as with any new technology, a photoresist platform change requires a lot of momentum to trigger industry-wide adoption. For existing nodes, the benefit was not large enough to induce a change.

[![](https://substackcdn.com/image/fetch/$s_!qozS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcc74f33c-fe5c-4380-964a-dd55cd23fb12_434x220.png)](https://substackcdn.com/image/fetch/$s_!qozS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcc74f33c-fe5c-4380-964a-dd55cd23fb12_434x220.png)RLS trade-off concept for photoresist performance. Source: Lawson et. Al. Overview of materials and processes for lithography

It looks like MOR’s time has finally come with the introduction of high-NA. Depth of focus is also one of the key drivers as it decreases with the square of numerical aperture (NA); meaning the high-NA scanner has a very small depth of focus. DoF is also affected by the illumination pupil, which must be optimized for a certain pattern to produce the best image. Unfortunately, the best pupil for smaller and smaller patterns often reduces DoF. The combination of lens NA and illumination pupil both reducing depth of focus produce a tipping point where very thin photoresist films are unavoidable.

The resist thickness must be smaller than the depth of focus so that the image is in focus through the entire height of the resist, or else the resulting pattern in the resist will be poor quality. Here is where a thin MOR resist will excel over thin CAR resist. The conventional CAR resist platform utilizes an organic acrylic polymer backbone (Carbon-Carbon chain) as the basis to block the etch for pattern transfer into a hard mask, such as Silicon Nitride (SiN). A thin organic polymer film doesn't have sufficient etch resistance to survive pattern transfer; however, a metal oxide resist provides much better etch selectivity to pattern transfer into most hard mask films. Therefore, MOR resists provide both better optical and etch performance over CAR.

[![](https://substackcdn.com/image/fetch/$s_!9VmW!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd5e470fd-32ae-48dd-a22a-aea6f91da0cf_722x811.jpeg)](https://substackcdn.com/image/fetch/$s_!9VmW!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd5e470fd-32ae-48dd-a22a-aea6f91da0cf_722x811.jpeg)Resist thickness becomes a challenge as depth of focus decreases. Source: ASML

Taking the example of vias, tightly patterned holes that will be filled with metal to form interconnects between metal layers, the crossover point looks to be somewhere in the range of 30nm pitch. Vias will probably scale to this pitch ~2 nodes from now, at the A10 process. This matches with our expectation for when it is [economical to introduce high-NA](https://semianalysis.com/2023/12/11/asml-dilemma-high-na-euv-is-worse/). In other words, it will probably make sense to adopt MOR at the same time as high-NA for a small number of critical layers like metals and vias. Most SPIE papers this year with high-NA exposure data used MOR rather than CAR.

## **Wet vs. Dry: Resist Coating**

Additional research is ongoing that will decide the war for the future of photoresist. To be decided is whether wet or dry application and develop will be used for MOR. TEL is the incumbent here with wet spin-coat application and wet develop both the current standard, with the processing done in their track tools. Lam is attempting to take market share at critical layers with dry resist deposition and etch to develop, both done in Lam’s tools separate from the traditional litho cell.

Winners are starting to emerge in research results. Below, we’ll discuss which of Lam or TEL is likely to win market share. We’ll also cover the next generation of pellicle technology, critical for reducing low-NA EUV costs, complementary patterning techniques like pattern shaping and DSA, along with the potential successor to high-NA: hyper-NA.

Amongst all the combinations, it appears wet spin-coat resist application combined with a dry (RIE etch) develop is preferred. For coating, wet application is cheaper and has long been the industry standard. It also reduces the risk of environmental contamination of the MOR, which can happen when moving the coated wafer from the separate dry resist tool to the scanner.

Wet spin-coating is done in wafer tracks (produced by TEL and Screen) linked directly to the scanner. This minimizes process delay times between resist coating and exposure, which can degrade the patterning quality. The track performs a few additional steps prior to exposure: a chill step just prior to transfer into the scanner ensures the wafer temperature is consistent at the time of exposure. Also, a wafer-edge-exposure (WEE) exposes partial die at the wafer edge to prevent any loose patterns. In other words, a track would be necessary no matter what resist coating method was used.

There are still some remaining challenges for a wet coating where a dry film deposition could offer advantages. First, metal contamination is a serious concern for fab tooling. State-of-the-art CAR resists must be produced with a trace metals specification of single-digit parts-per-trillion (ppt). When these are spin-coated inside a wafer track, a solvent is dispensed at the edge of the wafer to safely remove the organic photoresist—called edge-bead-removal or EBR. Because wafers are typically moved by robots that grip the wafer edge, cleaning it is important. Contamination on a handling robot can easily spread to every wafer it touches. There is no clear solution yet for how a metal containing resist can be spin coated with an EBR applied. Ultimately the process must meet trace metals specification on the order of ppt or at least parts-per-billion.

Lam’s proposed solution is a new version of their Coronus bevel etch tool. Meant to be used in tandem with their ALD dry resist deposition tool, this amounts two new, separate tools required for their dry resist coating process. In chipmaker testing it appears the dry equipment suite offers little advantage over the traditional wet process and comes at a premium price. There seems to be no strong reason to adopt the dry resist coating stack at this point. But the story is the opposite for dry develop…

## **Wet vs. Dry: Develop**

A major theme of the conference was dry MOR development, with dedicated talks from imec, IBM, LAM, Samsung, and others. The term “dry develop” can be a bit misleading since these terms have traditionally never been combined for lithography. _Developing_ a photoresist typically refers to applying a liquid puddle of a basic solution, TMAH in water, on top of exposed photoresist (note for MOR a solvent developer is used and the resist pattern tone is reversed; the overall concept is still the same). The exposed areas are soluble in the developer and dissolve away, leaving the desired circuit pattern. Notably, because the solvent is a liquid, the dissolving reaction proceeds in all directions.

_Dry Etching_ on the other hand, refers to Reactive Ion Etching (RIE) or plasma etching. In this case, the wafer sits in a sealed chamber between conductive plates and a reactive gas is introduced. An RF electrical signal is applied to the plates which strikes an ionic plasma above the wafer. The resulting electric field directs the reactive gas species in a single direction, down into the wafer where it etches the surface. MOR dry develop is indeed just a directional plasma etch for photoresist. In experiments, it appears this directional etch results in better pattern quality than a wet develop.

[![](https://substackcdn.com/image/fetch/$s_!8dQa!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5c969f85-4cd8-4cc2-ac3d-7abd933de25c_592x650.webp)](https://substackcdn.com/image/fetch/$s_!8dQa!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5c969f85-4cd8-4cc2-ac3d-7abd933de25c_592x650.webp)Reactive ion etch chamber similar to that used in dry develop. Source: Impedans

Samsung presented their testing at the imec/ASML high-NA EUV lab in Veldhoven that directly compared MOR wet develop and dry develop. In the first set of testing from the figure below, they evaluated an 18nm pitch line/space pattern for metal, similar to the initial layers where high-NA could be introduced. The wet developed splits in this DOE showed a very limited CD process margin of about 1nm (10% of the metal size), before line bridging or pinches defects led to failure. For the dry developed splits, the CD margin was increased to 2.7nm or 30% of the metal wire size.

At more aggressive pitches, 8nm lines at 16nm pitch, the differences were even more pronounced. LWR was much better along with a nearly 50% improvement in DoF. The consensus around wet coating and dry develop for MOR bodes well for both LAM and TEL. For TEL, the track will still be used as has been traditionally done for high-NA, albeit fewer (if any) developer modules would be included. Despite only the develop portion of their dry resist suite being adopted, this is still pure upside for Lam. Their Coronus tools also may still see adoption to mitigate trace metals contamination at the wafer edge.

## **Low-NA EUV: Mask Lifetime & Pellicle**

Despite being a “mature” technology used in high volume for more than five years, low-NA is still a focus for further R&D. Pellicles are a key piece of the ecosystem that until recently were not in widespread use. A pellicle is a thin film used to catch particles and keep them out of focus from the mask image, thus, preventing any fall-on defect from being repeated with every exposure and completely killing the yield for entire lots of wafers. Without a pellicle, a single particle on the mask can ruin thousands of wafers before detection and pose a multi-million-dollar scrap incident for a fab.

[![](https://substackcdn.com/image/fetch/$s_!nNTu!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f29aeab-e3cd-4846-b145-96dd022cdd5d_458x232.png)](https://substackcdn.com/image/fetch/$s_!nNTu!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0f29aeab-e3cd-4846-b145-96dd022cdd5d_458x232.png)A pellicle keeps particles out of focus, preventing repeater defects. Source: Mitsui

In older generations of projection lithography, pellicles are standard. They’re an underappreciated safety feature that reliably prevent major scrap events. DUV pellicles are 100% transparent, fully seal the mask image in a protective chamber, and often survive the lifetime of the mask - millions of exposures.

For EUV the use of a pellicle poses some major challenges. EUV systems operate in a near vacuum, so moving the sealed pellicle between ambient fab pressure to vacuum puts serious stress on the pellicle film, which is well under 100nm thick. In addition, any molecule or thin film in the light path heats up as it absorbs EUV light, potentially burning through at the hotspot. Even the pellicle film itself can heat up to over 700° C. Extreme temperature stress on the film is the main cause of failure. EUV pellicles have nowhere near the lifetime of their DUV counterparts.

While TSMC has been using a proprietary version for at least a few years in high volume, pellicles from 3rd party vendors lagged and are just now being adopted by other chipmakers. It’s a difficult materials science problem: the pellicle must endure the extreme environment of heating to 1000° C, attack from energetic hydrogen plasma nearby, and acceleration of well over 10 Gs almost constantly throughout its lifetime. And they can only be 10s of nanometers thick to avoid absorbing too much of the expensive EUV light.

Today’s pellicles can survive roughly 10,000 wafer exposures before replacement. They must be swapped out before failure since they tend to fail in brittle fracture – meaning shards of broken pellicle spray onto the mask and multimillion dollar projection optics. As source power continues to increase, the heating effects on the pellicle will become too intense for existing materials. Metal-silicide used today is unlikely to work beyond this generation of light sources with 600W power.

Carbon Nanotubes (CNTs) pellicles are probably the next gen solution. Results shown at this conference and SPIE EUV last September prove they can meet most specs, except for cost which will need to come down. The revelation from the last year or so of research is that in certain regimes, pellicle lifetime can _increase_ with source power.

Assuming the material can handle increased heat (metal-silicide cannot but CNT can) a pellicle can survive source powers >1 kW. This is enough to meet the ASML roadmap at least through the end of the decade. The mechanism is a counterintuitive effect in hydrogen plasma. Hydrogen flow is used near the mask to prevent particles from contaminating the patterned surface. But the hydrogen is turned into a plasma as it absorbs some of the EUV light. In turn this high energy plasma etches away the pellicle material, gradually weakening it until failure.

Higher source power generally causes lower pellicle lifetimes as the hydrogen plasma etches faster at higher energies. But unexpectedly, there is an inflection point (somewhere around 600W it appears) where the plasma becomes so energetic that the etch rate decreases – hydrogen desorbs from the pellicle surface so quickly that it doesn’t have time to etch. The outcome is that CNT pellicle performance increases with source power.

Finnish startup Canatu and Lintec are competing to bring the cost of CNT pellicles down in time for the next generation light source a few years from now.

[![](https://substackcdn.com/image/fetch/$s_!ATup!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fefeef67e-f0a3-4ad3-956c-a64f56a4d358_1024x556.png)](https://substackcdn.com/image/fetch/$s_!ATup!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fefeef67e-f0a3-4ad3-956c-a64f56a4d358_1024x556.png)Micron on EUV pellicle: source power advances are limiting lifetime, not ready for HVM. Source: Micron

Given that today’s pellicles still aren’t perfect in terms of lifetime, cost, and contamination on failure, certain chipmakers have yet to adopt them. Without the protection of a pellicle, mask cleaning becomes critical to avoid printing unwanted particles. This introduces a delicate balance as too little cleaning increases the risk of printing particle-induced defects, but too much cleaning wears away the pattern, ruining the million-dollar mask.

Micron gave an interesting presentation on the effect of cleaning on various structures relevant to DRAM like 1D lines and spaces with pitch close to 30nm and 2D patterns in the low 40 nm range. They showed depth of focus and exposure latitude (the acceptable variation in dose. Critical dimension of the pattern on wafer varies with dose) are affected by cleaning cycles. Mask performance degraded significantly over multiple cleaning cycles, the conclusion being that 1) designs should be optimized for cleaning resilience, 2) you can get ~200,000 wafer exposure from an EUV mask before cleaning degrades it beyond usability.

[![](https://substackcdn.com/image/fetch/$s_!m334!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F50055536-afa4-4139-827e-8d51b4fbe817_1024x686.png)](https://substackcdn.com/image/fetch/$s_!m334!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F50055536-afa4-4139-827e-8d51b4fbe817_1024x686.png)Source: Micron

## **Complementary Patterning: Pattern Shaping**

Since an EUV exposure is the most expensive process step, by almost an order of magnitude, chipmakers are strongly incentivized to reduce usage. Pattern shaping and directed self-assembly (DSA) are the two leading “complementary” technologies that can reduce EUV usage (this is not the same as _replacing_ EUV totally, just reducing multi-patterning and operating the scanners economically).

[Pattern shaping](https://semianalysis.com/2023/03/06/euv-requirements-halved-applied-materials/) is more mature – Intel and possibly others have adopted it in high volume manufacturing. It’s just a directional etch tool applied to smooth and extend lines. EUV exposures done at low doses are cheaper because the scanner can be run at higher throughputs, but typically have poor line width roughness (LWR). A pattern shaping pass can smooth the lines, meeting LWR spec at a lower total cost.

Small tip-to-tip distances, the space between the ends of adjacent lines in a pattern, are a challenge near the low-NA resolution limits. Often a second EUV exposure would be needed to “cut” a line, rather than try to print separate lines in a single pass. Pattern shaping can instead be used to “push” lines after a single EUV exposure. The line ends are etched in one direction, extending them closer to the adjacent line end. This means the initial EUV exposure has much greater latitude tip-to-tip distance and a second cut mask won’t be needed. This also can potentially offer some design rule flexibility, the T2T dimensions are often restricted in the design-rule due the difficulty of patterning them, by reducing the resolution limit, vias in the metallization process, could be spaced closer together.

[![](https://substackcdn.com/image/fetch/$s_!Q583!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a6ff43d-72d1-42a0-81d8-3e29f8a682e8_1024x760.png)](https://substackcdn.com/image/fetch/$s_!Q583!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F5a6ff43d-72d1-42a0-81d8-3e29f8a682e8_1024x760.png)Pattern Shaping applications, Tip-2-tip reduction (left two) are the most practical. Source: Intel

[![](https://substackcdn.com/image/fetch/$s_!VJzs!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8fcb4c42-a915-4cb6-89a2-be6479506755_1024x700.jpeg)](https://substackcdn.com/image/fetch/$s_!VJzs!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8fcb4c42-a915-4cb6-89a2-be6479506755_1024x700.jpeg)Source: imec

AMAT’s Sculpta tool appears to be enjoying a first-mover advantage as Intel and imec specifically are using the tool in research and HVM. TEL showed promising results from their Acrevia tool but no mention of its economics versus Sculpta. Notably it uses a small beam roughly similar size as the scanner exposure field, whereas the Sculpta uses a curtain beam that spans the entire wafer. This might offer increased control as the etch beam parameters could be tuned per field. But it also is probably more expensive as the tool scans field-by-field, requiring expensive motion stages and likely reducing throughput.

Lam has also announced a directional etch “pattern shaping” tool but is not publicly showing data. At any rate, the results generally from pattern shaping look strong and with at least one large customer adopting it for HVM the assumption going forward is that new processes will use it wherever possible. The potential savings in EUV layers and throughput are significant.

## **Complementary Patterning: DSA**

In the past years of SPIE, Intel had championed DSA for use in 1x metal patterning in the sub-20nm pitch regime. Results from DSA-rectified EUV patterns had a significant yield advantage and up to 60% dose reduction, meaning enabling higher throughput and lower cost.

This year Intel added a new use case: gate contacts. Although the gate pitch is significantly relaxed versus a 1x metal pattern, the CD variance is a challenge for this layer. In particular the spacer that isolates the gate contact from the source/drain contact has requirements just as aggressive as tight 1x metal patterns. The spacer CD is on the order of a quarter of gate pitch, posing a significant open/short yield issue for any LWR present in the pattern.

[![](https://substackcdn.com/image/fetch/$s_!uK9p!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3cbc27da-b257-421e-84a4-bc926eb30fcf_1024x640.png)](https://substackcdn.com/image/fetch/$s_!uK9p!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3cbc27da-b257-421e-84a4-bc926eb30fcf_1024x640.png)Intel’s DSA talk showed two applications: BEOL SALELE metal & FEOL gate contact with spacer (new). Source: Intel

The results showed a large CD process window improvement when applying DSA to rectify the EUV patterned images. Although Intel did not share device yield data, they performed a simulation based on the LWR improvements that indicated >10% yield enhancement with the DSA process. With the move the gate-all-around putting FEOL under the microscope for yield, DSA may see application there along with metals going forward.

Overall momentum for DSA is increasing. This SPIE we saw a much higher volume of DSA papers and by potential customers, not just the materials suppliers. Intel is continually positive on the topic and IBM is even including DSA in its patterning roadmap.

[![](https://substackcdn.com/image/fetch/$s_!73Ky!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb5ac56f0-1f08-4c4c-8ffe-4e09ec8e5552_1024x602.png)](https://substackcdn.com/image/fetch/$s_!73Ky!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb5ac56f0-1f08-4c4c-8ffe-4e09ec8e5552_1024x602.png)IBM’s Patterning Roadmap. Source: IBM

[![](https://substackcdn.com/image/fetch/$s_!_mvw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05633190-99d7-45a8-9b54-72c410315c8e_1024x622.png)](https://substackcdn.com/image/fetch/$s_!_mvw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05633190-99d7-45a8-9b54-72c410315c8e_1024x622.png)DSA applied to gate spacer patterning improves process margin. Source: Intel

[![](https://substackcdn.com/image/fetch/$s_!KZwO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07485dc5-7d81-451c-8213-aac21898de6b_1024x653.png)](https://substackcdn.com/image/fetch/$s_!KZwO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07485dc5-7d81-451c-8213-aac21898de6b_1024x653.png)Intel FEOL DSA Yield Simulation shows >10% improvement. Source: Intel

## **Hyper-NA**

While many papers were focused on high-NA introduction, ASML was already starting to pump the next-gen hyper-NA. As the name suggests, it’s a continuation of the high-NA strategy, with similar benefits and challenges.

[![](https://substackcdn.com/image/fetch/$s_!JDbr!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F66fbb135-b06e-42f2-b3a4-13e8c3a5dccd_1024x532.jpeg)](https://substackcdn.com/image/fetch/$s_!JDbr!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F66fbb135-b06e-42f2-b3a4-13e8c3a5dccd_1024x532.jpeg)ASML roadmap including hyper-NA “opportunity” early 2030s. Source: ASML

Zeiss is giving the green light, saying that hyper-NA mirrors are feasible. The infrastructure developed for the high-NA projection optics was pre-emptively designed for compatibility with 0.75 hyper-NA as well. This is one big item removed from the hyper-NA critical path, important because mirror manufacturing was one of the biggest risks for high-NA.

But there are still serious risks both economic and technology-related. Depth of focus is already a key challenge for high-NA, and it decreases relative to the square of NA. This means the depth of focus for hyper-NA, all else equal, is close to half that of high-NA. Printing features with pitches in the teens or single digit nanometer range will require even thinner resists than MORs today along with further improvements in scanner focus control.

With shrinking depth of focus, wafer topography also becomes a concern. New planarization technologies will be needed to achieve nanometer-scale topology control. Canon’s inkjet-enabled planarization method, kept mostly under wraps for now, is one we will be watching.

The economics of hyper-NA are also an open question. Given the [cost challenges for high-NA](https://semianalysis.com/2023/12/11/asml-dilemma-high-na-euv-is-worse/), it’s unclear that another step increase in scanner price is palatable or makes sense for chipmakers.

ASML is proposing hyper-NA will be needed for the first CFET nodes, which would be post 2030 (probably closer to 2035). Seems like they need to get major customers fully on board for high-NA before any momentum can gather behind hyper.

[![](https://substackcdn.com/image/fetch/$s_!RUp9!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07918542-b9bb-4eb8-9245-557a20208551_1024x677.png)](https://substackcdn.com/image/fetch/$s_!RUp9!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F07918542-b9bb-4eb8-9245-557a20208551_1024x677.png)ASML hyper-NA barriers, 10nm thickness resist, need a positive tone MOR resist developed by materials vendors, no barriers for system integration except DoF. Source: ASML
