---
source: https://www.youtube.com/watch?v=UfaIU6h0YdY
title: Quick Takes: Nvidia GTC Keynote
date: 2026-03-17
kind: transcript
note: 유튜브 자막에서 옮긴 전사. 화자 바뀜(>>)마다 한 줄. 600자 넘는 발언은 문장 넷씩 더 쪼갰다.
---

It's a honking big PCB. Like I've never seen a PCB this big. Like usually PCBs are something you can hold in your hand. This thing requires like two people to lift this PCB, okay?

And from what I've seen, this midplane PCB has like 52 layers and is like a work of engineering, to be honest, to even manufacture a board this complex, you know, is fantastic. And so what this does is Welcome to another Semi Dope podcast. I'm Austin Lyons from Chip Strat and with me is Vic's Newsletter. So if you're wondering, why does it look like Austin's in a hotel room with a crappy webcam and terrible audio?

That's because I'm in a hotel room with a crappy webcam and terrible audio coming at you live from San Jose outside of Nvidia's GTC. I'm not too far from the SAP Center where they had the keynote today and also the conference center where they'll be having a lot of stuff tomorrow. Um but I will say, Vic, I missed the keynote so I had to stream it from the plane because we had some weather in Iowa and my flight got canceled yesterday. So Vic and I wanted to come to you people and listeners and give you a keynote debrief and sort of digest what we learned together and we wanted to get you it to you ASAP, sort of like an emergency podcast and that's why it is 8 50 p.

m. Pacific time here so it feels like 10:50 p. m. which is past my bedtime.

But uh Vic, how are you doing over there? I'm pretty good. You know, usually we record this podcast like your morning time, my evening time. And so I'm kind of used to doing it late at night, but like after you've traveled like all over the place with delays and all of that stuff and then landing up and meeting with all the other analysts and all these things and now you have to record a podcast.

So yeah, I feel for you. It's far worse than what I usually go through.

[laughter]

Yeah, totally. So yeah, for listeners, we had a blizzard in Iowa. It came through Sunday afternoons so they canceled my flight. And then it got colder and colder and the wind was blowing overnight and so this morning everything kept getting pushed back.

I think when I left Iowa it was 7° Fahrenheit feels like -17 and then when I I went I went down to Dallas and then I went over to San Francisco and in San Francisco it was like 78° Fahrenheit when I landed. So I was like, "Uh-oh, the feels like temperature is like a diff- it's like a difference of 100° Fahrenheit from when I left when I arrived. You know, remember I was joking on the next comment on your your tweet basically like how you were like you're like basically one of those frozen shrimp that you take from the freezer and you put in the microwave to thaw it out but you end up cooking it. So that's that's basically Austin today.

Yes. Exactly, exactly. So yeah, I landed, came down to hotel and then there's I'm an analyst so I got to go to the analyst relations dinner and there were some Nvidia folks there. Ian Buck was there.

Gilad, the head of the networking business was there and a couple of other folks. So that was cool to get to mingle with people quick. Had some good California wine. Now I'm plugged in, got some decaf and Vic and I are going to unpack the the keynote with you.

Okay, let's do it. He said so much stuff like you know, two and a half hours so I kind of my time I got up early in the morning and like I was like on Jensen's keynote before I even brushed. So I've been listening to it like the whole thing immediately because yeah, I was asleep when he actually did the thing. So yeah, he said a whole lot of stuff but I'm wondering if it's really worth like two and a half hours of talking.

Now he had all these like like science fiction videos of cool stuff. I know it's nice to see when you're in there probably, but you know, I skipped past a lot of science fiction videos. Yeah, so you know, I have an interesting take here which is when I was talking to analyst relations team, they were saying like

[snorts]

because Nvidia is so big and they have so many businesses, you know, autonomy, telco, data center, client, gaming that they're trying to be respectful of all their customers and they want to like talk to each of them. But on the other hand, they're like one of the world's biggest companies and therefore even in three hours they can't talk about everyone. And so I thought it was interesting, you know, for example the keynote opened up talking like very early on about gaming and it was it was like a it was like a really cool demo of showing their like how they use generative AI to to make their like gaming better and then they talked about it for like a minute and then that was that. But you know, it's probably more than they talked about it at CES so I think it was like a nod to the gamers like, "Hey, we got you covered.

" Yeah, so on our podcast too, you know, we we do care about cons- consumer stuff once in a while. And I think this was cool because of all the videos that I saw that Jensen was playing, I think I liked this the most because it don't know they showed this like before or after that deep learning super sampling technology which is like DLSS.

Yes.

Yeah, which is like an AI-powered suite that you know, mixes that deep

was really good, too. It was awesome, yeah. I think anybody watching this should at least see the it's the first part of the keynote so you can see like how, you know, you have this typical video game characters, you can always tell they're video game-ish. But what ends up happening after DLSS is like awesome.

It's just like a real person playing these games. It's amazing. Yes. I literally want to go buy a like a gaming, you know, card if it's not a million dollars because of like memory problems.

Memory. Actually play some games. Totally. Yeah.

Yeah, it went from like kind of blocky faces to just very realistic and like stubble on people's chin and stuff. Like Yeah, you got like strands of gray hair like we do. It's awesome. Yeah, totally.

Totally. So now then Jensen quickly went past consumer GPUs and ultimately this was a data center conversation and what I liked how he teed up the framing I liked the framing and the business case talk. So let's start with that. You know, I think Jensen did a really good job of reminding people that there's been sort of like three big sort of step change eras with generative AI.

At first it was like the training and post-training area era where it was like, "Whoa, GPT-3, GPT-3.5, like this is amazing. This is the thing. It's a chatbot. " But people were still concerned about hallucinations and whatever so it was like, "Ah, this is a cool party trick but you can't trust it.

