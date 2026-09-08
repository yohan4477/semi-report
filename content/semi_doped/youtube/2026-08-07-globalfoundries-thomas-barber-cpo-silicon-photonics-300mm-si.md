---
source: https://www.youtube.com/watch?v=WVaUk7NzCZ8
vid: WVaUk7NzCZ8
title: GlobalFoundries Thomas Barber: CPO, Silicon Photonics, 300mm, SiGe, OCI, NRZ
date: 2026-08-07
duration_sec: 2373
channel: Semi Doped
kind: transcript
---
Hello everyone. Today we have a special
guest, Tom Barber, VP Communications
Infrastructure and Data Center at Global
Foundries. Hey Tom.
&gt;&gt; Morning. How are you?
&gt;&gt; Good. Good. Thanks for coming. So today
I want to talk about Global Foundries
and your photonics and optics
sort [clears throat] of background and
experience as a company. I don't think
most people think of Global Foundries
when they hear CPO or when they're
thinking about photonics. So I I thought
you'd be the perfect person to talk to
on this topic. So So let's jump in. So
you know, I think right away when I
heard Global Foundries in this space, I
thought, wait, Global Foundries does
photonics? So you know, most people
probably like me know Global Foundries
as the foundry that um was in the
running at the leading edge for a while
and then stepped back and started
focusing really on foundational nodes.
Um but what people like myself don't
know is that you actually do have a
background
in the business of moving data with
light and you have for well over a
decade. I think it traces back to the
IBM microelectronics business. So maybe
start very high level for us. Like what
does Global Foundries even do in
photonics? How far back does it go? Just
educate us.
&gt;&gt; Sure.
Yeah, and I think you know, Global
Foundries
focus is really on what we call
essential silicon, right? And that's the
foundation of all our electronic
systems, you know, including data
centers, right? It's power, it's
communications,
you know, it's memory, it's it's all the
things that are essential to making
these communications these electronic
systems work. And silicon photonics
perfectly aligns with that strategy. You
know, it's very differentiated, it's
very complex technically, and it's in a
very challenging market, right? So
there's great opportunity for to
differentiate.
Um for those people that don't know, you
know, Global Foundries, we were born out
of out of AMD. We we the AMD foundries
that were spun off.
But over time, we acquired both
Chartered Semiconductor, which had a
silicon photonics effort, and we
acquired IBM Microelectronics, which has
a long history in silicon photonics.
The effort at uh IBM Microelectronics
actually started in the mid-2000s
with, you know, doing very basic
integration of waveguides, modulators,
and photodiodes into CMOS technologies.
In the mid-2010s, so after about 10
years of effort, that turned into real
products shipping, you know, 25 gig per
lane type of products shipping in mass
volume. Um, the volumes were fairly
small at the time because it was really
only used for long-range point-to-point
communication.
But we've continued to invest, and now
we're on our third generation of
integrated silicon photonics, and that's
really what's being rolled out in mass
scale in the data centers today.
&gt;&gt; Hm, so interesting. Okay, so the history
traces back, you got AMD and
acquisitions of Chartered Semi and IBM
Microelectronics. That's super
interesting. And yeah, it sounds like
you've been in this uh
long-distance optical communication
space. So, I did not know that. Now,
what also surprised me is I'd heard
recently that GlobalFoundries claims to
be the largest pure-play silicon
photonics foundry by revenue. And again,
I think people think of um TSMC Coop, or
they think of Tower Semi. And again,
that's kind of like a shocking fact. So,
can you maybe tell us a little bit more
about like, is that true? And and tell
us a little bit more about the business.
&gt;&gt; Yeah, so that is true.
I think that's really, you know, we have
been working with key customers for a
very long time, right? And and growing
as the business grows.
Um, and that's been key to us to make
sure that we have those strategic
customers in place that are the market
leaders.
The second piece of this is we made a
very early investment in moving silicon
photonics to 300 mm foundries, right? We
put it into our facility in Malta, New
York. Um and that's been huge for us
because it has allowed us to
significantly expand our capacity. And
that's what the market's looking for as
much as anything right now is there
everybody's just desperate for more
capacity. And we are available to
provide that capacity.
As a part of that, we added the AMF team
in Singapore, which brought in a full
range of very highly differentiated
products that were actually orthogonal
to what GF was doing. GF's primary focus
was on was on short range um and data
center products, where AMF was doing a
lot of business in long range. And so,
that helped us round out our portfolio
and added a complimentary set of very
high-value products. And the combination
of the GF silicon photonics business
plus the AMF business is what made us
number one by revenue.
&gt;&gt; Ah, okay. Okay. So, there was the
short-range play and the long-range via
the acquisition. Um one interesting
thing, going back a little bit, you said
moving to 300 mm um wafers. Can you
explain that more? Like, was that coming
from 200 mm to 300 mm? And why is that
such a big deal to unlock more capacity?
&gt;&gt; Yeah. So, yes. Most silicon photonics
today is actually still produced on 200
mm wafers. That's where most of our
competitors are.
When you go to a 300 mm wafer, you know,
it's it's the radius squared, right? So,
you go up by 50% of radius, you square
that, you know, you get 2.25 times as
many die per wafer, right? So, running
the same number of wafers, you get more
than twice as many units coming through.
And that's really important as we scale,
you know, photonics
even going back 5 years was a relatively
small business, right? For two reasons.
One is, you know, there were other
alternatives in indium phosphide and EML
that were very competitive at 50 and 100
gigabits per second. Plus, you know, the
overall market was just significantly
smaller. The data center piece had not
really taken off yet. But with data
center piece taking off and 200 gigabits
per second being the node that's really
taking off, that's the optimal place for
silicon photonics, and that's why we've
seen an explosion in silicon photonics.
So, having that extra volume available
via 300 mm wafers is really helpful.
&gt;&gt; Mhm. Yes, okay. So, let's talk more
about this 200 gigabits per second and
sort of the opportunity right now um
for uh
optics and and maybe let's talk like
scale up. Um so, I know you know, early
rack scale AI systems, the switch was at
the top of the rack. You had like eight
GPUs interconnected in nodes, and they
were connected to a switch at the top of
the rack. But, um as these racks are
getting denser and we move to 200 um
gigabits per lane speed, now all of a
sudden um I think it's difficult to get
the I know the switch has moved to the
middle of the rack because it's harder
to reach from top to bottom. So, like
unpack the problem that the industry is
trying to overcome right now.
&gt;&gt; Yeah.
So, so it all comes down to the
fundamental limitation of copper, which
is range.
Right? So, at 100 gigabits per second, a
direct attached copper cable, so no
intelligence, just a dumb cable, could
span about 2 m, which is basically the
height of a rack, right? So, you could
go, you know, any connection within a
rack you could do with copper without a
problem.
When you get to 200 gigabits per second,
that range drops to about 1 m, which is
why when you look at like an NVL 72,
they moved the switches to the middle of
the rack because that's kind of as far
as they can go realistically.
When you go to 400 gigabits per second,
now the range is half a meter, and you
you you're not going to quarter the size
of the rack, right? So, you have to go
to something faster or something Yeah,
something with more range, which is
optical.
That's really kind of the the high-speed
stuff.
And that's within a rack. Now, right
now, most of the scale up networks are
within Iraq. So, an NDL 72 is one rack.
The Helios that was just announced by
AMD as a single rack.
But, you really want to go to multiple
racks. And when you go to multiple
racks, now you're talking about spanning
tens or even hundreds of meters. And
that's when you absolutely have to
switch to optical. You cannot do that
with copper. Not at the speeds we want
to do.
&gt;&gt; Mhm. Okay, so for
scale-up,
what you're saying that copper's getting
shorter and shorter, and so one way to
move forward is to just try to move
closer and closer to the GPUs, but
ultimately that's going to run out of
steam. So, even within the rack, you
might need
optics. But, then of course, the
question is why stop with one rack? Why
not have a scale-up domain that could
stretch into neighboring racks or or
four racks side by side? And so, of
course, that it was about like
shrinking, but then it's about expanding
as well. And And you're saying that only
optics can pull that off.
&gt;&gt; Yeah, if you If you look at what Google
has done and even what Huawei has done
with their scale-up networks, they've
gone beyond a single rack. So, instead
of being limited to, you know, 72 or 144
GPUs, depending how you you count them,
you know, they're doing 300, 500, 1,000
GPUs across, you know, six, eight, 10
racks. Right? So, they're really
expanding the size of their scale-up
networks using optical communication to
span multiple racks.
&gt;&gt; Got you. Okay, so then walk me through.
Are we talking about like
pluggables for the optics or NPO or CPO?
And And where does GlobalFoundries come
in?
&gt;&gt; Right.
So,
it can be any of those options.
What we see is a trend to
from pluggables
first going toward NPO and then toward
CPO.
And the reason is really cost and power
and density.
So, when you're at the edge of the rack
with a pluggable, you're looking at
about 35 dB of loss
from the edge of the rack to the GPU or
switch ASIC in the middle of the server.
Right? That loss has to be compensated
for by a, you know,
kind of expensive and pretty power
hungry
uh DSP in the pluggable.
When you move to an NPO system,
now you've dropped your loss from about
35 dB to somewhere between 15 and 20 dB.
Right? That allows you to significantly
reduce the amount of compensation you
need to do on the electrical side, even
eliminate it. Right? So, if you have
enough link budget end to end that you
can handle the extra, you know, 15 dB of
loss on either end due to the transition
from the NPO to the core processor,
then you can get away with not having a
retimer in the NPO, which is what most
people are doing. They're doing what's
called linear.
And so, that removes that DSP from the
system, which saves a lot of cost and it
saves a lot of power.
But, you still have a fairly bulky
package
um for this NPO.
And what you want to do, and you still
have a lot of loss in the system, right?
There's still 15 dB of loss that needs
to be compensated for.
If you continue to co-package optics,
and you move that transition from
electrical to optical into the package,
now you've dropped your loss from, you
know, 15 dB down to like 6 dB.
And [clears throat] that really helps
you both from the link budget,
obviously, cuz you've gotten yourself an
extra 20 dB, but that also allows you to
lower the power of your serdes
significantly. Right? So, what we're
trying to do is we're trying to minimize
the number of picojoules per bit that
you need for the communication.
So, in our pluggable, you're talking
about, you know, a fully retimed
pluggable is somewhere around 20 to 25
picojoules per bit.
When you go to NPO, you can go to linear
and get rid of the DSP, which does a
lot. It gets you down to maybe 10
picojoules per bit, but you still have a
pretty powerful serdes to overcome that
15 dB of loss between the co-processor,
core processor, and the
uh NPO. When you go onto the package
with the GPU or the or the ASIC, now
you're talking about 3 dB of loss, and
now you can go to the lowest power
serdes, which allows you to get down to
less than 5 pJ/bit.
Now, that's really critical because all
of these systems are thermally limited.
So, every picojoule of power that goes
into the communications is one you can't
use for compute.
So, what you want to do is minimize the
amount of power that you use for the
com- for the communications between the
GPUs, so you can run the GPUs as fast as
possible.
&gt;&gt; Mhm. Sure. Okay. So,
if we orient around power, the goal is
to in a gif- given a fixed power budget
in this data center, it's only got 50 MW
or 100 MW, whatever, we want to use as
much power as possible for compute and
as little as power as possible for
communication, sending data around. Now,
talk us through again why, kind of
zooming back out, um you talked about
pluggables,
why do they have so much loss in them?
You talked about they have a DSP, but
like where does the loss come from? Cuz
I think people
it it's not in the optics, right? It's
like the electrical trace?
&gt;&gt; Yeah, it it what it is it's it's the
it's the electrical traces through the
PCBs from the core processor, you know,
couple hundred centimeters
to the edge of the server.
Right? And so, those are very thin
wires, um and when you're talking about,
you know, a 200 gigabit per second PAM4
signal has about 55 GHz of bandwidth.
Right? So, you're trying to run a 55 GHz
signal through a very long trace on a
PCB, and you end up with a lot of loss.
&gt;&gt; Mhm.
So, then
a step in the right direction, uh
NPO, near pluggable optics, you're
ultimately shortening that trace. And
then finally, co-packaged optics, maybe
you're getting rid of it entirely. But
can you walk us
Can you walk us through the trade-offs
of, you know, why doesn't why doesn't
every I know people are talking about
using NPO as a stepping stone to CPO.
So, can you talk us through like why not
just jump to CPO if it's the most power
efficient?
&gt;&gt; Right.
So,
the concern
with moving away from pluggables is
reliability.
Right. So, right now, optical
communications in general is seen as a
reliability risk.
And so, the data center customers are
very comfortable with it being
pluggables because if something goes
wrong, they just swap the pluggable,
right? Just take one out, put a new one
in, and and move on.
They don't always do root cause to
ensure that the pluggable is really the
problem, but if you swap out the
pluggable and the problem goes away,
then you're fine, you keep going.
Moving to near packaged optics is a half
step in the right direction. Those
solutions will probably be socketed, so
they'll still be relatively easy to
maintain. You'll still have to open
You'll have to open the server and and
swap it out physically, but it's still
something that can be swapped in place
without completely replacing the GPU.
When you go to co-packaged optics, now
you're talking about something that is
permanently attached inside the package
of the GPU. So, the reliability has to
be extremely high.
So, data center customers, Meta in
particular, are going through the effort
to validate the reliability of those
solutions right now. And Meta's released
a couple versions of a study that
they've had running for a long time
with,
you know, 50,000, I think it is, GPUs in
a network using co-packaged optics. And
what they found is the reliability is
actually higher than it is with
pluggables. And they found no link flap,
which is the primary cause of concern in
optical communications
across their entire testing range, which
I think is up to 50 million hours or
something like that right now. So, you
know, they're they're doing the work and
becoming more and comfortable with the
reliability, but they're not going to
deploy it at scale until they're
absolutely certain that it's a reliable
solution.
&gt;&gt; Fascinating. So, tell us why why do why
are people expecting that the
reliability is not great for CPO and
then
finding out from Meta like, oh, actually
it's not as bad as you think. I mean, is
this about like is the laser is it a
external laser and the concern was that
the laser is sitting near a hot chip,
but that's not a problem or or what is
the problem that people think should be
happening and then maybe it's overblown?
&gt;&gt; I think it's problems that are actually
happening today
because
you know, and again, there's not great
Meta has actually done some good work on
this in Recon's, but you know, the
things that end up causing problems in
optics, some of them are actually due to
the fact that it's pluggable. Right?
Because you're plugging it in, there's
the opportunity for dust to get in the
connector and block the optical signal.
Right? So, when you're swapping out a
pluggable, if dust gets in there, all of
a sudden you have a reliability issue,
right? And it's attributed to the
pluggable, but it's not the inside case
of the pluggable that's the problem,
really. It's the fact that the
pluggable, you know, there's something
interfering between the pluggable and
the
and the connector. So, when you go to
CPO and you have a fully integrated
solution, you know, that's done in a
clean room facility, right? There's no
dust there. Right? When you have things
that are permanently attached or
semi-permanently attached, you know,
you're not dealing with these connection
issues that you get uh where where
reliability concerns appear. So,
that's what the hyperscalers are really
trying to become more comfortable with
is not that CPO will be as reliable as
pluggables. That's not good enough. CPO
has to be way more reliable than
pluggables. So, I don't think anybody
questions that CPO's as good as
pluggables. The question is, is it so
much better than pluggables that it can
be made a permanent part of the system?
&gt;&gt; Gotcha. Sure, fascinating. So, it's
almost it how surprising if the idea was
like, oh yeah,
pluggable is like the release valve
where if there's a problem, you can
unplug it and put something else in.
But, actually, what if the problem is
the pluggable that the act of plugging
it in itself? It's kind of funny. So,
yes, if you can make something
co-package in a clean room facility,
maybe dust never gets in and you
actually don't see those issues. That's
really fascinating. So, then, um what
about like
cost? I mean, everything has a
trade-off. So, if if CPO potentially has
great reliability and um it's much lower
um from an energy cost, what about like
dollars and cents? Is it Is it more
complicated? Is it expensive or does it
Is it all a wash compared to like linear
or or traditional pluggables?
&gt;&gt; Yeah, and again, it's it comes down to
If you look at a pluggable,
you strip away a lot of the components
of the pluggable when you go to
co-package optics, right? You obviously
don't need the case anymore, right? That
disappears immediately.
There's a lot of support circuitry on
there, um some MCUs, some power, um and
in particular, especially the DSP that
goes away, right? So, the DSP is
probably the biggest component that goes
away uh from a cost standpoint.
So, that saves you a lot of cost. Um and
then, you get into the operating costs,
and when you have significantly lower
power, that obviously translates
directly to operating cost.
&gt;&gt; Mhm. Mhm.
Interesting. Okay, so, um
let's move on a little bit. So, I saw
some news about uh
the OCIMSA,
like a multi-source agreement for
optical interconnects. So, can you
enlighten us, like, what is an MSA? What
is this and why does the industry write
one? I think that some of the names
involved AMD, Broadcom, Nvidia, Meta,
Microsoft, OpenAI. So, like all
It seems like everyone is a part of
this. Um why is this necessary?
&gt;&gt; Yeah.
So, an MSA is a multi-source agreement.
And what it is effectively is the
industry looking at a standard,
typically a standard from the IEEE, and
saying, "Okay, this is great, but
there's a lot in here that maybe is
options. And what we're going to do is
we're all going to agree on here's the
options we're going to do, here's the
options we're not going to do, here's
how we're going to test things, here's
how we're going to make sure it's
interoperable.
You know, so that is is what an MSA is.
The one that's it's not called an MSA,
but honestly the most famous MSA is the
Wi-Fi Alliance. So, the Wi-Fi Alliance
takes the Wi-Fi spec from IEEE and turns
it into something that can be
productized, right?
The optical industry has typically at
MSAs focused primarily around
mechanical.
So, if you look at the you know, there's
one for it's called OFSP. That's the
form factor for the pluggable. So, it
defines the mechanical electrical
interfaces so that when you plug these
things in, they all work, right? The
electrical interface is defined by OIF.
And the the optical interface is defined
by IEEE, but the MSA kind of brings all
those things together and says, "Okay,
how's here's how we're going to combine
these pieces and wrap them up
mechanically such that we have a
interoperable pluggable."
And the OCI MSA is a little bit
different in that it's actually taking
and defining the optical interface,
right? So, that for most the optical
communications used in data centers is
defined by IEEE. IEEE 803 802.3.
That is not sufficient for what we want
to do for scale-up compute, right? And
OCI is really focused on scale-up
compute. And so, when you look at the
participants,
the founders of OCI,
they are the key suppliers in the data
center industry. They know
absolutely
what is the best solution for scale-up
networking, right? And so, they've come
together and said, "Hey, listen, the
specs
the optical specs that the IEEE is
defining are not really fit for purpose
for the scale-up application.
This is what we believe is fit for
purpose for the scale-up application.
This is how we think you should do
things. And it's really focused around
maybe not going as far range-wise cuz,
you know, 2 km maybe is a little too far
for for a scale-up network. So, we're
going to back off on that a little bit,
and we're going to go to a wide, slow
solution. And what that is is
you know, the to go as fast as possible
with as much data as possible over a
single fiber, IEEE has moved to
multi-level modulation. So, it's called
PAM4, and, you know, you transmit two
bits per symbol, and you have four
levels.
And the issue is those levels are pretty
close together, so you have to either
have a lot of power or very low noise to
receive them properly.
What they've done with OCI is they've
gone back and said, "We're going to go
back to a binary system,
so only one bit per symbol, and we're
going to slow it down to 50 GHz.
But, we're going to do four wavelengths
per fiber.
So, we're going to take advantage of the
fact that you can put multiple channels
on a single fiber to still have that 200
Gbit/s of bandwidth.
We're just going to do it in the four
wavelengths.
And what that does is it makes the
receiver a lot less complex, so the
amount of channel equalization you need
goes down quite a bit,
and the amount of forward error
correction you need to goes down by
quite a bit.
The native bit error rate for NRZ 50 GHz
is about a million times less than what
it is for PAM4.
&gt;&gt; Oh, wow.
&gt;&gt; It's significantly easier to receive an
NRZ signal. And that translates into
reduced costs, and it translates into
reduced power.
&gt;&gt; Oh, fascinating. Okay, so the industry
is coming together saying we're going to
make an interoperable standard, and
presumably that's just so that
there can be competition so that
everyone can say, "Hey, we're building
to this spec collectively."
Um and then
what I heard you say, which is
fascinating, is it sounds like the
industry is aligning around not just
trying to continue to increase the per
lane speed and double it, double it
again, but actually to like walk back a
little bit instead of PAM 4, go back to
NRZ, and say, "Hey, let's go back to 50
um gigabits per second uh NRZ, but can
we send four um like wavelengths down
the same fiber, kind of four colors, if
you will?" And those are being sent
simultaneously?
&gt;&gt; Correct. Yes.
&gt;&gt; Inter- interesting. So,
if there's more
if there's different wavelengths being
sent simultaneously, is that like a boon
for like people that make the lasers? Do
you need more lasers to to do that?
&gt;&gt; So, so just back up one second. Just to
explain something about the difference
between the the scale up application and
scale out application. So, the scale up
application, what you're trying to do is
you're trying to connect as many GPUs as
you can
using a single hop network.
Right? And so, if you look at the
maximum size switch you get today is a
100 terabits per second.
And so, with 200 gigabits per second per
fiber, you can connect 512 GPUs to each
switch.
Right? And then what you do is you stack
up switches to give you the most
bandwidth. So, if you look at the NBL-72
system, they have 18 switches in
parallel, which allows them to get to
that 7.2 terabits per second
bandwidth they have per GPU. But each
fiber is only or in this case, they use
copper, each copper pair is only 200
gigabits per second. It's just shared
over 18
18 uh switches. The other thing that the
OCI team has done really well is so when
you look at the amount of lasers you
need, it's not as simple as one laser
per wavelength because the laser power
can actually be split and used by
multiple fibers.
Right? So, if I have a transceiver
that's got eight fibers connected to it,
um I typically right now the ratio is
four to one, so I'd have two lasers to
drive those eight fibers.
But for pluggables, it's actually moving
to eight to one. So, you'd only have one
laser driving all all eight of those
fibers.
With the OCI spec, they've backed that
off even further to you can get to as
extreme as 32 fibers per laser.
So, one laser could drive 32 fibers. So,
you could get a full optical engine
solution with the eight wavelengths of
light that's needed for OCI with just
eight lasers.
&gt;&gt; Got you. Okay. And then you were saying
that we don't need to think about like
one laser per port or anything like
that. In fact, the laser the light can
drive
many different fibers. Maybe it is up to
as many as 32.
&gt;&gt; Correct.
&gt;&gt; In like the most extreme case. That's
pretty cool.
Um okay, so now
tell about where does GlobalFoundries
come in here? I know you guys announced
scale and you called it the first OCI
capable platform. So, tying back to that
MSA, can you explain a little bit more
about scale and you know, how you're the
first OCI capable platform?
&gt;&gt; Sure.
So, what we're doing with scale is we're
putting together everything you need to
do the electrical to optical translation
in a known good form factor, right? And
call it a chiplet, call it a module,
whatever, right? And so, what that
includes is it includes an electronic IC
which is going to be used to communicate
to the CPU or the GPU or the the the AI
ASIC.
And then that electronic IC electronic
IC sits on top of a photonic IC which
does the translation between electronic
and photonic signals.
The photonics IC has a detachable
connector on there.
And that detachable connector is key
because when you're assembling a CPU,
what you don't want to have to do is
have a fiber dongle hanging off your
your photonic IC at all times. You want
to create, you know, you want to build
your server using rectangles, right? And
then plug everything in at the end. And
so with that detachable fiber connector,
it looks very much like copper where you
build all your PCBs, put them all
together, and then you have a wiring
harness, this case of
optical wiring harness instead of
electrical wiring harness, that you
connect at the end that bridges from
those CPO modules connected to the GPU
to the edge of the server.
&gt;&gt; Mhm. And Global Foundries, you you can
fabricate
Which of those pieces do you guys
fabricate and assemble?
&gt;&gt; Yeah. So, we have the ability to
manufacture all of it. Um the photonic
IC for sure we do 100% of the
manufacturing. Um we have a number of
different design partners working with
us on photonic IC designs.
The electronic IC, it really depends on
the complexity of the design,
particularly digital. So, if it's a less
complex design, we can use our FinFET
process or one of our FDX processes. If
it's a simple, you know, linear
translation, we can actually use our
silicon germanium process even. Um if
it's a more complex digital translation
and a customer wants to use an advanced
node like a 3 nanometer or 2 nanometer
node, then they're free to do that and
and we'll bring that wafer in and do the
assembly and test.
The micro optics, um again, are are
manufactured externally, but we do the
assembly and test on that. And so, what
we deliver at the end of the day is a
known good, fully tested module with
very high reliability.
&gt;&gt; Mhm.
Okay, fascinating. So, then talk to us
more about like position yourself
against what some other people are
doing. Like I know TSMC is in this space
with Coop and they use a grating coupler
and I think Global Foundries uses a
different technology and edge coupler.
And could you maybe explain a little bit
more about the technology and
differentiation that and the approach
you're taking?
&gt;&gt; Right. So we do so yes, the mechanism
for the light getting into the wave
guides
is very similar to edge coupling
but we use we don't do it at the edge of
the die. We actually have a micro mirror
that we implant into the wafer so the
light can still come in vertically.
Right? So the light comes in vertically
exactly the same as you would with a
grating coupler. We just have a mirror
and that reflects the light horizontally
into the wave guides on the photonic IC.
The reason we went with that approach
instead of grating couplers is because
grating couplers inherently have limited
bandwidth. Um and so you can't service
the entire O band with a single
solution. With a micro mirror we can do
the entire O band which gives us the
maximum flexibility as far as doing the
wavelength planning. Right? So so OCI
today is is four wavelengths in each
direction.
You know, one of the ways we're going to
scale that to do higher bandwidth is to
add more wavelengths. And so as we're
thinking about how do we evolve into the
future, we wanted to make sure that we
made the entire O band available to use
for as many wavelengths as possible.
&gt;&gt; Ah, fascinating. And for listeners who
might not know, can you define like what
is O band mean?
&gt;&gt; Uh yeah. So the O band is you know, you
think about AM FM bands for your radio.
So O band is an optical band. It's
around 1310 nanometers
which I can't divide by the speed of
light in my head to figure out how many
gigahertz it is but or terahertz's but
it's really really fast.
&gt;&gt; [snorts]
&gt;&gt; Gotcha. Okay, thanks. That's helpful.
All right. So then Okay, so you guys are
taking a different approach and you
think you know, it keeps the whole O
band on the table which will be helpful
in the future as you're trying to
increase bandwidth, it will keep more
wavelengths sort of at your disposal. Um
at the end of the day, you know, I see
people online and they'll say, you know,
oh, this one company's better than the
other. Um but it feels like a little bit
sort of like armchair quarterbacking.
Like Like can you help us understand as
people interested in the space like How
How do we know as a non-engineer, uh you
know, non-silicon photonics engineer,
how do we know how good, you know,
GlobalFoundries components are?
Is there like a good proxy or a good way
to understand? Is it just like looking
at the customers or what do you think?
&gt;&gt; Yeah, I mean, that's the, you know, the
the market doesn't lie, right? So the
market will choose the best solution,
right? And so that's, you know, we're at
the very beginning of this market. Um
and like I say, right now, you know,
TSMC, other foundries, they're not the
enemy to me, right? The enemy to me
right now is copper. I'm trying to beat
copper.
Right? If If TSMC wins and we win,
that's great because we're both
displacing copper. And until all the
copper is gone,
there's plenty of market to go around.
So um
but from a standpoint, yeah, how do How
are you, you know, how are you going to
tell from the outside?
You know, you will you will see
customers adopt certain solutions and
and that's going to tell you who's who's
got the best solution.
&gt;&gt; Got you. That's helpful. Um so then also
one other thing I think I saw in a press
release somewhere um about Scale mention
of known good die testability. Can Can
you explain that a little bit more for
listeners?
&gt;&gt; Yeah, and known good die is probably
under calling it. And I mentioned
earlier, it's known good very, very high
reliability die.
&gt;&gt; Mhm.
&gt;&gt; So with known good die, what we're doing
is making sure that what we deliver to
our customers is
100% functional,
right? And that's a very complex process
because we're looking at a solution that
has electrical signals on the bottom, so
you can connect it to the substrate or
the interposer, and the optical signal
coming in from the top. So, normal
electronic test is only one-sided. You
you you know, you drop your probe pads
on and you test things and you pull it
off. We've got to do a two-sided test,
right? We've got to take light in from
the top. We've got to put electrical
signals in from the bottom. We have to
test at high speed cuz we're talking
about signals at 200 GHz
coming in, and we've got to test a lot
of channels cuz these optical engines,
you know, a normal
uh pluggable transceiver right now maxes
out at 1.6 terabits per second. These
optical engines are going to be 7.2,
14.4, even higher, right? So, we're
talking about a lot of bandwidth that
has to be done in parallel. So, we put a
huge effort into, you know, building
test systems that A can connect top and
bottom, and B have enough bandwidth to
do this full testing.
And so, we'll deliver that known good
optical engine to to the GPU provider or
the ASIC provider, and they'll integrate
that onto into their package very very
similar to how they would do an HBM
today or an I/O die today, right? That's
And then and that testing gets you to
you know, time zero reliability, right?
Time zero yield.
But, now you have to have reliability,
right? You need this to survive in a
very very extreme environment for a very
long time,
right? You can't fail in the field. You
can have zero failures, right? So,
beyond just the kind of time zero
testing and make sure it works, you
know, the first time you plug it in, we
need to make sure that it works for 10
years plus under very extreme
circumstances, right? And that
reliability testing is actually key to
success long-term.
&gt;&gt; Nice. That makes sense. Interesting. So,
when I'm zooming out and I'm thinking
about, you know, the technology you have
and the ability to offer the PIC, the
photonic IC, and the um electronic IC or
package that in from someone else and do
all the coupling um and then of course
we're talking about scale up where this
feels like it's going to be a very large
tan because
just there's your have the opportunity
to connect lots and lots of GPUs so
there could be lots of optical engines
lots of fibers
big opportunity there like what are you
guys saying publicly about how big you
think this market is and and how much
opportunity there is for GlobalFoundries
with CPO?
&gt;&gt; Yeah I mean if you look at the scale up
bandwidth compared to scale out right
the scale up bandwidth is somewhere
between five and 10 times what scale out
is
right and the scale up today is all
copper
so if we can convince everybody to move
their scale up networks from copper to
optical you know we're sort of instantly
talking about increasing the size of the
market by 5x or 10x
right that's why I say the enemy is
copper it's not other foundries right we
want we want to enable that conversion
we want to work with other people we
want to partner everything we can to
convince the market to move from copper
to optical for scale up you know and and
because it's the right solution right so
that's
that opens up a huge potential market so
if you look at I can't remember what the
latest projections were from from
LightCounting or Signaling AI but you
know tens or or close to 100 billion in
in optical you know think of that market
going 5x 10x bandwidth now it's not
going to make the market go 5x or 10x
because like I said the the CPO
solutions have to be much more cost
effective
than what you're looking at for
pluggables but you know doubling easy 4x
maybe and then pile on top of that you
know the bandwidth continues to increase
you know the number of servers continues
to increase so you know it's it's a very
high growth market for a for a while
&gt;&gt; Mhm.
That's promising that's exciting. Um
okay one other topic You mentioned
silicon germanium in passing and I I
think [snorts] I saw in your most
not today's earnings call, but the most
recent one before that, a quarter ago,
um mentioned of silicon germanium
capacity in Vermont being over
subscribed. And anytime I hear something
over subscribed, you know, my ears kind
of perk up. So, can you tell us like
what is the silicon germanium used for
and like yeah, enlighten us a little
bit. And why is it in such demand?
&gt;&gt; Right. So, when we're looking at optical
transceivers today, there's two
components that are used to
locally on the pluggable or even between
the pluggable and the GPU to amplify the
signal coming into or going out of the
the photonics, right? One is the driver,
which is a it's a modulator driver, so
it it amplifies the signal coming out of
the DSP, such that you can drive the
modulator, that's the silicon photonics
modulator on the PIC.
That to some degree is being integrated
into the into the DSP, so the market's
shrinking a little bit on that. The
other one is a transimpedance amplifier.
So, that takes the current out of the
photodiode, which detects the incoming
light and translates it into a voltage,
which is then converted and processed on
the DSP.
The bandwidth of those is similar to
what I talked about earlier with the
PCB. You know, for a 200 gigabit per
second PAM4 signal, you're talking about
55 GHz of bandwidth if you've got a
retime system and closer to 70 GHz of
bandwidth if you're trying to do a
linear system.
Typically, for an amplifier, you need
about the transistor speed needs to be
5x what your bandwidth is. Right? So,
now you're talking about transistors
that need to run 350, 400 GHz
to do the 200 gig per lane. When you
talk about 400 gig per lane, now you're
talking about doubling that, right? So,
you're talking about transistors that
are 600, 700 GHz.
Very, very few companies can do that at
scale and reliably. And silicon
germanium from GF is one of those few
technologies, right? So, we have you
know, very, very good silicon germanium
technology. Our our transistor speeds
are extremely high, much higher, you
know, higher actually than what you need
for 200 gig per lane. And we have new
generations, you know, road maps that
support 400 gig per lane very quickly.
So, you know, we've been fortunate that
we've gotten a lot of adoption on 400
gig per lane. So, as you see the 1.6 T
transceivers volume increasing, you
know, we're getting a disproportionate
share of that right now.
&gt;&gt; Mhm. Okay, interesting. So, silicon
germanium is about transistor switching
speed. And as we see switching speeds uh
or bandwidths of like 200 gig, 400 gig,
it means we should think silicon
germanium and we should think
GlobalFoundries.
&gt;&gt; Yes.
&gt;&gt; Fascinating. Awesome. All right, Tom,
we've covered a ton of ground. It was
pretty technical, but I appreciate you
walking us through and teaching us and
enlightening us also about
GlobalFoundries um from a business
perspective. So, thanks so much for your
time.
&gt;&gt; Thank you, Austin. It was great talking
to you. I appreciate the time.
