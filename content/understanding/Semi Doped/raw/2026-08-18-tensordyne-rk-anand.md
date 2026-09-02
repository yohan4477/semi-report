---
source: https://daily.semidoped.com/p/new-episode-tensordynes-r-k-anand
title: 🎙️ NEW EPISODE: Tensordyne's R K Anand: Juniper Fabric, Logarithmic Math, MoE Inference, Air Cooling, 3nm
kind: transcript
---

🎙️ NEW EPISODE: Tensordyne's R K Anand: HPE Juniper Fabric, Logarithmic Math, MoE Inference, Air Cooling, 3nm

Austin talks with R K Anand, co-founder and chief product officer of Tensordyne, about the company’s unique approach to AI inference. RK explains how Tensordyne leverages logarithmic math to build a more power-efficient compute engine that stays below the reticle limit, allowing them to pack more SRAM and HBM onto their 3nm chip. They also discuss how a partnership with HPE Juniper provides a battle-tested, low-latency scale-up fabric, enabling a balanced system that excels at both pre-fill and decode.

Things we cover:

Logarithmic math vs. traditional matrix multiplication

Logarithmic math vs. traditional matrix multiplication

Juniper’s router fabric for AI scale-up

Juniper’s router fabric for AI scale-up

Balancing compute, memory, and networking

Balancing compute, memory, and networking

Combining pre-fill and decode on a single system

Combining pre-fill and decode on a single system

Tensordyne’s 30kW, 72-chip quarter-rack system

Tensordyne’s 30kW, 72-chip quarter-rack system

The role of partnerships with Broadcom and HPE Juniper

The role of partnerships with Broadcom and HPE Juniper

This podcast is lightly edited for clarity.

Introduction & Juniper’s Origin Story

Hey everyone, and welcome back to another Semi Doped podcast. Today we’ve got a special guest, R K Anand, co-founder and chief product officer at Tensordyne. If you haven’t heard of Tensordyne, it’s building an inference chip, an inference rack that does its math in a completely different number system and has other interesting architectural tricks that we’ll talk about. RK, I’m pleased to have you here to talk more about Tensordyne.

RK: Austin, it’s a pleasure to meet you and I’m very glad to be here. I watch a lot of your podcasts and I’m a big fan, so I’m glad to be here today.

Oh, right on. Awesome. Awesome. I love that. Thank you. Okay, so let’s start with you. You have a fascinating background in networking, which is really interesting because I think now that we’re at rack scale, obviously networking is a big part of the AI inference story. So, maybe tell our listeners more about you. Take us way back. You were at Sun, you were a founding engineer at Juniper. Kind of tell us about your career arc that led you all the way here.

RK: Yeah, so, this is my 37th year in Silicon Valley. I started my career at Sun in 1990, actually, designing microprocessors. So I was part of a microprocessor team. And Sun was building high-end servers for the market. So it was a really fascinating time. There’s a lot of competition, there was risk versus risk, and you got exposed to building really large multiprocessing systems.

Fast forward a few years to 1996, I was fortunate to join Juniper Networks as one of the founding engineers and led the first Silicon efforts there. And the reason I was able to do that was because Pradeep Sindhu, who’s the founder of Juniper, was one of my early mentors at Sun, was part of a team from Xerox Palo Alto Research Center helping us build these big machines.

And he gave me the opportunity to join Juniper. And I spent almost 17 years there with a little bit of a break. And saw the company from zero to like over $4 and a quarter billion dollars of revenue and the most fascinating part was that we were in the early days of the internet. The internet was doubling every six to nine months and I think Juniper transformed networking pretty significantly.

So it was a very good learning opportunity to start from scratch, grow with the company and eventually be very successful in building the biggest routers in the world. But most importantly, I think building great relationships and great friendships and being able to mentor a lot of the talent there. So I think it was a great learning experience for me.

Oh man, it sounds like it. Okay, so interesting. So you got to work on compute back at Sun and then you got to work on networking for a long time at Juniper and then here we are in this era, which is both compute and networking. So it seems like you have learned all the right things that you need for this era.

RK: Yeah, it’s fascinating, you know, I think the Silicon Valley, if you’ve been here long enough, go through cycles, right? And we’re in one more of those really great innovation cycles. And yeah, you’re right. You know, computing, you think about computing and you say, okay, general purpose computing or high-end client server computing and how was that built? Because we started from PCs, you know, mainframes, then PCs, then they went to client server.

And Sun was a premier company, a great innovation, a great place for innovating and and building great technology. And then Juniper ends up being the premier company in networking, building high-end core and edge routers, right? The fact that we have the internet today that works so flawlessly is because of all the work that companies like Juniper, Cisco and others did. And then we come to the world of AI and it’s again, back to computing, but then we start hearing for the last couple, three years, like networking is so central to AI.

So it’s a coming together of all of these things and, you know, you can then reflect back and see if you can take those learnings and apply them to what you’re doing today, I would say.

So, what I think is interesting and, you know, correct me anywhere I’m wrong, but when you guys started at Juniper, I assume that it was Cisco was probably the dominant player in the space.

RK: They were. Cisco was started in the early 80s and by or probably mid 80s, I don’t know the exact time, but when Juniper started in 1996, the browser had just appeared, right? Out of Urbana Champagne and Netscape, the Mosaic browser and Netscape had appeared and we were trying to put a lot of our data on the internet.

