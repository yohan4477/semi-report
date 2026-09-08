---
source: https://www.youtube.com/watch?v=ENLpjxTmAFI
vid: ENLpjxTmAFI
title: Tensordyne's R K Anand: HPE Juniper Fabric, Logarithmic Math, MoE Inference, Air Cooling, 3nm
date: 2026-08-18
duration_sec: 3332
channel: Semi Doped
kind: transcript
---
Hey everyone, welcome back to another
Semi-Dope podcast. Today we've got a
special guest, RK Anand, co-founder and
chief product officer at Tensordyne. Uh
if you haven't heard of Tensordyne,
Tensordyne is building an inference chip
and inference rack that does its math in
a completely different number system and
has other interesting architectural
tricks that we'll talk about. Um so RK,
I'm pleased to have you here to talk
more about Tensordyne.
&gt;&gt; Austin, it's a pleasure to meet you and
I'm very glad to be here. I watch a lot
of your podcasts and I'm a big fan, so
I'm glad to be here today.
&gt;&gt; All right on. Awesome. Awesome. I love
that. Um thank you. Okay, so So, let's
start with you. Um you have a
fascinating background in networking,
which is really interesting because I
think now that we're at rack scale,
obviously networking is a big part of
the AI inference story. So, you know,
maybe tell our listeners more about you.
Take us way back. You were at Sun, you
were a founding engineer at Juniper.
Kind of tell us about your career arc
that led you all the way here.
&gt;&gt; Yeah. Um
yeah, so you know, this is my 37th year
in Silicon Valley. I started my career
at Sun in 1990, actually, designing
microprocessors. So, I was part of a
microprocessor team.
And Sun was building high-end servers
for the market. So, it was a really
fascinating time. There was a lot of
competition. There was RISC versus CISC.
Uh and you got exposed to building
really large multiprocessing systems.
Uh fast forward a few years, so 1996 I
was um
fortunate to join Juniper Networks as
one of the founding engineers and led
the first silicon efforts there. And
the reason I was able to do that was
because Pradeep Sindhu, who's the
founder of Juniper,
uh
was one of my early mentors at Sun. He
was part of a team from Xerox Palo Alto
Research Center helping us build these
big machines and he um
gave me the opportunity to join Juniper.
Um
And I spent almost 17 years there with a
little bit of a break. Um and saw the
company from zero to later or 4.25
billion dollars of revenue and the most
fascinating part was that we were uh in
the early days of the internet. Uh
the internet was doubling every 6 to 9
months and I think Juniper I think
transformed networking pretty
significantly. So, it was a very good
learning opportunity opportunity to
start from scratch and grow with the
company and uh and eventually be very
successful in building the biggest
routers in the world.
But most importantly, I think building
great relationships and great
friendships and being able to mentor a
lot of the talent there. So, I think
it's a it was great learning experience
for me.
&gt;&gt; Oh, man, it sounds like it. Okay, so
interesting. So, you got to work on
compute back at Sun and then you got to
work on networking for a long time um at
Juniper and then here we are in this era
which is both compute and networking. Uh
so, I it seems like you have learned all
the right things that you need for this
era.
&gt;&gt; Yeah, it's a it's fascinating, you know,
I think the Silicon Valley, if you've
been here long enough, goes through
cycles, right? And we're in one more of
those really great innovation cycles and
yeah, you're right. Uh you know,
computing, you think about computing and
you say, "Okay, general purpose
computing or high high-end client-server
computing." And how how was that built?
Uh you know, because we started from PCs
and you know, mainframes then PCs and
then went to client-server and Sun was a
premier company, a great innovation a
great place for innovating and and
building a great technology. And then
Juniper ends up being the premier
company in networking building high-end
core and edge routers, right? The fact
that we have the internet today uh that
works at so flawlessly is because of all
the work that companies like Juniper,
Cisco, and others did.
Um
and then we come back come to the world
of AI and it's uh again back to
computing but
then we start hearing for the last
couple of three years like networking is
so central to AI.
So, it's the coming together of all of
these things and you know, you can then
reflect back and see if you can take
those learnings and apply them to what
you're doing today, I would say.
&gt;&gt; Sure, yeah, totally. So,
what I think is interesting and
you know,
correct me anywhere I'm wrong but when
you guys started at Juniper, I mean I
assume that it was Cisco was probably
the dominant player in the in the space.
&gt;&gt; They were. It's you know, Cisco was
started in the early 80s and by
or probably a mid-80s, I don't remember
the exact time but when Juniper started
in 1996,
the browser had just appeared, right?
Out of Urbana-Champaign and Netscape,
the Mosaic browser and the Netscape had
appeared and we were trying to put a lot
of our data on the internet and we were
starting to start sharing our think of
it almost like sharing your hard drives
basically.
And
and there were there were these internet
service providers like UUNET was an
example of them and and they were they
were using Cisco routers and Cisco was
the dominant player. I think Cisco had
like 93, 94% of the core router market
share.
And
fortunately for us, Pradeep who was the
founder of Juniper looked at the way the
routers were getting built and he was
trying to wonder why are they not
getting built like high-end servers.
So, he had a general thesis that he
could actually build routers far more
efficiently.
And
and then you then we got get to hear
from people like Mike O'Dell was CTO at
UUNET that the internet was doubling
every 6 to 9 months and he was not able
to keep up.
And
and so Juniper fundamentally
re-architected how routers were built
and that completely transformed how the
growth of
the internet happened.
Cisco by the year something 2000 was the
number one market cap company in the
world. You know what they were like. And
and John Chambers was on the cover of
every magazine in the world.
And and Juniper appeared in the
landscape and we built the highest
performing router. And then I think
within the span of a year couple of
years we had 30% market share. So there
is proof positive that when new markets
evolve there opportunities for startups
to come in and if they have technology
that's differentiated they can have an
impact in the market.
&gt;&gt; Nice. Awesome. Yes, you you took it
exactly where I was thinking in my head
which is like wow, this actually feels
very similar to back then where there's
a new
technological revolution happening
that's impacting end users which was the
internet at the time and it's LLMs
today.
And
there's an incumbent that of course you
know is the largest market cap company
in the world and is quite dominant and
I'm sure when you guys started Juniper
there was probably a lot of people that
just said like what are you doing? How
could you ever possibly compete with
Cisco? But then what I heard you say was
the interesting insight is like well if
you think that there's a different way
to tackle the technology that ultimately
you do think you can compete on
technical performance and then probably
TCO and other things.
&gt;&gt; Yeah
and you know of course the battles only
quickly ended because the size and scale
of the market is kind of way way
different now.
And and the competitive landscape you
know I mean you know when in those days
the internet information was more
constrained. Everybody knew we live in a
different world today. Information is
instantaneous. Everybody knows everybody
else.
But in that period between say 96 and 99
there were many other companies that
were funded to build routers.
I mean all those names are etched in my
mind right? There's Avici and there's
Fluris and Nexabit and there's a bunch
of companies. So, uh
there's an opportunity that a landscape
opens up, an opportunity opens up.
I think if you look at today,
the scale is orders of magnitude larger.
The you know, the market capitalization
of some of these companies is quite
significant. And then the
uh and the technology power that is
there, especially with uh
Google or a lot of hyperscalers also
building silicon systems, is that
there's a lot more information.
Um
but I think there's a there's a there's
a there's a you know, just like anything
else, there waves and there changes that
happen. I think that if you if you look
at the last 5-6 years, uh the initial
phase was all training, AI training,
right? And then we have slightly shifted
from training to inference. And
inference was initially we were doing
monolithic kind of models, and now we're
in the world of
2 trillion plus MOEs.
So, the the architecture demands for
inference are different
from training. And then for monolithic
models to MOEs with you know, 2 plus
trillion models or 2.8 like Gopher 3,
the the pressures on the system are
different. So, there's a window of
opportunity that opens up on if you
think about it and how can you build a
system that addresses demand for today's
market that looks different from
something that's 4-5 years back.
&gt;&gt; Yes, perfect. Okay, so lead us into from
there then into TensorDyne and what we
have this window here. It's it inference
at just kind of massive scale. Um it's
mixture of experts, 2 trillion
parameters. We want high interactivity
these days. It's agentic AI, right? So,
agents want to run at thousands of
tokens per second ideally. Um and so
therefore so we've got this gap, we've
got this window. There is definitely a
way that everyone's doing it now, which
is mostly like running this inference on
racks and racks of GPUs. And TensorDyne
is taking a different approach. So, like
tell our listeners what is the technical
differentiation that you guys are
pursuing that you think is a different
bet?
&gt;&gt; If if one were to break down the
problem,
uh
you know, the models are immensely
large.
They, you know, so they don't fit on
single devices anymore. So, so now you
have to have many devices that somehow
operate in a kind of a
synchronous or orchestrated mode. Well,
how do they do that? Well, you have to
connect them together. So, there's a
networking problem that's in front of
you that makes you makes makes apparent
that the model ain't fitting on a single
device. You got to
spread it across many devices.
Then, there are power and other
constraints that are in front of us,
right? We can't get power quickly
enough. These data centers are large.
And,
uh
you know, we didn't I mean, we didn't
start at this point, right? We If you
look at If you had to, you know, rewind
a little bit,
Tenstorrent got its uh was prior to this
was named as Recogni, and we we had our
series A funding in 2019, and we were
more at that time the world was about
image and image recognition and ResNets
and ResNet 54, ResNet 101.
And, we started as an inference company.
So, but
uh because it was image recognition, we
had to think, okay, how are we going to
build uh
uh piece of silicon and a system that
can do really exceptional perform
deliver high performance for AI for
inference
for image recognition. And, the market
was automotive that we focused on.
Automotive has a power constraint. The
car can only give you so much energy.
So, there's a power constraint, and you
have to deliver inference, and you have
to process,
let's say, incoming frames of from
cameras that are at 8 megapixels.
So, we set that up as a problem
statement.
And, then the realization was that if
you took traditional math and try to do
it in the car, you would blow the power
budget of a car.
&gt;&gt; Mhm.
&gt;&gt; You know, rather than using it to move
the car more more miles, you would
basically, you know, shrink the range of
the vehicle. So,
our approach to inference at that time
was like, let's think about
mathematically it being different.
And let's approach math it from a first
principles math perspective.
And that's how we converge on using log
logarithmic math for AI.
So, that set up uh if
you know, you don't want us to be
fortuitous, well, that set up the
foundation for TensorDyne today.
We didn't build a perfect device, but we
uh we validated our math. We validated
that it really worked for AI.
Uh and
and the uh analogies were that, you
know, first of all, log math's been
around since uh John Napier
invented it over 400 years back. So,
it's not something that we dreamt of of.
And uh log math has been used, you know,
if you think about like the Apollo
program and all these programs, people
used to use slide rules and log math to
determine escape velocity and re-entry
and all these things.
And then, over the last two three
decades, we've been using log math in
DSPs.
So, it's not like we were the inventors
of log math, but our realization was
that can we use log math in AI.
&gt;&gt; Mhm.
&gt;&gt; And so, that that helped us, right? And
set us up for today.
&gt;&gt; Gotcha. Okay. Okay, interesting. So, for
listeners who uh haven't heard of
TensorDyne before, TensorDyne actually
started as a different company. What did
you say the name was?
&gt;&gt; Recognai. R E C O G N I.
&gt;&gt; Recognai. Okay, so probably image
recognition, maybe it came from that.
Yeah, yeah, yeah, yeah. So,
&gt;&gt; Exactly.
&gt;&gt; Um so, you were looking at like
convolutional neural networks, that kind
of stuff pre-LLM, pre-transformers, and
you were asking, okay, how can we do
this at the edge thinking automotive, so
that you know, self-driving cars, that
kind of thing makes a ton of sense. Um
And you obviously have power constraint
there, which I'm sure we'll get to it
same power constraints in the data
center same but different but like
thinking about power.
But you were you were taking a you were
asking how can we do this incredibly
efficiently
and the the idea was to use log math
instead of the traditional like matrix
multiplication
multiplies and adds like to tell our
listeners a little bit more about like
what does log math unlock as the
benefit?
&gt;&gt; So,
you don't you can't avoid matrix
algebra. Matrix algebra is a fundamental
for all of AI. So, it's not like we
could avoid that.
But if you take a number and convert it
to a log number,
then
and most of the operations are
what I call Matt malls, right? Which is
basically if you think about it is a
multiplication followed by an accumulate
and addition. So, we're doing trillions
of multiplications and additions in AI.
Whether we're doing in convolutional
neural networks for image recognition or
in LLMs, it's exactly the same.
So, when you take a number and make it a
log number, then log base 2 A * B is log
A + log B. So, multiplier becomes an
adder.
&gt;&gt; Huh.
&gt;&gt; And you know, let's think of ourselves
as young children. Let's say we are in
elementary school and we're trying to do
multiply two numbers or add two numbers.
Adding is easy, right? You just take the
numbers and add them. But when you want
to multiply, you know, you have to do
the long multiplication and add a bunch
of after that.
It's the same thing in silicon. If you
think about it, you have to have a lot
more gates. You're going to take a lot
more area, a lot more power to multiply
two numbers. But you want to add two
numbers, it's more easy.
Adders are you know, like a building
block in silicon.
So, you solve the first part of the
problem.
The second problem part of the problem
is really hard because now you have to
take the the result of the
multiplication and add it.
And the minute you are in a logarithmic
domain, adding becomes a problem.
And if you were to take a traditional
approach of a lookup table or Taylor
series, all the gains that you have in
going to addition in place of
multiplication are lost.
So, our fundamental innovations that we
have patented it was to figure out how
to go back from a log to linear space.
&gt;&gt; Uh-huh.
&gt;&gt; And perform the additions without losing
the gains in area and space and power
that we got from multiplying the numbers
with actually adding them, right?
And so, we spent inordinate amounts of
time in mathematics. So,
almost half the company spent almost
half a decade in math.
Right? Because that's what you that's
how
uh you can be a revolutionary startup
rather than an evolutionary startup.
Because then you can do Because if you
do it If you do the same thing like
everybody else has done, and you have
access to the same say silicon geometry,
7 nanometer, 5 nanometer,
you're not going to have no advantages.
You can't compete uh against the biggest
guys. So, you actually have to think
about this differently. And that goes
back to how
you know, in my thinking reflecting back
in '96 and '97, how Pradeep and
and the other co-founders of Juniper
thought about routers, right? And do it
differently. Forwarding in silicon
versus forwarding with, you know,
microprocessors. So, the similar
analogies applied here. And so, we spent
a lot of time thinking about that.
&gt;&gt; Nice. Okay, awesome. So,
you reached for long math because you
realized, okay, we have a bunch of math
mults to do, and if we instead of in
multiplication is expensive from a power
and a uh
dies area perspective, um and ultimately
probably latency as well. And therefore,
if we can convert it to the logarithmic
domain, we can turn these into adds, but
then eventually it has to get turned
back, uh converted back, and you guys
thought really hard about how to do that
uh efficiently, effectively, cleverly.
Um
and so, okay. So, then you said, "Okay,
we figured this out. This is great. This
is more power efficient,
uh small, fast." So, then you took it to
market ultimately, or at least built
chips for automotive um to kind of prove
out essentially the R&amp;D side of things
and to Okay. Now, connect me from there
to getting into data center inference.
&gt;&gt; Let's do that. Let's do that. So, um
think of a convolutional neural network
as like a 3x3 matrix.
So, you have to perform nine operations,
nine multiplies followed by all the
additions that make add up those nine
numbers.
Uh
so, we had the building block for it.
And we had functioning silicon in 7
nanometer that was fully functional and
we were able to demonstrate taking
camera streams and doing that.
Um we hadn't incorporated a lot of
safety features that we needed for
automotive.
&gt;&gt; Mhm.
&gt;&gt; And so, at that time in, you know,
late '22,
early '23, ChatGPT happened.
And we realized quickly that our
building blocks were really set up
perfectly for this moment.
Uh the market was 50 or 100 times
larger. The ability to have
a product from power on to getting to
revenue is much, much faster in the data
center, in in networking rather than in
automotive because automotive has a long
qual cycle, right? It takes a long time
to build a car. You got to certify it.
You got to make sure it's safe. There's
a number of things that need to happen.
So,
uh we coalesced as a team and said, "Let
us look at our technology and see how
applicable is it for LLMs." In LLM, you
do 1x1 multiplications, not 9 3x3.
Great. Uh well,
LLMs, so if you look at ResNets and all
the thing you have 100 million parameter
And now you're going for 100 million
to multiple 100 billion to trillion
parameter.
So, the memory hierarchy, the memory
architecture has to change. You have to
think of memory slightly differently.
&gt;&gt; Yeah.
&gt;&gt; Uh but your fundamental building blocks
for math you can build upon.
And so, that's what we did. And so, we
started architecting in 2023. So, we had
the good fortune of retrospective view
on
um
on math
uh and 100 million parameters. But we
also had a view that what was the
problem statement in front of us.
That is that you could go from multiple
hundreds of billions to maybe trillions
of parameters.
And so, how do we build an architect a
chip for that?
We still hadn't solved the networking
problem though. So, we said, "Okay,
let's understand how to build first
an accelerator that could be world-class
and deliver world-class performance for
LLMs. And then the multi-100 billion
parameter problem now became a
multi-trillion parameter problem.
&gt;&gt; Yeah.
&gt;&gt; And so, now you have to think of the
networking problem next.
&gt;&gt; Yes, yes. Okay, so you you guys said,
"Oh, we've got all the building blocks.
The opportunity is enormous. Uh the path
to production is shorter. Uh
I'm sure it was hard decision, but in
retrospect it's kind of a no-brainer.
Um but of course you had to make new
memory dis- hierarchy decisions. And
then uh to your point, that leads to the
like oh, that
the the model weights are not going to
fit on one chip. Therefore, we have to
connect lots of chips. Therefore,
networking has to be like a first-class
design priority.
&gt;&gt; It does.
&gt;&gt; Yeah, so tell us more then about your
networking and where you guys ended up.
&gt;&gt; Yeah, so now now um
now let's for a moment step back and
think about the first principles of uh
how do you build uh GNA inference
systems, right?
So,
this compute, uh, there is constraints
that are there place, right? What is
your compute, whether you compute bound,
uh, whether you are like memory
bandwidth bound, how much of bandwidth
you have coming in from external memory,
memory capacity bound, how much memory
can you put,
right? And then, uh, when you think
about the networking problem, then you
say, "Okay, how much bandwidth do I have
facing, uh, in and out of a, let's say,
scale-up network? And then, what is my
scale-up network latency? Because that
also might have an effect." So, now you
think about silicon and you say, "Okay,
how much of my real estate do I allocate
for all of these things? How much do I
allocate for compute?
How much do I allocate for memory
interfaces and memory capacity? Uh,
how much do I allocate for on-chip
memory? There's SRAM.
&gt;&gt; Mhm.
&gt;&gt; And then, how much do I allocate in
terms of interfaces and bandwidth and
for my fabric interfaces? So, when we
sat back and looked at it, and this was
like an, I think, I believe in the
summer of 2023,
the realization from some me and some of
my colleagues were,
"Gosh darn it, we've been building these
networking systems for
15-20 years at Juniper Networks.
And I had the good fortune of leading
some other efforts at Juniper for in
silicon,
uh, for almost 17 years.
And in the backside of a router,
in the rear of a router, is a scale-up
fabric.
Because if you think about a router,
it's got lots of front side ports. So,
think of like a high-end router, it
could have,
I don't know, s-
almost over hundreds of 800 gig ports.
So, traffic comes in from one port,
and then goes into the back, the rear of
a router, and somehow that traffic has
to be routed to an outbound port.
&gt;&gt; Yeah.
&gt;&gt; So, router typically is, you know, in a
large, uh, uhm, of presence,
AT&amp;T or Verizon, or connect big data
centers of Google or Amazon.
So, in the rear of a router is a scale
of fabric.
And it's designed to deal with
any-to-any traffic,
any packet size. So, typically, you
know, in typical if you look at TCP/IP,
you could have like a small 40-byte,
20-byte packet, you could have a jumbo
frame, 9K, and the and the fabric has to
deal with this random traffic. Uh, it
might have like email, which is SMTP
traffic, or it might have real-time
video like this call.
&gt;&gt; Mhm.
&gt;&gt; So, the router has to be robust under
all conditions.
And so, the realization internally was
like,
there is a ready-built scale of fabric
available for us.
If you can make the connection, and so
we had the good fortune to be Juniper
alum, and HPE Juniper now, HPE Juniper
alum.
And so, we reached out and partnered
with Juniper Networks and leveraged one
of their
highest-end routers, and took the scale
of fabric in the rear of it, and
leveraged that for our system. So,
suddenly, we have went from having an
accelerator that could be world-class,
highest-performing,
to an accelerator that is now
well-connected in a scale of fabric.
So, this combination of networking and
compute,
if you had that, if you had the
background, if you thought about it,
then
some of these dots can connected, and we
were fortunate to do that.
&gt;&gt; Gotcha, fascinating. Okay, so you had
the compute, and then you needed
ultimately you needed a scale of fabric
cuz you're like, "Hey, we need to
connect let's say 72 chips together into
a rack, and instead of having to start
from scratch there, you were able to
partner with HPE Juniper, uh,
and come up with a scale of fabric that
that fits your needs there." And okay,
so talk to us more about the scale of
fabric because ultimately, I know that
this could limit like the the of tokens
per second at the end of the day. Um so
like but but but but take us there and
explain it.
&gt;&gt; Let's think about
um the system broadly, right? Um
So I I've always been I mean I think
I've had good fortune to have mentors
through my career that told me that when
you design systems
think about the balance. So if you if
you over pivot on one resource, let's
say you're compute compute heavy,
then you might be in points in time
where the computer is sitting idle.
Uh if you are uh
if you have undersized something,
then uh you might be starved off that
resource.
So you have to think about how uh you
allocate the precious resource in a in a
silicon.
So
um
the thing that happened to us was that
we wanted to build a scale-up fabric
that was ready for yesterday, today, and
tomorrow.
And the best scale-up fabric in the
world was at the back side of a router.
Uh why does why is that? Because it has
to have some really exceptional
any-to-any characteristics, so you can
connect like multiple accelerators or
multiple Think of routing devices that
you can connect them together.
It had to have incredibly low latency
because we know that, you know, on a
video call like this, latency has an
effect on how we experience each other.
Uh we we, you know, today we use
FaceTime and or whatever, and we
call people on the other side of the
globe. Think of that latency, right? Uh
with multiple hops.
Uh it had to be congestion free. It had
to be reliable.
And it had to be it had the capacity the
fabric or the the scale-up network had
the should have the capability that you
can push its utilization all the way up
to 99 plus percent, and it will still
perform really well under those
conditions, under loaded conditions. So,
all of these were key elements for us.
If you have to look at all of these
elements,
that was the the Juniper file HP Juniper
Networks cell fabric in the backside of
a router had those properties.
So, its latency characteristics are like
sub one between one and two
microseconds.
Okay. So, now you look at this picture
and you say, "Wow, this is the this is
the perfect fabric for us."
What had happened in parallel in the
world in networking in in sorry in AI
models, the models got larger
and the traffic patterns went from
rhythmic tensor parallelism kind of
uh
patterns to random traffic because when
you do experts, the experts are random
in nature.
So, now communication uh
at the if for the high tokens per second
per whatever, communication now becomes
a bottleneck.
And if your fabric is better than
anybody else's, that communication
bottleneck
is uh
relieved somewhat.
&gt;&gt; Sure, sure.
Okay, this is so interesting. So,
taking a step back, you guys said, "Hey,
uh when you when you first start
thinking about this, you needed to
balance
um
compute, memory capacity, memory
bandwidth, networking bandwidth, and on
the uh scale-up bandwidth, you said
essentially, yeah, what's like the the
best
maybe maybe you're able to look forward
and think that this would be like the
defining bottleneck
of sorts. Um what's like the best
possible scale-up networking technology
that's out there and you looked and you
said, "Hey, at the back of these
world-class routers, like that's great."
And and and to your point, they can
handle, you know, heavy load, low
latency, and so on and so forth. Um Then
so you so you're adopting that and now
to your point, we're in a world where
it's like, "Yes, you actually do need uh
rack of, you know, 72 chips, maybe many
racks even, running a 2 trillion
parameter a mixture of experts. So, the
experts are living in different places
and for every token it might need to go
to a different expert. So,
irregular communication pattern.
Um and now,
contrast it for listeners with maybe
like what's being used today. Like when
you say 1 microsecond,
um how should they benchmark that
against like um
you know, like say an NVLink or or
AMD's UA link or something. Like or or
is it like an order of magnitude or how
should we think about it?
&gt;&gt; Yeah, so uh
let's reflect back uh last couple of
years. So, the first scale-up system for
AI in the world
is a GB200 NVLink NVL72. So, it's the
first time because prior to that uh only
eight devices got connected together.
&gt;&gt; Yeah.
&gt;&gt; So, to connect 72 devices, it's Gen1.
NVLink 72 is Gen1.
We are in Gen7 of a scale-up fabric
when we lever leverage the Juniper HPE
Juniper Networks fabric. That's point
number one.
Uh
so, there's a learning cycle, right?
Because when you build scale-up systems,
you have to build them, learn them,
refine them. You know, there's iterative
process.
&gt;&gt; Yeah.
&gt;&gt; That learning process we can leverage
uh from HPE Juniper. Uh
so,
that's one part. Now,
if you look at the world of AI, most of
the most of the vendors now said, "Okay,
we need a scale-up fabric."
So, you saw a consortiums come together
with UA link,
uh with Ethern,
still early days. They're still in, you
know,
specs and then early implementation. We
still don't have accelerators that can
talk UA link or and and UA link fabric
chips and all of those things.
So, there's a learning cycle that has to
we skip those learning
with with Juniper because we know the
architecture of the of that fabric. A
lot of our engineers were like core
chief architects on some of that in the
prior generation. So, we know that.
That's one aspect of it. If you look at
the Helios system from AMD, they they
needed to get to this quickly. So, they
are now tunneling
U-Link kind of
packets through
standard Ethernet kind of network.
Uh so, now you think about, you know,
typically when you move data over any
link, you have to think about, okay, how
much space is used by headers,
addresses, and all those other stuff.
And then how much is payload? Because
what matters is how much payload? And
how long does it take to transmit the
payload?
So, all of these things
are important elements in our choices.
The other thing is as a startup,
uh
if you carry the burden of building
silicon, but also carry the burden of
building a system, then you have to
qualify the system. The system has to
have reliability characteristics.
There's all of these other things that
now
affect your time to market.
So, by partnering with HP Juniper
Networks, we can leverage an existing
shipping system that's shipping today
from the Flexus factories in Penang.
So, we get to get to we get to take our
our silicon
integrated into and transform a router
into a compute box, and get to market
faster with a reliable scale of fabric.
So,
I honestly believe, hand on heart,
that
NVLink is the first NBL-72 is the first
scale of fabric in the market.
We will be the second vendor in the
market with a true scale of fabric.
Right?
Uh that has exceptional latency
characteristics. Now, what is the
latency? It's between 1 to 2
microseconds. And this is, by the way,
I don't know for a fact, but this is
what I've heard anecdotally, that
typically
the NVLink fabric has some latency
characteristics that are not amenable
to, for example, decode performance. So,
maybe there
there's some refinement that needs to
happen with NBL72 in future generations.
So,
net-net, as a result of that, we end up
with a system that's really
well-balanced
and can do prefill really well, but can
do decode really well, too.
So, you don't have to have
uh you know, these heterogeneous systems
that have to appear to solve this high,
what's called interactive kind of AI
needs of today.
&gt;&gt; Yes. Yes. Okay, great. Let's go into
that thread, too. So, there was the era
where it was just like use, you know,
Hoppers for inference, and then Grace
Blackwells for inference, and then um
some early AI ASIC startups who started,
you know, well before LLMs,
um namely Groq and Cerebras, have S-
SRAM-heavy
um
designs that worked in the inference
world for high interactivity, decode
very fast. Ultimately, of course, they
had their own tradeoffs of uh you don't
have HBM, you have to chain together,
you know, tons of these to get enough
memory. Um
And then, recently, in the last, you
know, 12 months, basically, we've lived
in this world where it's like, okay, if
you want really high interactivity, you
can use an Nvidia system with Groq. Um
and then that lets you extend that
Pareto curve to the very high
interactivity, low throughput, but high
interactivity.
&gt;&gt; Yeah.
&gt;&gt; And, you know, we've seen AMD uh partner
with Cerebras. Um AMD also bought uh
Talos recently, which is different
conversation. But, um so, there's we're
kind of in like phase two. Phase one was
just run everything on a GPU. Phase two
is disaggregation, split prefill and
decode, put prefill on the GPUs, put the
decode on the SRAM-heavy chips. Um
And then, you're kind of hinting at like
this next era beyond that, where I, you
know, I think Tensor Dine is aiming and
and so are some other AI ASIC startups,
um, which would be actually can you just
use one uh chip to do both workloads,
prefill and decode? And so so but tell
us more about that cuz it feels a little
counterintuitive because because you
know, as you said, you know, prefill may
be compute bound, decode is decode is
memory bandwidth bound. So, how does
like one chip do do both?
&gt;&gt; Really good question there, Austin. So,
uh
So, let let's go back maybe
10 months back. So, something happened
towards end of last year, right? Uh
GPD 4.5 got really good and then
suddenly people started seeing, wow, the
code it's generating is functional. I
don't have to debug it a lot. And then
comes uh you know, GPD I think 5.3,
correct me wrong. And then uh Opus 4.5,
right? And uh so, suddenly the demand
for AI goes through the roof.
And what are those models? My gut My gut
says they're over 2 trillion parameter
models.
So, there's a realization in the
industry that those models
cannot really work at a high in high
interactive environments where the
developers are saying, "Listen, I need
code faster. I need everything faster."
And
so, the reaction of the industry is
well,
we have great systems for training. They
do prefill really well.
And you know, uh kudos to the Groqs and
Cerebras of the world that have already
shown for smaller models like Llama 70
or GPT-OSS 120B, high tokens per second
per user. So, now comes the problem
statement. Like, I have a system that
does really well in prefill, can be used
for training, but now let's talk about
inference only. Now, I need to uh pair
it with a
a system that has a lot of SRAM and has
low latency and I can do decode faster.
So, I think that is an intermediate
solution from these vendors, whether
it's Nvidia plus Groq or Amazon Tranium
plus Cerebras or Helios plus Cerebras.
&gt;&gt; Mhm.
&gt;&gt; Uh
Imagine, you know, nine racks or 14
racks to run a two-trillion-parameter
model.
Imagine trying to build a compiler that
compiles in CUDA for a for a Vera Rubin
and not CUDA for a Groq system.
&gt;&gt; Yeah.
&gt;&gt; And then imagine connecting them with
lots of Ethernet switches because you
have to hook up these chassis together.
So,
uh
that is an answer to the demand of the
market, right? Because the demand from
everybody else is that we want to run
these two-plus-trillion-parameter
models. And now, if you look at Kimmy
K3's, 2.8 trillion parameters.
Uh but we need
we need high token, you know, in the
agentic world, you want high token
rates, for example, token per second per
user. Here, the user could be human or
could be an agent for all you care.
All right. So, now let's go it back to
what did we do at TensorDyne?
So, when I look at silicon real estate,
there's only so much space.
Now, if my compute takes less space,
what does it free up? It frees up space
for more SRAM.
&gt;&gt; Mhm.
&gt;&gt; So, now you
Imagine now a chip that has more SRAM,
kind of like the Groqs and the
Cerebras's of the world,
but also has HBM,
and has the compute capacity of an
Nvidia or AMD.
So, you get the best of both worlds. You
get what's called
uh you know, you can do high throughput,
but you can also do high tokens per
second per user uh with the same system.
Uh why? Because ultimately, what you
want to do is when you have compute,
what matters is
I know, model flops utilization, MFU,
for example.
Well, if you have a lot of SRAM adjacent
to, let's say, a computer array,
you can keep that computer array really
busy.
And you can hide the latency of getting
data from HBM.
So, if you have a lot of SRAM, you are
not penalizing yourself by stalling your
computer array every time you're going
to fetch data or activations or weights
from HBM.
So, we start getting the kind of unique
properties of both of best of those both
worlds.
But, that's necessary, but not
sufficient.
Because now suddenly there's
communication now that now these models
also have.
So, you know, you got to compute, then
you got to communicate, then you got to
compute, then you got to communicate.
And this rhythm of compute communicate
or expert selection now,
the communication starts becoming a
dominant effect on latency or through
throughput or tokens per second per
user. So,
our good fortune was to stick with log
math, have the power characteristics,
not blow the silicon, you know, you
don't have to build a chip that's
vertical size to achieve the performance
uh that that's on par with others. And
then suddenly you get the benefits of
both of these.
So, now you have a great machine for
prefill and decode.
&gt;&gt; Ah, yes, yes, yes. Okay, so the key
insight is by using the logarithmic Mac
math that we talked about earlier, the
compute doesn't need to be radical size,
it can be smaller. So, then the question
is, what can you do with the rest of the
silicon? And oh, we can have even more
SRAM, for example. So, you can have a
lot of compute, a lot of flops, you can
have a lot of SRAM, which is great for
decode. Um but then you can still also
have HBM for prefill and it's having HBM
in general, um KB cache, that kind of
thing.
Um and then you also feel confident in
the competitiveness of your scale-up
network. So, as you're communicating
between all these things, you feel
competitive there, too. So, ultimately
then, um if I have a rack of Tensor Oh,
which And by the way, we'll touch on
power, too. But my first question is, if
I have a rack of TensorDyne chips,
is it, you know, 72 chips in your rack?
And if so, like, do you still sort of
split pre-fill and decode amongst them
within the rack?
&gt;&gt; So you know, immense flexibility. So
first of all, we are building the
TensorDyne system is only 13 rack units.
So it's a tiny It's 1/4 of a rack. We
can put four of them in a rack.
At 1/4 of a rack,
think of our system, it has 72 chips in
1/4 of a rack.
That's point number one. Secondly, it
consumes only 30 kilowatts.
So if you want to comp- do apples to
apples, the comparable system is like a
Blackwell GB300.
So 1/4 of a rack,
one full rack.
30 kilowatts, 150 kilowatts. So
how do we do that?
So first of all, we leverage the Juniper
air-cooled system, so it's not
liquid-cooled. Secondly, we have a
scalar fabric that has the
characteristics that are necessary for
these multi-trillion parameter MoE
models.
Thirdly, our log math allows us to have
silicon that consumes much lower power.
&gt;&gt; Yeah.
&gt;&gt; And so you get you get you know, you get
multiple benefits that are compounding
in nature
that now allows us at a
uh you know,
to have performance at the
you know, GB300 Blackwell levels in a
1/4 of a rack.
&gt;&gt; Ah.
&gt;&gt; The second thing is that because we have
the scalar fabric has these elegant
properties,
you can you can do you can put some
chips on pre-fill, some chips on decode.
Or in a full rack, we can basically say,
"Okay, there's one of our pods is a
pre-fill pod, and three pods are decode
pods."
&gt;&gt; Mhm.
&gt;&gt; But ultimately, if you look at it,
because of our characteristic nature of
our
any-to-any scale-out fabric and the
characteristic nature of keeping a
keeping a very high MFU because the SRAM
keeps that you know, I always refer to
it as the compute dragon. Keep the
dragon fed because the dragon is hungry.
You got to keep it, right? You can't You
can't let it off. So, you keep the
dragon fed. Now, you get a system that's
so much more balanced and can can
perform really well. And in some of our
metrics, now we are yet to power on our
system, but in a some of our sense, we
think that we could have advantages in
the order of almost a magnitude over
the latest greatest systems in the
world.
&gt;&gt; Wow. Wow. Okay, I'm going to reflect
this back. So, it feels almost too good
to be true.
So, you can fit 72 in a quarter of a
rack. That's only 30 kW. You can stack
four of those in a rack. Um
so, 120 kW or so. And then it that whole
rack is air-cooled, right?
&gt;&gt; Yes. Yes. So, you could deploy it in
brownfield data centers, existing data
centers.
&gt;&gt; Yeah. So, imagine, you know, if you look
at it, we have data centers around the
world. You know, some of these
hyperscalers have 400 data centers
around the planet.
You They're not liquid-cooled.
You can't retrofit them, right? They're
in Some of them are in bigger cities or
in countries where you don't have enough
power.
But you want to get AI around the globe.
How are you going to do that?
So, our system is because it's a Telco
rack, it's 19-in wide, it fits in AT&amp;T,
Verizon, Deutsche Telekom, NTT, New York
Stock Exchange. That rack is perfect for
being used in anywhere in the world.
&gt;&gt; Yeah.
&gt;&gt; So, suddenly you can get that benefit.
The other is that you can imagine
building smaller data centers, but
having the performance characteristics
of a large data center. So, imagine, you
know,
you know, with our system, you can
actually get You might need You can get
the
You can get like 1/8 the power. You You
get
uh you know, you can have a data center
that's similar to a very large data
center with the latest systems from our
biggest competitors.
&gt;&gt; Yeah.
&gt;&gt; So, now you can deploy them in smaller
locations, smaller cities. You can put,
you know, 20 30 kW kind of data centers,
not needing a gigawatt data center, but
having the performance characteristics
of a 200 MW or 500 MW data center. So,
you get all of these benefits, too good
to be true, but, you know, if you build
systems, you know, you you have to know
the system characteristics and system
performance before you build it. You
don't want to discover it in the lab.
So,
&gt;&gt; Yes.
&gt;&gt; So, we spend a lot of time at this,
simulating everything.
&gt;&gt; Totally. Okay, very interesting. So,
then my mind naturally goes to a couple
questions. One, who are the target
customers? Because on the one hand, I
think of like enterprise um
because it can fit into existing
enterprise data centers. And maybe
instead of needing to buy, you know,
nine racks or 13 or however many, you
know, maybe they can buy one for their
needs or or a few or whatever. Um and
then two, yeah, timing. So, um you know,
I think you had mentioned that this
isn't totally taped out or stood up or
productionized or something. So, yet
remind us like so, tell us who are your
your target customers? Because of
course, I can also see, yeah,
hyperscalers in the model labs and and
stuff being just as interested. Um and
so, maybe like target customers, route
to market, and timing.
&gt;&gt; Yeah. So, um
our target customers are certainly
number one hyperscalers. Number two, uh
a lot of the neo clouds. We have
significant number of letters of intent
from almost all the neo clouds in the
world.
Uh well, I want to clarify, neo clouds
in North America and Europe. Um
and and then uh maybe some sovereigns
and some enterprises, right? So, but as
a startup, you have to be laser focused,
right? We don't have a very large sales
team. So, we have to focus on uh If
Doggett has of customers, and we're
doing that.
Um the second question was timing,
right?
&gt;&gt; Yeah, yeah, yeah.
&gt;&gt; Uh so, we've taped out our 3 nanometer
chip with our uh awesome partner
Broadcom. And so, we expect devices back
late October, early November.
And we expect to power our system and uh
and then, you know, probably sometime in
Q1 start doing beta with customers. We
have some customers have signed up for
beta.
And then,
potentially go into production, early
production sometime in end of Q2, early
Q3 next year. So, we're not far away
from there. Now, how can we do that?
Because 80% of the system is already
validated, uh qualified, certified in
like 70 countries.
&gt;&gt; Sure.
&gt;&gt; We're We're building it out of the same
factory.
Uh so, uh in in Penang, Malaysia. So, we
can actually quickly go from power on to
qualification to certification
to shipping uh of our system. So, we
have our work cut out uh for the next, I
would say, 10 months. But, uh we're
fairly confident that we can get from
here to there pretty rapidly.
&gt;&gt; Nice, nice. So, is that because you're
riding the supply chain that Juniper was
already riding, or is this the advantage
of partnering with Broadcom, or both?
&gt;&gt; It's both. So, you know, Broadcom is one
of the largest
consumers of TSMC capacity, both TSMC
and HBM capacity, right? They have a
deep partnership, and we have a
exceptional relationship with the
Broadcom team.
They're great friends and great
supporters of us, and
uh and so, we designed of of course, our
front-end design is ours, but the
physical design and the partnership with
TSMC is a Broadcom led.
Uh so, that's one part. So, that means
that from a supply chain perspective, as
long as we forecast uh well in advance,
we can get uh parts from Broadcom,
right? That's part number one, uh
qualified tested parts.
The second part of the story is that can
we get to volume with our systems? And
this is where the partnership with HPE
Juniper Networks and the fact that
things are shipping out of a Flex
factory and Flex knows how to build
these systems in volume gives us those
advantages.
The third most important part is that
these systems have to be reliable
because you're running business critical
AI now in them. So
uh
Juniper's routers and HP Juniper's
routers are carrier grade. They're
something called five nines of uptime.
So five nines of uptime, if one were to
Wikipedia it, is that the system cannot
be down for more than
5.7 odd minutes in a year or 680
milliseconds in a day.
So that is a reliability characteristic
that we leverage uh from our partner
uh and so we are able to we will be able
to deliver systems that are reliable
uh and can run the largest models in the
world, right? At 2.8 trillion parameter
like a Kim E3 or a Gwen or uh from the
Frontier labs, their biggest models,
right? Uh our systems have adequate
amount of memory, you know, if I if I
look at the quarter rack system, we have
we have 10.8 terabytes of HBM capacity.
We have uh
you know significant, I would say over
18 gigabytes of SRAM.
&gt;&gt; Wow.
&gt;&gt; So imagine we have SRAM capacity of the
the big SRAM guys and we have DRAM
capacity of also the largest I think. So
now
uh you know, better than KB cache and
agentic workflows, we we're well set up
for those system uh for those markets
and those customers.
&gt;&gt; Mhm. Mhm. Fascinating. Amazing. A really
nice way to punch above your weight, so
to speak, as a startup by kind by you
know, partnering with people who can
help bring you along. Um
when you mentioned Flex, by the way, is
that Flextronics? You
&gt;&gt; It's Flextronics.
&gt;&gt; Yeah, yeah. Okay.
&gt;&gt; Yeah. And and you know, I mean uh most
of Silicon Valley thrives on
partnerships, right? You can never go
alone, right? Whether it's silicon
partners, system vendor partners,
uh
the ecosystem actually lends itself to
that partnership. And we we uh
you know, we benefit from it. We
mutually benefit from it. And we we
really love these partners because they
are helping us get to that scale, will
help us get to the scale. And they're
very supportive of us, right? They're
supportive of a startup. Not only that,
HP Juniper Networks is an investor in
the company. So, you think about it.
They uh
they, you know,
in in all of these things, you know, you
can never go it alone. It's like
building a team, right? In the company,
the team is multidisciplinary, but you
can't build a product by yourself. All
these functions come together. It's the
same in the ecosystem of
uh
of vendors and partners who come
together to build these uh solutions.
&gt;&gt; Yeah, sure. That makes sense.
&gt;&gt; And cu- cu- And customers are the final,
you know, arbiter of product, right? And
we we customer validation's going to be
super important for us over the next
many months.
&gt;&gt; Yes, totally. Okay, so let's let's land
the plane there, customers. So, you
know, you mentioned uh really ramping up
in 2027 with customers, beta, and then
production. Um the one thing we hadn't
touched on yet with software. So, you
know, for those model labs, those
hyperscalers, what does it look like as
far as how heavy of a lift is it to
take, you know, your system and get
their software their frontier grade
software up and running?
&gt;&gt; Yeah, uh exceptional question, uh
Austin. I think
a few things have happened, right? One
is that
from the signals of
dis- disaggregated stories, we
understand that the moat of CUDA don't
exist anymore for inference because
we have proof positive of a number of
inference companies running solutions
and then these disagree solutions with
CUDA and non-CUDA or neuron and
non-neuron or ROCm and non-ROCm, right?
So, we have this.
So,
uh
I think there a couple of things that
have helped us. Uh one is obviously we
have to build a robust compiler for our
hardware,
but also at the higher layers having
a technology that can take PyTorch or
Triton kind of models and then convert
them quickly and compile them quickly is
super one of which you spend a
significant amount of time. So, for
example, in our engineering
organization, almost 60 to 70 60 plus
percent is software, right? Because you
have to have a software team that do
does that.
But one of the things that's happened
with this beauty of uh these new Opus
4.5 and and uh you know, GPT 5.6 and
other models
is that the agentic workflows are now
proving that you can take kernels
and quickly get them ready for your
hardware.
&gt;&gt; Yeah.
&gt;&gt; So, we have
incredible momentum on taking like the
best models in the world and quickly
getting them running on our you know, in
our simulators and then eventually in
our hardware. So, the the walls for
taking new architectures and new systems
are quickly crumbling when it comes to
software because you can take models and
because you have all these workflows and
automated kernel generation capabilities
that you can actually get to there get
to that
and also get to high what's called
utilization of our systems quickly. That
means that you can get first proof
positive that the model works on the
system and then you can iterate quickly
to get the model performance up in the
system. So, both those things seem to
coincide with uh you know, our systems
coming on.
&gt;&gt; Yeah. Yeah. What Yeah, what fascinating
timing um with the rise of the agentic
AI to kind of help you with that that
last hurdle that people are a little
concerned about, you know, am I going to
have to spend a lot of time, not to your
point, not only getting my code to run
on this new system, but also optimizing
it to get the most utilization out of
it.
&gt;&gt; Indeed. Indeed. And that's super
important because, you know, you don't
want to 800 horsepower car and get like
50 horsepower out of it, right? Because
then you're leaving stuff on the table,
right? You're paying for it, but you're
not using it.
&gt;&gt; Right.
&gt;&gt; And we believe that we have we will have
some of the best MFUs in the industry
with our system.
&gt;&gt; Nice. Amazing. Okay. Well, we're at
time, folks. I hope you learned a lot
about RK and Tensordyne and networking,
a lot in logarithmic math. We covered a
lot of ground here. RK, you'll just have
to come back and keep us updated, you
know, as you guys get closer to
delivering ships
chips and systems and when you're you
have customers to talk about, you know,
can't wait to hear more.
&gt;&gt; Austin, again, thank you for the
opportunity. Thank you for, you know,
the very thoughtful questions.
And, you know, and navigating all the
different parts of the terrain
on our behalf. And, you know, we'll
certainly keep you in the loop. We'll
keep you posted as we make progress, as
we bring up our systems, as we get to
beta.
And
would love to come back and tell you
about our our success and our progress.
Again, like I I want to again give
credit to my broader Tensordyne family
because we we won't be here without the
the complete dedication of a number of
people. And then most importantly thank
our partners, Broadcom, TSMC, HP,
Juniper Networks, and Flex, and others
because we can't be here without any
without all of them helping us in this
journey. So, thank you, Austin. I really
appreciate it.
&gt;&gt; Yeah, team effort, very cool. All right.
We'll talk We'll talk next time.
&gt;&gt; We certainly will. And my best to you,
Austin. Thank you.
&gt;&gt; Thank you.
&gt;&gt; Cheers.
