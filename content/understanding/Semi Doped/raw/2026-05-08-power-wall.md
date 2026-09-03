---
source: https://daily.semidoped.com/p/power-as-the-next-physics-wall-for
title: 🎧 Power as the Next Physics Wall for AI - Semi Doped
kind: transcript
---

🎧 Power as the Next Physics Wall for AI

The same physics that drove copper to optics is now coming for power delivery. Vik and Austin walk through why 48V breaks at 600kW, why the answer is 800V from the EV world, and why every conversion stage from the grid to the GPU is suddenly up for grabs.

Things we cover:

Why 600kW racks at 48V mean 12,500 amps of current

Why 600kW racks at 48V mean 12,500 amps of current

48V → 800V and CPO-style vertical power delivery at the GPU

48V → 800V and CPO-style vertical power delivery at the GPU

Reusing the EV power electronics ecosystem in the data center

Reusing the EV power electronics ecosystem in the data center

The full grid-to-GPU power conversion chain

The full grid-to-GPU power conversion chain

800V → 48V (reuse) vs skipping straight to 6V

800V → 48V (reuse) vs skipping straight to 6V

Coherent’s six-inch indium phosphide ramp

Coherent’s six-inch indium phosphide ramp

This podcast is lightly edited for clarity.

Quick hits, high signal. Takes from semi industry experts. Sign up for free daily updates!

Welcome and Earnings Season

Vik: Every part of this power supply chain has a different player, has a different technology. It is not like what you can see in HBM. It’s HBM. What is it? The same three companies, what are they doing? Stacking the same way? It’s kind of a closed problem in a sense. Power is a wide, wide open problem.

Austin: Welcome to another Semi Doped Podcast. I’m Austin Lyons of Chipstrat and with me is Vik Sekar from Vik’s Newsletter. What’s going on, Vik? It’s been a crazy earnings week this week.

Vik: Yeah, I can’t listen to all the earnings calls. I just try to listen to a few of them and run the transcripts through LLMs and tell me what happened. But other than that, it’s too much to keep up. It’s a fire hose of earnings calls this season. I can’t keep up.

Austin: Yes, I know. In a dream world, they would just all talk to each other and schedule one per week for the whole season. But no, instead it’s everyone in the span of a couple of days.

Vik: It’s not intended that people listen to all of them. I’m guessing that people have investments in company A, B, C, D, and they just listen to those. You don’t listen to everything because even big investment firms have people who address certain sectors of the semi market. People like us try to cover optics, data centers, memory, CPUs, power. Power, speaking of power, that’s what we’re going to talk about today.

Austin: We’re here to talk about power. So before we dive into power, should we address — we had lots of YouTube commenters. So thank you, YouTube commenters. Should we address any of the questions?

Follow-Ups: Memory Tax and Boardfly

Vik: Yeah, I think we should at least address one or two of them. One was on the memory tax episode that we did. The comment was basically that when we said memory costs going up and all the capex being directed into memory means that money is not available for compute. I think the overall sentiment around that was, yeah, the money that’s going into memory is more like inflation and it doesn’t usefully contribute to compute or solving the memory bandwidth or making data move faster between racks. It doesn’t solve any technical problem in any way other than that you’re just paying memory companies more. So I think that was mostly the sentiment.

Austin: Yeah. So the comment was something like, you know, that we’re misunderstanding and compute’s not the bottleneck, memory’s the bottleneck and therefore you should spend more money on memory. But yeah, to your point, what we were saying is, no, no, no, no one’s — we’re not saying don’t spend more money on memory. We’re just saying that you bought a gallon of milk for $2 today and tomorrow it costs $2 and 50 cents for the same gallon of milk. So you’re just spending more to get the same stuff. Yeah, it’s the cost. Inflation, right?

Vik: It’s like you got chocolate milk. Chocolate milk would be nice, but you don’t. You just get regular plain old milk, but you pay chocolate milk prices. Exactly. That’s not helping anybody. It doesn’t increase our quality of life.