And we were trying to start sharing our, think of it almost like sharing your hard drives, basically. And there were these internet service providers, like UUNET was an example of them and they were using Cisco routers and Cisco was the dominant player. I think Cisco had like 93, 94% of the core router market share.

And fortunately for us, Pradeep, who was the founder of Juniper, looked at the way routers were getting built and he was trying to wonder why are they not getting built like high-end servers? So he had a general thesis that you could actually build routers far more efficiently. And then we got to hear from people like Mike Odell, who was CTO at UUNET, that the internet was doubling every six to nine months and he was unable to keep up.

And so Juniper fundamentally re-architected how routers were built and that completely transformed how the growth of the internet happened. Cisco by the year, sometime 2000, was the number one market cap company in the world. You know, they were like and John Chambers was on the cover of every magazine in the world.

And Juniper appeared in the landscape and we built the highest performing router and then I think within the span of a couple of years, we had 30% market share. So there is proof positive that when new markets evolve, there are opportunities for startups to come in and if they have technology that’s differentiated, they can have an impact in the market.

Nice, awesome. Yes, you you took it exactly where I was thinking in my head, which is like, wow, this actually feels very similar to back then where there’s a new technological revolution happening that’s impacting the end users, which was the internet at the time and it’s LLMs today. And there’s an incumbent that of course, is the largest market cap company in the world, and is quite dominant.

And I’m sure when you guys started Juniper, there was probably a lot of people that just said like, what are you doing? How could you ever possibly compete with Cisco? But then what I heard you say was the interesting insight is like, well, if you think that there’s a different way to tackle the technology that ultimately you do think you can compete on technical performance and then probably TCO and other things.

RK: Yeah, and you know, of course, the parallels only quickly end there because the size and scale of the market is kind of way, way different now. And the competitive landscape, you know, I mean, in those days of the internet, information was more constrained. We live in a different world today. Information is instantaneous. Everybody knows everybody else.

In that period between say 96 and 99, there were many other companies that were funded to build routers. I mean, all those names are etched in my mind, right? There’s Avici, there’s Fluris, and Nexabit, and there’s a bunch of companies. So, there’s an opportunity, the landscape opens up, an opportunity opens up. I think if you look at today, the scale is orders of magnitude larger.

The market capitalization of some of these companies is quite significant and then the technology power that is there, especially with Google or a lot of the hyperscalers also building Silicon and systems is that there’s a lot more information. But I think there’s a, you know, just like anything else, there are waves and there are changes that happen.

I think that if you look at the last five, six years, the initial phase was all training, AI training, right? And then we slightly shifted from training to inference and inference was initially we were doing monolithic kind of models and now we’re in the world of two trillion plus MOEs. So the architectural demands for inference are different from training.

And then for monolithic models to MOEs with, you know, two plus trillion models or 2.8 like Kimi K3, the pressures on the system are different. So there’s a window of opportunity that opens up on if you think about it and how can you build a system that addresses demand for today’s market that looks different from something that’s four or five years back.

The Log Math Advantage

Yes, perfect. Okay, so lead us into from there then into Tensordyne and what we have this window here. It’s it’s inference at just kind of massive scale. It’s mixture of experts, two trillion parameters. We want high interactivity these days. It’s agentic AI, right? So agents want to run at thousands of tokens per second ideally. And so therefore, so we’ve got this gap, we’ve got this window.

There is definitely a way that everyone’s doing it now, which is mostly like running this inference on racks and racks of GPUs. And Tensordyne is taking a different approach. So like tell our listeners, what is the technical differentiation that you guys are pursuing that you think is a different bet?

RK: If one were to break down the problem, the models are immensely large. They don’t fit on single devices anymore. So now you have to...

So there’s a networking problem that’s in front of you that makes it apparent that the model ain’t fitting on a single device, you got to spread it across many devices. Then there are power and other constraints that are in front of us, right? We can’t get power quickly enough, these data centers are large. And we didn’t start at this point, right?

If you look at, if you were to rewind a little bit, Tensordyne was prior to this was named Recogni and we had our series A funding in 2019 and we were more at that time, the world was about image and image recognition and Resnets and Resnet 54, Resnet 101. And we started as an inference company.

So, but because it was image recognition, we had to think, okay, how are we going to build a piece of silicon and a system that can do really exceptional performance, deliver high performance for AI for inference for image recognition and the market was automotive that we focused on. Automotive has a power constraint. The car can only give you so much energy.

So there’s a power constraint and you have to deliver inference and you have to process, let’s say incoming frames of from cameras that are at eight megapixels. So we set that up as a problem statement. And then the realization was that if you took traditional math and tried to do it in the car, you would blow the power budget of a car.

You know, rather than using it to move the car more miles, you would basically, you know, shrink the range of the vehicle. So our approach to inference at that time was like, let’s think about mathematically it being different. And let’s approach math it from a first principles math perspective. And that’s how we converge on using logarithmic math for AI.

So that set up, if one has to be fortuitous, well, that set up the foundation for Tensordyne today. We didn’t build a perfect device, but we validated our math. We validated that it really worked for AI. And the analogies were that, you know, first of all, log math’s been around since John Napier invented it over 400 years back.

