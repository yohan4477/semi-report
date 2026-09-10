---
source: https://www.youtube.com/watch?v=aIX5Sku2URI
title: Credo + Dust Photonics, XPO, Nuvacore
date: 2026-04-17
kind: transcript
note: 유튜브 자막에서 옮긴 전사. 화자 바뀜(>>)마다 한 줄. 600자 넘는 발언은 문장 넷씩 더 쪼갰다.
---

So, CPX is the socketed CPO where you can put anybody's optical engine and socket it and close it down. Like you know you put a CPU onto a motherboard, right? Welcome to another Semi-Doped Podcast. I'm Austin Lines of Chip Strat and with me is Vic Shayker from Vic's Newsletter.

Hey Vic, what's up today, man? I don't know. How's it going with you? It's like so much stuff happened to Semi.

I don't know what to start about. So, I get like this analysis paralysis and be like, I don't know. Is it like Credo acquisition of Dust Photonics? Is it like Broadcom's deal with Meta to make chips?

I don't know. There's so much to talk about. But I suggest like we we trim the scope of this thing to keep it like tame. And let's just talk about photonics today because there's like so much photonics stuff going on.

But before all that, did you see this piece of news about this company called NuVia Core?

I mean, I saw something on Twitter, but it's like you said, there's so much going on right now. It just went right past me. So, let me let me explain. This is kind of close to me in a sense.

So, what NuVia Core is, it's a new CPU company, but it's founded by the same guys who founded NuVia, which is the CPU company that Qualcomm bought in 2021. And it turned out be really good thing for the company because they kind of made it into the Orion series of chips and CPUs that like run on laptops and such. And it was kind of the core of their whole argument with ARM and the lawsuit about whether it was okay to use NuVia's architecture and the ARM architecture's licensing agreements that NuVia had. Was it okay to move over to Qualcomm and make their chips?

So, I don't know if you remember the whole lawsuit thing.

Yep. Yep. This was the contention of the whole thing. Uh I think like I was it like last year?

Founders actually quit Qualcomm. And everybody was like, wait, what's going What's everyone doing? And then I think people watched Gerard Williams, who's one of the founders of NuVia, painting his room. He's like, yeah, I'm just painting rooms now.

Whatever. This relaxing. And everybody's like, why is Gerard This is Gerard Williams you're talking about, you know. He's like ex-Apple also.

And he was part of the M-series processors. And then like he founded NuVia, sold it to Qualcomm. And wait, why is he painting his house? Like I guess that's what you do when you win the game.

Like apparently not because now it's like NuVia Core is the new CPU company that is going to guess sweep in and uh you know, provide CPUs for the agentic AI era. I'm not exactly sure what it is, but we have a new CPU player in town. And I'm not sure they have a product yet, but it's it's exciting to see the same guys try this one more time because why not? They sold a CPU company before.

They can do it again. Interesting. There you go. Yeah, where my head goes is like, okay, cool.

Respected founders who had done this successfully before at Apple and Qualcomm. Um makes sense if they're just kind of doing something similar, but probably different. Obviously, CPU demand is super high right now. It will be interesting to follow and ask the questions like who are their target customers?

Presumably hyperscalers. Now we we've got Intel AMD, but then we also have ARM and Nvidia. And then to your point, you know, there's the Qualcomms and there's, you know, everyone making their own ARM-based chips. And so another CPU, it does raise the question of like, what's different?

Who's going to buy it? What are others not doing that these guys believe that they will do differently? So, this will be fun and interesting to see what happens. Yeah, lots of questions.

And in the CPUs for agents and agentic AI era, it's really a question that I have gotten many times ever since I wrote my CPU article. From many people, investors and professionals alike, about what kind of CPU is the best one for agentic AI. Is there like x86 and ARM? I know we spoke about it.

