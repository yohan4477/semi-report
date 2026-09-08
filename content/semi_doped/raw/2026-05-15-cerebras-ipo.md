---
source: https://daily.semidoped.com/p/cerebras-ipo
title: 🎧 Cerebras IPO - Semi Doped
kind: transcript
---

🎧 Cerebras IPO

Cerebras IPO is the only thing to talk about this week. 🔥

IPO prices at $185/share → pops nearly 70% right after! Vik and Austin record on the morning of May 14th, pricing day, and cover everything about this wafer-scale engine stuff. In a water-cooler-style convo when you’re not ready to get to work kinda way.

Things we cover:

Basics: what wafer scale is, how GPUs compare

Basics: what wafer scale is, how GPUs compare

Actual construction of WSE; TSMC special sauce

Actual construction of WSE; TSMC special sauce

Power and cooling insanity of rack-in-a-wafer

Power and cooling insanity of rack-in-a-wafer

Curse of Trilogy Systems; why they failed, why CRBS succeeded

Curse of Trilogy Systems; why they failed, why CRBS succeeded

The OpenAI deal

The OpenAI deal

Cerebras: Mission Impossible

Cerebras: Mission Impossible

This podcast is lightly edited for clarity.

Learn from semi industry experts. Sign up for free daily updates!

Welcome and IPO Day

Austin: Hello listeners, welcome to another Semi Doped podcast. I’m Austin Lyons of Chipstrat and with me is Vik Sekar from Vik’s Newsletter. So Vik, we’re recording this, it’s the morning of May 14th, Cerebras IPO day. What do you say, should we talk about Cerebras?

Vik: Yes, it’s all about Cerebras today. That’s it. Nothing else. Single focus topic. No deviations.

Austin: Totally, I love it. Which by the way, I don’t even know how to pronounce it. Cerebras.

Vik: I don’t know, Cerebrous? Cerebral. How do you say cerebral?

Austin: Right? Yeah. Cerebrals, Cerebrous. Totally. So listeners, you know who we’re talking about. The big wafer company.

Vik: Yes, those guys.

Austin: All right, so let’s see. Okay, so they priced their IPO, 185 bucks and they raised $5.5 billion, I believe. I was looking at it this morning to see if the stock price is immediately bouncing around and stuff, but it was just pegged at 185 as far as I can see. So I don’t know if there’s some price discovery thing that happens early in the morning or what.

Vik: Yeah, this was an insane IPO because it was oversubscribed massively and they used an eBay bidding style approach where they were like, okay, how many shares do you want and at what price are you willing to go up maximum? Pretty much like eBay does. And then people were putting in those orders. It’s kind of insane. Then what happens is Bloomberg reported that Arm and Softbank came in last minute and tried to buy it at the 11th hour, typically like an eBay snipe. You come in last minute with your bid, the eBay snipe, didn’t work anyway, didn’t get bought.

But it was, I’ve been tracking it all week and it was, initially it was like, oh, it’s going to be priced at 135. And I saw it was going to be priced at 150 to 160. Finally, it came out to be 185. I believe they were intending to raise like 3.5 or 4 billion anyway. Came out about one and a half billion above that. It’s insane.

Austin: It is crazy. Man, yeah, congrats to everyone who has equity in that, the team and all the venture capitalists. So what do you say? Should we remind listeners at the highest level what Cerebras builds?

The Wafer-Scale Engine

Vik: Yeah, there’s some technology and history behind this whole thing, which is an interesting discussion that we can have, at least for me, because I’m such a technology-minded person. So let’s get into it. So this wafer company that we were talking about, Cerebras. The reason we call it the wafer company, the guys who make the wafers, is because typically how wafers work is it’s just like a giant dinner plate. And then you’ve got many, many little GPUs on it. At least this is what Nvidia does. So they take out all these GPUs and package them separately. They just cut it out of the dinner plate and they package it and they ship it. That’s how typically GPUs work.

But Cerebras was like, why do we have to cut up this stuff? We want to keep the whole wafer as a single chip. So all those chips that you would have otherwise cut out, they just hooked it up together with metal lines on the wafer. That’s how it came about. And they were like, okay, now this whole wafer is a chip. And that’s about it.

Austin: Which I’d say it’s pretty intuitive in that if you look at Nvidia’s roadmap, it was one die per chip and then it’s like, wait, we want to scale bigger, so let’s have two dies. So you’re taking this wafer, you’re dicing it up into individual dies. It’s like a checkerboard and you’re cutting out all the little checkerboard squares. But then all of a sudden, they’re putting them back together and then they want to go to four dies, and you can imagine where people want to go to eight dies.

And by the way, when you cut these up, now they have to communicate with each other. If you’re lucky, you can stitch them together and it feels as if they’re one piece of silicon, but otherwise now you have to go networking and even switches and whatever. So conceptually, I think everyone can understand — yeah, don’t cut it up, leave it all on silicon, let it communicate all with each other, have better network bandwidth, et cetera.

