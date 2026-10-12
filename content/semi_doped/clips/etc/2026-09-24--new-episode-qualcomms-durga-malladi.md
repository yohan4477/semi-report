---
source: https://daily.semidoped.com/p/new-episode-qualcomms-durga-malladi
title: 🎙️ NEW EPISODE: Qualcomm's Durga Malladi - HBC vs HBM, Dragonfly AI 250, and Winning on TCO
date: 2026-09-24
kind: clipping
genre: etc
audience: everyone
subtitle: High Bandwidth Compute (HBC) vs HBM, Dragonfly AI 250, 18x effective bandwidth, 768 GB per card, and more
---
Austin sits down with Qualcomm’s Durga Malladi to get the details on High Bandwidth Compute (HBC), the company’s big bet for AI inference. They dive into the architecture of the upcoming Dragonfly AI 250, how stacking DRAM directly on a logic die solves the memory wall, and why TCO is the ultimate metric for hyperscalers.

**Things we cover:**

  * Qualcomm’s High Bandwidth Compute (HBC) architecture

  * The upcoming Dragonfly AI 250 accelerator

  * How near-memory compute differs from HBM

  * The role of TCO in hyperscaler decisions

  * Scaling HBC from data center to edge devices

  * Fitting a trillion-parameter model on a single card




 _This podcast is lightly edited for clarity._

## What is High Bandwidth Compute?

**Austin:** Hello, listeners. Austin Lyons here with Chipstrat, and with me is Durga Malladi, IEEE fellow, which is pretty cool, and EVP and GM of Tech Planning for Edge and Data Center. So, we’re here to talk high bandwidth compute. But first, before we get into that, which is a great topic, I want to know more about what your job title means. Tell me what you do at Qualcomm.

**Durga:** I run all the IP and the technology planning for what we need to do across all the products, ranging from data center all the way down to edge solutions including devices. So, that means the IP, if you think about it, is what should we be doing in our CPU portfolio in let’s say three, four years downstream in ‘29, in ‘30 in data center, versus what do we need to do in devices, in handsets, in new agent tech devices. And then rinse and repeat the same exercise for what do we need to do on GPU, what about NPU, what about modem, what about sensing hub, and so on. So, these are all the different IPs. That’s the planning exercise which runs the road map behind the scenes, but it is across all the business units.

**Austin:** Nice. That’s pretty cool. I like that you see across all the different technologies so that it’s not like CPU running not together with GPU or not together with the different products. It’s pretty cool. Okay, so let’s talk high bandwidth compute, HBC. The way I see this is obviously Qualcomm is trying to enter and is in a competitive space with inference solutions in the data center. You’ve got GPUs, there’s XPUs, and Qualcomm has the Dragonfly lineup—AI 200, 250, 300. It feels to me like HBC is Qualcomm’s big technical bet to differentiate and bring something different to market as compared to what everyone else is doing. So, of course, I want your thoughts on that, but also then tell us what is this HBC and how is it different from what others are doing?

**Durga:** Absolutely. So, when we re-entered the data center business last year—and I actually ran it for one year last year—one of the things that we really focused on is, you’re absolutely right. There’s a lot of players already in the market and they have some pretty incredible solutions already. So, it wasn’t one of those moments where we said, “Okay, let’s also jump into the fray,” and it’s not a me-too moment or anything of that sort, but it was, “What is it that is going to be differentiating us from the rest of the ecosystem there? And what is a really good tough problem that we really want to solve?” because that actually gives us the benefit of, “Okay, that is different, let’s take a look at Qualcomm.”

And we latched on to the fact that—and we had an R&D project that was running internally for a while on what is called near-memory computing. The principles of that are very simple, but before that, what is the problem that we are trying to solve? It turns out that if you go back in time, maybe over the last six years or so, you will see that the compute capability, if you just take any of the GPUs and say generation over generation, how much is it improving? It improves quite a lot actually. It’s at least a factor of two, sometimes a factor of three. But the memory bandwidth wasn’t actually improving at the same league. And so the natural next question to ask is, so what? What does that do? Well, if you go back to some of the basic principles of how do you do compute, you have all your data sitting somewhere and you have to fetch the data to do the compute processing. But at some point in time, what happens is that your computer is so good that you’ve tilted the scales quite a bit. So, you might be just idling, you’re waiting for the data to actually show up. So, memory bandwidth becomes a bottleneck and it’s called the memory wall. And you see that a lot more with AI inference, especially in the decode portion of it.

