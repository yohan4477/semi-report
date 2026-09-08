---
source: https://daily.semidoped.com/p/semi-doped-advanced-packaging
title: 🎙️Semi Doped: Advanced Packaging - Semi Doped
kind: transcript
---

🎙️Semi Doped: Advanced Packaging

Things we cover:

Why the silicon interposer exists and what CoWoS-S, CoWoS-R, and CoWoS-L each trade off

Why the silicon interposer exists and what CoWoS-S, CoWoS-R, and CoWoS-L each trade off

EMIB: how embedding tiny silicon bridges directly into the substrate sidesteps the reticle size limit

EMIB: how embedding tiny silicon bridges directly into the substrate sidesteps the reticle size limit

EMIB-T and EMIB-M: the two variants and what each adds

EMIB-T and EMIB-M: the two variants and what each adds

The yield question: if EMIB yield is “only 90%,” what does that actually mean at GPU cost?

The yield question: if EMIB yield is “only 90%,” what does that actually mean at GPU cost?

Google’s 3M TPU EMIB order via MediaTek, SK Hynix testing, and Intel Foundry’s optics opportunity

Google’s 3M TPU EMIB order via MediaTek, SK Hynix testing, and Intel Foundry’s optics opportunity

Where the scaling roadmap goes: 5.5x reticle today, 9.5x next, System on Wafer at 40x on the horizon

Where the scaling roadmap goes: 5.5x reticle today, 9.5x next, System on Wafer at 40x on the horizon

This podcast is lightly edited for clarity.

SpaceX IPO Day

Vik: These parasitics — when it becomes a flip chip — became lesser, and it was important for the RF work I was doing. And flip chip saved a lot of design work because when you design the chip, it works just as is. You don’t have to account for the package as much if it’s a flip chip. It is the chip. So I think now there is no chip without the packaging.

Austin: Hello everyone, and welcome to another Semi Doped episode. I’m Austin Lyons with Chipstrat, and with me is Vik Sekar from Vik’s Newsletter. Hey Vik, what’s going on, man? Are you a trillionaire yet? Because I know somebody who’s gonna become a trillionaire right about sometime soon. I’m talking about the SpaceX IPO.

It’s Friday when we’re recording this — Friday, June 12th for listeners — and today is SpaceX IPO day. Elon Musk is gonna graduate from billionaire to trillionaire.

Vik: Apparently I’m not sure really how close to a trillionaire he actually is. It’s just too many zeros.

Austin: You know, usually we record stuff pretty close to when we actually publish it. But since I’m going to be traveling next week, we decided to move this up a little bit. So if you’re hearing the SpaceX news and we’re like, “Wait, wasn’t that like last week? What’s he even talking about?”—

Vik: Yeah, that’s because we’re recording it early this time.

Austin: Yes, totally. Summer is for travel and vacations.

Vik: Yeah, so trillionaire — I’m just a thousandaire, so it must be nice.

Austin: Just adding zeros, how hard can it be? Come on.

Vik: Yeah, right. Just add a zero. That’s what I’ll tell my kids when they grow up. You just gotta add a couple of zeros. That’s your goal.

Austin: Yeah. But it’s nice though. It’s valued at what, like $75 billion or something? This is one of the biggest IPOs in history. It’s exciting. It’s listed under the ticker SPCX. So now we have this publicly traded company that does rockets, chips, AI, self-driving cars — you name it.

And what’s interesting, compared to what we’ll talk about today, is Elon Musk’s link to Terrafab — a project closely tied with Intel, which we’ll be talking about a lot today. So it all checks out. SpaceX is tangentially related to what we’re talking about today, which is advanced packaging.

There’s an interesting thing about Elon’s whole constellation of projects — it’s like the culmination of “deep tech is cool again, deep tech is valuable.” Satellites, space, internet, electromagnetic waves. They make their own PCBs — fabrication, manufacturing, Terrafab — but it goes all the way up to xAI and self-driving cars. They span the full hard tech stack, all the way from atoms to intelligent bits.

Vik: And space.

Austin: And space — yes, the vast universe beyond Earth. Totally.

Vik: Elon is everywhere. He’s omnipresent. And all these projects are technically very interesting. The way you put it — yeah, you’re right. He’s going all the way from chips all the way to space, with everything in between. Robotics, self-driving cars. That’s a lot of cool tech in one place. That’s all I have to say about it.

Austin: Totally. And he does the Neuralink stuff and the Boring Company — he’s got his hands in all sorts of interesting stuff. But okay, we’ll save Elon for a whole episode sometime.

Vik: Let the IPO settle down.

Austin: Yeah. They’ll have an earnings call, so we’ll get to listen and learn a lot. And I haven’t even read the IPO prospectus or anything, but we’ll talk SpaceX sometime. But today we’re gonna talk advanced packaging. But first, a quick message from our sponsor.

Today’s episode is sponsored by SambaNova. If you’re running inference at scale, you know the hardware trade-offs between memory capacity, chip count, and quantization. SambaNova Cloud sidesteps these constraints entirely. You get API access to frontier models, including full-precision DeepSeek R1 at 250 tokens per second with no hardware lead times. Texas Advanced Computing Center, OVH Cloud, and Hume are already on the platform. Try it today at the SambaNova dashboard. The link is in the show notes.

