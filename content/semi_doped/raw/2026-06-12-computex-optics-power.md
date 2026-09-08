---
source: https://daily.semidoped.com/p/computex-mania-2026-optics-and-power
title: 🎙️Computex Mania 2026: Optics and Power - Semi Doped
kind: transcript
---

🎙️Computex Mania 2026: Optics and Power

Six months into the podcast, Vik and Austin finally meet in person. The venue? Computex. 🔥

They break down everything they saw in Taipei, from Jensen calling Marvell the next trillion dollar company (the stock popped while Vik filmed the leather jacket) to a show floor wall-to-wall with CPO and 800V demos. Optics? Yes. Power? Yep. Prefab data centers? Yep. Intel Foundry? Oh yes.

Things we cover:

Jensen’s Marvell keynote cameo and the hundred billion dollar sentence

Jensen’s Marvell keynote cameo and the hundred billion dollar sentence

The copper wall, Teralynx, and whether CPO can actually scale

The copper wall, Teralynx, and whether CPO can actually scale

XPO modules, Ayar Labs’ scale-up CPO rack, and MediaTek microLEDs

XPO modules, Ayar Labs’ scale-up CPO rack, and MediaTek microLEDs

800V power delivery, silicon carbide at the grid, plain silicon below

800V power delivery, silicon carbide at the grid, plain silicon below

Prefab AI infrastructure blocks and a chest freezer full of GPUs

Prefab AI infrastructure blocks and a chest freezer full of GPUs

Clearwater Forest as an Intel Foundry flex (18A, EMIB, Foveros Direct 3D)

Clearwater Forest as an Intel Foundry flex (18A, EMIB, Foveros Direct 3D)

This podcast is lightly edited for clarity.

Back from Taipei

Austin: Alright, hello everyone. Welcome to another Semi Doped podcast. I’m Austin Lyons of Chipstrat, and with me is Vik Sekar from Vik’s Newsletter. We’re back from Taiwan, and I’m getting over my jet lag. This is my first time to Asia, and as hard as I tried to not have jet lag, my internal clock is just totally screwed up. So I’m back, I’m awake, I’ve got some coffee in me. And listeners, you may not know this, but Vik and I are six months into a podcast, but we’re actually in two different countries, and we met in person for the very first time. So Vik, you took a picture, it was pretty cool.

Vik: Yeah, it was awesome. It was totally cool to meet you. And when we met each other, the first thing that came to my mind is like, holy crap, Austin is tall, man. In video, I can’t really tell. When I met you in person, I’m like, who is this guy? Why is he all the way up there?

Austin: That’s hilarious.

Vik: I’m this small Indian dude. This is like my regular height — I’m kind of average, I would say, for Indian height. But yeah, Austin’s tall. So we took a picture — you can see the height difference there. We are on the same floor level. That was cool. It’s nice to meet you in person finally, after all this talking online. It’s amazing what you can do with the internet these days, right? You can start a whole podcast. We got this thing, we talk so much semis, but in person, it was awesome. We met so many people that were also in the online world, and you meet them all in real life.

Computex is such a big show. It’s amazing how big it was and how many people there were. All of them looking at this AI hardware stuff. I’m like, wait, are all of you really interested in AI hardware? I’m amazed.

Austin: Yeah, totally. I agree with you. It’s really cool to meet you in person and hang out more. And then just the other Substackers, YouTubers, people in the industry that we know of. It’s very humanizing — you get face to face, and you’re just like, yeah, this is another person who also has the same crazy interest that I do, going really deep on the businesses and the technology.

And I agree with you. On the one hand, we are in Asia and a lot of people work in this industry. But on the other hand — even with how the whole AI and semis thing has blown up in the last two years — it is still a little crazy. I’ve always been into this stuff, and it’s deeper tech than maybe just pure software. And it’s crazy to see there are hundreds of thousands of people that also feel the same way.

Of course, as they’re walking through, I thought, I wonder how many of them have seen the podcast. And if not, there’s a huge subscriber base right here, in the Computex pre-registration line. Where apparently I actually didn’t pre-register. There was literally a thousand people in this line where, if you pre-registered, you got to pick up your badge. And somehow I screwed it up and didn’t actually pre-register, so I got to go to a different place where there’s only 10 other people. And I was like, okay, I guess I’m never gonna pre-register, because I like the fast pass. But I looked at that long line and I just thought, we gotta get all of them to check out Semi Doped.

