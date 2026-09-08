---
source: https://daily.semidoped.com/p/new-episode-globalfoundries-thomas
title: 🎙️ NEW EPISODE: GlobalFoundries Thomas Barber: CPO, Silicon Photonics, 300mm, SiGe, OCI, NRZ
kind: transcript
---

🎙️ NEW EPISODE: GlobalFoundries Thomas Barber: CPO, Silicon Photonics, 300mm, SiGe, OCI, NRZ

Austin talks with Tom Barber, VP Communications Infrastructure and Data Center at GlobalFoundries, about the company’s deep, often overlooked, history in silicon photonics. Tom explains how GlobalFoundries became a leader in the space, the critical role of 300mm wafers, and the industry’s shift towards new optical interconnect standards to overcome copper’s limitations in AI data centers. 💡

Things we cover:

GlobalFoundries’ history in Silicon Photonics

GlobalFoundries’ history in Silicon Photonics

The shift to 300mm wafers for optical components

The shift to 300mm wafers for optical components

Copper’s limitations in high-speed data centers

Copper’s limitations in high-speed data centers

Co-packaged optics (CPO) reliability and power efficiency

Co-packaged optics (CPO) reliability and power efficiency

The OCI Multi-Source Agreement

The OCI Multi-Source Agreement

NRZ modulation for scale-up networks

NRZ modulation for scale-up networks

Silicon Germanium’s role in high-speed transceivers

Silicon Germanium’s role in high-speed transceivers

This podcast is lightly edited for clarity.

GlobalFoundries’ Photonics History

Austin: Hello everyone. Today we have a special guest, Tom Barber, VP Communications Infrastructure and Data Center at GlobalFoundries. Hey Tom.

Tom: Good morning. How are you?

Austin: Good, good. Thanks for coming. So today, I want to talk about GlobalFoundries and your photonics and optics background and experience as a company. I don’t think most people think of GlobalFoundries when they hear CPO or when they’re thinking about photonics. So I thought you’d be the perfect person to talk to on this topic.

So, I think right away when I heard of GlobalFoundries in this space, I thought, wait, GlobalFoundries does photonics? Most people probably like me know GlobalFoundries as the foundry that was in the running at the leading edge for a while and then stepped back and started focusing really on foundational nodes. But what people like myself don’t know is that you actually do have a background in the business of moving data with light, and you have for well over a decade. I think it traces back to the IBM Microelectronics business. So maybe start very high level for us, like what is GlobalFoundries even doing in photonics? How far back does it go? Just educate us.

Tom: Sure. Yeah, and I think GlobalFoundries’ focus is really on what we call essential silicon, right? And that’s the foundation of all our electronics systems, including data centers, right? It’s power, it’s communications, it’s memory, it’s all the things that are essential to making these communications, these electronic systems work. And Silicon Photonics perfectly aligns with that strategy. It’s very differentiated, it’s very complex technically, and it’s in a very challenging market, right? So there’s great opportunity to differentiate.

For those people that don’t know, GlobalFoundries, we were born out of AMD. We were the AMD foundries that were spun off. But over time, we acquired both Chartered Semiconductor, which had a Silicon Photonics effort, and we acquired IBM Microelectronics, which has a long history in Silicon Photonics. The effort at IBM Microelectronics actually started in the mid-2000s with doing very basic integration of waveguides, modulators, and photodiodes into CMOS technologies.

In the mid-2010s, so after about 10 years of effort, that turned into real products, shipping 25 gig per lane type of products, shipping in mass volume. The volumes were fairly small at the time because it was really only used for long-range point-to-point communication. But we’ve continued to invest and now we’re on our third generation of integrated Silicon Photonics, and that’s really what’s being rolled out in mass scale in the data centers today.

Austin: So interesting. Okay, so the history traces back. You got AMD and acquisitions of Chartered Semi and IBM Microelectronics. That’s super interesting. And yes, it sounds like you’ve been in this long-distance optical communication space. So I did not know that.

Now, what also surprised me is I’d heard recently that GlobalFoundries claims to be the largest pure-play Silicon Photonics foundry by revenue. And again, I think people think of TSMC or they think of Tower Semi. And again, that’s kind of like a shocking fact. So can you maybe tell us a little bit more about like is that true and tell us a little bit more about the business?