So it’s not something that we dreamt of. And log math has been used, you know, if you think about like the Apollo program and all these programs, people used to use slide rules and log math to determine escape velocity and re-entry and all these things. And then over the last two, three decades, we’ve been using log math in DSPs.

So it’s not like we were the inventors of log math, but our realization was that can we use log math in AI? And so that, that helped us, right? And set us up for today.

Gotcha. Okay, okay, interesting. So for listeners who haven’t heard of Tensordyne before, Tensordyne actually started as a different company. What did you say the name was?

RK: Recogni, R E C O G N I.

Recogni. Okay. So probably image recognition, maybe it came from that.

RK: Exactly. Exactly.

Um, so you were looking at like convolutional neural networks, that kind of stuff pre-LLM, pre-transformers and you’re asking, okay, how can we do this at the edge, thinking automotive, so you know, self-driving cars, that kind of thing. Makes a ton of sense. And you obviously a power constraint there, which I’m sure we’ll get to.

It’s same power constraints in the data center, same but different, but like thinking about power. But you were taking a, you’re asking, how can we do this incredibly efficiently? And the idea was to use log math instead of the traditional like matrix, multiplication, multiplies and adds. Like tell our listeners a little bit more about like what does log math unlock as the benefit?

RK: So, you don’t, you can’t avoid matrix algebra. Matrix algebra is the fundamental for all of AI. So it’s not like we could avoid that. But if you take a number and convert it to a log number, then, and most of the operations are what are called mat mul, right? Which is basically, if you think about it, it’s a multiplication followed by an accumulate, an addition.

So we’re doing trillions of multiplications and additions in AI, whether we’re doing in convolutional neural networks for image recognition or in LLMs, it’s exactly the same. So when you take a number and make it a log number, then log base two A times B is log A plus log B. So multiply becomes an adder. And, you know, let’s think of ourselves as young children.

Let’s say we’re in elementary school and we’re trying to do multiply two numbers or add two numbers. Adding is easy, right? You just take the numbers and add them. But when you want to multiply, you know, you have to do long multiplication and add a bunch of after that. It’s the same thing in silicon. If you think about it, you have to have a lot more gates, you’re going to take a lot more area, a lot more power to multiply two numbers.

But you want to add two numbers, it’s more easy. Adders are, you know, like a building block in silicon. So, you solve the first part of the problem. The second part of the problem is really hard because now you have to take the result of the multiplication and add it. And the minute you are in a logarithmic domain, adding becomes a problem.

And if you were to take a traditional approach of a lookup table or Taylor series, all the gains that you have in going to addition in place of multiplication are lost. So our fundamental innovations that we’ve patented was to figure out how to go back from a log to linear space and perform the additions without losing the gains in area and space and power that we got from multiplying the numbers, actually adding them, right?

And so we’ve spent inordinate amounts of time in mathematics. So almost half the company spent almost half a decade in math, right? Because that’s what you, that’s how you can be a revolutionary startup rather than an evolutionary startup because then you can do, because if you do, if you do the same thing like everybody else has done and you have access to the same say silicon geometry, seven nanometer, five nanometer, you’re going to have no advantages.

You can’t compete against the biggest guys. So you actually have to think about this differently and that goes back to how, you know, in my thinking, reflecting back in 96 and 97, how Pradeep and and the other co-founders of Juniper thought about routers, right? And do it differently, forwarding in silicon versus forwarding with, you know, microprocessors.

So the similar analogies apply here and so we spend a lot of time thinking about that.

From Chip to System: The Networking Problem

Nice. Okay, awesome. So you reached for log math because you realized, okay, we have a bunch of mat mul to do and if we, and multiplication is expensive from a power and a die area perspective, and ultimately probably latency as well. And therefore if we can convert it to the logarithmic domain, we can turn these into adds, but then eventually it has to get turned back, converted back and you guys fought really hard about how to do that efficiently, effectively, cleverly.

And so, okay, so then you said, okay, we figured this out. This is great. This is more power efficient, small, fast. So then you took it to market ultimately or at least built chips for automotive to kind of prove out essentially the R&D side of things and to, okay, now connect me from there to getting into data center inference.

RK: All right, let’s do that. Let’s do that. So, think of a convolutional neural network as like a three by three matrix. So you have to perform nine operations, nine multiplies, followed by all the additions that make add up those nine numbers. So we had the building block for it. And we had functioning silicon in seven nanometer that was fully functional and we were able to demonstrate taking camera streams and doing that.

We hadn’t incorporated a lot of the safety features that we needed for automotive. And so at that time in, you know, late 22, early 23, chat GPT happened. And we realized quickly that our building blocks were really set up perfectly for this moment. The market was 50 or 100 times larger, the ability to have a product from power on to getting into revenue is much, much faster in the data center, in networking, rather than in automotive because automotive has a long qual cycle, right?

It takes a long time to build a car, you got to certify it, you got to make sure it’s safe. There’s a number of things that need to happen. So we coalesced as a team and said, let us look at our technology and see how applicable is it for LLMs. And LLM, you do one by one multiplications, not nine, three by three. Great. Well, LLMs, so if you look at Resnets and all, think of 100 million parameter systems.

And now you’re going for 100 million to multiple 100 billion to trillion parameters. So the memory hierarchy, the memory architecture has to change. You have to think of memory slightly differently.