" And then of course in like and that was like late 2022. In 2024, late 2024, the 01 model came out and now of a sudden you could reason and that of course helped solve the hallucinations problem. And then we started to get into test time compute scaling where it was like, "Dude, if this thing can think, just let it think for longer inference time and you'll get a better you'll get better intelligence. So you could start to see we're shifting from the training era where everyone needed Nvidia GPUs for training to inference to like even more inference cuz now of a sudden it's going to have real demand because it's trustworthy and it's going to have maybe 10x the tokens because you're going to have it think for longer to make sure it's right.

And then Jensen was pointing out like we've now entered honestly truly in in 2026 um like late December 2025 into 2026, this third sort of era which is the agentic AI era. So think like Claude code and as we've talked about things like open claw. And again, it's like another 10x um you know, another order of magnitude in need of tokens because all of a sudden it's not humans talking to a chatbot, it's a it's humans talking to AI and then AI spawning all this other compute, tool calling, CPUs, you need long context, you need lots of storage. And and actually Ben Thompson even wrote a great Stratechery article this morning, I think is when he published it, saying like, "Hey, I used to think this was a bubble and now I'm actually not so sure it's a bubble because with agentic AI it feels truly useful and it truly feels like we're going to need all the compute, not just GPUs, but CPUs.

" And so I think Jensen was sort of taking the same similar framing and just saying like, "Guys, you have to believe us. We're in a new era and we it's not that AI was a party trick, but it's but especially with open claw like you're seeing the world is changing. " So let me let me pause there. Like what did you think of that framing?

Did you think it was on? Does it resonate with your experience? Yeah, I mean this is this is why and I wrote that article about CPUs and the agentic AI boom and all that. It is a real need for inferencing now and what Jensen pointed out is that inferencing is what will generate revenue and this is why people, you know, AI has become a true revenue generator only because of inference.

All this time like people are deploying GPUs for training and all of that. And with the inference problem, people initially thought, you know, inference is an afterthought. But what Jensen said was inference is an incredibly hard problem because of the kinds of spaces it has to address. You need low low latency, you need high throughput.

It is a big problem and you need long context and you have to work with so many different tools and it has so many different use cases and it has to work on so many different kinds of hardware. So it's it's actually an incredibly difficult problem that now we are really deploying and he calls it the agentic AI inference inflection. And so yeah, we are here right now. Yeah, totally.

And okay, so what I liked also about the framing and you made the point starting to call out where he talked Jensen talked about these different tiers. The The question is like as you're inferencing and you've got the Pareto curve of throughput on the Y axis. So, you know, how many tokens can you generate at a time versus token speed or interactivity on the X axis and this is a iso power. Um and we very early on, you know, uh these sort of AI supercomputers, first we were in the training area so the talk was about like, "Hey, Nvidia has scale up and scale out networking and you can have huge clusters and you can train faster.

" Then as it started to shift into inference, there was this simple Pareto curve and it's just like, "Hey, no matter what you're optimizing for, we we own the frontier. So, if you want the most efficient frontier, it you it's the cheapest or the most efficient to use Nvidia as, you know, that's that where the Pareto frontier everyone else is behind us. " Now, and what I really appreciated about Nvidia is acknowledging that there's really one workload that matters at scale. 60% of the customers are CSPs hyperscalers that are serving AI labs and it's transformer-based LLM inference at scale.

And but but as we've seen over the last 3 months, it's not just about throughput or about like tokens per dollar because um yes, there are some use cases where you're like, "Oh, okay, I'm fine with a 70B model that's good enough and I just want it as cheap as possible. " But then there's also use cases where you're like, "No, no, no. I want um Opus 4.5 or 4.6. And so I want the the biggest model.

And oh by the way, or I want the fastest model. " And then especially with coding, you're kind of like, "Actually, I want the biggest model and the fastest model. " And so Jensen and Nvidia started to break down that Pareto curve and they introduced this concept of tiers of like, "Oh, hey, maybe you have a free tier and it's very high throughput, very low speed. " Like Qwen 3 was the example they gave.

It's, you know, a decent size model. You've got a very small context length and you actually just give it away for free because it's like responds to those simple questions for those simple use cases. And this is just like top of the funnel, get you new customers, get them hooked because it's some free inference. Um but then you want to introduce tiers beyond that where it's like a little bit larger model, it's a little bit faster, it's a little bit longer context length.

So, maybe you have like a medium tier where now you're charging $3 um per million tokens. And then maybe you uh have a uh like a high and a premium tier which he he would said that, you know, Hopper could maybe only serve like those lower tiers and then um Grace Blackwell unlocked these like higher tiers where you could have an even because of because of the um HBM capacity uh and the especially with the NVL2 72 scale up, now all of a sudden you could legitimately do inference and and do like really big models and have them fast and have like a pretty long context length. And then, you know, finally he he transitioned this very nicely when they introduced Grok which we'll get to, which is to say, "Well, what if um 400 tokens per second is not fast enough and you actually want to unlock a thousand tokens per second or longer. " And so, I'll pause there.

I'll get your reactions, but I I just want to say like what I liked was this was an implicit acknowledgement of like, "We're past just GPUs are great for training and GPUs are perfect for inference kind of one-size-fits-all to acknowledging like there are different use cases, there's different user demands um from intelligence, context, speed, and there's therefore we are going to start optimizing our system so that you can hit different points. And as we'll get into, he talked about like maybe you need Grok to unlock some of those certain user experiences. " Yeah, so I have a couple of things I can say about this. So, first thing is like I like the free tier, you know, the way he described it, you know, everybody uses it, you get a Qwen 3 model or whatever at almost zero cost.

This is great because this is like something I can get my mom to use. Like, just use a you know, just don't Google anything. Can you just like use an LLM to get your answer? And it provides a good enough answer.

You know, she's not going to be like, "Oh, go off and launch some coding you know, task with some database queries. " You know, she's impossible. Like she just wants to know like, you know, basically some kind of a travel plan that she's planning to go next month or whatever. So, perfect tier for that.

I mean, it's going to solve like you know, it's going to rewrite the basic use case tier for everybody in the world. And everybody should be using this for at least basic queries if you're not already. So, that out of the way, I think then we can go to the extreme end of Grok. Which is what I've been saying to many people who asked me about this is that Grok is a like you said an ultra premium tier.

