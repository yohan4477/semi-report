---
source: https://www.youtube.com/watch?v=qD4Lk2Koabo
title: MicroLEDs Ain’t Dead, Micron Snags Vera Rubin
date: 2026-03-20
kind: transcript
note: 유튜브 자막에서 옮긴 전사. 화자 바뀜(>>)마다 한 줄. 600자 넘는 발언은 문장 넷씩 더 쪼갰다.
---

I'm like, Jensen, why are you signing on a memory wafer? We need that stuff. There's been a lot of noise about how Micron's out, it's not going to be on the Vera Rubin, and I was just I was like, oh look, uh Jensen must not have gotten the memo. He must not have gotten the memo that Micron is not designed in.

Hello listeners and welcome to another SemiAccurate podcast. I'm Austin Lines with Chip Strat and with me is Vik Shaker from Vik's newsletters. So, Vik, what's going on? What's up this week?

A lot of things, right? This was the GTC conference week and OFC, which is optical fiber conference. So, after Nvidia's announcements and all the stuff that happened in the optics world, I don't know. I I'm kind of like like seriously, I'm like filled up, my mind is like filled up with all this news, and I'm like I've come to the point where this week I've actually made a bunch of tweets that made no sense at all.

Like I'm just tweeting stuff that makes like no sense. Like I don't read through stuff fully, and I just like say this, and and then I'm like, what am I doing, man? Like calm down. I think my brain is like fizzling out.

Totally. That's right. Let's see. So much to say.

Yeah.

Yes. So much to stay on top of. And yeah, I was at GTC and then I was trying to like keep up with what was going on in OFC, and then I was just like, never mind. I can't do both, you know.

I'll just have to read it next week. But today I'm not reading any of it. It's it's Friday and I'm just going to go outside cuz it's nice here. Yeah, that's nice.

Yeah. Then I mean, you just got back from California, right? Yeah, yeah. Which it was hot there.

So, when I left Iowa, it was like 7° Fahrenheit, -17 wind chill. I had to park on like the outside of a parking ramp like at the top. It was like freezing. Um and then when I came when then when I got to California, it was like 88° when I landed.

They're having like a heatwave. Um and then even when I got home, it was like 78 here and my kids were sunburned from playing outside. I heard Austin I was like, oh, it's spring. Actually, my day-to-day temperature in Bangalore is around 80 85°, and if you're like at, you know, I think you're easily at -15.

I don't know. Yeah, yeah. Yeah, we have 100° just between this podcast between us. That's hilarious.

That's so good. Yes, I'm not used to it. Yeah. But okay, so yeah, where should we start?

Let's let's start not Nvidia. What do you think? Yeah, so I have to tell you this first. Like I had I've heard so many people like right now saying, oh, I spent so many tokens in like agents and this and that.

And then Nvidia comes and says like the guy Jensen in the Allen podcast, I think he says, if you're a $500,000 engineer working for a company, I expect you to spend at least $250,000 in tokens. I'm like, wait. That that's not going to go down well. I was like, you kind of like imagine going to your boss and says like, yeah, I want to spend 250k in tokens.

I'm like, I thought AI was supposed to make things cheaper. What's going on?

[laughter]

That's hilarious. Yeah, you know, so I I got some interesting thoughts on this. So, I actually I was in an industry analyst Q&A earlier before Jensen said that the podcast thing. Um and I asked him the question cuz he had said in the keynote, hey, you know, I think that we'll soon get to a point where a token budget is a differentiator for employees.

Um and so I and and I said to him like, hey, look, I agree because to me, I think that agentic AI is the killer app that we've all been waiting for for generative AI, right? When gen AI first came out, it was just a chatbot. Everyone was like, okay, this is cool, but what's the killer app? I think agentic AI is, and I think like for me specifically, it's coding, but I think it'll be more more broad than that.

Um but maybe it will just be coding. Maybe it's just like everyone can code, you know. Um uh we So, anyway, so I said to Jensen, I was like, hey, I I actually believe you that once you go agentic AI, you'll never go back. So, if you're at a company where you're they're just like, ah, sorry, we've got strict token budgets, you can't spend much, and then some other company says like, dude, you can go to town, cloud code all you want, like you'll never go back.

You'll be like, that's amazing. But to your point, I started thinking about it and I was like, well, wait a minute, if you give people actual token budget, like let's say $10,000 a month. We'll just use round numbers. Well, what if I'm super productive and I'm going to town and I blow through it in a week?

