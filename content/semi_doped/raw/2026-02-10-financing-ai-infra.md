---
source: https://www.youtube.com/watch?v=I1eKrYsgt1k
title: The future of financing AI infrastructure with Wayne Nelms, CTO of Ornn
date: 2026-02-10
kind: transcript
note: 유튜브 자막에서 옮긴 전사. 화자 바뀜(>>)마다 한 줄. 600자 넘는 발언은 문장 넷씩 더 쪼갰다.
---

financing costs are super expensive. It's what's keeping a lot of the you the top Neoclouds you their profit margins are very small and it's because they're paying these huge huge costs per chip every year. So by saying that there's a person willing to buy this hardware in four years. It's certainty and with certainty there's less risk and with less risk you get charged less.

Welcome to another semi-doped podcast. I'm Vicram from Vick's newsletter on Substack. With me is Wayne Nelms, CTO of ORD. OR is building a financial exchange uh for trading GPU compute as a standardized commodity.

Think of it like a futures market for compute power and more recently memory too. So, we're going to talk about it in this episode. So Wayne, how you doing?

I'm doing well. How are you?

Pretty good. Pretty good. Uh so I I heard you got back from PTC in Hawaii. How was that?

It was amazing. Just got back uh late last week. Unfortunately, the flight the flight back was a little rough. There were uh some stops for weather and I think the brakes on the plane weren't working, but got back safe and sound to cold New York. So yeah.

Yeah. Was the weather warmer in Hawaii?

Oh, way way warmer. It was t-shirts and uh actually Hawaiian shirts and khakis every day. So

yeah, now you're back to your your your heavy jackets, I suppose.

Yeah, exactly.

Awesome. All right, so like how did you get into the idea of starting a financial exchange for GPU compute? This sounds like a great idea. Uh but like how did you even come across this thing and uh give give me give us some background of how you got into this?

Yeah, sure. So I can give you the full the full rundown. So, uh, I graduated not only just last year, I graduated in December of 2024, a semester early, from MIT. Um, and there I was studying math and computer science at school.

Um, I was on the tennis team. I was a big tennis player in high school as well. Um, and then I got into poker in in college. And so, uh, pretty much after I graduated, I was trying to figure out what to do.

I started working in trading. So, I was a quant trader uh doing equity options at Suscuana or SIG in New York. And um I love the job, but at the time I saw all these companies, all these Bitcoin miners that were evolving their business models into GPU as a service. So, you know, iron and terolf, you know, then Cororeweave u most famously, I guess.

And I kind of saw their stocks take off and I was wondering what, you know, what's going on here? I have to figure out, you know, what is what is a semiconductor? What is going on? So, I took some time, did a bit of research and went to one of my closest friends at MIT from school.

We had known each other for four years. His name is Kush Bubaria. Uh, he's the current CEO of Orin. Um, but we were just trying to figure out what to do.

And at the time, I was doing a little bit of stuff on the weekends with a friend in private equity. Kind of talked to him about what they were doing every day. And he told us, both Kush and I, that, you know, they were looking into data center deals, but they didn't really know what was going on. They didn't know how to measure risk.

And this theme kind of was the genesis of what orange is today. It's how do you categorize risk in the data center space in the neocloud industry. Um you know what is the value of compute and then we kind of took that idea and ran with it um using my financial background and Kush has a background in venture and and startups. So taking our our unique set of skills and then coming together to try to solve this issue.

That's awesome. Actually that's an important question like what is the value of compute because now you know you have this the era of like uh agentic AI and you have cloudbot that's like taking over uh all you know people's computers I suppose now people are trying to buy Mac minis uh so compute has somehow landed up in the edge uh all of a sudden you know so that the question is always what is it on the cloud and what's the value on the cloud and things like that. So yeah, this is a very important question. So uh basically what what financial infrastructure exists for AI compute today or is there no such thing?

Uh what's out there?

Yeah. So we're still in the very early stages of of all this stuff of the financialization or commodification of compute. I would say there's a few uh startups uh that are focused on trying to you know standardize it. Um so you have people that are actually focusing on the offtake um like SF compute uh those sorts of models and they have standardized compute in a sense right they have a minimum benchmarks for your compute um that you can resell on their platform um and then there's also a few businesses like ours that are you know tracking prices of compute across the country um based on provider based on you know chip type networking etc.