Vik: Austin is over there counting TAM. That’s my TAM right here. Computex is my TAM — my Substack TAM, my podcast TAM. But yeah, you’re right. I was truly amazed. And it’s so funny, because the previous evening, I think you had some events you had to attend, and by the time you showed up and we met, it was already past four PM. We went to the registration counter and they were like, no, it’s done for the day. And the next morning I walk into the venue and I see the lines at the registration. It goes the entire length of the conference hall or something — half a mile. I’m like, my God, Austin should have done this yesterday. He just needed to show up ten minutes earlier, and now I don’t know how he’s going to get his badge. But I’m glad you’re out there counting TAM.

Austin: Yes, totally. I thought the same thing. I was like, crap, I screwed this up — but then it turned out okay.

Niche Famous (and Ben Thompson on the Plane)

Vik: Another thing that stood out to me was there were so many people who came up to us and said, hey, I watch your podcast and I like it and I love what you guys do. Super thankful for meeting these people in person. Because it’s insane — we don’t know who’s on the other side of this video, right? But there are people, apparently, and it’s nice to meet them.

Austin: Totally. Yes. I felt the same way. When people subscribe to our Substack and read it, we can see the email of who signed up, so you get a general sense of who your audience is. But with the podcast, we just kind of throw it out into the ether. So it’s cool when people came up and they’re like, hey Austin, what’s up?

I had someone at breakfast one day that was like, are you Austin? I was like, yeah, what’s up? And then he was like, do you write a Substack? And I was like, yes. And then I was like, I have a podcast too, you know. It’s like niche maxing or something — in a very, very, very narrow niche, people know who we are, and that’s very cool.

But on my flight home — I was supposed to fly through Tokyo, but that got cancelled because there was a typhoon. So I hope all of our Tokyo listeners are okay, Japan listeners. And so I took a different flight, Taipei to SFO. And when I got there, someone sat down next to me. I was like, that looks just like Ben Thompson. And so then later I was like, I think that is Ben Thompson — he writes Stratechery, for those of you who don’t know. And so later I was like, hey Ben, I’m Austin, and I introduced myself to him. But same — I thought about him, he’s hyper famous in a certain slice of the world, and then everyone else at the airport has no idea who he is.

Vik: Yeah — for those who don’t know, I think we should mention this. Ben Thompson is the OG newsletter guy. He started a newsletter when there was no Substack or anything like that. Substack is built on Ben Thompson’s idea of creating an email newsletter. He has tens of thousands of readers, he writes every day, and he has a podcast. So we all know him in the tech world, but it’s so cool you ran into him in an airport. And he’ll be like, my God, nobody ever recognizes me here, but it’s only Austin who walked up to me. It’s a hyper niche thing. The moment we step out of Computex, nobody knows who we are.

Austin: Yes, totally. In my neighborhood, everyone just is like, that’s that dude that runs all the time. But other than that, people have no idea. And then you go to Taiwan, to another country, and all of a sudden people recognize me, and it’s like, this is weird.

Vik: Yeah, maybe this is a consequence of being in a highly populated country, because in my neighborhood somebody recognized me — I’m like, whoa, that’s insane, I was just going to buy milk. And then in the airport somebody said, hey, are you the guy who writes a newsletter? And I was like, yeah, that’s me. That’s amazing. In Computex too, we met so many people, and it was great.

Vik: But part of the Computex appeal is actually the exhibition, which is fantastic. It has multiple buildings and multiple floors of everything from AI racks to chairs. I saw chairs, okay — computer chairs that you could sit on and work on. And all the gaming and all that in between. I suppose it’s natural to have gaming chairs as well. It covers so much.

At one point I walked onto the ground floor, and there was a ton of people, and I was like, yeah, everybody’s looking at AI racks. But it’s not so — there was actually Jensen at the other end of it, looking at all the racks and stuff. I was with a couple of people — I think you had gone back already — and we were like, that’s it, dude. We’re not going into this hall right now. Because the way it is, there’s security walking on either side, making way for him, and he’s walking by.

Somebody told me people were keeping track of whichever booth he stops in and buying stock or something. Each place he went to was having these mini pops, and maybe people were counting — he stood at the Delta booth for twenty seconds. Hmm. Must be something there.

Austin: It’s like momentary arbitrage. You get a signal before everyone else. While someone else is posting the picture to X, you quick invest — and then everyone sees on X that Jensen stopped there, and then they buy the stock. That’s crazy.

Jensen Moves Markets

Vik: So talking about momentary events — let’s talk about the networking keynote I attended, which is Marvell’s. I was in the front row, because they let the media in. I guess I’m media now. So I was sitting there, and I was pretty surprised, because I didn’t have any idea Jensen’s gonna come trotting on stage. He comes in and is like, hey everybody, what’s up — and everybody was happy. Yay, Jensen, we get to see the Jensen. I was pretty happy because I missed GTC, actually. I’ve never seen Jensen in person. So I was pretty stoked.

