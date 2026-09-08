---
source: https://daily.semidoped.com/p/a-masterclass-on-ic-lithography
title: 🎙️A Masterclass on IC Lithography - Semi Doped
kind: transcript
---

🎙️A Masterclass on IC Lithography

You can spend one hour and catch up on the entire arc of semi lithography.
Things we cover:
- Economics of modern lithography
- what is takes to build a leading-edge fab
- how we evolved from DUV to EUV
- fun stories from history along the way
- where we are going with xLight and Substrate
Check it out!

This podcast is lightly edited for clarity.

The Cost Problem

Austin: Hello everyone, and welcome to another Semi Doped podcast. I’m Austin Lyons with Chipstrat, and with me is Vik Sekar from Vik’s Newsletter. Hey Vik, what’s going on, man?

Vik: Yeah, not that much. Other than everybody’s panicked about the 13F from that Situational Awareness hedge fund, and there was a sell-off in optics and everybody freaked out. I’m like, what’s going on? First of all, I still don’t really know what a 13F is. I guess a hedge fund has to report some holdings that they hold, and what they sell and what they bought. Something like that.

Leopold Aschenbrenner — is that how you pronounce his name? Sorry if I got that wrong, I have no idea. It’s too many syllables. I guess he made a lot of money and converted a few million into a billion or something. And then everybody is following him for the latest stock tips. And when everybody looks at his 13F, they panic and there’s this whole sell-off. Apparently he shorted optics and shorted AMD, Intel, and sold it. I don’t know.

So everything is down in the semi market because of some hedge fund thingy. This is what’s happening. It’s funny.

Austin: I mean, so if I’m him, I’d wake up and look and go, wow, I can buy a few puts, because on this 13F — I don’t think it talks about the size of his puts or anything. So he can just buy a few puts at some point, drive the price down. Could he use that to then buy at that (depressed) price? That’s market manipulation, but in their hand, people are trading on public data and on vibes. He could throw people off his trail, right? Just buy a tiny amount of puts in everything and you wouldn’t know what he’s investing in.

Vik: Yeah, I don’t know. I don’t think Leopold listens to this podcast — but if you do, just let us know. Maybe you can come explain to us what a 13F is, because I don’t know about you, man, I have no idea what all this stuff is. So I’m happy to learn from the best.

Austin: Yes, Leopold, you’re welcome anytime. All right, so today we’re going to talk lithography. I thought it would be really interesting to talk about the economic challenges of lithography, modern EUV lithography especially, because ultimately incentives drive outcomes, and there are challenges with the increasing costs of lithography, the increasing costs of fabs.

And you start to see TSMC can afford the next process node, and Intel and Samsung are trying to stay in the race, or be in the race. There aren’t that many other competitors. And from afar, if you’re a semi-tourist, as they like to say on X, you might say, hey, TSMC is crushing it, why aren’t more people in this game? And of course, as you start to unpack it, you realize that costs are a barrier to entry.

And so you start pulling on the thread and you ask, well, what costs? And one of those major contributors to the capex needed to participate is modern EUV. So what do you think — should we talk EUV?

Vik: Yeah, that’s a great topic for today. I think it ties in tangentially to what’s happening to the market today, and why people think we are not on an unconstrained trajectory upwards. And this basically stems from the recent Gavin Baker interview that I put in one of our Semi Doped Daily updates on Substack. So if anybody is not subscribed to the Substack, I recommend it. It’s free. You can go get subscribed — semidope.com.

The idea that Gavin floated in that interview was: we are not in a bubble, because TSMC is basically holding back the entire industry by not creating enough chips for everybody, by controlling their level of capex spend on tools that require DUV and EUV. And most famously, I think TSMC is not pro-EUV. They think the tools are too expensive, and they want to stay on DUV with multi-patterning as far as they can manage to. And we’ll talk about what DUV with multi-patterning means in this episode.

This is where we are right now. Tools cost a lot. I think an EUV machine costs something to the tune of $400 million. And that’s just one machine. You need to run many of them to produce the chips at the scale we need, and that scale is continuously increasing. So it really comes down to: is EUV the only way forward? And then there’s Hyper NA EUV, which is extreme — I don’t even know if those are in production yet. I don’t think so. But those are going to cost close to a billion dollars. That’s insane.

Austin: Yes, totally. So we’ll unpack all this for everyone — what’s DUV, what’s EUV, why does it cost so much? That’s what this episode’s all about. A lithography masterclass, hopefully to set the stage for future conversations around lithography and some of the startups that are out there.

And actually, I just saw ASML shared a roadmap. I think imec had a conference — it’s going on right now, the ITF World conference — and ASML showed some of their roadmap and how they think they’re going to be able to bring the cost per exposure down. It would be nice to unpack this, but before we get to all those nitty-gritty details, we want to educate our listeners on some of the fundamentals. So let me throw out some numbers.

Inside the Clean Room

Vik: Hold on, I want to set one thing for Austin, before Austin. Most of this stuff, Austin is actually the expert, because he actually spent time working on this kind of lithography stuff in a clean room, which is something I can’t say I’ve done. I’ve measured wafers and measured transistors, that kind of stuff. I’ve handled completed silicon wafers, but I’ve never actually done lithography myself, and you have. So this is a cool thing. You can tell us a little bit more, rather than just what you can read on the internet. It’s interesting what it looks like inside a clean room. I’m excited to hear.

Austin: Yes, yes. Well, thank you for mentioning that. So when I was in grad school, I worked at the University of Illinois Urbana-Champaign, doing research as a research assistant, making graphene-based transistors. I was in a lab with Professor Eric Pop. He’s at Stanford now, and he studies 2D materials. People on our team were studying carbon nanotubes, and then I got to work in graphene.

