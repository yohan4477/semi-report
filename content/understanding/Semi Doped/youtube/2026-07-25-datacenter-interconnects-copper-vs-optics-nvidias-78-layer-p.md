---
source: https://www.youtube.com/watch?v=1mkGZgYhulo
vid: 1mkGZgYhulo
title: Datacenter Interconnects: Copper vs. Optics, Nvidia's 78-Layer PCB, Co-Packaged Optics (CPO)
date: 2026-07-25
duration_sec: 2952
channel: Semi Doped
kind: transcript
---
The biggest computers in the world today
are basically not in single boxes,
right? They are in entire data centers.
And the whole point about this is that
all these chips are intended to work as
one big computer. But the whole problem
with this approach is that the compute
capability has grown much faster than
how you can hook up all these chips in a
data center together. So today's compute
capability is more restricted by how the
CPUs and GPUs are interconnected in a
data center rather than this performance
of the silicon by itself. So the biggest
problem facing data centers today is how
to hook up all these chips to work as
fast as possible. So networking is all
the rage today and it goes from a wide
spectrum of whether to use copper,
whether to use optics and where to put
all this stuff together. So by the end
of this episode, you should be able to
understand, you know, why we need
networking to begin with, what are the
three kinds of networks um that all data
centers are built up from, and why
perhaps co-ackaged optics is coming.
That's what we hear. We don't know.
Hello everyone and welcome to another
semi-doped podcast. Uh I'm your host
Austin Lions from Chipstrap and with me
is Vic Shaker of Vick's newsletter. Hey
Vic, what do you say? Should we talk
about data movement interconnects?
Yeah, we should do this because it's the
biggest problem that we are facing in
the history of computing because in the
past we've always had the discussion of
what is the per core performance of a
CPU or then you know multi then we went
to the multi-core era like hey we have
you know 16 cores in this chip or even
servers server grade chips have like 256
cores and then uh then the GPU era came
and then you could put in the
accelerator cards in your gaming PC and
then you got you could get graphics
acceleration and we could uh you know if
you remember there was this Nvidia uh
SLI which is like basically that you
could put two Nvidia GPUs together and
you could put this uh local interconnect
bridge I I I forgot what SLI is actually
called but it's basically think about it
like a bridge that is like an
interconnect between two GPUs so that
they work as one you know that's like
the simplest form of what we're talking
about here Nvidia SLI was a way to make
two GPUs work as one but now we need to
make you know a 100,000 GPUs work as one
for LLM reasons so networking is the
biggest discussion today totally and you
know obviously for training it's all
about like yeah how can we have a a data
center size brain but even for inference
you know this is why we're going to
scale up domains of 72 GPUs and
eventually beyond is even with
large, you know, frontier models that
have 10 trillion parameters and their
mixture of experts. Um, we are getting
to the point where uh preill and
especially decode need as much memory
bandwidth as possible. There's so much
data movement that it's all about like
how can we actually put together a bunch
of chips on this scaleup fabric. And
we'll talk through all of these scale
up, scale out, scale across, scale in,
all that stuff here. But it's not even
just about training but even inferences
demanding lots of data movement to be
able to do frontier models at high you
know throughput but also obviously large
batch sizes and so don't let people
think that this is just about um
training but this is also an an
inference story too.
&gt;&gt; Yeah for sure. So whenever uh we talk
about data movement right so it involves
data movement at all levels that's what
is interesting about this uh data
movement could be restricted to uh
information moving between memory like
HBM to the GPU so that is like a really
short distance over which you need to
move a lot of data really quickly and
that's just because of the way LLMs work
you need to read a lot from memory all
the time and the faster you can do it
the more performant your LLM is right in
inference for example in training it
would mean that uh a faster network
bandwidth between memory and uh you know
uh the GPU or overall bandwidth being
high implies that your training run
finishes faster and that is everything
because everybody wants to be in the
next uh biggest model everybody wants to
train it before the next guy gets there.
So that's the whole idea. Everything
gets faster, right?
&gt;&gt; Yep. Yep. So should we share some slides
in this talk so it's a little bit more
visual? We've heard from lots of our
YouTubers who are awesome. Thank you for
watching us and they've said we want
more visuals. So if you're listening, of
course, you know, we'll try to describe
it so that you can understand it as
you're uh you know, lifting weights or
something. But for those of you who are
watching, we're going to pull up some
slides here and we'll talk through some
of them as we go.
&gt;&gt; So the whole data center essentially has
networking on three different layers. So
the first one is uh scale up which is
literally what you think it looks like.
You go up a rack. So you have a rack
full of GPUs and then you hook them all
up going from bottom to top. So that's
scale up. And then the other dimension
of scaling is the scale out network
which means that you can have different
racks each of which has its own scale up
network but now you hook them up all up
together. So that is scale out. And just
between these two, you can al already
start to tell that scale out networks
are kind of longer reach networks than
scale up, right? Because scale up only
means that you have to go within a rack.
And if you've never stood next to a data
center rack, you know, you can imagine
that it's about the height of a tall
adult human or a little bit higher. Um I
think it'll be like maybe 7 foot 6 to 7
ft high racks. That's about the whole uh
the length of the rack that uh scale up
network has to cover scale out. It
depends on how many racks you're going
to put. So if you put you know one of
these super pods or something you know
you could travel a dozen racks um across
from east to west by the time you hook
them all up right and then all of the
racks in a data center are all scale
out. But if you decide that you want to
now hook up a entire second campus maybe
located 20 mi away 50 mi away you need a
whole new network to do that and that is
called scale across right u so you you
you can even hook up data centers to act
as one big chip. So it's not just uh you
know one data center that acts as a big
big chip. You could hook up five of them
or two of them whatever that's called
the scale across network and this scale
across network has the largest reach of
the three. So it because it spans
obviously you know tens of miles right
uh so the technologies used in each of
these layers are substantially
different. So let's talk about these
because someone listening might say like
well why does scale up why do we call it
something different than scale out for
example why and and you hinted at it
that there's different technologies that
are used um whether you're staying
within the rack versus rackto rack um
versus building to building now a couple
things I wanted to uh mention so scaling
up like the problem that we're trying to
solve is in a dream world we would just
have like the biggest compute with the
most memory possible and it would just
you know that would be your rack. It's
just like what like uh you know like
Cerebras for example like they've just
got all these um chips on one wafer and
they got a ton of compute and they can
all communicate really quickly on that
like wafer within to each other. Um the
the problem is the way that uh the
industry works today. GPUs are packaged
maybe it's it started out with one die
then eventually made its way to two die
but it's packaged with a discrete amount
of high bandwidth memory on a particular
chip and and you know in the future you
know some of these uh a AI A6 and
startups are they're choosing you know a
certain amount of HBM and maybe a
certain amount of SRAMM or making
different memory decisions that we've
talked about in other episodes but at
the end of the day each GPU only has
access to so much HBM and what we want
is um more HBM than what's possible to
physically package on it. So we want to
make two different GPUs let's just say
on the same board for example or in the
same server node um forget the whole
rack even within the same server node we
want neighbors you know GPU A and GPU B
to be able to access each other's memory
as if it was their own. So scale up is
really defined as how many other GPUs
can I talk to at low enough latency that
it feels like we're sharing memory and
this is you know RDMA um reaching out
and uh you know talking to other
accelerators memory that's what this is
all about and so when you ask yourself
like well how how big could my scaleup
network be it it one way to think about
it conceptually is like well it can be
as big as when I talk to every other um
GPU, it feels like I'm actually
accessing my own memory because the
latency is so low, you know, using
NVLink or something, for example, um
some high bandwidth fast um network. So,
you can actually have a scaleup domain
that spans two racks. It's like
technically possible so long as GPUs
between the neighboring racks are still
so close and connected in such a way
that it feels like you're accessing each
other's memory as if it's your own. Um,
so that is scale up. And then scale out
is of course like now when I'm talking
my rack and that rack like you know 30 m
down obviously there's going to be
enough latency, enough hopping through
switches and things like that that it
won't feel like I'm accessing their
memory. So I won't I won't try that.
will communicate in a different way and
send uh information differently. Um I
also want to just mention one other
thing. So east west like everything on
the same sort of like high bandwidth GPU
toGPU communication fabric. My
understanding is that's east west and
technically when people use north south
usually I think they're talking about
talking to the front-end network like
GPUs talking to external CPUs like a
like a the chat you know I'm chatting on
a chatbot and it it's gets sent in
that's like the north south network.
&gt;&gt; Okay so we've got this slide from Nvidia
that starts to show that scale up scale
out scale across like we've hit on at a
high level. Um, and of course, now
there's another new term because why
stop there? Um, on the far right side,
we've got scale above. So, hey, what if
you have um data centers that aren't
physically connected via fiber optics,
maybe, you know, 50 miles apart, but are
actually literally in space and and
there's um, you know, communication, I
guess, uh, through satellite frequencies
instead of uh, fiber optics. And then on
the far other end, we've also started to
hear about people talking about scale in
um which do do you want to say anything
there on that or do we plan on covering
that today? Not too much, but there is a
whole networking uh effort to make uh
the connections within a compute tray,
you know, the thing that slides into a
rack that holds maybe the two GPUs or
whatever. You could talk about
networking even within that. like how do
you make that faster? We won't cover it
too much today, but we'll briefly touch
on it um as we progress along. So these
two are like really outside the norm,
you know, of what normally is in the
conversation of data center networking
that is scale in and scale above, but
they do exist. Yes, totally. All right,
so let's keep going on scale up. Um, so
if the goal is to make a group of
accelerators behave like one large
accelerator, they can access each
other's memory. Um, you obviously want
the highest bandwidth possible, you want
the lowest latency possible. Um, these
are going to be short reach. So we're
talking potentially next to each other
in the same board or um within the same
server node or within the same rack. So
like a few meters at most. Um so tell us
Vic you know this is the question that
everyone talked about a lot and and
people are still talking about is this
copper is this optics
&gt;&gt; what is scale up
&gt;&gt; it's a big question right like at this
point it all comes down to what is the
speed it can handle right the whole
motive the whole mantra of this
networking at this level is copper when
you can and optics when you must so
copper is deep. It is low power. There's
always worked uh for decades. There's no
need to do anything fancy if we can
avoid it. However, there is another
problem is that when you do go to opt
optics, if you go to optics, it is very
very power hungry because the number of
cables um in a scaleup network is
enormous. And we have some pictures and
coming up we'll show you. But uh it is a
lot of cables and it's a lot of uh
transceivers on either side. So you know
you've got to make conversions into
optics from electrical you know and then
go from one point to another and convert
back into electrical. Those conversions
are handled by basically transmitter
receivers or transceivers and there are
like way too many of them, right? So
nobody wants to go to something like
optics which is more power hungry
because of these conversions from
electrical to optical and back uh if
they can avoid it, right? And that's in
this picture you see this as basically
the backend network. The backend network
is this really high-speed fabric. Think
about infiniband. Uh it could also be
Ethernet scale up, right?
&gt;&gt; Uh so these are like really fast
connections which bring down the latency
between these GPUs to be as low as
possible so that they can act as one
domain.
&gt;&gt; Yes. So scale up networking historically
it's been NVLink with from Nvidia with
NV switches. Um there's also UAL link
which is an industry standard that AMD
is spearheading but there's lots of
other people coming along um to try to
make like an open alternative for fast
scale up networking. Um and then
Infiniband
has historically been scale out
networking. Um and also Ethernet so um
Spectrex Ethernet from Nvidia and
Ethernet from others for scale out. Um
but but Broadcom back to scale up has
also been pioneering using Ethernet for
scale up. They called it sue I believe
scale up Ethernet. Um so so there's
definitely appetite as other merchant
GPU vendors like AMD or AI ASIC
companies um are also trying to connect
all of their accelerators together uh
using copper talking you know very high
bandwidth uh they need protocols so that
you could buy switches from Broadcom or
use a Marvel switch or whatever and so
there's there's some uh industry
standards that are build being
developed. So if you hear of UA link or
if you hear of I think it's called EON
now um you'll know it's uh scale up E
Ethernet Ethernet for scale up
networking. I think that's what ESON
stands for.
&gt;&gt; What about the front-end network? I
think it's like a worth a brief mention.
&gt;&gt; Okay. So so what is the front-end
network here? So the front-end network
here is all of the information coming
into the data center from the outside
world. So, this is connecting. Yeah,
obviously you've got all of your GPUs,
but like when I type uh when I use my
cloud code locally and it needs to send
all this context in, it's coming in over
the front-end network and then the GPUs
are all talking to each other doing
their thing and then it comes back out
over the frontend network.
&gt;&gt; Yeah. And then you have data center
interconnect which is like the scale
across thing that happens uh outside of
the data center. Right. So, that's
that's that's what it is.
&gt;&gt; Yeah. on this slide I'll that I'll pull
up again you know so scaling up you know
conceptually you can think of it as
adding like more and more accelerators
it
they're added in three dimensions so you
have some like within a board and then
some within the rack and you might even
have rackto-rackck connections but
ultimately they all have to talk to each
other and so there's um a lot of
thinking that goes into how do you
design the topology of the network you
can have leaf network switches spine
network switches um but obviously you
can see the trade-offs. Even when you
look at a picture like this, like if you
in the far if you got the far left
bottom GPU trying to talk to the far
right bottom GPU, there's going to be
hops through the network switches. And
so what's actually really interesting
here is if you go look at how long does
it take for um even an NVLink switch to
send information, you can um you know,
let's say it's like four milliseconds or
something. And then you start to look at
um for an LLM like uh like a mixture of
experts LLM how how many how much infer
like how many times does information
need to be sent back and forth you can
start to calculate like the minimum
amount of time for um inference to
happen. So you know um if you have a
certain number of milliseconds and you
have to make a certain number of sending
information back and forth you can
multiply that and you can get a number
of milliseconds which then can actually
tell you what um your throughput will
be. So you know like oh uh even for one
user we might only be able to get you
know 400 tokens per second and that is
the limit that maybe a GPU could do in a
particular architecture. Um and it's not
even like compute limited but it's about
data movement limited. Um so I just
wanted to share that because I I thought
it's interesting that uh inference it
it's just like another use case of
showing that inference can be limited by
uh how quickly you can move information
and how many hops you have to make and
and how each piece in the chain how long
it takes to respond. it can actually cap
the interactivity which is ultimately
like the the user experience and and and
so this is why again you've got these
SRAM based uh systems the GROs and the
Cerebras where because maybe they don't
have you know in Cerebris's case
everything is just on one wafer right
next to each other if you can fit all
the model weights in and you can keep it
all onto you know one wafer or a few
wafers you can skip a lot of this
communication hops and ultimately get a
much higher [snorts]
uh interactivity.
&gt;&gt; Awesome. Yeah, there's a lot of
networking decisions that goes into, you
know, how well tokens work out for you
when when using it at scale, right?
&gt;&gt; Exactly. Exactly. Oh, this is uh this is
one of the pictures that always like
fascinates, right? Because you can see
this rack there with like all these
cables going up the rack uh hooking up
all the cables, all the GPUs within it.
It's just uh it's just a nice way of
visualizing what kind of cabling goes on
within
a single rack. Now for a 72GPU rack, uh
you know, so because you want to have an
all to-all connection between all the 72
GPUs, which is pretty much 72 squared,
you know, you'll get like a little over
uh 5,000 cables that require to go uh
between uh GPUs in a single rack. And I
read somewhere that this this adds up to
about 2 km of cables within a single
rack. And they carry an enormous amount
of information. That is just staggering,
right? Because if you think about how
fast each of these cables are, you are
looking at in the Blackwell era, you're
looking at 200 gigabits per lane. Uh so
that's really fast, you know, now you
can multiply that up uh you know by
whatever and you have like in incredible
amount of data going by everything. In
the Reuben era that's going to be 200
GHz but birectional. So it's going to
have both directions running on a single
cable at that speed. So that's just goes
to show that the the kind of speeds that
you have on this stuff is is insane,
right? Because I bet that, you know, if
you go to Cat 6 cables that like run in
your home, for example, uh they don't uh
most people don't even run like uh like
a 10 Gbit per second in at their homes.
They don't run 10 GB networks, right?
Because you need special switches for
that kind of nobody even cares about
that. So all the stuff that runs on your
in your house, your networks, they're
all like like very slow, like if if at
all, it's like maybe running at one one
to 5 Gbps or something. We can do a
network check in your own house later on
a wired network. Don't do it wirelessly
on a wired network and see how that how
slow that is. This is incredibly fast
and you got like so many cables and
that's just one rack and then you have
like you have so many racks in a data
center all of which are carrying this
much data. Then you hook them all up
together. So it's just it's just amazing
how much networking there is.
&gt;&gt; Indeed. Indeed. We we'll move to the
next slide. So, I remember when Elon
posted this um when they were standing
up the XAI Colossus 2 data center in
Memphis, I believe. And obviously, these
are purple cables. And so, you know,
Credo is synonyominous with purple
cables. And so, I remember when everyone
saw this, they're like, "Credo, go
Credo. This is amazing." Um now I think
interestingly uh now I think some
customers are asking for different
colored cables so that it's
&gt;&gt; people aren't you know getting caught up
in like what color is your cable and and
does that should I invest in a
particular company but again um just
looking at this beautiful picture of all
these well-managed cables um is just you
know still emphasizes like uh how much
information is getting sent back and
forth just seeing seeing all these
pipes. It's crazy.
&gt;&gt; Yeah, this is Elon actually posted it
himself on X, you know. So, it's like
look at this beautiful cables
arrangement and it's like so satisfying,
you know, like
&gt;&gt; it is satisfying. [laughter]
&gt;&gt; It's also a little terrifying like holy
cow, that's someone's job to make sure
that all of those are connected and that
it all works. Man,
&gt;&gt; I know. And imagine them getting tangled
up, right? Like imagine tangled network
cables at data center scale. Like it's
impossible. You got to you probably have
to burn the data center down. You can't
fix that, [laughter]
&gt;&gt; right? Totally. So, what are we looking
at here in this one? Another Elon tweet.
&gt;&gt; Yeah, this is another one in in XAI
Colossus where you see all these like uh
I think these are optical cables that go
within a data center, right? Like these
are the cables that like hook up racks
and stuff.
&gt;&gt; Uh kind of long reach ones.
&gt;&gt; Longer reach ones. Yeah. And that's uh
very beautifully laid out as you can see
in the picture. You know, it's uh it
requires a lot of reach actually because
you just can't like hook them up like uh
you know you you know you would with the
minimal possible thing or whatever. No,
to [snorts] actually do cable management
at the data center level, you actually
need more reach than you would
physically measure the distance between
tape, you know, with tape, you know,
between different racks. You can't just
go like, oh, 12 racks. Okay, how about
uh you know we just multiply the each
rack is like 2 feet wide, 12 racks 24
feet and that's the reach. I mean that's
like just the beginning estimate like
usually you need much much more because
of all this cable management that
happens. I just wanted to put this up
there just so that now these are like
GB200 deployment in like Xiai Colossus
&gt;&gt; save us going inside and taking pictures
ourselves right
&gt;&gt; by the way which we were totally willing
to do. Uh this is the second best thing.
[laughter]
Yes, Elon, let us know. We'll be there.
Um, so I guess for people who are
listening and not watching, we're
obviously showing pictures um, first of
connections within Iraq and then between
racks and this is uh, like long distance
ones. You'll just have to go check it
out to see it for yourself. But I'm
going to flip back through these slides
and make an interesting point, which is
if you look at the cabling within even
an individual rack, there's tons and
tons of connections, lots and lots of
cables. eventually, you know, there's
some midplane stuff that we could talk
about, but um the point is when you've
got on the scaleup network, when you
have all these GPUs and they're very
close within the same rack and they're
all connected all to all, there's a ton
of connections. Now, even when you um go
look at the next picture and you start
to get some interconnections between
racks and between switches, um there's
still lots of cables. Um but as you go
farther and farther out, like on the
scale out and eventually on scale
across, there's less and less cables.
And so what's interesting is you can
think of that as sort of a proxy for um
addressable market size. So these as
we'll get into later when the optical
companies are saying like oh we want to
get into scale up um they're very
excited about it because in scale out
where where they already play um and
scale across where they play you know
you've got fewer connections. You can
think of it like a like, you know,
there's um highways that run between
towns and then you've got like
interstates that run between, you know,
LA and all the way over to New York
City. Um but obviously within a town,
even though it doesn't feel like it,
that's where you've got the most miles
of roads because you got house to house
to house to house, street to street to
street. Um and so scale up
interconnects, there's going to be tons
of connections and huge huge opportunity
and huge TAM. Scale out, not as many
connections. scale across even fewer
connections and you can physically see
it when you look at these pictures. So I
just thought that was cool.
&gt;&gt; Yeah. I wanted to go before we go ahead
I wanted to touch on the the midplane
PCB you mentioned. Can you go back to
the Nvidia slide and I'll tell you I
think this is the perfect place to
mention it. So the basic thing is that
you know when when your speed gets
higher and higher this amount of cable
doesn't reach right. So in the next
generation of uh uh racks, Nvidia
decided that they will instead build a
gigantic PCB and then come up with a
very funny and novel way of like hooking
up the compute on one side and the
networking on the other side and then
make all the connections within the PCB
itself. Right? That's like a not it's
not an insane idea because I think
people have done these kinds of PCBs
before like data center PCBs can be
pretty big and complex like this.
They're usually in the range of 25 layer
PCBs and stuff like that. Problem is
that uh this one this complex PCB is
about 78 layers I believe. So that is
because you have so much routing that
needs to happen. Like the the way I
describe this on on PCB scale is like
think of a fly over, right? Like a
clover or something like in a big city.
You got to make all these transitions
from like the north, you know, the
highway going east and this south
highway going west and nothing should
intersect, nothing should, you know,
everything should move smoothly around,
go up and above and below. That's
exactly what happens on the PCB as well.
All this traffic needs to be routed
somehow and you need 78 layers to do it.
So think about the freeway uh
intersection. Now you have 78 different
levels doing that. It's quite complex
and it's very difficult to manufacture
too. So it's quite an engineering
challenge going forward. And this is all
because they obviously want to avoid
going to optics. Right? This is really
pushing the copper story.
&gt;&gt; I don't want to say any more about it.
There are always people are
contemplating whether this thing can be
made or it can't be made because it's
too hard. But regardless, I think that's
one nice engineering approach to do it.
&gt;&gt; Yeah, that 78 layers. That's wild, man.
Um Okay. Yeah. Tell us about large scale
AI data center challenges.
&gt;&gt; Yeah. Yeah. Yeah. So ba you know when
you go to multi- building uh campuses uh
or even between u entire campuses now
you have like a whole different problem
like you have to route enormous amount
of cable uh from the data center out and
uh you know about and send it through
like all these underground fiber
networks that have already been laid out
and all that. I just want to put this in
here because it's like it presents a
different challenge, right? Like you
could have a few kilometers of reach,
you could have tens of kilometers of
reach. So the technologies tend to
become different, right? So within a a
rack, you could basically use basically
simpler forms of modulation like PAM 4
is uh one way where you just um use four
different signaling levels, right? like
0 0 is one voltage level, 01 is one
voltage level and so on. And you can
just modulate like that and send
information. It's simple. Now in data
center scale when you're trying to go
far off, you know, the comp the
modulation methods are not as simple
like PAM 4, right? Uh you you have to
end up using a lot more complex schemes
like coherent optics where you use both
the amplitude and the phase information
to send in send data over long
distances. And this is all well known.
This has been done for a long time. Um
using also other techniques like
wavelength division multiplexing in
which if you if you're looking at the
slide on YouTube, you'll see it as WDM.
So you in WDM is basically the idea is
that you will send data on uh multiple
wavelengths altogether, right? So you
can send if you use eight wavelengths at
the same time, you can send eight times
the data and so on. And uh the the
example of 8 is more of a coarse
wavelength division multiplexing. So
many times it's referred to as CWDM. You
could have dense wavelength division
multiplexing which is you could even
have a 100 wavelengths, right? Traveling
through a single optical fiber. So there
a lot of there's a lot of different
technology when you go at at scale here.
And remember that this is all optics.
There is simply no way you can send
copper over the distances required
between buildings or between data
centers at that domain. There's no there
is there is no argument here. Optics is
a must. This picture if you're seeing it
on YouTube uh I saw this online so I
thought I'll throw it in here. It's
basically just the intra building fiber
trays uh in the metadata center. So you
can just see like how many cables are
like going through that and it doesn't
even look very like cable managed to me.
It just looks like a bunch of optical
fiber just like clues together. I'm like
how how does that even work? Yeah. So I
just it's just a lot of fiber. It's a
lot of fiber. Anybody looking at this is
going to go like oh you know who makes
all this fiber by the way you know uh
Corning Glassear you know is one. And so
they, you know, as as optics picks up, I
guess there's going to be more demand
for their stuff. But
&gt;&gt; absolutely.
&gt;&gt; But again, it all comes down to, like
you said, um, is it going to be within
scaleup domain? That's even more optics.
There a lot of cables, but then scale
across also has a lot of optics and a
lot of fiber [snorts] optic cables.
We've talked about scale up, scale out,
scale across. We talked a little bit
about fibers, but uh should we talk a
little bit more about like lasers and
how you actually send the information?
&gt;&gt; Yeah. Yeah. Uh I think it all ties into
essentially u having these um optical
transceivers. What you know, if you're
looking at this on YouTube, what you're
seeing on the screen right now is an
optical transceiver. It's kind of a
beautiful thing to look at because it
has all this like gold plings and these
like transparent glass fibers coming in
and they're all like arranged
beautifully and symmetrically. uh I'm
just describing what I'm seeing
basically and uh yeah and the whole
function of this optical transceiver
uh is to convert electrical signals into
optical signals and vice versa right so
the way it uh converts electrical
signals into optical signals is that
there is a laser on this uh transceiver
and then the laser is uh turned on or
off based bas on the maybe the
information that's coming in like if
it's a zero the laser's off and if it's
a one the laser's on like this is a
simple example right this form of
modulation is called essentially
intensity modulation it's as simple as
that
and um the on the on the receiving side
you have basically a photo diode which
is a a device that converts light back
into electrons so once it senses that
the light is on it says hey it's a one
once the light is off like hey that was
a zero you know so you have both the
transmitter and the receiver inside this
and then uh you have the appropriate
electronics that goes with this the
laser needs a driver chip and the photo
diode on the receiving end needs some
amplifiers right because you what you're
sensing is basically an analog signal
which should be eventually converted
into digital signals and so on so all of
this is it takes energy it takes power
you know
&gt;&gt; and on top of all of this
&gt;&gt; if you need to and if the reach of this
optical cable is long enough, you also
need a digital signal processor, a DSP.
The reason you need a DSP is because
sometimes bits don't arrive the way you
think they arrive. Like a zero becomes a
one, a one becomes a zero. And uh by
using DSP, you can use like parity bits
like what these are are like like error
bits, right? like you say, hey, wait for
10 bits to come and then the 10 bits if
you do certain mathematical operations
should match these next two bits that
come. Uh, and if they match up, that
means the 10 bits that you sent were
correct and therefore it's all good.
Otherwise, the DSP has a way of finding
out the error bits and then correcting
for it. So, what ends up happening is
that you can actually even if the whole
link screws up and it's really terrible,
you can actually fix it with a DSP. So
that's the whole point of this this
optical transceiver assembly and I just
want to put it up here so that we
understand that you know this is this is
how the whole optics works and all of
this takes a lot of power. This is
primarily the reason that you you only
want to use this when it's really
required.
&gt;&gt; Yes. Yes. And I just want to lean into
that a little bit more. So obviously uh
the AI accelerator everything all the
communication within the chip is
happening in the electrical domain. it's
electrical signals traveling around um
currents, voltages, and so on. Ideally,
if you just communicate over copper,
you're still sending electrical signals.
No big deal. Anywhere you're converting
to optics to to the what we've been
talking about here, you have to do the
electrical to optical conversion. Then
you have to convert back from optical to
electrical. And and to your point,
sometimes you might have to have a DSP.
You might have to send parody bits, do
this all this error correction. There's
power, there's latency, there's time.
And and I know, you know, you said all
this and I'm just emphasizing that like
now when we start to scale up with
optics, you have to ask yourself, oh
man, is every GPU going to talk to every
other GPU and have to have all of these
transceivers to, you know, on every
lane? Um, and and so like what what's
your reaction to to the idea of having
to have so many transceivers for even
even for like scale up?
Yeah, that's what Nvidia has been pretty
vocal about it in all the conferences
that I've been to that they don't want
to do this. They don't want to use
pluggables to scale up a network because
each uh module you're looking at here is
about 30 W. I'd say that's a lot. You
know, considering that you need two of
these on either end of the cable and
then you got like 5,000 cables, you can
do you can add it up, right? it becomes
quite a lot and they don't want to add
to the power that is already being
sucked up by the compute trays
&gt;&gt; uh in a rack because those GPUs are like
massive massively power hungry and
nobody wants to add another 10 20% to it
because modern data center racks are
already 100 200 kilowatt racks uh and we
are not even talking about the kyber era
of racks which are like 600 kilowatt in
supposedly Right? And in the future we
want to make 1 megawatt racks. So you
know these things are already pretty
power dense and they don't want to add
to the power usage if they can avoid it.
So they're like no I mean like let's
let's not use optics if we can. There
are probably better solutions rather
than just adding optics because if
you're sucking so much more power it has
consequences all the way to the grid,
right? because you have to uh back
calculate based on all the efficiency
loss all the way to the grid because
what the grid produces is not what you
get at the GPU level. There are losses
along every conversion along the way. So
all of that matters and then there's
heating problems, right? So you need to
cool it and then you have to have the
right amount of power electronics that
can supply this much power. So
everything explodes if power goes up. So
they're like, "No, we're not going to do
this. So, we're going to stay scale up
in copper as long as we possibly can. If
we have to go optics, we'll do something
else. We'll we'll talk about why what
that is.
&gt;&gt; Nice. Very good.
&gt;&gt; Yeah. This is just the transceiver
looking at it. We already spoke about
this, but essentially the TOSA in this
picture refers to, you know, the
transmitter optical subasssembly. This
is just the fancy way of saying, you
know, all the electronics that goes into
the transmitter side. So the ROSA here
refers to the receiver optical
subasssembly which is another fancy way
of saying like all the receiver
components in one place right and you
can show this picture shows essentially
how the optical signal goes in one side
and the electrical signal comes out the
other side and there's these heat
spreaders and the whole housing this
whole thing is called uh in this picture
showing a QSFP connector but you know
you have various kinds of connectors you
have OSFP you have OSFP XD which is
extra dense which means you can even put
more optical cables into this thing. It
has more channels or you you know the
modern one that is really massive and
huge is the XPO form factor which is
basically like eight of these things to
put together. So you know this is just
like the pluggable module. It's not like
these are useless and it's not like
they're going to go away anytime soon
but they have their uses and
disadvantages.
And what is happening is as we going to
more and more uh you know faster
networks you can see like in this
picture uh that some of these p these
generations of speeds are like kind of
going down and newer generations are
picking back up right for example if
you're looking at the picture the graph
here um you know most of the networking
was 100 and 200 Gbps networking uh early
2020s
you know 2021 1 2022
uh and then you know you slowly 400 Gbps
started picking up right and 2023 and
2024 where the time when the 400 gig uh
networking took off and then you you
started seeing the the the the entry of
800 gig networking and uh that that
started occupying a sizable portion and
400 gigs are like is like kind of dying
away in 25 26 at least according to this
this this graph right uh and then The
projection is that the next generation
1.6 terabit per second networking comes
in and takes up an increasing portion of
the networking uh hardware uh and
displaces the previous generation. The
one thing I wanted to say here on this
chart is that so this is aggregate
bandwidth 1.6T that could be like eight
lanes of 200 gigs per lane for example.
Um
&gt;&gt; 1.6T is just beginning. We we in
earnings calls you you hear people talk
about it a lot. Um, but this chart is
nice to show you that like no, no,
there's still lots of 800 gig out there.
Um, there's still 400 gig out there
even. Um, and then I'll also just remind
people that, you know, with each
industry jump to the next speed, which
is usually doubling of speed, obviously
there's opportunities for every player
to try to get there first and there's
opportunities to charge more um per
component wherever they are, if they're
the transceiver or in the supply chain.
And so usually um the exciting thing is
that um the addressable market can end
up being bigger and bigger because it's
more and more valuable because it's
frontier and obviously the hyperscalers
are going to willing to pay more for
1.6T than maybe they are for 800T and so
on. So you know these are uh just the
continued cycles that companies are
racing for and trying to capture outsiz
value. But even if you're not there
first, there's still money to be made in
the other uh speeds, you know, that you
were competing in.
&gt;&gt; Yeah, the next generation is interesting
because you would imagine it's 3.2T,
right? But there is some like uh talk in
the industry generally that there is a
possibility that we would go to 300 gigs
per lane and have a 2.4 generation uh
before we go to 3.2t. That's
interesting. uh I think it's primarily
pioneered by by Google uh because they
need um all kinds of fancy
interconnections for the TPU pods. So
they I heard that this is what is being
driven. So the final thing that is is
worth mentioning here is uh really we've
all the time all that we've spoken about
optics so far has been basically the
pluggable optics which is also like
basically the what goes into the face
plate of the switch. So you can just go
plug it in and that's that's your
transceiver. But like uh we mentioned
earlier, it's essentially very power
hungry. And the reason it's power hungry
is that between the front panel of the
switch and where this actual switch
silicon lies, there is a long pathway
through a PCB, right? And that pathway
is so long that uh it's basically
terrible for signal integrity uh when
the speeds get to you know 200 gigs per
lane and you know faster or whatever. So
it really doesn't scale and now the only
way to overcome that is like using these
DSPs and all that which is power hungry.
Nobody wants it. So one idea is like
okay why do we put this optical
transceiver at the edge of the face
plate of the switch which is basically
outside the box like why are you putting
the transceiver outside the box why
don't you put it inside the box and put
it as close to the switch as possible so
that you can stay in optics as long as
possible and then you can just go
through the copper interconnect really
quickly to the switch and then that's it
like now you don't probably need all
those DSPs and life is great because
uh you don't need to uh you know make
any corrections and you don't need to
blow all this energy running the DSPs
and things like that. So one option to
do this is what is called near package
optics which is you put it on the same
board you put the optical engine close
to the switch you don't put it outside
the box you put it inside the box close
to the switch and uh yeah and then you
have a much shorter path and then uh
stuff is working great but the ideal
solution that the world wants to go to
is basically co-ackaged optics or CPO
which is you basically ally put the same
uh the GPU and the the optical engine
right next to each other and co-ackage
them using some advanced packaging
technology like TSMC's KOAS or Intel
E-IB or something like that. And then
what you have is like you have basically
a switch with an integrated optical
transceiver that is almost an entirely
optical link now because there is almost
no copper interconnect left except that
very tiny sliver that goes between the
GPU and the optical engine. So this is
where the world wants to go to but this
is not easy right the CPO approach has
been in the industry. People have spoken
about this for a very long time now,
could be even a decade. There are good
reasons it hasn't come to market yet.
It's a challenging problem because if
any one of those optical engines die,
and they do, right? Because if it has a
laser in it, lasers are terrible when it
comes to handling temperature, they're
going to die. So when they die, what do
you do with the switch now? You can't
just change out an optical engine. to
throw away the whole silicon switch made
in probably a 2 nanometer process node
technology which is thousands of dollars
and it's it's a big waste. So nobody
wants to do that. Uh so this is where
the industry is. So they're like looking
at it saying hey okay what what dies the
most? Is it the laser that dies the
most? Okay why don't we move the laser
outside the rack but we'll keep the rest
of it inside the rack. And so that's one
approach. But then um there are still
other concerns with co-ackaging it. And
so people said okay fine fine fine let's
take a step back. Maybe we'll go to near
packaged optics. It's not as good as
co-ackaged optics but maybe this will
just work out just fine. So the beauty
of this whole CPO NPO approach is that
uh it is actually much lesser energy
usage than you would do with a regular
pluggable transceiver. you could make
the energy drop to a third of what you
could get from a pluggable transceiver.
And so now all of a sudden optics has
become an interesting technology for
scale up. And that is where the industry
is today because if people realize that
if you can go to, you know, near
packaged optics or co-ackaged optics,
it's it's amazing because now you're
just only limited by what optics can do.
And remember optics can go very very
fast. Optics can go very long distances
like we spoke about in scale across. So
the possibilities are endless. If you
can get co-ackaged optics to work and
then hook up the entire scaleup domain,
you know the hundreds of thousands of
GPUs uh on the scale up and scale up
scale out networks all with optics. you
know that is that is the the holy grail
of networking uh which the industry is
headed towards and the big question
remains uh as to when so nobody knows
that.
All right. So, uh that's the end of this
episode. I think the networking idea is
a very fascinating one and there is
really a lot to be said about what
happens when each part of this whole
supply chain uh and each little bit of
technology has its own deep dive. So, we
could talk about just external lasers uh
and what kind of lasers you need for CPO
for like a whole episode. So, uh we'll
we'll cover those on like future
episodes. But if you've made it this
far, thank you for listening and tell
your friends if you enjoy this episode.
And you can always find us on YouTube
obviously, which we recommend watching
this on because of all the pictures, but
also on all the podcast platforms. And
uh if you're listening on Apple
Podcasts, please do give us a fivestar
review and hope to catch you on the next
one.
