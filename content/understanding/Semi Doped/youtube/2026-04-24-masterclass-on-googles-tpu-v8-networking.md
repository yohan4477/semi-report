---
source: https://www.youtube.com/watch?v=yd-_iMCM-C4
vid: yd-_iMCM-C4
title: Masterclass on Google's TPU v8 Networking
date: 2026-04-24
duration_sec: 2819
channel: Semi Doped
kind: transcript
---
the constraint, the constraint is no
longer compute, but it is instead the
networking that underlies all of compute
today. That is the bottleneck that needs
to be solved, and that is what Google's
innovations now address.
Hello everyone. Welcome to another
semi-doped podcast. I'm Austin Lyons of
Chip Strategy, and with me is Vic
Shayker from Vic's Newsletter. Today,
we're going to talk all things Google,
TPUs, networking, silicon.
Oh, yes. And Vic is going to try sharing
his screen. So, if you're listening to
this, you might want to watch it on
YouTube.
&gt;&gt; Yeah. Uh, this is our first attempt at
sharing video because like there's so
much developments on networking in the
Google announcements recently in their
whole TPU architecture, and how they
deal with training and inference
differently, not just from a chip side,
which we'll talk about, but also from
the networking side. It's easy to talk
about chips in the sense of, "Oh, look,
this hit has so much RAM. It has so many
flops." It's very difficult to talk
about networking without showing a
picture.
&gt;&gt; Mhm. So, I've like
pasted a bunch of pictures on Google
Slides. I'm just going to share that.
It's very rough. This is not going to be
seriously edited or professional or yet
yet yet, maybe we'll get there one day.
But anyway, it's I think it's useful to
show some pictures, so definitely watch
it on YouTube if you can.
Yes. And so, I'm excited. I think
there's a lot to learn there. I'll set
the stage for listeners. So, Google had
at their Google Cloud Next 2026, they
had their keynote yesterday, and in it
they announced the next version of the
TPU, and of course, the most exciting
thing that most listeners probably have
heard is that there's not just one TPU,
there's actually two. TPU version 8,
there's 8T, which is the training chip,
and 8I, which is the inference chip.
This is interesting in that
historically, it's for a for quite some
time it with the TPU, there's just been
one chip. V1 was like an inference-only
chip, then V2 was training and serving,
V3, V4 was training and serving. I they
split out this like efficiency chip
versus a performance chip. V6 was back
to one chip. V7 was one chip kind of
marketed very heavily as an inference
chip. But here we have Now we've got a
specific training chip or training
system, as we'll get into, and a
specific inference chip.
&gt;&gt; Maybe I should point out the elephant in
the room right away. The TPU 8I has like
384 MB of SRAM, which is like three
times as much as the 8T, which is for
training. That was like, "What? That's I
mean, it makes sense. Why not put SRAM?"
You know, Groq LPUs that Nvidia is now
integrating into their platform is
basically SRAM, and why not do that
right now in the TPU 8I because, you
know, put in as much SRAM as you can so
that you can get your low-latency
inferencing from SRAM
right there. Get high throughput, faster
tokens. So, that's like one obvious uh
thing to do, which is put in more SRAM.
So, it's a good decision, but, you know,
it's explicit right now after seeing how
we're going for like fast decoding. Yes,
yes. And this aligns with um when I
talked to Rainer Pope from Matrox, you
know, he talked about how they do
weights in SRAM and KB cache and HBM,
and these are architectural decisions to
try to get both like really fast decode,
but also all the context you need. So,
we see see Google going this direction
with three times as much SRAM, but then
also uh 288 gigs of HBM on the inference
chip. And I will point out one thing
that I thought was interesting, which is
the training chip has less HBM. It's 216
gigs. By the way, listeners uh and
people watching,
Google has amazing uh technical blogs
for these chips, and they talked a lot
about it. So, they kind of talk about
why they made these tradeoffs. But I
think it's interesting cuz right away in
my head I'm saying, "For training, if
you're going to have less HBM, you could
sort of frame that as like why overpay
for HBM you don't need?" So, for
example, if someone's just selling one
chip like a GPU that's like, "Hey, one
size fits all. Use it for training, use
it for inference." You could say, "Well,
hey, look what Google's doing. Maybe
am I overpaying for expensive HBM on a
training chip that maybe I don't
actually need it?"
Yeah, I was wondering about why the
training chip has lower HBM, and I think
the inference part of it is obviously
now so memory hungry that you want to
put in as many fast memory tiers as and
as much of it as you possibly can
because the decoding and the inference
gets like so much faster with much
better memory throughput that the
inference chip is simply,
you know,
peaked. It's It's maxed out with the
best memory you can ever put down in the
current environment, the current
scenario. This is what you can do. Why
is HBM lower in training?
I guess you could always put more chips
together if you don't have enough
memory. You could just like add more
GPUs, and your cluster total GPA GPU
memory in the cluster gets bigger. So, I
guess that's the solution to it. But in
inference,
it's it only makes sense to max out
every tier. You know, remember Nvidia's
like memory tier, where you have like
SRAM right up They don't actually
mention SRAM. It should have been there.
But it should have been like tier zero,
and HBM was tier one, and you know, DRAM
was tier two. This is an
effort at maximizing the fastest memory.
Makes sense, yeah. Okay. What else was
interesting? Both chips do use the Arm
Axion, so Google's Arm-based custom CPU
as the head node CPU. And I think there
was a quote here. I'll read it. It said
in the announcement blog, "TPU
introduces two distinct systems, TPU 8T
and 8I. These new systems are key
components of Google Cloud's AI
hypercomputer." So, yet another
interesting marketing name. Of Of
course, again, it though it hints that
it's it's a whole data center these
days. You're not just thinking at the
chip level. "An integrated
supercomputing architecture that
combines hardware, software, and
networking to power the full AI life
cycle. While both systems share the core
DNA of Google's AI stack and support the
full AI life cycle, each is built to
address distinct bottlenecks and
optimize efficiency for critical stages
of development. Additionally, by
integrating Arm-based Axion CPU headers
across our eighth-gen TPU system, we've
removed the host bottleneck caused by
data preparation latency. Axion provides
the compute headroom to handle complex
data preprocessing and orchestration so
that TPUs stay fed and don't stall."
So, they're really framing these as the
CPUs to feed the TPUs.
Yeah, that's what is important. Never
let a GPU stay idle. Yes, yes. That's
That's what it So, also points out that
Arm is a is a very viable alternative to
any x86 CPUs. Not not to be ruled out at
all in terms of ISA
in the architecture.
So, yeah. Um I think they're all equal
fair game now. And like we mentioned in
an earlier episode,
the best CPU is the one you can lay your
hands on. So, just whoever can deliver
most of them, they'll make it work. Arm
or x86.
That's the name of the game right now.
Okay. Now, let's talk let's talk
networking. Where Where should we start?
I noticed that they've got this nice
little table, and they're showing 8T
uses a 3D torus network topology, but 8I
uses the Board Fly topology. And so,
this is interesting because not only are
we now starting to make different SKUs
for different workloads, but we're
starting to have different network
topologies for different workloads. So,
that's super interesting. So, take us
take us there. Yeah. So, in terms of the
chips that,
you know, we just spoke about
themselves, they're cool. I mean,
they're good chips. They have HBM. They
have SRAM. This is all like standard
stuff in some sense.
Now, I think the real innovation here,
and the it is a tectonic shift in how
networking is implemented in the future
of Google data centers. There is a big
change, and this is a change that
happens once in a decade kind of a
change. And so, I'll explain what that
is, but for that I need to explain what
was there before, all right? So, the
fundamental assumption and the basic uh
need for scaling AI today is the
is to realize that the constraint, the
constraint is no longer compute, but it
is instead the networking that underlies
all of compute today. That is the
bottleneck that needs to be solved, and
that is what Google's innovations now
address. Google has now reimagined the
data center in a sense. And as we talk
about it, we'll kind of break down why
that is because they have different
chips, as we just mentioned, for
training and inference. They have
different networking architectures for
training and inference as well, and
we'll talk about why that is. And what
is most interesting is that a lot of
this networking is going towards optics.
And you will hear me talk about like OCS
a lot, which stands for optical circuit
switching, right? And I want to like
explain what that is right up front so
that, you know, when I keep saying this
word while talking about networking, and
I will say it a lot, that people
understand what it what this actually
is.
So, optical circuit switching is a way
to redirect light from one port in a
switch to another port in a switch so
that you can connect one GPU here
or to another GPU here, or TPUs in this
case.
And you do it entirely in the optical
domain. And the idea is very simple.
It's just like holding up a mirror and
reflecting the sunlight from coming in
from your window. You know how you can
point it to different spots in your on
your wall or something. That's exactly
the theory of like the concept behind
OCS. Why convert optics to electronics
and like do silicon packet switching
like all the Tomahawk switches do?
Just stay in light. You're already in
the optical domain. Stay in light. So,
that's what the OCS So, this is optical
circuit switching. You can simply
connect one port to another by changing
how you shine light into different
ports. So, that's what OCS is, okay? And
so, that's becoming the substrate on
which Google's networking is built
today.
And I'll explain what parts of the
network do. So, the first thing we
should talk about was
what Google called their Virgo
networking solution. Their previous
network was actually called Jupiter and
this is from 2015.
And was at the time it was a industry's
first like petabit scale network. Like
nobody had ever seen anything before
that at that scale. It was pretty
fantastic.
Because and you know, it was built
primarily for the internet era cuz
that's what was driving everything.
And data centers relies, you know,
relied on a claw network which is
uh basically have these racks and you
can have uh different levels of
networking switches.
This This is when I have to kind of
experiment with uh with a picture
because um I actually have a picture of
what a claw network looks like.
And uh uh yeah, so I hope this works.
While he's pulling that up, for people
listening claw is spelled c l o s.
Yes, it is. You might not know that when
you're listening. If you're trying to
Google it yourself. Yes, so c l o s claw
network. It looks something like this.
So, basically there are these racks and
then you have the first layer called a
leaf switch that is the racks hook up
to.
And then at the next layer is what is
called a spine switch. They you know,
have have another layer on top called a
super spine switch. And so, what ends up
happening is that
if you have to go from like one rack to
another rack or one GPU to another GPU,
you know, between different pods or
whatever. Uh you can see this picture if
you're looking at it on YouTube, you'll
see there are two pods. And basically
you have to go through a lot of network
hops. Think about it. You have to go
from the GPU in the rack to the leaf
switch. From the leaf switch one higher
level to the spine switch. From the
spine switch you go to the super spine
switch. And then you get switched into
the right super spine switch and then
you come back all the way down the
hierarchy.
This is too many hops, okay? And when
you have to go from
one GPU at one end of the data center to
the other end of the data center, it is
it is too much, okay? So, that's the
whole thing here and that's why
uh we don't it doesn't work for the AI
era.
And the reason Yeah.
This This was definitely designed and
made a lot of sense in like the cloud
server web app era. You're hitting a
database over here, you're hitting an
API over there, but it's not that you
need every leaf talking to all the other
leaves and having to hop way up and way
back down to do that.
Yeah, it happens sometimes and the
latency is kind of
you know, undeterministic. It happens
latency is what it is and
the problem is training networks don't
like that. And like AI does not like
random latencies and all that. And
another reason I think this is very
important. That this claw network has so
many hops and you need so many layers of
networking switches is because each
switch does not have enough ports.
In networking terminology that is called
the switch radic.
So, when you say a switch doesn't have,
you know, enough ports, it's just
another way of saying that is like yeah,
it's a low radic switch. So, when you
have a low radic switch, you need to
multiply the number of ports by adding
layers on top.
Okay, so that's why you need so many
layers.
Now, that problem is changed like we
have really high radic switches and
we'll come into why that is. Now, all of
this communication was managed uh in a
data center in the Jupiter network of
Google's Jupiter network by their
software layer called Orion. As this
internet era grew really in the 2020
around 2022,
uh Google introduced optical circuit
switching into the data center because
it actually has a large switch radics.
You can I I think if you see Lumentum's
uh OCS switch and even Coherent's,
you'll see that has like 300 by 300
ports. It's like a lot of switches
actually. Uh switch ports at high radic
switch. And so,
these were like also switched to optics.
Now, it's not doing silicon switching
anymore. So, when they started doing
like optical switching, they also do
started doing wavelength division
multiplexing which means they sent
multiple wavelengths. So, all that
increased the bandwidth.
So, it around 2022 it was like six
a petabit per second speed. So, six
petabits. A peta is like 1,000 tera.
So, you're talking about like 6,000
terabits per second. That's what like
2022.
And then they went to like faster
networking speeds like going to 400 gig
networking.
Made it like a staggering like 13.1,
you know,
petabits per second. That's 13,100
terabits per second. That's a lot.
Remember this number like 13.1 petabits
because later when I tell you about
Virgo, I'm going to tell you what the
number is and you'll see how much how
amazing that is. Right? So,
yeah, it's from 2015 to 2023 it's grown
13 times. That's pretty cool, right?
Like and you know, they've been growing
it pretty quickly. Uh so, it just was
great. It worked great for internet,
YouTube videos, web search. It's it's
great. But when AI showed up, when
you're training a trillion parameter
model with highly synchronous traffic.
See, the internet does not work that
way. Internet is like I don't know,
Austin is checking it at his time zone.
I'm losing the internet on my time zone.
Maybe there are like spikes because
everybody watching a sporting event at
some particular time. But those tend to
be regional and you know, it's it's
okay. It's kind of an asynchronous thing
really. Internet is an asynchronous
really for the most part. AI does not
like that. It's like
when all of it hits AI the same time,
the latencies go crazy and it's always
limited by the slowest deer in the pack,
you know? The highest latency is what is
going to cause problems and that is what
is called like tail latency. The highest
latency is the limiting factor.
So, that is the Jupiter network. That is
what there was a status of the world
until like Google changes everything.
Yeah. And so,
okay, so they had a network and it was
made more for the previous era of like
cloud unpredictable network. And by the
way, it's not all just one big job like
AI training. You're just running one job
across the network. It's coordination.
It's all the machines are contributing
to one big job. But obviously the
Jupiter network was not designed for
that era. It was highly distributed tons
of jobs running at the same time. Even
if there was some pattern to the
traffic, it's just highly distributed.
And then to your point with training,
not only is it all coordinated, but it's
coordinated in such a way that there's
this tail latency concept where everyone
has to do work and update everyone else.
And if there's a straggler, the whole
bus has to wait for that one straggler.
Yes, that's exactly the word they use in
their blog post, too. So, stragglers are
bad. Yeah.
&gt;&gt; Yes.
Yeah. All right, so let's now talk about
the new network called Virgo. They call
it the Virgo megascale network. So
fancy. It is actually a megascale
network and you'll see why. So, Virgo is
basically designed for AI. They saw the
network like no, this internet era stuff
doesn't work anymore. We need to
redesign this to actually make it work.
And
the biggest change here is that they
reimagined each part of the network for
what it is.
And this is why, you know, need a
picture again from um
their blog
which I am going to put up if you're
watching it on YouTube. It really helps,
but I will try to explain it without
having the visuals as well. So,
essentially what happens is that you
have three layers of their networking
stack which is first one is the scale
up.
And we'll talk about scale up a little
separately, but you know, you got the
scale up network, okay? You got it
within a pod and you know, however the
pod is hooked up. The Virgo fabric
itself where the interconnect happens is
in the scale out, also called the back
end network. So, this is where this is
an east-west connection where you hook
up all the racks in the data center.
These TPUs to act as one big
AI hypercomputer. And so, that's the
whole scale out network. And then you
got
A tiny bit of nuance there for people
listening. Scale up, you're trying to
make all the TPUs act as one and they're
sharing their memory. So, it's like
memory coherence. So, it's like they're
all talking at like as fast of latency
that it seems like all their HBM is
shared. And then with scale out, from a
training perspective, we're still trying
to make one massive training computer,
but everything on the scale out network
is is not sharing memory. Now, they're
they're talking as a big coordinated
system, but not as tightly coupled. And
I know that and everyone when it comes
to GPUs, they think oh, scale up is
within the rack and scale out is many
racks. And that's mostly the case
although you can have scale up in
between like side-by-side racks. But
TPUs are a bit of a different beast
because even on their scale up domain,
they'll have lots and lots of TPUs more
than just a rack. Did I Did I get that
right? Yes, so TPUs go to thousands
actually. But in terms of memory
coherency, there are some improvements
that I will mention next. And that is
very
&gt;&gt; Ooh. Ooh. It's a combination of
how the latency between memory can
actually be reduced as well. And that's
an innovation here. Yeah, actually that
actually brings me to the
pretty much explaining the last part of
this networking thing here which is the
front end network. The front end network
is simply
I don't know, compute and storage or
connecting to the internet. This is not
like fancy networking, okay? So, you can
use the Jupiter network for this.
So, you can use like the leaf spine
topology, the cloth networking thing
that we spoke about. That's fine. Don't
need to reinvent every part of the
network stack. Just reinvent what is
required, right? Yeah, so that's that's
how this basically looks. So, the Virgo
network, this is what we should talk
about now. They collapse it entirely to
a two-layer network. Because they have
these high radix switches, which are all
OCS, by the way, and they have, I think,
300 by 300 ports if they're using
Lumentum's OCS.
The future of OCS is going to scale
2,000 by 1,000 ports. So, you can
imagine you can even flatten the network
further.
But regardless, I don't know if Coherent
is an OCS provider to Google as well.
Things I don't really know. But anyway,
all this technology exists from these
companies
and have viable uses in these data
centers.
So, OCS used to be optional before, but
now it has become an integral part of
Google's data center networking
approach.
And the way you can connect
with OCS, because it has so many ports,
and you can connect it in simply two
layers, means you don't have all those
hops. You can get from one TPU to
another TPU with like going across two
network layers. That is That makes it
really, really fast. And not only that,
because you have these high radix
switches, you can connect
1,000 What What was the number I have
here? A
134,000 TPUs to all act as one in the
data center. That's crazy. That's
insane. So, they call it campus as a
computer. It's crazy.
Yeah,
that sounds right.
Yeah.
Whole campus is a computer. You're
You're staring at a whole computer.
That's right.
And you want to know what the aggregate
bandwidth of this whole
network now is?
What What was it before? Like
13 petabits or something? I don't know.
You told us to remember, and I don't
remember.
Yes, 13.1 petabits per second. Okay, and
now?
Now it's 47 petabits per second. Wow.
Wow.
&gt;&gt; It's like 4x. Okay, it's like 4x faster.
So, that's
one reason is that it's optics entirely.
No silicon-based switching really in the
back end network.
And they have re-re-rearchitected a
bunch of things
that makes makes this happen.
So, it's really amazing. And now, you
know, what happens when you put 134,000
chips together in a campus as a computer
is that stuff breaks all the time. And
so, they have an enormous amount of
telemetry built in
so that they can continuously monitor
these things and
keep their good put high. Good put is
like, you know, the the stuff when it's
actually working. So, not just
throughput. Throughput doesn't When you
say throughput, it's just like, yeah,
the CPU is capable of making flops, but
does that actually generate enough
tokens or do what it's supposed to?
Sure, probably. The good put terminology
nowadays is to be like, okay, the the
working throughput. Yes. Yes, that's
good. That's actually good. Yes, it's
not just like the theoretical max, it's
what actually happens in practice.
Yes.
Now, I should quickly hit upon the
memory thing you mentioned, right? They
have this thing called TPU Direct now.
And what that is is basically remote
direct memory access or RDMA.
RDMA as a technology has been around for
a while, and in Nvidia land, it has also
been called GPU Direct. Also, TPU Direct
is like an evolution of that concept, I
suppose. But the idea is like fairly
simple, and it's honestly, this is not a
good like a fantastic innovation or
anything. It's been around for a while.
So, so not new, but it's been
implemented in TPUs now. So, what this
is that before, if TPU 1 had to access
the memory of TPU 2
TPU has to go through the host CPU.
Mhm.
neighboring thing of the neighboring
TPU.
And then it has to the host CPU will
like interact with the DRAM and like
interact with the network interface
card, the networking stack, and all of
them will like have conversations. So,
what do you want to access the memory?
Cool. Which access memory do you want to
do? And like CPU is involved and all of
this stuff. And then it'll go and tell
the destination TPU
the CPU of that TPU. It's like, "Hey,
like this guy wants to access your
memory. Would you allow me to do this?"
And the the destination CPU would be
like, "Yeah, yeah, fine. Let's Let's do
this. Let's all make it happen."
And then you finally you get to the HBM
of the destination TPU. So, the memory
coherency, like you're saying, is like
has so many handshakes.
It's like so many middlemen. Exactly.
Managers ruining the organization. So,
they're like, "Take it out. Just let's
take it out. Let's Let's handle Let's
get the middle middleman out of this
thing and remove the host CPU from the
picture." And that is what is called
remote direct memory access. So, TPU 1
will talk to TPU 2 directly through the
network interface. No CPUs involved. And
this is how GPUs [clears throat] do it,
too, right? GPU Direct is is also been
there, yeah. Nvidia does this, too.
Yeah, so this is how like So, this is
significantly speeds things up. So,
there's like memory co- you know, speed
and latency increases as well.
So, now now we should go to
So, that was that was all about scale
out.
Right?
This is where we are with the TPU Direct
thing, you know.
At some point, we should get into
talking about scale up.
Because
scale up networks in this TPU v8 thing
comes of two two flavors.
Comes with the 3D torus approach, which
everybody is like well familiar with,
which is like the picture on the screen
if you're watching it on YouTube.
Um and then now they have something
called the board fly.
Mhm.
Right? Have you Have you heard of any of
these things? So, I remember hearing
about the torus topology SemiAnalysis I
don't know if this is from SemiAnalysis,
but
&gt;&gt; This picture is from SemiAnalysis, yeah.
&gt;&gt; Okay, perfect. Yeah, they had they had
some nice diagrams showing how it works.
Is that historically This is
historically how the TPUs have done
scale up? Is through the torus?
&gt;&gt; I'm going to very briefly try to explain
a complicated 3D picture with words.
Yeah, okay.
Follow this carefully if you're
listening and not watching. Yes, think
of a Rubik's Cube in your brain. Thank
you. I was going to say Rubik's Cube. I
was so going to say Rubik's Cube.
&gt;&gt; I'm sorry, I interrupted. No, no, no,
that was perfect. That was perfect.
So, this is a very large Rubik's Cube.
But you know what, think of it like the
regular 3 by 3 one. It's okay. 3 by 3 by
3.
So, the Rubik's Cube
has all its inner faces, right? You
don't see the inner faces of a Rubik's
Cube, really. So, all of those are like
uh
connected
to each other
with cables, okay? Let's just say.
Each movable cube of a Rubik's Cube here
we're thinking about is a a TPU. And the
TPUs are connected through each other in
cubes like the Rubik's Cube. And the
inner faces are connected with like
copper cables all around the Rubik's
Cube. So, it's like every face is
connected to every other face
with copper.
But now, you also want to connect the
outside faces of the same row and the
outside faces of the same column to each
other.
That's what makes it the torus.
Right? And that is done with optics.
Because like clearly you have to go a
longer distance to connect the faces of
the Rubik's Cube of the same row or same
column, but on the opposite ends
together
has to be connected with optics. So,
this is how the 3D torus works. And
it has a problem when used for
inference, actually.
Because
in training, it's fine. You know, you
can you can do all of these All of these
TPUs are working together and
whatever, it's fine.
But
the the hardest
distance that any GPU to GPU
communication will happen in a Rubik's
Cube
You should think about this one
carefully. Is actually from the edge of
the Rubik's Cube. Think about one very
edge.
But if you think the farthest edge is
the other edge of the Rubik's Cube, you
would be wrong. Because you can always
use the outside optical cable to reach
the other end. So, that's not the
hardest portion to get to.
In a torus in a 3D torus, the hardest
position to get to is the middle
of the torus. The middle of the Rubik's
Cube is the hardest and requires the
most number of hops to get to in a 3D
torus.
Okay?
And so
if you think about how you're going to
get from one very, very edge of the
Rubik's Cube to the middle of the
Rubik's Cube
you're going to hop halfway along one
dimension, halfway along another
dimension, and halfway along the third
dimension. That'll get you to the
middle, right? Mhm. So, that is So, you
know, what happens is like when you have
a 4 by 4 by 8 Rubik's Cube, which is, I
think, what is on the screen, right?
Like, yeah. This is a TPU v7
configuration.
When you have a 4 by 4 by 8, you're
going to hop two hops in one direction,
two hops in the other direction, and
four hops in the third direction.
Right? So, you're going to have 2 + 2 4
+ 4 8.
Eight hops in this thing. So, that's how
you calculate for any 3D torus topology,
which doesn't have to be 4 by 4 by 8. It
could be 8 by 8 by 16, which means you
have 4 + 4 8 plus another 16x2 8. So,
you have 16 hops. So, that if you see
the Google blog, that's what they That's
the example they use. They use an 8x8x16
topology, which means you need a maximum
of 16 hops to get from one point of the
the Rubik's Cube
to the farthest point in the Rubik's
Cube, which is the middle.
Let me interject here really quick and
reflect it back cuz we're going really
deep and and I want to make sure
everyone's tracking. So,
we were talking about scale out, just
kind of like connecting pods to each
other, and now we're talking about
connecting individual TPUs to each
other, and we don't want to use a clone
network because if you have these
neighbor TPUs in training, you've got
with like dense models, you've got just
like neighbors talking to each other.
Just think of like different layers in
the network and you just want like GPU
one to talk to GPU two or TPU to talk to
TPU three to two TPU four. So, they talk
to their neighbors a lot. And and so we
don't want a world where they have to
like hop up and hop back down just to
talk to their neighbor. And so, the
traditional way to lay out for training
is like, "Oh, how can we densely pack as
many TPUs to have as many neighbors that
are close by as possible that we could
connect like with copper, just like
really easily?" And so, Vic has this
picture here of this Rubik's Cube just
showing like
this is actually pretty optimal to think
about connecting these in three
dimensions where you've got like if I'm
in the bottom left corner, if that's my
little block or TPU, I've got a TPU to
my right, like called the X axis, a TPU
to my left, called that like the Y axis,
and then a TPU right above me, called
that the Z axis. So, I've got all these
neighbors really close to me. And then
Vic was also pointing out that like if
I'm if I'm in that bottom left corner
and I want to connect to anyone else on
my like X axis row, it's one It's like
one neighbor or two neighbors or three
neighbors or you can put optical to
connect me from zero all the way to the
other end, let's call it three. So,
there's there's there's actually it's
pretty easy to talk to my neighbor's
neighbor, but the the hardest one to
talk to is the one right in the middle
because I have to traverse through
neighbors in kind of every dimension
down the X and the Y and the Z to get to
there. So,
I'll hand it back to you.
Yeah, thanks. That's good summary.
That's good summary because
that's is important. That is what the 3D
torus is.
In the 8x8x16, I I showed you like you
how you need half of half the hops in
each direction.
And anybody listening to this might want
to pause and think about, "Okay, what is
he saying? How many hops?"
But, yeah, this is how this this
networking is serious business. But,
anyway,
the 16 hops is what was mentioned in the
Google Google document uh blog. And so,
16 hops is a lot. Mhm. This is not a
very good It's It's a good architecture
for training, okay? Because all of these
TPUs are talking to each other all the
time.
In inference, it is not a good
architecture. And why is that? And the
reason is
because not all GPUs are are TPUs are
activated all the time.
And when you have a mixture of experts
model,
only some of them are going to be active
depending on which parameters are
getting activated. And so, the all the
GPUs don't function all the time
together.
And they do traverse a lot more hops.
And you want that hop latency to be
minimized cuz otherwise it adds to the
inference time and, you know,
performance. You don't want that. So,
the question is,
how do you architect 3D torus for the
world of
inferencing with mixture of expert
models? Yeah, and this is why we come to
the concept of board flight.
Yes, yes. So, let me reflect it back
really quick for people.
For training, we want all this
neighbor-to-neighbor communication. And
what Vic was saying is if you got a
mixture of experts when you're doing
inference,
there's not necessarily going to be all
this neighbor-to-neighbor communication
because it might just be like, "Oh, hey,
for this token, I want this expert
expert 21 over there. And for this
token, I want that expert expert four
over there." And so, it's it's not the
same communication patterns every time,
just neighbor-to-neighbor neighbor,
layer-to-layer layer. But, now it's this
routing, which actually kind of reminds
me back to what we were talking about
earlier of the sort of non-deterministic
era that that we were living in. So, all
this is to say
the workload communication pattern is
different for training than it is for
inference. So, that raises the point
that why not design the interconnect for
the workload, which in this case is
mixture of experts. Which, by the way,
if you go listen to the Rainer Pope
talk, he actually talked about how
they're thinking about this as well,
designing the interconnect specifically
for mixture of experts. But, okay, carry
on, Vic.
Awesome. Yeah, it's good context. Good
context because we need that. We need to
always take a break and think about and
say to ourselves what networking is.
That's the only way you learn
networking. You have to say it out loud,
you know? So, pause the video and say
whatever we've spoken out loud so far.
Okay.
So, what ends up happening is we need to
go to the board flight. And this is
it is not an It is not a dramatically
new invention, uh but it's a
modification of an existing idea.
So, the board flight approach
is fundamentally to reduce the number of
hops. Remember how we're like I told you
like 8x8x16 has 16 hops?
Now, we want to get that down. And board
flight topology allows you to do that.
Okay, so how this works is uh uh
you have a board.
Okay? And on a board, you have basically
four TPUs. And you'll see this picture
in all Whenever you search up TPU V8,
you'll see these like a board with like
four TPUs. And those are PCB connected.
And so, there's like copper. Okay,
there's no like optics here. It's just a
board PCB with copper connections.
So, that's copper connection.
Now, you take eight of these boards and
you put them in a rack.
And you hook them all up with active
electrical cables.
You see how scale up still uses active
electrical cable. So, it's not like
everything's like optics and copper is
dead. No. So, AEC is still used to
connect
the boards
uh eight boards together.
Okay? And this is now called a group.
Okay?
Now, how they are connected is what is
called the dragonfly approach. And this
has been around since the supercomputing
days. Again, this is this has been
around for decades. This is not like a
fantastically, you know, revolutionary
idea. It was at the time, not today.
Yes, let me give you a tiny bit of
trivia. I I found this when I was
Googling. I've been waiting to tell you
this. I haven't told you this before.
Okay, so I was looking up dragonfly and
there was a paper from 2008 talking
about some computer architecture paper
introducing the the dragonfly network.
And the authors on the paper, someone
named John Keen from Northwestern,
William Dally from Stanford, whom you
might also know as Bill Dally, who is
now at Nvidia, and he's the head of
Nvidia's research, which is, by the way,
probably one of the coolest jobs in the
world.
Then, another author is Steve Scott,
some guy from Cray,
which of course Cray supercomputing, a
lot of history there. And uh people who
don't know, that's in Chippewa Falls,
Wisconsin, which is a town of 14,000
people. So, just kind of crazy. Kind of
cray cray.
And then the the last name on it is um
from this 2008 paper
is Dennis Abts. I'm not sure how you
pronounce his last name, A B T S. He was
at Google at the time. Then he went to
Groq and he was an early Groq engineer
from like 2017 to presumably doing all
of their network design and stuff. And
then he went to Nvidia. And so, he's
been at Nvidia ever since. So, when I
saw the paper, I was just like, "Woah,
these are some of the who's who's of
networking of Nvidia." And it was just
crazy to see that this traced back to
them from 2008.
But, with that, I'll give it back to you
to keep going. I just I just thought it
was cool. That was great. That was
great. That's a great piece of trivia.
And I want to add to the the fact that
Dennis Abts, when he was at Groq and the
Nvidia then he went to Nvidia and all
that, if you look at how Groq architects
their rack scale solution, it's also
dragonfly. They don't hook up boards.
They hook up individual LPUs in
dragonfly configuration. That is what
Groq does, too, by the way.
I see. I see. Gotcha. Yeah, yeah,
because it's still it still reduces the
amount of hops. Even if they're not
connected on boards, it's still going
from 16 hops down to something less.
Yes, exactly. So, this is called board
flight because you're not hooking up
like GPUs
uh in a dragonfly configuration. You're
hooking up boards of four
TPUs in dragonfly configuration. So,
it's, you know, the port monitor, you
know, board flight. So, this is still
AEC. The next level is that you connect
up all of these groups together. So,
remember we had four TPUs to a board,
eight boards to a rack,
also you can call it a group. And then
you have 36 groups connected to each
other in a pod.
So, if you multiply 36 groups * 8 boards
* 4 TPUs, you get 1,152 chips.
And so, 36 groups are all connected
together
with OCS. Again, you see how OCS is the
underlying substrate on which all of
Google networking is built. It tells you
how important this technology is now.
Yes, yes. So, all of this scale out
in Virgo or whatever it's called, it was
all of that OC
Virgao, yes, that is all because it is a
high rated switch that connects two
layers that connects all of this stuff
up into layers. Okay, so all the scale
out was OCS and then scale up
on the board it's PCB traces, nearby
boards in a group are AECs, but then
group to group is connected via OCS.
OCS, all optics, yes. So, it's optics is
the primary driver in all of this
networking and all of this is like OCS.
And now, what is the benefit? Why do all
this stuff? I promise that class will
end soon. Like, but I think this is
fascinating. Okay, so let's I'll take
you show you like a couple of more
pictures if you please do watch this on
YouTube. So, the board flight tells you
why how exactly the hops can be
minimized. Okay, so the only the picture
can show you this and because what you
can do is you can go from board to board
within a rack
you know, and you will you'll have a
couple of hops within the rack and then
you will make one big hop via OCS to a
different group
you know, and then you will make a
couple of more hops there and ultimately
you'll reach your destination in
probably six or seven hops.
And so, your hops has come down from 16
all the way down to seven because of
this approach of architecting a board
flight networking scheme for scale up.
That is a big deal. You know, the
latency has dropped by over 50%
because of this clever way of hooking
stuff up.
See, that's why the networking of a data
center is vital in the performance it
provides.
It's critical, right?
So, that's
I I don't know. That That's about all
the spiel I have. It's pretty fancy.
Yeah. It's very technical. I know this
episode. But essentially
to summarize, there are two major
inventions. One in the scale out
network, which is
pretty much all OCS.
And then there is re-architecting of the
scale up network to go from 3D Taurus,
which TPUs are typically known for
to make it inference specific
and use board flight topology. So,
that's my long spiel.
Very good. Thank you, Professor Vic. And
yes, just as a reminder, so so why we
wanted to spend a whole time talking
about what Google introduced is because
again, we're seeing these big shifts
from one chip that does everything to
two chips, training and inference, but
it's not just two chips, it's two scale
up networks, 3D Taurus for training for
dense neighbor to neighbor communication
and then the board flight for inference
scale up for mixture of experts, which
is again sort of proving the point that
a lot of people have been saying is it's
no longer one size fits all, not not for
silicon, not for networking but actually
the data centers, the complete data
centers are being architected around the
workload. And so, you know, whether
you're a startup in this space or you're
tracking optics, like, you know, this is
a big shift that we we see from Google
and then of course there's lots of
interesting questions like will we start
to see this level of network innovation
coming from others like AWS with
Trainium? Are they going to stick to the
way they've architected things for their
cloud environment or are they going to
be starting to design data centers that
are uh you know, specifically designed
for MOE inference or whatever, even if
it means they have to
think differently than they used to in
the web server API era.
Yeah, yeah. It's interesting, right?
Like, now you have training and
inference have distinctly fallen into
two two different camps. They have
different chips, they have different
networking solutions.
I don't know what's next. Different
power solutions, too? Different
locations based on the direction of the
wind? You know, it's extreme co-design,
man. Like, you know, it matters. The
wind matters. No, yeah, it it definitely
is extreme co-design. And then of
course, there's a million dollar
questions that I'm sure we'll circle
back to like
is it just these two architectures
forever or are there going to be other
workloads that demand something slightly
differently? For inference, yeah, is
this sort of one size fits all? For all
inference workloads, whether they're
like world models or just, you know,
textual
inference. Yeah. Maybe we'll build out
agentic inference data centers in the
future. Some somebody will figure out
that agentic workloads need a different
infrastructure.
No, I mean, okay, I'm glad you mentioned
that because I still want to know more
about like where CPUs fit in this
communication, this network topology.
Obviously, they talked about the Axion
CPUs to feed the TPUs, but what about
all that other
all the other agents that are just
running on CPUs and virtual machines
somewhere. I know that a lot of them are
just kind of long running and latency
doesn't matter, but what about the ones
that where may latency does matter? Do
those come into the networking topology
somehow?
I don't know. Come tell us to teach me.
There's so much to learn here. This is
just scratching the surface. We haven't
even talked about like other stuff that
I saw on their core in the
CAE, which is called collectives
acceleration engine. Yes, yes, I don't
even know what that is. I haven't gotten
around to reading about it. Yeah, yeah,
we'll have to follow up on that. I I did
a little bit of reading and and it
sounded like it actually is related to
networking in that it sounded like
offloading some communication stuff to a
specific accelerator. So, yeah, I think
I have written down here like the CAE
collectives acceleration engine um
it the each TPU AI has two tensor cores
and one CAE on a chiplet die and the CAE
offload offloads all reduce, all gather,
all to all type collectives. It's a
workload specific accelerator. It's kind
of like Nvidia's sharp. So, it's it's
it's kind of similar to what DPUs do as
well, which is how can you let let GPUs
just do as much matrix multiplication as
possible, let CPUs not get in the way,
save those, you know, for doing some
messaging stuff maybe or feeding the
TPUs, but then as much of that
networking stuff you can just put it on
a network specific optimized silicon.
So, it's just kind of
it's turtles all the way down,
optimizing everything. Yeah, it's true.
All right, that is too much information
for anybody to process. This is going to
be going to have to split this up into
16 clips, I think. I don't know. It's
like It's like a whole course on OCS and
Google network. Yes, we hope that you
liked Professor Vic's lecture in near
real time after Google's announcement
yesterday. Thanks for listening. That's
it. If you're enjoying Semi-Doped, the
first thing you should do is just tell
your friends. We are so happy when we
see people sharing our videos. Thank you
so much for that word of mouth
recommendation. Subscribe to our
newsletters if you haven't yet. I'm sure
Vic and I will write about this more in
depth. And yes, thanks and we'll see you
next week.
