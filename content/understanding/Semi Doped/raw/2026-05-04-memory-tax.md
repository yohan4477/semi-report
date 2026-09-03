---
source: https://daily.semidoped.com/p/capex-is-just-memory-tax-now-deepseek
title: 🎧 CapEx is just Memory Tax Now, Deepseek V4 NAND impact
kind: transcript
---

🎧 CapEx is just Memory Tax Now, Deepseek V4 NAND impact

HBM4? Sold out. SanDisk margins? 78%. On-prem? Pulled to the cloud. Plus the SunDisk origin story.

The big four hyperscalers committed nearly $700B of 2026 capex, but the new wrinkle is that a chunk of the raise isn’t buying more compute — it’s just paying higher memory and storage prices. SanDisk gross margins? 78%. Samsung HBM4? Sold out. DeepSeek v4? SSD-centric inference. Vik and Austin walk through who’s winning, who’s paying, and whether this whole loop has any ROI.

Things we cover:

The memory tax: hyperscaler capex rising on component prices, not flops

The memory tax: hyperscaler capex rising on component prices, not flops

Samsung HBM4 and the unwritten Gbps-per-pin race beyond the JEDEC spec

Samsung HBM4 and the unwritten Gbps-per-pin race beyond the JEDEC spec

SanDisk’s 78% gross margins and the new multi-year supply lock-ins

SanDisk’s 78% gross margins and the new multi-year supply lock-ins

DeepSeek v4 and the move to SSD-centric inference

DeepSeek v4 and the move to SSD-centric inference

Jassy’s counterintuitive take: memory shortages are pushing on-prem to the cloud

Jassy’s counterintuitive take: memory shortages are pushing on-prem to the cloud

Qualcomm’s mystery custom ASIC, plus the SunDisk → SanDisk origin story

Qualcomm’s mystery custom ASIC, plus the SunDisk → SanDisk origin story

This podcast is lightly edited for clarity.

Vik Goes Full-Time

Austin: Hello everyone and welcome to another Semi Doped Podcast. I’m Austin Lyons with Chipstrat and with me is Vik Sekar from Vik’s Newsletter. Hey Vik, a lot has changed since the last time we recorded a podcast. What’s up with you?

Vik: Yeah, a lot has changed. So after 15 years of working in the semiconductor industry across small, medium, and large companies, I finally decided to hang up that corporate hat and do the Substack, this podcast, full time. And see where it takes us, in the podcast front. And I hope the Substack continues to grow too, because it is so much fun that I figured, okay, let’s give this a shot.

I learned so much from writing and reading about so many different things. Corporate roles tend to be a little bit more hyper-focused. And I’ve spent 15 years doing kind of the same thing. So I was like, okay, instead of trying to change roles everywhere, I’ve kind of managed to carve out this role for myself. So I said, let’s try it for a while. What’s the worst that can happen? Let’s try it.

Austin: Awesome, I love it. Yeah, okay, so you’ll have more time, presumably, for writing, podcasting, researching. What are you most excited about?

Vik: Yeah, I’m just going to do the same thing. I’m not trying to add too many things because I think we already added one other thing to the Semi Doped umbrella, which we haven’t really spoken about, which is Semi Doped also has a Substack presence now, and it is a free-for-all subscription. It does not have paywalls. And what Austin and I do here is we just give our daily takes. So this is a once-daily newsletter that’s short to read, like within three to five minutes, just with some key highlights of what’s happening in the day. Because we monitor this stuff so much every day now that we figured, okay, so much goes unmentioned because we can’t write everything in the newsletter and we can’t talk about everything on a limited time podcast.

Not everything requires a full deep dive Substack or a full hour podcast. But if we try to stick it in the podcast, it gets fragmented. So the best place for this kind of information, but that’s also very relevant. The reason you sign up for the Semi Doped Substack is that you’ll get one email a day. You open it up while you have your coffee, you glance through it. Anything that piques your interest, you read that section or not. You’ll get another email the next day and it’s an easy read. It’s unlike our deep dives on Substack, which are highly researched and thought through. These are just quick hits. So that is the second project that’s common to us apart from the Substack.

Austin: Yeah, I’m excited about it. I’m looking forward to it. It’s been fun this week. For listeners, definitely go sign up. It’s basically Vik and I having a quick water-cooler conversation that you’re part of. Hey, here’s this news from yesterday. Vik will give a take, I’ll give a quick take, move on to the next thing. I think it’ll be fun, informative, and you’ll just be more intelligent about semiconductors and AI for reading it.