Vik: Yeah, so that’s the whole idea of this. And the beauty of this is that you can fill all of these chips with SRAM in it. And since SRAM-based accelerators are so much faster because the memory bandwidth is so amazing, you can get the entire wafer’s worth of SRAM for inferencing, which is amazing in theory, for certain use cases, which we’ll talk about. It’s amazing. This whole wafer.

If you look at the wafer-scale GPU that we’re talking about, it’s about the size of, I would say, 60 Nvidia H100s. And it consists of about 84 reticles, which is basically that one shot that people are cutting out. It contains about 84 of them stitched together in a grid format. And so this is a piece of engineering, and we’ll get into why that is so amazing.

Now, for anybody who’s dealt with these wafers and dealt with silicon technology before, one thing is very clear. You can never make a perfect wafer. A wafer is always going to have defects. And that’s why you always hear people talking about yield, or what is the yield of 18A, and that means how many defects does this wafer have? Lower, the better. And every wafer has them. There is simply no way to avoid this whole defect thing.

So what does that mean for Cerebras? How come the Cerebras wafer is defect free? No, it has defects. And the way it works is instead of these giant GPUs that are there and stitched up, which is the analogy we used to explain the idea, in reality, each of them are actually very tiny. They’re not as big as a GPU. Each of them is much, much smaller. It’s like 1/100th or 1/20th of a GPU in size. And these are their processing cores.

They basically have a little bit of processing and a little bit of memory. Each one a little bit. These little thingies are the ones that are ultimately all connected together in the whole wafer. There are about a million of these things. And out of the million, the exact number is like 970K or something. Anyway, simply just think about it as a million. Out of these million, about 900,000 of them are the ones that are actually working at any time.

And the reason it’s 900,000 is because you have to overcome these defects. So whenever they figure out that this particular core has a defect in it, what they do is they have a networking fabric that is on the wafer, and all they do is they just route around it. Like, this chip is bad, so let’s just go to the spare one right above it, and we’ll route around it. We’ll hook up the wires, just avoid the defect.

So they look at a wafer — I don’t know how they do this by the way, do they inspect every wafer? Because every wafer has different defects. Anyway, they look at a wafer and be like, okay, these processing cores are all terrible, let’s route around them, and you reconfigure it, you get a defect-free chip. Which has 44 GB of on-wafer SRAM operating at 21 petabytes per second memory bandwidth. That’s amazing.

Austin: Amazing. Yeah, two things I want to add in here. So for listeners, zooming you back out — when Vik is talking about yield, as you know, because there’s just this statistical noise, the stochastic things happening, you get a dopant in the wrong place and something might short circuit or it might be just an open circuit and it doesn’t work. If the size of the chip gets bigger, then you have a much more significant surface area for a defect to happen. And so the bigger and bigger your chip gets, the more likely that chip is going to have some bad defects.

And so you might think, well, if the chip is the whole wafer, surely every wafer is going to fail, right? And what Vik is saying is no, no, they’re making a wafer, yes, but it’s full of all these teeny tiny little cores. So each tiny little core has a tiny surface area. So it’s going to have fewer defects. So each core will have good yield. But yet at the size of the dinner plate, you’re still going to have some that don’t work.

And so literally, I think when they power on the wafer, they just test every core, and maybe it only happens once, I don’t know how often this happens, but they test every core, and then yes, whichever ones don’t give a signal back, they say, okay, row 10, column 13, that core’s dead, and so you just map around it, and then they just know that once they run their software that probably some sort of orchestration system knows to not orchestrate to that little area. So pretty cool. It’s a really interesting innovative way to tackle yield and harvesting good cores and routing around other ones dynamically.

Then I will say also Vik’s SRAM point. There’s different ways to store memory. We’ve talked a lot about memory. SRAM is with transistors, six transistors. And so that’s the beauty of having a big silicon wafer just full of transistors is you can allocate transistors to memory, fast memory, or you can allocate it to logic. And in this case, they’re allocating about half of all the transistors on the chip to 44 gigs worth of SRAM, which ends up being quite a lot.

Vik: Were you saying that I think each compute core is roughly 50-50 compute and SRAM? Is that how it is?

Austin: I think so, yes, because I think they want the SRAM very close to the compute core. It’s almost like processing in memory, if you will.

Vik: Yeah, yeah, yeah. So yeah, that’s basically the idea. You give it this little cores have 50% silicon dedicated to SRAM, 50% to compute, have a lot of them stitched together, route around the broken ones, and you have a working wafer that works at enormous SRAM speeds and it has 44 GB of capacity.

Power, Cooling, and Thermal Expansion

Vik: Now we have to talk about a few things. 44 GB is not nearly enough to hold any kind of thing. Okay, so that brings up some concerns. The second thing is how are you going to deliver power to this thing? This is a big, big question because you essentially have a rack’s worth of chips on a single wafer. Seriously, that’s what it is. When you put 84 reticles — 84 reticles could be 84 GPUs, roughly speaking. That’s a lot of chips. The NVL72 only has 72 chips. You’re talking about 84 chips. That is a rack-scale GPU count essentially in a single wafer.