But your fundamental building blocks for math, you can build upon. And so that’s what we did. And so we started architecting in 2023. So we had the good fortune of retrospective view on on math, and 100 million parameters. But we also had a view that what was the problem statement in front of us?

That is that you could go from multiple hundreds of billions to maybe trillions of parameters. And so how do we build an architect a chip for that? We still hadn’t solved the networking problem though. So we said, okay, let’s understand how to build first an accelerator that could be world class and deliver world class performance for LLMs.

And then the multi 100 billion parameter problem now became a multi-trillion parameter problem.

And so now you have to think of the networking problem next.

A Router Fabric for AI

Yes, yes. Okay, so you you guys said, oh, we’ve got all the building blocks, the opportunity is enormous. The path to production is shorter. I’m sure it was a hard decision, but in retrospect, it’s kind of a no-brainer. But of course, you had to make new memory hierarchy decisions.

And then to your point, that leads to the like, oh, that the model weights are not going to fit on one chip. Therefore, we have to connect lots of chips. Therefore, networking has to be like a first-class design priority.

RK: It does.

Yeah, so tell us more then about your networking and where you guys ended up.

RK: Yeah, so now, now, let’s for a moment step back and think about the first principles of how do you build GNA inference systems, right? So, there’s compute, there is constraints that are there place, right? What is your compute, whether you’re compute bound?

Whether you’re like memory bandwidth bound, how much bandwidth do you have coming in from external memory? Memory capacity bound, how much memory can you put, right? And then when you think about the networking problem, then you say, okay, how much bandwidth do I have facing in and out of a, let’s say scale up network?

And then what is my scale up network latency? Because that also might have an effect. So now you think about Silicon and you say, okay, how much of my real estate do I allocate for all of these things? How much do I allocate for compute? How much do I allocate for memory interfaces and memory capacity?

How much do I allocate for on-chip memory? There’s SRAM.

And then how much do I allocate in terms of interfaces and bandwidth and for my fabric interfaces? So when we sat back and looked at it, and this is like I think I believe in the summer of 2023, the realization from some me and some of my colleagues were, gosh darn it, we’ve been building these networking systems for 15, 20 years at Juniper Networks.

And I had the good fortune of leading some of the efforts at Juniper for in Silicon, for almost 17 years. And in the back side of a router, in the rear of a router, is a scale up fabric. Because if you think of a router, it’s got lots of front side ports.

So think of like a high-end router, it could have, I don’t know, almost hundreds of 800 gig ports. So traffic comes in from one port and then goes into the back, the rear of a router, and somehow that traffic has to be routed to an outbound port.

So a router typically is, you know, in a large point of presence, AT&T or Verizon or connects big data centers, Google or Amazon. So in the rear of a router is a scale up fabric. And it’s designed to deal with any-to-any traffic, any packet size.

So typically, you know, in if you look at TCP IP, you could have like a small 40 byte, 20 byte packet, you could have a jumbo frame, 9K, and the and the fabric has to deal with this random traffic. It might have like email, which is SMTP traffic, or it might have real-time video like this call.

So the router has to be robust under all conditions. And so the realization internally was like, there’s a ready-built scale up fabric available for us. If you can make the connection. And so we had the good fortune to be Juniper alum and HP Juniper now, HP Juniper alum.

And so we reached out and partnered with Juniper Networks and leveraged one of their highest end routers and took the scale of fabric in the rear of it and leveraged that for our system. So suddenly we went from having an accelerator that could be world class, highest performing, to an accelerator that is now well connected in a scale of fabric.

So this combination of networking and compute, if you had that, if you had the background, if you thought about it, then some of these dots can connect it and we were fortunate to do that.

Gotcha, fascinating. Okay, so you had the compute and then you needed, ultimately, you needed a scale-up fabric because you’re like, hey, we need to connect, let’s say, 72 chips together in a rack. And instead of having to start from scratch there, you’re able to partner with HPE Juniper, and come up with a scale-up fabric that that fits your needs there.

And okay, so talk to us more about the scale-up fabric because ultimately, I know that this could limit like the amount of tokens per second at the end of the day. So like, but but but take us there and explain it.

RK: Let’s think about the system broadly, right? So I I’ve always been, I mean, I think I’ve had good fortune to have mentors through my career that told me like, when you design systems, think about the balance. So if you if you over pivot on one resource, let’s say you’re compute, compute heavy, then you might be in points in time where the computer is sitting idle.

If you are, if you have undersized something, then, you might be starved of that resource. So you have to think about how you allocate this precious resource in a, in a Silicon. So, the thing that happened to us was that we wanted to build a scale-up fabric that was ready for yesterday, today, and tomorrow.

And the best scale-up fabric in the world was on the back side of a router. Why does why is that? Because it has to have some really exceptional any-to-any characteristics, so you can connect like multiple accelerators or multiple, think of routing devices, and you can connect them together.

It had to have incredibly low latency because we know that, you know, on a video call like this, latency has an effect on how we experience each other. We, you know, today we use FaceTime or whatever and we call people on the other side of the globe. Think of that latency, right? With multiple hops.

It had to be congestion-free, it had to be reliable, and it had to be, it had the capacity, the fabric or the the scale-up network had the should have the capability that you can push its utilization all the way up to 99 plus percent and it will still perform really well under those conditions, under loaded conditions.