Okay, it's ultra premium because it is not that everybody needs this. There are only a few people who need it. And I think Meta initially said that they would like this to be like 10% of the inference needs. In Jensen's talk, he actually said like maybe 25% would be this kind of Grok thing.

Okay, so yeah, you got some delta of numbers here, but we can say like bracket it, you know, 10 to 25%. That's all about That's all the ultra fast inferencing will need. And maybe it's the uh you know, enterprise that you know, needs this because for them time means money and they are willing to pay for the ultra premium tier. And that will accordingly cost a ultra premium token cost which they are willing to pay because their ROI is significantly different from somebody like my mom who's just trying to plan a trip.

She does not need Grok. So, between these two use cases and everything in between, you still have a massive need for HBM. It's not going anywhere. Like I've had some investors asking me like, "What happened to HBM?

Like is Grok going to take over the need for HBM? Is the memory pressure going to ease off of HBM? " I don't think so at all because for majority of the use cases, this is not the technology that will be most useful. And this by me By that I mean the SRAM based thing.

So, it addresses a particular market where you like you say, "What if 4,000 tokens per second per user isn't enough? What if you want 1,000? What if you want 10,000? " You know?

So, those are the kinds of questions that like the agentic AI world brings to the table. But uh there still for a majority of use cases I think the uh HBM based inferencing systems are here to stay. So, all of that Vera Rubin GPUs, they're not going anywhere. And whatever else anybody else is developing based on HBM systems, those are all still going to be needed.

So, that's where I think Yes. This chart was really useful in setting the stage on what kind of inferences useful where. Totally. Totally agree.

And And uh so should we dive more into like the full Vera Rubin system and and talk about all the components including Grok? Yeah, let's do that. I think the what this GTC introduced was the seventh chip. Uh like the last conference uh CES was actually like the sixth chips that he showed.

uh LP30 chip uh that is now part of a rack unit. So, you can basically slot on slot in this compute tray with uh eight Grok chips I believe uh into one rack unit and you can build a rack of uh Grok chips. Which is which is pretty sweet. And I was closely looking at the picture of that tray actually even has like a CPU and like four DRAM sticks.

That's interesting. So, it's not just like the you There is a CPU on that tray. No, so yeah, speaking of that, so I'm going to pull it up on my side and look at it. Uh I don't have the I don't have the screenshot right in front of me, but yes, there's the Grok chips, there's a CPU, there's callout of an FPGA which I thought was interesting and I was like, "I wonder what the FPGA is used for.

" Would love to know more. Um but I saw Patrick Kennedy from ServeTheHome has a bunch has a really good YouTube channel. He had tweeted like, "Hey, that looks a lot like an Intel CPU. " And people were like, "What How do you know?

Like they never said anything about Intel CPU. " And he's like, "No, I guarantee you it's a Yes, they didn't say anything, but I guarantee it's an Intel Xeon because I've just dealt with a lot of CPUs and it looks a lot like a Intel Xeon CPU the way that they uh have a heat sink on it and the way that they like kind of physically attach it in. And actually down at this dinner that I went to right before, he was down there. And so I I was asking him about it and he's like, "Yeah, man, I don't know what it is, but just based on experience, it looks like an Intel CPU.

" So, for all the Intel bulls out there, maybe maybe the Grok rack is going to sell some extra Intel CPUs. But it's pro I I don't remember which version of Xeon he said. It's probably an older version that maybe they don't have enough supply anyway cuz Intel has some supply issues with their older CPUs. So, we'll see how this all shakes out.

it'd be funny if it is actually Intel because then I'm like, "Didn't you just say that like CPUs are all the rage? " And you know, even Jensen said, "Oh, I don't think I didn't think CPUs are going to be such a big deal, but they are. " And so, he's introduced basically this CPU rack compute rack which like has I don't know how many CPUs. Four CPUs?

Two CPUs? I can't remember. Uh But yeah, there is now a target of two. Eight CPUs to a tray.

Yeah, in a tray. Maybe in a tray. I don't know. Someone had a great picture a great tweet and it was like cuz it I think it was like eight CPUs and just a ton of memory.

It's just like all memory. And then someone's like, "Oh, I see why memory is so expensive right now. "

Okay. Yeah, so what are the how many of the CPUs are to a tray? Basically now, you can get these like CPU trays, computer trays, uh that are based on Vera systems, and you can build a rack of CPU. It's nothing new.

I mean, we've had racks of CPUs for years. But now, the fact that you need a rack of CPUs tells you something about CPU demand. Totally. So, yes, for people I don't know if everyone has seen the the keynote end to end, but basically now, the Vera Rubin system is actually a full data center, and it has Yes, it has GPU racks where each GPU tray has GPUs and a head node CPU, but it also has a CPU rack, or maybe multiple, I can't remember, of just Vera CPUs, and that is for the Agentech AI and orchestration processing.

The head node's all about like feeding the GPU and keeping it fed. But all of that tool calling and everything, you want it to happen on CPUs, but you don't want to reach out to a different data center or to the other end of the data center. You still want that CPU rack as close as possible. So, Nvidia introduced the Vera CPU rack, and I had some quotes from Jensen.

He said it's extremely high single-threaded performance, incredibly good at data processing, extreme energy efficiency. He said, "It's the only data center CPU in the world that uses LPDDR5, which is like mobile memory. So, therefore, the performance per watt is unrivaled. " He made sure to say it's in production.

And then, to your point, Dick, um he said, "We never thought we'd be selling CPUs stand-alone. We are selling a lot of CPUs stand-alone. This is going to be a multi-billion dollar business for us. " And for reference, you know, I think Nvidia or uh AMD and Intel do something in the order of like tens of billions of dollars a year in CPU revenue.

So, to say you're going to do multi-billion is not too shabby. Yeah, and I know he likes to play up the Vera thing, but it has good single-threaded performance, but its Olympus cores are like there are 88 cores, and they have the equivalent of multi-threading. I forgot what their their it's marketing term for it is. But yeah, basically it has like 176 threads.