Tom: Yeah, so that is true. I think that’s really, we have been working with key customers for a very long time, and growing as the business grows. And that’s been key to us to make sure that we have those strategic customers in place that are the market leaders. The second piece of this is we made a very early investment in moving Silicon Photonics to 300 mm foundries, right? We’ve put it into our facility in Malta, New York.

And that’s been huge for us because it has allowed us to significantly expand our capacity. And that’s what the market is looking for as much as anything right now is they’re everybody’s just desperate for more capacity and we are available to provide that capacity. As a part of that, we added the AMF team in Singapore, which brought in a full range of very highly differentiated products that were actually orthogonal to what GF was doing. GF’s primary focus was on short-range and data center products, where AMF was doing a lot of business in long-range. And so that helped us round out our portfolio and added a complementary set of very high-value products. And the combination of the GF Silicon Photonics business plus the AMF business is what made us number one by revenue.

Austin: Ah, okay, okay. So there was the short-range play and the long-range via the acquisition.

Scaling with 300mm Wafers

Austin: One interesting thing, going back a little bit, you said moving to 300 mm wafers. Can you explain that more? Like was that coming from 200 mm to 300 mm and why is that such a big deal to unlock more capacity?

Tom: Yeah, so yes, most Silicon Photonics today is actually still produced on 200 mm wafers. That’s where most of our competitors are. When you go to a 300 mm wafer, it’s the radius squared, right? So you go up by 50% in radius, you square that, you get 2.25 times as many die per wafer, right? So running the same number of wafers, you get more than twice as many units coming through.

And that’s really important as we scale. Photonics, even going back five years, was a relatively small business, right? For two reasons. One is, there were other alternatives, Indium Phosphide and EML that were very competitive at 50 and 100 gigabits per second. Plus, the overall market was just significantly smaller. The data center piece had not really taken off yet. But with the data center piece taking off and 200 gigabits per second being the node that’s really taking off, that’s the optimal place for Silicon Photonics and that’s why we’ve seen an explosion in Silicon Photonics. So having that extra volume available via 300 mm wafers is really helpful.

The Limits of Copper and the Rise of Optics

Austin: Yes, okay, so let’s talk more about this 200 gigabits per second and sort of the opportunity right now for optics and maybe let’s talk like scale up. So I know, early rack scale AI systems, the switch was at the top of the rack. You had like eight GPUs interconnected in nodes and they were connected to a switch at the top of the rack. But as these racks are getting denser and we move to 200 gigabits per lane speed, now all of a sudden, I think it’s difficult to get the—I know the switch has moved to the middle of the rack because it’s harder to reach from top to bottom. So like unpack the problem that the industry is trying to overcome right now.

Tom: Yeah. So it all comes down to the fundamental limitation of copper, which is range, right? So at 100 gigabits per second, a direct attached copper cable—so no intelligence, just a dumb cable—could span about 2 meters, which is basically the height of a rack, right? So you could go, any connection within a rack, you could do with copper without a problem. When you get to 200 gigabits per second, that range drops to about 1 meter, which is why when you look at like an NVL 72, they move the switches to the middle of the rack because that’s kind of as far as they can go realistically. When you go to 400 gigabits per second, now the range is half a meter and you’re not going to quarter the size of the rack, right? So you have to go to something faster or something, yeah, something with more range, which is optical. That’s really kind of the high-speed stuff. And that’s within a rack.

Now, right now, most of the scale-up networks are within a rack. So an NVL 72 is one rack. The Helios that was just announced by AMD is a single rack. But you really want to go to multiple racks. And when you go to multiple racks, now you’re talking about spanning tens or even hundreds of meters and that’s when you absolutely have to switch to optical. You cannot do that with copper, not at the speeds we want to do.

Austin: Okay, so for scale up, what you’re saying that copper is getting shorter and shorter and so one way to move forward is to just try to move the switches closer and closer to the GPU, but ultimately that’s going to run out of steam. So even within the rack, you might need optics. But then, of course, the question is why stop with one rack? Why not have a scale up domain that could stretch into neighboring racks or four racks side by side? And so, of course, now it’s about like shrinking, but then it’s about expanding as well. And you’re saying that only optics can pull that off.