So yes, I got to be in a clean room with silicon wafers — etching, depositing, doing lithography. And in fact, I even got to do E-beam lithography, because we were trying to make very precise, one-off little nano-electronic systems. It didn’t matter that the throughput of E-beam is really low. We’re not going to talk about E-beam lithography much here, but it’s a cool thing that I got to experience.

When I first started, we were mechanically exfoliating graphene, which means we were taking tape — we get graphite, layers of pencil lead essentially, and then we take literally clear tape and stick it on top of the graphite and pull it off, and then take it under a microscope and look, and you can figure out how many layers of graphene you have there. So I’d just scan around, doing some of this stuff in a bunny suit, and then going back into the lab and moving this thing around, just thinking, what am I doing with my life? I’m trying to find single-layer graphene. That’s what I’m doing.

But of course, once you find single-layer graphene, then we’d pattern the transistors right there on it, and take measurements and publish it, because it was a hard thing to do. So we kind of had an advantage that we knew how to do it. I won’t talk too much more. We eventually did chemical vapor deposition to create graphene using copper foil essentially, and then we could grow graphene — it wasn’t as pristine and pure, but it was more scalable. Anyway, good memories. I spent a lot of time there.

Vik: Amazing stuff. I bet it was a great experience. At the time, it’s probably frustrating as all hell, as all research is, but then looking back at it, it’s like, I don’t mind doing that again now. At least going into a clean room and pottering around would be nice.

Austin: Totally, man. It was challenging in that you couldn’t just do the research — you had to do a lot of exploration to figure out how to even make the thing before you could actually measure it and do the research. So yes, it was frustrating at the time, because you’d spend a whole day and then get to the end and be like, that didn’t work. But looking back now, it’s like, how fun was that? How much intellectual freedom there was. Your research professor says, hey, go make this thing, and you’re like, well, I guess I’ve got to read and experiment and try to figure out how to make it, and then measure it, and then see if our hypothesis was correct.

Vik: Yes, yes. Nice. Okay, now we’re good. We hit carbon nanotubes already — research that’s never made it out of the lab. You spent time doing that. Awesome. Now let’s talk about stuff we can actually make.

Rock’s Law and the Price of a Fab

Austin: Okay, so let’s talk about — have you heard of Rock’s Law, by the way?

Vik: I have not.

Austin: Okay, so this is a quote-unquote law, just like Moore’s Law. It’s really an observation, named after Arthur Rock. He was an early investor in Intel, maybe one of the founders of the venture capital industry, if you will. But the observation was that the cost of a semiconductor fab doubles every four years.

So it gets more and more expensive. Now this is interesting — this is related to Moore’s Law, where Moore’s Law said that the number of transistors in an integrated circuit doubles every two years. And so if the cost of a fab doubles every four years, that’s slower than the number of transistors doubling every two years. What that means is that Moore’s Law is really an economic statement that says: for roughly the same price, we can get more transistors per die area, per chip, per unit area over time. And that’s really what drove the industry — that economic realization that for the same dollars, you could get more compute over time.

We are getting to the point where the cost of fabs is getting so high that we’ve seen, decades ago really, Moore’s Law — the number of transistors doubling — shrinking for physical reasons, but also from an economic perspective, the cost of transistors flatlining and potentially even the cost per transistor coming up. And again, the question is what’s driving that fundamental change to some of these important economic scaling laws that we’ve seen for decades. And lithography is a big contributor. Like you said, low NA EUV tools used to cost around $250 million, now high NA’s coming out around $400 million, give or take. These numbers change over time, and it probably depends per customer. You can back some of this stuff out of ASML’s reports, because they don’t sell many of these per year.

But anyway, yes, the rumored Hyper NA, which would be a future tool, could cost anywhere from $600 to $800 million potentially — if the Strait of Hormuz stays closed, maybe a billion dollars, because that’s driving everything up. So which means lithography, all of these tools — like you said, we’ll get into it — you might need 15 tools to open up a new fab. I think I’d seen some CNBC coverage where it said that Intel’s 18A fab in Arizona, Fab 52, needed 15 EUV machines. So imagine that: half a billion dollars a pop, and you need 15 of them. That is no joke. And that’s why a brand-new fab costs on the order of $20, $30 billion.

So I just wanted to quickly paint the picture of the enormous capex cost to just build one new fab to try to stay in this race. And of course that ultimately means the cost per wafer will have to go up too, because you can only do so many wafer starts per month — say tens of thousands of wafer starts per month, or a hundred thousand — and you need to amortize the cost of all those tools over that fixed number of wafers.

Vik: Okay, cool. So let me back up a little bit and quickly frame it in a way that I usually process things. One of the biggest problems of modern lithography is cost. And that primarily stems from having to make smaller and smaller transistors. We have gone from deep ultraviolet, which is what we’ll refer to as DUV, to eventually extreme ultraviolet, which is what EUV stands for. Then within EUV, we have several levels of numerical aperture. I think we should define what that is next, so that we have all these basic terms in place.

So we have low numerical aperture, or low NA EUV, and high NA EUV, and then Hyper NA EUV. The higher you go, from low to high to hyper, the smaller the transistors you can make. So basically, the higher the numerical aperture, the smaller the transistors, the smaller the feature sizes you can make.

Now, regardless of whether you choose a deep ultraviolet or an extreme ultraviolet machine, you’re going to need at least 10 or 20 of them in a fab. And if each of them costs, I don’t know, half a billion dollars, and you want to put in 10 of them, you’re spending $5 billion on just these EUV machines. Not only that, you have to put in a whole lot of other infrastructure, like cooling. The clean rooms are difficult, because you have to have HVAC systems that pull all of the dust particles out of the air. Based on how many dust particles you can find per unit volume, these clean rooms have different classifications — you’ve got class 1, class 10, class 100. I think the higher the number, the more particles per cubic volume of air.