So all of these were key elements for us. If you had to look at all of these elements, that was the the Juniper, HP Juniper Networks scale-up fabric in the back side of a router had those properties. So its latency characteristics are like sub one between one and two microseconds.

Okay, so now you look at this picture and then you say, wow, this is a this is the perfect fabric for us. What had happened in parallel in the world in networking, in sorry, in AI models? The models got larger and the traffic patterns went from rhythmic tensor parallelism kind of patterns to random traffic because when you do experts, the experts are random in nature.

So now communication at the if you for a high tokens per second per whatever, communication now becomes a bottleneck. And if your fabric is better than anybody else’s, that communication bottleneck is relieved some bit.

Sure, sure. Okay, this is so interesting. So, taking a step back, you guys said, hey, when you when you first start thinking about this, you needed to balance compute, memory, capacity, memory, bandwidth, networking, bandwidth, and on the scale-up bandwidth, you said essentially, yeah, what’s like the the best maybe maybe you’re able to look forward and think that this would be like the defining bottleneck of sorts.

What’s like the best possible scale-up networking technology that’s out there and you looked and you said, hey, at the back of these routers, that’s a really good one. So the experts are living in different places and for every token, it might need to go to a different expert. So irregular communication pattern. And now, contrast it for listeners with maybe like what’s being used today. Like when you say one microsecond, how should they benchmark that against like, you know, let’s say an NVLink or or AMD’s UALink or something.

Like, is it like an order of magnitude or how should we think about it?

RK: Yeah, so let’s reflect back the last couple of years. So the first scale up system for AI in the world is a GB200 NVLink NVL72. So it’s the first time because prior to that, only eight devices got connected together. So to connect 70 devices, it’s Gen 1. NVLink 72 is Gen 1. We are in Gen 7 of a scale of fabric when we leverage the, you know, HP Juniper Networks fabric.

That’s point number one. So there’s a learning cycle, right? Because when you build scale up systems, you have to build them, learn them, refine them, you know, there’s iterative process. That learning process we can leverage from HP Juniper. So that’s one part. Now, if you really look at the world of AI, most of the most of the vendors now said, okay, we need a scale of fabric.

So you saw consortiums come together with UALink, with Eson, still early days. They’re still in, you know, specs and then early implementation. We still don’t have accelerators that can talk UALink or and and UALink fabric chips and all of those things. So there’s a learning cycle that has to. We skipped those learning cycles with with Juniper because we know the architecture of that fabric.

A lot of our engineers were like core chief architects on some of that in the prior generation. So we know that. That’s one aspect of it. If you look at the Helios system from AMD, they they needed to get to this quickly, so they are now tunneling UALink kind of packets through a standard Ethernet kind of network. So now you think about, you know, typically when you move data over any link, you have to think about, okay, how much space is used by headers, addresses and all this other stuff, and then how much is payload?

Because what matters is how much payload and how long does it take to transmit the payload. So, all of these things are important elements in our choices. The other thing is as a startup, if you carry the burden of building silicon, but also carry the burden of building a system, then you have to qualify the system, the system has to have reliability characteristics.

There’s all these other things that now affect your time to market. So by partnering with HP Juniper Networks, we can leverage an existing shipping system that’s shipping today from Flexus factories in Penang. So we get to get to we get to take our our silicon integrated into and transform a router into a compute box and get to market faster with a reliable scale of fabric. So, I honestly believe, hand on heart, that NVLink is the first NVL72 is the first scale of fabric in the market.

We will be the second vendor in the market with a true scale of fabric, right? That has exceptional latency characteristics. Now, what is the latency? It’s between one to two microseconds. And this is by the way, I don’t know for a fact, but this is what I’ve heard anecdotally that typically the NVLink fabric has some latency characteristics that are not amenable to, for example, decode performance.

So maybe there there’s some refinement that needs to happen with NBL72 in future generations. So, net net, as a result of that, we end up with a system that’s really well balanced and can do pre-fill really well, but can do decode really well too. So you don’t have to have you know, these heterogeneous systems that have to appear to solve this high, what’s called interactive kind of AI needs of today.

One System for Pre-fill and Decode

Yes. Yes. Okay, great. Let’s go into that thread too. So, there was the era where it was just like use, you know, Hoppers for inference and then Grace Blackwills for inference. And then, some early AI ASIC startups who started, you know, well before LLMs, namely Groq and Cerebras, had SRAM heavy, designs that worked in the inference world for high interactivity, decode very fast.

Ultimately, of course, they had their own tradeoffs of, if you don’t have HBM, you have to chain together, you know, tons of these to get enough memory. And then recently in the last, you know, 12 months, basically, we’ve lived in this world where it’s like, okay, if you want really high interactivity, you can use an Nvidia system with Groq, and that lets you extend that Pareto curve to the very high interactivity, low throughput, but high interactivity.

And you know, we’ve seen AMD partner with Cerebras. AMD also bought Tallas recently, which is a different conversation. But so there’s we’re kind of in like phase two. Phase one was just run everything on GPU. Phase two is disaggregation, split pre-fill and decode, put pre-fill on the GPUs, put the decode on the SRAM heavy chips. And then you’re kind of hinting at like this next era beyond that where I, you know, I think Tensordyne is aiming and and so are some other AI ASIC startups.