Vik: Yeah, just semidoped.com should get you there. Or you can search for it on Substack, semidoped. You’ll see the same logo of this podcast, and you’ll find it there. And the last thing that is forming still in my life is the fact that now I am available to do consulting. And my newsletter itself actually runs under the umbrella of Semiexponent, which I came up as a name to say, this is the most exponential technology that ever existed. So I was like, okay, Semiexponent is a nice — what is the exponent? The exponent is zero means it’s a flat line, but it’s never zero. So anything above zero is like an exponent. So I’m like, okay, that’s a nice name. So the consulting arm is going to be under Semiexponent. So now I’m just starting to find clients who want to work with me on various different aspects of semiconductors, have chats, pick my brain on various aspects of what I write and talk about. We’ll see how that goes. It should be fun. I like talking to people anyway.

Austin: Yeah, nice. So you’ll be researching, writing, talking, and consulting. That does sound like plenty.

Vik: Yeah, that’s enough. That’s why I’m not doing anything to the Substack. Things will continue as it is. And I hope there’ll be more research involved because I have more time to think through carefully a lot more stuff. But I’ve always tried to maintain a high level of quality on the Substack. So hopefully if I’ve been doing my job well enough, you won’t notice any changes.

Austin: There you go, love it.

Earnings Week: The Memory Tax Quarter

Austin: All right, let’s get into it. So this past week, you were on vacation, there was earnings week, they didn’t wait for you. But I stayed on top of it and I know you’ve caught up a lot on it. So of course, listeners, I know you know all about this. Microsoft, Google, Meta, Amazon, Samsung, SanDisk, Seagate, Western Digital, Qualcomm, Cadence, NXP, even Rivian, which I love to follow, even though they’re kind of downstream as a semiconductor consumer. All those companies reported. Impossible to listen to all of it. But we are going to cover it.

And I thought the angle that we could take is actually starting with memory and storage companies. And here’s why. As everyone’s been tracking, the big four hyperscalers have now committed to nearly $700 billion of 2026 capex, which is up from roughly $500 billion just in 2025. So every quarter, the story is always: hey, did they keep capex or did they raise it even more? And the reason for raising capex has always just been we need more compute, we need more flops, we need more intelligence.

This quarter there was something different, which was: yes, we’re raising capex, but it’s because of needing extra dollars allocated specifically to cover rising component costs. Memory is more expensive, storage is more expensive, even things like fiber and optics are more expensive. So I thought that was an interesting shift of: yeah, we are increasing capex, but it’s just to pay — not to buy more flops, but just to pay for the things that we are committed to. So I thought it’d be fun to start with the beneficiaries of this capex raise, which would be the memory and storage companies that reported. So we’re going to start there. How does that sound?

Vik: Yeah, let’s do it. Memory and storage is something I keep ranting on on the podcast. How much more expensive is it going to get? How much more are they going to raise prices? Everybody is now getting like — I don’t know what is it called, like price hike infatuation. Or in other words, what I wanted to say was they expect a price hike every time, but if the price hike isn’t good enough now, they’re like, wait, you’re only doubling it? Why not? Why is it not five times? What is that?

Austin: Yes, investors, totally. Man, aren’t you happy that prices are going up? Not going up enough. Yep, your stock goes down. It is crazy.

Samsung HBM4 and the Memory Tax Debate

Austin: All right, let’s start with Samsung, or Samsung Electronics. The number that stuck out to me was that their memory revenue was up 101% year over year, which obviously is pretty crazy for memory. They said as a company, their Q1 revenue and operating profit were at all-time highs. HBM sales are expected to triple year over year in 2026. And they expect HBM4 to be 50%-plus of HBM sales by Q3. So there’s a mix shift going from HBM3E to four.

Now for people who haven’t followed Samsung as closely. In the HBM market, the story over the past couple years was — there’s basically three big players, SK Hynix, Samsung, and Micron. And Samsung used to be up there with SK Hynix, having a lot of market share on the order of, even just about this time last year — or actually maybe like six quarters ago — there was like 40% market share for Samsung. And in 2025, it dropped drastically down to like 13%, 15%, 20%. So the story of Samsung is they’ve fallen behind and now they’re trying to catch back up. Now, of course, there’s always a new technology — HBM3, HBM3E, HBM4. And when a new standard comes out, there’s an opportunity to try to be first to it and regain some market share.