Uh I mean, you compare that to AMD's Venice uh dense that is due, I think, later this year. Uh it's it has like 512 threads and like extremely good single core performance. I mean, so there are some really competitive uh CPUs out there. And I like had like a CPU um yellow pages that I created that I compared various data center CPUs according to various metrics, uh including memory.

So, if he's saying like LPDDR5 is the thing that is unique, I'm going to go back to my yellow pages and compare it because I don't know why. It doesn't seem like it to me. I don't know. I feel like they have other things going on.

Yeah, totally. Yeah, you'll have to dig into it. And for for listeners like the number of cores, you could think of it as just having access to more agents per CPU that you could run in parallel.

Yeah, that's exactly it. Yeah, so maybe Vera system is not the greatest for like maximizing the number of agents, in my opinion. Uh if you need like one agent per one core or something, then you're just going to have to put in more CPUs. Uh yeah, but they're like good fast CPUs, so it's not Yeah, so they're they're drawing a fine line here between what kind of CPU is required versus not.

But uh yeah, I wrote in in my article, I I proposed that we might see a time where the number of CPUs might increase compared to the number of GPUs at the rack scale. And now, when you start adding CPU racks next to GPU racks, Yes. the question is how many CPU racks you need to you to add, and it depends on what kind of workload you want to run. So, there could be use cases where CPU excee- exceed GPUs in a rack scale system.

It's my theory, at least. Totally. Yeah, totally. Yeah, I know I know.

We should go count in his reference diagram like how many CPUs there were and get that updated CPU to GPU GPU ratio. Yeah, yeah, exactly.

Cuz it could get a lot closer to one to one. Definitely. So, um on the CPUs Yeah, exactly. Exactly.

Exactly. So, to Vera Rubin, the full data center system. So, now there's GPU racks, there's a Vera CPU rack. Um there's a if you want, you can get a Groq 3 LPX rack, which I honestly was a little confused cuz it you called it Groq 3 LPX at first, and I was just thinking like, "Ah, they've only got Groq 1, right?

Like just they've only had one chip. " Um it was, you know, some sort of like 14 or 16 nanometer chip. Um but and I think it was maybe fabricated at GlobalFoundries. But then, on this call, he talked about Groq 3, and there was a shout-out.

He's um Jensen said, "I want to thank Samsung, who manufactures the Groq LP3 chip for us. They are cranking out as hard as they can. I really appreciate you guys. We'll ship in second half, about Q3 time frame.

" I know that Groq had publicly stated they were working on a next version of chip, and that they were working with Samsung on that. I think maybe Samsung 4 nanometer, maybe.

Yeah. Uh don't quote me. Um so, this seems to be that next iteration. It but it was a little surprise that it wasn't just like Groq 2, but that's Groq 3.

I I don't know. Would love to hear more, but um Let Let me tell you some other quotes. I think on the Groq one, there was a picture where Jensen showed nicely, "Hey, we're going to do pre- Well, first he said, um hey, Groq has been attractive to me because uh you know, it's a deterministic data flow processor. It's statically compiled.

The compiler schedules it. The compiler figures everything out. Um the compute and data data, it's all there right at the same time, so you're not waiting on memory. Um there's no dynamic scheduling.

Therefore, you can just have SRAM, and the computation just flows through, and it's super low latency. And he said, you know, obviously this is designed just for inference, ultra-fast inference, um just one workload. But guess what? That workload is the workload of our era.

So, woohoo. Um they you know, they're they're good to go. But then, he did say, "But guess what? Groq only has a tiny amount of SRAM per chip.

So, the downside is it takes a lot of chips, and that has historically limited Groq. Oh, you want to run a 70B model? That'll be 576 chips, or you know, spread over whatever, 12 racks or something. " You're like, "Wow, that's pretty expensive to run a 70B model.

" But then, Jensen framed it as like, "We, Nvidia, with Dynamo, having that software layer to decouple prefill from decode, we essentially unlocked Groq to be the decode stand-in. If you recall, they had the Rubin CPX Q, but he didn't talk about that at all today. Now, it's Groq LPX as the stand-in. And so, he said, 'Guess what?

Now, all of a sudden, we have unlocked Groq, and it's okay if it takes a ton of Groq chips, so we'll just have a Groq server. ' And then, he had a nice picture that said, 'We'll do the prefill on Vera Rubin, tons of HBM. Um we'll also handle all the KV cache and do the uh attention mechanism part of the decode. And then, we'll just send over the activations to the Groq rack.

It'll do all the decode, um the feedforward network part that happens sequentially, because because that's bandwidth limited because but since Groq is all just SRAM, it's super high bandwidth, and then it'll spit out the tokens. And so, I kind of like how he both acknowledged why Groq had a shortcoming and couldn't really take off on its own, but then acknowledged how it fits in perfectly with what Nvidia was building, and so that's why, you know, they like And he's very specific. They never said they acquired Groq. It was like, "We licensed Groq's technology and acquired the team, essentially.

" Yeah.

Um but did you hear the piece about him The question is, how do they communicate? Um is it over NVLink or something? And he said Jensen said, um "The two systems work together tightly coupled today over Ethernet with a special mode that reduces latency by half. " And so, I thought it was interesting that it's over Ethernet, which feels still kind of like scale out.

So, the Although he said like it's Ethernet, I think that eventually it's going to become NVLink, or more specifically like NVLink Fusion, because the ability to use like the hardware maybe become important in the future. I don't know. Like if Nvidia wants to maintain compatibility with other platforms in the future, it could be useful that this is actually NVLink Fusion. We'll see.

Totally. Yes. Yes. Yes.

So, to that end, right? If it's NVLink Fusion, maybe you could plug in any hardware at the other end. It could be Groq's next versions. They They called So, it's LPX, but the first version, which was Groq 3 LPX, was also called LP30.

