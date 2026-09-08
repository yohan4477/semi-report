---
source: https://www.youtube.com/watch?v=Yr0Bc6sGJJw
vid: Yr0Bc6sGJJw
title: Grok Bots and How CPUs are used in Agentic AI
date: 2026-08-24
duration_sec: 2694
channel: Semi Doped
kind: transcript
---
So check this out. So this uh week was
actually the release of Grockbot which
is an agentic AI platform. So you think
about it like an open claw but like
extremely easy to use so that like
everybody can run agents all the time
right now even if your computer is
closed. So this is a very important
development I think uh because it's not
so much for what the grothbot is as a
product but what it means from an
underlying substrate of compute and
specifically what it means for CPUs.
&gt;&gt; All right, hello listeners. Welcome to
another semi-doped episode. Um I'm
Austin from Chipstrat and this is Vic
from Vick's Newsletters. And if you're
watching this on YouTube or something,
you'll notice Vic is in a different
location. Um, so Vic, tell us where are
you? And then I also saw that you are
trying this Grockbot, which I saw on X,
but I have not tried I honestly don't
even know anything about it. So, uh, I
want to hear where are you and then tell
me about Grockbot because I know you've
been playing with it.
&gt;&gt; Awesome. I am in the Bay Area. I came
here for like uh hot chips next week
which is very exciting. A lot of people
are coming down for this conference, but
I decided to show up a week early
because I was actually in Taipei
attending uh the Open Compute Project
APAC, like the Asia-Pacific region
version of this conference. And I was
like, um, yeah, I think it makes just
sense to like come here a little bit
early cuz I've got so many people to
meet in the Bay Area. It's been amazing.
I've met so many amazing people and so
many amazing things have happened that
we should eventually it'll all come out
at some point and we'll discuss it on
the podcast or whatever when the context
is right. But yeah, it's been an amazing
week and so I am in the Bay Area. Uh I
got my little camera rig with me but I
don't have my semi- doped sign which I'm
very bummed about. So I'm going to
travel with my neon sign next time.
Uh yeah so like Grothbot Grothbot is an
interesting thing uh because this is an
agentic AI software like I don't know
they call it an agentic harness is the
term for it. It's a piece of software
you just download off the website and
you install it and uh you got an
interface where it's pretty much
everything works out of the box, right?
Uh, so what you do is the first thing
that comes up and you go, um, oh, hey,
here's the, you know, what do you wanted
to do? And I said, hey, I want you to be
a chief agent and then you're the chief
of my agents and we'll, you going to
talk to all the other agents. And then
it's like, oh, what other agents do you
want? I'm like, oh, I want an agent that
does this. I want an assistant agent. I
want a I don't know, a news monitoring
agent, something like that. And it just
spins it all up automatically, right?
It's fancy. Uh it's it's really nice. So
I think this will open up the doors to a
lot of people starting to use agents now
because the whole openclaw approach and
the Hermes approach was like a little
bit difficult like you got to install it
and you got to go into the command line
and you've got to set up an API key and
you've got to like set up all of this
stuff. It is a little bit involved for
everybody to use but Grockbot takes care
of everything.
&gt;&gt; Nice. Amazing. Okay. So like OpenClaw
and Hermes Hermes, however it's
pronounced, those ran locally on like
your own machine, right? And and this
Grockbot, this must how much of it runs
locally on the machine versus like in
the cloud. You said you downloaded
something.
&gt;&gt; Yeah, [snorts]
this is just a piece of software that
essentially communicates with a computer
in the cloud. This is the nice part of
it, right? uh which is what I really
like about this is it is actually
running your own little dedicated
computer in some server somewhere. So
you have like a little virtual machine
that's running somewhere and everything
is within that box. All your tools are
installed there. All your signins are
installed there. Like you don't need all
these MCP connections and uh these
plugins and those plugins. It's just
think about it as your computer but
somewhere in the cloud. It's a VM. It's
a virtual machine, right? The nice thing
about this is that all of the security
practices and everything that matters
for these agents to run in its sandbox
environment is all contained within
there. So if your agent has like signed
in uh into one tool, it is available
easily across all your agents and
everything because it's it's a local
computer. you have that's the difference
compared to like OpenClaw and Hermes.
&gt;&gt; Nice. Amazing. That does sound so
convenient. So in this would you say
it's better than just like having a
bunch of cloud code agents running
locally on your machine that you have to
manage. [snorts]
&gt;&gt; So it's it's a give and take, right? Um
there's a lot of control when you have
your own cloud code agents. You can
specify
uh a whole lot of stuff uh to the finest
detail like which model you should use
for doing what and you can token
optimize and be like saying hey for
these queries you can do you know so you
can set up open router as a model
provider through the cloud code
interface and you can in open router you
can say okay use the auto router or use
this hierarchy of models such that these
requests are routed here and those
requests are routed there. This does
this takes all that out of the equation.
Like you just you don't know what's
happening. You just have tokens and you
use those tokens. [laughter]
&gt;&gt; Nice.
&gt;&gt; That's it. You don't know what's being
used.
&gt;&gt; You know, I think the easy button is how
it's going to go. Agents will go to the
masses where they don't need to go buy a
Mac Mini. They don't have to install
something. They don't have to know what
Open Router is or which maybe is getting
acquired by Stripe now. Um yeah,
&gt;&gt; but uh they don't have to configure and
token max or you know get token
efficient token min um you know they can
they can just hit the easy button. So
then does that mean I should buy a bunch
of CPU stocks
&gt;&gt; if Grock is going to spin up all these
VMs?
&gt;&gt; We'll get we'll get to the not financial
advice part really quickly. [laughter]
But um you mentioned Mac Mini. So I just
wanted to like touch upon that. Like
there was this when agents were rolled
out not so long ago. It was like only
December last year that we even heard of
this thing. Um it was such a rush to get
compute that even Intel was caught
unawares of the demand for CPUs. Right?
In their earnings call in February, they
said, "Oh, we have a lot of CPU demand.
We have we had no idea it was coming."
So the question is why did all that
happen? If people observed keenly enough
at the time, you could kind of tell why
what's happening because the moment
agents showed up, everybody ran and
bought a Mac Mini. So what exactly were
they buying? Were they buying a Mac Mini
for its memory? Were they buying it for
its NPU based, you know, the graphics
processing they have in there? Uh or
were they buying it for just compute or
a CPU? Right? So that question if you
revisit and ask yourself why people
bought the Mac Mini that is that will
tell you something and the reason is
people didn't want to run open claw on
their existing laptops
um because you're giving it access to
your whole computer and that's dangerous
because you don't know what it's
accessing. You don't know what it's
going to do with the information on your
computer. Does it access sensitive
information, medical records? You have
no control. So the idea is what if I
could buy a separate machine a Mac mini
keep it only for this purpose install
openclaw on it and then have that as my
agent computer and then there I don't
put all the sensitive information I give
it only what it wants and then it works
all the time. Now the problem with that
setup and this is familiar to anybody
who's run a home server setup like I'
I've run one for like 10 years. uh but
keeping that up and running is a real
big pain because you are responsible for
power right like if there is an outage
or if your computer's I don't know like
some part the PSU blows up or you know
something happens power goes down or
[snorts] if your internet is out uh
that's a problem because you don't have
connectivity into your own machine at
home but you have to set up networking
like how are you going to access your PC
at home when you're traveling like I am
right now. How are you? So, you've got
to set up some kind of a VPN network.
Like we, you know, you and I set up tail
scale for all this stuff all the time.
It's not that simple for everybody to go
off and be like, "Hey, if I tell my mom,
hey, mom, all you need to buy is this
Mac Mini and then set up tail scale and,
you know, set up a UPS so power doesn't
go down and have some failover internet
so nothing happens." She'll be like,
"I'm I'm out. I can't use this stuff."
Okay, you keep your agentic PC. I'll
just go back to my regular laptop.
[laughter]
&gt;&gt; Yeah, 100%. Yes, it is all about the
easy button for for 99% of people.
Seriously.
&gt;&gt; Yeah. Yeah. So, that was the problem.
So, people were buying these computers
just to sandbox their environment and
have its own you know uh area for a
agents and stuff to run. At that time
itself I thought about it and thought
like wait what is the right way to do
this? Like do you have to buy a PC and
go do this? No. At the time too, what
you could do was you could get on a VPS,
you could rent out a little virtual
machine on a server and you could
install OpenClaw on that one and then
you you just go off and run it on the
cloud, which is a much better solution
because you don't actually have to buy a
I don't know $600 $800 machine, which
got so much more um attention because
like everybody's buying it. So it was
like a craze and prices went up and all
that. assuming you don't want to run
models locally because some people
actually bought the Mac Mini, the high
version with the maxed memory version.
Great decision in hindsight. I think you
could pull out the memory and sell it
for a profit compared to the cost of the
machine itself now. But consider it an
investment. But yeah, if you wanted to
run models locally, you could do it,
right? But I don't think models could
all be run locally. They're really big.
say you want to run a frontier model
like the fable class model with your
agents, there's no way you could do
that, you know.
&gt;&gt; Right. Right. Yes. I have an agent
computer by the way and I do run a few
models locally but it's obviously
smaller things for the nonfrontier tasks
including um like audio uh basically
like transcription you know voiceto text
like so I'll run this podcast through on
that when I post it to our semi-dope
newsletter to give the transcript to
people that's like the simple kind of
thing that can run on local box but for
most people when they want to spin up
agents and they want to do things. I I
think that there's a lot of work that
you would want an Opus or a Fable
quality, you know, frontier model.
&gt;&gt; Yeah, it depends on the workload. You
know, you might want better quality
model. So, what is the right way to do
this right now? That's what Grockpot
does. All all of this. It does all of
this for you because you don't actually
have to when you get Grockpot, this is
not a sales pitch and they're not really
a sponsor or anything, but what problem
it solves is all I'm trying to
articulate. I'm not suggesting anybody
go and I'm not shilling this product,
okay? [laughter] So, don't get it.
Actually, it's $200 a month. You most
people probably won't get it, okay? It's
very expensive. So, not saying you
should. Uh, but what this what Grockbot
solves is you just get the virtual
machine with all the integration tied
in. It asks you when you install like,
hey, what integration do you want? I
said, I I want my Google calendar. Um, I
want my Google Drive. you know, some
some of these things you can just say
add add and [snorts] all those things
are natively installed and ready to go
for you. You don't have to do anything
like there's Canva, there's Figma,
there's so many tools out there. You
don't have to set up each one. So, you
set it up there into your Grockpot
instance and it's available across all
your agents and [snorts] then it runs on
a virtual machine and you don't have to
be responsible for anything including
the security of that virtual machine
because that's Grock's problem. They I
hope they have experts taking care of
that. I don't have to become like a
cyber security expert now, [laughter]
&gt;&gt; right? I mean, I don't know. I thought
Elon fired all the people at X or
slimmed it way down, but anyway, carry
on. I'm sure [laughter] I'm sure they've
got their zero.
&gt;&gt; Maybe they don't. Okay, fine. Then
deploy Fable to be your security expert.
&gt;&gt; There you go.
&gt;&gt; Got to be a creative problem solver.
[laughter] Come on. Uh yeah, whatever.
Like all this is No, you don't have to
worry about anything. You get a virtual
machine that sandbox securityities uh
supposedly insured. Then you've got all
your tools installed. You run your
agents and it's amazing. So now we go to
the question of CPUs. So do we need
them?
&gt;&gt; Right? Like let's now go into the
question of do we why do we really need
CPUs? Because
&gt;&gt; we never even mentioned GPUs in all of
this stuff. Yeah, sure. For doing the
inference, we want to do GPUs, but we
really never haven't even touched upon
what CPUs have really done for us in the
last 6 months since agents showed up and
I thought that's what we should like dig
into now.
&gt;&gt; Let's dig into it because from your
example, okay, so we talked about
running cloud code on like your laptop.
So there's going to be work done on the
CPU there as well as calls to a GPU in
the cloud. Um, we talked about running
OpenClaw on a Mac Mini. So now you've
got another CPU on your desk. It's not
your laptop. It's your Mac Mini. It's in
its own little contained environment.
It's got a CPU and yet it's still
running to the going to the cloud for
the GPU. Um, and then of course now
you're talking about um using Grockbot,
which is actually spinning up a VM in
the cloud. So a CPU in the cloud. And so
it's a CPU in the cloud talking to a GPU
in the cloud and then communicating
results back down to you. So there's so
there there's actually and we'll get
into this, but what I'm alluding to is
there's different work happening. In
some scenarios it's happening on your
local CPU, some it's on your home server
CPU and others it's on a rented cloud
CPU. And so there's obviously
interesting implications, but um yeah,
let's get into it. Let's first talk
about like what what do the CPUs even do
versus what is the GPU doing?
&gt;&gt; Yeah. Yeah. Yeah. Before the show, we
were talking about a nice analogy we
could come up for this. Um why? Yeah.
I'll let you explain that analogy
because I this is a very nice framework
for which people can think about where
GPUs lie, where CPUs lie and uh how we
should think about this going forward.
&gt;&gt; Yes. Okay. So ultimately like I I think
of a good way of like where the value
happens is the GPU. The GPU is like the
the genius you know um now it's like the
ph the the genius that has a PhD in
everything which of course you don't
always need. Um but the the GPU is like
the genius and then but at the end of
the day once like the brain the genius
like thinks of all the work that needs
to be done which I mean this is what I'm
doing with fable is I'm I'm trying to
say like you know give me your very
thoughtful approach or opus 2 and then
once it is decided like what work needs
to be done ultimately most of this work
or it depends on the workload but a lot
of the work can actually be given to
like assistants like little doers little
task carry outers. Um, so ultimately,
you know, I think about the GPU is like
the the genius that is doing all the
thinking and delegating work and then
ultimately the CPU as the assistants
that once told what to do, they can go
carry out all the work that the genius
told them to do. [snorts]
&gt;&gt; Yeah. So, ideally, you don't want a
genius doing all the work like the
genius is thinking about it. uh genius
has paid a lot of money per hour to come
up with this brilliant ideas [snorts]
and you don't want the g genius going
off and uh I don't know putting uh
paperwork in the drawers or you don't
want the genius looking up some
information from a file uh that's in the
drawers or you don't even want the
genius going out to fetch the mail. Like
ideally in an ideal world you want to
have the absolute genius aka the GPU
just doing what it does best. Actually
there's one we can break this analogy
down into a little bit more detail. So
if all the workers are like CPUs like
you know CPU cores doing their thing for
example um I think we can break down
what kind of worker that is too because
there is something called the head node
CPU and the analogy to the head node CPU
is an assistant to the genius. The
assistant to the genius which is the GPU
the job of this assistant is to keep
handling the genius work. You don't, you
know, if the GPU, if the genius needs
coffee, you give the genius coffee. If
the genius needs water, you give, the
genius doesn't stop working because it's
a lost uh, you know, you know, you're
losing money if the genius stops
working. So, you want to make sure that
once the genius is done with this task,
the next folder of materials is ready
for the genius work to be done. And the
host node CPU will be like, "Here you
go, sir. This is what you got to do
next." genius is like let's go let's do
this. So that's the host node [snorts]
and it has to have a I'd say it has to
have a pretty fast per core performance
because it's constantly monitoring what
the GPU is doing. Are you done? Are you
done? No. Okay. Like let's get this
ready. Let's keep it ready. As soon as
the GPU is done, this has to hand it in
like you know no delays, no wasting
time. Do not waste the genius time. So
that's the host node CPU.
&gt;&gt; Yes. Yeah. I love it. I love it. It's it
shows that you want like a high clock
speed uh or a very responsive CPU but
also obviously you want like the
communication between the CPU and the
GPU between the assistant and the genius
to be as fast as possible right so that
um you know that there's no like so for
example you ideally you wouldn't have
the assistant like uh be in a different
building and then they have to come over
and check in and then walk back to their
building and then come back and check in
right you want them like in the same
room talking with each other and and so
maybe to take it like a layer deeper,
there's differences between a coherent
host and a standard host with these host
nodes. So like a coherent host would be
like Grace Blackwell where you've got
like the GPU and CPU and they can talk
over a shared really fast network. So
like NVLink [clears throat] C2C um
versus like a standard host where you
know maybe you have um just some hoppers
and you take an x86 processor and you
put it on the board but it's still
talking over PCIe. So that that would be
a little bit more of an equivalent to
like uh you know they're in separate
buildings or separate rooms. M so the
uh the the the chip to chip the C2C
protocol that the GPU and the CPU uses
the coherent protocol the you know the
coherent CPU would be somebody who's
standing right next to
&gt;&gt; the genius and looking over I'm like oh
here you go here you go you know
&gt;&gt; right there right
&gt;&gt; and if they Yeah exactly and if they
have like memory coherency and then they
it's like I can see the I'm the
assistant And I can see the genius's
notes and I could like jot down on his
notes too or something.
&gt;&gt; Yeah. So I was thinking about HBM is in
this analogy and this is where we push
it too far and we shouldn't but we'll do
it anyway. But I think of HBM as the
stack of papers next to the genius's
desk, right? The genius is not going to
get up off the chair and go and get it
from the cupboard or anything. HBM will
be the stack of papers on the desk and
the genius can just take it and keep
working on it and putting it back on or
whatever. The co the coh memory
coherency comes from the assistant
having access to the same pile of papers
on the desk because they're in the same
room. So if the assistant wants can also
access the the memory directly.
&gt;&gt; Exactly. Exactly. When you zoom out to
your point, this CPU assistant, this
host node, it has one job and it's keep
the GPU fed. And that's that's
ultimately what the host CPU needs to
do. Keep the GPU fed. So then it starts
to raise the interesting question that
made a lot of sense in the chat GPT area
where everything's just a chatbot and
it's just like, yo, I'm asking questions
and it's just like just keep the genius
fed so he can respond to questions. Now
all of a sudden when there's all this
extra work to be done, like the genius
is spewing out code and you need to
compile the code, see if it compiles.
Maybe you need to run the code. Maybe
the genius is like, I need information
from 50 different uh sources, go, you
know, hit SEC filings and go Google the
web or search the web, you know, and go
do all this stuff. Now all of a sudden,
the question is, can that CPU assistant
go fetch all these filings? Can it take
all this data? Does it have the memory
uh capacity and bandwidth to analyze all
this data and keep the GPU fed or is
this too much work for that assistant
standing right next to him and do we
need an army of other CPUs to help?
&gt;&gt; Yeah. Yeah. So, this brings us to the
concept of what is it? I don't know. Is
there a thing called an agentic CPU? I
don't know. That's like a marketing term
probably, but I think it's it makes
sense in this context. [laughter]
&gt;&gt; Yeah. So, you know, I'll give you my
take on the Agentic CPU and and actually
I just recorded a podcast recently with
AMD and and
&gt;&gt; they were aligned and and thinking very
similarly, which is, you know, if you
zoom way out, sort of breaking this
analogy, just going back to how things
used to work back in the cloud era,
obviously we had all these general
purpose CPUs and they they did they back
all of the SAS products that we use in
the cloud, right? And so now as we're
standing up all these uh GPUs so that we
can ask them our little chat questions,
you know, of course they're not
necessarily going to go communicate with
a CPU that's already running um an API
server or running my database for my
company or something like that already
has a job and that CPU is kind of
already shaped to fit the workloads of
like I run big databases quickly or I
run tons of small little API servers
quickly or whatever. Um, so then the
question is, okay, now fast forward, if
we've got all these general purpose GPUs
that already have jobs, they're already
running SAS products or web servers or
what databases or whatever, and then we
now we've got these new geniuses that
are standing up and there's they have a
little assistant CPU next to them trying
to keep them fed. But if now there's
work that it's going to spill out
because it's too much for the host node
CPU, then the question is what CPU
should those fall on and where should
they live? And so there is this term of
art that has come up lately, agentic
CPU, which is more about, hey, this
these are CPUs that are dedicated to
doing this agentic work, all this
spillover work that the host CPU could
do, but it's too busy keeping the
assistant fed or it's keeping the genius
fed. So there should be racks of CPUs
that are dedicated to this task. But of
course it then raises the question, well
what should those CPUs look like? Should
they look like the host? Should they
look like the assistant or should they
look more like the general purpose or do
they need to have their own shape? Um,
so that's kind of like the framing for
this new kind of middle ground agentic
CPU.
&gt;&gt; Aentic CPU. Yeah. So you don't want to
use the host CPU like you said to do any
of this work that the genius is asking
like hey go search the internet. No, you
because the once the host node goes off
and does something like this, it stops
feeding the GPU and the Genius and then
the whole thing goes down. Like what's
the point? Now the G gen Genius is idle,
which is the worst case scenario. So you
need a different kind of CPU that does
this stuff. Uh it doesn't even have to
be a different kind of CPU. It's in
function. It's a different CPU, right?
You could use the same CPU like the host
node CPU with it may not need the C the
coherency that we spoke about because
it's not talking to the genius all the
time.
&gt;&gt; Yes.
&gt;&gt; But otherwise it could be the same CPU.
But ideally what you can think of this
is like let's take a CPU with like I
don't know uh let's say 128 cores or
something. [snorts]
So what you can do is you can think of
all the cores and as like a floor plan
of an office building and then you can
kind of draw little boxes and say okay
these four cores are the finance
department these four cores are my
research group these four cores are like
my uh you know uh facilities team
whatever it is right and so what you do
is then somehow you've got yourself a
little company and the genius is saying
hey I need this stuff to be done
and uh the host CPU is going to, you
know, yell across the room and said,
"Hey, finance team, I need you to go and
like scrape up the SEC filings from last
night, you know, go do that." And the
those guys will be like, "Okay, cool.
We'll do that." And the team of four
cores will go off and be like, "Okay,
I'm going to do this stuff." And they'll
report back to the uh host node CPU, the
assistant, who will then feed it to the
genius, the GPU. Right? So in this
scenario, uh a multi-core
CPU that is either like one of the AMD's
256 core or Intel's more recent 288 core
CPU. These are great because uh you can
assign lot of little departments across
doing different functions. Um or you
could have
basically uh bigger teams of people. So
if you have more cores, you can put like
eight people in the finance team versus
like four people in the finance team. So
they kind of get the job done faster,
right? But also you want each person to
be competent. So each core each core
should be fast. It should not be like an
ultra slow. You don't want a team of
eight interns versus a team of eight
experienced people matters. So single
core performance matters because if you
get like very slow single course, it's
like you're putting eight interns on the
job which is fine depends on the task.
nothing at least in terms but it really
is okay but it depends on what the task
is.
&gt;&gt; Totally totally and this this analogy is
good because for example your host CPU
the one that's feeding the genius it
obviously it may have something like 88
cores um but it may be super fast and
those cores may be dedicated to keeping
the genius fed. Now all of a sudden if
you take that same CPU and you move it
into this agentic
uh situation, you might stop and ask
yourself like, oh, do I want um on my
little floor plan in in my with all my
cubic do I want 88 cubicles of like
really fast thinkers or sometimes would
it actually be better to have 128 or 256
or 288 or 512, right? And you know, it
reminds me, right, of working at lots of
other companies where you look around
and of course you've got some management
tier uh and senior architects and stuff,
but then you also have a lot of like um
level like uh fresh out of college
&gt;&gt; hires that are maybe cheaper and maybe
they work a little bit slower, but guess
what? Some of their tasks may be like go
fetch this from the web and it's going
to take two or three seconds to respond
and you're just going to sit there
anyway, so maybe it doesn't matter. uh
you know and then you go go process and
you process a little bit slower but to
your point there's definitely certain
like um IObound networkbound tasks uh
and then just tasks that don't have to
finish instantly because they're not
blocking the genius and and therefore
zooming out then you you start to think
oh maybe for these agentic CPUs there's
probably a lot of companies that are
mostly interested in getting as much
work done out of a CPU as possible so
having as many cores and as many threads
as possible. And you know, of course,
zooming out even further, if you have a
fixed amount of power in your data
center, you might start to say like, can
I get the most amount of cores or
threads per watt, for example, or per
dollar, depending on your situation.
&gt;&gt; Yeah, it's about the cost per employee
now, right? You know, how many cores can
you get and how expensive is each
employee in that uh floor plan? You
know, that's important. So you want to
have the most capable employee and many
of them at the lowest possible cost of
acquiring them.
&gt;&gt; Yes.
&gt;&gt; And that has to be suited to your
workload. You don't want to put like
really really um inexperienced people on
a very complex task or very experienced
people on a boring task you know. So
when people many times ask what's the
best agentic CPU or what's the best host
node? I think host node CPU you can kind
of tell what it is and we've both
written about this in quite some detail
on our substacks.
host node CPU you can actually tell you
need coherency you need speed you know
cores are not all that important but
like the single core performance in you
know getting stuff to the GPU is very
important so I think you can identify a
host node CPU when you see one however
like you mentioned the whole floor plan
of employees that the CPU cores are and
you're going to fill racks of them in a
data center there is no reason you can't
fill
several racks with different kinds of
chips like you've got some high core but
low core speed chips in one rack when
you've got really fast chips but not as
many cores in another rack. And the
whole problem now comes down to how do
you architect your workflow to the
workload that you are going to be using
it for. I think that's very important.
So there's no such thing as the right
CPU. I think they're all right CPUs.
um it's all about the cost you know that
you get per core kind of the total cost
of ownership of the chip and how you use
it together. So that co core design and
co-op optimization is very important and
I spoke to an you know an Intel speaker
also at Taiwan and that was a very good
talk and he explained that they actually
if you go to Intel they actually do
explain to you what the right CPU
configuration should be for a given
workload. So they have recommendations
that they provide for these kinds of
things. So it's very important.
&gt;&gt; Yes. Yes. And um this is why Intel had
recently launched this past summer like
a P rack and an E-Rack for a Gentic AI
trying to make the point that it's not
necessarily one-sizefits-all and there
may be particular workloads that you can
map to needing more performance even for
agentic AI tasks or needing more or just
wanting as much efficiency in as many
workers as possible. There's a lot of
analogies with like uh org design and
I'm thinking back to companies where
it's like oh budgets were bad and or you
know the year was bad, budget was tight
so they had to lay people off and so
then the question is like do you lay off
the junior workers where they're all
really cheap so you'd have to lay off a
lot of them or do you lay off like
middle management where they're
expensive and and you know a lot of
times it's like lay off the middle
managers and this kind of reminds me of
like saying you know I don't need the
host node over here actually I just want
a bunch of maybe like junior employees
or early career employees that are
essentially cheaper but can still get
the work done.
&gt;&gt; And then you've got the general purpose
employee general general purpose CPU.
I've even lost the analogy now. Sorry,
I'm in office mode now. I've even
forgotten we speaking about CPUs. Uh but
yeah, the general purpose CPU will be
like I don't know, it's just like good
for everything. Like sometimes you've
got these people who just have the skill
to do quite quite a lot of different
things. Those are also can be valuable.
So it's the agentic CPU is one thing.
The host node CPU is another. And then
you've got general purpose CPUs. These
are just people you need. Okay.
&gt;&gt; Right. Right. Which
&gt;&gt; the receptionists or the the people who
maintain the building, you know, all all
important tasks, but you can't do
without them.
&gt;&gt; Totally. I I will say at hyperscaler
scale they tend to still have particular
workloads in mind and therefore they
will buy a skew a general purpose cloud
skew but still with a particular shape
like we know this is memory optimized
because we're going to have like
in-memory databases
you know running here and so what will
be interesting whereas if you're just an
enterprise you might buy more sort of
generically shaped like yeah it's kind
of fast enough and it has enough memory
and it you know enough compute that we
think it can do a broad set of tasks. So
it'll be interesting to see also how
agentic tasks and agentic CPUs if
there's if there's any difference at the
enterprise level you know kind of can I
buy a one-sizefits-all uh a gentic CPU
rack versus um obviously hypers scale.
Uh but now that I won't even go there
because then you start to ask like are
enterprises really going to be buying
additional racks of CPUs or are they
going to be still leaning on the cloud
here? you know how's this going to play
out? [snorts]
&gt;&gt; Yeah. Uh so rack scale ideas is is quite
interesting too. Um I was at this is a
different kind of a I realize this is a
slight tangent but I just wanted to
mention it because yesterday uh
considering where we are recording or
when we're recording this yesterday was
the Cerebras uh announcement of the uh
their new rack scale solution. And so we
always thought of Cerus as a as a wafer
scale uh you know a chip right a wafer
scale chip but they are saying no like
you know the next next unit of compute
could be putting them into a rack. So
you think of this as a rack scale
solution. So even CPUs could be could be
filling into racks and that's nothing
new. It's been part of the data center
uh cloud data center for for for decades
now like that's how CPUs used to be
filled into racks and they used to do
the compute right. So now you've got a
rack of GPUs, you've got a rack of CBRS
GPUs, uh you've got a rack of you know
PC core like Intel calls it or a rack of
ecore. All of these have different
capabilities like fast latency like this
this genius is specialty the cerebrous
genius specialty it's just speed
&gt;&gt; it is only speed right this this thing
this genius can't remember this kind of
forgetful genius but is very good and
very fast at doing stuff then you've got
the other kinds like the the large HBM
based accelerators those geniuses uh
have a little bit more context they're
not like ultra fast they're very smart
But, you know, they they kind of have
larger context, a little bit more
general purpose genius, you know, not
just genius. [laughter]
&gt;&gt; And then perhaps you could have the slow
genius, the slow thinker. I'm just
pushing this analogy because [snorts]
what if um you know, you really don't
need that token speed in in the genius.
You don't need this fastness of the
genius. You just want the genius to
think for a long time and come back with
whenever the genius has an answer. you
know this this is definitely a workload
uh for like science and you know medical
problems or solving can cancer or
something. It's not like you want the
answer tomorrow. We would all like it
but it would be much better if we you
this genius could think for a very long
time and come back with a nice answer
that we could all work with you know
without blowing the budget because you
can't say like I will put cerebras on
solving cancer tomorrow like that
cerebrous kind of high token speed maybe
it will uh maybe that's what it takes
because it's a hard problem but maybe
sometimes you're like you know I just
want to study weather patterns and the
inferencing can go really slow I don't
But total anyway. Yeah.
&gt;&gt; Yeah. Yeah. And well, there's like
overnight jobs that could be like, "Hey,
go look at all my transactions from
today and summarize them and write write
them in some log or something." You
might want some intelligence where you
can't write deterministic software. I
mean, that use case, you probably could
write deterministic software, but you
might want to extract some insights
first from all of those transactions and
write that to the log as well. You would
need some intelligence. Frankly, that
could be an LLM that runs on a CPU, too.
if you've got like a cluster of pores
which uh then it makes me ask the
question about orchestration which is
like do we have the right orchestration
software um to schedule across uh super
fast geniuses and regular geniuses and
even like CPUs um or is there actually
opportunity there for someone to make it
simpler?
&gt;&gt; We've obviously got like Nvidia Dynamo
and stuff like that but like even a
layer higher.
&gt;&gt; Yeah. Yeah. You know the Nvidia Dynamo
thing is all about how to make the
genius work better, right?
&gt;&gt; Yeah.
&gt;&gt; But that's not the orchestration layer.
&gt;&gt; Yes.
&gt;&gt; So it's Yes. So we do need a
solution. I think modular is one such um
orchestration layer if if I get this
right. But maybe more so for the genius
still. I don't think it's going to do it
over everything or I'm not entirely sure
but
&gt;&gt; well yeah that's I mean we should talk
to the modular people they you can you
can write with Mojo and it can run on
CPUs or GPUs all with one programming
language which is pretty sweet but I
don't know a ton of details yet about
their orchestration level capabilities
&gt;&gt; but the one thing I understand is that
they can talk to disagregated hardware
of different kinds you can mix and match
various pieces of hardware for
inference. We're still talking about the
genius, but even that, you know, you
could have orchestration like do a
little bit of tokens here, you know,
deal with a different architecture here
like can you mix AMD rack and uh Nvidia
rack all together in a data center and
have a software platform that does all
this inferencing. But then yeah,
ultimately then you've got to have a
software layer above all of that. maybe
does exist and we are not entirely
software guys. uh but yeah that platform
will orchestrate how the CPUs and the
GPUs interact with each other and how
the data moves between all of them you
know uh it's a very very complicated
problem to
&gt;&gt; totally totally and I know Gimlet Labs
who I talked to on this uh podcast I
don't know back in May I believe um they
were kind of working in this same space
which is as a neocloud could you
ultimately have lower costs by having
different hardware and being very good
at scheduling it across the correct so
that the correct slice of work gets done
on the correct hardware. Um
&gt;&gt; but you know all these are topics for
another time. I think um this is
probably a good place to call it quits.
So we talked about CPUs, we talked about
agentic AI, where should it run? Oh,
let's circle all the way back to
Grockbot. So where do you think your
Grockbot VM lives?
&gt;&gt; Is it?
&gt;&gt; Yeah, it lives. Go ahead.
&gt;&gt; Yeah, it lives in some a general purpose
CPU somewhere. Uh I think because this
general purpose CPU is just running an
OS somewhere and it has a um little
computer that's made only for me and I
go in there and it's the only job of it
is to do what an operating system does,
right? It makes uh it's like hey go
access the memory and here you go like
you know I'll get the data from the
internet and all of this stuff. This is
not entirely like agentic per se that
but it's just a computer like it's a
computer like the one you're on watching
this on your phone or like your laptop
or whatever. It's just a computer
[gasps]
and uh yeah so that computer
accesses a whole lot of other hardware
that mini virtual computer you have has
access to the genius that has access to
all these host node CPUs which the
assistant that's feeding the GPU
you know that entire office building of
stuff uh is accessible to the my little
virtual machine and I can spawn as many
agents as possible. possible from my
little you know VM and send them off to
do various tasks you know so it's a
little it's it's a nice it's a nice
approach I I think and it's going to
cause more demand for CPUs
&gt;&gt; now because you you're opening up not
only the layer that was previously
inaccessible to people because not
everybody could actually install
openclaw
&gt;&gt; now if more people can use tools like
grockbot I'm not again trying to say
this is one particular product I think
more will come out like is [snorts] it
opens up uh the AI world to a lot more
people the agentic AI world which means
that
if more and more people start even
regular people not like the high-tech AI
using token maxing crowd if the regular
old people like who never really wanted
to use AI but now find use in it start
using this remember how many VMs are
going to be you know aortioned for each
of the pe each of these people who use
this tool or tools like these. Then
you've got
those little VMs spawning off so many
calls to CPUs and GPUs. Imagine, you
know, each one can run 10, 50, 100
agents.
&gt;&gt; Uh there's a lot of hardware demand.
What can I say? There's a lot of
hardware demand.
&gt;&gt; Absolutely.
Think 10 million people doing this is
not crazy. And that could be 10 million
VMs running on 10 million cores in the
cloud. And then if people are kicking
up, you know, uh, let's just say
whatever, a hundred, uh, you know,
agents per VM, all of a sudden you're at
a billion cores that are needed. It's
not that crazy to imagine that world.
Um, and you know, that's coming quickly.
And so and maybe I guess to contrast
that with the Mac Mini craze, you know,
yes, Mac Mini was sending a lot of new
to like not new requests for tokens from
GPUs, but al and so that was also
selling lots of host node CPUs, but
ultimately a lot of that agentic work or
whatever is running on the Mac Mini and
but this the easy button, the fast path
is you push that button and it spins up
a VM in the cloud. And I to your point I
do think that's where really we're going
to see a lot of proliferation of agentic
AI to the the normal crowd to normies
and therefore you know obviously going
to be good for server CPUs.
&gt;&gt; Agree.
&gt;&gt; Totally. All right let's wrap there.
We'll check back in the future. Um you
know anyone who has any interesting
thoughts or corrections or interesting
orchestration stuff that we should be
aware of uh send us an email, put it in
the comments, whatever. Um Elon and
Grock team if you're listening we'd love
you to come on and explain how it works
for us you know and and I think one
maybe last little point is
&gt;&gt; [clears throat]
&gt;&gt; um the question is how much of this
stuff is actually running on agentic
CPUs versus you know VMs on general
purpose machines and because these are
newly marketed things you know uh I
would love to hear from anthropic or
open AI how much of if they would be
willing to share how much work are they
actually putting on aentic CPUs versus
just still regular general purpose CPUs
and what are the pros and cons? But so
much that we would love to learn. So
anyone who's in the space that's
listening, let us know. We'd love to
talk to you. With that, we're going to
wrap here. Thanks everyone.
