---
source: https://www.youtube.com/watch?v=Mvp-DAfzoRk
title: Optical Networking Supercycle - ALL the Tech You NEED to know
date: 2026-02-20
kind: transcript
note: 유튜브 자막에서 옮긴 전사. 화자 바뀜(>>)마다 한 줄. 600자 넘는 발언은 문장 넷씩 더 쪼갰다.
---

The scale up opportunity is a brand new market that didn't exist before. All right. Hello listeners. Welcome to another semi-doped podcast.

I'm Austin Lions from Chipstat and with me is Vic Shaker from Vick's newsletters. Today we're going to talk to you about the optics and networking super cycle. But first a quick teaser. Vic, I saw you had a really interesting post today about CPUs for AI.

So let's talk about that really quick. Yeah. So the Substack post today is basically about how CPUs are a big bottleneck when it comes to AI and it could actually limit how much GPU usage is actually going to uh happen depending on the kind of workload you have. So if it's highly agentic that the CPUs need to go off and do a whole lot of things like pull databases, scrape information, that could be significantly different from just like doing something that's GPU heavy like inference.

So I basically the article c categorizes a whole bunch of uh CPUs according to their best use cases. So yeah I I had fun writing it.

Nice. Yeah I bet because honestly lots of people are saying oh CPUs are a bottleneck but I don't feel like anyone's really dove into what kind of CPU and what what they're used for the use cases and like why they are the bottleneck. So good read. Very good read.

And then I'll I'll throw out there I just posted today about Nvidia's autonomy business strategy. Um again I had fun like Vic really kind of getting in deep and asking a lot of questions that people have been asking me and I had been waiting to write about because I've been writing also about optics and networking which is very hot. But um with that let's jump into it. So Vic uh Silicon Phetonics had a big week last week.

Um why why are we talking about it right now? Yeah. So, it seems like optics has become a big thing now because the connectivity bottleneck is a big deal in data centers. And a few months ago, I made a tweet that went got way too many likes that like retweets than it should have.

I said optics is the next memory. You just don't know it yet. So, this is like off the cuff remark. It was not like highly highly educated or whatever, but I thought it was funny, but I think a lot of people agreed with it.

And now I see a lot more uh articles and news uh outlets with with that phrase. U I mean of of their own accord. It's not because of my tweet obviously but I think the main reason this is coming up to be the case is that we need faster interconnects between GPUs. uh copper is running out of speed and distance and reach and in order to do this we have to go uh to the optical world for which we need pretty much everything uh like lasers we need foundaries to make these photonics chips uh we need people to assemble these transceivers and the problem is that there aren't so many people making these things because typically optics has only been limited to like longhaul communications and maybe a little bit of LAR and things like this.

But now we are on like data center scale where you need everything on massive massive scale and there are only a handful of companies kind of dominating the space right now and I'm sure we'll get into all of that but all of these companies are signing multi-year long-term agreements with customers getting fully booked out and all these customers are like prepaying for all laser capacity like even one or two years into the future. It sounds a lot like memory and HBM.

Yeah, you know that's the reason I can see a few parallels between this and HBM is because like in HBM there are only a few concentrated suppliers who make lasers and all the optical fiber and things like that. And so structurally because only a few people do it there's there is an under supply. And what that leads to is that like a lot of people can have pricing power. If you're the only game in town, you have the pricing power. And then when you have everybody wanting what only a few people can make, you are in the same situation as HBM is.

Mhm. And I think in both races, the HBM race and like this the connectivity race, scale up speeds, scale out speeds, there's always these sort of like inflection opportunities too where a new technology comes out. So HBM 3 to HBM4 uh or you know uh 800 gig to 1.6T. Um it it's it's and it and it's almost like the foundry race too of like who can get to the next node first.

There's just like this appetite where uh all these hyperscalers are trying to build the next data center and they want it to be on like the fastest scale out scale up networks possible. And so if you're one of the three or four suppliers somewhere in the supply chain and you can be prepared for the next industry leap in speeds first, then you get a temporary advantage essentially. And and kind of same and the uh analogy to HBM there is like yeah, whoever can get have validated HBM4 first um with say Nvidia where they're qualified and Nvidia feels good about it like that's a huge advantage. And so that's something that just came to mind to me of like there's also so the the question is all for these companies not just who is it but it's around kind of like the industry timing and maybe like do any companies have a lead to get there first.

