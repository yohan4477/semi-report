---
source: https://www.youtube.com/watch?v=sy-PzR9dXDU
vid: sy-PzR9dXDU
title: Qualcomm's Durga Malladi: HBC vs HBM, Dragonfly AI 250, and Winning on TCO
date: 2026-09-24
duration_sec: 1250
channel: Semi Doped
kind: transcript
---
Hello, how listeners. Austin Lyons here
with Chip Strat and with me is Durga
Maladi, IEEE Fellow, which is pretty
cool, and EVP and GM uh
of tech planning for edge and data
center. So, we're here to talk
high-bandwidth compute, but first,
before we get into that, which is a
great topic, I want to know more about
like tell me what your job title means.
Tell me what you do at Qualcomm.
&gt;&gt; [laughter]
&gt;&gt; So, uh
I run all the uh the IP and the
technology planning for what we need to
do across all the products uh ranging
from data center all the way down to
edge solutions including devices.
So, that means the IP, if you kind of
think about it, is what should we be
doing in our CPU portfolio in let's say
3 4 years downstream in '29 and '30 in
data center uh versus what do we need to
do in devices uh in enhances and in new
agentic devices. And then rinse and
repeat the same exercise for what do we
need to do on GPU, what about what about
NPU, what about modem, what about
sensing hub, and so on. So, these are
all the different IPs. So, that's the
planning exercise which kind of runs the
road map behind the scenes, but it is
across all the business units.
&gt;&gt; Nice. That's pretty cool. I like that
you see across all the different
technologies, so that it's not like CPU
running not not together with GPU or not
together with the different products.
&gt;&gt; Yeah, it's pretty cool. Okay, so, let's
talk high-bandwidth compute HBC. So, the
way I see this is is obviously Qualcomm
is trying to enter and is in a
competitive space with inference
solutions in the data center. You've got
GPUs, there's XPUs, um
and Qualcomm has the Dragonfly
lineup um AI 200 25300. It It feels to
me like HBC is Qualcomm's big technical
bet to differentiate and bring something
different to market as compared to what
everyone else is doing. Um so, you know,
of course I want your thoughts on that,
but also then tell us what is this HBC
and how is it different from what others
are doing?
&gt;&gt; Absolutely, yeah.
So, when we reentered the business uh
data center business last year,
uh and uh I actually ran it for 1 year
like last year. One of the things that
we really focused on is you're
absolutely right. Uh there's a lot of
players already in the market and they
have some pretty incredible solutions
already. So, it wasn't one of those
moments where we said, "Okay, let's also
jump into the fray." And it's it's not
like a me too moment or anything of that
sort, but it was like
what is it that is going to be
differentiating us from uh
the rest of the ecosystem there?
And what is the really
uh what is a really good tough problem
that we really want to solve because
that actually gives us the benefit of,
"Okay, that is different. Let's take a
look at Qualcomm."
And we latched onto the fact that um
and and we had an R&amp;D project that was
running internally for a while on what
is called as near memory computing.
And the principles of that are very
simple, but before that, what is the
problem that we're trying to solve?
And it turns out that if you kind of go
back in time, maybe over the last 6
years or so, you will see that uh the
compute capability, like if you just
take any of the GPUs and say generation
over a generation, how much is it
improving?
It improves quite a lot, actually. It's
like uh at least a you know, factor of
two, sometimes a factor of three.
But the memory bandwidth wasn't actually
improving at the same league.
And so, the natural next question to ask
is, "So what? What does that do?"
Well, you know, if you kind of go back
to some of the basic principles of how
do you do compute? Well, you have all
your data sitting somewhere
and you have to fetch the data to do the
compute processing, but at some point in
time, what happens is that your computer
is so good
that you've kind of tilted the scales
quite a bit. So, you might be just
idling. You're waiting for the data to
actually show up. So, memory bandwidth
becomes a bottleneck, and it's called
the memory wall. And you see that a lot
more with AI inference, especially in
the decode portion of it.
&gt;&gt; Mhm.
&gt;&gt; And so, what we did is our HBC
architecture
is based upon what is called as near
memory compute. Instead of treating
memory and compute as two distinct
concepts,
what if we actually do a lot of the
compute right next to memory? Like,
literally right next to it.
It does two things. One,
the latency comes down quite a bit.
And second,
uh we can uh reduce the power
consumption quite a lot. So, today in in
data centers, HBM, you know, it's the
the bandwidth is very high,
but uh it's expensive, and it's a power
hog. So, uh we actually wanted to make
sure that we can solve it in a different
way.
And one thing led to another, and as we
started talking about this with a lot of
the hyperscalers and a lot of other
partners,
they loved the idea. And uh
uh as we announced it, we actually
announced a uh couple of names in terms
of some of the partners that we have.
So, it's been a great journey on HBC.
But, uh
as we briefly mentioned in our investor
day in June and today at Snapdragon
Summit, in fact, Cristiano left a teaser
out there.
Uh but, let me just tell you uh you
know, what is the point of this.
HBC for us is a technology, but it's not
just for data center.
It actually applies to everything all
the way from data center to servers and
accelerator cards and automotive and PCs
and XR and yes, in smartphones as well.
Uh but, it actually works in a different
way in some of these things. But, the
principle remains the same, which is
you're doing a lot of computation right
next to memory.
&gt;&gt; Mhm. Mhm.
&gt;&gt; [clears throat]
&gt;&gt; That's good. That's great explanation.
And And I like how you mentioned that
HPC is something that can be applied
across from the data center all the way
to the edge, and that's a good
organizational design as you're talking
earlier about how your job is to see IP
across all that. So that that's pretty
cool. Okay, so what I heard from you was
that the problem is compute is
increasing quickly, memory bandwidth is
not increasing fast enough. So this like
all this extra compute can't get fed
quickly enough, and maybe instead of
trying to just
increase the bandwidth of the memory we
use today, you guys stopped and said,
"Wait wait a minute. Why have to shuttle
all this data? Why Why shuttle even more
like wider buses or even faster speeds?
Why not just bring it really close to
the compute?"
&gt;&gt; That's correct. Exactly. And uh keep in
mind that it's uh
uh it's a principle that, you know, as
you start bringing down the power
consumption quite a lot, uh just uh
going one step further on devices, power
consumption matters quite a lot in
devices, especially as you think of all
the agentic AI-based devices that you
see these days. They're still evolving,
by the way. There's a lot of new players
who are coming to the market. In fact,
quite a few of them have very little
background in manufacturing devices or
making devices. They come in from an
AI-first mentality, and they're coming
up with these devices.
And
the job of agentic AI devices is to be
kind of being constantly on because
they're working all the time. So that
power consumption benefit that we talked
about is going to be key,
uh we believe, uh in unlocking the full
potential of agentic AI devices.
&gt;&gt; Yeah, that makes sense. So it's not just
the memory bandwidth problem, but the
also added benefit of because you're not
shuttling this data so far horizontally.
Now it's just going vertically, which
we'll get into. There's also big uh
power savings. And of course we know
that power is the big constraint. Um
okay, so then you know, to someone who's
listening this the first time they've
heard of high-bandwidth compute,
are you sticking memory on top of a
accelerator or
Tell us more about like the stacking and
the separation. What is being sent kind
of across the wire horizontally versus
vertically?
&gt;&gt; Yeah. Uh by the way, there's a really
cool animation that we showed at
investor day. I wish we had that, but
I'll just use my hands as props. Okay.
So,
so the way it works is that uh the
memory is like uh you know, you have
these individual, you know, the DRAM
it's called as a stacked DRAM. You're
basically stacking DRAM one on top of
the other.
And there's a lot of wafer-on-wafer
bonding techniques that are used on
that. So, this is this is a hardcore
process technology, by the way. This is
In fact, it has nothing to do with
computer at this point in time.
But then, right underneath that stacked
DRAM is what is called as the logic die.
That's where you put in all the compute.
And depending on the use case, you might
actually say, "I want some specific
logic to actually reside over there."
There might be yet another processor
that is still sitting, which is away
from it. But you've brought in a lot of
the heavy computational needs, like the
ones which really need that memory
bandwidth. You put all of that right
next to memory in that base die. And
that HBC therefore is a combination of
both. The stacked DRAM on top, plus the
logic die that is underneath or the
compute die that is underneath. And now,
you've kind of done a bulk of the work
just with that alone. There might still
be some residual compute that you want
to do, and that could occur in a
separate processor over here.
In some sense, HBC kind of is like
it's a bit of like a co-processor,
because it's doing a lot of the compute.
But it's not the only thing. You might
still have another main processor that's
running out there. But it removes that
complexity quite a bit. So, uh in short,
it is literally right underneath that
stacked DRAM that we're talking of.
That's where all the compute is being
done.
&gt;&gt; Okay. Okay. That that's helpful. So,
anyone who's familiar with HBM will say,
"Well, this sounds a lot like HBM 4E
with a custom base die and stacked DRAM
on top. So, tell us the the differences.
First of all, is it a different class of
DRAM that's being stacked? And And then,
how should we think about the difference
between the accelerator at the bottom
versus a custom die?
&gt;&gt; Yeah, that's a In fact, this is exactly
one of the things uh when we first came
out with the concept and when when we
talked about it, uh you know, I went to
Korea and we
and some of the other memory vendors in
the US and in other parts of the world.
And to be honest, I half expected people
to say, "Now, wait a minute. Now, we're
doing exactly the same thing. I don't
know what you guys are talking about.
Uh you know, we have a pretty robust
road map coming in." Actually, what I
heard is the diametric opposite of that,
which is, "How can we work with you
closer on this?" Because yes, this is
indeed the right way of actually doing
it. Because one thing that happens is
there might still be ways of, you know,
the basic principles and the concepts
look similar,
but that wafer-on-wafer bonding that we
are talking of, and we still use a lot
of LPDDR-based
uh interfaces towards the main
processor, which is sitting out there,
which means we still keep the power
consumption extremely low.
Uh there are evolving things that are
coming up in HBM as we move forwards,
but at this point in time, we see that
if you're a memory vendor,
uh
even if you are working on HBM and
you're looking at customizing HBM a
little bit further going towards 4E and
beyond,
I think stacked DRAM is here to stay.
Mhm. And you might have noticed a couple
of announcements that have been made
even by the memory vendors. They have
different terminology for that. It is
their equivalent of HPC, but actually
they are partners of ours. So, uh we
expect that uh
these two technologies will co-evolve
for a period of time, and we'll see what
happens after that.
&gt;&gt; Mhm. Interesting. Interesting. Okay, so
then um which by the way, have you guys
disclosed anything about the layers
number of layers that you're stacking?
&gt;&gt; Uh
we have not yet provided all the
numbers. In fact, stay tuned on that
front because, uh, you know, you haven't
asked the question how's the silicon
coming along and so on because we've
talked a lot about it in terms of, uh,
PowerPoint presentations and and, uh,
you know, most people are actually
taking our numbers for what they're
worth. But, we will be talking we will
be showing some proof points over the
next quarter or two as the silicon is
back in the lab and it's coming along
very well. So, stay tuned.
&gt;&gt; Okay, awesome. I'd love to hear that.
So, you'll have silicon coming back
soon. Looking forward to that. Looking
forward to see the benchmarks. That
really turns it real, for you know, from
just PowerPoint. Um, back to the the
stacking of the, uh,
memory. Talk talk to us about the
thermals.
Is is does that become a constraint for
that base die?
&gt;&gt; I think it is, uh, one of those things
that, uh,
as Qualcomm, when we come in with, uh,
you know, we are not when we talk about
IP, for instance, it's not just about
what we are doing, uh,
uh, for our CPU or our NPU logic and so
on. We have a a rich heritage of, uh,
both, uh, packaging technologies and and
3D stacking and a lot of these things
that we do. We work very closely with
the foundries in terms of like how these
techniques need to come together.
And that has played in our favor as we
brought out, uh, HPC. And, uh,
uh, one thing to mention is that, uh, in
this space,
uh,
you know,
you have to think through carefully as
to
which product are you designing this
for? And based upon that, you have to
think about the right kind of packaging
so that you don't start hitting other
constraints. Like, it's not the power,
maybe, but then you start hitting
thermal constraints. So, we do have a
lot of experience in that space. So,
different depending upon which product
it is, we have dimensioned the compute
in such a way, compute plus the memory,
which is dimensioned in such a way that
we avoid the thermal problems. And and
so that is something that we've paid
some careful attention to.
&gt;&gt; Nice. Nice. Very promising. Okay. So,
the Dragonfly AI 250 is the first
product that will have HBC in it.
&gt;&gt; That's correct.
&gt;&gt; And that's coming in 2027.
&gt;&gt; That's correct.
&gt;&gt; Um I saw that compared to the AI 200,
they both have the same amount of LPDDR
in the card. It's like 768 gigs.
&gt;&gt; 768 gigs.
&gt;&gt; Um and yet the 250, which is the first
to have the HBC, has 18x the effective
bandwidth, I believe is what the what
the website said. So, again, just for
everyone, can you
uh remind us again why that uh HBC in
the stacking is 18x the bandwidth as
compared to in the 200, where presumably
the LPDDR is, you know, a little bit
further away.
&gt;&gt; So, first of all, the raw memory is
completely different concept compared to
the actual memory bandwidth in itself.
So, this is LPDDR, which means we can we
can actually pack It's a very dense card
that we have. So, it's 768 GB.
You know, a lot of the other things that
we see in the industry, they have like
288 GB per card. This is like 768 GB.
Which, by the way, if you kind of think
through that, 768 GB per card means
if you take a typical order of magnitude
trillion parameter model, and it's all
like at mixed precision FP4,
you can fit a trillion parameter model
in just one card.
&gt;&gt; Mhm.
&gt;&gt; That is like seriously mind-boggling.
And we have shown that. We have shown
shown some proof points associated with
that. But that's just the memory
capacity.
The memory bandwidth is where, as we
bring in HBC, then you have this
combination of the underlying logic plus
uh plus DRAM stack. So, this actually is
a slightly different concept. This is
not about the capacity anymore. Using
the same capacity, you've just boosted
the memory bandwidth significantly.
That's why they are two independent
concepts.
But another way of looking at it is, if
you take an AI 200 card and it has a
certain performance certain
exaflops per rack or exaflops
in a given rack and of course we have
disclosed that you know our racks are
like 160 kilowatts. When you go from AI
200 to AI 250
the amount of memory inside it's like 41
or 43 terabytes or so
that doesn't change but because of the
fact that there's a huge memory
bandwidth increase
the number of exaflops in the card in
the in the rack actually goes up
substantially because of that because
the decode performance improves quite a
lot. So you see it's the the the total
number of like the amount of capacity
that you have in the rack is the same.
But now you've dismantled that memory
wall with HPC and that's the reason why
our overall performance goes up
significantly with AI 250.
&gt;&gt; Mhm. Okay, so let me reflect back to you
if there's a part where I'm a little
fuzzy on. So we've got more bandwidth in
the AI 250 which of course would mean
better decode performance so just like
more tokens per second.
&gt;&gt; That's correct.
&gt;&gt; How does
that that unlocks more flops because the
flops are not under utilized they're not
like sitting waiting is that what it is?
&gt;&gt; right. In fact because of the fact that
you're running it that way your TCO also
becomes better in the sense that if you
just taken because the tokens per second
per watt goes up significantly because
your tokens per second has gone up it's
the same power consumption by the way
it's 160 watt
kilowatts. But then in addition to that
then when you take a look at the total
it's called the tokenomics where you
also normalize it by what's the cost
associated with that it comes out to be
even more favorable compared to some of
the other things that you see in the
market today. So in that sense every
time we have talked about the benefits
of AI 250 we have talked about not just
tokens per second but tokens per second
tokens per per per watt and tokens per
second per watt per dollar or sometimes
even tokens per second per dollar.
When you put the entire arithmetic
together, then you see why it becomes
actually far more favorable to go with
this.
&gt;&gt; Nice. Okay, so I was going to ask you
that. So when you have talked to
hyperscale partners, ultimately, is
there one of those that's most
compelling? Is it Is it about the TCO or
about the tokens per watt or kind of all
of it?
&gt;&gt; I think
increasingly these days,
it's about the TCO, increasingly.
It used to be about raw tokens per
second and tokens per second per watt,
but I would argue that TCO already kind
of captures that. Because if you kind
of, you know, think about it, what are
all the things that you need to worry
about? Well, okay, if I buy one of these
racks, first of all, how much am I
paying for it? So that's like one
variable. Second, what's the power
consumption? And then you have to figure
out for that power consumption, what's
my utility rate and there is some number
associated with that. The third one, of
course, is
how many tokens per second does it
really generate? Like how effective is
it?
And you put all of these three variables
together and I'm discounting things like
water that you need into the for cooling
and so on.
It's the TCO
that is something that is emerging as
the most important, but it does take
into account like these three big
variables.
&gt;&gt; Yeah, yeah. Yeah, no, I think that makes
a lot of sense. And just like
the simplest way for me to think about
it is like, okay, if I have a billion
dollars to spend and I have like a gig
Not even a gig, a 100 megawatts. If I
can buy X racks from some provider that
fit within the power envelope and my
budget or I can buy 2X racks from
someone else, well, even if the
throughput's a little bit different, you
know, generally if you have 2X the
racks, you're going to get more more
throughput. Um so that makes a lot of
sense to me. So I guess um let's see,
maybe last question,
when So there are other AI ASIC startups
who also, because they're coming in and
needing to do something different,
they're also making different technical
bets. And usually, like the skepticism
that people get with them is they say,
"Okay, that's great. Um
can you actually manufacture it? Can you
actually get allocation?" Now,
obviously, Qualcomm has is one of TSMC's
largest customers, and you have play for
allocation, but I also know that you
have many different business units from
data center to edge who all want the
same wafers. So, like talk us through
like how does that work? And I I assume
that, you know, you do have the
advantage there because you are
manufacturing things at production at
scale.
&gt;&gt; So,
you know, that's one of the places where
it is true that it's not enough to just
have the just the technology in itself.
That's why we've been placing careful
bets in terms of making sure that,
you know, our wafer allocations we have
like an excellent set of relationships
with all the foundries and also with the
memory makers.
And so, as they have come up as
extremely valuable partners and
across the entire portfolio, not just in
one domain.
Those relationships do matter. When we
go in front of a customer and say yeah,
we are in a position to supply you. How
much do you want? You want okay,
these many megawatts or maybe a
gigawatt. This is what you want. Yeah,
we have the supply chain lined up for
that because we do have those
relationships across all the different
businesses. And that actually helps us
quite a lot.
&gt;&gt; Yeah, sure, totally. That makes a lot of
sense. All right, well, that's it for
today.
&gt;&gt; All right.
&gt;&gt; There you go. This was great. We will
have to talk again once you guys have
more to share about the actual measured
performance of HPC.
&gt;&gt; All right, sounds good.
&gt;&gt; Thank you.
&gt;&gt; Thanks. Thanks again.