So all of this stuff takes an enormous amount of money and time to build. Actually, here’s another point. If you look at TSMC’s construction of their fabs, critical machines are suspended on pistons. Entire factory floors are suspended on pistons so that it’s immune to earthquakes and stuff. So it is very expensive to build a fab.

And it takes years. It could take three to five years. So this is why we can’t simply add chip capacity willy-nilly.

Austin: Totally, totally. And not only that — if you haven’t seen a fab, I’d encourage people to figure out how to get on a fab tour if they can somehow. I know it’s very difficult. But Vik wants to go. I actually had the good fortune recently of getting to go to Intel’s Fab 52 and tour it. So not only do you not want the machines to move around even a tiny bit from earthquakes, but even from passing traffic and stuff.

Vik: I’ve never been in one.

Austin: Of course, we’re making transistors on the atomic scale, nanometer scale, and so you don’t want any sort of mechanical wiggling and movement. Also, these EUV machines have big power sources, and the light source — a lot of that actually goes in the sub-fab floor. So there’s a floor beneath the main floor where the tool sits, and they have all this equipment underneath it. And then of course there’s a floor above it, and you’ve got to flow all that air through.

So I also wanted to illustrate that it’s not just like data centers, where you find some real estate, slap a building up, throw some racks in and you’re good. Even from a construction and HVAC perspective, building a fab is no joke.

Vik: And it goes beyond that, because if you look at Intel fabs and the way they’ve built them in the past, they had this “copy exactly” method, which means they copy exactly. This is not something they mess around with. They use similar plumbing. I’ve heard that they even use the same brand of paint, because they do not want anything to go wrong. If small things happen and change the way a fab functions, you can’t get the yield up. And if you can’t get the yield up after spending $20 billion, you can’t make enough wafers, which means you can’t sell them and make a profit.

So Intel decided to copy exactly. And that actually slowed a lot of stuff down for them — that’s a different story. But really, that’s how difficult it is to build a fab. I mean, that’s insane.

DUV and the Art of Multi-Patterning

Austin: Totally. All right, going back — you mentioned DUV and EUV, so let’s tell listeners a little bit. Back in the DUV days, the light source that was used had a wavelength that eventually made its way to 193 nanometers.

And zooming out even further: lithography, at the end of the day, for those who don’t know — I think everyone probably does these days, because ASML is an awesome company and everyone wants to invest, or has invested, and so at a high level understands what lithography is. But we’re talking about ultimately being able to expose light to, in quotes, “draw” the shape of transistors, or the shape of areas that you want to etch away — you leave parts of the transistor but etch away other parts of the surface of the chip.

And so ultimately, to make transistors smaller and smaller, you need to make the wavelength of light smaller and smaller. But there’s also something we can get into, which is the numerical aperture — the mirrors you talked about, changing the numerical aperture. But just focusing on making the wavelength of light smaller: the canonical example here is, if you’re writing with a Sharpie, you’re going to draw fat lines. And if you can write with a fine-tip marker, a fine-tip pen, you can make a lot thinner lines, and you could draw smaller, precision features. So that’s what the industry was trying to go to, from DUV, deep ultraviolet lithography, to EUV, which uses 13.5 nanometer light. So ultimately you’re going an order of magnitude smaller, from the fat marker down to the fine-tip pen.

Vik: Yeah. So this whole relationship you mentioned, where you want a smaller wavelength of light but a higher numerical aperture — this is governed by what is known as the Rayleigh criterion, which means that the smallest dimension you can make on a wafer is literally proportional to the wavelength, but inversely proportional to the numerical aperture.

There is also a constant factor here that’s often called K1, which we won’t get into, but think of it as another knob you can use, by designing the masks that selectively allow light or don’t allow light in regions. They do all kinds of tricks on those masks to improve this proportionality factor K1. We won’t get into it, but these are the factors. So there’s a bunch of tricks, then there’s the wavelength, and then there’s the numerical aperture.

So the smaller the wavelength you go, the better. And to Austin’s point, deep ultraviolet lithography most famously ended at what is called argon fluoride lithography — is that right? — at 193 nanometers. And then there was a quantum leap down to 13.5 nanometers with EUV, with extreme ultraviolet. So that’s a big change. That’s more than a 10X change. And going down another 10X hasn’t happened yet, but we will get to how that can happen at the end of this episode. But yes, keep going. Let’s go.

Austin: Okay, let’s talk about DUV for a second. Do you want to explain where the 193 nanometer light comes from, with argon fluoride?

Vik: There was a whole evolution to that as well. It’s not like we just landed there right when we started lithography. In the 1980s, it was mostly what was called i-line lithography, which had a wavelength of 365 nanometers. Then over the years, people realized, wait, we’ve got to make this better. And then they came up with krypton fluoride lithography, KrF lithography, that went to 248 nanometers. So just by changing the kind of light source you’re shining through, and the wavelength of the light source, you could get better features.

So going through the 90s, you could have 248 nanometers. That evolved to argon fluoride lithography, where they went to 193 nanometers. And that was pretty cool. But then that lasted all the way through the 2000s, let’s say. They kind of ran out of light sources. They did try some other light sources along the way, but they didn’t really work out, for various reasons. And then they were kind of stuck with argon fluoride for a while.

But then they thought about it: how do we improve numerical aperture? Somehow we have to improve it. And the answer was extreme, actually. It’s amazing. If you come to think of the history of lithography, it’s insane. Some smart guy came up with the idea and said, how about we put water on the wafer? Let’s just put water on it. You want to put water? So yeah, that’s literally what they did. They put extremely pure water on top of the wafer, and then put the light through the water onto the wafer. And that came to be called immersion lithography. So that actually helped scale transistors further, just by putting water on the wafer. It’s insane, right?