Tom: Yeah, if you look at what Google has done and even what Huawei has done with their scale-up networks, they’ve gone beyond a single rack. So instead of being limited to, you know, 72 or 144 GPUs, depending on how you count them, they’re doing 300, 500, 1,000 GPUs across, you know, six, eight, 10 racks, right? So they’re really expanding the size of their scale-up network using optical communication to span multiple racks.

Austin: Gotcha. Okay, so then walk me through, are we talking about like pluggables for the optics or NPO or CPO and where does GlobalFoundries come in?

Tom: Right. So, it can be any of those options. What we see is a trend from pluggables first going toward NPO and then toward CPO. And the reason is really cost and power and density. So when you’re at the edge of the rack with a pluggable, you’re looking at about 35 dB of loss from the edge of the rack to the GPU or switch ASIC in the middle of the server, right? That loss has to be compensated for by a, you know, kind of expensive and pretty power-hungry DSP in the pluggable.

When you move to an NPO system, now you’ve dropped your loss from about 35 dB to somewhere between 15 and 20 dB, right? That allows you to significantly reduce the amount of compensation you need to do on the electrical side, or even eliminate it, right? So if you have enough link budget end to end, that you can handle the extra 15 dB of loss on either end due to the transition from the NPO to the core processor, then you can get away with not having a retimer in the NPO, which is what most people are doing. They’re doing what’s called linear. And so that removes that DSP from the system, which saves a lot of costs and it saves a lot of power. But you still have a fairly bulky package for this NPO.

And what you want to do, and you still have a lot of loss in the system, right? There’s still 15 dB of loss that needs to be compensated for. If you continue to co-packaged optics and you move that transition from electrical to optical into the package, now you’ve dropped your loss from 15 dB down to like 6 dB. And that really helps you both from the link budget, obviously, because you’ve gotten yourself an extra 20 dB, but that also allows you to lower the power of your SerDes significantly, right? So what we’re trying to do is we’re trying to minimize the number of picojoules per bit that you need for the communication. So in a pluggable, you’re talking about a fully retimed pluggable is somewhere around 20 to 25 picojoules per bit.

When you go to NPO, you can go to linear and get rid of the DSP, which does a lot. It gets you down to maybe 10 picojoules per bit, but you still have a pretty powerful SerDes to overcome that 15 dB of loss between the co-processor, core processor, and the NPO. When you go onto the package with the GPU or the ASIC, now you’re talking about 3 dB of loss, and now you can go to the lowest power SerDes, which allows you to get down to less than 5 picojoules per bit.

Now, that’s really critical because all of these systems are thermally limited. So every picojoule of power that goes into the communications is one you can’t use for compute. So what you want to do is minimize the amount of power that you use for the communications between the GPUs, so you can run the GPUs as fast as possible.

Austin: Sure. Okay. So, if we orient around power, the goal is to in a given a fixed power budget in this data center, it’s only got 50 megawatts or 100 megawatts, whatever. We want to use as much power as possible for compute and as little as power as possible for communication, sending data around.

CPO Reliability and Cost Advantages

Austin: Now, talk us through again why, kind of zooming back out, you talked about pluggable. Why do they have so much loss in them? You talked about they have a DSP, but like where does the loss come from? Because I think people—it’s not in the optics, right? It’s like the electrical trace.

Tom: Yeah, it is. It’s the electrical traces through the PCBs from the core processor, a couple hundred centimeters to the edge of the server, right? And so those are very thin wires, and when you’re talking about, you know, a 200 gigabit per second PAM4 signal has about 55 gigahertz of bandwidth, right? So you’re trying to run a 55 gigahertz signal through a very long trace on a PCB, and you end up with a lot of loss.

Austin: So then a step in the right direction, NPO, near pluggable optics, you’re ultimately shortening that trace and then finally co-packaged optics, maybe you’re getting rid of it entirely. But can you walk us, can you walk us through the trade-offs of, you know, why doesn’t—why doesn’t—I know people are talking about using NPO as a stepping stone to CPO. So can you talk us through like, why not just jump to CPO if it’s the most power efficient?