And like, wait, ARM is coming up to speed in the whole server era. And people have also argued with me about like what kind of software really doesn't work on x86 and or rather ARM and what kind of software works only on x86. And I've been saying like yes, there's some legacy stuff that happens. But I think it has come down to something very simple right now in the CPU space.

The supply for CPUs is so short, the demand is so high that even normal cloud providers are not able to get CPUs anymore. The force of AI has taken over all CPU chips now and like nobody gets anything for anything else. So, the best com chip for AI CPUs use, you know, is the CPU you can actually get your hands on. It doesn't matter if it's x86.

It doesn't matter if it's ARM. It doesn't matter if it's Intel, AMD, Vera, Graviton. I don't know. Like whoever can make these things fast enough, people will write code software to port it over and get it done it is so much in demand.

Yes. Yes, that is a really good point. It's not about what is the optimal chip, it's about what is the available chip. There's lots of questions that I have to untangle eventually and hopefully we'll hear it from the CPU designers themselves, which is getting deeper into the workloads of what is the GPU orchestration that has to live on or close to the head node.

What is the actual agentic workloads that's doing tool calling? And then what about CPU orchestration like agent orchestration? And where where should all of these live like with respect to latency of like talking to GPUs quickly cuz even if you're doing agentic stuff as like general purpose as it is like, oh yeah, it's just running code. Every step is inner is like ping-ponging with an LLM.

I tell it, hey, I want to write this code and it goes to the LLM and then it comes back. And then the CPU might the LLM's going to write some code. The CPU might execute it for me or something. But there's this constant ping-pong.

And so there's this in to me something I'd love to understand better is just like that that's obviously like there's some latency there. And so I'd love to get deeper into what are the optimal designs for the different workloads? Is it, you know, Nvidia, it's kind of like a one-size-fits-all. It's like we have a CPU.

And it happened to be our head node CPU. And now we're going to have racks of them, you know. And so I would love to pull on that thread more. And I know you've written about it.

But but getting much deeper and I'd love to hear from people who are actually using these agentic CPUs. But do think there's lots more to be talked about from all the different players. I think like they were pretty early on in the game of agent CPU, agentic AI.

Yeah, for sure. So, we really have to keep a tab on this stuff and see how it evolves because it's a new space for a lot of people. And I was watching the interview that Jensen had on Dwarkesh podcast. And he was explaining things about so many things.

A good podcast. You should really watch it if you haven't. And I think the EDA tools are going to get very sophisticated. There are going to be agents running all kinds of EDA workloads.

And Cadence and Synopsys are going to sell more licenses than you can ever imagine because agents need to use licenses to do stuff. And he says engineers are going to deploy tons of agents. And the reason this hasn't happened yet is that we haven't really figured out how this tool calling with CPUs really works yet. We're still working on that part.

Once we figure out how CPUs will really orchestrate and work with a wide variety of tools, there is so much untapped potential in what agents can do when they start calling tools, really calling tools, that the best is yet to come. So, we have to wait and see how this evolves. And I'm sure we'll keep talking about this. But like we promised, maybe we should like go and talk about photonics.

Because CPUs are cool and all, but you know what? Everybody does photonics now. Talk photonics or you're not cool. That's right.

Let's talk photonics, man. Let's see. Should we start with the Credo acquisition? Yes, we should.

I did so many Substack articles on this. And everybody has been writing about this. So, definitely this is something we should at least talk about because it's very important in the frame of what Credo has been typically viewed as versus what they are viewed as now. Yes.

Totally. Impact to the stock, impact to the narrative. And lots here. Let's start at the top.

So, Credo acquires Dust Photonics for $750 million cash upfront and almost a million shares and an earnout as well on top of that. So, the total potential is I just over a billion dollars. I had never heard of Dust Photonics. What did you learn about them when you looked into them?

Yeah, I had not either. But apparently this is a company that was had investors like Actuaries Management and Gavin Baker behind it. Seems like they are founded in 2017. They're a Israeli company that is fabulous.