Now, am I going to just not get to use cloud code for the next 3 weeks until it resets, right? And so the the the the incentives are maybe a a little misaligned. Um so, what I said to Jensen was, are companies in this situation going to buy tokens for every employee, or are they going to buy token generators? Are they going to buy the hardware itself?

Because then you essentially have like unlimited tokens, if you will. Now, I was also hoping that that would open the door to talking about like on-prem inference, like the um Dell ProMax with the GB300 where you can literally like air-cooled, plug it in at your office, um and have the data center GPU because and there's I think a lot to explore here and a lot more I want to hear from Dell, which is like, hey, what if for a team, instead of saying, yeah, um we're going to spend a million dollars for this dev team in tokens per year. What if you're just like, we're going to get these are like $120,000 machines. What if you're like, we're going to get like four of them, and you can all remote in and share them and go to town, and I think it's got like 768 gigs of memory or something.

Now, not all of that's HBM, but like hey, run run big open-source models, do what you can, uh you know. Maybe that's actually going to be a lot more cost-effective than people just getting these crazy token budgets where once you've spent it, it's gone. And it's a whole the whole op ex versus cap ex type conversation stuff. Like I just feel like CFOs are going to really want something other than, oh great, now I got to spend an extra 200 grand per person with OpenAI, for example.

Yeah, that's that's the way I think it's going to go, and the op ex cap ex thing is obviously very important. But you know, even when you deploy on prem, I don't think you're going to have virtually unlimited tokens or anything because, you know, there's a token per second generation thing for a given quality of hardware, and then there are so many engineers, so it's going to be divided up at some point. Just think of it as like EDA licenses, right? You you sign up for 20 licenses.

And when somebody is using it all up, I have done this personally, I go to somebody and say, hey, can you please get off the license if you're not using it because I want to run something. And then they do, and then that's how it goes. So, this is will be on a similar note, I think. Not exactly the same, but I think it'll be like, yeah, you you you've used up your token budget this week.

Can you chill? Can you like do something else and maybe next week get back on it, right? Sure, sure, sure. Yeah.

I I I see your point. And and that would be the the trade-off is like, well, this machine can generate a certain number of tokens per second for a certain number of concurrent users 24/7, but now the onus is on the employees to have to kind of manage that and share it and whatever.

Yeah, it's a resource. It's a hardware resource like any other that has to be shared. Right? You know, we used to have these like big computers where I used to do a lot of like electromagnetics work, which is like heavily computational.

And yeah, so that was how it was. Like you you submit a job to it, um and then you you hang out or whatever, and then it gives you the results back. Or think of it like LSF clusters. Like you submit a job, you don't see the machine, right?

And it when the simulation is done, it gives you the results. It'll be like an LSF cluster of uh tokens, right? So, you're going to be using from this cluster instead of compute, which is kind of what it does anyway, LSF. Load sharing facility, I think it's called.

So, it's going to be like that. It's going to be a bunch of servers that every big company at least will deploy. Um and smaller companies will deploy smaller versions of the same thing. Yeah, exactly, exactly.

But the nice thing is you you have a fixed cost. You know exactly what you're going to spend as opposed to just like APIs where everyone can they don't have you kind of don't have to share in some respects when you use APIs, but you could go to town, you could blow through things or blow over and spend too much, you know. Yeah, and nobody wants to send their tokens anywhere else outside premises. This some of these industries are very, very sensitive to this, and you just can't do it.

It's very because even if how do you know that like your tokens don't like go somewhere else in the cluster and some somebody else does something because you're using a bunch of CPUs and GPUs in a like a facility, data center somewhere. Totally. What is a guarantee that your bits did not go to your competitor's bits which are using GPUs from the neighboring rack? Like that kind of security guarantees are coming into newer Nvidia GPUs.

They have been talking a lot more about security guarantees. That's coming up. It's going to be a thing. But a lot of companies will not like that, right?

Totally. And and you know, Jensen, when I asked him this question, he spoke to it, and he sort of said like, hey, I think that there'll be a hybrid. Like there'll be times when you want the biggest, best frontier models, and it's going to have to run in the cloud, whether it's your own cloud or, you know, someone else's cloud. Um but there's to your point, there's going to be sensitive data.

