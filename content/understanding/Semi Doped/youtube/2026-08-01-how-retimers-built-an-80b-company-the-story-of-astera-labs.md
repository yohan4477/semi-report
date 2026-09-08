---
source: https://www.youtube.com/watch?v=u3Le3CBnFM4
vid: u3Le3CBnFM4
title: How Retimers Built an $80B Company: The Story of Astera Labs
date: 2026-08-01
duration_sec: 2865
channel: Semi Doped
kind: transcript
---
In March 2024, a company almost nobody
outside of the industry knew IPOed at
$36 a share. This June, it hit $499,
joined the NASDAQ 100, and printed 93%
year-over-year growth at 76% gross
margins. Astera Labs doesn't even make
GPUs. They don't make memory. They don't
make optics. Astera makes the chips that
fix copper. The little devices that
catch a dying high-speed signal halfway
down the board and relaunch it clean,
unglamorous, invisible, and in every
single AI server Nvidia's partners ship.
Today's episode is a story of how a
repair part became a franchise and how
that franchise is now going after the
biggest socket in the AI rack.
Hello everyone, welcome to semi-doped.
I'm Austin Lines of Chip Strat and with
me is Vic Shaker of Vick's newsletter.
So Vic, let's talk Astera Labs, but
let's talk retimers. Like when I first
heard about rettimers, I was like, what
does that even do? What does that mean?
So what do what do you say? Should we
get into that today?
&gt;&gt; Yeah. Like let's talk about the problems
uh of copper connectivity which we have
spoken about a lot before, but I think
rettimers is an interesting concept
because we always talk about stuff that
is outside let's say a server tray,
right? We talk about how GPUs are
connected together and scale up. We talk
about how to connect racks together and
scale out and scale across all of that
stuff. But what we've never covered is
how does a GPU connect to a CPU
within a server tray or how does a GPU
connect to the network interface card or
the nick? We'll keep referring to this
as the nick nic network interface card.
So how does that connection happen? You
know, it may not seem like it's much of
a connectivity problem because come on,
how far are these things, right? Like
the server tray is maybe this, you know,
yay big with about 2 ft wide by 4 ft
deep. But
that is still a problem because the way
you connect a GPU to a CPU or to a nick
is through the uh PCB that is inside the
server rack, right? Like it's it's a
host board that is holding all these
chips. And so those are not like
excellent conducting mediums to carry
high speed signals, right? And so that
is the problem we're going to talk about
today and how Astera Labs solved that
problem and became pretty much an
integral part of what is inside the
server rack server tray today.
&gt;&gt; Awesome. Interesting. Let's get into it.
Yes. because already you got my wheels
spinning because you're talking about
copper PCB traces and high-speed signals
and we've been talking about like with
with Credo uh you know um and active
electrical cables like the copper
problem. Um so yeah, let's get into it.
When a GPU talks to a nick and it talks
over this uh you know PCB trace like
what are we what are we talking about?
Okay, so let's go back from the
beginning and like set the stage quickly
but also in a complete fashion so
everybody understands what's happening
in this uh part of the AI stack right
fundamentally what happens outside you
know we always talk about NVL link for
scaleup or you know Ethernet or you know
infiniband all these things these are
all like outside
the server tray what happens inside is
something that has been around like very
long Right. This is then every PC that
you build out. It's been in gaming PCs
forever. It's called uh PCI Express or
PCIe. Okay. So PCIe is how uh the GPU
communicates with the CPU or the nick
for example. It's just a protocol that's
been around for a very long time. So the
whole idea is that these don't have to
run very fast on a single lane basis.
However,
uh they have many parallel lanes. So a
PCIe interface can have uh 16 lanes and
so it's called a PCIe x16. Now the way
this is dealt or dealt with or spoken
about is that uh you have so many giga
transfers per second, right? So you can
have uh let's say a gen 5 uh PCIe
uh you know has essentially let's say 32
giga transfers per second. This was
actually used in the hopper era anyway
for connectivity. So what that means is
that why why are we saying transfers and
not like bits right transfer we are
talking about transfers because we are
talking about transferring a symbol a
symbol can be a collection of bits. It
can be one bit is one symbol which is
basically this NRZ modulation zero or
one very simple
&gt;&gt; or it could be a PAM 4 modulation which
is like four levels right uh so you
could have different kinds like so when
you do PAM 4 you have two bits to a
symbol so giga transfers means you're
transferring 32 billion symbols of
either one or two bits uh every second
so if you look at that in the time
domain Like let's see like how so what
are we talking about? How many symbols
every second? So every every 31.25
picosconds you have a symbol going by.
So you think of a string with like a lot
of beads on it and each bead is a symbol
and the beads are moving from left to
right. Right. So that's that's how it
looks. Uh if you kind of imagine bits
moving on a wire and that's exactly
what's happening between the GPU and the
CPU.
&gt;&gt; Did you say picosconds like 10 the
minus12?
&gt;&gt; Yes. Yes, it's very less. Yeah, it's
very it's a very small amount of time
and that's what it takes to transfer
like a billion symbols per second. It
takes pico seconds like you know it's
very very small period of time and so
the thing is that it's not easy to do
this. Okay, it's not easy to move bits
across from one place to another because
it faces several problems. Copper is a
pro problematic medium and when you try
to push these bits from one place to
another things go bad. Okay. So one
thing is like loss right like you know
you put you know a signal of high
strength in one end and it loses all its
strength by the time it reaches the
other end of the wire right that's one
problem then the PCB itself has problems
and all that and then these things are
like high-speed signals so you you can
think of them like sometimes they
pingpong so they reflect from that end
so you can think of the beads trying to
come back on the wire you don't want
that right those are reflections
&gt;&gt; right uh then cross talk you know if you
put two sets of beads uh uh next to each
other. Imagine if one bead on this
string is affecting the bead on the next
string. That's a that's a terrible
outcome. But these things happen in
copper. So all of these things they
basically need correction. They need
some way to fix this, right? But that's
just the copper thing. Actually I should
mention that there are two more problems
we should talk about and that is inter
symbol interference is one of them.
Which means the beads on a string don't
actually stay like one bead on the
string. Like imagine that you know
they're made of sugar or something and
they try to like stick to each other and
try to become you know one larger ball
of sugar instead of like staying
distinct sugars like as they travel
really fast you can imagine they like
heat up or something and then try to
stick and become one and like a blob
right that actually happens all the
time. So when one symbol travels the
next symbol kind of starts to overlap
with it and it starts to spread out and
that's terrible right? You don't want
inter symbol interference.
Let me jump let me jump in there for for
listeners you know so you can think of
if you're familiar with like square
waves or sine waves like if you have a
square wave you can imagine that as it
travels down this medium it starts to
spread out instead of being a square you
know maybe it's like more of like a hill
and so you can imagine if you're sending
these different like pulses in the
simplest sense that as they start to
spread out they could start to overlap
each other to Vick's point of like the
sugar sticking together so now all of a
sudden instead like a a a steep up to
one, steep down to zero, some space, and
then another steep up to one. You start
to get like a ramp up to one and a ramp
down, and then maybe it overlaps another
one to the to the point where what you
receive is like a 0.5 and you're and
it's slowly transitioning and it's a
little bit confusing. Is this a one or
is it a zero? And then, of course, to
your point, as you mentioned earlier,
there's this attenuation. So, by the
time it gets all the way down the
copper, it's just like lost, you know,
the peak amplitude as well. So, um, but
but back to the inter symbol, um, sort
of overlap here. Yeah. There's like this
smearing where you tried to send certain
symbols and they're kind of overlapping
each other and somehow we have to figure
out what was said at the end. Yep. Carry
back on. What's the Yeah. Yeah. What's
the the next one that you were going to
mention?
&gt;&gt; Yeah. The other one is jitter, which
means that the pulse is not where you
think it is, right? uh the pulse you
think you sent it uh some time ago but
by the time it reaches a given location
it's it isn't there
are random uh variations in the system
that cause the pulse to be further than
you think it is or like earlier than you
think it is. So when you go in be like
okay at this moment I'm going to look
and see if this is a one or a zero and
I'm going to like lock it down right
like that's what you were saying like
&gt;&gt; let's say that you know the.5 question
isn't a thing like we are constantly
monitoring this particular point on the
wire and we're going to be like okay
when the thing comes I'm going to call
it a one or I'm going to call it a zero
but the thing doesn't come at all or it
comes like you know late and you're like
what happened so now you can't detect
the bit because the thing wasn't there
when you expect it to be there that
thing is that thing is called jitter.
And that also causes problems in
communication. All of these are big
issues.
&gt;&gt; Gotcha. Okay. Yeah. So, you're saying
like with jitter, it's like if I'm
thinking about like I'm on a clock, I'm
at the end of the wire, I'm checking and
it's like what am I reading? What am I
reading? What am I reading? It but but
nothing comes but then it comes a tiny
bit later like in between readings or
something, you know? It's like what's
going on here? But let me ask you, Vic,
um between the inner symbol interference
and the jitter, like how much of that is
deterministic? like we can figure out,
oh, this is copper and we know how a
high frequency symbol behaves and how
much of that is just like random noise
or random something [clears throat]
randomness. I think that um inter symbol
interference is somewhat deterministic
and you can kind of figure it out and
there is a way to do this and I'll get
to that. Jitter is more random. you
really can't do much about it and all
this affects uh how we will ultimately
detect if it's a zero or a one. See that
the whole problem here is to tell
whether at any particular instant you
have a zero or a one. If it's a
two-level modulation, if it's a
four-level modulation like PAM 4, you
have to tell which of the four levels it
is. M
&gt;&gt; and typically they they talk about it in
PAM 4 as
&gt;&gt; uh 0 1/3 2/3 and 1
&gt;&gt; instead of trying to use something else
they just uh break up the one into four
four levels right so it's up to you to
tell what the level is that's the whole
problem
yes okay yeah I could see how that's
challenging especially for PAM 4 like if
you're trying to read zero volts is 0 0
a third volt is 01 on 2/3 volts is 1 Z
and a volt is uh 1 one or something like
that. How um now all of a sudden when
there's that smearing and stuff, it's
not like oh is it a zero or one and
we're at 0.5 and we don't know. Now it's
like really crazy. It's like oh it's
supposed to be zero or 0.33 but I got
0.28 volts or 0.16 volts or you know
it's tighter. There's like less there's
less margin.
&gt;&gt; Yeah. Yeah. There is a nice way to
visualize this and you will see this
mentioned a lot in this interconnect
world and those are what are called eye
diagrams. Okay. And I'm just going to
explain quickly what that is. So imagine
at this one particular time called a
unit interval. That is basically the 31
picosconds that I mentioned because you
know that that is the symbol uh period
right that's that's the period. So that
thing is called a unit interval and is
usually on these charts you'll see it as
UI [snorts] and so you're looking in
that unit interval and you're seeing all
the bits that go by like you're looking
at just one beat on the string but this
that bead is moving right like you're
continuously looking at the string think
of it that way and what you're looking
at is an overlapping bunch of zeros and
ones for example and always you want to
have some kind of a separation between
zero and one right so that you can
clearly say anything above
75 is a one or anything below 0.25 is a
zero like we just round up that round
down that way and so but nothing should
be there between 75 and 025 because you
don't know where it goes. The
uncertainty is too much, right?
&gt;&gt; Yeah.
&gt;&gt; So that that gap is usually referred to
as the eye opening. The eye of this
signal must be open because if the eye
closes, which means there is no space
between the voltage levels, you can't
tell what it is. So the eye opening
determines everything.
&gt;&gt; Okay. Okay. So you you basically take a
bunch of snapshots at this unit interval
and then plot them all like on top of
each other, right? So you take like a
thousand of them and in the ideal sense
you would have like a like a rectangle.
You have a bunch of ones and a bunch of
zeros and that's it. But of course it
there it like takes time to get up to
one and time to get back down and so
that's why you kind of end up getting
this eye shape because it like ramps up
and ramps back down and and same and but
to your point is when you throw
thousands of these measurements on top
of each other, there should be some sort
of gap where it's very clear, hey,
there's nothing in here. So it's clearly
a zero or one. But if they start to like
if that gap closes that's bad news
because hey some of these the
measurements that we took are in the
middle and we won't know what to call it
exactly. So now the whole problem of why
Astera Labs uh solved this problem is
that they needed to find a way to keep
this eye open when the communication is
going between a GPU and a nick or a GPU
and a CPU and the distance is in the
range of like about 30 cm. It's not that
much, but it's still required because at
the speeds that we're talking about
because gen 5 is 32 giga transfers per
second. Gen 6 is 64 GB, you know,
transfers per second and it goes to PAM
4. So that makes it harder because
you're adding more levels and you're
going faster. So it really requires
retiming. And then in the future um we
will go to Gen 7 which is at 128 giga
transfers per second with PAM 4. So Gen
6 is already in I think in the Blackwell
era of chips it's being used. So yeah
we'll get to all this but so Aster Labs
is basically
their job is to keep the eye open within
a a compute tray. That's their whole
purpose with rettimers. So what are
rettimers? Right? Let's get to that
portion because we need to talk about
okay now we have inter symbol
interference um and we have jitter whose
main effect is to close the eye. Now we
have to find a way to fix it, right? And
there are a few tools to do this. Okay?
I think we should first introduce the
idea of uh equalization.
It's a fancy way of saying look, I'm
going to lose half the signal like down
the line. So what if I just boost the
signal twice now so that by the time it
reaches that point, it'll still be like
what it was here because I amplified it
beforehand. And so that when it degrades
later I can I can uh keep the voltage
level constant. Right? So that is
equalization. You're basically applying
the inverse of what will happen to the
actual signal. Right?
&gt;&gt; So okay let me let me interject really
quick. So back to the eye diagram. So
you're saying the problem is the eye
starts to collapse especially if we just
don't do anything but it we're
increasing the speeds. of course it's
copper and so kind of the the distance
at which you can effectively like keep
the eye open is shrinking. Um and so the
so the question is you know how do we
keep the eye open and you're saying like
one of the simplest ways is sort of like
hey if if we if we know that it's going
to like uh attenuate or degrade as it
goes through can we just amplify it? And
it's kind of like um if you and I were
in a hallway and I was talking to you
and then you went and went a lot farther
away, I would just shout so that by the
time it got to you, it would sound
normal. Yeah, exactly. That's a good
analogy because you know, you can kind
of see how far away that person is and
there's no point talking softly because
you know they're not going to hear it.
So you would like adjust your volume to
be good enough so that you have a good
chance of them hearing it at the other
end. Yeah, exactly. That's a good
analogy. I like it. That's on the
transmitter side though. That's that's
what you can do by shouting in louder.
But what can the receiver do? What can
the person on the other end do? Right?
&gt;&gt; Uh that's that's what uh like what you
will often uh see as CTLE is is called
continuous time linear equalizer. Okay.
So this is um like a long acronym but
it's in concept it's relatively simple.
Okay. Um
it is
just that you want to amplify the high
voltages
more compared to the low voltages so
that you can kind of stretch the eye
open. Imagine that you you have remember
I told you that you know 75 or above is
a one. Now what if you can just amplify
the 75 to make it 0.9 so that the eye is
even more open and what if you can make
the 0.25 0.25, you know, 0.1, you know,
so now your eye is like a much nicer and
much wider open. So you can amplify the
highs while keeping the lows low.
&gt;&gt; Okay? So that's that's one way the
receiver can deal with this um problem
of all these channel imperfections that
happen. Uh this is still analog stuff,
okay? There's no like digital work going
on. This is just a simple amplifier.
[snorts] But the problem with this is
that it amplifies all the high frequency
noise stuff. like if there's any noise
and all that, everything gets amplified
because it's it's just a dumb amplifier
like it amplifies high signals and
keeping the low signals low. That's it.
That's not a good thing. And if there is
any interference from the neighboring uh
bits moving up and down, it'll amplify
that as well. So, it's not it's not
entirely very clever. Uh but it's it's a
necessary part of the system.
&gt;&gt; Yeah. It reminds me sort of like naively
like if I'm the receiver, if you're at
the other end and and we got far away
and you shouted and then uh I can kind
of hear you, but instead I'd like put
headphones on and I just hold a
microphone and then the microphone sort
of like does that. It like hears you and
I turn up the gain or something and it's
like, "Oh, okay. You what you said at
one volt was down at like 0.75 by the
time, but then this microphone just
amplified it back up to one volt and I
can hear it fine."
&gt;&gt; Yeah. Yeah. Yeah. Yeah. Yeah. Exactly.
Exactly. So now there are other other
ways there's one other way we can do one
other thing we can do with the receiver
and I think it's a little bit important
and this is uh this is the clever one.
So what this does is remember that it's
a very good question you asked me before
as to which of these errors uh inter
symbol interference or jitter is like
deterministic and the fact that inter
symbol interference is deterministic
actually helps because you can predict
you know how this spreading of the
square pulse into hills happens
beforehand by running some tests on the
channel and you know how it spreads and
then you can like back calculate and uh
subtract it out of the received signal
because you know how much spreading has
happened and so you add it back or
subtract it back and you reconstruct the
waveform. This is called a decision
feedback equalizer. So it just knows
what's going to happen in inter symbol
interference and it cancels it out.
Gotcha. Nice. That's that is pretty
clever. So does it look at like it
depends on like what I just received
like oh I know that I just received one
one 01 and therefore I can calculate
sort of in real time what kind of like
noise or smearing or interference I
would get from that particular pattern
based on this particular channel.
&gt;&gt; Mhm. Yeah. So it has some kind of a
characterization
uh and then it uh reconstructs it based
on how much it knows the spreading or
the smearing has happened. Very clever
stuff you know very complicated stuff
and it is because of this that even Gen
5 PCIe works. It's a very essential
component. Uh these DF are very
essential components right
&gt;&gt; does that really quick does that have to
get tuned in manufacturing like per
board or something?
&gt;&gt; I think it does. Yeah I think it does.
Um
&gt;&gt; interesting. So it's not it's not all
that straightforward to do, but uh it is
a system that's been around a while. So
it's not like ultra new, but these are
all like um very clever uh chip design
techniques. You know, there are these I
have some friends who actually do this
for a living and they're really good at
it. Uh they're like these analog guys.
They're awesome. Okay, so and when you
go to these conferences like ISCC and
all that, you'll see all these designs
of how they do this. It's quite
complicated. let's just say uh just
we're just trying to cover it at like an
extremely superficial level but the
reality is very very hard. Uh finally I
think it also extracts what is called a
clock and data recovery. So, uh, what
that means is whenever, let's say I'll
be like, Austin, whenever you see a
symbol go by, just clap. Okay, just clap
for me. And I'm going to sit here and
kind of write down all the times that
you clapped.
&gt;&gt; And I'll be like, "Okay, I know the
period of the symbol. I know I know the
clock now. So now I can set like a
metronome. You know what a metronome is?
It's like that music thing that goes
click click click click." So I can set
the speed on my metronome
&gt;&gt; and uh that should work out well because
now I know when bits are coming just by
hearing the sound. So I have recovered
the clock this way. Right. That's pretty
clever and that kind of helps with that
problem that we had talked about where
it's like if I'm on a particular clock
and stuff isn't flying by right when I
expect I'm like man this isn't lining up
but but you're saying no no do the
opposite. Just watch what's happening
and then figure out the clock from that.
&gt;&gt; Yeah figure out the clock. So this is
all these are all the techniques that
people use to correct it and pretty much
this is all there is to it. So you can
do the the just to quickly summarize you
can do the equalization at the
transmitter thing. Remember you said
like just shout louder you know or you
[snorts] can do at the receiver side you
can do the equalizer on the receiver
side which is like just put a little
amplifier or some microphone and turn it
up. Uh or you can do the decision
feedback equalizer which is you know
what the smearing is happening. I don't
think we have a very good analogy for
this but you know you can reconstruct
based on the inter symbol interference
and finally you have to recover the
clock too by you know basically clapping
out and fitting a metronome to it or
something and you figure out the clock
with all this information you can kind
of tell to a high degree of accuracy
what the received signal is going to be
doing and you can correct for errors
with these methods and that is
essentially with all these build up a
full you know PCIe channel in the
transmitter and receiver and you with
this chain you can build what is called
a rettime timer. So and I I wanted to
also mention the clock and data clock
recovery process because it ret times
the signal right and I'll tell you what
that does in in just a minute. So now
I'm going to just explain what is a red
driver and what is a rettimer because
this is a very there there is a
difference here. Okay. So red driver has
it does everything that I just said but
it does not do the clock and data
recovery part. Um and it it also does
not do the decision feedback equalizing
cuz I think it needs some amount of uh
like uh sophistication to do that. So
imagine you're just shouting louder and
you're using an amplifier on the other
end or a microphone and picking up the
signals better.
&gt;&gt; That is called a red driver. It is just
an analog megaphone. That's it. And
&gt;&gt; yeah, you're just driving the signal on
one end of the the other.
&gt;&gt; Yeah. So what are the benefits of this?
Yeah. It lo uses lesser power and
energy. It's less complicated. You know,
a red driver is simpler and uh things
are good. That's it, you know, and you
don't have much latency. You can do this
quickly, low energy, all that stuff. But
the downside is that when you go to
faster and faster signals, you got have
more and more crazy things happening to
the signal. You can't recover it. So now
what do you do? You have to go for the
whole enchilada and go for full retiming
where you get the decision feedback
equalizing to remove inter symbol
interference. You recover the clock. So
it's not just that uh you amplified it
but it's the retiming process basically
accumulates all these bits and sorts
them nicely into the windows they are
supposed to be in because you remember
you have the metronome clock so you know
where the bits should lie because your
the clock that you recovered tells you
where they should lie. So you can take
these bits that arrived late or that got
messed up somehow and slot them into the
correct time slots and now you have a
beautifully recovered signal because you
took the bits you received and you put
it on where the clock should be. So you
rettime the received signal based on
your recovered clock.
&gt;&gt; Yes. Okay. Okay. So to to sort of
simplify it like back in the analogy of
like when you and I spread out the
further out we go I shout louder. you
have a little microphone and headphones,
but eventually it just doesn't work. Um,
and so because whatever in this analogy,
we're just too far apart. And so this
essentially with the rettimer, are we
ultimately just putting someone in
between us and like I'm shouting and
they're listening to what it what I was
trying to say and then they're sort of
cleanly repeating what I was saying down
to you. Um,
I think it's a little bit different.
That sounds like it's more like a
repeater to me, a repeater amplifier to
me. This is not really that.
&gt;&gt; This is uh like somebody who
knows what is going to be said on the
other end to some extent. Like
I'm going to talk to you about you know
rettimers and you are an expert on
rettimers and so even if you hear it
faintly you kind of have an idea of what
it is that is being said when you hear a
garbled word you're going to be like oh
he's talking about rettimers so he
probably meant clock and data recovery
because a a general person who's not
familiar with the domain would not
understand that word but because you
heard it halfway and you know the
context you can kind of reconstruct it
better than a normal person would.
&gt;&gt; Nice. Nice. Very good. Okay. Okay. I'm
tracking.
&gt;&gt; Okay. I hope everyone else is too. But
yeah, so this is very important. So
these rettimers now that we under got to
the point of retiming these rettimers
are what make sure that
bits from a GPU make it to the nick so
that you can then go do scale out or the
bits from the GPU make it to the CPU and
then you can do all this agentic fancy
stuff right the bits have to make it
from point A to point B otherwise you're
not going to have any communication so
this was this is a problem that
essentially Aster lab solved uh for
Nvidia and in their HGX baseboard I
think the H100 which is just it had like
eight GPUs in it they needed to make
sure that things can communicate uh with
each other on the board on the on the
board. So that's what this this rettimer
chip did [snorts] and it really got off
Astera Labs to a running start for sure
because you need about a one is to one I
think a rettimer chip
&gt;&gt; for every GPU. You might even need two
on either end,
&gt;&gt; you know.
&gt;&gt; So that's like a fair bit of content
that goes into uh Nvidia
uh H100. And at the time that HB1, you
know, came out, like that was when like
AI exploded pretty much.
&gt;&gt; Totally.
&gt;&gt; And winning this slot was like fantastic
for the company, right? Like because
[snorts]
&gt;&gt; every hopper tray that was made had
Astera chips in it.
&gt;&gt; Everybody and they had like a large even
now they have a pretty large market
share. So imagine how much money can
come out of that business alone. And
this was called their Aries series of
rettimer chips. This was like their
first product line.
&gt;&gt; Yes. Yes. Okay. Let's get into Astera.
So what I'm hearing you say is that when
Nvidia exploded and things took off with
the Hopper era for every single GPU that
was ever sold, there needed to be a
rettimer. So so that the GPU could talk
to the nick, for example. And my
question is, how did a startup own that
socket? Where did ATALabs come from? And
how did they get into presumably the
H100 reference design so that they would
get designed in? Like that's amazing.
That feels hard to do, but it's
incredible.
&gt;&gt; That's a good question. But these guys
uh I was looking at the company earlier.
Uh all the founders are actually ex
Texas instruments guys and they were
basically high-speed interface folks and
their ultimate bet was that in 2017
uh they left TI I believe and their bet
was that that PCIe5
would be required on every server board.
That bet was turned out to be right.
&gt;&gt; Gotcha. So they saw they saw this
coming. they they said, "Oh, every
server board
&gt;&gt; e even presumably CPUs um would need
PCIe
Gen 5 and at that speed we think copper
is going to fundamentally have a problem
and that these rettimers will
fundamentally be required." Yeah, they
they they they foresaw that coming and
that like as soon as servers go like
faster that uh they're going to have to
use these chips and so they they made
this whole company. Uh and then it was
it was great when um the H100 and the
chat GPT revolution happened was great
for Astera Labs. Uh the question was
when I was researching this I was like
why not why not other companies like
PCIe has been around a long time right
like but what's the what's the big deal
like why a labs why not broadcom why not
even TI um I think one of the smart
things they did was
uh they have I think they were first to
PCIe5 market so that is one thing
&gt;&gt; and the other thing I believe is that
they have this monitoring platform they
built pretty early on called Cosmos
which
not only tells you when the link is
going down or something is going bad but
it you know all this channel impairments
you know all this uh data that we all
this technical stuff we spoke about they
could capture everything on their
platform and you know hyperscalers
uh love that stuff too so I think the
software platform had something to do
with it as well and then when they get
qualified it is a major win because now
you're locked in. It's a very sticky
slot. Nobody wants to change this stuff
if it works, right? To
&gt;&gt; totally totally interesting. So, you're
saying like when they were seeing that
this socket was needed and rettimers
would be needed, presumably others saw
it as well. People who work on the Gen 5
spec, for example, would have known well
in advance, hey, we're trying to qualify
32 giga transfers per second. This is
going to be a problem. Um, but Texas
Instruments has a huge catalog, for
example, and so do other companies. And
so they might have just thought just
about like the rettimer as a component
in their catalog. But what you're saying
is maybe Astera thought like no it's
more than just a rettimer. It's also um
a sensor that can give you health
monitoring information about your entire
fleet. So we'll capture telemetry. We'll
build software around it, give you a
user interface and it's not just a
little um blackbox component on your
baseboard, but it's actually something
that can give you all sorts of insights.
So that for example, if you imagined
that the world of tens of thousands,
hundreds of thousands, millions of GPUs
in a training cluster, imagine if they
can all be telling you about the health
of their link, for example. I I can
definitely see how obviously that's
supremely valuable for the end customer,
but also that it might take a company
oriented around that mindset of this is
more than just a little component on a
board. But obviously, it's very
customer- ccentric. And then to your
point, of course, sometimes when there's
I I should say a good time for someone
to try to take some market share is to
obviously be first to that next
generation thing um or create a market.
And of course, if they were there first
and they got designed in, then all of a
sudden now it's like their socket to
lose even though they're a startup. And
again, this is the beauty of fabulous um
companies, which is, you know, your fab
partner can manufacture at scale. So if
you can get designed in, you can figure
out h you know how to build these things
at scale and and now it's sort of your
game to lose.
&gt;&gt; Yeah. This is the benefit of startups,
right? They can pick a problem and just
go after it. Bigger companies uh are not
as nimble and that's that's one of the
nice things about this industry that
somebody can come in and disrupt
something amazingly different and which
is why we would love to you know also
talk to startups on the podcast and
stuff. This is a very interesting uh
industry because Broadcom did come in
later uh as a second source. They did
come up with a ret a similar rettimer
chip for doing gen 5 timers in 2024 but
by the time when you're designed in
you're designed in right like it's hard
to move because the hyp the Nvidia will
have to re-qualify everything and they
have to make sure that the channel link
budgets are correct. It's like a big
problem once you're designed in and it
works you're done you know. So the
question is did ASA keep the slot when
Hopper went to Blackwell? [snorts] Uh
yeah they did actually they did keep it
in the B200 boards as well and uh I
believe it was the A6 which is the Gen 6
part of of the same family which was
doing 64 giga transfers with PAM 4. So
they had like a fancier chip. Of course
this this chip has more ASP. Good for
money, right? Yeah. So uh
all through you know the money every
time they sell these chips the revenue
keeps going up and up and up you know so
you can see all these charts probably
elsewhere like that people are charting
all these revenue tramps right like for
Astra Lab so it's all public information
uh but yeah but one interesting thing
that happened in the blackwell era was
people got a little spooked because
Nvidia said like okay this is not
happening guys like the the distance
between the nick and the GPU is too far
so we're going to move it close by. And
now everybody like freaked out because
what does that mean for Astra Labs right
now? If you put them close together, why
do you need like Gen 6, I don't know,
some fancy rettimer chip or maybe did
you don't even need retiming if it's
close enough. Maybe you just go with a
red driver, cheaper chip, you know,
lower power. All well and good, like,
you know. So that was like a bit of a
scare, but as reality would have it, it
turned out differently. Do you want to
know how?
&gt;&gt; Yeah. Yeah.
&gt;&gt; So, what happened was uh it turns out
that not everybody deployed racks this
way. The the the gray the Grace
platform, the Grace Blackwell platform
uh had variations like there were a lot
of customized deployments going on for
whatever reason. I don't fully
understand why there were customizations
but everybody didn't use Nvidia's
so-called reference design where things
were placed in a certain way. there were
customizations as soon as customization
started to happen it wasn't the reach
went up again and so the rettimers were
required and then the second thing
happened which is the birth of like
custom accelerators like XPU the tranium
thing know all of that came in and once
all that came in like you're not no
longer tied only to Nvidia like the ASIC
world is wide open for you you can go
and do uh put rettimer chips in all of
those accelerators Absolutely. Totally.
There's a new TAM for you. And I could
see, you know, once people got used to
having the ret timers and the telemetry
information, it it might also be a
little scary to take that information
away. Even if Nvidia said, "Oh, if you
you if you put everything close together
in our NVL72
um configuration, our reference design,
you won't need it. It'll be great." But
I could I could see being like, "No, no,
I think we do want to pay to have that
telemetry and to make sure those signals
are clean."
&gt;&gt; Yeah. Yeah. Yeah. Exactly. So, I have
some numbers actually. Uh so, in 2023,
their revenue was about 115 uh million.
Uh after their hopper thing took off. Um
in 2024, they were at nearly 400
million. And in 2025
they moved to other product lines which
we will also briefly mention uh right
after this. They were at 850 million for
2025.
Uh and in Q1 2026
my note says that uh it is they're
already at about 300 million and it's
just the first quarter. So you're like
looking at a company that's going to do
over a billion in revenue now. So all
these are revenue numbers by the way.
&gt;&gt; So yeah. So you're looking at a company
that you know uh revenue just 3 years
ago was a 100 million and now they're at
a billion. It's an interesting story and
it's this general story of you know how
retimers and how getting the signal from
just a GPU to the other end of the line
whether it's a CPU or a nick could make
a company a billion dollars right it's
it's quite a nice story
&gt;&gt; that's amazing so of course one must ask
is it just retimers or is there life
beyond rettimers
&gt;&gt; there is life beyond rettimers because
this is where their [snorts] next uh you
know, big big move is really, you know,
the big socket that you mentioned in the
cold open basically is that they're
like, why why stay within why stay
within the tray, right? Like we know how
to condition signals. Why don't we uh go
up and make a full switch? We'll make a
switch, you know, and this is competing
with basically the NV switch or it's
competing with uh the Broadcom Tomahawk
switches. So they have their Scorpio, I
believe P and the Scorpio X switches. Uh
the P is basically for U scale out.
[snorts] So this is going to be pretty
much a tomahawk replacement switch. And
they have Scorpio P series switch with
up to like 320 lanes. It's a very high
red radic switch. And then the X series
that they have is basically uh for scale
up. It's like the NV switch replacement
that uh like anybody else could do with
like merchant silicon. So NV switch is
basically NV link and N N N N N N N N N
N N N N N N N N N N N N N N N N N N N N
N N N N N N N N N N Nia's switch, right?
But if you wanted a similar performing
thing you could do Scorpio X. So there's
that.
&gt;&gt; Yeah, totally. So you're saying Asteris
said, hey, what are our core
competencies? It's it's networking but
it's it's signal conditioning and we are
doing that really well with rettimers
but ultimately let's move into switches.
Is that because conceptually a switch is
like signal conditioning of every lane
plus routing
&gt;&gt; or something? So like is it is it pretty
conceptually similar?
&gt;&gt; Yes. uh the signal conditioning part is
but then the actual switching process in
packets and stuff isn't very simple that
straightforward because so far we're
just talking about signal conditioning
but how the silic the packet is actually
switched within uh a Scorpio switch
isn't that straightforward it's like
literally like how to build switches
right um and this this complexity
because it's not incremental is exactly
what makes this a very high ASP part
like they expect a lot of revenue from
the Scorpio switches uh because I
believe the a the tranium 3 uses this
Scorpio X as well in scale up. So yeah,
it's it's probably going to be uh quite
a bit of revenue from the Scorpio parts
um going forward.
&gt;&gt; Speaking of Tranium, does Amazon have
warrants in Astera Labs? I feel like a
lot of times I'll have to look it up. I
think they do. I think a lot of times
when uh a company like Amazon
works with a very early stage company
like Astera Labs um they also
&gt;&gt; to make sure that all their incentives
are aligned. they end up getting some
warrants or some ownership of the
company and and that that obviously can
help
&gt;&gt; um okay Astera
&gt;&gt; get the opportunity to build out their
port silicon portfolio and have the get
the right to play in train in future
tranium and then of course um it maybe
incentivizes
Amazon to put a silicon in in their
silicon when they can instead of for
example broadcom
&gt;&gt; yeah yeah yeah I mean that because that
there's another big big story there
which I briefly mentioned because it's
really interesting uh because you know
so AMD actually wanted to put as because
they are all about UA link right like
the open standard of hooking stuff up uh
AMD actually wanted to put a UA link
switch but there was no UA link switch
in the market so what Broadcom did was
they were like okay this is the only
thing that was available was a Broadcom
Tomahawk switch outside of like Nvidia's
NV switch or whatever So there's no
option. AMD had to go with Broadcom. And
so what Broadcom did like this is what
this is ruthless business, right? What
Broadcom did was they immediately exited
the UA link consortium and they're like
Ethernet is it you know they had like
scale up Ethernet Sue and then they
merged it with like OCP and called it
EAN
and they were like that's it you know
we're not doing UAL link. we are in. If
you are designed in with us, we're going
to go Ethernet all the way. It's
basically puts, you know, the nail in
the coffin for all these other people
who are trying to do UA link and they're
like, "No, we have the only switch in
the market and we're not doing UA link.
Screw that." Like, we're going, you
know, Ethernet. That's it. No more. And
remember, the tranium thing with the
Scorpio switch right now is uh is a PCIe
switch. It's not Ethernet,
&gt;&gt; right? PCIe could be used for all this
as well, by the way. and uh Amazon
tranium is running on PCIe but the
future of Scorpio switches actually has
UA link in there and it's probably a
2027 I think story um along with Marvel
who's also building something like this
for UA link now the the risk here is
like will AMD and the others uh go go
away from using Ethernet EAN and go jump
on UAL link and buy all these people's
uh switches or are they going to say no
forget it Ethernet is it we have been
designed in remember Astra Labs' own
story right when they got the Aries slot
on the hopper series Broadcom couldn't
nudge them out now what has happened
took the AMD slot because there was
nothing else in the market and now
they've cornered the Ethernet way and
exited the UA link consortium
now can they get back in that's very
interesting to see
&gt;&gt; yeah well we yeah we should do a deep
dive on this because I know that with
the Helios platform AMD is doing UALE
UAL UAL link over Ethernet and
[laughter] and so they're using like the
UA link protocol but they're doing it
over an Ethernet switch and so I do
think they're planning to take a step in
that next gen of Helios to moving to UA
link but to your point
&gt;&gt; Aster Labs in the market didn't have the
UA link switch ready in time so this is
like an intermediate step So I think
that you know Helios 500 and beyond will
be interesting to help tell us what
direction things go.
&gt;&gt; Yeah, for sure. UAL link is supposed to
be the more purer networking. Uh you
know you can you know GPUs you can
access each other's memory and all that
nicely with the ULink protocol. It's
built for this kind of stuff. It's very
you know low overhead very lightweight
protocol.
&gt;&gt; Yes. uh Ethernet and EAN and all these
are like kind of uh derived from the
previous era uh of Ethernet and is not
optimized for what AI needs today. UAL
link is more so. So we we'll have to
talk about these standards another day
because that's like a whole different
subject but I just wanted to like
mention like the two other things that
it's only a mention. I think Astera
[snorts] Labs has um
uh their Taurus product line which is
essentially uh basically the same signal
conditioning product but you put it
inside cable and you make an active
electrical cable out of it like AEC's.
So they have like these chips that they
can put in AEC cables. This is not like
a high margin business and they are very
clear that look our gross margins may go
down because this is not a high margin
business but we want to do it anyway.
like if there's a way we can use our
existing technology, we will, right? So,
they're like, we'll do it.
&gt;&gt; And then their newest line, I think um
is the LEO uh product line, which is
basically a CXL controller, which is
used to maybe pool memory and do that
kind of stuff, right? So, we it's still
that's still new. Um so, but there is
some promise. There are apparently some
design wins already. So, we have to keep
a tab on that. with CXL is a new topic,
a new episode for another day.
&gt;&gt; Totally. Totally. CXL is old, but it's
new and it's coming [clears throat]
back. Maybe we'll talk about another
time. But with that, listeners, we hope
that you learned a lot about rettimers.
We hope that you learned a lot about
Aster Labs and you had fun with it like
we did. So, thanks for listening. Check
us out on YouTube. Leave us comments.
Share this with your friends. Check us
out on Spotify, Apple Podcast, wherever
you listen. And of course, check us out
on X. We're trying to post this of
course on X as well as our daily takes.
If you like our daily takes, check out
our newsletter. Just go to semi-dop.com
and you'll find it under the daily tab.
And then yes, also follow us on X. We're
trying to share some clips there as well
so that if you missed some old stuff,
you'll get to see it again. Um, so thank
you for your support and until next
time.