Vik: Yeah, very important. Advanced packaging is basically what drives AI chips these days, and it’s just such a bottleneck. TSMC has been the typical provider of advanced packaging. Now we have news that Intel is getting in some orders for their EMIB process, which is also advanced packaging — and I should just expand that right up front.

Austin: Embedded multi-die interconnect bridge — EMIB. That’s EMIB, which is a way of connecting different chips together on some kind of substrate. We’ll talk about all the differences between what TSMC’s Chip on Wafer on Substrate is — which we will refer to as CoWoS. There are many variations and flavors of that, so we should bring all those fine details to light. Then we’ll talk about EMIB — what’s different? And then really at the end, we should hit on Google’s commitment to EMIB technology going forward. It’s very interesting. That’ll come at the end — stick around for that one.

Simple Packaging: Wire Bonding, Flip Chip, and OSATs

Austin: So, friends, let’s first start with advanced packaging. What does that even mean? What is advanced about packaging, and what is un-advanced packaging? What is simple packaging? Let’s start at the very basics.

Vik: So packaging. We talk a lot about wafers, TSMC making wafers and making logic chips on wafers. We’ve talked about the size of these wafers — like dinner plates, these big silicon wafers with everything patterned. We’ve talked about lithography before. But interestingly, when you think about your computer or your phone, there’s not necessarily an exposed piece of silicon that people see. The silicon that gets made on this wafer has to get diced into individual chips, and then they need to be packaged — which is basically everything that happens to the wafer after it leaves the fab.

You need connections from the die to the outside world — for power, for signals, to get the heat out. You need mechanical protection — plastic or ceramic or something — so that the die actually survives the real world. So if you break open your phone, you don’t just see a beautiful piece of silicon sitting there. You’ve got packaging. You’d have to cut off the packaging to actually get to the silicon.

So at the highest level, packaging is: take the wafer, dice it up, take individual dies, and connect them to the surrounding environment — whether it’s a PCB or whatever.

Austin: Anything else in your experience as an electrical engineer to say at a very high level about packaging?

Vik: The silicon itself, apart from its interconnectivity to the outside world, needs to be protected from the elements — and also from electrostatic discharge and things like that. All of this means that packaging is important. You need to protect the chip inside while also being able to connect to it, because you just can’t put a piece of silicon in a phone and expect it to do anything.

So the leads — the connection points into the chip — are all done through packaging. It’s an essential step that has been around for a very long time. The earliest simple packaging approach was wire bonding: just a piece of metal that comes from your PCB to the chip sitting on the PCB. A very crude example — a metal wire that goes up and over and connects into the chip.

This has been around for a very long time. And believe me, even in the age of AI, wire bonds still exist. They’re still being used for a whole variety of products, because not all advanced packaging can handle things like power chips. Power chips require wire bonds because they need to carry a lot of current — big, old-school wires that still work well. So simple packaging isn’t dead. It’s still there today, required for some applications.

The other way to do simple packaging: flip the chip upside down and put solder balls there, then put it onto a PCB and melt the solder balls a little so that it sticks. That is the flip chip approach. That was a game changer — I’d say in the ‘90s — because the connection distance between the chip and the external world just got a whole lot shorter. Those wires are so long. But if you can put a solder ball and flip the chip upside down, it was amazing. It blew people’s minds. It was a revolution in packaging in the ‘90s. Performance was better, the parasitics — the resistances and the capacitances — all got lower, and the chips could work so much better. Everybody was like, “Yeah, flip chip is the best.”

And as it improved over time, they made the distance between these solder balls closer and closer. So you could put more connections into the chip. If you wanted to put a thousand connections into a chip, you need these solder balls to have a short distance between them. That became a big thing — how to make these things smaller and smaller.

Austin: So that is the evolution of wire bonding and flip chip. For somebody who’s never seen the world of packaging before: wire bonding — think of the simplest thing possible. If you’re in a lab building something for a class and you had a wafer, you would probably literally glue it onto a PCB and then attach wires from the die — from the leads, the edges of the die — to your PCB. You can imagine that is both very labor intensive and very error prone. And you kind of have these weird exposed wires. And like Vik said, they’re long and they have resistance, and it just feels fragile.

So of course, the flip chip is nice because now instead of having the top of the wafer where you have to attach wires, you just turn it upside down and have these short, direct connections. Now it’s the back of the wafer that’s exposed to the elements, and the connections are made by sandwiching these together. You have these little micro bumps — electrical conductors to help you attach and connect the die to the PCB below it.

Once you figure out how to do that with high yield and at scale, it’s a little bit less labor intensive — more complex, but more reliable.

For those early decades, packaging was sort of the unglamorous part. The manufacturing, the logic chip and everything — that’s the front end of the process, where the value was captured. Very complicated, very CapEx intensive. And packaging was really just mechanical assembly — even some human assembly. CapEx light, but also lower margin, lower value add.

And so the industry structure, way back in the day: people used to manufacture their own wafers and do their own packaging. But eventually some of that packaging got outsourced to OSATs — outsourced semiconductor assembly and test. Think of companies like Amkor, ASE, SPIL, Powertech. The foundry ships finished wafers, the OSAT dices them, wire bonds or flip chips them, molds them, puts them in a protective casing. And usually the OSAT does the testing too, to show that the final package still works. So just for the rule of thumb: fabless companies design it, a foundry fabs it, and OSAT packages it. But of course, companies like Intel — IDMs — do some or all of it in-house.

