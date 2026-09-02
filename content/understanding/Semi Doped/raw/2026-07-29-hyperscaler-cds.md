---
source: https://daily.semidoped.com/p/semi-doped-3-stories-behind-the-semi
title: 🎙️ Semi Doped: News Take: Hyperscaler CDS, SK Hynix Earnings, China's DUV
kind: transcript
---

🎙️ Semi Doped: News Take: Hyperscaler CDS, SK Hynix Earnings, China's DUV

A timely 18-minute, engineering-first update for you on the recent market volatility.

Austin and Vik break down a crazy week in the semiconductor market. They discuss the rising concern over hyperscaler debt as reflected in credit default swaps, the market panic following SK Hynix’s earnings despite massive growth, and what China’s reported breakthrough in DUV lithography actually means for the industry.

Things we cover:
* Credit default swaps and hyperscaler debt
* Gavin Baker’s counter-take on GPU profitability
* SK Hynix’s earnings and the subsequent market reaction
* The HBM vs. DRAM profitability dynamic
* China’s announcement of a domestic immersion DUV tool
* The long road to EUV lithography

This podcast is lightly edited for clarity.

Credit Default Swaps

Austin: So some major things have happened in the market this week. I think we should talk about it. Have you kept a tab on what’s going on?

Vik: Everything’s going on. The sky is falling and overnight—and it doesn’t stop either because overnight in Korea things freak out and so then it’s just constant news.

Austin: Yeah, it’s insane. Okay, what’s the first thing you’ve heard?

Vik: Okay, let’s talk credit default swaps. This is interesting and this was related. I think Gavin Baker had a good take as well where he was kind of downplaying it a little bit. But the topic here is the idea that right now there are a lot of all the hyperscalers—traditionally, yes, OpenAI and Anthropic are the ones using all the compute, but it’s the hyperscalers providing the compute and the hyperscalers are the ones that have to go buy billions and billions and billions of dollars of racks from Nvidia, basically.

Historically, they’ve been funding this out of cash flow, out of their free cash flow. But as the quarterly CAPEX investments get bigger and bigger and bigger, it’s getting to the point where these hyperscalers are starting to exhaust all of their free cash flow and they’re starting to do things like take on debt or do these off-balance sheet special vehicle things. Like Meta had something with some company. I think it was called Blue Owl or something.

Anyway, so now all of a sudden the debt market at first, debt investors were like, cool, we like hyperscalers. We feel good about taking on their debt. But there’s been such an influx and projected influx of these hyperscalers coming to the debt markets to take on debt to fund this that debt investors are starting to get a little cautious and you see this showing up in this thing called the credit default swap, which is essentially like you could think of it as insurance.

If you think that the debt has a chance of ever not being repaid, you’ve got this credit default swap thing and if as there’s a higher premium on that, it sort of suggests that debt investors are getting more and more nervous. And so it’s more expensive to basically finance this. And so that’s the first thing that people are starting to freak out a little bit about of saying like, whoa, there’s a lot of debt. Maybe everyone’s a little unsure that this is actually going to get paid.

Austin: Yeah, credit default swaps if folks aren’t familiar with it. I’m no finance person, so I had to kind of look it up to make sure that I understand it right. So it’s basically a form of insurance on a company’s debt. So if you see a company is taking on way too much debt, what investors do is they pay a premium. It’s like getting insurance for yourself, right? Like, hey, you’re going to fall sick maybe, so you get insurance so that you can pay for it when it happens.

The same thing with investing, when investors are investing in a company and they see that the company is taking on too much risk, they feel like the company is eating too many burgers or unhealthy foods and they’re probably going to get sick. And they’re like, okay, I’m going to get this insurance so that when the company defaults and doesn’t pay back its debts, I get some money back. So that’s those are credit default swaps. And what’s happening, like you were saying, is a lot of credit default swaps are trading at a higher premium. The spread has gotten higher. And so everybody’s nervous about this circular financing that Nvidia is paying money to people like hyperscalers and Neoclouds or whatever to to buy their product, right? To buy Nvidia chips. And so these kinds of circular deals in AI have been around now at least for a year and we’ve spoken about them. It’s making a lot of investors nervous. So this is, I think, one of the worries and fears fueling the sell-off this week.

The Counter-Take on Debt

Vik: Yes, and so I thought Gavin Baker did put a nice take kind of pushing back on this on X where he basically said, hey, here’s some things that aren’t being considered. Yes, the free cash flow of these hyperscalers is headed toward zero, which suggests there’ll be more debt and then you’ve got the circular financing thing where everyone’s just starting to get concerned. He said, but here’s two interesting data points.

One, the spot price for GPU rentals is much higher than these contracted rates. For example, he said at times it’s even 2X higher. And therefore, he thinks hyperscalers are actually under-earning for the GPUs that they’ve rented out because they rent out these GPUs a lot of times on three-year contracts, long-term contracts. So as those contracts begin to roll over, they will be able to charge a lot more. So, just because you’re only getting $3 an hour per GPU, let’s say, as those start to roll over, maybe they’re going to renew them for $5 or $6 an hour or whatever. I’m just making up the numbers here, but you get the point.