Now, you can imagine that this requires some serious power delivery techniques and some serious thermal issues that have to be dealt with. So these are the basic things that we have to address in some detail. I recommend that we get to the SRAM question and the limited bandwidth slightly later. The reason is that there’s a lot of stuff to talk about.

But I’ll just mention briefly what the power delivery looks like. Each wafer consumes about 23 kilowatts of power. It’s enormous. If you think about a one volt supply that is feeding these GPUs, you’re talking about something in the tens of thousands of amps of current that have to flow into a single wafer. There is no way that you can supply the wafer with a power connector on one side and expect all this current to flow to the other side of the wafer. I point that way, but it’s really not that big. A wafer is a 12-inch wafer. It’s a foot, that big. But it’s still a lot. You will drop a lot of power from one end of the chip wafer to the other end.

So the way they do this is that they have these specialized vertical power delivery connectors that come in across hundreds of points on the wafer and deliver power directly on the vertical way. It’s the only way you can deliver power to all these chips. So that whole thing was completely unique to how Cerebras built its architecture.

The second thing is cooling. They have this entire crazy cooling system that has vertical flow of micro fluidic channels in the thing and you have to cool the whole wafer at once because remember, a wafer can have hot spots. You’ve got hot yards up there, you have to cool all this. So the cooling is done with what they call the engine block, and it’s just this honking piece of metal that has this complex construction. If you go into the Cerebras website, you’ll see it. It’s amazing. The whole cooling problem is also amazing. You have to cool a rack’s worth of wafers in a small space. That’s insane.

The one other thermal aspect of this is that the wafer actually expands too. So not only do you have all these problems, the wafer expands. So their connectors are also custom designed and patented by Cerebras themselves. They have this unique material that goes there and controls the coefficients of thermal expansion in a way that things match with the board and the connectors and the PCBs and the power delivery. All of this has to match. So they have a whole patent that Cerebras actually owns on this, to just deliver power and cool it. So that’s my spiel on how complicated it is to develop a wafer-scale engine.

Austin: Okay, wow, yes. So first of all, you said it’s not like you can just put some power pins on one side and route the current all the way through, but they actually have to have a grid coming from the top or maybe it’s from the bottom and deliver the power to all the little places individually. And then on top of that, getting power in is complicated, but also getting heat out is complicated. So it sounds like they have to engineer some big crazy engine block, which yes, we should all go look at a picture to figure out per dinner plate how to get all the power in, how to get all the heat out. Now tell us very quickly when you say that the wafer expands and you’re talking about thermal coefficient, tell people what that means.

Vik: Whenever stuff heats up, it expands. Essentially, the wafer also expands. I was looking at some numbers. It expands by about a tenth of a millimeter. And that’s a problem. Alignment goes out of whack. And not only that, when you have attached it to a printed circuit board on the other side, and you’re delivering power through this printed circuit board, there are different coefficients of expansion on the printed circuit board versus the silicon wafer. They don’t have to expand at the same rate. So what is a tenth of a millimeter here in the silicon might be a hundredth of a millimeter on the printed circuit board. Now you’ve seriously got connectors and stuff that are not going to stay connected anymore. They’re going to rip off. So that is a problem to solve when you’re putting that much power and that much current through a single wafer.

So they have some unique solutions towards this. I’ll just leave it at that. They had to solve this all by themselves. This is not a unique industry problem. This is a unique problem to them.

Not About Cost

Austin: Amazing. So quick question, just riffing here. The idea of having a wafer instead of dicing it all up and then packaging and connecting everything, at first it sounds like it’s actually going to be a lot cheaper and then you can yield harvest correctly and everything. Because you’re not processing one 20, $30,000 wafer, chopping it all up, packaging it, interconnecting it. But on the other hand, you’re talking about these different trade-offs. Okay, great, you’ve got the big wafer and it’s full of all these 900,000 harvested processing elements, but it’s really complicated from a mechanical and thermal and power delivery perspective. Do you know, how does that impact the cost? This big engine block thing must not be cheap. Is it kind of like, it’s not a cost advantage one way or the other?

Vik: I don’t think this whole thing is about cost at all because all those processes exist, yes, but ultimately the engineering and if you think about the non-recurring engineering, NRE costs to develop something like this, including, by the way, we didn’t mention, just stitching different reticles together is not easy because it requires patterning slightly differently because the mask when you pattern a reticle only has a shot that is a certain size. That’s why chips are a certain size because the shadow it casts on the wafer is a certain size. So if you have to connect chips up together, that itself is a manufacturing complexity that they have worked out for TSMC over the last decade.

So this is right from the get-go, a non-standard wafer fabrication procedure all the way through the power delivery, cooling, expansion, mechanical problems. Everything is challenging. This is a very hard problem Cerebras has solved. It is kudos to them. And we’ll get into how people have failed at doing this too. And it’s amazing that we now have a wafer-scale engine from a company that’s working and has gone public. This is history in itself.

The 44 GB Wall and Off-Wafer Bandwidth

Austin: Totally. Okay, so it’s definitely not about cost. So when they started down this path at the get-go, they said, hey, we’re going to have to make a ton of technical innovation to make a wafer-scale engine work from manufacturing, power, cooling, all the things. But it’s going to be worth it because it gives us a ton of compute and it gives us a ton of on-wafer memory. And probably at the time the company started, which was pre-ChatGPT, 44 gigs of SRAM probably seemed like plenty.