So Samsung on their call, they were really trying to position that, sure, the past is behind us, but we’re totally ready for HBM4. So I thought I’d read a couple of quotes quick and then we can get into it. They wanted to make sure to say that they are the first and they are the best around HBM4. So the quotes from the call, J.June Kim, EVP of Memory Sales said, “after we became the world’s first to commence commercial shipment of HBM4 in February.” So right there, like saying in passing, don’t forget we were the world’s first shipping HBM4. And then he said, “the differentiated performance of our HBM4 led to concentration of demand and our production-ready capacity is fully booked and sold out. Our outstanding performance has been translating into actual premium on pricing.”

So the read-through there is there’s always been a question around memory, around storage, which is, is it just a commodity? A bit’s a bit’s a bit, doesn’t matter who it’s from. And here Samsung was trying to say, hey, not only are we first, but our performance is the best. And that’s why — and we’ve gotten the capacity ready — that’s why we’re sold out. Customers prefer us. That’s why we’re able to have a premium on pricing. Any reaction to that, Vik?

Vik: I remember this, there was this whole discussion about how many gigabits per second you can get out of HBM memory by designing the base die for HBM4 to be on a certain node. Or even if it doesn’t matter what node it is, because there was some discussion that Micron was using a memory technology to make the base die while the other competitors like Samsung and SK Hynix were actually using a true logic node.

The point is that the speed becomes a differentiating factor. So it’s no more memory just memory. How it performs has become a very important factor for which company Nvidia or AMD will pick for their performance. And not only that, it comes the other way too. The JEDEC spec for HBM4 is like, I think, eight gigabits per second per lane. But then because they want supremacy on inference performance and tokens output and tokens per watt per dollar and all that, they are pushing the speed per lane of HBM4 faster and faster and faster. So it’s become a competition as to who can get to like 10 or 11 or 12 Gbps per pin. And that is way beyond the spec, but it has become the thing that drives sales and drives lock-in.

Because once these hyperscalers choose and qualify a HBM vendor, it is a sticky decision. Qualification — if you remember, with HBM3, Samsung couldn’t really get qualified at Nvidia for a long time. They had so many yield issues and things like that. Qualification and performance makes this very sticky. So it’s not fungible. You just can’t take out Samsung and drop in Micron tomorrow, although there are only three companies doing this.

Austin: Yes, so zooming out and hitting on what you said again for listeners, the real interesting thing is there is a spec — this JEDEC spec, J-E-D-E-C — that defines the performance level and the various other things that a spec defines, about how it’s supposed to work, how it’s supposed to communicate, that these three companies are trying to hit. And normally, if everyone just hits that spec exactly, it would be fungible. But what Vik is saying is that Nvidia said, hey, wait a minute, I’ve got to compete against AMD and against XPUs. And if you could give me HBM memory that’s even faster, then I can get even better tokens per second, tokens per watt, that kind of thing.

So actually there is a pull from the silicon vendors to the memory manufacturers to say, I know the spec says eight gigabits per second per pin or whatever, can you go higher? And so then there’s this interesting dynamic where someone’s trying to get to 11 and now the others have to try to get to 11 as well. There’s this interesting pull to go faster. And now this kind of unwritten spec, this performance, that they’re all trying to compete on. So as you move away from “everyone meets the spec, we’re all fungible” to “how fast can you go at what yield, at what cost,” it is more of a true competition on the things that do allow you to have premium pricing over commodity pricing, which is performance and yield and cost and that kind of thing. So that’s a little bit of the back story here for HBM4 and how Samsung is trying to regain market share — to truly compete on performance.

Austin: Okay, one more quote from Samsung’s EVP of memory sales. He said, “our demand fulfillment rate is now at a record low. Customers who are concerned about supply shortages are actually bringing forward their demand for 2027 already.” So not surprising, but again, it’s just crazy to hear. If customers are asking for this much, maybe it used to be like, we can only give you 80% of that, or 50%, maybe now it’s even lower than that. I’m making up the numbers, but trying to illustrate the point that customers are asking for a lot of memory and the memory suppliers are saying, I can give you less than ever. So that would be the environment that we’re in.

Vik: Yeah, that’s crazy to me. How much longer is this going to continue? Because these hyperscalers are increasing the capex just to pay these memory companies. Literally, that’s what their capex is going into, just to pay these players for HBM and NAND memory and things like this. I’m not sure how much higher it’s going to keep going. I keep thinking that that’s it, but I’m always wrong.