But in terms of actually being able to trade it, which is the next step, right? We can track it, build indices and and look at how numbers move, but if you can't trade it, if you can't, you know, hedge your actual operating expenses with this number, I would say the value is is minimal. So what we do at OR is we actually allow you as either a data center um colo operator neocloud or on the flip side right if you're buying a lot of compute um if you're you know a lab university hospital we allow you to actually take positions against this number or on this number and that can help you you know materially hedge some of your operating expenses. So I can give you a brief rundown, a brief example.

So

yeah,

let's say you're a lab and let's say you know you have a long-term contract of course you know three to five years let's say but let's say you're have some inference demand and that demand is very spiky. You can't really predict for the inference demand. So you need to buy some compute on the spot market let's say and the spot market meaning right now I need it today. Um, a lot of the time if you're buying a lot of compute at once, it can drive the price up.

That's just how markets work, right? Supply and demand. What people need right now is a way to hedge the price. So, if I'm buying a lot of compute at once, I want to be able to protect or put a ceiling or a cap on how much I'm paying.

So, what we do is we allow you to buy a feature on our platform. It's fully cash settled. Meaning when you buy a feature on or you don't actually get the GPU hour, but what you do get is a way to hedge your cash risk. So if the price of the index moves up because you're buying a lot more compute, you actually make money on the hedge.

So in effect, you're you're capping your upside and your payment. And on the flip side, you know, if you're a data center and you're selling a lot of compute, you can sell a future on our platform and put a floor to the price that you're selling all of your compute for. So it works in both ways and and we've seen a lot of people being interested in this product because in every single commodity space if it's oil and gas, you know, electricity, this sort of product exists because there's a lot of people buying today or tomorrow and they care about, you know, putting a cap or kind of a collar we call it in finance on their on their prices, their costs um and their revenue.

Awesome. All right. So for like basically GPU pricing, let's take an example. Uh so I know it varies depending on what kind of surrounding resources you have with the GPU compute that you're going to rent out for example on the spot market today like I want to run a little you know fine-tuning run on a model and I need some compute to do that.

So let's say we pick I don't know an H100 or a B200 or something you know take take your pick. Uh what is the pricing example like? Is it $100 an hour? Is it $10 an hour?

How does that spot market number look like uh between a few providers? If you have any numbers to put out there, I think it helps understand even for me where this is coming from.

Yeah, sure. So, we track a variety of providers. So, let's just say H100, um, SXM, uh, that's one of the the models that we we think about the most as a benchmark. So, you know, on in marketplaces, a lot of the marketplace pricing is a bit lower on the lower end. Um, so we have roughly around a$1.70 180 today for an hour on a H100 GPU.

Okay.

But as you move up the stack, so I'm saying, you know, NeoCloud level pricing, so call it the Corewave, Lambda, Crusoe, Nebus, you're getting around, you know, three to four dollars range. And then if you go up to, you know, the AWS GCP, you're looking, you know, five to six to seven dollar range. And so, you know, part of the problem when you think about standardizing compute is how do you, you know, how do you standardize across all these providers because each of them is kind of providing a different level of service potentially, a different level of quality, um, uptime, you know, sort of these benchmarks and metrics. So what we do is we exclusively think about the marketplace.

So closer to the, you know, the quoteunquote lower end of the spectrum, at least in terms of cost, because we think that these marketplaces are a more um realistic example of how a spot market should work, right? There's a lot of people that list compute, there's a lot of people that buy compute. The market is very dynamic. When you go start when you start looking at these hypers scales, the truth is the prices don't change very much, right?

they they might decrease their cost or increase their cost every quarter, once a quarter, twice a quarter potentially. And we don't think there's a true reflection of where daily markets are moving. You know, as a product that tracks GPU hours, we want to have our index be as dynamic as possible and, you know, allow you to have real exposure to the truest form of on demand comput. So, we track marketplace compute.

