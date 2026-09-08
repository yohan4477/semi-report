---
source: https://www.youtube.com/watch?v=WWbEfDilXuM
vid: WWbEfDilXuM
title: A Masterclass on Lithography
date: 2026-05-22
duration_sec: 3797
channel: Semi Doped
kind: transcript
---
The main idea of making masks and making
transistors smaller came about because
this guy, I think he was working for TI,
came about
uh and he was looking at a microscope
and he was like,
"Wait a minute. If I can flip the
microscope over and shine light from the
other side,
it gets smaller."
Hello everyone and welcome to another
Semi Dope Podcast. I'm Austin Lyons with
Chip Strat and with me is Vic Shaker
from Vic's Newsletter.
Hey Vic, what's going on, man?
Yeah, I don't not that much other than
like everybody's panicked about uh the
13F from that Situational Awareness
Hedge Fund and uh there was this
sell-off in optics and everybody freaked
out. I'm like, "What's what's going on?"
First of all, I I still don't really
know what a 13F is. I guess it's like a
hedge fund has to report some holdings
that, you know, they hold and what they
sell and what they bought. I think
something like that.
&gt;&gt; Yeah, yeah, yeah.
&gt;&gt; And
uh
Leopold Aschenbrenner, is that how you
pronounce his name? Sorry if I got that
wrong. I have no idea. It's too many
syllables. Um
yeah, I mean, he he I guess he made a
lot of money and converted like a few
million into a billion or something and
then now everybody is following him for
the latest stock tips and when everybody
looks at his 13F, they panic and there's
this whole sell-off. Apparently, he
shorted optics and shorted AMD, Intel
and he sold it. I don't know.
&gt;&gt; [laughter]
&gt;&gt; Yeah.
&gt;&gt; So, it's like everything is down in the
semi market because of some some hedge
fund thingy. I It's This is what's
happening. It's funny. I mean, so if if
I'm him, I'd wake up and look and go,
"Wow, I can buy a few puts because on
this 13F, it doesn't talk I don't think
it talks about like the size of his puts
or anything." So, he can just buy a few
puts at some point in time, drive the
price down. Could he use that to then
buy the price? I mean, that's market
manipulation, but on the other hand,
it's like people are trading on public
data and on vibes, you know? So, just
like he he could throw people off his
trail, right? Like just buy a
tiny amount of puts in like everything
and you wouldn't know what he's
investing in.
Yeah, I don't know. I think Leopold
listens to this podcast. If you do, just
let us know. Maybe you can come explain
to us what a 13F is because I don't know
about you, man. I have no idea what all
this stuff is. So, I'm happy to learn
from the best. Yes, Leopold, you're
welcome anytime. All right. So, today
we're going to talk lithography. So, I
thought it'd be really interesting to
talk about the economic challenges of
lithography, modern EUV lithography
especially, um because you know,
ultimately incentives drive outcomes and
there are challenges with the increasing
cost of lithography, the increasing cost
of fabs, and you you start to see, you
know, TSMC
uh can afford the next
you know, process node and and Intel and
Samsung are trying to beat stay in the
race or be in the race. Um there aren't
that many other competitors and from
afar, if you're like a
semi-tourist, as they like to say on X,
um you might say like, "Hey,
TSMC is crushing it, you know, why
aren't more people in this game?" And of
course, as you start to unpack it, you
realize that um costs are a barrier to
let people enter. And so, then you start
pulling on the thread and you ask,
"Well, what cost?" And one of those
major contributors to the CAPEX needed
to participate is modern EUV. And so, um
yeah, what do you think? Should we talk
EUV?
Yeah, that's that's a great topic for
today. I think it ties in tangentially
to what is happening
uh to the
market today and why
people think that we are not in an
unconstrained
uh trajectory upwards. And this
basically stems from the recent Gavin
Baker interview that I put in in one of
our daily semi-doped daily updates on
Substack. So, if anybody is not
subscribed to the Substack, I recommend
it. It's free. You know, you can go get
subscribed on that semidoped.com. But,
the idea that Gavin said, you know,
floated in that interview was
we are not in a bubble because
TSMC is basically holding back the
entire industry by not creating enough
chips for everybody
by controlling their level of CapEx
spend on tools that require
you know, DUV
and EUV. And most famously, I think,
TSMC is not pro EUV. They think the
tools are too expensive
and that they want to stay on
DUV with multi-patterning as far as they
can
manage to do so. And we'll talk about
what DUV with multi-patterning means in
this episode. But, this is where we are
right now. Tools cost a lot. I think an
EUV machine costs something to the tune
of $400 million.
And that's just one machine. And you
need to run many of them to produce the
chips at scale that we need. And that's
that scale is continuously increasing.
So, it really comes down to
is EUV
the only way forward?
Um and then there is
hyper
NA EUV, which is like extremely I mean,
I don't even know if those are in
production yet. I don't think so. But,
those are going to cost close to a
billion dollars.
That's insane.
Yes, totally. So, we'll Yes, we'll
unpack all this for everyone when you're
like, "What's DUV? What's EUV? Why does
it cost so much?" That's what this
episode's all about. Lithography
masterclass, hopefully, to set the stage
for hopefully even future conversations
around lithography, some startups that
are out there. And actually, you know, I
just saw ASML shared a roadmap. I think
it was IMEC had a conference. It's going
on like right now, the ITF World
Conference. And ASML showed some of
their roadmap and how they think they're
going to be able to bring the cost per
exposure down. And it would be nice to
unpack this, but before we get to all of
those nitty-gritty details, we want to
educate our listeners on some of the
some of the fundamentals. So, let me
throw out some numbers. So,
a a brand new
&gt;&gt; say one thing. I want to say one thing
for Austin before us. So, most of this
stuff Austin is actually the expert
because
he
actually spent time working on uh this
kind of lithography stuff in a clean
room, which is something I can't say I
have done. Uh I've measured wafers and
measured transistors,
uh that kind of stuff. So, I've handled
completed silicon wafers, but I have
never actually done lithography myself,
and you have. So, this is a this is a
cool thing. You can tell us a little bit
more rather than just what you can read
on the internet, perhaps. It's it's
interesting what it looks like inside a
clean room. I'm I'm excited to hear.
Yes, yes. So, well, thank you for
mentioning that. So, yes, when I was in
grad school, uh I worked at the
University of Illinois Urbana-Champaign
in doing research as a research
assistant making graphene-based
transistors. So, I was in a lab with
Professor Eric Pop. He's at Stanford
now. And he studies 2D materials. So, we
were studying
People on our team were studying carbon
nanotubes, and then I got to work in
graphene. And so, yes, I got to be in a
clean room with, you know, silicon
wafers, um etching, you know,
depositing, doing lithography. And in
fact, I even got to do e-beam
lithography because we were trying to
make, you know, very precise kind of
one-off little um nanoelectronic
systems. And it didn't matter that the
throughput of e-beam is really low,
which we're not going to talk about
e-beam lithography much here, but it's
just a cool thing that I got to
experience. In fact, when I first
started, we were mechanically
exfoliating graphene, which means we
were taking
um basically tape and mechanically we'd
get graphite like layers of pencil lead
essentially, and then we'd take like
literally like clear tape um and then
stick it on top of the graphite and then
pull it off, and then take it under a
microscope and look, and you can kind of
like figure out how many layers of
graphene you have there. And so, I'd
just scan around, you know, I'm I'm like
doing some of this stuff in a bunny suit
and then going back into the lab and
moving this thing around, you know, and
just thinking like, "Oh, what am I doing
with my life? I'm trying to find
single-layer graphene. That's what I'm
doing." But of course, um once you find
single-layer graphene, then we would
make tran we'd pattern the transistors
right there on it and and then take
measurements and publish it because it
was a hard thing to do. And so, we kind
of had an advantage that we knew how to
do it. Um I won't I won't talk too much
more. We eventually did chemical
chemical vapor deposition um
to create graphene using like uh copper
foil essentially, and then we could grow
graphene, and it wasn't as pristine and
pure, but it was more scalable. And
anyway, uh good memories. I spent a lot
of time. Yeah, it's amazing stuff. I bet
it was a great experience doing all this
stuff. At the time, it's probably
frustrating as all hell as all research
is, but then looking back at it, it's
like, "Yeah, I I don't mind doing that
again now." At least like going into a
clean room and like pottering around
would be nice. To- Totally, man. It was
like It was challenging in that you had
to You couldn't just do the research.
You had to do a lot of exploration to
figure out how to even make the thing
before then you could actually measure
it and do the research. Um and so, yes,
it was frustrating at the time cuz you'd
spend all this time a whole day and then
you get to the end and be like, "Oh,
that didn't work, you know." But, yes,
looking looking back now, it's like,
"Oh, how fun was that? How much
intellectual freedom there to just be
like, you know, your research professor
says, 'Hey, go make this thing.' And
you're like, 'Well, I guess I got to
read and experiment and try to figure
out how to make it and then measure it
and then see if our hypothesis was
correct." you know? Yes, yes, yeah. It's
nice. Okay. Now we Now we're good. Now,
you know, we hit carbon nanotubes
already like research that's never made
it out of the lab. You spent time doing
that. Awesome. Now, let's talk about
stuff we can actually make. Yes, okay.
So, let's talk about Okay, so um have
you heard of Rock's Law, by the way?
&gt;&gt; not. No. Okay. So So, uh this is
a, you know, a {quote} {unquote} law
just like Moore's Law. It's It's really
an observation, um named after Arthur
Rock, and he was a an early investor in
Intel, maybe um kind of one of the
founders of the venture capital
industry, if you will. But, um the the
observation was that the cost of a
semiconductor fab
doubles every 4 years.
So, you know, it gets more and more
expensive. So, now this is interesting.
This is related to Moore's Law, where
Moore's Law said that the number of
transistors in a
in an integrated circuit doubles every 2
years. And so, if the cost of a fab
doubles every 4 years, that's slower
than the number of transistors doubling
every 2 years. And so, what that means
is that Moore's Law is really like an
economic statement that says,
for roughly the same price, we can get
more transistors per die area, per chip,
per unit area over time. And that's
that's really what drove the industry
was that economic realization that for
the same dollars, you could get more
compute over time. We are getting to the
point where the cost of fabs is getting
so high that that you know, we've seen
decades ago, really, Moore's Law, the
number of transistors doubling shrinking
for physical reasons, but also from an
economic perspective, actually the cost
of transistors flatlining and
potentially even coming up, the cost per
transistor.
And again, the question is, well, what
what's driving that fundamental change
to some of these important economic
scaling laws that we've seen for
decades?
And lithography is a big contributor.
Like you said, low NA EUV tools used to
cost around 250 million. Um now high NAs
coming out around 400 million and give
or take, you know,
these numbers change over time and it
probably depends per customer. Um but
you can back some of this stuff up out
of uh ASML's reports because they only
sell
they you know, they don't sell many of
these per year. But anyway, yes, the
rumored hyper NA, which would be a
future tool, could cost anywhere from
600 to 800 million.
Potentially if the straight of four
moves stays closed, maybe a billion
dollars cuz that's driving everything
up. Yeah. Um so which means lithography
all of these tools, like you said, we'll
get into it. Um you know, you might need
15 tools to open up a new fab. So I
think I'd seen some CNBC coverage where
it
uh it said that Intel's 18A fab in
Arizona, Fab 52, needed 15 EUV machines.
So imagine that, you know,
half a billion dollars a pop and you
need 15 of them. That's no joke. And
that's why uh a brand new fab costs on
the order of 20, 30 billion dollars. So
I I just wanted to quick paint the
picture of the enormous CapEx cost to
just build one new fab to try to stay in
this race. And of course, that
ultimately means the cost per wafer
will have to go up, too, because you
only can do so many wafer starts per
month, say tens of thousands of wafer
starts per month or 100,000, and you
need to amortize the cost of all those
tools over that fixed number of wafers.
Okay, Cool. So, let me back up a little
bit and, you know, quickly frame it
in a way that, you know, I usually
process things. So, one of the biggest
problems of modern lithography is cost.
And that primarily stems from having to
make smaller and smaller transistors.
And we have gone from
deep ultraviolet, which is what we'll
refer to as DUV,
to eventually extreme ultraviolet, which
is what EUV stands for.
And then we have, within EUV, we have
several levels of numerical aperture. I
think we should define what that is, you
know, going going forward next, so that
we actually have all these basic terms
in place.
So, we have low numerical aperture or
low NA EUV,
and high NA
EUV, and then hyper NA EUV. And the
higher you go from low to high to hyper,
you can make smaller and smaller
transistors. Right? Yes. So,
basically, higher the numerical
aperture, the smaller the transistors,
the smaller the feature sizes you can
make. And now, what you need is,
regardless of whether you choose a deep
ultraviolet or an extreme ultraviolet
machine,
you're going to have to need like at
least 10 or 20 of them in a fab. And if
each of them costs like, I don't know,
half a billion dollars, and you want to
put in 10 of them, you're spending $5
billion in just these EUV machines. And
then, not only that, you have to put a
whole lot of other infrastructure like
cooling,
like clean rooms are difficult because
you would have to have the vac the HVAC
systems that pulls out all of the dust
particles from the air. And so, based on
the how many dust particles you can find
per unit volume, these clean rooms have
different classifications, right? So,
you've got class one, class 10, class
100.
Um and I think the higher the number,
you got more particles per cubic, you
know, volume of air. So, all of this
stuff takes like an enormous amount of
money and time to build. And if you
actually this is like another point, if
you look at like the TSMC's construction
of their
fabs, it's actually critical machines
are suspended on pistons. Like entire
factory floors are suspended on pistons
so that it's immune to like earthquakes
and stuff. So, it is very expensive to
build a fab and takes years. It takes
years. It could take 3 to 5 years, you
know. So, this is why we can't simply
add chip capacity willy-nilly, right?
Totally. Totally. And not only that, if
if you haven't seen a fab, I'd encourage
people to figure out how to get on a fab
tour if they can somehow. I know it's
very difficult, but I want to go. I've
never been in one. They they want to go.
Um I I actually had the good fortune
recently of getting to go to Intel's uh
Fab 52 and tour it. But, a fab you also
need a So, not only do you not want the
machines to move around even a tiny bit
from earthquakes, but even from like
passing traffic and stuff because
of course, we're making transistors on
like the atomic scale, nanometer scale.
And so, you just you don't want all that
any sort of mechanical wiggling and
movement. But, you also uh these EUV
machines, they have like big power
sources and those
in the light source, like a lot of that
actually goes in the um subfab floor.
So, there's a floor beneath like the
main floor where the tool sits, and they
have all this equipment underneath it.
And then of course, you know, there's
like a a floor above it, and you've got
you've got to flow all that air through.
And so, I I just also wanted to
illustrate that it's not just like um
like data centers where you're just
like, "Oh, find some real estate, slap a
building up, throw some racks in, and
you're good." But, yes,
it takes uh even from a construction and
HVAC perspective, building a fab is is
no joke. And it goes beyond that because
if you look at Intel's fabs and the way
they have built it in the past, they had
this copy exactly method. Which means
they copy exactly. This is not something
that they mess around with. They
use like similar plumbing.
I've heard that they even use the same
brand of paint cuz they do not want
anything to go wrong. Because
if small things happen and change the
way a fab functions, you can't get the
yield up. And if you can't get the yield
up after spending 20 billion dollars,
you can't make enough wafers, which
means you can't sell them and make a
profit. So, Intel decided to copy
exactly. And that actually slowed a lot
of stuff down for them. That's a
different story. But really, that's how
difficult it is to build a fab. Really.
I mean, that's that's insane.
Totally. Totally. So, all right, going
back, you mentioned DUV and EUV. And so,
let let's tell listeners a little bit.
So, back in the DUV days, the light
source that was used um had uh
a wavelength that eventually made its
way to 193 nanometers. And I guess even
zooming out even further, so lithography
at the end of the day, for those who
don't know, I think everyone probably
does these days because ASML is an
awesome company and everyone wants to
invest or has invested and so at a high
level understands what lithography is.
But we're talking about ultimately being
able to expose light to sort of and I
put in quotes uh draw you know, the
shape of transistors or the shape of
areas that you want to etch away, that
you will leave parts of the transistor
but etch away other parts of the surface
of the chip. And so, ultimately, to make
transistors smaller and smaller, um you
can either make the wavelength of
ultimately, you need to make the
wavelength of light smaller and smaller.
Um but there's also something which we
can get into, which is the numerical
aperture, the mirrors that you talked
about making um changing the numerical
ap- aperture, but just focusing on
making the wavelength of the light
smaller. You know, the canonical example
here is like writing with a Sharpie,
you're going to draw like fat lines, and
if you can write with a fine tip marker,
a fine tip pen, you can ultimately make
a lot thinner lines than you could draw
smaller precision features.
So, that's what the industry was trying
to go to from deep
DUV um deep ultraviolet lithography to
EUV, which uses 13.5 nanometer light.
So, ultimately you're going an order of
magnitude smaller from the fat marker
down to the fine tip pen. Yeah. So, this
whole relationship that you main you
mentioned here, where you want a smaller
wavelength of light,
but you want a higher numerical
aperture. This is governed by what uh is
known as the Rayleigh criterion,
which means that the smallest dimension
you can make on a wafer
is literally proportional to the, you
know, wavelength, but inversely
proportional to the numerical aperture.
There is also a constant factor here
that's often called K1,
which we won't get into here, but think
of it as another knob which you can use
by designing the the masks that, you
know, selectively allow light or don't
allow light in these regions. You know,
they do all kinds of tricks on those
masks to improve this proportionality
factor K1. We won't get into it, but
these are the factors. So, there are
some bunch of tricks, then there's the
wavelength, and then there's the
numerical aperture. So, the smaller the
wavelength you go, the better. And to
Austin's point here,
deep ultraviolet lithography was most
famously,
you know, ended at what is called argon
fluoride lithography, is that right?
Mhm. at 193 nanometers.
And then
there was a like a quantum leap down to
13.5 nanometers with ultra
EUV with extreme ultraviolet. So, that's
a big change. That's like more than a
10x change, right? And going down
another 10x hasn't happened yet, but we
will get to how that can happen at the
end of this episode. But, yes, so keep
going. Let's let's go with that.
&gt;&gt; Let's let's let's talk about DUV for a
second. Um
so, do you want to explain like where
the 193 nanometer light comes from with
argon fluoride?
Yeah, there was a whole there was a
whole evolution to that as well. It's
not like we we just landed up there
right, you know, when we started
lithography like in the 1980s, it was
mostly like what is called I-line
lithography, which had a wavelength of
like 365 nanometers.
Then
over the years people realized like,
"Wait, we've got to make this better."
Um and then they came up with um you
know, krypton fluoride lithography, KrF
lithography that went to, you know, 248
nanometers. So, just by changing the
kind of uh light source that you're
shining through and the wavelength of
the light source, you could get better
features. So, this was like going
through the '90s, you could have like
248 nanometers. That evolved to like
uh argon fluoride lithography, where
they went to, you know, 193 nanometer.
And that was pretty cool, but then
uh that lasted all the way through the
2000s, let's say.
And kind of they kind of ran out of
light sources. They did try some other
light sources uh along the way,
but they didn't really like work out for
for various reasons. Um and then they
were kind of stuck with like argon
fluoride for a while. But then like they
thought about it and they're like, "How
do we improve numerical aperture?
Somehow we have to improve it." And the
the answer was extreme, actually. It's
amazing if you come to think of the
history of lithography, it's insane.
Some smart guy came up with the idea and
said, "How about we put water on the
wafer?" Like, let's just put water on
it. Like, "What do you mean you're going
to put water?" So, yeah, that's
literally what they did. They put
extremely pure water on top of the mask
and then put the light through the water
onto the mask. And that came to be
called like immersion lithography. So,
that actually helped scale transistors
further by just like putting water on
the wafer. It's like insane, right? It's
all right.
No, the history of lithography is
amazing. I wanted to tell you the way it
all started. I don't know if you know
this, but the way it all started,
um
was in the early days,
uh
I I forget the name of this guy, but,
you know,
a look out on Semi Dope. We'll we'll
have a a poll post on this thing. The
main idea of making masks and making
transistors smaller came about because
this guy, I think he was working for TI,
came about uh and he was looking at a
microscope and he was like,
"Wait a minute. If I can flip the
microscope over and shine light from the
other side,
it gets smaller, right? Everybody knows
you look the wrong way at these things
like stuff gets smaller. I'm like, "This
is it. Like, I'm going to turn the
microscope upside down and shine light
through the the wrong end and everything
gets smaller." And that that's how all
of lithography came about. Like, turning
the optics in lithography came about
because this one guy had the idea to
turn the microscope upside down. So,
that's how it all started, right? And
then, we've been continuously going down
the path of these various laser
materials, down down to putting
immersion lithography with water, and
ultimately coming down to like extreme
ultraviolet lithography, which is an
engineering feat that
is an achievement for like humankind.
That's how big it is. We'll talk about
it too, but yeah. Yes, yes. So, yeah,
Vic, you make some interesting points
here which
optical lithography, it's all about
light sources and about the optics,
about the mirrors, about how do you bend
the light. And so, when you talk about
yeah, the guy having the insight of
like, oh, when I look at a microscope,
it makes small things seem bigger. So,
if I flip that lens, I can make big
things seem smaller. What an amazing way
to take a big mask and make it smaller
to be patterned. And then ultimately,
you know, when you're talking about, you
know, moving through various materials
and getting unlocking smaller
wavelengths, we're talking about lasers.
These are light sources to shine through
the optics that we've been talking
about. And ultimately, the industry was
just playing with like, what are
different materials that can laze at
lower and shorter and shorter
wavelengths.
And this actually leads me to you know,
we got to argon fluoride 193 nanometer,
and the industry sort of stuck for a
while waiting to figure out what's that
next way of unlocking
even lower, even shorter wavelengths,
ultimately EUV as we know it today,
which we'll get into.
But in the meantime, the industry came
up with this nice trick called
multi-patterning.
And I thought it explain it really
quickly because there's also economic
tradeoffs to multi-patterning. So,
multi-patterning is ultimately about
like, the question is, how do you draw
smaller than
the a single wavelength features?
How would for example,
here, let me let's let's come up with an
analogy. Let's say you're drawing the
lines on a football field, like an
American football field, you know,
the end zone, zero yard line, 10 yard
line, 20 yard line, so on and so forth.
And maybe you have a machine
&gt;&gt; [clears throat]
&gt;&gt; that is like, I don't know, really fat
and it can only draw a line every 10 yd.
You know, the 10-yd line, 20-yd line.
Well, then maybe the coach comes here
and says, "Oh, hey, we also need a
markers at the the 5-yd line, and the
15-yd line, and the 25-yd line." And at
first, you're like, "Well, wait, my
machine, it can only print them every 10
yd. Like, how am I going to possibly do
that?" And then some clever person comes
up and says, "Oh, well, just draw 10,
20, 30, 40, and then go back to start
and scootch it over 5 yd and draw 5, 15,
25, 35." And ultimately, when you're It
takes twice as many steps, but instead
of having to get a new machine that can
now print every 5 yd, 0 5 10 15 20, you
just draw them every 10-yd space, and
then you offset
by 5 yd, and then you draw 15 20 20. So,
when you zoom out and you're done,
you're like, "Wait a minute, now I've
drawn lines every 5 yd, even though I
didn't have to get a new machine." And
that's like a very
crude analogy for what's going on in
multi-patterning, which is drawing
features in step one that are only
spaced at the distance that you can
comfortably make, and then coming back
in with another step and drawing a
second set of features and just
offsetting it. And so, the amazing thing
is with a trick like multi-patterning,
you can unlock shorter dimensions
between the drawn features, but of
course, the uh economic cost to this is
it takes twice as many steps, or it
decreases your throughput by half.
Awesome. So, I love the analogy, by the
way. That's like super cool way to
understand it.
So, what you're saying is basically you
can do
a a coarse etch, scootch it over, do a
coarse etch again, and what you're left
with is like a fine etch. Because you
can now by scootching over somewhere in
between the last two etches, you can get
a, you know, finer spot, you know? And
if I remember it right, this terminology
is called litho etch litho etch. So,
you'll see this as L E L E, right? Is
this Is this the same thing I'm talking
about?
&gt;&gt; Yes, exactly. You You nailed it. Okay,
cool cool. Now,
I think that people have taken this to
more than two levels of litho etch,
right? They've gone to like triple
patterning and even quad patterning,
which is all cool and all because
the now you're in stuck with two
problems. One, it becomes increasingly
difficult to even align masks between
the yard lines. Like, okay, like when
you had to align the mask at like the
15-yard line, it was okay, whatever, it
was between 10 and 20. But now you want
to align it at,
you know, 12, 14, 16, 18, and you're
like, "Okay, that's a problem." The
second problem is you're going to run
through four different quad patterning
steps, which each one takes the same
time, so it's kind of scales linearly,
and now it takes four times as much time
to make that one lithography step.
Um, and
I'm not sure like how many levels this
can be applied to quad patterning, but,
you know, making a transistor isn't like
one etching step or one lithography
step. There are many of them. And if you
have to quad pattern on multiple steps,
it adds up a whole lot of time, and the
throughput decreases, which means
uh, the cost per transistor goes up or
you don't get enough amortization of
your original 20 billion investment, and
now we are at like a crossroads here.
Yes, yes. And um, case in point, I know
SMIC had to which is the fab in China,
um, they're not allowed to get EUV, and
so they
were able to take DUV and use tricks
like quad patterning to get to, you
know, 7-nanometer class and then
5-nanometer class transistors,
um, which I wanted to point out, by the
way, because it's related to
lithography, um,
nowadays when we're talking about making
transistors, it's no longer just like
two-dimensional transistors, but it's
really three-dimensional transistors
with FinFETs that have these fins. We
should find some pictures and you know,
people go Google it. And ribbon FinFETs
um and so now you've got these
three-dimensional shapes. So it's also
making a transistor actually takes on
the order of like 60 or 70 or 80 steps
because you have to pattern and etch and
deposit material um kind of over and
over and over to build up this 3D shaped
transistor. Um so it's not only which
but but there's a kind of a marketing
thing that um like you know, the
semiconductor tourist for lack of a
better word, which just means you're new
to semis. It's no shade. We have I was a
semi tourist at one point.
&gt;&gt; Everybody's welcome into semi land.
&gt;&gt; the club. That's this podcast exists for
you. Um Very inclusive.
Yeah, exactly. When
a fab says we make two nanometer
transistors or 1.8 nanometer
transistors, it's not the smallest
dimension, this you know, critical
dimension like we talked about before,
the distance between any two really
close lines is not two nanometers.
It used to be, you know, like back when
they were 90 nanometers uh and 180
nanometers and 45 nanometers, that was a
lot closer, but it became a marketing
term. And so actually something that's
called two nanometers, the smallest
dimension may still be on the order of
like 30 nanometers.
Yeah, yeah. So it's not ex- actually
two, but that's how we now call it cuz
it's somehow the equivalent of two.
Yeah, correct. Correct. Yeah, correct.
Right. It's like the equivalent of like
when you think about like transistor
density and whatnot. But I will say it's
important because you know, naturally
when we say 13.5 nanometer
um EUV wavelength, someone might go,
"Oh, well, that's still way too big to
draw two 2 lines." But it's it's not
exactly. So, you might think then, "Oh,
if we went from big fat marker DUV to
fine tip Sharpie EUV, we must not have
to multi-pattern anymore, right?" And
actually,
your intuition is correct, but
from a resolution perspective, we don't
have to, but actually from a yield
perspective, the industry
can still
need to rely on some multi-patterning.
And there's a really nice graphic from
Fred Chen Substack. He wrote a nice
article on it. We'll link to it in the
show notes. But ultimately, we are
getting so small that when you're
shining
you know, very short wavelength light at
a certain dose, there's only really so
many photons that are that are hitting
there, and you can like control them so
precisely, and you've got like resist
chemistry chemistry going on, and there
might be some
Ideally, there's not there might be some
impurities or even dopants in the way,
and so you end up getting like this
stochastic nature. When you draw with
the Sharpie, you don't actually get a
very fine line, but if you zoom in,
there's some little dots around the
edges and stuff.
Think of it I don't know, maybe like
spraying with a spray paint can or
something. It's like not a perfect line,
you know? I'm I'm looking at the
picture, and I was thinking of spray
paint exactly. So, if you didn't You
always nail these analogies, and I was
like, "I'm going to nail the spray paint
analogy." [laughter] I I stole from you.
I'm I'm sorry. Yeah, so
ultimately, yeah, that's what they do is
basically you might draw with the spray
paint twice to get a better defined
line, especially as you're starting to
go in three dimensions.
So, I just wanted to throw that in it to
mention that yes,
we now we've jumped up to these, you
know, $300 million EUV tools, but it the
throughput isn't just immediately solved
because there's still some
multi-patterning that may have to
happen.
And there's other things about the power
of the light source and the dose, but we
won't get into those now cuz we're
really starting to get into the weeds.
Um
but okay, what do you say we jump in
Should we talk about high NA next?
Um or do you have anything else to add
here that's useful at a high level?
I think that
we should conclude before we talk about
NA, we should talk about how we can
generate light at 13.5 nanometers in EUV
because we mentioned that
these were like laser light sources
based on argon fluoride lasers.
But um
it's quite different when it comes down
to 13.5 nanometer EUV.
And that is where the hardest innovation
actually like was was um
holding back the industry from going to
this for a very long time. And
fundamentally what in a simple way, it's
far more complex than I'm explaining it.
But in a simplest way, it is basically
tin droplets uh that, you know, fall
through a chamber and you hit it with um
laser light
and it gets activated. And then you hit
it again with a laser light. Remember,
you have to hit a falling tin droplet
that's about 50 micron in size
uh twice as it falls through this, you
know, chamber. And the second time it
gives you an explosion of 13.5 nanometer
light. And that keeps happening
precisely. Uh ASML has an awesome video
on their website where you can can I see
these tin droplets falling. It's it's an
animation you can't really see this
thing. But then these droplets are
falling and these like laser sources are
like continuously hitting the droplets
and you see these explosions of EUV
light that is then it goes through like
a mirroring It goes through like 13
different mirrors because it has to be
focused ultimately onto the wafer.
And then ultimately lands up on the
wafer where it hits a mask and then it
selectively exposes or doesn't expose
stuff.
But this whole power that this you went
you the one of the big problems is that
you went through all this trouble to
get extreme ultraviolet light by, you
know, shooting tin lasers, but then you
reflect it through so many mirrors and
at each reflection you lose some power.
Like less like a single digit percentage
of the actual generated EUV power
actually gets to the wafer. It's a big
loss because of these mirrors. There's
literally no way around it, or so we
think. But yeah, that's what I wanted to
talk about because now that we finished
talking about how lasers entirely work
and how light sources work, numerical is
a good transition to get into right now.
Yes. Now, this is good. You I tried I
almost skipped over EUV entirely. At
least low and EUV. So so it's a good
introduction, which is we were stuck at
DUV. We tried multi-patterning. In the
meantime, the industry was trying to
work on EUV and as Vic talked about, you
know, ultimately we're trying to find a
light source that has a much shorter
wavelength. And, you know, there work
had been done that that showed with tin,
you could um
basically induce a plasma. Like that's
why you hit it twice ultimately. And
that plasma would generate 13.5
nanometer wavelength light. But there
was a lot of engineering challenges and
optics challenges around, okay, great.
Yes, when we're under vacuum, we can
generate a plasma and we and it will
emit this really low wavelength light,
short wavelength light. But how do we
ultimately harvest all that light? How
do we reflect it back and then use, you
know, with mirrors like aim it?
Ultimately you need to like gather this
light cuz it's just going to shoot in
any direction presumably from the tin
droplets. And you need to gather it all
and then you need to like get it to
where it needs to be to where the mask
is ultimately. And in in while you're
doing that, you're trying to focus all
the light. And like Vic said, there's a
lot of losses every time light hits a
mirror, it's not going to all bounce
perfectly exactly in the direction that
you want. There's going to be some
scattering and some loss. And so then
ultimately you end up losing so much
light in the process that you don't have
enough to like
expose the photo resist. And so, then
the question is that the industry has
working on for a long time is not only
how do we just make all this work and
repeatedly, but also how do we increase
the light source so that we ultimately
by the time we harvest all this light,
get it exactly where we need to, get it
focused all the way down, we still have
enough to actually expose the photo
resist and draw the transistor. So, that
Of course, that's why we're stuck at DUV
for a while because this is an amazing
engineering feat. And it Of course, it
takes Read the book Focus by Martin
something. I don't remember his last
name, but it's about ASML. And what's
really interesting is it talks about the
entire supply chain and all the
co-innovation needed, for example,
famously from Zeiss with their mirrors.
Um
it's So, it's it's no joke to even build
the laser
produced plasma light source, but then
you have all the optics. And of course,
there's something called a scanner. We
won't talk about it a ton, but
ultimately the mask you're patterning
You don't want to just pattern one You
don't pattern like one die or one chip.
You pattern a die on the chip, and then
you Like we talked about before, it's
like a checkerboard pattern on a big
dinner plate. You need to draw these
transistors for every checkerboard
square. So, you need some like um
mechanical, you know, mechatronics that
ultimately move the everything around so
that you can repeatedly print all of
this. So, there's a ton of engineering
to make this even possible.
Yeah, that's insane. That's what 39.5
nanometer EUV make. It's a incredible
feat of engineering and um
we are here today because ASML took 20
years
to develop this.
And
uh
the the whole question of how come ASML
landed up with this
is another interesting question because
this technology was actually developed
in the United States.
And at some point it was sold to ASML.
And at that that time the United States
government didn't actually come in and
say, "No, this is critical technology.
We want to hold it." You know, the US
government has blocked many such things
before, like including like protecting
5G technology. They've done all of this
stuff. Even now they're like there's so
much export control. This was like
before the day of export control. So we
as you know, from the United States
have handed over
the keys to the kingdom to ASML like a
few decades ago. And to kudos to them,
they spent like 20 years developing it.
And there's an enormous supply chain
that goes into ASML's machines that all
need to come together to make this work.
So it's it's built on a massive amount
of effort. But I just wanted to point
out that this was actually US technology
at one point. Totally. Yeah, that's a
good a great history lesson there. Of
course we should write more about that
history sometime.
Um okay, so we're running long, but let
me blow through. So okay, wow, it's an
engineering marvel to get 13.5 nanometer
light, but we want to make transistors
smaller. What do we do? Okay, like we
talked about with the Rayleigh criteria
criterion, um you ultimately have two
big knobs that you can turn. One is the
wavelength of light, but if you're like,
"Dude, we spent so long to get here.
We're not just going to
turn that all of a sudden. Just 13.5 was
hard enough." The other um knob is the
numerical aperture, which ultimately has
to do with like the size of mirrors.
Um and so that's where we get into high
NA and extreme like extreme NA or
whatever it was called, hyper NA. Um but
but but maybe really quick, the
industry's trying to move from 0.33
numerical aperture and low NA to 0.55
and high NA, which makes features on the
order of like 1 and 1/2, 1.7 times
smaller possible. But, there's a catch.
There's always a catch in engineering.
There's always trade-offs. You need
bigger mirrors. When you have bigger
mirrors, you've got these steeper light
angles ultimately as they bounce in, and
you have something called anamorphic
optics that come into play.
Um and I won't get way in into how that
works and what that means other than to
say you ultimately end up you can only
pattern an area that's like half the
size of what you could with low NA. They
call this the half field. So, basically,
now instead of your $250 million machine
printing an area, you've got, you know,
a $400 million machine printing half the
area. Of course, that sounds horrible.
Now, you need You're telling me I need
Okay, Mr. Salesman, I just bought a $250
million machine from you, and now you
say I need not only your $400 million
machine, but I need two of them, right?
That's crazy. So, what um
ASML's done a ton of amazing engineering
where they've said, "Yes, we can only do
a smaller size, but what if we speed up
like the scanner and the mechatronics to
go even faster to make up for it?" So,
it's like, "Sure, we we this the area's
going to be smaller, but we're just
going to move that thing around the the
wafer even faster." And again, um ASML
has all these amazing videos on YouTube
where they show like how fast they're
accelerating and moving this stuff, and
it's crazy. It's like
fighter jet style acceleration, but with
nanometer precision, moving things
perfectly around, stopping, reversing.
Like, it's crazy that it all works. But,
again, things are expensive. There's
more trade-offs. There's a lot more
innovation that needed to happen. And
ultimately, even with the proposed hyper
NA, even bigger mirrors, there's even
more trade-offs. Um even with stuff like
photoresist.
Um so, I'll probably just leave it at
that, and we won't deep dive on high NA
or hyper NA, but just trying to
illustrate that like not only are there
economic challenges, but there's also
just like
engineering challenges probably
presumably reliability challenges. So
then
we'll leave you with this. The question
is, well, instead of the mirrors, could
we make the wavelength smaller? How
could we make the wavelength smaller?
Yeah, I want to add one more thing about
the mirrors that's like an engineering
challenge. But then we're going to go
and talk about how to go even smaller
wavelength, right?
These mirrors are not simple. You just
It seems like what's the big deal going
from low and you just have to make a
bigger mirror. Make a bigger mirror.
What's the problem? These are not
ordinary mirrors because
they are actually made up of multiple
layers of 40 There's like 40 or 50
layers of alternating layers of very
thin molybdenum and silicon layers. They
are layered like this and it is insanely
smooth and
I read this book
Chip War by Chris Miller. It's a It's a
good book. I recommend it.
It talks to a lot of history and a lot
of what I've said in here is from that
book. Um and I have a quote here from
that book. It says, "If the mirrors in
the EUV system were scaled to the size
of Germany,
their biggest irregularities would be a
tenth of a millimeter."
Think about that. Think about how flat
those mirrors are. Yeah, and
we're going to put up a picture here and
you'll see like, you know, how how
smooth it is. It is very difficult to
even hold this thing. Uh and I feel like
I would only even want to breathe on it
like at this this level. I don't know.
They probably have protection protective
gear. But making bigger mirrors isn't
easy. It is an incredible engineering
feat to make irregularities a tenth of a
millimeter when the mirror's scale is
the size of Germany. That's That's
really flat, right? So
that's very smooth surface.
So it's not simple that we can go from a
0.55 NA, which is like hyper NA, to like
0.75 like next year, you know, if we're
used to like incredible pace of AI.
Everybody's like, "Oh, what's the big
deal? Like we can go to like 3.2T, 6.4T,
12.8T networking, right? No problem.
Like when are we going to get that?
Like, you know, 2 years, 3 years? What's
the time frame?" No, no, this stuff is
difficult. You cannot make a mirror that
simply, that easily. So, that's where we
are right now. And now the question is
what's next? Like a machine costs a
billion dollars and now now you tell me
like this is only half field and now I
need two two two billion dollar
machines. This is like the economics is
exploding. Something is going wrong. And
so, this is where we have new ideas to
go where no human has gone before.
Totally. So, okay, transitioning here,
people will say, "You could never
compete with ASML. It took the industry
so long to figure out this 13.5
nanometer light and they have a supply
chain like they have a relationship with
Zeiss. The only person in the world who
can make these perfect mirrors. Why
would Zeiss sell their mirrors to you,
dumb startup? Of course they're not
because they don't want to make ASML
mad, right? And so now you're going to
have to go get another person to be the
next AS or the next Zeiss. You're going
to be the next ASML. It's never going to
happen, right?" And so, some startups
are saying, "Okay, hold the phone. Let's
just like forget all that. Let's just
think simple from first principles.
Could we get a smaller wavelength light?
Um how do we tackle the optics? How do
we tackle the integration, the
mechatronics, all that stuff?" So, one
startup, X-light, out of um
California and I think uh Pat Gelsinger
is on their board maybe now, maybe he's
the chairman of the board or something.
Um
what they're trying to do is they're
saying, "Hey, what if we use
free electron lasers as the light
source? So, we'll replace LPP, laser
produced plasma, that's the tin droplet
shooting it with the laser machine gun
and all the magic that happens. Um but
what if we start by using this different
light source that can ultimately um
which by the way, a free electron laser,
um it essentially like think of it as
like accelerating electrons to like near
light speed. You've got these undulators
that like wiggle them. You can get this
coherent light. It can ultimately scale
down to like 1 nm, sub-1 nm. But what if
we start by using this new technology,
but still producing 13.5 nm light, so
that it can plug in to existing
ASML scanners and ASML optics. So what
if we could generate light in a new
fashion, in a by the way, FEL has a much
higher
total power source, so you can What you
could ultimately do is have higher dose,
which is better for yield. But actually,
what X-lite's trying to do is say, "What
if we use um one free electron laser,
and we can actually split the beam and
feed many EUV scanners?" So they're
ultimately trying to decouple the light
source from the scanner. So what if you
could buy um you know, 10 scanners and
feed it with one light source. Or
obviously, maybe they would have to have
two light sources, one as a backup in
case one doesn't work. Um but you get
the gist. And so that's the approach
they're trying to take is say, "Hey,
what if we build one massive free
electron laser next to the fab, and pipe
the light into all of your ASML
scanners? You can amortize the cost of
your FEL across all those scanners. Um
and then ultimately, it there will be
some integration, but we're not going to
ask everyone to change not only the
optics, but the the photo resists, and
we're not going to ask anyone else in
the industry to change. We are just
going to decouple the light source."
That's fancy, yeah. I haven't looked
into X-lite, so I'm actually learning on
the fly right now. That's amazing. One
of the things that you can do with a
a laser source that has a higher output
power is that Tell me if I'm wrong.
If you can get more light onto a wafer,
the throughput actually increases,
doesn't it? Not only yield yield, but
the throughput goes up. Correct.
Correct. Correct. The throughput
Exactly. Exactly. You
uh you know, whatever. If you only need
like a small flashlight to shine on
something and now you got really
powerful light, you could get the same
amount of light by actually taking your
really powerful light and shining it for
less long, exposing it for less long,
right? You just like you get
&gt;&gt; many photons get in? Yeah. Exactly.
Exactly. Exactly. They're So So
therefore, you can increase the
throughput, but you could say, "Okay,
well, hey, the yield maybe isn't that
great um at this the way the industry is
doing it now, so we'll shine it for just
a little bit longer than we need to and
you'll get even more extra photons,
right? So, you can, you know, have a
higher dose um but ultimately have a So,
both better yield and better throughput.
So, who would be the end customer of uh
X-light? Would it be ASML?
No, it would be the fab. So, the fab
would be buying and then the crazy
thing, and I wrote about it on on Chip
Strat, you can go check it out, is the
business model here is ultimately
selling light
sort of like a utility, like photons as
a service. So, um
you might ask like, "Okay, well, if Why
would TSMC go build an FEL from some
startup and then they'd have to go like
rejigger, you know, and work with ASML
to say, 'We don't want your um
LPP like light sources, we just want
your scanner part.' And like that seems
like a lot of risk and a lot of effort
for TSMC, but what if and a lot of
capex, by the way, what if um X-light
came in and they said, 'We will pay to
build this utility right next to your
fab, just like you get electricity
delivered, just like you get water
delivered.' And even um
just like you buy gas. So, like uh these
fabs, they will buy inputs like gas in
in sort of this consumption-based way.
Let us build the FEL, the light source,
and then
we will just charge you for what you
consume. So, it's on our books, we take
the capex hit, and then we'll just
charge you. So, if you want to just spin
up
three scanners, fine. We'll feed you
three scanners. Now, of course,
X-Lite wants to ultimately have you spin
up as many scanners as possible, but
X-Lite, there's a way that X-Lite can
take a lot of the risk and
do a lot of the upfront investment, and
then they will just sell light to TSMC
over time. And by the way, then once
they build that relationship, not only
could they sell you 13.5 nanometer
light, but maybe for a premium later,
once you and the industry are ready,
they could sell you 1 nanometer light.
So, it's a very interesting business
model.
So, the optics and stuff still comes
from ASML, but then you've got this
free electron laser sitting on premises
in TSMC, just like supplying light. So
&gt;&gt; Exactly. They count the number of
photons you used and charge you for it.
Is that the whole business model? Yep,
presumably. How they How they do that,
how they, you know, track how much light
you're consuming it would be also very
interesting to know, but that's that's
exactly It's like your electricity bill
at the end of the month, it's going to
be your light bill, your light for
lithography.
Amazing. So, what what other ways are
there to make
1 nanometer wavelength of light?
&gt;&gt; So, one more that we'll hit on today,
Substrate is another startup. They're
also California, in San Francisco.
And they are throwing out the playbook
and also taking a different approach.
And instead of FELs, they're saying,
"Hey, what if we use X-ray X-ray
lithography?"
Historically,
um
X-rays were generated by big
synchrotrons,
um football stadium size, you know, a
particle accelerators essentially. Um Um
but there's actually precedent and and
those again, you speed up these
particles, they get super high energy,
super high energy means really short
wavelength. And you can ultimately
control and use it as a light source.
Um there's actually the industry has
actually explored using x-rays as a
light source. And again, if you Google
chip strat substrate, you'll find this.
I wrote about the history, but IBM did a
ton of work. So again, a lot of this
early research happening in the United
States. IBM did a ton of work here to
see could this be a path forward for the
industry? And they actually made um
a synchrotron or an x-ray light source
um that fit on a truck. So it's a bit of
a myth that it has to be massive. They
figured out a way to to make it a lot
smaller. And this is the approach that
Substrate's taking, which says, "Hey,
ultimately [clears throat] I'd I'd
phrase it this way.
Hey, uh IBM and a bunch of other people
back in the '80s and '90s, they explored
x-ray lithography and it was a working
prototype. Um it wasn't
economical yet, but a lot has changed in
30 years.
Not only
about light sources, but um with photo
resists and with optics and everything
else that it takes to build a light
source and a scanner and do lithography.
What if we went back and revisited from
first principles and we took a stab at
at x-ray again and said, "Hey, given all
that we've learned in the last 30 years,
could it now be economically possible to
do lithography using
um x-ray, you know,
particle accelerator based x-ray
lithography?"
Yeah, I wanted to just step back 1
minute and just quickly explain what a
synchrotron is. The idea of a
synchrotron is that you accelerate uh
charged particle
in a ring, right? In a circle or an
ellipse or something like that. And as
the charged particle that is
continuously being accelerated turns
around
and changes angle, it spits out x-rays
as it uh turns around. That's That's
basically how a synchrotron works.
And
typically
in the past, you know, like you
mentioned, they these are really big uh
installations. Particle accelerators
tend to be really big, depending on what
energy you have to accelerate them to.
And uh I think they
the invention for making table top uh
synchrotrons has been around already
like 20, 30 years. So, it's not
something that you really need uh a
whole lot of like space to do. So,
that's one thing. So, that's very
important because people shouldn't be
like, "Oh, you know, what do you mean?
You need a football field? We don't have
that kind of space, so we can't do x-ray
lithography." No, no. I think it I think
it's it can be done in a smaller way.
But the one thing that I uh learned when
I wrote about this It's on my Substack,
too, about uh
substrate and x-ray lithography,
is that it's very difficult to like
actually focus x-rays. So, you know, we
spoke about the mirrors for EUV
lithography, but you can't do that for
like um
x-rays because they go through things.
You can't reflect them. That's a big
problem. So, the optics for x-rays is uh
a challenge. It really is a challenge.
So, one of the ways that you can do is
uh do this is that you have to do what
is called proximity printing. Because,
you know, like we mentioned uh earlier,
the the the inverted microscope approach
means that you could scale down a mask.
You could put the mask on the big end of
the microscope, and then the other end,
you know, scales down, let's say five
times. Uh
that is called um you know,
uh
reductive printing or something. I
forgot the exact term. Basically, you
can reduce the the magnification factor
by a factor of five because you got this
inverted microscope approach.
But that By the way, it came to me, the
person who did that was Jay Lathrop. Um
and so he's the guy who come up with
this idea. It came to me later. But
yeah, so
you can't do that with X-rays because
you There is no optics that works for
this. You have to do proximity printing,
which means that you've got to make
masks the same
critical dimension as the stuff that
you're patterning. So the masks are
actually very fine. And so for this
purpose, the mask making is
significantly harder when you're using
X-ray lithography because you don't have
the optics for them. So there are a
whole lot of challenges that require to
be solved. So it's not just like oh,
we've got X-rays now that go to 1
nanometer. So just let's just just swap
out
you know, the the
LPP 13.5 nanometer source for a 1
nanometer X-ray and then voila, you can
like print, you know, 0.1 nanometer
transistors gate all around or whatever
it is. It doesn't work that way. So once
you change the wavelength, everything
changes. And that's where we are now.
And there's this startup called
Substrate that's working on this. They
made quite a splash sometime back
because they feel that not only can they
make smaller transistors and continue to
scale Moore's law, but X-ray lithography
can be significantly cheaper. And that
you don't need to spend uh $1 billion
for an
EUV anymore, which means
that
and most people now with far less a
capital investment, going back to the
whole economics angle that we started
with in this podcast, can make more
fabs. And then if this technology is
held within US soil this time and not
given away,
maybe all of manufacturing will come
back to US soil if we can make x-rays
work. And now we can own all of the
supply chain
you know required to make I don't think
we can own the supply chain, but if we
can at least make wafers on US soil and
have so many fabs that we don't rely on
anybody else, that would really propel
the chip-making industry like we have
never seen before. So, that is the case
for making extreme lithography
on US soil.
Totally, man. There's so many
implications. We have to have a full
episode on this. Hopefully we'll talk to
them because first of all, it's good
that you point out that
there's lots of engineering that has to
happen not only with the light source,
but with the optics. There's
implications for the mask. How do you
draw a mask at such small dimensions?
Maybe it's E-beam. There's going to be a
cost to that, right? So, there's lots of
technical questions to get answered, but
to your point, the implications are very
profound.
If in fact it can reduce ultimately
reduce the cost. Um hey, could Global
Foundries make 2 nanometer chips? Could
Texas Instruments? Why not? So, what are
the implications that I think is super
interesting of these legacy fabs,
trailing edge fabs now being able to
make
even smaller transistors at the cost of
maybe their trailing edge nodes.
Tons of implications. What does that
mean for fabless design companies where,
you know, you're like, well, yeah, maybe
we'd make our own chip, but that's
pretty expensive and I don't know,
probably we can't amortize a hundred
thousand dollars per wafer across what
how many way We only need five wafers or
something, but what if all of a sudden
again it was, you know, the cost of a 90
nanometer chip that
you can now buy wafers for ten thousand
dollars instead of a hundred thousand
dollars, but get 2 nanometer you know,
transistors. Yeah. Crazy implications.
And then to your point, the geopolitical
implications are fascinating, too. So,
You know what will happen
What Jerry Sanders said, real men will
have fabs again.
Totally, totally. So, that even that,
like, why did every company at the start
of semiconductors have a fab? Well,
because ultimately, if you're vertically
integrated, you're going to get a better
product if you can co-design across the
fabrication across the design and the
fabrication. If you can design, but also
design for manufacturability all in the
same house, you're just going to go
faster, you're going to build a better
product. But ultimately, the cost
because of Moore's law got so big that
people had to drop out because they
couldn't afford a billion dollars for
the next fab, two billion dollars, four
billion dollars, eight billion dollars.
Everyone has to drop out because like
the the Global Foundries or the TIs,
like, they just can't they don't have
enough volume or high enough ASPs to
amortize that cost. So, it's just
dropping off. But yes, in an ideal
world, some of these players would still
love to
build, design, and build their own
chips. And then of course, from a wafer
allocation perspective, you own your own
destiny. Like, there's just so many
amazing implications. So, I know
everyone gets super hung up on like the
technology's impossible, who dares think
that they can take on ASML and Zeiss and
all that crap, but I'm more excited
about all the positive implications that
will happen, that will benefit all of
us.
If you've been watching this on YouTube,
you'll notice that I've been drinking
from this lens cup. So, now that it's
over, I guess our episode is too. We've
spoken a lot about lithography, so let's
let's get on with it.
Totally. Okay, that's it for today,
everyone. Thanks for listening. Thanks
for hanging with us. We hope you're
enjoying Semi Doped. Please tell your
friends about it. Pass it along. If they
want to learn about lithography, send
this to them. Send us questions,
comments on the YouTube. Subscribe at
semidoped.com to our Substack that we
started. And thanks, as always,
for
joining us in this journey.