Which would be actually, can you just use one chip to do both workloads, pre-fill and decode? And so so but tell us more about that because it feels a little counterintuitive because because, you know, as you said, you know, pre-fill maybe compute bound, decode is decode is memory bandwidth bound. So how does like one chip do do both?

RK: Really good question there, Austin. So, let let’s go back maybe 10 months back. So something happened towards the end of last year, right? GPD 4.5 got really good and then suddenly people started seeing, wow, the code is generating is functional. I don’t have to debug it a lot. And then comes, no, GPD, I think 5.3, I correct me wrong.

And in Opus 4.5, right? And so suddenly the demand for AI goes through the roof. And what are those models? My my gut says they’re over two trillion parameter models. So there’s a realization in the industry that those models cannot really work at a high in high interactive environments where the developers are saying, listen, I need code faster. I need everything faster.

And so the reaction to the industry is, well, we have great systems for training. They do pre-fill really well. And you know, kudos to the Groqs and Cerebras of the world that had already shown for smaller models like Lama 70 or GPT OS 120B, high tokens per second per user. So now comes the problem statement. Like I have a system that does really well in pre-fill, can be used for training, but now let’s talk about inference only.

Now I need to pair it with a a system that has a lot of SRAM and has low latency and I can do decode faster. So, I think that is an intermediate solution from these vendors, whether it’s Nvidia plus Groq or Amazon Tranium plus Cerebras or Helios plus Cerebras. Imagine, you know, nine racks or 14 racks to run a two trillion parameter model.

Imagine trying to build a compiler that compiles in CUDA for a for a Vera Rubin and not CUDA for a Groq system. And then imagine connecting them with lots of Ethernet switches because you have to hook up these chassis together. So, that is an answer to the demand of the market, right? Because the demand from everybody else is that we want to run these two plus trillion parameter models and now if you look at Kimi K3, it’s 2.8 trillion parameters.

But we need we need high token, you know, in the agentic world, you want high token rates, for example, tokens per second per user. Here the user could be human or could be an agent for all you care. All right, so now let’s get back to what did we do at Tensordyne. So, when I look at silicon real estate, there’s only so much space. Now, if my compute takes less space, what does it free up?

It frees up space for more SRAM and more HBM.

So you get the best of both worlds. You get what’s called, you know, you can do high throughput, but you can also do high tokens per second per user, with the same system. Why? Because ultimately, what you want to do is when you have compute, what matters is, you know, model flops utilization, MFU, for example. Well, if you have a lot of SRAM, adjacent to, let’s say, a compute array, you can keep that compute array really busy.

And you can hide the latency of getting data from HBM. So if you have a lot of SRAM, you are not penalizing yourself by stalling your compute array every time you’re going to fetch data or activations or weights from HBM. So we start getting the kind of unique properties of both of best of those both worlds. But that’s necessary, but not sufficient. Because now suddenly there’s communication now that now these models also have.

So, you know, you got to compute, then you got to communicate. Then you got to compute, then you got to communicate. And this rhythm of compute communicate or expert selection now, the communication starts becoming a dominant effect on latency or through throughput or tokens per second per user. So, our good fortune was to stick with log math, have the power characteristics, not blow the silicon, you know, you don’t have to build a chip that’s reticle size to achieve the performance that that’s in power with others.

And then suddenly you get the benefits of both of these. So now you have a great machine for pre-fill and decode.

The Tensordyne Rack: Power, Density, and Cooling

Ah, yeah, yeah, yeah. Okay, so the key insight is by using the logarithmic math that we talked about earlier, the compute doesn’t need to be reticle size, it can be smaller. So then the question is, what can you do with the rest of the silicon? And oh, we can have even more SRAM, for example. So you can have a lot of compute, a lot of flops, you can have a lot of SRAM, which is great for decode. But then you can still also have HBM for pre-fill and just having HBM in general, KV cache, that kind of thing.

And then you also feel confident in the competitiveness of your scale up network. So as you’re communicating between all these things, you feel competitive there too. So ultimately then, if I have a rack of Tensordyne, oh, which and by the way, we’ll touch on power too. But my first question is, if I have a rack of Tensordyne chips, is it, you know, 72 chips in your rack? And if so, like, do you still sort of split pre-fill and decode amongst them within the rack?

RK: So you have immense flexibility. So, first of all, we are building the Tensordyne system is only 13 rack units. So it’s a tiny, it’s 1/4 of a rack. We can put four of them in a rack. At 1/4 of a rack, think of our system, it has 72 chips in 1/4 of a rack. That’s point number one. Secondly, it consumes only 30 kilowatts. So if we were to compare do apples to apples, the comparable system is like a Blackwell GB300.

So 1/4 of a rack, one full rack, 30 kilowatts, 150 kilowatts. So, how do we do that? So, first of all, we leverage the Juniper air cooled system, so it’s not liquid cooled. Secondly, we have a scale up fabric that has the characteristics that are necessary for these multi-trillion parameter MOE models. Thirdly, our log math allows us to have silicon that consumes much lower power.

And so you get you get, you know, you get multiple benefits that are compounding in nature that now allows us at a, you know, to have performance at the, you know, GB300 Blackwell levels in a 1/4 of a rack. The second thing is that because we have the scale of fabric has this elegant properties, you can you can do you can put some chips on pre-fill, some chips on decode.