Yeah. So it's interesting that you mentioned the 800 gig versus 1.6 uh T generation shift. I think that's a good point to get into the whole optics discussion here because the way you get 800 gig optical networking is basically you have 800 gig lasers and the way you get to 160 is of course you could have 16 1 point uh 16 100 gig lasers but you'd rather have eight 200 gig lasers. So now you are going for these uh lasers that are like twice as fast and those are all um externally modulated lasers.

So there is a light source and there's a modulator and this is all done externally to the silicon photonics chip. So now it's interesting is that um the 200 gig lasers uh can be sold for a a lot more money than the 100 gig ones. And

uh it's it it rises the revenue of all these companies selling it. And to add to the benefit of all these optics companies making this stuff,

you have both the 800 gig ramping. I mean we are not yet in the peak of the 800 gig cycle. We still if you look at the scurve, we are still in the in the rising part of the 800 gig curve. And then you have the 1.60 60 which is starting up sometime 2026 I would guess and a lot of this is like what they call an overlapping scurve so it's not like 800 generation is phased out the 800 gig one and the 1.60 60 has come in newly.

They kind of overlap. So these companies can not only sell into the 800 gig market which is still not topped out but they can add additional revenue on top of this by uh shipping out 200 gig lasers.

Nice. Yes. So they can have a product portfolio and the newest products are all they're slowly ramping. they'll probably have the highest ASPs, but then the, you know, their last generation will probably have significant volume, but lower ASPs and so on and so forth. And it actually that kind of reminds me of like TSMC for example, as they're ramping, you know, two nanometers. Well, they're still making a ton of money on five nanometers or three nanometers, right?

Yeah. Exactly.

Totally. Okay. So, let let's dive in this systematically. Should we talk companies or should we talk like technology like scale across, scale out, scale up?

Let's go with the technologies part of it. We'll get to the companies a little later because once you understand the underlying technologies, I think the companies would make a lot more sense.

Yeah, sounds good. Okay, so let's start scale across. We'll start there. Scale across talk to me about scale across optics and is it interesting?

Uh scale across is actually to me technologically the most interesting part of optics. Actually we don't talk too much about it. Uh that's because you need to connect entire data centers with uh optics that are like long haul optics. And so you have these things like 400 ZR uh which this specifies like uh a really uh long range connection uh over I don't know kilometers tens of kilometers hundreds of kilometers things like this and this whole scale across technology is transitioning from 400 ZR to 800 ZR as well.

uh this is not even those 800 gig to 1.60T we were just talking about. So in the scale across also there is a transition happening and the technologies to me is very fascinating because you these connections can send pabytes of data across extremely long distances. Of course, now this is like power hungry, you know, these are not like co-ackaged optics. This is not like that.

But what they actually do is they use a whole bunch of lasers um in a comb fashion. They call it a comb laser because if you look at the spectrum versus wavelength, it looks like the teeth of a comb, like closely spaced signals. And you have like 96 of them, like even even more than 100. And each one of these the the teeth of the comb u or actually carries a signal and the whole thing is like modulated and it's sent and then demodulated on the other side and there's like a whole lot of error correction that goes on.

So it's to me it's technologically amazing

and it is coming up now because like data centers are being built out and they do want to connect them together and uh Jensen I think framed the scale across term and It's become the the new dimension of optics. But uh really I don't think that's where all the excitement nowadays is lying. It's just my personal preference to look at right now. But

yeah, totally. Let me ask you two quick questions. So when you talked about the spectrum versus wavelength in the combs, are you saying that like they'll send signals using like 96 different wavelengths down the same fiber at the same time?

Yes. Yes. Absolutely. And then and then of course so they have to you have to be able to do that with the laser on one end and they have to be able to receive receive all of it with the photo diode and sort of it's probably all multipplexed together and sort of demultiplex it and error correct it and it's kind of magical that it all happens.