And then secondly, he said, historically, the big consumers of that compute is ultimately Anthropic and OpenAI. Early on, it was all for training. Obviously, now we’re into the era where they’re using a lot of the compute for inference and this inference has very high margins and especially now that both companies have figured out. This is really good for OpenAI. Anthropic came first and figured out like, hey, there’s a ton of money to be made from enterprises and from coding, in Fable and charging API token costs. And OpenAI, which had been just focused on consumers who will not pay anything or maybe they’ll pay $20 a month with Codex, they’re catching up. They’re chasing after these customers too and realizing like, okay, we can make a ton of money on inference. We have very high margins.

And so Gavin was saying like, don’t forget, these end customers are now incredibly profitable. Well, they’re making more than the market probably appreciates and therefore they will be good buyers and will have their own free cash flow to be able to invest in paying for more of this GPUs. So, a little bit concerned of like the end users used to not be able to afford this and that’s why Nvidia and whoever had to come in and backstop it. But now actually there’s ROI on the investments.

Austin: Yeah, that’s an interesting take. Let’s see how it pans out.

SK Hynix Carnage

Austin: Next, SK Hynix. This week in SK Hynix land, they made a lot of money. And I have it in my notes here. They have 257% year-over-year revenue and more than a six-fold jump in operating profit too, I believe. And then there’s like a 76% operating margin. All great, right? It’s amazing. But it apparently came in below consensus.

So everybody believed that the outputs would be in terms of revenue would be even higher and they came in a bit short. So everybody freaked out and it went terribly bad for SK Hynix investors and the Seoul-listed shares dropped by 20%, which is one of the worst single-day stock falls on record. It dragged down all Korean stocks. It dropped the Kospi index. And so yeah, they had to limit this kind of leverage trading only to institutional investors and not retail investors. So it’s just carnage, right? The memory market all of a sudden is carnage. Which is to me a little bit like, I don’t know why, but I feel like it’s an overreaction. Fundamentally, do you think the memory requirement has changed from a technical point of view?

Vik: No, no. Fundamentally, there’s so much need for HBM, there’s so much need for DRAM from CPUs to GPUs, right? Bigger models, more context length, none of this is going away. It’s truly useful. Agentic AI, of course, is now you’ve got tens of agents and they’re just spinning up all the things, doing all the things. This is not going away. Fundamentally, nothing has changed.

The Memory Hierarchy

Austin: Yeah, so that’s the whole point. It’s interesting you mentioned HBM because DRAM is making more money for these companies than HBM because the bit output of HBM is three times worse. You need three wafers of DRAM to make the equivalent number of bits in HBM. So it takes up more wafer supply and the spot pricing of DRAM has gone insane. And a lot of companies who are just selling DRAM and not HBM have ended up making a lot more money.

And so this is this is the whole thing, right? Selling DRAM is profitable, but HBM isn’t. But then the demand for HBM isn’t going away anytime soon because literally there is no alternative to provide the kind of performance as a memory tier. There are alternatives that people are looking at. We’ve been always hear about offloading to KV cache storage and doing different techniques like TurboQuant or Kimi’s Delta attention, you have these algorithmic approaches. But all of them fundamentally rely on HBM to give you the tokens per second throughput because SRAM isn’t just enough capacity. So it’s sitting in that sweet spot, that sweet tier and it’s very hard to dislodge HBM. Now all of a sudden because you’ve fell short a few billions or whatever, everything is wrecked.

Vik: Yes, yes. So to your point, there’s the memory hierarchy, of course. SRAM is the fastest, but it’s transistors, it takes up a lot of area, it’s very expensive. HBM is that nice tier right beneath it where it is DRAM, but it’s 3D stacked DRAM and it’s super close to the chip and it gives you that bandwidth you need. Definitely the sweet spot. That’s not going away. You can argue that that is less of a commodity too going forward because we’ll have these custom base dies. DRAM underneath, lots of capacity, less bandwidth, less of a commodity. And so historically, that’s not where the value capture has been, but because to your point of the whole we can only make so many DRAM wafers and when we stack them for HBM, it’s less bit efficient. Then at the same time CPUs and agentic AI making just LPDDR, DDR or whatever, even more in demand. It’s this weird imbalance where normal DRAM’s capturing all the value, but you can argue that in the long run, HBM in that sweet spot will still capture more value.

But I guess last thing I’ll say on this is, we’ve got levered investors, you’ve got Korean investors. I mean, think about it. And you know this well because you’re in India, like in the United States, I can invest in all these companies. I can invest in Micron. SK Hynix is new via the ADR, but if you’re in other countries, maybe locally, you just invest in the local industry. If you’re in Taiwan, maybe you invest in TSMC. If you’re in Korea, maybe you invest in SK Hynix. So I think a lot of people, of course, and of course, because memory has gone to the moon, you’ve got a lot of retail traders, everyone’s in. Some people are highly levered, you’ve got funds in. So I think that you miss your mark a tiny bit, people start to freak out. Of course, there’s other things and macro things going on too that are causing people to freak out. And especially if you’re levered, a little miss, a little change in the stock and suddenly, you were up 500% and now all of a sudden you’re only up 300% and you’re like, I should just sell and get out and take what I can. So I do think there’s a lot of deleveraging and a lot of selling going on, not based on the fundamentals, more based on fear and volatility.