Vik: Yeah. So that’s the basic coverage of what packaging is — and it’s been around a very long time.

As a personal anecdote: even when I started working, I ran into a lot of the packaging guys. And those were just like — it seemed like a necessary evil. “Yeah, we gotta send it for packaging.” Nothing fancy about it. Just grunt work — make sure the chip can sit inside, do all these tests for whether it survives the heat and temperature. It’s like dotting the i’s and crossing the t’s of the semiconductor world.

It did become a performance limiter at some point, even in my own work early in my career. These parasitics — when it becomes a flip chip — became lesser. And it was important for the RF work I was doing. Those things matter. Wire bonds are still terrible. Because my work was so parasitic-sensitive — RF and all that — it was important. And flip chip saved a lot of design work because when you design the chip, it works just as is. You don’t have to account for the package as much.

However, as things got more complicated, packaging became part of the design process itself. It eventually became part of the chip — or an extension of the chip. And now, if you look at all the AI chips, it is the chip. Without advanced packaging, there is no chip. So I think now there is no chip without the packaging — and it’s good to define how we transition into advanced packaging, right?

Why Advanced Packaging Exists

Austin: Yes, yes, totally. If what we talked about was simple packaging, then what is advanced packaging? What puts the “advanced” in advanced packaging?

Vik: Well, ultimately, in a dream world, we would just have huge monolithic silicon chips — because you would have the fastest communication and the lowest latency between dies.

Austin: But as we talked about before, there’s something called a reticle limit. You can only make silicon dies so big. There’s also the concept of chiplets — some things don’t scale when you make transistors smaller, like SRAM or IO. We talked about this with Clearwater Forest, where Intel says: let’s make the compute dies using 18A with the smallest transistors possible, but use Intel 3 and Intel 7 dies for IO and memory. Ultimately those need to get connected together.

And even if you’re Nvidia making GPUs where your GPU is at the reticle limit — they make it as big as they possibly can — they actually want even more compute, so they take two of those. With Grace Blackwell, there are two GPUs — two huge reticle-size GPU silicon dies — but they want them to behave almost as if they’re still just one big piece of silicon. That’s always the goal. And you can’t do that with wire bonding. Flip chip is a step in the right direction, but can we do even better?

Advanced packaging is saying: could we actually use the same semiconductor processes as the logic chip itself? Could we use deposition, etch, and lithography to actually pattern metal interconnect at micron-scale pitches, instead of big wires? Could that give us lower latency, smaller resistance? Going back to tau — RC time delay — could we shrink features even in the packaging to limit tau and really make it seem as if these dies being stitched together are more like one piece of silicon?

Vik: Okay, yeah. So that’s the fundamental basis for the two technologies we mentioned in the beginning — TSMC’s CoWoS and Intel’s EMIB. These are technologies designed to hold multiple chips together — whether it’s HBM and a GPU, or multiple GPUs like the Blackwells or the Rubins. And those chips are really huge. Since you can’t make one infinitely large GPU die — you have to stay at the reticle limit, which is actually 858mm², a 26mm by 33mm reticle — to make it bigger and add more compute, you’ve got to put multiple reticle-limited GPUs into one substrate.

And then you hook them up with very, very fine wires, because the number of connections between GPU to GPU, or GPU to memory, is way too many. There are just an incredible number of wires. And the connection that happens between them is not just on a single level. Whatever the interconnecting mechanism is underneath these chips has to support pretty complex routing.

Austin: That are all very finely featured — that’s the key that makes this advanced packaging. These are not crude traces like a PCB. These are almost chip-level features being printed on substrates so that you can make one die almost an extension of the other.

Vik: Yes. And HBM3, I think, had something like 1,024 signals. There are a lot. And you’re having to route all of those to the GPU in small dimensions. Think of it as an ultra-mini PCB, but as small as possible.

Austin: And HBM4 took it to 2,048 parallel lanes. That’s an example of why you need very, very fine interconnects — very fine metal lines between these chips on this interconnection substrate. And that has become the stronghold of maybe one company, maybe two, in the world today, right?

Vik: Yes. TSMC dominates the CoWoS packaging required for all AI chips today. And they are extremely capacity limited, because the way TSMC does it is actually a wafer fab process. It’s not something you can do in an external third-party factory. You need sophisticated fab equipment to be able to make these things. And that’s where the whole “advancedness” of it comes in — and why somebody like TSMC, who knows how to make this with high yields and has a long history of running a foundry, is dominant. Not everybody can get into this game.

Austin: Yes, yes. This is a really interesting point. Going back in history: everyone used to be their own IDM, and then people said: let’s outsource the back end and let OSATs do some processing. Along the way, foundries came up, and even TSMC — which was a foundry — said we deliver the wafer and someone else can package it. Not huge value there.

But now we’re talking about advanced packaging that takes the same know-how as a foundry. The same tooling, the same expertise. So all of a sudden: simple packaging is still totally used — high volume, cheap to expensive components — but this advanced packaging bit is something that fabs capable of making logic chips or memory chips can actually do.