Exactly. The term for this is DWDM or dense wavelength division multiplexing. So you densely put multiple wavelengths, multiplex them and send them down this huge optical uh cable like that goes tens of kilometers and it's like decoded on the other end. It's not like fantastically new technology, but the fact that that that is also undergoing a a speed transition.

Yeah. Yeah. Okay. And so when you say it's not new technology, tell me historically where was this longhaul optics used and then why is it interesting now in terms of connecting data centers full of GPUs?

So this technology has been used in basically subc cables like in the telecom world you have to lay down uh like these gi like cables under the oceans that basically takes all the information from one point to another when you make uh calls between continents and things like that it all it all goes under the ocean in optic fiber. So these kinds of things use uh basically technologies that are like dense wavelength division multiplexing. The reason is because on each wavelength you can send information. If you can send like hundreds of them you can send more information and we really do want to send more information and you have to have like amplifiers um everywhere and to to boost the signal as it goes through the ocean and stuff like that.

So all of that exists already but today it is important because uh we want a lot of bandwidth between u data centers and a lot of this technology is also used in metro data centers which means not I mean metro I would say metro telecom right within a city you have a lot of optical fiber that's going everywhere providing you know stuff to people's homes and collecting all the information and like feeding it to the main optical trunk. So all of this exists in technology like whether it's subc or within a metro but now they want to connect data centers and yes you can reuse the metro uh already laid out optical fiber to do a lot of these things but sometimes for business reasons and for exclusivity reasons data centers prefer to have their own cables drawn out between them. So that's yeah that's a deep dive later.

Yeah. Yeah. I guess two last points and then we'll carry on because this is a very interesting topic. I I'm sure the scale across for uh data centers full of XPUs communicating with each other during training.

So that's the use case. This is not inference. This is just like I've got so many XPUs that I actually have to have different physical halls a and data halls. And by the way, maybe they are in, you know, two separate states, uh, you know, Tennessee and Mississippi or something because there's only so much power that I can get access to and I'm trying to ramp this up quickly.

And so now these things are spread apart by, you know, 100 miles, but I want them to all communicate as if they're in the same building. Um, I'm sure I would assume that that scale across network is probably optimized differently than a telecom network, right? So, I assume that the and I don't know this, but I'm assuming that like the GPU use case they're trying they're probably making different trade-offs with respect to like latency, handshakes, error correction or something. Do have you looked into that at all?

Not in depth, but there is a fundamental limitation to this stuff. The coherency between GPUs across data centers will never be faster than the speed of light through a fiber. You know, there is simply nothing you can do about it. And that latency will have to be handled uh by the entire system uh put into place because these are latency sensitive applications.

So there will be some protections in put into place but I I did read about it I think but I can't like like put it across to you right now exactly about that. But this technology exists and it's not just for hooking up data centers and GPUs together because

a data center inherently is useless if it cannot be connected to the outside world. Now when there are so many people like putting inference requests and you know asking it to do this and that agents are coming in and saying all of this stuff uh there's a lot of data center traffic that goes in. So

that connection also requires wide bandwidth connections.

Sure. Totally. Okay, last question then we'll move on. When you say that there's amplifiers on these longhaul routes and some of them are under sea and of course some are just in metros, how are those powered? Like how do they power those under the sea?

They draw electrical cables through too.

Okay.

These are not like low power. You can't just like dump in batteries and call it a day. They have to be powered with electrical lines that are also drawn under the ocean. So bottom of the ocean, it's optical lines and electrical lines.

Yeah. Yeah. Because you have to amplify it every so often.

Yeah. Yeah.

And they're terrible. They're terrible. Like there there are uh you know sharks chew through them. Like the trwlers break them. You can look in the news every now and then uh you know

people are cutting subc cables all the time. So people are like, "Oh, like now I'm they're just like I'm going to have a backup link that goes through satellites, you know, high bandwidth free space optical link so that you know in case this gets cut, at least a conversation may drop in bit rate, but it doesn't have to drop. You know, it's a big problem." Yeah, it's a big problem.