So, maybe the X is a stand-in for 30, LP30. And then, I think they teased an LP35 and an LP40. I don't know if I wrote that down. Um so, there's clearly more Groq chips coming.

Um but but presumably, it could be other accelerators, because Jensen did hammer home that they are fully vertically integrated, but they're also horizontally open. So, if you only want certain parts of their stack, you could do it. So, in theory, maybe you could do prefill with Nvidia, and you could do decode with something else. Yeah, maybe some other AI startup.

Or Or the other way around, you maybe you could do prefill with um Intel Crescent Island or something. Uh and then, you could do decode with Nvidia. Who knows? Yeah, yeah, yeah.

So, and maybe they want to have the optionality to swap out Intel CPUs in their CPU rack. I don't know. Yeah, it's interesting. You'll see how it goes.

And one of the thing other thing is like he declared that like spectrum CP spectrum networking is now in production and it uses CPU at scale. So, that's cool. Actually, like we have now I assigned that CPU is no longer the mythical beast that has been, you know, always threatening to come but never did. But now it's like I don't know, something is in production and it says CP you want it, right?

I mean, that has to count for something. To totally right. Okay, let's talk Yes, let's talk CPO. Let's talk scale out and scale up.

So, when Jensen first introduced CPO, he was very clear to say that it was for scale out. So, he right? I feel like he's very clear about that saying it's CPO but for scale out. Yeah.

It was yeah, it was scale out. Then he then he went on to talk about the whole optics versus copper debate. So, I'll let you continue. You have you have a good way of saying it.

Okay, for sure. But feel free to jump in. So, there was a road map slide where Jensen was showing their future like Oberon which he accidentally called Opturon at first Opturon at first but which was funny. But Oberon and he he was very specific about saying, you know, hey, there's a lot of talk about copper versus optical scale up and where is Nvidia going to land?

And he basically said we're going to do both. So, let me see if I don't Yeah, Kyber is going to have copper scale up. And then he said CPO scale up which I felt like maybe it was a slip of a tongue. But then he said

it's not actually. Here is how it works, right? Let I tell you what he was like talking about here. So, when you're talking about scale up, he brought out that NVLink cartridge spine, right?

That that heavy spine thing that he always shows. And he brought it out and like look at all the copper cable in this and I was thinking to myself, oh yeah, look at all the copper bulls now going out. Look at all that Jensen still holding up copper spines. That's good.

So, then he was like, okay, this is the what has been used to scale up the Oberon rack, the NVL72 and that's the copper that connects everything in the rack. And then he went on to like, hey, do you want to see Rubin Ultra, right? And then he comes up and then he's just like summons like like he's, you know, and the the thing appears from the ground and it's very dramatic. It's awesome.

Uh so, then the Rubin thing shows up and then Rubin Ultra shows up and he's like, look, this Rubin Ultra is not a rack that goes in horizontally, it goes in vertically, right? And we saw this in the Kyber rack pictures if you've ever seen it in the past. It goes in vertically. The reason it does that is because instead of the giant spine that connects stuff now, they have what is called a midplane PCB.

Okay, it's a honking big PCB like I've never seen a PCB this big. Like usually PCBs are something you can hold in your hand. This thing requires like two people to lift this PCB, okay? And from what I've seen this midplane PCB has like 52 layers and it's like a work of engineering to be honest to even manufacture a complexity a board this complex, you know, is fantastic.

And so, what this does is in the Kyber rack, this thing will plug into the midplane PCB. And think of it like instead of all that copper cable going up and down the rack, now the midplane PCB is like the burger patty where on one bun is basically the compute you know, whatever is planning into this side of it and the other side of it is like the back end network thing. So, it's like you know, you've got two buns like you've got computer networking and in the middle is this midplane PCB that hooks it up. So, you can run really fast copper interconnects because of this midplane PCB approach which is awesome.

So far, so good. We're still at copper, right? Now, both systems Oberon and Kyber can scale up to 576 GPU domain. How does it do that?

So, basically you can take NVL72 and put all these racks next to each other and connect them with optical links. And so, what that happens is now you have it's still scale up. Just because it does it's it's different racks doesn't mean it's scale out. It's still scale up because it's within the same pod.

But you have optical connections between all of them because you need the reach and the speed. And for the same thing in the Kyber rack, you have 144 GPUs to a single rack. And so, you can what they call a canister in that terminal. So, you can hook up four canisters together with optical links and get to the 576 domain.

So, the copper is both in the scale up, you know, and optics is scale out. So, that's how this whole thing is. It's very cool, actually.

Yes, yes. Now, that's good. Yes, exactly. The 576 specifically is is where you're right where he's saying, okay, within a canister, it's copper scale up.

But then between these canisters, it's optical scale up. But it's still scale up because it's all one domain. So, they're all like doing the remote memory access and thinking that they're all part of a system and they're sharing their HBM even though they're literally separate racks next to each other. Yeah, so this is why, you know, scale up has both copper and optics.

Yes, yes. And then still in that scenario, optical scale out as well. Yes, that is that is a thing, right? I mean, optical scale out is definitely the future.

Is here. The future is here. It's exactly, exactly, exactly. So, so, so then CPO still fits in the optical scale out there.

Co-packaged optics. I what I'm not sure of is that when you're connecting these canisters together in the Oberon or Kyber rack, is that a pluggable transceiver or is that CPO? Because he said that it's going to involve NVLink 6 to do connect between those canisters. And NVLink 6 does not have CPO cuz you need the switch hardware to have CPO if you were going to connect this thing with CPO.

So, it's going to be pluggable transceivers for now because I'm guessing it's not like that many connections as if it's like scale up like within a rack. That's a lot of cables. But within between canisters, maybe it isn't that many cables. I don't know.

I have to count the number of cables that will go between canisters and how many of them are optics and how many pluggable transceivers will be used there and what is the power consumption of each pluggable transceiver and when that will go to CPO. Because I know that people are going to listen to this are going to ask all these questions. I don't really know. Right, totally.