TSMC entered advanced packaging — I think in the late 2000s or early 2010s — where they started looking ahead and saying: this will be a thing, and this is something we could do. It could create a new market or bookend what OSATs can do. TSMC started doing R&D and came up with CoWoS. They also did some early work on InFO — integrated fan-out packaging — which we probably won’t talk about much today.

But I wanted to point out that OSATs are now trying to say: we want to get into advanced packaging too. If you go listen to Amkor’s earnings call, you’ll hear about this — because that’s where a lot of the value is accruing, and it’s going to be more and more important going forward. A forward-thinking OSAT is saying: I don’t want to be left out. I want to get into the advanced packaging game.

Vik: Yeah, that’s amazing. And now what happens is that once advanced packaging has gone into a fab — and traditional OSAT packaging houses like Amkor want to get a piece of the bigger pie by doing what a fab does — anybody doing this now starts to run into the same limitations of wafer manufacturing and chip making.

To put this in perspective: we spoke about the reticle limit being 858mm². The H100 was already at that limit. And you mentioned that the Blackwell die is basically two reticle-sized dies stitched together into one GPU using CoWoS, right? So what’s the next one? How many chips are we gonna put in next? We already have two.

Austin: I believe for Rubin there are supposed to be four GPU dies stitched together. So with the four-die thing, it starts getting complicated. The manufacturing process for the packaging that holds these dies together is the same thing used for the chip itself. What that means is: you couldn’t make chips bigger than the reticle limit — which is why it stopped there. But now you need to make packages that are bigger than the reticle limit — otherwise, how are you going to put two GPUs into one and stitch them together?

These packages that you’re running in a wafer fab process now need to be, let’s say, two-reticle-sized to hold two chips. Usually more, because you need to put HBM and other stuff — maybe three-times. The first generation of CoWoS was actually something like 3.3x the reticle size. And that started becoming the limiting factor.

The question is: how can you make packaging substrates bigger than reticle limits but not ICs themselves? I’m not entirely sure of the right answer, but my educated guess is that these wafer fabs that run packaging substrates are actually much simpler — you don’t actually make transistors. And so you can probably stitch together a few reticle shots and make a larger substrate that can hold maybe two or four GPUs at one time. Is that the right answer?

Vik: Yeah. Well, by definition, advanced packaging has to be bigger than reticle size, because you’re taking reticle-size dies and wiring them together. The key is that ultimately advanced packaging is still just drawing wires. You’re not trying to, in one shot, draw a bunch of tiny transistors. You’re not using 18A-style pitch and tools. You’re using semiconductor tools, but it’s still bigger — you’re drawing metal wires.

And I don’t think you’re drawing all the wires in one shot. You’re probably putting wires in over here and over there, still stepping around.

2D, 2.5D, and 3D: What Each Actually Means

Austin: So this whole Chip on Wafer on Substrate — CoWoS technology — is typically referred to as a 2.5D packaging technology. It’s only 2.5D because you have an active piece of silicon with transistors packaged over a passive piece of silicon without transistors — but it’s still silicon. That is the chip-on-wafer process. The chip with active elements like transistors is packaged over silicon-on-wafer — chip on wafer — and that is 2.5D.

The 3D version would be stacking a logic chip on top of a logic chip — active on active. So 2.5D is active on passive, 3D is active on active. That’s a packaging technology that exists in fabs too, but we won’t get into it much today.

Vik: Yes. So let me say it again, because the terminology is weird — but this is industry standard. There’s 2D, 2.5D, and 3D. And 3D is really cool — we should talk about it sometime — but we won’t get into it a ton today. Just to define these things, because people are probably thinking: two dimensions, like a piece of paper. Three dimensions — we live in a 3D world. What the heck is 2.5D?

Again, just industry conventions. Sorry, the semiconductor industry is weird. Just like “18A” doesn’t mean things are 18 nanometers — that’s kind of a lie — and 2.5D is also a lie, but it’s just the naming convention. Engineers don’t overthink this.

So basically: when we talked about flip chip or hybrid bonding, think of that as 2D. You’ve got a die and you slap it on a substrate and you wire it together — the die is just 2D. 3D is the far other end of the spectrum: you’re stacking things, like building a skyscraper. Multiple stories.

2.5D is: hey, we’re going to increase the size of this house, but instead of building many stories, we’re just going to put a bunch of little houses next to each other and build a hallway that connects them all. So you’ve got a compute die and another compute die — two GPUs, for example — and you’re stitching them together. That would be 2.5D.

Austin: And technically, HBM memory connected to a GPU is also considered 2.5D — which can get a little confusing because internally within HBM, it actually is 3D — it’s stacked. HBM can be 12 high or 8 high or whatever. But I’m giving you way too much information — you’re probably getting confused.

But generally, when you think about 2.5D: one story, chips next to each other, and they’re connected. And as Vik said, there’s a key point in 2.5D — we’re going to finally explain what CoWoS is. Vik, let’s talk about chip on wafer on substrate.

Vik: Okay, yeah, we’ve got to get to it. But all this background is important — otherwise, if we just dive right into CoWoS, people who aren’t familiar with this stuff just lose context immediately. I’ve felt it in the past. I think this background was useful.