Gotcha. So for the same H100 depending on where you're running the actual hardware the price actually varies right is there a reason for that? That's my first question. And the second question I have is how do you standardize a fixed price if everybody is charging different rates for the same hardware?

Yeah. So a lot of the differences comes down to the the hardware itself as well as the regionality or where is the compute or the GPU actually located. But these are problems that have been solved in the electricity markets as well. Right?

So in electricity markets the way it works is that you have hubs and each hub is a location you know either in the US or across the world which has a different price for the same electricity and for compute for powering a GPU you know electricity is a huge input cost. So you can only expect that this you know these this regionality bias in electricity should also be analogous to the regionality bias in in compute. So what we do is we consider only the compute in a certain region of the United States and the we instead of kind of trying to standardize across the entire country or in the entire world, we say look we only will track a specific type of compute in a specific region. Um and that allows us to maintain kind of uniformity across our product.

allows your hedge to be very specific and as a result hopefully uh makes your hedge a way better product for you and your business.

Gotcha. So as a going back to the example of where I was going to rent an H100. So now through on let's say I I can uh purchase a amount a certain amount of compute at a certain price that is determined by the on index that you determine through the spot price market. Is that right?

Yes.

Okay. And so so basically so now that I have this bunch of compute now let's say the next quarter rolls around and the compute prices go up and now for the same because I kind of bought compute at a certain uh lower price I'm doing better off now because I was able to get in early and get my fixed rate. Is that that that's how it works right?

That's roughly correct. So yeah, I can pretty much how it works is that the futures the way it works is you're buying it today for a time in the future. So what you can say is look I will be buying a lot of compute in let's say February of 2026. So what you can do is you can go on our platform there's a February 2026 future and it has a price let's say $2.

Mhm. you can buy that future for $2 right now. And what it does is it exposes you to the spot prices in or across February. So if we get to February 1st and the price of our index is $21 and then on the 2nd of February it's $22 and then let's say it goes up and down around $25 across the entire month.

You're buying compute across February because that was when you needed compute. However, because you bought our future for $2, you effectively have locked in your your your cost. So, even if compute prices went to $10 or $20, you know, it would ideally never happen. But if it went up significantly, it wouldn't matter to you because you already bought the orange future.

So, what we're doing is effectively putting a price cap on any computer that you would be buying in the future.

Gotcha. Gotcha. And so, what determines the spot pricing? let's say of $2 in the beginning of February. What are the factors that kind of go into this pricing to begin with in the markets? The market set this value, right? Somehow.

Yeah. I mean, it's purely supply and demand, right? And it all boils down to that. So, just how many people are offering H100 hours in February and then what is the demand from both, you know, the research, the training and and the inference needs of the community um of of AI users, right?

And that's kind of how every single market works. And that's why we love and we've tried to bring all those financial concepts to compute because at the end of the day there's huge supply constraints in this market and also huge demand and in any sort of you know resource of human history in which this sort of dynamic existed financial markets have closely followed. So we just believe that you know we're at a stage in which there needs to be a financialization of compute and we're trying to build the first kind of take the first steps to make that possible. That's awesome.

So you talk about supply and demand you know with these massive hyperscaler buildouts these days you know all you ever hear in the news is essentially uh how much there is a shortage of this and there's like always an over demand and then under supply. So, is there anything holding you back from extending your GPU compute as a as a commodity concept to other parts of the AI infrastructure market? There's memory, there's storage, there's lasers, uh there's like optical fiber, you know, is there anything stopping you from extending all the way across the chain?

I mean, no. So there's definitely a lot of things that we are thinking about rolling out in the near future in terms of you know components in the AI supply chain just like memory. So what we recently did um so thanks for bringing it up is we have memory features now. So if you have an opinion on the future price of DRAM, no DDR5, DDR4 as well as SRAMM products um you can trade that on or um and these are products that we recently launched on architect um with Brett Harrison and you know this is a a future that we think needs to exist.

So there's obviously been a lot of talk recently about this the skyrocketing price of memory right memory is a huge

input into a chip. It's very necessary for compute and people want to have access to memory in the future today, right? And so that's exactly what a futures product is made for. And you can see future demand right now on our product. You know, memory is trading way higher than what any of us could have expected. Um, and hopefully some of the existence of our product will alleviate some of those future demand concerns.

