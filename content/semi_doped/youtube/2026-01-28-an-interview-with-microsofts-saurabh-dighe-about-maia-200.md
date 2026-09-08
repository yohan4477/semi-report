---
source: https://www.youtube.com/watch?v=6R-oMCdnLiI
vid: 6R-oMCdnLiI
title: An Interview with Microsoft's Saurabh Dighe About Maia 200
date: 2026-01-28
duration_sec: 3161
channel: Semi Doped
kind: transcript
---
The question inside Microsoft was never
can we build a GPU. The question really
is like what do we need to build the
best AI infrastructure for this era of
AI.
Hello listeners. We have a special guest
today to discuss Microsoft's Maya 200
their AI inference chip that was
announced earlier this week. Welcome
Sarro Day CVP Azure systems and
architecture. Thanks for coming on to
chat with me. Oh, it is a real pleasure,
Austin. Thank you for inviting me. I'm
happy to disclose Maya and happy to take
any questions you may have.
&gt;&gt; Awesome. Great. Okay, so I want to talk
a lot about the why behind Maya um from
business decisions to why make custom
silicon and and then of course the why
behind the technical trade-offs because
I think those are interesting and
communicate something about what you're
prioritizing and what you're not. Um,
but first, how about a quick refresher
for anyone who missed the Maya 200
announcement? What what's it all about
and who's it for?
&gt;&gt; Yeah. No, great. So, I'll just start off
like we have been on this
multi-generational silicon journey at
Microsoft, right? Uh, we know that our
customers want leading AI infrastructure
and one of the things that we have to do
when we develop leading AI
infrastructure is have the freedom to
innovate across every layer of the
stack. So silicon is is a very important
part of this aspect and so uh just
yesterday we announced Maya 200 which is
our second generation of AI accelerator
and we'll be happy to go into a lot more
detail with you as as the podcast
progresses but this is really targeted
towards you know performance leadership
for inference. So performance per dollar
and performance per watt leadership for
inference. We have we made very
deliberate architectural choices and we
said hey we really need to make sure
that as this wave of AI adoption and as
more and more customers and you know the
world starts using AI inference
economics is going to be a big important
reason to invest in silicon and systems.
So that's what my 200 was all about. It
was really to drive uh the best AI
infrastructure for us and meet the
customer at the highest performance
layer but at the also at the lowest cost
point.
&gt;&gt; Okay. Yes. Let's dive in there. So you
talked about designing for your
customers and and you're thinking about
uh TCO and performance. So
when most industry observers talk about
custom silicon, they frame it as a
margin play traditionally. Oh, you know,
build your own chip, cut out the middle
men's markup. But you're talking
differently about Maya as and and I saw
the blog too. There was you had a nice
post and EVP Scott Guthrie had a nice
post too and it talked a lot that you
both talked a lot about working backward
from what your customers need with
respect to those um metrics you
mentioned. And so yes, let's let's take
it from that angle like what are
customers asking for that today's GPU
fleet might not deliver for them.
&gt;&gt; Yeah, I know that's a great question.
See, um the question inside Microsoft
was never can we build a GPU, right? The
question really is like what do we need
to build the best AI infrastructure for
this era of AI? And and if you take it
from that lens, right, it starts
becoming obvious that you know AI
inference is actually a frontier
efficient. It's a curve and you have to
be able to deliver real world capability
and accuracy at different points in the
curve latency, cost and energy points.
And so when we looked at it as a as a
portfolio, we knew that it was not about
one sizefits-all. It's a really about
making sure that we have uh
infrastructure that's heterogeneous
because we are embracing this multimodel
you know multi-use case scenarios where
we have you know certain use cases that
could be super latency sensitive right
if you're coding or if you're running
co-pilots are highly interactive
environment you're going to look for you
know extremely low latency applications
on the other hand if you're you know
batch batching inference you're doing
some summarization and you know it's
okay to take some time but more
important it is about throughput and
cost at what you deliver that's a
different use case that's a different
model that you're going to be using and
there's probably a spectrum in the
middle so we look at this as you know
inferencing is not a onepoint solution
inference is there's an frontier
efficient curve and we need to make sure
that our infrastructure is not about one
sizefits-all it's about delivering the
customer the choice and the flexibility
that they need to be able to deliver the
inference workloads. Now that's just one
aspect to it right and now you say hey
but I need to run this at planet scale
&gt;&gt; right so then you go in and say hey the
core principle about building Maya or in
fact any custom silicon for us whether
it's cobalt Maya or Azure boost uh
integrated HSM we have a portfolio of
custom silicon now in Azure the the core
principle here is that when you do full
stack innovation across software across
data center infrastructure about rack
scale and network infrastructure, you're
you're actually able to unlock a lot
more efficiency and customer
experiences, right? For example,
availability is a big customer
experience in the cloud, right? So, not
only in every region, but also the
uptime that you can deliver, the ability
to deploy it globally, the ability to
find the right telemetry from your
systems and integrate that back into the
control plane. So these are all things
that helps you kind of really innovate
across the entire stack and that's why I
think that you know it kind of comes
down to hey do we meet the customer
where they want to be met do we have
that freedom to innovate do we have to
deliver the economics and the cost point
and then also control our own supply
because this is going to be a big
portion of our fleet so the ability to
manage capacity and supply becomes an
important consideration as well. So
that's how we kind of try to do this
holistically across the entire you know
value proposition of building custom
silicon and custom systems for Azure.
&gt;&gt; Sure. Yeah. And custom systems that's a
good framing and especially when you're
talking about innovating up and down the
stack not just with the AI inference
chip but CPU networking and so on. Um
you you know you talk about enabling
this e efficient frontier for workloads
some that might need ultra low latency
or some that maybe don't need that and
just high throughput at large batch
size. So talk to me like who are those
customers and what are those workloads
that you guys were designing for?
&gt;&gt; Yeah. Yeah. That's a great question. I
I'm going to refer back to like uh what
what Satya said like Javon's paradox
like if you if you build the right
infrastructure and continue to drive the
cost down you you see more and more
adoption it you know you actually are
able to see more consumption and I'm
hoping that the way we build our
infrastructure it actually eases
customers into driving more and more use
cases. So like you ask me what are the
customers or what are the uh key points
and areas of our optimization. I think
what where we look at it is obviously
when we designed Maya 100 uh we we were
in the era of CNN's right you know
conventional neural networks but we
obviously moved to uh large language
models and LLMs and so we designed Maya
to be really inference optimized for
these you know large reasoning models
chain of thought uh some of the use
cases that we are looking at is if
you're let's say you're training a
frontier model and we're working very
closely with our Microsoft super
intelligence team like you still need a
lot of inference in training loops,
right? So, how do you provide that
inference at the right capability but
also at the right cost point is is a
great use case for us. When you run
something like co-pilots, right? You
have different use cases in co-pilots.
You have use cases where you have to
really sometimes go down to, you know,
time to first token could be less than a
second or it could be up to 10 seconds
because you're just doing a
summarization of a meeting that just
happened. And so that gives you a little
more flexibility. So we've designed the
architecture taking into consideration
how do we design for large language
models, how do we design for Microsoft
use cases that we know are kind of
growing with our own Microsoft super
intelligence team with our co-pilot uh
offerings as well as with Microsoft
foundry offerings. So those are some of
the optimization points as you see in
the architecture and and one deliberate
choice that we made was we didn't pursue
training as a first step. We knew that
if we had to go pursue and make a system
that was both training and inference, we
would be adding a lot more cost into the
system, we'd be adding a lot more uh
inefficiencies from our point of view
into the system because we are trying to
do something that is much much more than
what a customized more optimized system
could be able to do.
&gt;&gt; Sure. Yeah, that that makes sense. I
actually like that you guys just focus
on inference because as we'll get to in
the technical tradeoffs, you know, we
can really see the decisions that you
made are definitely tuned for inference
specifically. Um, okay, backing up a
tiny bit, you mentioned Maya 100 was
sort of designed preGPT more for like
CNN era and the two my Maya 200 was
designed with large models in mind and
even with reasoning in mind. when when
were you guys starting to put pencil to
paper on the Maya 200?
&gt;&gt; Yeah, know that's a great question
because silicon takes a long time. Yeah,
but uh but uh we we have like think
about it this way like we have a we have
a research team that looks ahead and you
know looks at what is the evolution of
the models. We look very closely with
you know our models team. We have data
science team looking at new data formats
and then we have an architecture team
that has to now could put it on pencil
and paper. So, so you're right. I mean
around the year 22 23 we kind of started
really focusing and making a much more
concrete proposal of what a Maya 200
would look like and at that time uh we
had good information on how the
architectural is shifting right so if
you for example you brought up Maya 100
it was definitely designed with CNN's in
mind which is basically a it is
dominated by convolution layers it is
the data is much more local it is much
that there's much more dense operations
going on. There's not a whole lot of uh
focus on how much HBM bandwidth. In
fact, my 100 I only had 64 GB of HBM
capacity. And then when you looked at it
from an LLM standpoint, we said, "Oh,
look, wait, I do need to change the
shape of my compute, right? I do need
large matrix multiplications. I do need
more horsepower in SIMD operations. I do
need a much bigger HBM bandwidth." So we
moved to HBM 3e. We moved to TSMCN3
technology to give us to for us to
change the computation flop. Uh we
actually uh added 216 GB of HBM because
we wanted to have all the capacity to
serve these models. So just changing the
balance of the machine making sure that
we had the right computation right uh
you know even communication I didn't
talk about but even when we're looking
at our scale up networks like we know
that tensor parallelism we have would
have a lot of like you know all toall
traffic how do we optimize all toall
traffic this is all aspects of the micro
architecture architecture that are being
tuned for something like an LLM machine
rather than uh a Maya 100 so That's why
we believe this is like almost a grounds
up design
&gt;&gt; uh from an micro architecture
perspective to be able to deliver to
these kind of next generation use cases.
&gt;&gt; Yeah. Yeah. No, that makes a lot of
sense.
as you're designing the 200 for this
sort of new world that we're in this
sort of postGPT world. Um you mentioned
that you've got research teams, you've
got frontier teams inhouse that that can
help sort like look ahead and
essentially shape your requirements and
it clearly worked because I mean if
you're putting pencil to paper 22 23
like we didn't have reasoning models yet
then um and and make and there was a a
bit of a bet that in at that time the
the public conversation was all about
training and you you guys are making a
big bet already at that time on
inference. Do do you feel like uh a big
company making a custom AI chip um like
you guys actually has an advantage say
compared to a startup just given that
you have so many like internal users who
know the shape of their workloads or are
looking further ahead.
&gt;&gt; Yeah. No, I I do think that you know uh
when we're designing silicon inside an
hyperscaler you you really have I would
use the words again the freedom to
innovate
&gt;&gt; because you control a lot much portion
of the entire stack right just going
back to uh in November we introduced uh
a state-of-the-art data center called
fairwaters and if you look at the data
center uh it's amazing to see how much
technology came together in terms of
just building the data center
structures, bringing liquid cooling
inside it, being able to, you know,
bring in the latest GPU gear in it,
being the just the amount of technology
and the innovation across the stack. How
do you, you know, create a control plane
that manages all this? How do you put
compute and storage around it so that
you know it's not just about the GPUs?
So you just look at kind of the layers
of innovation and freedom that you get
inside a hyperscaler versus if you were
just a silicon startup, it's going to be
extremely difficult. So I truly believe
that this is not a chip story, right? It
is really how do I create an
infrastructure that's best suited for
this efficient frontier and silicon
although is a very important part seems
to be taking a lot of the focus
sometimes. uh but I do want to kind of
re refocus it towards yes there's
there's obviously competitive silicon
that's super important but then how you
compose it across the stack is equally
important so that you can unlock the
efficiency across the entire system
&gt;&gt; yes
&gt;&gt; and and we we understand the workloads
as well right uh being the ability to
really understand that workload and then
codify some of the decisions across the
infrastructure of all layers of the
infrastru structure in in some ways
that's an engineer's dream come true
&gt;&gt; because you you got the operating system
guys sitting right next to you've got
the Azure control plane guys sitting
next to you've got data center
infrastructure operations you know just
uh a few buildings away and so it's it's
all it's all one team at that point.
&gt;&gt; Yeah. Fascinating. Amazing. So you are
innovating full you're fully vertically
integrated as a as a hyperscaler and
you're able to innovate from the
transistors all the way up through the
systems and the software all the way to
the data center which is pretty cool. Um
you're trying to be at the efficient
frontier and you internally I guess
maybe one of the uh the flip side one of
the challenges is you probably have all
sorts of customers who want to get their
hands on this. you mentioned Microsoft
foundry um there was mention of the
super intelligence team open AIS GP2 5.2
2 models I think might be served on it
and even using this for inference during
training and there's I know also
obviously Microsoft owns GitHub right so
there's all sorts of opportunities um
internally how who decides who gets
access to this and and how do they get
access
&gt;&gt; yeah that that's a tough question but
but you're right um we do have a lot of
internal I mean I would say internal but
obviously it is for our customers but we
do a lot of internal consumption of this
so and and we we are very deliberate in
how we deploy capacity, which regions we
deploy capacity and where's the customer
demand is and so uh there is a welloiled
process inside the company that looks at
you know basically allocation of
capacity I leave it at that and and of
course as as a new architecture and a
new system comes into play uh we we
would ramp it through the course of this
year as well we'll add more capacity
into our fleet we obviously will be
adding um you know other GPUs into our
fleet as well. Like I said, we we we
believe in a more heterogeneous fleet.
And so depending on where we want to
optimize and place the system like you
know we look at the shape of the
workload, we look at the customer
readiness and then we are able to deploy
the capacity in in that form of shape.
So uh yes it's it it is a tough problem.
Everybody wants more capacity. Everybody
wants uh you know cheap capacity but but
capability at the same time and and we
we're going to serve our customers. Uh
so that way in a way like it laid it out
the GitHub copilots or any co-pilot they
be able to do it through foundry which
is more of a enterprise platform and
then able to do it with uh our internal
frontier model trainings and and
inference.
&gt;&gt; Yep. Yep. Makes sense. Yeah. I do not
envy whoever has to make the the
capacity allocation decisions.
&gt;&gt; I do not either. Thank god I have an
engineer.
&gt;&gt; Yeah. Yeah. Right. Exactly. So now we've
talked about a lot of firstparty
customers. What about third-party
customers? I mean h how will they
experience the Maya? Will they be
renting it as bare metal or will they
just be consuming services that run on
Maya and therefore maybe have a
different price point compared to other
alternatives?
Yeah, I think uh like we discussed a lot
of it is just going to be being able to
embed it into our fleet and being able
to in some ways that point gets
abstracted away but the goodness of
obviously a more efficient
infrastructure flows through through the
customer right uh we are going to be
previewing our uh full software
development kit we started working with
some universities and some some you know
I would say whitecluff customers because
we want to make sure that we can onboard
them through our full stack. And so
there's going to be a process where we
actually focus first on our internal uh
customers, but they are serving
obviously external demand, but it's just
more abstracted away. And then there's
going to be a motion to give this in
preview to a select few customers as
well. And as time goes by, uh we will
obviously our our level of maturity in
serving this to a wider base will
improve as well.
&gt;&gt; Sure. Yeah. No, that makes sense.
Especially it, you know, this is only
the second system in the road map and
the this is a significant maybe like
redesign from the first system and so I
can see how also there's the benefit of
serving it internally are probably a
little bit slightly more forgiving
customers
as you're ramping it up. Um let's let's
talk uh let's jump to software. So, you
know, I know that that's always like the
the biggest hangup when it comes to a
new chip or a new system is just making
it so simple that a developer can port
their model or write it from scratch.
How are I'm sure you know we we've seen
others struggle with this. You guys have
seen it too. Like how are you guys
thinking about overcoming that software
adoption barrier?
&gt;&gt; Yeah. No, I think the way we think about
our software ecosystem is actually in
some ways it's simple in the sense that
you have to invest in software at the
same time you're building so so in the
past few years we were not just building
the silicon but we were building a
software fully fully developed ecosystem
around it as well right so things like
investment in Triton compiler that was a
big big thrust for us because we know
that you know we have to lower the
barrier for model porting and this is
one of the I guess learnings that we got
from Maya 100 as well is as we put our
first generation system out now we had
the time to actually go and start
building hey what are we learning from
the system how do we reduce the friction
for software developers to come on board
and we and we picked like two paths
right first is how do we go in like a
much more automated way from you know
PyTorch down to Triton compilers into
you know lowering that into Maya
hardware and we have a programming
language called nested parallel
programming language or we call it
internally as NPL, right? And so that
would be one path where you can use the
compilers and the debuggers and the
profilers that come with it to be able
to kind of move your models ported over.
But we also have the ability to actually
create a a standard kernel library. And
what that standard kernel library does
is it takes the most used operators that
are in our models today and it populates
them and and they are very performant
kernels because we have experts that
understand the micro architecture who
are writing this at the at the closer to
the bare metal and they're able to
populate a very uh you know strong
robust kernel library. And so and we
know that most of the performance is
actually determined by these kernels as
we profile our models. And so that has
given them we have the option to say hey
you are a ninja programmer. You really
want to go down absolutely we have a
full tool suite. We have the Maya
simulator. I know we have all of the
work that you knew. You can run a JSON
trace into a a model look at how things
are progressing. But that requires a
more sophisticated programmer to go
down. So we have done that heavy lifting
for a lot of the operators already. It's
it's an optimized kernel library that
will be available in the SDK as we
preview it. And so for operators that
may not be there, you have the Triton
compiler path. So we we made sure that
we made those investments. And so you're
right, this is not just about getting
the silicon and the system into the
fleet, but reducing that friction and
the model porting speed is going to be
super critical for
&gt;&gt; adoption. that yeah that makes a lot of
sense because of course yes you will
have benchmarks and and on paper the
chip looks exciting and of course
developers have to get their software to
run but then they have to extract all of
that performance that's sort of latent
in that system and it sounds like you
guys are are working hard to have
optimized kernels to help them extract
that
&gt;&gt; and and even before silicon arrived we
invested in a significant amount of what
I'll say pre-silicon environment
&gt;&gt; right And that preschool environment was
a combination of simulators and
emulation, you know, and so that really
helped our developers, our internal
developers to be able to build these
kernels way ahead of time even before
silicon came. And then when silicon
came, they were off and running because
they had a very, you know, a very
sophisticated
environment to work in. Uh so that was
that was a very deliberate again very
intentional investment that we done
because we knew that if you wait till
silicon to show up and then we say hey
here software go build on it it was just
take another and and these systems don't
have a long shelf life like this the
innovation engine is super fast and so
if you spend six months trying to
optimize software on it you've lost a
significant portion of the systems uh
you know useful life and so that's a
very important aspect of how do enable
our own developers with the right
infrastructure and tool set ahead of
when silicon comes by.
&gt;&gt; Interesting. Yeah, that makes a lot of
sense. Investing to make sure that
software is ready to go because to your
point, yes, the cadence is so short
these days, shelf life, you're right.
And so I know you guys, you said
multigenerational, you're already
thinking about Maya 300. So like given
where you're at in your road map, what
is a measure of success? like how will
you deem Maya 200 was a success as
you're moving toward Maya 300?
&gt;&gt; Yeah. No. Uh measure of success for us
again going back to
how have we changed that economics for
AI inference, right? How have we made
sure that we've covered that efficient
frontier? And today we know that there
are opportunities for us for certain
class of workloads, for certain
applications, for certain customers to
really drive the price point to where
there'll be increased adoption. there'll
be more usage and consumption and more I
would say uh innovation in the I I come
from um you know a semiconductor
background and I've worked in uh you
know building chips and I've I've seen
Mor's law kind of play out over years
and I've seen how Mors law has not just
you know driven down the cost of the
transistor but it has enabled new
industries
&gt;&gt; right it you know starting from PC to
mobile to you know now AI and so I
believe that really as an industry as a
whole. This innovation cycle in silicon
and systems is really what's going to
drive a completely new industry and a
new innovation cycle in AI. So at maybe
I'm I'm talking a little more
philosophically that's success as a
whole for our industry is to be able to
is able to now for us I mean we are
being pragmatic about it. We have we
have a lot of you know enthusiasm on the
system. So we're bringing in uh a lot of
models on it completely end to end
models are running on it. We are
populating uh different use case or
lighting up different use cases and this
helps us kind of ramp up capacity, ramp
up usage throughout this year but it
also flows into the multi-generational
road map like Maya 300 right this gives
us that onramp to Maya 300 because then
that will be another faster uh you know
acceleration. So we we what we would
like to see is yes we had the Maya 200
ramp and we had a faster Maya 300 ramp
uh and more and more I would say the
fleet the shape of the fleet the
economics of the fleet is continuing to
shift towards a more efficient point.
&gt;&gt; Sure as 200 ramped fairly quickly. You
made a lot of changes from the 100. You
ramped 200 quickly. You're innovating
full stack up and down the system. Do
you expect the 300 to be sort of less
drastic of architectural changes which
we we'll get into the architectural
details but do you expect that those
ramps will be easier like for example
you said you invested in all this
simulation and kind of pre-silicon
testing
&gt;&gt; yeah we do uh we we do I mean one thing
about you know architectures is you
don't change architectures dramatically
every generation there is a lot of value
in that
&gt;&gt; strong foundational stability
And when you have that frown
foundational stability and you innovate
on top. So my 300 is obviously we're not
talking about my 300 today but it is
coming with a lot of innovations but it
is also coming up on a very strong
inherently stable foundation that you're
going to build up. So from a developer
standpoint it is going to be you know a
lot easier to move faster and a lot of
that obviously will be abstracted away
in terms of just performance better cost
efficiency. Um so yes that's kind of
where we are approaching this from is uh
we don't believe in making architectural
right-hand turns every time and shifting
the entire ecosystem. There's there's
100% value in being able to build up on
a strong foundational base. Yeah. So
&gt;&gt; we believe 200 is that from foundational
base for us to continue to leaprog from.
&gt;&gt; Yeah. Yeah. And that totally makes
sense. And that sort of implicitly
suggests that you believe that today's
workloads will still matter in the
future with the Maya 300 generation.
&gt;&gt; Yes. Yes. Absolutely. I mean uh we still
see that you know this transformer kind
of models and the ability to I mean
there is going to be refinements there
is going to be new techniques coming
from research right but um you know the
the architecture is built in such a way
that you're able to continue to take
those in into your current architecture
I I do believe that that's that's not uh
that's not going to be an issue for Maya
300 or or in some ways many of us who
are building hardware have to place
those bets whether it's a third party
merchant silicon whether it's another
hyperscaler building we got to we we
we've got to look at the headlights and
I know there's that crystal sometimes
can be foggy and new research can pop up
but we still confident that uh you can
you can continue to scale with the
transformer uh u kind of transformer
technology we have in our models today
&gt;&gt; yep makes sense makes sense so um you
talked about cost efficiency and I think
one of the headlines in the blog and the
announcements was 30% better price
performance. Uh, and I and specifically,
uh, Scott Guthrie had called it the most
efficient inference system Microsoft has
ever deployed. And so I was curious if
we could get into a tiny bit more of
those like benchmarking details. Like
was that for small 70b models? Was that
large one trillion uh, parameter models?
Like h, you know, what workloads is that
because 30% is a lot and and and
comparing it to like your fleet. I know
Microsoft has Nvidia GPUs, you have AMD
GPUs, and so this this is a very sort of
like intriguing statement. So I just
want to unpack it a little bit.
&gt;&gt; Yeah. Yeah. No, absolutely. I think uh
what we do is we we look at different
use cases, right? And if if you look at
it like time to first token, right? You
could have something that's extremely
sensitive, less than a second. You could
you could sweep it to about 10 seconds
also depending on what use cases like we
talked about summarization use cases or
you know you want to do something in the
night come back in the morning it's
ready. So we've kind of swept across
that. Uh we've also looked at like SLA
for like time between tokens. Is it 20
millisecond? Can we be actually more
strict like 10 millisecond? I do believe
that the way you shard the model is
driven by your application. Right? So
the what we do from at the system level
is we give the ability for the system to
or or the next level up to say hey this
is kind of my use case and then uh we
have some unique topology requirements
like or not requirements but topology
choices that we made like hey we have a
fully connected quad. So tensor
parallelism in Ford works really well
and then you can move to export
parallelism inside the rack and so that
that's how we kind of are able to serve
that point that the customer or the
application needs. All right. So when
when we claim 30% we have actually in
some ways done this hardware software
core design to say hey this this chip
here or this system has a been cost
optimized. You brought out uh you know
hey how are we making some changes?
Well, we we have not invested in a
scaleout network,
&gt;&gt; right? We have invested in inferenced
driven uh chip. We have invested in uh
kind of taking a scale up approach more
than a scale out approach. That's
brought our cost down. We have kept our
wattage to just 750 watts. That's
brought our cost down. So it's a
combination of really hardware software
core design to extract the best you know
token output for that particular SLA or
capability and then you look at the cost
structure of the system compared to
whatever we have deployed in the fleet
and that's significantly lower and you
pull those two together and that's where
you get the 30% per per dollar
advantage.
&gt;&gt; Gotcha. So, so it's it's yeah it's it's
it's about making those right choices so
that you know that if if you were if we
were trying to build the most
performance system in the world we would
be making very different choices
&gt;&gt; right we would be pushing the TDPs up to
very high you know we would be pushing a
lot of other system and then we're
saying oh and if you're trying to do
training and inference both then there
will be another set of choices that we
would have made and so those are you
know paths that we pruned out early on
so that we can hit that 30% push per
dollar.
&gt;&gt; I love it. Okay, that's a perfect segue
for me, too. So, thank you. So, let's
get into those technical trade-offs you
made to unlock that 30%
&gt;&gt; per dollar. Um, you let's talk
networking because you mentioned no
scale out and a big scale up domain and
and I think the the blog post said 6,144
accelerators um was the size of the
scale up domain. Um, and so like tell us
more, you know, why no scale out? Why
such a big scale up?
&gt;&gt; Yeah. Yeah. Absolutely. I mean when we
studied inference patterns, we've seen
that a lot of our inference like you
know how many devices or accelerators
you need for inferences actually could
fit well within the rack, right? But for
the when you think about as an operator,
right? Because we are operator of the
system. We are we are deploying it for
our customers. We don't want customers
to be limited by hey you got to try to
fit inside the rack or you know if it
spills outside the rack suddenly you
have a very thin pipe and and everything
kind of slows down. So what we did was
we said we will have a two-tier scale up
and that gives us the ability to
actually take different jobs and place
it across the cluster and still have the
ability to communicate at you know a
relatively good performance. Right? So
that's where we kind of decided that we
won't do a scale out network but instead
invest in uh an innovative scale up
which is a it's got its own AI transport
layer. So although we use you know we we
we had this principle we don't want to
use anything custom or proprietary at
the you know so that our supply chain
gets more efficient. So that's why
you're using commodity switches, you're
using, you know, Ethernet cables and
switches. But then we said we can
innovate at the transport layer when two
mayas or two accelerators talk to each
other, right? And so those were the
innovations we put in our scale up
network and we able we were able to
basically say, yep, we are able to
reduce cost here but still make it a
high performance, highly reliable
scaleup network that can scale up up to
6,000 accelerators. And that gives the
flexibility to the operator to place the
jobs that they would like to in a way
that doesn't constrain them, right? And
so you get a lot more available nodes
and available accelerators to work with.
Now, we know that none of the inference
models today are going to need 6,000
accelerators, like they're going to
mostly fit into maybe 32 devices or 48
devices, how depending on how, you know,
constraints that you apply on them. But
the ability to span across a larger
cluster gives you the flexibility to
place the jobs or sprinkle them across
the cluster and you know ease your bin
packing problem.
&gt;&gt; Yeah, sure. Makes sense. Yeah. And of
course since you guys are operating all
these, you definitely have to think
about how to get as much utilization
even across different workloads as
possible. So that's super interesting.
Now um you mentioned uh keeping the
switch you know efficient uh and and
maybe multi- vendor possibilities but um
you talked about scaling up with
Ethernet and innovating at the transport
layer which sounds a lot like S sue
scale up Ethernet T or EON. Um I is are
are you guys using EON? Are you not?
Enlighten our readers. That's a great
question because because when we started
on this journey u een didn't exist
&gt;&gt; right and and we saw the need that hey
look u ethernet is is a perfectly
capable you know ecosystem to rise up to
the scale up challenges right and that's
why we believe and it's ob obviously
it's a multi-endor ecosystem you've got
you you have a healthy market you can
your supply chain is is much more
healthier uh you you can also
uh say that with Ethernet we say oh wait
but I think we have a we're not trying
to build an Ethernet that's across
10,000 20,000 endpoints or millions of
endpoints right a scaleup domain
actually has a certain I would say
criteria that you're optimizing for so
why don't we bring that smarts and
Ethernet fabric together and that's
where we started on this journey where
we said we're going to keep everything
standard and you know nonproprietary and
then we're going to only innovate on the
transport layer. Now that thinking that
philosophy is actually what ESEN is also
so we've been working very closely with
our partners. We were uh a very active
uh contributor to OCP last year when we
actually announced EEN with our partners
because we actually truly believe in
that philosophy because that's how we've
been designing our our systems and so we
were very happy to see the ESEN motion
come across basically says yeah you know
now all you need to do is if there is a
set of features that we believe are
important for optimizing at the switch
level let's bring everything together
let's bring those people together, make
those changes and then let the you know
XPU people or the accelerator people
continue to innovate at a transport
layer. So you kind of get the best of
both worlds in that sense. You get
features into your switch that are
agreed upon by a community in an open
fashion. Nothing proprietary there. And
then if you want to innovate at the
transport layer, if I want to innovate
or some other wants to innovate, you can
still have innovations at the transport
layer. So that that kind of demarcation
keeps the ecosystem healthy but also
innovating.
&gt;&gt; I like it. Interesting. Really
interesting. I like the philosophy. Um
now kind of related you did I feel like
I saw somewhere that the nick is
integrated onto the die.
&gt;&gt; Yeah. and and so there's like a little
bit of a different decision there to and
so uh was curious if this is like so any
sort of IP related to the Azure boost
DPU and and why you chose not to have
like a nick on the board but to actually
integrate it into the die.
&gt;&gt; Yeah. No, it it comes down to uh you
know we we we were extremely cognizant
of cost and power like if you like look
at a system you will see that uh you
know the operating cost or the opex
portion of a system in the fleet is
pretty high too not just the capital
cost like you know not just when you
purchase the system but when you run it
for six years and so we we were very we
were very I guess diligent about
extracting every watt from the system uh
and that's where we get that you know
cost and power efficiency point. And we
believe that with external nicks we were
adding a lot more cost into the system
and that's perfectly fine if you wanted
to scale out to a lot lot you know
thousands of accelerators for training
but we thought we thought that it was
not needed for inferencing and so we did
build a very you know I would say
optimized on die network controller that
is Ethernet based um but that's also
optimized and we don't like buffer or
anything like that like so we have an
extremely small area and power that goes
with the nick. We use our oni SRAMM
which is we've invested in a much bigger
SRAMM to keep the packets. So if there's
congestion right you know typically what
Ethernet switches do or anything that
they will try to create a buffer inside
uh the nick uh but we would say hey
we've got this large SRAMM let's be
smart about it let's use the SRAMM to
store some of the uh packets and things
like that and then pull directly from
the SRAM. So we built some specialized
DMA engines to do that. So there's
there's there was like a real thought
behind how we are going to optimize the
cost and the power of the scaleup
network. At the end we still have 1.4
terabytes of you know scale up bandwidth
unidirectional scale up bandwidth coming
out of every chip. So that's extremely
uh you know well provisioned but we do
it at extremely low cost and power
&gt;&gt; right and then we use Ethernet switches
and Ethernet cables which again brings
the cost down. So that's kind of the
thinking behind integrating the nick and
having a scaleup uh domain that's not
proprietary.
&gt;&gt; Ah this is good. This is really good.
This is very illustrative of the type of
decisions that can be made when you're
optimizing specifically for a certain
class of inference workloads. Now you
mentioned the large SRAM. So let's
transition to memory. Tell us about the
memory hierarchy decisions that you made
and and why you chose the SRAM. why you
chose a certain capacity and and
bandwidth for your HBM. Tell us more.
&gt;&gt; Yeah. Yeah. In fact, the the the entire
memory subsystem was really designed
ground up for LLMs, right? One thing we
know in inferences is actually the
system may not be flop limited. It may
not be, you know, computebound, but it
actually might be memory bound. And so
it was very important for us to a get to
the best S HBM technology that we can we
find at that time it was HBM3e but it
was also important to increase the
effective bandwidth of the HBM3e and
what I mean by effective bandwidth is if
I can reduce the pressure on the HBM by
smart innovations on my silicon then I
can get a better output out of the chip
and the system right and so this is
where we kind of invested in SRAMS
And what that SRAMM does is because of
our the way we our programming model is
we give explicit control to the compiler
or to the programmer to actually pin the
data where they want to be and the data
locality helps and so when you have a
lot more data sitting on die you don't
have to go to the HBM all the time right
so that's one reason why we actually
invested in a much bigger SRAMM um
because it kept and then the bandwidth
on die is about 80 terabytes per second.
But if you go to HBM, it becomes seven
like it just changes like a order of
magnitude, right? And then if you go
from HBM to some offchip, some other
accelerators HBM, it will reduce even
more. So thinking about the data
locality, the the pico per bit of data
movement was a very key consideration in
some of these design choices. So that's
why I think the combination of our
programming model and the way the
programmer can utilize this on memory
and then the micro architecture and
silicon innovations that went with the
onai memory. how we have partitioned it
across big clusters across some tiles.
Uh we have a advanced uh network on chip
that actually connects these SRAM
modules with our compute modules so that
the ex the the data can move between
compute and memory on much faster. These
were some of the innovations that we did
on chip to be able to really in some
ways the ultimate motive is how do I get
more tokens out of the chip right out of
the system and how do I increase the
effective bandwidth of the HBM because
everybody has access to the same HBM
technology.
&gt;&gt; So these innovations differentiate us in
being able to get to a much better
optimization.
&gt;&gt; Interesting. You're I'd like to hear how
you're thinking about designing your
memory so that you can have memory as
local as possible to the compute as you
can to minimize data movement to
increase effective bandwidth. Um this is
super interesting. Now it's kind of it
feels like a little bit of a new mental
model for programmers or developers like
how much will they have to learn? Is
there like a learning curve here or does
the compiler can compiler handle a lot
of this and just take it?
&gt;&gt; Yeah, the compiler is is extremely
sophisticated. I think the team has done
an excellent job over the last two years
to really build this out through um and
and like I said I think there are like
you know 80 90% of the performance of
the model is actually dominated by a few
operators right right you know how do
you run gym do you how do you run
attention different attention mechanisms
and things like that so we are able to
really kind of ease off that burden
because we have an optimized kernel
library that we have populated
Um we are of course happy for programmer
like real programmers who want to
extract every you know percentage of
performance out of the system. We've
given them full kind of access and uh
you know capability to go and program at
the nested parallel language level the
the NPL level. And so I think I think we
have a good balance here between you
know programmers who just want to port
something very fast and get running or
programmers who want to spend the time
really going down and and even then you
you can either rely on your our
optimized kernel library or if you want
to do some operator fusion or if you
want to do some you know kernel
programming we will support you in that
right we will give you the tools we'll
give you the visibility into the
architecture we have a similar later
that you can use. We can we can give you
all the traces. You can extract all the
traces that you need to really get to
that performant point.
&gt;&gt; Nice. So given that you've got all that
SRAMM and the HPM and you're giving
developers tools to kind of go crazy if
they want and get and just really like
eke out all the optimizations to reduce
latency as far as possible. Um, I have
to ask like zooming way out right now
what's hot in the news is like these uh,
you know, SRAMM only type chips that are
sort of like hypers speed, super low
latency. Uh, do do you feel like that
you guys have the right architectural
design so that people could start to get
that level of like really low latency
given given how much SRAMM is at their
disposal? Yeah, I I think it comes down
to like again the system choices you
have made because we've seen some
architectures that depend a lot on SRAMM
but don't have a memory hierarchy or
don't have the the right HBM uh behind
it. Uh we we've obviously seen some very
innovative very exciting uh products in
the market. You know you obviously have
like wafer scale engines. So I do think
and going back to what I believe is in
like if if you are really optimizing for
a certain class of workloads like
extremely low latency but everything is
staying in your SRAMM you don't have to
go your model doesn't you know spill out
of the SRAMM there is a there is a use
and need for those kind of applications
in your fleet those are great
architectures uh we've tried to become a
little more broader in that sense it's
like hey uh maybe the word I want to use
is that we're not as brittle sometimes,
right? You know, we can actually expand
a bit and say, "Hey, this might be the
class of workload that we want to
optimize for. This has a little more of
that ability to have a large enough SRAM
to pin the data that we need. But if you
have to go outside those boundaries, we
have an HBM uh basically memory
subsystem that we are serving with an
extremely you know fast on uh onchip
knock. We have specialized DMA engines
to go out on scale up and go towards HBM
sitting in somebody else's know data
sitting in somebody else's HBM. So we
give that the system is actually
broader enough to be able to absorb
those use cases. Uh so absolutely you'll
you know I I think there is a need and a
reason for those architectures to exist
but they have a certain criteria under
where they perform well and certain
criteria where they may not perform
well.
&gt;&gt; Yes. Yes. I hear what you're saying. So
okay this is a perfect segue again. So
you talked about you've got SRAMM but
you can spill over into HBM which the
chips that don't have any HBM they can't
do that right. So they're perfect for if
it all fits in SRAM. you've got the HBM,
you've got uh the ability to
reach into other accelerators through
the scaleup network to to get to their
HBM if it's like a really large model.
Now, another sort of hot thing in the
news lately has been that uh context
memory storage from Nvidia where you
actually can offload out if it doesn't
fit in HPM, you can offload to like
flash SSDs or something. Um
&gt;&gt; and and that of course the the use case
there is like really long context and
managing KV cache te tell me about like
really long context workloads with the
Maya like you've got access to lots of
HBM do you see ever see needing to like
offload KV cache or how you think about
it that's a great question and it comes
down to like how uh how you're using the
system right so obviously if everything
needs to be really hot KV cache then you
want the data to be in your HB BM and
what you would do is based on the your
model size based on the SLA that you
want to deliver you would shard the
model between maybe you know if if you
want to deliver an extremely high um or
extremely
fast response like time between tokens
is let's say 10 millisecond right what
you would do is you would actually take
the model and shard it or divide it
across a lot more accelerators
right that way you are using the HBM
bandwidth of a lot of accelerators
&gt;&gt; right at the same time if you don't if
you relax that to 20 millisecond or
something above you say hey I don't need
to use 32 accelerators for this I can do
it in 16 and sometimes if you relax it
even more I could do it in even less
time when you relax the HBM what happens
is that you can actually do it in much
fewer accelerators so that's kind of the
hot KV cache now there's also a use case
where it is a warm KV cache let's say
the users are not in there. It's like a
session, right? And you go back and you
come back in and you want to load up the
session again. This is where you don't
need to keep the data in your HPM. What
you can do is at that point you can keep
it in a second tier of memory. So we
have a head node and in that head node
we have provisioned u you know DDR
memory. we have SSDs in that head node
and then if it's a another tier we also
have like the Azure boost in our in our
system which is which can go over kind
of a network and pull data out of a blob
storage or a storage an Azure storage
account. So we have this cheering of
memory systems where we have the HBM, we
have local DDR and local flash and then
we can actually go over Azure boost
which is optimized for remote storage
and bring pull data in from the remote
storage u um as well. So we kind of
thought through like hey how does the
how does the user how does the
application want where where is the data
locality of the that is needed if it's
needed on die is on on the package is it
needed in the system but close enough or
you can take tolerate the latency of
pulling something from further out
&gt;&gt; nice awesome well thank you for the
education that was very interesting I
know we're bumping up on time so last
question I saw the blog said that these
were getting deployed near de mo Iowa
and that's exactly where I live. So, uh,
when can I come take a tour?
&gt;&gt; Oh, yes, absolutely. Anytime. In fact,
you know, maybe we'll we'll ship a rack
to your house.
&gt;&gt; Hey, there you go. I'll plug I've got an
extra bedroom. I'll plug it in.
&gt;&gt; I saw I saw it can be air cooled. It can
be air cooled.
&gt;&gt; It can it can be air cooled. Just make
sure you have the right power.
&gt;&gt; True. Yes. I definitely don't. Yes.
&gt;&gt; So, it was it was great chatting. I
appreciate all the questions. appreciate
uh you know h getting us the opportunity
to talk about Maya 200. It's an exciting
product for us. We're obviously this is
a multigenerational journey. Uh but we
truly believe that this is the kind of
innovation that changes the curve of AI
inference economics and and we're going
to be on it.
&gt;&gt; I love it.
&gt;&gt; Efficient frontier curve.
&gt;&gt; Awesome. Very exciting. Congratulations
to you and the team. Uh and let's stay
in touch. Come back again in the future
and update us.
&gt;&gt; We would love to. Thank you, Austin.
&gt;&gt; All right. Thank you.