Austin: Well, that’s an interesting point. We can get into it more, both here and later, which is — I am very bullish on capex continuing to get higher when it’s buying more flops, when it’s buying more compute. Because I, like everyone else, believe that the more compute we have, the more intelligence we have, the more we can do. I too have experienced, I’m sure everyone has, ChatGPT or Gemini or Claude Code just spinning or saying like, I’m busy right now, or come back, we’ve reached our limits. So that’s frustrating and that just shows that, dude, they need more GPUs, they need more XPUs.

But this is a different conversation when it’s, how high can you convince your CFO to let capex go when you’re not buying any additional compute, but you’re just paying increased memory prices? Is that going to be the straw that breaks the camel’s back?

Vik: Exactly. Because if all of this money went into expanding compute, then a lot more users of AI tools or whatever get actually something out of it. They get better tools, they use it to build better projects, that drives revenue, that drives an economy. It completes the circle in some way. What is happening now is if all the capex is going to memory players, it’s like you’re siphoning all this money out into somebody’s pocket. It’s not going into the positive reinforcement loop we want to see. So this is a bit concerning for me.

Austin: Yes, you’re totally right. Put succinctly, there’s no ROI on that additional capex.

Vik: Except for a few companies.

Austin: Yes — for the hyperscalers, there’s no extra ROI, no return on invested capital. It’s just a tax. It’s a memory tax.

Vik: It’s a tax, yes, a memory tax.

SanDisk and the SunDisk Origin Story

Austin: Okay, let’s move on to SanDisk. So when we talked Samsung, we were focused on HBM, focused on memory. So let’s talk other memory and storage. We’re going to talk SanDisk, but really quick, I thought I’d give a quick history sidebar because we haven’t talked about SanDisk on the podcast yet. So SanDisk and Western Digital, really quick. They were two companies. Back in 2016, Western Digital actually acquired SanDisk for around $20 billion. And the thesis I think back then was having a full storage portfolio. Can we own both hard disk drives and NAND flash, and therefore we can sell hyperscalers a complete stack? Makes a ton of sense right now in the era we’re in, but prior to AI, that thesis didn’t really age well.

I think they’re very different businesses. They have different cycle dynamics, capital intensity, customer mix. So running them under one roof wasn’t as simple as, great, we share customers and now we can more easily cross-sell into them. It was actually sort of like, oh, these are two different businesses and there’s some different customers at play and we’re not getting the quote-unquote synergies that we thought we would. So back in October of 2023, Western Digital announced that they were going to split SanDisk back out. And by February 2025, that spin-out happened, SanDisk re-emerged as a standalone publicly traded company.

So now when you think about SanDisk, you can think about NAND flash, SSDs, embedded flash. They have a joint venture on some fabs in Japan with Kioxia — Kioxia, not sure how to pronounce that. So SanDisk, you can think of flash, SSDs, et cetera. And then Western Digital is hard disk drives only. They are working — we were doing a little bit of research — Western Digital is working on this interesting next generation HAMR, “Hammer,” which stands for Heat Assisted Magnetic Recording. I’d never heard of it, but the goal is to achieve 100-terabyte-plus hard disk drive capacities for AI scale data. And they’re planning volume production in 2027. Have you heard of this?

Vik: Yes, so HAMR has been there for a while, actually. It’s not that new. HAMR has been cited, advanced — I’ve heard this at least for like five years now. I can’t pinpoint exactly how long it’s been around. So it’s always been the next greatest thing in hard disk drive technology. But then what has happened recently is that if you look at quad-level cell SSDs, QLC SSDs — the SanDisk ones, for example, the highest capacity one is 256 terabytes. And you get it in an SSD form factor already. So I’m like, what is this HAMR and it’s going to give you what, 100 tera? It’s not that great, honestly, in today’s day and age. Of course, the price point will be lower. It should be. But HAMR — it’s been around, I don’t know how relevant it is or where we are on that right now.

But I wanted to go back in the history a little bit more. I think you’ll find this fun. Does the name Sanjay Mehrotra ring a bell to you?

Austin: Interesting. Oh yes, Micron?

Vik: Yes, Micron, Micron. Do you know who founded SanDisk? Sanjay Mehrotra.

Austin: Seriously? What?

Vik: Yes, it’s true. He was one of the founding members of SanDisk. This was way before he became the CEO of Micron, only in 2017. He was the original founder of SanDisk. So he’s a real memory guy. And another fun bit of trivia on the name — one of the other founders, Eli Harari — yeah, he’s one of the other co-founders. So they were trying to find a name for the company. And then his daughter comes in and looks at some of the disks lying there, these platters or something. And they’re like, yeah, that looks like the sun. So they decided to call it SunDisk.