Also, he he said he believes in like a lot of local fine-tuned models where a company will say like, hey, we have our bespoke data, we've trained our model for our particular use cases, let's let that run on prem and handle and then any of that stuff, you know? And so I I definitely do think we'll get to a world Of course, then there's lots of questions around like how's all this orchestration going to work and who's going to build it? But hey, now that we have AI, maybe it can get built easily and quickly. Yeah, I Now that you mentioned that like these fine-tuned models, I have to mention Matthew Berman.

I don't know if you've seen his YouTube channel. It's pretty amazing. Yeah. And yeah, he he has all these amazing videos and he mentioned this one thing that he's working on.

He said, "Yeah, I had the my open claw agent has all of my information. It has all of my memories, everything I prefer, don't prefer, all of that stuff. And all of that has like the outputs from a frontier model. So he's like, I'm going to take like a lighter model, like an open source model, smaller one, and I'm going to train it just on my inputs and outputs that I have already stored in my open claw environment.

Nice. And that's going to save my token cost enormously. " Nice. He said he's going to like look at it and like like post a future video or something.

It's very exciting. So I decided after watching Matthew Berman, I'm going to like take this open claw thing seriously because Jensen was also like so emphatic about it at GTC. I'm like, "Okay, fine. It's time.

Okay, let's I I played with it a little bit earlier on my laptop and then, you know, all these security things. So I didn't I just quit it there. But now I deployed it on I have a little home server that I run where, you know, I keep my own files. I I run my own little cloud with all my family photographs and stuff like that.

So I deployed it in a docker container within my home server and I put in like a reverse proxy to some kind of like an open claw. dot something. dot something, you know? So if I go there, I can go to my dashboard now Nice.

whatever I want. And before anybody listening to say like saying like, "Hey, why are you reverse proxying it to an URL? That's like the worst thing you can do to agents. " To be fair, this is entirely within my local network.

It doesn't go outside. It's not exposed to the internet. If it is, it's through Tailscale. So I have a VPN Tailscale that's going.

So I do have security protocols Nice. Nice. in place. But yeah, I set it up and I bought a bunch of credits for like Claude.

And I'm [snorts] like, "Okay, fine. Let's Let's do this. Let's set this up. " And I've been playing with it.

That's amazing. You I you'll have to share what you do with me sometime. I'd like to set up something that's same. One of the things that I really want to do cuz I like my mantra right now is ABC, always be Claude-ing.

And so like I I always just want to check on my jobs, my agents, and then just just cuz usually it's like okay, they're good on their own, but then after a few minutes they'll just ask for something. And I'm always like, "Yes, yes, yes. " You know, like even if I tried to to give it like disable all things, never ask me anything, just go to town. Like it seems to always still have to ask me.

And so I want to just be like from my phone be able to like check, you know, go to that URL, check on the dashboard, or have a terminal or something and just be like, "Oh, yep, keep going. Keep going. " You know? Wait, doesn't it didn't you set it up with like Telegram or whatever?

WhatsApp?

Well, there you go. That's a great idea. I think that's was like the one of the like the most initial use cases that like got everybody hooked on this because you could just like hook it up to WhatsApp. And then And then you could chat with it on your phone like messaging. Oh, beautiful.

And it's like keeps doing whatever you want on the phone. I think it's only

Nice. like quite easy. Well, it's solved. It's solved problem then. Yes. Yeah. Anyway, I don't know if I'll continue this docker container approach or I maybe I'll get I have an old Mac M1. So maybe I'll like set it up on that. I don't know. But yeah, I think it's kind of cool. I'm going to agentify this thing because like I told you earlier like I'm overwhelmed with the news. I can't take it. Like I am I have so many subscriptions on Substack that I have to read. With the news, I'm I'm kind of done. I'm overwhelmed. So let's go agentic on this one

[snorts]

and we'll we'll talk about it at least briefly on the podcast. I'll tell you how it's going. Sounds good, man. Sounds good.

All right. So okay, on top of all the conferences, there was also Micron earnings. Did you Did you pay attention to that at all? A little bit, I think.

I I didn't do too much of it because as I said, I mean like memory now, I mean okay, Micron's doing great. That's the That's the takeaway I have. They showed a lot of earnings and their stock is up I don't know some 60% this year. Amazing.

And they are supplying HBM4 to Vera Rubin. Which is something you posted on X. And I was like, "Wait, what? That's cool.

" And Jensen's like signing a wafer and Sanjay Mehrotra's holding the wafer. I'm like, "Jensen, why are you signing on a memory wafer? We need that stuff. Stop Yeah, [laughter] that's way too expensive to be signing, dude.

