---
source: https://www.youtube.com/watch?v=OmM8224MZh0
vid: OmM8224MZh0
title: LiDAR, Explained: How It Works and Why It Matters
date: 2026-01-19
duration_sec: 2141
channel: Semi Doped
kind: transcript
---
Whenever there is sunlight, right, that
is the biggest cause of interference for
LAR. The only thing that really destroys
LAR is sunlight.
&gt;&gt; Hello listeners. Welcome to another
semi-doped podcast with Austin Lions
from Chipstrap and Vic Shaker from
Vick's Newsletters. Today we're going to
talk to you about Liar. So Vic, I know
you wrote a post or maybe even more than
one on LiDAR. It was it was quite a long
time ago actually, but tell me why are
you tracking LAR?
&gt;&gt; Yeah, LAR was interesting to me at the
time and particularly on my Substack.
It's an article I hold close to my heart
because that was one of my first posts
that made it to the top or the top three
or whatever of hacker news and it was
like a first thing for me. It's like the
first time it ever happened and I was
all like stareyed because of that. It's
so it's and the only reason I wrote
about it at the time was uh because
there was all this discussion that
self-driving cars should not be using
LAR and the real way to do this
according to you know Elon Musk is to do
it with cameras and the argument is we
don't have LAR sensors and lasers
attached to our heads so if we can drive
with just vision alone why can't cars do
the same so you know so that was the
argument And Elon was like significantly
vocal about calling any car company that
used lidas as dumb and that they're
going to it's just too expensive. He
said it's just too expensive and nobody
should be using this technology.
However, ever since then, the technology
has dropped uh in cost significantly and
is now well within reason for use in
like autonomous vehicles.
&gt;&gt; Totally. Totally. Yes, definitely. I
would say that Elon and Tesla have been
driving the conversation quite a lot in
the past few years. Um, now I'll say
from my side of things where I started
to see the benefits of LAR actually when
I was working for a startup Blue River
Technology that was owned by John Deere.
We were working on autonomy with
tractors and in the field you can
actually if depending on what operation
you're doing there can actually be lots
of dust and lots of wind. I mean, we're
out here in the prairie in the middle of
Iowa, and we started to realize that
like cameras couldn't see through dust
clouds, and it it would happen, for
example, like every time you turn on the
north end of the field and you turn
south, the way the wind's blowing, it
could blow that dust cloud that from the
implement you were pulling behind you,
it's creating a dust cloud behind you.
And now all of a sudden, you're turning
back into it to go through the dust
cloud. And so it was kind of funny to
see no one around the field but a dust
cloud stop this really big heavy
equipment and then it would pick up and
go again. And then the same thing would
happen over and over. And from there we
start to realize like oh cameras can't
see through dust but maybe radar maybe
LAR could deal with things like dust
dusk dust fog etc. And of course once
you start talking about putting other
machines in the field, we kind of
realized like just because you can do it
with cameras, maybe it's safer to have
additional modalities for sensing. So
that's where I first got interested in
it. But I will say um recently I went to
Rivian's AI and autonomy day where I saw
up close in person an R2 where they're
actually putting uh a LAR behind the
windshield in the R2. And I honestly
didn't realize that LAR was getting that
small of a form factor. And that's where
I first went like, "Oh, wow. What if
this is like the backup cameras and the
ultrasonic sensors of past where at
first it was like a nice feature on the
premium cars, but nowadays every single
car has it, right? So that's kind of
where I started to track LAR and say
what is the cost and could this actually
at economies of scale actually get to a
cost that could be literally on every
vehicle in the future.
Um, so with that, I thought it would be
interesting for our readers for me to or
listeners for me to quick share some of
what Riven said for their argument
behind why LAR, which would be maybe
some counterarguments to the uh thesis
from Elon. So, just really quick, I'm
going to read some of the transcripts.
So, at the AT Rivian's autonomy day,
they said, "We're adding a third sensor,
lidar. Liidar is an optical sensor and
its strength comes from the fact that
unlike the camera, it has an active
light source enabling it to see much
better in the dark. Another advantage is
that it provides a three-dimensional
view of the world unlike cameras which
provide a 2D view and require the AI
models to infer depth. and they said the
camera is still the main workhorse for
our our AI but radar and lidar are
critical to addressing edge cases which
would otherwise create longtail
problems. Then they continue to go on to
your point to say the cost has come
down. 10 years ago they used to cost
thousand tens of thousands of dollars.
Today several hundred dollars. The
resolution is better. It's about 25
times better than 10 years ago. And of
course the size like I talked about you
used to have a mechanical spinning beast
which we can get into those technical
details. And now it's solid state and a
lot slimmer form factor. And so finally
they said that nowadays also with their
transformer architecture large driving
model it's trained end to end from
millions of miles of driving sequences
collected across their fleet and so
directly fed in the pixels from the
cameras the radar returns and the LAR
points and they can take all of that and
then predict trajectories. So I I'll
pause there. What's your reaction?
&gt;&gt; Awesome. Okay. I think we can unpack a
lot of that statement and we'll get into
depth about some of why that happens. So
essentially the argument is for LAR you
can use technology that is just beyond
vision that can make cars safer and
provide a better driving experience than
what a human would. So that argument is
a way of saying yes humans don't have
lidar sensors attached to their heads
but if we could we would because it
makes the experience safer right so the
question uh is why are lighters lidar
sensors and radar we'll talk about both
of them briefly so why is it that they
actually make driving safer uh so the
the main difference comes from using
light in the case of LAR or radio waves
in the case of radar to basically uh
send a pulse of light or radio waves
from your car into the distance and it
reflects like off of a tree or another
vehicle on the road and comes back to
your sensor and based on that you can
estimate much like a bat does
echolocation you can estimate how far
stuff is and now this because it works
fundamentally different from the
wavelengths of light that we
uh provides a much better field of view
um and much more uh detail even in the
dark. Right? So that's why one would use
these LAR sensors. So the basic idea of
LAR is to use infrared sensors and these
are beyond the visible light range. So
you'll never actually see LAR and even
if you see a LAR sensor, you shouldn't
be looking into it. And we'll get into
why right so the whole lidar uh school
of thought really splits into two
fundamental wavelengths I think there is
one 905 nanometer and there is a 1550
nanometer school of lighter now this is
where the space is and this is where
companies compete okay now you can ask
why these specific wavelengths what's
what's so you know special about them
why don't you just use like 940 or why
don't you just use like 1,200? Why why
these numbers, right? The the the reason
for that is
whenever there is sunlight, right? That
is the biggest cause of interference for
LAR. The only thing that really destroys
LAR is sunlight. That's the major
factor. And luckily for us, we have this
atmosphere above Earth that sucks up a
lot of frequencies and wavelengths and
does not let certain wavelengths reach
the earth. And these are called
transmission or absorption windows
depending on which uh wavelength is
being transmitted or absorbed by the
atmosphere. So if there are a bunch of
wavelengths that never make it to the
ground, it makes sense for us to use
them for LAR. So that's where this whole
thing comes about. So are you saying
essentially the the sun is sort of like
spamming us with all this
electromagnetic noise in a sense, but
there are certain areas of the spectrum
where it's quiet down here because it
gets absorbed in the atmosphere. So
you're saying we should use those
wavelengths because there's less noise
down here locally.
&gt;&gt; Yes, absolutely. So that's the reason we
use these very specific wavelengths. But
that's not to say that people don't use
other wavelengths like Aster for example
uses 865 nanometers because they figured
&gt;&gt; oh we can we can deal with the
atmospheric problems but it provides a
whole lot of other advantages in terms
of cost um and you know we can make it
work regardless of the fact that it's
more in the absorption range. So there
are a lot of engineering trade-offs just
going with uh what wavelength we have to
use.
&gt;&gt; So 905 versus 1550 since those are most
of the predominant ones. What are the
tradeoffs of choosing one versus the
other,
&gt;&gt; right? I'm going to get to the
trade-offs. I want to say one other
thing about why LAR and not radar. And
the reason is it comes down to the
frequency of the signal. Now if you have
a wavelength that is small like in LAR
versus radio frequencies that have a a
larger wavelength right
you can detect objects only in the range
of the wavelengths that you are
emitting. So if you're sending smaller
wavelengths you can make out smaller
features like you can say what the you
can identify a dog on the road versus a
car quite easily. in in radar it's gets
a little more blurry but the other side
of this wavelength frequency discussion
is that radar can go much further away
uh and LAR has in automotive LAR you
have a range of maybe 300 m so that's
the major wavelength frequency trade-off
between radar and LAR and you can you
have to use both of them because
sometimes you want to be able to see
further away does not have to be as fine
resolution however in closer range
ranges. You want to be able to identify
the dog within a 200 meter range or
something. So that's where LAR and radar
come in. So now the tradeoffs,
&gt;&gt; let let me ask you quick. So with radar,
it has the longer wavelength. Um I
always think of kind of as an analogy
like AM radio where I can hear radio
stations from like hundreds of miles
away versus FM which is shorter
wavelength and I can only hear ones that
are like 20 miles away. Um with radar it
can see longer.
Can it also do better with like rain or
something that I assume would scatter
like the shorter wavelength?
&gt;&gt; Yes, good point. Yeah, great point.
First of all, I like your analogy of AM
versus FM because that's exactly it,
right? AM wavelengths are very very long
wavelengths and the way they work
obviously is they reflect off the
ionosphere and goes anywhere in the
world. FM is a much shorter wavelength
and doesn't go as far. So you can use
the same analogy to go to radar and then
lidar is even shorter wavelengths. So
excellent analogy there. Now uh yes so
it is also scattered less radar is
actually scattered less by rain and dust
and fog for the same reason that it does
not have resolution because the
wavelength is large. So anything that
are like small particles don't affect
its vision so to speak.
&gt;&gt; Sure that makes sense.
&gt;&gt; Yeah. Nice. Okay. So, LAR LAR short
wavelength. It could be as short as 95
nanometers or it could be 1550
nanometers. Why choose one versus the
other?
&gt;&gt; Okay. So, before I explain why one
versus the other, we have to think about
what wavelengths the eye can actually
see because this is very important. Uh
the eye can see about 400 nanometers to
about 750 nanometers. And if you notice
the 905 is closer to 750 than 1550 is.
So immediately you will see that people
start talking about eye safety
regulations. The very fact that 905 is
closer to the what the eye can see makes
it more dangerous to the eye. So you
will see anybody using 1550 LAR
nanometer LAR claiming that they are
better eye safety ratings and therefore
should be used. uh it which is true you
know you can put it further away from
the visible light and it's good but
there are some fundamental differences
beyond what just eye safety is. So for
example in 905 you can use basically
detectors that are based on silicon and
silicon based detectors are cheaper and
that goes a long way in building cheaper
lidar systems like we just spoke about.
1550 nanometer systems require indium
gallium arsenite which is definitely
more exotic because silicon does not
give you enough photo detector gain at
1550 nome. So it automatically makes it
a little more specialized and a little
more hard and expensive to make because
of the lack of silicon here, right? And
the other thing is that at lower
wavelengths like 905, you can really
have higher powered lasers. Uh, of
course, then there is the eye safety
issue, but you know, but you can make
good lasers cheaper at 905. 1550. Yeah,
there are companies like Coherent which
which is interesting because it's so
much in the data center space now. Uh
they also make LAR but they actually
have a high power 1550 nanometer LAR. Um
so it's a competing uh balance between
which technology should be used all the
time really.
&gt;&gt; Gotcha. Yeah. So obviously eye safety is
interesting one because if we do have
these on every single car you do have to
think about at every intersection even
when you're just driving down the street
every car passing you shining lasers at
your eyes essentially. So I I I'm glad
that people are thinking about eye
safety there but definitely sounds like
trade-offs of cost is is one big one
using silicon always cheaper. So, okay.
So, we've talked about the different
wavelengths for lasers that people use,
but what about how the LAR actually
works? Like how they measure distance
and objects. Are are there different
implementations?
&gt;&gt; Yeah. So like we briefly discussed
earlier uh LA works basically on what is
called direct time of flight which is a
fancy way of saying you just have a
glorified bat attached to your car
instead of sending acoustic waves it's
just sending light you know so it's a
very well-known uh echolocation method
of detection and the reason it is the
most popular form of detection is that
it's literally very easy because you can
measure the time it takes for the light
signal to come back to your detector and
based on that you can calculate how far
away the object is and this is the very
this fact actually helps create 3D
images of the image of the scene ahead
of you and the reason is because
different parts of the scene have light
arriving at different times so you can
reconstruct a 3D image this way and
that's a big advantage of LAR over
cameras right
and the other method method that is now
being used but is still complicated to
in implement is called a frequency
modulated continuous wave. Now some LAR
companies claim this is like
revolutionary technology. It's really
not because this has been used in
automotive radar at 77 to 81 GHz for a
very very long time. So the fundamental
principle of FMCW radar is that
you don't send a single burst of light.
Instead, what you do is you send
what is called a chirp signal. A chirp
signal is a signal that is sent for a
given amount of time. However, within
that period of time, the frequency or
the wavelength, however you look at it,
of the signal is continuously increased
from one value to another. So, in
automotive radar, it is increased from
77 to 81 GHz in the period of the chirp
signal. And in uh LAR, you could do
similarly with wavelengths. Now, the
advantage of doing this is that what you
receive isn't a single
uh a single point of reference. you
receive a whole chirp that is shifted in
time. So if you compare it with the
original chirp at every point in time
you have a difference in frequency
between the chirp you sent and the chirp
that came back to you. Now you can
measure this difference in frequency as
a beat frequency and based on that you
can detect uh what the object distance
is in LA. Interesting. So this is
actually much more robust but also more
complicated to implement because now you
need a modulated laser source that can
quickly ramp up its wavelength but in a
short span of time.
&gt;&gt; Uh I see interesting. The only analogy
that I can think of when you're talking
about this is like the Doppler effect.
Like when there's a siren going away
from you, you can hear the frequency
shift or when it's coming towards you,
it you can hear it. When it's going
away, it gets deeper and when it's
coming towards you, it gets higher and
it kind of sounds like this chirp signal
does that and you get a sense of
probably where the something is. Do you
also get like a direction or a velocity?
&gt;&gt; Yes. Uh you you do get all of that. At
least I know that this can be precisely
calculated for FMCW radar technology in
automotive radar. Actually wrote four
entire articles on how this is
calculated in velocity and direction
&gt;&gt; and you actually have multiple antennas.
So based on which antenna receives
things first, you can calculate angle.
So you can take the entire data set that
is received by a LAR or radar system and
get everything out of it. distance,
velocity, and angle. It's It's pretty
amazing actually.
&gt;&gt; That That is cool. Now, I know when I
started to look into different LAR
companies, most of them used time
offlight except one, Ava, who uses this
FMCW,
um, which they call 4D LAR. Any thoughts
on why some people use time offlight
versus FMCW?
&gt;&gt; Time of flight is much simpler actually.
The electronics that goes into doing the
actual detection is simpler overall
because it's just measuring the time
delay between what is sent and what's
coming back and it works really well for
the most part. So people are just
focusing on using lowc cost components
with low cost detection and that makes
it sufficiently accurate for most
applications. So I think this is why you
see time offlight radar be
radar and LAR being uh dominantly used.
&gt;&gt; Gotcha. Now that that matches I was
looking through Inovvis which is one of
these manufacturers. I was looking
through their earnings calls in their
recent earnings call. They said they
they are time offlight um 9005
nanometers and they actually taped out
and tested their own FMCW chip. Um yet
they're in quote more confident than
ever that time of flight will remain the
way forward in automotive LAR. And they
explain that it's because they're making
it with proven mature technology and it
has the cost profile and the
manufacturability
to but yet still gives them good enough
performance.
In your investigations, what have you
found about these uh spinning radar
domes that you see on Whimos in San
Francisco? Has that changed at all?
&gt;&gt; Yeah, you know, most of who I looked at
were and maybe they're a little bit
newer, but all of them it seemed to be
using solid state approaches except
there was one Hai or I'm not sure how
you pronounce it to be honest. It's a
Chinese company, HSAI,
and they used a 1D rotating mirror,
which they called hybrid solid state,
which I thought was interesting. But do
you want to walk our listeners through
the old mechanical spinning uh LAR and
maybe the progression to pure solid
state?
&gt;&gt; Yeah. Yeah. Yeah. So, that's
interesting. So, uh, the way lighters
you see are actually basically
mounted on a motor and it just spins
really fast and it's just blasting light
all over the place. And uh, it collects
the reflections back and then it mapped
its entire 360 surroundings. And the
problem with this approach is that, you
know, throughout the history of
electronics, nobody likes anything that
moves. That eventually is a wear and
tear issue and especially car
manufacturers don't like it. even though
they have so many moving parts in the
vehicle like still uh nobody likes stuff
that moves especially when there is an
electronic way of doing it. So anyway
that was the first implementation
especially of LAR uh mechanical spinning
LAR domes. The next evolution of that
was basically a MEMS based mirror uh
approach to scanning LAR and the idea is
simple. You keep the LAR source constant
and instead you just put a micro mirror
and you move the mirror around really
quickly in certain angles and it kind of
scans uh based on the reflection of
light off the mirror the the the field
of view that you want to see. Right?
It's much like you know you have a ray
of light coming through the window and
you put your mirror and you reflect it
onto your ceiling. You know that's the
idea, right? It it works well. It's
surprisingly it works well. Uh yeah, but
still you know now you've made moving
parts but much smaller moving parts in
MEMS's mirrors. These micro
electromechanical systems are actually
more surprisingly reliable than people
make them out to be. So yeah, that
technology actually does work. Then what
ended up happening is people said okay
look I don't want I don't want anything
scanning and there's a problem when you
scan things right because at a certain
time you get this reflection from a
particular direction now the LAR has
gone spinning around uh 360° let's say
now if there is an obstacle between the
point you looked last and by the time
the LAR spins around back to that spot
there is a child there you're going to
miss the child
&gt;&gt; and you don't want that. So, nobody
wants to miss stuff like this. So, the
alternative to doing this is to use what
is called a solid state flasher. It's
exactly what it says it is. You put a
bunch of like laser sources and
detectors in a grid and you just take a
picture and what it does is it sends a a
blast of light out and picks up the
return signal and it maps the entire
image. And now it's a question of how
fast how many pictures per second you
can take. It's like a frames per second
thing, you know. Gotcha.
&gt;&gt; So that's that's a flash lighter. Now
apart from all of this, there is just
one other technology and I think there's
one company that's still working on
this. It's the most complicated but
fanciest approach and that is called an
optical phased array LAR. So what you
can do is like phase arrays are a
technology in uh radar technology that
has been around I don't know 60 to 80
years and they're usually found on the
planes and you know jet end you know
fighter jets on the nose cones they have
these uh phased arrays and the way it
works is like this. You put a bunch of
light sources in an array and you excite
each one at a slightly different time.
So you depending on whether you delay
the activation of each of these light
sources by a small amount or a big
amount, you can actually form the
direction in which the light is
pointing. So this is how phase arrays
work. So what you have to do is have
these tiny delays and you can change the
wavefront of the wave being sent out of
the LAR. This is complex. Okay. And this
is a truly solid state approach of doing
things because you can scan
electronically and have all solid state
parts, right? You can scan almost a 120
degree field of view by doing something
like this. At least I know that number
is true in radar. In LAR I'm not sure
what the field of view optical phase
arrays can scan. So basically you have
four approaches. I'll just quickly
summarize. First approach mechanical
spinning domes. Second approach move the
mirrors around like you'd reflect light
from a window. Third approach the photo
camera approach. You take so many frames
per second. Finally you use this fancy
steer the beam of light around by uh
activating each one at different times
approach. These are the four ways you
can detect it.
&gt;&gt; Nice. That's helpful. With the flash
camera one, how do they get the wide,
you know, say 120 degree field of view?
Because I'm just kind of picturing like
it's looking just like straight ahead.
&gt;&gt; Yeah, you can't. You have to put a whole
lot of uh pixels and make a really large
uh you know frame and take as much of a
picture as you can. So yeah, you can't
scan that one. Yeah.
&gt;&gt; Yeah, that makes sense. Super
interesting. Okay. So,
let's see. Another question that I had
for you, technical question. You
mentioned going back a little bit, you
mentioned, you know, there's lasers
involved. Those that's what's creating
the light for all of these. And you
pointed out um very quickly that there's
actually some names who make LA lasers
for data centers who also make lasers
that are used in LAR, which I think is
super interesting. You know, I think a
lot of these names, the optical names,
um, they had a great 2025, you know,
lummentum coherent. Um, because
everyone's realizing like, oh, with the
rise of all these GPUs and data centers,
all the GPUs need to talk to each other.
They do that, you know, as we've
discussed before, uh, scale out. It
requires optical transceivers. There has
to be a laser in it. Um tell me who are
some of the folks that make these lasers
for these essentially edge AI
applications. So for LAR.
&gt;&gt; Yeah, I actually looked it up only
recently in my original investigations.
I didn't really look at uh the suppliers
as much as the technology and I found
like there are three big players in this
field. The first one is a company
honestly I have never heard of and
that's because I don't work in LAR. Um
so it's probably completely wellnown.
It's like saying I don't know who Nvidia
is to somebody but there are people who
probably are like oh how does this guy
not even know this company anyway it's
called AMS
Oram how do you that's how I think it's
said you know AMS OSAM OS RAM anyway
it's a company in Netherlands I think uh
they are actually the world leader in
edge emitting lasers uh so those are 905
nanometer lasers and they are pretty
much the biggest supplier to automotive
LAR
companies and they have the highest
volume. So this is a very big player but
they deal primarily in the lower
wavelength um LAR technology and then
the other two big players are the data
center players that everyone is talking
about these days that you just
mentioned. Lummentum uh actually is a
leader in uh vixels or vertical cavity
surface emitting lasers and they focus a
lot on the consumer side and uh they
were a supplier uh to Apple for face ID.
Face ID is not exactly LAR but anyway it
works based on light uh in a point grid
and it measures the distortion of the
grid and then tells where's your nose
and the eyes and your mouth is. So
that's how it works. It's not exactly
LAR but anyway uh yeah and I I also
found out that uh ouster uses Lmentum
for their digital LAR technology. So
this company that is going to become u
or what everybody at least wants to
believe is a predominant supplier of
lasers for co-ackaged optics and all the
optical scale out and scale up but
whatever that people are talking about
in data centers. Lummentum is a favorite
pick for all these people talking about
this. This happened to also be a big
supplier in lasers for uh you know
consumer applications.
And the third player is uh coherent.
Again coherent is specializes in high
power 1550 nanometer lasers. So they
they do the fancy stuff. Uh and you know
as we discussed earlier this needs the
fancy detector with the indium gallium
arsenide. So people don't a lot of
people are becoming anti-550 now and
that's causing some grief to coherent
right now. Uh but the good thing about
coherent is that they are vertically
integrated. They have their own fabs to
do this stuff and that's a good thing
for them. So really these are the three
big laser sources uh that people use in
LA technologies. A lot of overlap with
data centers.
&gt;&gt; Interesting. Uh I I love that we didn't
even know that they already play in this
space. The fun, you know, as you kind of
pull apart various supply chains to
realize how interconnected some of the
players are, which makes a ton of sense.
If you make lasers, what are all the
applications? Definitely.
&gt;&gt; Yeah. Yeah. And you know, Austin, this
may be a thing that you and I look at so
much data center stuff. Maybe to the
people who are listening to this, they
like obviously are these guys even
listening to the earnings call. That's
true. They they did mention vixels and
they have all this. Why do you think
they have vixels? But of course, vixels
are used in data centers too for like
lower level like lower speed
communication, blazers and all that. So
yes, this is news to some may not be
news to some. Yeah.
&gt;&gt; Hey, I'm learning.
&gt;&gt; Yes, likewise.
&gt;&gt; Yes.
So, okay, we've covered a lot about the
technology behind LAR and I hope people
have appreciated that, have learned
something. We talked about some of the
suppliers. Um lastly, I think that the
market dynamics around LAR are very
interesting. How many people can win in
this space? You know, how do companies
differentiate that their LAR is better
than another person's lidar? And this is
something I plan to dig in deeper in in
future articles. Um but did you have any
quick thoughts as a teaser at all?
Yeah, I mean the biggest pressure is
coming from Chinese companies doing LAR
and uh from what I could do with my uh
base level of research, it seems like
Robocense and Hessi are the two big
companies are really making cheap or
rather inexpensive LAR that uh people
are really starting to use and a lot of
these companies are focusing on being
vertically integrated make their own
lasers
So they don't want to buy stuff from
momentum and coherent if they can avoid
it. So we have to see how far this
vertical integration is going to take
off. And I also read that Hesai
announced at CES 26 that they're
doubling their laser production. So
that's that's some important news I
would think for the LAR world. U but of
course in our last episode we only spoke
about the Nvidia portion of CES. It's
such a big show. There was so much
interesting stuff but this is another
nugget from that one.
&gt;&gt; Yes. Nice. Good. Yes. I agree. Both the
vertical integration as a means to
reduce cost is interesting. And then of
course the big story is as we'll see in
the future is definitely the China
market versus the western market. And of
course right now there's the whole
geopolitical angle. So you know there's
conversation to be had around will there
actually be two markets here? Would an
uh American automotive company put a
Chinese LAR in their vehicles and vice
versa?
&gt;&gt; The the China discussion really depends
on you know people are making chips
that's entirely different from a light
source. Like a light source can't spy on
you, right? I mean so it's it's really a
supply chain question and it it it ties
into the larger geopolitics of the whole
thing and you know recently also there's
been some kind of shortages of Indian
exports from China because the
government does not want to uh ship out
all this stuff. So they they they placed
export restrictions that affects a lot
of optical companies. So as much as
coherent and luminum where all the talk
late 2025 and the optics uh world
uh recently it's been facing a whole lot
of headwinds and the stock prices are
depressed and stuff or because of this
geopolitical angle of people suddenly uh
not believing that they're going to get
indium for making these lasers or you
know there are other concerns why but
you know regardless this this China
versus the western world debate pervades
through all of semiconductors. It
doesn't matter if it's data centers or
GPUs or even LAR sensors or laser
sources. It's everywhere.
&gt;&gt; It is. It is everywhere. We'll leave it
at that. Thanks for listening. I hope
you guys enjoyed this uh LAR deep dive.
Um if you're enjoying Semi-Doped, we'd
love if you gave us a rating and a quick
review in Apple Podcast, Spotify, or
wherever you listen to this. And of
course, check out Vick's newsletter and
Chipstrat. Thanks for listening.