Austin: No way.

Vik: You can look up early logos of SunDisk and you’ll see like a plate-like thing with the sun’s rays coming out of it. That’s their logo. We could put a picture if we find one. Yeah, that would be cool.

Austin: Yes, we should. Totally. Great trivia.

Vik: And what happens is that later, Sun Microsystems came after them for some trademark stuff, like, oh, well, you can’t use Sun in it or something. So they changed Sun to San and that’s what it came about.

Austin: Funny thing. Yeah, I was wondering. I was like, “Sun” — how did it make it “San”?

Vik: Yeah, that changed only like seven years after the company was even founded. Seven years after the company was fully functional, they changed the name to SanDisk thanks to Sun Microsystems.

Austin: Nice. Well, we should talk to Sanjay sometime and ask him if the “San” came from his name too.

Vik: Why not? Yeah, it could be.

Austin: Yeah, we should seriously see if he would talk to us about the history. That’s so fascinating that he was a co-founder of SanDisk and now he’s CEO of Micron. Super interesting.

Vik: Yes, yes, they’ll mention that as part of the history lesson here.

Austin: Oh man, good history lesson. Okay, so SanDisk, they reported earnings. Their CEO is not Sanjay. It is someone named David Goeckeler, I believe, SanDisk CEO. So this quarter, they had revenue of almost $6 billion. They were up 97%, the revenue was up 97% sequentially. So that’s just quarter over quarter. And of course, how do you do that? You raise prices. They’re up 251% year over year. Here’s a couple things that stood out. It is pretty crazy. Gross margin, 78.4%. That’s like gross margins of a software company.

Vik: What? Yeah, I have my notes here that it was 51.1% the prior quarter. And the revenue estimate was supposed to come in like, I don’t know, $4.8 billion or something. They come in a billion above that. I’m like, what? They are up 250% year over year in revenue. And the funny thing is that they haven’t shipped that many extra bits. This is all pricing. It’s not as much you think — like, oh, they sold maybe that much more to account for like a 97% quarter-over-quarter increase. No, no, no, not really. You can’t bring on that much capacity that quickly. I mean, you’re talking about making wafers and stuff in a fab and that stuff doesn’t move in the time frame of a quarter. This is all price increases.

Austin: Totally. Wow, so you said their margins were 51% last quarter, now they’re up to in the 70s.

Vik: And I think they projected above 80 next quarter. The guidance is above 80 next quarter.

Austin: Nuts. They’re going to make Nvidia look like they have work to do.

Vik: Nvidia is only like 75, right?

Austin: Yeah, right, totally. Of course, Nvidia is a very, very large company and has had these margins for quarter after quarter after quarter. So the question is, why is SanDisk crushing it? And the story that I heard on the earnings call was that they really believe that the NAND market is transitioning from commodity spot business to something less cyclical.

So the points that they made on the call — and I’ll read some quotes here too. They have five multi-year supply partnerships signed. These three new ones in Q3 — they announced two previously and they had announced three more. And those three new ones account for $42 billion of RPO, remaining performance obligations. You can kind of think of it like a backlog. And this was the first time they’ve actually disclosed that. So clearly there’s long-term agreements for many years and people are signing up. And these customer commitments already cover one third of the fiscal year 27 bits. So it’s not just people signing up for 2026, but they’re already signing up and paying for and committing to 2027 bits, which actually have financial guarantees backing them. So people are putting their money where their mouth is.

And the longest contract — yeah, the CEO, Goeckeler, said he wanted to drive those long-term commitments to above 50% of bits. And already one of the longest contracts was for five years. So the quote that I thought was pretty telling on how SanDisk is perceiving this, from the CEO: “Last quarter, we were engaged in discussions with customers on multi-year supply partnerships, what we refer to as new business models, or NBMs. I am pleased to share that we have successfully advanced those conversations with five multi-year partnerships signed so far. They are structured to lock in committed supply for our customers and committed financials for SanDisk.” So the customers are prepaying almost. “Our customers’ commitments are backed by firm financial guarantees. These partnerships support durable, structurally higher earnings in a significantly more predictable and less cyclical business for SanDisk. We believe this marks a fundamental evolution of our business, which is centered on deeper customer alignment, enhanced visibility, and long-term value creation.”