Yeah, that's awesome. So that's a memory is like so important. So memory is one of those things right now where it's a clear example why you would want to hedge your prices and lock it in at a lower price because it's like it's insane, right? The memory is a great example of why or how futures markets uh should work and you know how people should lock in or h be able to hedge on these prices.

So uh but that's awesome. You mentioned one thing about architect. Um, so do you want to dig in a little bit about your partnership with Architect Financial? Cuz I it was in the news recently.

So, you know, I think I'll let you explain what that partnership is all about.

Yeah. So, before our partnership with Architect, we on Orange's um dashboard or trading platform, we allowed you to trade swaps. So what a swap is it's agreement between two parties um in which one party takes one position let's say buying the future one party takes the other position selling the future and it's a onetoone matching in trading so it's a bilateral swap on architect the beauty of it is it's a perpetual exchange and what that means is not only is it are you exposed to the daily price every day so it's like buying a stock almost it if it goes up you make money if you're buying it. Um, if it goes down, you lose money if you're, you know, also if you're buying it.

But it also allows you to match many to many or one to many. So, if there's a big seller, right now we have to match the big seller to one big buyer, if that makes sense. On architect, if there's a big seller, Brett and his team at Architect can match them with a bunch of small buyers.

And so, it makes this market way more, you know, uh, representative of, you know, true true markets. And this is kind of what the future of or might look like but also just the future of compute training in general.

Okay. Okay. Awesome. I mean so you you have like basically two things we have discussed so far and looking at it it's like compute is one thing and compute is based on let's say hardware and you know like H100 was an example we spoke about right so there's been a lot of discussion about how long an H100 is actually useful what is the useful life of an H100 and if you look at that in that sense the more time passed passes by maybe H100 compute should get cheaper over time. Is that right? Is that a right way of looking at it?

There's a lot of factors that are involved, but I would largely agree that we expect that H100 prices will fall over time. However, what I will say is that we've been tracking, you know, H100 pricing in the spot market um with our index for the last year and a half or so. We've also been tracking A100 prices, you know, in the small market for the last year and a half or so.

And what we've seen is that A100 pricing per hour has remained relatively stable, if not increased over the last few months. And so we believe that this could also be a potential path for the spot price of H100s. So, I think there's a lot of questions and there's a lot of factors that are involved here, but it's really going to come down to in the near future, you know, inference demand for older generation of chips. Um, just like the A100s, you know, potentially V100's and H100s.

That's awesome. What do you what do you believe is the way GPUs depreciate? Like there's so much discussion about whether it's a 5year depreciation period or whether it's should be counted as 2 years and Michael Bur actually on his substack kind of came in with a bang with this whole discussion and people have like so many opinions. What's your opinion?

Yeah. So first of all I want to shout out to Michael Bry. I love I love the big short. Um

it's really interesting. So I think there's a difference between useful life of a GPU and the prime life of a GPU.

And I think a lot of times when we think about and when people say what is the useful life of a GPU, it kind of implies that after five or six or you know however many years that this GPU is just suddenly worthless. It's just scrap metal, right? But we've seen with A100s that that's not the case whatsoever. There's always a use case.

someone's always going to need that piece of hardware or that piece of HPC equipment for some use case, right? So, there'll always be some residual value. So, I think the prime life of an H100 or of a B200 or a Reuben, you know, I think 5 years could be reasonable. I think it's probably closer to two or three years.

But I think when you think about the useful life, how long is a chip actually going to be in a data center for? You know, we need to be thinking longer term here. it could potentially be five, six to 10 years just having relevance to the market. So I would if I had to model this out right I come from a trading you know quant background you know it's definitely not linear and I think that's the biggest mistake that people are making today right if you think about how is it depreciating on a financial model if you have to map out the profitability of a data center right a lot of people are thinking about this in a straight line depreciation aka the GPU loses the same amount of value on the balance sheet every single year I think that's a very naive assumption And I'm almost certain that no one thinks that's exactly correct, right?