Yeah, that's interesting. Okay, carrying on to scale out. So let's talk about scale out and talk about how it works and where we are today with industry shifts. Yeah.

So scale out is basically uh within a data center building you have these multiple racks and you want to connect all the GPUs in the different racks you know they're kept in a row right if you see the pictures of data centers you know you have these racks kept in a in a single row all of them with GPUs and uh you want to hook them all up together so that they can be coherently used for training runs and things like that. So in order to do that uh you just can't use copper because the distances are uh several meters or tens of meters u maybe up to 100 if you consider the end of the rack or whatever. Uh also it comes down to speed. Now you can use copper but you require special kind of cables uh that require like some kind of error correction that accounts for the losses in the copper across the thing.

So it's not like it's never usable but beyond a certain point which we have I think reached already optical is the best way to connect different racks together. So optical has been the way that we do scale out now and that is kind of the de facto standard.

Gotcha. So tell me where do co-ackage optics come in? Do those come in does that come into play with scale out?

Uh yes. Yes. So you can do scale co-ackaged optics because even when you do scale out you want to save energy because uh you these transceivers you know if you don't these optical transceivers transceivers are just things that convert electrical to optical signals and vice versa. Uh these are typically uh called pluggable optics.

Uh and then these are like little uh handheld like modules that are like rectangular in shape that you can just plug into the back of a network switch and it does the optical to electric conversion at the back of the instrument. The problem is that in the network switch which is sitting inside like this rack case box is actually sitting right in the middle of this thing. So there is like several cm of electrical connection that is extremely uh terrible in term in in electrical uh terms. It doesn't really preserve a high-speed signal very well.

So now you have to correct for this which is why these pluggable transceivers actually have a DSP chip in them so that you can recover the bits that are all garbled by traveling through this really crappy copper connection from the end of the rack unit to the middle of the rack where the silicon chip is actually sitting. So all of this sucks a lot of energy and it sucks like per connector it takes like 20 watts just to run a DSP you know it's terrible. So the idea of co-ackaged optics is like okay how about we do the optical to electrical conversion not outside the rack but as close to the switch as possible like what if we can put it next to it or even better put it on top of it somehow and as close as possible you know is better because then the electrical signal travels very short distances and doesn't get as garbled because optics is like always much better electrical is terrible. So that's the idea of co-ackaged optics.

And so you can talk about uh Nvidia's Photonix X switch and the Spectrum X switch which are like CPO based where they have these optical to electrical conversions happening right next to the switch chip, the NV switch chip. And these are usually placed on top of a rack and all of the the the cables from the GPUs connect up to this top of the rack and that is called basically the leaf switch right and so you can connect into other uh leaf switches in neighboring racks now with optics because you have co-ackaged optics right at the leaf switch level. So co-acked optics makes a lot of sense in scale out actually because there are lot of data center racks in use and all of them need to be connected and we need energy usage to get lesser because clearly we we need have gawatt data centers every amount of energy saved is money saved right

yes yes or watts that can go toward compute

yes yeah

totally okay so we've talked about scale cross talked about scale out. We've talked about co-ackage optics. So, now let's talk scale up. And let me I grabbed a couple quotes from some earnings calls last week uh to kind of set the stage.

I just thought this was interesting. Uh Lummentum their the president on their call said the scaleup opportunity is a brand new market that didn't exist before and on the coherent call uh their CEO said scale up CPO is orders of magnitude larger than scale out and it's all incremental TAM for them. So people are very excited about scale up and a lot of people are coming to play in it now. Historically it's just been Nvidia with NVLink NVLink switches.

Um now more companies are interested. So tell us what is scale up and why is everyone excited about it?

So scaleup is just uh connecting up all the GPUs within a single rack. That is a simple way to view it. uh you could actually have the same idea over two racks like in a Reuben Ultra, but that's that's an extra detail we don't need to care about for now. We can just think about scale up as connecting all the GPUs together in a single rack and scale out as connecting racks together.

So that's that's enough of a definition for now. And typically, if you look at the NVLink uh connections in an NVL72 rack, they are all copper and they all go through this like spine that Jensen's always like holding and wielding like like like a sword in all these pictures, but it actually has a lot of copper cables going through them. And uh what they do is they hook up um all the GPUs kind of to each other. And that is a lot of cables.