And so what we did is our HBC architecture is based upon what is called near-memory compute. Instead of treating memory and compute as two distinct concepts, what if we actually do a lot of the compute right next to memory, like literally right next to it? It does two things. One, the latency comes down quite a bit. And second, we can reduce the power consumption quite a lot. So, today in data centers, HBM, the bandwidth is very high, but it’s expensive and it’s a power hog. So, we actually wanted to make sure that we can solve it in a different way. And one thing led to another and as we started talking about this with a lot of the hyperscalers and a lot of other partners, they loved the idea. And as we announced it, we actually announced a couple of names in terms of some of the partners that we have. So, it’s been a great journey on HBC.

But as we briefly mentioned in our investor day in June, and today at Snapdragon Summit, in fact, Cristiano left a teaser out there. But let me just tell you what is the point of this. HBC for us is a technology, but it’s not just for data center. It actually applies to everything all the way from data center to servers and accelerator cards, in automotive, in PCs, in XR, and yes, in smartphones as well. But it actually works in a different way in some of these things, but the principle remains the same, which is you’re doing a lot of computation right next to memory.

## Stacking DRAM on a Logic Die

**Austin:** That’s good. That’s a great explanation. And I like how you mentioned that HBC is something that can be applied across from the data center all the way to the edge, and that’s a good organizational design as you’re talking earlier about how your job is to see IP across all that. So that’s pretty cool. Okay, so what I heard from you is the problem is compute is increasing quickly, memory bandwidth is not increasing fast enough. So this all this extra compute can’t get fed quickly enough. And maybe instead of trying to just increase the bandwidth of the memory we use today, you guys stopped and said, “Well, wait a minute, why have to shuttle all this data? Why shuttle even more like wider buses or even faster speeds? Why not just bring it really close to the compute?”

**Durga:** That’s correct. Exactly. And keep in mind that it’s a principle that, as you start bringing down the power consumption quite a lot—just going one step further on devices—power consumption matters quite a lot in devices, especially as you think of all the agentic AI based devices that you see these days. And they’re still evolving, by the way. There’s a lot of new players who are coming to the market. In fact, quite a few of them have very little background in manufacturing devices or making devices. They come in from an AI-first mentality and they’re coming out with these devices. And the job of agentic AI devices is to be constantly on because they’re working all the time. So, that power consumption benefit that we talked about is going to be key, we believe, in unlocking the full potential of agentic AI devices.

**Austin:** Yeah, that makes sense. So, it’s not just the memory bandwidth problem, but the also added benefit of because you’re not shuttling this data so far horizontally, now it’s just going vertically, which we’ll get into, there’s also a big power savings.

**Durga:** Yes.

**Austin:** And of course, we know that power is the big constraint. Okay, so then, to someone who’s listening, this is the first time they’ve heard of high bandwidth compute, are you sticking memory on top of an accelerator or tell us more about the stacking and the separation? What is being sent across the wire horizontally versus vertically?

**Durga:** By the way, there’s a really cool animation that we showed at investor day. I wish we had that, but I’ll just use my hands as props. So, the way it works is that the memory is like, you have these individual, the DRAM, it’s called a stacked DRAM. You’re basically stacking DRAM one on top of the other. And there’s a lot of wafer-on-wafer bonding techniques that are used on that. So, this is hardcore process technology, by the way. This is in fact, it has nothing to do with compute at this point in time. But then right underneath that stacked DRAM is what is called the logic die. That’s where you put in all the compute. And depending on the use case, you might actually say, “I want some specific logic to actually reside over there.”

There might be yet another processor that is still sitting, which is away from it. But you’ve brought in a lot of the heavy computational needs, like the ones which really need that memory bandwidth. You put all of that right next to memory in that base die. And that HBC therefore is a combination of both, the stacked DRAM on top plus the logic die that is underneath or the compute die that is underneath. And now you’ve done a bulk of the work just with that alone. There might still be some residual compute that you want to do, and that could occur in a separate processor over here. In some sense, HBC is a bit like a co-processor because it’s doing a lot of the compute, but it’s not the only thing. You might still have another main processor that’s running out there, but it removes that complexity quite a bit. So, in short, it is literally right underneath that stacked DRAM that we’re talking of. That’s where all the compute is being done.