So chip on wafer on substrate. The chip — the GPU — is sitting on a wafer. The wafer in this case is a piece of silicon, but it doesn’t have any transistors on it. It just has metal lines that can connect to a neighboring chip sitting nearby. That’s the chip-on-wafer. And this stack — this chip sitting on a piece of silicon — now sits on top of a substrate. So it’s a three-layer stack. That is CoWoS. And that’s the big thing TSMC made go into production around the early 2010s with FPGAs, initially.

But it actually enabled the stitching together of multiple active pieces of silicon. Now the obvious question is: why do you need this wafer in between? Why not just put the chip directly on the substrate?

Austin: What is this interposer? What is this intermediate wafer — sometimes called an interposer, sometimes a passive silicon wafer? Are these all the same thing?

CoWoS: Three Flavors

Vik: Yes, these all mean the same thing. And why it’s required: on a substrate — something like a PCB, or an organic substrate made of organic materials — you can’t pattern fine lines. And that’s the whole problem.

The CoWoS solution was: okay, we don’t need to pattern the fine stuff on the substrate. We’ll just do the coarse stuff on the substrate — power lines that come into the chip, hooking it up with the outside world. But the connections between the chips need their own separate layer, which requires foundry-class technology to connect those things together. That’s why you need a silicon interposer. That’s what “chip on wafer” does.

Austin: Yes, exactly. It’s about that intermediate layer — so you can have very fine-pitched routing, lots of wires, lots of signals.

So TSMC started with CoWoS-S. There are different flavors of CoWoS, and we’ll talk about three of them.

CoWoS-S — Chip on Wafer on Substrate with silicon interposer — means that the middle layer of the sandwich, where the routing happens, is a big silicon interposer. The nice thing about silicon is that it’s great for fine-pitch metal. And then you have TSVs — through-silicon vias — that come up to the chips. The downside is that it’s expensive. Now you’re using silicon wafers for routing. Ideally we would use the world supply of silicon wafers for logic, but now you’re using silicon wafers for routing.

Which is fine, but it can be expensive. So naturally the question is: could that intermediate layer be something cheaper? Do I have to have silicon?

So TSMC came out with something called CoWoS-R, where you have an organic RDL — redistribution layer — interposer. The R stands for RDL. This routing layer is a cheaper organic material, not necessarily the same material as a substrate, but cheaper. And you can route through that.

Now, if you were paying attention, you’re going to say: but Vik literally just said organic materials are not good for fine-pitch routing. And that is the trade-off. If you have this middle layer — maybe it’s ABF or something — you can’t get as fine a pitch of routing as you can with silicon. And there’s also dimensional stability: these organic materials can shrink when heated, absorb moisture, warp. Routing connections can move around or disconnect or short circuit. That limits how closely you can put the wires.

So CoWoS-R cannot support GPU accelerators, but it can still be a nice advanced packaging path — maybe for lower-end smartphones or automotive chips. But it’s not what we need for AI accelerators.

So then the question is: do we just have to use CoWoS-S with the expensive silicon? And the answer is no — there’s another step from TSMC that tries to get the best of both worlds. Could we get the routing density of silicon with more of the cost profile of an organic substrate? This is where CoWoS-L comes in.

L stands for local silicon bridges in an interposer. The idea: let that middle section of the sandwich be cheap organic material, but then wherever we need really dense, really fine-pitch wiring connecting dies — could we have just silicon there? These are silicon bridges.

So you have a big cheap organic substrate, but in certain places you put these little tiny silicon bridges and route through that. It’s an engineering trade-off: how can we get a little of the best of both worlds?

I’ll pause there. Any thoughts on CoWoS-L, Vik?

Vik: Yeah. So I wanted to let you finish going through the three kinds of CoWoS, because if I interrupt the flow of the trade-offs, it gets very hard to follow. Good explanation.

The one thing I wanted to mention: one problem with CoWoS-S — the silicon interposer — is that you’re essentially making a foundry-class packaging technology, which means the reticle size is inherently limited. There’s only so much you can do to make really large CoWoS-S packages.

Austin: You can only make them, what — 3.3x the reticle size, something like that?

Vik: Yeah. Very difficult to go past that. So the early generations of accelerators did use CoWoS-S in spite of the cost. But the industry grew out of it because the chips got so much larger.

And then comes CoWoS-R. I wanted to expand the R here. You said it’s an RDL interposer. RDL stands for redistribution layer. The thing with a redistribution layer is it’s usually a thin layer of polyimide dielectric. Within the polyimide dielectric, you can pattern about two or three levels of metal layers. Even in the chips I’ve worked with, RDL layers come in much above the chip — they’re outside the chip, really. You can even deposit RDL layers on top of a chip and route connections out via RDL. That’s a fan-out technology — it’s called fan-out because you can take one connection and fan it out to greater reaches that you can’t get out of a chip. The chip is so small and you want to connect it to a big PCB, so you have to fan it out.

So the redistribution layer has been around a long time. The idea was: why don’t we spin this same polyimide onto the wafer and pattern on that instead? And you’re not as restricted by reticle sizes, because it’s a different process technology — not fab-based lithography. So you could actually make stuff bigger. But like you say, it’s not nearly fine enough to connect AI accelerators together. So it never ended up being used for that.