Austin: Well, that was your first time seeing the leather jacket in the flesh. Cool. Nice.

Vik: I only write about all the stuff Leather Jacket creates on my Substack, but I’d never seen him in the flesh.

Austin: There you go. And how was it?

Vik: I don’t know — it is cool, I guess. I don’t think that one-time Jensen sighting is a feeling that’s ever gonna come back. It’s like, that’s Jensen, by the way.

And then he comes in and says, Marvell, everybody — the next one trillion dollar company. And I was like, ha ha ha, funny joke. You know why? Because just then Matt Murphy, the CEO of Marvell, had said, we have already had three trillion dollar memory companies recently in the AI boom. And I was like, yeah, that’s pretty cool. And I didn’t expect Jensen to come by and say, yeah, next trillion dollar company. I thought he was just saying that to make Matt feel better. Like, don’t worry, you’ll be a trillion dollar company too someday. And then I learned the next day — or the same day, whenever the markets opened — Marvell is up 70%. And I was like, my god, there was my arbitrage event. And I was there taking Jensen-in-the-jacket video the whole time. My video cost me thousands of dollars. I should have bought.

Austin: That’s hilarious. They were truly up like 30%. Maybe they got something crazy like fifty billion in market cap just from Jensen’s comment. Of course, you could say it was because of what they presented, and the merits were good and the story was good and whatever. Regardless, I thought to myself, man, Jensen goes around and gives two billion to this company, two billion to that company. At this point he doesn’t have to give two billion, he just has to give compliments — and maybe that’s even more valuable to the company than a two billion dollar investment.

Vik: Yeah, that’s more valuable. You can keep your money. Jensen says your company is good, and you’re better off than his two billion. So Jensen’s happy he gets to keep his two billion, and the others are seeing everything pop. Anyway, it’s strange times we live in. I thought it was funny because I have never been in the middle of an event like that. I think it was close to a hundred billion, actually. And it’s like, wow, I saw a hundred billion dollar sentence come right by my face, and I just let it go by. I did absolutely nothing.

Marvell’s Copper Wall and the CPO Question

Vik: But the whole talk from the Marvell CEO basically was, optics is here, and the copper wall has now moved out to the point that you can only do on-package stuff. Everything within the rack is now going to be optics. He showed this cool slide about that. I think the whole keynote was basically about Marvell’s prowess in optical interconnect, especially since they acquired Inphi many years back — great acquisition, I think they have a very strong optical portfolio now. They showed off their Teralynx switch, which is a 102.4 terabits per second switch — similar to the Tomahawk 6 by Broadcom, a similar 102.4 terabit per second switch. So that was their big announcement there.

And they showed a big, big tray of pluggables, and he’s pointing to it and saying, look at that — that’s how big it was. Those are big, right? If you have to do a pluggable implementation, those are really big. But then he showed the CPO, which was much smaller — the size of your whole hand extended. So it’s amazing the kind of compression in size CPO can bring about.

The whole show was essentially very heavy optics. People loved CPO. Every demonstration is CPO this and CPO that, and the talk was all CPO. That’s the sense I got, at least. So it was cool, actually. The whole keynote was nice. I’ve never been to too many such high-profile talks, right up front. All this is very new to me. But I had fun.

Austin: Yeah, good. I thought the Marvell keynote was good. I think Matt Murphy is a good public speaker. Of the stories I’ve seen them tell over the last say two years, I’ve always felt that Marvell has not done a good job of articulating who they are. Are they an ASIC company that also has interconnects? Are they an interconnect company that also makes custom ASICs? In this story, they really tried to position themselves as an interconnect company. And if I recall, they showed how the majority of their revenue was from interconnects, and then some of it was from AI ASICs. So I thought at least they narrowed in on, hey, we’re talking interconnects — think of us as a connectivity company. And then they talked a lot about the copper wall and their portfolio.

I did feel like they missed an opportunity to talk about how those two businesses can cross-sell each other. Think about it — if you’re Marvell and you’re making an XPU for someone, it’s not just about the XPU, it’s also about the XPU attach. And a lot of that is around interconnects. So the whole point I’m trying to make is they can say, we can work with hyperscale customers to make their XPU, XPU attach, their data centers — it’s really bespoke data centers. And that can help us sell the interconnects there. And vice versa — as we sell interconnects for people, maybe that’s opportunities to get our interconnects into their systems and then maybe eventually sell some AI ASICs.