But let’s dive into this. We’re in the LLM era where even a small to medium size model is more than 44 gigs, right? Llama 70B already is going to be bigger than that, depending on how you quantize it, but you need enough storage for activations and KV cache as well. So let’s talk about what happens even with inference when you can’t fit all the weights and all the KV cache on one wafer.

Vik: Yeah, that’s the whole problem, right? If you can put a model that’s within 44 GB and it runs SRAM-based inference off of a single wafer, you get extraordinary speeds. I mean, you get tokens per second that you can’t dream of with GPU-based systems. And you can even compare it to LPU. LPUs don’t have as much. You’re not talking about a wafer-level system. And a single LPU has a few hundred megabytes of SRAM, not 44 gigabytes. And you have to hook up a lot of them together to fit a model and then you have networking overhead. All that concern exists.

But now as long as you can fit a model in 44 GB, it’s great. Really modern frontier models are actually much, much bigger than that. So then the question becomes, how do you do it? Now you have to put multiple wafers in a rack and you have to split it up. You have to split up the model between these wafers. And remember that as much as power was delivered on the whole face of the wafer, the networking doesn’t work that way. Networking still leaves through one end of the chip and is significantly slower compared to the on-wafer bandwidth of data movement, which is a big bottleneck. At the moment you have to go off-wafer, you’re in a bottleneck. That’s the problem.

Austin: Gotcha, yes. So you’re saying if we have a small enough model that can all fit on the wafer, then you can unlock crazy tokens per second that just aren’t even reachable with GPUs and maybe not even with Groq’s LPU because they only have, like you said, 170 megabytes or something very small of SRAM. And so that makes me think, okay, there’s got to be use cases where it’s a small model and you want it to run crazy fast, crazy high throughput.

So I think of Google rewriting ads on the fly where they probably only need a small model and they just need to know like, this is Austin and here’s a tiny bit of context about him. So when you advertise, rewrite the ad in almost real time so it still comes back really quickly. But you’re saying when you actually want useful enough language models that don’t fit on one wafer, getting information off the chip — which by the way, the chip is a big square essentially of a ton of tiny little chips — getting information, you still have to get it off the edge of the WSE somehow and over some network communication and into another wafer. Have they said much, do you know much about how this scale-up interconnect works at all?

Vik: I don’t know much about the interconnect, but one of the ways you can deal with it is that you do parallelism, which means that you can do various kinds of parallelism. So what that means is basically you break up the whole problem into what is called pipeline parallelism. One option, which means that wafer one handles a few attention layers, wafer two handles a few attention, whatever, then wafer three handles a feed forward network, and then you pipe it through this. But then it’s not that straightforward because data has to flow through the pipe between various parts of the inference process.

Then you’ve got tensor parallelism where you say, okay, look, we’ll break up the matrix into five parts and we’ll run it across five different wafers, tensor parallelism. Finally, you’ve got expert parallelism which is, we’ll run this expert on this wafer and this expert on this wafer. The ultimate benefit of running a wafer-level system is diminished by the fact that you have to somehow break it up into wafers and that you don’t have communication bandwidth between them. That is the fundamental downside as to why it goes against the very basic concept of wafer-scale engines.

Austin: Yeah, okay, got it. So ultimately the wafer-scale engine is best when everything fits on the wafer and you’re pointing out that, well, if we break up the problem, there’s ways to break up the problem into sub-problems that can fit within the wafer. But at the end of the day, they still have to communicate with each other. But maybe you can overlap some of the communication and computation by using parallelism to keep things tightly into the wafer. But at the end of the day, that is going to be a bottleneck, this off-chip, off-wafer IO essentially.

Which by the way, I think I saw Semi Analysis had this great article that came out yesterday. I tried to skim as much as I could. These are like PhD theses that take you a month to read because they’re so long and have a nice big team. But I believe I saw somewhere in there that Cerebras was experimenting with wafer-scale photonic interconnects. It’s hard. There’s not a ton of bandwidth between every core and off chip, but what if we put another wafer on top and that allowed you to route information essentially in the Z direction, almost like 2.5D? You could go up to this photonic wafer, connect wherever you need and then come back down. I didn’t read too much about it, but I thought interesting. It also sounds complicated and challenging to take two wafers and connect them like that.

Vik: It’s already hard enough what they did. Now you want to put… there was also talk of stacking SRAM wafers on top of this or DRAM wafers and bonding it. Have you not solved the hard enough problem already? You want to make it harder?

Austin: Right, right, right. Totally. Well, okay, and that’s an interesting point, which is, okay, if you’re looking at all these other AI accelerator startups, they’re talking about memory hierarchies. Like MatX, we talked to Reiner Pope and he was talking about can you put weights in SRAM and KV cache in HBM. And other people, Qualcomm, Intel, maybe d-Matrix, others have talked about using DDR as another tier of memory storage. And so the question is, could Cerebras’s SRAM-only wafer also use DRAM in a way that’s not just pipe it off the slow pipe that they have over to some rack full of DRAM or something?