Austin: Right, right. So the purchasing power of a dollar is going down for compute. So a bunch of CFOs are going to say, hey, we’re spending more for equivalent compute. Does this meet our internal ROIC targets? What’s the projections? When will this stop? So on and so forth. Okay, so we addressed that. I think we had a lot of people asking about Boardfly. Did you want to talk about it at all and how to get to seven hops?

Vik: Yeah, so the best way to go about this, even rather than me going through and explaining how this works, is that Google has published a deep dive on the TPU 8i / 8t blog. It’s a deep dive blog on their website. So if you go there and look at the picture there in the blog, it explains exactly how the 3D torus approach has 16 hops and how the Boardfly approach has actually seven hops.

So the idea is that you have to get from the board into the group where you have so many boards in a rack kind of thing. And then you go between rack to rack through the OCS switch. And then finally you follow the same process on the other side. You reach the other rack and reach the other board. The Google picture actually shows seven hops. So you can see how each hop has a different location it goes through.

So the fact is that you can reduce network diameter by using their Boardfly topology, which means that the latency equivalently comes down compared to using a 3D torus. The latency is more than twice better.

Austin: Nice, okay, so folks, if that’s not enough, go read the original source for yourself and you should be good to go.

Vik: Yeah, it’s a good explanation. They do a good job. Google blogs are…

Austin: Nice. Yes, totally. They spend a lot of time and effort. So thank you, Google. Whoever wrote that out there, we appreciate you.

Coherent’s Six-Inch Indium Phosphide Ramp

Austin: So, okay, let me hit really quick. Last thing. I had a couple of quotes from the Coherent earnings call that I thought were interesting. And we’ve talked about these topics before, but I’m going to hit on it again, just because it’s a continued theme that people should be tracking, which is ultimately there’s massive demand for indium phosphide based lasers. And everyone is scrambling to create more supply. And for Coherent, the quote was from the CEO, James Anderson: “we are aggressively ramping six inch capacity because six inch wafer compared to a three inch wafer will produce more than four times as many chips at less than half the cost.” So this is how Coherent is trying to rapidly increase their supply, is moving to six inch wafers.

And so again, I just wanted to unpack it in case people hadn’t heard that before. If you’re like, how do you get to 4X more chips at half the cost? We’ve talked about this a little bit, but ultimately it’s about the area of a six inch wafer compared to the area of a three inch wafer. It’s radius squared. And so if you — six squared is 36, three squared is nine, 36 divided by nine is four. So that’s how you get to four times more.

And then of course the cost thing is interesting, and I don’t think we’ve talked about that quite as much, but at the end of the day, if you have the same number of steps and you’re just processing a bigger wafer, your costs are fairly equivalent. You have the same number of steps. You might have to pay more for a bigger substrate and you have to pay a little bit higher input costs because maybe more photoresist and chemicals and gases and things. But let’s say the cost is maybe 2X higher. You could still see a world where to process a six inch wafer, you can still see a world where you get four times as many die per wafer, and because it’s bigger and yet it only costs you twice as much to process it. So your cost efficiency is twice as good and therefore it costs you half as much per die. So I just wanted to remind people really quick that that’s Coherent’s play.

Now the question of course that everyone’s asking is, okay, they’ve got six inch wafers, but is it yielding and what are they actually making? And so James Anderson did address that as well. He said: “Given the healthy yields we are seeing with six inch production, we began production of six inch indium phosphide at a second site in Järfälla, Sweden.” I’m not quite sure how to pronounce it, Järfälla, Sweden. “And ramping at two sites in parallel will significantly accelerate our production capacity ramp. Additionally, we are in production on three different types of key transceiver components on six inch indium phosphide. EMLs, continuous wave lasers, and photodiodes.”

And somewhere else, he said — I think it was in a Q&A — he specifically said that their six inch yields were as good or better as their three inch yields. Pointing out, that’s comparing to the mature three inch yield, not just when three inch was ramping. So I think he, you know, without saying much about yields and performance, Coherent was definitely trying to signal: hey, we’re not just building the simplest component, we’re building photodiodes, CW lasers, EMLs, and they’re pretty confident in their yields.