Maybe that’s not a story they want to tell, because maybe these companies that they make the data centers for don’t always buy their switches, for example. Maybe they’re still buying Broadcom switches, so maybe that’s not the true story. But I would love clarity — are these two distinct businesses, or can they actually benefit each other and cross-sell? And they never seem to talk about that. So if anyone from Marvell is listening, one, I’d love an answer. And two, if you have a good answer, then you should tell that part of your story.

Vik: Yeah, absolutely. I was listening to the Bank of America conference today, where Matt Murphy also spoke about their connectivity products. And then in the middle he was also like, yeah, we also do some ASIC stuff too. So I see what you mean by the disconnect there. But I guess their essential business is data movement, however you want to frame it. ASICs move data inside the chip — that could be one framing. We are a data movement company: within the chip, as in the ASIC business; between chips, as in the interconnect business; or between data centers, in their DSP business. They have a very strong DSP business, actually.

Austin: Mm-hmm. And I guess it is a bit of counter-positioning against Broadcom, who of course has an amazing data movement business but spends a lot of the earnings call talking about the ASIC XPU business. I think that’s also just what analysts want to ask a lot about. So we are in an interesting world, I think, both for Broadcom and for Marvell — as they have these two different businesses — to figure out what is the cohesive narrative, basically.

Vik: Yeah, that’s true. So that leads to the question of — all of the interconnects today, optical is used in scale-out. We know that. And there are still a lot of benefits to using copper or optics. It’s not one or the other yet. But as speeds go up, I think copper will run into its limitations. And so optics is nice, and they have their entire portfolio around it.

But I think what is more interesting to talk about is the scale-up scenario. Because when Matt Murphy drew that line and included the rack in the optics thing, it’s very interesting that now, internally, we may be seeing the birth of optics for scale-up. And recently there’s been a lot of debate online about whether CPO is really here. When is it going to be here? Can we support optical engines and packaging them at scale? Because I don’t think that we have done them at scale. Spectrum-X and Quantum-X, and the Tomahawks from Broadcom, have CPO, but they are just one application, and it’s just coming into production this year. So nobody really knows if you can produce CPO at scale, if there’s capacity to do so.

And there’s also the question of yield. The reason I’m saying yield is, you’re packaging in the TSMC SoIC process — you’re putting the optical engine on top of the electrical engine. I don’t know how that can be done at scale. They said something like, we have 99% yield in engineering samples, but that doesn’t mean you can scale up to millions of these things. So those are all unknowns at the moment.

And there’s also the question of testing optical engines. Especially when you have a two-sided die, it’s a problem, because you have to align the top of the wafer and the bottom of the wafer to test them simultaneously. You need the electrical side and the optical side to be aligned, and then you can test each one. And that alignment, from what I have read and spoken to people about, takes time. So that is a big unsolved problem — a problem that is currently being solved in terms of testers and things like that. How do you test CPO fast enough to make it a reality?

So CPO is definitely coming, because we have to go to optical down the line — there’s no way around it. But there are a lot of challenges. So a lot of the discussion online has been, why don’t we go to near-packaged optics for now? We won’t have to deal with the advanced packaging part of it, at least — we can just do the optical engines in silicon photonics and maybe put it into a socket. That’s the kind of discussion that’s out there right now, and it’s interesting to see how it’ll evolve. I don’t think I have all the answers at the moment, but it’s interesting.

Austin: Yeah, I totally agree with you. Ultimately, near-package optics takes a step in the right direction — gets that copper trace much shorter — but doesn’t jump all the way to CPO. Feels like a decent intermediate step, especially when you think about manufacturing. And of course, then there’s XPO, as we’ve already talked about, which I think will continue to extend pluggables. What else did you see — much on NPO or XPO, or was it all CPO that you saw at the show?

XPO, Ayar Labs’ Scale-Up Rack, and MicroLEDs

Vik: I wanna talk about both of them. Let me go with XPO first, because the CPO one is also nice. This is the first time I’ve seen an XPO module in person. There’s this whole video I took of me talking over it, and we’ll play it right after this. It is essentially a honking big connector — it’s as big as my hand. You know what, let’s just look at the video and then it’ll work out.

[Show floor video] Check out — this is the XPO module, which is the next generation of connector. Do you see how big this thing actually is? This is a honking big XPO module. Ridiculous. Look at this — this thing is liquid cooled and is the equivalent of eight OSFP plugs. It’s insane how big this is. I’ll show you all the cables after this for size comparison, and all the other connector types. Just for comparison, this is how big it is in my hand.

Amazing. So the whole thing with XPO is that it is effectively eight pluggable OSFP modules in one. It’s a massive, massive connector that’s liquid-cooled. It’s quite amazing. See the number of cables that came out of it. So this is nice — I like looking at it, and I genuinely think that it has a shot at being an alternative to CPO, if the ecosystem wants to stay pluggable. I don’t think it’s ruled out yet. So I’m glad I saw that part of the future of optical interconnects.