What are you doing?

People need that, Jensen. That's hilarious. That's good. Yeah, yeah, I posted it because, you know, there's been a lot of noise about how Micron's out their HBM4 is not going to be on the Vera Rubin.

And I was just I was like, "Oh, look. Uh Jensen must not have gotten the memo. He must not have gotten the memo that Micron is not designed in. " Somebody bought Somebody paid up for the wrong thing.

No, I'm kidding. Yeah, I think maybe it there was so much news about this couple of months ago that Nvidia is not going to be choosing Micron and they have 0% share. And a couple of people like on Substack wrote about it and pushed back and said like, "No, we don't believe that's the case. Maybe SK Hynix is going to have the lion's share of it, but it's not zero.

I mean, I think it's a smaller percentage. " I still don't know what the percentage is, to be fair. And then there was this you know, argument that even if Micron was out of HBM, it's not a bad thing because have you seen DRAM prices recently? You know, one It's like easier to make DRAM.

Just make DRAM and then sell it. You can like ship so many bits. You don't need to stack them, package them, test them. HBM is a nightmare.

I know you have like a lot of margin for selling HBM. It's a high high margin, high high dollar count product, but just ship DRAM and you're going to be fine. Is what I read from some other Substack. And I was like, "Yeah, I kind of buy that.

" Yeah.

So anyway, turns out they were in. They're in. Well, and they Micron had a press release. I think it was maybe it was part of their earnings or whatever, but they had specifically said that they have been their HBM4 has been designed in.

Now everyone's asking, "Okay, but does that mean you're qualified yet? " But no vendor has yet said they're qualified. So I think Micron has publicly said probably everything that they're allowed to say, which is "Look, Jensen signed our our thing. You saw it.

It's public and we are designed in and we, you know, have the right pin speeds. So, you know, we can't say anymore, I'm guessing. But all signs point to they're they're going to play this ball here. " Yeah, the pin speeds is an interesting thing because glad you mentioned it.

The JEDEC spec for HBM4 is I think about 8 GBPS per pin. I hope I got that right. I don't know if it's 8 GBPS. It's okay.

So let Anyway, let's at least look at random numbers. I probably got the units all wrong. But then the news is that they have been pushing the JEDEC speed per pin higher and higher so that Nvidia can like stay ahead of AMD. Whose MI450 I don't know is arguably really competitive or better, I don't know, than Vera Rubin.

We have to see. But they wanted to get ahead of AMD and they've been pushing all these HBM vendors to make faster and faster memory. Now one of the thing is like it's gone up to 11 GBPS, right? I mean, that's the kind speeds that like SK Hynix is reporting.

Oh yeah, we did 11 In one of the earnings calls, I think not this one, but the last one or one before that, the detail was that the base die, the logic die that sits below all these DRAM chips in a HBM, was actually designed with a memory node. So a memory node is like a one beta node or a one alpha or a one gamma. These are how these memory chips are actually designated. It's not so much as a two nanometer or three nanometer.

Those are like logic nodes. So memory is like a different process technology because you've got to make those very tall capacitors that sit on a transistor for the 1T1C cell that goes into the DRAM, right? So the 1T1C cell requires like a unique amount of engineering. So the entire process of making memory is entirely very different on a wafer level than logic chips.

This may not be like news to some people listening to this, but if you ask me the same thing two years ago, it would have been news to me because I I thought maybe everything is like a chip, right? Whatever. So memory chips are very different. The thing is these memory chips are typically not designed for speed.

I mean, they are designed for memory density. They are not designed to be the fastest transistor ever made. That is what logic tip chips do. That's why you go from a three nanometer transistor to a two nanometer transistor and you get all these speed gains and you know, this is how you know, chips have been scaling forever, right?

They get smaller and faster and all that. Memory nodes are not built for that. So the whole argument was Micron HBM used a memory node for its base die and therefore they are struggling to meet the speeds that is being demanded by Nvidia. And so that was like another case against Micron.

But I think they repeatedly came out No, no, we are fine. The speeds are fine. And then there were like questions about like, yeah, really? How How many speeds are fine?

One out of 10 are fine or five out of 10 chips are That's you know. That's right.

All valid questions. I mean, these are like legitimate good questions that have to be asked. But this is what is behind all of this stuff. Right now we see that yes, uh it is being designed into Vera Rubin.