So I would just say it’s something to track. Coherent is telling the story that they’re progressing nicely. I think maybe the final read-through will be on their margins, because of course if they are increasing supply, decreasing the cost and yielding well, which would impact your costs, and those devices they’re making on the six-inch wafer have good performance, which means you can maintain ASPs or increase ASPs, then ultimately this should flow through to their margins. So that’s probably just the final takeaway. If you’re trying to track it and really trying to figure out, is this just a story or are customers actually buying devices that are built on this new capacity, ultimately it’s about yields and ASPs and we should be able to track that.

Vik: So one small caveat to that is that when talking about yields of CW lasers or electro absorption modulated lasers, EMLs, which are the workhorse for 200 gig transceivers, and CW lasers are the workhorse of co-packaged optics. These are the two hotly contested areas really right now between Coherent and Lumentum and all these companies. It is very important to distinguish that CW laser — but at what power? Are you talking about 50 milliwatts, 100 milliwatts, 400 milliwatts? That is significant differences between what yield means on what product.

Similarly, EMLs are the same way. EMLs have two components to it. It has the laser and the absorption modulator. And they are usually co-designed to work together. And that is a significantly more complicated problem to solve compared to maybe CW lasers, where you just have to put out laser, right? You’re not modulating anything. It’s just like a flashlight that’s on. You’re not turning on and off the flashlight depending on a zero or one. So CW lasers are structurally — functionally, I wouldn’t say structurally, functionally easier. So it really depends on what yields, which product line, what power, what output levels.

So it’s very easy in an earnings call to put a blanket saying, yeah, everything’s great. But if everything is great on a 50 milliwatt laser, that’s not what we’re talking about. So it really depends on what exactly is yield meaning here. So that’s the wet blanket I want to put on your otherwise optimistic statement.

Austin: No, yeah, no, totally. I definitely don’t disagree with that. There’s the high level directional guidance they’re giving. And then to your point, there’s the nuance and they probably won’t share that level of nuance on a call, just like Intel’s not going to get super nuanced into the yields on 18A and 14A and give engineering specs. So then that’s the game. How do you sort of reverse engineer back out what you can to get a good sense of — they are actually just insinuating 50 milliwatt lasers continuously, they did not 400 milliwatt. And maybe again, that shows up in revenue, top line revenue, or maybe it shows up in margins or something where it’s like, their margins aren’t great because it’s customers buying the cheap product versus high performance power.

Vik: If they are selling high ASP products at high yield, it will show up in the money. Follow the money.

Austin: Exactly, totally.

Power Is the Next Physics Wall

Austin: So, okay, cool. All right, let’s jump into power now. So you wrote an article on power and this is a perfect forum for us to unpack it. So yeah, set the stage for us.

Vik: So there is this growing sentiment — it’s not just from me, a few people in the industry have pointed it out as well — that we are coming to a point, maybe not in this generation, maybe it’s the next generation of accelerators and racks, probably Rubin Ultra, because the Kyber rack is a 600 kilowatt per rack power consumption. That is much higher than what usually data centers are used to.

So in the cloud era, each rack used to consume like 20 kilowatts. Now AI accelerator racks consume anywhere between 100 and 120 kilowatts. Now we are talking about the Kyber era of racks where the Rubin Ultra will go in at 600 kilowatts a rack and the future will hold one megawatt a rack. That’s an enormous amount — that’s a hundred times power per rack compared to what was in the data center, the cloud era, pre-AI era, which was like approximately 10 to 15 kilowatts. You’re talking about one megawatt per rack. And imagine how many will go into a data center and imagine how many of those data centers are going to be connected together via scale across, all of that stuff.

So this is a looming problem, a bigger and bigger problem with every generation of AI that comes out, chips that come out. So I wanted to address it in my Substack article to just point out that power is the next physics wall. And this is a theme I want to pursue in a little bit more depth over time, because as you can imagine, it’s an enormous problem. You’ve got power generation all the way at — whether you’re talking turbines or nuclear power, how that’s transmitted, and how it reaches the substation, how it is converted into the data center, and how it is ultimately delivered to the GPUs.