Tom: Right. So the concern with moving away from pluggables is the reliability. Right? So right now, optical communications in general is seen as a reliability risk. And so the data center customers are very comfortable with it being pluggables because if something goes wrong, they just swap the pluggable, right? Just take one out, put a new one in and move on.

They don’t always do root cause to ensure that the pluggable is really the problem, but if you swap out the pluggable and the problem goes away, then you’re fine, you keep going. Moving to near packaged optics is a half step in the right direction. Those solutions will probably be socketed, so they’ll still be relatively easy to maintain. You still have to open, you’ll have to open the server and swap it out physically, but it’s still something that can be swapped in place without completely replacing the GPU.

When you go to co-packaged optics, now you’re talking about something that is permanently attached inside the package of the GPU. So the reliability has to be extremely high. So data center customers, Meta in particular, are going through the effort to validate the reliability of those solutions right now. And Meta has released a couple versions of a study that they’ve had running for a long time with, you know, 50,000, I think it is, GPUs in a network using co-packaged optics. And what they found is the reliability is actually higher than it is with pluggables, and they found no link flap, which is the primary cause of concern in optical communications across their entire testing range, which I think is up to 50 million hours or something like that right now. So, you know, they’re doing the work and becoming more comfortable with the reliability, but they’re not going to deploy it at scale until they’re absolutely certain that it’s a reliable solution.

Austin: Fascinating. So tell us why—why do—why are people expecting that the reliability is not great for CPO and then finding out from Meta like, oh, actually it’s not as bad as you think. I mean, is this about like is the laser—is it an external laser and the concern was that the laser is sitting near a hot chip, but that’s not a problem or what is the problem that people think should be happening and it maybe it’s overblown?

Tom: I think it’s problems that are actually happening today because, you know, and again, there’s not great, actually done some good work on this and root cause, but, you know, the things that end up causing problems in optics, some of them are actually due to the fact that it’s pluggable, right? Because you’re plugging it in, there’s the opportunity for dust to get in the connector and block the optical signal, right? So when you’re swapping out a pluggable, if dust gets in there, all of a sudden you have a reliability issue, right? And it’s attributed to the pluggable, but it’s not the inside case of the pluggable that’s the problem really, it’s the fact that the pluggable, you know, there’s something interfering between the pluggable and the connector.

So, when you go to CPO and you have a fully integrated solution, you know, that’s done in a clean room facility, right? There’s no dust there, right? When you have things that are permanently attached or semi-permanently attached, you know, you’re not dealing with these connection issues that you get where reliability concerns appear. So, that’s what the hyperscalers are really trying to become more comfortable with is not that CPO will be as reliable as pluggables. That’s not good enough. CPO has to be way more reliable than pluggables. So, I don’t think anybody questions that CPO is as good as pluggables. The question is, is it so much better than pluggables that it can be made a permanent part of the system?

Austin: Gotcha. Sure, fascinating. So it’s almost how surprising if the idea was like, oh yeah, pluggable is like the release valve where if there’s a problem, you can unplug it and put something else in, but actually what if the problem is the pluggable, the act of plugging it in itself? It’s kind of funny. So yes, if you can make something co-packaged in a clean room facility, maybe dust never gets in and you actually don’t see those issues. That’s really fascinating.

So then, what about like cost? I mean, everything has a trade-off. So if CPO potentially has great reliability and it’s much lower from an energy cost, what about like dollars and cents? Is it more complicated? Is it expensive or does it is it all a wash compared to like linear or traditional pluggables?

Tom: Yeah, and again, it comes down to if you look at a pluggable, you strip away a lot of the components of the pluggable when you go to co-packaged optics, right? You obviously don’t need the case anymore, right? That disappears immediately. There’s a lot of support circuitry on there, some MCUs, some power, and in particular, especially the DSP that goes away, right? So the DSP is probably the biggest component that goes away from a cost standpoint. So that saves you a lot of costs, and then you get into the operating costs and when you have significantly lower power, that obviously translates directly to operating costs.

OCI MSA and the Shift to NRZ

Austin: Interesting. Okay, so, let’s move on a little bit. So I saw some news about the OCI MSA, like a multi-source agreement for optical interconnects. So can you enlighten us like what is an MSA? What is this and why does the industry write one? I think some of the names involved AMD, Broadcom, Nvidia.