But then the other thing I saw was Ayar Labs’ scale-up CPO demonstration with the Wiwynn racks on the show floor. It was cool. In the picture of the rack, you can see all of these external laser modules that are sitting in the front panel, the faceplate, and then all of the optical fiber that’s coming in from the co-packaged module inside the rack. It’s not in production or anything, but concept-wise, as a demo, it’s really nice to see a fully scaled-up optical CPO rack and be like, wow, this is what maybe data centers will be filled with in about three to five years, some time frame.

And what was really cool about this was they had a video on the side that, for people who didn’t know what they’re looking at, explained the whole blowout image. So check this video out.

[Show floor video] So this is cool — watch this video and I’ll show you what comes up after this. This is Ayar Labs’ scale-up optics. On the other side of the rack is the actual hardware. So you can see all the external laser modules plugging into this thing, and those go into the rack. Yep. So that’s a fully optical scale-up rack.

So what I did after that was — once you see the insides of this rack, what is inside it and how all the optical engines are sitting next to the silicon and stuff, they have their actual rack. So I took a whole video of all the little details in the rack, and how they give you handles so you can pull them out. We should just play the video too, because there’s a reason I took all of this stuff, so we can put it in the podcast.

[Show floor video] Look at this — this is CPO rack-level scale-up. Each of these blue things are external laser modules. And I believe this entire handle exists so that you can pull out the rack and change it out, like it was in that video. But you can see internal to it is the optical cable going to the CPO switch. And all of these yellow cables are actually optical fiber. That would be the switch, I believe — the optical switch that hooks up all these XPUs in an all-to-all configuration.

Other than that, there was a microLED demonstration by MediaTek, which was interesting, but nothing new. I don’t know what I was trying to find out from them — what is their reach and how fast they can run it — but I didn’t manage to get too much info out of that. It definitely looks like it’s still nascent, at least in the MediaTek demonstration. So I need to go to the next optics conference — either ECOC in Spain, that’s coming up, or maybe OCP will have some stuff about microLED interconnects. I’d definitely like to see more of that stuff.

Austin: Interesting. I didn’t know MediaTek had a microLED offering.

Vik: Yeah, they’ve been working on it, actually. MicroLEDs can only run one to four Gbps per lane, so the whole idea is that you have multiple lanes and you transmit wide but slow. But this array — we counted it — had only like a hundred LEDs, something in that range. In reality, what you see Avicena demonstrate is more like four hundred LEDs, each running at maybe one to two Gbps, and then you get four hundred or eight hundred Gbps out of the whole thing. So that’s what I was hoping to see, but it wasn’t really a demo. The videos with the LED lights were just coming on and off. So I’m like, I guess you’re turning the lights on and off — and there was a microscope on there, and it’s turning on and off. Which is cool. I was like, yeah, I see some flashy lights, and those are blue microLEDs. Maybe they’ll carry data one day.

Austin: Sounds like a children’s science museum or something. Like, look, these blink.

Vik: I see blinky things every day. All of these racks were full of blinky things. I’m like a cat — you shine a laser at me, I’d be like, that’s optics, that’s CPO.

800 Volts Everywhere

Austin: That’s good. So, okay, we talked a lot about networking. What about power? Did you see anything? I remember, kind of right as we came into one of those conference buildings, wasn’t there a wall of power chips?

Vik: Yeah, power was cool, because everywhere on the show floor you see this stuff. There’s 800 volts this and 800 volts that. Everybody had 800 volts in their racks. It doesn’t matter who was making the rack — every rack provider had an 800 volt system there. So I’m like, wait, are we already there now? This is the thing with shows like Computex. You look at this stuff and you start to believe, yeah, this is what’s in the data centers today. It’s really not. It’s what’s in the future. And it’s nice to see, but it’s also important to keep in mind that not everything is running at volume today.

Apart from that — like you say, we walked and we saw this entire wall of chips, and it had these power converter chips — 800 volts to whatever, to twelve volts, or 800 volts to fifty volts. All these chips from every provider were there. You could see all of them. And it was cool, because you’re like, wait, this is your competitive analysis right here. If somebody gives me a lab setup, let’s start testing this right now. And let’s find the alpha from this wall. This wall has the alpha.

Austin: I wonder what they would do if you started plugging in and trying to test.

Vik: I’ll just get my oscilloscope and wheel in some power supplies and get to work.

