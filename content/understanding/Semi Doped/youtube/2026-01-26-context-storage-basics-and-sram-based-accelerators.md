---
source: https://www.youtube.com/watch?v=_qYDXB_aXA0
vid: _qYDXB_aXA0
title: Context Storage Basics and SRAM-Based Accelerators
date: 2026-01-26
duration_sec: 2282
channel: Semi Doped
kind: transcript
---
I guess there's all this talk about like
agentic uh coding with uh very fast
codecs, right? Like as Salman put it,
but do they have a way to handle long
context storage with this whole
cerebrous system?
&gt;&gt; Welcome to another semi-doped podcast.
I'm Austin Lines of Chipstrap and with
me is Vic Shaker from Vick's newsletter.
Hey, what's up Vic?
&gt;&gt; Hey Austin, how's it going? It's going
&gt;&gt; I shouldn't call you I shouldn't call
you Austin. I guess you're now Tom. Do
did you see on Twitter how somebody said
you look like Tom Holland? They're like
wait why is Tom Holland speaking
semiconductor stuff? Like what's going
on? Like is everybody an AI head now?
And then I'm like
&gt;&gt; and then I looked up Tom Holland. I'm
like holy you look like him. That's
that's awesome.
&gt;&gt; I Yes. I've never gotten that. I too had
to look him up and I was like oh yeah
it's the Spider-Man guy. Cool. I'll take
it. I haven't gotten it, but famous
movie star. I'm sure he's like 10 years
younger than me, so let's go.
&gt;&gt; All right. Your friendly neighborhood
Spider-Man talking to you semi stuff
today. You know,
&gt;&gt; I liked it. I guess I need a teacher.
&gt;&gt; Let's do it.
&gt;&gt; All right. So, Vic, you wrote a post
about context, memory, storage, and I
learned a ton. It It was really good,
very in-depth, and I I actually liked
you had a lot of really cool
illustrations, but um let's start there
with our audience. So why don't you take
it from the top like what what what
should we know about context memory
storage?
&gt;&gt; Yeah. So the whole thing got started
because Nvidia at CES uh mentioned the
influence context memory storage. We
mentioned it in our podcast about Nvidia
CES also. And the whole thing is all
about having just a bunch of NVMe flash
storage in uh in a rack and then hooking
it up with like really fast networking
uh to your main GPUs and just just have
it store stuff. And it seems like this
idea is not new. You know, people have
had these
flash disc arrays in a network storage
for a very long time. But the very fact
that Jensen mentioned it in this big
forum immediately has everybody looking
up NAND and then the prices went up for
all these NAND companies. It's it's the
usual thing.
&gt;&gt; The the Midas touch.
&gt;&gt; Yeah. The the Midas touch, the Jensen
touch. Uh yeah, he does this and you
know, everybody talks about this stuff.
So I think it's important to talk about
it a little bit more than we did last
time because it unlocks a whole new era
of things we can do in AI inferencing
that just wasn't possible before right
now. So for anybody who's actually used
uh like these tools and I'm guessing
it's a lot of people at this point uh
you know I in Claude especially the more
I keep talking to Claude especially in
the opus mode which consumes a lot more
tokens pretty soon it says like that's
it this chat has now run out of like uh
full it's full or you're done with this
chat continue your conversation in a new
chat you know if you ever see that um or
more recently it has started saying hold
on I'm just compressing our chat so we
can continue talking. So what is
actually happening behind that is the
context memory is filling up like there
are only so many tokens that can be
stored and after some time something has
to be done with those tokens to continue
the conversation right or they have to
be discarded in which case you know AI
forgets the entire conversation you've
been having with it all this time which
is extremely frustrating because now
you're like so what do I have to tell
you all that stuff I just told you all
this stuff now you want me to say all
that stuff again is terrible Right? So
then you copy your original prompt and
begin it's very frustrating. Uh so the
compacting idea uh was good except that
in my own usage of claude for example uh
it it kind of forgets stuff. It gets
amnesia and it's like tells me stuff
that I've already told it before and
it's like did you forget that or or or
it tells me something I never said to it
before. Anyway, it's just messy
&gt;&gt; and All of this is because context is
running out. Okay. So what this context
memory storage solves is exactly that
uh you can actually have really long
conversations if you can store more
context right and this is getting more
and more important especially when we
are in the age of uh agentic AI and
agentic workloads especially like AI
based coding. Um, you know, there was
like a piece of news weeks ago where the
cursor CEO said that they built an
entire web browser just with like chat
GPT 5.2. They just like prompted it and
then let it run for like a whole week.
&gt;&gt; It came up with a browser. It's just
kind of fantastic.
&gt;&gt; This is wild.
&gt;&gt; Yeah. It used to take like a couple of
years before and a whole team of people
building browsers, right? you didn't see
browsers come out every day like like
when Chrome came out that was like a big
deal and then before that was I don't
even like you and I probably remember
Netscape Navigator like you know that
was like way before even Internet
Explorer so you don't have browsers
coming out every day but if AI can make
a whole browser uh with all all of all
the support possible in like a week
that's fantastic now what does it take
to run a whole AI job for a week to do
something like this you know this This
is the kind of stuff that context memory
unlocks
&gt;&gt; because it takes lots and lots of
tokens. It probably has like a big code
base that it's generating and at the end
of the day it can't store all this in
HBM, right? So, it needs to store it
this context somewhere.
&gt;&gt; Yes, we should talk about a unpack that
a little bit, right? So tokens are our
currency of AI in a sense because all
the words we put into the chat box on
LLMs are converted to numbers and that
process uh you know is the resulting
number is called a token. It's kind of
broken up in some way. Now
the question is what what does it mean
that we're running out of uh we can't
store tokens? What does that even mean?
Like are we storing everything? like
there is some nuance to what it is that
we exactly have to store, right? So, one
of the big things that is
uh selling point for a lot of LLMs is
the context window. So, when you see
like Gemini has a 1 million token
context window, what that means is that
it can take 1 million tokens together
and uh form relationships between all
those tokens. So, it knows the first
token and the million token and the
relationship between them. So that is
what we want to do. Now in the process
of generating output tokens from the
input tokens we give it through a
prompt. There's like a whole uh bunch of
calculations that happen here. And this
is essentially what the LLM transformer
is doing. And within that functionality
is something called attention. Like this
is the fundamental revolutionary concept
that Google introduced in their 2017
paper saying attention is all you need.
Attention is a mathematical formula. Uh
and the whole idea is that you calculate
a bunch of matrices, right? So it
involves a bunch of matrices called the
key and the value and the query matrix.
And then of course there are the weight
matrices. Now for every token that comes
in there there is a key value cache
sorry there is a key and value pair that
is calculated based on the model
weights. So the model weights are what
has been come you know the model weights
are basically what you get from training
and using an input token you can make a
key value pair and that is stored in
memory. Then the next token comes by,
you make another key value pair and you
add it to the first one. And you keep
for every input token, you keep adding
key value pairs to this original matrix.
And so as the context length grows, your
key value matrix grows linearly with it.
It's not a quadratic or you know cubic
or anything. It's a linear increase of
the KV matrix and that is what is called
the KV cache. This KV cache has to be
stored somewhere. Now imagine if you
have a 100 million token input window or
a billion tokens. I know I don't know
how many agents would need. If you have
a billion token uh window, you need to
have a massive KV cache stored somewhere
and it can't be in HBM. So this is why
this is where we land at what you said.
We don't just have enough HBM for this,
&gt;&gt; right?
&gt;&gt; Makes sense. Yes. So, okay, we calculate
all this key value pairs as part of the
attention, paying attention to all the
different words and the relationships
between them. And the longer the context
we have like the more useful the AI is
because we're giving it all this
reference information PDFs all you know
whatever what have you code bases entire
code bases but at some point there's too
much and this can't all fit on the HBM
on the GPU so where does it go
so HBM is on the Reuben is 288GB
okay half of that is taken up by the
model weights let's say it depends on
the model and so let's say you're left
with like I don't know 150 GB of HBM
that's not enough to store 100 billion
tokens it doesn't matter how small you
make it people have thought about ways
like with multi-headed lated attention
and grouped query attention smart people
have come up with very smart ways to
reduce the size of the key value cache
you can store but you just can't store
everything in HBM so what happens next
is that whatever spills over from HBM M
is stored in the CPU DRAM.
So we mentioned in the CES episode that
the Vera Rubin platform supports
uh 1 to 1.5TB depending on what kind of
RAM sticks you throw in there uh of DRAM
uh in the CPU. that is also
intentionally designed for longer
context storage because in the Blackwell
series you only had 480GB of DRAM
associated with the gray CPU. In the
Vera CPU you have over 1 TBTE. So you
can store a lot more context on this. So
whatever spills over from HBM goes to
DRAM. And DAM is good. It's not as good
as HBM. It's still pretty fast. So you
can get this back pretty quickly when
you need it. Now, if it doesn't fit on
DRAM of the, you know, on the on the
CPU, it goes out to the next level of
storage, which is maybe the local SSD.
The local SSD is all good, but uh you
know, when you're serving a 100 million
people, all of whom are running agentic
AI workloads, that is not going to fit
on a local SSD. So now you have to go at
scale. You need pabytes of storage in a
rack server somewhere and that is where
all your KV cache is stored. Gotcha. So
we're talking about memory hierarchies
here.
&gt;&gt; Yes, totally. And just like any other
memory hierarchy, right, you have a
latency and a throughput associated with
each one. HPM is the fastest. So if you
can get your KV cache quickly when you
need it, uh that's very good because you
can compute your output token quickly
and then you have a very low time to
first token and a high throughput of
tokens because you can keep getting KV
cache quickly. Now the farther down this
memory hierarchy you go all the way to
like network storage, uh this gets
pretty difficult to do quickly and the
time to first token and all those
metrics throughput drops. Now there are
ways uh that things have people like WA
with their augmented memory grid or even
the ICMS system the context memory
storage system that Nvidia is planning
they're all finding ways to make this
access of this data from this large
storage pool really quick and that is
where it all lies like so you have to be
able to store a lot of information but
also get it quickly.
&gt;&gt; Yes. So this reminds me if anyone has
studied CPUs and like L1, L2, L3 cache,
there's like that nice pyramid where at
the top it's SRAMM and it's like the
smallest and it's the fastest but it's
the most expensive. Then you go down a
layer and it's bigger and it's cheaper
but it takes longer to access. You go
down further all the way, you know,
SRAMM through DRAM all the way down to
SSDs and um even like cold storage. I I
saw that Nvidia put out uh a diagram
very similar. Instead of L1, L2, L3,
they called it like G1, G2, G3, you
know, probably for GPUs. Um same
concept. There's always a trade-off.
More storage and cheaper, but it's
slower to access. Now, I thought it was
interesting that uh they put G1 was uh
HPM when technically maybe there's a G0,
which is SRAMM. And I just say that
because of course they're only you know
in in Nvidia GPUs the SRAM is for like
local computations like registers but of
course there's other AI accelerators who
are using SRAMM to actually store the
weights in the activations and
presumably the KB cache as well. Um but
anyway I I just thought it was it was
interesting but but carrying on. So
you're talking about essentially um
Weta, Nvidia, others are trying to ask
how can we take like that lower tier of
storage on the pyramid and have the
benefits of cost and capacity but speed
it up. So kind of almost like move it up
the pyramid a little bit or you have a
nice diagram that where you showed this
as well. So talk a little bit more about
how to like get the benefits of the
storage but trying to speed it up so it
acts as if it was like a level higher.
So they're just these data processing
units that
uh really reduce the latency and
increase the throughput from all these
storage devices uh directly
uh to the GPU. So you can take a lot of
information and bypass all the middlemen
all so to speak uh like PCIe controllers
and all these network switches and then
directly take it straight to the GPU
using something called GPU direct
storage u so GDS. So you can just like
move large amounts of data and this will
help get it to the destination quicker.
So they're making some modifications to
the whole process to make sure that GPUs
get the information they need.
&gt;&gt; Nice. So tell me about the benefit of
this with regards to tokconomics.
&gt;&gt; Yeah, so I was looking this up recently.
Uh if you look at like Claude and go
into their API docs and look at how they
charge for tokens, they have a they have
a token system based on where the token
is in the inference uh process and so to
speak. So for so many input tokens, you
have a certain price. Uh, I think it's
like I don't know like let's say $10 for
million tokens or something like that.
Um, and then for output tokens it's
actually much more. It's more like $25
per million tokens. And then for uh cash
hits you have something like $5 per
million tokens. So what that means is
you're looking for that KV cache, but if
you
have a cash hit
uh or a cash miss, it charges you
differently. So if you want to write it
to cash, you you have to pay a certain
amount for a million tokens. So for
example, if you want to write a million
tokens to cash and hold it there for
like five minutes, it's probably going
to cost you like uh $5. Okay? Uh these
numbers are not exact. I don't but it's
on the API you can check it out and they
change too all the time. So uh if you
want to hold the same tokens for like I
don't know uh let's say an hour instead
of 5 minutes it costs more.
So you have to kind of plan what kind of
tokens you want to keep in cash and for
how long you know this arbitrage is very
important for you to keep the cost of
inferencing down.
Now I mentioned about the cash hit
versus cash miss. So you've made some
decisions on what you want to store in
the cache and for how long, right? If
you were right about that and you hit
the cache and it's a hit, then your cost
of inferencing is onetenth what it would
be if it's a cash miss. It makes a ton
of sense. It feels super complicated to
expose this in your pricing to say like
think about what you're storing in a
cache and if you get a cash hit it's way
cheaper but if you get a miss it's way
more expensive. Um, on the other hand,
and I'll let you carry on, but I just
want to point out it goes to show that
clearly this adds up.
&gt;&gt; Now imagine now you have this massive
pabyte scale storage system where you
can just store tokens infinitely. Now I
I feel personally this is what I write
about in my rather detailed article on
Substack is that I think that the cash
econ economics of storing cashes is
going to get much cheaper. you can
literally store an infinite amount which
makes it I guess infinitely cheaper to
store that many uh cash tokens, right?
Think about the fact that you have so
much cash now uh that you can store
rather cheaply and what that does for
long agentic coding like I described uh
the cursor CEO said you know how he
developed this whole web browser for in
a week that requires a lot of cash I
would imagine. So anyway, so what do you
think about all this agentic coding
stuff?
&gt;&gt; Yeah, so I think agentic coding is super
powerful. Uh, you know, I'm trying out
claude code myself. I was even starting
to talk to my children about it, showing
my middle school son, you know, like,
dude, you got to check this out. You got
to play with this. Um, and uh, anyway, I
now of course I I use cloud code. I also
am a heavy chat GPT user. And I saw that
Sam Alman had tweeted that open open AAI
wants to speed up codeex um which is its
aentic coding platform. And specifically
how they plan to do that is with a
partnership with Cerebrris and so I this
was super interesting. Um I I clicked I
was like what is all this? And I clicked
on it and there was an announcement
between Cerebrus and OpenAI that OpenAI
is partnering with Cerebrris to add 750
megawatts of ultra low latency AI
compute to their platform. And so of
course this is really cool. Now we'll
talk about Cerebras for those of you who
don't know. They are an AI accelerator
company. I call them a pre-GPT company,
which means they designed their chips
before GPT exploded in popularity, which
means they made design tradeoffs um
before we realized like, oh wow, we need
huge models in memory and we need con
huge context in memory too, right? Um so
this would be similar to the
conversation that we had with Grock.
They're another preGPT company.
Why? I have a question about Cerebras.
Why did they make a whole wafer scale
engine? Basically, they decided to make
a a single chip on a whole wafer. Why
did they do this before GPT? What was
the need for this level of compute?
&gt;&gt; You know, that's a good question and we
should have them on to have them talk
about it. But I think at the highest
level I think they weren't necessarily
the way it comes off to me is that they
were not necessarily starting with a
problem to solve as much as they were
thinking as engineers uh around
constraints and tackling problems from
first principles in a different order.
So let me explain. So you know today we
make these we have these wafers and you
can only make uh each die so big. It's
the reticle limit. It's like the window
that the lithography machine uses to
pattern silicon. And if you want to have
even more compute in a chip, you
actually start taking these reticle
sized chips and then you try to package
them together. So this is what Nvidia
does with their GPUs. They have like
two, you know, big reticle sized dies.
They package it together. Um, and then
now if you're if you think about Nvidia,
you know, you you put those on a board
and you put a CPU on a board and then
that's your board. uh you know you've
got two GPUs and a CPU and of course
that's not enough compute it's not
enough HPM like we've been talking about
and so you scale this up by having more
boards in in a server node and then
having more servers in a rack and then
connecting all these racks and so to get
you know massive compute for AI for
inference or for training you have all
of these you you started with a single
wafer and you make all these dies but
then you chop them all up and then you
package them separate them but then at
the end of the you connect them all
again. You have all this networking and
all these switches and you know all
these racks and so um if you zoom way
out and stop and think it's like uh the
the approach Cerebrus was taking was
like why cut the dyes up? Why not just
have it be one monolithic like the
extent of what monolithic silicon die
could be which is the entire wafer. Um,
and what if you just pattern a bunch of
dye there and connect them all? No, no
serties, no cables, no switches, but
just like wires on the silicon, if you
will, just metal traces, short distance,
you know, wouldn't the data never has to
leave the chip to HPM? By the way, if
they they just use uh like 44 gigs of
SRAMM on their wafer in the wafer scale
engine 3, why not just have all the
compute, all the memory coll located?
Wouldn't that be way lower power, higher
memory bandwidth, higher throughput? Um,
so I have a feeling and we should ask
them about their original intentions
that they were looking at where AI was
going even before large language models
because there was still lots of AI,
right? like timelines, ranking, that
kind of thing. And saying ultimately
more compute is always better. And what
if we fundamentally turned this on its
head and said how much compute can you
actually put on a wafer?
&gt;&gt; Yeah, that's fascinating. I like the how
you just like mentioned 44 gigs of SRAM
and just like continued talking about
it. That's actually a fascinating amount
of SRAM, right? because all this Grock
conversation with Nvidia like each chip
had 230 megabytes of it right and this
here you have this cerebrous wafer that
is 12 in uh looks like Captain America
shield you know that's Jensen's wielding
all the time it looks like that it's not
that but um yeah and you have 44 GB of
SRAMM that is extremely fast bandwidth
and what does it take to have a llama
70B model how many of these Cerebras
wafers do you need then?
&gt;&gt; Yeah, they needed four because you have
to you're not you're going to store more
than just the weights. You you'll store
quantized weights, but you you want to
also have room to store the the
activations and then of course the KB
cache. Um but yes, for for Cerebras,
they could run, you know, 70B llama on
just four of their systems, which would
be four big wafers.
&gt;&gt; Awesome. All right. Now that we've set
the tone of Cerebras, how does this tie
in back to like OpenAI and why why is
this whole thing with them?
&gt;&gt; Yes. Yes. Okay. So, OpenAI had an
announcement and it was uh Sachin Caddy
who was recently the CTO and AI officer
at Intel and he's also an adjunct
professor at Stanford and I think you
know within the last three months he
moved over to OpenAI and he specifically
said that the partnership with Cerebras
um was about OpenAI's compute strategy
to build a resilient portfolio that
matches the right systems to the right
workloads. And this was like music to my
ears. This is something I've been
talking about at Chipstrat, which is the
idea of having
heterogeneous or heterogeneous, I'm not
sure how you say the word, compute um in
your AI accelerator portfolio. Yes, GPUs
are flexible and can do every workload,
but when you're at such massive scale,
wouldn't it make sense to have
particular inference clusters really
hyper tuned to your specific workload?
And low latency is the first workload
where people saw oh interesting these
preGPT accelerators like Grock we talked
about this with Grock and Nvidia can
actually do way faster time to first
token and endtoend response time for
certain small model sort of low context
um workloads you know so again like a
70B model or something
um and if you have those particular
workloads
why take the same compute which you
could save for doing something like deep
research or video generation or
something really computationally
expensive that needs a huge amount of
context and really high you know
bandwidth storage. um why don't you save
that for that like frontier compute for
training or for those inference
workloads and why not have certain
systems that are perfectly tailored just
for that those particular you know
really fast really low latency workloads
and so uh interestingly you know Satchin
is coming in and he's saying yeah that's
what we're going to do we're going to
part with Cerebras and they're going to
cover this area of our portfolio of
workloads we're going to use their skew
essentially for this ultra low latency I
believe was the word that he used uh
workloads and what's what's very
interesting is actually um when he was
at Intel and I was at OCP you know back
in October so just whatever three or
four months ago um Sachin had a keynote
where he talked on behalf of Intel about
the I this a very similar concept where
he said you know at Intel we are now
going to take a workload driven approach
and so for aentic AI he pointed out how
each step in the workload has different
constraints. You know, you've got
prefill where it's computebound and you
actually would be fine with like cheaper
memory, not instead of HBM like LPGDR.
Um because you're not moving things in
and out of memory so much as you're just
computebound, you're just needing to
crank through and get a ton of flops
going. Um and to that end, actually
Intel introduced Crescent Island. So
this idea of an inference optimized GPU
for prefill. Um so think similar to like
Ruben CPX. Um so it was interesting to
see that Intel was starting to bet on
that same future of with what if
companies at scale actually optimize
their infrastructure for different tasks
and even different sort of subtasks in a
workload. Um, so going back to Cerebrris
or uh he's obviously at OpenAI and back
to their partnership. Um, that was the
announcement was OpenAI wants to
leverage some of this hypers speed
compute, if you will. Then Sam Alman
retweeted it and he said, "Hey, Codeex
is going to get a lot faster. Check it
out. We're partnering with Cerebras and
we're going to speed up coding."
So uh we have 44GB of SRAMM and some
really fast inferencing solutions and uh
we have also this
disagregated prefill and decode systems
that uh Intel has in their crescent
island platform. Right? So we have all
these uh different platforms that do
different kinds of workloads depending
on the application. I think that is the
key takeaway here is that there is no
real one-sizefits-all especially when it
comes to inferencing because there are
so many demands like you could have
accuracy as one of the dimensions uh you
could have time to first token or
latency if you want to put it that way
as another dimension
&gt;&gt; uh so I don't what other dimensions do
you think of I remember in one of your
articles you had this like really nice
radar plot which I always now use to
visualize what workload should look like
do you remember what the dimensions you
had in that plot were?
&gt;&gt; I should have pulled it up, but yes, it
was definitely like accuracy
um uh interactivity
um and and then like you know like
context length
&gt;&gt; and and and quantization and ultimately
at the end of the day you can sort of
think of it as intelligence too. Like
&gt;&gt; is is this a a very large model that's
really intelligent or is it just like a
small model not not as smart but good
enough?
&gt;&gt; That's great. like so one of the
dimensions obviously is context length
which goes back to our original
conversation about you know context
storage memory so I guess there's all
this talk about like agentic uh coding
with uh very fast codecs right like as
Sal Maltman put it but do they have a
way to handle long context storage with
this whole cerebras system
&gt;&gt; so that is the question
cerebras if they've got 44 gigs on a
wafer and they use four wafers to run
llama 70B. That sounds promising. But
then you have to ask, oh, where does a
KV cache go? And if they want to in
unlock really long context for
developers and they want to offload the
KV cache, do they like where would they
offload it? Right? Because they don't
even have HBM, it's just that SRAMM. Do
they have some sort of memory server
like Nvidia has announced and like
others have? And if you're from
Cerebras, come on the pod and educate
us. Um I I don't know, but I'll tell you
what I learned when I was googling. Um,
so I did see that Cerebras for training
has already thought through this because
when you're training obviously you these
days people are are training like
trillion parameter models and so
Cerebras has built this memory server
that's a mix of DRAM and flash and it
offloads all the weights into the memory
server and then it just streams in the
weights that are needed at the right
time um with a like a high bandwidth
fast interconnect. So I think of it as
like streaming in you know a particular
layer of the network at a time or
something. And if and if you squint
you see oh they've got offloaded memory
and the ability to stream it in at the
right time for the computation. And so I
kind of wonder if they could use some of
the same technology and use those
primitives and build a KV cache
management where they could offload KV
cache into memory and stream it back in
as needed. So my answer is I don't know
but I bet they're doing something like
this. Yeah, this question extends in my
mind to a a lot beyond what it's only
cerebrus is doing like any SRAM based
approach even if it's Grock um would
they offload from SRAMM because it's so
limited would they offload to HBM first
&gt;&gt; and in in that case is it any different
from uh GPU because you have uh you know
the Grock LPU approach uh but now you
offload to HBM so like you said The
SRAMM is a G0ero tier, right? Which I
don't know, but like Nvidia didn't put
it in their diagram of uh memory storage
for GPUs. So I wonder if all these SRAM
based inferencing companies just are
working in the G0ero tier um for a very
specific application and when they start
offloading to other tiers I wonder what
level of advantage the ASIC based
approach has over general purpose GPUs.
&gt;&gt; You know what I mean? I don't think I
understand the answer entirely. But if
anybody knows the answer, you know, get
in touch with us. We'll figure out a way
to learn from you.
&gt;&gt; Yes. Yes. Let me let me zoom out and
give you my thoughts on that. So, at the
end of the day, there's GPUs,
there are preGPT AI accelerators, and
there's postGPT AI accelerators. PreGPT
would be like uh Cerebrus and Grock. and
and they made certain trade-offs at the
time saying like yes, we're just going
to focus on SRAMM and it's really fast
and now to your point as they start they
were made before GPTs and so they're
saying like with our systems to actually
make it work for today's workloads maybe
we have to have this memory offloading
and then to your question well what if
that's HBM doesn't that defeat all the
benefits that they had by not having HBM
which is cost right
&gt;&gt; and it makes it feel kind of similar in
a way to GPU used, which had made
different trade-offs of, yeah, we're
going to have the HBM right there, right
near the die, and it's going to be
expensive, but you'll have it there. And
now it's sort of feeling like they're
almost converging where it's like
they're all using the same components.
Now,
you've got also, which I'm really
excited about, companies like Etched or
Maddx, who are post GPT AI accelerator
companies, which is they know what the
workload is. And so from day one, they
can design their system for transformer
LLM inference and they can design around
KV cache. We haven't gotten many
technical answers or demos from them,
but it'll be really interesting to see
where they land in their memory
hierarchy decisions. Um because at the
end of the day, GPUs are super flexible.
They can be used for anything. You can
totally use them for LLM inference.
There's all these optimizations you can
do. You can disagregate, prefill, and
decode using Dynamo. You can have a
memory, context, storage system. You've
got all this software. You can take all
these tools and put together a cluster
that's really tuned for LLM inference.
You can take these preGPT clusters, try
to tune them for LM inference, LLM
inference, and on maybe a different
vector like low latency. And then soon
we'll have these postGPT AI
accelerators. And it'll be fascinating
to see the trade-offs across all of
them. and which workloads they all end
up serving at the end of the day.
&gt;&gt; That's fascinating. Didn't uh Etched
recently raise funds too? I saw that
they were in the news.
&gt;&gt; Yes, totally. They were in the news. It
was pretty quiet. Um Bloomberg I think
had the scoop that they raised 500
million at I think a $5 billion
valuation. Etched hasn't publicly said
anything themselves yet, so they must be
waiting maybe until they have more
technical information that they want to
share or something. I'm not 100% 100%
sure, but what you can what I surmise
from such a large fund raise is etched
must have customers, right? If you're
raising half a billion dollars, you're
building not only chips, but you're
building racks and you must have a
hypers scale customer or two lined up,
right?
&gt;&gt; Yeah. I hope you're right. I mean, I
don't know. Maybe you don't need all
that to raise money these days. Maybe
you can just build a concept
accelerator. You know why I say that?
Because wherever there is compute
nowadays, Altman is at that place. Like
if anybody builds an accelerator with
any form of compute, Sam Alman's going
to come knocking. They're so computed
deprived anyway. So totally I think
people will fund it if it's a cool
technology.
&gt;&gt; We should Yes, we should have a venture
capital on to to refute that or to say
yes if we you know we'll we'll fund it
because we think Sam will come play
ball. you know that to that end when I
first saw the Cerebrris announcement and
it said um we're partnering with
Cerebras they have 750 megawatts of
compute at first I thought like oh is
this just a power thing like
&gt;&gt; they're comput limited they're power
limited and if any startup has both
compute and access to power we're
willing to talk
&gt;&gt; yes I think so right I mean those are
the two things that will really drive uh
the availability of compute from
anywhere so it Doesn't matter what kind
of inferencing solution you have. SRAM,
HBM, I don't know, edged, we'll take it.
Can you can you multiply matrices? Yes.
Okay, you're in
for sure. Now, of course, when we
haven't we won't get into it today, but
there are really interesting software
questions to get into as well, which is
like, oh wow, Sam is signing up his
software team to write software that
runs on all these different
accelerators, AMD, Nvidia, Cerebrris,
right? Um, so what how easy or how hard
is that these days? So that'll be
something fun to circle back to in the
future.
&gt;&gt; Yep.
But for that I think we are at time. So
that's it for today. Thanks for
listening. If you're enjoying
semi-doped, we'd love if you give us a
fivestar rating and a quick review in
Apple Podcast, Spotify, or wherever you
listen to this. Thanks everyone and
we'll see you next time.