Tom: Yeah. So an MSA is a multi-source agreement. And what it is effectively is the industry looking at a standard, typically a standard from the IEEE and saying, okay, this is great, but there’s a lot in here that maybe is options and what we’re going to do is we’re all going to agree on, here’s the options we’re going to do, here’s the options we’re not going to do, here’s how we’re going to test things, here’s how we’re going to make sure it’s interoperable. So that is what an MSA is. The one that’s—it’s not called an MSA, but honestly, the most famous MSA is the Wi-Fi Alliance. So the Wi-Fi Alliance takes the Wi-Fi spec from IEEE and turns it into something that can be productized, right?

The optical industry has typically had MSAs focused primarily around mechanical. So if you look at the, you know, there’s one for it’s called OFSP. That’s the form factor for the pluggable. So it defines the mechanical electrical interfaces so that when you plug these things in, they all work, right? The electrical interface is defined by OIF, and the optical interface is defined by IEEE, but the MSA kind of brings all those things together and says, okay, here’s how we’re going to combine these pieces and wrap them up mechanically such that we have an interoperable pluggable.

The OCI MSA is a little bit different in that it’s actually taking and defining the optical interface, right? So that for most the optical communication used in data centers is defined by IEEE, IEEE 803 802.3. That is not sufficient for what we want to do for scale-up compute, right? And OCI is really focused on scale-up compute. And so when you look at the participants, the founders of OCI, they are the key suppliers in the data center industry. They know absolutely what is the best solution for scale-up networking, right? And so they’ve come together and said, hey, listen, the specs, the optical specs that the IEEE is defining are not really fit for purpose for the scale-up application. This is what we believe is fit for purpose for the scale-up application. This is how we think you should do things.

And it’s really focused around maybe not going as far range-wise, because, you know, two kilometers maybe is a little too far for a scale-up network. So we’re going to back off on that a little bit, and we’re going to go to a wide slow solution. And what that is is, you know, to go as fast as possible with as much data as possible over a single fiber, IEEE has moved to multi-level modulation. So it’s called PAM4, and, you know, you transmit two bits per symbol and you have four levels. And the issue is those levels are pretty close together, so you have to either have a lot of power or very low noise to receive them properly.

What they’ve done with OCI, they’ve gone back and said, we’re going to go back to a binary system, so only one bit per symbol, and we’re going to slow it down to 50 gigahertz. But we’re going to do four wavelengths per fiber. So we’re going to take advantage of the fact that you can put multiple channels on a single fiber to still have that 200 gigabits per second of bandwidth. We’re just going to do it with four wavelengths. And what that does is it makes the receiver a lot less complex. So the amount of channel equalization you need goes down quite a bit, and the amount of forward error correction you need goes down by quite a bit. The native bit error rate for NRZ 50 gigahertz is about a million times less than what it is for PAM4.

Austin: Oh, wow.

Tom: So it’s significantly easier to receive an NRZ signal. And that translates into reduced costs and it translates into reduced power.

Austin: Oh, fascinating. Okay, so the industry is coming together saying we’re going to make an interoperable standard. And presumably that’s just so that there can be competition so that everyone can say, hey, we’re building to this spec collectively. And then what I heard you say, which is fascinating is it sounds like the industry is aligning around not just trying to continue to increase the per lane speed and double it, double it again, but actually to walk back a little bit instead of PAM4, go back to NRZ and say, hey, let’s go back to 50 gigabits per second NRZ, but can we send four like wavelengths down the same fiber, kind of four colors if you will. And those are being sent simultaneously?

Tom: Correct. Yes.

Austin: Interesting. So if there’s more if there’s different wavelengths being sent simultaneously, is that like a boon for like people that make the lasers? Do you need more lasers to do that?

