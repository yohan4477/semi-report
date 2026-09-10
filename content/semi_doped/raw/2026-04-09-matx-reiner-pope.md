---
source: https://www.youtube.com/watch?v=7Ph9i1KYHxY
title: Reiner Pope (MatX): Designing AI Chips From First Principles for LLMs
date: 2026-04-09
kind: transcript
note: 유튜브 자막에서 옮긴 전사. 화자 바뀜(>>)마다 한 줄. 600자 넘는 발언은 문장 넷씩 더 쪼갰다.
---

So, as it happened, we left Google, um, 1 week before ChatGPT was released.

No.

We did not know it was coming.

We have a special guest today, co-founder and CEO of MatX, Rainer Pope. So, welcome, Rainer. Um, for listeners who haven't heard of you and MatX, who are you? What is MatX? What are you guys trying to do?

Thanks, and very happy to be here. So, um, who am I? As you mentioned, I'm CEO of MatX. Um, what we're doing at MatX is we are making the best, uh, chips for LLMs that is allowable by physics.

So, the way we got here, my co-founder, Mike Gunter, and I, um, prior to MatX, we were working at Google for a long time. Most recently, I was on the Google Brain team training one of the LLMs at the time, and Mike was on the TPU team. And there are a lot of things that we wanted to to do to make the TPUs much better for, uh, running LLMs. Things like running at much lower precision, having much much more compute performance based on large matrix support, uh, and then generally, uh, really optimizing for LLMs, reducing a lot of the other circuitry that was needed for non-LLM workloads.

Um, at the time, this was in 2022, uh, we we figured that, uh, turned out the best way to do this would be by starting a separate company, which is MatX.

So, take me back. You mentioned 2022, you came out of Google, which I will say, um, it seems like everyone came out of Google that's that's at the forefront of AI and hardware.

Yeah, yeah, there will be a book written, you know, 10, 15 years from now that we'll get to go back and read, and it'll be fun for us to remember the good old days. But, okay, so 2022, around then you started it. Now, and I know your Series A talks about, um, proving out all your technical bets in that Series A blog post was in 2024, and it said, you know, over the past 2 years. So, my where my brain first went to was like in late 2022 was sort of the pivotal moment, that I think is November 30th when chat GPT officially launched.

How much ahead of that were you guys thinking about this direction? Did you launch before chat chat GPT, after chat GPT, and how did that sort of like inflection point from the general public becoming aware of transformers, how much did that change your life in in so far as fundraising, vision casting, hiring people?

Yeah, so as it happened we left Google um 1 week before chat GPT was released.

No.

We did not know it was coming, but the like the historical context there was that GPT-3 had been released more than a year earlier. And so it was released in this developer demo. It was really hard to use, but you could go online and you sort of had to get in the mindset of like, I am writing a document and I want the rest of this document to be the response uh that I'm looking for. And so it's not a chat interface at all.

It's totally different interface. Uh but if you were paying a lot of attention you could see like just the potential there. Uh and so I think a lot of people um insiders in the industry were appreciating something big is happening here. And then the question really at the time pre-chat GPT was these models are incredible, but they're a hundred times more expensive than the models we're used to running.

Like they're a hundred billion parameters instead of like a hundred billion parameters. Um can we even afford to run them? And just the the simple economics doesn't work out if if you're used to running software as a service where every query is free. And now you have to spend like cents per query.

When I've got millions of queries per second, it doesn't pencil out in the traditional math. Um and so the big question prior to chat GPT was like, okay, cool demo, but it's too expensive. Can you actually productize it? And I think there's a lot of skepticism that that you actually could.

Uh chat GPT, that's the big thing that chat GPT demonstrated is that you can and and not only that, but the product is incredibly uh valuable. So what that meant for us was we had already seen, "Look, prices are going to be high. If prices are high, can you like can you make how do I to make prices cheaper? " Um it turned out to be quite difficult for us to fundraise even after ChatGPT.