I still don't know what the speeds are. I don't know whether they're different from SK Hynix. So yeah, you know, take take all of this with a grain of salt. Whether you're like in the engineering world or um in the chip world in general or whether you're an investor like I think so if people had sold off on the 0% um content in Vera Rubin, they would have I don't know lost out 60% uh share growth now, yeah.

So yeah, you make a good point. Look, it's it's very nuanced. Just because you can hit those speeds, how many chips can hit it? And then of course, you know, what how are you yielding?

It which is asking the same thing. So essentially like how expensive are your chips going to be can hit that 11 Yeah. gigabits per second per pin or whatever. So yes, lot lots of nuance, um lots of noise.

It'll be nice once these things just ship and then the companies can just tell us. Yes, we you know.

Yes, eventually we'll know. But the whole point of the investor game is to kind of figure this out early.

[laughter]

Correct. Yes, that that is 100% correct. And I think um so another thing that stuck out. So obviously Micron, you know, crushed their earnings.

They beat on all fronts. I think they even surprised investors with just how how much the revenue was. Um They One of the things that I did notice was there are lots of investments in new capacity that'll be coming online in like 2028. So there's a DRAM fab, I believe, in Taiwan that they have acquired and are kind of pulling that forward.

There's a new NAND fab in Singapore and I think they're ramping up fabs uh in Idaho and New York. And so of course, naturally, I think in memory there's always going to be this tension of like, great, you're winning and you're reinvesting in in more capacity, which is good because AI demand will continue to increase, capex will continue to increase, but there's always the like caution that people have of like, oh, this feels cyclical in nature and so it feels like you're doing what always happens, which is you're winning and so you're investing in more capacity and eventually there's going to we're going to be flooded with more capacity and what's that going to do to prices? Um but do you have any any reactions on that front on the the the capex investments? So yes, I understand the fear and we've been through this cycle many times in memory.

It's a brutal of all semiconductor verticals, I think memory is the most brutal one. It has had some really bloody stories in the past. So it's very valid that like people who are either working in memory or in have invested in memory in the past have been through these cycles. So the fear is legitimate.

But looking at uh you know, Vera's I think I was looking at the Vera CPU tray, you know, the Vera has eight CPUs. And I'm like, what's all the black stuff around the CPUs? Like look at all that like tiles. Like the entire the tray is like huge.

All of that Is that all DRAM? Like it's incredible if that's all DRAM. Where the memory is not going away anytime soon. I don't see this going away next year or the year after.

If we are talking in five years from now, I don't really know. Things change way too fast. Like five years ago, we didn't even have AI. So I couldn't have told you anything.

Right? But where the the the need for memory is getting incredibly uh you know, stringent and very important. And the another reason why is that all computers are now going to do agentic AI work. You like it or not.

Like, you know, um everything is going to do some amount of AI work. Like and memory is what is going to drive all of it. Like you know, HP and the Dells and the everybody needs memory because everything is going to run AI at some point or the other. The phones.

So I don't see the demand going away. So I am quite bullish about this stuff. Yes. So yes, my argument would be very similar, which is there is a fundamental sort of step that happened with generative AI where huge value is being unlocked, but that requires these massive LLMs, right?

So we've always you know, we've had AI, we've had ML for a long time. In in every sort of step change in the past, um like to personal computers or to the cloud, you know, demanded more memory in that we started to get more machines. Um but the applications running didn't necessarily demand like orders of magnitude more memory. So more higher volume of machines, but not necessarily higher volume of memory per machine.

But now we're in this era where um we do need a a massive you know, increase in volume in AI accelerators. Um and but those also need a, you know, massive like a order of magnitude increase or more orders of magnitude in memory per accelerator. And then to top it off, to your point, the whole surrounding ecosystem, whether it's the CPU trays to support the GPUs or even just like all of our, you know, thin clients will still also want more memory because they we are going to still be running even more generative AI at the edge, whether it's on on prem racks or potentially, you know, even our devices, which although today thin clients work now, so you know, I can I can get to the agents even if I don't have a ton of memory, but surely there will be a pull for doing more and more locally. So I do think that the generative AI has definitely there's a step change in the amount of memory we're going to need on every device.

Yeah, and I'm not saying for edge AI that necessarily means we'll be running full models on the edge devices. I think the models can remain on the cloud, but just inference and agentic use cases will need memory. Yeah, yes, yes, 100% right. Like like all of my tool usage stuff today, it'll be like, oh yeah, go hit these websites and scrape them or make these API calls and then get a bunch of JSON or HTML or whatever and process it and then feed it into the LLM, right?