And so then people postulate, well, what if you took a wafer of DRAM and just attached it to the compute SRAM wafer? But also my head is like, well, Vik just told me that’s how power is getting in and that’s how cooling is getting in. So if you’re going to start slapping other wafers and you got a wafer sandwich, how do you cool it all? How do you power it all? Sounds complicated.

Vik: Yeah, yeah, I’m thinking of a multi-stacked wafer, Cerebras wafer-scale engine, photonic layer, memory wafer, then next Cerebras wafer stack, and then wait, how do you power all this stuff? I don’t know, man.

Austin: Throw some high bandwidth flash in there. Why not?

Vik: Why not? It’s going to make the problem harder. This is not hard enough.

Austin: Yeah, right. I mean, we want jobs for our kids, right? They need to work on challenging things.

Vik: Yeah, yeah. We should talk about basically what this means for their business and who’s going to use this stuff really and why it’s useful or whether it’s useful at all. I think we should talk about the use cases, not the deep silicon tech.

Austin: Yeah, all of that. But one, maybe as a transition, this is very technically hard. And you mentioned earlier, someone has tried this before, this wafer scale. Tell us quick.

The Trilogy Systems Saga

Vik: Yes, yes. This is a good story. I think this is a good transition to going to talking about business. Because just when we said that, oh, this is super hard and Cerebras has done great to solve all these technical challenges. Oh, by the way, here’s some more you can solve or whatever we’re doing over here. This has been tried before. And this is the story of Trilogy Systems.

In the 1980s, Gene Amdahl raised about $230 million, which is about close to a billion dollars today, to build basically the same idea that Cerebras has achieved today, the wafer-scale engine, except that at that time it was a 2.5 inch wafer. It’s a small wafer, not like this giant dinner plate. It was a small saucer wafer. But then the ambition was amazing. It was way ahead of its time. Because at that time in the 1980s, Gene Amdahl said, okay, look, I’m going to make a wafer-scale chip. Why should I cut it up?

And their idea was the same. They’re a bunch of smart guys, so they said, we’ll just route around defects like Cerebras does today and we’ll make it work. Anyway, the story goes really crazy, but they really didn’t succeed, because the yields in the 1980s for even a 2.5 inch wafer were just too low. Manufacturing processes were not at the sophistication that they are today. We have figured out a lot of things in wafer manufacturing today that actually makes wafer-scale engines possible.

But then it got crazier. The story of Trilogy Systems got crazier. So what happens in early 1980s, I think 1982, is that there are these storms that flood the factory. So it’s a $33 million factory, and then water starts seeping into the air conditioning and all of this stuff. And what happens is the pipes start to rust. It starts to blow microscopic dust into the clean room. And nobody knew what was happening to the yields. They didn’t know that this is due to water seepage and rust that now the clean room is getting sprayed with dust and all the wafers are dying because of this storm that came through.

So they took months to figure this out and they blew through capital because it was blowing dust into the clean room. And at the end of the day, they’re running out of money. So they wanted to complete this wafer-scale engine. So they said, okay, let’s make a Hail Mary IPO. In 1983, they went and said, we’re going to go IPO and they raised like $60 million without a product in hand. They didn’t have a product. And they used all that money to still try to make a working wafer and just nothing happened. And then ultimately the public market lost it. They’re like, okay, that’s it. You guys are not going to do any of this stuff. And so the stock at the time, which was like $12 a share, eventually plummeted to near zero in the next couple of years that followed. It was totally terrible.

And it doesn’t stop there. The story gets even worse, even sadder. Because right after this, this company getting wrecked by a product not working because of microscopic dust caused by rainstorms, Amdahl crashed his beautiful green Rolls Royce. And while all this chaos was happening, their finance guy, who I’ve written down his name as Clifford Madden, he died of a brain tumor at the height of the crisis. The whole thing is going on and he dies of brain tumor. And so everything has run out now. So the company was forced to restructure, they laid off a lot of people and then finally they kind of abandoned the idea of building a wafer-scale engine supercomputer. And all of that money that they had raised, everything evaporated, nothing happened. And wafer-scale technology was dead.

And basically, Amdahl said, we are not in a position to do this for another 100 years. We cannot make this happen for another 100 years. He used the rest of what money was left to buy some mini computer startup. And so he pivoted out of wafer-scale engines. Eventually after the whole thing, he was basically defeated by the wafer-scale engine process and he stepped down at the end of the decade, in 1989. Amdahl stepped down and said, that’s it.

So now what Cerebras has done is made that a reality. Sure, it took, I don’t know, 40 years. It was not his 100 year estimate. It took 40 years. We’re 40 years since the Trilogy Systems saga. But it puts a little bit in history to appreciate what we have today and what kind of engineering has gone behind this. I don’t know. We’re probably going to talk about, it’s not good enough. Memory bandwidth is not good enough. It doesn’t make enough money. Revenue will not grow. Their business model is flawed. We’re going to probably nitpick at all these things. But from a pure technology sense, it is fantastic. What Cerebras has done is fantastic. That’s my story.