Which is interesting because the moment you say they're fabulous, you have to ask, so who is the fab? And in all likelihood, it's Tower. So, there's like this common beneficiary of Tower Semiconductor becoming the photonics TSMC. Still that narrative keeps happening.

Anyway, they have about 70 employees. And they've been doing photonic chips. They have this whole photonic IC portfolio that does all the way 400 gig, 800 gig, 1.6 T.

They have a roadmap up to even 3.2 T. So, they're a very interesting company. But to me it seems like, yeah, they have a couple of core IP.

We'll talk about it for sure. But essentially they're a photonic IC company that seemingly has some hyperscaler design wins already. I don't know what it is exactly. But seems like it's a successful company that was basically up for grabs by somebody like Credo.

It's a match made in heaven because it brings all the abilities that Credo doesn't have right there and becomes like a perfect synergy between what Credo offers and what Dust Photonics does as photonic ICs. So, it's a perfect match. Yes, so let's go into that. So, everyone thinks AECs, copper cables.

Credo has strong serdes. I think they actually started just licensing serdes IP, but then they moved into the AECs. They kind of pioneered that and made the the end-to-end cable. They also have DSPs, optical trans and optical transceivers, the zero flat optics.

So, tell us as Credo started as as more of like they're an interconnect company, but they started on the cable side. They've been moving into optics. So, how does Dust Photonics fit into who Credo is becoming and where they're headed? Credo is one of those copper cable companies that is also vertically integrated within the cable section.

It's not like what Marvell does, for example, on this front because Marvell makes these like DSPs and they make the active electrical portion, you know, the the things that do the forward error correction and the amplification and the equalization and all that at either end of the cable, but they don't actually own the cable. Credo does the cable, too. So, they're an end-to-end cable provider, which is why they were so popular in all those purple cables we've seen in the past. And they basically are useful for scale out.

Like scale out is basically Credo's bread and butter, really. And even their optical um interconnect portfolio, the ZF optics, is for scale out. And that is their you know, their hottest area that which they provide the best solutions for. And then they have this zero flat method where they have this thing called pilot, I think, the software platform.

It monitors all the link health, telemetry, and all the metrics that comes from whether the link is on or not. And then it reports back via software screen, you know, a interface where you can see which link is going to go down and like replace it preemptively. This is becoming more and more it's always useful to contrast this with Marvell, also because Marvell has a similar thing called Reliant, which is a telemetry system where they monitor link health and all that. So, this is where things are.

So, they have excellent serdes team. They have been doing serdes design for copper cables, of course, and they have optical DSPs, so they do it on that side as well. Now, the acquisition of Dust Photonics brings in the ability to make photonic ICs in house. That is something they did not have before.

So, this was this fits right in into the missing portion of Credo's optical portfolio, which means now they can compete on anything that you want, near package optics, linear pluggable optics, co-packaged optics, whatever that you want. If you can make silicon photonics chips and you have the ability to drive them with serdes circuits and you know how to now monitor telemetry and you understand how all these interconnects fit into the context of a data center, you have yourself a powerfully integrated vertically, you know, a vertical stack of technology that goes all the way. So, that's why people love this a lot and the stock has been up like I don't know, 50% over the last week. And typically Credo has been synonymous with copper so much so that when the CPO news came out, the stock has been dropping.

On this podcast we have maintained that copper is never going to go away and we are always pro copper and pro optics because they both have their uses and needs in the data center. So, to me this is great that it is vertically integrated now, Credo as a company, but I always was never very happy with the whole sentiment of Credo equal to bad because copper going away. Totally. So, okay, let me pause you here and ask a question.

So, why does Credo need to own the silicon photonics picked as opposed to source that from some other vendor? What's the bene- benefit to being fully vertically integrated there? Well, there are a couple of things I can think about, actually. The first uh thing is that when you own the serdes, you might as well own the design of the chip itself because you can optimize all of this in one go.