I think what is reality is that a lot of the value is lost across the first three years and then the remaining five, six, seven years are fairly flat or fairly stable. Um, so at OR, you know, one of the products that we haven't talked about yet that we're doing currently and we're we're spinning up today is a residual value product on the GPU. So this is very interesting, right?

Okay, tell us more.

Yeah, what this allows you to do as a data center or as a Neocloud is sell your GPUs in the future for a certain price. So I can give you an example of how this might look. So let's say you just bought a few, you know, let's say 72 racks B300s, right? And let's say you're uh a data center operator in NeoCloud and you built these and you're installing them for a certain client.

You have a tenant that has a let's say four-year contract with you, right? So they agreed it's a take or pay model for four years. They will pay for this for access to this B300 cluster. The issue is after these four years, you know, there's a high likelihood that, you know, maybe Reubins are in production or there's a better chip available for you from an efficiency standpoint.

And if that's the case, this tenant that you have for the first four years might not renew the contract, right? So at the end of the four years, you as a Neoclad want the optionality to sell that cluster to someone else to pretty much get rid of it to clear the space in your site so you can install different types of GPUs or you know something else just to reout your your site. And so what we do is at OR is we allow you we give you a price today for that hardware in four years which helps facilitate that easy transfer of hardware. It helps, you know, clients have access to better chips and it really helps create the market that is necessary for an efficient marketplace.

That's a good explanation. So, what you're what the way you describe uh the depreciation of the GPU is kind of more like buying a supercar and driving out of the, you know, showroom. The moment you drive it out, it rapidly drops its value and then your McLaren is still probably worth it or your Lamborghini is still worthwhile. I mean, it has a value. It doesn't ever go to zero, right? I mean, is that like a very naive analogy or is that uh even remotely what you're describing here?

Yeah, I would say yeah, that's roughly correct. Like

okay,

there is a huge depreciation um kind of drop in the first four or five years. Yeah. So, so what people would want to do is they want to uh get the best hardware for their training runs initially and that's what you were saying that some a tenant is going to get in on the best hardware that a Neocloud has built out in a certain space and then once they realize or they have moved on to the next generation to train the future models which is what the tenants's main business objective might be. uh the the same facility can be used by someone else to maybe run inferencing on uh and the compute is not entirely worthless just because the original tenant has left the building because they didn't have access to the best hardware, right?

And so

yeah, so what you what AR on helps you do is uh price today what uh the whole data center would be worth in four years from now when this tenant leaves and so that the next person coming in for you know picking those same chips up for inference can lock in their rate today. Is that right? Did I get that right?

Exactly. So we just price the GPUs and we don't worry about the switches and some of the networking stuff but yeah we will give you a price for the hardware the HPC just the GPUs um

yeah today and for four years just like you mentioned so someone else can come pick them up use them for another purpose you know offload that to the secondary market and you know I have a lot of thoughts and about the emerging markets as well like where where are these chips going to end up

in four years right where H100's going to be geographically speaking in four years. You know, right now we see a lot of the data center and infra AI infrastructure buildout in America. Will that continue to be the or in Europe and in Southeast Asia. Will that continue to be the case?

Will there be you know places in South America potentially in more eastern Europe or you know potentially Africa or you know now we're saying the moon or in oceans in space right or or in deep ocean. There's so many places where, you know, data center development could happen in the next five years and it's really up to the resale market, the the people that have access to older equipment. It's up to them where this stuff ends up. Uh, and I think that's a super interesting space and we should all be looking at into the resale market for Nvidia hardware in 2028, 2029, 2030.

So interesting. Uh it's it's interesting that you said you would not price in the network and all that, but what about power? How do you price in power?

Yeah. So the power it's it's a little different, right? Because the power is sight specific.

Yeah.

So when we take out the hardware, we're not really pricing for power. However, we understand that that's a huge concern when you're building out a site, when you're choosing a site. Um especially as the market will shift more towards inference. you know, it's all about efficiency, dollars per token, and that's going to be largely based on electricity prices. Um, so this is a definitely a problem in the space that people need to think about. Um, but maybe luckily for me, I don't have to think about that.

Okay, that's awesome. Okay, so this whole pricing, you know, now I think you have a the index, right? The on index for uh whichever commodity it is. It could be GPUs, it could be memory. Uh, who benefits from this transparent pricing? Who benefits from having a a fixed index going into the market for let's say compute?