## Is This Just Custom HBM?

**Austin:** Okay, okay, that’s helpful. So, anyone who’s familiar with HBM will say, “Well, this sounds a lot like HBM4E with a custom base die and stacked DRAM on top.” So, tell us the differences. First of all, is it a different class of DRAM that’s being stacked? And then how should we think about the difference between the accelerator at the bottom versus a custom die?

**Durga:** Yeah, that’s a in fact, this is exactly one of the things when we first came out with the concept and when we talked about it, I went to Korea and we talked. And you might have noticed a couple of announcements that have been made even by the memory vendors. They have different terminology for that. It is their equivalent of HBC, but actually they are partners of ours. So, we expect that these two technologies will co-evolve for a period of time, and we’ll see what happens after that.

**Austin:** Hmm, interesting, interesting. Okay, so then, which by the way, have you guys disclosed anything about the layers, number of layers that you’re stacking?

**Durga:** We have not yet provided all the numbers. In fact, stay tuned on that front because you haven’t asked the question, how’s the silicon coming along and so on, because we’ve talked a lot about it in terms of PowerPoint presentations and most people are actually taking our numbers for what they’re worth. But we will be showing some proof points over the next quarter or two as the silicon is back in the lab and it’s coming along very well, so stay tuned.

**Austin:** Okay, awesome. I’d love to hear that. So, you’ll have silicon coming back soon. Looking forward to that, looking forward to see the benchmarks. That really turns it real, from just PowerPoint. Back to the stacking of the memory, talk to us about the thermals. Is that become a constraint for that base die?

**Durga:** I think it is one of those things that, as Qualcomm, when we come in with—we are not, when we talk about IP, for instance, it’s not just about what we are doing for our CPU or our NPU logic and so on. We have a rich heritage of both packaging technologies and 3D stacking and a lot of these things that we do. We work very closely with the foundries in terms of how these tech need to come together. That has played in our favor as we brought out HBC. And one thing to mention is that in this space, you have to think through carefully as to which product are you designing this for, and based upon that, you have to think about the right kind of packaging so that you don’t start hitting other constraints, like it’s not the power maybe, but then you start hitting thermal constraints. So we do have a lot of experience in that space. So, different, depending upon which product it is, we have dimensioned the compute in such a way, compute plus the memory, which is dimensioned in such a way that we avoid the thermal problems. And so that is something that we’ve paid some careful attention to.

## Dragonfly AI 250: 18x Bandwidth

**Austin:** Nice, nice, very promising. Okay, so the Dragonfly AI 250 is the first product that will have HBC in it.

**Durga:** That’s correct.

**Austin:** And that’s coming in 2027.

**Durga:** That’s correct.

**Austin:** I saw that compared to the AI 200, they both have the same amount of LPDDR in the card, it’s 768 gigs.

**Durga:** 768 gigs.

**Austin:** And yet the 250, which is the first to have the HBC, has 18X the effective bandwidth, I believe is what the website said. So again, just for everyone, could you remind us again why that HBC and the stacking is 18X the bandwidth as compared to in the 200 where presumably the LPDDR is a little bit further away?

**Durga:** So, first of all, the raw memory is a completely different concept compared to the actual memory bandwidth in itself. So this is LPDDR, which means we can pack, it’s a very dense card that we have. So it’s 768 gigabytes. A lot of the other things that we see in the industry, they have like 288 gigabytes per card. This is 768 gigabytes. Which, by the way, if you think through that, 768 gigabytes per card means if you take a typical order of magnitude, trillion-parameter model, and it’s all at mixed precision FP4, you can fit a trillion-parameter model in just one card. That is seriously mind-boggling. And we have shown that, we have shown some proof points associated with that. But that’s just the memory capacity.

The memory bandwidth is where, as we bring in HBC, then you have this combination of the underlying logic plus DRAM stack. So this actually is a slightly different concept. This is not about the capacity anymore. Using the same capacity, you’ve just boosted the memory bandwidth significantly. That’s why they are two independent concepts. But another way of looking at it is, if you take an AI 200 card, and it has a certain performance, certain exaflops per rack, or exaflops in a given rack, and of course, we have disclosed that our racks are like 160 kilowatts. When you go from AI 200 to AI 250, the amount of memory inside, it’s like 41 or 43 terabytes or so, that doesn’t change. But because of the fact that there’s a huge memory bandwidth increase, the number of exaflops in the rack actually goes up substantially because of that, because the decode performance improves quite a lot. So you see, the total amount of capacity that you have in the rack is the same. But now you’ve dismantled that memory wall with HBC, and that’s the reason why our overall performance goes up significantly with AI 250.