The final thing: the best of both worlds. You take an organic substrate — stuff you can’t make really fine connections on. But then wherever you need the connections, just between the two chips you have to connect, you put in just the piece of silicon you need. There’s a very unique aspect to using these silicon bridges only where you need them: now you’re not restricted by reticle size, even though you’re using silicon interconnects between the chips — because you need to make these tiny bridges, of which you can get thousands per wafer. Then you just band-aid many chips together with the bridges. You get silicon-class interconnect performance without the reticle size limitations.

Austin: So you have the benefit from the CoWoS-S world — connecting with fine interconnect — but now you’re breaking the reticle size limitation. That’s the whole point of bridges.

Conceptually: with CoWoS-S, if you want to stitch together a ton of GPU dies, you have to have a huge piece of silicon underneath them. Could you have 20 dies? And you have the same lithography reticle stuff — you’d have to step all over the place to draw all these wires. But with bridges, it’s like: okay, I have a big cheap substrate, and I only need to take the silicon and put it in the little areas where I’m connecting dies. That’s CoWoS-L.

An analogy that came to mind: in Iowa, where I live, it’s very rural — mostly cornfields. We have roads that go all over the state. Ninety-nine counties, pretty much a grid, because everyone gets a square-mile-by-mile, 40-acre-type farm. We have all these roads, but we would never make all of them asphalt or pavement. Pavement is the best driving experience, but it’s expensive. We’re not going to cover the whole state with it, especially when there’s just one random farmer out there. So we put gravel everywhere. Gravel is way cheaper. Gravel is like the organic substrate — just throw it over the dirt so it gives you a little traction and doesn’t wash out, but it’s cheap. Pavement would be like silicon — the best, but expensive.

Now, yes, we live in Iowa, and maybe you call us hicks. But we’re not going to have gravel everywhere. In town, we still use asphalt. That would be CoWoS-L — use the cheap stuff to cover most of the state, the big areas that aren’t as heavily traveled. But then by my house, I want asphalt. Best of both worlds.

Vik: Only Austin can connect corn fields and chips like this.

Austin: Corn chips. For better or worse.

Vik: Corn chips are a thing. There you go.

EMIB: Intel’s Bridge Approach

Vik: So the whole idea of putting localized interconnects — fun fact — didn’t actually come from TSMC. It was Intel who initially developed this bridge concept. Before CoWoS-L. So there was this whole thing about TSMC copying Intel, and people said we should file a lawsuit because they copied us or something. But yeah, EMIB predates CoWoS-L.

The whole idea of EMIB was to eliminate the silicon interposer entirely. Even today, they skip the middle layer, they skip the interposer entirely. They just take the chip and put it on a substrate — bam, done — like gravel road all around. And wherever required, they just put in these multi-die bridges. What they actually do is embed this thing into the substrate. I think of pushing a piece of cracker into jello — that’s the feeling I have when I think about EMIB.

The benefit: obviously the bridges themselves are really tiny. You could make tens of thousands — or at least thousands — per wafer. But the substrate itself is not limited by reticle size, because it’s not even made in a fab. And the second thing: it’s not even in a circular wafer format. It’s made on square panels — because if you can make these substrates on square panels, there’s no wastage. If you’re cutting square shapes from a circle, you always have wastage. And the bigger the square shape you cut out, the fewer you can cut from the circle.

To your original point: silicon wafers are already difficult to come by. But then you make these gigantic packages on them and throw out half the wafer. The example is: my kids, when I make pancakes, always say, “I want shapes.” We have cookie-cutter shapes — we press them down, you get a deer and a squirrel, and they’re happy. But then they say, “I want another squirrel.” And there’s no more pancake left — the moose already took up the last one. I couldn’t cut out a squirrel and a moose. Now I have all these carcasses of pancake that I end up eating.

That’s exactly what happens with packaging. But if you’re cutting out rectangles, and you have a panel that’s already square, wastage is very little. And these panels are not the size of a 300mm diameter wafer. These panels are like 500mm by 500mm or something — much bigger than a wafer, by a factor of maybe five or six times.

Austin: Totally. And the point you make is very key: these little bridges are just little rectangles. Think of the die as a big rectangle, and the little bridge in between them is a little rectangle. And as we’ve always talked about with yield — the smaller things are, the better your yield will be intrinsically, because there’s just less surface area for a random defect to pop up. So EMIB can have good yield too.

Zooming way back out: we did wire bonding, we did flip chip, what’s next? We want to draw connections between things. We said the substrate is not a great place to do it. Intel had the foresight to say: why not just embed little bridges into the substrate? EMIB — embedded bridge. That’s how I remember EMIB. And that’s all they’re doing — taking that little high-yield bridge and embedding it down in there and connecting the die.

So what’s the difference between EMIB and CoWoS-L? As a reminder: both have bridges. CoWoS-L is a three-layer sandwich — bridges in the middle, which is organic material with bridges inside it. EMIB is just two layers — the dies and the substrate — with bridges embedded into the bottom layer.

Vik: Yeah. So EMIB itself has two versions you’ll see if you look it up.

EMIB-T means there are through-silicon vias going through the bridge. This is quite important for use in AI accelerators, because you need access to power and high-speed signals through the chip. So the TSVs are important.

And there’s another version called EMIB-M, which stands for metal-insulator-metal capacitors — MIM capacitors. These are capacitors built into the bridge, useful for power delivery. Whenever you put a power signal, you want a bypass capacitor so that power supply fluctuations get smoothed out through the capacitor. So it’s very useful to have them embedded — you can provide a clean power signal to whatever’s on the chip.