Um the it took about two quarters for for that to really land where the impact on Nvidia's stock price showed up because then there was the realization, "Okay, this is using a ton of GPUs. Now a ton of folks are buying a ton of GPUs. " And then eventually like Nvidia reported these gangbusters quarters and then and then and then I think at that point investors started seeing the potential.

Oh, okay, interesting. So, you started by just saying like, "Hey, it's going This is really transformational and maybe we have if you're paying attention, we have a sneak peek, but it we can tell already that on the current hardware it's going to just be like too expensive. So, there's got to be a better hardware solution. " ChatGPT launches a week after you guys leave.

And I would kind of expect that maybe investors would go, "Oh, I can see this is going to be productized like you said. " But at the same time, I see your point where it's also like, "Oh, Nvidia is the one who's capturing all the value here and selling GPUs. " So, was the early um sort of skepticism just around like, "Why will anyone buy hardware that's not a GPU? " Um or did they quickly connect the dots of like, "Oh, it's a GPU, but GPUs aren't necessarily the most efficient.

" Yeah, so I think some of the skepticism definitely is about how why would you would buy hardware that's not a GPU. And then the other one is just how do you compete with the world's biggest company?

Ah. Yes.

On the why why would you buy something that's not a GPU, the big uh consideration there is the the the software moat that that Nvidia has. Everyone writes CUDA. Um how could you imagine? And especially like historically we've seen how much software lock-in there is in so many businesses. Um why is this one different? Where like isn't there going to be software lock-in here? Would everyone really rewrite their software onto onto a different hardware platform?

Got you. So, let's let's jump into that right now. So, is there lock-in and and how are you thinking about it from a software perspective?

So, I mean at this point I think it's proven that that the lock-in is pretty weak. Um all of the I mean barring Google who has been on TPUs forever, uh all of the other frontier labs are multi-platform. So, OpenAI, Anthropic, Meta, X like they are all on Nvidia. Just Many of them are on TPUs. Uh there are Cerebras announcements. Um AMD, uh some some Broadcom develop chips as well. Um So, all of these players are multi-platform. Uh they're willing to do that. Um and so I think like that is the proof already that that the software lock-in is not that that great.

Sure.

If you want to sort of think about what are the first principles reasons why that is, it's because um software versus hardware lock-in is really a question of like how much spend are you putting on the hardware versus how much spend are you putting on the software engineering uh to support the hardware. And this is really the first time where that that balance has changed and this has violated a lot of people's intuitions. Uh historically like the whole history of software as a service is um you're paying like really large salaries to a large software engineering team um and then the compute spend is is a small fraction of that. And so, uh engineering time is precious is the mantra.

Um and so, of course there you have to prioritize that ease of software. But, this is totally turned around now. All of the frontier labs are spending tens of billions of dollars on compute and the the salaries of the people who are writing software for um uh for that compute are very high, but it's still small in comparison to the compute spend. And so, that ends up just meaning the the rational choice is to do anything you can to get hardware costs down.

Be multi-platform, be willing to get the negotiating power that you get from that and so on.

I see. Interesting. So, from first principles it makes a lot of sense. Now you're going to spend so much money on hardware, how can you spend it correctly on software to unlock that even if it means like you have a team that's writing kernels specifically for this architecture or something.

Now, to your point, um fast forward from 2022 and you started to now, now we're seeing like everyone has multi-vendor silicon in it and it's made the point. It's very easy for you. Back then, if we put ourselves back in sort of like you're you're just starting and you're trying to raise that series A, um you you clearly were just trying to articulate that and and hope that it came to fruition. But but tell me like of your early investors, I mean some of them must have believed.

Like what got them to sort of believe you in a world where it looked like Nvidia was had all the GPUs and and had the lock-in. And and that this is to to your point, like this is actually different than all the past sort of eras that we've gone through.

Yeah, I mean ultimately I think all of early investing is primarily a bet on people rather than on technology. There's a bit of both. Like you can have the best people in the world and have a business plan which like doesn't make any sense at all, but I think the at least to some extent the premise that there is a physical product that we make that we will sell for dollars is a very easy business plan. Like it's clear how you can make margins off of that and so on.