We’ll cover some of that in detail in this podcast. At least I’ll explain how this conversion happens and where the markets directions are going to go going forward. But you can imagine this entire chain has so many players and it has so much going on there, and all of it is important to deliver the next generation of power. So that’s what I wanted to touch upon in this abstract post and we’ll briefly cover as the next physics wall.

Austin: Nice, nice. Okay, let’s get into it. So what is the problem with a one megawatt rack? Why is that a problem?

The Rack-Level Resistance Problem

Vik: Yeah, so in this one, I want to start at the rack level. What is the underlying physics problem? And then we will zoom back a little bit and understand how power is actually generated and delivered up to that one megawatt rack, because it’s important to understand how the power gets there. And then we can talk about what happens within the rack, which is essentially what I focus on in the Substack article. So the thing is very simple.

The idea is — why are we talking about optics now? I promise this is not a tangent. This has something to do with how. Why are we talking about optics? The whole problem was with copper and reach. So as the speeds got higher and we needed to connect racks over longer distances, optics was the only way forward because copper reached its physics limits.

And the physics limits in copper is, as you increase the speed, what is flowing within the copper cable is actually an AC signal. It’s a varying signal, right? Because you’re transmitting bits that go up and down, like whatever. So it’s like a varying signal. And what happens in the copper interconnect when you have varying signals is that all the current doesn’t flow through the whole copper wire. They tend to concentrate on the periphery. Only the outermost ring of copper actually holds any signal. There’s nothing happening with the rest of the copper cable. This is because of the phenomenon called skin effect. It goes to the skin of the copper cable, not really the whole cross section of the copper cable. So the resistance goes up. Because you have all this cross section, but if you’re not using it, you now have more resistance.

So resistance was the fundamental bottleneck for why we needed to go from copper to optics. And now you see everybody’s in the optics — like indium phosphide shortages, the rest is history. Look at the optics market we are in. So this was a bottleneck that was physics driven. And whenever something is physics driven, it’s easy to identify. So go ahead.

Austin: Totally, totally, no, that is what we try to do here is look for the fundamental physics constraints and then ask what is going to happen beyond this. All right, so really quick for maybe less technical listeners — when Vik said AC, he meant alternating current, that’s the varying current. And then this skin effect thing — I like to think of electrons flowing through a wire as sort of like a pipe, or even you can think of it as a subway tunnel with lots of people trying to push through it. And if the skin effect means you can only walk at the edges of the subway tunnel, then you try to take the same people and push them through the edges of the subway tunnel. There’s gonna be more resistance. You’re gonna bump into each other more, right? Then if you could just — everyone could just walk nicely with lots of space around them.

So when Vik says there’s an increased resistance and the skin effect becomes worse and worse at higher and higher speeds — when we’re trying to communicate more and more data at higher and higher speeds, then you get more of this skin effect resistance, bumping in together. So there’s just a little analogy for non-technical folks. Vik, now please carry on.

Vik: Yeah, thanks. That’s good. I like the subway analogy. I like analogies. It’s always great. Thanks. So it is the same thing, right? Now, when you have a lot of power, say 600 kilowatt or something, ultimately, you have to make two decisions. And actually, it’s one decision and the other one follows from it. What voltage are you going to operate in? Because power is basically voltage times current. So if you are operating at a high voltage, you have lower current. If you’re operating at a low voltage, you have a higher current for the same power. And that decision is very important to make.

Now, typically in racks earlier in the cloud era, we didn’t really need to go to very high voltages because there’s no need to. The currents are manageable because the power is manageable. So why do you want to go to high voltages? Because you have to use special transistors to actually handle such voltages. Not everything can handle it like that. No need to go exotic if you don’t need to.

So typically what has happened is the voltage choice in racks from — it’s not that long ago — Meta really standardized on the 48 volt architecture. So the 48 volt DC architecture. And so the current was OK. When the power was low, the current was manageable.

So now what happens when you go to some massive amounts of power is that now if you’re at 48 volts DC, you are going to go to a lot of lot of current. Like take this for example: 600 kilowatts of power and 48 volts of rack voltage, you are burning 12,500 amps of current through the rack. Think about that, that’s enormous. And what happens is that wherever, whichever method you use to transmit data — it can be copper, wires, buses, connectors, whatever. Everything has a resistance. And so even the tiniest resistance at 12,000 amps of current means that you are going to dissipate a lot of power. The power dissipated through a resistor is like the square of current times the resistance. So not only do you have a high current, now you are going to square it.