And then the second thing I can think of is the supply chain issue. You're not here waiting for somebody to make you photonics chips. Mhm. Because everybody is trying to service their own needs.

It's not entirely prudent to try to keep sourcing chips from other places. So, if you own the entire design flow end-to-end, then you can provide a complete solution to somebody who says, you know, you don't have this. Optics is the way to ahead, but, you know, CPO is coming, but Credo is not ready for it. How are you going to address this this CPO world?

So, if you have your photonics solution in house, then now you know that question is answered.

[laughter]

Yeah, that makes sense. And I guess it also allows you to caption capture more margin. I'm I'm thinking about comparing why did Credo do AECs vertically integrated versus Marvell who does the DSPs, but then Marvell has to partner with an ecosystem of people who will build the cable and bundle in the Marvell AEC. And one potential trade-off with that is the customer.

Sometimes I think for these hyperscalers when time is of the essence, like one throat to choke, the idea of one throat to choke, just one one vendor that I'm working with is actually pretty nice. You know, you're going to get the whole thing. You don't And then when there's a problem with it, you know exactly who to talk to, right? And so, I can see that strategy obviously worked for Credo with AECs, so it makes sense that they continue that strategy and continue to differentiate from a Marvell or whoever by owning all the components so they can do silicon photonics as well.

And and and and basically own the whole sort of end-to-end system. So, Credo not only do they have AECs, now they have silicon photonics. And how should we think of that in terms of also owning Hyperloom? Is that who it was with the micro LEDs?

So, they've got a strong copper play and now as they go into the optical play, it feels like they can both stick with the like current laser route, but also there's the micro LED route. So, kind of explain more of the differences and why they would want to own both. I think that the context to all of this comes from Gavin Baker's tweet on this whole affair, which is amazing. And I think we should link it in the show notes.

The reason is he explains clearly like where all this falls now given in the optics world. And interestingly, in his tweet he says that micro LEDs is picking up a lot of interest from hyperscalers and they're being very open to it. And this is the same message that I got when I spoke to some of the micro LED guys myself. And that's why I started writing about it on my substack, too, because I don't think this is out of the running yet.

And this is something we can even talk about a little bit more in depth, but micro LEDs are an option where we could put, you know, this slow but wide approach. You know, micro LEDs can't run really fast on a per lane basis. They are not like lasers. Lasers can run at 200 gigs modulated waveforms data rates with the the PAM4 modulation, but micro LEDs can't do that.

They run at like 100 the speed. You can you can run at 2 Gbps or 4 Gbps or at most 10 Gbps, something like that. So, you put a lot of strands of fiber next to each other and make it like a big pipe. And that's how you communicate at like 1.6 T. It's a far simpler technology and it's it's an ongoing piece of work for me to understand the thermal effects and the reliability effects in my micro LEDs. So, all of these benefits exist. And so, I don't think it's out of the running yet, but it's interesting that Credo also has this active LED cable ALC technology based on their Hyperloom acquisition from late last year.

Think about it, right? They have everything from copper interconnect all the way through micro LEDs, which is not really optic, not really optics optics, and not really terrible like copper. Then they have the optical portfolio that is like ZF optics that goes up, you know, like to longer reach. They also have the ability to do like photonics and near near reach for CPO or NPO or LPO.

So, they have now the ability to do all of this stuff. Gavin Gavin, I like this because he says copper is not going away. Copper is going to stay till 2030. It is simply the choice because all of these things going up in speed and in interconnectivity and all of that.

If you just think of the Ruben Ultra, they solved the problem of copper interconnect by putting a midplane PCB. A midplane PCB basically is like a burger, you know, like the the burger patty is the PCB. One bun is the computer chips. The other other bun is the networking chip.

So, your interconnect path just got super short. Like it just goes across the PCB. And that's it. And that's why you see Ruben Ultra, you see him, you know, the thing is like vertical cuz it plugs into the PCB like this.

