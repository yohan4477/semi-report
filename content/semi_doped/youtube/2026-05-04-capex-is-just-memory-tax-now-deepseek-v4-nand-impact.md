---
source: https://www.youtube.com/watch?v=SbRsmWZytsw
vid: SbRsmWZytsw
title: CapEx is just Memory Tax Now, Deepseek V4 NAND impact
date: 2026-05-04
duration_sec: 2753
channel: Semi Doped
kind: transcript
---
And the reason for raising CapEx has
always just been we need more compute,
we need more flops, we need more
intelligence.
This quarter there was something
different, which was
Hello everyone and welcome to another
Semi-Doped podcast. I'm Austin Lines
with Chip Strat and with me is Vic
Shaker from Vic's Newsletter. Hey Vic,
man, a lot has changed since the last
time we recorded podcast. What what's up
with you?
&gt;&gt; Yeah, a lot has changed. So after 15
years of working in the semiconductor
industry across like small, medium, and
large companies, I finally decided to
hang up that corporate hat and do the
Substack, this podcast um
full-time
and uh see where it takes us
&gt;&gt; [laughter]
&gt;&gt; you know, in the podcast front. And I
hope the Substack continues to grow,
too, because it is so much fun that uh I
figured like, okay, let's give this a
shot because
I learn so much from like writing and
you know, reading about so many
different things and uh corporate roles
tend to be a little bit more like
hyper-focused and I've spent 15 years
doing kind of the same thing. So I was
like, okay, instead of trying to trying
to change roles everywhere, I've kind of
managed to carve out this role for
myself. So I'm like, okay. I said, let's
try it for a while. What's the worst
that can happen? Let's try it.
&gt;&gt; Awesome. I love it. Yeah, so
okay, so you'll have more time
presumably for writing, podcasting,
researching. Like, what are you most
excited about?
&gt;&gt; Yeah, I'm just going to do the same
thing. Like, I'm not trying to
uh
add too many things because I think we
already added one other thing to the
Semi-Doped umbrella, which we haven't
really spoken about, which is
Semi-Doped also has a Substack presence
now and it is a free-for-all
subscription. It does not have paywalls.
And what uh Austin and I do here is uh
just we just give our daily take. So
this is like a once daily newsletter
that's short to read like within 3 to 5
minutes just with some key highlights of
what's happening in the day because we
monitor this stuff so much every day now
that we figured okay like there's so
much that goes like
unmentioned because
we can't write everything in the
newsletter and we can't talk about
everything on a limited time podcast but
not everything requires a full deep dive
Substack or a full hour podcast.
But if we try to stick it in the podcast
it gets fragmented. So the best place
for this kind of information but that's
also very relevant because
the the reason you sign up for the Semi
Doped Substack is that you know you get
you'll get one email a day you open it
up you know while you just have your
coffee you just like glance through it.
Anything that picks your interest you
just read that section or or not you
know you'll get another email the next
day and it's an easy read it's unlike
our deep dives on Substack it's just
highly researched and thought through
and all that. These are just like quick
hits. So that is that is the second
project that's common to us apart from
the Substack.
&gt;&gt; Yes yes yeah I'm excited about it. I'm
I'm looking forward to it it's been fun
this week.
You know I think for listeners
definitely go sign up. It's just
basically like
Vic and I having a quick water cooler
conversation and that you're part of.
You know hey here's this news from
yesterday Vic will give a take I'll give
a quick take move on to the next thing.
I think it'll be fun informative and
you'll just be more intelligent about
semiconductors and AI for reading it.
&gt;&gt; Yeah just semidoped.com should get you
there or you can just search for it on
Substack semidoped you'll you'll see the
same logo of this sub this podcast and
you'll find it there.
&gt;&gt; Exactly.
&gt;&gt; last thing that is like forming still in
my life is the fact that now I am
available to do consulting.
And my newsletter itself actually runs
under the umbrella of semi-exponent.
Which I came up as a name to say like
this is the most exponential technology
I like you know that ever existed. So I
was like okay semi-exponent is a nice
it's like you know what is the exponent
you know the exponent is zero means it's
a flat line which is never zero. So
anything above zero is like an exponent.
So I was like okay that's a nice name.
So the consulting arm is going to be
under semi-exponent. So
now I'm just starting to find you know
clients who want to work with me on
various different aspects of
semiconductors have chats pick my brain
on various aspects of what I write and
talk about. Ah we'll see how that goes.
Should be fun I like talking to people
anyway.
&gt;&gt; Yeah yeah nice nice. So you'll be
researching writing talking and
consulting. That that does sound like
plenty.
&gt;&gt; Yeah that's enough right. That's why
that's why I'm not doing anything to the
substack. Things will continue as it is.
And
I hope there'll be more research
involved because I have more time to
think through carefully a lot more
stuff.
&gt;&gt; Yeah totally.
&gt;&gt; I've always tried to maintain a high
high level of you know quality on the
substack. So hopefully if I've been
doing my job well enough you won't
notice any changes.
&gt;&gt; There you go. There you go. Love it. All
right let's get into it. So this past
week
you were on vacation.
There was earnings week they didn't wait
for you
um and but I stayed on top of it and I
know you you've caught up a lot on it.
Um so of course listeners I know you
know all about this. Microsoft Google
Meta Amazon Samsung Sandisk Seagate
Western Digital Qualcomm Cadence NXP
even Rivian which I I love to follow
even though they're kind of downstream
as like a semiconductor consumer. Um all
those companies reported impossible to
listen to all of it. Um, but we are
going to cover it and I thought the
angle that we could take is actually
starting with memory and storage
companies.
And here's why. You know, as everyone's
been tracking, the big four hyperscalers
have now committed to nearly 700 billion
of 2026 CapEx, which is up from roughly
500 billion just in 2025. So, they they
every quarter the story's always like,
"Hey, did they keep CapEx or did they
raise it even more?" And the reason for
raising CapEx has always just been, "We
need more compute. We need more flops.
We need more intelligence." This quarter
there was something different, which
was, "Yes, we're raising CapEx, but it's
because of
needing extra dollars allocated
specifically to cover rising component
costs. Memory is more expensive. Storage
is more expensive. Even things like
fiber and optics are are more
expensive." And so, I thought that was
an interesting sort of shift of like,
"Oh, yeah, we are increasing CapEx, but
it's just to pay not to buy more flops,
but just to pay for the things that we
already committed to."
Um, so
I thought it'd be fun to start with the
beneficiaries of this CapEx raise, which
would be the memory and storage
companies that reported. So, we're going
to start there. How How does that sound?
&gt;&gt; Yeah, let's do it. Memory and storage is
something I keep ranting on on the
podcast. Like, "How much more expensive
is it going to get? Like how much more
are they going to raise prices?" They
expect a price hike every time.
&gt;&gt; Mhm.
&gt;&gt; But if the price hike isn't good enough
now, they're like, "Oh, wait, you're
you're only doubling it? Why not? Why is
it not five times?"
&gt;&gt; Yeah, yes, yes, investors. Totally. It's
good that
&gt;&gt; [laughter]
&gt;&gt; Man, aren't you happy the prices are
going up? Not going up enough. Yep, your
stock goes down.
It's crazy. So, all right, let's start
with Samsung or Samsung Electronics. Um,
I I the number that stuck out to me was
that their memory revenue was up 101%
year-over-year, which obviously is
pretty crazy for memory.
Um they said as a company their Q1
revenue and operating profit were at
all-time highs. HBM sales are expected
to triple year-over-year in 2026,
and they expect HBM 4 to be 50% plus of
HBM sales by Q3. So there's a mix shift
going from HBM 3 3E to 4.
Um now, for people who haven't followed
Samsung as closely, in the HBM market,
um the story over the past couple years
was they used to
be there there's there's basically three
big players, SK Hynix, Samsung, and
Micron.
And Samsung used to be, you know, up
there with SK Hynix uh
having a lot of market share on the
order of even just
about this time, you know, last year, it
was uh maybe like or actually maybe like
six quarters ago that it was like 40%
market share for Samsung. And in 2025 it
dropped drastically down to like 13%,
15%, 20%. And so the story of Samsung is
fall they've fallen behind and now
they're trying to catch back up. Now, of
course,
there's always a new technology, HBM 3,
HBM 3E, HBM 4. Um and when a new
standard comes out, there's an
opportunity to try to be first to it and
and regain some market share. And so um
Samsung on their call, they were really
trying to position that like, "Sure,
uh the past is behind us, but we are
totally ready for HBM 4." And so I
thought I'd read a couple quotes quick
and then we can get into it. Um but they
wanted to make sure to say that they are
the first and they are the best around
HBM 4. So the quotes from the call, Jae
Jae-joon Kim, EVP of memory sales, said,
"After we became the world's first to
commence commercial shipment of HBM 4 in
February,
and then also he called out so so right
there like saying in passing like don't
forget we were the world's first um
shipping HBM 4, and then um
he said, "The differentiated performance
of our HBM 4 led to concentration of
demand, and our production ready
capacity is fully booked and sold out.
Our outstanding performance has been
translating into actual premium on
pricing."
So, the read through there is
there's always been a question around
memory, around storage, which is is it
is it just a commodity? A bit's a bit's
a bit, doesn't matter who it's from. And
here uh Samsung was trying to say, "Hey,
not only were first, but our performance
is the best, and that's why
and and we've got the capacity ready, so
that's why we're sold out. Customers and
that's why we're able to have a premium
on pricing is because customers prefer
us." Um
any reaction to that, Vic?
&gt;&gt; I remember this there was this whole
discussion about uh how many gigabits
per second uh
you can get out of HBM memory
by designing the base die for HBM 4 to
be uh you know, on a certain node.
Or even if it doesn't matter what node
it is because there was some discussion
that Micron was using a memory
technology to make the base die, while
the other competitors were like Samsung
and SK Hynix were actually using a two
logic node.
Um
the point is that the speed becomes a
differentiating factor. So, it's no more
memory is just memory.
Like
how how it performs is become
has become a very important factor for
like which company Nvidia or AMD will
pick for their performance. And not only
that, it comes the other way too. The
JEDEC spec
for HBM4 is like I think 8 gigabit per
second per lane.
But then, because they want supremacy on
inference performance and tokens output
and tokens per watt per dollar and all
that,
they are pushing the speed
per lane of HBM4 faster and faster and
faster. So, it's become a competition as
to who can get to like 11 10 or 11 and
or 12 GBPS per pin.
And that
is
not even is way beyond the spec, but it
has become
the thing that drives sales and drives
lock-in because once these hyperscalers
choose and qualify
uh HBM vendor, it is a sticky decision
cuz qualification, if you remember like
the HBM3, Samsung couldn't really get
qualified at Nvidia for a long time.
They'd so many yield issues and things
like that.
So, qualification and performance makes
this very sticky
uh and so it's not fungible. So, you
just can't take out Samsung and drop in
Micron tomorrow. Although, there are
only three companies doing this.
&gt;&gt; Yeah yes, and so assuming out and and
hitting on what you said again for
listeners, the the real interesting
thing is there is a spec, this JEDEC
spec, J E D E C, um
that defines
the performance level that and you know,
the various other things that the spec
define about how it's supposed to work,
how it's supposed to communicate, um
that these three companies are trying to
hit. And and normally, if everyone just
hits that spec exactly, it would be
fungible. But but what Vic is saying is
that, you know, Nvidia said, "Hey, wait
a minute. I've got, you know, I've got
to compete against AMD and against XPUs.
And if I could if you could give me Um
memory HBM memory that's even faster
then I can get even better, you know,
tokens per second, tokens per watt, that
kind of thing. And so actually, there is
a pull from the the silicon vendors to
the memory manufacturers to say, "I know
the spec says 8 gigabits per second per
pin or whatever. Um
can you go higher, right?" And so then
there's this interesting like someone's
trying to get to 11 and now the others
have to try to get to 11 as well. So
there's this interesting pull to go
faster and now this kind of like
unwritten spec that this performance,
you know, that they're all trying to
compete on and and so as you move away
from just everyone meets the spec, we're
all fungible to like how fast can you go
at what yield at what cost, it is more
of a a true competition on the things
that do allow you to have premium
pricing over commodity pricing, which is
which is performance, you know, and
yield and cost and that kind of thing.
So that's that's a little bit of the
story the back the back story here for
HBM4 and how Samsung is trying to regain
market share is to to truly compete on
you know, on performance. Okay, so
here's an interesting thing. Uh
as we move out of that looking at the
the competition there between the three
companies um and go focusing back on
Samsung, another quote that they had
was, "Our demand fulfillment rate is now
at a record low. Customers who are
concerned about supply shortages are
actually bringing forward their demand
for 2027 already."
So I you know,
not surprising, but again it's just
crazy to hear, you know, if customers
are asking for this much, maybe it used
to be like we could only give you 80% of
that or 50%. Maybe now it's even lower
than that. I don't know, I'm making up
the numbers, but trying to illustrate
the point that customers are asking for
a lot of memory and the memory supplier
is saying, "I can give you less than
ever." So that would be uh the
environment that we're in.
&gt;&gt; Yeah, that's crazy to me. Uh how much
longer is this going to continue?
Because people these hyperscalers are
increasing the capex just to pay these
memory companies. Literally, that's what
their capex is going into just to pay
these
players for HBM and like NAND memory and
things like this.
I'm not sure how much how much higher is
going to keep going. I keep thinking
that that's it, but I'm always wrong.
&gt;&gt; Yeah, you know, that's it's an
interesting point. We can get into it
more both here and and later, which is
I am very bullish on capex continuing to
get higher when it's buying more flops,
when it's buying more compute. Because
I, like everyone else, believe that the
more compute we have, the more
intelligence we have, the more we can
do. You know, I I too have experienced,
I'm sure everyone has, you know,
chat GPT or Gemini or Claude code just
spinning or saying like, "Oh, I'm busy
right now, you know, or like
come back, we've reached our limits."
So, that's frustrating, and that just
shows that like, "Dude, they need more
GPUs, they need more XPUs." But, this is
this is a different conversation when
it's like, "How high can you convince
your CFO to let capex go when you're not
buying any additional compute, but
you're just paying increased memory
prices?" Is that going to be the straw
that breaks the camel's back?
&gt;&gt; Exactly, because
if you if like you say, if all of this
money went into expanding compute, then
a lot more users
of AI tools or whatever get
actually something out of it. They get
better tools, they use it to build
better projects, that drives revenue,
that drives an economy. It It completes
the circle in some way. What is
happening now is if all the capex is
going to memory players, it's like
you're siphoning all this money out into
somebody's pocket. It's not going into
the, you know, positive reinforcement
loop that we want to see. So, this is a
bit concerning for me.
&gt;&gt; No, you're totally right. I mean, put
succinctly, there's no ROI on that
additional CapEx.
&gt;&gt; Except for a few companies.
&gt;&gt; Yes, yes. But, for the hyperscalers,
yes, there's no ROI. No extra ROI C,
return on invested capital. It's just a
tax, really. It's
&gt;&gt; It's a tax. Yes, it's a memory tax.
&gt;&gt; It's a memory tax. So, okay. Let's move
on. Um, so we're going to talk SanDisk.
So, we've talked when we talked Samsung,
we were focused on HBM, focused on
memory. So, let's talk um
uh other memory and storage. So, we're
going to talk SanDisk. But, really
quick, I thought I'd give a quick
history sidebar cuz we haven't talked
about SanDisk on the podcast yet. So,
um
SanDisk Western Digital, really quick.
They're two companies. Um, back in 2016,
Western Digital actually acquired
SanDisk for around $20 billion,
and the thesis, I think, back then was
having a full storage portfolio. So, can
we own both hard disk drives and NAND
flash, and that therefore we can sell
hyperscalers a complete stack.
Makes a ton of sense right now in the
era we're in, but
prior to AI, um that thesis didn't
really age well. I think they're they're
very different businesses. They have
different cycle dynamics, capital
intensity, customer mix. Um so
running them under one roof wasn't as
simple as like, "Oh, great. Um, we share
customers, and now we can more easily
cross-sell into them." It was actually
sort of like, "Uh, these are two
different businesses, and there's some
different customers at play, and we're
not getting the
quote-unquote synergies that we thought
we would."
Um, so back in October of 2023, Western
Digital announced that they were going
to split SanDisk back out, and by
February 2025, that spin-out happened.
SanDisk reemerged as a standalone
publicly traded company. And so, when
now when you think think SanDisk, you
can think about NAND flash, SSDs,
embedded flash.
Um they have a joint venture on some
fabs in Japan with Kioxia.
Kioxia, I'm not sure how to pronounce
that. Um and then so SanDisk, you can
think of flash, SSDs, etc. And then
Western Digital is a hard disk drives
only.
Um and they are working when I was doing
a little bit of research, Western
Digital is working on this interesting
next generation
tech, HAMR. HAMR, it stands for
heat-assisted magnetic recording and it
I never heard of it, but the goal is to
achieve 100 TB plus
hard disk drive capacities for AI-scaled
data and they're planning volume
production in 2027. Have you heard of
this?
&gt;&gt; Yes. So HAMR has been there for a while
actually. It's not that new.
&gt;&gt; Okay.
&gt;&gt; HAMR has been
cited about I've heard this at least for
like 5 years now.
Uh I can't pinpoint exactly how long
it's been around. So it's always been
the next uh you know, the next greatest
thing in hard disk drive technology.
But then what has happened recently is
that if you look at uh
you know, quad-level cell
SSDs, QLC SSDs,
those SanDisk ones, for example, the
highest capability, the highest capacity
one is five 256 TB and you get it in an
SSD form factor already. So I'm like,
what is this HAMR and is it going to
give you what, 100 TB? It's not not that
great. Honestly, today's day and age. Of
course, the price point will be lower.
It should be.
Uh but you know,
HAMR, yeah, it's it's been around, but
it's I don't know how relevant it is or
how where we are on that right now. But
I wanted to go back in the history a
little bit more. I think you'll find
this fun.
So the
Do you does the name like Sanjay
Mehrotra ring a bell to you?
&gt;&gt; Uh yes, Micron?
&gt;&gt; Yes, Micron, Micron.
&gt;&gt; Yeah.
&gt;&gt; Do you know who founded SanDisk?
&gt;&gt; That person?
&gt;&gt; Sanjay Mehrotra.
&gt;&gt; Serious? What?
&gt;&gt; Yes, yes.
&gt;&gt; What?
&gt;&gt; Yeah, it's true. He was He was one of
the, you know, founder you know, he was
one of the founding members of SanDisk,
uh, and you know,
this was like way before his he became
the CEO of Sand of Micron only 2017. He
was the original
&gt;&gt; Wow.
&gt;&gt; founder of Sandisk. So, he's like real
real memory guy. And another fun bit of
trivia on the name, right? Uh, one of
the other founders, um,
whose name I'm uh, Eli Harari, yeah.
He's uh, one of the other co-founders,
and so they've, you know,
they were trying to find a name for the
company or whatever, and then his
daughter comes in and it's like
looks at some of the discs lying there,
you know, you have these these these
platters or something. He's like, "Oh,
yeah, that looks like the sun."
So, they decided to call it SunDisk.
&gt;&gt; [laughter]
&gt;&gt; No way.
&gt;&gt; You can look up early logos of SunDisk,
and you'll see like a plate-like thing
with like the sun's rays like coming out
of it. That's their logo.
&gt;&gt; Serious?
&gt;&gt; Yeah.
We could put a picture if we find one.
&gt;&gt; Yes, we should. Totally. Oh, great
trivia.
&gt;&gt; Yeah, yeah, yeah. And what happens is
that later they like Sun Microsystems
came after them for some trademark stuff
like, "Oh, well, you can't use sun in it
or something." So, they changed sun to
SanDisk.
&gt;&gt; Okay.
Fascinating. Yeah, I was wondering. I
was like, "Sun, how did it make it
sand?" Uh,
I don't know if
&gt;&gt; really like 7 years after the company
was even found like running. 7 years
after the company was just like fully
functional, they changed the name to
SanDisk thanks to Sun Microsystems.
&gt;&gt; Nice. Well, we should talk to Sa- Sanjay
sometime and ask him if the San came
from his name, too.
&gt;&gt; [laughter]
&gt;&gt; Why not? Yeah.
&gt;&gt; Yeah. Well, yeah, we should seriously
see if he would talk to us about the
history. That's so fascinating that he
was a co-founder of SanDisk and now he's
a CEO of Micron. Super interesting.
&gt;&gt; Yes. Yes. So, I thought I'd mention that
as part of your history lesson here.
&gt;&gt; Oh, man. Good good history lesson. Okay,
so SanDisk they reported earnings. Their
CEO is not Sanjay. It is someone named
David Geckler, I believe, SanDisk CEO.
Um so,
this quarter they had revenue of almost
$6 billion. They were up 97% The revenue
was up 97% sequentially. So, that's just
quarter over quarter.
Um and of course,
how do you do that? You raise prices. Um
they're up 251% year-over-year.
Um
Here's a couple things that stood out,
which is pretty crazy. Gross margin,
78.4%.
That's like gross margins of a software
company.
&gt;&gt; Yeah.
&gt;&gt; [laughter]
&gt;&gt; Yeah, totally.
Um
&gt;&gt; I have my notes here that it was 51.1%
the prior quarter.
&gt;&gt; Okay.
&gt;&gt; know, the revenue estimate was supposed
to come in like, I don't know, 4.8
billion or something.
&gt;&gt; Yeah. Yeah.
&gt;&gt; It came in a billion above that. I'm
like,
what? Like, they are up 250%
year-over-year in like revenue.
And you know, the funny thing is that
they haven't shipped like that many
extra bits. This is all pricing.
&gt;&gt; Uh-huh.
&gt;&gt; Yeah.
This is not as much you you think like,
"Oh, they sold maybe that much more, you
know, to account for like 97%
quarter-over-quarter increase." No, no,
no, not really. You can't bring on that
much capacity that quickly.
&gt;&gt; Yeah.
&gt;&gt; I mean, you're talking about making
wafers and stuff and in a fab and that
stuff doesn't move in the time frame of
a quarter. So, this is all price
increases.
&gt;&gt; Totally. Wow, so you said their margins
were 51% last quarter and now they're up
to in the 70s.
&gt;&gt; 70s and I think they're projected above
80 next quarter.
&gt;&gt; Nuts.
&gt;&gt; The guidance is above 80.
&gt;&gt; They're going to make yeah, Nvidia look
like they have work to do.
&gt;&gt; Nvidia is only like 75, right?
&gt;&gt; Yeah, right. Totally. Totally.
Oh, yeah, of course. Nvidia is a very,
very large company and has had these
margins for quarter after quarter after
quarter. So, the question is
um why why is SanDisk is crushing it? Um
and the what they the story that I heard
on the earnings call was that they're
they really believe that the NAND market
is transitioning from commodity spot
business to something less cyclical.
Um and so the the points that they made
on the call and I'll read some quotes
here, too.
Um they have five multi-year supply
partnerships signed. Um these three new
ones in quarter two three They announced
two previously and they had they had
announced three more. Um and those three
new ones account for $42 billion of RPO,
remaining performance obligations. You
can kind of think of it like a backlog.
And this was the first time they've
actually disclosed that. Um so, clearly
there's long-term agreements for many
years and people are like signing up.
And these customer commitments
um already cover 1/3 of the fiscal year
27 bits. So, it's not just people
signing up for 2026, but they're already
signing up and paying for and committing
to 2027 bits, which actually have
financial guarantees backing them. So,
it's not, you know, it people are
putting their money where their mouth
is. Oh, yeah, the CEO Gettler said he
wanted to drive that those long-term
commitments to above 50% of bits and
already that one of the longest
contracts was for 5 years. And so, the
quote that I thought was pretty telling
on how
SanDisk is perceiving this.
Um from the CEO, he said,
"Last quarter, we were engaged in
discussions with customers on multi-year
supply partnerships, what we refer to as
new business models or NBMs.
Um I am pleased to share that we have
successfully advanced those
conversations with five multi-year
partnerships signed so far. They are
structured to lock in committed supply
for our customers and committed
financials for SanDisk." So, kind of the
customers are prepaying almost. "Our
customers' commitments are backed by
firm financial guarantees. These
partnerships support durable,
structurally higher earnings, and a
significantly more predictable and less
cyclical business for SanDisk. We
believe this marks a fundamental
evolution of our business, which is
centered on deeper customer alignment,
enhanced visibility, and long-term value
creation." So, so far in this quote, he
said, "We're signing up people for the
long run, and they're paying for it."
There hasn't yet, in my opinion, been an
argument for why it's not cyclical. It
could just be demand is crazy, and
people are signing up. Um
We as we talked about earlier with
Samsung,
when you're a commodity, when you're not
a commodity, you're actually competing
on performance, for example. And he
hasn't talked about that yet. But then
later, there was a quote that started to
get into this, which I thought was
interesting. Um
he said, "As AI models scale from
billions to trillions of parameters and
deployments advance from simple
inference to deep reasoning and
increasingly agentic systems, NAND has
become a critical component of the
underlying infrastructure. Inference
optimization such as KB cache, along
with workloads like rag, will require
substantial high-performance,
low-latency flash to deliver real-time
responsiveness and quality of user
experience. And then he goes on to say,
basically, "NAND flash is emerging as
the only economically viable solution to
deliver that capacity, performance, and
efficiency."
And then he said, you know, goes on to
make the argument that SanDisk is the
best on these metrics and therefore um
that's why, you know, they're capturing
this value. So, I want to throw it over
to you, Vic. Do you think this is
SanDisk Is this Is this AI, you know,
truly needing lots of NAND and
performance matters to your economics,
to your token cost? Um or and bits are
therefore no longer interchangeable?
Um or or is this just a demand thing
where it's like, "Hey, they're locking
up people for 5 years because they have
supply and it's sort of
preventing true competition on like
performance, latency, that that kind of
thing?
&gt;&gt; Yeah, yeah. This is This is good. Did
you look at
the Deep Seek V4 announcement? Did you
look into what is happening there?
&gt;&gt; a little bit, but please tell us about
it. It's It's related.
&gt;&gt; to NAND. You can see basically how uh
Deep Seek V4 has compressed KV cache
massively compared to the previous
version 3.2, I think.
And
you would think like, "Why would you
need NAND now if your KV cache is
compressed?" The problem is that the KV
cache
still, when you're doing agentic AI and
agentic multi-turn AI, none of it fits
in HBM. You're running hundreds of
agents. They all have to have long
context, long-running context,
multi-turn context. All of those key
value cache pairs
are just too much to store in HBM or
DRAM.
So,
if you see the Deep Seek V4 inventions
recently, it is optimized to be an
entirely SSD-centric
inference system where KV cache is
stored almost entirely on SSDs. It is
pretty amazing, actually. And
earlier after GTC, when
uh Jensen announced the inference
context storage system, which now I
think he calls CTX,
uh context storage, or whatever.
So, you basically this is a bunch of
SSDs in a rack that is sitting there and
connected uh via like high-bandwidth
fabrics to the GPUs so that they can
offload the KB cache matrices into this
this like SSD storage.
That is becoming
uh
very important. And at that time, I
wrote a Substack post pointing out how
this is going to change the inference
tokenomics forever, because
one of the ways you can save on
inference cost when you're using, you
know, the API, you can look this up for
any model, is that
it really depends
on a few things. First of all, you've
got the input tokens, you've got a
certain number of tokens uh cost per
million tokens. Then you've got the
output number of uh
dollars per out million output tokens,
right? It's usually like a four or five
is to one. Output tokens are like five
times more expensive than input tokens,
because it go undergoes this like
reasoning, this thinking process, right?
The thinking process costs a lot more
money, so the output tokens are more
expensive than input tokens. In the
middle, you have another pricing point
called the cache hit or cache miss.
So, what that means is that if you have
KB cache and
your
uh inference is able to reuse that KB
cache as much as you possibly can,
right? You have a cache hit. And when
you have a cache hit, your cost of
inference goes down massively.
So, what people do now is to basically
have a bunch of system instructions
right up front, and then they'll like
only append to the bottom, so that you
can maintain your cache hierarchy
completely. So, this is like cash aware
inferencing.
And
DeepSeek, for example, like there was
some metrics saying that like in agentic
use,
you can make it use 95% of cash hit
rates. So, 95% of the time it's hitting
cash. It in very few cases it even goes
to 99% it's hitting cash. So, even now
if you go to the DeepSeek API pricing
page and see how much the cost has
dropped for the DeepSeek V4 Pro.
Okay, it has gone down to
a fraction of a cent per million tokens,
okay?
You can compare that to Opus. I don't
remember the number right now, but it's
like significantly high.
So, what this says is basically
SSD-driven
uh
inference
is basically the only way forward.
DeepSeek has kind of portrayed that
clearly now. And
you cannot store all of this information
on DRAM on or HBM. It's just too much.
It's too much. And you almost have an
infinite storage of SSDs. You know, the
cost per unit is like an order of
magnitude higher when it comes to DRAM
versus SSD. So, you've got this
essentially free storage. And now you
have like capacities are solved problem
if you go to SSDs. The only problem is
then
you have this bandwidth better
bottleneck because you can't access
stuff as fast
from SSDs as you would.
&gt;&gt; Right.
&gt;&gt; know,
I've been meaning to read this new paper
that's come out from the DeepSeek team
called I have it on my screen right now.
It's called dual path breaking the
storage bandwidth bottleneck in LLM
inference, especially agentic LLMs. So,
I want to see exactly how all of this
ties in together. So, I've basically
given a surface-level overview of
justifying why SanDisk is saying that
NAND storage is so important in the
future of agentic or you know, AI
because Deep Seek is already a data
point that is heading in this direction.
&gt;&gt; Mhm.
&gt;&gt; There's a long answer to your rather
simple question.
&gt;&gt; this is so good. Okay, so I'm going to
summarize it and then I have a follow-up
question for you. Okay, so you're
saying, "Hey, look, Deep Seek is showing
us that uh SSDs are more important than
ever, NAND flash are more important than
ever, and if you think about the
tokenomics, it's way
more economical when you've got these
cash hits versus cash misses. So, you
got to think really hard about can we
have
a very big cash or memory hierarchy and
can we store as much as possible and and
people are going to be very
incentivized, even the end customers
using APIs running agents and stuff are
going to be incentivized to actually
think about memory and think about
caching. Um therefore, SSD market is
going to just continue to grow. Um but
my question for you then is, "Okay, SSD
market SSD TAM going to explode, all
good news, invest in these companies,
but why SanDisk?"
&gt;&gt; Not advice.
&gt;&gt; Oh, yes, not not This is not investment
advice. This is not investment advice.
We're just thinking very hypothetically
here.
Um do your own due diligence, you know,
uh
&gt;&gt; [laughter]
&gt;&gt; don't hold Victor accountable. Okay. So,
uh
the SSD TAM is going to explode or is
exploding, but is there is a bit is an
SSD bit a bit a bit or is is SanDisk's
bit better than someone else's?
&gt;&gt; I think a bit is a bit. I mean, is is
NAND is a rather established technology.
There isn't a controller
Actually, there is a controller
difference. SanDisk controller for the
QLC NAND is called Stargate and they're
still working on it. And
usually the more bits you add, so in
going from a triple level cell
uh to a quad-level cell, you go from
having nine states a single cell has
nine states in a triple-level cell. In a
quad-level cell, it has 16 states a
single cell. And now, depending on how
you program the cell, you should be able
to distinguish between nine or 16
different states. Otherwise, you don't
know what bit is holding. Is it holding
like a pattern 10 or pattern 15? So, the
complexity of the controller for this
NAND gets significantly higher even when
you add a single bit. Like, if you go to
penta-level cells, which exist in
research mode, you will go to 32 levels.
Now, you have to distinguish between 32
levels, you know? That it makes it very
difficult. Um I have a whole article on
how all of this works. But, yes, there
is a difference in controller uh and how
they how it works and all that, but it's
not really a differentiating factor,
okay? The controller needs to work well,
and
as far as I can understand it, please
correct me if you know, there are
[snorts] any storage experts out there
who actually work on this stuff on a
day-to-day basis,
they always know better. But, as far as
I know, a bit is a bit.
&gt;&gt; Mhm. Yeah, we should follow up and bring
on someone Micron, SanDisk, Samsung,
whoever is listening out there, of
course, to talk memory, but also to talk
storage. Let's I would love to talk
storage here and hear like a product
manager's argument for a bit is not a
bit because it probably comes down to
things like
reliability or
pricing per bit or or other other
factors
than just
straight-up read latency or write
latency.
&gt;&gt; Yeah, yeah, yeah, yeah. Maybe there's
some controller magic there because a
lot of the latency comes from adjusting
the voltages just right to read, you
know, this particular state of the cell.
So, what it does is it it iteratively
programs the right voltage to reach that
state. That takes time, you know? So, if
there's like some fancy new algorithm
that can go quickly and, you know, that
you can reduce the latency that way.
That may be a differentiating factor.
Actually, from IEDM last year, and if I
think we spoke about this on a past
episode, we spoke about a totally
different kind of cell where you can
dramatically increase
the the the reliability while still
having like 36 states to a cell, you
know?
&gt;&gt; That's right. Yes, it was a circle one
or something?
&gt;&gt; The circle yes, yes.
&gt;&gt; Yes, yes. All right. Listeners, go check
out our backlog.
&gt;&gt; [laughter]
&gt;&gt; Okay, this has been a super good memory
deep dive. Let's Let's carry on real
quick. Okay, so let's talk hyperscaler
earnings quick. Um so,
hey, it was a good quarter for Samsung,
it was a good quarter for SanDisk. Um
memory storage price through the roof,
demand through the roof. What does this
mean for the hyperscalers? We kind of
already hinted about it. Um Microsoft
disclosed um $190 billion of CapEx for
2026, and the CFO Amy Hood said roughly
$25 billion of the calendar 2026 CapEx
is specifically higher component
pricing. So, that's pretty crazy. We are
only a few years removed from someone
like Microsoft spending a total of $25
billion per quarter
uh just on all of their CapEx. And now
we're talking about in a year they're
going to spend like kind of a quarter's
worth of CapEx just on higher memory
storage component prices.
&gt;&gt; Um
&gt;&gt; Just give it to the memory guys.
&gt;&gt; Yeah, right. Pretty much. Uh
hey, good good time to be a memory guy.
Meta Meta raised their CapEx, um
and Zuck on the call said most of the
raise is higher component costs,
particularly memory pricing.
Google has a higher CapEx, although they
didn't talk about that as much. Um
Sundar did say that their cloud oh their
cloud business was up 63%
um which was insane. And Sundar said
that that would have actually been
higher if they were able to meet demand.
So still talking about demand and
capacity being the the bottleneck there.
And then Amazon, they didn't uh talk
specifically about uh component prices
in impacting their capex but but check
this out. This was an interesting
question like uh
commentary that came out. The CEO Andy
Jassy was asked if memory constraints um
are negatively impacting them.
And he answered by saying that for their
cloud business for AWS, memory
constraints are actually driving cloud
growth. And here and that feels very
counterintuitive and here's what he
said.
Who knows how big this is in aggregate,
but he said one of the interesting
things that we see right now with the
change in price and in supply on things
like memory is it is actually a further
impetus pushing companies who have been
on premises infrastructure into the
cloud. And it's because these suppliers,
the memory suppliers are prioritizing
their very largest customers, the
hyperscalers, cloud providers. And so
therefore there's a number of
enterprises who can't get on-prem
infrastructure and it's actually pushing
them to speed up their move to the
cloud.
&gt;&gt; Mhm.
&gt;&gt; So I thought that was pretty
interesting.
&gt;&gt; And I think people are generally
comfortable in using like AWS cloud.
It's it's a very easy switch to go and
do your stuff on there because
it has been the the bread and butter for
like pretty much the software industry
for the last decade. Right?
&gt;&gt; Yeah, totally. It would be interesting
to dive in with them because at this
point you ask well who's still running
running on prem? And it's it's got to be
people who
are still just thinking about like oh
what data do I keep on prem because I'm
in the financial industry or health
industry or something but even those
folks are still moving to the cloud and
they're getting pulled there faster
because the only place they can get
compute and memory is actually from the
cloud players which is
very very fascinating.
&gt;&gt; Yes.
&gt;&gt; [laughter]
&gt;&gt; Yeah, if that's the only place you can
get it, that's where you go. I mean it
doesn't matter what you want, right?
&gt;&gt; It's like yo sorry compliance team. I
know we're we're dotting all the i's and
crossing all the t's but literally we
have to we have to make this move happen
right now.
&gt;&gt; Yes, if you can buy memory from the
memory guys then maybe.
&gt;&gt; Yeah, yeah exactly exactly. Yeah, you go
you go find it. You go find it, okay?
Um so okay AI accelerators were talked a
lot about across the hyperscalers.
Google up said you know publicly on
their earnings call that the TPU will be
sold in a merchant capacity for the
first time and at multi-gigawatt scale
and and then actually if you look in the
10-K there was some risk language now
confirming that
the risk to doing that is getting CoWoS
and HBM allocation.
&gt;&gt; [clears throat]
&gt;&gt; So I thought that that was interesting.
Um
&gt;&gt; Yeah, just go to EMIB. Forget about
CoWoS.
&gt;&gt; Hey there you go. Yeah, go to EMIB.
&gt;&gt; That's right. Intel for the win.
&gt;&gt; Yes, I hope to write something about
EMIB here shortly soon comparing it to
like CoWoS L which also has bridges but
to unpack that for people. Um AWS talked
about Trainium
um at a $20 billion run rate growing
triple digits and of course people are
not generally
asking to buy Trainium and they're not
even necessarily uh renting it directly
but they are consuming Amazon Bedrock
and all these services that run on top
of Trainium. Um Trainium 2 largely sold
out. Trainium 3 nearly fully subscribed
and uh Jassy said on the call that um
because they do custom XPUs they will
save tens of billions of dollars of
capex savings each year which translates
into several hundred basis points of
operating margin advantage versus
relying on merchant chips. And on the
one hand, normally I'd been like wow,
that's so incredible they're going to
save tens of billions of dollars, but
then right away I thought, oh, so they
can pay for their memory.
&gt;&gt; [laughter]
&gt;&gt; Yeah. Yeah. We're making our own
chips so we can pay the memory guys.
Yeah, right now it's a funny cycle. I
don't know what what's what what what is
happening right now but yeah, we'll see.
&gt;&gt; Totally. So
then Meta mentioned of course they've
had tons of
press releases building up to this
quarter about 1 gigawatt worth of NTIA
with Broadcom and they had showed their
road map of you know, four chips in two
years
NTIA XPUs.
We had a great conversation with Meta
recently on that with Matt Steiner and
hopefully we'll have more getting into
it further.
They now Meta did mention significant
deployments with AMD and then also
running on some new Nvidia. So they were
talking
up all their multi silicon vendor
partners.
So with that we've run long. I think we
should call it quits here. Thank you
everyone for listening. YouTube YouTube
folks, thank you for your comments. We
see that you would like Vic to explain
again from our Google TPU one why is it
seven hops with I think it was with
board fly and not 16 hops. So we will
follow up with you will draw a picture
sometime. So keep writing your comments,
keep writing your questions. Thanks for
everyone for listening, watching us on
YouTube, watching us on X and reach out.
Thanks again. We'll talk to you guys
later.