**Austin:** Okay, so let me reflect it back to you. There’s a part where I’m a little fuzzy on. So, we’ve got more bandwidth in the AI 250, which of course, would mean better decode performance, so just more tokens per second.

**Durga:** That’s correct.

**Austin:** How does that unlock more flops? Because the flops are not underutilized? They’re not sitting waiting. Is that what it is?

**Durga:** That’s right. In fact, because of the fact that you’re running it that way, your TCO also becomes better. In the sense that, if you just take it because the tokens per second per watt goes up significantly, because your tokens per second has gone up, it’s the same power consumption, by the way, same 160 kilowatts. But then in addition to that, then when you take a look at the total, it’s called the tokenomics, where you also normalize it by what’s the cost associated with that, it comes out to be even more favorable compared to some of the other things that you see in the market today. So, in that sense, every time we have talked about the benefits of AI 250, we have talked about not just tokens per second, but tokens per second, tokens per second per watt, and tokens per second per watt per dollar, or sometimes even tokens per second per dollar. When you put the entire arithmetic together, then you see why it becomes actually far more favorable to go with this.

## The Primacy of TCO

**Austin:** Nice. Okay, so I was going to ask you then, so when you have talked to hyperscaler partners, ultimately, is there one of those that’s most compelling? Is it about the TCO or about the tokens per watt or kind of all of it?

**Durga:** I think increasingly these days, it’s about the TCO. Increasingly. It used to be about raw tokens per second and tokens per second per watt. But I would argue that TCO already captures that, because if you think about it, what are all the things that you need to worry about? Well, okay, if I buy one of these racks, first of all, how much am I paying for it? So that’s one variable. Second, what’s the power consumption? And then you have to figure out for that power consumption, what’s my utility rate? And there is some number associated with that. The third one, of course, is, how many tokens per second does it really generate? How effective is it? And you put all of these three variables together, and I’m discounting things like water that you need for cooling and so on. It’s the TCO that is emerging as the most important, but it does take into account these three big variables.

**Austin:** Yeah, yeah. No, I think that makes a lot of sense. And just the simplest way for me to think about it is like, okay, if I have a billion dollars to spend and I have 100 megawatts. If I can buy X racks from some provider that fit within the power envelope and my budget, or I can buy 2X racks from someone else, well, even if the throughput’s a little bit different, generally if you have 2X the racks, you’re going to get more throughput. So that makes a lot of sense to me.

## Manufacturing at Scale

**Austin:** So I guess, maybe last question. There are other AI ASIC startups who also because they’re coming in and need to do something different, they’re also making different technical bets. And usually the skepticism that people get with them is they say, “Okay, that’s great. Can you actually manufacture it? Can you actually get allocation?” Now, obviously, Qualcomm is one of TSMC’s largest customers and you have wafer allocation, but I also know that you have many different business units from data center to edge who all want the same wafers. So, talk us through how that works. And I assume that you do have the advantage there because you are manufacturing things production at scale.

**Durga:** That’s one of the places where it is true that it’s not enough to just have the technology in itself. That’s why we’ve been placing careful bets in terms of making sure that our wafer allocations, we have an excellent set of relationships with all the foundries and also with the memory makers. And so, as they have come up as extremely valuable partners in across the entire portfolio, not just in one domain, those relationships do matter when we go in front of a customer and say, “Yeah, we are in a position to supply you. How much do you want? You want these many megawatts or maybe a gigawatt, this is what you want.” Yeah, we have the supply chain lined up for that because we do have those relationships across all the different businesses. And that actually helps us quite a lot.

**Austin:** Yeah, sure, totally. That makes a lot of sense. All right. Well, that’s it for today. Durga, this was great. We will have to talk again once you guys have more to share about the actual measured performance of HBC.

**Durga:** All right, sounds good. Thank you.

**Austin:** Thanks.

**Durga:** Thanks again.
