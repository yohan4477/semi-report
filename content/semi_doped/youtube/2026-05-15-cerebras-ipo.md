---
source: https://www.youtube.com/watch?v=SVwpN-pfpg4
vid: SVwpN-pfpg4
title: Cerebras IPO
date: 2026-05-15
duration_sec: 3036
channel: Semi Doped
kind: transcript
---
Each wafer consumes about 23 kilowatts
of power. That's like enormous. Like if
you think about a onevolt supply that is
feeding these GPUs, you're talking about
something uh in the tens of thousands of
amps of current that have to flow into a
single wafer.
Hello listeners, welcome to another
semi- dope podcast. I'm Austin Lines of
Chip Strat and with me is Vic Shaker
from Vick's newsletter. So Vic, we're
recording this. It's the morning of May
14th, Cerebrris IPO day. What do you
say? Should we talk about Cerebras?
&gt;&gt; Yes, it's all about Cerebras today.
That's it. Nothing else. Single focus
topic. No deviations.
&gt;&gt; Totally. I love that. Which, by the way,
I don't even know how to pronounce it.
Cerebras.
&gt;&gt; I don't know. Cerebras.
&gt;&gt; Cerebr. Cerebras. Yeah, whatever.
&gt;&gt; How do you say cerebral,
&gt;&gt; right? Yeah. Cerebral. Cerebras. Yeah,
totally. So, listeners, you know who
we're talking about. the big wafer
company.
&gt;&gt; Yes, those guys.
&gt;&gt; All right, so let's see. Okay, so they
price their IPO 185 bucks and they raise
5.5 billion, I believe. I was looking at
it this morning to see like if the stock
price is immediately like bouncing
around and stuff, but I it was just
pegged at 185 as far as I could see. So,
I don't know if there's some price
discovery thing that happens early in
the morning or what.
Yeah, this was an insane IPO because uh
I I've it was overs subscribed massively
and they used like an eBay bidding style
approach where they were like okay how
many shares do you want and at what
price are you willing to go up maximum
pretty much like eBay does and then
people were like putting in those orders
it's kind of insane then what happens is
like Bloomberg reported that
uh ARM and Soft Bank came in last minute
and tried to buy it at the 11th hour.
Typically, like like an eBay snipe, you
know, you come in last minute with your
bid, the eBay snipe. Didn't work anyway.
Didn't get bought. But it was I've been
tracking it all all week and it was
initially it was like, oh, it's going to
be priced at 135 and I saw it was going
to be a price at 150 to 160. Finally, it
came out to be 185. I believe they were
intending to raise like 3.5 or 4
billion. Anyway, came above came out
about one and a half billion above that.
It's insane.
&gt;&gt; That is crazy, man. Uh yeah, good. You
know, congrats to everyone who has
equity in that the team and all the
venture capitalist. So, what do you say?
Should we remind listeners at just like
the highest level like what Cerebrris
builds? Yeah, there's some uh technology
and history behind this whole thing
which is an interesting discussion that
we can have at least for me because I'm
such a technology-minded person. Um so
let's let's go get into it. Right. So
this uh wafer company that we were
talking about cerebrus, right? The
reason we call it the wafer company, the
guys who make the wafers, is because
typically how wafers work is just like a
giant dinner plate and then you got like
many many little GPUs on it and at least
this is what like Nvidia does. So they
take out all these GPUs and package them
separately. They just cut it out of this
dinner plate and they package it and
they ship it. You know, that's how
typically GPUs work. But Ceras was like,
why do we have to cut up this stuff? We
want to keep the whole wafer as a single
chip. So all those chips that you would
have otherwise cut out, they just hooked
it up together with metal lines on the
wafer. And that's how it, you know, came
about. And they were like, okay, now
this whole wafer is a chip and that's
that's about it.
&gt;&gt; Mhm. Which I will say it's pretty
intuitive in the in that if you look at
like Nvidia's road map, it was one die
per chip and then it's like, oh wait, we
want to scale bigger, so let's have two
dies. So you're you're taking this
wafer, you're dicing it up into
individual dies. It's like a
checkerboard and you're cutting out all
the little checkerboard squares, but
then all of a sudden they're putting
them back together and then they want to
go to four dyes, you know, and you can
imagine a world where people want to go
to eight dies. And so like in the long
run, and by the way, when you cut these
up now, they have to communicate with
each other. If you if you're lucky, you
can stitch them together and it feels as
if they're one piece of silicon, but
otherwise now you have to go networking
and even switches and whatever. So like
conceptually, I think everyone can
understand like, oh yeah, don't cut it
up, leave it all on silicon, let it
communicate all with each other, have,
you know, better network bandwidth, etc.
&gt;&gt; Yeah. So that's the that's the whole
idea of this and the beauty of this is
that uh you can fill all of these chips
with like SRAM in it and since SRAMM
based accelerators are so much faster
because the memory bandwidth is like so
amazing uh you can get the entire wafers
worth of SRAM for inferencing which is
amazing uh in theory right for certain
use cases which we'll talk about it's
amazing um this whole wafer if you look
at the wafer scale GPU that we're
talking about it's about the size of I
would say it's like 60 Nvidia H100s
right and uh it consists of about 84
reticles which is like basically that
one shot that people were cutting out
right it contains about 84 of them
stitched together uh in a grid format
and so this is a piece of engineering
and we'll get into why that is so
amazing now for anybody who's dealt with
these wafers and you know dealt with
silicon technology before is one thing
is very clear you can never make a
perfect wafer in a wafer is always going
to have defects and that's why you
always hear people talking about yield
or what is the yield of 18A and how that
means how many defects does this wafer
have lower the better and every wafer
has them there is simply no way to avoid
uh this this whole defect thing and so
now so what does that mean for cerebras
like how come how come the cerebras
wafer is defect free no it has defects
and the way it works is now instead of
these giant GPUs that are there and
stitched up which is the analogy we use
to just explain the idea in reality each
of them are actually very tiny they're
not as big as a GPU each of them is like
much much smaller it's like 100 or 120th
of a GPU in size and these are their
like processing cores right they
basically have a little bit of
processing and a little bit of memory
each one little bit little bit these
little thingies are the ones that are
like ultimately all connected together
in in the whole wafer. There are about a
million of these things. Okay? And out
of the million
the exact number is like 970K or
something. Anyway, simply just think
about it as a million. Out of these
million, about 900 of them are the ones
that are actually working at any time.
900,000.
And the reason it's 900,000 is because
you have to overcome these defects. So
whenever they figure out that this
particular core has a defect in it, what
they do is they have a fabric networking
fabric that is on the wafer and all they
do is they just route around it like oh
this chip is bad. So let's just go to
the spare spare one right above it and
we'll route around it. Like we'll hook
up the wires just avoids the defect. So
they look at a wafer. I don't know how
they do this by the way. Do they inspect
every wafer? Because every wafer has
different defects. Anyway, they look at
a wafer and be like, "Okay, like this
this this this this, you know, these
processing cores are all terrible. Let's
route around them." And you reconfigure
it. You get a defect feature.
&gt;&gt; Mhm.
&gt;&gt; Which has like 44 GB of onway for SRAMM
operating at 21 pabytes per second
memory bandwidth. That's amazing.
&gt;&gt; Amazing. Yeah. Two two things I want to
add in here. So for listeners, you know,
zooming you back out. Um so when Vic is
talking about yield as you know because
there's just like this statistical noise
the stat stoastic things happening you
get a dopant in the wrong place and
something might short circuit or it
might be like uh just an open circuit
and it doesn't work. If if the size of
the chip gets bigger then you have you
know it's its area. So you have like a
much more significant surface area for a
defect to happen. And so the bigger and
bigger your chip gets, the more likely
that that chip is going to have some bad
defects. And so you might think, oh
well, if the chip is the whole wafer,
surely every wafer is going to fail,
right? And what Vic is saying is, no,
no, no. They're making a wafer, yes, but
it's full of all these teeny tiny little
cores. So each tiny little core has a
tiny surface area. So pro it's going to
have fewer defects. So each core will
have good yield, but yet at the size of
the dinner plate, you're still going to
have some that don't work. And so
literally I think when they power on the
wafer they just test every core and
maybe it's maybe it's only happens once.
I don't know how often this happens but
they test every core and then yes
whichever ones don't give a signal back.
They say okay um row 10 column 13 that
core is dead. And so you just map around
it. Uh and then you just they just know
that once they run their software that
probably some sort of orchestration
system knows to not orchestrate to that
little area. Um, so pretty cool. It's
it's a it's a really interesting
innovate innovative way to tackle like
yield and and sort of like harvesting
good cores and routing around other ones
dynamically. Um, then I will say also uh
VIX SRAMM point. So there's different
ways to store memory. We've talked a lot
about memory. SRAM is with transistors,
six transistors. And so that's the
beauty of having a big silicon wafer
just full of transistors is you can
allocate transistors to memory, fast
memory, or you can allocate it to logic.
And in this case, they're allocating
about half of all the transistors on the
chip to 44 gigs worth of SRAM, which
ends up being quite a lot.
&gt;&gt; Were you saying that I think each
compute core is roughly 50/50 compute
and SRAM? Is that how it is?
&gt;&gt; I I think so. Yes. Because I think they
want the SRAML very close to the compute
core. So it's
&gt;&gt; Yeah. Yeah. Yeah, it's almost like
processing in memory if you will.
&gt;&gt; Yeah. So, yeah, that's basically the
idea. You give it this these little
cores have 50% silicon dedicated to
SRAM, 50% to compute. Have a lot of
them, stitch them together, route around
the broken ones, and you have a working
wafer that works at enormous SRAMM
speeds. Um, and it has 44GB of capacity.
Now, we have to talk about a few things.
44GB is not nearly enough to hold any
kind of thing. Okay. So that that brings
up some concerns. The second thing is um
how are you going to deliver power to
this thing? This is a big big question
because you essentially have a rack's
worth of chips on a single wafer.
Seriously, that's what it is. When you
put like, you know, let's just think
about it as 84 reticles. 84 reticles
could be 84 GPUs roughly speaking.
That's a lot of chips. Like the NVL72
only has 72 chips. So you're talking
about 84 chips um that is a rack scale
GPU count uh essentially in a single
wafer. Now you can imagine that this
requires some serious power delivery
techniques and some serious thermal
issues that have to be dealt with.
Right? So these are these are the basic
things that we have to like address um
in some some detail. I recommend that we
get to the SRAMM question and the
limited bandwidth in a slightly later.
The reason is that there's a lot of
stuff to talk about, but I'll just
mention briefly what the power delivery
looks like. Each wafer consumes about 23
kW of power. It's like enormous. Like if
you think about a 1V supply that is
feeding these GPUs, you're talking about
something uh in the tens of thousands of
amps of current that have to flow into a
single wafer. So there is no way that
you can supply the wafer with a power
connector on one side and expect all
this current to flow to the other side
of the wafer. I I I point that way, but
it's really not that big. It's a wafer
is a 12in wafer. So it's a foot like you
know that's about that big. So
but it's still a lot. You'll drop a lot
of power from one end of the chip uh
wafer to the other end. So the way they
do this is that they have these
specialized vertical power delivery
connectors that come in uh across
hundreds of points on the wafer and
deliver power directly on the you know
in a vertical way. That's the only way
you can deliver power to all these
ships. So that whole thing was like
completely uh unique to how Cerebras
built its architecture. The second thing
is cooling. They have this entire like
crazy uh cooling system that has uh you
know uh vertical flow of like
micrfluidic channels in the thing and
you have to cool the whole wafer at once
cuz remember a wafer can have hot spots
you know you've got hots up there you
have to cool all this so the cooling is
done with what they call the engine
block um and it's it's just this honking
piece of metal that has this complex
construction if you go into the cerus
website you'll see it you know It's it's
it's amazing. The whole cooling problem
is also amazing. Like you have to cool a
rack's worth of wafers in in a small
space, right? That's insane. The one
other thermal aspect of this is that the
wafer actually expands too. So not only
do you have all this problems, the wafer
expands. So their connectors are also
customd designed and patented by Cerus
themselves. They have this unique
material that goes there and controls
the coefficients of thermal expansions
in a way that things match with the
board and the connectors and the PCBs
and the power delivery. All of this has
to match. So they have like a whole
patent that Ceras actually owns on this
to just deliver power and cool it. So
that's that's my spiel on like how
complicated it is to develop a wafer
scale engine.
&gt;&gt; Okay. Wow. Yes. Okay. So fascinating.
So, first of all, you said it's not like
you can just put some power pins on one
side and route the current all the way
through, but they actually have to have
a grid um come in from the top or maybe
it's from the bottom and deliver the
power to all the little places like uh
individually and then um on top of that
getting the so that's you know getting
power in is complicated but also getting
heat out is complicated. So, it sounds
like they have to engineer some big
crazy engine block, which yes, we should
all go look at a picture to figure out
per dinner plate how to get all the
power in, how to get all the heat out.
Now, tell us very quickly when you say
that the wafer expands and you're
talking about thermal coefficient, like
tell people what that means. Whenever
stuff heats up, it expands, right?
Essentially, the wafer also expands. I
was looking at some numbers. it expands
by about a tenth of a millimeter. Uh,
and that's a problem. You know,
alignment goes out of whack. And not
only that, when you have attached it to
a a printed circuit board on the other
side, uh, and you're delivering power
through this printed circuit board,
there are different coefficients of
expansion on the printed circuit board
versus the silicon wafer. They don't
have to expand at the same rate. So what
is a a tenth of a millimeter here and
the silicon might be a hundth of a
millimeter on the printed circuit board?
Like now you've seriously got connectors
and stuff that are not going to stay
connected anymore. They're going to rip
off, you know. So that is a problem to
solve when you're putting uh that much
power and that much current through a
single wafer. Uh so they have some
unique solutions towards this. I'll just
leave it at that. Yeah, that that they
had to solve this all by themselves.
This is not a unique industry problem.
Um, this is a unique problem to them.
&gt;&gt; Amazing. So, quick question, just
riffing here. The idea of ha of having a
wafer instead of dicing it all up and
then packaging and connecting
everything. At first, it sounds like,
oh, it's actually going to be a lot
cheaper and then you can yield harvest
correctly and everything because you're
not processing one, you know, 20 $30,000
wafer, chopping it all up, packaging it,
interconnecting it. Um, but on the other
hand, you're talking about these there
are different tradeoffs like, okay,
great, you've got the big wafer and it's
full of all these pro 900,000 harvested
processing elements. Um, but it's really
complicated uh from a mechanical and
thermal and power delivery perspective.
Do you know like how does that impact
the cost? Like this big engine block
thing must not be cheap. So is it is it
kind of like you're not it's not like a
cost advantage one way or the other.
&gt;&gt; I don't think this whole thing is about
cost at all because all those processes
exist. Yes. uh but ultimately the
engineering and if you think about the
nonrecurring engineering NRE costs to
develop something like this including by
the way we didn't mention just stitching
different reticles together is not easy
because it requires patterning slightly
differently because the mask when you
pattern a reticle only has a a shot that
is a certain size That's why chips are a
certain size because the shadow it kind
of casts on the wafer is a certain size.
So if you have to connect chips up
together that itself is a manufacturing
complexity that they have worked out
with TSMC over the last decade. Right?
So this is right from the get-go a
non-standard wafer fabrication procedure
all the way through the power delivery
cooling expansion mechanical problems
everything and is is is challenging.
This is a very hard problem CERS has
solved. It is you know kudos to them and
we'll get into uh you know how people
have failed at doing this too and it's
amazing that we now have a wafer scale
engine from a company that's working and
has gone public. Uh this is history in
itself really.
&gt;&gt; Sure. Totally. Okay. So it's it's
definitely not about cost. So, when they
started down this path at the get-go,
they said, "Hey, we're going to have to
make a ton of technical innovation to
make a wafer scale engine work uh from
manufacturing, power, cooling, all the
things. But it's going to be worth it
because it gives us a ton of compute and
it gives us a ton of onwafer memory. And
probably at the time the company
started, which was pre-Chat GPT, 44 gigs
of um SRAMM probably seemed like plenty.
But let's dive into this. We're in the
LLM era where even a small to mediumsiz
model is more than 44 gigs, right? Like
llama 70B already is going to be bigger
than that depending on how you quantize
it, but you need enough storage for
activations and KV cache as well. So, so
let's talk about like what happens in
even with inference
when you can't fit all the weights and
all the KV cache on one wafer.
&gt;&gt; Yeah, that's that's that's the whole
problem, right? If you can put a model
that's within 44GB and it runs SRAMM
based inference off of a single wafer,
uh you get extraordinary speeds. I mean,
you get tokens per second that you can't
dream of with GPU based systems. And you
can even compare it to LPU. LPUs don't
have as much as you're not talking about
a wafer level system and a single LPU
has a few hundred megabytes of SRAMM not
44 GB and you have to hook up a lot of
them together to fit a model and then
you have networking overhead all that
concern exists but uh now you as long as
you can fit a model in 44GB it's it's
great but you know you really modern
frontier models are actually much much
bigger than that so the then the
question becomes you how do to do it.
Now you have to put multiple wafers in a
rack and you have to split it up. You
have to split up the model between these
wafers and remember that
as much as power was delivered on the
whole face of the wafer the networking
doesn't work that way. Networking still
leaves through one end of the chip and
is like significantly slower compared to
the onwafer bandwidth of data movement
which is a big bottleneck. Right? At the
moment you have to go off wafer you're
in a bottleneck. That's the problem.
&gt;&gt; Gotcha. Yes. So, as long as So, you're
saying if we have a small enough model
that can all fit on the wafer, then you
can get you can unlock crazy tokens per
second that just aren't even reachable
with GPUs and maybe not even with Gro's
LPU because they only have Yeah, like
you said, 170 megabytes or something
very small of SRAMM. and and and so that
makes me think, okay, there's got to be
use cases where it's a small model and
you want it to run crazy fast, crazy
high throughput. Um, you know, so I
think of like Google rewriting ads on
the fly where they probably only need a
small model and they just need to know
like, hey, this is Austin and here's a
tiny bit of context about him. So when
you advertise, rewrite the ad in almost
real time so it still comes back really
quickly. Um, but you're saying when when
you actually want like useful enough
language models that don't fit on one
wafer, getting information off the chip,
which by the way, the chip is a big rect
or a big square essentially of a ton of
tiny little chips. Um, getting
information, you still have to get it
off the edge of the WSC somehow and o
over some network communication and into
another wafer. Have they said much? Do
you know much about how this sort of
like scale up interconnect works at all?
I don't know much about the interconnect
but one of the ways you can deal with it
is that you do parallelism which means
that you can do various kinds of
parallelism. So what that means is
basically you break up the whole problem
into uh what is called pipeline
parallelism one option which means that
wafer one handles you know a few
attention layers wafer two handles a few
attention whatever then wafer three
handles a feed forward network and then
you know you pipe it through this but
then it's not that straightforward
because data has to flow through the
pipe between various parts of the
inference process then you've got tensor
parallelism where you say okay look
we'll break up the matrix into five
parts and we'll run it across five
different wafers. Tensor parallelism and
finally you've got expert parallelism
which is oh we've got like we'll run
this expert on this wafer and this
expert on this wafer. The ultimate
benefit of running uh a wafer level
system is diminished by the fact that
you have to somehow break it up into
wafers and that you don't have
communication bandwidth between them.
&gt;&gt; That's like the fundamental uh downside
as to why it goes against the the very
basic concept of wafer scale engines.
&gt;&gt; Yeah. Okay. Got it. So ultimately the
wafer scale engine is best when
everything fits on the wafer. And you're
pointing out that well if we break up
the problem there's ways to break up the
problem into sort of subpros that can
fit within the wafer but at the end of
the day they still have to communicate
with each other. But maybe you can
overlap some of the communication and
computation by using parallelism to keep
things tightly you know into into the
wafer. But at the end of the day that is
going to be a bottleneck is this off
chip off wafer IO essentially which by
the way I think I saw semi analysis had
this great article that came out
yesterday. I tried to skim as much as I
could. You know these are like PhD
thesis that take you like a month to
read because they're so long and have a
nice big team. But I believe I saw
somewhere in there that um Cerebras was
experimenting with like wafer scale
photonic interconnects to go like oh
&gt;&gt; um it's it's hard like there's not a ton
of bandwidth between every core and
offchip. Um, but what if we put another
wafer on top and that allowed you to
route information essentially in the Z
direction or almost like 2.5D? Like you
could go up to this photonic wafer,
connect wherever you need, and then come
back down. I didn't read too much about
it, but I thought interesting. It also
sounds complicated and challenging to
take two wafers and connect them like
that.
&gt;&gt; It's already hard enough what they did.
Now you want to put like there was also
talk of like stacking SRAMM wafers on
top of this or DM wafers and bonding it.
&gt;&gt; Right. Right. Right.
&gt;&gt; Do you not want do you want do you not
have you not solved a hard enough
problem already? You want to make it
harder.
&gt;&gt; Totally. Well, okay. So, and that's an
interesting point which is like, okay,
if you're looking at all these other AI
accelerator startups, they're talking
about memory hierarchies to say like
like Maddox, we, you know, we talked
with Rainer Pope and he was talking
about like, oh, can you put um weights
in SRAMM and KV cache and HBM and other
people um Qualcomm, uh, Intel, maybe
Dmatrix, others have talked about using
DDR as like another tier of memory
storage and so the question is could
cerebras's SRAMM only wafer also use
DRAM in a way that's not just like pipe
it off this slow pipe that they have
over to some rack full of DRAM or
something and so then so you know people
postulate oh well what if you took a
wafer of DRAM and just attach it to the
compute SRAMM wafer but also my head is
like well Vic just told me that's how
power is getting in and that's how
cooling is getting in so if you're going
to start slapping other wafers and you
got a wafer sandwich like how do you
cool it all how do you power at all
sounds complicated.
&gt;&gt; Yeah. Yeah. I'm thinking of a
multistacked wafer, you know, uh
Cerebras wafer scale engine photonic
layer memory wafer and then next
Cerebbras wafer stack and then like wait
how do you power all this stuff? I don't
know man.
&gt;&gt; Throw some high bandwidth flash in
there. You know why not?
&gt;&gt; Why not? You know got to make the
problem harder. This is not hard enough.
&gt;&gt; Yeah. Right. I mean we want jobs for our
kids, right? like they need to work on
challenging things.
&gt;&gt; Yeah. Yeah. Yeah. Yeah. Yeah. We should
talk about basically what uh this means
for their business and who's going to
use this stuff really and why it's
useful or whether it's useful at all. I
think we should talk about the use cases
not the deep silicon tech. Yeah.
&gt;&gt; Yeah. All of that. But but one maybe as
a transition this is very technically
hard and you mentioned earlier someone
has tried this before
&gt;&gt; this way for scale. Tell tell us quick.
Yes. Yes. I mean this is a good story. I
think uh this is a good transition to
going to talking about business. Okay.
Because just when we said that oh this
is like super hard and you know cerebrus
has done great to solve all these
technical challenges. Oh by the way
here's some more you can solve or
whatever we're doing over here. This has
been tried before. And uh this is the
story of Trilogy Systems. Uh in the
1980s, Gene Amdal uh raised about $230
million
uh which is about close to a billion
dollars today. Uh and to build basically
the same idea that Cerebrus has achieved
today, the wafer scale engine except
that at the time it was a 2.5 in wafer.
Okay, it's a small wafer, not like this
giant dinner plate. It was a small, you
know, saucer saucer wafer. But then the
ambition like was amazing. It is like
way ahead of its time cuz that was a
time in the 1980s the Gene Amdal said
okay look I'm going to make like a wafer
scale chip why should I cut it up I want
to do it and their idea was the same
they're a bunch of smart guys so they
said you know we'll just route around
defects like cerebrros does today and
we we'll we'll make it work but anyway
the the story goes really like crazy but
they really didn't succeed okay because
the yields in the 1980s for even a 2.5
in wafer were just too low.
Manufacturing processes were not at the
sophistication that they are today. We
have figured out a lot of things in
wafer manufacturing today that actually
makes wafer scale engines possible. But
then it got crazier, right? The story of
trilogy systems got crazier. So what
happens in like early 1980s, I think
1982 is that there are these storms that
flood the factory. So, it's a it's a $33
million factory and then like water
starts seeping into the air conditioning
and all of this stuff and what happens
is the pipes start to rust and it starts
to blow microscopic dust into the clean
room and nobody knew what what's
happening to the eels like they didn't
know that this is due to water seepage
and rust that now the clean room is
getting sprayed with dust and all the
wafers are dying because of this storm
that came through. So they took months
to figure this out and they blew through
capital because it was blowing dust into
the clean room and at the end of the day
they're running out of money. So they
wanted to complete this wafer scale
engine. So they like okay let's make a
hailmary IPO. In 1983 they went and said
we are going to go IPO and they raised
like $60 million without a product in
hand. They didn't have a product. Okay.
and they used all that money to still
try to make a working wafer and just
nothing happened. And then ultimately
the public market lost it. I'm like,
"Okay, that's it. You guys are not going
to do any of this stuff." And so the
stock at the time, which was like at $12
a share, like eventually plummeted to
near zero in the next couple of years
that followed. It was like totally
terrible.
&gt;&gt; And it doesn't stop there. The story
gets even even worse, even sadder. Okay?
Because right after this like this
company getting wrecked by a product not
working because of microscopic dust
caused by rainstorms. Uh Amda like
crashed his like beautiful green
Rolls-Royce. And while all this chaos
was happening their finance guy who I've
written down his name as Clifford
Madden, he died of a brain tumor at the
height of the crisis. Like like the
whole thing is going on and he he dies
of brain tumor, right?
&gt;&gt; And so everything has run out now. So
the company was forced to restructure.
They laid off a lot of people and then
finally they kind of abandoned the idea
of building a wafer scale engine
supercomput and all of that money that
they had raised and everything
evaporated. Nothing nothing happened and
wafer scale technology was dead and
basically Amdal said
um this is not we are not in a position
to do this for another 100 years. We
cannot make this happen for another 100
years and that he used the rest of what
was money was left to buy some some mini
computer startup. Okay. And so he
pivoted out of wafer scale engines and
eventually after the whole thing you
know he he was basically defeated by the
wafers scale engine process and he
stepped down in like the end of the
decade like in 1989 Amdal stepped down
and said that's it I can so now what
cerebras has done is made that a reality
sure it took I don't know 40 years it
was not his 100redy year estimate it
took 40 years where in 40 years since
the trilogy system saga, but it puts a
little pin in history to appreciate what
we have today and what kind of
engineering that has gone behind this. I
don't know. We're probably going to talk
about, oh, it's not good enough, memory
bandwidth is not good enough, uh, it
doesn't make enough money, revenue will
not grow, their business model is
flawed. We're going to probably nitpick
at all these things, but from a pure
technology sense, it is fantastic. What
Cerebus has done is fantastic. So that
that's my story.
&gt;&gt; Amazing. Yes. And they did it without
running out of money. They made real
products. They're on the what the are
they on the wafer scale engine three. Is
that what they're
&gt;&gt; three? So they're able to fund several
iterations of this. And by the way, is
this Gene Omdal of Amdall's law? Is is
he the guy that's named after?
&gt;&gt; Nice. Amazing. Cool. Wow. Fascinating.
Well, let's hope that it's not this is
not their story of IPO and then crash to
the ground, but IPO. I don't want the
curse of wafer scale engines carrying on
anymore. We want success.
&gt;&gt; Exactly. But but let's Yeah, let's talk
about the business and let's talk about
um how they got here. So, do you happen
to know I tried to go back and and I
couldn't find early like product
positioning, but what problem were what
business problem were they trying to
solve at the start of the day? Because
to be honest, as an engineer, this feels
like a cool engineering project. Like,
hey, what if we did this? I'll bet we
could do this. I'll bet that would be
useful, but it doesn't necessarily tie
straight, it's not obvious how that ties
into like this solves a real customer
problem.
&gt;&gt; So, the one blanket answer to ask um you
know, whenever you ask why did they make
this chip before LLMs, the default
answer you can always think of is for
supercomputing.
So they figured that you can just do
supercomputing out of this and make like
a great chip that gives enormous flops
performance if you do wafer scale
engines. So that was I would imagine
their initial vision of this company.
It's always supercomputers.
&gt;&gt; Okay. Because supercomputing it used to
be tie a 100,000 CPUs together even and
and eventually maybe GPUs. But they're
saying look what whatever the processing
element is why why not tie them together
on the same piece of silicon
essentially.
&gt;&gt; Yeah. So it's an ultimately a
supercomputing play as when it started
out. Um at least that's how that's how I
think of it as maybe maybe there's
another story. I I somebody will let us
know. They always do.
&gt;&gt; Yeah. Leave a comment.
&gt;&gt; But ultimately when the
the training era took off of LLMs they
pivoted into doing training. They
figured, oh hey, let's let's do this
because you got this enormous memory
bandwidth. Actually, it is not memory
bandwidth at the time. It's the same
supercomputing problem. Like you can get
a lot of flops out of this. So why don't
we uh do training with this stuff? It's
amazing. It's a supercomputer you can
use for training. So that was the idea.
And there was a reasons it didn't work
out for training, right? Because the
CUDA expertise, this the CUDA mode was
so so amazing. People just like decided
to just go with that. And it was easier
to program. how are you going to program
this stuff? It's it's not really that
easy. And uh yeah, maybe maybe it was
just not in in the right time at the
right place for training. Um but it was
because it was not a memory bandwidth
bound problem anyway. But anyway, but
right now where we are with Cerras is
that they pivoted to inference.
inference uh and the need for memory
bandwidth during the decode phase of
disagregated inference uh is a gift that
landed in Cerebras' lab
to them.
&gt;&gt; Definitely totally agree. In fact, open
models was a gift to Grock. Grock was a
gift to Cerebras. Uh Nvidia's Dynamo and
and disagregating pre-fill and decode.
All of these things came before and the
time is perfect for them.
Yeah. Yeah. That's what that's what has
led to this moment where we can actually
do something with this. So that's that's
how we've landed up here.
&gt;&gt; So So what then is their current value
prop today? Like why why why are people
even interested? Why do people want to
invest? Why are they IPOing?
&gt;&gt; The thing is the value prop is off late
for inference engines especially since
Aquire of Grock is low latency
inference. It seems like uh LLM is
generally slow and I agree like even if
you use like cloud opus you ask it a
question it thinks for like five minutes
before it gives you some answer it's
like annoying sometimes you're like dude
I just want to know like what is what is
the capital of this and that it it takes
a few seconds to tell you whatever
doesn't matter but uh even I find myself
wishing sometimes can this be faster
like I'd really like it to be faster so
when you're doing coding or something
you it really means Time is money now
because if you have faster inference,
you can get a product out to market
better like faster and that can
translate into revenue. Uh and this is
like a race that's going on. Everybody
wants immediate results and the need for
speed has been around always like
whether you think about it networking
computer computers flops or whatever
everybody wants to go faster. So this is
the same theme around that. Um so so
essentially that's one of the things and
then there is some applications maybe
financial trading or a low latency
translation live voice translations
&gt;&gt; which I don't know like why do you need
such amazing technology to do voice
translation it's a premium technology
you know you're going to to get tokens
out of the system is going to be a
premium and the premium to token cost
better have monetary return that's why I
said financial analysis or like coding
or maybe but not like lowgrade items and
so that's the that's the whole thing and
the whole inference market also most of
us don't need this low latency inference
like I can wait another minute I'll go
like refill my cup of water by the time
I get my answer for most of the
population GPUs are just fine so I don't
know what fraction of the inference
market requires low latency inference
but it's not a lot and so this is going
to serve that market
&gt;&gt; yes yes I mean I will say you know
agents do come to mind for me which is
if businesses are starting to build
business processes where you've got
agents running off and doing lots of you
know work yes sure some of it's like
tool calls that might be network bound
or CPUbound but it does feel like once
you're starting to chain agents it's
just like a compounding problem which is
like 10 seconds and then 10 seconds and
then 10 seconds versus one second then
one second then one second you know um
but but but I I do hear you like
obviously coding it makes a lot of sense
where it's just like hey if this can go
fast and the code the developer can stay
in the flow you don't necessarily like
think hard about the architecture but
after that you're just spitting out like
JavaScript and Python like don't
overthink it just go faster you know
&gt;&gt; yeah I I refer to coding as agentic
coding I mean like I don't really ask
you to write functions or anything right
I give you just say I do this problem
and it figures out and does it and it
launches tools whatever build a database
I build a website it figures out
everything so coding is kind of become
agentic anyway now so But yeah,
essentially that's the whole point. you
want stuff done quickly and that's where
the market lies and that's why Nvidia
got a hold of Grock uh chips and then
their LPUs and they're like okay fine we
have the ability to provide low latency
inference now and the cerebus is going
to be the same thing right except that I
feel like the complexity of these racks
and uh the hardware within it I always
have a concern of like how can this
scale like when you tell me Gro LPUs are
little chips with SRAM in them and then
you hook it up on a board and you do the
regular things. I'm like, "Yeah, yeah, I
I I see that." You know, but when you
tell me you have to do all these wafer
scale engines, all these complicated
things and do it at scale, I don't know.
Can you deploy
uh 100,000 wafer scale engines in the
next year?
&gt;&gt; Mhm.
&gt;&gt; Do you have the supply chain to do that?
Is everybody prepared to generate at
that level? Um what is, you know, what
is the deployment thing? And that's
another thing we should talk about the
OpenAI deal. Like do you want to talk
about that now or do you have
&gt;&gt; Sure. Yeah, let's get into that. But
first let me just say one thing which
you actually hit on something very
important which is the supply chain and
the ability to ramp quickly which is
when you invent new technologies like
the engine block you usually have to
co-invent it with supply chain partners
and then the question is if if great you
got a prototype and now you know open
AAI anthropic Microsoft Google whoever
comes to you and they're like yeah we
would like um I don't know you know a
small data centers worth of these can
all of your supply chain partners
suddenly have this new thing that you've
co-designed with you and can they
quickly jump to the crazy volume or will
even cerebras best case scenario they
have a ton of demand but they actually
can't scale their manufacturing supply
chain to meet it so that's like an open
risk and an open question that would be
interesting
&gt;&gt; but to push back on that isn't that the
story of the entire AI data center ch
supply chain right now
&gt;&gt; 100% but at least it's components that
they already build at massive scale
Still, you know,
&gt;&gt; also at least maybe there's a chance
that at least two, three players can
build it.
&gt;&gt; The Lum's lasers are in big demand.
Yeah, sure. But Coherent is saying,
"Yeah, we can build it, too." Something
like that, you know.
&gt;&gt; Yes. Yes. Yes. Exactly.
&gt;&gt; Happras
too.
&gt;&gt; There you go. There you go. Yeah.
Interesting. Okay. So, yeah, let's get
into the open AI thing. So, um you know,
uh Nvidia has Grock and that allows for
fast inference. uh you know OpenAI says
hey fast inference that's awesome we
want that they're working with Cerebrris
um have you looked much into the terms
of the deal and and clearly this is like
the big customer that Cerebrris is using
to go IPO because previously when they
tried to IPO openAI wasn't they didn't
have the relationship with OpenAI and so
it it to be honest it felt a lot
sketchier where it was just like oh
you've got a big sovereign um investor
and also cloud buyer and you're trying
to IPO on that that didn't really feel
like an actual business validation that
it was a sound business and you had
product market fit but but with open AI
it's a bit of a different story but it's
still customer concentration so like
what's your read on the open AI deal
yeah so the open so the one thing is
that I like the Grock deal in a sense I
I still think Nvidia paid a lot of money
for it you can't change my mind okay
it's like overpaid fine whatever they
got it they have a lot of money good so
the thing is that they have the hardware
they have the compiler team uh they have
their rest of their ecosystem. They have
CUDA, they have their GPUs, they have
their Rubins or whatever and all the
pieces are in place for all these things
to work together and work nicely. So
when Nvidia provides a low latency
inference solution, I can actually kind
of see how it works. Uh what the OpenAI
deal is a little bit different because
OpenAI is not really buying cerebrous
hardware. They never said give me your
wafer scale engines. I'm going to build
a data center out of it or you know
anything like that. They're actually
paying for compute time. They become
they're basically saying I'll pay you
for tokens and that's completely
different because now uh you know there
are some terms of the deal like yeah
they get some warrants and uh I I don't
know I wrote a whole Substack post on
this with all these things in it so you
can see it there. I don't want to go
into those number details it's too
boring. Uh but um basically the idea is
that uh OpenAI
is uh going to give uh Cerebras
uh money for buying tokens from them and
that's about it and Cerebras is
responsible for manufacturing, building
data centers, running their cloud
service, providing AI tokens, all of
this stuff. And they are not actually
selling any hardware. So that is I mean
this token factory business is expected
to grow but I just feel like it's a lot
of trouble. Not only do you have to make
this complicated chip and handle the
supply chain around it and now you got
to build out data centers run run your
own um become a neocloud you know it's
&gt;&gt; yeah yeah yeah exactly interesting
fascinating so presumably Cerebrus has
like some sort of little cloud because I
remember Grock did this like you know
they were the they had their chips but
then the best way to show it off when
the open models came out was to be like
oh wait let's actually build our own
little cloud and have an API and just
tell developers go hit our API you can
see how fast it is And I think that most
other AI accelerator companies went and
did the same. Sabbanova maybe and and I
assume that Cerebras did. But do you
know like do they they must have some
some experience of running their own
cloud at a very small scale.
&gt;&gt; They do have
uh a cloud service I believe but in any
case it's not something that you can run
at scale. uh yes you're talking about
open AI kind of scale now where people
are going to use codecs uh and you know
do coding jobs on this low latency
inference it's it's a lot and you're
going to have to provide that at scale
so that's that's the only thing why do
you have to also make all this
complicated hardware and also act as a
neo cloud is a lot of no you make a
great point which is like look I if
Azure if Microsoft bought cerebras I'd
say oh okay Microsoft knows how to run a
cloud at scale. They know how to run um
OpenAI workloads at scale. They've
worked together on all of that. They
will know how to take Cerebrus'
hardware, fit it into the Azure cloud,
deal with SLAs's, all that stuff, and
then Cerebras can just focus on probably
the hardest thing, which is what's the
way for Scale Engine 5 that can support
long context length, KV caching, world
models, all this stuff. But to your
point, it's like no, no, no. Now, yes.
Uh, Cerebras now needs to also be the
Microsoft Azure style partner for
OpenAI. That sounds pretty challenging.
&gt;&gt; Yeah, it's like a whole another. That's
the thing. So, let's see. Let's see how
they do, honestly. Um, I'm not I'm for
it. I'm not anti- anything, but I just
I'm just talking about some of the
things that I find it's like really
difficult to do and that they're really
continuing to solve the unsolvable. I
hope. So, we'll see.
&gt;&gt; Totally. Well, hey, they've got $5.5
billion to go hire some more people. How
about that?
&gt;&gt; Yes, let's do that. Yeah,
&gt;&gt; you got the money now. Make it happen.
&gt;&gt; Let's go. Um, okay. Any any last
thoughts before we close?
&gt;&gt; No, I I feel like uh this is only now
starting to get interesting. There are
so many people in the SRAMM inference
game right now. We've only seen the LPU
now and we've seen uh the cerebris which
was I think it is expected that cerebrus
was going to be next. A lot of people
were talking about this.
&gt;&gt; Then you have so many others. You have
Samonova, you have Maddx that you you
spoke to Raina Pope, you have Talis, you
have uh the other companies like Sohoo.
&gt;&gt; Yeah.
&gt;&gt; Tense Torrent.
&gt;&gt; Edge. Tens torrent. Um, Fractal just
raised $220 million yesterday. Um,
there's a lot of people playing in the
space. Dematrix, you know, so I think
&gt;&gt; uh to be honest, I have always been
bearish. Uh, the companies that designed
their systems prior to LLMs because of
course they just didn't know what
trade-offs to make. So be I was bearish
Grock and Cerebras, bullish these post
LLM style companies. But um the nice
thing is gro and cerebrus live long
enough to be kind of in my opinion at
the right place at the right time and to
say we've got low latency options. They
might not scale the greatest. Um we need
to work on our roadmap to continue to
iterate toward the demands that LLM
inference places on us. But we're here
and as you've said with CPUs, the best
CPU is the one you can buy. And you
know, the best AI accelerator is the one
you can buy, which now you can kind of
get maybe you can buy TPUs, but before
you couldn't, so this was your only
option. And of and of course these are
different than architecturally than than
TPUs, but to the MaddX and the etched
and the fractals, you still can't really
buy them, you know, at scale yet. So
this is the sweet spot in the moment in
history and time for Gro and Cerebras.
But again, that just opens the question
about like what happens when these other
players come to market. Does it not
matter at that point for Gro and Strius
because now they have partnerships and
customers and they're already embedded
or is it competitive pressure where
suddenly the shortcomings where they
have trouble scaling. Um they maybe now
all of a sudden you were the only one
that could do a thousand tokens per
second, but now there's 10 people who
can do a thousand tokens per second and
maybe they can support other things that
you can't.
&gt;&gt; Yeah. And we live in the wild west of
the inference world. And looking back 10
years from now, we'll talk about this
moment and be like, do you remember that
time when like this company was doing
this wafer scale engine and Grock was
there was a company called Grock who
just decided they're going to do
everything deterministically with this
very large instruction word. And then do
you know that Samanova was a you know a
company who was trying to put like all
SRAMM HBM and DRAM all together because
why choose or like no no two companies
ever did it the same and then there were
companies who were trying to etch it
literally hardcode LLMs onto chips like
what were we thinking? That's what it
seems like we'll say in 10 years.
&gt;&gt; Yeah. Yeah. It'll be interesting. It'll
be like Yeah. Everyone splattered all
the architecture spaghetti against the
wall and a couple things stuck.
&gt;&gt; It'll be interesting. Yeah. And where
does the value acrew eventually? You
know, I talked to Gimlet recently and
people can go listen to that and they're
talking about being able to abstract
across all these different silicon
vendors and take your workload and
disagregate across all of them. So it'll
be very interesting too to to see in the
long run is it like no no no you're best
when you just play in the Nvidia
environment and even if they have a a
portfolio with different SKs it's
vertically integrated and that gets you
the best efficiency or does do things
become unbundled and software layers
come in that can orchestrate and and
optimize across different hardware that
might make different um TCO trade-offs
because look maybe for some parts of the
workload maybe you don't actually need
really expensive of HBM4,
you know.
&gt;&gt; Um, so yes, guys, we're on a fun ride.
Uh, and we're here to bring it to you
every week as it unfolds. So, uh, thank
you for listening. If you're enjoying
semi-doped, share it with your friends.
Word of mouth means a ton to us.
Subscribe to our newsletters. We just
started, um, semi-dop.com, which is like
the companion daily. I I think of it as
like the morning brew for semis that
accompanies this podcast. You can get
that in your inbox Monday through
Friday. Vic and I just we look at the
news, we give little takes. We think
it's worth you reading while you drink
coffee. And last but not least, keep
commenting on our YouTubes and send us
emails and everything.
So with that, thank you.