I'll I'll try to take out pictures and then and then you try to, you know, just reverse engineer it from like the power and, you know, thinking about it from first principles.

Yeah, it's a good exercise. Yeah. Totally. So, okay, back to Vera Rubin system.

So, you can have the CPU compute, you could have the Vera CPU rack. There's going to be some CPO switches. You could have the Grok rack. You could with the the different once you're on Kyber, you know, you could even like have a huge scale up domain.

The last thing that was mentioned was this STX rack with BlueField 4. I at first I was a little confused by that but my cuz he's talking about AI native storage and I was like, wait, I thought this was ICMS like that we've been talking about this like massive, you know, inference context memory storage server or whatever. But then I kind of left and you clarified for me but I kind of left thinking like, oh, maybe ICMS is an implementation of this STX rack. But how did you interpret it?

Yeah, I think that's what it is. Like I think you can put this STX racks in a separate STX trays in a separate rack and build out like an ICMS storage unit with DPUs in it and then put it next to all these compute racks, GPU racks, LPU racks, you know, networking racks and now you have a storage rack built with these STX. That's what I interpreted it as but he said very little about it. Yeah, it was just confusing that they like would change the name or abstract it or something.

Yeah, yeah, storage. I think the S stands for storage, right?

[laughter]

There you go. Totally. So, all right, what next? I feel like we hit on Vera Rubin pretty good.

Yeah, yeah. So, I think that's like the meat of what what ended up happening. What other like thing I took away from um the keynote here was that the Fineman CPU is going to be called Rosa for a Rosalind and we were discussing who this Rosalind is. Do you have a theory?

Well, I thought it was Rosalind Franklin, some sort of English chemist, X-ray crystallographer. Um I remember hearing her name having to do something with DNA and RNA. So, that's who I thought it is. But who who apparently according to Wikipedia, she died when she was 37 which is sad.

But what who did you who do you think Rosa is or Rosalind? I don't know. I've been I've been trying to find out but you know, I think we will let's go to Nvidia's company blog because I found you know, what That's the best source, right? Like they say something.

Yeah, for sure. Yeah, they actually say it. So, it's actually you are right. It is named for Rosalind Franklin for X-ray crystallography.

So, yeah, you win that, you know.

[laughter]

You win this round of Jeopardy. You're the Jeopardy champion. So, you were right. Yeah, that's what I would thought it was somebody else but uh I will take it from Nvidia's blog.

So, you're right. Thank you. Well, that's good to know that after Vera we have Rosa. So, um we have a name for the next CPU.

Kind of interested to see what's in there. Well, that's in the fine print uh architectures. Yeah, it'll be fascinating to hear what's architecturally different because now they'll be fully designing it for the agentic AI era. Yeah, I think the next thing that we should like briefly mention I think a couple of things like I just to wrap up this and now beyond this, you know, if we make this whole episode 2 and 1/2 hours people might have as well watch the GTC.

Why would they watch a fun? So, let's keep it

quick. Okay.

So, we have two more things like one is um their idea of DSX which is I would say a digital twin platform that is going to be useful for uh like future building of AI factories. Very broad concept but this is uh seems like something that they are uh introducing as a new platform for the digital twin universe. Yes. Yes, I thought this was super cool.

Like the way I felt uh Jensen positioned it was like, "Hey, all of a sudden we have to start to work with all these new companies as we're manufacturing data centers and how do we best work with them? Oh, we decided let's just create a simulation in Omniverse and we can just simulate the whole thing and essentially just co-design it together in Omniverse. Run all the tests, the thermals, the power grid load and everything and then we can all agree like, "Oh, yeah, this seems to be working in simulation. " and then we'll build it.

But but not only can you design and simulate it and and make sure you build it current to spec, but then it sounded like you can close the loop and when you're actually operating the real data center, you can feed the data back into your Omniverse simulations. You can have real data like from the grid, from whatever thermals you're measuring and stuff actually feed back into your simulation to help you like refine it and continue to iterate on it. I just thought this was pretty wild. It seems pretty wild, but I don't know like many times I've I've been to many like software tool presentations in my lifetime uh as part of a career right in this stuff.

And when I actually end up using the tool, when I see the demonstrations it's always like amazing like, "Wow, look at all oh co-optimization and the co-design. " But ultimately when you get to working with it you're like, "Oh, I guess this export doesn't work. That interface doesn't work. This doesn't.

" And then like there's so many bugs in this and that, but yeah, in theory it's a pretty good concept. I don't know. I want to talk to somebody who actually uses this platform. I want to get some, you know, if anybody has actually used this Omniverse, you know, let us know.

Like leave a comment or something like really I don't know how this digital twin emulation thing even works. On a data center scale it seems like you can simulate everything from like power to like GPU usage and to tokens and and then feed it all back and it sounds too amazing to me.

It's it is pretty meta to be like, "Yeah, you could simulate." I was like, "Okay, well, what model are you running on those GPUs?" You know, like are you going to

Yeah, yeah, it sounds a little bit like if only EDA tools were like that amazing. Uh yeah, I don't know. So, anyway, cool idea. Cool idea.

very bullish the future possibilities of simulation. I think there's a lot of real world manufacturers who make things and who could be iterating a lot faster by simulating, but they're actually just making the real thing and finding out it doesn't work and then iterating and making another real thing, you know. Um So, for example, wind tunnels with car design. It's like, "Oh, yeah, you could make a million dollar wind tunnel or you could just simulate it all and then like change the shape of the mirror and see what happens.

" And so, yes, anyone who's an expert in simulation, I'd love to learn more. So, hit us up for sure.

Yeah, so going down the software path, let's talk about the last one. And I want to mention something like I think Nvidia needs somebody who can make up acronyms properly. Like they don't think this stuff through. Okay, when they introduced their like lithography platform, they called it Coolito which I guess like a certain like Spanish speaking people in the audience told me it means little donkey or something like that. Seriously? Yes. That's hilarious. And now they're coming up with this Nemo claw open claw thing and calling it it agent as a service. Like what do you think that spells?

