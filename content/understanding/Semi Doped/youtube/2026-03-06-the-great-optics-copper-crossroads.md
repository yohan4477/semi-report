---
source: https://www.youtube.com/watch?v=47cQTPjDUB8
vid: 47cQTPjDUB8
title: The Great Optics-Copper Crossroads
date: 2026-03-06
duration_sec: 2897
channel: Semi Doped
kind: transcript
---
Oh, wait. 200 gig. Yeah, we can do that
in copper, no problem. And then he also
drops the bombshell saying, "Oh, by the
way, we can also do 400 gig 30s, which
is like years away. Like we're not even
talking about it right now."
&gt;&gt; Welcome to another Semi-Dope podcast.
I'm Austin Lyons of
So, uh Vik,
a lot to talk about today. Let's quick
plug our newsletters, and then we'll get
into it. Um for listeners who don't
know, we write Substack newsletters, uh
hit on some interesting topics this
week. Vik, uh
you wrote about decode hardware for
inference, and specifically how Groq's
LPUs could fit into the mix for Nvidia.
Um I thought it was pretty level-headed.
You know, there's a lot of people on
Twitter kind of going crazy with all the
possibilities of what Nvidia could do
with Groq. And I The way I read your
article was like, "Guys, it's only been
2 months. Uh there's probably not going
to be some sort of crazy engineering
announcements at GTC because literally
it's been 2 months." Um but yeah,
what what maybe a really quick like
high-level take uh on your side?
&gt;&gt; Yeah, so the
I wasn't going to much write about this
at all, but somebody on X suggested
like, "What do you think like they're
going to announce in GTC? Like do you
have any ideas of
what will happen uh with their
acquisition of Groq? What are they going
to do with that chip? How is it going to
change things?" And then I started
looking at it, and then I one thing led
to another, and I had so many things to
talk about in the article.
Um
and so basically the idea is like, yeah,
they got this chip called the LPU from
Groq, uh which is like a Christmas Eve
announcement last year. And then
they
uh uh it uses this unique architecture
that is very deterministic. We spoke
about it on our very first podcast
episode Uh and so if anybody wants to go
back and listen to that, I highly
recommend it.
So yeah, all the details are in that
episode, but basically what can Nvidia
do at this point? It seems like they can
put all those chips into a rack and
stamp it something like Nvidia branded.
People think it's going to be called the
LPX. Might as well be, but if it's
called something else, whatever. But
yeah, basically I think it creates the
missing piece of the puzzle that Nvidia
has been building up to because in last
GTC they introduced the Dynamo, you
know, inference software platform where
they basically
that software handles the disaggregation
of prefill and decode. It handles the
movement of KB cash, all of that kind of
stuff. And then late in September, I
think last year they announced the CPX,
the chip for prefill only, which uses
GDDR and not HBM.
And
because, you know, prefill is more
compute bound. And then the missing
piece of the puzzle is like you need now
decode specific hardware, which is
almost entirely memory bandwidth bound.
It's not compute bound. And how do you
get the best possible memory bandwidth?
You don't go off chip. And the only way
to not go off chip is to use SRAM, which
is what the Groq chip does. So this is
the missing piece of the puzzle, but
then I started imagining what other
companies should be doing or you know,
what AMD should do, things like that. So
yeah, so that it ended up being a fun
article to write. So I really enjoyed
writing it and think it's been doing
okay.
&gt;&gt; Nice, nice.
This reminds me. So when you talk about
last GTC in the introduction of Dynamo,
that was the start of a shift that's
happening where it used the narrative
used to be, oh, GPUs, they're very
parallel processors, so they're better
than CPUs, but they're supremely
flexible
and Nvidia has CUDA software libraries
for everything. So, everyone should use
GPUs.
And and yet and and then when there were
companies who came out and said like,
"Oh, we're going to build, you know,
XPUs or AI ASICs." Everyone's like, "No,
no, no, those are those are not flexible
enough. What are you doing?" Um, but
interestingly,
uh
a year ago already, Nvidia basically, by
introducing Dynamo and saying, "Oh, you
should actually put parts of this
workload on different hardware, prefill
and decode." And then later coming out
with a skew for um prefill, uh that's
actually Nvidia like shifting and
saying, "Wait a minute, actually it
makes sense to optimize your systems for
particular workloads. Transformer-based
inference is here to stay, it's growing,
it's massive, and it's actually worth
optimizing for." And
I I know that um
they might not come out and say it so
broadly, but that has really kind of
ushered in this year, especially the
past 6 months, where now all of a sudden
we're talking Groq, we're talking
Cerebras, Tachyum, Edge Matrix, and all
of and and of course, uh even just like
um NTIA or Maya or AMD's Helios. And
it's like a proliferation
of hardware from other vendors. Of
course, some of that's due to
uh supply and demand, um but I really
think it actually, in hindsight, also
really started to usher in when Nvidia
themselves came out and showed Dynamo.
So, I know, conversation for another
time, but again, what you're writing
about just has me reflecting on like we
are in a new era where it actually makes
sense for inference especially to have
hardware tuned to specific requirements
and specific workloads.
&gt;&gt; Yeah, so I wanted to tell you three
things about this, basically.
First thing is that
uh yeah, GPUs are really not the best
thing for all parts of inference because
during the decode phase the GPU is
sitting idle basically and it's like a
big waste of time, you know, it's like
this is not like a one-size-fits-all
thing. So, clearly that that came into
this pre-fill decode disaggregation
concept. So, that's one thing.
The second thing is that
uh
basically
it's
came about because I in a sense like
China had all these export restrictions
at one point.
And uh they, you know, I think Jensen
mentioned this in last GTC. He said
that, "Wait, people are using the H800
for pre-fill which was more memory
limited
and they were using the H80 for decode
which was more compute limited.
&gt;&gt; [laughter]
&gt;&gt; Right? And he was like, "Wait, what's
going on?" So, it turns out that like a
bunch of papers uh before that
uh that
uh
mentioned like it's called uh
uh uh anyway, I forgot the names of the
papers themselves but
uh yeah, DisServe was one of them.
DisServe was one of them. Uh and they
basically these papers explain how you
can use these different topologies to do
this. So, you know, it kind of comes
about from the whole thing of of this
doing it this way.
&gt;&gt; Fascinating. I I never realized that the
export controls which created different
SKUs where they're trying to clamp down
on China's abilities and so therefore
you have one SKU that, you know, that
maybe with more memory and one SKU with
less memory um
forced the innovation to say, "How can
we best distribute our workloads across
these
for pre-fill and decode?" And I think,
you know, we'd get there anyway but it's
interesting how geopolitics played a
hand in shaping where we are today.
&gt;&gt; Yeah. And um the last thing I wanted to
say about this was that uh um
it is actually a backtracking like you
mentioned about how Nvidia has has been
beating the GPU drum. They've kind of
backtracked now into like you separate
hardware for each kind of thing and then
they were also beating the like the GPU
better than CPU drum. Now that has also
changed around and now everybody is
wanting CPUs. So it's all like going
backward in time it seems like.
&gt;&gt; Yes, it's um
I don't you could call it a pendulum or
maybe sort of circular like what's old
is new, you know, CPUs are dead and now
it's like long live CPUs.
&gt;&gt; Yeah, yeah, yeah.
&gt;&gt; For sure.
&gt;&gt; Now I want to actually also mention what
you wrote this week because uh like we
may we spoke about a lot of companies
last time and how all these companies
are doing like Lumentum and Coherent are
making all these lasers and Indian
phosphide lasers which everybody wants.
But what was interesting about what you
wrote is basically Broadcom is actually
one of the biggest supplier of lasers
and I think the reason you don't see it
being talked about so much is because
they don't sell externally.
And they use it for their own products
and they are so vertically integrated
and self-contained so that you know,
other people are not going to have
access to that laser source. Is that
right?
&gt;&gt; Yes, yes, exactly. Um
it's a really good point and I frankly
didn't even realize it myself for that
exact reason until I had someone reach
out and say, "Hey, sharpen your pencil
on this." Um
and yeah, as I did a bunch of research
and wrote about it, yeah, I was shocked
but it makes perfect sense. It's like,
"Okay, Broadcom has great switches, you
know, great
transceivers or you know, um
all sorts of great digital logic chips
and inside of it they actually built are
fully integrated and not only building
the logic which we focus on
and the switching but actually the laser
components themselves.
&gt;&gt; Yeah, it's a good piece. I think people
should go read it. I I learned a lot of
stuff out of it actually.
&gt;&gt; Oh, nice.
&gt;&gt; about how Broadcom has all these
facilities and where they make stuff and
you know, how they diversify supply
chains and yeah, it's amazing. I liked
it a lot. So, I think it's a good
article.
&gt;&gt; Oh, thank you. Yeah, you know,
it's fun to ramp up in optics as you
know, the world is always changing.
There's always more to learn and it's
fun to have an excuse to dive deep and
share it here with folks and write about
it. Definitely.
&gt;&gt; Yeah, speaking of going backwards in
time and the world changing,
what what
what did you see the whole thing this
week about how it's like all optics
optics all over the place and then
suddenly oh yeah, copper is here to
stay.
&gt;&gt; Yes, yes. So, this week Monday some big
announcements from Nvidia investing in
Lumentum and Coherent. So, so the
you know, optics bulls are out there
you know, beating their chest and saying
I told you so, it's all optics. Here's
Nvidia you know, locking up supply and
then
last night Broadcom's earnings on on
Wednesday
Hock Tan was was very pro copper and
just like hey, we have great serdes and
we want to use copper as long as
possible which is funny because they
also make CPO switches
but and we'll we'll get into all of this
and then of course now all the copper
folks are like
yo and I think Credo was big time after
hours and Lumentum and Coherent were
down and everyone's like see, I told you
copper still has legs. So,
set the stage like we should talk about
that today.
&gt;&gt; By the way, I'm one of those the latter
guys who was like I told you copper's
here to stay. I told you copper. You
know, I never like believe physics-wise
copper has reached its limits. Anyway,
we'll talk more about it. But basically
what is happening is this, right? We
have had so much news over the earnings
calls of all these companies that have
reported in the last month or two,
Lumentum, Coherent, and everybody's
like, "Oh, the laser is sold out. Indian
phosphide is all the rage, and
we can't make these things fast enough.
We have like a 30% back like like, you
know,
waiting line, you know, people are
standing in queue for this stuff, and we
can't make these things fast enough. The
wafers are too tiny. They are not 3 in.
But, 6 in isn't yielding well. So,
everybody's been thinking, "Okay, wait.
So, optics is here, right? Like,
definitely, right? Look at the backlog.
Look at the revenues. Look at the
projections of all these companies.
Everything is growing like 100% or more.
And
then Nvidia comes along and says, "Oh,
how about I invest 2 billion
each for for Lumentum and another 2
billion for Coherent, you know, because
we love lasers, right? Nvidia loves
lasers, too, apparently." And then,
well, we In each of these earnings
calls,
these companies went and said like, "Oh,
yeah, we like scale up is now going to
go to optics because that's where all
the orders are coming from." And then
when Nvidia invests 2 billion into each
of these things, you immediately look at
it and go, "Obviously, like scale up is
now obviously going to optics, right?
Look at Nvidia's money. Why would they
put the money down?" So, anyway, that's
where the people's mind was until like a
couple of days ago where
two companies reported earnings like in
almost consecutive days, I would
imagine,
which is I think Credo followed by
Broadcom.
&gt;&gt; Yeah.
&gt;&gt; Credo goes, "Oh, no, like copper is
going to have a long life still, like
AECs are
doing great, like active electrical
cables are doing amazing. So, what's the
problem here? Why do we need
You know, we've heard this CPO story for
many years. I don't think it's going to
come anytime soon. Like, you know,
they've been saying this even in the
last earnings call. CPO, oh, we've heard
that song. We we've heard that song into
so many different names. You know, this
is just another phase. Whatever. We've
heard this. We've been around the block.
And then then Hock Tan shows up and says
something like really amazing. Like he's
like, "Oh, wait. 200 gig? Yeah, we can
do that in copper. No problem. 200 gig
per per lane translates to 1.6 T."
You know, which is even now just only
ramping up. And then he also drops the
bombshell saying, "Oh, by the way, we
can also do 400 gig serdes, which
translates to 3.2
like generation. 3.2 T, which is like
years away. Like we're not even talking
about it right now." Anyway, so this is
how this is where we are, right? This is
the landscape of
optics first. Yay, everybody's going to
scale up. All these optics companies. We
spoke about AXT. The company doesn't
even make any money, but it's like up
like 1,000%. And then then comes like
these companies and say, "Yeah, yeah,
yeah, copper." Right? So that's where we
are.
&gt;&gt; Totally. Totally. And you know, I think
kind of what you're pointing out is that
every company has a different message
and framing. And
no one is saying that they'll never be
optics for scale up ever, but it's all
about timing. And if the optics and and
I think that's where
maybe a lot of investors are investing
heavily if they think that the timing is
like it is happening right now. Optics
for scale ups like it's coming in 2027.
All the I should invest in these
companies and get like ride the wave. Um
but then the copper companies to your
point, uh Credo, you know, Bill Brennan,
I think he had a quote exactly to what
you're saying, which is like, "Show me
the CPO deployments. Oh yeah, there are
none. Okay, next." You know, uh
and and [clears throat] now to be fair,
Credo's uh investing in optics for scale
up as well. Um but they're they're
building out a portfolio and they're
staggering it in with respect to time.
So, it's like you know, again, it's
still like, "Dude, we're still just
deploying like we're literally deploying
800 gig copper still right now, you
know, and 1.6 will come and and these
things will happen over time." And then,
yeah, to your point, I think Hock Tan
surprised everyone and said like, "Hey,
maybe that timeline when everyone
thought CPO scale up was like '27 or '28
and and maybe it's actually even later
into 2030." And so, I think the the
correct thing to do when interpreting
all this information is to think about
the incentives in this company's
business models. If you're a CPO company
or you know, any sort of optics company,
of course you're going to say,
"Yes, it's coming. It's immediately
coming." And and to be fair, they are
talking to customers and customers are
probably saying like, "Yeah, we like get
ready. We want to do it." Right? So, I'm
sure from their point of view and from
the people their set of customers they
talked to, I'm sure they are working to
that end. So, I
I would assume that no one's like wrong
per se. And then on the other end,
obviously, you know, Credo has customers
who are who are telling them, "Yeah,
we're going to continue to deploy your
active electrical cables." And so, it is
that tough like mental state where I
don't think there is like a black and
white right or wrong, a certain date
that everyone agrees on. But, there's
all sorts of moving components, moving
pieces. And really, it is all about like
the you know, five kind of hyper scalers
at the end of the day depending on how
you count it and their deployments. But,
even they are deploying different
technologies in different places at
different times. So, you just have like
all these moving parts. You kind of have
to wrap your head around all of it and
then zoom out and sort of get a sense
for it's really a sort of like again an
adoption or deployment curve of like And
we've been talking about this like the
stacking S-curves of you know, 800 gig,
1.6, and eventually 3.2. So, it's kind
of knowing like who's deploying what,
where, and at what scale.
&gt;&gt; Yeah. By the way, by the end of this
episode, remind me if I don't say this,
but I have a total 4D chess move
hypothesis conspiracy theory for why
Hock Tan is all about copper when he is
actually a CPU company guy. So, you
might Interesting.
&gt;&gt; Okay, yes. Well,
&gt;&gt; Uh we can only explain that when we go
through whatever we have to say because
otherwise it would not make any sense.
So, I think we should first begin with
why like in video
is investing into these companies. Kind
of dig into that a little bit and then
we'll hit up a little bit of the copper
stuff and then I'll give you my theory.
&gt;&gt; Okay, perfect. I just made a note on my
side. Think 4D chess at the end.
&gt;&gt; Yeah.
&gt;&gt; All right. So, should we start with
start let's start with Nvidia and their
news $4 billion on optics?
Um so, you know, I think what's worth
maybe zooming out to the question is why
would Nvidia invest in in Lumentum and
Coherent? In my head I always say light
by the way. Lumentum's ticker, you know.
&gt;&gt; [laughter]
&gt;&gt; Yeah. Um and I think it's worth
reminding people, you know, if we look
at Nvidia's optical supply chain today
for their 800 gig and 1.6 T transceiver
vendors, actually
um
if you look at like the the Grace
Blackwell generation, the 800 gig
transceiver was uh I think my notes say
like 40% of the share is actually a
company called InnoLight, which people
don't talk about much because cuz you
can't really invest in it if you live in
America, I'm assuming because it's a
Chinese company. And so, um
they they are a major supplier of lasers
for or transceivers for uh
Nvidia and I think they have the first
1.6 T qualification with Nvidia as well.
Um of course, Lumentum and Coherent also
are vendors and suppliers for Nvidia. Um
and then I I found a note somewhere and
I need to understand this better, but it
seems that Fabrinet, the contract
manufacturer we talked about
an episode or two ago, um they also
build
Nvidia-designed modules. So, maybe you
would call that like a white box module
or something.
Um
And and
&gt;&gt; Fabrinet is the one who provided
most of Nvidia's optics, actually.
&gt;&gt; Mhm.
&gt;&gt; And Fabrinet's
assembly, I think, happens in like
Thailand, I think.
&gt;&gt; Yes. Yes, exactly.
Um so, I wanted to quick hit on this to
set the framing that maybe something
like, you know, 40-50% of Nvidia's
transceiver volume runs through China. A
lot of it, yeah, might run through
Thailand. And and therefore, in the big
picture of export controls, tariffs,
geopolitical risk, that would be part of
Nvidia's supply chain that is at risk to
export controls.
&gt;&gt; Mhm.
Actually, for them, it's just like they
want to have all these purchase
commitments. They mean they they have
multi-billion dollar now purchase
commitments, right? And what it gives
them actually is like future capacity
access for when they need it. And and
interestingly, both these deals
are not only multi-year, but they are
non-exclusive. And Nvidia is kind of
known to do this. You know, the reason
is they don't want to actually acquire
this company for two reasons. One,
nobody wants to deal with antitrust
stuff.
&gt;&gt; Yeah, totally.
&gt;&gt; monopoly. Anyways, big enough a company
for so much trouble. So, the second
thing is that they want to enable
multiple providers like this and then
have put them to a price war against
each other.
Because this is exactly Nvidia's
playbook when it came to HBM. Because
initially,
um SK Hynix was the dominant HBM 3E
supplier. And Samsung was struggling
with yields. So, what Nvidia actually
did was they championed Micron as a
third supplier. They gave them specs,
validation support, all of that
qualification. They did all of that
stuff. Um of course they did not invest
equity like like they did here. But they
gave them so much and encouraged them so
much to make HBM that now it ended up
being a three supplier ecosystem which
is much more healthy and better pricing
and better dual sourcing, so many
benefits.
&gt;&gt; Totally totally. Okay, interesting. So,
you're saying uh besides the
geopolitical angle that I raised, one,
they just want access to capacity and so
whoever can supply lasers, awesome.
That's great. Let's talk. But then two,
the more suppliers to some extent, maybe
three is the magic number, um
then the more like benefit to Nvidia in
terms of price competition. Yeah. And
therefore lower prices.
&gt;&gt; They have They are known to do one other
thing and they did this with CoWoS
basically, chip on wafer on substrate uh
packaging. Because when the Hopper
series chips were in like high demand,
what they did was they went and like uh
pre-bought
a lot of commitment from TSMC. So,
Nvidia is like this, when they sense
they're like hounds, you know, when they
sense a little bottleneck somewhere,
they immediately go dump repayments and
they secure supply before anyone else
can. So, this is standard Nvidia
playbook when it comes to this. So, what
it means here for optics is yeah, it's a
big demand uh signal.
&gt;&gt; Yes, yes. And uh to your point, I think,
you know, whenever we see news in Asia
taking pictures of Jensen at street
market eating noodles or drinking beers
with his vendors, it means he's over
there
locking up capacity. That's usually like
&gt;&gt; And when he's not there eating like
fried chicken, uh he's always at a
Denny's and I saw it on one forum
saying, "Why is he always in Denny's?"
That's because like Nvidia was started
in a Denny's.
&gt;&gt; Right. Right. Totally.
Yeah. Some some good history. I need to
visit the original Denny's.
Um Oh, yes. So, okay. So, back to the
supply chain or the
geopolitical angle, I noticed that in
these announcements both Lumentum and
Coherent talked about US manufacturing.
Um Lumentum in fact, I think announced
for the first time that they were going
to
use this money, or maybe not directly
use this money, but in this announcement
they said that they will be investing in
a new US fab. And then, uh you know, Co-
Coherent talked about building more US
manufacturing build out. They already
have a Sherman, Texas fab. Um but it did
seem
at least maybe it was just for the
administration to read, but it it it
very much felt like Nvidia was trying to
invest in its partners and they went and
talked about US-based manufacturing. So,
I think all of these are probably true.
Getting, you know, price competition,
supply, and uh US-based manufacturing.
&gt;&gt; Yeah. Uh I would also add a couple of
more things to it, which is basically
CPO.
Because word on the street at least, I
don't have any specs and I was planning
to look into this.
Uh is that
Lumentum's 200 gig EMLs, or externally
modulated lasers, are the best in the
world. They're the top-of-the-line. I
have no idea how they compare to
Broadcom. I would imagine Broadcom's
lasers are actually very competitive. I
would not like put it past them at all.
Except that nobody knows I publicly what
those lasers look like, I suppose. If
they don't release it or sell it to
anybody, how do you know?
&gt;&gt; Yeah. Yeah. You just have to buy the
transceiver and rip it apart and try to
reverse engineer test it.
&gt;&gt; it. Yeah.
But but CPO is different because you
don't need that modulated laser. You
need a CW a continuous wave laser in
in that particularly because there is no
modulation involved. Uh it's actually
simpler to make. The difficulty comes
from the high power it requires. So,
both Lumentum and Coherent actually have
very competitive CW lasers and
you know, Lumentum makes it on 3-in and
Coherent is
I think still ramping 6-in
which they will eventually get to. I
mean I don't I don't have a doubt in my
mind. So, this is a very good source
dual source of uh CW lasers for CPU.
Right?
So, the second thing I the second thing
that matters to Nvidia here is uh
optical circuit switches
because Lumentum's has this R300 which
is basically a MEMS-based mirror that
does the switching and uh the Coherent
has a slightly different technology
which is based on like uh
I think uh
crystal liquid crystal technology.
&gt;&gt; Yes. Yes.
Yeah. No moving parts.
&gt;&gt; No moving parts, right?
Uh so, yeah, I don't know if which is
really the better approach here, but
anyway, it gives uh Nvidia uh an option
to integrate one or the other or both
because they have now access rights to
so many things with this investment,
right?
&gt;&gt; Mhm. Mhm.
Totally. Okay. So,
that's optics and the early
announcements in the week. Should we
jump to Credo?
&gt;&gt; Yeah, yeah. Credo Credo first
uh and then we'll hit up uh Broadcom.
&gt;&gt; Oh, yeah, Broadcom. Sure, totally. Okay,
so Credo
&gt;&gt; Almost chronological order.
&gt;&gt; [laughter]
&gt;&gt; That's funny. Uh
they had a monster quarter
um
you know, I think what their revenue was
up 52% quarter over quarter, 200% year
over year. And I will say all of these
components companies are basically have
revenue risk concentration in it revenue
concentration risk in a sense where of
course they have like three or four or
five big customers.
Um
that's just part of the nature of the
game right now.
I think it's fine, but what it can
mean is like lumpy quarters. Like, oh,
Meta is ramping hard this quarter, so we
have a ton of revenue. Or someone got
delayed a tiny bit. But if you zoom out,
you know, I think you can get away from
the lumpiness looking at year over year.
And so, you know, when you see 200% year
over year, that's that's pretty good. Uh
obviously Coherent not dead.
Um
their gross margins were good. Uh you
know, almost 70% pretty not again, not
too shabby for a a component supplier.
Um I think they got dinged by Wall
Street because they were guiding gross
margins down to 64 to 66%, which still
sounds pretty good to me. But that's
kind of a mix shift that they were
forecasting as their optics ramps.
Um
their margins are going to come down and
that's just the nature of it.
Um but I think, you know, probably the
quote and then I'll hand it off to you.
The quote that stuck out to me was uh
the CEO Bill Brennan was talking about
how they've grown 6x in 2 years. And he
said few companies in semiconductors
have scaled at that pace.
So, it's like, yeah, totally.
&gt;&gt; Yeah. And I also like this other quote.
I wrote it down. He said, "There has
been a bit of a signal-to-noise ratio
issue in the market. And the noise right
now is dominating the signal."
&gt;&gt; [laughter]
&gt;&gt; All right. So, what a what an
engineering way to say that everybody is
talking trash.
&gt;&gt; Yes, I love it. I was just going to say
the same thing. Like, engineer by heart.
SNR. That's great.
&gt;&gt; SNR is how you say like people are
talking trash. Anyway, yeah, so they
their miss their basic uh premises that
copper is here to stay and AECs uh
electrical active electrical cables are
basically their cash cow at this point.
And in listening to the entire earnings
call, there's like one word that keep
kept coming back over and over again
with what Bill Brennan was saying, and
it's reliability.
&gt;&gt; Mhm.
&gt;&gt; This is like a core thesis to what a
Credo does. And the reason is they have
these uh telemetry devices. So, what
these things do is they essentially
monitor the health of the cable. And
they have like a software platform in
which you can like monitor uh which
cable is going down, you know, how many
cables are in a data center. So, you can
actually see all of them and see like,
"Oh, this one's failing, you know, it's
only 80% health or whatever." I don't
I've not seen the dashboard, but I'd
imagine it's something like that. And
so, what you can do is before it fails,
you can like preemptively take it and
fix it.
And that's fantastic. Right? Like So,
reliability is their really their key
thing, and that extends to their uh
optical play, which they call zero-flap
optics. By the way, a flap in
uh
in a data center in a networking sense
is when a link goes down. Like if a
cable fails at that Think of it like one
cable like came off the you know, switch
port is like flapping around. You know,
that's it's like what it has come loose
and it's flapping around. That's what it
is. So, zero flap means it doesn't flap
around and it's always connected, right?
So, they are applying the same telemetry
uh and reliability metrics to optics uh
for scale-out. This is not scale-up, so
these are all pluggable optics for
scale-up.
And those are still being used, by the
way. So, and he said that like, you
know, AECs and copper uh
are actually used both within a rack,
outside a rack, for front-end
networking, you know, all of this stuff.
Like it can be used everywhere, right?
And so that is their their major thing
here as to why copper is still working
um and is going strong.
&gt;&gt; Yes, yes. So the reliability angle is
pretty huge. There was a really nice
talk um
that Bill Brennan had with
uh an an engineer from uh OCI Oracle
Cloud, whatever I stands for. I don't
know what I stands for.
There you go. Oracle Cloud
Infrastructure, thank you. Um
and he was talking about that basically
um Oracle was trying to build, you know,
a huge GPU cluster and and that these
link flaps uh and and failures and just
kind of running blind to these failures
until they happen was like the biggest
problem that they had. And so they
actually kind of co-engineered
some of this telemetry together to try
to give large clusters, especially for
training,
insights into uh
when there would be issues like
preventative maintenance in a sense. But
then of course, if you can replace
optics
at short reach with copper, there's just
a lot less
there's no lasers and a lot like fewer
parts that can fail. And so yeah,
reliability's a big thesis. And and to
um Credo's credit,
we're getting like a densification of
compute going from 72 GPUs in a rack,
you know, to 144 or maybe 576 or
something. And so
actually more and more GPUs and switches
are getting closer and closer. Um so
kind of coming within the reach of
copper, 3 5 7 m.
Um so that's definitely helped like
helping sort of
I think I saw there was an attach rate
that was mentioned in in maybe two
earnings calls ago. That was something
like or maybe it was at a conference,
but it was like 1.5 to 5 plus AECs per
GPU depending on the the data center and
their configuration. So, I thought that
was pretty crazy like five AECs per GPU.
That's a lot of Credo content.
&gt;&gt; Yeah, yeah. Yeah, and so the reach is
like between 3 and 7 m within a rack and
that is a very important number because
that dictates like you say whether you
can you know even go outside the rack or
is like what is called very short reach
which means it's like within the rack.
Um very short. So, it really depends on
the speed. So, when you're talking about
100 gig per lane or 800
yeah, 800 gig
uh
links
they are actually ready today. They're
they're already doing that and in
copper, no problem.
200 gig also works in copper. They are
saying that the 200 gig AECs are ready.
And I believe them because I've seen
like Marvell has this Alaska DSP that
also does it.
And um
the the other thing I want to mention is
that whenever you think say AEC, then
you think about the the Nvidia uh
like rack in VR 72.
Where there are no AEC cables there,
right? They're like passive copper
cables that go through the spine.
&gt;&gt; Yes.
&gt;&gt; So, I've always thought about this and
be like how are they doing that like
even
I believe that there is there is this
kind of signal conditioning that happens
at the switch silicon level
uh where you do equalization and error
correction because you just can't do it
across a scale of a rack if you don't do
it in the silicon. So, when we say AEC
here, it's only because it's like
Credo's marketing term, but in in
theory, you could do it anywhere, you
know? So, it's basically still copper.
&gt;&gt; Gotcha. Yeah, so you're saying
even if it looks like it's just like oh,
pure copper or a direct attached copper
if you will, uh a copper black flame, um
it there's actually got to still be
conditioning happening which is
conceptually the same as an AEC.
&gt;&gt; Yeah, if you're running 200 gigs across
a rack, it doesn't matter whether you
call it a a direct attached copper or
AEC or whatever it is.
200 gigs, there is going to be some
equalization and forward
error correction going on. There is
simply no way you can do it without.
Simply no way.
&gt;&gt; Yep. Yep.
&gt;&gt; So, the thing is that it seems like the
reach of a 200 gig cable
for 1.60 communication is like 7 m.
Um
Oh, actually I think he mentioned it's
come down from 7 m at 100 gig to 5 m at
200 gig. I think that's what he said on
the earnings call.
&gt;&gt; Yeah, that's right.
&gt;&gt; Anyway, 5 m, right? It's pretty pretty
big. And if you think look up a look at
the racks, you'd say the the height of a
rack is I don't know, probably like 8
ft.
Uh I don't know. It's like about 8 ft.
So, yeah, that that is plenty of reach
for entirely a rack. And you know, you
need some amount of give. You can't like
have exactly 8 m of cable. You need like
12 ft of cable, right? So,
so 5 m would like definitely fit that
bill.
Yeah, so this is this is this is where
they are today. And they believe that
it's just just fine.
&gt;&gt; So, do you want to talk to about where
Credo's going with optics?
&gt;&gt; So, yeah, I mean, they they do have
their zero flap optics, but one other
thing they have is basically their
I don't know if you're referring to
their uh LED cables.
&gt;&gt; Yes. Yes. Yeah, ALCs I think they called
them active LED cable.
&gt;&gt; Yeah, yeah, they're based on micro LEDs
and they kind of somewhere between a
copper cable and an optical cable with
which uses lasers.
Now, micro LEDs are cheaper and somewhat
established technology from displays
actually.
So, you can put these micro LEDs and
then get pretty much or at least this is
what they claim, you can get the same
performance and energy efficiency as
what you get out of copper.
But,
you can get better reach. They say that
you can go up to 10 m in the near
generations of ALC and eventually they
will say that this can go up to 30 m.
30 m is like plenty. I think you can
connect the entire row with an ALC, if
that's true.
&gt;&gt; Yeah, it sounds like it. Agreed. Yeah,
so, you know, today AECs 1 to 5 m and
you know, I think they've been quoted as
saying a thousand more X reliable than
laser optics at half the power. Again,
copper if you can, optics if you must.
30 m plus zero flat optics. So, if
you're going to have optics, how can you
design it in such a way and use
telemetry and whatnot to minimize the
amount of downtime? And then in the
middle, 5 to 30 m, could we have this
micro LED based technology for or ALCs?
Um so, it'd be like AEC like reliability
but optical. Um so, that would be the
portfolio that that that they're working
on.
&gt;&gt; Yeah, but note that this is still
pluggable. Even if it's an ALC, the
entire the micro LED transceiver is a
pluggable transceiver.
&gt;&gt; Yes.
&gt;&gt; Right.
&gt;&gt; call out.
&gt;&gt; And what happens is I think they they
plan to do this in like FY 2028. I don't
think ALC is coming out anytime before
that. Um
Anyway, even if you say it's 2028, the
big question is if CPO shows up before
that,
it basically invalidates ALCs. You don't
need ALCs because your optics engine has
gone basically into the into next to the
silicon switch silicon. So why do you
need a pluggable ALC thing? You don't
need it anymore. So that that's the
that's the whole problem here. If CPO
shows up, it kills a lot of their
future, you know, plans here.
&gt;&gt; Totally. Totally. So yeah, that would be
something for listeners to track is when
you're thinking about when CPO shows up,
then you also have to be thinking about
for Credo when ALC show up. And ideally
for Credo, you'd like ALCs to show up
before CPOs.
&gt;&gt; Yeah.
&gt;&gt; Definitely.
&gt;&gt; Yeah, so this is a great time to jump
into a hot dance like shocking
statements.
&gt;&gt; Yes, let's hear it. 40 chess, what do
you think?
&gt;&gt; No, no, no. Before the 40 chess, I have
to tell you what he said.
&gt;&gt; Oh yeah, no, we haven't even covered.
Yes, you're right. We haven't even
covered Broadcom yet.
&gt;&gt; Yeah, yeah, yeah. So what he said
basically was like look, copper is going
to be here for scale.
It doesn't matter. Copper is going to be
used at 100 gigs,
200 gig.
Scale up is not going anywhere other
than copper.
And he said, I think the thing that took
everybody by surprise is what I
mentioned in the beginning of the
podcast.
400 gig
can work
um
across the reach of a rack, which I'm
guessing is like at least 3 m.
&gt;&gt; Yeah.
&gt;&gt; Right?
Over copper. And that's a that's a tall
claim.
&gt;&gt; [laughter]
&gt;&gt; It's a very tall claim. And he actually
claims that it is actually possible and
it's working in their labs right now.
But I know, I need to see the receipts.
I will be watching conferences.
&gt;&gt; Yes, there you go.
&gt;&gt; Yeah.
&gt;&gt; Totally.
&gt;&gt; So I want to see what he's talking
about. And what this means is very
important because if you can do 400 gig,
that's basically 3.2 T
um
uh technology with just like scale up
with just copper.
So, it's only now that we are even
ramping 1.6.
Right? And I think might only finish
ramping, I don't know, by 2028 or
something, 2029. So, the next generation
we like we are looking at is probably
2030 is when 3.2 is going to ramp.
And if copper works at 3.2
and everybody is happy with copper
because of the receipts Hawk is going to
bring
to a conference and I'm going to see at
some point.
Is that it's now 2032 because I would
imagine that if if copper works at 3.2
T, what's the problem? I mean, why would
you need to go CPO and all of that
stuff?
&gt;&gt; Right.
&gt;&gt; You know.
There is one big reason why CPO might
still come out even if copper works at
3.2 D. And that is energy efficiency.
How many picojoules per bit are you
going to burn
&gt;&gt; Mhm.
&gt;&gt; in order to make sure that you can drive
400 gigs over
3 m. That's very important question.
&gt;&gt; Yeah.
&gt;&gt; Because if CPO is lower energy usage,
they're going to go CPO.
&gt;&gt; Yeah. Sure. That That's a great point.
And I think we'll probably
hear a lot about the these tensions and
tradeoffs um because I was saying about
like, "Oh, if you're Celestial AI
acquired by Marvell or IR Labs or
companies who are
really betting heavily on CPO uh
photonic fabrics, that kind of thing, to
hear that it could get pushed out
another three or four years, I think
would be a tough place to be. But I
expect it they'll come out and counter
position and say, "Yeah, yeah, it could,
but at what cost?" To your point. It's
going to come at a huge power cost. And
so then, you know, there's going to be
conversations about power, about
reliability, and what's what's really
the constraint that we're trying to
optimize for.
&gt;&gt; Yeah, so that's very important to wait
and watch here. and I think everybody is
confused online that I can see is that
what's going on basically? Why is on one
side Nvidia investing all this money and
why is like everybody's like lasers in
short supply
and why Lumentum is like
you know, beating the drum on scale-up
CPO, but on the other hand we are
turning around and like saying that oh,
copper's going to stay here by the way
even Nvidia actually has said in the
past that they will use as much copper
as they possibly can.
&gt;&gt; Mhm.
&gt;&gt; Right? So, I think it comes from both
sides in the sense that
it makes sense for companies like
Lumentum and Coherent to kind of
make it interesting to investors and you
know, sell it up a little bit like oh,
yeah, scale-up is here. Look, look, we
are the best providers. So, you know,
they're a growing company and they need
to do that. Uh Hock Tan and Broadcom
don't. I mean, they can afford to be
very conservative.
&gt;&gt; Yeah.
&gt;&gt; He doesn't need to tell you if he sees a
CPO coming out in 2 years from now. He's
not going to say CPO is going to be in 2
years and we are going to change all our
product lines by the way. Right? He's
going to like announce it at the very
last minute. Until that time he will
remain in his conservative mode.
&gt;&gt; Sure. Yes. Yes, different business units
he might want to be less conservative
and more forward-looking like he might
say, "No, no, no, our XPU business is
doing great. Meta's actually ramping
even if people say they're not.
Open AI, we're making good progress with
them, right?" But I I agree that for
like his like transceiver business,
switch business, all of those like they
can afford to be conservative as the
industry leader.
&gt;&gt; Yeah, and he actually kind of did that
too because people were like asking in
the earnings call, "Hey, you know,
people are trying to make their you
know, bypass you and make their own
silicon." You know, like I think Google
is trying to do it with MediaTek or
something.
&gt;&gt; Uh-huh.
&gt;&gt; And customer owned tooling is the term
everyone uses.
&gt;&gt; Yes, customer owned tooling, right? COT.
&gt;&gt; Yep.
&gt;&gt; And yeah, and that the response to that
was like playing it up too, right? So,
Hawk goes, "Yeah, we are the best at the
silicon we do. Nobody can ever catch us
up." Something like that.
&gt;&gt; Yeah,
listeners should go listen to that part
of the conversation. It was fun. It was
very definitive where he's basically
like,
"Good luck. We're the I'm going to be
humble here, but we're the best and
you'll never catch us. So, nice Yeah,
let's see what happens."
&gt;&gt; Yeah, yeah, yeah, exactly.
Yeah, so anyway, so this is where we
are. So, now are you ready to hear my my
&gt;&gt; Yes.
&gt;&gt; my 4D chess move?
&gt;&gt; Let's hear it.
&gt;&gt; Okay. So,
the reason that my conspiracy theory
reason, by the way, totally not true
probably, but I thought it's fun to
think about, is that
ultimately
Look, Broadcom is a CPO
uh
ready company. They have CPO technology.
So, why would you play down CPO
technology and say copper copper this
copper that?
And the hype the the the conspiracy
theory
explanation to that is
you know, he does not want all the spine
switches to be replaced by OCS
because that would mean bad news for the
Tomahawk series. Now, the Tomahawk does
have CPO, but it's it's fundamental
operation is still like packet-based
switching cuz it's a silicon switch.
&gt;&gt; Yeah.
&gt;&gt; OCS does not do that. Like, if you think
about the MEMS mirror, it's just a dumb
mirror that just points light in
different directions.
&gt;&gt; Yeah.
&gt;&gt; And it is actually far less of power
because it does not have to make
decisions as to where things have to go.
And for a training run, for example, you
don't need to keep changing switch
orientations. I think we spoke about
this in a previous episode.
&gt;&gt; Yes. Yes, that's right.
&gt;&gt; So, OCS is good for that because the
GPUs at the spine level are kind of like
fixed. You know, you know which GPU has
to connect to which GPU, so you just
turn the mirrors in that orientation and
you leave them there. And that's just
going to work fine. And it's great
because spine switch replacement is like
a is is is I don't know if it's
happening. Like I hear it all over the
place. Everybody wants to replace spine
switches with OCS or something like
that. So, my hypothesis is that if it
all goes to optics, then
they can replace the spine switch with
OCS, which would spell bad news for
Tomahawk spine switches.
&gt;&gt; Interesting. Interesting. So, if it all
goes to optics, it's easier to just
start, yeah, switching out the Broadcom
spine switch for OCS.
&gt;&gt; Yeah. There's probably something
fundamentally wrong with my explanation.
I'm sure some people will let us know,
but anyway, I thought it's a fun
experiment to think of.
&gt;&gt; Interesting. Fascinating.
All right. Yes, listeners, if you have
thoughts, you know, definitely send it
send us. Um we get lots of good
insights, um some nice gentle
corrections. So, thank you everyone who
listens and and provides their thoughts.
And of course, if you have
uh arguments for Vic's 4D chess thinking
uh conspiracy theory, feel free to let
us know.
&gt;&gt; Yes. I'm happy to
uh be told how wrong I am. It's it's no
problem at all. So, please feel free to
leave that in the comments.
&gt;&gt; Awesome. So, all right, that's it for
today. We covered a lot of ground. Um is
it optics? Is it copper? I think it's
both right now. I think
uh the question is is always is a really
around timing. Um Nvidia needs optics
for scale out. They are working on CPO,
but they need copper for, you know,
Ethernet scale out, etc. Credo's doing
both. I think the name of the game is
both. Um
timing again. So, that's it. Thanks for
listening. If you have feedback, if you
have thoughts on
uh copper and optics, let us know. If
you're enjoying Semi-Dope, subscribe,
give a quick review.
YouTubers, thanks for all the comments.
We had a lot this week, so keep them
coming. Thanks everyone for listening.
