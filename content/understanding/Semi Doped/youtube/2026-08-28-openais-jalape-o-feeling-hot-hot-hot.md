---
source: https://www.youtube.com/watch?v=lrNN4mCVloo
vid: lrNN4mCVloo
title: OpenAI’s Jalapeño! Feeling Hot Hot Hot!
date: 2026-08-28
duration_sec: 3272
channel: Semi Doped
kind: transcript
---
We're recording this less than 12 hours
uh since Open AI actually announced
Jalapeno at hardships and I have got a
flight to catch in about 4 hours from
now to travel across the globe. But this
couldn't wait. So we wanted to talk
about OpenAI's Jalapeno inference chip
uh as soon as possible and break it down
to the level of uh you know
understanding we have and from the
conversations we had with people at Hot
Ships. So, let's get into it.
[music]
&gt;&gt; Hello listeners. We've got another semi-
doped coming for you today. Um, so like
Vic said, just Jalapeno and Open Eyes
talk was so awesome. We just wanted to
get straight into it as soon as we
could. Um, obviously lots to digest.
This won't be comprehensive, but I think
we both have a lot of interesting
takeaways as we watched it. And I'll
just say that I personally thought it
was the best talk at Hot Chips that I
saw. I'm watching it remotely and uh you
know the first thing that came to mind
was like did they name this chip
Jalapeno because they knew they were
going to launch it at Hot Chips?
Yeah, that was so funny because
everybody in the volunteers and
organizers there were wearing these
yellow shirts with like red jalapenos on
them and I'm like wait is this like a
self organized advertisement for OpenAI
jalapeno like everywhere like the
subliminal messaging across the whole
conference was these chili peppers and
like okay I don't know if it's a
coincidence or plan but it's pretty
cool.
&gt;&gt; Totally. Yes. 40 chess if that was the
plan. That was genius. Um but okay, so
let's get into it. So, you know, I just
took some of their slides and a few
screenshots from semi analysis who had
an amazing article. So, go read it if
you haven't. Um props to Semi analysis
and OpenAI for benchmarking this chip
together in advance. So, that semi-
analysis had a great article to drop. Um
but let's let's start talking through
some of the slides from the talk and
pull out our insights. And I thought
what would be really interesting to
start with is sort of the vision that
was set um by uh the the OpenAI team was
Richard Hoe and Ravi and Chris. Um so uh
Richard was previously with Google
working on TPUs and has like a long an
interesting legacy. Um and then Ravi is
the chip architect and Chris was kind of
like the software codeesign guy. All of
them were very interesting and um early
on they they said that really the two
metrics that they were designing for
which I put on this slide are the user
experience and which they defined not as
the time to first token but really like
the time to last token the endto-end
latency ultimately it's not like how
quickly does this start processing it's
just how quickly does it get done right
um and then also the energy per request
so how much energy did it take to do
that? Um, and what of course I thought
also was interesting was they basically
said, look, those two are at odds with
each other. You can always go faster if
you use more energy. Um, therefore, we
ought not to report standalone numbers,
but we should always try to show Pareto
Frontier curves whenever possible to
show you as we dial one knob how it
impacts the other. And so, I thought I
kind of like that because right away
they're saying like, we're not trying to
game this. We're going to show you the
full curves. Um, but what the other
thing that stood out to me right away
was like, hey, wait a minute. This is
really interesting. This is a model lab
whose customers are AI users designing
chips and they are designing first and
foremost for the user the end AI user
experience and not cost. And I thought
that was interesting. I've seen a lot of
presentations from merchant silicon
vendors and they are selling to the AI
labs or to the hyperscalers but they're
ultimately they have a different set of
customers so to speak and that can
impact even design decisions and so you
know traditionally you hear a lot of
hyperscalers or or sorry merchant
silicon vendors right away talking about
designing for TCO which makes a lot of
sense but I just thought it was
interesting here that we've got a
different person design a sort of team
designing the chips that is closer to
the end user and then therefore they
were actually thinking about you and I
using AI more than they were thinking
about the buyer of the silicon. So I
just wanted to pause there and that I
thought now that we've got a model lab
kind of vertically integrating and
designing their own chips, it's
interesting to see how they might make
design decisions differently than a
silicon vendor designing the chips.
So, uh, Nvidia and Jensen actually has
said this before. If you're choosing an
architecture for a chip that is based on
making the chip cheaper to make or
something like that, it's a bad
decision.
You've got to make the best performance
decisions period because we are not in
the era of um you know trying to save
money in making of a chip but like the
the running of a chip the the the tokens
per jewel which is a nicer way of saying
tokens per second per watt which is like
too many division symbols there but yeah
watts and seconds can be like mangled to
form jewel. So tokens per jewel. Jewel
is a unit of energy. uh what is a unit
of power right so um that so the tokens
per jewel is a very important metric uh
so
that is the ultimate cost of ownership
because you are going to put in energy
and you're going to get out tokens right
you're going to put in jewels you're
going to get out tokens so the energy
per request is one important uh metric
but I don't think the concept is new uh
you know people have been putting tokens
per second per megawatt on these
interactive activity curves that you see
all the time and I'm sure it's there in
this presentation too all the time. So
it's always like this is the y-axis in
most curves. Um and then some form of uh
latency or how the user is served. So on
these charts we will see it's usually
tokens uh per second per user. Right?
That's the x-axis in most of these
interactivity curves you see. But yeah,
so their idea is just essentially to
bring on the TPU team and vibe code a
chip in 9 months. Okay, that's their
whole play. [laughter]
Yes, totally. And uh I think yeah, maybe
maybe last thought here, there was a
quote I think from Ravi as he was
talking about that it said that there's
a market for tokens. It wants them fast,
it wants them cheap, and making things
go fast gives us joy. So I thought like,
oh, cool. What a cool team to work on
too. Um, so then they
had a slide where uh the OpenAI team
gave major props to semi analysis is
inference X and said hey we benchmarked
against inference X we think it's a fair
public powernormalized comparison. So
again saying we want to be as
transparent about how our system
performs as possible. Um, and a couple
things they pointed out is instead of
picking a particular model that fit
well, what they liked about inference X
was there's multiple open-source models.
So, um, they can be tested on something
that's small, something that's big,
something in the middle. Um, and they
also liked that at the end of the day,
all that really matters is that user
experience from the entire system. Um,
so they thought this was a fair way to
capture and compare end-toend
um,
latency and how the whole system does.
So tune your hardware, tune your
software, tune your networking, whatever
you need to tune to make the best
experience possible for users. Um, I
will point out, you know, some of the
feedback that that in the conversations
that have happened since where people
pointed out that this was uh Jalapeno
was tested with a pretty small input and
output uh context length and um so you
know I think there's probably questions
on okay that's cool that's awesome but
would love to see how it performs with
like you know a million input context
length. Did you talk to anyone on on
that topic?
&gt;&gt; Uh no actually. Um
they people were generally uh quite
happy with this but not amazed. I was
more towards the amazed side than you
know I mean I was obviously happy about
seeing the chip come out or whatever.
But uh to me it's just like the
performance. I I read the semi analysis
article at least halfway even before I
attended the talk and uh it's a very
performant chip
to be clear uh I think even semi
analysis says that they have not run any
agentic workloads on it so they also
have the agent X platform that it has to
be benchmark benchmarked against some at
some point I'm sure they'll get there
but inference X is a good start uh so
throughout the conversation I I was
trying to figure out what are the
parameters here that would break you
know uh the jalapeno chip like are they
cherrypicking
let's say I don't know the input
sequence l length and output sequence
length here that is like 8k and 1k is
one metric but I'm like I'm just always
trying to think of like is this a cherry
pick use case you know so I'm trying to
be critical the whole time but it's it's
really hard to tell because if you think
that this is an easy case then you're
like oh wait what what's the number in
the other case so it's hard to dis
figure out the whole thing
&gt;&gt; yes
&gt;&gt; but one thing that is um
very useful is this slide yeah actually
you should just go there yeah because if
I mean if anybody's listening to this we
are actually talking through the slides
on YouTube so if you want to like look
at the slides and see our annotations on
the slides we have them all marked up so
you know we could obviously um try to
talk through some of the stuff you're
seeing. So if you're watching this or
listening to this while driving,
shouldn't be watching while you're
driving. But yeah, uh we'll try to
explain we try to explain some of these
things. One thing that people
immediately thought when in Jalipeno
came out is like oh it's optimized for
the open AI models but they actually
showed that it's not so and they
actually ran GP OSS which is like a
narrow small model all the way to a
Kimmy K2.5 model which is much different
shaped model. So, it's not designed for
that. And semi analysis points out that
in fact they were able to play Doom on
it, you know. Uh I I guess it could do
other things than inference, but I'm not
sure how Doom uh plays into this. I
guess Yeah. Cool. It can do other things
is all I take away. [laughter]
&gt;&gt; Yeah. Yeah. No. Okay. So, you make very
interesting points, which is like we
want to ask what all is this chip good
for and where does it kind of break and
are they cherrypicking something here?
And I think the point of this slide was
the OpenAI team saying look we made a
sort of generalized inference chip. So
it is an inference chip. It is focused
on inference not training. It is focused
on LLMs, not um convolutional neural
network inference, right? Um but it's
general enough that it can run a small
model, it can run a medium-sized model,
it can run a huge model. Um, and so I
think, you know, as you're trying to
think about all the different corner
cases that it can and can't handle, I
think probably the only knob that we
would like to see more is really that
context length because I think right
here they're showing, you know, hey, we
can run these different models. And to
your point, it's not just specifically
the open AI models, but it's more
broadly it can run any open- source
model. Now, of course, right away you
have to ask, oh, interesting. They're
obviously as engineers trying to show
that it's flexible enough to handle
innovations that come down the pipe in
the future, whether it's um algorithmic
innovations or harness innovations or
what have you. But right away, if you're
thinking from a business perspective,
you're like, "Wait a minute. Um this can
run other models. That's super
interesting. What is the implication for
Nvidia's or AMD's general purpose GPUs
which kind of make the argument of like
hey they can run all sorts of different
shapes of models it's not um set in
stone and then when when the ratio of
this to that changes oh no the the
hardware is dead on arrival um and then
even the implications for Google TPUs
which Google TPUs used to
counterposition against GPUs to say like
hey we are more specific for you matrix
multiplication and data flow uh with a
data flow architecture but we aren't as
narrow as like it only works on a
particular model and so here is open AI
coming in and sort of saying like hey
we're fairly generic too but of course
still really focused on large language
model inference
yeah do you think just like Google TPUs
they weren't selling these initially to
the general market they were doing it
for themselves Do you think uh you know
OpenAI is going to start selling these
ships? Clearly, it runs any model. So,
do you think they're going to start
selling it to everybody?
&gt;&gt; Yeah, that's a good question. On the one
hand, you could say
no, they shouldn't. They should use
their vertical integration as a means to
compete against anthropic, against
Google. um have better margins, move
faster, control their costs, make a
better user experience, and so on. Of
course, what gets complicated is if
you're like on the finance team, you're
like, "Okay, that's great, except this
is so expensive to, you know, build and
run these things at scale. Wouldn't it
be nice to offset these costs by being
able to rent them to others or sell them
to others?" So for example, I kind of
think of the analogy of foundaries and
IBMs where it's like, hey, for the
longest time, of course, Intel wanted to
use their foundry captive. They wanted
to keep it to themselves and take all
the advantages for their product team
saying like, hey, we're on the new node
sooner than everyone else and our
product team can benefit that and
that'll ultimately benefit our business.
Why would we share this node with AMD or
or a competitor? Um but then of course
the cost of a fab just keeps doubling
and doubling and at some point you know
you have to like amortize those costs
and so now um they made this chip with a
small team and they did it quickly but
obviously still the cost to to tape it
out and and to ramp it up or we're still
you know talking$und00 million or or
whatever and and so that would be the
question is like [snorts]
&gt;&gt; is there a reason where they would want
to advertise those costs and and rent it
or sell it to others but do it in a way
that's u maybe sort of doesn't lose a
competitive advantage. So what I think
the first thing that I think is like
[snorts] what about enterprises like
don't sell them to or rent them to uh
anthropic but what about enterprises who
want to run onrem or run cheaper could
you part could you sell them to a
neocloud have the neocloud you know rent
rent it to enterprises and of course it
doesn't have to be bare metal rentals it
could still just be like I want to run
uh you know open AAI inference as a
service I just want the cheap version
this is what AWS is doing tranium. It's
like, hey, you know, we can give you uh
we can run our models, whatever models
at 30% cheaper or whatever because it's
running on our XPUs and not on G uh GPUs
with the various middleman margins. And
so, yeah, I'm just thinking out loud
here, but [snorts] I think there could
be ways that OpenAI could pursue this
line of business if they wanted to.
Time will tell.
&gt;&gt; I think I'm going to go think go go go
go at this a little differently.
I think that
OpenAI's uh benefit or unique advantage
here would be to make a chip specific to
their architecture. I'm like I'm not
exactly sure why they are showing that
this works with every every other model
unless they want to go and sell this to
other people. Like otherwise in the
spirit of extreme code design you want
to get let's say there is a way and
we'll get to some numbers here but let's
say there's a way to make this chip
perform like a Cerebbras class chip
because you can uh essentially
finely tune the hardware for the actual
software you're going to run on it and
the actual workloads that you're going
to run on it because this is the
information that Nvidia does not have.
Nvidia does not sell these tokens or
anything like that. Anthropic and OpenAI
have these chips that are, you know, can
be finely tuned to what their models are
supposed to run, you know. So, if you
can make extreme performance just by
co-designing with it, they should do it
because they even have all kinds of
statistics and data and things like that
that nobody else has about how their
tokens are being like, you know, what
kind of workloads and know how, you
know, their models are being used. And
so they should use that to their unique
advantage. I mean like what I don't see
why it's a bad idea to design Jalapeno
only for open AAI models and finally get
performance up to cerebrous levels.
&gt;&gt; Okay Vic. So to the question of should
they design even more specifically for
their own models or should they keep it
general because to your point they know
their models and they know it's coming
down the pike better and therefore they
would have that advantage of we are
vertically integrated. we can co-design
with our model team and run out ahead
and that could be our secret sauce is
just knowing what the model team's doing
and designing to that. I thought I I
included this slide. There was a a
fairly related point made by Ravi I
believe during the talk where he said at
design time there's two costs that we
have to consider. Marginal cost which is
hey how much will it cost to include yet
another feature? We've got a laundry
list of features. how many transistors
or how much floor plan area would it
take to include that? And opportunity
cost, which is if if there's user demand
that you can't supply because you didn't
have the feature, then um too bad,
you're out of luck. And he said, you
know, the opportunity cost is generally
much more than the marginal cost, which
he said there's like a regret factor
there. So ultimately they have a laundry
list of features. They want to include
them all and you have to think about
like ah which ones we going to regret if
we don't do that. Now of course you take
all these features and um you try to fit
them into your floor plan and then it's
like oh wow we have way too many
features and we actually there's no way
we're going to make this fit in the
chip. So you just have to like start
cutting stuff and eventually you just
need to tape out the chip. So that's
where the road map comes in. You say ah
maybe we can get this feature in um
later. And so my thinking and question
is like I [snorts] wonder if there are
ways to still have a sort of general
design, if you will, meaning it'll work
for any uh transformer-based LLM, but
yet also be designing for particular
features for your model team in the
chip, maybe that you aren't going to
talk about, but um that
&gt;&gt; so this is good because I think it by
keeping it relatively general, I mean,
they don't have to run Kimmy on it,
having generality will help them develop
their own future models on it. So I can
I can kind of argue against my own
argument on that front.
&gt;&gt; The second thing that is that somebody
in the audience actually asked, "Hey,
what was the hardest decisions you had
to make on this chip, you know?"
&gt;&gt; So I I I like that question cuz it
really opens up the door to a lot of
answers. Of course, Ravi was very
measured in answering and he said the
hardest decisions were the ones that we
had to decide what to cut from the chip.
Like we we wanted to make all these cool
things but you can't, you know, so how
do we decide what to cut? So that's the
hardest decision.
&gt;&gt; Exactly. Yeah. Which I thought that was
an insightful question. And then I think
Richard also pointed out with this next
slide like hey but guess what? We have a
road map of chips. We've got I'm holding
jalapeno in my hand. our Gen two is
already approaching tape out and we're
thinking about Gen 3. So, I'm sure it's
a little bit of uh kind of just
scheduling and prioritization of like we
really want this feature, but these
things are not going to make Gen one,
but how can we get them in Gen two? Um,
and so maybe
&gt;&gt; I like the approach that this is our
first take. Um, and they made this chip
in a really short span of time. It is
about 9 months from first RTL to tape
out which is an incredibly short period
of time for anybody who's worked
[snorts] on chips would know that this
is ridiculously short. Usually these
things used to take 2 to 3 years at the
very minimum and it it involved a lot of
manual work. It seems like AI has really
helped them. And I was like, wait, is
this a way of saying that you should use
more AI because it kind of is a proof of
concept that more AI is better and it
helps OpenAI's business by showing how
the sausage is made, you know, to use AI
to make chips and then chips to make AI,
you know, it's so I was like, yeah, it's
cool. I don't know. It's cool if people
use AI to make a chip. Yeah.
&gt;&gt; Oh, totally. Totally. And um yeah, semi
analysis I believe made the point of
like hey most people their first chip
it's like almost throw away. It's like
proof that they can do it and they learn
a lot through it but where they want to
compete is on chip two or three or four.
Yeah.
&gt;&gt; So it's very interesting that they came
out swinging with chip one. Um let me
actually go back a couple slides though
because uh you know okay here's a slide
uh screenshot from semi analysis. Um
this is they've got Jalapeno which is
the purple line here that's that's out
on the PTO has set a new Pareto
frontier. It's with Deepseek R1 671
billion parameters. So not the biggest
model but a fairly decent sized model
and you can see that you know at given
ISO uh interactivity it's much higher
throughput and can it can also reach
much further out in interactivity than a
GPU. Now, I think to be fair, some of
the push back was the uh Jalapeno will
have HBM4 and a lot of these chips that
it was comparing to the Blackwell um is
on HBM 3E, I believe. And so the the and
this, you know, MI355 as well. And so
the fair comparison is going to be
Jalapeno against Vera Rubin and Jalapeno
against Helios. Um,
but I I just wanted to make the point
that um this is their first chip and uh
it's obviously in instantly competitive
and so I think that's also what's
impressive. Not only was it fast but it
is competitive as well. So that was that
kind of medium model when they when they
showed like look we can do models for
you know from left to right on the
spectrum. This was that point in the
middle. They also showed um when they
run a small model GPTO OSS 120 billion
parameters um probably what really stood
out and has very interesting
implications to sit and think about for
a while is hey look jalapeno can reach
out to above 1,000 tokens per second per
user and that's the SRAMM territory and
so you know GPUs just can't get there
and so then that's where GPUs said okay
fine we will um you have Dynamo will
split the workload to prefill and decode
and we'll run the decode on these SRAM
chips Grock or it could be Cerebrris um
and now all of a sudden Jalapenño is
coming in and saying wait a minute which
this is the same argument by the way
that AI AS6 startups are making which is
like hey actually um what if you can
have one chip that can do both high
throughput at a lower decode speed but
also reach those you know thousands of
tokens per second
&gt;&gt; [snorts]
&gt;&gt; This is compared to Blackwell of course.
So uh if you put the Reuben system with
the LPX, you know, basically the Gro
chip, uh you can get this potato curve
too. So it's not like there isn't
hardware out there that can't do this.
It exists in different forms. Uh but
it's nice to see that this chip in a
small model can do over a thousand
tokens per second per user.
&gt;&gt; Yes. Which again is interesting, you
know, can it will be interesting to see
how far Vera Rubin can get by itself on
this because then you have to ask
yourself like oh okay well you can get
it with uh Grock that's nice but
remember how many racks of Grock it
takes you know of LPUs. So then you have
to ask is it is the cost worth it and
probably the power consumption worth it
to have a NVL72 rack and nine Groc racks
or whatever it is or could you just have
a rack or two of jalapenos?
So jalapeno's benefit really seems to be
the token throughput per watt. It is
actually very energy efficient in u
generating this kind of performance.
That's one of the key takeaways
especially if you normalize it per watt.
It's a 700 watt TDP chip. Um, which
compared to the Blackwell, you know, the
Blackwell GB200 is over 1,2 I think it's
1,200 W. So, that's a big difference in
the power consumption. It's a very
energy efficient chip as well.
&gt;&gt; Yes, totally. Which matters. And they
another that was another point why they
liked uh semi- analysis inference X was
it is power normalized. Um, so it's not
like, oh, just use more power and you
get more tokens or higher interactivity.
Uh, well, that's kind of cheating. So,
you know, power normalized. Um, okay,
one other thing. So, back to this slide
that had their road map. At the bottom
of the slide, they called out, you know,
and hey, thanks to our incredible
partners, especially Broadcom and
Celestica. So, I thought it'd be worth
talking through really quick. Who are
some companies that are helping and
participating? And if you're thinking
about like what happens if this goes
really well for OpenAI and as literally
one of the two biggest uh consumers of
compute, if their own chips uh seem to
fit their needs very well and they
eventually spend more and more of their
gigawatts or megawws on their own chips,
who might be some of the other supply
chain vendors who will benefit? Um
obviously broadcoma and then there's
some other ones as well. Do you want to
talk through these quick?
&gt;&gt; Uh, yeah. So, the uh CPU is an x86 CPU.
People believe it's a Turin class CPU,
which is a which is a good CPU. I'm sure
the Venice will do better if they want
to do AMD. Uh, there are Intel
alternatives. So, there's a lot of CPUs
out there, but this is a Turing class
CPU, which is a good one. I mean, it's a
good CPU for sure. It's built on TSMC N3
node. Um and I think they they have the
N3P versus N3E
uh which are slight variations of the
same process node but for different
power optimization uh and speed. And I
think the biggest speculative thing is
that uh this uses HBM from Samsung, HBM
4 from Samsung and seemingly has a
slightly better uh you know speed per
pin compared to I don't know like SKH
highix perhaps. Uh so that's maybe
giving some more boost to the
performance but that's entirely
speculative.
Yes, and thanks for semi analysis. You
know, they talk about this uh you the it
was semi analysis speculated that
Celestico was the partner here at the
system level design. So, you know, I
think you kind of think of them as like
the ODM partner helping build out the
full system. Um sort of like how AMD
acquired that company I'm blanking on to
help them with their Helios rack design.
Um Celestica partnering here and then
Broadcom. So, Broadcom um obviously is
like uh the partner in helping the ASIC
get built. Sometimes that can be like
all the backend design. It's not quite
clear, but there was mention um in semi
analysis article and sort of a little
bit in the Q&amp;A um about interface IP and
IO chiplets. So, I think the in the the
Q&amp;A there was mention of most of the
chip is designed from scratch. I think
this was uh Richard talking the compute
die I think only has some interface IP
and then there's also an IO chiplet as
well a lot of the interfaces are
existing IP um the the rest of was all
fresh RTL so basically maybe Broadcom is
also the partner on the like IP the IO
chiplet but then obviously as we'll get
to when we talk about the the networking
um they're participating with their
Tomahawk uh switches so Broadcom sort of
benefits from potentially IP and IO, but
then definitely the switches.
Um, so let's let's get into the
networking because obviously that's an
interesting piece. So let's start
talking about architecture. So when they
when Chris Liry came up and talked about
the architecture, he set the stage of
like and and I think kind of implicitly
in my head I'm thinking like, oh dude,
like all day Sunday Monday was about HBM
the memory bandwidth wall and
everything. And then and then he came up
and said hey actually uh memory
bandwidth is a limiter but it's we are
not fully utilizing and hitting that
ceiling where literally if we don't get
more memory bandwidth we're dead because
he's like if you run the math and the
math is here on the screen. Um we should
be getting 1 to 2,000 tokens per second
per user without speculative decoding
and with it we should be getting 5 to
10,000 tokens per speculative you per
user. We're nowhere near that. So if you
just pencil out like what is the HBM
ceiling, we are not there. And then the
questions are why are we not there and
how can we get closer to it. Um, and one
of the really interesting things that
um, Chris hit on and I wanted to zoom in
on was he talked about KV cache and I
have a couple quotes I'll read them and
how KV cache is very important but done
wrong you're shuttling or all this KV
data around and then also maybe you have
like copies of it everywhere to try to
like not have to move it around and so
um, the question is could you think
differently about it to overcome some of
those trade-offs? And so uh let me read
these. So in he said in agentic
inference the largest and fastest
growing data structure is the KV cache.
We do not believe that the long-term
solution involves moving large KV
states. Disagregated prefill is a
solution for GPUs because GPUs need to
build a large batch to make sampling
efficient. This ends up requiring a lot
of prefill replicas supplying a sampling
replica. the cost of losing KV locality
is also replicating these weights in
every single HBM. Um so you know
obviously pointing out like hey the way
that GPUs work uh there's some dirty
tricks that they have to do to make it
work and obviously you know we we talk a
lot about how like oh prefill and and
decode and disagregation is the way and
then here they're kind of questioning
like is it and and he uh Chris went or
let me pause. Do you have anything to
say there? Uh that's a very interesting
calculation essentially that the fact
that [snorts] hey yeah this uh if you
have the total aggregate bandwidth if
you take all the HBM4 chips uh across
128 chips which I believe is what they
goes into their rack you get like one
pabit per pabyte per second and then uh
at a 4bit you know FP4 if you have a 1
trillion parameter model and you have
you know let's say.5 terabytes of data
you should be getting about 2,000 tokens
per second but even just from HBM but
like we are not getting 2,000 uh tokens
per second from HBM because that's the
whole thing about why you know Cerrus is
using SRAM and LPUs are using SRAMM and
all that so that you can get it faster
you know above 200 I mean cerebras
actually in a in a separate discussion
we can probably have promises like you
know 4,000 tokens per second because of
SRAM, but the complexity of their system
is enormous. This is a good argument
saying like, hey, why are we not even
using HBM to the max and you can see
people like Nvidia are pushing the
future per pin lane rate per pin rates
from, you know, 10 GB per second to like
16 Gbit per second. And I saw some
charts in the memory uh talks at hot
chips that HBM 5 will reach more like 23
24 you know Gbit per second. But are you
actually using all that bandwidth and
does it show up in the token count?
Open AAI says no it's not we are not
using the whole capability of even HBM
so why don't we do that so I like that
approach very much
&gt;&gt; totally which you know has all sorts of
interesting implications then when
you're thinking through memory companies
which is like well how important like
exactly what you're saying which is like
okay today we're not even fully
utilizing HBM but our solution is just
like make it go faster make it go faster
make it go faster but it's like whoa
whoa do we need to make it go faster
every single year or do should we slow
down and focus us on taking advantage of
what we have before we go faster.
&gt;&gt; Um,
&gt;&gt; and I like the KV cache locality idea as
well because it's like, you know, KV
cache is the biggest problem in decoding
uh because you need to move all this
data back and forth and you have to do
it token by token. So they argue that
this is not the right idea. Like this is
long-term. Don't move KV cache around.
Like if you don't have to move it
around, then it solves so many problems.
Like keep it local somehow. And they
have another uh statement later that we
will get to that you know dark silicon
like if you can turn off some stuff it
is still better than not using GPUs like
dark silicon is better than unused GPUs
but we'll get to that.
&gt;&gt; Yes. Yes. We'll get there. Okay. So, as
Chris was talking about like, hey, so
why aren't we using the full bandwidth
of HBM it um one of the things he
pointed out was like, well, guess what?
When we're trying to do some operation,
some mattel, the data is not there when
we need it. Like, that's a really big
problem. And so, he, you know, he called
it uh the operands arrive late. So, the
data is not in the registers when we
need and why. And so, they talked about
like, oh, well, you've got these unified
memory subsystems and you've got all
this contention. So you've got all this
HBM and you're sharing HBM with all your
neighbors on the scaleup network and
there's copies of things in various
places and there's all this contention.
So yes, you can get the data off quickly
from the HBN, but then getting it to the
right place at the right time is a
problem. And so his point was that
utilization falls. So sure, we have all
this HBM4 bandwidth, but the utilization
falls if compute or memory is blocked
just waiting on data in transit. Um, and
so that's where this uh local HBM slice
thing comes in. And I'm going to show
the the diagram of it, but maybe some
quick quotes again. I probably won't
read these whole things, but he said,
"Okay, so how do we stop this
contention?" What they came up with was,
"What if you have little local HBM
slices for every accelerator and they
have dedicated buses that have high
efficiency and low latency?" Um, so how
can you use up all of those flops? And
he then there was like this one um nice
quotable sound bite where he said
because ultimately the show flops don't
matter. It's how many flops you actually
deliver. Meaning like who cares if you
have a bunch of transistors and you do
you show on napkin math that you could
achieve this many flops. If the data is
not there in time, it doesn't matter.
All that matters is the user experience.
Which is kind of back to the argument I
was trying to make like they're really
thinking about the user experience.
Okay, how do we just make the user
experience as good as possible? Well, we
have to actually utilize our memory
bandwidth. we have to actually utilize
our flops. How they came up with it was
this HBM slice with a local low latency
view which he he called a NUMA style
architecture. So here's the screenshot
of that. Um I'll let you jump in here
and take the first stab at it.
&gt;&gt; Yeah. [snorts] So instead of so numa num
to to those who haven't heard the term
numa it stands for non-uniform memory
architecture and it's often used in like
CPUs because when you have a multi- you
know core CPU um how does each core um
have memory uh shared along with it. So
what you can do is you can you know um
[snorts] have parts of the memory
cordoned off for each core very broadly
speaking I'm not going to get into it
too much I've actually written about
NUMA um architectures in the CPU article
that I I have on the substack so the
same way here the idea is that instead
of having the HBM as a resource that is
contended for you just slice it up and
dedicate a slice of HBM to a processing
core and then that way there is no
contention for HPM memory and everybody
has their own lane they can keep
operating on. So I like the idea it's a
simple fast approach to minimize
contention. Right.
&gt;&gt; Yes. Yes. And now and they made the
point on uh in the presentation which
was like this we think is the best
design. every HBM slice or every
accelerator has its own local HBM slice
and this starts to lead into the
networking and then therefore we have
like they can talk very quickly to the
HBM then we have this next level of
communication this collective network
which is high bandwidth and low latency
and then um to kind of talk further out
we've got this general knock um that's
not as fast but uh it gives us the
flexibility to talk between them um but
the point that was raised was like hey
okay [snorts] this is how the computer
design is designed. Yes, that could make
things a little bit more complicated
because now you have to ask okay how do
we make sure that the right data is in
the right place and how do we think
about taking the workload and mapping it
to this architecture but ultimately that
complexity is was worth them solving
because this results in a better user
experience and better performance. They
just have to solve the problem of like
okay we need to think about this
differently. what happens when you have
all these NUMA style HBM slices what
should we put where ultimately um so
with that you see on this slide there's
mention of the scale up Ethernet bridge
and so I think I have the the next slide
yes okay so the next slide is they said
okay that was the architecture or like
thinking about you know each chip but
let's think let's talk about the system
and they called out a large scaleup
domain for theund
128 8 jalapenos can talk on this large
scaleup domain. There's Broadcom um
Tomahawk 6 switches that communicate at
600 gigabits per second per chip. And
and then there is a broader um scaleup
domain that scales all the way to 248
jalapenos and that's at 200 gigabits per
second um interconnect. And this is
communication using EON um which is the
uh scale up networking sort of uh
protocol or or group that Broadcom
ultimately spearheaded uh and is
different than UAL link which is a
different one. Um but yeah take take it
away on this slide.
&gt;&gt; Um yeah so this is a EAN based scaleup
network. So they have 200 um Gbit per
lane uh in the in connections here and
so uh I so this uh picture itself
doesn't explain all that much to me but
yes so it's a it's a bunch of uh chips
connected with networking and tomahawk
switches and uh people were trying to
count how many switches and how many
tomahawk switches obviously but uh yeah
it's it's a it's a networking setup you
need to network a bunch these chips
together.
&gt;&gt; Yeah. Yeah. I think probably the maybe
the interesting point is this is all
scale up and there's sort of like a
two-tier scale up network here. So
there's probably like
&gt;&gt; within the rack
are those those 128 are probably all
within one rack and then the 2048 I
think was 16 racks. So their scaleup
network is kind of two-tier and it
actually can spread out across 16 racks.
&gt;&gt; Yeah.
Um, and and with that, I guess I'll
point out a lot of times you'll hear
people say, "Oh, scale up is within the
rack and scale out is like rackto-rack."
And this that this continues to show
that that's not the case.
&gt;&gt; That was a case for a point in time, but
obviously really scale up is the
accelerators that are sharing memory.
&gt;&gt; Yeah, they they say that this is what is
called a half flattened two-level clo
topology. I was like, "Okay, I really
need to think about this." Like I cuz I
don't understand what that exactly means
at this moment because it heard it for
le, you know, less than a day ago. But I
really want to think about what that
means for networking. But that's an
interesting point there.
&gt;&gt; Indeed. Indeed. So on the next slide,
here's [clears throat] this quote that
you mentioned that dark silicon is
cheaper than idle accelerators. So I
thought this this slide was really
interesting. Again, zooming out, the
OpenAI team was saying, "Hey, we're not
designing to one specific algorithm
implementation as it stands today
because um in this chart in the top
left, they they say like depending on
the type of workloads, obviously they're
running all sorts of different models,
right? Like they have their big models
and their medium models and small
models. Um there's a different ratio of
prefill to
drafting and specular decoding to
verifying and it's always changing and
um we don't want to be locked in forever
on one particular ratio. One way that
GPUs solve this is say, "Okay, have some
GPUs that are um dedicated to prefill,
have some that are dedicated to the
decode side of things." And um OpenAI
said, "Why?" So the only problem with
that is then you literally could have
like GPUs or racks of GPUs sitting idle
um if you know you're focused on
prefill, you're focused on decode. Um
they said why not just have a single
balance chip where every chip has enough
compute and enough memory bandwidth and
enough IO that it they could handle
different parts of the workload and then
we can just gate and not power on the
sections that aren't needed. Um so yeah
did you want to say more on this topic
here?
&gt;&gt; Yeah. So I wanted to explain what draft
and verify means in a workload because
everybody may not be aware of what that
means or what speculative decoding is.
So the idea of speculative decoding uh
has like two two parts of it right right
the drafting and the verification
process. So what the drafting is is that
you know instead of trying to um just
generate the right token every time what
this speculative decoding is is it tries
to make a guess. So a smaller model
often called a draft model will generate
a bunch of tokens like let's say it
generates eight tokens all at once. And
now we want to make sure that like one
of those tokens is correct because it's
a small model.
&gt;&gt; It's not very smart. Let's just call
this like a not a very smart model. So
it could make mistakes. So out of the
eight tokens it has given you maybe only
one token is correct. Right? And the
idea is now you need to verify those
eight tokens and find out which is the
right one. So the drafting and
verification process it it is really a
dynamic thing like you if you have a
smarter draft model you could probably
only generate two tokens and then have
it the verification process decide which
of those two two tokens is the correct
one. So this is like a faster way to
improve token rate because you don't
have to make the large model generate
the right token. Instead you just
eyeball it and then this decide which is
the right one. Right? But that changes
like if you want to use a smaller draft
model, maybe the approach is just you
spray a lot of tokens and then the
verification workload takes over because
now you have to find out which of these
is the right token. Now to eight of them
to verify. So none of these are like set
in stone. So the draft the speculative
decoding has these knobs you can turn
and each of the depending on the
workload can generate different token
throughputs. So the the point here is
that yeah there could be a different
kinds of mix of draft and verify models
that really uh require the chip to
operate differently based on the need of
the workload.
&gt;&gt; Yes. Yes. And so then the argument is
back to hey these one chip can handle
different workloads, different parts of
the workload. Um, and actually there's
probably an argument there for the
useful life of the chip. When I think
about a um, Vera Rubin paired with a
Grock LPU, you have to ask like what's
the useful like life of that Grock LPU,
it's really focused on decode um, in a
particular format. And if that should
ever really change, either it's going to
be potentially like less efficient on a
new workload or you could say like, oh,
is all that silicon just have a shorter
useful life or it's only fixed to run a
much smaller set of workloads. Um where
here they're trying to say like no the
way we're designing it and thinking
about it is
uh it could run all sorts of different
workloads probably have a very long
useful life um even beyond when it's not
when they have version two of the chip
out.
Um, okay. So, this was just the last
slide that I had and it kind of had all
their specs listed again and a floor
plan which I thought was pretty cool and
again the most important spec and I
think you actually hit on this already
which is just performance per watt on
the end to end workload. Uh,
&gt;&gt; yeah, it's a pretty cool chip overall.
It's a pretty cool chip. Uh, they they
made it in a really short amount of
time. It's by no means um you know
optimized anything like that but you
know they their next version of the chip
and the one that follows should all be
very interesting. So it's a great start
for sure and it's very exciting that you
know they have all these TPU guys. So I
was like how do they design a chip so
quickly? I think it's a combination of
AI and having the right people on the
team. That's my takeaway from talking
with people.
&gt;&gt; AI having the right people on the team.
I think Richard specifically said or
somewhere that also just starting with a
blank sheet is an opportunity where you
know you're they're not thinking about
like how do we make legacy software fit
into this or anything like that. Um but
obviously they have the right team they
have AI. We haven't even touched on AI.
It probably could use its own podcast,
but um a lot of the on their slides, a
lot of things they did were very
interesting on how they used AI to go a
lot faster. If you haven't watched the
talk, definitely just watch it. But
maybe if people are interested, you
know, we can keep going into that
because then again, I think there's all
sorts of questions about like um what
did OpenAI do to help them write RTL?
Um, and is that apples and oranges
versus what Cadence and Synopsis are
doing or is it apples to apples and just
starting to think about the AI for EDA
space and where open AI fits in there?
&gt;&gt; Definitely a lot of people are uh, you
know, using EDA already for like chip
design and AI enabled EDA on top of
that. This is kind of proof, public
proof that hey, this really is
worthwhile and it really works and it
accelerated the design uh pretty quickly
and had a open AAI developer chip in 9
months. So that's a good story to tell,
but it also is a wakeup call to a lot of
people building inference accelerators
now because if somebody can come in and
generate a a chip that's better than
Blackwell in in under a year, the
question is
&gt;&gt; where does acceleration take us now?
like how much better of a chip
&gt;&gt; will a company with the right AI tools
and the right people be able to design
given 2 years you know and that will
dictate like how money should flow like
who should be funded who is capable of
doing this right and what kind of
hardware will emerge because of AI
building AI uh in a sense
&gt;&gt; and what does that mean for people like
Nvidia like is there really um you know
something to worry about for the
hardware where that you know cuz if if
in one year somebody can come and beat a
blackwell I understand there are like
HBM 4 HBM3 discussions but those are not
not the broad view the broad view is
that some you know I think the semi
analysis article has some comparisons to
Reuben as well so it's it's much more of
a Reuben class chip than it is a
blackwell class chip because of HBM4 but
regardless you know a company with the
right people and the right tools could
make a Reuben class chip in a year
that's the takeaway [laughter]
&gt;&gt; yes yes and actually what's really
interesting So there's you called out
you got to have the right team and they
used AI and so also if you compare to
other startups so there are startups
that had teams that for example came
from Google like I think of Maddx and
Rainer Pope and um they they had folks
who came from Google and so they started
with people in the knowhow but they
didn't necessarily have the AI tools
right away and so you can kind of
compare uh merchant silicon vendors GPU
vendors versus AI as startups who had
people and knowhow um now versus have
the knowhow and have the AI tools and
you know compare and contrast how
quickly these folks move. Actually
during the talk um one of the speakers
mentioned that the initial RTL was
developed with a GPT3 class model and of
course as they kept developing their uh
models got better and they could use
newer models but it's not like any of
these companies don't already have a
GPT3 class model available. I'm not
saying that it's all because of AI that
they could do this but I think it's a
part of it and it's something to pay
attention to. To me, it's, as I
mentioned at the start of this episode,
it's kind of amazing to me that this
could be done in under a year and you
can gen generate Reuben performance out
of a chip.
&gt;&gt; Yes,
&gt;&gt; that's pretty cool.
&gt;&gt; Yes, that is very cool. Obviously, you
know, um Nvidia can totally push back on
lots of this to say like, okay, let's
see you manufactured at scale. Let's see
you ship it at scale. How reliable is it
at scale? Right? And so so obviously the
um
&gt;&gt; the market leaders that have all the
experience and all the production hours
uh are doing fine but still very
interesting implications. Like honestly
one thought I had was I wonder if Nvidia
is already or sees this and will have a
little skunk works team go off to the
side and say white sheet uh design and
do the same. let's stand up a chip in a
year and maybe don't worry so much about
CUDA and legacy stuff, but like hey,
what if we internally built our own XPU?
What design decisions would we make and
how quickly could we make it?
&gt;&gt; Yeah. Yeah, that would be fun to see.
[laughter]
&gt;&gt; Yes.
&gt;&gt; And then I also thought um Yeah,
totally. Oh, uh Opening Eye hasn't gone
public yet. Maybe Nvidia could just buy
them, [laughter] but I'm just kidding.
&gt;&gt; Stop it. No, no more no more $20
million. Okay. Yeah, I'm kidding.
&gt;&gt; Okay. Okay. We'll we'll so many stuff to
buy and yeah there's there's so many
like what's AMD's path now
&gt;&gt; [snorts]
&gt;&gt; uh what's forget about AMD what about
Anthropic what's anthropic going to do
right I mean
&gt;&gt; where's the where's Antropic's chip
&gt;&gt; Anthropic correct they have a team um
and so you know Anthropic we'd love to
have you on to talk more about it but of
course OpenAI we want to have you on
because you just shipped at hot chips
and you have uh chip in hand of course
so uh There's so much more to talk
about. I I think even the the chip and
system itself, we didn't even touch on
everything, but obviously the AI angle
is just kind of mind-blowing. And and to
your point, Vic, just um this is
ultimately good for EDA in that it just
goes to show that small teams can use AI
and use their knowhow and bring
competitive chips to market quickly. Um
so, you know, there's going to you could
argue that the barrier to entry maybe
kind of lowers in some sense and
therefore more EDA is going to be used.
We would love to talk to EDA companies
as well to get their two cents a lot. Uh
that 2027 is going to be very
interesting.
&gt;&gt; Totally.
&gt;&gt; So with that, we'll cut it here. Uh
thanks everyone for listening to
Semi-Doped. Thank you for sharing us on
X. Thanks for all of your comments on
YouTube. Um share it, tell a friend,
send Go ahead. Oh, no. I wanted to add
like I met so many listeners on uh you
in person actually at Hot Ships and it
was like amazing like I was so humbled
to hear like so many of you enjoy the
podcast. So, so everybody who like
actually spoke to me in person, thank
you.
&gt;&gt; I love it. And with that, um you know,
send us your feedback and we'll talk to
you next time.