Intel has been doing EMIB for about a decade now — from early FPGAs to their CPU SoCs, and still using it now. Over time, as transitions have gotten smaller and density has increased, Intel needed to move beyond the original EMIB. That’s kind of where EMIB-T and EMIB-M came in — solving problems along the way, thinking: there are better ways to improve it so we can continue to have higher bandwidth, tighter density, smaller footprint.

CoWoS vs. EMIB: Trade-Offs and the Yield Question

Austin: Awesome. Now that we’ve described all the technology — do you want to quickly hit upon the value propositions of EMIB versus CoWoS-L?

Vik: Sure. Pros and cons between EMIB and CoWoS?

Austin: Yeah. Let’s go through the pros first and then we can try to argue why EMIB is bad.

Vik: Okay, sure.

Austin: So EMIB — pros: two layers instead of three layers. From a cost perspective, you don’t have to deal with the cost of the separate interposer, whether that’s silicon or organic substrate with local silicon in it. That reduces process steps, material costs, interposer dicing, interposer waste. Those are some cost things that come to mind.

You talked about panel utilization — the embedded die can come on a rectangular panel, and you can dice that up with less waste. Not only is the panel bigger, but utilization rates are very high compared to circular wafers. And on top of that, I’ll just mention briefly — we won’t get into it — but TSMC has the idea of going to what is called Chip on Panel on Substrate. They plan to go panel-level soon — by “soon” I mean 2028 or 2029. So they have this in mind as well.

Scalability past the reticle limit. Obviously if you have a silicon interposer and you want to make it big enough for a ton of GPU dies — it starts to get back to what Vik was saying: you’ve got a dinner-plate wafer, you take a big brick rectangle out of the middle, and that’s as big as it can get. You’re leaving all that area on the sides and the curved edges as waste. EMIB has cost benefits from that.

And then for EMIB — with just the embedded bridges — you can imagine scaling up to very large packages. Say you have a 3×3 grid of GPU dies. Well, you just put EMIB bridges between all of them. Why 3×3? Why not 4×4? You can see how it’s very scalable conceptually. And yield — you’re just making these little small pieces. There’s advanced packaging that has to happen, obviously, but naturally the yield is pretty good.

Those are some pros. Now the other side — what are some cons of EMIB?

Vik: The couple of arguments against it: one, it’s never proven at scale. TSMC has run a lot of volume on CoWoS. There’s a lot of history with AI accelerators. All the customers are very familiar with it. There is a risk going to EMIB.

Austin: Although it does look like from the last Intel earnings call, they have a lot of advanced packaging orders in already. So I’m going to push back on your pushback. Intel’s been using EMIB for a decade and they ship millions of chips every year.

Vik: Okay. So internally —

Austin: EMIB itself has a ton of reps. To put a fine point on your argument: you could say it doesn’t have a lot of experience in other people’s packages.

Vik: I see. Okay, so Nvidia has never built one with EMIB — although I think they’re considering it. Folks are considering it.

So Intel Foundry will tell you: hey, bring us your die — it can be from TSMC — and we will use EMIB and just do the packaging for you. You don’t have to commit to building your GPU with Intel Foundry just to unlock EMIB. You can build your dies wherever and Intel will just package it. But yes, there aren’t a lot of examples of that yet.

In theory, it should be no different whether it’s an Intel CPU stitched together with EMIB, or a Qualcomm CPU from TSMC stitched together with EMIB, or an Nvidia GPU stitched together with EMIB.

Austin: Or a Google TPU — which we’ll get there.

Vik: Which we’ll get there. But in practice, someone’s gotta go first at scale.

I always kept seeing this — and we posted about it in the Semi Doped Daily newsletter — the yield of EMIB is crossing ninety percent. I read somewhere it’s ninety-five percent. So if EMIB has been shipping for that long internally, do they already have yield at scale? Is yield something to even worry about?

Austin: I wouldn’t think so. And EMIB-T and EMIB-M are newer. I don’t know off the top of my head which chip was the first to use EMIB-T or EMIB-M. But Sapphire Rapids, Granite Rapids — these all used EMIB as well. At least the original EMIB, definitely at scale. So the yields will be totally fine.

Vik: See, that’s the argument — because somebody was saying: if the yield of EMIB is only ninety percent, that’s not good enough. The packaging yield has to be essentially 100%, because you’re putting a GPU on it. You’re burning a whole reticle’s worth of two or three nanometer technology. You can’t lose one chip out of every ten. That’s just not acceptable.

Austin: When I saw that, I was like — okay, I buy that. Nobody wants to lose one GPU out of ten to advanced packaging. So ninety percent isn’t good enough. So then I was wondering: what is TSMC’s packaging yield? Is it ninety-nine percent — you lose one in a hundred? Is it ninety-nine point nine percent — you lose one in a thousand? Nothing is a hundred percent. The higher the yield, the better. But I was a little surprised by the ninety-percent EMIB claim.

Vik: Because if you have product shipping in Intel internally — as you mentioned — the dots are connecting. Why is the EMIB yield ninety percent? Is it not ninety-nine point nine percent already?