Austin: Amazing, yes. And they did it without running out of money. They made real products. They’re on the wafer-scale engine three? Is that what they’re doing? So they’re able to fund several iterations of this. And by the way, is this Gene Amdahl of Amdahl’s Law? Is he the guy that’s named that?

Vik: Down three, yes.

Austin: Nice, amazing. Cool, wow, fascinating. Well, let’s hope that this is not their story of IPO and then crashed to the ground, but IPO and onwards.

Vik: I don’t want the curse of wafer-scale engines carrying on anymore. We want success.

From Supercomputing to Inference

Austin: Exactly. But yeah, let’s talk about the business and let’s talk about how they got here. So do you happen to know — I tried to go back and I couldn’t find early product positioning — but what problem, what business problem were they trying to solve at the start of the day? Because to be honest, as an engineer this feels like a cool engineering project, like, hey, what if we did this? I’ll bet we could do this. I’ll bet that would be useful, but it doesn’t necessarily tie straight. It’s not obvious how that ties into, this solves a real customer problem.

Vik: So the one blanket answer to ask, whenever you ask, why did they make this chip before LLMs, the default answer you can always think of is for supercomputing. So they figured that you can just do supercomputing out of this and make a great chip that gives enormous flop performance if you do wafer-scale engines. That was, I would imagine, their initial vision of this company. It’s always supercomputers.

Austin: Okay, because supercomputing used to tie 100,000 CPUs together even, and eventually maybe GPUs, but they’re saying, whatever the processing element is, why not tie them together on the same piece of silicon, essentially?

Vik: Yeah, so it’s ultimately a supercomputing play when it started out. At least that’s how I think of it. Maybe there’s another story. Somebody will let us know. They always do.

Austin: Yeah, leave a comment.

Vik: But ultimately, when the training era took off of LLMs, they pivoted into doing training. They figured, hey, let’s do this because you’ve got this enormous memory bandwidth. Actually, it is not memory bandwidth at the time. It’s the same supercomputing problem. You can get a lot of flops out of this. So why don’t we do training with this stuff? It’s amazing. It’s a supercomputer you can use for training. So that was the idea.

And there were reasons it didn’t work out for training. The CUDA expertise, the CUDA moat was so amazing. People just decided to just go with that. And it was easier to program. How are you going to program this stuff? It’s not really that easy. And yeah, maybe it was just not in the right time at the right place for training. But it was because it was not a memory bandwidth bound problem anyway.

But anyway, right now where we are with Cerebras is that they pivoted to inference. And the need for memory bandwidth during the decode phase of disaggregated inference is a gift that landed in Cerebras’ lap.

Austin: Definitely, totally agree. In fact, open models was a gift to Groq. Groq was a gift to Cerebras. Nvidia’s Dynamo and disaggregating prefill and decode, all of these things came before and the time is perfect for them.

Vik: Yeah, that’s what has led to this moment where we can actually do something with this. So that’s how we’ve landed up here.

Austin: So what then is their current value prop today? Why are people even interested? Why do people want to invest? Why are they IPO-ing?

Vik: The thing is, the value prop is, of late for inference engines, especially since the NVIDIA acquisition of Groq, is low latency inference. It seems like LLMs are generally slow, and I agree, even if you use Claude Opus, you ask it a question, it thinks for five minutes, it’ll give you some answer. It’s annoying sometimes. You’re like, dude, I just want to know what is the capital of this and it takes a few seconds to tell you, whatever, it doesn’t matter.

Even I find myself wishing sometimes, can this be faster? I’d really like it to be faster. So when you’re coding or something, it really means time is money now. Because if you have faster inference, you can get a product out to market better and faster, and that can translate into revenue. This is a race that’s going on. Everybody wants immediate results. The need for speed has been around always. Whether you think about it networking, computers, flops, or whatever, everybody wants to go faster. So this is the same theme around that.

So essentially that’s one of the things. And then there is some applications, maybe financial trading or low latency translation, live voice translations, which I don’t know, why do you need such amazing technology to do voice translation? It’s a premium technology. The tokens out of the system are going to be a premium. And the premium token cost better have monetary return. That’s why I said financial analysis or coding or maybe, but not low grade items.

So that’s the whole thing. And the whole inference market also, most of us don’t need this low latency inference. I can wait another minute, I’ll go refill my cup of water by the time I get my answer. For most of the population, GPUs are just fine. So I don’t know what fraction of the inference market requires low latency inference, but it’s not a lot. And so this is going to serve that market.

Austin: Yes, yes, I mean, I will say, agents do come to mind for me, which is if businesses are starting to build business processes where you’ve got agents running off and doing lots of work. Yes, sure. Some of it’s tool calls that might be network bound or CPU bound, but it does feel like once you’re starting to chain agents, it’s just a compounding problem, which is like 10 seconds and then 10 seconds and then 10 seconds versus one second, then one second, then one second.

But I do hear you, obviously coding makes a lot of sense where it’s just like, hey, if this can go fast and the developer can stay in the flow, you don’t necessarily think hard about the architecture, but after that, you’re just spitting out JavaScript and Python, don’t overthink it, just go faster.