In some sense that's even an easier business plan than starting a frontier lab. A frontier lab it's like, we're going to make a model we hope we can sell it in a product that hasn't been defined yet or something. Um but with uh but but with selling hardware at least the the business case there is clear. And then I mean especially for early like seed stage investors, um it's primarily going off of just uh uh who we are, our backgrounds, and then also folks we've worked with who who vouched for us.

Sure. Yeah, that makes sense. And of course, you have the credibility of having been TPU people at Google.

Yeah.

So, makes a lot of sense. So, tell me Okay, actually really quick question. I don't know if I've heard you say this anywhere. Where What Explain the name MatX.

Yeah, um matrix multiply. So, like one angle is like just uh you remove RI from matrix. Another one is like the the X is a is a times.

Nice. Nice. Okay. So, now then take us into the first chip, the MatX 1. And now And let me also say that, you know, I know that you raised $100 million to start and then and later uh just a couple months ago you you raised $500 million and we're we talk about a chip, but I know you're actually building a system and the goal is obviously like data center deployments. So, with all of that context, like tell us tell me about the chip, but I I want to get into like the bigger system.

Yeah. So, um a few of the the sort of core bets of the chip um are uh I mean, primarily very high matrix multiply performance, higher than anyone else uh as announced in in the market. Um There There's a whole story there, but I would say in a in a summary it is the um the marginal returns on having more matrix multiply performance seem to be much higher than marginal returns on more HPM performance or or other other considerations. So, uh got to invest in that first.

Um And then in addition to that, uh there's the sort of this thing that has just been like uh a free money that's been sitting on the table, um which is like get your memory system right. Um and so that that is a combination of seeing two good ideas in the market. Um Nvidia, Google, Amazon have been like uh all all tensors in HPM, so HPM first. And then Cerebras and Groq have been uh weights in SRAM.

Um That gives you very low latencies, but it has some capacity problems. Um You can put those two together. It's It takes careful engineering and you need to balance it the system right. It's hard to balance the system right, but but it is totally doable.

And so that is the other thing we've done and it gives some some really big advantages in both latency and throughput.

Nice. Yes, that makes sense. And I think a lot of people are now starting to connect with that as they see you know, the Grok LPUs and the Cerebras. Um, so so they see the benefit of SRAM weights and SRAM for low latency, but of course HBM for high throughput. And KB cache as everyone's starting to realize like context is awesome and the more context I can give it actually the more interesting, you know, insights I can get from the model. Um, so you made the right bet. Was that an architectural bet that was sort of made from day one? Just based on first principles, yes.

Yeah, I mean, so one of the things I mean one of the things we're very good at is uh workload mapping to hardware and like creative and new ways to do that that that are more optimal, especially when you consider that the space of what potential hardware could be. Um, and so the this combination of uh of these different memory systems uh was a sort of a core idea going in. Um, uh the one of the things that really enables like you look through the list of uh um uh parallelism and partitioning techniques, tensor parallelism, expert parallelism, pipeline parallelism. The last one is like the sort of ugly stepchild in some sense.

It It doesn't It really doesn't have a lot of the It It misses a lot of the advantages of uh um optimizing latency and optimizing memory footprint that the other ones do. Um, and it turns out that's actually a memory system choice. Uh, if you like this this combination of uh SRAM and HBM actually brings makes pipelining work sort of as well as the other things for the first time ever. And so So, we understood that and and that was the thing we were going after.

Okay. So, back in in 2022 when you're making these early architectural decisions about the big systolic array, big big matrix multiplication, hence the name Matx, um and also the right memory choice. You're talking now about like um mixture of experts and how you can have uh you know, different like parallelism and uh some of that is is you have to actually tune those memory choices correctly, um which I think would be sort of like IP in a differentiator for you uh having already sort of figured that out as compared to someone who's like, "Oh, this is a good idea. Uh weights in SRAM and HBM.

