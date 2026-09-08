---
source: https://www.youtube.com/watch?v=CFIdyjrtwgw
vid: CFIdyjrtwgw
title: A New Era of Context Memory with Val Bercovici from WEKA
date: 2026-02-06
duration_sec: 3267
channel: Semi Doped
kind: transcript
---
100,000 tokens, one megabyte of data
translates to 50 gigabytes of KV cache
working memory. And that's because
you're vectorizing. You're adding 10 to
20,000 dimensions of intelligence to
this 100,000 tokens, this one megabyte
of data. So if one megabyte equals 50
gigabytes, and that's just at the
beginning of one session for one user.
Welcome to the semi-dote podcast. I'm
Vicram from Vick's newsletter on
Substack and with me is a special guest
today, Val Burkovichi, chief AI officer
at WKA. Weta is a California-based
technology company that provides an AI
native data platform designed to solve
the massive data bottlenecks found in
modern high performance computing.
Founded in 2013, the company is
currently valued over 1.6 6 billion by
focusing on the infrastructure needs of
the AI era. In today's episode, we'll go
over WEA's technologies, especially in
the context era of AI and with what it
means for the future of inference at
scale. Thanks, Val, for uh being on the
podcast with us. How you doing?
&gt;&gt; Really good. Excited to be here. Very uh
very enthusiastic and new fan of the
newsletter.
&gt;&gt; Great. Thank you so much for giving
feedback on my article on context memory
storage. It is a big area and I learned
a lot from all the articles on the WA
website and so it was fantastic. Uh the
whole the whole thing I learned about
context storage is really fascinating
and I think we'll get into some of that
today with uh our listeners too and
break down a lot of what's going on. How
does that sound?
&gt;&gt; Absolutely. My favorite topics. We
should go. Let's go.
&gt;&gt; Awesome. Let's start with a brief
background. So you were a former CTO at
NetApp. Uh my internet travels showed me
were called the cloudsar for leading the
cloud storage s strategy and now you are
a chief AI officer at WKA. So can you
what's your transition here? How did you
get to working on storage solutions or
is that something you've always been
doing?
&gt;&gt; Yes and yes and yes. You know, it's uh
it feels like deja vu because I remember
I left NetApp actually joined a small
cloudnative storage startup called
SolidFire out of Boulda, Colorado and
then got reacquired back basically into
NetApp surprisingly enough and by then
we were doing cloud storage and that was
after VMware kind of a golden era of
enterprise storage and these NAS and SAN
acronyms of the past and I figured you
know Kubernetes was really cool. I
actually got involved with the Borg team
at Kubernetes, Craig McClucky and Sarah
Natne, Joe Beta and others and we
created the cloudnative compute
foundation under the Linux foundation
together. You know, I got on the board
the the first board governing board of
the CNCF. So I thought around 2017 there
was nothing left to do in storage and I
left it. Uh but it was a very disruptive
time back then, you know, 2012 to 2015.
It's hard to remember that now, but
cloud was hyper controversial, right?
kind of as controversial as AI eating
software today. Back then it was cloud
software eating the world. So it's deja
vu in that you know it's it's just big
transitions all over again. And at Weta
I joined again on the promise of
actually not joining another storage
company. And what I mean by that is that
you know we we were using the term data
platform last year. And fundamentally
that confuses some people because it's
an overloaded term. There's so many
things up and down the stack which we'll
get into that could be called platforms.
But fundamentally what WKEA provides is
high-speed storage and memory for AI
infrastructure which ultimately is the
key bottleneck that we'll be diving into
right now.
&gt;&gt; That's awesome. It's amazing that you
you're saying that in 2017 nobody really
thought about storage solutions too
much. It was considered boring and you
know probably commodity but fast forward
not even a decade things have turned
around entirely. We have entire
generative AI and people running agents
all over the place and we want to store
infinite context and the need for
storage has completely changed within a
short span of a decade. Who would have
thought, right?
&gt;&gt; Exactly. Exactly.
&gt;&gt; And uh yeah, it's uh you know it it
changed even three weeks ago which we'll
get into, you know, with Jensen's latest
announcements at the CES keynote.
&gt;&gt; Yeah. Let's get into that straight away
then because uh for those who missed
that announcement, it's at CES 26 Jensen
announced that they are in uh
introducing an inference context memory
storage platform uh as a firstass
citizen uh into the whole uh Ruben
platform and this is something that's
going to be here uh for the future and
is is here to stay because we need a lot
of uh context going forward especially
in the agentic AI era. But maybe we
should just start with what context
memory is and why we need it so badly
today.
&gt;&gt; Yeah. What we've learned obviously uh in
the just breathless evolution since
three years ago that chat GPT moment
three years ago at about two or three
months now is November of 2023 I guess
no 2022 right uh what we've learned is
that prompt engineering came and went as
sort of an important focus. you know,
kind of instructing the models was
important at one time when the models
really didn't understand how to process
large attachments, if you will, large
memory. Uh, then we reached like the era
where yeah, you know, ra retrieve
augmented generation rag where we
figured out ways to attach just the
right snippet of large attachments into
the limited memory and be able to
instruct the models to give us very
clever answers. So chatting with your
PDF, you know, was one of the most
interesting things you could do,
particularly when it was a large PDF and
you only had to chat with a subset of it
automatically. We're very much in the
era of agents right now. So, of course,
the viral agent of this week is
Claudebot and Moldbot and the amazing
things people are doing with it. What we
are seeing right now is that agents, I
like to say, are not really a singular
thing. you either have an agent swarm on
your hands with dozens and hundreds of
sub aent tasks and and sessions or
you're not really doing an agent at all.
And at that point now you basically have
hundreds of parallel instructions to a
model with hundreds of parallel
attachments so to speak whether that's a
codebase whether that's documentation
whether it's a video stream telemetry
logs etc. uh and there's still even
though the models have gotten smarter
about understanding larger and larger
context windows there's never enough
right uh so context memory now a way to
extend the memory windows extend the
interactivity of these models is is the
hottest field and there's lots of
different ways to create memory for LLMs
and for even diffusion models and I
always like to say if you think you know
how to do this from your experience even
two to three years ago It's almost
easier to just unlearn what you know
about memory and storage and relearn
from scratch because it really is very
different this time.
&gt;&gt; That's amazing. Uh I want to get into
what exactly has changed. But before
that, I just want to uh quickly go
through what you mentioned about prompt
engineering which was all the rage in
the early days of GPT. And I think it
evolved most recently into a slightly
different form of context engineering
which I think Manis AI has some really
good documents on their website of how
they go about this. And the key of uh
context engineering is that you want to
keep uh as much as the previous
conversation already you know in the uh
GPT inference or uh the cache that it's
holding and just add on sequentially to
what you can like don't delete anything
from your instruction sequence instead
add on to it because what that allows
you to do in the era of context
engineering is you can
reload a lot of the KV cache that was
already stored and then you know it's
incremental so you don't have to
recomputee. So all of the storage stuff
in the era of context engineering and
now agents and sub aents all comes down
to I suppose storing this key uh matrix
called the key value cache that really
explodes with larger and larger context
that you put into the system. So with
this in mind, so how exactly has stuff
changed from uh a few years ago to now,
what exactly has changed?
&gt;&gt; The biggest change really is the fact
that there's never enough memory. If you
just do the math, and the math is not
complicated. It's not calculus, but it
is a multivariable formula. When you do
the math of, for example, loading the
weights of the models, which are very
big, we're in the era of trillion
parameter models right now. The hyper
popular Opus 4.5 is a trillion parameter
model. The latest DeepS seeks are
trillion parameters. Kimmy K2.5 just
came out yesterday. The thinking
version. That's a high-end trillion
parameter model. Merely loading the
weights of these models into memory is
more than a big GPU server can handle.
It's literally more than like you know
an H100 can handle. And that's still a
very very popular GPU server. You need
an H200. very often you need multiple
hoppers or even more than one Blackwell
server which is eight GPUs per server
just to handle the weights of these
models and then you and I enter the
picture and we open up a prompt session
right and we start chatting with the
model we start feeding attachments we
start feeding context into the model uh
and very quickly the math gets quite
brutal because uh the the round numbers
about 100,000 tokens which is roughly a
megabyte of actual data and that could
the system prompts that can be at the
model level, at the agent level, at our
own preference level. Then you've got
the prompt itself. Then you've got the
data in question, the real context that
we want to focus on, those attachments,
so to speak. Uh 100,000 tokens, one
megabyte of data translates to 50
gigabytes of KV cache working memory.
And that's because you're vectorzing.
you're adding 10 to 20,000 dimensions of
intelligence to this 100,000 tokens,
this one megabyte of data. So if one
megabyte equals 50 gigabytes, and that's
just at the beginning of one session for
one user, and we have multiple users
kicking off agent swarms, so hundreds of
subtasks per user, you see that quickly,
uh, you know, you're you're very much
out of the working memory, the high
bandwidth sort of primary memory tier
that's on the GPU package itself. And
last year saw a really nice evolution of
the engineering of realizing we have
these old concepts, right? Virtual
memory concepts of being able to use
other storage tiers or other tiers, if
you will, of memory, uh, and and and
basically be able to, you know, flush
data, old memory pages out, you know,
bring fresh memory pages in. So we've
applied these algorithms and concepts to
you know context memory right now which
means and Nvidia has a very nice I think
you included it in your newsletter a
very nice hierarchy now of essentially
the first level is a high bandwidth
memory on the GPU package itself and
that's memory if you're a gamer you know
this right it's memory on the GPU card
itself so to speak it's independent of
the motherboard's memory every GPU on a
server there's eight GPUs each one has
its own dedicated some people call it
VRAM for video RAM if you're kind of
come from in the gaming background. Data
center people call it HBM, high
bandwidth memory. So there's dedicated
memory per GPU, and that's where most of
the work really happens, but there's
never enough. By the time you load the
model weights in a few of our own
prompts, you're out of that memory. And
now the software layers. So we have very
popular inference servers VLM, SGLANG,
Triton, you know, TRTLM from Nvidia that
understand now with these KV cache
managers how to tier the memory, how to
basically, you know, tier down to other
memory. And now we go to the
motherboard, the shared memory across
all the GPUs on the motherboard. So
there's about one terabyte of shared
memory and sliced up on each GPU on the
HBM there's almost 1 to two terabytes of
dedicated memory and aggregate split
across eight GPUs. So let's say you've
got about four terabytes of actual
working memory again with today's latest
models with today's very contextrich
user sessions and agents not enough. So
context memory now and context memory
engineering is all about where do we go
next? Unfortunately, there are these
10-year-old standards called the NVMe
nonvatile memory express was the
original, you know, term or or
definition of NVMe. I like to call it
nonvatile memory extension because I
like to joke there's no s there's no
storage in NVMe. It is designed to treat
NAND flash as a memory extension using
more native memory semantics. Flash
memory is memory. It's just slower
memory than DRAM. And now there's ways
to engineer storage solutions based on
this NVME protocol into this taring
hierarchy. And the the art of it, you
know, is it is obviously still code. So
it is science but it seems a bit like
alchemy at the moment is how do you make
this lower performance higher capacity
lower cost tier of memory NVMe behave
just like regular memory to the model so
that you and I especially in a voice
chat don't notice awkward latency with a
voice agent and things like that.
&gt;&gt; Awesome. That's a that's a great rundown
of the whole technology situation we are
in right now. So just to summarize so
there is a memory hierarchy and ideally
we would want to keep all any and all
information model weights KV cache
everything on HPM and the reason is that
it's the highest G1 as Nvidia calls it
tier of memory and it is the fastest
lowest latency great if we could have
infinite of it but because of the way
it's made and the density it allows and
the supply you can actually get a hold
of it's virtually impossible to do that
right then there is the second tier that
one could then the backup option there
would be actually DRAM which is on the
CPU host and that on the Reuben platform
seems to be about 1 TB or more which is
a significant step up but like you say
100,000 tokens 1 MB of input uh to
tokens context and that explodes to 50
GB of storage requirements DRAM isn't
going to cut it either you're going to
have hundreds of users, thousands of
users each kicking off tens of sub
agents, hundreds of sub aents. You know,
the problem is just staggering. So the
next question is that obviously you go
to a even higher capacity, the backup of
the backup plan and you go to NVME
storage. Now you hope or science your
way out of this by making it as fast as
possible. So we can't tell that it's
actually being pulled from NVME SSDs and
it behaves just like HBM. That's the
ideal goal, right?
&gt;&gt; That's the ideal goal. And and there is
again some complicated formulas, but we
can maybe walk through those to
understand how that can actually work if
you piece the these puzzles together
correctly.
&gt;&gt; Yeah. Yeah. Absolutely. Now I want to
get to that formula and I love formulas.
I'm definitely going to get to it. But I
just want to understand one thing like
so NVMe storage at scale is not a new
technology. It's just a bunch of flash.
It's been around for a long time. So
what is different today between uh
the storage solutions that are fast
enough with low latency and you know the
older solutions like NFS and Luster
which have been around for like decades.
&gt;&gt; That's exactly it. They've been around
for decades. And when those solutions
started, NFS and Luster in particular,
they're very, very popular in the AI
world, were literally built around the
era of hard disk drives. We have to
remind ourselves, this is now history.
It's funny because I started my career
with these things, but it's history now.
These are antiques where essentially you
have rotating media, these rotating
platters, many many platters and you
have this head, an actuator which goes
across all these platters and you have
to wait for a platter to spin before you
can read data off of it. Then the
actuator has to move the head to where
that you know which sector which which
track like if you remember for people
that like you know vinyl records again
which part of the record you know the
data is on and then finally retrieve it.
It really is like a record player and
very much like an antique. Uh, and NFS
and Luster were excellent protocols for
that because they made assumptions
around the latencies of accessing
metadata. You know, basically like um
finding out exactly where the index card
is to find the ultimate data, you know,
looking at the glossery of the book and
so forth. That was the way that these
protocols worked. Fast forward to flash
drives. NAN flash drives first started
out as these SCSI SC small computer
systems interface devices underneath
these network protocols. Then you had
fiber channel. You had serial access
sequential access sequential access
scuzzy SAS all these other protocols
that came out of the spinning rust
spinning disc era. Only when the NVME
standard came around were we finally
able to treat nan flash as a true memory
extension. And even then uh you you
really didn't have the latency
sensitivity that you needed to to make
flash behave more like memory where NVMe
devices and this is going to be very
important for your audience and your
readers going forward are are also going
to go through an upcoming evolution
called high bandwidth flash. And so
these flash devices speaking the NVME
protocol are nothing more than layers
and layers of nan flash with these like
ARM style microcontrollers in front of
them. And each of these microcontrollers
has a work Q and you have multiple cues
per device. You have multiple devices
per NVMe fabric. So the art to this is a
modern protocol. We call it neural mesh.
And it's a modern protocol that actually
understands that there are thousands of
cues across tens of thousands of devices
in a fabric. And you have to understand
natively the depth of each cube. So you
understand at a global level for every
read and write across the entire system
what you know that latency is going to
be across the entire system by
understanding all the individual
components. That's what we call neural
mesh. That's the magic of Weta and it's
because Weta has the advantage of
timing. We were designed from the era
where there was no spinning disc. We
tier to that but we don't use it
directly. You know there there isn't
really a need for NFS or luster. It was
just a brand new era with NVMe. And
another key thing here is when Weta was
born, the networks, the high-speed
networks at supercomputers were faster
than the motherboard. And even today, I
have to keep reminding people that
everyone just assumes the memory
hierarchies are static. The motherboard
is always the fastest way to move data
around and everything on the network is
the next compromise down. And it's
inverted now. And Nvidia by acquiring
Melanox and building now, as Jensen will
say, they don't ship chips, they ship
systems. And the systems are these
chipsetworked together to form these
amazing AI factories, these
supercomputers. They all depend on the
fact that the network is actually faster
than a motherboard. And that's how the
GPUs are not kept waiting are actually
able to collaborate together and and
behave like a giant GPU.
&gt;&gt; That's awesome. There is there is so
much to talk about that like I'm glad
you mentioned all the things that you
did. So uh I want to hit on uh the
latency aspect first. So essentially the
biggest concern historically over the
storage solutions of the past has been
latency and they're primarily designed
around spinning rust discs which are uh
completely different when you're looking
at NAND flash NVME storage today and
those protocols are not really valid
anymore and they kind of need to be
rewritten. So in terms of the equation
you mentioned below how does all this
latency translate into maybe time for
time to first token or uh how does that
whole thing work out you know how does
it relate? Yeah. So, a very important
question, a vital question. You know,
the motherboard math is again
non-intuitive because you have to factor
in the software and the hardware into
the final latency equation for all of
these pieces. Latency particularly
because we have two kinds of kernels. We
have the kernel that boots the server,
the Linux kernel that runs on the CPU.
Then we have the kernel that actually
runs the inference server. That's the
GPU kernel. We hear about CUDA all the
time, right? CUDA kernels in the Nvidia
world. Um and so those are two different
kernels that have to communicate on the
same server and the inference server you
know that runs our deepseek that gives
us our tokens from deepseek or Kimik2 or
GLM or all these wonderful new models
miniax etc. Open AAI of course and
anthropic included uh these kernels are
communicating between each other. So
when an LLM is processing your request
and it runs out of memory, it still
communicates before it runs out of
memory at nancond speeds and with a high
bandwidth memory and very very low
nanconds. We aren't even talking about
this little thing called SRAMM which we
should come back and talk about because
that's really what the whole Grock with
the Q acquisition was about.
&gt;&gt; I always I always joke Yeah, I always
joke that that Nvidia should have
labeled SRAM as the G0ero tier, but I
think they will. they have nowhere to go
now, right? So there has to become the
G0ero tier. Absolutely. But in order to
not confuse matters, let's just focus on
G1 and and and above.
&gt;&gt; So with the G1 layer, that's nanoseconds
and that's the GPU kernel. As we know
now, we're basically tearing and
including G2 in this hierarchy very
commonly today in every modern LLM
inference environment. Uh and that
crosses the motherboard now because
you're going from the GPU kernel across
something called a bounce buffer.
historically sometimes now a
chip-to-chip interconnect between the
GPU and the CPU and the memory that the
CPU addresses and on paper the DRAM the
DIMs the DRAM dims on the server
motherboard that the CPU controls on
paper it's also nanoseconds but not in
reality by the time that communication
between the GPU kernel and the CPU
kernel happens we're into the
microsconds of latency so already kind
of you know three orders of magnitude
between the HBM and the effective of
DRAM latency and that's not great but
it's functional right the inference
servers definitely do enough parallelism
and enough asynchronous memory copies
and things like that that it doesn't
feel like a big step down however uh the
big step down now comes from various
legacy protocols entering this equation
by tiering the G2 memory the the DRM the
CPU DRAM to storage uh they introduce
enough overheads because of the way they
go between user mode and kernel mode and
the way they deal with metadata that
you're not just going another three
orders of magnitude from you know
microsconds to to milliseconds. You're
going to many many milliseconds two
three four five milliseconds. thousands
and thousands of microsconds as you make
that transition and that's where you hit
a wall the kind of the memory wall
because that's where it's very
noticeable additional latency to the mo
to the model and then to you the user
and an agent right really notices that
because if the agent spinning up
hundreds of subtasks they can either
complete in minutes or they can complete
in hours with this additional latency.
So the key design goal for Weta is to
keep this real world effective
transition from high bandwidth memory in
nanoseconds to DRAM in microsconds to
flat microscond latencies at DRAM
performance levels but with the benefit
of flash capacity. So it is a best of
both worlds scenario when you understand
the engineering and the math. And
instead of capping out at four terabytes
of memory per server, you can extend
that G2 layer now to hundreds of
terabytes easily to pabytes. And in some
extreme cases, we've done the math. Some
of the biggest, you know, LLM apps like
Cursor of the World and the various
models they use are processing tens of
trillions of tokens a day. and the KV
cash numbers that you refer to,
especially that great Manis blog from
last summer. I call it the two billion
dollar blog because of course they're
part of Meta now for two billion dollars
that requires an exabyte of KVach to
service trillions of tokens a day
effectively. So, we're going to be
seeing this. This is why Jensen called
it the biggest future storage market of
the world because when you're dealing
with an exabyte of memory, uh you you
have to think about some kind of storage
semantics at least and even the industry
now uh referring specifically to context
memory is referring to it in the context
of cache writes and cache reads. sort of
like a database or a file system, but
remembering it's at these crazy memory
speeds, hundreds and hundreds of
gigabytes per second, ultimately
terabytes per second, at these crazy
capacities, at these microscond rigid,
you know, tight latencies.
&gt;&gt; Awesome. And the all of this is possible
today only because of that network layer
that you mentioned earlier. The fact
that there is so much innovation across
the interconnect and networking space
like infiniband or Ethernet that hooks
up or scale in scale up scale out across
the data center. You've got this really
high bandwidth um fabric that connects
everything together including storage.
So now you're able to serve pabytes of
data over this high high bandwidth
fabric right to the GPU. And I believe
that there there are technologies from
Nvidia for this like GPU direct to
storage. So it bypasses a lot of these
host controllers and all these middlemen
and just gives the information straight
to the GPU. Right.
&gt;&gt; Precisely. So so many acronyms here, so
many protocols we're throwing out here.
Hopefully we're not losing people. But
after you deal with the storage
protocols, there is an effectively a new
memory protocol. Uh so memory access is
like a native thing. you access the HBM,
you access a DRAM, etc. Uh direct memory
access is figuring out again how to
access it. Remote direct memory access
is where things get interesting where
you access memory at memory latencies
and memory throughputs, but you access
it over a high-speed network of some
kind. That can be these other obscure
technologies, the memory pool
technologies from CXL, like an extended
PCI over network, or it can actually be
the Melanox style uh high performance
RDMA networks. And unfortunately for the
readers, you just have to get used to
these things being called multiple names
meaning the same thing. So NVLink is a
brand, that's one name for it. Backend
network is another name for it. East
West Network is another name for it.
Nickel NICCL network is another name for
it. if you're a developer, they actually
all mean the same thing. They basically
mean another set of network adapters on
a GPU server that are just dedicated to
very high-speed traffic. And what's
fascinating to me and it's good to be in
the networking business nowadays is what
Jensen announced three weeks ago is
effectively a third network on these
servers. You have the regular
communications network which again goes
by multiple names. Front-end network is
a common one. North south network is a
topology that's another name. storage
network just you know internet you know
public access network that's one way to
get inside these servers that's often
one or two high-speed network adapters
again traditionally you've had eight or
more network adapters Oracle cloud for
example gives you 16 east west network
adapters now there's a third network
that's being introduced with the the ver
rubin generation so sec second half of
this year that will be powered by these
more powerful data processing units
these super network adapters called
DPUs. The brand uh the brand name is
Bluefield and the Bluefield 4
generation. So now with Bluefield 4 on a
third dedicated network, you now can
isolate GPU traffic from Nvidia's
preferred way to do context memory
traffic from the regular front-end
network for all the other traffic if you
will. And what's fascinating to me is
you've got resource constraint geniuses
like DeepSeek over in Wanghu in China
and they don't play by Nvidia's rules,
right? they they utilize every single
ounce of resource that's available to
them. So they're going to be some of the
first I predict perhaps alongside WA
we've been doing this as well to publish
how you can use all these networks you
know dynamically just in time to get all
the bandwidth you can just in time you
don't really have to go on these
dedicated toll lanes if you will.
&gt;&gt; Does this network have a name? I know we
have we scale up scale out and scale
across. What is this thing called?
&gt;&gt; I think it's going to be called the
context memory network right there.
There's there's no other logical way to
describe it. You can add fancier, you
know, sub, you know, adjectives to it
and all that and superlatives, but it is
a dedicated network for the blue field
adapters and it's it's supposed to be
dedicated in a clean architecture, just
a context memory, so it doesn't
interfere with the occasional bullet
train of traffic on the GPU network and
it doesn't collide with the regular
front-end network for regular user
traffic and and other more traditional
legacy storage traffic.
&gt;&gt; Awesome. Now I want to before I get into
neural mesh and you know augmented
memory grid which is WA's uh unique
solution here I just want to touch upon
what you mentioned about high bandwidth
flash because you're right that is a
very interesting uh con concept and idea
for the listeners of this podcast. Uh so
where does that fit in? Because the idea
of highbanded flash is that you take a
bunch of uh flash chips and you stack
them up like you would do HBM and all of
a sudden you have this entire high
capacity. You could get like I don't
know 4 terabytes on a like a little
thing that looks like HBM. Uh and now
the question I think I have had and a
lot of people would I assume have is
where do you put this thing? Like if you
put it on next to the GPU just for
context storage, you're now taking away
from the beachfront of HBM. So nobody
wants to give up HBM for high bandwidth
flash. And then there is always the
question of uh endurance of flash in
general. Like if it fails on the network
storage, you could change out the flash
drive. No, no worries. But how do you
change it out on a GPU? It's terrible
when that happens.
&gt;&gt; So where does I bandwidth flash fit in?
It's a great question. I think we're
going to be talking about this a lot
this year, especially when these devices
ship very very soon. So, high bandwidth
flash for me, it's like a game of
musical chairs. The the first principle
science doesn't change. NAN flash still
nan flash. If you stack a lot of it, uh,
you know, you basically have to figure
out exactly, you know, where the the the
wear leveling is because what most lay
people don't know about flash is it has
a very finite life cycle of how many
writes, how many four kilobyte blocks
you can write to it before it just stops
accepting writes and then the device can
only be read only. So kind of great for
archive after a certain point basically
because it becomes inherently immutable,
but that's not what people want out of
storage. is absolutely not working for
memory, right? Memory has to have these
very rapid load stored operations and
billions and trillions of them in
parallel. So high bandwidth flash is
essentially taking all the same
components stacking more NAND layers.
Now instead of stacking you know QLC
layers these quad or quintuple layer
cell which are very very dense but don't
endure rights very well over many many
years maybe it's stacking more of these
TLC triple layer cell that endure more
rights but it's 3D stacking of flash
depending on again the grade of the
flash and then how many controllers and
cues do you put in front of it so high
bandwidth flash is not magic it's just a
lot more controllers right a lot denser
ARM style controllers and other kinds of
AS6 that are in front of denser and
denser high endurance flash so that you
can have more cues and ironically you
know WA provides us at a fabric level
today what WA provides is a single way
to see thousands and thousands tens of
thousands of cues across thousands of
NVMe devices as effectively one drive
you know that's what this WA neural mesh
software actually does so what we're
going to see is just more and more
density available to the market. It
absolutely will be a denser option now
for our own stack and through our
partners like Dell and Super Micro and
Hitachi and HPE and so forth uh you're
going to be able to see these you know
meshes of even denser high bandwidth
flash essentially the promise is at a
lower cost extend the context memory
comfortably into the pabytes and
exabytes because I predict by the end of
this year we're going to be seeing more
than one exabyte per GPU, you know, per
super pod of just context memory.
&gt;&gt; Fascinating. So, the nice thing about
neural mesh is that it gives you all
this on a on a aworked uh drive that to
a GPU looks like as if it's local
storage. It doesn't really know the
hardware behind it from a software
sense. So from my looking at WKA's
website, it seems like the Axon is a
critical innovation that enables this
whole thing of what is called converge
storage. Could you maybe dig into that a
little bit so we understand what the
technology is all about?
Axon is the classic definition of you
know luck equals preparation plus
opportunity, right? Axon was just
designed inherently to be very
intelligently
native to a GPU server. A GPU server, as
we've already said, has eight GPUs,
memory on the GPU, shared memory on the
motherboard, dims there, but often
comes, you know, with up to 16 drives,
NVMe drives per GPU before you add on
remote network storage to it. So, these
embedded drives were originally kind of
left alone. you know, they were very
convenient to boot the Linux, you know,
kernel for the GPU for the CPU side.
Very convenient to hold these large
model weights and load them quickly from
storage into the GPU memory and begin
to, you know, either train or infer the
the the weights and the tokens
respectively, but they were largely
ignored. And what we're seeing with a
severe supply chain crunch today in the
industry is that now you can basically
if you're a GPU provider instead of you
know getting your real you know your
data center built with all the real
estate and power and cooling and and all
the other things you have to do the
water management uh and then waiting
another you know three four months just
for your storage systems to arrive and
giving up millions and sometimes
billions of dollars of inference revenue
while you're waiting. you've got
built-in storage and memory resources on
those GPUs themselves with those
stranded drives. Axon is simply a way to
install software, no additional
hardware, and transform those drives
into either a large capacity pool of
storage. It's that's even faster for
loading weights, even faster for logs
and temporary storage. But when you have
enough of them, the math is around 50 to
60, but 72 is a nice one to one match.
72 GPUs in an NVL 72 rack. If it's about
a one drive per GPU ratio, 72 drives
actually can give you the bandwidth to
get memory performance hundreds and
hundreds of gigabytes per second of
effective DRAM performance to these
kernels and also you know it gives you
just the latency that we talked about
that if you can manage the cues on all
those drives as if they were memory
instead of storage. So not using the NFS
protocol, not using Luster file systems
which have complicated metadata
management and so forth, but just using
a native mesh architecture,
you actually create this new category of
softwaredefined memory out of standard
vanilla generic GPU servers. Uh and you
can decide how much of of those NVME
devices you allocate to storage and how
much of them you treat as memory as
truly extended context memory.
&gt;&gt; It's fancy. So what what I'm hearing is
basically you have all these uh local
SSD drives uh in a rack and those are
not always entirely used and so Axon is
a way of like intelligently carving out
a portion of each NVME drive per GPU and
then pulling all those together and
providing it as a memory tier at a high
access uh bandwidth rate and not really
storage. And this is really elegant for
most NVL72 racks. If you were to pick
that kind of configuration, you know,
instead of talking about AMD, Helios or
others in the Nvidia world, you get this
built-in scale up network called in
infiniband in these racks. And so
without even purchasing additional
network ports, which are very expensive
at 4 and 800 gigabits per second,
without purchasing expensive switches
that are 800 gigabit, you know, switches
for, you know, 32 64 ports, this is all
built in. So, it's literally just adding
Weta software in this configuration Axon
and and almost magically getting
additional storage capacity and really
magically getting additional memory
capacity without memory compromises out
of this system.
&gt;&gt; That's a that's a really clever way of
engineering it just out of software and
existing hardware.
&gt;&gt; Our engineers are are geeky to a fault
and and they love very elegant, clever,
deep tech solutions. And like I said,
that was a preparation. The opportunity
is of course the the severe NVME and
DRAM crunch today and so the timing
couldn't be more ideal for this.
&gt;&gt; Perfect. Yeah. So this entire thing if
you scale it out over the network not
you know have local SSDs that you carve
out with neural mesh when you put it out
on a just a bunch of flash drives on a
network is that what augmented memory
grid is and what is the concept of a
token warehouse uh maybe we can explain
all of that.
&gt;&gt; Yeah really important here. So let's
start with the first part of the
question. What is augmented memory grid?
It's another software configuration that
is optional. So it makes Axon optional
because it doesn't depend on using the
if you will builtin or stranded drives
inside an NVL72 or GPU rack of any kind.
It works there very very well. In fact,
it's the easiest way to get augmented
memory grid up and running. But it's
independent of that. It fundamentally
works across the three kinds of networks
we have today. We have the traditional
north south network where a lot of
conventional storage traffic goes and
some people call that high performance
storage. It's just all relative now
compared to memory. But you know that's
one way to configure AMG augmented
memory grid. The second one in the near
future second half of this year will be
over the Nvidia context memory network
the blue field network that goes to just
a bunch of flash. The best practices way
to do it today is also the third way and
these are not mutually exclusive. you
can do all of them. So the third way is
where literally as long as there is that
memory network that GPU compute network
available and that could be in the rack
that can be across an aisle that can be
across a whole fleet pretty much limit
is inside the data center. Speed of
light is a thing and you know and and
switch ports are expensive and you know
spine leaf and all that gets config gets
complicated and expensive if you try and
scale it you know out too too much but
as long as there are there's enough of
that bandwidth that east west bandwidth
again the brand is nvlink but it's not
really nvlink traffic as long as there's
enough east west bandwidth six or more
eight or more 16 maybe ports of east
west dedicated GPU network bandwidth the
backend bandwidth that AMG just takes
all of that and it naturally extends the
G1 HBM memory, the G2 DRAM memory into
the the the memory that we actually call
G1.5 because it performs at the level of
G2 memory. But the way inference
happens, if we have time to get into the
two key phases of inference, prefill and
decode, by being able to optimize those
things, we deliver better than G2
performance. It sometimes can rival G1
performance easing today's NVMe
technology but in aggregate of course.
&gt;&gt; Where does pool DM come into this? So
what are the comparison of speeds
between pooling DM over CXL versus
running AMG?
That's a great question and the key
thing is as I mentioned earlier on this
bounce buffer concept of the two kernels
communicating and actually exchanging
you know forwarding storing and
forwarding memory back and forth between
the two different buffers. Uh CXL is a
really great example of the fact that
that latency is already uh through you
know memory access through CXL already
into the microsconds. It's not nancond
memory anymore. I think CXL is a
fantastic stop gap solution today,
right? It's an innovation also about 10
years old where now if the DRAM if if
the HBM is so precious and we just don't
have enough of it and the DRM the G2 is
so precious we don't don't have enough
of it there's actually a lot of stranded
DRM in servers and what I mean by that
is it can be stranded in time so there
can be um you know model weights and
they're mixture of experts as an example
where just a subset of the weights are
only active at any one time so there
could be traffic patterns that come into
an inference service where certain
certain GPU servers and certain GPUs on
those servers are busier than others and
certain DRAMs are fuller than others. So
if you have spare DRAM that's not being
used at a particular moment, you want to
make that available to another server
that's starved for DRAM and again you do
this over yet another kind of network.
Again, it's not really a traditional
Ethernet style or even Infiniban
network. It's a CXL memory poolled
network, but it's a way to take this
this precious finite limited resource
and not have any of it be stranded. It's
a way to maximize utilization of that G2
layer. And it has plenty of advantages
because who doesn't want sort of more
access to available G2 memory, but it's
finite. You know, dims are dims. They
have the same, you know, cost profile as
uh as as, you know, DRAM memory, CPU
memory. It's a very high cost profile.
They're as limited in the market right
now and they just don't have the
capacity you want to do what Manis again
advises which is to maximize your KV
cash hit rates not evict we really
haven't used this term yet not have to
evict KV cache which is a common thing
after about five minutes of inference
operation especially for agents but keep
KV cache forever so you can bump that
hit rate that KV cache hit rate above
the industry norm of 50 60% into the
best practices of 70% if you can do it
without extended or augmented memory and
it's really exponential benefits if you
keep going up to 80 and 90 and 99% and
that's what naturally happens when you
have large capacity KV cache without the
memory latency compromise you inherently
get to 99% KV cache hit rates almost
automatically uh and there's a video you
know link we can we can leave here later
on for the reader to follow up that
discussion
&gt;&gt; but that is the nirvana of of context
engineering when you effectively can
automatically get 99% KB cache hit
rates. There are no latencies for your
users for you know for big agentic jobs
uh for voice agents in particular and
more importantly you're very energy
efficient now because the really
energyintensive comput intensive process
of prefill is done once and you decode
forever for those tokens. You don't have
to repill every five minutes. If you
want to pay a premium to Antropic and
Google and others, you can only rep
prefill every hour or so. But the
reality is we need this information for
days and weeks and as the science
evolves, we might find even months of
value in these KV caches. Uh and if you
can prefill them once and decode
forever, that is the the ideal goal here
in in in programmer talk. It's taking an
order of n operation down to an order of
one operation. That is an ideal
algorithmic optimization. And that's
really the mathematically and and
technically what the augmented memory
grid offers. And I'll pause there
because I want to also, you know, talk
about what the token warehouse does over
and above that.
&gt;&gt; Yeah, let's uh so we'll get the token
warehouse is obviously the next
immediate concept we need to hit up. Uh
the the whole point about the KV cache
hit rates is that if you have basically
a a large amount of storage available at
very low latencies to the GPU, what it
can do, the inferencing solution can do
is it can store KV cache and as long as
you get KV cache hits, the cost of
inferencing dramatically drops. If you
need to uh recomputee, it's a very
expensive proposition. If you have a
cash miss, the cost is now treated as an
input token because you have to recmp
compute the pre prefill phase. Exactly.
If you can if you can keep hitting cash
every time you need KV u then that is
the ideal solution and that will
dramatically change the the landscape of
tokconomics and you know changes
everything based on how agents work
because now like you say you can keep
the context for a week like if you look
at anthropics uh pricing right now
you'll see that like holding it for an
hour is a certain pricing versus holding
it for 5 minutes is another pricing in
cash. Exactly. Exactly.
&gt;&gt; That comes from a fundamental hardware
limitation. So if you can store it in
infinitely then it drops the the
tokconomics changes completely and
that's where token warehouses come in.
&gt;&gt; Exactly. So where token warehouses come
in is the the widely reported reality of
inference economics today are negative.
The joke is people want to climb up to
positive unity economics you know in
infant serving today and that's because
it is expensive. you have to recomputee
these tokens over and over again every
five minutes or in some cases an hour
but you're always paying for the
privilege of extending that recomputee
uh and it's hard whether you're you know
AI native startup or whether you're an
enterprise in production to meet the
insatiable demand of tokens right now
with this particular cadence I kind of
like to call it like assembly lines you
know before Henry Ford and Model T we
were basically having all the workers
come to a car do their job and then
leave and go to another car or
something, but the workers moved around.
It was very expensive to move them
around. And the assembly line brought
the work to them, right? Don't move the
workers around. Pump out 10 times, 100
times more cars than before just by
reorganizing your factory. So that's
what we're seeing now basically with
these token warehouses now that enable
the ability to now not evict KV cache to
you know minimize that prefill and at
scale now you're basically at data
center scale able to have all sorts of
systems now again over one network the
north south network over the context
memory network and especially over the
uh the GPU you know GPU direct if you
will network all those Three network
types can participate in not recomputing
those tokens and figuring out based on
their service levels where they want to
read those premputed tokens from. And
because the to premputed tokens are
always available in the warehouse at
Lakehouse, uh you're you're now able to
choose whether you want to, you know,
burn trees, so to speak, and light up an
entire rack's worth of energy to
recomputee tokens or whether you just
want to read them from this token
warehouse. And this decision is going to
become more and more important because
everything changes, right? So the
evolution of hopper to blackwell,
blackwell to rubin means that the
premputing is faster and more efficient.
So it's not always a static equation of
yes, it's always cheaper to read from
the token warehouse from the stored KB
cache. But the hack ultimately with all
the gobbledegook we're talking about
here if you don't follow the technology
is it's very transparent pricing. So the
way to really understand tokconomics and
the way to understand whether you can be
a positive gross margin AI based
business is to go to sites like open
router which are wonderful because open
router.ai will let you look at your you
know category and then your models and
for any particular model. So let's pick
a deepseeker. Let's pick openai's GPOSS
model. You can actually see all the
inference providers that serve that
model across the world. Hopefully more
than one for some of your models so you
have competitive choice. And it's very
transparent. You have a price per
million input tokens there that you were
referring to, a price per million output
tokens, and the ones that are just being
filled in now are price per million
cached read tokens and a price per
million cache write tokens, which isn't
often populated now because these are
advanced features that aren't yet
offered by most inference providers. But
you can see it right there. The real
hack is if you can see a cash read token
that's close to a full price to full
input token price and compare those that
are often 10 to1 differences today. If
you see that narrowing to, you know,
5:1, 3:1, 2:1, 1.5 to one, you know
someone has a token warehouse. You know
they're being efficient there. And you
know now that their pricing is positive
unit economics and therefore your own
app economics, your agent economics can
be positive unit economics as well
because you don't want, you know, less.
You you want more tokens. your billions
of tokens are just going to go up that
you want but your price per can't
continue to be what it is today.
&gt;&gt; Yeah. So don't the message is if there
is any way to make the GPUs work less
that will save money. So find a way
[laughter]
&gt;&gt; find a ways to find ways to make the
GPUs lazy because if you can just store
the stuff you need and retrieve it, it
is far better than churning those GPUs
around.
&gt;&gt; And and the natural, you know,
consequence of that is you don't buy
less GPUs. That's just not in the
vocabulary of anyone in this industry.
you always preciously consume whatever
allocation of GPUs you get, but you can
reorder them as in an assembly line so
much more efficiently that in this
two-phase approach of, you know, prefill
and decode, you essentially can allocate
fewer GPUs to that redundant prefill
operation and more GPUs now to the
money-making decode operation, which is,
you know, directly mapped to output
token pricing, for example. uh and
you're just generating more tokens off
the same capex and the same opex the
same energy consumption which is which
is again the ideal optimization state.
That's fascinating. That's really good
insight. Thank you for that. What do you
what are your views on the future of
storage? Like what are we going where
are we going? What's next? What can we
expect down the line? What do you see?
So there's all sorts of exotic media
coming out, DNA based storage, right,
for archival and glass and diamond vein
storage and all that. You know,
ultimately we're we're still uh kind of
bound by the reality of the modern
storage protocols. So more innovation in
NVMe, NVMe fabrics, more innovation in
the networks supporting NVMe. So better
scale up whether it's Infiniband or more
and more Ethernet now. Certainly more
innovations like ultra ethernet, you
know, um and and RDMA, Rocky, you know,
RDMMA over Ethernet over ultraethernet.
Those are going to be the heart of
innovations going forward because, you
know, Bob Metaf will just be very happy.
He's grinning right now, right? Ethernet
just keeps winning and keeps being the
most manageable way to to manage large
networks. Even that insanely fast serial
deserialization ses of those networks.
Uh optics, right? going from from copper
to more more optics to to not have these
these furnaces basically on the network
side you know with the very very hot
transceivers that's a big innovation CPO
co-ackaged optics that's a big
innovation so optics and Ethernet and uh
you know these modern storage protocols
NVMe and NVMe fabrics understanding all
the cues across all the devices and
having just native software that
understands that without some of the
burden of 30-y y old technologies that
were designed for spinning rust.
&gt;&gt; Yeah. And this is all important. All
these innovations affect everything
else. So the everything is so squeezed
now uh that like Jensen described, it's
extreme co-optimization across
networking, compute, storage that is
really going to drive the industry
forward. And it's not just like any one
thing that would change the world
forever or anything. Maybe we already
saw that with the LLM. Uh but but
there's so much required everywhere.
&gt;&gt; Absolutely. I mean, there's never been a
better time to be a true systems
engineer, right? You've got to engineer
all sorts of discrete components into a
very balanced, cohesive, reliable,
single system. All right, that's it for
this episode. Thanks so much, Val, for
spending the time to be with us. This
was an enlightening conversation. I
learned a lot about this, and I hope our
listeners did, too. Uh, please check out
wcker.io.
I know I learned a lot from their
fantastic collection of blogs on their
website that talk so much about storage
protocols and technologies from a very
understandable point of view and a lot
of pictures. So definitely do check that
out and if you enjoyed this podcast,
please consider leaving us a review or a
like on your favorite platform and
thanks for listening.
&gt;&gt; Absolute pleasure, Vic.