Tom: So, just back up one second. Just to explain something about the difference between the scale-up application and the scale-out application. So the scale-up application, what you’re trying to do is you’re trying to connect as many GPUs as you can using a single hop network, right? And so if you look at the maximum size switch you get today is 100 terabits per second. And so with 200 gigabits per second per fiber, you can connect 512 GPUs to each switch, right? And then what you do is you stack up switches to give you the most bandwidth. So if you look at the NVL 72 system, they have 18 switches in parallel, which allows them to get to that 7.2 terabits per second bandwidth they have per GPU. But each fiber is only, or in this case, they use copper. Each copper pair is only 200 gigabits per second. It’s just shared over 18 switches.

The other thing that the OCI team has done really well is, so when you look at the amount of lasers you need, it’s not as simple as one laser per wavelength, because the laser power can actually be split and used by multiple fibers, right? So if I have a transceiver that’s got eight fibers connected to it, I typically right now the ratio is four to one, so I’d have two lasers to drive those eight fibers. But for pluggables, it’s actually moving to eight to one, so you’d only have one laser driving all eight of those fibers. With the OCI spec, they back that off even further to you can get to as extreme as 32 fibers per laser. So one laser could drive 32 fibers. So you could get a full optical engine solution with the eight wavelengths of light that’s needed for OCI with just eight lasers.

Austin: Gotcha. Okay. And then you were saying that we don’t need to think about like one laser per port or anything like that. In fact, the laser, the light can drive many different fibers, maybe as up to as many as 32.

Tom: Correct. In like the most extreme case.

GlobalFoundries’ OCI-Capable Scale Platform

Austin: That’s pretty cool. Okay. So now tell about where does GlobalFoundries come in here? I know you guys announced Scale and you called it the first OCI capable platform. So talking back to that MSA, can you explain a little bit more about Scale and, you know, how you’re the first OCI capable platform?

Tom: Sure. So what we’re doing with Scale is we’re putting together everything you need to do the electrical to optical translation in a known good form factor, right? And call it a chiplet, call it a module, whatever, right? And so what that includes is it includes an electronic IC, which is going to be used to communicate to the CPU or the GPU or the AI ASIC. And then that electronic IC sits on top of a photonic IC, which does the translation between electronic and photonic signals. That photonic IC has a detachable connector on there. And that detachable connector is key because when you’re assembling a CPU, what you don’t want to have to do is have a fiber dongle hanging off your photonic IC at all times. You want to create, you know, you want to build your server using rectangles, right? And then plug everything in at the end. And so with that detachable fiber connector, it looks very much like copper where you build all your PCBs, put them all together, and then you have a wiring harness, in this case, an optical wiring harness instead of electrical wiring harness, that you connect at the end that bridges from those CPU modules connected to the GPU to the edge of the server.

Austin: And GlobalFoundries, you can fabricate which of those pieces do you guys fabricate and assemble?

Tom: Yeah. So we have the ability to manufacture all of it. The photonic IC for sure, we do 100% of the manufacturing. We have a number of different design partners working with us on photonic IC designs. The electronic IC, it really depends on the complexity of the design, particularly the digital. So if it’s a less complex design, we can use our FinFET process or one of our FDX processes. If it’s a simple, you know, linear translation, we could actually use our Silicon Germanium process even. If it’s a more complex digital translation and a customer wants to use an advanced node, like a three nanometer or two nanometer node, then they’re free to do that and we’ll bring that wafer in and do the assembly and test. The micro optics, again, are manufactured externally, but we do the assembly and test.

Micro Mirror Technology and O-Band

Austin: Okay, fascinating. So then talk to us more about like position yourself against what some other people are doing. Like I know TSMC is in this space with CoWoS and they use a grating coupler and I think GlobalFoundries uses a different technology, an edge coupler. And could you maybe explain a little bit more about the technology differentiation that and the approach you’re taking?

Tom: Right. So we do, so, yes, the mechanism for the light getting into the waveguides is very similar to edge coupling, but we use, we don’t do it at the edge of the die. We actually have a micro mirror that we implant into the wafer, so the light can still come in vertically, right? So the light comes in vertically exactly the same as you would with a grating coupler. We just have a mirror and that reflects the light horizontally into the waveguides on the photonic IC. The reason we went with that approach instead of grating couplers is because grating couplers inherently have limited bandwidth. And so you can’t service the entire O band with a single solution. With a micro mirror, we can do the entire O band, which gives us the maximum flexibility as far as doing the wavelength planning, right? So, OCI today is four wavelengths in each direction. You know, one of the ways we’re going to scale that to do higher bandwidth is to add more wavelengths. And so as we’re thinking about how do we evolve into the future, we wanted to make sure that we made the entire O band available to use for as many wavelengths as possible.