Austin: Yeah, crazy, crazy. So you’re saying power equals current times voltage. And ideally we would just have low voltage and not much current, not a big deal, low power. But we’re in an era where we already have a fixed voltage. It’s, what did you say? 48 volts coming in. Yep. And so we want to have much, much higher power at the rack because we want to have much denser racks with way more GPUs and they’re all power hungry and so in aggregate they want to consume a ton of power. And so you’re saying the only way today, if we stay with the 48 volts, to have all these GPUs that are power hungry and to power them, is to increase the power. And if P equals IV and the voltage is fixed, the only thing we can do is increase the current to something crazy like 12,500 amps or 12.5 kiloamps. It’s hard for me to even comprehend that. When we were taking EE courses, we were never using currents this high when we were doing our little by hand toy problems.

Vik: It’s always milliamps, right? All of our circuits are milliamps, and now you have kiloamps. Power electronics is a beast, okay? So it’s fine, but it’s still a lot of current.

Austin: Yes, yes. But then what Vik also said was, okay, well, resistance is what — I squared times — what did you say the resistance is? Yeah.

Vik: The power dissipated. The amount of power you lose through some form of resistance, whether it’s the connector or just the metal itself, there’s always some resistance. And you lose power via heat to that resistance. You generate heat when you push current through a resistor. And that power dissipated is the square of the current. So not only are you in 12 kiloamps of current, you’re now squaring it. And then the resistance is, how low can you make it? I have some example calculations on the Substack. We don’t have to go through all of it now. But yeah, it’s insane. You will have a lot of power dissipated.

Austin: Nice, nice, yes. So the problem is we’ve got a ton of power. We’ve got a really high current. We’re gonna dissipate a lot of heat because it’s the square of that current. So just lots of people bumping into each other in the analogy and giving off friction, giving off heat. So how do we solve this?

Why 800 Volts and Vertical Power Delivery

Vik: So the one way to fix this is go to a higher voltage. So for 600 kilowatt, don’t use 48 volts, use 800 volts. And it is coincidentally the voltage that is used in EVs, traction inverters. And so that entire automotive industry has matured this silicon transistor technology called IGBTs or more recently the silicon carbide, gallium nitride — all these exotic wide band gap semiconductors as they are called. These are specialist transistors that can handle a thousand volts of voltage and they are well suited for such applications. So might as well reuse that EV industry and the transistors around them. Go to 800 volts.

So when you go to 800 volts and you do the same math, the current drops from 12,500 amps to 750 amps. Much better, right? 750 amps. You don’t even have to use the kiloamp unit.

Austin: Yes, yes, totally. Okay, so you’re saying if we had P equals IV was our problem where the V was fixed, so we had to increase the I a lot if we wanted to increase the P, the power, but you’re saying, wait a minute, what if we don’t fix the V? What if we actually increase the V and hold the P constant, then the I can go down, right? So you’re saying instead of 48 volts, we could increase it to 800. And then we could still get the same really high power at a lot lower current. And then of course the question is, well, which V should we increase it to? And I heard you say, well, everyone looked around and said, hey, why not 800 volts? Because that ecosystem already exists. That power electronics ecosystem already exists for EVs. So that seems like a great place to bring it into the data —

Vik: Because those are ruggedized components. Transistors that go in cars — if it’s driving your wheels, that is basically driven by transistors too, by the way. The battery power is converted into alternating current that drives the motor, that drives the wheels. Those things are rugged. They have to operate in all conditions. They have high thermal tolerances. They have quality standards. There’s a lot of things in place. Why not reuse that stuff? Yes, and it also gives an opportunity for EV companies to pivot into data centers because everybody wants a data center angle.