So like these are still, you know, memory intensive, memory dependent things. Cool. I think we should hit up one more topic and then we'll keep this episode rather light. Okay, so recently there was this optical compute interconnect multi-source agreement.

Okay, like that's so many like letters I had to like look it up. Uh OCIMSA. Okay, so what that really means is like this bunch of important companies, Meta, Broadcom, Nvidia, OpenAI, you name it. All the names are here.

They kind of got together and formed this multi-source agreement for optical components um that is going to be used primarily for scale up, I would imagine. And so this is very important because this is like an official declaration that optics for scale up is now important and big players are getting together to hold hands and make this an open ecosystem where many people can make components and supply into the industry. As opposed to like one player getting in and doing things there with. Yeah.

Yes, this is an industry consortium and just like say UA link or Eason or something, they're saying like, let's get together, define sort of I'm assuming I didn't read too deeply. And but like let's define some standards and then we can all agree to those and then we can all compete based on performance and anyone can buy us and plug us in. Yeah, so there are a bunch of technical specifications defined on the website, OCI-MSA. org.

So yeah, so this is going to be like an evolving thing. Like the version 1.0 is out, but I'm sure it's going to evolve. There are other MSAs like I think there's like dense wavelength division multiplexing, which is another optical technique where you send multiple wavelengths through the fiber. That has an MSA cuz multiple people are going to supply into that.

And this has been around for a while because this is used in telecom and things like that. This is a big movement. But typically, uh when you talk about optics for scale up, you know, there are going to be a lot of uh connections because you know how many GPUs they say like connected in an all-to-all fashion. So scale up represents a very large interconnect problem because there are just literally so many cables that have to go in scale up, which is why everybody in the optics industry is extremely excited that optics for scale up will be a thing, whenever that is.

Next year, two years from now, three years from now. Can't really say. But it is coming. We are heading towards that direction.

Copper at some point will reach its limits. We're going to need optics. So now here's the big question. What kind of optics do you really need for scale up?

Right? The easy, lazy answer to it is to say, like like all other optics, why is it any different? Like why would I not use indium phosphide uh electro-absorption modulated lasers? Actually, I don't think anybody says that except us nerds on the pod, but you know what I'm talking about.

[laughter]

But essentially, why not, you know, do do optical connections like they've always done? Like uh the telecom companies have done it for decades. Optical scale out has been doing it between racks, scale across between data centers. That's because because you know, the scale up problem is a small one.

It's within a rack, let's say, or very close by rack. So now it ask whether the technology we already have, which involves indium phosphide lasers, is actually the best suited technology for optical scale-up. Right now people assume it is. Like you just put that in, you put CPU, whatever, you hook it up, and then you do it like you've always done optics.

But I think that in the industry there is a whole different bunch of technologies that are being looked at or are evolving that could completely change the equation here. And I think this is important to talk about. Yeah. Yeah, that makes a lot of sense, right?

So like um I guess for listeners thinking about the distance you if you need to send something 10 m versus 1 m versus a tenth of a meter versus a hundredth of a meter, maybe you would have different requirements for the light source to use if you've got like if you're only connecting chips that are really close, maybe you would use a particular technology. Is that kind of where you're going? Yeah. So that's what that's what I'm going towards.

So one option that I think people have been looking at is micro LEDs. And it is interesting because these LEDs are basically gallium nitride on silicon devices. And the way they are done is they are manufactured like separately and then they are like uh like placed onto um you know, a silicon wafer that has, you know, transistors and circuits and all of that stuff. So these are GaN LEDs.

And GaN LEDs uh they require what is called a microlens. And the reason for that is the light from a GaN isn't like very pointed. Like, you know, lasers, you know, you you point you just go from one place to another. This is like turning on a light bulb, okay?

Yeah, it like diffuses. Yeah, it goes out like in a in a cone, I'd say. So you need to put these microlenses on top of each GaN LED that actually focuses the light. So that's an important part of this thing, okay?

So that's that's what people are looking at. And it's difficult because this is not a very, you know, high-quality light source, and its characteristics uh for modulation, like, you know, you want to send on-off bits, right? So you send a light or you don't send a light. That is basically uh called intense intensity modulation, right?