Vik: I refer to coding as agentic coding. I don’t really ask it to write functions or anything. You just say, do this problem, and it figures out and does it, and it launches tools. Whatever, build a database, build a website. It figures out everything. Coding has kind of become agentic anyway now. But yeah, essentially, that’s the whole point. You want stuff done quickly, and that’s where the market lies. And that’s why NVIDIA got a hold of Groq chips and then their LPUs. And they’re like, okay, fine. We have the ability to provide low latency inference now.

And Cerebras is going to be the same thing. Except that I feel like the complexity of these racks and the hardware within it, I always have a concern of, how can this scale? Like when you tell me Groq LPUs are little chips with SRAM in them and then you hook it up on a board and you do the regular things. I’m like, yeah, yeah, I see that. But when you tell me I have to do all these wafer-scale engines, all these complicated things and do it at scale, I don’t know, can you deploy 100,000 wafer-scale engines in the next year? Do you have the supply chain to do that? Is everybody prepared to generate at that level? What is the deployment thing? And that’s another thing we should talk about, the OpenAI deal. Do you want to talk about that now?

The OpenAI Deal and the Wild West of Inference

Austin: Sure, yeah, let’s get into that. But first, let me just say one thing, which you actually hit on something very important, which is the supply chain and the ability to ramp quickly. When you invent new technologies, like the engine block, you usually have to co-invent it with supply chain partners. And then the question is, if great, you got a prototype and now OpenAI, Anthropic, Microsoft, Google, whoever comes to you and they’re like, yeah, we would like a small data center’s worth of these, can all of your supply chain partners suddenly have this new thing that you’ve co-designed with you and can they quickly jump to the crazy volume? Or will even Cerebras, best case scenario, they have a ton of demand, but they actually can’t scale their manufacturing supply chain to meet it. So that’s an open risk and an open question that would be interesting.

Vik: But to push back on that, isn’t that the story of the entire AI data center chase off right now?

Austin: 100%, but at least it’s components that they already build at massive scale, you know.

Vik: Also, at least maybe there’s a chance that at least two, three players can build it. Lumentum’s lasers are in big demand, you have shortages, but Coherent is saying, yeah, we can build it too, something like that. Maybe that’ll happen with Cerebras too.

Austin: Yes, yes, yes, yes, exactly. There you go. Yeah, interesting. Okay, so yeah, let’s get into the OpenAI thing. NVIDIA has Groq and that allows for fast inference. OpenAI says, hey, fast inference, that’s awesome. We want that. They’re working with Cerebras. Have you looked much into the terms of the deal? And clearly this is the big customer that Cerebras is using to go IPO because previously when they tried to IPO, OpenAI wasn’t, they didn’t have the relationship with OpenAI. And so to be honest, it felt a lot sketchier where it was just like, you’ve got a big sovereign investor and also cloud buyer. And you’re trying to IPO on that. That didn’t really feel like an actual business validation that it was a sound business and you had product market fit. But with OpenAI, it’s a bit of a different story, but it’s still customer concentration. What’s your read on the OpenAI deal?

Vik: Yeah, so the one thing is that I like the Groq deal in a sense. I still think NVIDIA paid a lot of money for it. You can’t change my mind, okay? It’s overpaid, fine. Whatever, they got it. They have a lot of money, good. So the thing is that they have the hardware, they have the compiler team, they have the rest of their ecosystem, they have CUDA, they have their GPUs, they have their Rubins or whatever. And all the pieces are in place for all these things to work together and work nicely.

So when NVIDIA provides a low latency inference solution, I can actually kind of see how it works. The OpenAI deal is a little bit different because OpenAI is not really buying Cerebras hardware. They never said, give me a wafer-scale engine. I’m going to build a data center out of it or anything like that. They’re actually paying for compute time. They’re basically saying, I’ll pay you for tokens. And that’s completely different because now there are some terms of the deal, they get some warrants and I don’t know. I wrote a whole Substack post on this with all these things in it. So you can see it there. I don’t want to go into this number details, it’s too boring.

But basically the idea is that OpenAI is going to give Cerebras money for buying tokens from them and that’s about it. Cerebras is responsible for manufacturing, building data centers, running their cloud service, providing AI tokens, all of this stuff. And they are not actually selling any hardware. This token factory business is expected to grow, but I just feel like it’s a lot of trouble. Not only do you have to make this complicated chip and handle the supply chain around it, and now you’ve got to build out data centers, run your own, become a new cloud.

Austin: It’s a lot. Yeah, exactly. Interesting, fascinating. So presumably Cerebras has some sort of little cloud, because I remember Groq did this. They had their chips, but then the best way to show it off when the open models came out was to be like, wait, let’s actually build our own little cloud and have an API and just tell developers, go hit our API. You can see how fast it is. And I think that most other AI accelerator companies went and did the same. SambaNova maybe. And I assume that Cerebras did, but do you know, they must have some experience of running their own cloud at a very small scale.