Let me go do the same thing. " And I hear you saying like, "Well, you know, we've we've worked through all this. " But it when I'm reflecting back in 2022 like I'm not sure mixture of experts was even out yet. So, like how much are you reading papers every day as stuff was happening in 2022, 2023, 2024 and saying, "Oh, do we need to tweak the architecture?

"

Yeah, so I mean we've been reading papers since like 2017.

[laughter]

Uh yeah.

of course. Yes.

Uh yeah, I mean the I think the big and disappointing inflection point in 22 was when Google stopped publishing. Google, I mean, we were talking about how like Google is where all the researchers came from. A big part was they they I mean, had an incredible team in Google Brain and uh they were publishing so much. Uh everything all of the good work they did they published.

Um very vibrant place to be. Um they stopped doing that in 22. Um uh because of like seeing the competitive market playing out. Um and so like you could just get all of the trendlines of where the best models are going until then and then that stopped.

Um it's like a pretty good imitation of that started again with DeepSeek publishing, um but the like it's it's sad the volume of that has has not been so large.

Totally. So, I I will admit I haven't read all of your papers on your website, but I see that you guys do some publishing still. How How are you thinking about that fine line of what to publish and what to not? Cuz obviously for talent, it is to your point, it is exciting to get to publish to the world and share what you're thinking about.

Yeah, I I think the ability to publish neural net papers is a differentiator for us in terms of hiring. Um it's uh So, we have two different areas of neural net research in our company. We're a small company, especially our ML team is very small because, you know, uh that is part of what we do, but it is not the main thing we do. We're not selling ML, we're selling chips.

But, the the agenda of our ML team is twofold. It is attention uh uh research and specifically focusing on um memory bandwidth efficient attention. And so, that is something that is quite aligned to to where we see the future of hardware being. Um and then the other one is numerics.

Uh uh numerics is so has been the single best improvement in uh in chip performance over the last decade. Um and so, I think we have some of the best numerics um uh talent and and IP um here. And then in terms of what we publish, we we don't currently publish the numerics. Um that that goes into our chip and is fundamental to our chip.

We will probably publish it on a 1-year or 2-year delay after releasing the chip. Um but we we do publish all of the attention research we do.

Nice.

And so, uh that's because really what we're doing there is advocacy by saying um hey model designers, uh you should probably have these considerations in mind, especially when you think of future hardware that's going to be have a ton of flops, but is going to be somewhat more memory bandwidth constrained.

That makes sense. Yeah, so diving in there a little bit, so it sounds like you're obviously making hardware to sell at the end of the day, but you have ML researchers to research attention, memory bandwidth, efficient attention, and and also numerics. And obviously, that goes to inform your own architecture. So, this would be like extreme co-design.

Um but you're also trying to show model labs, like the end customers, kind of what's possible. How much if they are to adopt your chips, how much will that change how much these model labs have to think about how they train or how they do inference?

Yeah. We're We're trying to not go too far outside of the comfort zone. That's just like if you want product market fit, you have to mostly meet the customer where they are. The way to quantify that for us is you can look at the chip specs, and there are maybe five big most important ones, which is HBM bandwidth and capacity, matrix multiply throughput, SRAM bandwidth and capacity, interconnect performance.

And generally, we see that our attitude to to playing in this market is we want to be at least on par with the best competition, like Nvidia, on all of these, and then substantially ahead on at least a few of them. So, the substantially ahead for us is obviously the matrix multiply performance, also interconnect performance, and SRAM. But there is no place where we are substantially behind in in these big big considerations. Maybe in some sort of less LLM-relevant considerations, we're behind.

But in these big five, we're at least on par everywhere. And so, that is the thing that make means it is never a The opportunity cost of switching to Matics is is is never too large. But then the headroom you can get, like if you want to maximize the benefit, then you can tune your model. That means things like change the the the balance between the MLP layer and the attention, more MLP, less attention, or use some of our lower precision arithmetics.