So, so far in this quote, he said, we’re signing people up for the long run and they’re paying for it. There hasn’t yet, in my opinion, been an argument for why it’s not cyclical. It could just be demand is crazy and people are signing up. As we talked about earlier with Samsung, when you’re a commodity, when you’re not a commodity — you’re actually competing on performance, for example. And he hasn’t talked about that yet.

But then later there was a quote that started to get into this, which I thought was interesting. He said, “as AI models scale from billions to trillions of parameters and deployments advance from simple inference to deep reasoning and increasingly agentic systems, NAND has become a critical component of the underlying infrastructure. Inference optimizations such as KVcache, along with workloads like RAG, require substantial high performance, low latency flash to deliver real time responsiveness and quality of user experience.” And then he goes on to say basically NAND flash is emerging as the only economically viable solution to deliver that capacity, performance and efficiency. And then he goes on to make the argument that SanDisk is the best on these metrics. Therefore that’s why they’re capturing this value.

So I want to throw it over to you, Vik. Do you think this is SanDisk — this AI truly needing lots of NAND, and performance matters to your economics, to your token cost, and bits are therefore no longer interchangeable? Or is this just a demand thing where it’s like, hey, they’re locking up people for five years because they have supply, and it’s sort of preventing true competition on performance, latency, that kind of thing?

DeepSeek v4 and SSD-Centric Inference

Vik: Yeah, this is good. Did you look at the DeepSeek v4 announcement? Did you look into what is happening there?

Austin: A little bit, but please tell us about it. It’s related.

Vik: That ties in perfectly to NAND. You can see basically how DeepSeek v4 has compressed KV cache massively compared to the previous version 3.2, I think. And you would think, why would you need NAND now if your KV cache is compressed? The problem is that the KV cache still — when you’re doing agentic AI and agentic multi-turn AI, none of it fits in HBM. You’re running hundreds of agents. They all have to have long context, long-running context, multi-turn context. All of those key-value cache pairs are just too much to store in HBM or DRAM. So if you see that DeepSeek v4 invention recently, it is optimized to be an entirely SSD-centric inference system where KV cache is stored almost entirely on SSDs. It is pretty amazing actually.

And earlier, after GTC, when Jensen announced the inference context storage system — which now I think he calls CTX, context storage or whatever — so basically, this is a bunch of SSDs in a rack that is sitting there and connected via high-bandwidth fabrics to the GPU so that they can offload the KV cache matrices into this SSD storage. That is becoming very important.

And at that time, I wrote a Substack post pointing out how this is going to change the inference tokenomics forever. Because one of the expenses — one of the ways you can save on inference cost when you’re using the API, you can look this up for any model, is that it really depends on a few things. First of all, you’ve got the input tokens. You’ve got a certain number of dollars per million tokens. Then you’ve got the output number of dollars per million output tokens, right? And it’s usually like a four or five is to one. Output tokens are like five times more expensive than input tokens because they undergo this reasoning, this thinking process. The thinking process costs a lot more money, so the output tokens are more expensive than input tokens.

In the middle, you have a pricing point called the cache hit or cache miss. So what that means is that if you have KV cache and your inference is able to reuse that KV cache as much as you possibly can — you have a cache hit. And when you have a cache hit, your cost of inference goes down massively. So what people do now is to basically have a bunch of system instructions right up front, and then they’ll only append to the bottom so that you can maintain your cache hierarchy completely. So this is cache-aware inferencing.

And DeepSeek, for example — there was some metric saying that in agentic use, you can make it use 95% of cache hit rates. So 95% of the time, it’s hitting cache. In very few cases, it even goes to 99% it’s hitting cache. So even now, if you go to the DeepSeek API pricing page and see how much the cost has dropped for the DeepSeek v4 Pro, it has gone down to a fraction of a cent per million tokens. You can compare that to Opus. I don’t remember the number right now, but it’s significantly higher.

So what this says is basically SSD-driven inference is the only way forward. DeepSeek has portrayed that clearly now. You cannot store all of this information on DRAM or HBM. It’s just too much. And you almost have an infinite storage of SSDs. The cost per unit is like an order of magnitude higher when it comes to DRAM versus SSD. So you’ve got this essentially free storage. Now capacity is a solved problem if you go to SSDs. The only problem is then you have this bandwidth bottleneck because you can’t access stuff as fast from SSDs as you are.