The history of lithography is amazing. I wanted to tell you the way it all started — I don’t know if you know this. The way it all started, in the early days — I forget the name of this guy, look out on Semi Doped, we’ll have a poll post on this thing — the main idea of making masks and making transistors smaller came about because this guy, I think he was working for TI, was looking at a microscope, and he was like, wait a minute, if I can flip the microscope over and shine light from the other side, it gets smaller, right? Everybody knows, you look the wrong way at these things, stuff gets smaller. So he’s like, this is it, I’m going to turn the microscope upside down and shine light through the wrong end and everything gets smaller. And that’s how all of lithography came about — the optics in lithography came about — because this one guy had the idea to turn the microscope upside down.

So that’s how it all started. And then we’ve been continuously going down the path of these various laser materials, down to putting immersion lithography with water, and ultimately coming down to extreme ultraviolet lithography, which is an engineering feat that is an achievement for humankind. That’s how big it is. We’ll talk about it too.

Austin: Yes, yes. So, Vik, you make some interesting points here — optical lithography, it’s all about light sources and about the optics, about the mirrors, about how you bend the light. When you talk about the guy having the insight of, when I look at a microscope, it makes small things seem bigger, so if I flip that lens, I can make big things seem smaller — what an amazing way to take a big mask and make it smaller to be patterned.

And then ultimately, when you’re talking about moving through various materials and unlocking smaller wavelengths, we’re talking about lasers. These are light sources to shine through the optics that we’ve been talking about. And ultimately, the industry was just playing with what different materials can laser at shorter and shorter wavelengths.

And this leads me to — we got to argon fluoride, 193 nanometer, and the industry sort of stuck for a while, waiting to figure out the next way of unlocking even shorter wavelengths, ultimately EUV as we know it today, which we’ll get into. But in the meantime, the industry came up with this nice trick called multi-patterning. And I thought I’d explain it really quickly, because there are also economic trade-offs to multi-patterning.

So multi-patterning is ultimately about — the question is, how do you draw features smaller than a single wavelength? Let’s come up with an analogy. Let’s say you’re drawing the lines on a football field, an American football field — the end zone, zero yard line, 10 yard line, 20 yard line, and so on. And maybe you have a machine that is, I don’t know, really fat, and it can only draw a line every 10 yards. The 10 yard line, the 20.

Well, then maybe the coach comes to you and says, hey, we also need markers at the 5 yard line and the 15 yard line and the 25 yard line. And at first you’re like, well, wait, my machine can only print them every 10 yards, how am I going to possibly do that? And then some clever person comes up and says, oh, well, just draw 10, 20, 30, 40, and then go back to the start and scooch it over five yards and draw 5, 15, 25, 35.

It takes twice as many steps, but instead of having to get a new machine that can now print every five yards — zero, five, 10, 15, 20 — you just draw them every 10 yards, and then you offset by five yards and draw 5, 15, 25. So when you zoom out and you’re done, you’re like, wait a minute, now I’ve drawn lines every five yards, even though I didn’t have to get a new machine.

And that’s an analogy for what’s going on in multi-patterning, which is drawing features in step one that are only spaced at the distance you can comfortably make, and then coming back in with another step and drawing a second set of features and just offsetting it. The amazing thing is, with a trick like multi-patterning, you can unlock shorter dimensions between the drawn features. But of course, the economic cost to this is it takes twice as many steps — it decreases your throughput by half.

Vik: I love the analogy, by the way. That’s a super cool way to understand it. So what you’re saying is basically you can do a coarse etch, scooch it over, do a coarse etch again, and what you’re left with is a fine etch. Because now, by scooching over somewhere in between the last two etches, you can get a finer spot. And if I remember right, this terminology is called litho-etch, litho-etch. So you’ll see this as LELE, right? Is this the same thing I’m talking about?

Austin: Yes, exactly. You nailed it.

Vik: Okay, cool, cool. Now, I think people have taken this to more than two levels of litho-etch, right? They’ve gone to triple patterning and even quad patterning, which is all cool and all, because now you’re stuck with two problems. One, it becomes increasingly difficult to even align masks between the yard lines. When you had to align the mask at the 15 yard line, it was okay, whatever, it was between 10 and 20. But now you want to align it at 12, 14, 16, 18, and you’re like, okay, that’s the problem.

The second problem is you’re going to run through four different quad-patterning steps, and each one takes the same time, so it kind of scales linearly. Now it takes four times as much time to make that one lithography step. And I’m not sure how many levels this can be applied to with quad patterning, but making a transistor isn’t like one etching step, or one lithography step — there are many of them. And if you have to quad-pattern on multiple steps, it adds up a whole lot of time and the throughput decreases, which means the cost per transistor goes up, or you don’t get enough amortization of the original $20 billion investment. And now we’re at a crossroads here.

What “Two Nanometers” Really Means

Austin: Yes, yes. And case in point — I know SMIC, which is the fab in China, they’re not allowed to get EUV. And so they were able to take DUV and use tricks like quad patterning to get to seven-nanometer-class and then five-nanometer-class transistors.

Which I wanted to point out, by the way, because it’s related to lithography: nowadays, when we’re talking about making transistors, it’s no longer just two-dimensional transistors, it’s really three-dimensional transistors — FinFETs, that have these fins. We should find some pictures, and people, go Google it — and RibbonFETs. So now you’ve got these three-dimensional shapes. And making a transistor actually takes on the order of 60 or 70 or 80 steps, because you have to pattern and etch and deposit material over and over and over to build up this 3D-shaped transistor.

So there’s also kind of a marketing thing — the semiconductor tourists, for lack of a better word, which just means you’re new to semis. It’s no shade. I was a semi-tourist at one point.

Vik: Welcome — everybody is welcome into Semi-Land. Love you. Very inclusive.

