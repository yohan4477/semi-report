---
source: https://www.youtube.com/watch?v=wMLKWyvMNXs
vid: wMLKWyvMNXs
title: Nvidia "Acquires" Groq
date: 2026-01-05
duration_sec: 2437
channel: Semi Doped
kind: transcript
---
Welcome listeners. [music] Thanks for
listening to the very first episode of
the semi-doped podcast. I'm Austin
Lions. I write a Substack called Chip
Strat. And with me is Vic who writes
Vic's newsletter.
&gt;&gt; Hey Austin. Yeah, I really love the name
for this podcast. I hope we continue to
love it like five episodes in. Uh by the
way for listeners who are not familiar
uh my name is Vicram Shaker and I write
a substack called Vick's newsletter. We
write so much semiconductor content
between Austin and myself that we
decided we should just talk about it uh
on a podcast and so here we are. All
right. So we should talk about what's on
everybody's mind right now. Uh Nvidia
decided to drop a whole lot of coin to
buy a company called Gro. And pretty
much everybody online lost their mind
about the sheer size of this deal and
what it means really for Nvidia. Like
there was so much narrative about oh HBM
is going to be affected. Oh GPUs are
dead. This is the new thing. We are in
the age of inferencing. SRAMM is what
it's all about. Anyway, there was so
much noise that I spent so much time
reading all these threads and figured,
you know, I think we should kind of sit
down and have a little chat on what's
going on here and kind of break down
some of the more technical and business
aspects of what's going on here and uh
maybe give some more context. What do
you think?
&gt;&gt; Yep, that sounds great. Let's talk
Grock. So, for listeners, this is Grock
with a Q, the chip company. And yes, the
news dropped. It was Christmas Eve and
um I it felt like that was strategic
like it was surprising and Grock had an
announcement and Nvidia didn't really
say anything and then everyone signed
off for the holidays and so I think that
also helped lead to a lot of speculation
you know amongst us who track the
industry closely. Um, and so yeah, it
was a what we read at first I actually
read it as it was an acquisition and
then quickly people came and pointed out
and said no no no this is a a 20 billion
dollar deal that Nvidia is doing where
they are acquiring a non-exclusive
licensing agreement of Gro's assets for
$20 billion and I think Grock's
announcement said you know CEO Jonathan
Ross
and the CTO Sunonny Madra or whatever
his title is will be going to Nvidia um
as well as many key employees. And so I
think right away I I was first a little
bit like oh is this just like the
leadership going over um but then I
think later there were reports that
actually it's like most of the company
is going but right off the bat it was a
little surprising in that like oh this
is not an acquisition. This is more of
this like new fangled pseudo acquisition
that we've seen with AI labs. Um, did
you have a take when you saw that news?
Yeah. So, I was actually disappointed
when I saw that it was kind of an
acquire kind of deal initially or at
least what I thought it was because I
think it sets a really bad precedent for
startups in the Bay Area or anywhere uh
really because if they only were to hire
the key executives or the you know key B
brains behind the project and not really
take the whole team with them and just
pick the brains and the technology then
there is really no incentive for anybody
to work at startups anymore because
everybody knows the payout is going to
go to the top I don't know two three
employees and nobody else is going to
get anything out of it but I'm happy
like you mentioned later even I found
out that it's not like that and they did
right by the employees of Gro so this is
a good precedent I'm actually happy with
the way things turned out in a sense
&gt;&gt; yeah totally it did have a happy ending
and I have seen now there's talk where
lots of people are saying hey we should
make sure that this gets it's codified
somehow that that companies can't come
in and sort of like raid the executives
and the IP and the employees are left
with options that they were promised.
And that's part of the comp package for
startup employees is this idea that your
options could be worth a billion dollars
someday and if that can't manifest then
it it does sort of break the whole
premise of startups in the first place.
Um so yes it was happy to read that uh
Jensen did right by the Gro employees.
&gt;&gt; Why do you think that uh the whole
narrative came about after the
acquisition or rather aquire or whatever
it is uh that GPUs are dead? Why did we
get there? I think that the, you know,
zooming out, looking back in 2025, the
narrative like coming into 2025 was
really about like GPUs versus XPUs and
is Broadcom and and their hyperscalers
going to eat Nvidia's lunch and so
there's a lot of push back about like no
no GPUs are really flexible and XPUs
like uh you know where are they you know
Google's got a road map and they've
shipped seven uh you know generations
but at the time we had barely seen
tranium And I don't know no Maya from
Microsoft that just seems like a design
on paper and so it was a lot you know
the pendulum was in GPU's favor and a
lot of people pushing back on XPUs. I
think throughout 2025 then there was
started to be a lot of talk about TPUs
&gt;&gt; especially with like Google potentially
selling TPUs to others and and the
pendulum started swinging a lot. there
was a lot of narrative and conversation
around TPUs and so it felt like sort of
a GPUs versus TPUs dance and meanwhile
um at AWS reinvent there was talk about
tranium 3 and so again kind of TPUs and
XPUs were a thing now of course all of
these use HBM and so then it is a little
interesting that here at the at the tail
end all of a sudden LPUs slid in and
everyone's like HBM is dead
&gt;&gt; but the thing with u LPUs which is Gro's
solution and why everybody declared HBM
dead when this acquisition uh news uh
showed up is because it uses SRAMM
instead of HBM and SRAMM is actually so
much faster than HBM is even though it's
actually high bandwidth memory SRAMM is
actually faster the only problem with
SRAMM is that its capacity is highly
limited so the question immediately
comes up is GPUs are great And HPM is
highly supply constrained and it
requires chip on wafer on substrate
packaging from TSMC which is very hard
to get and is also highly supply
constrained. Uh and I think that I read
in the news that several Google
executives
uh were affected by the uh fact that
they could not you know get sufficient
HBM procurements on time. So it's like a
serious matter this thing. Uh so the
SRAMM solution from Grock provides an
entirely different alternative universe
because you don't have to deal with HBM
because HBM is only made by three
companies SKH, Samsung and Micron. Did I
get that right?
&gt;&gt; Yes.
&gt;&gt; And SRAMM is actually uh made on logic
chips. So TSMC could make it. There's no
need of all this fancy packaging. and uh
you don't have to package it you know
try to stack DM die or package it on a
co interposer
uh or any such thing. So it like takes
out so many capacity bottlenecks from
using HBM and so that's why it seemed to
everybody that oh wow this is a solution
that you know breaks all barriers and it
could take over. The main problem lies
in the fact that it does not have
capacity. So if you were to run a Kim K2
model, you're going to need 1 TBTE of
memory to run that model even for
inferencing. And that is simply not
possible with SRAMM based chips like
Grock LPUs because you're going to need
a lot of them cuz each Grock chip has
230 mgabytes of SRAMM. So you can
imagine how many chips you would need to
run 1 TBTE requirements of memory. So
that introduces a whole dimension of
complexity because now you will be
bottlenecked by how the networking
between so many GPUs work and how the
interconnect bandwidth and limitations
start to show up in the big array. So
it's not as simple that just because you
have SRAMM basis that you can just
substitute HBM and take over everything.
Right.
&gt;&gt; Totally. Totally. And you make a good
point and I think the the framing
that leads to all this is is not HBM
versus SRAM because I think people who
aren't quite as close forget that every
chip uses SRAMM for for local storage
for cache, right? CPUs, GPUs, LPUs,
TPUs, whatever. But it is HBM versus no
HBM. And so yeah, Gro's LPUs don't have
HBM. And so to your point that that's
that's like the key insight which is no
HBN means no capacity constraints like
co-ass and HBM constraints totally but
of course you know you point out yes but
there's a trade-off SRAMM it takes up a
lot of die area and thus is expensive
it's very fast it's very local to the
compute very fast but with only to your
point 230 megabytes per chip you're
talking like tying together thousands of
chips to run a really large model and
even, you know, several hundred, 500,
600 to run a smaller or or midsize
model. And so then that's definitely the
trade-off. Now, if you've got hundreds
of chips, you have to ask, how are we
tying all these together, shuttling all
the data around? And of course, what is
the power cost of all of those chips?
What is the real estate cost of all
those chips, right? And so of course the
economic cost might be a lot less
because by the way you know you one
might ask well why why did they only
have 230 megabytes of essentially SRAMM
on these chips and you know you have to
remember that um this chip was designed
many years ago I think 2020 on like 14
nanometer technology and this
essentially was designed prior to chat
GPT exploding I mean transformers were a
thing but I don't think that they were
probably necessarily designed designing
this chip with these really large
language models in mind, which is how we
end up in a place where you have to tie
hundreds of them together to run today's
large language models. Now, back to uh
real quick going back again in all the
narrative, you know, some of the nice
things, not only do you not have the HBM
constraints and the cost constraints,
it's on 14 nanometer technology, so
surely these chips are cheap. So, there
is the whole like, well, yeah, you need
hundreds of them, but they're probably
way cheaper than buying a GPU. Um, but
yeah, let me pause there and ask you.
So, going back to LPUs, so we we know
they're cheap, but we know the trade-off
is they don't have much memory. Um, do
they have any other benefits
using LPUs?
&gt;&gt; Yeah, LPUs are an interesting
architecture actually. It is
substantially different that we should
talk about this for just a minute
because GPUs are, you know, graphics
processing is what they've been used
for, but they're very general purpose.
You can do a lot of stuff with GPUs. You
can, you know, do rate tracing or
whatever. You can do AI with it. It's
all about how you program this thing and
it does whatever you want it to. LPUs
are actually quite different because
they are like uh a finely tuned machine.
An an analogy I really like is that uh
they're like a factory where every
worker's movement is coordinated to the
last millisecond before their shift
starts. So that whenever the product has
to run through that factory, there is
almost no wasted time motion energy that
uh is is used to push the product
through the factory line. So that's kind
of the the basis between behind what
LPUs actually do.
So they fundamentally work based on what
is called a very large
uh instruction word or v l i w and this
is so unique that uh
actually I should take that back. It's
not it has been around a long time but
its context in inferencing is important
to understand because
typically how processors work is that
when you give it an instruction and say
hey go and uh compute this for me uh
what it does is it takes the instruction
and the hardware decides okay what
instructions need to be executed first
do I need to make the multiplications
first then do I need to add them so that
means means wait the multiplication
should be done before I can add them
together. So the sequence has to go this
way and then I can probably take this
and load this into memory and so it
decides all this at runtime. So this is
how general processing works you know in
GPUs and things like that and uh the
very long instruction word approached by
gro kind of flips the whole argument. So
nothing is done at the hardware level
everything is decided beforehand. So
what that means is that you have to take
a bunch of these operations. So if
you're going to do the addition, if
you're going to do the multiplication,
if you're going to do load it in memory
or store it somewhere else, everything
has to be defined beforehand and you
have to specify it exactly and the
hardware is just dump. It just does
exactly what you tell it to do, right?
So this is very difficult. So think
about that. Not only do you have to uh
orchestrate hundreds or thousands of
these u gro chips but you also have to
be very specific about how the
instructions are executed on this thing.
So that makes it very very difficult for
people uh to to write code to it. Uh and
it is actually a compiler nightmare
because it is so complex because
everything has to be decided beforehand.
You know one one analogy to this is
um actually before that I should explain
another thing. There's another benefit
to LPUs and that is that it is very
deterministic and it kind of falls out
of the
process of predetermining what has to be
done well in advance, right? Because if
a compiler
if the instructions have to be decoded,
what actually happens is uh it has to
determine when it it's going to access
the cache. if the data is available in
the cache or it misses the cache. So
there's a lot of variability in how
general processing works. But with Gro's
VIW approach, it is fixed because the
whole orchestration, the choreographing
of all the instructions are done
beforehand, right? So you can exactly
count to how many clock cycles certain
instructions will take. So that makes it
very deterministic.
&gt;&gt; Right? Uh
&gt;&gt; I'm going to give one last analogy to
explain how determinism works here.
Because
let's say I'm giving you Austin
instructions to go to a restaurant in
let's say San Francisco. So I'm going to
tell you, hey Austin, just go down to
Union Square. You know, go four blocks
east, you'll find a gas station and
diagonally opposite from the gas station
is going to be this restaurant I'm
talking about. So what that requires you
to do is first you need to think about
how do I get to Union Square and then
wait then I have to go what how many
blocks east and what's and then you need
to find the gas station and then you're
going to find the destination right the
Grock approach to doing that would be
I'm going to give you the GPS
coordinates to Union Square and then I'm
going to tell you exactly how many
meters you're going to go from there in
a given direction and at what angle the
from that destination point the
restaurant is at, right? So, this makes
it very difficult to program things like
this. So, although it has its benefits
in terms of very low latency because
nothing is determined uh on the fly,
it's all predetermined and you know
exactly how long it's going to take. So,
this has important use cases which we
should talk about actually.
&gt;&gt; Yeah, definitely. Definitely. Let me
summarize it for listeners. So
[clears throat] Gro's LPU
architecturally it takes the complexity
and moves it from hardware into
software. So the hardware is very
simple. No scheduling like a CPU for
example. Anyone who took a CPU
architecture course would remember uh
like out of order scheduling and
execution, right? You know the the
hardware might just look at the
instructions and and schedule them
differently to try to optimize on the
fly. And what you're saying is that with
an LPU, the hardware is very simple. All
of that scheduling is done in software
by the compiler. It takes a look at the
program, decides how to order
everything, and then gives precise
instructions such that when anything is
running on the LPU,
everything is known. And that's why it's
called deterministic. Like we know
exactly where the data is and how long
it's going to take to flow through and
when it's going to come out the other
side. And so an LPU has ultra low
latency. It's deterministic and the the
determinism comes from how the
architecture is built and designed. And
then the late ultra low latency is just
like you everything's running. It's
there's computation and then there's
accessing memory. And the memory is
SRAMM. It's it's fast and it's it's
close to the compute. Um, and then the
determinism is just, you know, where
everything is going to be. Um, now GPUs,
you know, are more general. Now, I will
say with data center kind of cloud GPUs,
obviously they're not being used for
graphics anymore and and some of that
stripped out and they're definitely
tuned for AI. You can think of them as
AI AS6 in a sense. Even like with the
with every new generation of uh Nvidia
GPU, they tune it specifically for AI
workloads. for example, putting more
spending more compute area and and die
area on lower precision like you know
FPA FP16 and not spending as much on
FP64 right so they're they are making
architectural decisions that are tuned
for AI but at the end of the day it's
still general enough that if you want to
run all sorts of programs and with
different quantization like it can
handle it um and so so there's some
trade-offs just on the way they're
designed LPU deterministic ultra low
latency versus GPU
flexibility dev friendly of course and
and you know we can get into that of
some of the trade-offs of the LPU but um
let me hand it back over to you to keep
going.
Yeah. So now we have established that
LPUs cannot hold large models because it
is SRAM based and SRAM does not have
that capacity. SRAMM has stopped scaling
quite a few generations ago. Maybe we'll
see small improvements as we have gate
all around we have a little bit
improvement from there. Maybe as we go
to complimentary fetss we'll see more.
But essentially SRAMM doesn't get any
denser and therefore it's going to be
expensive to begin with. So you just
can't stack SRAM the way you do HPM.
There are many reasons for that. Maybe
we shouldn't you know get into all those
re reasons right now but fundamentally
it's limited in capacity. You cannot run
big models whereas you can run really
big models with HPM
and that has implications on what kind
of use cases HPM based inferencing can
do and what SRAM based inferencing can
do. Right.
&gt;&gt; Yes. So what so I'm going to going to
ask you uh cuz I really like your
article on Substack where you refer to
hypers speed inferencing using grock and
SRAMM which is a very important use case
um that we do need. It's not always
about serving the large mixture mixture
of expert models that we use day-to-day
nowadays. Uh there are so many
applications that require just small
models. So I let you explain some of
these awesome applications you had in
your article.
&gt;&gt; Sure. Yes. So yeah, I coined uh Gro's
LPU like a hypers speed machine or
focused on hypers speed work cases which
is if you go to think about it, okay,
I've got this LPU, it doesn't have much
memory, so it can only hold a small
model. What are use cases where this
still matters? And of course it's use
cases where latency matters a ton and
the model just has to be good enough.
And um so you can think of something
like um serving ad copy and you know
Google actually already does this um
with their TPUs but historically when
you serve ads um you know it's a person
searches for a thing and then you try to
match the keywords and then give them an
ad that kind of matches it but it's not
necess the ad copy itself is not
necessarily hyperpersonalized to you.
Um, that being said, with LLMs, it
becomes very easy to in natural language
like know about me, know that I should
see this ad and actually write the ad in
such a way that speaks specifically to
me, Austin Lions, you know, given where
I live or what I'm really interested in.
But of course, um, at the end of the
day, like Google, a search engine is all
about responding as fast as possible.
So, if you're going to hyperpersonalize
it, that's going to improve like the ad
click-through rate. Um, but it still it
can't come at the cost of being much
slower. Um, so that's a perfect example
where like, hey, maybe something like
Grock could have just a good a small
model, but it's good enough to write
some plain English to hyperpersonalize
this ad for me, but do it crazy fast.
Um, so that was one one that came to
mind. Um, you know, of course, you can
think of lots of other use cases. I
think even routing between models used
to be of course there was that terrible
user experience on chat GPT where you
had to know enough to say yes I want the
um slow thinking model or the fast you
know just respond right away model. Um
in an ideal world the user wouldn't have
to take on that burden and the
application would just know which model
to route it to and obviously now chat
GPT does that with 5.1 5.2 too. Um you
generally how they do that is they just
take a peek at what you're asking really
quick and then decide like oh I should
probably think about this or no I can
respond very quickly to this. Um that's
another example of a a model that's
small and but just needs to respond
really quickly and then could actually
just forward it on to a different bigger
model or a huge complex model or even
like your video generation model or your
image generation model or whatever. So I
think uh routing between models is
another one. And then of course you know
agents is an interesting one because
agents
now we're talking about if you give a
task to an agent it might run inference
not once but like hundreds of times like
as it loops through deciding like okay I
did this I did this I did that. What's
tricky is you want like the smartest
agent you can usually for those because
you're like, I'm entrusting with some
work and I want to walk away and come
back a few minutes later and you've made
progress. But what would be interesting
to ask is are there ways that an agent
could still have access to a fast model
or are there certain use cases where
most of what the agent's doing is simple
enough? Like could it all run on this
like ultra low latency? And so, you
know, I can definitely see a world where
an agent maybe it has like tools to call
different models and at times when it
knows, oh, these steps are really easy,
could it call out to a model that's
running on like a some hypers speed
hardware like a Grock LPU? Um, so I'll
just pause there, but those are a couple
examples where latency matters most. At
the end of the day, it's anything that a
human's interacting with and needs a
real-time response. That's where
something like Gro's LPU could shine.
Yeah, I like another example I think I
had uh another example that I read in
your article and uh that has to do with
you know speaking with chat agents or
doing dynamic translations where speed
is everything like you don't want to
talk to a a an L&amp;M who's helping you out
on a chat session or whatever and say
something and then you don't get a
response because the inferencing is slow
and there's like a long time to first
token and you're like Wait, did it hear
me? And then you start speaking again
and then it again gets a bunch of tokens
and it's inferencing that it's a bad
user experience. So anytime you have
like chat bots, you know, it's you need
fast inferencing. It doesn't have to be
super clever. It's not like you're
asking it to cure cancer or something,
you know, just you're just talking
regular stuff with it and it's good to
have a fast model for something like
that.
&gt;&gt; Yes.
&gt;&gt; Right.
&gt;&gt; And those and those of course are all
running on the cloud. Um but you
mentioned in your article on your
newsletter an interesting edge
application.
&gt;&gt; Yeah. So this was something I came
across in a discord conversation and uh
one person on it uh mentioned what about
robotics and that really got me thinking
because that is another application
where Nvidia is pretty invested in. they
have their Jetson platform um and
everything that SRAMM based inferencing
uh which Grock is capable of doing fits
that bill because it has to be really
low latency because the environment
changes so quickly if you're doing
physical AI it needs to process uh and
make decisions really quickly. So that
low latency that you can get from uh
SRAMM based inferencing really fast
inferencing is very useful. It's usually
single user because the robot is only
like doing whatever sensing stuff it
does around itself. It's not like a
multi-user G GPT scenario here at all.
And
in order to respond quickly to
environments, it has to respond in a
deterministic time frame because you
need to know that the correction has to
be applied within so many clock cycles.
That kind of stuff is very helpful. And
these models that run on these kinds of
robotic applications could be quite
specialized cuz if you have a vision one
or if you have something that just
drives motors based on you know what
it's doing. So you know all these edge
applications could be very specialized
models that don't have to be big but
need to be really fast and
deterministic. So I it looks like the
the croc application really is a good
one on this.
&gt;&gt; Yeah that's really interesting. You
know, I think of industrial robots where
you need them to do a thing and you need
them to do it quickly. And so although
the selling point is never determinism,
it's it's always about, you know, just
speed to the to the user or to the
process in an industrial setting, there
is something nice about being able to
talk about like tail latency and hey,
we'll always be able to make a decision
in this amount of time so you can plan,
you know, your factory line accordingly.
that that that'll be super interesting
to see if this type of architecture
comes to the edge.
&gt;&gt; Another application actually that really
took me by surprise that when somebody
mentioned it in a comment on my post uh
is like radio access networks or AI RAN.
Somebody said what do you think about AI
RAN? And I was like, hold on a minute.
Cuz Nvidia just invested like $1 billion
into Nokia trying to get them to use
like GPUs in RAM applications. I think I
should explain what RAN is a little bit.
It's basically radio access networks
take all the wireless information that's
from devices and stuff in the cellular
tower and then process the multi-user
interferencebased scenarios. does
manages a spectrum all of this stuff and
then sends out all that information on
the wired network you know to go you
know through the long haul networks and
you know subc cables or even between
continents. So the first stop from all
this wireless data that comes in is the
radio access network. So there's a lot
of decisions that need to be made based
on the current environment that the
cellular tower is seeing.
So right now there are custom AS6 that
run these kinds of things and FPGA is uh
and Qualcomm is a big big player in
this. So Nvidia wants to somehow get
into this market by introducing GPUs.
The one problem with that and I read a
light reading article on this that's
explained this a little bit in detail is
that Nvidia's solutions are just too
power hungry like the existing incumbent
solutions are like onetenth the power of
what a GPU would use so the article
described it as like
&gt;&gt; outfitting a Vesper with a V8 you know
you don't need it is is it cool yeah
it's cool but you really don't need a
Vesper with a V8 engine so you have to
put something that fits the application
And interestingly it might be that these
SRAMM based inferencing solutions Grock
or otherwise may find applications there
because again you know when you're
talking about 5G networks or even 6G
because you know I think that's the
whole goal is you know to make better
radio access networks for 6G the latency
is a very specific number you cannot
have latencies you know it has to be the
sub millisecond latency.
which means that you can't run uh just a
general GPU and having the these kinds
of pre-ompiled
uh preddecided instructions that just
run on dumb hardware is the best way to
get the lowest latency. So I'm not sure
whether this is even a thing but in
thinking through this I thought this was
an interesting edge application for like
SRAM based inferencing. So I just
thought I'd mention it.
&gt;&gt; Yeah, that's super interesting. So now I
have a a a question to push back a
little bit on this, but first let me
take us back. So at the very start we
asked like are GPUs dead? And then we've
talked through like well no there's just
architectural differences. GPUs use HBM
so they can have large models. They're
very flexible. They can be high
throughput dev friendly. Of course they
have trade-offs. Um they consume a lot
of power. They're expensive. LPUs,
ultra- low latency, deterministic, only
smaller medium models though because
they don't in Grock's first generation,
there's barely any memory there.
Barely any memory with respect to the
size that LLMs need. Um, now when we
talk about edge applications, I think
the push back would be okay. Well, still
with Grock's Gen One chips, even if you
want to do AI RAN, like
yes, it it could be a lot lower power,
but can you cram a hundred of those
chips in an AI rand box or 500 or
whatever? And so, I guess my question to
you, Vic, you know, obviously we're
speculating here, but for an LPU like
architecture to come from Nvidia and
Grock to the edge, do you think that's
something they could do with their first
generation chips? Are we talking about
taking the IP and building new
offerings, new SOC's?
I am not sure what kind of resources
these workloads require. Actually,
that's that's a piece of information I
need to really look up because you're
right like if there is a large memory
requirement to run these loads, uh it it
you need HBM again, this is not going to
be the solution for it. But uh these are
currently run by specialized DSPs you
know that ran applications today.
&gt;&gt; So they are not kind of they do not have
that kind of large bandwidth
requirements from what I can tell.
&gt;&gt; So it might be more well suited to using
gro like inference solutions rather than
HBM like inference solutions.
&gt;&gt; So I think it's closer to one end than
the other.
&gt;&gt; Sure. Do you see a middle there where
it's like could we see a grock like
heavy SRAMM but also accesses some DDR
in a use case like this?
Yeah, actually uh there is that's kind
of what Dmatrix solution is because they
have onchip SRAMM which they use for
digital in-memory compute but they also
have the ability to offload uh KV caches
and stuff to DDR uh LPDDR and their next
generation chips are going to have 3D uh
stack DRAM
&gt;&gt; chips so you're going to get
&gt;&gt; a much better
uh DM throughput
compared to LP LPDDR on a on a board. If
you stack chips on top of memory because
you have so much more you have the
entire surface area to put parallel
lanes through. So, you're going to get a
much higher memory bandwidth if you
stack up chips. It's not going to be as
good as SRAM maybe. I don't know. Uh but
it's going to be really good. So yes,
SRAMM and HBM can work together or HBM
SRAMM and DAM can work together too.
&gt;&gt; So there are those kinds of solutions
but it but not with Grock. Grock does
not have that solution right now. It's
only SRAM.
&gt;&gt; Sure. But but presumably if Nvidia
wanted to this is all well known and
they could take work with Grock to take
their IP and make some of these other
offerings if they wanted.
Yes. Yes, it has been done too. You
know, if you look at Intel's Ponte
Vetio, you know, the chiplet
architecture, uh, you know, chip,
&gt;&gt; uh, they do have SRAMM and then the
ability to do more on on DDR. So, those
kinds of things, uh, do exist, you know,
in in out there. So, it's not like it,
you know, Nvidia cannot use the IP they
just acquired to do some cool stuff
with. And I think we're all waiting to
see what that is.
&gt;&gt; Totally. Totally. So I think probably
last question or topic here. I think
kind of what you're getting at from the
memory angle which is really interesting
is a spectrum of systems that use that
make different architectural decisions
with different trade-offs. Some are
SRAMM only on the other end of the
spectrum. Some are SRAM and HBM. And
maybe somewhere in between it could be
like SRAMM and DDR LP DDR GDDR. Um
we've actually which of course allows
you to get different outcomes from
ultra- low latency uh but com
complicated compilers to not quite as
much latency but easier for developers
and uh you know high throughput
flexibility.
Um we are actually we talked about it uh
in thinking about the context of the
edge market but we're actually seeing
this in the cloud market already.
Nvidia, not only did do they have
obviously they have Hopper and
Blackwell, which are pretty much a
little bit of one-sizefits-all, although
you could have um Hopper, you know, HGX
or DGX. So, there's different SKs within
there, but at the end of the day, it's
it's the Hopper architecture, it's the
um Blackwell architecture, Grace
Blackwell or Blackwell standalone. So,
there's, you know, some knobs you could
turn, but now with Reuben, we've heard
of Reuben, we've heard of Reuben CPX,
which makes those memory tradeoffs. Um,
and it's focused on prefill workload.
Um, and then we even saw Nvidia talk
about using RTX Pro servers which again
are make different memory uh
architectural decisions to use for AI
workloads for example in simulation like
in autonomy they talk about having three
computers. One is the edge autonomy
computer like Nvidia Thor. Um, and then
one is the the big training computer. So
that might be a Grace Blackwell. But
then running simulation like hey I just
want to simulate this car running this
intersection and all the different
weather conditions I can think of. You
could actually run those simulations
which involve AI on say these RTX Pro
6000 servers. So, um I guess my point
here is we're already seeing a portfolio
of options from Nvidia that have that
have different compute which everyone
focuses on, but they also make different
memory choices. Um
do you have any thoughts? Will we
continue to see this and and you
mentioned Dmatrix in the mix. Will we
continue to see this in the cloud? Will
we see this happen on the edge? What do
you think?
&gt;&gt; Yeah. So there are so many applications
like video generation, image generation
are definitely the more compute heavy or
the heavier applications of LLMs. Uh
whereas you see like we spoke about
these lighter requirements may I don't
know if it's robotics or uh you know ads
being served on the fly. These are
completely different applications which
require actually completely different
pieces of hardware and that is what I
think is emerging right now because
there is no oneizefits-all and
throughout the history of technology we
have kind of seen that there is no
oneizefits-all and everybody's
applications and needs are different and
so what we are seeing here is an
emergence of a whole variety of
applications where depending on the
workload that you're going to run data
centers have to deploy the right kind of
inferencing solutions to have the
maximum cost benefit from running these
data centers, right? And this whole
Grock thing might just be that little
piece that Nvidia was missing uh with
hypers speed inferencing like you call
it. Maybe this just, you know, checks
that box and gives them the entire uh,
you know, salad bar of inferencing
options that they can now deploy
anywhere they want.
&gt;&gt; Mhm. Yeah, totally. That resonates with
me. I I was thinking of of it in terms
of like it increases their portfolio's
surface area, you know, and and and
agreed with you that as
we continue to progress with enterprises
actually adopting AI, figuring out where
it fits, figuring out where interesting
use cases might be on the edge that at
the end of the day, it is always about
TCO and it's about that cost benefit and
and that's where it gets back to
sometimes you only need a good enough
model. a small model might work, but it
has to be super fast. And so I think
probably to wrap up this episode, that's
our takeaway is the LPU is different
than a GPU. Both are super useful and
they serve different use cases. So HBM
is not dead. GPUs are not dead
&gt;&gt; and agree,
&gt;&gt; Nvidia seems to know what they're doing
here.
&gt;&gt; Yeah. And I think a lot of people have
been trying to find the grand meaning in
Nvidia's move uh for acquiring Grock
here. But it might just be as simple as
you know I think it's a cool piece of
technology. We are missing it from what
we can do. So you know here's a price uh
of $20 billion to buy it because why
not? We have the money.
&gt;&gt; Totally. Totally.
&gt;&gt; Nvidia can do that. Not too many people
otherwise
&gt;&gt; they can.
&gt;&gt; Awesome. Cool. All right. Thank you,
Vic. Well, listeners, I hope you liked
our first episode.
