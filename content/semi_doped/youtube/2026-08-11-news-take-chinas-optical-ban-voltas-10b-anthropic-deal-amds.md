---
source: https://www.youtube.com/watch?v=WuFA3971k60
vid: WuFA3971k60
title: NEWS TAKE: China's Optical Ban, Volta's $10B Anthropic Deal, AMD's Earnings
date: 2026-08-11
duration_sec: 2123
channel: Semi Doped
kind: transcript
---
All right. Hello everyone. I'm Austin
Lyons from Chip Chat with me is Vic
Shaker from Vic's Newsletter and we are
bringing you a news flash
news take from Semi Doped. So this is a
little bit different than our regularly
scheduled programming. Vic and I decided
that you know, lately every week or so
every couple weeks there's like just
some really interesting stuff that we're
like really itching to talk about and it
doesn't always align with our schedule
of when we are normally going to record.
And so we just thought it'd be fun to
have these shorter kind of news take
episodes that we bring to you. So um
Vic, what is it that made you want to
jump on and talk this week? What are we
talking about today?
&gt;&gt; It's this whole Reuters news article
about how
the Trump administration is
proposing to you know, put a ban on
Chinese optical transceivers.
And it stirred up quite the panic you
know, in the markets because
you really can't build out any AI data
center without optical transceivers and
whether people realize it or not like a
bulk of this
entire optical component assembly stuff
including the pluggable modules are
actually assembled in China. So
it was like quite a shock to everybody
and everybody was scrambling to make out
you know, what's going on here.
And at that time I was like, I think we
should just cover this at least because
it's an interesting thing to talk about
because it's just like what what's going
on? What if we are cut off from the
optical transceivers tomorrow? You know,
what would happen or why you we think it
will actually happen
or not happen. So that's why I was like,
let's do a news flash today.
&gt;&gt; Yes, totally which is good. So let So
let's get into it. You know, I I too I
woke up and I read this and my initial
reaction was
you can't just cut these off from China
immediately because you're not going to
backfill that supply immediately from
the United States, right? So, there
would be if you shut it it it down,
there would be a period of time where
it's just like, all right, we just have
less optical transceivers at the point
in time when we're trying to build out
data centers, you know, at scales like
we never have before. Um but but yeah,
walk me through your line of thinking
when you read it.
&gt;&gt; All right, yeah. Uh so, if you're
watching this on YouTube, I just have
the article up on on the screen. Um so,
it can we can actually look at, you
know, what what's going on here. Uh
essentially
the news that was reported on August 4th
uh says the Trump administration is
drafting a ban on US imports of new
models of Chinese data center components
um as it seeks to protect the
infrastructure that undergirds the AI
boom. Okay, they got some part of it,
right? Basically, it really is an
important part of the AI boom, right? Uh
because you can't without optical
interconnects, you can't do any scale
out or like scale across or even like
hook up uh
to the data center. You can't even do
inference or training or whatever. Like
it it's a big it's a big part of the AI
infrastructure, so that's pretty good.
Um so, the specific ban actually comes
down to Chinese optical transceivers
uh which we've spoken on this podcast,
it just converts op light to electricity
and back again uh because light travels
much better distances uh at a much
faster rate. Uh so, you know, compared
to electrical transceivers, optical
transceivers can connect longer
distances. So, we've done a whole
episode on this uh the basics of like
transceivers and networking and all
that. Uh which you should check out uh
if if you're uh
wanting to get more into this. So, but
the whole thing was that um
this was the dumbest thing I saw in the
article. I'm going to read this out,
okay? Like after this, I'm going to ask
you what do you think about this because
it's like really dumb. It says, "The
move, not previously reported, uh aims
to prevent Chinese firms from stealing
data, installing malware, or disrupting
service at US data centers, which house
the chips to train and run AI models."
Like
why do you think that, you know, banning
the shipment of optical transceivers
will prevent the stealing of data and
installing of malware? I mean, like
literally has nothing to do with it.
&gt;&gt; Right, right. I too was struggling to
understand this, and I kind of went down
a little bit of a research rabbit hole
to
figure out like, is this even possible?
Like just So, the question is
if a Chinese company assembles an
optical transceiver,
is that actually a security risk? And
so, by the way, I kind of emphasize
assembles because at the end of the day,
um
what do these optical transceivers have
in them? A lot of times, it's a Broadcom
or Marvell DSP. It's like re-timers,
drivers, TIAs, all these various
components, a lot of which actually will
come from American companies, not
necessarily Chinese companies. Um so,
you know, these particular transceiver
companies, InnoLight, for example, or
Eoptolink, or these other ones, um a lot
of it is is the assembly and the final
kind of cabling and putting everything
together. And so, the question is like,
well,
where are they going to put malware?
Like what what are we talking about
here? If if they're sourcing a lot of
the components, and the one thing I
could find is that there's often like a
little MCU, like microcontroller, that
has some firmware on it, and that
firmware can be written to by the
vendor.
Um but as far as I could tell and I
would of course I would love some
transceiver person in the industry to
tell us more about that. I did find um
some links. It was like a OIP
optical interconnect
group or something that that had these
slides. It was in our SemiEngineering
Daily. I should have pulled it up this
morning, but it was like okay, it's it
is very
it's a normal thing for optical
transceiver companies to have an MCU
that has firmware on it and it can be
programmed. Um and and sometimes they
make it so you you couldn't just go in
and read it back out yourself to be like
what did they put on here? You know,
like I want to audit this. Um but it's
not clear to me that after it gets
shipped they would have any way to get
in and upgrade that firmware. So it's
not like I could sell you my transceiver
and then remotely connect from China and
then put all this malware on it and you
know,
do something.
&gt;&gt; Uh these pluggable transceivers don't
have too many components honestly. They
have an amplifier on the transmit side
and they have a you know, an amplifier
on the receive side. And then they have
some conversion circuits.
And that's about it. I mean then you've
got some optical connections like you
know, fiber attach units or whatever if
you want to connect to the optical
engine.
Uh that's it. I mean what else is here?
Like in an optical engine there's
nothing and then there's like a optic
fiber that plugs into it. There's no
there's no malware or stealing data or
whatever is going on here. You know
what's ironic about this is that they
want to make this whole uh ban to
prevent the disruption of service at US
data centers.
&gt;&gt; [laughter]
&gt;&gt; Which the ban would do that.
&gt;&gt; Exactly. The ban would exactly do what
you're trying to avoid.
&gt;&gt; Yeah, totally. Totally.
&gt;&gt; [snorts]
&gt;&gt; So you do wonder of course with
things like this is it
you You kind of wonder, is it the
government saying, you know, we want to
continue to put pressure on China, and
here's yet one other angle. It's not,
you know, Nvidia GPUs, it's somewhere
else in the supply chain, can we put the
squeeze on?
The regardless of it's technically sound
or not. And in fact, it's um a technic
it's kind of a
technically complicated area. So, if we
just tell people, "Hey, optical
transceivers from China are bad, they
could have malware." Maybe most people
would just believe it at face value. So,
you wonder how much it actually has to
even be true.
&gt;&gt; Yeah. Yeah.
&gt;&gt; I don't know. I'm not in Washington D.C.
&gt;&gt; Oh, speaking of Washington D.C. Yes, I'm
glad you said Washington D.C. because
read this next. "Transceivers definitely
pose a risk."
said this person who's an AI policy
expert at Washington D.C.
"As data center buildout scales up, you
want to make sure the data center supply
chain is secure from the get-go."
Like, you know,
again,
it's there's there's nothing about
security in this thing. Like, this
components have nothing in them that you
can like hack into or like install a
virus or something. You know the best
analogy I have for this? It's like
saying,
"If you hook up this USB cable to your
computer, you're going to get a virus."
Like, it's just a USB cable. Like, why
would I get a virus? Exactly, you won't,
you know.
&gt;&gt; Right. Right. Yeah, it it just transmits
on it. Yeah. I did find Yeah, I did find
this Okay, it's OIF Optical
Internetworking Forum, and they had this
webinar, and there are some slides
around like
a little MCU on these
transceivers for some little bit of
firmware stuff. Um so, there is a little
bit of trusting the module vendor. But
But again,
&gt;&gt; Okay.
&gt;&gt; and I'll I'll We can put a link in the
show notes, but again, it's very unclear
that it is an attack vector.
&gt;&gt; [sighs and gasps]
&gt;&gt; Yeah, yeah, actually there is there are
some management services that that
actually go on inside
you know, so that's there. Yes, there's
some there are some functions that do
this kind of stuff.
But one other thing is that the moment
the the biggest company that was hit in
China for this is Zhongji InnoLight,
right? They
seemingly contribute to about 34 34%
of the global sales of transceivers,
which some analysts actually revised up
from what this Reuters article calls to
be 27%. So down here it says InnoLight
has a leading 27%
a share of the global transceiver
market,
but some people said it's actually a
little bit more than that.
And there are others too in the Chinese
supply chain who make these things. And
if you add them all up, they constitute
about 50% of the global optical
transceiver market.
That is a significant amount of
supply to just like ban
because you can't get these things
anywhere else. And I have to explain
what that means because
the shares of like Lumentum and Coherent
and all these things and Applied
Optoelectronics goes up with when when
this news came came out.
&gt;&gt; [snorts]
&gt;&gt; But none of these companies other than
maybe Applied Optoelectronics to some
small fraction
actually assembles transceivers.
Yeah, I mean Lumentum and Coherent are
still going to make lasers, but they
kind of make the hard to make high-end
content of an optical transceiver like
the 200 gig EMLs.
And ultra high-power lasers that aren't
really like accessible to too many like
Chinese modules makers or whatever. So
what the Chinese module makers actually
do is like they they work on this very
low-margin stuff, but it's a very
essential portion of the market. And
without them, this is you can't have
optical interconnections in the data
center, right? So, it's I don't know
what how to think about this, but
ultimately if there is nobody to
package
and these optical transceivers into a
pluggable module, then I would imagine
that Lumentum and Coherent would be
upset like affected by the situation
because their sales would go down. So,
you would actually want people shipping
pluggable modules, right? So, I'm not
sure why Lumentum and Coherent went up
as soon as Chinese
you know,
ban was supposed to show up.
&gt;&gt; Yes. Okay, so I had that take as well,
which is like, okay, look, if there's a
fixed supply and then we take the
Chinese supply off the table, that
doesn't mean that immediately Lumentum
and Coherent are going to sell more.
They still have fixed supply, right? And
so, it's like
Okay, maybe like Fabrinet and these
other contract manufacturers could try
to pull some supply online, and then
maybe that would be allocated to the
Lumentums, Coherents, and whoever, but
none of that happens immediately. So,
actually just immediately
you know, just immediately, the only
thing that happens is that like now
we've traded uh you know, security
concerns for actually building capacity,
right? And so, this is actually very
European in some sense, which is just
like, oh no, we're scared about
something, let's just put a bunch of
regulations and slow down the building
of it whatsoever, you know, like because
there could be a tiny uh attack vector
that that can Austin say doesn't really
seem possible, let's just stop building
data centers because we just cut off
supply to all the interconnect cables.
&gt;&gt; Yeah.
&gt;&gt; And there's another complicated angle to
this because
TerraHop, which is actually the
non-China arm of InnoLight, is actually
uh
you know, is a is a subsidiary of of the
Chinese
company InnoLight, but they are entirely
operated out of Singapore and they don't
have anything to do with China. Like
none of the parts come from China. None
of the assembly happens in China.
Everything happens in like Southeast
Asia, but now what would you do with
those? Like how would you deal with
TerraHop? Would you ban them? Would you
not ban them? It's very gray area. So so
many of these things and they also said
that this this ban only applies to new
modules.
But what does new mean? Like these
things have revisions all the time. Like
what is new? Like a new slightly
different revision V2 to V3 makes it a
new product? Like
changing a slight orientation of a part
on a module become makes it a new
product? Like what what is it? So I
don't think any anybody knows. But
&gt;&gt; [laughter]
&gt;&gt; do you actually think that this is
actually going to come into play and
actually last?
&gt;&gt; Uh so I don't I don't think so. I don't
see
&gt;&gt; Yeah.
&gt;&gt; I think enough people I mean, come on.
If you're Broadcom, Marvell, Coherent,
Lumentum and everyone in the supply
chain Oh, and by the way, if you're
Microsoft Azure or
OCI or anyone who's building out data
centers, like everyone's going to
literally say like hold the phone. This
is not right. This is not it. So I I
don't think Yeah, I don't think this is
going to
&gt;&gt; And I don't think anybody is going to
any US maker is going to like I don't
know, like Fabrinet or
uh Sanmina and you know, all these
companies are going to go off and
immediately say,
uh you know, let's start building
capacity. Yeah, this is our business
model because you know, the before you
know it, like in a few months if this
reverses and then all that the is gone
to waste. Nobody going to do anything.
&gt;&gt; Correct. Yes. No, you make a very good
point, which is like
no one can proactively take action on
this because it would be manufacturers
who'd have to try to ramp up supply, and
that is a very expensive and kind of
one-way door, right? You you you buy you
have shells, you build you buy tools,
you stand up a a supply
uh like a a
fab line, and then all of a sudden the
government decides, "Never mind, we're
not going to do this." And you're like,
"Oh, well.
Now we have all this excess capacity."
&gt;&gt; Yeah.
&gt;&gt; Totally.
&gt;&gt; Awesome. I think we've hit on that topic
uh pretty nicely. Uh I don't have
anything else to say about it. Do you?
Let's
Okay. Because we have to see how it
rolls out. What's your uh take on the
whole AMD earnings scenario? Like
uh did they seem to have posted some
really good earnings?
Uh
but
the stock fell, and people are like
questioning something. What's going on
there?
&gt;&gt; Yeah, yeah, yeah. So, okay. AMD, they
had good earnings. Um you know, they are
record revenue of 11 1/2 billion, up 50%
year-over-year, 13%
quarter-over-quarter. Their data center
segment, 6.7 billion, which is up 107%
year-over-year, and is um importantly is
now 58% of their total revenue. So, they
have shifted from a sort of consumer uh
client PC client graphics
company to a data center company, which
you would hope that they would do that,
right? So, they're actively executing it
on that. Uh epic CPU demand is good. Um
Helios has good reception and is
shipping
end of Q3, Q4, Q1, right? So, everything
at a high-level looks good. Now, the
stock dropped after hours um after their
earnings call, and uh so then there was
a lot of like, "Oh no, you know, people
must not What what don't investors like
about AMD's earnings?" And And there was
a couple things that people were poking
on. Um
one, it was o- okay, well, how [snorts]
much growth is actually happening with
GPUs? Um obviously, CPU agentic CPU
demand for Epic is very strong. Uh
Helios is promising, but it hasn't
really shipped yet. And And they you
know, there were some comments about
like
uh acceleration and like Stacy Rasgon,
if you listen to the call, he was poking
on it saying like, "Oh, well, is it
actually like
not accelerating as much as possible?"
Or you you know, because there's like
quarter-over-quarter acceleration versus
just like half-over-half. And And
you know, whatever, there was some
surprises about um
spending 800 million in CapEx instead of
the expected maybe two or 300 million.
And And you know, there are some
legitimate On the one hand, um you know,
some of that spend might be into their
own compute infrastructure, um but
there's some concern that some of that
is actually
needed to for example, uh
get supply for substrates and um help
OEMs and ODMs like get to the finish
line with these rack-scale Helios and
stuff like that. And so like the the
nuanced argument there is that
it's not so simple to be fabless
anymore. Like you used to be a fabless
company and not have to take on a lot of
that have that skin in the game for like
getting allocation to certain things.
But now that it's hard to get
substrates, it's hard to get memory or
anything like that like that, the point
is like, "Hey, wait a minute, AMD's
supposed to be a fabless company, but
they're having to you know, put their
own money in to to get allocation." But
again, that doesn't necessarily say that
uh AMD is an unhealthy business. Um It
that's just like a dynamic of the time.
So I I personally
the stock had run up ahead of the
earnings and then it fell off a little
bit, but I wasn't necessarily concerned
about anything. I think if I was trying
to push on AMD and take like a more
skeptical bearish angle and and try to
really push on them, the the line of
thinking that I came up with is
after listening to the earnings call
there was definitely talk about demand
out pacing
supply and Lisa had said something like
it was unforecastable. It was just like,
"Wow, this demand is crazy." So then I
would ask, "Okay, what demand are we
talking about?" So the answer there is
CPUs, right? Like Agentic AI came on
stronger than we expected
and we need to sell
uh they said they had double-digit
growth on CPU unit volume. So this is
epic server CPUs and um s- epic ASPs.
And so that's why they they were very
strong is cuz they sold a lot more CPUs
at a lot higher price than they
expected, but also they they're leaving
money on the table because they didn't
have
enough supply because they didn't see it
coming on so strong. Okay, good. Good.
That's great. AMD is a very strong
server CPU business.
But then I would say, "Okay, but what
about GPU demand? Cuz we're in the GPU
era and that's where the money is made.
Is does your GPU demand outstrip your
supply?" And so the answer they would
probably give is like, "Yes, demand is
very strong and Helios is a great
product." They say, "Okay,
uh but like does demand outpace supply?"
And you know, the answer is like, "Well,
right now of course it does because we
haven't shipped any, right? So it's
like, 'Okay, we're shipping a little bit
at the end of Q3. There'll be a step up
in Q4 and a step up in Q1.'"
And we've seen
some nice conversation
uh in customer uh
partnerships around Helios where, you
know, Open AI, Meta, lots of folks have
um stepped up Anthropic and said they're
going to deploy Helios.
And so, you know, you you'd say, "Okay,
um
great, there's strong demand for Helios
and you're ramping supply, but the
question is how many quarters ahead do
you think that the demand for Helios
will still outstrip supply when Helios
is at full ramp? Maybe it's like Q2,
will there still be more new demand for
it
than supply? Um and so, you know, I
think that the answer would probably
still be yes, especially because
AMD took a particular they made a they
made a particular design bet as they did
it with the 300 series, which is let's
have more memory HBM memory capacity
than the competition. And so,
AMD I think would say, "Well, yes, there
will be certain workloads where we'll
still have a ton of demand because it's
you get better TCO if, for example, you
can run inference of this particular
model on eight AMD GPUs versus 16
Nvidia, right?"
Um but here's where it gets really
interesting. Okay,
so you're betting on
HBM being the differentiator here, but
HBM um
the price of HBM has gone crazy, right?
So, it's like
really expensive for HBM, but it's worth
it for certain workloads.
But what about workloads where it's not
worth it? So, for example, prefill and
decode,
prefill is very compute bound, compute
heavy. You don't actually need as much
HBM. Um decode very memory bound, so
that's where the HBM shines. So, then
the next logical question is like,
"Okay, but
you kind of only have one SKU, so it and
and you decided to put a ton of memory
on it, so is it going to be really
expensive to use Helios MI 455 chips for
pre-fill?
And so, on the call, actually,
um
there was some interesting conversation
where
Lisa said, um "Hey, we are flexible.
We're a chiplet-based company. We have
the flexibility to change the compute to
memory ratios. And so, for certain
workloads, if our customers if the TCO
of the way we've designed the chip
doesn't work, we could actually reduce
the HBM footprint for them." Um okay,
okay, this is this is promising. Um so,
that I think what that leads to is
I wouldn't My prediction would be I
won't be surprised if AMD comes out and
says,
"We're going to start to have more of a
portfolio of offerings in the uh
Instinct family." Obviously, they
already have these other ones for like
that are more focused on enterprises and
air cooled stuff like that, but even
with their high-end MI 450 series,
I wouldn't be surprised if they start to
say like we've got some offerings that
don't have as much HBM if you want to
use it for for for pre-fill, and you can
use our current ones for decode. Um and
maybe end up moving toward a portfolio
of offerings, which is aligns with the
direction the industry's heading anyway.
Um I think the memory costs are really
just
putting pressure on AMD's design
decision and sort of pulling them in
this direction.
&gt;&gt; I mean, Nvidia had this whole CPX thing
for pre-fill, uh
but then they we never heard of it
again. So, maybe disaggregating pre-fill
and decode into separate hardware SKUs
is wasn't the greatest idea.
&gt;&gt; Well, okay, so that's that is a great a
great question a great pushback.
The solution was instead of to say, uh
"Let's have GPUs, some with a lot of
HBM, some without. Then they actually,
of course, came in and did the whole
SRAM thing and said, "Wait a minute,
what if we use the SRAM for decode and
then we keep our HBM for the pre-fill?"
And so, that would also continue to um,
point out that AMD doesn't really have
an SRAM offering, although they did just
launch or make that announcement at
Advancing AI about partnering with
Cerebras to sort of fill Yep, yep. To
fill that out, but again, I think we'll
maybe we'll see more from AMD here on
flushing out what is their strategy,
where does SRAM come in, where does GPUs
with less HBM come in. So, I think
there's probably going to be
more coming from AMD. That That's my
takeaway.
&gt;&gt; Okay. Yeah, that's an interesting
interesting approach. It's a good
explanation, actually. I don't have
anything to add to it, but we'll see how
it, uh, rolls out from here.
Um, because I wanted to, uh, go on to
the next piece of, uh, interesting news,
which is this company called, uh, Volta
Infrastructure. Have you heard of this
company?
&gt;&gt; I didn't until you texted me, to be
honest.
&gt;&gt; Okay. So, let me let me, uh, run through
what this thing does. This is very This
is quite amazing to me, okay? Uh,
because
there is this company called Volta
Infrastructure, which is a London-based
company,
not to be mis- mistaken for another
company of the same name, which is
Singapore-based, and also does something
very similar. I was totally confused
when I saw the website. Um, actually, I
I should actually pull that up, uh,
because it is, quite nice to see what it
is that they are trying to do. And so,
I'm just going to, uh, share
basically volta.com and, um,
go from there.
Okay.
So, this company was very interesting
only because this company is, uh,
has been around only for about six or
seven months, okay? This company, let's
say, as old as our podcast as we record
this right now because we started it.
&gt;&gt; [laughter]
&gt;&gt; Okay? And
they seemingly have gotten a $10 billion
uh deal with some unknown unnamed AI lab
or something, uh which later I think
Bloomberg, was it? Uh yeah, reported
that it's actually Anthropic who has put
in a $10 billion computing deal with
this new cloud startup that's been
around only six or seven months. So,
you've got this like big player coming
in and [snorts]
uh just like putting in a compute deal
that's worth,
you know, nine figures, and you've got
this company that becomes instantly a
multi-billion dollar valuation company.
So, I was like, "Wait, what does this
company even do that like how can they
get like a $10 billion deal in computing
like six months? You know, why do what
can I learn from this for Semidopa
podcast, right?"
&gt;&gt; [laughter]
&gt;&gt; Yes, yes, my original thought was like,
"Oh man, they're the same age as
Semidopa. Dude, we picked the wrong
industry."
&gt;&gt; I know. Podcasting. Yeah.
&gt;&gt; you know. Maybe we should
Yeah.
&gt;&gt; Why can't we start a
&gt;&gt; [laughter]
&gt;&gt; Yeah.
&gt;&gt; Okay.
&gt;&gt; Let me explain the the the idea of this.
Okay, the fundamental idea behind this
company
um is that they treat it
like it's infrastructure. And this, you
know, they treat this as inf you know,
basically institutional grade
infrastructure buildout. And I had no
idea what that meant, okay? So, I was
like, "Okay, let me dig into this a
little bit more." And it's interesting
because
whenever you borrow money to build
infrastructure, which can be like roads
or uh you know, something that you know,
you can just get um
basically money out of on a regular
revenue basis, right? Just let's use the
example of roads, right?
Infrastructure debt to build out roads
is very different from what you would
borrow to do something like a VC or like
a corporate uh financing deal. And so,
the whole idea is that
you treat this asset, whether it's roads
or compute, as a contracted but
predictable cash generator. So, it
generates cash. Like a toll road
collects tolls, and it's going to
continue to do so for decades. Like a
power plant sells, you know, electricity
for a very long time, often 15-20 years.
So, the bet is that AI is not like a
data center, you know, AI is not you
know, we call it data centers, but it's
really not that because
uh there is a lot of sharing and there's
like a lot of virtualization, and you
get part of the compute in a data center
typically in the old days. Compute is
very different. Like
it is a token factory. It's an AI
factory. Think of it as infrastructure
and that is factory. So, whenever you
say that I can produce revenue like
collecting tolls for a long period of
time,
institutional lenders, right? They tend
to give this loan to you at lower
interest rates, which means that they
are uh
not betting on growth or some fixed
outcome, but they know that you're going
to start generating revenue by
collecting tolls immediately. So, the
cost of the capital, right? Because you
are getting this at a lower interest
rate, means that the person building out
with them gets compute at a lower price
somehow, right? So,
that's where this whole thing is built
built out. So, this is their whole idea
behind building data centers
uh from capital to tokens
uh for, you know, companies like perhaps
Anthropic who's coming through the door.
&gt;&gt; Sure, totally. And I know we're short on
time, so I'll keep my take short. Uh so,
first of all, I'll say that um Jensen
would be very happy to hear you talk
about token factories and financing it
like a utility, and that's how how
thinks about it, too. So,
uh
you know, congrats on uh
thinking the same way as Jensen. So,
okay, there's one other way that I would
approach this. When I started to think
about this, I thought like, okay, let's
say it's Anthropic. Um [snorts]
Anthropic says, "Oh, wow, uh we need a
bunch of Nvidia GPUs." And let let me
remind people that Anthropic
traditionally used Trainium, and then
they also said, "We need more compute."
And so, they started using TPUs. And
like 9 months ago, there's announcement
where Microsoft, Nvidia, and Anthropic
said like, "Hey, there's this three-way
partnership, and Anthropic's going to
commit to 30 billion of Azure compute
plus up to 1 gigawatt additional
initially on Grace Blackwell and Vera
Rubin." And in Nvidia was investing,
Microsoft investing, okay? And so, it
was like, "Oh, wow, this is actually
upside TAM for Nvidia," which I think
people forgot was one of the two biggest
model lab companies wasn't actually
really using Nvidia yet. Um okay, so
now, let's say you're Anthropic, and
you're like, "Great, we want even more
Nvidia. How do you find it?" You you
every Neo large
Neo cloud and large CSP who has Nvidia
compute has already has customers that
it's allocated to. So, where are you
going to find it? Okay, well, you just
maybe Jensen says, "Hey, I'll allocate
you some." And then you say, "Okay,
well, I have to find power." Okay, so
where do you get the power and and
someone to operate it? Well, basically,
in this case, it um this Volta is the
balance sheet company that just started,
but the operator is actually this um
crypto miner like Bitdeer. And or or
something like that. And so, there's an
Yeah, existing crypto miner that has
experience operating data centers, but
they're not going to be able to take on
any of the balance sheet. They're not
going to get that low cal- cost of
capital financing. And so, I think, you
know, this is also just a clever way to
say, "Let's start a new new clean
balance sheet, and they're going to
receive the money, and they're going to
be sort of like the parent, um but
actually they will pay Bitdeer for power
and operations, and Nvidia will help
make sure that
some new GPUs get built and allocated
and and set up there, and then Anthropic
can It to me it feels like the fastest
way for Anthropic to spin up more
uh Nvidia GPUs was essentially needing a
clean balance sheet to borrow against.
&gt;&gt; [snorts]
&gt;&gt; So someone to come in and and play that
role. But but it is obviously Yeah, it's
very good.
financially creative.
&gt;&gt; It's amazing. Yeah, it's financially
creative. And I'm like, wait, what's
going on? Like people just drop like 10
billion like just like that nowadays
into a company of Nick never even heard
of uh or
but it's it's fascinating. It We live in
fascinating times. And it's
it's great, like
&gt;&gt; Let me add one
&gt;&gt; I had to work for a long time for that
much that much money, you know.
&gt;&gt; I know. But now think about if you're
Volta, you're like, yeah, we've got one
customer and we've got 10 billion
dollars. But on the other hand, it's
like, dudes, you guys have one customer.
Like what's the long-term game plan? And
I'm sure the game plan is like just keep
making that customer happy as long as
possible, and then maybe eventually win
some other customers. But then that's
essentially every other neo cloud in the
world is like we've got one big customer
and we're hoping to differentiate.
&gt;&gt; That's true. So they're like basically
two things, right? Like most startups
can't even say, yay, one customer,
right?
&gt;&gt; [laughter]
&gt;&gt; Right, right.
&gt;&gt; So one customer's amazing. Uh so the
second thing is that
if the
customer is like Anthropic, that's a big
customer to nail like on like
level one, and you've like already
nailed Anthropic. Everyone's going to
follow suit, right? The pack of cards
and the dominoes will fall. Everybody's
going to throw compute money everywhere,
and CAPEX is going to continue going to
the trillions.
Uh yeah, I don't know when this uh uh
This is This is very interesting, so I
thought we should cover it on the
podcast. Anyway, enough of that. Let's
see what happens. It's nice nice to keep
a tab on these kinds of creative
financing deals.
I know, we are not really finance guys,
but I love to like understand the
financial creativity behind how some of
these things work. Uh or maybe it's just
new to me, which either way I have fun.
&gt;&gt; Absolutely. It is going to be It is the
story that's woven through the period of
history we live in right now, which is
very interesting technical
um innovations as we move to uh data
center scale computers, and then very
interesting financial innovations to
finance it all.
And so with that, we'll call this
episode a wrap. Thanks for listening,
guys.