Or in a full rack, we can basically say, okay, there’s one of our pods is a pre-fill pod and three pods are decode pods. But ultimately, if you look at it, because of our characteristic nature of our any to any scale of fabric and the characteristic nature of keeping a keeping a very high MFU, because the SRAM keeps that, you know, I always refer to it as the compute dragon. Keep the dragon fed because the dragon’s hungry, you got to keep it, right?

You can’t you can’t let it off. So you keep the dragon fed. Now you get a system that is so much more balanced and can perform really well. And in some of our metrics, now we are yet to power on our system, but in some of our sense, we think that we could have advantages in the order of almost a magnitude over the latest greatest systems in the world.

Wow. Wow. Okay, I’m going to reflect this back. It feels almost too good to be true. So you can fit 72 in a quarter of a rack. That’s only 30 kilowatts. You can stack four of those in a rack, so 120 kilowatts, or so. And then it that whole rack is air cooled, right?

RK: Yes.

Yes, yes. So you could deploy it in brownfield data centers, existing data centers.

RK: Yeah, so imagine, you know, if you look at it, we have data centers around the world. You know, some of these hyperscalers are 400 data centers around the planet. They’re not liquid cooled. You can’t retrofit them, right? They’re in some of them are in bigger cities or in countries where you don’t have enough power. But you want to get AI around the globe. How are you going to do that? So, our system is because it’s a Telco rack, it’s 19 inch wide, it fits in AT&T, Verizon, Deutsche Telecom, NTT, New York Stock Exchange.

That rack is perfect for being used anywhere in the world. So suddenly you can get that benefit. The other is that you can imagine building smaller data centers, but having the performance characteristics of a large data center. So imagine, you know, with our system, you can actually get, you might need, you can get the, you can get like 1/8 the power, you can get, you can have a data center that’s similar to a very large data center, with the latest systems from our biggest competitors.

So now you can deploy them in smaller locations, smaller cities. You can put, you know, 20, 30 kilowatt kind of data centers, not needing a gigawatt data center, but having the performance characteristics of a 200 megawatt or 500 megawatt data center. So you get all of these benefits too good to be true, but, you know, if you build systems, you know, you have to know the system characteristics and system performance before you build it.

You don’t want to discover it in the lab. So, Yes. So we spend a lot of time at this simulating everything.

Go-to-Market: Partners and Timeline

Totally. Okay, very interesting. So, then my mind naturally goes to a couple questions. One, who are the target customers? Because on the one hand, I think of like enterprise, because it can fit into existing enterprise data centers and maybe instead of needing to buy, you know, nine racks or 13 or however many, you know, maybe they can buy one for their needs or or a few or whatever. And then two, yeah, timing. So, you know, I think you had mentioned that this isn’t totally taped out or stood up or productionized or something.

So, yeah, remind us like, so tell us, who are your your target customers? Because of course, I can also see, yeah, hyperscalers and the model labs and and and stuff being just as interested. And so maybe like target customers, route to market and timing.

RK: Yeah, so, our target customers are certainly number one hyperscalers. Number two, a lot of the neo clouds. We have a significant number of letters of intent from almost all the neo clouds in the world. Well, I want to clarify neo clouds in North America and Europe. And and then, maybe some sovereigns and some enterprises, right? So, but as a startup, you have to be laser focused, right? We don’t have a very large sales team.

So we had to focus on a targeted set of customers and we are doing that. The second question was timing, right? Yeah, yeah, yeah. So we’ve taped out our three nanometer chip with our awesome partner Broadcom. And so we expect devices back late October, early November. And we expect to power on our system and and then, you know, probably sometime in Q1 start doing beta with customers. We have some customers who have signed up for beta.

And then potentially go into production, early production sometime in end of Q2, early Q3 next year. So we’re not far away from there. Now, how can we do that? Because 80% of the system is already validated, qualified, certified in like 70 countries. We are we are building it out of the same factory in Penang, Malaysia. So we can actually quickly go from power on to qualification to certification to shipping of our system.

We have it worked out for the next, I would say, 10 months. But we’re fairly confident that we can get from here to there pretty rapidly.

Nice, nice. So is that because you’re riding the supply chain that Juniper was already riding or is this the advantage of partnering with Broadcom or both?

RK: It’s both. So, you know, Broadcom is one of the largest consumers of TSMC capacity, both TSMC and HBM capacity, right? They have a deep partnership and we have a exceptional relationship with the Broadcom team. They’re great friends and great supporters of us and so we designed, of course, our front-end design is ours, but the physical design and the partnership with TSMC is a Broadcom led. So that’s one part. So that means that from a supply chain perspective, as long as we forecast well in advance, we can get parts from Broadcom, right? That’s part number one. A qualified tested parts. The second part of the story is that can we get to volume with our systems? And this is where the partnership with HP Juniper Networks and the fact that things are shipping out of a Flex factory and Flex knows how to build these systems in volume, gives us those advantages.

The third most important part is that these systems have to be reliable because you’re running business critical AI now in them. So, Juniper’s routers and HP Juniper’s routers are carrier grade. There’s something called five nines of up time. So five nines of up time, if one were to Wikipedia it, is that the system cannot be down for more than 5. some odd minutes in a year or 680 milliseconds in a day.