Austin: Totally, totally. Yeah, no, I think it’s super fascinating to be like, there’s already power electronics here and they’re already ruggedized to be in harsh environments from automobiles, to be hot or cold or whatever. And so guess what? Data centers are crazy hot. No big deal. And then yes, of course, naturally anyone, when their investor brain is listening, they’re going, wait, wow, this is going to be really interesting. I should look into anyone who’s already doing power electronics for 800 volts or EVs or whatever, because now they’re trying to move into the data center. That’s interesting.

Vik: Yeah, so it’s a nice solution to the problem. And NVIDIA is looking into it. I mean, this is not news to people who are following the power side of things in data center world. We’re talking about the basics, but that’s good. We’ve always got to set the baseline of understanding so that we can follow what happens in the industry closely later. That’s where the foundational understanding comes. It’s good to have this. It’s a good discussion we’re having.

So the point is that, think about the power dissipated through heat now. The resistance, let’s say, is the same, okay, for argument’s sake. Your current is so much lower. Now the square of the current is also significantly lower. If you can drop current by two orders of magnitude — how much should we? At least we dropped it by one order of magnitude, right? Like 750 to 7500, whatever.

Austin: 12.5K down to 0.75K. So yeah.

Vik: So if it’s like 10–15 times lower current, then your power dissipated is square of that. It’s like 100 to 200 times lower than that. So you see, the fundamental problem is that increasing the voltages reduces the current. And now this is the only viable way to overcome the same problem of resistance that was plaguing the copper interconnect world that is due to plague the power world as well. Because you cannot push that much current through any form of resistance.

And this is not like the skin effect kind of resistance we talking about. This is like standard Ohm’s law resistance. This is DC resistance we talking about here. So basically, this is the same limiting factor that drove everybody from interconnect world into optics, copper interconnects into optics. This is the same limitation — that is, resistance — that will drive people from low voltage systems to high voltage systems.

And when you go to high voltage systems, it creates an entirely new socket, because this 800 volts to 48 volts conversion, which is one way to do it, you don’t have to bypass 48 volts. You can convert from 800 volts to a certain voltage. What that voltage is, is a question that requires some engineering discussion. It’s all on the Substack. But that conversion is a new socket basically that does not exist in the data center world. And that is what people are trying to compete for and land it properly.

And think about the whole CPO argument again. You wanted to do the optical to electrical conversion as close to the chip as possible. Right? Because you don’t want to be in the copper land at all. Because the problem is resistance. The same problem exists in power. You don’t want to convert to power — to low voltages — far away from the chip. If at all possible, you want to have the highest voltage possible right up to the edge of the chip. Make the conversion at what is called the point of load. So think about it as the CPO of the power world. So now you have what is called vertical power delivery. You put the chip under the GPU and you deliver power at the GPU. Convert as much as possible.

Not that I’m saying you’re going to convert 800 volts to 1 volt at that chip. That’s like too much. There are still many conversion stages that need to happen before that happens. But ultimately, that is the CPO equivalent of power delivery.

Austin: Yeah, no, that’s good. I really like the analogy of looking at CPO to say, basically, you want to keep it in light as far as you can, as close in as possible before you convert it to the electrical domain. Otherwise that whole problem of, like with linear pluggables, was you’ve got that long copper trace and it’s very noisy and lots of power loss and signal loss. So no, no, no, just bring in the signal as close to the chip, the ASIC or the GPU or whatever, as possible. Trying to do the same thing — high voltage, low current, bring that in as close as possible before you essentially step it down to lower voltages.

And this actually reminds me — analogies for people — this is like how the transmission lines work in your neighborhood, right? You’ve got really high voltage lines that are sending power across — for me in Iowa, like across cornfields to the next town. And then only once it gets closer, does it get sort of stepped down and brought down. It’s kind of the same thing here we’re talking about — high voltage to reduce the current and reduce the power loss along the way.

The Grid-to-GPU Conversion Chain

Vik: Yeah, yeah, it’s very important. The power efficiency dictates how much compute, because there is a fixed budget per data center. You can’t get more than so many gigawatts, right? And so you want to convert all of that into compute. You don’t want to burn it in poor power conversion systems. You want to have all that power available to generate useful AI output. So that is the key thing here.