So I’ve been meaning to read this new paper that’s come out from the DeepSeek team called — I have it on my screen right now — it’s called “Dual Path: Breaking the Storage Bandwidth Bottleneck in LLM Inference,” especially agentic LLMs. So I want to see exactly how all of this ties in together. So I’ve basically given the surface-level overview of justifying why SanDisk is saying that NAND storage is so important in the future of agentic AI. Because DeepSeek is already a data point that is heading in this direction. Long answer to your rather simple question.

Austin: No, this is so good. Okay, so I’m going to summarize it and then I have a follow-up question for you. Okay, so you’re saying, hey look, DeepSeek is showing us that SSDs are more important than ever, NAND flash is more important than ever, and if you think about the tokenomics, it’s way more economical when you’ve got these cache hits versus cache misses. So you’ve got to think really hard about — can we have a very big cache or memory hierarchy and can we store as much as possible? And people are going to be very incentivized — even the end customers using APIs, running agents and stuff are going to be incentivized to actually think about memory and think about caching. Therefore, SSD market is going to just continue to grow.

But my question for you then is — SSD market, SSD TAM going to explode, all good news, invest in these companies, but...

Vik: Not advice, not advice, not advice.

Austin: Why SanDisk, is there a — say that again? Yes, this is not investment advice, this is not investment advice. We are just thinking very hypothetically here. Do your own due diligence. Don’t hold Vik and I accountable. Okay, so the SSD TAM is going to explode, or is exploding, but is a bit a bit a bit, or is SanDisk’s bit better than someone else’s?

Vik: I think a bit is a bit. NAND is a rather established technology. There isn’t a controller — actually, there is a controller difference and the SanDisk controller for the QLC NAND is called Stargate and they’re still working on it. And usually the more bits you add — so in going from a triple-level cell to a quad-level cell, you go from having nine states. A single cell has nine states in a triple-level cell. In a quad-level cell, it has 16 states, a single cell. And now, depending on how you program the cell, you should be able to distinguish between nine or 16 different states. Otherwise, you don’t know what bit it’s holding. Is it holding like a pattern 10 or pattern 15? So the complexity of the controller for this NAND gets significantly higher even when you add a single bit. Like if you go to penta-level cells, which exists in research mode, you go to 32 levels, now you have to distinguish between 32 levels — it makes it very difficult. I have a whole article on how all of this works. But yes, there is a difference in controller and how it works and all that, but it’s not really a differentiating factor. The controller needs to work well.

And as far as I can understand it — please correct me if there are any storage experts out there who actually work on this stuff on a day-to-day basis, they always know better. But as far as I know, a bit is a bit.

Austin: Yeah, we should follow up and bring on someone — Micron, SanDisk, Samsung, whoever is listening out there, of course to talk memory, but also to talk storage. I would love to talk storage here and hear like a product manager’s argument for why a bit is not a bit, because it probably comes down to things like reliability or pricing per bit or other factors than just straight-up read latency or write latency.

Vik: Yeah, maybe there’s some controller magic there, because a lot of the latency comes from adjusting the voltages just right to read this particular state of the cell. So what it does is it iteratively programs the right voltage to reach that state. That takes time. So if there’s some fancy new algorithm that can go quickly, then you can reduce the latency that way. That may be a differentiating factor.

Actually, from IEDM last year — and I think we spoke about this in a past episode. We spoke about a totally different kind of cell where you can dramatically increase the reliability while still having like 36 states to a cell. We won’t get into it here. A circle one, yes.

Austin: That’s right, yes, it was like that circle one or something. Yes, listeners, go check out our backlog.

Hyperscaler CapEx and the Memory Pull

Austin: Okay, this has been a super good memory deep dive. Let’s carry on real quick. Let’s talk hyperscaler earnings. Hey, it was a good quarter for Samsung, it was a good quarter for SanDisk. Memory storage price through the roof, demand through the roof. What does this mean for the hyperscalers? We kind of already hinted about it. Microsoft disclosed $190 billion of capex for 2026 and the CFO Amy Hood said roughly $25 billion of the calendar 2026 capex is specifically higher component pricing.

So that’s pretty crazy. We are only a few years removed from someone like Microsoft spending a total of $25 billion per quarter just on all of their capex. And now we’re talking about in a year, they’re going to spend like a quarter’s worth of capex just on higher memory storage component prices.

Vik: Yeah, just give it to the memory guys.

Austin: Yeah, right, pretty much. Hey, good time to be a memory guy. Meta raised their capex and Zuck on the call said most of the raise is higher component costs, particularly memory pricing. Google had a higher capex, although they didn’t talk about that as much. Sundar did say that their cloud business was up 63%, which was insane, and Sundar said that that would have actually been higher if they were able to meet demand. So still talking about demand and capacity being the bottleneck there.