Austin: That’s what this podcast exists for. Yeah, exactly. When a fab says we make two-nanometer transistors, or 1.8-nanometer transistors, it’s the smallest dimension. This critical dimension — like we talked about before, the distance between any two really close lines — is not two nanometers. It used to be, back when they were 90 nanometers and 180 nanometers and 45 nanometers, that was a lot closer. But it became a marketing term. So actually, something that’s called two nanometers, the smallest dimension may still be on the order of 30 nanometers.

Vik: Yeah, yeah. So it’s not actually two, but that’s what we call it now, because it’s somehow the equivalent of two.

Austin: Yeah, correct, correct. It’s the equivalent, when you think about transistor density and whatnot. But I will say it’s important, because naturally, when we say 13.5 nanometer EUV wavelength, someone might go, well, that’s still way too big to draw two-nanometer lines. But it’s not, exactly.

So you might think, if we went from big fat marker DUV to fine-tip Sharpie EUV, we must not have to multi-pattern anymore, right? And actually, your intuition is correct — from a resolution perspective, we don’t have to. But from a yield perspective, the industry can still need to rely on some multi-patterning. There’s a really nice graphic from Fred Chen’s Substack — he wrote a nice article on it, we’ll link to it in the show notes.

Ultimately, we are getting so small that when you’re shining very short wavelength light at a certain dose, there’s only so many photons that are hitting there, and you can only control them so precisely. You’ve got resist chemistry going on, and there might be some — ideally there’s not — but there might be some impurities or even dopants in the way. And so you end up getting this stochastic nature. When you draw with the Sharpie, you don’t actually get a very fine line. If you zoom in, there’s some little dots around the edges and stuff. Think of it maybe like spraying with a spray paint can or something. It’s not a perfect line.

Vik: I’m looking at the picture, and I was thinking of spray paint, exactly. You always nail these analogies, and I was like, I’m going to nail this spray-paint analogy.

Austin: Yes. So ultimately, what they do is, you might draw with the spray paint twice to get a better-defined line, especially as you’re starting to go into three dimensions. So I just wanted to throw that in there — now we’ve jumped up to these $300 million, $400 million EUV tools, but the throughput isn’t immediately solved, because there’s still some multi-patterning that may have to happen. And there are other things about the power of the light source and the dose, but we won’t get into those now, because we’re really starting to get into the weeds.

But okay, what do you say we jump in? Should we talk about high NA next? Or do you have anything else to add here that’s useful at a high level?

Making 13.5nm Light

Vik: I think we should conclude — before we talk about NA, we should talk about how we can generate light at 13.5 nanometers in EUV. We mentioned that these were laser light sources based on argon fluoride lasers. But it’s quite different when it comes down to 13.5 nanometer EUV. And that is where the hardest innovation actually was, holding back the industry from going to this for a very long time.

Fundamentally — in a simple way, it’s far more complex than I’m explaining it — but in the simplest way, it is basically tin droplets that fall through a chamber. You hit it with laser light, and it gets activated, and then you hit it again with the laser light. Remember, you have to hit a falling tin droplet that’s about 50 micron in size, twice, as it falls through this chamber. The second time, it gives you an explosion of 13.5 nanometer light. That keeps happening, precisely.

ASML has an awesome video on their website where you can see these tin droplets falling. It’s an animation, you can’t really see this thing — but these droplets are falling and these laser sources are continuously hitting the droplets, and you see these explosions of EUV light. That then goes through mirrors — it goes through like 13 different mirrors — because it has to be focused ultimately onto the wafer. And then it lands on the wafer, where it hits a mask, and then it selectively exposes or doesn’t expose stuff.

One of the big problems is that you went through all this trouble to get extreme ultraviolet light by shooting lasers, but then you reflected it through so many mirrors, and at each reflection you lose some power. Less than a single-digit percentage of the actual generated EUV power actually gets to the wafer. It’s a big loss because of these mirrors. There’s literally no way around it, or so we think. But that’s what I wanted to talk about, because now that we’ve finished talking about how lasers and light sources work, numerical aperture is a good transition to get into right now.

Austin: Yes, this is good. I almost skipped over EUV entirely, at least low-NA EUV. So it’s a good introduction. We were stuck at DUV, we tried multi-patterning, and in the meantime the industry was trying to work on EUV. And as Vik talked about, ultimately we’re trying to find a light source that has a much shorter wavelength. Work had been done that showed with tin, you could basically induce a plasma — that’s why you hit it twice, ultimately — and that plasma would generate 13.5 nanometer wavelength light.

But there were a lot of engineering challenges and optics challenges around: great, yes, when we’re under vacuum we can generate a plasma and it will emit this really short wavelength light, but how do we ultimately harvest all that light? How do we reflect it back, and aim it with mirrors? Ultimately you need to gather this light, because it’s just going to shoot in any direction, presumably, from the tin droplets, and you need to gather it all. And then you need to get it to where it needs to be, to where the mask is ultimately. And while you’re doing that, you’re trying to focus all the light. And like Vik said, there are a lot of losses every time light hits a mirror — it’s not going to all bounce perfectly, exactly in the direction you want, there’s going to be some scattering and some loss.

So ultimately you end up losing so much light in the process that you don’t have enough to expose the photoresist. And so the question the industry was working on for a long time is not only how do we make all this work repeatedly, but also how do we increase the light source, so that ultimately, by the time we harvest all this light and get it exactly where we need it, focused all the way down, we still have enough to actually expose the photoresist and draw the transistor.

So that’s why we were stuck at DUV for a while — because this is an amazing engineering feat. Read the book Focus, by Martin something, I don’t remember his last name, but it’s about ASML. What’s really interesting is it talks about the entire supply chain and all the co-innovation needed — for example, famously, from Zeiss with their mirrors. So it’s no joke to even build the laser-produced plasma light source, but then you have all the optics.