Yeah. So, I think the real value ad really goes to the people buying compute, especially smaller players, right? Um having transparency in markets is great for usually all market participants but I would say in this specific case it's largely beneficial for the buyers because I think the way the market currently looks is a lot of people are paying for compute or a level of compute in terms of benchmarking and performance that they might not need. either they're overpaying, they they have too many GPUs themselves that they're not utilizing, or the actual performance is higher than they actually need.

And so by showing the markets kind of where the marketplace compute prices are, I think a lot of people are starting to think like, wait, I'm paying X amount more for AWS or GCP clusters or instances, you know, why am I paying so much? Am I actually using all of it? And there's a huge efficiency question for a lot of the smaller players. Call it, you know, the hospitals, uh, some of the labs, the smaller labs.

Um, people using it for recreational uses, you know, like the claw bot kind of community, right? Like maybe they don't need to pay $8 per GPU hour. Um, and so we're trying to bring that transparency to the market first and then, you know, from there allow you to to put on the hedges, to do the trades, um, to think about selling your GPUs in the future. All all those products are built on top of that index.

Do you ever so fundamentally the hardware scene is changing so much you know you could have in inferencing land you suddenly have all this talk about SRAMM based inferencing and most recently you have Nvidia announcing context memory storage systems which are basically just large drags of flash storage um which is extremely good for long context inferencing. So when you're pricing out uh a data center buildout for the future like you were explaining like the four years out kind of deal what is the risk from an inferencing provider point of view that the hardware is just no longer relevant and somehow the earlier generation GPUs used for training are simply not somehow useful for inferencing. Is that a possibility at all? How do you price that in?

It's certainly a possibility. Um the thing what we think about when we price these hardware or this hardware is largely from a you know what is the obsolescence risk. So obsolescence risk what is the likelihood that this GPU will be usurped by a better hardware architecture generation etc. You know we're pricing the tail risk.

So, you know, we're usually covering between 15 to 30% of the residual value, aka if you bought, you know, let's say one ship for $30,000. You know, we're protecting around 8 to to $10,000 of the residual value. So, often times we're covering the very tail ends of the of the market. And so, as a result, we think that, you know, from an inference demand standpoint, this price is still very attractive uh per chip.

I will agree with you however that there's a large chance that potentially these chips aren't even used for inferencing anymore. They're just put in an emerging market for training. Um which is where we think a lot of the future demand will come from. So yeah, it's it's kind of both of these both of these players would be interested in the secondary market, the inference kind of providers as well as you know younger labs potentially that are spun up in emerging markets.

Yeah, that's a good point. I mean, I like I like the way you you address this because I don't think it's obvious that inference is always a byproduct of training hardware cuz I think people view this as a downstream consequence. They're like, "Okay, let's get the best hardware out there, the you know, the the Reubins and the best Blackwell or the 200, 300, put them in training runs, and you know, when their useful life is done, we just shift them over to inferencing, and that's the that's going to be the future, whatever. " Maybe that's not the case.

Maybe with the rise of inferencing with so many agents now starting to do inference long context stuff uh and people are running you know these inference bots on chron jobs so they basically run forever you know or on timers and things like that the amount of computing you need is enormous so we might come to a point where we're like wait we need more compute and more hardware and better hardware for inference than we do for training and so the problem is flipped on its head in a sense.

Yeah. No, that's exactly right. I mean, it's going to be so interesting to see like how the market moves in the next few or few years uh with the like the rise of inferencing demand. I mean,

only time will tell, but um will be a very very interesting market.

Yeah. Does any of this change how data centers are built out at all going forward?

Yeah. So, this is one of like the long-term effects that we believe, you know, our product provides. So when you think about a futures market how this actually looks is you can put a price on compute in each month of the year multiple years in advance. So I can say that you know uh in 2026 February an H100 hour is worth this March it's worth this you know etc. in 2030 an H100 hour is worth this, right? Which is incredible information. You can kind of plot across uh you know a cartisian plane like what the value of compute is.

Yes.