And then Amazon, they didn’t talk specifically about component prices impacting their capex, but check this out — this was an interesting commentary that came out. The CEO, Andy Jassy, was asked if memory constraints are negatively impacting them. And he answered by saying that for their cloud business, for AWS, memory constraints are actually driving cloud growth. And that feels very counterintuitive. Here’s what he said. Who knows how big this is in aggregate, but he said, “one of the interesting things that we see right now with the change in price and in supply on things like memory is it is actually a further impetus pushing companies who have been on-premises infrastructure into the cloud. And it’s because these suppliers, the memory suppliers, are prioritizing their very largest customers, the hyperscalers, cloud providers. And so therefore there’s a number of enterprises who can’t get on-prem infrastructure and it’s actually pushing them to speed up their move to the cloud.” So I thought that was pretty interesting.

Vik: And I think people are generally comfortable in using AWS cloud. It’s a very easy switch to go and do your stuff on there because it has been the bread and butter for pretty much the software industry for the last decade.

Austin: Yeah, totally. It would be interesting to dive in with them because at this point you ask, who’s still running on-prem? And it’s got to be people who are still just thinking about, what data do I keep on-prem because I’m in the financial industry or health industry or something. But even those folks are still moving to the cloud and they’re getting pulled there faster because the only place they can get compute and memory is actually from the cloud players. Very fascinating.

Vik: Yes. If that’s the only place you can get it, that’s where you go. I mean, it doesn’t matter what you want.

Austin: Yep, it’s like, yo, sorry compliance team. I know we’re dotting all the I’s and crossing all the T’s, but literally we have to make this move happen right now.

Vik: Yes, if you can buy memory from the memory guys, then maybe. Just maybe.

Austin: Yeah, exactly. Yeah, you go find it.

AI Accelerators: TPU, Trainium, MTIA

Austin: Okay, AI accelerators were talked a lot about across the hyperscalers. Google said publicly on their earnings call that the TPU will be sold in a merchant capacity for the first time and at multi-gigawatt scale. And then actually, if you look in the 10-Q, there was some risk language now confirming that the risk to doing that is getting CoWoS and HBM allocation. So I thought that was interesting.

Vik: Just go to EMIB, forget about CoWoS. Just go to EMIB. Intel, Intel for the win.

Austin: Hey, there you go. Yeah, go to EMIB. That’s right. Yes, I hope to write something about EMIB here shortly, soon, comparing it to like CoWoS-L, which also has bridges, but to unpack that for people.

AWS talked about Trainium at a $20 billion run rate, growing triple digits. Of course, people are not generally asking to buy Trainium and they’re not even necessarily renting it directly, but they are consuming Amazon Bedrock and all these services that run on top of Trainium. Trainium 2 largely sold out, Trainium 3 nearly fully subscribed. And Jassy said on the call that because they do custom XPUs, they will save tens of billions of dollars of capex savings each year, which translates into several hundred basis points of operating margin advantage versus relying on merchant chips.

On the one hand, normally I’d been like, wow, that’s so incredible. They’re going to save tens of billions of dollars. But then right away I thought, oh, so they can pay for their memory.

Vik: Yeah, making our own chips so we can pay the memory guys. Yeah, it’s right on a funny cycle. I don’t know what is happening right now, but we’ll see.

Austin: Totally. And then Meta mentioned, of course, they’ve had tons of press releases building up to this quarter about one gigawatt worth of MTIA with Broadcom and they had showed their roadmap of four chips in two years — MTIA, XPUs. We had a great conversation with Meta recently on that with Matt Steiner and hopefully we’ll have more getting into it further. Now Meta did mention significant deployments with AMD and then also running on some new Nvidia. So they were talking up all their multi-silicon vendor partners.

Outro

Austin: So with that, we’ve run long. I think we should call it quits here. Thank you everyone for listening on YouTube. YouTube folks, thank you for your comments. We see that you would like Vik to explain again from our Google TPU one — why is it seven hops with, I think it was Boardfly, and not 16 hops? So we will follow up with you. We’ll draw a picture sometime. So keep writing your comments, keep writing your questions. Thanks everyone for listening, watching us on YouTube, watching us on X. And reach out. Thanks again, we’ll talk to you guys later.

Thanks for reading! Subscribe for free to receive new posts and support my work.