When I hear “EMIB is ninety percent,” my question is: which EMIB, and who says that? Because some sell-side reports that report this stuff probably don’t know the history of EMIB deeply. They’re probably thinking: every new process has a yield, everyone has to ramp from zero. So — EMIB must have to ramp from zero. But I find it a little hard to believe.

It is a really interesting question: what are the CoWoS-S, R, and L yields from TSMC? I don’t know if that’s ever been published. That would be a nice data point. Obviously it must be insanely high, because everyone uses it. And literally — that’s why EMIB is interesting.

Google TPUs, MediaTek, and the Intel Foundry Opportunity

Austin: Right. That’s why there’s news recently that other people are considering EMIB. It’s not necessarily because CoWoS is bad or expensive or because yields are low. It’s because there is only a fixed capacity of these interposers and of all that advanced packaging.

And there’s been a slew of news around this, because apparently the Google TPU order seems to be booking three million TPUs to be packaged with Intel EMIB — around 2028. And apparently SK Hynix is testing EMIB for HBM integration as well.

And if you’re talking about the Google TPUs: it’s actually going through MediaTek, who is then using EMIB. MediaTek is becoming an increasing threat to Broadcom’s custom ASIC model, especially with Google TPUs — something to really watch out for. That’s why in recent earnings calls, people are realizing this tide is shifting from Broadcom toward MediaTek, and that’s why Broadcom stock has been low lately.

Vik: Yeah, and I wanted to mention one more very interesting thing that very few people pay attention to: Intel actually has an extremely good optics process. And technically, with their ability to package this stuff, they could use EMIB and their optical engines to make some really cool CPO stuff. Just saying — Intel has that ability to make CPO.

Austin: We should have a podcast on it sometime. Intel has a history of optics and photonics — not well known. Some stuff has gotten sold off. But the foundry has capabilities that open up interesting doors.

Now of course, Lip-Bu is here, laser-focused on customers, laser-focused on 18A+ as a better version of 18A, working toward 14A, trying to win customers — and it seems like it’s working. Both from a packaging perspective: they have a lot of advanced packaging capacity in New Mexico. You want to do EMIB? No problem. MediaTek — get your TPUs fabricated at TSMC, send them to us, we will stitch them together, no problem.

Everyone’s very focused on that. EMIB and the advanced packaging business are growing. David Zinsner, the CFO, said: “Don’t forget — advanced packaging alone, these are billions of dollars worth of commitments that we’re getting.” So it’s no joke.

Of course they’re trying to win customers to actually build logic chips with Intel Foundry. But if they have bandwidth, they ought to be throwing their weight toward CPO, optics, photonics. Can they make lasers? Can they buy lasers and package them? We’d have to go into exactly what their capabilities are, but it could be a really interesting opportunity for Intel Foundry.

Vik: Absolutely. And just in terms of sizes, let’s quickly summarize where we are now. The first generation of CoWoS was around 3.3x reticle size. Currently, the Blackwell Ultra class and Rubin class chips are all at the 5.5x reticle packaging that TSMC CoWoS is capable of today. The next generation planned will take it to 9.5x reticle size. And then they start talking about what is called System on Wafer, which targets something like 40x. I’m not sure exactly when that comes out, but even the 7x target is toward the latter half of the next few years anyway.

Austin: Totally. It’ll make for good launch events. It used to be: hold up a chip. Now it’s: hold up an SoC. Eventually they’re going to hold up this 7x big thing. And someday — maybe when our kids are doing this — are they holding up whole wafers? I mean, Cerebras already—

Vik: Yeah, yeah, Cerebras is one.

Austin: CoPoS or whatever — that would circumvent the whole System on Wafer discussion. We’ll save that for another episode.

Vik: Yeah, yeah. We’re not gonna do that. But what is the biggest EMIB package size right now?

Austin: I don’t know exactly what it is today. I know that with EMIB-T they’re going to get to 8x reticle size — maybe that’s where they are today. And then in just two years, they’re going to get to greater than 12x reticle size by 2028. And it’s rectangular — like 120mm by 180mm. If you Google it, it’s cool — they’ll show a 2×4 grid of dies, and you can see all the little rectangles that are the bridges connecting on the perimeter of the dies and in between them. Your 2×4 grid, little bridges on the outside connecting to HBM or whatever, and in between stitching everything together.

Vik: So yes, CoWoS is good, EMIB is also good. They have their pros and cons. I hope you learned a lot about packaging, about advanced packaging, about CoWoS and EMIB. And thank you for listening.

Austin: Thank you to everyone who’s listening. Very long episode — maybe we’ll edit it down a tiny bit. We’ll see. But I hope you enjoyed this.

To our YouTube listeners: thank you so much. We had so many YouTube listeners listen to our last one on tau scaling. Tons of comments, tons of engagement — really appreciate that. We read all of them. It’s super enlightening and fun to see you all learning and engaging. Thanks to everyone who downloads the podcast and shares it with their friends. People who watch on X too — also cool. Good luck with the SpaceX IPO. And that’s it.

So if you’re enjoying Semi Doped, share it with your friends. Subscribe to our newsletters. We have little takes daily at semidoped.com — totally free. Check it out. Share it with your friends as well. And with that, we’ll wrap it here.

Discussion about this video

great explaination .. keep up your great work guys