We have a range of precisions. Uh to get the the biggest advantage is out.

Got you. So, it it sounds like you're saying you make sure that these like five most important areas, none of them are too weak to prevent a customer from switching or like, "Yeah, good. You You helped me on these fronts, but that one front is like so weak that I just can't convince myself to take the leap, but you're saying, "No, no, no, like we will be there on every front, but then also if you take a step further and optimize for our chips, like you actually can you'll have more headroom, you can do more."

Yeah, that's that's right.

Let me then use that to like segue into like who are those customers in broad strokes that are target customers for this chip system?

Yeah. The most interest has been from just the frontier labs, um which is I mean sort of as expected. Um the that is who we are designing for and the reason there uh why we're designing for them and why they're most interested is their spend is biggest, um and so that also means that the the economics of being willing to tolerate a new software stack is also uh biggest there, too. Um

[clears throat]

And and they also have this like longer-term vision of 3 5 years out, which is where you need to be when you're you're buying custom hardware. Um uh you know, you if you want to do really good co-design with your hardware provider, you need to be thinking on that time scale rather than just like I'll I'll buy what's on the shelf today. Um and so uh so so that's where we've seen uh strong interest. Um and this has shown up uh really across all of the workloads from training, uh reinforcement learning, and inference both pre-fill and decode.

Nice. Okay. Let Yes, let's let's talk about those workloads. So so let me reflect it back.

Your your customers obviously are going to be the frontier labs. They have the most compute spend. They are the most incentivized to squeeze as many flops as they can out of that, as much intelligence as they can out of that. They're thinking 3 to 5 years ahead.

They are incentivized to not only work with all their current partners, but to always be listening and see what else is out there. They have So market is telling us at the end of the day the defining workload of our time is LLM inference or you know, it's uh and therefore you can actually optimize around that around the transformer um around even splitting it into prefill and decode. We see that with Nvidia uh you know, and with Dynamo, I think everyone's getting used to that concept. Now, um that means the market narrative has gone from like GPUs for everything to like, oh actually at the rack scale, maybe it actually makes sense to have some SKUs that run prefill and some that run decode.

And this is their way of saying that those workloads, those kind of like sub workloads of the the broader inference, have different constraints and therefore like let's have hardware if it's memory bound, let's have the right hardware versus if if it's compute bound. But then I know you talked you had a great podcast that everyone should go listen to with John Collison on Cheeky Pint and and you talked to there about being competitive on kind of all those workloads on training, prefill, decode, RL. And it it kind of felt like going back to the days of like, oh a GPU can do everything. And so I wanted to hear your thoughts on like, how are you talking with these partners about their different workloads?

And how do you not like feel like a salesman just like, oh yeah, we can do that. We can do that. We can do that. Or or why can you do that?

Yeah, I mean, uh we just have to be like honest about uh what the strengths and weaknesses are. Um and so uh let's give that a shot here. Um our product has a really large amount of compute. Um traditionally uh training and inference prefill are the compute intensive uh workloads and then decode is the memory bandwidth intensive one.

And so then you might think, well, matter does a lot of compute. Why would we use that on a memory bandwidth intensive workload uh like decode? Um and and and there are the other side of what we've done, the the joint like uh hybrid SRAM HBM design uh turns out to be that is the place where that really shines. And so, uh the you spend none of your HBM bandwidth on loading weights.

All of All of that bandwidth is spent uh entirely on KB cache. Um so, you can get better use out of your HBM bandwidth than um than you can out of, for example, Nvidia. Um uh but you get the very low latency because the weights are stored in SRAM, you get the very low latency of Cerebras and Grok. Um and then sort of really digging into that, um there are some more things that you get from that memory system and and the overall rack and and pod system design as well, which is uh you this combination of low latency um and and and then the HBM gives you something a little bit unique.

Um you Low latency means small batch sizes. That's just like little law. The number of things in flight are are are smaller. The memory occupancy in HBM goes as batch size, is proportional to batch size, and so you can actually fit longer contexts in HBM than you could if the latency were larger.