[laughter]

Like

[gasps]

really like think through the acronyms, okay, before yeah, anyway.

feel like Jensen even said something like a gas. They're they're going to move from SaaS to a gas. To a gas. No, no, no, agent as a service.

Anyway, uh we keep this like, you know, child friendly, you know, because I think a lot of people might want to play this with kids in the car, okay? So, yeah, they yeah, I think this open claw he showed a like a graph of GitHub stars uh for like Linux versus something else versus open claw. Open claw GitHub stars is like like a vertical line literally like it has a vertical line that uh Linux took 35 years to achieve the same number of GitHub stars or something like that.

Yes, well, to I will say to that end Linux existed before GitHub stars. It's kind of like how your favorite old bands aren't big on Spotify. You're like, "Yeah, cuz in the era in the '70s they weren't on Spotify, you know. " I completely agree.

But definitely obviously open claw definitely going vertical is really cool uh and for for for all the good reasons. And so, I thought this the Nemo claw thing was interesting. Um the idea I think, you know, I I actually loved it. Let's see if I wrote it down somewhere.

I don't know if I included it in my notes. Um but basically Jensen was like, "Yeah, uh yeah, open claw. It uh Where is it? He Let's see if I have this quote cuz it was so good.

He's like, "Oh, yeah, yeah, it can access sensitive information, it can execute code, and it can communicate externally. " All right, chew on that again as if you're an IT security person. It can access sensitive information, execute code, and communicate externally. So, obviously he said like obviously this possi- this can't possibly be allowed.

So, it sounds like Nvidia came in and helped their ver- their version, you know, I don't know if they just forked open claw, but then they tried to like patch it up and make it secure and give it guardrails and stuff like that so that it's like enterprise ready which I think it's pretty cool. Would love to learn more there because I I definitely think I like I've been doing a lot of agentic AI myself and it's all like internal software if you will. I'm just trying to like automate my life in my work um because there's so much like manual stuff that I do or things that I would love to do that I just can't, but if I can write throwaway software to do it for me, awesome. Let's do it.

But I'm definitely scared of the idea of open claw, you know, just having access to like my um iMessages and stuff like that, you know. Uh so so I I definitely can see the real this is like a real need. I know San Francisco people probably don't love to think about it, but like for enterprises this is like make or break. This is like Microsoft like right up their alley, you know, like enterprise stuff.

Yeah. You know, I have a I'm going to like say something that is not popular opinion uh and kind of contrary to what everybody believes in this software world because everybody's like, "Oh, this you can write throwaway software. Anybody can build these platforms. So, what's the use of SaaS and this and that?" But yeah, I buy it, but like I feel like sometimes the cost of building a tool like this in just in terms of token usage uh is actually outstrips what I can pay for a SaaS service. Yes.

Like I was trying to, you know, build a bunch of these news aggregator things, right? Like we read so much of the news and I wanted to have a method in which I could like parse it and collate all these sources and show it to me. And I built all this stuff like I made like Claude code do all this stuff and it writes into my Google Docs and I can just like come and look at it every morning and I know all the news. It's very cool, but then I had to upgrade to the like uh you know, the max plan because I used all these tokens and it's like it's $100 a month and I was paying all that stuff.

But then I was like looking at some, you know, services that do this and it's like Feedly Pro for example like has it's like I got it for like 100 bucks a year. And it does all this AI aggregating stuff and so, it's just like there is a marginal benefit of making tools yourself with these coding tools versus having a tool that I can pay for without a token cost. So, there is a cost to doing software tools yourself, you know.

Yeah, definitely there is a token cost, a financial cost, and there's obviously a time cost and an opportunity cost. You need to focus on what makes your beer taste better. And so, like writing your own news aggregator or your own CRM or your own back of house stuff, it's like are you really going to want to become an expert in that or you're just going to want to do what you do best, right? Yeah, exactly.

So, if there's something that doesn't exist for what you do because maybe it's a niche tool then or a niche area that you work in and there's no tooling for this, but you kind of know what the tooling flow that will help your work is because you are an expert in that domain, then it makes sense to go agent code yourself something up and it's a great productivity enhancer. But just like declaring like SaaS dead or something because of this is like a is like a weird stance to take because I don't think everybody can code up a Feedly or or a CRM like HubSpot or something like that.

do they want to commit people to maintaining it and adding features and stuff. But now what you need to do

Yes. So, what happened? So, I I worked at a company once uh a very large grocery retailer and they made all their own back of house stuff. They should have been running it just on like SAP or whatever for like inventory, pricing, all this stuff.

But they're like, "Oh, we have a couple bespoke features that are really important to us and because we operate as a business differently than other people and if we go use like SAP, they don't really support it out of the box. So, we'll just have to pay someone gobs of money to customize on top of SAP because we're just one customer, so SAP is not going to build this feature for one customer and at that point if we're going to have to build a bunch of software on top of SAP, why not just build our own software? Now, it came there's there's trade-offs which like okay, now you have to have teams of people for the rest of your company's existence to create this software which you could just be using SAP, but they they did have this like dilemma where it's like yeah, but we want these custom features and we're just one customer. Now, anyone like that can just go to SAP or whoever and say excuse me, I have these custom features and now SAP if they're using AI internally, they'll go cool, we'll just create that for you because yes, you're only one customer and that used to used to not be worth it cuz we'd have to pay a few engineers to build that, but you're only going to upgrade a little like pay in a little bit, but now we can just have one intern vibe code that essentially or whatever and now the cost of writing your custom features has come down.

So, we can customize this for you and so it's like win-win. The all the customers who could never get high enough priority on the product manager's backlog can now get the bespoke things they want and the the SAP or whoever the SAS company can have potentially more customers and serve of their needs because it's cheaper to write software. Yeah, so this is a net positive for the software world in a sense, right? Because we had this recent SAS SAS apocalypse or whatever like the SAS mageddon, but yeah, like if if this is the case and Jensen was also saying about how each company needs to have its agentic strategy in place like how are you going to deploy agents agents with the company?