And so when I think about okay I'm I'm a data center operator. I'm thinking about what ship do I want in my data center.

Yeah.

One of the earliest questions that you know Kush and I had when we talked to data center operators is how are you modeling your profitability? Right? Like you're spending hundreds of millions, billions of dollars on hardware.

Yeah.

On chips from Nvidia or others. How are you thinking about profitability? How much can you rent out this this chip for?

They would tell us a price. Sure. What about next year? They tell us another price.

Where are you getting that price from? Right. And so with our product, you can actually map out your profitability per chip, per hour for the next three, four, five years. And that can help you determine whether or not you should even get into the business, whether or not you should build the site in that location, whether or not you should use that chip or maybe the newer generation, right?

It's so important and so valuable. And so we think that that in and of itself will help facilitate data center development both in America and across the world. And just to add on briefly with the GPU value insurance product that I mentioned where you know will come in put a price on your hardware in four years.

Yeah. that actually allows a data center to do a very similar thing which is tell their lender right a big credit fund a big uh backer of their project look in four years even if my tenant doesn't renew the contract I can sell this hardware to someone else and what that allows them to get is a cheaper financing cost right financing costs are super expensive it's what's keeping a lot of the you the top neoclouds you their profit margins are very small and it's because they're paying these huge huge costs per chip every year. Um, so by saying that there's a person willing to buy this hardware in four years, it's certainty and with certainty there's less risk and with less risk you get charged less.

Yeah, that's a that's amazing. We need some of this stuff like you know all my my my days go into looking at engineering about these things and how these things are built. So, it's really fascinating for me to talk to someone like you who's looking entirely at the financial side of things and it is so important because it determines how all of this stuff is built out. There so much money moving around these things.

It's just fascinating. How do you think we will look back uh in 10 years from now and think you know that was something weird we did or uh what what do you think is like we're going to think back about the current GPU compute boom in 10 years time?

Well, I think the the first thing is we'll just realize how crazy of a time it was, right? The Mac minis, the quad bots, right? because you know being able to buy compute um and the the price of memory just skyrocketing right these are things that um you know might not be relevant in 10 years or maybe they are but it'll be a crazy time nonetheless but I think the more important thing kind of going back to something we talked about is that we'll realize how insane it was for these data centers to be built almost based on intuition or hope right like oh I just hope that there will be more compute demand Right? I mean, I'm not saying that there won't be more compute demand, but right now there's no numbers backing that up.

It's hard to quantify what feature demand will look like.

Um, so right now, I think we're in this interesting time where trying to figure out and try to quantify that number itself is so valuable. So looking back in 10 years, we'll be wondering how were we able to finance these projects, you know, without without that sense, without that insight. Um, and hopefully, you know, ORN is the first step to to providing those insights as well.

That's awesome. I think I know I'll be laughing back at the time when Meta started building data centers in tents and just because they had to build them out fast enough. I think it's like f we don't realize what we're living through now, but it's going to become evident u in like a decade from now.

That's that's pretty awesome. Thanks for explaining all this stuff. So I think it's very very valuable to see the business and financial side of semiconductors and while on this podcast we generally talk a lot about the technical side uh my other co-host Austin handles the business side really well usually so this has been a bit of a adventure for me so thanks for like putting up with my questions probably very engineering like as it seemed. Wait, no, I think well, first of all, thank you for having me and I think this stuff will become even more important in the future.

You know, financial engineering and helping these data centers exist um will allow and fuel the compute and AI revolution uh moving forward. So, yeah.

Awesome. Uh so, if people need to visit uh on I think it's onai.com, is that right?

Awesome. And Wayne is on X at Wayne_nelms with a Z. Right.

Yes.

And so you can follow him on X and uh do check out on I think it's a very uh interesting u financial product that's out there and it's very important to have futures just like we've had in oil and electricity and so many other things going forward. Right. Uh that's uh we'll call it for now. That's the end of the podcast for this one.

Thanks Wayne for being on and um for all the listeners out there. If you are uh enjoying this podcast, be sure to give us a five-star rating on Apple Podcast or any other platform you're listening to. We also put these episodes up on YouTube or any other podcast uh platform of your choice. Thanks for listening.

I'm honest.