And then the other side it plugs in like this. If you're listening in the audio, I'm just holding up my hand and like showing how things plug in, but basically, you know, it plugs in from either side of a PCB. So, that's why I think that copper is here to stay in some form of an or the other. You don't have to think of it like copper cabling all the time that goes through the spine and all that.

That is evolving. The second thing that he highlights in terms of like a three-year growth span for interconnects is actually scale across. I was surprised when I saw that cuz I thought like it's CPO and all that is going to come up immediately. And I thought scale out would be first.

Because CPO is first use of CPO is in scale out. It is not scale up. You'd be very clear about that. That's not going to be in scale up.

It's going to be scale up. So, what he said scale across is the next big growth vector for, you know, interconnects. And I'm like, I'm trying to think to myself, why? Why is that?

My hypothesis, my understanding is that, you know, when you think of a myth or scale model, 10 trillion parameter model, and this is going to be the future, like you're going to have to train these things on massive clusters. The training models are becoming more and more complex. Of course, myth house was not trained on this. I think myth house was on on tranium chips, actually.

As far as I understand, myth house was straight

Yes, yes. There's a lot of people saying, "Oh, it's the first Blackwell class trained model." But then, I believe someone from AWS, Matt Garman, or somebody was Andy Jassy, even. Someone said, "No, no, no, this was trained on tranium." Yeah, yeah, it's not Blackwell class, right? I mean

Yeah, yeah, yeah. So, anyway, regardless of what you're using as CPU or in or from which vendor, you need massive data centers with incredible number of chips to train models like this. And with the power constraint and land constraint, you're not going to have it in one place. So, you're going to have multi-data center training, and this is already in place, like Google's been doing it.

And to do this, you need scale across. It is very interesting what scale across needs, because you need coherent optics. You're not going to do it with just regular old optics. You need coherent optics, which means the modulation requires both amplitude and phase.

It's not simply on-off modulation that you see in shorter region interconnects, which is often called IMDD, right? Intensity modulation. But, you can't do that in scale at that reach, you have to do coherent optics. And it's very interesting.

So, who does coherent optics then? The biggest players are like Ciena, right? I think Cisco does it. And who else?

Yeah, I can't think of anything else, but like yeah, it's not coming to me right now, but I have to go look at like long-range coherent optics again. But basically, that is the second big growth vector. And finally, he says like, yeah, scale out. Yeah, you know, scale out is basically still can be copper.

This is still can be CPO or whatever. But yeah, that's that's where we lie here on the interconnect space. So good and interesting. And obviously, Credo wants to play.

They they play in scale out, and they want to play in scale up. And so, would you say that their portfolio now is better positioning them to play in scale up between like micro LEDs and maybe with the Dust Photonics acquisition? Yeah, yeah, they can play across a lot of different things. Again, some of these things I'm still unclear about, because micro LEDs I feel like I'm not really sure if still about whether it's like a scale up or a scale out in a application, really.

Cuz the reach is better than copper, but you know, it can be pretty low energy like copper. So, that is a little bit like sketch for me, like where it's going to be used. And I think people are still working that out. Yes, yes.

Apart from that, the other company that comes up comes to scale across now that came to me is like Nokia. Nobody thinks of Nokia. They they acquired Infinera, right? The the company for that does a lot of optics.

So, Nokia is actually a big name right now. I mean, if you're not paying attention to Nokia, you probably should. They're doing some good stuff. Even Ciena, like look at how they're doing, like Ciena is interesting.

Totally. So, scale across is really an important scaling factor that is not often spoken about, because it's probably not as fancy. But I've always told you that I like the scale across aspect of optics the most with coherent optics and all that. It's very fancy, where you send like complicated waveforms and modulation schemes, and you know, many, many, many bandwidths by wavelength division multiplexing and uh it's insane here the how that works.

I'm I'm Googling quick.