Austin: Ah, fascinating. Oh, and for listeners who might not know, can you define like what does O band mean?

Tom: Oh, yeah. So the O band is it, you know, you think about AM FM bands for your radio. So O band is an optical band. It’s around 1310 nanometers, which I can’t divide by the speed of light in my head to figure out how many gigahertz that is, but or terahertz is, but it’s really, really fast.

Austin: Gotcha. Okay, thanks. That’s helpful.

Market Validation and Silicon Germanium’s Role

Austin: All right, so then, okay, so you guys are taking a different approach and you think, you know, it keeps the whole O band on the table, which will be helpful in the future as you’re trying to increase bandwidth, it will keep more wavelengths sort of at your disposal. At the end of the day, you know, I see people online and they’ll say, you know, oh, this one company’s better than the other, but it feels like a little bit sort of like armchair quarterbacking. Like, how, like, can you help us understand, as people interested in the space, like, how, how do we know as a non-engineer, non-silicon photonics engineer, how do we know how good, you know, GlobalFoundries components are? Is there like a good proxy or a good way to understand it? Is it just like checking the customers or what do you think?

Tom: Yeah, I mean, that’s the, you know, the market doesn’t lie, right? So the market will choose the best solution, right? And so that’s, you know, we’re at the very beginning of this market. And like I say, right now, you know, TSMC, other founders, they’re not the enemy to me, right? The enemy to me right now is copper. I’m trying to beat copper, right? If TSMC wins and we win, that’s great because we’re both displacing copper. And until all the copper is gone, there’s plenty of market to go around.

So, you know, I think the other thing that’s important to understand is that there’s two different types of components that are needed for these optical engines. One is the photonic IC, which is what we’ve been talking about, which is the silicon photonics piece. The other piece is the electrical ICs that are needed to drive the photonic IC. And those are typically high-speed analog components. And there’s two types of components. One is the driver, which is a modulator driver, so it amplifies the signal coming out of the DSP such that you can drive the modulator that’s the silicon photonics modulator on the pick. That to some degree is being integrated into the DSP, so the market’s shrinking a little bit on that.

The other one is a transimpedance amplifier. So that takes the current out of the photodiode, which detects the incoming light and translates it into a voltage, which is then converted and processed on the DSP. The bandwidth of those is similar to what I talked about earlier with the PCB. You know, for a 200 gigabit per second PAM4 signal, you’re talking about 55 GHz of bandwidth if you’ve got a retime system and closer to 70 GHz of bandwidth if you’re trying to do a linear system.

Typically for an amplifier, you need about the transistor speed needs to be 5X what your bandwidth is. So now you’re talking about transistors that need to run 350, 400 GHz to do the 200 gig per lane. When we talk about 400 gig per lane, now you’re talking about doubling that, right? So you’re talking about transistors that are 600, 700 GHz. Very, very few companies can do that at scale and reliably. And Silicon Germanium from GF is one of those few technologies, right? So we have, you know, very, very good Silicon Germanium technology. Our transistor speeds are extremely high, much higher, you know, higher actually than what you need for 200 gig per lane. And we have new generations, you know, roadmaps that support 400 gig per lane very quickly. So, you know, we’ve been fortunate that we’ve gotten a lot of adoption on 400 gig per lane. So as you see the 1.6T transceivers volume increasing, you know, we’re getting a disproportionate share of that right now.

Austin: Okay, interesting. So Silicon Germanium is about transistor switching speed. And as we see switching speeds, or bandwidths of like 200 gig, 400 gig, it means we should think Silicon Germanium and we should think GlobalFoundries.

Tom: Yes.

Austin: Fascinating. Awesome. All right, Tom, we’ve covered a ton of ground. It was pretty technical, but I appreciate you walking us through and teaching us and enlightening us also about GlobalFoundries, from a business perspective. So thanks so much for your time.

Tom: Thank you, Austin. It was great talking to you. I appreciate the time.

Discussion about this video