And the whole idea as to why this is an entirely new market with an order of magnitude better is that there are simply an extraordinary number of copper cables in a single rack that needs to hook up all the 72 GPA GPUs in an NVL 72 rack. Now, comparatively, scale out has fewer cables because they only go from the leaf switch onto other leaf switches or spine switches, which is the next layer of networking. Um, so other than that, you know, there's a there's far fewer optical uh connections at the leaf spine layer. Now, if you have to connect everything in the scaleup domain between the all the GPUs using optics, you're going to need a lot of optical fiber.

You're going to need a lot of lasers and a lot of pluggable transceivers um or however you want to do it. You just need a lot of laser components, detectors and things like that. So this is why everybody's excited about it because this literally means that you have unlocked a whole new domain of uh way like you know application for lasers, detectors, uh amplifiers, uh receivers and all all these optical fiber cables like think about all the people who make all this stuff the driver IC's the lasers and companies like Corning glassware who make all this optical fiber All of this will go into the rack. And the other nice benefit about doing this is copper is extremely heavy.

Like a single rack like weighs like three tons or something like that. It's extraordinary. Now the rack itself has copper. They have bus bars to distribute power.

So there is copper there. But when you have this many cables, um it's a big problem. And I was just talking to somebody earlier this week and I asked them like why don't we just use like um active electrical cable within a rack like uh because the NVL link uh connection the spine actually has all passive copper there are no active copper cables within them which means the the copper cables don't really have DSP or correction or amplification or equalization nothing like the NV link spine has just like passive copper like the cheapest form of you wire you can draw through it. Um and they explained to me that actually there is literally no space actually because this is such a space constraint thing that adding all the stuff in the NV link spine is actually going to make it much more difficult.

So on a per bandwidth basis it's much better if we could just uh go to optics straight away and not have to bother with all this stuff you know. So that's that's my understanding of why scale up and optics is like such a big attraction right now.

So okay now let me push back a little bit and and get your take. So you know Credo would say that actually they are cannibalizing some optics from 3 mters to 7 mters with their active electrical cables because of a reliability problem which is optics have lasers and lasers can be finicky. They have to be perfectly aligned to the fiber. And uh obviously copper, you know, kind of the industry maximum, copper when you can, optics when you must, you know, you're kind of framing it the opposite like ideally it' be optics when you can and only copper when you have to.

Um so talk to me about like scale up. And now we're going through the industry is going through an inflection point where as we go to these higher speeds, the reach of copper shrinks and shrinks and shrinks because as you said earlier, copper just can't handle really high-speed signals very well for very long distances. Um, but should we be concerned about uh, you know, lasers, temperature, reliability when when you're talking about connecting, you know, 72 or 144 GPUs within the same rack?

Yeah. So that's the typical uh the the traditional argument against co-ackaged optics because they're like wait uh lasers fail all the time and lasers are extraordinarily finicky uh components because if you think about the way a laser actually works it's basically uh has something called a band gap right so there is like an electron that goes from one band to another it's called the veence band and the conduction band so whenever the electron transitions between these these these states it it emits light. That's that's how lasers essentially work. And the thing is when you subject this thing to temperature uh this energy difference changes and when the energy difference changes then automatically that translates to a different wavelength of light that comes out right.

So it's not very stable if it's like temperature changing all the time. That's one big problem. The second problem is that whenever this thing gets heated up, right, uh its order it its lifetime drops by orders of magnitude like ridiculous like it drops 100 times if you like run it very very hot. And uh so the people have been always arguing like you know you can't put lasers right next to this switch chip which is burning I don't know like uh like a 100 watts of or several hundred watts of power like what's going to happen to the laser.

So the solution the industry came up with for this is that we'll take the laser and we will not put it into this co-ackaged switch no optics in the switch or near the optical engine. We'll only take the laser and we'll put it outside of the optical system like far away like where the rack connects and then we'll draw an optical fiber uh which also is a specific kind of optical fiber because it has to be it has to maintain the polarization of the light that comes through. So it's called a polarization maintaining fiber. So that has to come in and then that feeds into the the co-ackaged optics chip or the optical engine.