So that is basically the setup. But I want to just zoom out for one quick minute because I don’t want this to keep becoming a very long technical episode because we’re going to talk about this a lot. This is not the first or last time you’ll hear about power on this.

Austin: I like when we talk technicals, so —

Vik: Yeah, we will. We like this stuff. This is why we do it. And there’s so much nice technical stuff. And this is analog semis. Okay, I love this stuff. Personally, this is what I do. And so I love analog semis.

So zooming out, look at what happens. You got power generated at the nuclear power plant. And like you said, that power is transmitted with hundreds of kilovolts across the grid to maintain the losses to be minimal. And finally, it reaches some kind of a medium voltage substation that is usually on the data center campus. I have another whole article on how this whole big picture thing works, so look it up on the Substack. But it is converted to something like 10 to 30 kilovolts. This is all alternating current still. And all of these require these gigantic, huge transformers and insane looking things, right? These are not like sensitive, delicate, two nanometer gate-all-around. These are big machines that just burn power and it’s just the complete opposite of the sensitive AI world.

And then that power is then brought into the utility room, which is usually a little space outside the actual data center where the compute racks are kept. And in the utility room, it is converted into 430 volts. It’s actually converted probably in the data center campus, but the utility room gets like 400 volts or 430 volts. This is the three-phase industrial voltage that people get. At residential levels, you either get 110 volts or 220 volts or something like that, but usually industrial power is 400 volts. And then from there, it is distributed to all the racks within the data hall. It’s called a data hall where all the racks are kept.

At the rack level, this AC is converted to 48 volts at the rack. So that’s where it happens. So this is the power supply unit or the PSU. And after that 48 volts is available, to distribute it to various parts of the whole rack, it is in various stages converted to what is called an intermediate bus voltage. So you have these things called intermediate bus converters. What they do is they take the 48 volts and they convert it to 12 volts. Now we are talking about low voltage bus architectures, which is converted to six volts. So you can’t convert 48 volts down to one volt. That’s a challenging problem to do. You always have to have stages. So this 12 volts is an intermediate bus stage. So that conversion happens. And then ultimately the 12 volts is converted down to maybe one volt range, 1 volt, 0.8, 0.65, depending on what the GPU needs.

And those are actually different because those converters have one major requirement. They need to be highly voltage regulated. When the GPU wants 0.8 volts, it wants 0.8 volts. It doesn’t want 0.9. It cannot want 1.2. So voltage regulation to very fixed values is very important at that stage. So those are called voltage regulator modules. And those are very specific and they have the highest count in a data center, right? Because the voltage regulator modules are many compared to the rack level conversion that happens of either from the PSU or the intermediate bus converter. The actual mass market for power lies in those voltage regulator modules, or VRMs.

So yeah, what you can look back here and see is, look at the number of stages of power conversion, right from the grid all the way down to the GPU. And every section of this power conversion and voltage conversion that happens has a different set of technologies. Some of them operate on big inductor coils. You have these substation transformers, but then you have these — what are they called — LLC converters. They just use big transformers with windings like this, coupled to each other. And they just convert voltages. But those are not regulated voltages. It doesn’t matter if it converts to 48 volts or 50 volts, it’s fine. It doesn’t have to be accurate. So the entire technology chain and the supply chain for that is completely different.

Then you’ve got this different supply chain that goes from 48 volts to 12 volts, the bus converters. So there are companies that specialize in that, and those you have to get designed within data centers in that section. Then you’ve got these voltage regulator modules. There are a few companies there who dominate the space. So every part of this power supply chain has a different player, has a different technology. It is not like what you can see in HBM. HBM, what is it? The same three companies, what are they doing? Stacking the same way? It’s kind of a closed problem in a sense. Power is a wide, wide open problem. It’s a very wide range of topics and technologies to look at. So it’s very, very complicated, to be honest. It’s not something that’s very straightforward.

And now, just like everybody on the investors, the semi world and people who are interested — everybody has become an optics expert, right? Yes. Now everybody knows what is indium phosphide. Everybody knows there’s laser shortages. Everybody talks about fiber attached units and coherent optics and all of this stuff. Lane rates is quite common now. Now you’re going to hear people talk about power conversion topologies. But it’s going to be far more challenging, by the way, because it’s really a big wide area of power conversion.

