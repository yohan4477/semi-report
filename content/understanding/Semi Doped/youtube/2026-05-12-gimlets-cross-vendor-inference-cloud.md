---
source: https://www.youtube.com/watch?v=-f6oyMeN4rY
vid: -f6oyMeN4rY
title: Gimlet's Cross-Vendor Inference Cloud
date: 2026-05-12
duration_sec: 2933
channel: Semi Doped
kind: transcript
---
We're connecting chips that have never
been connected together before because
no one has taken chips from vendor A and
vendor B and plugged them together and
orchestrated a single workload across
them.
&gt;&gt; Hello everyone. Today we have special
guests from Gimlet Labs. We have Natalie
and Baltier and we're going to talk all
things heterogeneous silicon and
rethinking the data center. So let's
start Natalie with you. Our audience
probably doesn't know you guys or
Gimlet. So tell us more about you.
&gt;&gt; Not yet. Yeah.
&gt;&gt; There you go.
&gt;&gt; Um my name is Natalie. I'm a co-founder
of Gimlet.
Um
Gimlet we can go more into it, but what
we are is we're an inference cloud built
for agents and one of the kind of key
aspects about our technology is that
we've built this inference cloud across
heterogeneous hardware and we can get
more into that, but we think that that
is going to be the future of inference.
&gt;&gt; Nice. Exciting. And Baltier, who are you
and how did you get to Gimlet?
&gt;&gt; Um I'm Baltier. Nice to meet
you everyone. Um I joined Gimlet roughly
five months ago. Before joining Gimlet
um I've been at Intel
um and Gimlet was one of my four
portfolio companies um that I've been
working very closely. I'm amazingly
excited about what we are building at
Gimlet. So I ditched my corporate job
and jumped onto the startup wagon and
trying to build a very exciting
business.
&gt;&gt; Awesome.
&gt;&gt; It's been an amazing five months so far.
&gt;&gt; Exciting. Um so okay. I'm I'm just going
to try taking us through some of your
slides that I clipped from blogs and
found online and whatnot um to just get
your reactions and have you talk through
for our audience uh kind of in real time
what you're trying to do, what problem
you're trying to solve, and why it's
important. Um so you know, I thought
this was compelling. You know, I I've
written a lot about um this shift from a
GPU one size fits all GPU to
um multi-vendor multi-silicon
environment. Um so I was excited when I
saw that you guys are thinking about
this, too. Um Natalie, tell me like
make the case for heterogeneous
infrastructure.
&gt;&gt; Yeah, we'll do. So, I guess just
starting with the context that we're all
probably familiar with, it feels like
every day you hear an announcement that
one of the large frontier labs has made
some kind of compute deal for capacity
with some chip vendor, whether it's like
Traxion, AMD, TPUs, Nvidia.
And I think another piece of news you
hear, it feels like almost every day, is
that there's a new accelerator company
that just launched. They have amazing
performance on inference, they're
designed for inference specifically.
And I think that what we're basically
seeing in the kind of like broad context
is that everyone's extremely capacity
constrained at this point, trying to
scale out their inference. They're
trying to improve the performance of
their inference. They need as much
compute as possible, and then they also
need specialized compute potentially to
make it even faster. So then like how
does that all fit together? And
sometimes people ask like, "Oh, is this
new chip going to go be the GPU killer?"
Or something like that. So, the way that
we see it at Gimlet is a little bit
different. Um we think that all of these
options are really great for different
purposes, and that's important because a
gigantic inference is not a uniform
workload. Different parts of it have
different compute needs and different
bottlenecks. And so when you think about
a really, really large-scale workload
that you need to be very fast and
efficient, because we're pouring
trillions of dollars of CAPEX into it,
um then you want to start thinking,
"Okay, how can I optimize
my attention of this model? How can I
optimize my speculative decoder or my
tool calls?"
Each of those components actually
benefits from a a type of hardware,
because it has different trade-offs. So,
what we see is that
the industry is moving toward a
heterogeneous
uh stack for inference in order to meet
the performance needs.
&gt;&gt; Mhm. Mhm. Yes. So, yeah, I found you
guys had this uh slide here, and this
feels like it's exactly what you're
saying, which is breaking down the
workloads that are running at scale. It
used to be there was a time when it was
kind of like let's accelerate
everything, and we're not sure what the
dominant workloads are. So, like a GPU
can run high-performance computer,
scientific compute, or AI. Um but now,
obviously, all of the inference that's
happening is is really about like
LLM inference, these few frontier labs
at scale. Um and so, now you can, it
feels like, start to take that inference
workload and ask, "What is the right
silicon for this workload?" But maybe to
the point of the table, which I'll have
you talk to here, is like, "What are the
different parts of that workload? What
are their system requirements, and how
might those actually fit onto different
hardware even?"
&gt;&gt; Yeah, yeah, for sure. Like, I think that
one thing about GPUs is they're
incredibly versatile. So, we definitely
think they're going to be an important
part of the inference stack. Um when you
look at this table, we have it broken
down by different very, very high-level
phases of inference, um kind of showing
like the resource needs for each of them
and how they vary. And you actually
can't have one chip that is optimal for
all of these. It's just literally not
possible. But each of these is a
critical stage, right? So, how do you
solve that problem? Our core belief is
that you solve that problem by
disaggregating the workload and running
each segment on the chip that's the best
suited for it.
&gt;&gt; Nice.
&gt;&gt; So, the other thing I want to point out
about this table is that even this is
very, very coarse-grained.
Um you can subdivide each of these
components into more segments, each of
which have distinct bottlenecks from
each other. So, it's one of those
problems that
um, even at this level, I think, you
know, people will benefit from
disaggregating, but we're thinking even
more so than that. Like, even within LLM
prefill, how can we disaggregate that
further?
&gt;&gt; Mhm. Mhm. Okay, and I know we're
probably jumping ahead, but but say more
here. So, you're talking about um,
how can we split the workload up
at at ever finer and finer, and then
apparently in real time, being able to
sort of distribute that across the
correct hardware?
&gt;&gt; Right. And you also don't want to
indefinitely subdivide, right? Cuz there
is cost between sending the data from
one chip to another. But it's about like
expressing the workload, finding the
optimal points to split it up, and then
scheduling and scaling it across the
available hardware.
&gt;&gt; Okay. So, do you
do that in advance of running it then?
Like, you look at the workload and and
kind of figure out where those points
are to to break it up?
&gt;&gt; Yeah. Yeah, that's a great question, and
I think some of the other slides will go
into it a little bit more, but the way
to think about it is that we take the
workload, we trace it. So, like, if you
give us like PyTorch, we'll trace that.
Um, it could be something else, too. And
then we'll actually turn that into a
graph representation, and then our
orchestrator and scheduler basically
figures out how to segment it into its
component parts for uh, further
compilation. So, we basically trace it,
we walk that graph, and we understand
what's there. We break it up and
optimize how we do those splits. And
then for each of those segments, we'll
lower it to the target hardware. And so,
one thing that I also like to point out
here is we really work closely with our
hardware partners because we're trying
to use the frameworks that they have
available at the low level, not trying
to create a stack that is a programming
language for every single chip. So, once
we have those segments, we'll actually
compile them and lower them down to,
like for example, TensorRT on Nvidia or
other similar frameworks on other
hardware.
&gt;&gt; Sure, got you. Fascinating. So, I feel
like what I'm hearing from you is that
this is obviously more than just a
hardware play, but it obviously you're
doing a lot
in the software stack to really
orchestrate, is what I'm hearing.
&gt;&gt; Yeah, that's right. I mean, we think of
ourselves primarily as focusing on the
software layer. Uh we have to tap into
hardware as well because we're
connecting these different platforms
together. Like, we're connecting chips
that have never been connected together
before. Because no one has taken chips
from vendor A and vendor B and plugged
them together and orchestrated a single
workload across them. So, we end up
having to also play in that layer a bit
too, but what we're really, really
emphasizing, you know, at Gimbals is the
software layer for orchestrating across
this hardware. And we think that, like
to the slide that you just pulled up,
that this is a problem that is going to
compound, not ease over time, because
everyone is still coping from the
massive scale up of like simple LLM in
France, right? But what everyone's
moving to, and you know, we see this
with coding agents, is multi-step agents
that they're doing searches, they're
running things on your machine, they're
maybe calling out to other agents, and
these are even more heterogeneous than
the LLM chat models, which were much
more heterogeneous than people really
even account for on their own. Once we
start moving to background async agents
that are all communicating with each
other, they're multimodal, there's
different model types, I think that the
whole problem of the inefficiency of a
homogeneous stack is just going to get
completely untenable.
&gt;&gt; Mhm. Yes, yes, that makes a lot of
sense.
We're in a world where that we're
moving, especially we're moving to where
it's it's not just the human interacting
with the LLM, but you've got agents, the
agents are doing different things to
your point, calling different models. Um
so there's lots of opportunity to
optimize. So again, maybe thinking like
this sort of agent end-to-end workflow,
like
what does that look like from an
orchestration perspective? You have an
illustration here, but in my head it
just feels like very complicated when
I'm thinking about agents,
tool calling, and all that stuff. Like
talk to me more about this orchestration
layer.
&gt;&gt; Yeah, yeah. We touched on it a bit
before, but I think that we think about
optimizing and orchestrating across an
entire agent, not just an individual
model, right? I think that that's what
you're saying.
&gt;&gt; Yeah.
&gt;&gt; I think that like these things we
represent them as like graphs in our
system, right? And at the end of the
day, we don't really care
what type of model it is, what things
it's doing, as long as we can represent
it in our compiler's framework, and then
figure out what its bottlenecks are, and
then schedule it on hardware. So like
whether it's one model, two models,
models with functions,
um it's all kind of the same in the way
that we've designed our system. The
important part is that we can trace that
entire thing,
and then split it up, and then like this
diagram shows route it to the
appropriate accelerator.
&gt;&gt; Mhm.
In in this diagram you showed GPU,
specialized accelerator, so maybe like
an SRAM heavy one, um
and CPU. Tell me CPUs are all the talk
lately. Tell me how you're thinking
about CPUs in uh from Yeah, yeah, like
what type of workloads are you putting
on the CPUs?
&gt;&gt; Yeah, yeah, that's a great question. I
think that it's been really uh
awesome to see the excitement about CPUs
recently because they are a really
important workhorse of workhorse of
these agentic workloads because a pure
LLM or a pure model, like it only has so
much capability unless you can actually
connect it to the outside world and
ability to do general purpose tasks. So,
I think the most obvious application of
CPUs is things like tool calls, but you
can also use them for things like
smaller models or data processing and
other types of things that benefit from
the CPUs trade-offs. But yeah, I would
say that like tool calls for me are the
most exciting thing and when you
actually run that tool call in the same
place that you're running the LLM, it
really improves end-to-end latency of
the overall agent.
&gt;&gt; Hm. What What do you mean by in the same
place as the LLM?
&gt;&gt; Yeah, yeah. So, like for example, when
I'm using a coding agent today, um the
LLM is running on someone's server and
then it's coming back to me saying to my
machine, "Please look up the contents of
this file." Or "Please do a web search."
And then that is executed from my
laptop. This introduces like a very
network-bound
aspect of the workload because it has to
constantly jump back and forth between
my laptop and where the model is
running. And so, what I'm saying is that
for cases where you can actually run
those tools on the server side, you end
up with much much better performance.
&gt;&gt; Yes, yes. Okay. So,
would you say then
especially in in your architecture, the
CPU rack should be like in the same data
hall, on the same network, or is it just
like as long as it's off of your laptop
and running in the cloud, maybe there's
like lower latency?
&gt;&gt; It depends on the needs of the workload,
but what we would generally say is that
the way we approach it at Imbue is we
want to connect all of this hardware
together through high-speed fabric.
&gt;&gt; Nice.
&gt;&gt; And so, that's why we're not just saying
this data center's for hardware A and
this data center's for hardware B, but
we're actually physically connecting
these racks together. So, yeah, in
general, like I think that it's better
the closer it is.
&gt;&gt; Sure, totally.
&gt;&gt; The reason why we want that proximity is
actually latency because there is a big
demand for really fast tokens
um and higher user interactivity. This
today usually comes at the expense of
throughput hit. And in a world where
everybody is power constrained, capacity
constrained, people have to make really
hard choices. Whether am I going to have
a throughput hit but for high uh
low latency tokens or am I just going to
optimize for throughput? By putting
these different types of hardware in the
same data center, interconnecting them,
we're trying to give customers a
solution that actually expands that
barrier where they can make these uh
choices without
um less of an up trade-off on either
end.
&gt;&gt; Yes, yes. Okay, interesting. So, at the
end of the day, if we want the as fast
tokens as possible, we should put the
You're saying we should disaggregate the
workload and put it on the right silicon
for that shape of the workload. And then
also that we need a
network. And I think this slide talks
about it. We need need a high-speed
fabric. And ideally, you would have all
of the hardware that you're scheduling
across sitting on the same fabric to
reduce latency.
&gt;&gt; Yeah, that's right. And I mean, I think
that for some types of disaggregation,
this matters more than others.
Um so, for something like prefill decode
disaggregation, you might be okay with a
hop because that's only happening one
single time between the ingestion of the
context and the outputting of the first
token. Then hop to emitting every
subsequent token. But for more
fine-grained disaggregation, it becomes
more important.
&gt;&gt; Sure. That makes sense.
Um okay, so the at a high level, we've
talked through some of what you're
trying to do, which uh again, reflecting
back for listeners, you're saying, "Hey,
what if we built a an inference cloud
for agents where actually inside the
data center, there's
lots of different kinds of hardware. And
we'll write a software stack that's like
an orchestration stack that looks at the
workload, figures out where's the right
place to break it into like little sub
tasks if you will, and then we will give
it to the correct hardware, whether
that's CPUs or SRAM accelerators or HBM
accelerators, and we'll have it all on a
high-speed fabric so they can all
communicate really well. So, I guess
that leads to the question then of
who's this for? Who are the customers?
And why why is
your cloud going to be compelling for
them? So, built here, I'll I'll hand it
off. Like educate us on the customers.
&gt;&gt; Um I put our customers maybe in a couple
of big buckets. The first bucket is
frontier labs in my mind who are making
all these contracts with many different
silicon vendors.
Um but again, everybody is power
constrained,
uh capacity constrained today. And as we
talked about, they're all trying to
solve solve the problem of how can I
provide the fastest tokens, which is
better user
experience,
without compromising my throughput or
getting as much throughput as I can from
my existing investment.
This is a never-ending problem as the
baseline keeps moving and the capacity
constraint constraints become more and
more of a bottleneck for everyone.
That's one bucket. The second bucket of
customers we get a lot of interest is
from sovereign cloud vendors who are
interested in supply chain diversity,
who are putting together multiple of
these contracts in place but lack the
capability to be able to serve them at
scale.
Um bringing up a new hardware vendor
is a lot of work.
Porting one same workload from Nvidia to
AMD to Matrix, it's a lot of work. What
we're talking about is not saying that
we will take your workload and we will
port it. What we're saying is you
shouldn't be worrying about these
different hardwares and porting your
workload to each and every one of them
separately. You should just make an API
call or you should have an intelligent
software stack if you're deploying our
software stack in your data centers that
actually takes your workload and figures
this mixing and matching algorithm
itself. Rather than your or your
engineers trying to write kernels for
each and every one of these hardwares.
This is also a big creates a big
bottleneck for them to get these new
emerging architectures because who's
going to write those kernels for those?
&gt;&gt; Sure.
&gt;&gt; It's pretty hard. The third set of
customers are what I call the up and
coming AI natives who are buying tokens
at scale. 11 Labs, Notions, Glean,
Harvey's of the world. Uh companies who
are building the next generation
diffusion models. Very latency
sensitive. They're amazingly constrained
what the current infrastructure is
offering them which is we have a good
enough
product but it doesn't give the latency
or the fast tokens that you need to be
able to innovate the next frontier tier
of user experience.
The first two buckets for us is a
combination of both us deploying our
software in their existing data centers.
The second third tier of customers is
mostly around um customers who buy
tokens at bulk from our new cloud
infrastructure.
&gt;&gt; Okay, this is super interesting. So I
want to unpack this and go into each of
them. So let's start with sovereigns. So
sovereigns what I heard you saying is
like hey, you're sovereign, you're
standing up your own data centers,
you're going to buy from different
vendors over time so that you can have
that supply chain diversity and then
you've gotten yourself into a situation
where you already have different
hardware but now you're stuck with like
oh man, that has increased the um amount
of software engineering we have to do
because now we have to decide maybe
manually or something which workload
goes where and we have to write
optimized kernels to run on the
different hardware and so that it's like
a software burden on maybe a customer
who doesn't have a huge huge software
team. So you guys can come in and say,
"Hey, we'll take a look at your hardware
and we will help you orchestrate across
that hardware." Is that kind of
ultimately?
&gt;&gt; That's it. Ultimately what we're trying
to go for.
&gt;&gt; Okay. Okay. Okay, so that makes a lot of
sense. Um so you're kind of like you're
the soft you're like the cracked
software engineering team that they
need.
&gt;&gt; Correct. Software a software platform
that they need, right? Today most of
these
infrastructure is being
set up as a bare metal as a service
infrastructure.
&gt;&gt; Mhm.
&gt;&gt; Which has its own challenges, right? As
we discussed from a software engineering
perspective. What we're offering them is
not a set of software engineers. We're
doing this work for our own Neocloud
offering anyway. We have we are building
this orchestration stack in deep
partnership with those hardware vendors
for our own business. What we're
offering them is a ready-made platform
that we can deploy in their existing
data centers for them to very quickly
get to market with the existing
investments that they're making, but not
only time to market, but also get better
throughput, better capacity, and better
user experience from that as well.
Because all the sovereign clouds also
they just don't want to build this for
the sake of building it, right? They
also want to be at the frontier of the
innovation as well. If you look at
Europe, there's a lot of government
funding that's going in this area for
them to be part of the innovation
ecosystem, same in Middle East, same in
India, same in Asia. Right? How can you
give them an offering that actually
helps them get there faster,
differentiate them is another part of
the equation. And the other one is they
are very keen on supply chain diversity.
Having an Nvidia and AMD doesn't solve
the problem, right? There is a lot of
hardware innovation that's happening
outside of US as well. They are also has
the same issues. If you look at Korea,
there is really interesting chip
companies that are coming out of Korean
ecosystem that we are talking together
right now. And they are also thinking
through how can these type of emerging
hardware architectures can also be
consumed
without the software burden.
Because being able to do this kernel
engineering, the software model porting,
is a lot of work.
&gt;&gt; Sure. Yeah, fascinating. I didn't think
about the point that like we tend to
focus on American chip companies, but
there's actually other chip companies
elsewhere. And so not only for
sovereigns can you solve the like
hey, you don't have to worry about
software, our platform solves that for
you. And then I did like your point,
which by the way, we will make sure that
it's highly optimized. So it's not just
that you got it to run, but we're going
to optimize it for you. But then on top
of it, yes, you can as a platform, you
can take on the burden of getting
comfortable and making sure that you
work with all sorts of vendors from
different countries because that makes
sense for you as a platform. And then
that's something that you can offer to
all of your customers.
&gt;&gt; Yeah, I mean, if you want the best
performance, you really have to partner
closely with the chip company. And that
applies to pretty much everyone. Like if
you're running a production scale
workload, you need to get a very close
relationship with the hardware maker
that you're running it on. Doing so for
N hardware platforms,
and also keep in mind, it's hard enough
to get it performing on one. Moving it
to another is another step up. Taking it
and breaking it up and running it on
even more,
that's something that we think is
optimal from an efficiency standpoint,
and it's why we're building Gimlet, but
it would be very difficult for everyone
in the space to replicate that.
&gt;&gt; Yeah, yeah, totally. Not to mention
merchant silicon vendors only have so
much bandwidth. It's like I'm sure they
can only help so many people that come
to them. So, I I can see how it could be
win-win for them if they can just work
with you and then you can make it work
with everyone.
&gt;&gt; I think it also like Sorry, one more
point is like the chip companies like,
you know, GPUs are amazingly versatile,
right? You have other hardware that's
really, really great at many parts of
inference. By putting it alongside other
types of hardware, it can really shine
in the task that it's best suited for.
&gt;&gt; Mhm. Mhm.
&gt;&gt; And it also de-risks from a customer
experience perspective. You were all
very comfortable with running on Nvidia,
running on AMD ecosystem, but you will
have a hard time porting your model on
another vendor's
cloud only option, right? Many of hard
silicon vendors tried to stand up their
own clouds because customers were
hesitant to use their cloud
infrastructure. But what they're also
seeing is even if they set up that cloud
infrastructure,
at scale customers, for them it's also a
lot of engineering effort to move their
workloads to one vendor's cloud only.
So, those clouds are not scaling. What
we're offering is a mix-match
environment for the customers who are
looking to benefit from this emerging
architectures before the emerging
silicon vendors a way to go to market at
scale without taking on the burden of
building their own cloud infrastructure
because that's not their core business,
either.
&gt;&gt; Yes. Yes, totally. Okay, so now let's go
to the hyperscalers or those serving the
frontier labs. Hyperscalers, we know
that they have multi-vendor silicon, you
know, Meta's always talking about a lot
lately. You know, they run Nvidia, they
run AMD, they have their own NTIA chips.
Um
Now, unlike the sovereigns, like a
hyperscaler has plenty of software
engineers, even though that this is a
laborious task, to go, you know,
optimize their kernels for all the
different hardware. Um so, tell me, why
is it better that they would partner
with you rather than just kind of try to
maybe they already built this sort of
orchestration themselves or or where is
what they're doing like suboptimal
compared to what you're doing?
&gt;&gt; Got you. I think um
it's not a solution or it's not a an
answer for a hyperscaler frontier lab.
They're at different stages in this
journey because 3 years ago we weren't
talking about this level of
disaggregation of inference workloads.
We didn't know what inference was going
to look like. PD disaggregation was like
very early PhD thesis type of
implementation. Today it's becoming more
commonplace and we're talking about way
more
complicated disaggregation methods.
Right, they're at different phases and
in different stages in their journey of
figuring out how they're going to serve
inference at scale.
Um some of them are trying to build this
in-house with competing priorities. Some
of them, the ones that we are working
very closely with, saying telling us
that this is not their current
strength or current focused. They're in
a place to meet the next generation
training wars.
In next generation differentiating their
product rather than trying to bring up
and different infrastructure, writing
kernels, getting them up and running,
they would like to outsource all of this
so that they can experiment because they
know their workloads. So that they can
experiment which of these combinations
will give them the best alternative. The
other part of this is as they're
investing more and more capex for their
data centers, their margins are getting
thinner and thinner. So what we're also
seeing is like they're trying to
outsource some of these investments to
companies like us saying okay, you take
the data center burden, you take the
capex burden, you bring it up and
running for me.
See how this will work for me in this
particular hardware combination because
they already have those type of deals
with the hardware vendors. So we see a
couple of different reasons depending on
where they are in their journey right
now.
&gt;&gt; Sure, sure. That
that really resonates with me especially
when you talk about like what are their
core competencies and what is their
ultimate business model and how can they
spend a lot of time, you know,
&gt;&gt; Exactly.
&gt;&gt; training a better model or or whatever.
It actually reminds me when I was in
grad school and when I was in undergrad
and I did research both times I
benefited from people who came before me
like a PhD student that would spend like
four years building a system and then
they would only have like two years left
to quick run some experiments on it and
then I would walk in and I just run
experiments the whole time and I'm like
man, I'm glad I didn't have to spend
four years building this. And it's kind
of the same thing like you're trying to
say like let us build that
infrastructure so that you can
experiment on top of it. Let us handle,
you know, optimizing and and really
focusing in this and you guys just worry
about your experiments.
&gt;&gt; Exactly.
&gt;&gt; Do you really want to go to all of those
chip companies
optimizing it for all like,
you know, it's a lot of work.
&gt;&gt; Totally and you're signing up to do that
forever. Like you just built a team that
is committed to doing that forever. I do
like the idea of just outsourcing it so
you know, you don't let let a company
exist solely to solve that problem.
&gt;&gt; Exactly. Think about every new hardware
coming up but not only that the
maintenance of an infrastructure like
this is also a big ongoing commitment
for them. Like every new work camera
release you have to update.
All of these create a lot of issue and I
think everybody is in a race to
differentiate themselves rather than
trying to figure out some of these
plumbing to do this plumbing in-house,
right?
&gt;&gt; Yes, yes, totally. That makes sense.
Okay, now lastly, let's talk about the
AI native. So, an AI native today
they don't own their own infrastructure.
They're just trying to buy tokens as a
service from directly from APIs or
Amazon Bedrock or Google Vertex or
something. And if I heard you right,
what you were saying was
today they can only get tokens like you
can pay a lot for a fast token or pay
less for a slow token, but maybe they
don't have enough fine-grained control
to get like the
or is it ultimately just like you buy
buying a token from you, it will be
faster and lower cost? Like what's that
pitch?
&gt;&gt; I it's a combination of both
um right now. I think uh there are two
different types of customers. One of
them are big enough so that the token
cost is hurting their profit margins as
they're growing. So, they're more
cost-sensitive and they're looking for
options to reduce that cost for them as
they grow.
The second one are emerging innovators
that are building diffusion models,
video-based solutions, voice-based
solutions where latency is a big big
bottleneck for them to bring a
competitive product to the market. They
have options in like I was mentioned on
um emerging neo clouds, own cloud
solutions, but it comes at a very
different trade-off for them to be able
to do that. They have to spend their
limited resources importing their models
to those cloud solutions as well. So,
it's a combination of two different
customers that are approaching for to us
right now.
&gt;&gt; Got you.
&gt;&gt; I think there's another thing here which
is that Actually, there's two points I
want to make. The first is that you get
tokens from someone. At the end of the
day,
you know, the limiting resource might be
like power capacity, right? If we can
deliver a shift in the Pareto frontier
for the available power by leveraging
heterogeneous hardware, we can translate
that for our customers to lower latency,
to higher throughput, to like it can be
a variety of benefits because you've
actually shifted what's possible by
doing this. And what the folks in this
bucket tell us is that
taking latency as an example,
it's not just that it's better to get
tokens faster. It's actually that
different product experiences have
different latency budgets. The user
can't wait for a response more than 1
second. By making it three times faster,
five times faster, what those folks tell
us is it actually lets them enable new
experiences that wouldn't have been
possible when using the providers that
run homogeneous stacks.
&gt;&gt; Got you. Interesting. So like, oh, I
only have a second to respond here, so I
can only do a couple things, but if I
could do a bunch of things in that
second, then yeah, I can unlock a new
user experience that is differentiating.
&gt;&gt; And this is especially important for
things like voice agents.
&gt;&gt; Sure, totally. Totally. Okay, so you
mentioned Pareto frontier, so let's give
one example before we end so people can
understand what we're talking about. Um,
tell us about D Matrix, your partnership
with them, and then I've got the Pareto
frontier slide after this.
&gt;&gt; Okay, Balter, I'll kick it to you and
then I'll talk through the slide after
this one.
&gt;&gt; Sounds good. So, um, one of the things
that we've been talking about is mixing
and matching different architectures,
but especially with GPUs and SRAM-based
architectures.
Um, not only we'll go into the technical
details, but this is how you can
actually pair a throughput machine like
an Nvidia B200 or GB200 with an
SRAM-based architecture, which are
amazing decode machines and can push the
latency frontier way more at multiples
of what an Nvidia or a GPU-based
architecture can do. So, we had this
hypothesis on mixing and matching
together actually can shift the Pareto
curve faster.
We partnered with D Matrix. D Matrix is
only one of our partners that we can
name publicly right now.
We are partnering with multiple of these
SRAM-based architectures. D Matrix team
has been amazing from time to market
from a speed and a partnership
perspective in optimizing
a software stack and a hardware for
this.
What we've done with them is basically
putting together in our own data center
a D Matrix Corsair card in the same rack
with Nvidia B200s directly connected to
each other to be able to test how much
we can push the frontier curve. And I'll
let Natalie to talk about what it means
and what we've done.
&gt;&gt; So,
let me first orient the chart. I think
your listeners are probably familiar
with the classic chart that Jensen often
shows, but just in case let's kind of
recap it. So, on the Y axis what we have
is throughput per kilowatt in terms of
tokens per second per kilowatt. So, this
is basically saying if I have a 50
megawatt data center, how many tokens
per second can I push through that data
center?
And then on the on the X axis what we
have is interactivity. So, if I'm a user
getting tokens being processed in that
data center, how quickly can I get those
tokens as my personal experience? Now,
you would think those two things at
first order would be very related, but
they're actually at odds. And that's
because the longer it like the longer
you give me to serve a token, the more
efficient I can be with how I generate
that token. But if you say, "No, I need
this token really fast right away for
Natalie's use case," then you have to
pull out all the stops to get that token
to that user as soon as possible. So, we
show these things as a frontier where
you can optimize for one or the other or
somewhere in the middle, but you're
never going to get something that's
fully fully in the upper right quadrant
because they're fundamentally at odds.
So let's now look at what we did with
the D matrix side of things. So
we show like three different Pareto
frontiers for three different
configurations for the same workload.
And this workload is running GPT OSS
120B
8K input sequence length, 1K output
sequence length. And what we're showing
is the frontiers for that workload. So
we have three configurations here.
The green one is a traditional prefill
decode disagg on GPUs.
So we can see that
that offers like, you know, certain
tokens per second at given interactivity
level. Usually what way people think
about it is, okay, my requirement is
that my users need at least X tokens per
second. And then from there I try to
push the throughput as high as possible.
So you would set a latency budget and
then try to maximize throughput given
that latency budget.
A common technique that people adopt to
speed up their workloads is they
introduce speculative decoders.
And what speculative decoders do is they
say
wow, like running decode is really slow
and inefficient cuz I have to run the
full model for every single token.
But sometimes I could maybe use a
smaller model or something like Eagle
which works a little bit differently to
guess at the next token. And maybe if I
could guess multiple tokens in a row
then what I could do is take my large
model and verify if they're correct.
Because it's a lot more efficient to
verify five tokens in a row and say, are
these correct? Then it is to actually
generate them one by one with that large
model.
So what we have in the blue line is a
GPU only speculative decode flow. And so
what we can see is compared to the pure
pre-filled decode disagg, it offers a
shift in the Pareto frontier that's
quite significant. And that's why folks
are adopting speculative decoders
because it really, really helps
you know, deliver better experiences,
have more capacity, etc.
But, what we did is we decided to take
this a step further and say,
"Okay, what if we take that same
speculative decode setup, but instead of
running all of those parts on a
GPU, we're going to take the spec decode
part and run D-Matrix Corsair." And
that's because D-Matrix Corsair offers a
lot of on-chip SRAM, and it's really,
really fast when you can store the model
weights in memory.
And so, by running that smaller 1.6B
spec decode model on the Corsair, even
um on top of the blue line, which is
already quite optimized, we see a
dramatic, dramatic performance benefit.
So, if you look, you can say like at a
reasonable point on the interactivity
side or on the throughput side, you can
get like a 4x benefit.
&gt;&gt; Mhm. Nice. Awesome. Interesting. So,
yeah, zooming back out for listeners,
you know, we talked about
taking parts of the workload and
scheduling it to the right hardware. And
so, D-Matrix's chip is one of those
SRAM-heavy ones. And so, if there's part
of this workload which is like, can you
do this really quick guessing and and
see if you get it right in advance, um
so that you have to do less work, what
if that ran on just that part of the
workload ran on an SRAM-heavy chip that
could do this guessing really fast? And
that allows Now, I I stole the chart
where it's like pushing it, um you know,
horizontally. So, for the same
throughput throughput per kilowatt, it
would get unlock a much higher
interactivity. And I know you had other
charts that said, of course, depending
on what people are trying to do, if
they've got a latency budget, um you
know, basically, they could also stay at
a fixed interactivity if they wanted and
get a higher throughput. So, serve more
customers more efficiently.
&gt;&gt; Right, you can choose you want your
customers to get their tokens four times
faster or do you want to serve like two
or three times as many customers at the
same latency?
&gt;&gt; There you go. Yeah, well said. Nice.
That's awesome. And so, I think, you
know, I I just clipped one of the slide
which you showed that you can get even
more of an unlock if you use like a
verify stage of 20 tokens instead of
five. Um but maybe I guess on this slide
a point here is for someone like a
sovereign
um it shows that you guys are thinking a
lot about how to tune infrastructure,
how to run little experiments, how to
um
take the latest and greatest like
speculative decoding and then take the
latest and greatest chips like a a D
Matrix one and figure out like what are
all the right knobs so that your
customers can just come to you and say
make it faster.
And you say, "Oh, we got you."
&gt;&gt; You know, we all have like limited
capacity, right? We need to serve a lot
of tokens. I think inference is
supposed to become the dominant workload
over training this year. So, what we are
doing here, and this is one example of
the type of disaggregation that we can
do and the type of, you know, hardware
we can deploy across, but it's not
limited to this. This is to illustrate
what you can get when you adopt a
heterogeneous stack.
&gt;&gt; Mhm.
&gt;&gt; And then so, we need to start from
customer back because every customer has
unique requirements. They have different
workloads. They run MOE, some of them
sparse sparse.
That changes what type of disaggregation
methods you need to apply. That also
changes which hardware combination would
be the best for that particular
workload. That's also something that we
can help with the customers as we learn
more about their workloads because
giving them an unlimited and option is
also not the solution, right? They want
There needs to be a limited solution
spec also for it to be cost advantageous
like
So, what is that right optimal
combination
uh for that particular workload? So, we
start from the other way around saying,
"Okay, this is the customer. This is the
workload. This is their constraint,
either latency or power or throughput.
That this is the constraint. This is the
characteristics of the workload and
their customer base." So, based on that,
we run simulations and tell them, "Here
is what we think would be the best
architecture mix of hardware for you.
And based on your needs, this is how you
can push the frontier. Uh and what
limits you can get. And then based on
that, we start designing what is the
smallest data center stamp
that is required because it has to be a
repeatable implementation to be able to
scale."
&gt;&gt; Interesting.
&gt;&gt; You need these to be in the same data
centers. You need to network them. What
is that network topology? And then build
a way a path to scale that
implementation. So, this is an
end-to-end
partnership with the customers.
&gt;&gt; Yes. And okay, that's super interesting.
Obviously, I love that you start with
the customer needs first and build to
their needs to get the most optimal
experience for them. And also, in the
back of my mind, one of the one of the
things I've been thinking is like, "Oh,
if you guys are essentially like a neo
cloud, there's tons of neo clouds. How
do you differentiate? Who captures that
in the long run? Some are just bare
metal." And so, it's like, "Okay, how is
it How can you differentiate there?" But
what I heard you saying is, "No, no, no.
We are like a full-service, almost like
consulting partner where we're helping
you design your data center footprint
and we're helping you optimize it and we
provide the software platform that will
help do this for you." So, it's very
differentiable
compared to others in the neo cloud
space.
&gt;&gt; Correct. And also, if If think about us
versus everyone else in the neo cloud
space, most of them are today backed by
one silicon vendor.
&gt;&gt; Mhm.
&gt;&gt; Um and in return, they gave part of
equity, significant part of equity. So,
it's hard for them to diversify their
silicon ecosystem. So, it's hard for
them to do mixing and matching that we
do. And if you look at what's going on
in this ecosystem is inference prices
are coming down, so everybody is getting
more pressure on their top line.
And they can they have very limited
opportunity to diversify supply chain.
They have no negotiation. Hardware
amortization is usually 70% of their
costs, annual costs. So, they have very
little to or room to optimize their
bottom line. This is why the software
innovation you see them announcing all
these segregation methods because
they're trying to create a sustainable
business model. What we are slightly, I
will say grossly, different is we have
two different dimensions that we work
with the customers. A is the end-to-end
software and the scaling motion with
large-scale customers. But for customers
who are up-and-coming, who cannot yet
commit, we also build our own neo cloud
with fundamentally different economics
because from a bottom line perspective,
we actually have a supply chain
diversity that optimizes our bottom
line. And from a top line perspective,
since we can offer very differentiated
token performance, we can also command
for a price premium than racing trying
to race to the bottom from a pricing
perspective. So, if you ask us, "Better,
are you differentiated?" I think we are
very, very much differentiated. And
having these two different dimensions in
our business model gives us the
liquidity and the financial stability
because one can fund the capex
investment of the other.
&gt;&gt; Mhm. Mhm. Fascinating. I really like it.
And I you make the very interesting
point, which is
the incentives that other people have or
are bound by that would prevent them
from trying to go in this direction.
I.e. you can buy whatever silicon makes
sense and then of course you have the
chops, the software chops in-house to
disaggregate whatever workloads across
that hardware as you see fit. Uh
yes, and you can control your destiny.
&gt;&gt; The other thing that I like like the new
cloud I see is in like two dimensions.
Yeah.
&gt;&gt; We have core wave type of people whose
core strength is buying GPUs, data
centers and offer that as a bare metal
as a service, but they lack the full
stack experience today. They're trying
to acquire companies to
figure that out, but it's really a long
journey, very hard journey to mix and
match acquisitions to create a unified
stack. The other ones are like together
with fireworks based on who is only
software and trying to acquire the
capacity from usually one silicon
vendors,
infrastructure providers. So, we are
don't want to be neither of them. We
want to offer the end-to-end experience
with two different business models that
are very complementary to each other.
&gt;&gt; Nice. I love it. Fascinating. So,
last slide,
earlier the slide when we talked about
business models it also had the headline
that I think in March you announced you
raised the series A
and then I saw you obviously are hiring
people. If people click on view on open
roles, there's several roles. So, tell
us a a little bit more of just like
who what you're looking for and what's
up next for the rest of this year?
&gt;&gt; Yeah, I would love to talk about that.
We are very focused on hiring right now.
We're set to
I forget how many X we're going to is it
triple, quadruple? It's something crazy
like that by the end of the year because
we are scaling rapidly to meet the
demand that we're seeing. So, if you
want to join a company that is uh in,
you know, crazy scale mode, this is a
good time to join cuz you'll still be
part of the old guard cuz we're, you
know, in that rapid growth phase. So,
who are we hiring? Um I think our main,
you know, like in terms of number of
roles, engineering is like the biggest
one.
Um we are looking for people who know
how to do high-performance AI systems
across the stack, whether that's by
working on our scheduler, working on our
compiler layers, working on how do we
monitor these like incredibly complex
distributed systems, how do we write
optimized kernels, how can we leverage
AI to automate some of the optimizations
that we're doing, you know, ourselves.
Um and then also general builders, like
folks that are the kind of Swiss Army
knives that love to go up and down in
the stack and contribute to different
parts.
Um
yeah, please, yeah, definitely reach out
to us if you're interested. I will note
we are uh based in we're an in-person
office based in Stanford, Cisco.
&gt;&gt; So, um just final words from my end,
right?
Um this is a crazy fast-growing rocket
ship right now because in many startups
there's always a concern, do I have the
product market fit?
We are we proved there is a product
market fit. We are very well funded.
We're on a fast pace to get accelerated
capacity.
Um most people are struggling with
supply chain problems. Given our value
proposition, that's least of our
problems. Right now, our biggest problem
right now is getting the right people to
execute and commit uh deliver the
customer commitments we have. So, we are
hiring across the tech stack from
low-level kernel engineering to software
engineering uh higher levels of software
engineering. So, we're building an
end-to-end cloud stack, not a bare metal
as a service. So, across the tech stack,
if people are interested, roles are
open. We are looking for creative
innovative engineers who are looking to
jump on a crazy growing ship.
&gt;&gt; Nice.
Good pitch.
&gt;&gt; I've been at startups like most of my
career and I think that I've been blown
away by the scale of the opportunity
here and I pinch myself almost every day
and yeah, we really look forward to
welcoming our new colleagues.
&gt;&gt; Yeah, awesome. I love it. Yes, having
product market fit, understanding your
business model and having it figured out
and then of course just the macro
environment that we're in where there's
so much demand and so little supply and
being able to come in and figure out a
unique way to make the most out of the
constraints. You know,
pretty exciting. So I hey, I learned a
ton. Thank you so much Natalie and
Baltazar. This was really engaging and I
know the listeners will walk away having
learned something. So thank you.
&gt;&gt; Thanks so much Austin. It's been a great
conversation.