Austin: Right, totally. I was surprised they had very different form factors and different shapes. I kind of thought — when Jensen always does the demo of, here’s everyone’s Hopper racks, it’s like rack, rack, rack, rack, and they almost all look the same, just different colors or something. But these boards were different shapes. Some were long rectangles, some were L-shaped or whatever. It was very different.

Vik: Yeah. I’m not sure how that slots into the actual application. Very interesting — it’s a good observation. I don’t know why they’re all so different, but these are big chips. And I went to the LiteOn power booth after that, and they had, again, the whole array of chips that they have. In the beginning they had this massive chip, and it basically converts from the medium voltage grid down to 800 volts. So this is the other side of 800 volts — the grid side of 800 volts. And I asked the guy, what is this made of? And he’s like, yeah, it’s silicon carbide. And so then I asked him, what do all these other chips do, from 800 volts down? He’s like, those are all silicon. I’m like, they’re not silicon carbide? No, no, silicon. And what about GaN? He’s like, nah, GaN is still new. It’s just silicon. I’m like, that’s cool.

Austin: Okay, so grid to 800 volts was silicon carbide, but then 800 volts all the way down was just silicon.

Vik: Yeah, that’s why I took a whole video of this thing. So definitely watch that too.

[Show floor video] LiteOn’s chip conversion portfolio is really cool. These are silicon carbide chips that use transformers and have single-stage conversion down to forty-eight volts. All of these other conversions from forty-eight volts — whether it is to twelve volts or six volts direct — are all silicon based. So the argument of whether it’s GaN or silicon carbide — it isn’t. All of this switch stuff they’re looking at here that converts voltages down is all silicon. So don’t discount silicon yet.

Austin: That’s so cool. There’s so much to learn from just talking to people on the show floor. I think that’s the best part — just asking what feels like dumb questions. There’s just so much that you can learn. It’s like asking ChatGPT that’s patient and will answer the dumb questions, except it’s the actual people that work for the companies and have the correct information, not something from 2024.

Vik: Yeah, I wish I could stay there and everybody could explain to me for the whole week, but that’s not to be the case. I was like a kid in the candy store. So I walked up to this demonstration, and there was this power whip, which is just this honking large cable. And I took a picture of me holding it, and you look at that thing and go, my god, what sort of a cable is this? Look at the size of that thing. No wonder people want to go to 800 volts, so you can carry less current and you can reduce the size of this honking massive cable. It’s ridiculous.

Austin: Yes, they’re literally like the size of my forearm or something.

Prefab Data Centers and a Chest Freezer Full of GPUs

Vik: That’s how big it is. So it’s crazy. And the other end of it was insane. You go to the Vertiv booth — by the way, before I even explain this, check out this video and I’ll tell you what it is.

[Show floor video] By far the Vertiv booth is insane. Inside that thing is the entire cooling solutions they have built up. By the way, those are not real, those are just pictures. I wish they were real though. But I’m gonna go around there and see if I can show you the cooling hall, I guess. There you go. Wow. Shiny colours.

Okay, so what that was, was basically what they call a prefabricated AI infrastructure block. What it is, is a container home — a modular home built for AI racks. So the way it works is, you wheel in all your racks into the data center. They could be 800 volt racks or whatever, right? But how do you hook this thing up? You have to give it power, you have to give it cooling, all of this stuff. So what Vertiv — and by the way, this is not just Vertiv. Delta has this, Schneider Electric, Eaton, all of them have the solution. But I just saw the Vertiv one in a little bit more detail. You just roll this thing in, and it is pre-fitted with all the cooling infrastructure and the power infrastructure, all this stuff. All you do is roll it in over the racks and hook it up, and it’s ready to go.

And the guy — I think this was at Delta — was telling me that this kind of reduces the time of deployment by half. It takes half the time to hook up power and cooling solutions. So these are prefabricated infrastructure solutions. It’s insane, right? You just can’t think about the chips. On one side you see all these chips that convert — you even see little chips that do the voltage regulator modules. And then on the other side, they’re wheeling in room-sized infrastructure just to power up these racks. It’s fascinating.

Austin: That is fascinating. It’s amazing — I hear lots of different companies, as a value prop, state that they’re trying to reduce the time to stand up a data center. You could call it time to first token, if you will, but in a different context — time to the very first token that’s ever generated. And of course it makes sense, right? If you’re Elon and you are building your xAI data center and you’ve bought billions of dollars of GPUs, they’re just sitting there depreciating every day. So obviously you want to turn them on as quick as possible. So it’s fascinating to think about, even from the physical infrastructure, power and water — how can you modularize that in such a way that it just makes it very quick to roll a thing in, plug everything in, off you go.