Vik: They do have a cloud service, I believe. But in any case, it’s not something that you can run at scale. You’re talking about OpenAI kind of scale now, where people are going to use codecs and do coding jobs on this low latency inference. It’s a lot. And you’re going to have to provide that at scale. So that’s the only thing. Why do you have to also make all this complicated hardware and also act as a neocloud? There’s a lot of…

Austin: No, you make a great point, which is, look, if Azure, if Microsoft bought Cerebras, I’d say, okay, Microsoft knows how to run a cloud at scale. They know how to run OpenAI workloads at scale. They’ve worked together on all of that. They will know how to take Cerebras’ hardware, fit it into the Azure cloud, deal with SLAs, all that stuff. And then Cerebras can just focus on probably the hardest thing, which is, what’s the wafer-scale engine 5 that can support long context length, KV caching, world models, all this stuff. But to your point, it’s like, no, no, no. Now Cerebras needs to also be the Microsoft Azure-style partner for OpenAI. That sounds pretty challenging.

Vik: Yeah, that’s the thing. So let’s see how they do, I’m for it. I’m not anti anything. I’m just talking about some of the things that I find it’s really difficult to do and that they are really continuing to solve the unsolvable, I hope. So we’ll see.

Austin: Totally. Well, hey, they’ve got $5.5 billion to go hire some more people. How about that?

Vik: Yes. Let’s do that. Yeah, I’ve got the money now. Make it happen.

Austin: Let’s go. Okay, any last thoughts before we close?

Vik: No, I feel like this is only now starting to get interesting. There are so many people in the SRAM inference game right now. We’ve only seen the LPU now and we’ve seen the Cerebras, which I think it was expected that Cerebras was going to be next. A lot of people were talking about this. Then you have so many others. You have SambaNova, you have MatX that you spoke to, Reiner Pope, you have Taalas. You have other companies like Sohu, Tenstorrent.

Austin: Yeah, Etched, Etched, Tenstorrent. Fractile just raised $220 million yesterday. There’s a lot of people playing in the space, d-Matrix, you know? So I think, to be honest, I have always been bearish of the companies that designed their systems prior to LLMs, because of course they just didn’t know what trade-offs to make. So I was bearish Groq and Cerebras, bullish these post-LLM style companies.

But the nice thing is Groq and Cerebras lived long enough to be, in my opinion, at the right place at the right time and to say, we’ve got low latency options. They might not scale the greatest. We need to work on our roadmap to continue to iterate toward the demands that LLM inference places on us. But we’re here. And as you’ve said with CPUs, the best CPU is the one you can buy. The best AI accelerator is the one you can buy, which now you can kind of get, maybe you can buy TPUs, but before you couldn’t, so this was your only option. And of course, these are different architecturally than TPUs. But the MatX and the Etched and the Fractiles, you still can’t really buy them at scale yet. So this is the sweet spot in the moment in history and time for Groq and Cerebras.

But again, that just opens the question about, what happens when these other players come to market? Does it not matter at that point for Groq and Cerebras because now they have partnerships and customers and they’re already embedded? Or is it competitive pressure where suddenly the shortcomings where they have trouble scaling, maybe now all of a sudden, you were the only one that could do a thousand tokens per second, but now there’s 10 people who can do a thousand tokens per second and maybe they can support other things that you can’t.

Vik: Yeah, and we live in the wild west of the inference world. And looking back 10 years from now, we’ll talk about this moment and be like, do you remember that time when this company was doing this wafer-scale engine and there was a company called Groq who just decided they’re going to do everything deterministically with this very large instruction word? And then do you know that SambaNova was a company who was trying to put all SRAM, HBM, and DRAM all together because why choose? No two companies ever did it the same. And then there were companies were trying to etch it, literally hard-coded LLMs onto chips. Like what were we thinking? That’s what it seems like we’ll say in ten years.

Austin: Yeah, it’ll be interesting. It’ll be like, everyone splattered all the architecture spaghetti against the wall and a couple things stuck. It’ll be interesting. And where does the value accrue eventually? I talked to Gimlet recently and people can go listen to that. And they’re talking about being able to abstract across all these different silicon vendors and take your workload and disaggregate across all of them. So it would be very interesting to see in the long run, is it like, no, no, you’re best when you just play in the NVIDIA environment. And even if they have a portfolio with different SKUs, it’s vertically integrated and that gets you the best efficiency. Or do things become unbundled and software layers come in that can orchestrate and optimize across different hardware that might make different TCO trade-offs because, look, maybe for some parts of the workload, maybe you don’t actually need really expensive HBM4.

So yes, guys, we’re on a fun ride and we’re here to bring it to you every week as it unfolds. So thank you for listening. If you’re enjoying Semi Doped, share it with your friends. Word of mouth means a ton to us. Subscribe to our newsletters. We just started SemiDoped.com, which is the companion daily. I think of it as the morning brew for semis that accompanies this podcast. You can get that in your inbox Monday through Friday. We just look at the news, we give little takes. We think it’s worth you reading while you drink coffee. And last but not least, keep commenting on our YouTubes and send us emails and everything. So with that, thank you and we’ll see you next time.