And of course there’s something called a scanner. We won’t talk about it a ton, but ultimately, when you’re patterning the mask, you don’t want to just pattern one — you don’t pattern one die or one chip. Like we talked about before, it’s like a checkerboard pattern on a big dinner plate. You need to draw these transistors for every checkerboard square. So you need mechatronics that move everything around so you can repeatedly print all of this. There’s a ton of engineering to make this even possible.

Vik: Yeah, that’s insane. 13.5 nanometer EUV is an incredible feat of engineering. We are here today because ASML took 20 years to develop this.

And the whole question of how ASML ended up with this is another interesting one, because this technology was actually developed in the United States. At some point it was sold to ASML. And at that time, the United States government didn’t come in and say, no, this is critical technology, we want to hold it. The US government has blocked many such things before, including protecting 5G technology — they’ve done all of this stuff. Even now there’s so much export control. This was before the day of export control. We, from the United States, handed over the keys to the kingdom to ASML a few decades ago.

And kudos to them, they spent 20 years developing it. There’s an enormous supply chain that goes into ASML’s machines that all needs to come together to make this work. So it’s built on a massive amount of effort. But I just wanted to point out that this was actually US technology at one point.

High NA and the Limits of Mirrors

Austin: Totally, that’s a great history lesson. We should write more about that history sometime. Okay, so we’re running long, but let me blow through this. It’s an engineering marvel to get 13.5 nanometer light, but we want to make transistors smaller. What do we do?

Like we talked about with the Rayleigh criterion, you ultimately have two big knobs you can turn. One is the wavelength of light — but if you’re like, dude, we spent so long to get here, we’re not just going to turn that all of a sudden, 13.5 was hard enough. The other knob is the numerical aperture, which ultimately has to do with the size of mirrors. And so that’s where we get into high NA and extreme NA, or whatever it was called, Hyper NA.

But maybe really quick: the industry’s trying to move from 0.33 numerical aperture, low NA, to 0.55, high NA, which makes features on the order of 1.5 to 1.7 times smaller possible. But there’s a catch — there’s always a catch in engineering, there’s always trade-offs. You need bigger mirrors. When you have bigger mirrors, you’ve got these steeper light angles as they bounce in, and you have something called anamorphic optics that come into play. And I won’t get way into how that works and what that means, other than to say you ultimately end up only being able to pattern an area that’s half the size of what you could with low NA. They call this the half field.

So basically now, instead of your $250 million machine printing an area, you’ve got a $400 million machine printing half the area. Of course, that sounds horrible. Now you’re telling me — okay, Mr. Salesman, I just bought a $250 million machine from you, and now you say I need not only your $400 million machine, but I need two of them. That’s crazy.

ASML has done a ton of amazing engineering, where they’ve said, yes, we can only do a smaller size, but what if we speed up the scanner and the mechatronics to go even faster to make up for it? So it’s like, sure, the area is going to be smaller, but we’re just going to move that thing around the wafer even faster. And again, ASML has all these amazing videos on YouTube where they show how fast they’re accelerating and moving this stuff. It’s crazy. It’s like fighter-jet-style acceleration, but with nanometer precision, moving things perfectly around, stopping and reversing. It’s crazy that it all works.

But again, things are expensive. There are more trade-offs. There’s a lot more innovation that needed to happen. And ultimately, even with the proposed Hyper NA, even bigger mirrors, there are even more trade-offs, even with stuff like photoresist. So I’ll just leave it at that — we won’t dive into high NA or Hyper NA — but just trying to illustrate that not only are there economic challenges, there are also engineering challenges, and presumably reliability challenges.

So we’ll leave you with this. The question is, instead of the mirrors, could we make the wavelength smaller? How could we make the wavelength smaller?

Vik: Yeah, I want to add one more thing about the mirrors — that’s an engineering challenge — but then we’re going to talk about how to go even smaller wavelength.

These mirrors are not simple. It seems like, what’s the big deal going from low NA? You just have to make a bigger mirror. Make a bigger mirror, what’s the problem? These are not ordinary mirrors, because they are actually made up of 40 or 50 alternating layers of very thin molybdenum and silicon. They’re layered like this, and it is insanely smooth.

I read this book, Chip War by Chris Miller. It’s a good book, I recommend it. It talks to a lot of history, and a lot of what I’ve said here is from that book. And I have a quote here from that book. It says, “if the mirrors in the EUV system were scaled to the size of Germany, their biggest irregularities would be a tenth of a millimeter.” Think about that. Think about how flat those mirrors are. We’re going to put up a picture here and you’ll see how smooth it is. It is very difficult to even hold this thing — I feel like I would only want to breathe on it. I don’t know, they probably have protective gear.

But making bigger mirrors isn’t easy. It is an incredible engineering feat to make irregularities a tenth of a millimeter when the mirror scale is the size of Germany. That’s really flat, right? That’s a very smooth surface. So it’s not simple that we can go from a 0.55 NA, which is high NA, to like 0.75 next year. We’re used to the incredible pace of AI. Everybody’s like, oh, what’s the big deal, we can go to 3.2T, 6.4T, 12.8T networking, no problem. When are we going to get there, two years, three years, what’s the time frame? No, no, this stuff is difficult. You cannot make a mirror that easily.

So that’s where we are right now. And now the question is, what’s next? A machine costs a billion dollars, and now you tell me there’s only half field, and now I need two billion-dollar machines. The economics is exploding. Something is going wrong. And so this is where we have new ideas, to go where no human has gone before.

The Startups Rethinking Lithography

Austin: Totally. Okay, transitioning here. People will say, you could never compete with ASML. It took the industry so long to figure out this 13.5 nanometer light, and they have a supply chain — they have a relationship with Zeiss, the only company in the world that can make these perfect mirrors. Why would Zeiss sell their mirrors to you, dumb startup? Of course they’re not, because they don’t want to make ASML mad. And so now you’re going to have to go get another company to be the next ASML, or the next Zeiss. It’s never going to happen, right?