Austin: Yeah, it sounds like a lot of opportunity, but a lot to cover if there’s different technologies, different materials, different companies in the supply chain. Man, if we thought we were busy with earnings calls already, just wait.

Topology Battles and Wrap

Vik: You can have an army of people just cover power earnings calls. I mean, that’s how many companies there are. The technologies are amazing. But also they’re amazingly simple. Ultimately, it’s all about converting between DC to AC or AC to DC. All you do is, if you want to convert from one DC to another, for example, the simple concept you can think of is you convert the DC to AC, then you use a transformer with a different number of turn ratio. So if you use a 10-to-1 turn ratio, you can bring it down by 10, the AC current by a factor of 10. Then you convert that AC back into DC. And now you’ve converted it basically back, stepped down the DC by that amount.

Then there are what are called synchronous buck converters. Those are basically based on square wave waveforms. That basically works on the principle of having how much duty cycle you want to have. You keep it on for some time and then you turn it off. And then when you average it out, you get a different average. So if you have it on for more time, you get a higher average. If you keep it on for less time, you get a lower average. So you can step down voltages using those kinds of synchronous buck converters. So the circuit topologies are also very fascinating, very interesting, and the trade-offs are enormous. So it’s a very wide space, and if we are entering a space of power limitations, we have a lot to talk about.

Austin: Yes. Man. You know, I took a little bit of power stuff in undergrad and at the time I wasn’t motivated to be excited about it. So it all came off as fairly boring. But what I liked about this episode is you helped motivate me to better understand all of this. Because there is a bigger reason for getting into the weeds here.

Vik: Yeah, yeah. Even the topologies — when we go into 800 volts is not set, by the way. There is a big discussion as to whether you should convert from 800 volts down to 48 volts and then reuse all the existing infrastructure that already is there at 48 volts. That’s one way to do it. And the other approach is, why don’t you convert from 800 down to 6 volts, go directly. So that’s what people like TI and Navitas and all these companies are doing. They want to go directly to six volts. Why the 48 volts? Because every conversion stage you lose efficiency. The fewer stages of conversion, the better. So why don’t you skip the 48 volts and go straight to the intermediate bus voltage of 12 volts or six volts. And then you do the conversion from there. So there’s all these battles of topologies and architectures that are still going on. Nothing is set in stone. It’s a time to look at this, really.

Austin: Let me guess — all the 48 volt incumbents are like, yeah, just go to 48 volts and reuse it. And then all the six and 12 volt folks are like, no, skip that, come to us. We’ll sell you more. Yes. Yes. We’ll make that component.

Vik: Exactly. If it’s a 48 volt conversion, yeah, those guys are happy. If not, they’re like, oh no, what do we do now? They’re skipping our voltage altogether.

Austin: Totally, fascinating. Well, all right, we should call it here. This has been great, but it’ll be fun to dive into more and see who ends up winning here.

Vik: Yeah, yeah. We’ll leave the Substack post that I have on there if you want to go read it. At least a lot of the engineering stuff that I mentioned is on the free portion of the post, so go read it. All right, I’m going to do the goodbye today because I’ve already spoken this whole episode. I might just throw the towel in. So thanks for listening to Semi Doped. This has been a fun podcast for us to run. And do check us out on YouTube because we always put pictures where we can. We are also on all podcast platforms if you ever want to listen on that. But also, we do have a Substack where we write daily updates on this stuff because we have so much news and stuff we monitor that we try to write it over there so that you have all the latest news. So definitely give us a follow on there as well. That’s it for this episode and catch you on the next one.

Relevant reading:
Vik’s Substack post on power:

Google TPU 8i / 8t blog (Boardfly deep dive): https://cloud.google.com/blog/products/compute/tpu-8t-and-tpu-8i-technical-deep-dive

Follow Chipstrat:
Newsletter:

X: https://x.com/austinsemis

Follow Vik:
Newsletter:

X: https://x.com/vikramskr

Thanks for reading! Subscribe for free to receive new posts and support my work.