So the laser is never kept on top of the actual co-ackaged silicon photonics chip that is sitting right next to the hot ASIC. So these modules are called external laser sources or ELS modules and it's fantastic though because uh it solves all these problems of like lasers and actually meta's uh studies I think they showed in like last year's open compute project OCP uh in 2025 showed that actually they actually have really good reliability. So this may be actually a myth that it's actually terrible. It's it's actually pretty good.

And I've heard like Saudi CEO say that oh co-ackaged optics reliability terrible don't do it but it's actually not so because the industry has solved the problem in these ways right fascinating that really interesting so yeah by taking the laser and not putting it near that heat source but keeping it external then it kind of solves the problem it does have to deal with all the temperature variation and the degradation. Um, so okay, if the sign if the laser is further away, that makes sense to me when you're sending the signal down to the ASIC. What about sending the signal from the ASIC back out? Like how does that work?

I think I'm missing a piece. So in the reverse path, how this works is uh you have the laser light that's coming in from the outside. You know, think of it as a a light source, you know, a a laser that's all would have been on chip, but it's not except that it's coming through a pipe. You can use that light to do whatever you want.

It could have incoming [snorts] um you know uh it it does not have actually any data. What it actually contain it it is just a simple source of light. It is not a modulated source of light. It doesn't contain any data.

It is literally a flashlight that's just like on.

What you choose to do with the light is up to you.

Gotcha. So it's like the like a drive light sort of. Yes.

And then the modulator sits outside.

Exactly. So this is a very important uh distinction because when you talk about a pluggable transceiver, you've got the laser on the pluggable transceiver and then the modulator is on it. So that's what the externally modulated laser does. So you have a laser chip that's sitting next to the externally modulated laser and then the externally modulated laser will take all the information and make it zeros and ones and then you know turn on or turn off the light to encode it into light signals.

Right? But in co-ackaged optics with an external laser source it's not a modulated light source. It's literally just a dumb piece of light called a CW laser. It's a continuous wave laser

and it is just like sitting there and it comes into the silicon photonics chip and you can do what you will with the light you know it's up to you. So that's how it works.

That actually brings it to another point because these co-ackaged optics light sources require to be high power. So these are actually called ultra high power CW lasers and they require to be about 400 mw which is actually lummentum specialtity also here because they have a really good uh external laser and they actually I think they have a product too. They assemble the entire module I think and uh you can just like plug it in. So which is a fantastic business model for them.

They make the lasers they make the high power lasers. Coherent also makes high power lasers which is the other company that is a laser supplier in this market. Although Lumenum seems to be the incumbent here really. Coherent is still trying to play catch-up in this in some sense.

So basically that's how co-acked optics works. You know you it it has special laser requirements that is different from what we have seen in pluggable optics so far.

Gotcha. Super helpful. So let's let's shift to talk about some of these companies. So, last week, Lumenum had record revenue.

I think it was $665 million revenue up 65% year-over-year, and they guided to a whopping 805 million next quarter alone. Um, so obviously they're on fire. Um, we had like Tower Semi, um, they reported earnings and said that they're building out almost a billion dollars worth of silicon photonics and silicon germanmanium capacity. And 70% of this plus is already pre-reserved.

So customers are just paying them to build it out. Um so talk to me. Let's talk about some of these companies that make lasers, that fabricate the lasers. And actually I have a couple quotes.

Um so maybe you can talk about demand and supply. So I noticed on Lumen's call, uh these are some great quotes. So the CEO said, "We are under shipping our customers demand by somewhere around 30%. " And then he went on to say even as we've added 20% additional capacity, the demand supply imbalance has increased.

So he's saying we can't keep up with demand and even though we're adding capacity, it's actually getting worse. So demand is like in accelerating. It's faster than we can we can keep up. So why is there this demand supply imbalance?