Vik: Yeah, that’s very interesting. And it’s just that these cooling solutions are not only at the data center scale. I saw one solution there — I’m not sure if you were there when we were looking at this; there were a bunch of people, but probably not — so I’ll tell you what it is. There’s this edge AI deployment. Let’s say you don’t want to deploy this whole data center thing, and you just wanna put eight or sixteen GPUs in your office server closet and provide some inferencing tokens to your employees. That kind of thing is going to become more and more popular just for overall cost optimization.

So they had this one company called Ketaflow Technologies, which is basically like a chest freezer in your garage. You open up the chest freezer, and what you see inside there is liquid. It’s just a transparent liquid — it looks like water, but it’s kind of like an oily thing. They let us touch it, even. So I stuck my finger in it, and it’s all oily. And they know that people are gonna do this, so they hand out tissues after. So we were all wiping our hands over there. But yeah, there’s this liquid — it wasn’t warm to the touch or anything — but inside that liquid is immersed an entire rack of GPUs and power and cables. It’s just dipped in there, and it’s doing liquid cooling. The whole thing is dipped.

And so we were trying to ask, how does the electronics still work? And he said it’s a non-conductive liquid. This is not like water, you know? So it’s a non-conductive liquid, and nothing is gonna happen to it. So you can put racks in here. He’s like, yeah, it’s running as we speak right now. I’m like, this is really fun.

Austin: Yeah, it is mind-boggling the first time you think about it. You’re like, wait a minute — I just always think liquid, short circuit, conductive. And then you’re like, wait, there’s non-conductive liquids, huh? Fascinating. You could just drop the whole thing in and it works. And then of course it dissipates heat, because the liquid helps carry that heat away. Amazing.

Intel’s Quiet Foundry Flex

Austin: So let’s see — we talked networking, we talked power. Let’s talk Intel a little bit. I went to Intel’s keynote and had a front row seat for Lip-Bu Tan. And the audience loved him. He started by speaking in Mandarin, and I thought that was really cool — talking to the locals, we were obviously in Asia. You can watch the keynote online. Really quick, since we’re kind of getting close to the end of time, one of the things that really stood out to me —

One of the big introductions was the Intel Xeon 6 Plus with E-cores, aka Clearwater Forest. So, high level: 288 E-cores, 12-channel DDR5, 8,000 megatransfers, a big L3 cache — the kind of things that you expect Intel products to be shipping. This is very much the space of going after AMD and Turin Dense, trying to catch up there. So good specs.

But I just couldn’t stop thinking about what a positive signal this is for Intel Foundry. As they went through the chip — some of the specs of how it was built, which is really cool — it just shows that Intel Foundry is putting in good reps, and these are the types of technologies that are being perfected on their internal customer, if you will. Although I know that Intel Foundry doesn’t position them as an internal customer anymore. They very much wanna say, we treat Intel Products as any other customer — we’re trying to become a real foundry and not give them preferential treatment. So let’s just call it their best customer, their biggest customer.

So Intel Products came and said, hey, we want to build this data center CPU. And there’s something like 17 chiplets. It’s two I/O tiles, or dies, that are built using Intel 7 technology. Three active base tiles on Intel 3 — this is for cache, mesh, fabric, stuff like that. And then there’s 12 compute tiles on Intel 18A, and these are the Darkmont E-cores.

And so then the cool thing is — and there’s a nice picture of it, we can try to include that — the active base tiles on Intel 3 are connected to the I/O tiles using EMIB. Which, by the way, I think we’re going to try to talk about EMIB in a future podcast — so here’s a teaser for listeners. I wrote about it recently. So obviously Intel’s got these chips that are built on different process technologies, all Intel Foundry. They’re connected with EMIB. And then on top of it, they’re using Foveros Direct 3D to stack the compute tiles on top of those active base tiles.

So this is hybrid bonding, which everyone likes to talk about — bumpless copper-to-copper bonding — but it’s also silicon on silicon, logic on logic. Active silicon stacked on top of active silicon. And that would be different than active silicon stacked on a passive silicon interposer, for example, or even cache memories stacked on active silicon. This is active silicon on active silicon, which has its own thermal things that you have to think through, and power delivery.

And so then, of course, speaking of power delivery — Intel 18A is the first generation for Intel Foundry of using backside power delivery. They brand it PowerVia. And then from a transistor perspective, this is using gate-all-around transistors, or RibbonFET, I believe, is what they call it.