And so, low latency is not just a like a usability win, but it actually improves your throughput as well. And so, uh it's This is sort of uh This is similar to what Nvidia is now doing with the the Grok and and Nvidia rack side by side. Um but there are some uh taxes you pay by them being in different packages. Putting Putting actually the whole thing in one package uh is sort of the first principles way to do that and gives you the most advantages.

Sure, that makes sense. So, you have a lot of compute. You also made the right memory choices. Therefore, you can do low latency, you can do high throughput, and actually there's even benefits in the small batch size low latency um with respect to how the HBM is used.

You talked about how Nvidia there has like essentially separate racks um of the Grok rack in their maybe say Vera Rubin. Um obviously, you're making one chip and there's benefits to both type of of workload. How are you guys thinking about like rack scale, interconnect, scale up, scale out? Like to the extent that you're willing to to share, like you know, what are you guys doing there?

Yeah. Um so, we we have a lot of interconnect in the product. Um uh I I think it is the most of any in our product um in fact. Um And uh the I mean, the first thing what is the reason for that is just so you can support um uh mixture of expert models with small experts um in a way that without becoming communication limited.

So, so very sparse mixture of expert models are uh the things that primarily drive the interconnect requirements. Um and we deploy um very large-scale up domains as well as then also supporting scale out. Um the it's so sizing of your scale up domain is really driven by um the sparsity and the kind of mixture of mixture of expert layers you want to support. You want to uh as much as possible do the mixture of expert routing within your scale up domain.

That is how everyone does it. Um and so, bigger scale up domains allow bigger mixture of expert layers. Um So, um and then on topology, we we do some interesting things with network topology. Um I won't sort of go into huge specifics, but I sort of contrasting what what is in the market um uh you know, Nvidia has done um some things like uh where they route everything through the NV switches.

That's an interesting idea. Um Google has these uh torus topologies. Um if you think about what you really really want for mixture of expert layers, you can um you can design something very custom for that.

I see. Nice. That that again aligns with the idea of you're designing not just the chip, but the whole system for these specific workload even to the point of network tip topology. That makes a lot of sense.

Um so, okay. So, then tell me like how many people, even if it's hand-wavy, do you have it Maddix? And we're talking about networking, we're talking about ML, we're talking about hardware, um probably you even have to think about like cooling and and operations and all sorts of stuff because it's data center design really. So, like tell me more about the company and it must be like very sort of cross-functional and what what's it like there?

Yeah, so I mean it's uh for a uh product like this it's a relatively small team actually. It's it's it's it's over 100 people. Um but you know, some of these projects like a video has 10 10,000 or 20,000 people. Um uh most of the team is is hardware, which includes the like the the core chip itself.

Um the logic design, design verification, physical design, and so on. Um and then we design the rack in connection with the partner as well. So, we have and folks who are even looking at like what is the insertion force of of a rack or um or or of a of a board into a rack. Um uh cable density, power delivery, um thermals, and so on.

That's sort of going down the stack. And then going up the stack, uh we have a really strong software team. Um they are writing the uh the software stack that can run LLMs on our chip. Um and then we we have also this ML team who are um doing exactly the research agendas I described.

So, very very cross um cross-disciplinary. Um I think super fun place to work as well because you can um you know, in one day you'll you'll have a conversation about like physical insertion forces and then at the same time functional programming or or um uh um uh SAT SAT solvers for for compilers and so on.

Nice. Interesting. So interesting. Sounds fun.

So, I'm I'm thinking about your very sort of interdisciplinary team, everything that you're trying to build in your first system, and at the same time the world is just constantly changing. We've got agentic AI, we've got cloud code, open claw, um a and maybe an explosion of inference tokens that are needed. We've got, of course, Opus is awesome, but it's expensive. And then all of a sudden Mythos has come out, and I'm just wondering, as a chip designer, but with ML researchers, like, how are you guys staying on top of all this, and are are things changing that make you think, "Oh man, in the next version of our chip, we should do things differently?

