---
source: https://www.youtube.com/watch?v=oWQG207QPvk
vid: oWQG207QPvk
title: NVIDIA's Marvell Strategy, Is Memory Different This Time?, Intel's Ireland Fab
date: 2026-04-03
duration_sec: 2522
channel: Semi Doped
kind: transcript
---
So, memory memory has gone crazy that's
all that's all I can say. Next topic.
Next. Wait, feels like you've been
saying this for the last several weeks.
No, it's gone crazier. I'll tell you
why.
Hello listeners and welcome to another
semi-dope podcast. I'm Austin Lines of
Chip Strat and with me is Vic Shaker
from Vic's Newsletter.
All right, Vic. So, I thought let's
start today with the NVIDIA Marvell
NVLink Fusion $2 investment topic. You
know, I felt like this one didn't get
much coverage in the press. Like not
many people talked about. I felt like
it's just like oh, another $2 NVIDIA
investment next.
Yeah, it's the NVIDIA $2 cookie.
Everybody gets a cookie. Exactly.
&gt;&gt; Everybody gets a cookie. Go ahead and
get your free cookie. Everybody.
&gt;&gt; get $2 and you get $2 and you get $2.
&gt;&gt; [laughter]
&gt;&gt; Yeah, totally. So, let me read a little
bit from the press release and then
we'll try to unpack what what does this
mean and what are some implications. So,
the press release stated from NVIDIA,
"This partnership builds on NVIDIA
NVLink Fusion, a rack-scale platform
that enables customers to develop
semi-custom AI infrastructure using the
NVIDIA NVLink ecosystem." And then it
went on to say, "Marvell will provide
custom XPUs and NVLink Fusion compatible
scale-up networking while NVIDIA will
provide the supporting technologies
including Vera CPU, ConnectX NICs,
BlueField DPUs, NVLink interconnects,
and Spectrum-X switches, and the
rack-scale AI compute." So, kind of a
lot there. Let me hand it over to you.
What what is your reaction in reading
this and maybe what are some insights
that you have? So, the first thing that
came to mind when I heard this was why
is NVIDIA investing in its competitor?
Basically, I thought okay, custom ASICs
are here to eat NVIDIA's lunch and
they're bad for NVIDIA. So, why is
NVIDIA giving a $2 cookie to Marvell so
that they can do better in making custom
ASICs which would hypothetically
displace GPUs, right? I mean, some
sounds like a weird deal to me. That was
my first reaction. But later, I think I
I thought about it and it was like okay,
it's not quite as simple as that. So,
we'll talk about it. Yes, yes. Which I
will say that the $2 piece is also
interesting, too. Which is like why?
Obviously, it's like let's partner
together and I'm incentivizing you. But
it's kind of interesting cuz it's like
lots of companies can partner jointly on
things and have skin in the game without
a $2 investment. But um tell me okay, so
tell me how did you get past the Wait a
minute, NVIDIA, you're investing in a
competitor XPUs. Yeah, so I read through
the whole announcement, too. And this
was the XPU was the one aspect that
stood out immediately. But then, if you
look a little bit closer, the the press
release also says "The companies will
also collaborate on silicon photonics
technology." Kind of broad. And if you
go down, you'll see that this is
something to do with
advanced optical interconnect solutions
and silicon photonics technology. So,
that is very interesting to me because,
you know, apart from this whole custom
ASIC discussion which is like obviously
the top of mind thing. You have to
remember that recently Marvell bought
Celestial AI which
is great for their like photonic
interconnect between dies.
So, they called it their photonic fabric
technology which is think about it like
you know how like Intel has EMIB which
is like a little substrate you just put
inside that connects two chiplets
together with like metal interconnects
and it could connect like any part of a
chiplet one to any part of chiplet two.
And so, this is like the same thing but
in optics. Like there are these are
light links between chips. So, this is
very cool technology. And Celestial got
bought by Marvell
for this for some like some time back.
And my thought was okay,
you're going to work together on silicon
photonics. Are you also going to work
on, you know, integrating your HBM and
GPU with like optical links at some
point?
Like is this the kind of scale-up? Then
the other question I had was like is
NVLink in the future going to be
optical? That's really interesting.
Yeah.
Could It could be, right? It's a just a
protocol. Yeah, it is. Right now, the
physical layer NVLink happens is on
copper and you know, they're just like
metal wires that, you know, connect
everything up and there are these serdes
circuits at either side that like send
the bits
you know, over this physical medium.
There's no reason the physical medium
cannot be light. NVLink in theory can
work over optics. Sure. Fascinating.
Okay, I'm going to Yeah, that's That's
really interesting. So, I I have another
angle and I think I can tie that that
together, too, with it. So, when I
started reading this and thinking about
it, NVLink Fusion. So, of course So, the
first question is going back to custom
XPUs like NVIDIA's basically saying, you
know, GTC recently we saw them say,
"Hey, now we're going to have like this
end-to-end solution that actually has
kind of like multi-vendor silicon in
some respects because it's NVIDIA's Vera
Rubin, but it's also the Groq now
NVIDIA-branded Groq LPU. And so, they're
they're sort of saying like if we
disaggregate inference depending on
the outcomes that you're trying to
achieve, you could have a system that
can get you very low latency using some
of the Groq stuff for decode, but also
like higher throughput with the with the
NVIDIA stuff. And naturally, my head
went into like oh, well, it kind of
feels like they're trying to say to
Marvell's partners like you should put
your XPU racks in the same data center
with our NVIDIA
GPUs and maybe our LPUs. And if you have
if you use NVLink to connect it all, it
can all talk together. So, it's it felt
like a step in the direction of even
more
heterogeneous. Is that how you say the
word? Homogeneous? Heterogeneous? I
don't I don't even [laughter] know.
More multi-vendor silicon
bringing or saying like okay, fine. We
admit like XPUs are going to be part of
the solution, but you should talk using
NVLink and like fit nicely into us. And
then I was trying to think more about
like well, who would want to do that and
and what what is the benefit versus just
having your like oh, you already have a
data center full of Trainium for example
and a data center full of NVL or GB300s
or whatever. And and I say Trainium
because Amazon had made an announcement
Well, first of all, Amazon Trainium,
they work with Marvell as a back-end
partner. So, there's already a
relationship between AWS and Marvell.
And then on top of it, I found from
December 2nd of 2025 and I don't I like
barely remember this cuz so much has
happened since then, but
there was an announcement around NVLink
Fusion that Amazon I think Trainium 4
was going to be open like was I'm not
sure I should go back to exactly how
they phrased it. But basically, that
they're going to use NVLink, but they
also talked about using UALink, too. So,
tying this all together, when I thought
about this investment, the more I
thought about it, I was like oh, this
kind of feels like the customer
AWS Trainium already said they're going
to use NVLink and Marvell needs to kind
of come along and make sure that their
XPUs can work with NVLink and this is
maybe NVIDIA bringing it all together
and saying yes, you were going to make
this happen for your big customer
Trainium who we want to be That's
Project Rainier or however you pronounce
it. It's like a million
XPUs already. So, clearly like AWS is
deploying things at scale. So, I I think
if you're NVIDIA, you you're thinking
like we can continue to sell AWS GPUs
and can we play in that expanding XPU
TAM as the interconnect and maybe as the
supporting CPU racks, supporting KV
cache storage clusters, right? So, I
maybe it's NVIDIA seeing a expanding pie
and saying we we want to play in AWS's
pie and this is how we're helping do
that. NVLink Fusion investment into
Marvell, like tighter friendship there.
So, what you're saying is like this is
more on a need basis because AWS is like
look, I want NVLink and I want you to do
it, Marvell. And Marvell's like, but I
can't do NVLink. And so, Marvell goes to
NVIDIA and is like, "Hey, I'm going to
make a lot of chips for this like and
they want NVLink. Can we work together?"
And NVIDIA's like, "Yeah, sure. Why not?
I mean, you're going to give the chips
to AWS anyway, but we can own the rest
of the platform and lock them into that.
So, it's like a win-win all around,
right?
That is my hypothesis, exactly. It's
win-win-win win-win all around. And then
to take it maybe one step further to
what you were saying about photonics and
and Celestial, if I recall, Celestial
and I I need to go double-check on all
this, but if I recall, one of their big
potential customers is Amazon Trainium.
I think that was part of the whole
Marvell acquiring Celestial because
Celestial had lined up such a customer
and my hunch is that the customer said,
"We want to bet on you, but we don't bet
on startups. So, you know, you should
get acquired and then you should be
acquired by Marvell and they're a
partner of ours here and then we will
trust that everything will come
together." So, I also don't wonder if if
you're not wrong in that like hey, this
is NVLink and it's working working
closer with Marvell into Trainium and by
the way, Trainium's excited about
photonic fabrics in the future. And so,
yeah, maybe this is a way for Nvidia to
even play there in the future with
NVLink over optical die-to-die
connections. Yeah, if you look at the
online reaction to this piece of news,
it's always like, "Oh my god, Jensen is
a galaxy brain. Look at him, like he's
he's not really giving up anything. In
fact, he is secretly locking in all the
customers into the interconnect fabric
and drawing them in because, you know,
there's only this many GPUs or A6 you
can put into a rack, but imagine when we
go to like over a thousand coherent GPUs
in a rack, or you know, we need
basically how much networking? So, you
know, he's betting on the substrate
instead of the compute. No point in
computing with A6, you know, competing
with A6 instead." Like, yeah, I kind of
get that, but I like your story better
because it's more of a need-based thing.
It's more like logical or realistic to
me. I don't know if it's actually real,
but sounds nice. Well, thank you. It's
my speculation, and I do feel like the
the customer pull of Amazon saying,
"Let's make this happen." is an
interesting angle. We'll see if it's
true. Can I add in one more benefit I
think there is to this whole situation?
Yeah, please. So, Marvell now has NVLink
capability, which is great for them, but
they also have UA link capability, which
means like anybody who wants to make
these A6 with Marvell has both choices
now. They are not locked in, and Marvell
wins either way because, you know, what
ecosystem do you want to AMD? Do you
want to work with UA link? You want a
custom ASIC? Sure, we'll make it for
you. Or you know, Google, do you want
something? Or like you say, AWS wants
NVLink? No problem, we got you, you
know? So, they can do everything now,
which is amazing.
As opposed to Sorry? Go ahead.
No, I was saying as I say, as opposed to
Broadcom who also makes A6, but like
they're tied into UA link now. They
don't have NVLink.
Yes, yes, and and Broadcom's definitely
pushing E-Sun. So, I do think this is
strategically sound from Marvell to say,
"We want to be an open partner so that
you don't have to get locked into
Broadcom switches, so you don't have to
do E-Sun if you don't want. You can do
UA link, but of course, UA link, like
AMD's pushing it. I think it's Tera Labs
is out there. Oh, Marvell, by the way,
they had an announcement a while back
that they are going to support UA link,
and they announced a custom UA link
scale-up switch back in June of 2025. By
the way, they bought that XCON company
kind of quietly recently. Um
&gt;&gt; [snorts]
&gt;&gt; and $540 million
um they have a uh Strata S
uh 260 lane PCIe 6.0 switch, but I think
maybe it's they're going to be able to
support NVLink or UA link with this
silicon. So, Marvell will say, like you
said, you can do NVLink, you can do UA
link, and we've got the silicon to do
the switching no matter what protocol
you want.
&gt;&gt; Yeah, so that opens up the door to a
like a lot of lot of people uh to use
Marvell for Marvell for whatever they
want. And I like the other thing that
you said, which is
you can deploy these A6 as a separate
rack right next to GPUs. So, one of the
fears that I read online was it's not
like it's going to eat up what Nvidia
GPUs, like they're going to sell lesser,
right? Why would you enable your your
competitor to put in A6? Now you can't
sell GPUs. I don't think that's ever
going to be the case. You always need
GPUs, and if you see the I think the
Blackwell Ultra ML perf six results that
recently came out, it is fantastic. Like
the the the those GPUs are fantastic
even now. Yeah, performance-wise,
they're amazing. So, it's not like
they're ever going to go away because if
you still need to train models, you
still need to do stuff, and the
inference is opening up all these
different workloads that we didn't
imagine like in the early days of AI
when we were more focused on training
models rather than just doing inference
now that at scale like we are starting
to do. And you know, with this agentic
AI, it's even worse, like token
explosion is like already here or is
going to get even more, right? So, in
all of these situations, I think Nvidia
wins because GPUs are still going to be
used, and now if you hook it up all with
NVLink, you can do this extreme
co-design approach that, you know,
Jensen always keeps talking about with
even A6 because why not? Totally, right?
Why not have those workloads running
really close to the orchestration CPUs
and the GPUs, like put it all right
there. Yeah, co-design it. Totally
totally agree. Very relatedly to this
topic of running NVLink and UA link and
E-Sun, there's a startup out there,
Upscale AI, and they've got they're
building the switch Skyhammer, and I've
talked to them at some of the the shows.
I think OCP and recently. And anyway,
their pitch is like, "Hey, we're
building silicon that can run either
protocol on it. You don't have to as a
company, you don't have to make an
NVLink switch and a UA link switch and
have team like put all the costs and
design the masks and everything, and you
could just have our switch. And there's
a little bit of a trade-off, which is
like there's a little bit of overhead if
we are in the software defining like
what protocol you're running, but it's
and it may be take a little bit bigger
chip size because we have a little bit
of overhead, but it's totally worth it.
And therefore, if you buy our switch, it
can run UA link, it can run presumably
NVLink, and then it can run E-Sun. And
so, I thought on the one hand, I thought
like, "Oh, this is exciting for Upscale
AI because it's sort of validating like,
'Hey, Marvell's saying we want to serve
customers who want any of these
different protocols.'" Of course, it
there's questions around route to market
for Upscale AI. It's like, "Is Marvell
going to buy you? Is Broadcom going to
buy you? Are you going to be able to
convince customers to buy your switch
instead of just partnering with these
guys?" And then on top of it, bringing
it all the way back to NVLink and
everything, I was Googling um Upscale a
little bit more to refresh on the
details, and I saw that Nvidia had
poached their There was an article
saying Nvidia poached Upscale AI's one
of their founding members and who was
like a chief architect to join Nvidia's
NVLink Fusion team as just like 2 months
ago. The conspiracy grows. Right,
exactly. So, make of that what you will,
but I do think there's a lot of
interesting things happening in this
space, and it'll be fascinating to see
in a year or two what scale-up protocols
people are running, and what is the
switch silicon supporting it. So,
tell me this, what happens if like UA
link and E-Sun doesn't become the
standard, and NVLink, because it likes
hooks up to everything anyway, and I
remember like sometime back Qualcomm
also like partnered over NVLink so they
can like provide their CPUs to hook up
with Nvidia GPUs via NVLink. So, it's
like a CPU supply thing that they signed
up sometime back. So, if it becomes so
that NVLink becomes a dominant
they've opened it up via the Fusion
platform, then what happens to UA link,
E-Sun, and what happens to Upscale AI
because now we need only one platform,
one protocol, right?
So, here here's my question to the
proposition of could it only ever be
NVLink? And I think immediately I think,
"Well, AMD has no incentive to support
NVLink because they don't want to.
Nvidia's their biggest customer, so they
would hate to be selling their own racks
and then giving a slice to Nvidia." Now,
you might argue, "Yes, but and so
therefore, that's why they're supporting
UA link so they can have an open
alternative." But what if customer pull
is totally all about NVLink because
customers are saying, "Yes, we're we're
going with multi-vendor silicon, but we
want to reduce complexity as much as
possible, so we want the scale-up to be
just one standard so we don't have to
mess around with it or worry about it."
But then you always get into a place of
whenever there's one winner, then they
can extract a premium, and everyone gets
tired of paying the Nvidia tax, and then
someone pops up. So, I have a hard time
seeing it ever settling on NVLink. But
you make a fair point, which is like,
"If all these XPU people are starting to
use NVLink so they can talk nicely with
Nvidia, Nvidia's sort of disaggregating
in their walled garden and letting other
vendors come in, but it's still sort of
like Nvidia's garden, if you will, and
they're kind of in calling the shots and
in control." And that's going to make it
hard for AMD to say, "Put put racks of
Instinct into your big multi-vendor
deployment, you know?" Yeah, but you
know, if history has taught us anything,
especially when it comes to interconnect
specifications, there has never been
like one solution. Like, Mhm. why do we
still have so many USBs, right? In the
history of interconnect, there has never
been like one platform. You remember
XKCD comic that says like, "Oh, we have
a standard specification. No, we have to
a dozen of them. Why do we need a 13th
one?" And then now every Now there are
13 different standard specifications.
Something like that. Yeah, yeah, I
remember that. I remember that for sure.
Exactly. So, it's that's what it is.
We're always going to have more more
standards than we know what to do with.
Totally. And at the end of the day, it's
never one-size-fits-all. There's As
engineers, you always like, "Okay,
there's something that's created that
works a lot for a lot of use cases, but
there's always that one use case where
it's like, 'Oh, if we strip out all this
stuff, we could do this use case way
faster.'" So, it does stand to reason
that there will be more than one, and
that the there are many incentives for
there to be more than one. How about
that?
&gt;&gt; All right, anything else to say on this
Marvell topic? No, let's see what
happens. I'd like to see some actual
products or some cool stuff happen with
all these announcements. Otherwise,
we're just like speculating and
pontificating and making up conspiracy
theories. Yeah, exactly, right? Come on.
Yeah, keep it interesting for us.
Totally. Otherwise, people are like,
"Dude, those guys dream up the craziest
things, and all this was was about
whatever, $2 billion or something. Yeah,
I know. All right, let's talk Let's talk
memory next. So, you had an article this
week about memory. Set the stage for us.
So, memory memory has gone crazy. That's
all That's all I can say. Next topic.
Next. Wait, it feels like you've been
saying this for the last several weeks.
No, it's gone crazier. I'll tell you
why. So, the DRAM contract prices,
right, in Q1 of this year
was like 95%
higher in just a single quarter. You
know, NAND has been up to, like, you
know, to a lesser extent, but still, you
know, mul you know, very high some 60%
or something. And now there's like
another TrendForce projection that comes
through that says the contract prices in
Q2 of 2026 is going to be like 58 to 60%
more compared to Q1. And it is
compounding at a rate that nobody has
ever seen since like the 2017-2018
cycle. And it's just like getting so
expensive that a smartphone makers and
PC makers are like, "I can't pay for RAM
at this price. I just can't. How am I
supposed to make a product and sell it
to a consumer who is already
cash-strapped in an economy that has
like an incredible like number of
layoffs and wars and you know, you name
your difficulties out there nowadays.
How can I make low-to-mid-tier devices
when RAM prices are going to eat up
like, I don't know, 20 to 30% of my bill
of materials? It's ridiculous." So,
what's happening is that a lot of
companies are thinking, "Okay, the only
way we can do this and absorb these
costs is to only make premium-tier
devices. Let's not make low-end and
mid-end mid mid-tier phones or, you
know, PCs. Like, anybody who wants to
buy like a sub $100 phone or the sub
$500 laptop, forget about it. They're
not going to have any RAM." So, that's
one option people are thinking about.
These companies are like, "No, we're not
going to do that low-end stuff. We'll
just go to the high-end stuff." The
other The other thing that usually
happens in situations like this, and it
has happened in the past, is companies
will start de-speccing low-end devices.
Like, if a mid-tier device had, you
know, 8GB of RAM, the new version of
that is only going to have 4GB of RAM,
right? So, what happens in this whole
process is that the demand from the
consumer side starts to go down cuz they
don't want to pay, right? And because of
this, once demand goes down, the supply
goes up, right? And then the then the
prices, you know, then there's then it
leads to overcapacity because nobody's
buying DRAM. And now the prices crash.
And so, this is
what is called the memory hog cycle, you
know, it's like hog as in pigs because
this is like when pork prices go up, all
the farmers go and they start raising
pigs. But then
when the pigs are like ready for like
making into pork or whatever, they all
hit the market at the same time and then
there is like an oversupply of pork now
and then the prices drop and then and
then again everybody stops growing pigs.
And now there's like a shortage of pigs
and it starts all over again. So, this
has happened in memory so many times. In
my Substack article, I give like three
examples of why it was happening. Yeah,
this is why memory is like insane right
now and like big companies are even
cutting down mobile chip shipments
because nobody can afford memory. Even
the Raspberry Pi has raised prices three
times since December and it's only been
three months, okay? You can't even buy a
Raspberry Pi, just saying. Now, the
whole question is is this time any
different? What usually happens when
customers and, you know, the consumer
market pulls back like this is that
stuff crashes. This has always been the
peak and the seasoned memory industry
people understand this sign very
clearly. They see this consumer demand
dropping and they're like, "Okay, this
is where things are going to turn
around." And it usually crashes after
that. So, the question everybody's
asking is like, "Is this time any
different?" With the demand of AI, which
is the fundamental reason why we don't
even have DRAM to begin with because all
the DRAM is going to made into like HBM
or server-class HBM DRAM DDR memory,
there's nothing left for consumers to do
like use, right? So, the real question
is is this time any different? Because
the AI demand for memory is ridiculous.
Like, so what if the consumer demand
drops? The memory makers will just sell
it all to AI companies. And think about
it. You You like Micron discontinued,
what is it, the Crucial line?
&gt;&gt; Yeah. Yeah. And all these big players,
SK Hynix, Samsung, they're all
converting their DRAM product lines into
HBM because there is like it's a higher
margin. I don't say margin anymore. It's
a questionable thing to say. Anyway,
it's a higher ASP kind of memory. It's
harder to make, but it's higher ASP. And
the reason I say that it's not a higher
margin per se is because the pricing for
like standard DDR memory or even
server-grade DDR non-HBM has gotten so
high that companies like Micron are
making more out of non-HBM memory than
they are with HBM memory. Right, which
is wild. Zooming out, like, memory
makers have only so many wafer starts
per month.
If they and then they have to decide
what percentage of these wafers, let's
talk DRAM, are going to be for HBM and
what percent are going to be for just
standard DRAM. And there's the trade-off
that it takes like 3x the wave bit of
HBM as it does for DRAM. And I think for
HBM
for that's increasing maybe even to like
4x. So, you're having to make a
decision.
Well, if I make more and more HBM, it's
going to just eat up a bunch of wafers
that could have gone to DRAM. But early
on it was like, "Hey, that's fine. The
HBM has really high prices and therefore
pretty good margins." Now, when you're
talking about like consumers, when I
think, "Okay, wow, there's going to be
less wafers needed to go into phones for
DRAM." I'm like, "Well, that's fine
because that wafer can immediately slot
Like, there's two different customer
classes here. There's like people like
data centers and consumers. And like,
data centers just going to eat up every
wafer that used to be a customer wafer.
That's not a problem." So, like, look,
if we don't sell as many phones, like, I
don't think that's fine. That wafer just
becomes a data center wafer. But the
interesting thing that you that you're
pointing out is like, "Okay, fine, but
does it become a DRAM wafer or an HBM
wafer?" And actually there's some pull
to make it DRAM because like because
there's not enough DRAM and and then
therefore like margins are really good
on the DRAM. And it's and it's like
probably has better yields and is less
complex and stuff. So, so there's an
interesting dimension there to say like,
"Okay, if you take that wafer from from
consumer, what should you allocate it
to? Should it be HBM or DRAM?" Yeah, but
as far as this time is different, like,
my hunch is like, I'm not sure that the
consumers don't need as many wafers.
Like, I think it feels like those wafers
for now can just get slotted right into
data center customers and go for servers
for all these CPUs that are needed for
agentic AI, obviously for all the
accelerators that keep getting created.
But what do you think? I mean, do you
think that the weakness from consumer
won't get picked up by all the data
center customers and there will be
oversupply?
You see, the the consumer market is a
giant whale of a market for DRAM because
think, you know, how many phones and PCs
are there? Because the question That is
the real question. What you're asking is
the good question because the question
is when the demand drops, does AI suck
up the overflow? Yes. Is it a big enough
market that sucks up the overflow? In
the past, if you look at the cloud
server cycles, it didn't absorb it well
enough. Then there was the crypto boom
where everybody was like buying like
crypto mining equipment and the DDR
prices shot up, too. The crypto Then
when crypto crashed or whatever, and
people decided it's too expensive to
mine the stuff, you know, it was an
oversupply similar situation happened.
Did In the past, it has never absorbed
it. Here, it's like a little bit
different. I think this time it can
absorb it for some time. Of course, many
companies are still building out
capacity, okay? So, when that actually
hits in 2018, I don't know when. Yeah.
Yes. Yes. You will have the oversupply
issue, I'm guessing. Like, because now
what's happening is that companies are
careful, okay? Like, these executives
have been burned many times. They're
professionals. They know what they're
doing, okay? It's not like guys like you
and me are like, you know, pontificating
about the wafer.
Yeah. Yeah, but they really know what
they're doing. So, they are actually
controlling how much supply is of DRAM
is being pushed into the market because
when you convert a conventional DRAM
line into HBM, it is a one-way capex
intensive conversion,
a fungible line. Before you could make
like LPDDR, which goes into phones, or
GDDR, which goes into GPUs, or standard
DDR, which goes into PCs, they're all
relatively the same. It could run off
the same wafer supply. Here, it's not
like that because the conversion is like
is completely different. Like, the HBM
product lines are very very different
because they have through silicon vias.
So, the processing steps for an HBM DRAM
is different. And that's why you need
three to four x times because these
through silicon vias have a keep-out
space around them. So, you just can't
like stuff transistors around through
silicon vias. So, the density of DRAM
drops when you build DRAM for HBM. And
now you need to stack so many like DDR
DRAM chips to make HBM. So, all of this
means that it just sucks and vacuums up
all the supply and goes away there,
right? So, the conversion process is
also expensive because now you have to
test HBM memory and make sure the yield
is right. All of these problems, it is a
commitment that a memory company makes
consciously. They're just not going to
do it like willy-nilly, which is why
there is the contract the contract
structure for memory has changed. Now
long-term agreements are pretty, you
know, 3 to 5 years ahead and companies
don't want to miss the long-term
agreement cuz in the cloud era it used
to be a quarterly or a yearly deal. So
the moment like people backed out, that
was the end of the cycle. Now No, it's a
multi-year deal and people are over
subscribing probably to memory. I don't
know if it's going to be an over
subscription. I don't want to say like,
"Oh look, we have so much demand for HBM
and this is it." There could be a case a
scenario where yes, we are repeating the
same mistake we have made in the past
and we are over all these cloud and data
center builders are over subscribing to
DRAM yet again
and we will see the same, you know,
history is only going to rhyme again,
but the long-term agreements are like 3
to 5 years. Companies don't want to give
up their line in in this, you know, in
the spot in the line cuz that means HBM
allocation will go to your competitor.
You go to the back of the line. Nobody
wants to be there. So why do why not
overbuy just because you can, right? So
So long-term agreement, so you're
committing to buy this certain amount at
this price for the next 3 to 5 years.
Are you locking in price or can the
price move?
&gt;&gt; So that is like a give and take, right?
So there are price floor clauses, which
means memory makers are saying like,
"Look, this is the minimum price lock
that we will do." So there is like
structure to that too. Because if you
think about it, given how the demand is
rising, it is in the interest of memory
makers to actually sign shorter term
deals. Like if you file quarterly, you
can go and renegotiate next quarter for
a higher price. So it's actually in
their benefit to do that. But no, that
from what I read, it seems like the
longer term agreements are in place so
that supply and capacity planning can be
better. There's better visibility when
you sign multi-year agreements.
&gt;&gt; Yes. Yes, that's exactly what I was
thinking, which is you're committing to
a volume and therefore
it feels like
there's going to it would it feels like
it'd be hard for
uh
demand even if demand kind of collapses
on the consumer side and maybe
the data center doesn't come in and suck
it up. Like from a supply perspective,
there should be very good visibility for
the next 5 years and obviously they're
bringing more capacity online, but maybe
I wonder if that prevents a sudden crash
and like oh suddenly we have way too
much supply and not enough demand, but
it's like no, you yeah, we have really
good visibility into supply. So we
should be able to commit our capacity
accordingly. Of course, is that's like a
supply floor and we don't know CAPEX
keeps going up at these huge
hyperscalers and we don't know
uh
what are their future projections. I'm
sure they talk with them, but it's still
hard to predict the future. I mean like
you can make a scenario where it's like
maybe some of that the consumer weakness
in mobile, fine. Is there going to be
consumer weakness in PC? I don't know.
And then what about this new form factor
like the agent computer that's going to
start sitting on some people's desks to
run open claw all the time or to run
agents all the time. Like very
speculative, but that could be a new
form factor that could also suck up some
of that consumer weakness. It's still
kind of a kind of a consumer form
factor. I picture it in the enterprise,
you know, but So PCs also looking down
like all the estimates I saw are like
it's going to be like 12 to 13% lower
shipping, which is a significant amount
actually. So PCs are actually affected
as well and interestingly, you know,
mobile phones use LPDDR low power DDR
and if you look at like the Vera CPUs,
they use low power DDR too. Think about
that. Like Nvidia wants to sell so many
CPUs now. All of them use low power DDR
that mobile phones use too. So where is
the supply going to come from? Totally.
There's a new competitor a new buyer in
town for LPDDR. Well, and I saw this
like interesting piece of news on X and
also on a website after.
I am not sure if this is true. Don't
quote me on it. Might be a total rumor,
but I'm going to say it because it's at
least entertainment value. The rumor is
that Apple is like overpaying for DRAM
right now and buying up vacuuming up all
the DRAM supply so that the competitors
can't get to it. So they can like even
though it's expensive to buy it, they
already have a premium tier product and
they will use it on that, sell it at a
high price and lock everybody else out
of DRAM supply. Fascinating. Who knows
if that's true, but it's a very
interesting chess move and it makes a
lot of sense that they would be
incentivized to do that.
Yeah. Essentially, Apple could help
right now. We're already hearing that
the low-end smartphone market is
basically going to be frozen for the
next couple years, dwindle and so they
could if they wanted to as the premium
flagship competitor, they could help
continue to freeze that out by buying up
all the DRAM and being willing to pay
the premium to to freeze their
competitors. Who knows? It's a
hyper-aggressive move, but yeah, this
business is like that. Right. Totally.
Okay, so let's move on from memory. We
have just a few minutes left. I think
the last topic, Intel buys back Ireland
fab from Apollo. So the news is that
Intel is paying 14.2 billion for the 49%
stake that Apollo bought just back in
2024. Um the funding is cash plus like
6.5 billion of new debt. What was your
reaction when you saw this news? Uh I
mean, it's not mine, but everybody
believes this is great for Intel and
that Intel's fab strategy and you know,
the their
Intel A everything is looking good and
this is great news. So everybody's like
hyper bullish on this.
It definitely does feel like a confident
signal from Intel that like, "Hey, 2
years ago we're bleeding cash. It's not
clear how the future's going to work
out. We have to get very creative on how
to finance these build-outs. We're even
willing to um sell just under half of
our crown jewel fab um to private
equity, which anytime you're dealing
with private equity, those those are
always like kind of more ruthless
partners, I should say. And so there's
got to be something in it for them. It
has to be very favorable for them,
right? So it kind of feels a little bit
like a back against the wall move. Now
just fast forward 2 years, it does seem
to signal a lot of confidence. Like,
"Hey, we feel confident in the signals
that we're seeing from our foundry
business and from our customers. Our
stock price has appreciated. It feels
like now is the right time to buy back
this fab. And by the way, it's I I
believe this this was in Ireland, right?
And it's Intel 4 and 3. There is a huge
demand for server CPUs and a lot of that
had actually been on Intel 107, but it
would make sense that even more 43
capacity will continue to be needed. And
so like I think conceptually like just
making sure that Intel owns that fab as
full control over it, which they were
already in direct control over it
anyway, but it just feels like a strong
signal and that like we actually think
there's going to be continued demand for
43, but my question for you is like,
does this signal that they feel very
confident about 18A P
and beyond or is it unrelated? Cuz I
think a lot of people right away are
like, "Oh this must mean that Intel
feels very confident in 18A P." And on
the one hand you could say, "Well, this
is an Intel 43 fab. They're just buying
it back and and getting rid of some
expensive debt." But on the other hand,
to me it does signal that like, "Oh
they're confident in the foundry
business." Which means they're confident
in 18A P and and potentially Intel 14A.
What what's your reaction? Yeah, I'm not
going to go so far. I'm going to err on
the side of caution here and be like,
"See, I don't know." And I really don't
know because
&gt;&gt; Yeah. I don't want to draw and
extrapolate a line to say that A18A
yields are good and that's why they did
this and all of that stuff because I was
thinking about why would Intel do this
now? Like why why? Cuz you look at it
this way. Like 2 years ago they sold it
uh for 11. What is it? 2 billion, right?
To a part this private equity firm
called Apollo. Before that, like 1 year
before that, that's when they opened
this fab. The fab 34 in Ireland was like
there was like an 18.4 billion dollar
investment, which is also by the way
Intel's only EUV fab in Europe. So it's
strategically important too. But then
like a year later under Gelsinger's
smart capital strategy, they sold it for
11.2 billion and they rebuy it back in 2
years for 14.2 billion. Like you said,
the private equity firm has to have
something in this and what they have
here is 3 billion dollars in profit in 2
years. Totally. Yeah, right. Someone's
going out for dinner and fancy steak and
champagne to celebrate that. Right.
Right. So in the
you know, down times of like Intel in
2024, this was a good way the smart
capital strategy to get some money by
did selling 49% of the stake uh of this
fab to Apollo and get it back. But then
uh the question is why now? Like and
it's like you said in the press release
too. It's not like an all cash deal
either. So they have they put some cash
down and then they have like 6.5 billion
dollars in debt. So the question is,
what if they didn't do it now? Apollo
owns 49% of it, right? So every core
Ultra and Xeon chip that is out of fab
34, which I think these are like at
least the server grade chips and
the one the the CPUs coming in Intel 3
and Intel 4, Apollo will take 49% of the
profit. So unless Intel believes that
they don't want to give 49% of the
profits and that it is better to pay
today
the the 3 billion dollars extra to buy
it back and spend the 14.2 billion
dollars so that they can have 100% of
all the benefits of all the output of
this fab going forward then why would
they spend the money? Yeah, that's a
really good framing. Like hey, we're
just going to give that 3 billion now
because we want those profits which
means they think that they're going to
sell a lot of these chips and they want
Yeah, that's the upside of the 49%
across tens of millions of chips to them
is better than that 3 billion dollars
now. Also, you don't want to be like
paying another extra 3 billion dollars
if you delay this by 3 years.
&gt;&gt; Correct cuz the value surely yeah will
increase. You know what it
reminds me of when you play Monopoly and
you could mortgage your properties like
in the good times you're like buying all
these properties and then times get bad
and then you're like oh crap I need to
mortgage these things so you flip the
card over and you mortgage it and then
but you can't make any money if someone
lands on it. You don't get that money,
you know? And they're like no no we want
to flip this card back over like we're
going to spend now to flip it over cuz
we think a lot of people are going to
land on this in
&gt;&gt; Yeah, like like like you know somebody
who's playing with you like your kids or
something like oh my god he's come twice
to this property and I've got it
mortgaged. I've got to unmortgage this
now because you know he's going to land
on this three more times and I'll get
the money back or I spent in
unmortgaging it even if I had to pay 10%
more. I think that's a great analogy. I
love it. Yeah, totally. It's like oh man
Meta and OpenAI and Google and whoever
keep landing on this and we need to flip
it back over.
Well, yeah I hope you know they land on
it though if if they don't land on it
it's like oh now I'm short of capital
again. Yeah, right which always happens
to me in Monopoly. My luck runs out. I
have lost Monopoly for the last 12 years
every game.
It was news. I think I won once and it
was like news like all my kids and my
wife we were all celebrating that I
actually won something. Like how am I so
bad at this game? It's a good thing I'm
not in charge of Intel. There you go.
It's a a strategy but it's also luck but
maybe your strategy is no good. Yeah,
it's user error man. It's not luck.
There you go. Well, hey that's it for
today. Thanks everyone for listening. We
hope you enjoyed this. If you're
enjoying Semi Doped we'd love if you
give us a five-star and a quick review.
Comments are great too on YouTube
videos. Reviews for Apple Podcast,
Spotify, wherever you listen to this and
share it with your friends. Word of
mouth is awesome and we hear from other
people that they had friends share it to
them and so that is really cool and
that's a nice signal for us that you're
enjoying what we're doing. So thank you
so much. Check out our newsletters and
we'll see you next time.