And yeah, who are some of these companies that are at the forefront and are set to benefit from it? Okay. So, one thing to understand about lasers and manufacturing and this supply demand thing is that these lasers are uh typically made on indium phosphide substrates which is another bottleneck on its own. uh there is you know you can't find enough indium phospite lasers and on my substack like last late last year I spoke to a professor Martin Hec who also mentioned this uh and we spoke a lot about these kinds of lasers and indium phosphide uh basically indium phosphide wafers are actually built on 3-in wafers that's what lumenum builds upon now come think about so if anybody who has not heard about this or it doesn't make sense why this is big deal.

A silicon wafers are made on 12-in wafers, right? So, when you have a diameter that's like four times bigger in silicon, uh you can basically get four square or 16 times more capacity from a single wafer than you would, you know, with a 3-in wafer. So, fundamentally, you can't you can't make that many on a single chip. Now all of a sudden you want to power entire data centers with light.

You're going to make them on these little bit like stroop waffle looking things. It's terrible, right? Like and so uh you just can't make too many of them. And the second thing is that it's not like you can it's like it's very different from a silicon manufacturing flow.

Um it requires a different set of equipment and the materials are different and therefore there are only a few people who who typically do this because the industry has only built up the capacity to be um what it needed at that time. right now. Seemingly everything has jumped and the the the supply has not caught up because if you do make a new fab which I think these these these uh companies are building out new fabs in in all these locations uh it takes time to bring them online and qualify them which is easily 6 to9 months. So when you suddenly have things like this, you can't you know global indium phosphide wafer capacity starts are like maybe a few thousand wafers per month or 10,000 wafers

but you know if you if you see silicon wafers they have millions of starts wafer starts per month. So it's like a entirely different ballgame and coherent actually has a 6 in uh wafer fabrication facility that they are bringing up but the word online is always that they don't have yield. I have spoken to so many people right now like trying to find out what are the factors that determine yield and why 6-in wafers should have less yield because when I spoke to professor Martin heck in that interview he said 6-in wafers actually are flatter like the bigger wafers are actually easier to do because it is also closer to what the legacy silicon equipment used to do because the legacy six silicon equipment was before 12 in it was on 8in wafers and before 8 8 in wafers it was on 6in wafers. So there's a lot of legacy equipment left behind there.

And it's all well understood technology. So I never have understood why coherent has this supposed uh yield problem. I never understood the reason.

But anyway, they're still ramping on that technology. And when they do it's interesting because they the whole thing is that they can make uh you know let's do the calculation again like the area uh has gone up a little over two times right because the diameter has changed 1.5 times which if you square it is like 2.25 times diameter and you can make that at like roughly half the cost as well. So coherent has the capacity to flood the market with indium phospite lasers if they can find enough wafers around it

because of their six inch supply. So

interesting

if they catch up I think they can they become very interesting player in the market. I don't rule them out completely.

Ah fascinating. Yeah. So this is a different dynamic than in silicon logic chips where no one is going to double their capacity quickly by making the wafer bigger. But here there's an opportunity with this compound semiconductor indium phosphide for someone to actually make the wafer bigger and truly get double the capacity without needing to take 12 24 36 months to stand up you know new fabs.

So is is the wafer frontend tooling all from the same suppliers as the silicon supply chain? Is it just that indium phosphide you someone else someone supplies that wafer but like are you still buying deposition and etch tools from the the same names?

There are specific uh deposition edge tools for compound semiconductors and uh there are companies that specifically deal with this too and they are also in the limelight because of these things. Uh sure I don't want to point them all out right now. The only reason is I might get some of them wrong. I don't want to.

Yeah.

Again, maybe we should

disclaimer all of this is that these are this is not really investment advice. So don't know don't buy anything based on what we say here. Uh do your own research. But yeah, but yeah, you need a different set of equipment to do this. You know, it's compound semiconductor deposition is fundamentally different because the materials are different and therefore you need different wer equipment.

Yes. Yes. Totally. Okay, man. We've covered a lot of ground. So what else should we hit on before we wrap it up?