" Or are you just seeing it play out and feeling like pretty confident like, "Oh man, we can help this problem of awesome but expensive inference? "

Yeah, I mean, so so like halfway through your question, I was like, is this going to be about how do we use a generative AI versus how do we serve it serve it, which are both interesting, but um, how do we serve it? Uh, there is this ongoing trend that, I mean, what has always been the case is you you see the incredibly fast pace of change in um, models, how people are using them, how they're training them. But then you when you filter that through the lens of what does what does that mean for the hardware? It's almost all noise.

Like 95% is noise. And so, the rate of change for what you need in hardware is much much much slower. So, uh, as that applies to a generative AI, um, the what is it doing? It's still doing decode.

It's still doing prefill and decode. Um, the some things that are different are it's sort of increased the demand for that. And so, like especially when the agent goes off and thinks for a long time, and the users like sitting there and waiting, um, you would like them to maybe instead of wait for 5 minutes, can they wait for uh, 30 seconds or something like that. And so, there is some sense in which just the demand of performance has gotten higher.

Um, that's sort of within expectations. Performance like demand is always going to get higher. That's a great place to be. That's the uh, I think one place where it's um, is sort of a difference is I mean, all of this is just about sizing, but like sizing exercises are what we do every day.

And so, one example would be um how long does the model sit idle while it's waiting for a response from an outside uh something? And so, that that question has an answer when in a chatbot context, you're uh the model has responded to you, and then you as a human are thinking, and maybe you're going to type another message, maybe you never do, maybe you leave. Um and and maybe that's on the order of like 30 seconds or a minute or something like that. Um and so, the the the context for the model has to be kept in a memory somewhere during that time.

Um and then you have to size that memory and say, "How big should that memory be? " Um that is a thing that has changed uh meaningfully in in in a agentic context, where now actually mostly the model is waiting for tool calls uh to to run a compiler, do a web search, uh uh check your email, and so on. Um and so, the time the times for those are very different. Checking your email can run in seconds rather than waiting for a human to do some thinking time.

Um and so, the memories in service of that end up being smaller, but then there are things like long-running jobs like uh running a compiler or running a like place and route tool, which can take hours. Um and so, I think that's actually the biggest place it's shown up is that there is this there is now some increasing demand for um uh like storage systems for when the KB cache isn't actively being used, but it is waiting for a response from an outside uh uh uh HTP.

Yeah, interesting. So, now also tell me, how are you guys using HNTKI?

Yeah, um most of chip design is is actually in practice software development. And so, like the the way you express a chip is you write Verilog, which is it is a programming language, it is an an an unusual programming language, which is massively parallel, but it is it is a programming language. And uh and so, um can you write that there? Um so, one of the things we look at is uh the places where the AI's are most effective is when there is a a well-defined objective function that they're optimizing against.

Does this compile? Is the area good? Is the power good? Does how many tests does it pass going to maximize the number of tests that test the pass?

And so, uh we look at our processes and say, "Can we do development in a way that that does does more of that? Puts it in that regime where which is really the sweet spot for for AI development. " The other thing we do is we, you know, in addition to Verilog, we use other languages. There's some traditional ones or like well popular ones like Rust and Python.

There are also some less popular ones like in our case we we really like using Bluespec. It's a it's a hardware description language that is comes from from functional programming. Uh And so, we are also doing things to look into how can we make like make sure that that the AI's are really good at Bluespec even though it's a more of a niche language.

Cool. Interesting. Yes, I've never heard of it. So, then is that something that you think about as like a competitive advantage or just generally like, "Hey, we want to make AI models better at Bluespec and share this with the world?"

Yeah, um there are so few Bluespec programmers in the world that we we just want to hire all of them and then that becomes a competitive advantage.

I love that. Um okay, since you're the CEO, I'm going to go back to talking to customers, route to market, that kind of thing. On the one hand, it's kind of nice cuz it's hey, maybe there's only five or six customers that would be a great anchor customer. On the other hand, like probably everyone in the space is wanting to talk with them and work with them.