Uh that that kind of modulation can be done, but it cannot be done like the way you do it with an indium phosphide laser because the characteristics of that laser are exq- exquisite, and they are basically built to do this. But GaN LEDs are not like that, you know, they're like micro LEDs are just they kind of they have all kinds of crappy characteristics. So you can the run 200, you know, gigabits per second like data on a indium phosphide laser. Uh you can probably run 2 gigabit per second on a micro LED laser.

So Uh I'm sorry.

on wafer per per channel basis is pretty crappy. Like you can't drive this thing 200 or like even 50, I don't know. I don't think so. But you definitely won't compete with an indium phosphide EML.

So what they do is they take these things called imaging fibers. Imaging fibers are what is used in uh let's say like endoscopy applications. Like you have a a cable with multiple strands of fiber in it. Okay, you can have like thousand strands of fiber.

Like you think about these long like you know these Golden Gate Bridge has this I don't know if you've ever seen When you've been to San Francisco, you should go see the museum at the Golden Gate Bridge. There is the cables in the Golden Gate Bridge that hold it up are not one single cable. They have strands of them inside. It's actually made of many cables that, you know, comprise of the Golden Gate Bridge.

So this imaging fiber is exactly what that is. So you can send thousand different lights light signals through one imaging uh core fiber. And so what you can do is like this is the slow but wide approach to optics. So what you do is you sense many snow slow signals, but you send a thousand of them at once.

Mhm. Right? It's like the HBM of optics. Essentially.

Totally. Totally. Okay, so we got slow and wide versus fast and narrow. So instead of like a ton of car like a highway with two lanes, but everyone can go it's the Autobahn, so you can go 150 miles an hour.

This is saying, "Okay, it's going to be a 100-wide lane, but you're only going 30 miles an hour. " But the throughput is the same. You're getting the same amount of people because you're wide, even if you're slow. Yes.

So that's the whole idea. There are like a few companies working on this. So one example like Avicenna's uh presentation is something that I saw last ISSCC, the Solid-State Circuits Conference in uh San Francisco. They had like a whole demonstration of how this works, and the slides had like this, "Oh, why are you taking an airplane to the grocery store?

" It still stands out in my mind. So they had this picture of this person taking an airplane to the grocery store. That's what it is like when you're using an indium phosphide laser uh to do scale-up. That's their argument, at least.

So why do you need this technology to do Why do you need an airplane to go to the grocery store? I said, "Okay. This micro LED is supposed to hold a spot between copper whose reach at high speeds is very limited. Now, you know, at 400 gigs per lane like Hock is Hock Tan of Broadcom is talking about, your reach is probably going to be a meter or a meter and a half at most, okay?

That's that's kind of reach. Maybe that's enough for some applications, but maybe it's not. What if you're going to go to 800 gig? It's copper's dead in the per lane era.

So optics is like power hungry. Like whatever you do with optics is quite power hungry. It's not like copper. I know people say CPO this and that.

Yeah. Yes. Optics is expensive to make all the CPO stuff, and it is power hungry. So unless you really need to go there, people are still looking for other solutions.

Micro LED fills the gap between the two. It has like copper-like cost structure, is at least what companies claim. But it has the reach that is could be 10 m or even up to 30 m, which is plenty to hook up like GPUs in a rack or multiple racks. Yes.

Yes. And And if I recall, maybe I saw this. So I know Avicenna's doing it, and then Credo bought a company, I think maybe Hyperloop or something that's also doing micro LEDs. And And And I believe everyone also talks about like the energy energy density efficiency per bit.

So it's like picojoules per bit times the gigabits per second per millimeter or something like that where like micro LEDs are kind of like in the sweet spot there. Yeah. That's That's what it is. And Hyperloop acquisition by Credo was interesting.

And Credo holds an interesting place, right? Uh they have a lot of copper expertise. Uh they have active electrical cables. Those are the purple cables you see everywhere, and everybody had so much love for them like a year and a half ago.

Everybody is all about uh purple cables. And in one Amazon picture they uh in you know, rack picture, they didn't see purple cables, they saw orange cables, and their stock dropped because of the cable color because everybody's like, "Where's the purple cable? " And then later it came out that like Amazon said, "We don't want purple for whatever reason, branding, I don't know. " They said, "Please make it orange.

" So Credo was like, "Fine, we'll make it orange, no problem. " And their stock dropped. Crazy. Crazy.

It's It's nuts. So yeah, so they have that, and they recently in OFC 26, they announced like a fair bit of like optical content. They have like a 1.60 optical DSP. They have new products at the 400 and 800 gig uh ranges.