Marvell has a scale across play from some old acquisition. I can't remember exactly who it was, but Marvell has a portfolio as well. I guess we should probably do an episode just on scale across sometime or going more into it, because some listeners probably hear you say the word coherent, and they probably think of the company Coherent. Um so, probably worth actually explaining what the word means and and, you know, getting more into it.

Yeah. Going back to the Dust Photonics thing, I wanted to add like one thing about Dust Photonics. They have one very interesting technology IP called L3C. It's called low-loss laser coupling, L3C.

And this is unique to them in the sense that they can put any CW laser, any continuous wave laser, right next to the photonics chip, and connect it up, couple it into the photonics chip without any loss, I mean, very low loss. But more importantly, without an air gap, okay? That is very, very important. Because the way Marvell does it is they put their laser on top of the PIC, and like they bond it in or something on top, okay?

So, this is different. If you're putting the laser on top of the chip, you have to acquire the laser, and you have to work with that supply chain. And here, you can put whatever laser you can lay your hands on and then couple it into the chip. So, low-loss coupling is interesting.

The reason that there is no air gap, and why that is interesting, is because if you don't have an air gap, you can put this entire thing into a liquid cooling environment. Think about that for a second. If there is air in between, and you put it into a liquid cooling environment, the liquid cooling liquid goes between the coupling fiber and the PIC or whatever, and changes the refractive index, and it messes up the loss profile. So, why is cooling important?

Now, that I think this leads us nicely into our next topic, because there is this new interconnect housing for optics called XPO. Now, XPO is the successor to the OSFP module. OSFP module is simply this cartridge-like thing, which fits into the front of a network switch, and you see many of them in any picture you'll see this cartridge going. And then you see the cable coming out of it.

This cartridge contains all the electronics, the optical transceivers, the AEC, you know, whatever, a 30 circuits, all of this stuff. That was like in 2016, right? Now, this XPO, which stands for extra-dense pluggable optics, it was introduced as by Arista Networks at like OFC this year, 10 years later. And it's as important as you would imagine OSFP was 10 years ago.

But people aren't really talking too much about it. And I think it's very important. The reason XPO is so important now is because per bandwidth of XPO, but like per connector, it acts as if this is like eight of the OSFP connectors, the previous gen. It's like you can put eight of them together in one connector.

It is that much bandwidth. You can get 12.8 terabits per second out of single connector. Think about that.

For an OSFP, you would only get like 1.6, right? It has 64 channels times 200 gigs. If you multiply that out, you'll get 12.8 T. And it can support 400 watts of power dissipation. And the reason it can support 400 watts of power dissipation per connector is because it allows for liquid cooling. Okay, so now this ties into why Dust Photonics is so important, that it's it's L3C technology does not have an air gap.

And that now it can actually be liquid cooled and put into an XPO module that couldn't be done in the past. Fascinating. Okay, so with XPO, we're able to bring liquid cooling actually to the transceivers ports themselves. And zooming way out, why would we want to do that?

Well, we've already started liquid cooling the data center and trying to cool off the GPUs. And I guess at this point, as long as you have the infrastructure of bringing liquid all the way in, you might ask, "Okay, now the GPUs aren't quite as hot, or they can still be as hot, but we can just cram more of them in because now we can dissipate the heat better. What else could we liquid cool? And so, this must be going down the path of trying to liquid cool every piece of electronics that you can to just have higher and higher power and and do do more.

And so, now you're saying, "Okay, well, what if with this XPO, we can cool these optical transceivers? " And then, to your point, it means that the technology that's actually used under the hood needs to be built in such a way that it can be liquid cooled. So, Dust Photonics is with their L3C or whatever it was called, that enables no air gap, and and which is amenable to liquid cooling. And so, it's just kind of like pulling on the whole supply chain and going under the hood and asking, "What can be liquid cooled?

