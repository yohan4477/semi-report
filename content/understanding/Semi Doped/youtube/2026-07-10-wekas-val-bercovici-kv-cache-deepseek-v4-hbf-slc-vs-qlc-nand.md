---
source: https://www.youtube.com/watch?v=swHE-VZxZik
vid: swHE-VZxZik
title: WEKA's Val Bercovici: KV Cache, DeepSeek V4, HBF, SLC vs QLC NAND, CXL, NVLink, Tokenomics
date: 2026-07-10
duration_sec: 3851
channel: Semi Doped
kind: transcript
---
Welcome to another semi- dope podcast.
Uh I'm Vic from Vick's newsletter and
with me is Val Burkovichi, chief AI
officer from WKA. Wcker is an AI data
and memory infrastructure company.
Val has been on Semi-Dope before and uh
you know a few months ago we spoke about
context memory storage uh right after uh
Nvidia announced their platform. So if
you want to check out that whole
conversation uh it's right in the back
catalog and we'll try to link it up here
as well. Uh but yeah today's
conversation is more about uh more
recent developments in the world of
memory and storage and where things are
going in AI inference. Val, thanks for
being on the podcast.
&gt;&gt; So much fun to to be back, Vic. And as
we predicted, the only constant is
change. So, uh, lots of updates to talk
about since I was last on.
&gt;&gt; Awesome. Isn't that so exciting? We have
like things that are constantly changing
and since we spoke like what was it like
a few months ago?
&gt;&gt; Yeah.
&gt;&gt; Seems like everything has changed and
you were mentioning before the show,
seems like 10 years have gone by in AI
land.
&gt;&gt; Exactly. In fact, I actually I don't
know if I made this prediction last
time. I expected a mythos fable moment
at the end of the year and it happened
in like what May or April I forget
exactly when. So things are definitely
happening faster than we thought.
&gt;&gt; That's amazing. Yeah. Yeah. It's really
picking up now and uh memory has reached
an all-time high. It's become extremely
expensive. I think a lot of people who
do who are deploying AI hardware are
like finding ways now to make the best
of what they've got. uh increase
utilization rates pool stuff offload to
different tiers uh whether it's other
kinds of RAM not just HBM or go to NAND
flash so there are so many techniques
that have sprouted up in a matter of
mere months because we we have to do
something about the memory situation
exactly I would say even one of the I
wouldn't say it's the simplest but one
of the most obvious and coar grain
techniques in my mind has been model
routing if you're not always using the
most memory hungry model for every
prompt, especially in an agent swarm
with hundreds or thousands of turns. Uh,
and you're intelligently routing
requests to medium and small models.
Implicitly there you've got lower memory
requirements. So that's kind of an easy
button if you will for reducing memory
and aggregate. But then we get obviously
much more specific here with regards to
each model's memory requirements,
working memory, KB cache and so forth.
&gt;&gt; Yeah, [snorts] exactly. So, so that's
what we were talking about in some sense
last time because the KV cache started
getting so big when the agents arrived
on the scene that uh it you couldn't
keep it on expensive HBM because it's a
very limited resource and it has to be
preserved and used judiciously. So there
was like a lot of talk about offloading
to DRM. Um and then as agents started
working more and more and having greater
context length they started talking
about offloading to context memory
storage which is what was this whole
rack which Nvidia calls what was that
STX right? Uh yeah the new storage
platform is STX. The biggest use case of
STX is going to be context memory
storage CMX context memory extensions in
Nvidia terminology. Uh and that is yeah
within the STX hardware framework.
Hardware and software framework.
&gt;&gt; Awesome. Uh so yeah I know Weta has uh
hardware we spoke about this last time
too where uh you have got WA's AMG uh
which provides really a lot of storage
directly to the GPU via a very fast
network connection and uh it occupies uh
it the the speed that you get out of it
is like uh really good comparable to uh
something like uh faster than NAND but
slower than DRAM, right? So that that's
where we were.
&gt;&gt; Let's let's let's double click on that
because it's actually uh different than
that even. So uh the standard
positioning is you can be faster than
NAND with higher bandwidth connections,
you know, faster than local storage
effectively. Uh but in a standard
hierarchy, you could slot in as slower
than DRAM. However, depending on your
architecture and whether you can take
advantage of the full line rate network
performance or something like NVLink the
way Weta does, you can be faster than
DRAM. So if you actually take a look at
the number of you know PCI lanes that we
have in these wonderful scaleup domains
with NVLink on Nvidia servers in
particular, there are far more PCI lanes
like 128 I think in NVLink than there
are PCI lanes from the CPU to DRAM which
is only 32 on the 32 on the motherboard.
So there's more. This is one of the cool
architectural
uh I I would guess leverage points of WA
is we recognized at company founding
inception about 13 14 years ago for high
performance computing which is what AI
factories are there is more bandwidth on
the network than the motherboard and PCI
is a bottleneck it's not an accelerant
and this is still something that I find
a lot of systems architects and
developers struggle with they assume
nothing is [clears throat] faster than
what I can access on on a motherboard
and they design entire database
hierarchies, entire application, you
know, latency profiles based on that
invalid assumption today because the
network is faster than a motherboard in
a GPU network and a high performance
network. And so yes, I think uh the
memory taring can have whatever you
connect on the other side of that high
high bandwidth network, the an NVLink
style network, you know, east west
compute memory network, nickel network,
it goes by many names. whatever you
connect on the other side of that can be
faster than DRAM and the way Weta
connects uh optionally we don't require
that network but we certainly leverage
it maximally uh but the way WA connects
we're faster than DRAM on a raw
bandwidth basis another confusing part
is the way CPU and GPU memory transfers
KV transfers for example and others
operate on most of these servers GPU
servers uh depending on a gener
generation. Hopper has something called
a bounce buffer between the GPU and the
CPU. Uh Blackwell introduced especially
with Grace Blackwell more sophisticated
chip-to-chip interconnects that are
faster between GPU and CPU transfers.
Ver Rubin yet again continues to advance
that with higher bandwidth, you know,
far more scalable memory transfers
between GPUs and CPUs, but you can still
be faster than DRAM on these servers
because of NVLink. There's a ratio in
terms of NVLink bandwidth relative to
memory bandwidth relative to front-end
network bandwidth. And as long as you
can be line rate on NVLink, uh you can
be faster than DRAM, which is
counterintuitive, but the math math is
math. It proves out.
&gt;&gt; That's awesome. Okay, that's great
because uh just to recap what what we
are doing is that the line the
networking on modern hardware is so fast
that when you hook up even storage using
that you can get bandwidths that are
faster than DRAM because motherboards
aren't the fastest and that is an
assumption that a lot of people are
making right now but instead if you view
the NV NV link as like a very high
bandwidth interconnect, you can actually
bring storage to operate with much
higher capacity but at speeds that are
better than DRAM speeds. Yeah. And these
networks are really critical right now.
We we've seen a rise in interest in
networks not just with co- package
optics CPO but what Google does with
their Taurus network AMD obviously with
Pensando and that line of of networking
that they're going to continue to
improve with Helios. Uh but just what
Melanox has done with NVLink has been
wonderful. Uh and it's not just NVLink,
right? Melanox offers CX7, CX8, CX9
network adapters, Bluefield 3es and
fours. There's multiple varieties of
Bluefield 4s and so we're not picky at
least at WKA with regards to where the
bandwidth comes from. As long as systems
architects configure the bandwidth they
want for the memory tiering they want,
Wacka can support it and uh and continue
to deliver you know these these radical
economic benefits in terms of more
tokens per second, more concurrent users
per second which is really hitting the
market sweet spot right now of agent
swarms.
&gt;&gt; Awesome. Yeah. So since we last spoke
like WA right now is shouldn't be viewed
so much as like a storage company
anymore because in the AI era uh because
of what solutions WA provides. I think
it's far more than that. We were
speaking a little bit about it before
the show. Do you want to double click a
little bit more into why WA should be
seen more as a memory company and a
company that does AI data infrastructure
instead?
&gt;&gt; Yeah, very much. you know, two of sort
of our our industry partners, if you
will. One is Grock with a Q that Nvidia
Aqui hired last December for $20 billion
in a non-exclusive license to their
technology and most of their founders
and engineers. And then of course a very
uh very popular and successful Cerebrus
IPO uh were clear indicators that uh the
inference market the inference
infrastructure market is very distinct
you know very different than the
training market that Nvidia dominates
with GPUs and even Google themselves for
me for some reason this is like the
clearest example Google has had seven
generations of TPUs that were applied
both to training and inference right in
radically different markets back Then
when you know TPU 1 2 3 etc through 7
was released with TPU8 which they uh
announced just a few months ago they
were very explicitly saying there is now
a TPU8 for training but there's a
completely different TPU8 for inference.
So that's just another example that you
know uh inference is different inference
infrastructure is different. It's great
when you can leverage you know the same
infrastructure for training and
inference. There's nothing wrong with
that, but understand that you know
whether it's really cool companies
coming back out of stealth like etched
you know or or Cerebrus or all sorts of
other LPU based uh you know ASICbased
SRAMM based companies inference will
continue to diversify in terms of
infrastructure and diversify away from
training. So Weta is very much following
in that trend. Weta has a great legacy
of high performance computing, HPC
storage. But the new tagline for the
company data and and memory
infrastructure reflects the fact that at
its first principles raw basis inference
is not storage centric. Inference is a
little bit compute ccentric as we know
for prefill and extremely memory bound
for decode and feed forward and so
forth. And that's that's really where
the Weta augmented memory grid product
line fits in is it's very much you can
use it as an inferenceonly product
without any WA storage whatsoever. Uh it
just happens to be backed by NAND at the
bandwidth of memory and as we just
discussed when that uh when that
particular context memory network
happens to be large then it's actually
more bandwidth than DRAM.
&gt;&gt; Uh yeah that's awesome. So uh depending
on the kind of hardware that is running
now you mentioned that cerebrus is one
uh and the whole inference landscape is
like really seems like there's no one
right way to do inference you could run
it all on SRAMM you could run it uh with
like LPUs which is also SRAMM then you
could uh [clears throat] run it with a
combination of HBM
and SRAMM or if you look at Samanova
they use all three so it's like really
breaking up all over the place. And uh
so how do all these compare like in
terms of performance or where does
storage play a role into this whole
thing?
&gt;&gt; So there's a memory hierarchy and it's
interesting now because when we last
talked about this memory hierarchy, it's
funny we we talk about it as if it's
been around forever, but it's really
only about a year old.
&gt;&gt; But a fairly wellestablished four tier
hierarchy that's going to have to change
now. And Nvidia's Dynamo team has done a
really good job of documenting this.
They even label it G1, the top tier in
the memory hierarchy is for high
bandwidth memory. G2 is for CPU DRAM,
but it also goes by LPDDR and SOCAM, but
it's, you know, for the uninitiated,
it's all the same thing. Uh, and then,
uh, so that's G2. G3 is what's called
local storage, and sometimes it's called
like the rack SSD that's in the servers.
And then the G4 tier is remote storage.
often it's NFS or or S3 type storage
layers. Uh and the one thing to really
not maybe confuse about this memory
hierarchy is there's no smooth
graduation from HBM to DRAM to storage
local or remote storage. These are very
very rough sort of jagged transitions
almost a grand canyon sometimes between
them because we're talking about orders
of magnitude higher latency between
those those memory tiers orders of
magnitude different bandwidth between
those memory tiers and you very quickly
reach these cliffs where um you know if
you're okay providing one token or 10
tokens per second to a user and you're
okay with latencies time to first token
of like 10 seconds and endto-end latency
of hours where they should be minutes
then you don't have a problem. But in
the real world no one tolerates you know
five or 10 tokens per second output kind
of the human eye depends human attention
span demands about 35 to 50 tokens per
second of output minimum and agents of
course at machine speed will take
thousands of tokens per second of output
in a multi-turn agent swarm. So, you
know, SLOs's, service level objectives
matter. And that's where we quickly find
right now that um even though there's a
lot of vendors talking about memory
tiering, including NAND and storage in
the KV cache hierarchy, it's kind of
irrelevant. Uh most of the benchmarks we
see out there today that include storage
in the KV cache taring hierarchy are
workloads that you could just run on a
on a DGX Spark or a Mac Studio today.
You don't even need a big server to run
some of these smaller models with small
context windows and uh and you know
single turn chat sessions or two to
three turn agent sessions that are not
representative of reality when you're
running real world workloads today
and uh semi analysis is actually working
on updates to inference x that they've
nicknamed agent x after my suggestion
actually um so uh agent x when it comes
out soon I'm not going to steal thunder.
But when that comes out soon, that's
going to reflect something called an
input sequence length, an ISL, which is
the context window of much larger than
8K, which has been the the the the limit
in the past. Hundreds of K. you know
they themselves have published uh
analysis of the fact that I think the
median traces for coding agents now are
two 300k tokens because of course we're
in the era since we last spoke of
million you know token context windows
instead of 100k or 200k token context
window limits so when you reflect the
reality of large models trillion
parameter models or models in that class
you know minia max is in that class even
though it's not quite a trillion
parameters but Kimmy is in GLM 5.2 into
the new hotness is and so forth. When
you reflect large models with large
multi-turn sessions with high
concurrency the way you know cloud code,
open code, codeex, actual pi, you know,
Hermes, open claw, actual agents work,
then you end up with a radically
different workload profile. Uh and on
the one hand, uh the models have gotten
so much better in terms of KV cache
consumption individually, right? uh I
use a number I think I remember of for
every 100k tokens with without optimized
compression like turbo quant without
optimized compression like sliding
window attention and others from
deepseek v4
&gt;&gt; you are up to 50 gigabytes of KV cache
usage for that 100k tokens that's been
reduced on a unit basis right now with
turbo with optimizations from deepseek
and others
&gt;&gt; uh to about five five gig of instead of
50 gig so that 90% reduction is great.
But what's happened on the other side?
Context windows 10xed and then agents
forms 10xed, you know, or 100xed the
number of concurrent sessions. Uh, and
on and on and on, we've gone multimodal.
Um, and so the the net effect we always
seem to see is that for pretty much
every 100x reduction in unit KV cache
size, there's a 10,000x increase in
consumption of KV cash.
&gt;&gt; Yeah. So, we're always looking about
that 100x more uh token volume and it's
reflected in the in the pricing push
back we're seeing by enterprises today.
Maybe they're not paying 100x times more
than they expected, but they're paying a
lot more than they expected because of
that token volume.
&gt;&gt; Yeah. Yeah. So, this is this is great,
right? Because clearly KVach
optimizations are on on the way like
Turbo Quant was one which scared uh the
daylights out of the market. Everybody
thought like memory is dead, HBM is
dead, everything's dead. But it turns
out that the quantization
u is a good thing because we we only
need like you said one10enth or 90%
lower KV cache storage for 100k tokens.
So 100k tokens was taking 50 GB. Now it
takes 5 GB. But this is great because
which means with our existing models, we
can run uh far more agents and do a lot
more work. And so the demand really
never went away. In fact, it got more,
right? It increased. Yeah. In fact, that
that it's you can almost make a meme out
of this that 50 gig that went down to 5
gig went right back up to 50 gig because
the context window size went from 100K
to a million. So there give and take
here and the net result is just always
more memory demand.
&gt;&gt; So just because KV cache is being
compressed like this, do you see that
it's going to continue to be so? Do you
think that we'll go to like maybe one
one gig per 100k tokens in the future?
And what does that mean for KV cache?
Because if you say like it it we dropped
uh usage by quantization techniques and
then we brought it back up because of
like agents. I guess we don't have a net
increase. Is that something that the
memory and the storage industry should
worry about? Because uh I don't know if
the increase in the usage is exceeding
the benefit coming in from the
quantization.
&gt;&gt; That cliche this time it's different
applies here too, right? Every time
there's this massive new innovation in
in KV cache compression,
&gt;&gt; uh it's not different. It just jeans
paradox keeps kicking in over and over
again and we're seeing that. Oh, you
know that higher increase in demand
every time there's a reduction in in
unit, you know, consumption. And so for
me, uh, let's look at context windows.
We're not stopping at 1 million. It
won't be long before we're at two and
five and and 10 million maybe by the end
of this year.
&gt;&gt; Everybody wants more context.
&gt;&gt; And, uh, we're going again longer
horizon in our agents. Uh, we're we're
giving agents far more ambitious goals,
being encouraged to by the agent and
model providers. The goals now span
hours and days. Soon I think some agents
will run weeks quite regularly. In fact,
for cyber security, which we can get
into, they run forever, right? You've
got to run the security operation center
persistent blue agent swarms forever
now.
&gt;&gt; So we're seeing longer multi-turn
horizons. Of course, we're seeing more
parallelism, more concurrent subtasks.
Cloud workflows was one sort of feature
introduction that became very popular to
just solve a problem in parallel 10
times faster. And uh and then again
we're going multimodal. So it's not just
language but we're inserting more video
and audio frames and image frames into
these agents. Uh and it all just results
in a continuous explosion of of overall
token demand and overall KV cash
consumption. [snorts]
&gt;&gt; Yeah, that's awesome. Okay. So the now
that we are we've established that this
is only going to get more from here. So
NAND and DRAM or whatever like form you
would want to look at it as pool not
pulled we're going to need more of this
because there is we're only going to run
more of these things. So we're going to
need more. So that doesn't spell any
decline or leveling off uh in the near
term because context windows are going
to get longer, agents are going to run
longer and more agents are going to run
per task because you can like have
parallel ones run. But I think one
interesting thing that you mentioned
earlier was like Deepseek's
optimizations because uh when DeepSeek
V4 came out there was a lot of emphasis
on uh SSD first approach to inferencing
which I think um really helped in terms
of their token pricing especially when
you end up hitting cash and they showed
that for some workloads you could hit
like 95% cash hits and what happens then
is that as long as you keep hitting KV
cache uh you already have the tokens
stored stored in a in a high bandwidth
the network connection to an SSD which
means now you can uh basically get like
free it's free now because they their
token pricing is so low for cash hits uh
it's it's insane like how is this
playing out into like other models or
are other models also hitting cash hits
at this level or h what do you think of
that?
&gt;&gt; Yeah, I'm so on the one hand I'm glad
you noticed that because we really want
to emphasize this key point now. Uh the
majority of token volume is agent swarms
by far 80 90% it's no longer chat
sessions. So chat sessions are almost
you know irrelevant to the conversation
from an infrastructure perspective
&gt;&gt; and um and agents uh it's interesting
even uh the sonnet 5 announcement just
the other day right that everyone looked
even anthropic interestingly enough said
here's the new pricing for input tokens
and here's a new pricing for output
tokens and it's a promotional price and
the reason why I don't even quote the
numbers it's really irrelevant because
of all the the the tokens used by agents
most of of them are cash read tokens and
some of them with anthropics particular
you know um unique uh pricing models you
have to pay for cash rights as well to
benefit from cash reads but we should
only be talking about cash read pricing
the the other pricing is a rounding
error and Deepseek's pricing reflects
that right they're dramatically new you
know ex inserting two zeros right
basically after the decimal point uh for
price per million cash tokens
&gt;&gt; really is a shock to the industry, not
so much the memory industry, it's a
shock to the other models and the other
inference providers. But the very
important asterisk there is that pricing
is only available out of China, right?
You have to use DeepSeek hosted. You
know, the rumor is I think a Mongolian
data center with very very low energy
costs. but also some secret sauce that
that DeepSeek has with regards to how
they've integrated version 4 flash and
pro with the uh you know uh FA highf
flyier file system the 3FS file system
parts of which is open source they
famously open sourced that last year and
wrote some wonderful papers and blogs
about it curiously unless I've missed
something they haven't updated those
blogs with what what definitely are some
new innovations and improvements that
factor into that that dramatic ically
low pricing. The net of it though, um I
think VentureB did some math uh which I
was quoted on earlier on is it's about
87 times lower cash read pricing from
China than the same model V4 Pro or V4
flash hosted in Singapore or hosted in
the US or Europe. And so the real
conversation is yes, Deep Seek has
completely set the bar for global
pricing for people that are able to
inference out of China, but for people
that can't inference out of China, uh
it's still by far the best pricing, but
there's a massive margin opportunity for
open weights inference providers to
differentiate on cash read pricing
because you you may not be able to match
Deep Seek's subsidized pricing, but you
can still leverage their innovations,
their sliding window attention, hybrid
compressor, attention, HCA and so forth,
you can still leverage those innovations
and offer very important uh reductions
in token cash read pricing and really
drive effective you know aggregate agent
pricing down because that that is the
one pricing metrics that dominates you
know the cost of agents.
&gt;&gt; Yeah. Uh so I have like a couple of
questions on this one. The first one is
why is it I it's news to me that that so
that pricing comes only out of China. So
if I run a DeepSseek model out of I
don't know open router I don't have that
pricing. Open router is wonderful
because it shows you the difference,
right? In fact, for some reason, I don't
even know exactly what this signifies,
but there's a little um a little slider
button you have to slide to say show
ignored. And I'm not exactly sure why
they label it button that the button
that way, but when you click on that, it
does expose the deepseek pricing out of
China. And then you can compare in fact
your agent of course your Hermes your
open Cly agent can compare uh side by
side in real time the pricing for the
exact same model the exact same input
pricing the exact same output pricing
the exact same cash read pricing and I
should double check because I I tend to
to stand that open router site quite a
bit daily. I should check whether
there's more and more cash right pricing
beginning to appear because I know for
some models it has and I it escapes me
whether it's appeared for deepseek
providers as well but you're going to
see some providers now differentiate not
just on cash read pricing which is a
major point of differentiation but also
on cash write pricing.
&gt;&gt; Okay. Uh so on term in terms of like
cache read in what the real workloads
that we're running today it could be
like agent work agent workloads right
because like you were saying any other
kind of workloads like chatting and
typing in you know uh on the chat window
is not is a negligible portion of the
inference market today. So let's just
talk aentic workloads. uh how does
somebody uh make sure that they have a
cash hit rate of I don't know 95%
because that will drive the pricing down
enormously
uh and create meaningful differentiation
like you were saying and where is the
industry right now in terms of cash hit
rates?
&gt;&gt; Yeah, you know what we could spend a
whole pod just on this question because
it's um it's very opaque
&gt;&gt; and and a little bit confusing. So let
me uh let me go through this because
this comes up a lot in other pods as
well. When you look at your um agent
dashboard, your claud code or just your
claude dashboard if you have both code
and co-work and and other clawed
products or open claw, pick your
dashboard, right? It'll have a cash hit
rate that is a logical cash hit rate
that that reflects the cachability of
the tokens in your agent swarms. And
that is often very very high. like every
agent pretty much has a cachability of
95%. Right? Because you are reusing a
lot of context for agents especially
agent swarms and so forth. However, the
providers, you know, the the actual cash
hit rate from the provider is not one to
one the cachability of your tokens,
right? The effective cash hit rate is
very much a function of the memory tiers
you have and everyone or by and large,
you know, uh most people in the first
quarter of this year and some in the
second quarter have had very finite
fixed memory tiers. There's only so much
HBM that comes packaged on your GPUs.
There's only so much of the URM that's
on the GPU servers. And as I mentioned
before, you can try and add storage
tiers and KV offloading to storage, but
they ruin your SLOs's. So they're it's
really not that common in production for
the popular models and popular token
consumption. M
&gt;&gt; uh and so the way to really understand
where where people actually have true
effective cash rate rates that are as
high maybe not as high as the logical
cash rates but close is in the pricing.
So open router again is a great proxy
for that because it's the only way to
introduce transparency to the real world
cash hit rates and even open router
themselves they publish actual by
provider by model by provider they
publish some cash hit rates and I like
them because if you look every few
minutes they do change right based on
the actual token traffic of the moment.
uh but even with some of the numbers I
see there, I don't think there's a real
effective infrastructure, hardware,
memory, cache rates. There's some blend,
but nevertheless, they're much closer
than what your own your own agent
dashboard reflects. And uh and yes, for
me, I like to joke now we're we're
seeing a lot of, you know, benchmaxing
in a lot of the models right now. You
know, for example, like SWE bench
everyone sort of trains for. So, it's no
longer that relevant to benchmark, but
deep is still a good benchmark.
&gt;&gt; Uh we see the same thing obviously when
when when vendors sort of, you know,
benchmark their KV offloading solutions.
There's not a lot of truth left in
benchmarking. So, my personal belief is
that profit and loss, right, pricing,
transparent pricing is the ultimate
benchmark. And you're going to see WA be
more explicit in that space to do that,
right? We we want to continue to prove
out our own advantages and we think that
you know real world metrics reflected by
pricing uh is probably the best way to
actually benchmark a solution now as
opposed to something in a lab.
&gt;&gt; Uh you also mentioned that deepseek's
sliding window attention is something
really to look into. Uh what's what's
unique about that uh sliding window
attention in deepseek?
It's actually uh if you've ever paid
attention to you know where compression
of files in general has evolved from
simple like PKzip compression or simple
blockbased dduplication towards the
similarity hashing algorithms and a
combination of you know sort of global
similarity and global hashing and local
hashing. The same thing is happening now
with KV cache. The same concepts are
being introduced at the token at the
attention level and sliding window is
just that. It's a way to take a look at
just, you know, the more recent tokens
and and and compress them as much as
possible and just assume the tokens that
your particular attention head hasn't
paid much attention to recently aren't
as relevant, aren't as compressible. And
it's it's just cumulative, right? I
think if you count it, there's a
formally about five different attention
mechanisms in Deepseek V4 now, all
simultaneously applied. And each one
specializes in, you know, short-term
compression, long-term compression, you
know, uh, context relevant compression
and so forth. And the net result is that
impressive 90% real world reduction in
KV cache usage per request. But again,
the requests now are just coming faster
and bigger. So it's kind of uh necessary
to support. In fact, I think the reason
why they continue to innovate so
aggressively on KV cache consumption is
they want to support million token
context windows and soon two and five
and 10 and the only way to do that
effectively is to keep being more and
more efficient, intelligent, current if
you will on how you consume KVach.
&gt;&gt; Okay. Yeah. Yeah. So uh deepseek what it
does the sliding window attention idea
is that
&gt;&gt; you just keep the window of attention to
what is most relevant right now and keep
discarding what stuff is isn't relevant
anymore and that saves you
&gt;&gt; K cash almost assume what's what's been
attended to before that's not being
attended to now has already been
compressed to some extent. So now let's
really be aggressive on what we're
tending to right now and and see where
the opportunities to compress token
memory, you know, is token attention in
KV caches.
&gt;&gt; Okay. In terms of just like NAND flash
storage even, I wrote an article
recently about uh what it really takes
for an SSD to be like AI ready. Like
SSDs in the past uh were meant for a
different use case really than what
they're being used for now.
And one theory I have which I want to
run by you is that NAND itself is now
breaking up into several tiers like we
always in the past wanted to get more
capacity out of NAND. So the industry
was like trying to go from single level
cells which has lower capacity but you
know more endurance and faster write
speeds or two going to QLC or you know
quad level cells on the other hand where
you can save you know so like basically
store four bits or 16 different states
in just like one cell. So it really
gives you a lot more capacity but
endurance is a concern and uh I'd say
it's harder to write to because you have
to make sure you can differentiate
between 16 states. How do you see these
nan tiers working out? Are single level
cells making a comeback? Uh how is that
working?
&gt;&gt; Yeah, it is making a comeback. And so uh
just like we talked about earlier uh you
know training infrastructure used
capacity NAND because you wrote a lot of
training data infrequently and you read
it very very frequently. So that was
ideal for QLC type approaches. Whereas
inference is just fundamentally
different, right? It's really
fundamentally memorycentric. So you're
really trying to make NAND appear more
like memory and a lot less like storage.
And memory doesn't care whether you
write or read at the same rate because
the assumption is there's no endurance
issue, right? There's a power issue, but
there's no endurance issue, a
persistence issue, but no endurance
issue with with with memory uh with with
memory with DRM in particular or HBM. uh
and that's not true. So this is where
nan flash struggles to act more like
true memory from a performance and a
consumption perspective as opposed to
just a capacity perspective. Again
something this is something that WA
anticipated a long time ago. Uh and so
you're seeing that largely because of
inference alone. Intel had this really
interesting technology with Micron
called Optane or 3D cross point.
&gt;&gt; It's a real shame. Oh my god. Yeah. You
know today inference is the killer app
for h for optain but it's gone now right
based on different materials phase
change memory and so forth
&gt;&gt; uh and what is tried to replace it is
SLC flash right
&gt;&gt; okay
&gt;&gt; if you have to if you can't optimize
your rights your KV cache rights
&gt;&gt; uh well enough then you have to buffer
that endurance issue that that driveware
issue with a more endurance form of nan
flash which is a single layer cell SLC
tier and sometimes that can be
complemented by QLC. So you buffer a lot
of writes in SLC and then you destage
them down to QLC later.
&gt;&gt; Again that adds complexity that adds
latency. That's no free lunch there. Uh
another thing you can do and this is
something that WA does is kind of
anticipate that you're going to write to
NAN flash a lot. You're going to read to
it a lot. Basically use NANFL flash as
opposed to just keep it for capacity.
&gt;&gt; Yeah. And in that case, yes. Um, what WC
has done is we've always advertised
rights across a whole fabric of NVMe
drives. My joke is there's no S, there's
no storage in NVMe. It's nonvile memory
express or memory extensions.
&gt;&gt; And when you treat it like a true memory
protocol and you amortize the rights
across a whole fabric of NVMe devices,
you don't need SLC. We don't have SLC,
for example, never have in Weta. we
literally can use TLC for a very high
write endurance workload like KV cache
and uh of course in in the future as
we're able to uh influence the uh the
rest of the inference stack so the
scheduling and the routing not just the
KV transfer storage layer uh we will be
adding support for QLC drives as well uh
but again we you got to be careful about
that because you don't want to break
those drives by doing unintelligent
things on scheduling rights or
unintelligent things on just routing
tokens to somewhere that needs a quick
write but is really kind of not worth
it.
&gt;&gt; So you can actually optimize uh the
controller layer and make sure that you
don't clobber the drive whether it's a
TLC or QLC drive and intelligently write
to the whole TLC/QLC array and still
keep endurance.
&gt;&gt; Exactly. This is uh something it's a
category of of storage technology called
shared everything as opposed to the
Hadoop style shared nothing
&gt;&gt; which you still see in parallel file
systems like GPFS or Luster etc. uh and
with a shared everything approach the
client if you will has global awareness
using a raph protocol of the the Q
status the work Q status there's
multiple cues in every NVME device every
SSD controller basically so when every
client has global visibility into the Q
depth of every NVMe device in a fabric
tens of thousands hundreds of hundreds
of thousands of cues on tens of
thousands of drives in a fabric then you
can treat NVMe like a cash line for DRAM
and you can be very intelligent about
where you you um you know you you shard
the rights right where you load balance
the rights very very intelligently
&gt;&gt; and at that point you don't need
expensive SLC tiers to buffer rights
you're you're not being you know
suboptimal you're not being
unintelligent or treating devices as
blunt storage devices you're really
&gt;&gt; you're digging into the devices and
you're making sure that you're you're
you're optimizing the actual underlying
NAND flash well and cooperating with the
controllers versus offloading work to
the controllers.
&gt;&gt; So you don't really see SLC as coming in
on its own tier. Maybe it's just going
to be used as a as a buffer.
&gt;&gt; Well, let me be, you know, let me
disclose here that I'm talking about how
Weta has decided to optimize flash
tiers. I think the industry needs SLC,
right?
uh the industry doesn't have our
patents, doesn't have you know our
implementation by and large uh except
for you know the server partners that we
partner with but generally uh that that
technology is not available outside of
WKA so you do need SLC there will be a
rise you know Nvidia is forecasting this
themselves even for CMX there will be a
rise in the need for SLC to buffer the
rights when you can't amortize them over
TLC uh but the the upside of that is
that if you buffer correctly to SLC, you
can still use QLC. At WKA, we're
skeptical, right? Because uh there
again, these are not capacity workloads
where you have the luxury of time to
dstage SLC to QLC. These are very
bursty, very intensive workloads that
are attempting to emulate memory. uh and
so we think that ultimately one tier
whether it's SLC or TLC is the only safe
and fast way to offload KV offload to
storage but you know the industry
there's a lot of smart engineers across
the industry and many vendors you know
the [clears throat] market will prove
what works over time we just know what
works for us right now
&gt;&gt; so in a NAND storage uh uh rack uh you
know you could amortize rights over many
drives but you also overprovision
uh like uh and with to what ratio like
if you have a 100 drives in a in a rack
and to make sure that you have the right
endurance even after amortizing over TLC
drives do you actually have 20% more
&gt;&gt; what is the
&gt;&gt; these these are tricks we can always
play right so if we don't have SLC
&gt;&gt; and economically or just supply chain
issues we need to use TLC or god forbid
today QLC only then yes you would really
have to overprovision and the the net
effect is you you would be buying you
know let's say a pabyte of storage but
only use only C 300 terabytes of like
effective or 500 terabytes of effective
capacity from that pabyte that you've
purchased and are powering
&gt;&gt; because the overprovisioning is needed
not to break those drives.
&gt;&gt; Yeah. So it could be even a two or 3 to
one overprovisioning.
&gt;&gt; Yeah. It's it's it's tough you know
because these are extreme workloads.
There's there's nothing gentle about
emulating memory with NVMe with with nan
flash, right? It's a very intense
workload.
&gt;&gt; Yeah. Yeah. Oh, that's great insight.
That's uh really great insight for me uh
on how SLC and you know TLC tiers work
and what the trade-offs are. Uh so I I
definitely has added to my uh body of
knowledge today. So
&gt;&gt; it's nuanced. That's why I said you know
we could spend a lot of time on this
alone. So
&gt;&gt; yeah yeah yeah we should move on. I
think like a lot of interest in the
market right now is for high bandwidth
flash because now if people can put in u
you know flash right next to
uh a GPU and have it store some stuff um
it would be a useful thing I would
imagine. So my two questions I think
around that are does HBF
use SLC like single layer cells that's
one thing and secondly what are really
the use cases for this thing?
&gt;&gt; Yeah great question I think uh HBF will
probably have to use SLC in in in the
most common configuration for the
reasons we just discussed.
&gt;&gt; It really is trying to be a great
offload tier. Uh it's trying in fact in
many cases to replace DRAM. Right.
&gt;&gt; Right. compliment high bandwidth memory
directly. Uh for me, it's always come
down to a packaging decision. You know,
I think SKH Highex has been public about
the fact that they want to package it,
you know, directly on the GPU package
itself. They don't want to go through
buses. They don't want to go through
networks. They want it to be really
tightly bound to GPUs. I think it's a
great vision. I haven't seen any GPU
vendor directly commit to that yet or
adopt that yet. But I think um in the
future, maybe 2028, I think we'll see
that. Uh but there's other vendors that
I can't discuss and NDA that are
packaging it differently uh on a PCI
card for example and not even packaging
it with GPUs but with AS6 you know
nonGPU accelerators. So there's going to
be different packaging form factors,
&gt;&gt; but ultimately I think it's a necessary
thing um because the opportunity
&gt;&gt; to get this right, the opportunity to
optimize the KV transfer layer, the
opportunity to schedule correctly, it
was really acquisition I think Qualcomm
of modular right and uh basically yeah
and be able to get that compiler
expertise. uh what NVIDIA aqua hired
with Grock was a lot of compiler
expertise from the TPU team over at
Google. That is going to be more
important over time to making HBF really
usable because as we recompile models to
understand HBM and HBF tiers and maybe
bypass you know this is a prediction we
have inside WA engineering bypass DRM
tiers altogether because you can get a
lot of bandwidth out of NVMe flash you
know uh NVME uh sorry out of nan flash
devices over NVME or other protocols or
without NVM DME but just nan flash. Uh
there are optimizations possible now and
there's definitely a trillion dollars of
opportunity that encourages those
optimizations between HBM and HBF with
raw nan flash andor NVMe. You can always
replace drives if you can run that
bandwidth over a high-speed network and
NVME drives and like we spoke about
overprovisioning and if something dies
you change it out or whatever. HPF I
don't know the one thing that always is
on my mind is it is NAND flash after all
and it will even if it's SLC it
ultimately has an endurance uh to it you
can't change it out if it's packaged
next to the ASIC or GPU
&gt;&gt; I agree
&gt;&gt; so is that like something that's going
to play out or the lifetime of this
thing is I don't know 50 years doesn't
matter we probably could throw the chip
away by then anyway
&gt;&gt; you've already done a good job in
covering This is a bag of tricks
engineers are throwing to mitigate this
problem. It's not one one solution or
one work around. Okay,
&gt;&gt; there's overprovisioning is one of the
tricks for sure.
&gt;&gt; Uh then again there's proper
amortization just at the storage at the
NVMe layer, NVMe fabric layer. Then
there's very explicit scheduling at the
inference at inference time but also
very explicit scheduling at rec you know
model recompilation time and and very
intelligent token routing inside the
level and even just at the gross model
level as well.
&gt;&gt; Okay. Okay. So you could engineer the
whole thing to a level that this is not
really a problem uh and you can still
use it. Not only can you do that, you
know, I've already seen anecdotes of
people applying fable, right, to very
complex engineering problems and seeing,
you know, months worth of sophisticated
systems engineering completed in four
hours. So one optimistic scenario is
that these agent harnesses and the eval
loops, the quality eval loops and so
forth, the judge judgment models and of
course the guardrail loops and the
guardrail tokens. When you package that
all together, some of these really deep
tech engineering advances can happen
much faster. But ironically, we need
more engineering in the harness to make
sure they happen reliably and safely.
&gt;&gt; Okay, that's amazing. Yeah, so much
stuff is happening that like we it's
really interesting to see how all this
plays out. So that's that's the whole
fun of this thing. And the one other
thing that has recently cropped up is uh
and I know like like we spoke about this
last time and uh um you had like ideas
around this that I want to see if it has
evolved or changed ever since is the use
of like CXL.
There's a lot of talk about using CXL
now because some of the RAM DRAM isn't
really being used on every server. I
think maybe like 50% is being used. So,
because memory is so expensive, uh even
Google has had a change of heart it
looks like to actually start using CXL
and reclaim some of the unused DRAM. Uh
what do you think like is CXL a thing
now or?
&gt;&gt; So, CXL has a lot of fans and I was one
of them 10 years ago.
uh I'm not a fan anymore, right? And
it's not because I don't like the
technology. It's because in the real
world there's alternatives. And so um
you know, personally, I think Melanox
and of course Nvidia's acquisition and
really great execution of scale up
domains kind of killed CXL in one sense.
the ability to have this great NVLink
style network and have it used for
memory, have it used, you know, um for
high bandwidth as well as regular DRAM
memory uh has been has been, you know, a
real, you know, glass ceiling or or
concrete ceiling really for CXL growth,
market growth. There's been less and
less need. Then you've got Rocky, right?
RDMA over Ethernet. Uh and you never bet
against Ethernet in this industry,
right? So the challenge XL has is
another bus. It's another bus you have
to engineer. It's another bus you have
to debug. It's another bus you have to
maintain and power. And it's not that in
isolation it's bad. And again, it's got
a great killer app today of of
utilizing, you know, this really
precious underutilized resource in some
cases of DRAM. But uh in the context of
real world alternatives, I'm just
pessimistic about the future of CXL. Uh
largely because again I'm I'm biased.
I'm able to leverage things like Rocky
or NVLink over Infiniband and deliver
better than CXL performance with NAND
flash economics cost of goods and
capacities. So it's one thing to pull
underutilized terabytes of DRAM. It's
another thing to pull pabytes and
exabytes of NAND flash at the same or
better performance. Right. And
&gt;&gt; yeah, won't a faster network bandwidth
also benefit CXL like it does?
The first principles are simple until
you have to engineer the real world
issues into it. But uh yeah, the first
principles are you know more bandwidth
is good. And so if you can have uh
faster than PCI bandwidth
&gt;&gt; to a pool of DRAM
&gt;&gt; as Google discovered there's benefits to
that. It's just that uh if if there
really were benefits to that, I think
it's you'd have seen it in Blackwell,
you'd have seen it in Ver Rubin from
Nvidia or in Helios from AMD or even in
Fineman, you know, the the the next
generation from Nvidia that's already
pre-announced and you haven't seen it,
right?
&gt;&gt; And and you haven't seen it as a
standard super micro offering and you
haven't seen it as a standard Dell or
HPE or Lenovo offering and so I think
it's that absence that speaks volumes,
right? Uh there there definitely are use
cases for it but for some reason it
hasn't broken out into mainstream.
&gt;&gt; Yeah. Yeah. Yet probably seems like uh
&gt;&gt; Yeah. It seems like the the shortage of
HBM is now causing some players like
Google to actually like consider it now
because it's just like capacity issues
are pushing uh you know hardware makers
towards solutions they probably didn't
consider before. So yeah, that's another
interesting thing to see how it'll play
out cuz you're right like so all this
time it hasn't been in there. There's a
reason for that, right?
&gt;&gt; There's a reason for that and I think
there's one important hint, right? So it
was reported I think by semi analysis
about two or three weeks ago that Nvidia
changed the bomb on Ver Rubin
&gt;&gt; and they cut the actual amount of DRAM
in half either from two four to two or
three to one and a half depending on the
model. But that's a clear indicator that
a DRAM has gotten too expensive and b
Nvidia is projecting with CMX solutions
in the marketplace from a number of
vendors including WA that there will be
less need for DRM for inference and uh
and so you're seeing that you know
people are are applying solutions to
this problem and it's not always just
pooling it better it's just reducing it
overall.
&gt;&gt; Yeah. Yeah. Yeah. That's a part of what
we spoke about in the beginning, right?
Like you could make optimizations to the
algorithm. You could use sliding window.
You could do whole lot of different
things uh that uh you know maybe uses
less memory overall going forward rather
than just use existing architectures but
start pooling stuff together. So yeah,
you know, it could go either way. If we
find better algorithms then we probably
don't need to pull it. Could be.
&gt;&gt; Yeah. Yeah. That's that's I think the
the prediction we're making.
&gt;&gt; Yeah. Speaking of better algorithms,
what do you uh what's your take on AMD's
uh MEX acquisition? Uh and for people
who may not have heard of this uh Next
is essentially a software company that
uh find found a way to optimize the use
of DAM by uh dynamically offloading all
the unused parts of DRAM to NAND flash
and then uh using AI to predict when
that same information is going to be
needed back in the DAM and preemptively
moving it back before the GPU even
notices it's gone. Right. So, it looks
like it's it's a cool way to use NAND,
but what what's what's your uh
engineering interpretation of what's
going on?
&gt;&gt; That was a fun one to review because I
wasn't familiar with MEX beforehand, but
it was clear in reviewing their use
cases pre-acquisition and the initial
positioning postacquisition is it's it's
AI technology. It's machine learning
specifically small language models and
small you know neural networks in
optimizing cache you know caching
algorithms and and being more
semantically aware than just le recently
used or so forth simplistic uristics. So
it's it's a the application of machine
learning and deep learning into caching
algorithms but the actual use case is
ironically enough not yet for KV cache
offloading. it has potential to be very
good there.
&gt;&gt; We've seen even um you know things like
um you know popular you know inmemory
databases Reddus and so forth uh
implement algorithms that you know
aggressively dstage DAMP and nan flash
and so forth and and retrieve it back
and reddus does position that for KV
cache offloading as well. So I think
it's an active space. Uh but right now I
think you know the AMD initially is
targeting scientific computing. So
whether it's life sciences, whether it's
Monte Carlo simulations and other kinds
of you know seismic analysis, weather
analysis, those are the kinds of
applications that that technology has
proven itself in and it we may see it
happen you know we may see it appear in
KV cache offloading as well.
&gt;&gt; Nice. Yeah, I I thought it was a
interesting use of the predictive nature
of an LLM because uh if you can predict
what the next word is, why why not use
it to predict what the next uh page of
memory is required and quickly pull it
from D from flash to DM. I I don't know
how real practical or useful it is
&gt;&gt; but I found the right idea was
interesting. Yeah,
&gt;&gt; I think your instinct is right. you know
why why has cursor customized you know
Kimmyk 2.5 it's a composer is many
companies are realizing now that the the
u the the bar towards being able to
train your own model has come down it's
a much more accessible thing for many
companies right now you don't need
million-dollar ML researchers to train
your own models anymore and when you can
customize a model for your domain it
actually doesn't have to be an LLM at
all it can be an ML it can just be a a
very tight neural network it can be
inferenced on a CPU. It can be
inferenced on a small low power CPU if
the model is really domain specific
&gt;&gt; and it's just a neural network at that
point. It's not a large language model.
And there's I think going to be again
another Cambrian explosion of use cases
and applications for clever small models
that do things that uristics, you know,
uh peaked at and and can no longer
optimize or improve.
&gt;&gt; Yeah. Do you think that this uh use case
is basically physical AI and robotics uh
where you could have those sensors at
the edge like process very specific
amounts of information? It's only one
kind of information from a sensor,
right? So it's not like a large model
you need. So is that is that a useful
use case you think going forward?
&gt;&gt; 100%. I think it's probably going to be
the reference architecture for robotics
and edge inference as we don't need
large language models. there will be
some aggressive you know cloud
connection whether it's through Starlink
in remote locations or just broadband if
you really have to you know burst to
some kind of complex decision that a
large language model has to make but you
know 90 95 maybe 99% of inference for
for robotics will be local and and
disconnected airgapped so to speak.
Yeah, that's the fact that like you
could make inference decisions at the
point of sensing uh or you know just
like put an intelligence anywhere
actually is a very very useful edge use
case.
&gt;&gt; How useful or how good that intelligence
is I think yet to be seen but in
principle you could deploy these little
models like everywhere. Yeah, the cost
of these Raspberry Pi style system on a
chip motherboards are are really
plunging and fortunately again whether
it's KV cache optimizations or just you
know small model quantization and and
just custom neural network training that
doesn't have to be a large language
model at all is intersecting really well
with really affordable you know system
on chips SOC's and yes that results in
some really interesting robotics and
drone use cases. Yeah.
&gt;&gt; Yeah. Didn't Jensen mention something
about the AI flywheel on in this
context?
&gt;&gt; Exactly. So this is a a general concept
of uh it's all about being able to
capture data domain specific data train
models and then customize that with more
either real world domain specific data
or synthetic data. Now that you have
enough real data to create useful
synthetic data and just keep iterating
on that loop of you're pushing the
frontier with big models, you're
customizing either through fine-tuning,
distilling, you know, quantizing, low
rank adapting, etc. All sorts of
customizations. You're customizing
smaller and smaller versions of those
models. you're able to maybe retrain
entire small neural networks that are
very domain specific of those models uh
and and just get more and more efficient
at processing inference, retaining some
of the new fresh data and and keeping
the flywheel going. So, it's a it's a
mix. It's definitely a whole ecosystem.
It's a thriving ecosystem of different
model types, different phases of data,
different types of data, but if you keep
the flywheel going, it stays relevant
with nature's natural entropy. So, yes.
&gt;&gt; Yeah, that's it's a fascinating idea.
Uh, since we're coming up on time, I
want to pick your brain for like one
prediction. What do you think is going
to happen in the next 12 months? What
are you most excited about? So zooming
out a bit uh again this is something
that Jensen referenced very very often
is that software is fundamentally
changing you know um a year ago we
wouldn't have predicted that all of our
engineers really would be using AI for
most of their daily work right now it
was it was heresy even a year ago uh and
so the not only the rate of change
that's happening right now but the
fundamental change in software is that
more and more software now is not
compiled and run it's basically compiled
called run and inference, right? It's
really agents now as we said being much
more intelligent in their token
consumption. We're not using Opus for
everything. We're not using GPT55i for
everything. We're definitely using now
model routing and a mixture of models
and a mixture of experts within models
right now to be very token efficient.
And what that means is now the cost of
running a software business is radically
different than before. It is a high
marginal cost. You can't just leverage
even with you know maybe KV cache is the
way to leverage but you can't just
leverage the cost of tokens across users
the way you could leverage you know
cloud instances and databases and VMs
and microVMs and and containers across
users
&gt;&gt; uh and SAS companies the reason I
believe the SAS apocalypse is real and
is a problem is that no matter how much
SAS companies figure out you know new
pricing models and new values you know
value based pricing and so forth their
opex is going through the roof.
&gt;&gt; The opex now is token opex. It's
tokconomics. It's token consumption. And
yes, all these engineering solutions we
just discussed are ways to manage those.
But if you just take a look at token
volumes on Open Router week after week
after week, it keeps rising and rising.
And we've really just barely begun
mainstream token consumption and
persistent agent swarms. uh the only way
to run a profitable gross margin
business in software will be to own more
of the token stack
&gt;&gt; and you can continue to outsource that
to an inference provider to a model
provider or you can acquire it. You can
merge with a neocloud you can merge with
a token factory
&gt;&gt; and you can essentially you know
vertically integrate more of that very
expensive token generation stack uh and
continue to run a high gross margin
software business. Oh, that's
fascinating.
&gt;&gt; The real question is with cash flows
what they are,
&gt;&gt; will SAS giants acquire Neoclouds before
neoclouds are able to acquire the SAS
giants? [laughter]
&gt;&gt; That's fascinating. You know, I always
spoke about like uh the best way for
large companies to save on token cost is
like you bring inference on premises,
right?
&gt;&gt; Exactly.
&gt;&gt; Uh so you could run that at the edge.
What you're suggesting is like one level
that concept on steroids. A big enough
software company can go acquire a
neocloud and say that this is my token
factory and now I can like there's still
a cost to run that token factory but the
tokens are yours to use. It's entirely
yours.
&gt;&gt; Now if every software big software
company starts acquiring new clouds of
some size I mean they don't have to be
like multi- gawatt data. You know, I was
predicting, you know, I made this
prediction before X acquired Cursor or
SpaceX AI acquired Cursor. I predicted,
you know, like workday or Monday.com or
something like that would merge with
like a mid-tier Neocloud. But now, of
course, first domino's fallen with with
X SpaceX AAI and Cursor and older
established SAS companies are going to
have to react as well. So yes, I think
whether the dominoes start falling in
the middle or one side or another, it's
kind of inevitable now that most SAS
companies and most neocons will have to
merge. [snorts]
&gt;&gt; That's a fascinating prediction. I would
love to see how that works out.
&gt;&gt; Yeah. Uh thanks so much, Val. Like it's
always a pleasure chatting with you.
You're like a fire hose of information
that I know I'm going to listen to this
podcast later myself as I'm reviewing
the edits and stuff and be like, "Oh my
god, I missed that when I spoke to Val."
But, you know, I hope this helps all our
viewers as well. It's really a pleasure.
&gt;&gt; Always a pleasure. We said we'd enjoy it
the next time. Last time we did it, and
I'm definitely looking forward a few
months from now from coming back. We
should come back, but well before the
end of the year because by the end of
the year again, we're going to be very
surprised by what happens.
&gt;&gt; It's an eternity. Every every 3 months
is an eternity in AI AI time. So, yeah,
we should do this more often.
&gt;&gt; 100%.
&gt;&gt; All right, guys. Uh, that's it for
today. Thanks for listening. Uh if
you're enjoying semi-doped, please share
it with your friends. And we also have a
daily newsletter on semi-doped.com
where uh we put our daily takes on the
news. It helps us keep a breast of what
is happening in this fast spa paced AI
uh landscape we are in. And it's
entirely free. So make sure to check it
out. And thanks for everyone who puts
comments on YouTube. We do read all of
them. Some of them are like really
amazing. Some of them are really funny.
We have a good laugh. But we read all
the comments even if we don't respond.
We promise and it helps us plan all the
future episodes. So definitely keep them
coming and if you can leave us a
fivestar review on the on Apple podcast,
it really helps us out. Right. Cheers
and catch you on the next