I think that's a good point because like you were saying this is a security aspect and the second thing is like are you going to use it for like core development or are you going to use it for like uh bells and whistles products that can be quickly churned and satisfy one particular customer? Maybe they can even tear it as like a like a custom support package.

Exactly. Exactly. Exactly. More revenue.

Yes and I agree with you. I thought it was pretty profound to think through like oh yeah, every just like everyone needed like a web strategy or or whatever like now everyone needs to have an agentic strategy. Now, I will say the only like if I could give, you know, uh gentle feedback to Nvidia, the the framing around like um hey, this uh throughput versus interactivity chart defines your revenue going forward. Every CEO is going to think deeply about that.

I thought like yeah, that totally resonates for Dario and Anthropic when your business is selling inference as a service like selling your model as a service, but most businesses at the end of the day are not selling like tokens as a service where right? They're still selling tractors or groceries or uh hotel rooms or something or Starbucks like coffee, right? So, yes, I I definitely believe that every domain will be using AI as an input and they'll be transformed AI, but the whole like your business model will now be a reflection of how many tokens you can generate and therefore you need to think about that. It's like it's just not right.

It speaks to the 60% of their customers that are like hyperscalers and AI labs because if you listen to that Dario and Dwarkesh podcast, literally Dario said this where he's like yeah, I've got only so much money I can spend per year and I need to spend enough on R&D so that I can unlock like the future models and then I need to spend as much as possible on inference because if I don't spend enough on like cuz that's where I make money, right? The R&D stuff is just for next year and and and and he's literally like he'll make as much money as he has inference compute. If he has this much inference compute, he'll make this much money. If he only has this much inference compute and of course if he doesn't calculate it right, he could like not make enough money and that makes a ton of sense for a few customers, but for those other 40% that are just your enterprises, right?

Like they need to have a different message and talk to them and and frankly, I think and this is a conversation for another time. We've been now we're going on Jensen time. We're probably almost on the three hours at this point, but I need to hear more about local AI on-premise AI like um talk to me about why I want to buy an RTX 6000 Pro because I want to spend $5 million a year and just get as much inference as I possibly can. I don't want to spend $5 million and realize that I blew it all in the first month because Opus is expensive, right?

And so like maybe I do want to buy a rack or maybe I want to buy DGX stations like we talked about before. So, I'd love to hear more from Nvidia on the 40% of customers and how they're thinking about like CapEx versus OpEx and planning their budgets in in light of this AI is going to transform their business and and I maybe here last thing. Um I love this quote. Jensen said, "Hey, every engineer going forward is going to need a token budget.

They'll make a few hundred thousand dollars in base pay and then I'll give them another half of that on top as a token budget so they can be amplified 10x. It's now a recruiting tool in Silicon Valley. How many tokens come with my job because those tokens make them more productive. " I can relate to that because I use the $200 max plan on Anthropic cloud coding all the time and if like if that goes away, I would be like uh I'm going to a new job where I can have that, you know?

Um and and by the way, I'm making stuff that runs in AWS and it's using Anthropic's API and and in one fell swoop, all of a sudden I'll just use 50 bucks and I'll be like dude, you re-ran and reprocessed all my data. Come on. Crap, I need to put I need to put some guardrails around that cuz that was super expensive, but I can see like all of this stuff is making me more productive. Um but I will say on the other hand like okay, do people want a token budget that they're going to go blow with open AI or with Anthropic or or could you just say like hey, for every engineering team, we're going to buy you a rack or a DGX station or something and then you divvy it up and keep it as busy as you can, right?

Because maybe you can actually know exactly how much you're going to spend and get all the tokens you need out of that. Yeah, that is the way it's going to go because for one simple reason like if you're going to like I I've been reading all these people who are saying like oh that that that small team of people is like using $500 a day, $1,000 a day on token costs and it's amazing because they don't have to hire a person because you know, I mean that's $1,000 a day is a little, you know, a little much because you know, in $300,000 I guess you could hire another person, but only thing is like this AI agent doesn't sleep. So, it's kind of a benefit. Like that $300,000 employee needs to sleep and needs a little work-life balance.

Yeah, totally. This thing doesn't sleep, so it's a good bet I suppose. But then like ultimately, there is this becomes an operating expense. If you buy a DGX system and staff up your on-premise AI, that is going to be a depreciating capital asset and longer term makes much more sense as, you know, this is how you deploy it.

And this token budget is is not really a thing. It's going to become more like a like a tool usage, a license tool usage. Like you you buy so many licenses for your company and you scale up the licenses if you're using too many or you scale them down per year, right? So, the same way you would build up certain infrastructure.

If you need to add infrastructure to that and people are using more tokens, you'll add another DGX rack. That's how it's going to go. Nobody's going to negotiate like I'm going to get you 10,000 tokens per per day and this is how your job is signed up, you know? Nobody really knows how these tokens are even like do you know when you which job of yours is using more tokens versus less tokens like It's very yeah, it's very hard to see that.

You don't know that up front. Like I said, I'll accidentally burn $50 a token. I'll walk away from my desk, come back, refresh and be like oh crap, I had no idea, you know? Yeah, exactly.

So, I don't buy this. Just Jensen's theory on I I do I do believe in Silicon Valley, you know, but I think the rest of the world's going to think a lot differently. It's basically like, you know, go talk to a CFO somewhere on the East Coast or in the Midwest or in Europe or somewhere, you know, and they'll tell you like we're [laughter] thinking about this differently. Awesome.

We've come up on an hour. We did it. We didn't hit two and a half like Jensen. There you go.

All right, man. Time for me to go to sleep. This was good. People, if you listen this far, we'd love to hear your feedback.

Um thanks for listening to Semi-Doped. Go, you know, follow us on YouTube and comment, send us emails. Thank you for listening to Spotify, Apple Music, everywhere you find us. Thanks for checking us out on X and uh yeah, we're we're always here to hear what you want to know.

So, so send us requests for future podcasts. We'll catch you next time.