So that is the reliability characteristic that we leverage from our partner. And so we are able to we will be able to deliver systems that are reliable and can run the largest models in the world, right? At 2.8 trillion parameter like a Kimi K3 or a Quen or from the frontier labs, their biggest models, right? Our systems will have adequate amount of memory, you know, if I if I look at the quarter rack system, we have we have 10.8 terabytes of HBM capacity. We have, you know, significant, I would say, over 18 gigabytes of SRAM.

Wow.

RK: So imagine we have SRAM capacity of the the big SRAM guys and we have DRAM capacity of also the largest thing. So now, whether it’s KV cache and agentic workflows, we we’re well set up for those system for those markets and those customers.

Mm, mm, fascinating. Amazing. A really nice way to punch above your weight, so to speak, as a startup by kind of by, you know, partnering with people who can help bring you along. When you mentioned Flex, by the way, is that Flextronics? Used to be.

RK: It’s Flextronics. Yeah, yeah. Okay. Yeah. And and you know, I mean, most of Silicon Valley thrives on partnerships, right? You can never go alone, right? Whether it’s silicon partners, system vendor partners, the ecosystem actually lends itself to that partnership. And we we, you know, we benefit from it, we mutually benefit from it, and we we we really love these partners because they are helping us get to that scale, will help us get to the scale, and they’re very supportive of us, right? They’re supportive of a startup. Not only that, HP Juniper Networks is an investor in the company.

So you think about it, they, you know, in in all of these things, you know, you can never go it alone. It’s like building a team, right? In the company, the team is multidisciplinary, but you can’t build a product by yourself. All these functions come together. It’s the same in the ecosystem of of vendors and partners who come together to build these solutions.

Yeah, sure, that makes sense.

RK: And and customers are the final, you know, arbiter of product, right? And we we customer validation is going to be super important for us over the next many months.

The Software Story

Yes, totally. Okay, so let’s let’s land the plane there, customers. So, you know, you mentioned really ramping up in 2027 with customers, beta, and then production. The one thing we hadn’t touched on yet was software. So, you know, for those model labs, those hyperscalers, what does it look like as far as how heavy of a lift is it to take, you know, your system and get their software, their frontier grade software up and running?

RK: Yeah, exceptional question, Austin. I think a few things have happened, right? One is that from the signals of these disaggregated stories, we understand that the moats of CUDA don’t exist anymore for inference because we have proof positive of a number of inference companies running solutions and then these disaggregated solutions with CUDA and non-CUDA or neuron and non-neuron or Rocm and non-Rocm, right? So we have this. So, I think there are a couple of things that have helped us.

One is obviously we have to build a robust compiler for our hardware, but also at the higher layers having technology that can take PyTorch or Triton kind of models and then convert them quickly and compile them quickly is super important, which we spend a significant amount of time. So for example, in our engineering organization, almost 60 to 70, 60 plus percent is software, right? Because you have to have a software team that does that. But one other thing has happened with this beauty of these new Opus 4.5 and and, you know, GPD 5.6 and other models is that the agentic workflows are now proving that you can take kernels and quickly get them ready for your hardware.

So we have incredible momentum on taking like the best models in the world and quickly getting them running on our, you know, in our simulators and then eventually in our hardware. So the the walls for taking new architectures and new systems are quickly crumbling when it comes to software because you can take models and because you have all these workflows and automated kernel generation capabilities that you can actually get to there, get to that and also get to high what’s called utilization of our systems quickly. That means that you can get first proof positive that the model works on the system and then you can iterate quickly to get the model performance up in the system.

So both those things seem to coincide with, you know, our systems coming on.

Yeah, yeah. Well, yeah, what fascinating timing with the rise of the agentic AI to kind of help you with that that last hurdle that people are a little concerned about, you know, am I going to have to spend a lot of time, not to your point, not only getting my code to run on this new system, but also optimizing it to get the most utilization out of it.

RK: Indeed, indeed. And that is super important because, you know, you don’t want an 800 horsepower car and get like 50 horsepower out of it, right? Because then you’re leaving stuff on the table, right? You’re paying for it, but you’re not using it. And we believe that we have we will have some of the best MFUs in the industry with our system.

Nice. Amazing. Okay. Well, we’re at time, folks. I hope you learned a lot about RK and Tensordyne and networking, a lot in logarithmic math. We covered a lot of ground here. RK, you’ll just have to come back and keep us updated, you know, as you guys get closer to delivering ships chips and systems and when your you have customers to talk about, you know, can’t wait to hear more.

RK: Austin, again, thank you for the opportunity. Thank you for, you know, the very thoughtful questions and, you know, and navigating all the different parts of the terrain on our behalf. And, you know, we’ll certainly keep you in the loop, keep you posted as we make progress, as we bring up our systems, as we get to beta. And would love to come back and tell you about our success and our progress. Again, like I I want to I can give credit to my broader Tensordyne family because we we won’t be here without the the complete dedication of a number of people.

And then most importantly, thank our partners, Broadcom, TSMC, HP Juniper Networks and Flex and others because we can’t be here without any without all of them helping us in this journey. So thank you, Austin. I really appreciate it.

Yeah, team effort. Very cool. All right. We’ll talk we’ll talk next time.

RK: We certainly will and my best to you, Austin. Thank you.

Thank you.

RK: Cheers.