So as we’re going through these slides — and it’s really pitching things from an Intel product perspective — all I could think the whole time about was Intel Foundry, and how there’s a lot of really interesting technology going on here. And I know everyone just likes to be like, what’s 18A’s yield? It’s bad, it’s good, whatever. But I’m like, no, man, it’s so much more than that. There’s even an economic story here about being able to build a chip. And of course, this is the benefit of disaggregated design, or chiplets, different than monolithic design — you can use the right process node that has the right economics. For example, I think they’re even just reusing the I/O tiles from Granite Rapids. I don’t think those are even new designs. And SRAM doesn’t scale that great, so just leave it on Intel 3. That’s fine. Only use Intel 18A for compute. And then obviously, from a yield perspective, you’ve got little dies instead of a big monolithic die.

Yet it also goes to show how good Intel Foundry must be at advanced packaging, to be able to take all these dies and stitch them together — not only with EMIB, which is not new, they’ve been doing EMIB for a while, but especially with this Foveros 3D logic-on-logic stacking. And it wasn’t really even hammered home, because that wasn’t the purpose of the talk. But I guess I’m doing Intel a favor here, as sort of a foundry person with foundry interests. I thought, wow, this is actually a really compelling Intel Foundry story.

So that was my takeaway from the whole Computex — which was not the story that Intel was probably even trying to tell, but that was my story. Just, dude, this is sweet, sweet technology that they’re building. And I’m sure that their customers — Intel Foundry customers — should be able to see that and think, yeah, this is the type of technology we want to use. And by the way, if it’s on 14A eventually, that’ll be second generation RibbonFET, second generation backside power. So Intel Foundry is learning all of this on behalf of their biggest customer, Intel Products, but they’re also improving on it too.

Vik: Yeah. So what I’m hearing you say is that it’s not so much a whole CPU flex or anything. It’s just, look at my advanced packaging that I’m capable of doing. It’s a packaging flex, really — when you can package up all this stuff nicely and do it at scale. It’s good to see that EMIB is coming up the way it is. There has been news that Google is also engaging with Intel Foundry for their TPUs. I don’t exactly know in what context — whether they’re actually gonna use 18A, which would be really, really cool, or they’re just going to use the EMIB packaging part of it, which is also amazing for their TPU products.

But it’s so good that there is a product that is not CoWoS from TSMC. Because it’s so supply constrained. And I’m not just talking about this from a business perspective — yay, we have Intel winning, we’ve had enough of TSMC. It’s not that. It’s just more that I would like to see technology accelerate, only for the reason that I don’t know what other cool applications are there for AI. And I would hate to see it constrained by the inability to package something, or by the inability of lasers, or something benign like that. I’m like, it’s a simple solution, it’s not a technological problem — why don’t you just make more, is the thing I want to say. But obviously reality is more complicated than that. You just can’t make more. Everything takes time, and capacity build-outs are a real thing. So I’m happy in that sense to see that there’s a second packaging option, so we can just make more chips in some regard.

Austin: Totally, totally. And, you know, to your point, TSMC is an awesome company, and it was so cool to be in Taiwan. I wish I would have been able to go to TSMC. I would love to meet the folks from TSMC and take a tour someday. But to your point, TSMC is doing everything they can within reason to increase their capacity. But ultimately there is a limitation on just the amount of chips that can be built, the amount of interposers that can be built, the amount of packaging that can happen. And it’s not to any fault of TSMC, because it is very, very expensive, and it’s a huge investment to spin up fabs. And you have to be very confident that the demand will still be there by the time you ramp these things up in two years. And so it is not fiscally responsible to just build tons and tons of fabs because Jensen wants it today, or Sam Altman wants it today, or Elon wants it today, right?

So they are doing everything correct and by the book. But zooming out, to your point — if there’s really only one big supplier, then the whole industry is limited, which means there are innovations that can’t come to bear, or can’t come to bear as quickly. And so just from an industry perspective, the more packaging capacity — because of course even OSATs will be able to do EMIB if they want — the more packaging that Intel Foundry can show off, the more wafers that Intel Foundry can build, just the better we will be as a society. Because we’ll have more capacity, and we can bring innovations to light quicker, and potentially cheaper, if you have competition and you can kind of keep prices in check, and so on. So I’ll stop my spiel there. We could talk a whole episode on just that, but I think it’s net positive for everyone to see Intel Foundry having success.

Vik: Agreed.

Austin: Well, let’s call it there. Everyone, I hope you liked this episode, our Computex breakdown. Enjoy the videos, enjoy the pictures. Thanks to everyone who watches this on YouTube — I know I call you out, but I think our last video was our best one yet as far as engagement, so thank you for all the comments on there. Please share it with a friend. Follow us on Spotify, or wherever you like to listen. Check us out on X, whatever, send us comments — we read them all. So thank you, everyone, and we’ll see you next time.

Discussion about this video

vjj