And if we liquid cool this thing, what of its components needs to be changed to make it work better and or work at all in a liquid cool environment? " Fascinating. Yeah, so that's the tie-in to XPO and Dust Photonics, right? That's something I was thinking about.

But then, I've been looking at XPO itself in more detail, and it's very fascinating. XPO can support everything from, you know, DR, the data center reach, you know, long reach, all the way to ZR, which is the longest reach. It can do coherent light. Um and apparently, it can even do like micro LEDs.

And if you think about wait, you know, why are we talking about a new connector? And okay, sure, there's like a multi-supplier agreement, right? What is it called? MSA?

And that so many people in many people in the ecosystem can make things and not locked in to anybody. If you look at XPO, actually, like 100 companies have signed up signed up to be part of this XPO movement, right? Yeah. Ask yourself, why are people doing this?

Why do we need a new connector? Yeah, and wait, aren't we going to CPO? Like who wants to put 400 watts in a It seems like you're going the wrong direction. Don't we want to save energy?

Like why are we going talking about cool liquid cooling 400 watts? It kind of seems like we're going the wrong direction. Mhm. CPO is the way we are supposed to go, right?

This is the essential tension in the industry right now. Do you go to CPO where you use lesser energy per bit and all of that stuff? However, you are locked into the ecosystem that is there around the switch silicon chip and the co-packaged optics within it, which is done only by a couple of people. Like Nvidia CPO is doing this, Broadcom CPO is doing this.

What about Microsoft? Like I mean like Are we all like or is all networking going to be beholden on the to the people who can do CPO with the networking switch? Like will Microsoft now have to go buy Nvidia stuff now or like so it's a lock-in to the ecosystem around CPO. And there are like a bunch of other like complexities of the supply chain and things like that.

XPO is the industry's resistance to CPO. It is the way of saying like hey, if you want more bandwidth per port, here's how you do it. It gives you all the benefits of all the technologies you're used to in the past. You know, if a transceiver fails, you just remove it, you put it away.

You know, and you put in a new transceiver, no problem. We can do all the telemetry stuff. You're used to doing this in data centers. You've done this this approach in data centers for decades now.

So, what does the connector of the future look like for the power density and the thermal requirements of AI data centers of the future? XPO is the answer to that. Mhm. XPO is what you need to run traditional pluggable interconne- interconnection in a data center for a massive number of chips for AI applications.

CPO is a complexity that you don't need. Mhm. And it's in Arista's interest to do this because if the whole networking layer like goes into CPO, then what is Arista going to do? They have their EOS software layer, which is like a really amazing sticky moat they have.

But what about the hardware integration part? Right now they buy the switch silicon from Broadcom, right? And then they build PCBs and they build the racks and all of that stuff. But if the networking portion, even the interconnect portion, the optical engine goes into the the chip that Broadcom is making, what what is the what's Arista going to do?

Just like put them in metal boxes and ship them and like what? And then like put a little bit EOS on top? It's a slightly losing proposition for people like Arista. What you actually want to happen is everybody goes XPO.

If everybody goes XPO, we have a new ecosystem around this connector that opens up a whole lot of doors and so many vendors and so many supply chain players that CPO does not offer. Fascinating. Yeah, this is strategically very interesting, which is to say there is a horizontal ecosystem around pluggable transceivers and those players the the value shifts when it goes to CPO and it becomes much tighter integration to like the switch silicon people like Broadcom or Nvidia. And so the players who are in the ex- isting transceiver linear pluggable LRO supply chain and market, they would rather extend their own road map rather than see CPO come because maybe that would be the end of some of their road maps and maybe they don't have as much of a CPO play or as much value to to add there.

And therefore XPO is a way to continue their road maps, continue their place in the value chain and their importance in the world. And then then to to your point, Arista already buys Broadcom chips, but they do a lot on top of it especially at the software layer, but if more and more is shifting into Broadcom, that's probably less and less for them where they add value. And yeah, fascinating.