They have some long-reach optics. All of this is covered with like their you know, their zero flap technology where they have telemetry. And I think telemetry is getting increasingly important. Actually today I saw a piece of news that Marvell is also inclu- including telemetry in their interconnect products.

Because you can't have We spoke of this in this about this in this podcast before. You can't have link flaps. You can't have links going down. It's a very expensive thing.

So by monitoring the health of each link and taking them down before they become an issue, this is a very big feature. So that is becoming important. And I think this micro LED thing fits somewhere in the middle. So Credo has like a spectrum of products that's very interesting.

Um and people I don't know why people tend to discount them in the light of optics news. I'm like, "Actually this is a good company. They They have a lot of stuff, like really. " Mhm.

So I'm not very anti-Credo, but my stock will not speak to my convictions here. So let's leave me out of it. Totally. Totally.

Yeah, I think uh obviously none of this is surprising to Credo. They work in this industry, and so they're building out beyond active electrical cables to micro LEDs, and then eventually to, you know, optical scale-out transceiver DSPs and that kind of thing. It'll be fascinating to watch this micro LED space with the the CPO and the VICSELs and everything else going on and see what ends up winning. Yeah, VICSELs.

I'm glad you mentioned VICSEL. Almost slipped my mind because vertical cavity surface-emitting lasers are really mature technology. People have shipped billions of these things. Um they are used in like uh lidar sensors.

Mhm. And also in like augmented reality has a lot of Actually, no. Uh I take that back. Augmented reality has my micro LEDs, interestingly, because I was looking at who makes all these like lenses and you know, focusing things.

And I came across like a whole bunch of augmented reality like uh content. I need to go look at that. So, this is why you have to subscribe to our substacks. You know, this is the kind of thing we do.

Go look at like strange stuff and write about it on substack, right? But, yeah. Other than that, like Vixel is interesting because Lumentum in OFC 26 mentioned that they're working on a 10 16 nanometer Vixel for optical scale-up, which is kind of cool. This is also a slow but wide approach.

Mhm. And uh they said something to the effect of I have it in my notes here that that this is actually better for like better speed um and higher temperature performance and they said exceptional long-term reliability. Like, what? Oh, that's that's good.

Uh because I think lasers people always worry that lasers are going to fail. Mhm. And there's a good reason for that, you know, they're they they when you then they heat up, especially, their lifetime drops like a rock. So, lasers are inherently like that.

So, if micro LEDs and Vixels and all these things have better lifetimes, remember we were talking about these link flaps? In the scale-up domain, believe me, you don't want link flaps because there are so many cables you don't want to be swapping them out because of failures. So, that's another interesting aspect towards scale-up interconnects that are coming up. And whatever has better reliability might be a selling point, just saying.

Oh, definitely. Definitely agree. Uh so, I guess it's probably enough for today, but you'll definitely need to write for us more about micro LEDs and get deeper into this optical scale-up. So, I think a lot is happening right now, but it's still very fuzzy as to what's going to come out on the other side.

Yes, it's very interesting and I, for one, I'm not discounting micro LEDs just yet. But, before I say anything further, I need to go dive deep on the substacks. So, until then, uh I will have to hold off on making big calls on this thing. I love it.

And I appreciate that. It's easy to make calls, but I appreciate that you as an engineer want to first study it and come to your own conclusions about the benefits, the pros and cons. How about that? Yeah, I'm a very low conviction guy and then I do a whole bunch of research and then I go from low to like medium low.

[laughter]

And then I don't invest in any of these companies and like then I look at the stock and I'm like, "What? What's going on? Like, why didn't I make any money out of this?" Yeah, I need to work on the investing aspect, yeah. Totally.

[laughter]

Good stuff. Okay, guys. Well, thanks for listening. Uh and I will say last thing.

So, when I was at uh GTC, several people came up to me and said like, "Hey, I love the podcast. " Or they'd say like, "Oh, are you the dude that does the podcast with that Indian dude with long hair and the guitars? " And I'm like, "Oh, yes. Yes, me and Vic.

That's right. " So, thank you. There you go. Um thank you everyone for listening to Semi-Doped.

Uh subscribe to our newsletters. Give us a five-star rating. Uh thank you, YouTube people who love to leave us comments. Uh and anyway, stay tuned.

We'll be back next week. Have a good weekend. Talk to you later.