And so some startups are saying, okay, hold the phone. Let’s forget all that. Let’s just think simple, from first principles. Could we get a smaller wavelength of light? How do we tackle the optics? How do we tackle the integration, the mechatronics, all that stuff?

So one startup, xLight, out of California — and I think Pat Gelsinger is on their board now, maybe he’s the chairman of the board or something. What they’re trying to do is they’re saying, what if we use free electron lasers as the light source? So we’ll replace LPP, laser-produced plasma — that’s the tin droplet, shooting it with the laser machine gun and all the magic that happens. A free electron laser, by the way — think of it as accelerating electrons to near light speed. You’ve got these undulators that wiggle them, and you can get this coherent light. It can ultimately scale down to one nanometer, sub-one-nanometer.

But what if we start by using this new technology, but still producing 13.5 nanometer light, so that it can plug into existing ASML scanners and ASML optics? And by the way, FEL has a much higher total power, so what you could ultimately do is have a higher dose, which is better for yield. But actually, what xLight’s trying to do is say, what if we use one free electron laser, and we can actually split the beam and feed many EUV scanners? So they’re ultimately trying to decouple the light source from the scanner. What if you could buy 10 scanners and feed them with one light source?

Or maybe they’d have to have two light sources, one as a backup in case one doesn’t work, but you get the gist. So that’s the approach they’re trying to take — what if we build one massive free electron laser next to the fab and pipe the light into all of your ASML scanners? You can amortize the cost of your FEL across all those scanners. There will be some integration, but we’re not going to ask everyone to change the optics, the photoresists — we’re not going to ask anyone else in the industry to change. We’re just going to decouple the light source.

Vik: That’s fancy. Yeah, I haven’t looked into xLight, so I’m actually learning on the fly right now. That’s amazing. One of the things you can do with a laser source that has a higher output power is — tell me if I’m wrong — if you can get more light onto a wafer, the throughput actually increases, doesn’t it? Not only yield, the throughput goes up.

Austin: Correct, correct, correct. The throughput, exactly. If you only need a small flashlight to shine on something, and now you’ve got really powerful light, you could get the same amount of light by taking your really powerful light and shining it for less long, exposing it for less long.

Vik: How many photons get in?

Austin: Exactly. So therefore you can increase the throughput. But you could say, okay, well, the yield maybe isn’t that great the way the industry is doing it now. So we’ll shine it for just a little bit longer than we need to, and you’ll get even more extra photons. So you can have a higher dose, but ultimately have both better yield and better throughput.

Vik: So who would be the end customer of xLight? Would it be ASML?

Austin: No, it would be the fab. The fab would be buying. And the crazy thing — I wrote about it on Chipstrat, you can go check it out — the business model here is ultimately selling light, sort of like a utility, “photons as a service.”

You might ask, okay, why would TSMC go build an FEL from some startup, and then have to rejigger and work with ASML to say, we don’t want your LPP light sources, we just want your scanner part? That seems like a lot of risk and a lot of effort for TSMC — and a lot of capex, by the way.

What if xLight came in and said, we will pay to build this utility right next to your fab, just like you get electricity delivered, just like you get water delivered, and even just like you buy gas? These fabs will buy inputs like gas in this consumption-based way. Let us build the FEL, the light source, and then we will just charge you for what you consume. So it’s on our books, we take the capex hit, and then we’ll just charge you. If you want to spin up three scanners, fine, we’ll feed you three scanners. Now, of course, xLight ultimately wants you to spin up as many scanners as possible, but there’s a way that xLight can take a lot of the risk and do a lot of the upfront investment, and then just sell light to TSMC over time.

And by the way, once they build that relationship, not only could they sell you 13.5 nanometer light, but maybe for a premium later, once you and the industry are ready, they could sell you one nanometer light. So it’s a very interesting business model.

Vik: So the optics and stuff still comes from ASML, but then you’ve got this free electron laser sitting on premises at TSMC, just supplying light. They count the number of photons you use and charge you for it? Is that the whole business model?

Austin: Yep, presumably. How they do that — how they track how much light you’re consuming — would also be very interesting to know. But exactly, it’s like your electricity bill at the end of the month is going to be your light bill. Your light for lithography.

Vik: Amazing. So what other ways are there to make one-nanometer-wavelength light?

Austin: All right, one more that we’ll hit on today. Substrate is another startup. They’re also in California, in San Francisco, and they are throwing out the playbook and taking a different approach. Instead of FELs, they’re saying, hey, what if we use X-ray lithography?

Historically, X-rays were generated by big synchrotrons — football-stadium-size particle accelerators, essentially. There’s precedent there: again, you speed up these particles, they get super high energy, super high energy means really short wavelength, and you can ultimately control it and use it as a light source. The industry has actually explored using X-rays as a light source. And again, if you Google “Chipstrat substrate” you’ll find this, I wrote about the history — IBM did a ton of work. A lot of this early research happening in the United States. IBM did a ton of work here to see, could this be a path forward for the industry? And they actually made a synchrotron, or an X-ray light source, that fit on a truck. So it’s a bit of a myth that it has to be massive — they figured out a way to make it a lot smaller.

And this is the approach Substrate’s taking. I’d phrase it this way: IBM and a bunch of other people, back in the 80s and 90s, explored X-ray lithography, and it was a working prototype. It wasn’t economical yet, but a lot has changed in 30 years — not only about light sources, but with photoresists and optics and everything else it takes to build a light source and a scanner and do lithography. What if we went back and revisited from first principles, and took a stab at X-ray again, and said, hey, given all that we’ve learned in the last 30 years, could it now be economically possible to do lithography using particle-accelerator-based X-ray lithography?