There is another aspect we won't get into today, but we should talk about it in the future. And after I mention this, we'll call the episode. And that is what is called CPX, not to be confused with Nvidia's Rubin CPX, which nobody talks about anymore. Like whatever happened to that, right?

It's true. So, CPX is basically think about it like co-packaged optics. It is a optical engine that is put right next to the sit switch silicon. Pretty much like what you would think CPO looks like.

Mhm. However, the CPO optical engine itself is socketed. Mhm. So, CPX is the socketed CPO where you can put anybody's optical engine and socket it and close it down.

Like you Think about like how you put a CPU onto a motherboard, right? Think about if you can put an optical engine next to a switch silicon and just, you know, swap it out with whoever you want supply chain. That is called the CPX thing that is very interesting. Okay.

Companies like Semtech Semtech and Molex are all leading that. Okay. them it's a connector technology, right? So Yes, yes, yes.

Okay, so to your point, the existing sort of modular ecosystem, the horizontal ecosystem around like pluggable transceivers and stuff, if they were to continue, they got XPO to continue their road map. If they were to try to continue into CPO, they would prefer CPX where it continues to modularize components so that the whole ecosystem can fight for that new socket, if you will. Now, even if they're not an optical engine part, fine, but at least there's it's more modular, there's more competition. Yeah.

You know, continue that value shift to just a few players. Fascinating. And how how far along is that? I've never even heard which By the way, let me also say XPO, CPO, CPX, like it's all getting very confusing.

It's too much. I can see Yes, yes, we need some diagrams and stuff, but I can see why they would want to name it something very similar to CPO. But yes, it should probably should I like socketed CPO. I like that concept.

That's easier to understand.

socketed CPO. That's the way to think about it. And you know, this this a problem we haven't even spoken about and it is getting way out there. But you know, when you're socketing a CPO like socketed CPO approach, think about how you're going to connect fibers. Like how are you going to connect all these fibers into that thing? It's so complicated.

It's complicated. So, the XPO approach is just hook it up there like on the outside of the rack. Keep all the optics to the outside of the rack and have co-packaged copper cables that route to the switch silicon. Use CPC inside the switch rack.

Copper is better off. You can wind it, you do stuff. It's not sensitive to bend radius issues as much as light is cuz if you bend the optical cable too much, light leaks out the side. You know, it doesn't make the turn, it just like leaves the optical cable.

And that that has loss problems when you bend it. Bend it even more, it'll just snap. And that's the end of it. So, routing optical fiber is a nightmare.

People would rather route copper inside the switch rack. This CPO thing is nowhere near oh, this is the way we are going forward or anything. There are so many moving parts within the industry, so many different things happening between different players. It is anybody's game right now.

We have to watch and see what happens. It's fascinating. It's a fascinating game of 10D chess. There's so much here and you need to write more on it and create some more diagrams because I'm visual and that will continue to help to provide clarity as there's so many moving parts and everyone is incentivized to put forth solution paths that make sense to the way that they play into the ecosystem they're in you know, so Yeah, yeah, yeah.

That's what the Substack is for, right? Because what we do is we go and like think about all this stuff and write down carefully formed sentences and write and draw diagrams in Excalidraw and anybody wondering, I don't know, we use Excalidraw a lot. We'll draw some pictures and explain all this stuff, copy pictures from blogs and try to explain it away. This is what we do.

So, keep keep an eye out for all this stuff. I'm sure Austin is now inspired to go and look up all this stuff. It'll show up on your Substack, too. Yeah, yeah, for sure.

Yeah, there's really interesting strategic implications for these businesses. But with that, that's enough for today. Thanks for listening, everyone. I hope you enjoyed all this photonics talk.

Send us your questions, send us the technologies and the companies that you're interested in. If you're enjoying Semi-Doped, share it with your friends. Thank you to everyone listening across YouTube, across podcasts, and on X. Subscribe to our newsletters and we'll talk to you next time.

Thank you.
