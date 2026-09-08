---
source: https://www.youtube.com/watch?v=1SAjYncVs_c
vid: 1SAjYncVs_c
title: Power as the Next Physics Wall for AI
date: 2026-05-08
duration_sec: 2495
channel: Semi Doped
kind: transcript
---
Every part of this power supply chain
has a different player, has a different
technology. It is not like what you you
can you see in HBM. Oh, it's HBM. What
is it? Like the three same three
companies? What are they doing? Stacking
the same way? Right? It's kind of a
closed problem in a sense.
Power is a wide wide open problem.
&gt;&gt; Welcome to another Semi Doped podcast.
I'm Austin Lyons of Chip Strat and with
me is Vik Shaker from Vik's newsletters.
What's going on, Vik? It's been a crazy
earnings week this week.
&gt;&gt; Yeah, I can't listen to all the earnings
calls. I just try to listen to a few of
them and try to like run
the transcripts through LLMs and tell me
what happened. But other than that, it's
too much to keep up. It's a fire hose of
earnings calls this season. I I can't
keep up.
&gt;&gt; Yes, I know. Like in a dream world, they
would just all talk to each other and
schedule like one per week for the whole
season.
&gt;&gt; [laughter]
&gt;&gt; But no, instead it's like everyone in
the span of a couple days.
&gt;&gt; It's not intended that people listen to
all of them. I'm guessing that people
have investments in company A, B, C, D
and they just listen to those and you
don't listen to everything because, you
know,
even big investment firms have people
who address certain sectors of the semi
markets. People like us try to cover
optics, data centers, like memory, CPUs,
power, I don't know.
Power, speaking of power, that's what
we're going to talk about today.
&gt;&gt; Power, we're here to talk about power.
So before we dive into power,
um, should we address we had lots of
YouTube commenters. So thank you,
YouTube commenters. Should we address
any of the questions?
&gt;&gt; Yeah, I think we should
at least address one or two of them.
One was on the memory tax episode that
we did.
The comment was basically that
when we said that
um
memory costs going up and all the capex
being directed into memory
means that that money is not available
for compute. Uh I think the overall
sentiment around that was like
yeah, the money that's going into memory
is more like inflation and it doesn't
usefully contribute to compute or
solving the memory bandwidth or making
data move faster between racks. It
doesn't solve any technical problem in
any way.
Other than that, you're just paying
memory companies more. So, I think that
was mostly the sentiment.
&gt;&gt; Yes, totally. So, the the comment was
something like um
you know, that we're misunderstanding
and and compute's not the bottom that
memory's the bottom that and therefore
you should spend more money on on
memory. But yeah, to your point, what we
were saying is like no, no, no. No one's
I we're not saying don't spend more
money on memory. We're just saying that
like
you bought a gallon of milk for $2 today
and tomorrow costs $2.50 for the same
gallon of milk. So, you're just spending
more to get the same stuff. You know, so
yeah, it's like the cost yeah,
inflation, right? So, it's like
&gt;&gt; It's not like you're getting chocolate
milk. Chocolate milk would be nice, but
you don't. You just get regular plain
old milk. But you pay chocolate milk
prices.
&gt;&gt; Exactly.
&gt;&gt; that's not helping anybody. It doesn't
increase our quality of life.
&gt;&gt; Right, right. So, so the purchasing
power of a dollar is going down for
compute. So, a bunch of CFOs are are
going to say like, "Hey, we're spending
more we're for equivalent compute like
you know,
does this meet our internal ROIC
targets? What's the projections? When
will this stop?" So on and so forth.
&gt;&gt; Yeah.
&gt;&gt; but okay, so we addressed that. Um I
think we had a lot of people asking
about board fly. Did you want to talk
about it at all and how to how to get to
seven hops?
&gt;&gt; Yeah. So, the best way to go about this,
even rather than me going through and
explaining how this works
is that Google has published a deep dive
on the TPU8 i/t
blog, you know, it's a deep dive blog on
their website. So, if you go there and
look at the picture there in the blog,
it explains exactly how the
you know, 3D torus approach has 16 hops
and how the board fly approach has
actually seven hops. So, the idea is
that you have to get from the board
into the group where you have, you know,
so many boards in a rack kind of thing.
And then you go between kind of
you know, rack to rack through the OCS
switch and then, you know,
finally you
follow the same process on the other
side, you reach the other rack and reach
the other board. The Google picture
actually shows seven hops, so you can
see how each hop has
a different location it goes through.
So, the fact is that you can reduce
network diameter by using
their board fly topology means that the
latency
equivalently comes down compared to
using a 3D torus. It's
the latency is more than twice better.
&gt;&gt; Mhm. Mhm. Nice. Okay. So,
folks at Best of Times Love, go read the
original source for yourself and you
should be good to go.
&gt;&gt; Yeah, it's a good explanation. They do a
good job. Google blogs are nice.
&gt;&gt; Yes, totally. They spend a lot of time
and effort. So, thank you, Google.
Whoever wrote that out there, we
appreciate you. So, okay, let me hit
really quick last thing. Um, I had a
couple quotes from the Coherent earnings
call that I thought were interesting.
And we've talked about these topics
before, but I'm going to hit on it again
just cuz it's a continued theme that,
you know, people should be tracking,
which is ultimately
there's massive demand for indium
phosphide base lasers and this everyone
is scrambling to create more supply. And
for Coherent, the quote was from from
CEO, James Anderson, "We are
aggressively ramping 6-in capacity
because 6-in wafer, compared to a 3-in
wafer, will produce more than four times
as many chips at less than half the
cost." So, this is how Coherent is
trying to rapidly increase their supply
is moving to 6-in wafers. And so, again,
I just wanted to unpack it in case
people hadn't heard that before. This
whole like if you're like, "How do you
get to 4x more chips at half the cost?"
And we talked about this a little bit,
but ultimately, it's about the area of a
6-in wafer compared to the area of a
3-in wafer. And you know, if you it's
radius squared. And so, if you 6 squared
is 36, 3 squared is 9, 36 / 9 is 4. So,
that's how you get to four times more.
Um and then of course, the cost thing is
interesting and I don't think we've
talked about that quite as much, but at
the end of the day, if you're if you
have the same number of steps and you're
just processing a bigger wafer, your
costs are fairly equivalent. You have
the same number steps. You might have a
you have to pay more for a bigger
substrate and you have to pay more of a
little bit higher input cost because
maybe more photo resist and chemicals
and gases and things. But, let's say the
cost is maybe 2x higher, you can still
see a world where to to process a 6-in
wafer, you can still see a world where
you get four times as many die per wafer
and because it's bigger and yet it only
cost you twice as much to process it.
So, your cost efficiency is twice as
good and therefore you it costs you half
as much per die. So, I just wanted to
remind people really quick that that's
Coherent's play. Now, the question of
course that that everyone's asking is,
"Okay, they've got 6-in wafers, but is
it yielding and are what are they
actually making?" And so, uh James
Anderson did uh address that as well. He
He said, um
"Given the healthy yields we are seeing
with 6-in production, we began
production of 6-in indium phosphide at a
second site in Järfälla, Sweden." I'm
not quite sure how to pronounce it,
Järfälla, Sweden.
And ramping it two sites in parallel
will significantly accelerate our
production capacity ramp. Additionally,
we are in production on three different
types of key transceiver components on
6-in indium phosphide, EMLs,
continuous wave lasers, and photodiodes.
And somewhere else they He said, I think
it was in a Q&amp;A,
he specifically said that their 6-in
yields were as good or better as their
3-in yields. And pointing out like
that's comparing to the mature 3-in
yield, not just when 3-in was ramping.
And so,
I think he, you know, without saying
much about yields and performance, uh
Coherent was definitely trying to signal
it like, "Hey, we're not just building
the simplest component, we're
photodiodes, we're building
photodiodes, CW lasers, EML, and
they're pretty confident in their
yields. Um so, I I would just say it's
something to track. Coherent is telling
the story that that they're progressing
nicely.
I think maybe the final read-through
will be on their margins because of
course if they are um
increasing supply, decreasing the cost,
and yielding yielding well,
which would impact your cost, and
those devices they're making on the 6-in
wafers have good performance, which
means you can maintain ASPs or increase
ASPs, then ultimately this should flow
through to their margins. So, that's
probably just the final takeaway is if
you're trying to track it and really
trying to figure out is this just a
story or
are customers actually buying devices
that are built on this new capacity?
Ultimately, it's about yields and ASPs,
and we should be able to track that.
&gt;&gt; So, one small caveat to that is that
when talking about yields of CW lasers
or
you know, electro-absorption modulated
lasers, EMLs, which are the workhorse
for 200 gig transceivers.
Uh and CW lasers are the workhorse of
co-packaged optics.
These are the two hotly contested areas
really right now between Coherent and
Lumentum and all these companies. It is
very important to distinguish that CW
laser
but at what power?
&gt;&gt; At what power are you talking
&gt;&gt; 50 mW, 100 mW, 400 mW? That is
significant differences between what
yield means on what product. Similarly,
EMLs are the same way. Uh EMLs have like
two components to it. It has the laser
and the uh the absorption modulator. And
they are usually kind of co-designed to
work together. And that is
a significantly
more complicated problem to solve
compared to, you know, maybe CW lasers
where you just have to like put out
laser, right? You're not modulating
anything. It's just like a flashlight
that's on. You're not turning on and on
the flashlight depending on a zero or
one. So, CW lasers are structurally,
functionally, I wouldn't say
structurally, functionally easier.
So, it really depends on what yields
which product line what
power, what output levels. So, it's very
easy in an earnings call to put a
blanket saying, "Oh yeah, everything's
great." But if everything is great on a
50 mW laser uh
that's not what we're talking about, you
know. So, it really depends on what
exactly is yield meaning here. So,
that's the
that's [snorts] the wet blanket I want
to put on your otherwise optimistic
statement.
&gt;&gt; No, yeah. No, totally. I
I definitely don't disagree with that.
There's
the high-level directional guidance
they're giving and then to you there's
the nuance and
they probably won't share that level of
nuance on a call. Just like Intel's not
going to get super nuanced into like the
yields on 18A and 14A and give
engineering specs.
But but then that's the game is how do
you sort of
reverse engineer or back out what you
can to get a good sense of like, "Oh,
they're actually just insinuating
50 mW lasers continuously they're not
400 mW." And maybe again that shows up
in
revenue like top line revenue or maybe
it shows up in in margins or something
where it's like, "Oh, custom Their
margins aren't great because it's
customers buying the the cheap
product versus the like high performance
powerful product.
&gt;&gt; If they are selling high ASP products at
high yield, it will show up in
the money. Follow the money.
&gt;&gt; Exactly. Exactly. Totally. So, okay,
cool.
All right, let's jump into power now.
So, you wrote an article on power and
this is a perfect forum for us to unpack
it. So, Yeah. Yeah, set the stage for
us.
&gt;&gt; So,
there is this growing sentiment. It's
not just from me.
Few people in the industry have pointed
it out as well.
That
we are coming to a point maybe not in
this generation, maybe it's the next
generation of accelerators and racks,
probably Rubin Ultra,
because the Kyber rack is a 600 kW per
rack
power consumption
that is much higher than what usually
data centers are used to. So, in the
cloud era, each rack used to consume
like 20 kW. You know, now AI accelerator
racks consume anywhere between 100 and
120 kW.
Now, we are talking about the Kyber era
of racks where the Rubin Ultra
will go in
at 600 kW a rack. And the future will
have hold 1 MW a rack. That's an
enormous amount of you know, that's a
100 times
power per rack compared to what was in
the data center, you know, the cloud
era, pre-AI era, which was like at
approximately 10 to 15 kilowatts. You're
talking about 1 megawatt per rack. And
imagine how many will go into a data
center. And imagine, you know, how many
of those data centers are going to be
connected together via scale across, all
of that stuff.
So,
this is a looming problem, a bigger and
bigger problem with every generation of
and, you know, AI that comes out and
chips that come out. So,
I wanted to address it in my Substack
article to just point out that power
is the next physics wall, you know, and
this is a a theme I want to pursue in a
little bit more depth uh over time
because
as you can imagine, it's an enormous
problem, right? You know, you got power
generation all the way at like, you
know, whether you're talking turbines or
nuclear power,
how that's transmitted, and how it
reaches the substation, you know, how is
this converted into the data center, and
how it is ultimately delivered to the
GPUs. We'll cover some of that in detail
in this podcast. At least I'll explain
how this conversion happens and where,
you know, the markets' directions are
going to go, you know, going forward.
So, but you can imagine like this entire
chain has so many players and it has so
much going on there, and all of it is
important to deliver the next generation
of power. So, that's what I wanted to
kind of touch upon in the Substack post
and kind of we'll briefly cover as the
next physics wall.
&gt;&gt; Nice. Nice. Okay, let's get into it. So,
what is the problem with a 1 megawatt
rack? Why is that a problem?
&gt;&gt; Yeah. So, in this one,
I want to kind of start at the rack
level.
What is the underlying physics problem?
And then we will kind of zoom back a
little bit and understand how power is
actually generated up to that one and
delivered up to that one megawatt rack
because it's important to understand
how the power gets there, right? And
then we can talk about what happens
within the rack, which is essentially
what I focus on the sub-stack article.
So,
the thing is very simple. You know,
the idea is why are we talking about
optics now? Okay, I promise this is not
a tangent. Okay, this has something to
do with power. Why are we talking about
optics? The whole problem was with
copper, right? And reach. So, as the
speeds got higher and we needed to
connect racks over longer distances,
optics was the only way forward because
copper reached its physics limits. And
the physics limits in copper is as you
increase the speed,
what is flowing within the copper cable
is actually an AC signal. Like it's a
varying signal, right? Because you're
transmitting, let's say, bits that go up
and down like whatever. So, it's like a
varying signal.
And what happens in the copper
interconnect when you have varying
signals is that
all the current doesn't flow through the
whole copper wire. They tend to
concentrate on the periphery. Only the
outermost ring of copper actually holds
any signal. There's nothing happening
with the rest of the copper cable. This
is because of the phenomenon called skin
effect, right? So, it goes through the
skin of the copper cable, not really the
whole
cross-section of the copper cable. So,
the resistance goes up because you have
all this cross-section, but you're not
using it
and you're you're now have more
resistance. So, resistance was the
fundamental
bottleneck for why we needed to go from
copper to optics. And now you see
everybody's in the optics like Indian
phosphide shortages. The rest is
history, right? Look at the optics
market we're in.
So, this was a bottleneck that was
physics-driven.
And whenever something is
physics-driven,
it's easy to identify. So, go ahead,
yeah.
&gt;&gt; Totally. Totally. No, But that is what
we try to do here is look for the
fundamental physics constraints and then
ask what is going to happen beyond this.
All right, so really quick um for maybe
less technical listeners um when Vic
said AC he meant alternating current.
That's the varying current. And then
this skin effect thing, I mean if you
think of like I like to think of
electrons throwing through flowing
through a wire as sort of like a pipe
and or even you could think of it like
as a subway tunnel with like lots of
people trying to push through it. And if
this skin effect means you can only walk
like at the edges of the subway tunnel,
then you try to take the same people and
push them through the edges of the
subway tunnel, there's going to be more
resistance. You're going to bump into
each other more, right? Then if you
could just everyone could just walk
nicely with lots of space around them.
Um so when Vic says there's an increase
resistance and and the skin effect
becomes worse and worse at higher and
higher speed. So when we're trying to
communicate more and more data at higher
and higher speeds, then you get more of
this skin effect resistance bumping into
each other. So there's just a little
analogy for non-technical folks. Uh Vic,
now please carry on.
&gt;&gt; Yeah. No, thanks. That's good. I like
the subway analogy. I like analogies.
Yeah, totally. It's great. Thanks.
So the power and power is the same
thing, right? Now when you have a lot of
power,
say 600 kW or something,
uh ultimately you have to make two
decisions.
And actually it's one decision and the
other one follows from it.
What voltage are you going to operate on
in, right? Cuz power is basically
voltage times current. So if you are
operating at a high voltage, you have
lower current. If you're operating at a
low voltage, you have a higher current
for the same power.
And that decision is very important to
make.
Now typically in racks earlier in the
cloud era,
we didn't really need to go to very high
voltages because there's no need to. The
currents are manageable because the
power is manageable. So why do you want
to go to high voltages? Because you have
to use special transistors to actually
handle such voltages.
Not everything can handle it like that.
So, don't no need to go exotic if you
don't need to. So, typically what has
happened is
the voltage choice in racks
uh
from the, you know, it's not that that
long ago, you know, but so meta really
standardized on the 48 V architecture.
So, the 48 V DC architecture.
And so, the current was okay, you know,
that when the power was low, the current
was manageable.
So, now what happens when you go to some
massive amounts of power is that now if
you're at 48 V
DC, you know, you are going to go
to a lot of lot of current. Like take
this for example. So, a 600 kW of power
and 48 V
of rack voltage, you are burning 12,500
amps of current through the rack.
Like think about that. That's enormous.
And what happens is that wherever
whichever method you use to transmit
data, it can be copper wires, buses,
connectors, you know, whatever,
everything has a resistance.
And so, even the tiniest resistance at
you know,
12,000 amps of current means that you're
going to dissipate a lot of power. You
know, the power dissipated through a
resistor is like the squared of current
times the resistance. So, not not only
do you have a high current, now you're
going to square it.
&gt;&gt; [laughter]
&gt;&gt; Yeah, crazy crazy. So, yeah, so you're
saying power equals current times
voltage and ideally we would just have
like low voltage and not not much
current not a big deal, low power. But,
we're in an era where
&gt;&gt; [snorts]
&gt;&gt; we have already have a fixed
voltage. It's
What What did you say? 48 V coming in?
&gt;&gt; Yeah.
&gt;&gt; Yep. And so, but we want to have
much much higher power at the rack
because we just want to have way
much denser rack with way more GPUs and
they're all power hungry and so in
aggregate they want to consume a ton of
power. And so you're saying the only way
today if we stay with the 48 volts
to have all these GPUs that are power
hungry and to power them is to increase
the power and if P equals IV and the
voltage is fixed the only thing we can
do is increase the current to something
crazy like 12,500 amps or 12.5 kiloamps.
Like I it's hard for me to even
comprehend that. That's like a when we
were taking EE courses we were never
using like currents this high when we
were doing our little by hand toy
problems.
&gt;&gt; It's always milliamps, right? Like all
of our circuits are milliamps and now
you have kiloamps. Power electronics is
a beast, okay? So it's it's fine but
it's still a lot of current.
&gt;&gt; Yes, yes. But then what Vic also said
was
um okay, well resistance is
uh what I squared times
What did you say the resistance
Yeah, yeah, yeah.
&gt;&gt; dissipated. You know the amount of power
you lose through some form of resistance
whether it's the
uh connector or just the metal itself.
There's always some resistance and you
lose power
via heat to that resistance. You
generate heat when you push current
through a resistor and that power
dissipated is the square of the current.
So not only are you in like 12 kiloamps
of current, you're now squaring it and
then the resistance is like how low can
you make it? Like you know, I have some
example calculations on the substack. We
don't have to go through all of it now
but yeah, it's it's insane. Like you
will have a lot of uh power dissipated.
&gt;&gt; Nice, nice. Yes, so the problem is we've
got a a ton of power. We've got a really
high current. We're going to dissipate a
lot of heat because it's the square of
that current. So just lots of people
bumping into each other in the analogy
and giving off friction, giving off
heat. So how do we solve this?
&gt;&gt; So, the one way to fix this is go to a
higher voltage.
So, you know, for 600 kW, you know,
don't use 48 V,
use 800 V.
And it's a coincidentally the voltage
that is used in uh you know, EVs,
traction inverters. And so, that the
whole entire automotive industry has
kind of matured this uh silicon
transistor technology called IGBTs or
more recently the silicon carbide,
there's gallium nitride, all these
exotic wide band gap semiconductors as
they are called. These uh are specialist
transistors that can handle 1,000 V
of
uh
voltage and they are well suited for
such applications. So, might as well
reuse that EV industry and the
transistors around them. So,
you know, go to 800 V.
So, when you go to 800 V and you do the
same math, the current drops from 12,500
A
to 750 A. Much better, right? 750 A.
It's not you don't even have to use the
kilo kilo amp
unit.
&gt;&gt; Yeah.
&gt;&gt; Yes, yes, totally. Okay, so you're
saying
if we had um
P equals IV was our problem where the V
was fixed, so we had to increase the I a
lot if we wanted to increase the P, the
power. But you're saying, "Wait, wait,
wait a minute. What if we don't fix the
V? What if we actually increase the V to
get and hold constant, then the I can go
down, right? So, you're saying instead
of 48 V, we can increase it to 800 and
then that that way we could still get
the same really high power at a lot
lower current. Uh and then of course the
question is, well, which V should we
increase it to?" And and I heard you
say, "Oh, well,
everyone looked around and said, 'Hey,
why not 800 V because that ecosystem
already exists.'" That power electronics
ecosystem already exists for EVs. So,
that seems like a great place. Bring it
in
&gt;&gt; Yeah.
&gt;&gt; into the data center.
&gt;&gt; Because those are ruggedized components,
right? Like transistors that go in cars,
if it's like driving your, you know,
wheels,
uh
that is basically driven by transistors,
too, by the way. The battery power is
converted into alternating current that
drives the motor that drives the wheels.
Those things are rugged. They have to
operate in all conditions. They have
They have high thermal tolerances. They
have uh quality standards, you know,
there's a lot of things in place. Why
not? Why not reuse that stuff?
&gt;&gt; Nice.
&gt;&gt; Yes. And this also gives an opportunity
for EV companies to pivot into data
centers, because everybody wants a data
center angle.
&gt;&gt; Totally. Totally. Yeah, no, I think it's
super fascinating to be like, "Oh,
there's already power electronics here,
and they're already ruggedized to be in
a harsh environments from automobiles,
uh you know, to be hot or cold or
whatever." And so, like, "Oh, guess
what? Data centers are crazy hot. No big
deal, you know."
Uh and then yes, of course, naturally,
anyone when their investor brain is
listening, they're going, "Oh, wait.
Wow, this is going to be really
interesting. I should look into it.
Anyone who's already doing power
electronics for 800 volts or auto EVs or
whatever, because
now they're trying to move into the data
center." That's interesting.
&gt;&gt; Yeah.
So, it's a it's a nice solution to the
problem.
And Nvidia is looking into it. I mean,
this is not news to people who are
following the power side of things in
data center world. This is We are
talking about the basics, but that's
good, you know, we've always got to set
the baseline of understanding so that we
can follow what happens in the industry
closely later. But that's That's where
the foundational understanding comes.
It's good to have this. So, it's a good
discussion we're having.
So, the point is that think about the
power dissipated through heat now. The
resistance, let's say, is the same,
okay? For argument's sake. Your Your
current is so much lower.
Now, the square of the current is also
significantly lower, right?
Uh if you can drop current by, you know,
two orders of magnitude,
uh how much should we? At least we
dropped it by one order of magnitude,
right? Like 750 to 7,500, whatever.
Yeah, it's
&gt;&gt; K down to 0.75 K. So, yeah.
&gt;&gt; It's like 10-15 times lower current than
your
power dissipated is square of that. It's
like uh 100 to 200 times lower than
that. So, you see the fundamental
problem is that increasing the voltages
reduces the current and now this is the
only
viable way to overcome the same problem
of resistance that was plaguing the
copper interconnect world that is due to
plague the power world as well. Cuz you
cannot push that much current through
any form of resistance.
And this is not like the skin effect
kind of resistance we're talking about.
This is like standard Ohm's law
resistance. This is DC resistance we're
talking about here, okay? So, basically
this is the same limiting factor that
drove everybody from interconnect world
into optics, copper interconnects into
optics, right? This is the same
limitation that is resistance that will
drive people from uh low voltage systems
to high voltage systems. And when you go
to high voltage systems, it creates an
entirely new socket because this 800
volts to 48 volts conversion, which is
one way to do it, you you don't have to
bypass 48 volts.
You can convert from 800 volts to to a
certain voltage. What that voltage is is
is a question that requires some
engineering discussion. It's all on the
Substack. But
that conversion is a new socket,
basically, that does not exist in the
data center world and that is what
people are trying to compete for and
land it properly, right? And think about
the whole CPO argument again.
Uh you wanted to do the optical to
electrical conversion as close to the
chip as possible, right? Because you
don't want to be in the copper land at
all because it's a problem is
resistance. The same problem exists in
power. You don't want to
uh convert to power like, you know, to
low voltages far away from the chip. Uh
at if at all possible, you want to have
the highest voltage possible right up to
the edge of the chip. Make the
conversion at what is called the point
of load.
&gt;&gt; Yes.
&gt;&gt; Right? So, it's like think about it as a
CPU of the power world. So, now you have
what is called vertical power delivery.
You put the chip under the GPU, and you
deliver power at the GPU. Convert as
much as possible. Not that I'm saying
you're going to convert 800 V to 1 V at
that chip. That's like That's like too
much. There are still many conversion
stages that
need to happen before that happens,
right? But ultimately, that is the CPU
equivalent of power delivery.
&gt;&gt; Yeah, now that's good. I really like the
analogy of looking at CPU to say
basically, you want to keep it in light
as far as you can, as close in as
possible before you convert it to the
electrical domain. Otherwise, that whole
problem of like with
linear pluggables was you've got that
long copper trace, and it's very noisy,
and lots of power loss and signal loss.
So, no, no, no. Just bring in the signal
as close to the chip, the ASIC, the GPU,
or whatever is possible. Trying to do
the same thing. High voltage, low
current, bring that in as
close as possible before you essentially
like convert it down to step it down to
lower voltages. And this actually
reminds me of the analogies for people.
This is like how the transmission lines
work in your neighborhood, right? You've
got like really high voltage lines that
are sending power, you know,
across for me in Iowa, like across
cornfields to the next town. And then
only once it gets closer does it get
sort of step down and brought down. It's
kind of kind of the same thing here.
We're talking about high voltage so that
to reduce the the current and reduce the
power loss along the way.
&gt;&gt; Yeah. Yeah, it's very important. The The
power efficiency dictates how much a
compute because there there is a fixed
budget per data center. Like you can't
get more than so many gigawatts, right?
And so you want to convert all of that
into compute. You don't want to burn it
in like poor conversion power conversion
systems. You want to have all that power
available to
generate, you know, useful AI output. So
that is the key thing here. So that is
basically the setup. Uh
but I want to just zoom out for one
quick minute cuz I don't want this to
keep becoming a very long technical
episode cuz we're going to talk about
this a lot. Okay, this is not the first
or last time you'll hear about power on
this podcast.
&gt;&gt; People like when we talk technical, so
&gt;&gt; Yeah, and we will and we will. We like
this stuff, which is why we do it,
right? And there's so much I like nice
technical stuff. And this is like analog
semis, okay? I I love this stuff.
Personally, this is what kind of I this
is what I do, okay? And so I love analog
semis.
So zooming out, like look at what
happens.
You got power generated at the nuclear
power plant and like you said, that
power is transmitted with like hundreds
of kilovolts across, you know, the grid
to maintain
the losses to be minimal.
Uh and
finally it reaches like some kind of a
medium voltage substation um that is all
usually on the data center campus.
Uh I have another whole article on how
this whole big big picture thing works,
so look it up on the Substack. But
it is converted to something like 10 to
30 kilovolts. Now, this is all like
alternating current still. And all of
these like require these gigantic huge
transformers and insane looking things,
right? These are not like sensitive
delicate 2 nanometer gate all around
FETs. These are like honking big
machines that like burn power and it's
it's it's just it's the complete
opposite of the sensitive AI world.
Uh and then you know, though that power
is then brought into the utility room,
which is usually like little space
outside the actual data center where the
computer racks are kept. And in the
utility room, it is converted into like
you know, 430 volts. It's actually
converted probably in the data center
campus. But the utility room gets like
400 and 400 volts or 430 volts. You
know, this is like the three-phase
industrial voltage that people get like
you know,
you in at residential levels, you either
get like 110 volts or 220 volts or
something like that. But usually
industrial power is a 400 volts, right?
And then it is from there it is
distributed to
all the racks within the data hall. It's
called a data hall where all the racks
are kept. At the rack level,
this AC is converted to 48 volts at the
rack. So, that's where it happens. So,
this is like the power supply unit or
the PSU, right? And the PSU
after the 48 volt is available,
there are
to distribute it to various parts of the
whole rack, it is in various stages
converted to what is called an
intermediate bus voltage. So, you have
these things called intermediate bus
converters. What they do is they take
the 48 volts and they convert it to like
12 volts. Now, we are talking about low
voltage bus architectures, which is
converted to 6 volts.
So,
you know,
you can't convert 48 volts down to 1
volt. It's a challenging problem to do.
You don't You always have to have
stages. So, this 12 volts is an
intermediate bus stage.
So, that conversion happens. And then
ultimately
the 12 volts is converted down to maybe
1 volt range, 1 volt, 0.8, 0.65,
depending on the what GPU needs.
And you those are actually kind of
different because
those converters are They have one major
requirement. They need to be highly
voltage regulated. When the GPU wants
0.8 volts, it wants 0.8 volts. It
doesn't want
0.9. It cannot want 1.2. So, voltage
regulation to very
fixed values is very important at that
stage. So, those are called voltage
regulator modules.
And those are very specific, and they
have the highest uh count in a data
center, right? I mean, because the
voltage regulator modules are like many
compared to the
the rack level conversion that happens
uh
either from the PSU or the intermediate
bus converter, which is
the the actual mass market for power
lies in those voltage regulator modules
or VRMs.
Uh so, yeah.
So, so what you can like look back here
and see is
look at the number of stages of power
conversion right from the grid
all the way down to the GPU. And every
section of this
power conversion and voltage conversion
happens has a different set of
technologies. Like some of them operate
on a big inductor coils. You know, you
you have these like substation
transformers. But then you have these
like what are the they call LLC
converters? They just use like uh big
transformers
uh with windings like this, uh you know,
coupled to each other. And uh they just
convert voltages. You But those are not
regulated voltages. You know, it doesn't
matter if it converts to 48 volts or 50
volts. It's fine. It's not doesn't have
to be like accurate, right? So, the
entire technology chain and the supply
chain for that is completely different.
Then you got this different supply chain
that goes from 48 volts to 12 volts, the
bus converters. There are companies that
specialize in that, and you know, those
you have to get designed within data
centers in that section. Then you got
these voltage regulator modules. There
are like a few companies there who
dominate the space. So, every part of
this power supply chain has a different
player, has a different technology.
It is not like what you you can you see
in HBM. Oh, it's HBM. What is it? Like
the three same three companies. What are
they doing? Stacking the same way?
Right, it's a kind of a closed problem
in a sense.
&gt;&gt; Mhm.
&gt;&gt; Power is a wide wide open problem and
it's, you know, it is a very
wide range of topics and technologies to
look at. So, it's very very complicated
to be honest. To be it's it's not
something that's very straightforward.
And now, just like everybody on on this
the investors in the semi world and
people who are like interested now,
everybody has become an optics expert,
right?
&gt;&gt; [laughter]
&gt;&gt; Yes.
&gt;&gt; Now, now everybody knows what is like
Indian phosphide, everybody knows
there's laser shortages. Uh you know,
everybody talks about like fiber
attached units and you know, coherent
optics and you know, all of this stuff,
lane rates, it's like quite common now.
Now,
now you're going to like hear people
talk about power conversion topologies.
But it's going to be far more
challenging by the way because it's
really really a big
wide area of power conversion.
&gt;&gt; Yeah, yeah. It sounds like a lot of
opportunity, but a lot to cover. If
there's different technologies,
different materials, different companies
in the supply chain. Um oh man, if we
thought we were busy with earnings calls
already,
&gt;&gt; [laughter]
&gt;&gt; just wait.
&gt;&gt; You can have an army of people just
cover power earnings calls. I mean,
that's that's how many companies there
are. Oh, but the the technologies are
are amazing, but also they're amazingly
simple. Like ultimately, it's all about
converting between uh DC to AC or AC to
DC. All you do is like if you want to
convert from one DC to another, for
example, the simple concept you can
think of is you convert the DC to AC,
then you you use use use a transformer
with a different number of turn ratio.
So, if you use a 10:1 turn ratio, you
can bring it down by 10 the AC current
by like a factor of 10. Then you convert
that AC back into DC. Then now you've
converted it basically back, you know,
step down the DC uh by by that amount.
Then there are that's a simple one um
but it's quite widely used that
approach. Then there are like uh what
are called synchronous buck converters.
Those are basically based on square wave
waveforms, you know, that is basically
works on the principle of
having, you know, how much duty cycle
you want to have. You keep a transistor
on for some time and then you turn it
off. And then when you average it out,
you get a different average. So, if you
have it on for more time, you know, you
you get a higher average. If you keep it
on for less time, you get a lower
average. So, you can step down voltages
using those kinds of synchronous buck
converters. So, the circuit topologies
are also very fascinating, very
interesting, and the tradeoffs are
enormous. So, it's a very wide space,
and if we are entering a space of like
power limitations, we have a lot to talk
about.
&gt;&gt; Yes. Oh, man. You know, I took
a little bit of power stuff in
undergrad, and at the time, I wasn't
motivated to be excited about it. So, it
all came off as fairly boring. But, what
I liked about this episode is you helped
motivate me to be like, "Man, I got to
better understand all of this." Cuz
there is a bigger reason for getting
into the weeds here.
&gt;&gt; Yeah, yeah. And there is it's a wide
and even the topologies when we going to
800 volts is not set, by the way. Like,
there is a big discussion as to whether
you should convert from 800 volts down
to 48 volts, and then reuse all the
existing infrastructure that it already
is there at 48 volts. That's one like
way to do it.
And then the other approach is that
you why don't you convert from
800 down to 6 volts, go directly. So,
that's what like people like TI and
Navitas and all these companies doing.
They want to go directly to 6 volts. You
know, why why the 48 volts? Why? Cuz
every conversion stage you lose
efficiency. The fewer stages of
conversion, the better. So, why don't
you skip the 48 volts and go straight to
the intermediate bus voltage of 12 volts
or 6 volts. And then you do the
conversion from there, right? So,
there's like all these like battles of
like topologies and architectures that
are still going on. Nothing is set in
stone. It's a great time to look at
this, really.
&gt;&gt; Totally. Let me guess, all the 48-volt
incumbents are like, "Yeah, just go to
48-V and reuse it." And then all all the
6-V and 12-V folks are like, "No, skip
that. Come to us. We'll sell you more."
Yes, we'll make
components.
&gt;&gt; If it's a 48-V conversion, yeah, those
guys are happy. If not, they're like,
"Oh, no, what do we do now?" Like
they're skipping our voltage altogether,
you know.
&gt;&gt; Right, totally. Fascinating. Well, all
right, we should call it here. This has
been great, but it'll be fun to dive
into more and see, you know, who ends up
winning here.
&gt;&gt; Yeah, yeah. We'll leave the Substack
post that I had on there.
Uh if you want to go read it, a part of
it, at least a lot of the engineering
stuff that I mentioned is is on the free
portion of the post, so go go read it.
All right, I'm going to do the goodbye
today uh because I've already spoken
this whole episode. I might just throw
the towel in. Uh
so, thanks for listening to
Uh this has been a fun podcast for us to
run. And uh do check us out on YouTube
because we always put like pictures
where we can. And uh we are also on all
podcast platforms. If you ever want to,
you know, listen on that. Uh but also
we do have a Substack where we write
daily updates on this stuff because we
have so much news and stuff we monitor
that we try to write it over there uh so
that you have all the latest news. So,
definitely give us a follow on there as
well. Uh that's it for this episode and
catch you on the next one.