Vik: Yeah, I wanted to step back one minute and quickly explain what a synchrotron is. The idea of a synchrotron is that you accelerate a charged particle in a ring — in a circle or an ellipse or something like that. And as the charged particle, which is continuously being accelerated, turns around and changes angle, it spits out X-rays as it turns around. That’s basically how a synchrotron works.

And typically, in the past, like you mentioned, these are really big installations. Particle accelerators tend to be really big, depending on what energy you have to accelerate them to. But I think the invention for making tabletop synchrotrons has been around 20, 30 years already. So it’s not something you really need a whole lot of space to do. That’s very important, because people shouldn’t be like, what do you mean? You need a football field, we don’t have that kind of space, so we can’t do X-ray lithography. No, I think it can be done in a smaller way.

But the one thing I learned when I wrote about this — it’s on my Substack too, about Substrate and X-ray lithography — is that it’s very difficult to actually focus X-rays. We spoke about the mirrors for EUV lithography, but you can’t do that for X-rays, because they go through things. You can’t reflect them. That’s a big problem. So the optics for X-rays is a challenge. It really is a challenge.

So one of the ways you can do this is what is called proximity printing. Like we mentioned earlier, the inverted-microscope approach means you could scale down a mask — you could put the mask on the big end of the microscope, and then the other end scales it down, let’s say five times. That’s called reductive printing, I forgot the exact term. Basically, you can reduce the magnification factor by a factor of five, because you’ve got this inverted-microscope approach. By the way, it came to me — the person who did that was Jay Lathrop, he’s the guy who came up with this idea. The name came to me later.

So you can’t do that with X-rays, because there’s no optics that works with them. You have to do proximity printing, which means you’ve got to make masks the same critical dimension as the stuff you’re patterning. So the masks are actually very fine. And for this purpose, the mask-making is significantly harder when you’re using X-ray lithography, because you don’t have the optics for them. So there are a whole lot of challenges that need to be solved. It’s not just, we’ve got X-rays now that go to one nanometer, so just swap out the LPP 13.5 nanometer source for a one-nanometer X-ray and then voila, you can print 0.1 nanometer gate-all-around transistors or whatever it is. It doesn’t work that way. Once you change the wavelength, everything changes.

And that’s where we are now. There’s this startup called Substrate that’s working on this. They made quite a splash some time back, because they feel that not only can they make smaller transistors and continue to scale Moore’s Law, but X-ray lithography can be significantly cheaper — you don’t need to spend $1 billion for an EUV machine anymore. Which means that most people, with far less capital investment — going back to the whole economics angle that we started with in this podcast — can make more fabs.

And then, if this technology is held within US soil this time, and not given away, maybe all of manufacturing will come back to US soil. If we can make X-rays work, and now we can own all of the supply chain required to make — well, I don’t think we can own the whole supply chain, but if we can at least make wafers on US soil and have so many fabs that we don’t rely on anybody else, that would really propel the chip-making industry like we have never seen before. So that is the case for making X-ray lithography on US soil.

Austin: Totally, man. There are so many implications. We have to do a full episode on this — hopefully we’ll talk to them.

First of all, it’s good that you point out there’s lots of engineering that has to happen, not only with the light source, but with the optics. And there are implications for the mask — how do you draw a mask at such small dimensions? Maybe it’s E-beam. There’s going to be a cost to that, right? So there are lots of technical questions to get answered.

But to your point, the implications are very profound. If in fact it can ultimately reduce the cost — hey, could GlobalFoundries make two-nanometer chips? Could Texas Instruments? Why not? So what are the implications, which I think is super interesting, of these legacy fabs, trailing-edge fabs, now being able to make even smaller transistors at the cost of maybe their trailing-edge nodes? Tons of implications.

What does that mean for fabless design companies, where you’re like, well, yeah, maybe we’d make our own chip, but that’s pretty expensive — I don’t know, probably we can’t amortize $100,000 per wafer, we only need five wafers or something. But what if all of a sudden, it was the cost of a 90-nanometer chip, where you can now buy wafers for $10,000 instead of $100,000, but get two-nanometer transistors? Crazy implications. And then, to your point, the geopolitical implications are fascinating too.

Vik: Ultimately — you know what will happen ultimately? What Jerry Sanders said: real men will have fabs again.

Austin: Totally, totally. Even that — why did every company at the start of semiconductors have a fab? Well, because ultimately, if you’re vertically integrated, you’re going to get a better product. If you can co-design across the fabrication — across the design and the fabrication — if you can design but also design for manufacturability, all in the same house, you’re just going to go faster, you’re going to build a better product.

But ultimately, the cost, because of Rock’s Law, got so big that people had to drop out, because they couldn’t afford a billion dollars for the next fab — $2 billion, $4 billion, $8 billion. Everyone has to drop out, because the GlobalFoundries or the TIs, they just can’t, they don’t have enough volume or high enough ASPs to amortize that cost. So it’s just dropping off.

But yes, in an ideal world, some of these players would still love to design and build their own chips. And of course, from a wafer-allocation perspective, you own your own destiny. There are so many amazing implications. I know everyone gets super hung up on, the technology is impossible, who dares think they can take on ASML and Zeiss and all that crap. But I’m more excited about all the positive implications that will happen, that will benefit all of us.

Vik: If you’ve been watching this on YouTube, you’ll notice that I’ve been drinking from this lens cup. So now that it’s over — I guess that’s our episode. We’ve spoken a lot about lithography. So let’s get on with it.

Austin: Totally. Okay, that’s it for today, everyone. Thanks for listening, thanks for hanging with us. We hope you’re enjoying Semi Doped. Please tell your friends about it, pass it along — if they want to learn about lithography, send this to them. Send us questions and comments on YouTube. Subscribe at semidope.com to our Substack that we’ve started. And thanks, as always, for joining us in this journey.

Discussion about this video
