---
source: https://www.youtube.com/watch?v=9iqRdrBYUxA
vid: 9iqRdrBYUxA
title: Synopsys’ Amazon Deal and GPT-Synopsys: Ravi Subramanian
date: 2026-10-08
duration_sec: 2543
channel: Semi Doped
kind: transcript
---
Welcome everyone. I'm Austin [music]
Lines from Chipstrat and with me is Ravi
Summer, chief product management officer
at Synopsis. [music]
So we are live here uh in New York City
after Synopsis' investor day. Um and two
big announcements yesterday. One was the
announcement with Amazon for custom IP.
Um, [music] and I think that was valued
at over a billion dollars. And then the
second one and surprising and
interesting one uh was the [music]
uh announcement about the Open AI deal
with GPT synopsis. So I want to get into
both of those for our listeners and I'm
also going to just [music] go deep into
uh AI for EDA. So first of all, Robbie,
thank you for being here with me this
morning. [music]
&gt;&gt; Be here Austin.
&gt;&gt; All right, so let's get into it. So um
tell me and remind listeners who may
have not seen investor day what was the
announcement with Amazon all about.
&gt;&gt; Sure. Um the announcement with Amazon
was about application optimized IP which
is a key trend going on in the
semiconductor industry. And if you look
at how the building blocks for
semiconductors called semiconductor IP
have evolved. Um these are building
blocks that allow customers to
dramatically accelerate the time it
takes to build their chip because they
don't have to design these blocks. So
typically at the beginning of a chip
project a team is thinking what are they
going to make themselves? What is core
and then what is context? What are they
going to buy? Design IP is readily
available offtheshelf IP and Synoptics
is a leader in interface IP which is the
IP that connects cores um blocks to each
other. ARM is leader in processor IP.
&gt;&gt; So we're complimentary in that way. Um
for the better part of history, the IP
business has been standardsbased. You
may be familiar with USB, PCIe, etc. And
on your channel, I know you have a lot
of great analysis on that.
Standardsbased means there's a standards
committee. It's working to develop a
standard with industrial commercial
members and then once the standard's
ratified people can build products to
those standards and you have an
assurance of interoperability between
those standards. What's been happening
recently over the last five years is the
rise of custom silicon is growing and
that's really first and foremost being
driven by hyperscalers and it's becoming
customized primarily because workload
specific semiconductor design is
becoming so important for them. For many
of these companies there's really only
one or two applications that drive all
the revenue and the profit in these
companies. So it pays to optimize the
full stack rack to chip.
&gt;&gt; So in that context application optimized
IP is IP that is optimized for the
application in which the chip is living.
So you may have a PCIe gen 6 but you
also may have an ultra low latency PCI
gen 6 to get much much faster time. For
example, we're here in New York City for
people who are doing high frequency
trading. It's a very very desired
customization. So application optimize
IP is something where you buy you build
once and you actually customize it and
that is optimized for a workload. Um
this is what we announced with Amazon
which is um multi-year $1 billion plus
deal to deliver application optimized IP
which typically would mean from the
system level they are driving the
specifications which come down to the
actual IP level. So it may be connecting
CPU with a AI accelerator AI
accelerators to memory. So you may have
heard all the standards that are on your
channel PCIe, HPM, LPDDR, UCI, die to
die, um, and Ethernet. And these are
really the five key interface IPs. And
that's what customization is all about.
&gt;&gt; Okay. Interesting. There's so much here.
This this is great. Okay. So first,
let's start with um IP. So, you know, I
guess for anyone who's uh written
software,
it reminds me of like just taking a
library off the shelf as opposed to, you
know, to do some sort of function as
opposed to rewriting everything by hand.
I remember when I first started writing
software, I was literally writing
everything by hand. And then once I
discovered that you could get software
libraries where people had already built
it for you, I was like, whoa, this is
way faster. I could just take Lego
blocks, put them together, and focus on
essentially like the application logic.
And so
&gt;&gt; that's exactly the analogy.
&gt;&gt; Perfect. Okay. So it sounds just like
that for hardware. Now you talked about
having standardsbased IP which would
sort of be like hey um I need these
components to talk to each other and um
there are uh standards bodies who define
this communication in between blocks so
that everyone's components are
interoperable. Um and that's more of
your traditional standards offtheshelf
IP. But then you're you're talking about
here um say making a AI data center with
an XPU at the heart of it and now um you
want these interfaces to be custom so
that they can be extra optimized for
that one particular workload that now
we're running at giga scale. Right.
Right. Um okay so a couple questions
that I have there. Um, first t talk to
me about the business model for
standardsbased IP versus custom IP
because obviously standards space and I
think Cine called this factory one
&gt;&gt; build it once sell it to hundreds of
people. I can wrap my head around that.
Now uh the custom IP that's you know
build it once but it's custom for that
one customer. Of course it's very huge
customers like Amazon with Trannium,
Gravitron and Nitro. Um but that clearly
that has to be a slightly different
business model because you're only
selling it to them. So how how does it
work?
&gt;&gt; So in um what we have with Amazon first
from a business model. So let's start
with factory one actually. That's where
we have
&gt;&gt; uh an NRE non-recurring engineering work
and then the actual license fee for the
use of that IP. In that case, um,
standards committees take about almost
three years to so to get to a standard.
And the two things about a standard are
number one, achieve the functionality
and performance required for that
specific function. And then it doesn't
actually say anything about how you
implement it.
&gt;&gt; So that's where the engineers creativity
comes into how are we going to achieve a
PCIe gen 7 or gen 8. What architectures
needed? What things are in the analog
world? What things are in the digital
world? and then what's the total power
consumption latency etc. So a lot of um
everything about how it should be
implemented is not in the standard.
What's happening now and the rationale
for application optimized IP is don't
there's no three years people want to
actually take some of these standards
ideas and take a pre-ratified version of
a standard and do some things to begin
start using it earlier. So in that case
what we have is first a license fee um
then we have a customization fee and
Cine explained yesterday um there's a
very large scarcity of resources in the
IP design world and so from an
engineering perspective and how we look
at staffing we have very specific slots
for example we have eight engineering
slots for UCI
&gt;&gt; or three engineering slots for PTI we
have to prioritize those resources
and to define okay what is the business
opportunity we're going after. So that
customization fee is really allocating
that slot of engineers for these
customizations for this customer. So
that's why Cine called it a
prioritization. So the customers in
terms of what they work with us um if
you remember um there was a slide where
Ceine was saying what was the difference
between one and two and in factory 2 we
actually begin with the system level
requirements. those system level
requirements as you go down through what
does it mean for the chip and how it's
communicating translates into chip level
specifications which are really the IP
specifications but some of the
customizations would come around latency
throughput uh how many picoles per bit
&gt;&gt; um and um through a variety of different
um I'm going to say figures of merit
that they want to target it's still
standardsbased it's not um a uh complete
completely um offtheshelf non-standard
but it's taking the standardsbased
approach but really optimizing or
customizing based on the workload that's
running. A simple way to make this real
is suppose you have ad server software
that's running the response time to
serve an ad is a key figure of merit.
Typically as a chip designer you may not
think about that first but now because
of workload specific requirements your
response time you may recognize an image
and then decide to serve up an ad based
on an image that latency completely
determines how many ads you can serve
across millions and millions of
customers that becomes a key driver for
the latency in a PCIe either a switch or
an endpoint etc. So and then the third
element of the business model is
royalties. So this is really looking at
how do we participate with our customer
to we do the customization but we look
at the economics for the customer across
license um customization fee and royalty
and so this will be the first time
synopsis is actually driving to a
royalty model and with the agreement
with Amazon and others we haven't
mentioned that's the direction for
application optimized IP.
&gt;&gt; Gotcha. Okay that makes a lot of sense.
[music] This episode of Semi-Dop is
presented by Crusoe. Crusoe builds AI
infrastructure from the ground up. Power
data centers and the cloud on top.
Crusoe intelligence foundry is their
managed AI platform. And a nice feature
in there is serverless inference. Now,
if you're going what in Jensen's name is
that it means that there are no GPUs for
you to provision and no clusters to
manage. You simply pay per token. If
you're running open models like GLM,
DeepSeek, Kimmy or Quen, Cruso's managed
inference is fast. Nearly 10x faster
time to first token and 5x the
throughput of VLM. Their memory alloy
caching layer routes requests to
maximize cache hits. Since it works with
Open AI SDK, switching over to Cruso's
API is quick and easy to get it running.
All you have to do is pick a model, grab
an API key, and start sending requests.
If you sign up with the link in the show
notes, you get $5 in free credits to try
Cruso Intelligence Foundry. Think of it,
five whole bucks, so you can just burn
some tokens just for fun. And some of
these open models are quite inexpensive,
so you'll actually have a ton of fun
with it. Check out Crusoe and see their
serverless inference on their managed AI
platform. You really got to find out
this for yourself. There are a whole lot
of more features in this that I want to
try out for myself, but serverless
inference, I found, is the best place to
get started. It's a great way to support
the show and try out Cruso's
Intelligence Foundry. The link is in the
show notes. And now back to the show.
[music] A lot of follow-up questions.
There's so much goodness here. Um, okay.
So, first one thought Wii with the
standardsbased IP. My first thought was
like, hey, if you're designing IP to a
standard, it feels um I'm wondering how
a person differentiates because there's
a standard and so it feels like anyone
else could um design to that standard.
But what I heard you say was the
standard defines how the like the
interface should happen, how the
communication should happen, but it
doesn't touch on any of the
implementation details. So even though
there's a standard, you can still
differentiate from other people making
standardsbased IP based on your
implementation.
&gt;&gt; Absolutely. And um standard specifies
the protocols um the electrical
interfaces. Um it doesn't specify how
much power it should take.
&gt;&gt; It doesn't specify whether you should do
equalization in the analog world or the
digital world.
&gt;&gt; And it doesn't specify the um
&gt;&gt; packaging that's needed.
&gt;&gt; How true.
&gt;&gt; Right. And um it doesn't specify
anything about the system environment
it's going to live in. So those are all
opportunities to differentiate in that
you can have the lowest power, lowest
latency, you could have the smallest
form factor, you could have a north
south very thin implementation of that
IP so it could fit in a very particular
way on a die or and so everything down
to the actual shape
&gt;&gt; Yeah.
&gt;&gt; of that IP
&gt;&gt; is where you can differentiate.
&gt;&gt; Gotcha. That makes a lot of sense. Okay.
So, and and really what you're talking
about is like which figures of merit are
the most important when designing this
IP and even in the standardsbased one.
I'm wondering do you have different
implementations of a given standard?
Like if someone comes to you and they
have different requirements they're
trying to fit it into.
&gt;&gt; So definitely and maybe some of the
biggest areas have to do with having low
power.
&gt;&gt; Sure. And what techniques are you using
in your implementation to achieve low
power? So the same PCI generates
standard two different IPs providing the
same functionality but dramatically
different power.
&gt;&gt; Sure.
&gt;&gt; And today there's so much pressure on
getting lower and lower pico per bit
that's being pushed through. you see
really creative implementations and yeah
the best place to get a front row seat
at that is to go to ISSC the
international solid state circus
conference every February in San
Francisco where all the world's leading
chip designers coming in with their
chips and they're showing how they
achieved amazing figures of merit right
from a a key IP building block all the
way to a full chip and it's just amazing
what creativity there is but that is
what the innovation that's fueling
circuit design today and continually
understanding How do you harness what is
possible in terms of energy consumption?
What's possible in terms of data flow
architectures and uh latency? How do you
have your hardware and fir your firmware
hardware interface to be able to have
very fast reef configurability of these
IPs? Uh very very rich source of
engineering ideas and creativity.
&gt;&gt; Amazing. Cool. So when these two
different IPs are designed, one is super
low power and one's not there.
Obviously, the other one must be
prioritizing something else or there's a
cost for that super low power.
&gt;&gt; Exactly.
&gt;&gt; So, there's there's a couple different
design tradeoffs that are made and and
yet I'm sure you have like, you know, a
certain portfolio, a few SKUs, but then
it sounds like with the custom IP, the
application optimized IP, um the your
partner, in this case, Amazon, is is
saying, "Hey, still those those handful
of off-the-shelf ones um aren't quite
perfect. if we think we could take it
farther and and and you're starting at
the highest level probably like the rack
scale or even the data center scale. Um
thinking and and deciding what is the
figure of merit like as a as a product
manager that's prioritizing what what is
the
&gt;&gt; figure of merit that's most important to
us. It might be power and what are
trade-offs we're willing to make. It
might be cost or die area or something.
Um so then that's coming all the way
down and and then it's getting
customized. Um, now you talked for the
standardsbased IP that there's a
licensing fee and NRE which is that NRE
sp like does every customer pay the NRE
or is that kind of like a we designed it
once cost that gets advertised or what
like
&gt;&gt; sure
&gt;&gt; explain that NRE.
&gt;&gt; So depends on the nature of what the
implementation is. Um there may be an IP
that's not available at a certain
foundry on a certain process node.
&gt;&gt; Ah
&gt;&gt; right. So if you look at the whole
spectrum, there's the IP, there's which
foundry and process node it's available
on, and then there's the I'm going to
say um kind of envelope for the
standards compliance, right? And a good
way to think about that is
a PCI standard. I know we keep talking
about PCIe, but or a UCI standard.
Actually, we should start with UCI. It's
a standard that's not a standard.
&gt;&gt; That's what I've heard. in that every
customer wants a different number of of
the ports.
&gt;&gt; So there's some effectively NRE
required. You need to be standards
compliant. The standard really doesn't
say that you can't have something with
only two wires instead of six. So that's
a type of NRE, right, that we'd have to
do. You could say, well, hey, isn't that
a factory 2 because you have to do some
customization. The the way to think
through this is once customization
is really challenging our engineering
scarcity that or the needs challenge our
scarcity we really need to look at how
we allocate those pieces. UCI complexity
much smaller than PCI or others. So
there we have some engineering work we
need to do but typically you'll see the
NREs associated with well we don't have
it on this process technology or they
want it um being able to talk to
something else in addition to what there
is but um those are things which we can
advertise right across the whole um
opportunity for that IP on that node.
&gt;&gt; Sure. Sure. That makes sense. And then
uh uh to the factory to the application
optimize IP um you mentioned the
customization fee which and you
explained that nicely it's more of the
prioritization
um fee and then of course the most
exciting part the royalties of course
this makes me think of ARM's business
model and and you actually had mentioned
ARM earlier where you're talking about
interface IP and their processor IP
&gt;&gt; um so yeah te tell me about the exciting
opportunity there with the royalties
Because obviously with the licensing fee
um it you guys get paid upfront
presumably for each like design start
but with the royalties you once the uh
design actually gets manufactured that's
when you collect the royalty. So it
feels like there's lots of upside
especially for a customer like Amazon
who's deploying millions of training
chips.
&gt;&gt; Indeed. So Amazon as a lead partner will
be lead in driving the specifications of
what gets built. Um but there's a good
story here to share. If we rewind
history and go back about a decade ago,
um when ARM was a mobile processor
company and they wanted to enter the
data center market,
ARM and Amazon
entered a relationship [clears throat]
&gt;&gt; which was really about application
optimized ARM processors for the data
center. And with AWS being a lead
customer at the time really drove the
evolution of that IP into the data
center world.
&gt;&gt; It's a very similar analogy here,
&gt;&gt; right? So indeed the opportunity for
royalty is is very good. But if we look
at the economics of what we're
investing, significant investment,
right, to get that return and and really
make the economics work for both
parties, really look at a model where
you have now royalty as an element tied
to the type of chip, the volume of chip
and what's the IP content.
&gt;&gt; And so it's pretty standard in terms of
the the model used for royalty. It's
well understood, but it's the first time
now with synopsis participating actually
in the silicon stream. uh we announced
Amazon yesterday and um as Cassine
mentioned there are other companies
already that have we've closed these
business with and we look forward to uh
sharing those details but um it's really
driven we see by one major thing and and
why it makes sense for these customers
people want highquality IP available
within a specific time window
&gt;&gt; and today meeting that time window is so
critical
And if you miss a generation of what we
call application optimized IP in a year,
then you miss a generation of your chip
on what you can do. And in the high
stakes game where companies are
introducing new chips every year and the
whole merchant to using your own uh
custom chip is the stakes are getting
bigger and bigger. the pressure we see
on these teams trying to reduce the time
of a particular generation from 18
months down to 12 months and making sure
they get to a very specific market
window and and so that is the challenge
and so the the if you will the
commitment is to be able to deliver high
quality IP on time to get that quality
some of the customization includes well
you should verify the IP in the context
of the system so what are the test chip
starts changing in his definition so you
can bring up the chip much faster. Do
you have a team to support the bring up
of the IP at the customer? Don't stop at
the door, hand off the IP and say, you
know, you're on your own.
&gt;&gt; Yeah.
&gt;&gt; So it starts really integrating Synopsis
success with the customer's success of
getting that chip into a system. And so
you see there's a lot of alignment of
interest now that Synopsis should be
aligned with the customer to get that
working in their product. Yeah. Yeah,
that makes sense. And you also make an
interesting point where this gives
Synopsis, traditionally an EDA company,
an opportunity to be part of the design
at the architecture level, the whole
rack system, maybe the whole data center
level all the way through to system
validation. So of course that EDA,
that's also IP. There's probably
opportunities, you know, all the way
down through simulation.
&gt;&gt; Indeed. Um, and then when you talk about
making a test chip, Synopsis then is is
design doing the front-end design,
backend design, and are you're actually
manufacturing the chip.
&gt;&gt; We we do hundreds of test chips a year.
&gt;&gt; Okay.
&gt;&gt; Right. From our just existing IP
business, and that's just part and
parcel. A key reason for Synopsis
leadership
&gt;&gt; is every single IP is silicon proven.
&gt;&gt; Nice. And you will see LinkedIn posts
with eye diagrams showing you know we've
got our first you know so many gigabit
per second IP out there and that is what
allows customers to trust that okay this
is going to come up and it's going to
come up right now the challenge is not
just that the IP should come up the IP
should come up in the context of the
system the customers have been living
with this challenge more and more as the
systems get more complex And we have to
participate in that success because
that's the window of time.
&gt;&gt; Yes. Yes.
&gt;&gt; And it ranges all a number of things. Um
yesterday we shared um at our investor
day etched
&gt;&gt; which is a company's building uh new
type of uh processor. Um after they got
their chip back it took 44 days for them
to get the workload running
successfully.
&gt;&gt; They did all of that with Zebu
emulation. We have IP ready on emulation
as what we call IP kits. So all of that
allows them to really compress the time
it takes so that as soon as the chip is
back, they've done all this validation
before. So they have high confidence of
how fast they're going to be able to get
the workload running. But that's a IP
coming together with hardware assisted
verification coming together with system
validation.
&gt;&gt; Nice. Nice. Great opportunity. And so I
like that you frame it around
compressing the time and just ensuring
that your customers get to market on
time because that's what it's all about
with this with these data centers and
and you know the race to the next
biggest model and so on and so forth. Um
so I'm going to use that to shift us
into AI for EDA. Um so you know
compressing time is what it feels like
it's all about. You know, uh, Richard
Hoe and OpenAI, partners of Synopsis,
um, had the jalapeno chip, which
everyone was very excited about how
quickly they were able to shrink down
the front-end design. Um, so tell us
about your Synopsis' agent engineer
portfolio, and maybe for people who
aren't as familiar, like tell us about
like the um, front-end design and
back-end design and where uh, agents
using synopsis tools uh, fits into the
agent engineer portfolio. like help us
under understand exactly where what the
agentic AI is doing and then where is
the handoff to the synopsis tools.
&gt;&gt; Sure. So um maybe the the best place to
start is if you look at the stages of of
chip design at the front end you're
actually you have a specification and
you're trying to write the description
of the function. Um this is typically
done in RTL hardware description
language and so it's very much like
writing software. You have a large piece
of software that describe the chip. Each
of those blocks that are there that and
that are ultimately connected to create
the functionality of the chip. The
design and the verification is the
writing of the RTL and the verification
that the functionality is correct.
Verification today also goes into
for example if you're in a a robotic or
a automotive application is the RTL safe
&gt;&gt; means does it fail safely so there are a
whole bunch of verification associated
with that is the RTL secure do you have
a threat scen set of threat scenarios
that test that RTL whether it's a block
a subsystem etc so all of that
verification goes on taking a specific
design under test and then really
challenging it. Functional verification
requires getting enough coverage. And a
good way to think about coverage is if
you have, you know, a four-bit circuit,
uh, you've got two to the four states.
If you have a billion circuit, you got
two to the billion states. And, um, it's
going to be impossible to cover two to
billion states. So the notion of
coverage is to say how many of the
states that are important have you
actually tested and it's impossible to
test 100% of them. So you need to be
able to explore the state space to
understand well you know you're running
the simulation but it's not giving you
any more coverage. So it's a waste
simulations. Don't spend more time
simulating that. So in the front end
it's all about design and verification
of the functionality and you know any
other capabil features such as safety or
security.
Then it's about well I'm going to
implement this. So is this RTL actually
the lowest power?
&gt;&gt; Two individuals can write RTL completely
separately.
each one thinking about their own
figures of merit and come up with
completely two different languages with
two different powers. So how is this RTL
going to translate into power into
performance and into area? So in the
front end people want to be able to
really get to a conclusion where I've
got my RTL defi defined for all the
blocks and I've got a good understanding
of the power and performance in area.
The minute you can start getting
subsystems, it's not just a power
consumption of one or the other. Um, in
many chips now they're turning on and
off different domains when they're not
using them to be able to minimize power
or they're putting thing into just
dripping or sipping current just to keep
it at a quiet pace until it's needed
again. So many many things are explored
in this front-end phase and then it
comes down to okay actual implementation
where you're deciding you're starting to
use um uh very specific rules about how
to build things for a specific foundry
and look at the actual synthesis
placement routing and the actual
implementation
and that gives you a view where
do I actually achieve the performance
because of the distance between blocks,
the wires between blocks, how should you
think about clocking, how should you be
thinking about the communication of
signals. Um, so you know the movement of
data now is taking more and more power.
So what you put close to each other in a
physical placement in RTL it just looks
like software
&gt;&gt; but on physical placement it looks like
oh I'm putting this software closer to
this because there's so much more data
that affects power. And then finally
there's a set of tools around
manufacturing and manufacturability
&gt;&gt; which is really guiding the a customer
tapes out but you tape in to a foundry.
So foundaries have a tapein process
where they determine are they going to
accept the database you sent them and
say yes it adheres to all the rules that
I require in order to actually start
designing this. So that's the front end
the implementation and then the
manufacturing piece. Now AI in chip
design in synopsis view is really about
exploiting the power that intelligence
brings in terms of um the capability to
move from automating to assisting to
then starting to create things that are
more autonomous.
&gt;&gt; So EDA the A in EDA is automation. Oh,
sure.
&gt;&gt; Um, as workflows get more complex,
um, many of the trade-offs between steps
in a workflow are not so obvious. So
assistants can start bringing knowledge
about different things, different pieces
of information in the workflow to the
designer to think about how can I
further optimize and in some cases I
mean ultimately it's assistance because
it is it is a co-pilot with you if you
will.
&gt;&gt; Sure. And then autonomy starts um the
process of starting to use reasoning and
some decision making to relieve the user
of making those. The user is still a
human in the loop to check the results
but the decisions made on how to get to
the fast the best solution starts
becoming autonomized. And then finally
in more complex things you have more
longunning jobs which are not about time
but are about outcome
&gt;&gt; and there you want to basically combine
reasoning and and and the autonomy to be
able to sequence how it's doing work
taking advantage of calling the tool. So
that's our spectrum and um we in
Shankr's presentation yesterday he had a
whole evolution of how this is going to
autonomy
with synopsis the way our autopilot uh
platform is set up is really we spent
almost I'm going to say 18 months um
really understanding
there is how we think about selling AI
in EDA there's how people are going to
consume it. So there were a number of
things we were testing about how people
want to consume it and one thing came
out really clearly. People want to think
about AI in a similar way about they
think about I have a budget and I'm
hiring verification engineers, design
engineers, implementation engineers,
they have skills. If I can think of AI
as coming to me with a certain set of
skills, then I can easily relate to how
I am going to use it in my work.
&gt;&gt; And what we've seen in many of these
companies, they've started off with,
well, this year my MBO is to learn about
AI. The next year my MBO is to find a
pilot project and try out AI. And then
the third year start using AI in some
part of a chip development effort. Of
course, that was earlier. Now time
scales have compressed. Everyone wants
to they hear about their colleagues and
what they do and they go I want that.
&gt;&gt; So that immediately um drives to a
different paradigm and our platform is
really thinking with the concept of
super agents or um which are really
longunning agents. Then you have the
task agents and then you actually have
the tools. So if you look at agent
engineer the notion we introduced about
a year ago making agent engineer real
for verification there are a set of
tasks you can that agent engineer based
on debugging something or verifying
something basically represents to the
user these are the type of skills I can
get these are the tasks they can do and
they can call the synopsis tool and
that's across the every stages in the
EDA design process chip design process,
but also in the simulation and analysis
process for mechanical, thermal,
computational dynamics,
&gt;&gt; and we're not done yet. We're really
thinking about what's the best way and
the easiest way for customers. How can I
adopt this on my team, can a
verification engineer say, I'm going to
check out 20 verification um agent
engineers today? So engineer paired off
with agent engineer
&gt;&gt; and the [clears throat] agent engineer
brings a set of skills and this engine
um this engineer says I'm going to have
that focus on root cause analysis for
all the bugs and then I'm going to
review what the fix is and so the nature
of each of the original EDA jobs starts
changing to be a co-working with the
agent that interesting
&gt;&gt; and every day you're coming in you may
be doing a a very taking a agent
engineer for verification but doing very
different things with it. So, we think
the the engineering landscape is going
to dramatically change, but it's it's
going to make engineers, I agree with
Richard, super engineers and make them
much more powerful in what they can do.
&gt;&gt; And the long-term vision for us is we
see so many companies in so many
industries wanting to build their own
chips. And in order to be able to do
that, we need to make it easier to build
chips, but we also need to have the
ability for many industries to create
those chips. And we think AI has a very
fundamental um role to play in driving
the growth of the world.
&gt;&gt; Yeah, definitely. So, okay, I have a
thousand questions, but I'm being told
that we only have like five minutes
left. Um so we'll have to do a follow-up
to dive into this but that's very
helpful to understand the front-end
design the backend design the design for
manufacturability um useful to
understand you know synopsis tools and
then agents that can do tasks with those
tools and then uh like higher level
agent that um can essentially like sort
of supervise or help take a task end to
end and then of course the human at the
top who can come in each day and think
about the outcome I need to accomplish
today and which like agents am I going
to use Um so let's talk about the GPT
synopsis announcement and then how does
that fit into um using agents like where
do I use GPT synopsis?
&gt;&gt; Sure. So um starting point is if you
look at what we announced with open AAI
it's really the alignment between the
two companies that for being able to
apply uh frontier models and frontier
intelligence to chip design it requires
a strong collaboration
and um the leaders collaborating to
create leadership is really the theme
and we are both aligned on really
enabling many more industries to be
building chips. So today um GPT synopsis
uh as we announced is a specialized
frontier model specialized for
semiconductor design with synopsis
tools.
So the way the model is you could think
of the autopilot platform that was
introduced or a customer's platform
those platforms essentially have compute
and LLM optionality typically which
means they can pick whichever LLM they
want and they pick the compute resources
what we see with customers is the
application of AI they want to get good
quality of results which means models
really need to understand chip design
&gt;&gt; and second compute is becoming a limit
limitting factor. It could have way more
licenses but if they didn't have the
compute and Cine shared yesterday what
we're hearing from customers in terms
their need to have more licenses to be
able to drive uh the ability to use AI
across certain parts of the chip world.
So where the uh GPT synopsis fits is
each of these agentic platforms have an
LLM optionality. GPT synopsis can be
that LLM
&gt;&gt; and the way with open AAI we decided how
are we going to bring this to the world
is it's going to be a service where open
AAI provides the specialized frontier
model that was carefully developed with
synopsis
set of compute needed to run that
&gt;&gt; and the forward deployed engineers to be
able to make sure our customers could
actually leverage that. Synopsis brings
the tools, the expertise and then the
skills that they're needed to
essentially make GPD synopsis an expert
user of a synopsis tool. What that means
is the productivity of the user is
significantly enhanced because they've
got an expert tool user there. They
don't really need to explore so much.
You can explore much faster with this
service. And that's how we're bringing
to market. So customers may use OpenAI's
cloud compute their compute resource and
um customers may want that model
resident on premises so that open AAI
would essentially have that running on
their own comput premises
&gt;&gt; right so one of the key things and and
you probably are hearing you know
spending more time thinking about well
what is AI and how do customers want to
consume it is a significant investment
for us in I'd say using the the rule the
lord gave us two of these and one of
these [laughter] it would be wise to use
that in that ratio and and really
understand how can it be easier to
consume this and we're really excited
with the early semiconductor companies
we've been working with this has been
long in the making uh but we all shared
a vision about you know what do we need
to think about everything from what the
engineer needs to security to um
protection of data movement of data and
then how do we challenge solve those
biggest challenges including computing
&gt;&gt; yep yep so I I'm thinking of um synopsis
GPT GPT synopsis as like a turnkey
option where I get a great frontier
model fine-tuned using synopsis tools
and um with the compute or get that
compute uh you know on premises of
course um and for deployed engineers
because nothing is actually turnkey and
so they can help you know ensure
success. Um, so I guess last question
and you know we could do a follow-up on
this probably alone. Um, but I know
we're running short on time. So then the
question that everyone's asking is
where's that layer between what the AI
can do and what synopsis can do? And
there was a saying yesterday. It was in
AI we believe in physics we trust. Maybe
explain that in like 30 seconds and help
us understand like why AI isn't the
solution for the physics and the
synopsis components.
&gt;&gt; Sure. So I think there's fundamentally
two things when we think about building
a product
and that is what's the ground truth and
the ground truth is what you see when
you have the physical product in front
of you and it is operating in the world
that it is meant to operate. Our point
here is the ground truth is based on
physics and not just one equation. Just
like the ground truth in you know in you
can say the ground truth in how you
simulate a crash of a car um depends on
so many variables even though you can
say well hey it's just the motion of the
car crashing into an object how does a
deformation happen etc. LSDina, a tool
from ANCIS, um the number one crash
simulator in the world. Why is it
trusted? It's trusted because the ground
truth is matching what's in the
simulation.
&gt;&gt; So, and that is over decades of how
should the simulation evolve. It's not
just taking one equation from a physics
book and implementing it. Similarly,
when you go to doing semiconductors, the
device equations for a transistor, they
evolve transistor to transistor. When we
went from planer to finfet, finfet now
on all all the way now to gate all
around uh and then moving to cfett what
are the things number of equations grows
by you know 200x
and so the physics to accurately model
what is being built is changing. It's
not static and many people say well you
know some equations haven't changed in
hundreds of years but the application of
those equations to be confident you can
build a product it's not there so in AI
we believe is the power of AI and what
it can offer is what we strongly believe
in but in physics we trust is because at
the end of the day the ground truth to
have the confidence not hallucinate and
be deterministic in your outcome
&gt;&gt; is really what defines is a product
going to be successful uccessful or not.
&gt;&gt; Yeah. Yeah. Makes sense. Especially the
stakes are so high. Hundreds of millions
of dollars to manufacture a product. Um
so you obviously can't get it wrong.
&gt;&gt; Indeed.
&gt;&gt; Um okay. Well, we're going to stop
there. Listeners, I hope you learned a
lot and enjoyed this. We have to follow
up because again, I still have like a
thousand more questions, but this was a
great start and uh big news, exciting
times for synopsis. Thank you.
&gt;&gt; Thank you, Austin. Great to be here.
&gt;&gt; Awesome. [music]
&gt;&gt; [music]
