---
source: https://www.youtube.com/watch?v=Ywh2BHKjeHM
vid: Ywh2BHKjeHM
title: PicoJool's Al Yuen: The Case for GaAs VCSELs in Scale-Up Interconnects
date: 2026-07-16
duration_sec: 2961
channel: Semi Doped
kind: transcript
---
[music]
&gt;&gt; Hello everyone. Today we have a special
guest, Al Yuan, CEO of Picogiga.
Picogiga is an optical connectivity
company and we'll get into all the
interesting details. Um, but first I
wanted to introduce you guys to uh Al.
So Al, tell us about you and your
background. I know you've been in the
industry for a long time.
&gt;&gt; Yes. So after grad school at UC Santa
Barbara, where a lot of the photonics
folks uh
have originated, um I went into HP, HP
Labs, where we focused on uh photonics
research, etc. And since then, uh around
'99, I left HP and started my first
company called Alvesta and we created
the world's first uh 10 gigabit
Ethernet. At the time, 10 gigabit, which
is 10 billion bits per second, um we
were actually trying to figure out
applications that how people would use
this in '99. Uh we would make up things
like people wanted to stream video
someday in all the rooms in their house.
Uh and so we had to actually uh but
today, of course, we're doing 1600
gigabit or 1.6 terabits. So since then,
I've gone to various companies. Uh I ran
a division for Coherent. And then uh
started some other solar companies and
clean tech and then finally ended up at
Lumentum in my last gig. And then about
2 years ago, uh through Playground
Global, which is our funder, uh we
started Picogiga and uh so far uh so
good. And uh what we're what we're doing
right now is basically in the
interconnect space and we'll talk more
about that today.
&gt;&gt; Awesome. Wow. Uh what a great
background. I love Yeah, that you guys
invented uh early 10 gigabit Ethernet
and then had to create ideas to sell
people to convince people that like yes,
this is useful. Uh yeah, people will
want to use it. That's awesome. Now,
remind me, you also um helped invent the
active optical cable.
Is that right?
&gt;&gt; Sure, yeah. So, very interesting story.
So, back in Alvesta, our first, uh, my
first startup,
uh, again, another small startup at the
time called Mellanox, which of course
now is inside Nvidia and created this
whole,
uh, kind of hyperscale and, uh, you
know, the the whole InfiniBand, etc. So,
they approached us. So, they had these
very bulky copper cables, even back
then, right? So, 20, 25 years ago.
And they said, "You know what? The
copper cables are very bulky. They could
only reach, you know, at that time, tens
of meters. Now, it's even shorter. But,
they said, 'We would like an optical
option, but we don't really want to
commit to a full kind of optical
solution. So, could you put the optics
inside the connector?'" And we said,
"Why not?" right? So, basically, we took
that same,
uh, transceiver that's typically on a
board, and we literally embedded it
right into the connectors, you see here.
And then we thought, "Well, that's kind
of, you know, not very, uh,
efficient and clean." And so, we
embedded that whole connector inside.
So, the optics, uh, went inside the
connector, and then this is the world's
first demo of an active optical cable,
meaning electrical to electrical. So,
electrical comes in, electrical goes
out, but inside the electrical to
optical transition. So, electrons come
in, photons carry the information, and
then electrons uh, go back to the, uh,
to the point B. So, that's how the whole
active optical cable concept came
through Mellanox. And then, since then,
for the last 25 years, the AOC, uh, has
been the standard workhorse in many,
many data centers today.
&gt;&gt; Amazing. So, having invented that and
then watched it sort of become, uh, just
widely adopted and probably produced,
you know, I don't know, in the millions
of cables or something. Um, how how has
that impacted the way you think about
like what's possible as an entrepreneur
and in this space?
&gt;&gt; I like to think of ourselves more, um,
as engineers, right? So, there's
difference between, I would say,
scientists or researchers or what people
call R&amp;D, right? Research and
development and engineering or product
development. And so,
I always kind of tell people I'm more of
an engineer. And engineers solve
problems and they want to basically
create products that are that kind of
basically meet specifications, right?
So, if you need a Prius, you certainly
don't design a Ferrari, for example,
right? So, that's a little bit overkill.
And and so, therefore, the product fits
the need, the spec, cost, reliability,
uh, in our case, reach or the number of
amount of power, etc. So, in answering
your question,
I feel like what we do is really look at
trying to solve the specific problem.
And today, right now, copper has shrunk
to about 3 m, 4 m reach at 200 gigabits
per, uh, second per lane. And therefore,
they can't get the information off each
rack, right? So, racks and racks of
these GPUs, CPUs, lots of compute power.
So, these racks are getting very hot
because they're packing more and more
GPUs per rack because they can't exit
the rack. And so, to exit the rack, you
need an optical solution. And so,
there's many technologies and of course,
Vixels-based
active optical cable is one of them and
that's what we're basically focused on,
solving this problem of low-cost, highly
reliable, again, going way back to our
roots, which is replacing a copper cable
with an active optical cable. So, the
problem really hasn't changed. It's just
that the speed and the aggregate
bandwidth is now 1,600 times more than
the old 1 gigabit Ethernet. So,
it's exciting. It's been a long journey,
but we're still at it and we see a you
know, a long future for Vixel based
technology as we go forward.
&gt;&gt; Nice. Nice. Okay, so you have this
history as thinking like an engineer of
just like what is the problem that's
right ahead of us in the industry and
not saying like we need to invent new
physics, but just like how can we be
thoughtful about you know, oh same cable
form factor for example in the AOC case,
electrons in electrons out, but we could
use optics here and could we put the
transceiver, you know, on the end of the
cable. So, you know, thinking very
pragmatically. And now, you know, fast
forward 25 years or so and I guess in
2024 you started Pico Jewel and it and
it sounds like you're
going to tackle the problem of again of
communicating lots of information this
time it's you know, GPUs that are
talking to each other like rack to rack
where
it's such high bandwidth copper is
shrinking to to 3 m or so and so you
guys again are thinking about how do we
use essentially active optical cables,
but this time with Vixels. So, tell us
like
why Vixels and what about the problem
made you want to start Pico Jewel to
actually start a company and like get
get in the game here?
&gt;&gt; Great question. So,
Vixels for one thing has been around
since '96, right? So, it's a technology
that's been in product in the field in
data centers since 1996 starting with
the first gigabit Ethernet. So, you
know, I'm more of a historian today.
So,
&gt;&gt; [laughter]
&gt;&gt; here's a 1 gigabit Ethernet that you
know, HP created and at the time
Honeywell etc. Very very early companies
that that did 1 gigabit. And so, from
the 1 gigabit all the way to today,
again 1,600 gigabit or what they call
1.6 terabits has all been fixed or
based. And going back to what I was
saying, the practicality of these
solutions has to meet capacity, demand,
cost, all of those, right? You need to
check all those lists. If you're trying
to get into a hyperscaler today, you
need to basically meet all that
checklist. You can't say, "Oh, I meet
everything, but you know, it's three
times the cost of your per target." Or
everything is great, but you know, I
can't get the reach. So, they want all
of that met. And so, right now, the only
thing is copper, right? And that's
mainly driven because of the cost. Cost
for copper, of course, is very, very
minimal. Even active copper, where you
have some signal integrity, signal
processing, etc., built in, like an AEC,
active electrical copper,
the cost is still quite minimal compared
to other technologies that are more
elegant, longer reach, etc.
So, getting back to your question,
what's very important in a data center,
if you have different fiber optic
communication. I think everybody hears
it and goes, "Oh, isn't that the over
the ocean, they have these transatlantic
subsea type of cables?" And said,
"Absolutely." And so, there's many
different flavors of optical
communication. So, when you say that, it
doesn't cover all of them, right? So,
it's a very big umbrella, and what we're
talking about today for
data centers is a very short reach.
Today, they call it scale up. So, it's
basically a row, typically 25 30 m,
right? Or in English terms, 75 ft, okay?
So, so, it's a very short, you know,
within your house, basically from one
end to the other end,
for potentially even shorter. So, in
that very short reach,
what happens in communication is the
shorter the reach, typically the higher
the volume, right? So, if you think of
it it is, you have a lot in the data
center where you're trying to connect
all of these different GPUs, CPUs, or
ASICs together. And so, there's millions
of interconnections, miles of fiber
inside a data center, which may be, you
know, a football field length today.
But, when you leave that data center,
and you go off to between cities,
between buildings, between countries,
you have fewer fiber, but you need
longer distance. So, getting back to the
data center now, and long kind of answer
to your question is, you have to have
millions per month capacity to meet the
volume demand. So, that's one of the
boxes, right? You got to check off all
the boxes. So, if you're able to
demonstrate one or two racks, or go to a
show and demonstrate this technology,
again, technology, science, R&amp;D shows
the capability. Let's call it a
demonstration. But, in order to ship in
volume, millions per month, you need
this whole ecosystem. You need people
who
make the connector, you need people who
make the transceiver, you need people
who make the sockets, right? So,
everything has to be millions per month,
and any one of those
bill of material parts that go into
these transceivers, if it's missing,
then you can't really ship in millions
per month. And that's what's happening
with a lot of these new technologies
that are fantastic, by the way, right?
From a demonstration, from a capability
going into the future. But, Vixels
domination is that the last 25 years
we've been shipping in the millions per
month. So, therefore, there is no
invention of a technology or capacity or
foundries in order to build these up. We
already have that. So, now we design the
latest Vixel. So, today it's 200
gigabit, which we just announced. And
then we put it into the whole ecosystem,
and they package together, and then
voila, we can build millions per month
without waiting for machines to be, or
actually even buildings to be built up,
and then new machines, and then new
process to develop. All All that has has
existed for the last 25 years to to get
service this very short reach data
center application.
&gt;&gt; Mhm. Mhm. Okay. So, yeah, let me reflect
it back to you. So, the the problem that
you're trying to solve is scale up with
optical interconnects. Um and but the
key insight that that you have kind of
with your pragmatic hat on is how can we
use
uh technology and a supply chain that
already exists and can already ship
millions of cables, components, parts
per month. And so, that's one reason why
Vixels is so attractive is because
they're not a new technology. The supply
chain is not new. So, even though as we
hear about all these other interesting
things get the cuz I think anyone paying
attention, you know, listens and they
say, "Oh, you know, the Broadcoms or
Coherents or Lumentums." I hear about um
silicon photonics. I hear about EMLs.
You know, I hear people talk about micro
LEDs. But you're saying like, "Hey,
don't rule out Vixels even though
they're not new, they're still there's
there's advantages to Vixels." But tell
us like, if if Vixels have been around
for so long, like why aren't other folks
trying to take Vixels to the 200 gig per
lane * 8 lanes 1.6T and beyond?
&gt;&gt; Yeah, so like you said, there's multiple
technologies, silicon photonics, EML,
uh even this micro LEDs right that are
coming. All vying for this 200 gigabit
type of electrical signal coming in. So,
from the ASIC, GPU, CPU, you have 200 G
per lane of electrical signal, right,
that's coming in. Now, when you go to
the electrical to photonic or E to O
type of transition, then it can go to
different lanes through, again, a
different IC that may be a gearbox, they
call it. And so, you don't necessarily
have to run at 200 G for uh straight
through, which we can, right? So, that's
the most elegant cuz if you can go
straight through without having to go
through it a intermediary gearbox, then
it saves power, cost, and then latency,
which is the delay going through there.
So, 200 gigabit would be ideal. But,
what's changed in hyperscale is
different from Ethernet. So, Ethernet
information is sent in what we call
packets. So, whatever information, oh,
where should I go in Italy? I'm going on
vacation, da da da. So, that information
is divvied up by the your search engine
and sent in packets. And then that's
comes back to you. And we're not very
cognizant if there's an error drop or
there is some delay because those are in
the, you know, hundreds of nanoseconds
or milliseconds. And to us, it's like,
you know, 1/1000 of a second. We're just
not going to delay. But, for hyperscale
systems, which are literally made up of
thousands of GPUs acting as one brain,
if you will, right? One supercomputer,
one high-performance kind of cluster of
computers, then that latency is super
critical because the GPU notices
anything in the tens of nanoseconds or
hundreds of nanoseconds. So, therefore,
the typical Ethernet bit error rate,
which is the measurement of how much
errors you're getting uh per second. And
so, if that needs to drop from 10 to the
minus six to below 10 to the minus 10 or
what we call error-free today because
any errors then slows down the whole
training inference all the AI uh
infrastructure that's needed. So, that
has changed and allowed these very,
very,
you know, typically higher cost single
mode, oh, I'll mention that. Single mode
being longer distance, longer reach,
very high performance for long distance,
now has come into the data center and to
the hyperscale systems because of this
requirement for very low bit error rate,
very high performance computing and
connectivity. And now Vixels has to
raise its bar from 10 to the minus six
typical Ethernet the last 25 years to 10
to the minus 10, 10 to the minus 12. And
we've done that, right? So now we've
pushed our Vixels to 200 gigabit even
though you can use it at 100 gigabit and
50 gigabit NRZ, you can still leverage
that to very low bit error rate. So the
answer is that things have changed for
hyperscalers to require error-free and
that's allowed all these very high-end
single-mode solutions now to compete
directly with Vixels because of that
additional specification that's new to
hyperscale AI systems.
&gt;&gt; Okay, okay. So because the capacity for
sustaining errors is is much much lower,
we don't want all these GPUs to just be
waiting. Um that sort of changes the
game from from like the cloud SAS day to
to now when everything's acting as one
one big computer. And uh so this bit
error rate has to be much much lower.
And so Vixels, which are short reach,
have to either like essentially come
down to meet that or what you're saying
is these other technologies that are
longer reach, higher power, those
already were closer in the demanded or
like the necessary bit error rate. And
so people are saying, "Oh, why don't we
take those technologies and bring them
into short reach?" But but surely that
has like power and cost tradeoffs of
taking something that could talk at low
error rate like over a long distance and
and trying to bring it in. And so you
guys must be taking a different tact and
saying like, "No, no, no. Like let's
just make Vixels error-free
essentially."
And presumably that's uh
like a cost or a power tradeoff that
that you'd rather go with? Or is it back
to the the manufacturing supply chain
capacity?
&gt;&gt; Yeah, so it's again, it's a quite
complicated matrix of items you have to
check off, right? So, those who are
shipping
uh silicon photonics and EML for long
reach or DFBs, etc. Single mode, very
high performance devices have been
around for again, similar time, 25 years
and they've been used for long reach
because they have that super high
performance, very few fibers and then
what we would call WDM, wavelength
division multiplexing. So, fibers are
very expensive when you're going
hundreds of miles, hundreds of
kilometers and so you want to use very
few fibers, but then pass more
information through more wavelengths,
more colors in that same fiber. For
again, short reach, when you're talking
about tens of meters, you're not as uh
kind of uh locked into the cost of the
fiber, it comes down because you're only
10 m versus 10, you know, kilometers or
or extending. So, therefore,
the
capacity for volume supply chain of the
very, very high performance, low bit
rate would be a natural, right? They
come in, hyperscalers want low bit rate.
Let's go with the Ferrari, right? Let's
go with the super high speed, you know,
high performance single mode, but
they've been used to building in the
maybe 100K, 100,000 kind of volumes
because you don't need as many of those
between cities, between countries. And
all of a sudden, they come into the data
center, even though their performance is
excellent, cost is a little bit higher
because of single mode nature of
packaging. However, just the
infrastructure to build millions per
month now is 10, 20, 50X what exists.
So, that's brick and mortar. That's
basically saying, I only have one pizza
oven and I've been used to, you know, a
small uh clientele that I can make maybe
about 20 a an hour. Someone goes in, I'd
like to place an order for 5,000 pizzas
and I need them in an hour. So, you're
going I need I need a basically 100
pizza ovens. That's the exact same
problem that the very high performance
single mode long reach traditional
having coming into so silicon photonics
EML excellent excellent technology very
very good bit error rate all of those
but then the infrastructure needs to be
built up and that's what you're seeing,
right? You're seeing a lot of
announcements with people holding
shovels and saying we're investing in
the next, you know, supply chain the
buildings etc. and that's great, right?
Certainly bringing more manufacturing
not only in the world but back to the US
and those are all great for the the
industry as a whole but Vixels have been
around for 25 years and shipping in the
millions. So, we're not building we're
not putting shovel to to ground etc.
We're just changing the actual Vixel
performance the chip and then getting
leveraging the existing infrastructure
and so what we call for Vixel capacity
it's unconstrained, right? So, there's
constrained meaning they're sold out we
we're sold out through next year. If
you're going to place an order it's
going to be after, you know, be a eight
month 18 months lead time a year and a
half from now we can get it to you. For
us unconstrained just means we have a
certain lead time that's basically only
limited by our cycle time of building
through the factory. So, if for us, you
know, a Vixel run
and then a packaging run maybe four
eight 12 weeks but that's limited just
to the fact that we have to build it out
and ship it but it's not limited by the
constraint of the supply and ecosystem
of machines or pizza ovens. We have
plenty of pizza ovens. Place the order
we'll get you your order in the cycle
time that we uh we commit to.
&gt;&gt; Gotcha. Okay, that's that's very
interesting and a great sort of
competitive advantage there for you. So,
on the constrained side, is that what we
hear about for listeners like when they
hear about like indium phosphide being a
bottleneck and just like or is it
partic- Like where in the supply chain
is it constrained? And then for for you,
like what's different about Vixels that
does make it unconstrained?
&gt;&gt; Yeah, so for indium phosphide, a lot of
the silicon photonics and EMLs, etc. is
based on this material, indium
phosphide. For um
Vixels, our technology has always been
gallium arsenide. I know for the
listeners that may be okay, one three
five compound versus the other, what's
the difference? Indium phosphide is
material constrained from the very
beginning. Like you can't even get a a
base substrate, right? Even before you
process it, just the substrates for
indium phosphide are limited before you
get it all done and basically made into
a product, whether it's EML, silicon
photonics or
Vixels. The indium phosphide substrate,
bare material is already limited.
Gallium arsenide, unconstrained. So, we
start with that. And now you go through
the fabs and then of course fabrication,
etc. Uh depends on foundries. They're
usually very large companies that do
foundries, companies like Picolight
Jewel and others. We don't own large
clean room factories that make these. We
design the Vixel.
Uh we design the individual kind of
Vixel chip device. And then we use
foundries to manufacture, right? So,
those foundries are available, but they
can't get enough indium phosphide
starting material to do that. Now, after
that, again, once you get to the chip
level, right? You dice up, you go,
"Okay, great. I've got the laser. I'm
ready to go." Now, to get to the from
the chip to a pluggable device, right?
To an actual optical engine, if you
will, there's a ton of stuff happens,
right? Now, you've got uh laser drivers,
you got boards. And then for single
mode, you have to have all the machines
that align that particular silicon
photonics EML to a very, very small core
single mode fiber. So, those machines
have to be readily available, etc. And
so, Vixell's again has that
millions per month type of volume
infrastructure, doesn't need to be built
up. And then we get back to from the
very beginning Indian phosphide material
constraint. And then you have to build
it into lasers and then finally have to
package it into transceivers. And at all
along that supply chain,
it's not used to building millions per
month. So, all of that has to be
built up like hardware, machines,
alignment machines, testers, etc. to get
get there. Again, Vixell's has all of
that infrastructure existing already.
&gt;&gt; I see. Yeah, that makes a ton of sense.
Um I love your props, by the way. I like
the little Vixell that you held up. So,
tell us more. So, you Yeah, that's
awesome. Um maybe you tell us what we're
looking at and then walk us through
exactly what you design and then kind of
where it gets handed off and built and
packaged and yeah, where where your
responsibilities end.
&gt;&gt; Yeah. So, basically,
&gt;&gt; [clears throat]
&gt;&gt; again, background is super important,
right? So, there we call kind of this
tree of knowledge of Vixell's, right?
So, you have this line from Honeywell
through Finisar and then Finisar goes
into 26 and then goes into Coherent. So,
there's a Coherent line. And then for us
was obviously HP went into Avago, went
into Broadcom, and there's this kind of
HP Broadcom line. And then finally,
there's this uh I would say Picolight
E2O. Again, throwing in some old names
from 25, 30 years ago. Uh they go into
JDSU, which is another another big name
in the 2000.com time. And then JDSU
spins off Lumentum and Viavi. And so,
we're in the Lumentum arm. So, all of
these three major arms have a lot of
VICSEL knowledge. And so the strength of
Picolight is we've tapped into and we
have people designers from all three of
these branches. So imagine that all the
know-how, again, not patented know-how
about recipes and you know, I I use the
example you can just hand three
different chefs a recipe for making
souffle and most likely you're going to
get three different types because it's
really difficult to get perfect souffle
if you will. It's not just getting some
oh you get the eggs, you crack the eggs,
you beat the eggs, right? So it's a lot
more to that. And the same thing is in
the VICSEL. So answer your question,
what do we do? So we take all that
know-how and then we design
the epi layer. So you see all these
little kind of lines. So these are epi
layers that are designing this vertical
cavity. So it's not an edge emitting. So
edge emitting basically is a flat chip
and then the light comes out of the
edge. Surface emitting, right? VICSELs,
vertical cavity, surface emitting, comes
out of the surface. And so we design all
of the
kind of an internal cavity of the laser,
all the dopings and I'm not getting into
too much detail, but all the process. So
after we design, we hand it over to a
epi foundry that grows this material.
They give us back a
epi wafer that's unprocessed and then
we've been working with Win
Semiconductor in Taiwan. That's our
foundry. So once that epi wafer's ready,
we hand it over to Win and then they
process it they process it into their
clean room process and then they make
the actual final
VICSEL device. And then the beauty of
the VICSELs also compared to an edge
emitter is at the wafer level you can
start testing and probing each one of
these, 100% tested, what they call known
good die, before you have to singulate
it and dice it up into arrays, etc. So,
that advantage is huge because if you
have to add the more work you add in
before you quote yield the device,
whether determine whether it's good or
not, the better the the cost, right? Cuz
you you always want to yield upstream.
The more value you add and then you
yield downstream, you lose all of that
value added. So, wafer level testing for
Vixels is really, really advantage of
versus the the other kind of
edge-emitting type of technologies.
&gt;&gt; Nice. This Man, I'm learning so much
history and so much sort of one Vixels
101 here. That's awesome. So, um you you
work with WIN, you design the Vixel, you
have an epi uh partner who helps with
that. WIN
is able to even do the testing uh at the
wafer level because it's a Vixel, known
good die. Ultimately, it gets built into
the device. Um uh so, they're they must
be doing the package like some level of
packaging for you, too, WIN?
&gt;&gt; Right. So, uh
WIN is only on the uh wafer uh
processing. So, they come to the wafer
and then it's diced up into individual
Vixels. And these individual Vixels, we
work with our partners to build into
either active optical cables, right, or
transceivers, etc. And there again,
another
um
foundry, if you will, but this is a
packaging company.
However, with that said, companies like
TSMC, right, Taiwan Semiconductor, now
is going into co-packaging, meaning
after they make their silicon wafer,
they'll start packaging the optics
directly on top of their wafer, which is
co-package. So, there's another whole
field that's growing called CPO, etc.,
where the traditional semiconductor
foundries that are kind of wafer
processing, now are stacking up
different technologies together and they
call it 3D kind of wafer level kind of
packaging. Uh so that's all emerging.
For us, we only do the wafer at WINN and
then that WINN uh VIXEL goes to our
module integrators partners and then
they'll build it up into the active
optical cables or transceivers.
&gt;&gt; Got you. That's That's helpful. So then
um take us back to your road map. I know
you mentioned a 50G version, 100G, 200G.
Can you tell us more about And And I
know you also mentioned a a recent
launch. Um so So tell us more about your
road map, what you launched, what you
announced.
&gt;&gt; As I mentioned early on, 200 gigabit per
lane is kind of the the benchmark,
right? It's the bar you have to clear.
And EMLs, silicon photonics have all
done that. And now VIXELs
uh have reached that. We could will just
announce our 200 gigabit will start
sampling next quarter. And so that's for
a very simple transceiver where you have
eight channels of 200 gigabit coming in.
The aggregate or the combined bandwidth
of that eight channels of eight by 200
is 1,600 gigabits or 1.6 terabits. So
that's the That's the standard uh
ramping today, right? There's 800
um gigabit transceivers as well. That's
also shipping. That's eight by 100. And
then the next generation or today's
generation is eight by 200. So that's
the 200 gigabit VIXEL that we announced.
However, there's many, many different
flavors of that because of the
specification. So
aggregate bandwidth 1.6 T, right? Check.
But there's different ways to get there
if you want very low power or very low
bit error rate. So running 200G, I liken
it to a Ferrari, right? It can give you
the 200 miles per hour, but it's a very
high-end, relatively expensive because
you need certain signal integrity,
signal processing, all of that that adds
to that. So, now I say, I want a very
low-cost, low-power, but I still want
low bit error rate. And then what people
have done is let's slow it down. Let's
use the 200G performance in the VICSEL,
but then actually run it at 100 gigabit,
right? So, now you have a excellent,
excellent VICSEL that gives you a lot
more performance. And if you use it at
half the speed, you really get much
better bit error rates or the
signal-to-noise kind of ratio or
relatively or relative intensity noise
drops, as well. So, that's 100G. So, but
you need more lanes, right? So, to get
to 1600, you need 16 lanes of 100. And
then recently, something came out called
micro VICSELs, and that's going even
slower, down to 50G. And then they call
it NRZ, so instead of PAM4, which has
four levels, 0, 1, 2, 3, now we go back
to the original NRZ, which is 0 and 1.
So, now you have the use of the entire 0
to 1 signal-to-noise, which again
reduces your bit error rate. But you
need more channels. So, you need 32
channels at 50G to get to 1.6T. But all
three we are shipping, and all three are
in demand by customers, depending on
whether they want what they call fast
and narrow, like 8 by 200, or they want
a LPO, linear drive, no DSP, low power,
and that would be a 16 by 100G. And then
finally, if they want really, really low
bit error rate, very, very low power,
then they go to the 32 by 50G
NRZ, which they call slow and wide. We
we tend to call it fast and wide, and
then faster and narrower. [laughter]
But
you know, when you're in the high-speed
interconnection, we try not to use slow
in any of our marketing.
&gt;&gt; [laughter]
&gt;&gt; That's good. That's good. Okay,
interesting. So, yeah, this this is
really cool. So, you're saying, okay,
there's many different ways to get to
1.6T. You could have 8 * 200, um which
would use PAM4, require a lot of DSP and
power, um but it's it's definitely
possible. Or you could do 16 * 100 or 32
* 50, and you need like less DSP for
each of those. The The The um fast and
wide 32 * 50 has like
much less like uh cuz it's NRZ, so less
like DSP and stuff. Um
Yeah, this is all very fascinating. So,
will that approach still hold once you
move to 3.2T?
Is it going to be kind of that
combination of different possibilities?
&gt;&gt; Great question, because people say,
right? And anytime you have a
technology, they always say, "What's the
road map ahead? What's the future? Is
this the end of the road?" Okay, 1.6T,
we get it. Vixels can do it. But is
there a 3.2T? Is there a 6.4T? Is there
a 12.8T? Right? I mean, Andy
Bechtolsheim, notorious, right? He He's
created an XPO that's literally going to
give you six 12.8T in a big pluggable
today, right? So, they're thinking way
ahead. They're They're planning way
ahead. Because no one has ever told us
in the last 30 years, "Oh, woah, woah,
we have way too much bandwidth."
Right? So, we have to have that
bandwidth. And exactly like you said,
what's the future? So, number one, we
can use something called BiDi,
bidirectional. So, meaning we can just
add another wavelength, not the
complexity of a WDM where you have eight
or 16 wavelengths like single mode uh
that would do, but we basically just add
another wavelength to our existing one.
So, two wavelengths, passing them in
both directions, so bidirectional. That
doubles the bandwidth without changing
anything else except for you just add
another laser
at a different wavelength and you can
leverage the entire ecosystem. So, from
1.6 to 3.2, we can add another
wavelength. The other ways to do it, of
course, is to increase double the speed,
right? So,
can we do 100G NRZ? That's in the works,
right? So, we're developing 100G NRZ.
Today is 50G NRZ, but we're developing
100G NRZ leveraging our 200 gigabit
Vixell and running [clears throat] at
100G NRZ, etc. And then in the future,
we can go to more channels, right? So,
the beauty of Vixell is it gets surface
emitting means for edge emitters, you
can only have a one-dimensional array.
So, you can have a 1 by 4, 1 by 8, 1 by
12, but it's just makes you a a long
bar, if you will. But for
surface emitting, we can have a
two-dimensional array, meaning I could
do 2 by 4,
2 by 12, 2 by 16, and then essentially
couple all the light very elegantly with
a optical fiber bundle to do that. And
then in that case, I'm kind of
unlimited, if you will, right? So, I can
go up to up to 64 channels today in a 4
by 16 connector that's the size of Let
me just show you. So, a 4 by 16 fiber is
this size, right? Here's my finger.
&gt;&gt; Yeah. [laughter]
&gt;&gt; Uh
and that's that has 64 channels in
there. If I run them at 200, that gets
me to 12.8T. So, in essence, the
technology of today without having to go
to 400G per lane, which we're also
looking at,
&gt;&gt; Yeah.
&gt;&gt; but at 200G with more channels, with
more colors, like another color for
BiDi, you double, you triple by size,
etc. So, that road map to 12.8T, we
believe is very solid, very clear,
without even having to invent any new
technology to get there. And then with
new technology, it just gets easier if
you can do a 400G per lane, etc.
&gt;&gt; Sure. Fascinating. So, it's just the
same 200G VIXEL kind of over and over.
It's just
what if you want to put it in an array
and you get more of those or or do you
are you having to sort of invent a new
VIXEL to try to get it the 100G version
to run it NRZ?
&gt;&gt; Um so, we're just starting test. We
believe that the 200G VIXEL has the
capability to go to 100G NRZ. That so,
it's it's not a new VIXEL. Uh
it's just basically using a different uh
coding uh with respect to the signal
coming in uh running at NRZ instead of
PAM4.
Um so, that's just to take advantage of
the zero to one using up the whole
signal to noise ratio as one bit as
opposed to four bits, right? So, that's
the the difference.
&gt;&gt; Got you. Yeah, this goes back to your
kind of engineering pragmatic mindset of
just taking a LEGO block and figuring
out different ways to place it or
different ways to use it and to sort of
unlock this whole road map and the
future road map. That's pretty cool. So,
okay. So, if uh a hyperscaler you you
talked about um unconstrained gallium
arsenide and working with WIN um and
they're you know, used to making this
stuff. They've got all the pizza box
pizza ovens they need. So, if if uh big
hyperscaler comes to Pico Jewel and
says, you know, we want a million of
your pizzas, um
what what does that look like? Like, how
does that actually happen?
&gt;&gt; Right. So, if if they want a million
VIXELs, then we would give them
typically an 8-week uh 10-week kind of
lead time. That's kind of the basic.
Obviously, the we can accelerate that
and and you know, kind of push and have
engineering carry certain wafers. But
typically, you know, 8 to 10 weeks on
the VICSEL side. So, you'll get a you'll
get a wafer or you get individually
diced VICSELs. If you want transceivers,
then that 8 weeks tags on a certain
number of weeks to package it all into
the transceiver, right? So, but those
are again constrained strictly by the
process of packaging, not about ordering
equipment or having to build capacity,
etc. That ecosystem works and it just
leverages this the the typical cycle
time, we call it, of building out. So,
typical cycle time, 8 weeks for the
VICSEL device and then potentially, you
know, 4 or 6 weeks for the additional
module and it after that. And so, you're
looking at
anywhere from 12 weeks to 16 weeks to
get to the full
module starting from a epi reactor,
growing epi and going all the way
through.
And so, we'll continue to drive that,
you know, lower as far as lead time or
cycle time, but also yields. I didn't
really mention too much. Yields are a
way to say if I make a VICSEL, how many
known good die can I get out of this
wafer or this particular process. And
the higher the yield up to obviously
100%, the fewer wafers I have to run
through, the higher the capacity of this
factory, if you will, right? So, if
every wafer goes through and I get 100%,
then I need fewer wafers and therefore I
need less capacity to for the demand.
But obviously, getting to 100% is very
hard. But VICSELs have been perfecting
that process for many years, for many
decades, and now we're leveraging all of
that. It's not new. It's not something
that has to be established. It's not
based on new technology. So, that's very
important is that since we've
Win has been doing it for about 10 years
since we transferred that uh, consumer
electronics application
back in 2016. They have a capacity of up
to a thousand of these wafers per week,
right? So, that capability, and then the
other thing is there's about 240,000
Vixels on each wafer, right? Cuz they're
really tiny.
&gt;&gt; Yeah.
&gt;&gt; So, they're very, very tiny. And so, you
that adds up to, you know, a million
yielded maybe 10 wafers. So, it it's,
you know, the capacity is huge for data
com. Um, so I think we have no worries
for us once we get to the 200G and the
product specs are met with the customer,
reliability qualifications done, then we
just ramp readily with WINN and they're
ready to go.
&gt;&gt; Nice. Amazing. It's it's quite
compelling, um,
I think normally when people hear like,
"Oh, there's a startup that's trying to
compete in a space that has these huge
incumbents." Um, it's, you know, the
question is like, "Well, how's this
startup going to compete? How are they
going to get to market? How are they
going to find customers? How are they
going to build up supply chain?" All
these things, but but what I hear you
saying is that like
you're you're taking sort of industry
veterans that have some process know-how
across like the probably, um, similar
ways of thinking as competitors, just,
you know, you've been in the game for a
long time, and then tapping into an
existing supply chain, and also at the
end of the day, it's not like you have
to go win, you know, 50 customers, but
there's a probably a handful of big
customers that would be really make a
difference for Pico Jewel at the end of
the day if they said, "Yes, you know,
we'll we'll take some of yours." And
then, but but the most important point I
think of all of this is the
unconstrained
gallium arsenide, like being able to
make a million, you know, 10 wafers with
240,000 on it, whatever you yield, you
know, we're talking millions of Vixels
very quickly. Cuz I think as we see in
across all of semiconductors, whether
it's, um, memory or CPUs or AI
accelerators or whatever, there's
obviously there's just so much demand
and such constrained supply that truly,
obviously, you want to compete on cost
and on engineering performance, but I do
feel like there is just a little bit of
like, if it's good enough and it's in
production and you can install it into
my data center, like, you know, game on.
Um so it it feels like, you know, like
you guys have a strategy that will allow
you to, you know, deliver shipped pixels
as soon as you possibly can,
uh which which
&gt;&gt; the model has been around for decades in
the silicon, right? I mean, Palo Alto in
Silicon Valley, most companies, most
chip companies designing uh integrated
circuits or uh CPUs, GPUs, they don't
have their own foundry. A lot of people
use Intel or even AMD uses TSMC, etc.
So, AMD's a huge chip company, they
don't have their own foundries today,
right? And so, TSMC, Intel,
GlobalFoundries, I mean, many foundries
are the quote factory floor, the the
clean rooms of all these startups. So,
just because of our small startup size
doesn't mean we can't ship in the
millions per month and compete directly
with the very large presence of uh other
optical, you know, suppliers and
companies, our competitors, etc. So,
that's the beauty, right? So, we can
stay very lean, you know, our motto is
stay small and that has to do with many
things. Our name is Pica Jewel, right?
That's low, very, very low power, and
that's one of the things that's driving.
And then we're also very well
experienced small team, but we can have
huge uh benefit by leveraging Wind
Semiconductor, by working with our
supply chain, and they've got the
factories, they've got the clean rooms,
and then we can ramp very quickly by
providing our designs and our unique
kind of specialty and then partnering
with these
large companies that are already
shipping and they would just drop ship,
right? So if we don't need a big large
company in order to ship in the millions
per month.
&gt;&gt; That's amazing. Yeah, definitely
punching above your weight. That is
awesome. So
when is your high volume ramp targeted
for I I if I recall the maybe the press
release said something but
&gt;&gt; Yes, press release said we're starting
to sample next quarter
and that's in different flavors, right?
So we've got customers for the 50G NRZ,
100G LPO and then also the 200G. So all
of those will begin to sample and the
process of from our device to actual
product shipment or revenue for our case
is a period what they call
qualification, right? Qualification or
reliability testing. So everything has
to kind of not only meet spec at zero
hour but it has to be predicted to last
10 years or a number of years etc.
Through what they call accelerated
aging. They test it out at higher
temperature, higher bias conditions and
then they kind of estimate back at the
normal operating condition can it last
10 years in the field etc. And that
period can for
very small companies like tier two kind
of customers be as short as three
months, right? To to go through that.
But for tier one because they obviously
have much more to lose if they have an
issue with their connection
could take more than six months to get
those up and running. So ramping at when
is available today. However, we have to
go through this qualification cycle with
our customers before they give the
orders, everything is
approved, meets their specifications and
qualification and then we start ramping.
So we we also said that we'll most
likely start ramping in early 2027 next
year.
&gt;&gt; Okay, okay, got it. Thank you for the
education here. So, yes, sampling and
then the qualification process and then
ramping. And it's probably Yeah, as
you've been saying throughout the whole
thing, you're not concerned about the
ramping. Obviously, it's you had to
build the product and let customers kick
the tires. And once they say, "Let's
go." then it's off to the races. Well,
uh
you know, we've covered so much. This
has been so amazing. I've learned a lot.
I know the listeners will have learned a
lot. I guess is there anything else uh
any last things about Pico Jewel or
anything that we didn't talk about that
you were hoping to cover?
&gt;&gt; Um I guess one one thing that's very
interesting to me, right? As you can see
there's the the image that you're seeing
is a very experienced uh elderly startup
person.
&gt;&gt; [laughter]
&gt;&gt; And uh one thing to point out is that
very few people went into hardware and
photonics in our space because young
people over the last literally when the
dot-com came out, it was 25 years ago.
So, those who are coming out of the
workforce were more in the application
side, what we call the software side,
right? So, people wanted to go into
computer science, etc. And so, what we
found is the aging kind of experienced
hardware folks in photonics needs to
transfer all of this knowledge. So,
that's one of my passions is to kind of
bringing on the next generation, the the
generation after that for the photonics
cuz we don't know just like Vixels and
other technology. We see many, many
decades and as I said earlier, no one's
saying, "Oh, way too much bandwidth."
So, we see bandwidth increasing and
bandwidth demand increasing with
robotics and autonomous vehicles and
what have you, right? Everything is
going to be uh bit and connectivity's
kind of constrained. And so, we want to
basically spend time to educate, train.
And so, we're trying to hire, you know,
hardware engineers and then train young
folks maybe without the experience to of
be the pixel designers, be the chance
fever designers of the future. And so
that's really exciting for us, right?
Because we've got all this knowledge,
you know, 10, 20, 30, 40 years and it's
really kind of feels wonderful to have
the hardware excitement again, not only
in the markets, etc., but the investment
community, Silicon Valley is booming
with photonics and hardware. So, you
know, we don't take it for granted. It's
a great opportunity and we definitely
want basically take young kind of
entrepreneurs, young engineers, folks
that are interested in this space, you
know, along for the ride and then they
take it from there.
&gt;&gt; I love it. I love it. Very inspiring. It
very cool. Um, and
you know,
uh, that it's never been a better time
probably for interconnects and photonics
and optics type folks and, uh, I love
that, you know, you industry veterans
want to bring up the next generation and
give them the opportunity to learn from
folks like you, uh, and to kind of
uh, revitalize, rebuild, um, make sure
we have like a reinvigorated workforce
so that, you know, we for my generation
and the generation of my children, that
they they can keep having more and more
data moved around faster and faster.
&gt;&gt; That's right. That's right. Yeah, so
really enjoyed our conversation, Al. So,
thank you.
&gt;&gt; Awesome. Cool. Thank you, Al. Appreciate
it.