What does that look like to say, "We're a startup. Trust us. We're building this thing. It's going to be awesome.

" Like how like how do you have those conversations to see risk, their concerns, and ultimately, how will they end up like buying your first chip or your road map of chips?

Yeah, I mean that that trust us goes, you know, as far as as as your word goes, right? Not very far. Um the So, you need to prove it. Um So, uh for us, proof means like a lot of detail on on the artifacts we have.

Uh What is our the core architecture? What are the very specific details inside the chip? How do we organize the chip into um like we call talk about this little bit systolic array. These are the different compute units inside the chip.

How do they connect to each other? Um What is the instruction set? Um uh What is the software SDK that we share with customers? And so, we give all of this information actually to customers under NDA.

Um uh It is a lot It is uncomfortable for us to give that information, but um but it it, you know, uh it it goes a long way to prove towards proving credibility.

Yeah, that makes a lot of sense. So, as far as the software, like what is the level of effort that they will have to commit to when they say, "Oh, here's yet another vendor. Um We're very excited about everything they've told us. We totally believe them. They like open kimono. They told us everything. Um But, there's probably still some level of effort to port. Like Yeah, sure.

Yeah, um I mean, if you look at the the top sizes of teams that are supporting each of these multiple platforms that that that are on, it's on the order of like 50 to 100 people per platform. Um uh really good people doing kernel development, uh maybe even building compilers, building debugging tools, and so on. Um And so, I think that that's the ballpark of what uh folks are expecting on on our platform as well. We um we want to help.

And so, we'll we'll do as much as we can to to do that work for you rather than than than you needing it to staff it all of yourself. But, I think ultimately um a frontier lab wants to protect its own IP. Um that is especially the model architecture. Um and so, uh the the the last mile of kernel development is always going to remain in the in in the frontier lab so that they can they can know specifically what they're doing rather than than giving it to us.

Um I think the first miles of uh giving a strong compiler and debugging infrastructure and so on is something we can actually do for for you though.

One or two last questions. What is the biggest skepticism that you hear from people

Yeah, um I mean one of the things we're focusing on over the next few years is uh how can we as a startup that is relatively new manufacture in massive volume? And I mean it's it's a really exciting opportunity, right? Like the volumes that people buy are uh the projections for like data centers over the next few years are in the many gigawatts, tens of gigawatts. I don't know when we're going to hit 100 gigawatts.

Um and so Nvidia chips sell for about 15 or 20 billion dollars a gigawatt. Uh you multiply that by 10 or 100, it's a really large um uh commitment. Um And so like the the opportunity is really large, but being able to get very quickly to selling such a large volume uh it it is also like a substantial challenge, which is um some big parts of that are ahead of us. So I I think that's a really exciting thing for us to do over the next year or year and a half.

Yeah, yeah, that's a good point. It's not just about building the system, but it's about can you scale it? Can you production ramp it? Can you get to, you know, huge deployments that people are comfortable with, that work, that are reliable, and so on. Okay, so then last question yeah, give give me like a hiring plug. You know, you guys are 100 some people, it's very interdisciplinary, but you know, why should people come work with you?

Yeah, I mean ultimately you have to to to uh to believe in in the product vision, and I I think we just have the best product in the market. Um like it's designed from first principles for uh for the best like for for what LLMs really need. Um and keeping in mind like years of uh know-how and techniques of like what is the right way to map uh and and what are creative ways to to map applications to hardware. So, um so that's sort of like the company vision, um but the way we operate, um it's a very friendly um and like high trust team with a ton of incredibly smart people.

And I think that's sort of the the day-to-day of why it's a really exciting place to be.

Sure. Yes, A+ people enjoy working with A+ people. Awesome. Okay, Reinier, this was great. I learned a lot. Uh thank you for for the time. I'll be fascinated to check in over time and see how things are going with you.

Yeah, thanks Austin. It was It was really fun.