So you we one thing we didn't really uh mention is this entire new world of what are called optical circuit switches which is another lummentum specialtity. You know what they are are basically mirrors a whole bunch of mirrors and these mirrors are just like turned around right like to reflect light and whatever. uh those optical circuit switches couple of years ago was not even a market like nobody even cared about them in fact Google used to use them in their in they had an in-house uh optical circuit switch that they used in their initial uh TPU pods because you need TPU pods you know to you need optics in a TPU pod so this is a topic for another dis you know another day but Google was the earliest user of optical circuit switches And uh it turns out like last year like OCS the market has exploded and like tons of money has is going to be made based on this and the backlog for OCS is like $400 million for Lum just for that. And it's it's really I think it's the fact that like Google has now gone to external suppliers for their OCS switch

uh really is a big deal and they are investing so much. We spoke in our last capex you know explosion episode where there's so much capex being you know built out TPUs are being built out and uh they require optical circuit switches and not only that actually a lot of these uh uh switches that do uh you know top of rack kind of stuff are also being the switching part of it right is also like they're considering using OCS in that part of it now and the reason for that is that typical network switches they work based on like packet switching. So

the the switch receives a packet and then it looks at it like okay what do I do with this packet? Oh I have to send it through this port. What do I do with this packet next? Send it through that port. But that is only useful if like the configurations are changing all the time. But in data centers especially when you're doing a training run you kind of know how to connect GPUs up together beforehand.

So they don't change all that often. So what you can actually do is you can use these OCS switches up there that are much lower power because they don't change very much. And because moving the mirror takes time, you don't have to move it all that much. You set it and forget it. And so

let me interject here for for listeners if it's not clear.

Traditional packet switch switches that's in the electrical domain. So if you have optical fiber coming in, there's the whole transceiver thing that we talked about. So your optics come in, it has to be converted to the electrical domain. So optical signals converted to electrical signals.

Then those um electrical bits, you know, tell you what's in a packet and then the switch decides where that information needs to go and then potentially it would have to get converted back into the optical domain depending on where you're sending it or it stays in the electrical domain. And so what Vic is talking about here too and part of why it's lower power is you can just have optics coming in and little are they MEMS's mirrors or

Yeah. Yeah. Yeah, little MEMS's mirrors. So, they're really small. Um, and then the information stays as optical signals and then just essentially bounces off the mirrors and travels to where it needs to go. So, that's part of why it's lower power is you don't have to convert back and forth.

Yes. And coherent has a switch too, but it is it works on basically a slightly different technology called liquid crystal displays. So, it's not really the men's mems mirror approach. So, coherence approach is slightly different.

Gotcha. So uh Google TPUs are the sort of flagship customer here. Are other hyperscalers talking about adopting OCS?

Yeah, I think so. I think that's the that's the reason why uh there's so much talk about OCS because people are trying to adopt it outside of the TPU uh ecosystem as well. So that's why it's so important and u I think signal AI uh like upgraded their forecast for um OCS like by a factor of three or something uh because there's just so much demand for OCS these days.

Yeah. And that's just for this year. Okay. So we'll have to keep tracking obviously we'll have to track scale across scale out scale up CPO uh AEC's copper versus uh uh optical and we'll need to keep track of the OCS market which seems to be just taking off.

Yes, there's a lot we will be revisiting this a lot because um I don't know if it's this episode got a little too technical too fast. Uh there's a lot of physics and a lot of stuff going on here. Uh it may be a little little hard to follow. Uh but you know that's how this business is. It's this stuff is complicated. But if you have any questions I think like we can always leave it in the comments. We'll try to answer after the fact.

Totally. Yes. Listeners listen to it a couple times. Um read everything Vic's written about it.

I've got some very high level intro stuff as well. And then yes, leave comments. We'll try to respond and we'll come back to this. We'll go more into the companies in the future.

But I hope you liked this technical deep dive. I hope you're as excited about optics and networking as we are. I think uh 2026 is going to be a big year for for this part of the industry. And with that, we'll call the wrap.

Thanks for listening. If you're enjoying semi-doped, we'd love you to give us a fivestar rating and a quick review on Apple Podcast, Spotify, or wherever you listen. A lot of you are on YouTube. Thank you.

Um so subscribe there, share it with friends. Thanks.