Austin: Yes, true, true. Everybody’s looking for the memory top and we kind of expected this. The first earnings call where somebody says, oh yeah, I’m short. That’s going to be the trigger for the panic, right? We kind of expected this, but now it’s happening out in real time really.

Vik: Yeah. And of course, I can’t say memory without saying consumers. So there’s pressures there too, which I think are freaking people out. So, but we’ll carry on.

China’s DUV Breakthrough

Austin: Yeah, that’s true. The next thing we should probably look at is Chinese announcement of immersion DUV. What do you think? You think they’ve broken through the lithography industry now and can make chips? What’s your take?

Vik: Yeah, I thought you had a good take there, which was like, hey, this is like ASML’s tool circa 2008 or 2003 or something. And I think it was a good reminder because just like with any startup, if someone in a lab says, hey, I built this thing, it doesn’t mean they’re taking down a company instantly. It doesn’t even mean that it’s necessarily competitive with where the frontier is for any given company. And so, yes, of course, China’s going to work on DUV and of course, they’re going to try to work toward EUV, but just because they can ship something that works doesn’t just mean that ASML is dead and the monopoly is over and so on and so forth. But yeah, take us into the technology a little bit.

Austin: Yeah, so we did a deep dive on this podcast about lithography. So if anybody’s wondering what’s immersion versus not immersion DUV, we have a nice full podcast with pictures about this stuff. But essentially, immersion DUV was what was used in the early 2010s to make a whole lot of chips below the 45 nanometer node. I think it could pattern 28 nanometer node in a single shot. Now, if you want to go to 7 nanometers, we have to do multi-patterning, which is another topic we’ve discussed on the lithography episode. So check that out. But essentially what you can do is you can only get to 7 nanometers, okay? You can’t go to 2 nanometers and that doesn’t automatically mean that China has advanced or whatever. So take everything with a grain of salt.

It’s a good milestone if it’s true. I mean, if this thing actually works, I’d like to see chips coming out of it. So I’m taking everything with a lot of hesitation about what has already been done, where their capabilities are, because none of this is really public and a lot of it is just announcements without any proof. So I’m always skeptical. But when you can make a 7 nanometer node, they have to do their logic folding and stacking in 3D chips to make anything useful out of this node to be competitive in today’s markets and technologies. And we’ve spoken about logic folding as well in another episode where Huawei is planning to take 7 nanometer technologies and put them vertically on top of each other so that you can get more transistors per unit area, right? It’s like instead of building suburban homes, you want to build basically apartment complexes on wafer so you can get more people or aka more transistors in a given footprint of urban space, which has now become very, very, very expensive as advanced nodes have gone into the EUV land, right?

So yeah, this is if it’s true, it’s a good advancement to make in-house lithography of reasonably advanced nodes. And some people on X had the belief that EUV is just three years away, which I disagree with because EUV is a substantially different problem and an extremely difficult one because you have to blast those tin droplets twice to generate 13.5 nanometer extreme ultraviolet light. That’s very difficult. It took ASML 20 years or so to engineer it without all of these supply chain restrictions, okay? So I don’t think EUV is going to just come out of it. There are options that like free electron lasers that like X-ray is doing, right? Maybe there are other technologies that could work. I’m not really sure. Maybe they’ll figure out X-ray lithography before Substrate does, which is another company in the Bay Area. So there are options that may come out of this, but I don’t think EUV is around the corner, right? So that’s my whole take on this thing.

The Long Road to EUV

Vik: Yeah, I hear you. If you’re rooting for China to have DUV here for our East Asian listeners, I think it’s probably the best sign here is the way like what a long journey starts with one step, right? And so if you want to make progress, you make progress toward DUV and then figure out how to ramp that and produce it at scale and see that it’s working and improve on it and that will continue to help you take steps. Yes, DUV doesn’t necessarily directly lead to EUV because it’s a different technology and there’s ways to leapfrog with free electron lasers or X-ray lithography like you said. But I think they can celebrate, hey, this is DUV. I think it said they’re trying to ship five machines this year and 20 in 2027. And so it is definitely a step in the right direction towards self-sufficiency, but it is a far cry from being at the leading edge and necessarily being competitive.

Austin: Yeah, overall, it’s been a hard week for semiconductor investors and with the recent run-up, there are a lot of people who haven’t seen the cyclicality of this industry before and is probably their first taste of it. Memory investors for a long time, for example, have seen these things happen over and over again. But long term, at least I believe that there is a lot of potential in the technology side. The technology works. What we needed last week, we still need all those things. We still need indium phosphide, we need lasers, we need better computers, we need more memory. Nothing has changed. So it’s not investment advice, but if you’re suffering in the market, things will get better. So that’s my closing line really.

Vik: There you go. Hang in there, people. All right, thanks.

Discussion about this video
