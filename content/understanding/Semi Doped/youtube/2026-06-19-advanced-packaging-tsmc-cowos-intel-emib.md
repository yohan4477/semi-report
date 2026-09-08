---
source: https://www.youtube.com/watch?v=1VbkgEHub5I
vid: 1VbkgEHub5I
title: Advanced Packaging, TSMC CoWoS, Intel EMIB
date: 2026-06-19
duration_sec: 4143
channel: Semi Doped
kind: transcript
---
These parasitics when it's becomes a
flip chips became lesser and like it it
was important for the RF work I was
doing and flip chip saved a lot of
design work because
when you design the chip it works just
as is. You don't have to account for the
package as much if it's a flip chip. It
is the chip. So, I think now there is no
chip without the packaging.
&gt;&gt; [music]
&gt;&gt; Hello everyone and welcome to another
semi-doped episode. I'm Austin Lyons
with Chip Strat and with me is Vic
Shaker from Vic's Newsletter. Hey Vic,
what's going on, man?
&gt;&gt; Uh I don't know. Are you a trillionaire
yet? Cuz I know somebody who's going to
become a trillionaire right about
sometime soon. I don't know how much
money he has. I'm talking about the
SpaceX IPO.
&gt;&gt; Yes, yes, it's Friday that when we're
recording this, Friday, June 12th for
listeners and right now today is SpaceX
IPO day and so Elon Musk is going to
graduate to from billionaire to
trillionaire.
&gt;&gt; Uh apparently it's I'm not sure really
how close to trillionaire he actually
is. It's just too many zeros. You know,
usually we record stuff
pretty close to when we actually publish
it, but
since I'm going to be traveling next
week, we decided to move this up a
little bit. So, if you're hearing the
SpaceX news and you're like, wait,
wasn't that like last week? What's he
even talking about? Yeah, that's because
we're recording it early this time.
&gt;&gt; Yes, totally. Yes, summer is for travel
and vacations.
Um yeah, so trillionaire, you know, I'm
just a thousandaire, so it must be nice.
&gt;&gt; [laughter]
[gasps]
&gt;&gt; It's just adding zeros. How hard can it
be? Come on.
&gt;&gt; Yeah, yeah, right. Just Just add a zero.
That's what I tell my kids when you grow
up. You just got to add a couple zeros.
That's your goal.
&gt;&gt; Yeah. [laughter]
&gt;&gt; [gasps]
&gt;&gt; Yeah, but it's it's nice though like
I think it's valued at what, like 75
billion or something? This is one of the
biggest IPOs in history. And so, it's
exciting. It's listed under the ticker
SPC-X.
Uh so, now we have this
publicly traded company that does
rockets, that does chips, that does AI,
self-driving cars, you name it, right?
And um yeah, what's interesting uh
compared to what you like we'll talk
about today is
uh Elon Musk's link to Terafab project,
which is closely tied with Intel.
Of which we'll be talking a lot about
today. So, it all checks out. So, the
SpaceX is like tangentially related to
what we're talking about today, which is
advanced packaging.
&gt;&gt; You know, there's an interesting thing
to Neuralink, which is like SpaceX and
all its projects is like the culmination
of deep tech is cool again. Deep tech is
valuable, right? So, it's like
satellites, space, internet,
electromagnetic waves. Um they make
their own PCBs, so fabrication,
manufacturing, and then like Terafab.
And And And But But But it does go all
the way up to they have XAI and they do
self-driving in cars. So, it does go all
the way to physical AI and and actually
to AI. So, they kind of do span the like
hard tech stack all the way from atoms
all the way, you know, to intelligent
bits.
&gt;&gt; And space.
&gt;&gt; [laughter]
&gt;&gt; And space. And yes, the
the vast universe beyond Earth. Totally.
[laughter]
&gt;&gt; Elon is everywhere.
He's omnipresent.
&gt;&gt; Indeed.
&gt;&gt; But it's cool. I don't know. I like all
these projects are technically very
interesting and like you The way The way
you put it is like Oh, yeah, you're
right. He's going all the way from chips
all the way to space and there's
everything in between, robotics and
self-driving cars, and that's amazing.
Like, that's a lot of cool tech in one
place. That's all I have to say about
it.
&gt;&gt; Totally. Right. And then, you know,
there he does the Neuralink stuff and
the Boring Company. So, he's got his
hands in all sorts of interesting stuff.
But okay, we'll save Elon for uh we
should give him a whole post sometime or
a whole episode, you know, but
&gt;&gt; Yeah, we should do SpaceX maybe at some
point. Let the IPO settle down. Yeah.
&gt;&gt; Yeah, yeah, yeah. They'll have an
earnings call, so we'll get to listen
and learn a lot and I haven't even read
like the IPO prospectus or anything, but
we'll talk SpaceX sometime, but today
we're going to talk advanced packaging.
But first, a quick message from our
sponsor. Today's episode is sponsored by
SambaNova. If you're running inference
at scale, you know the hardware
trade-offs between memory capacity, chip
count, and quantization. SambaNova Cloud
sidesteps these constraints entirely.
You get API access to frontier models,
including full precision deep seek R1 at
250 tokens per second with no hardware
lead times. Texas Advanced Computing
Center, OVH Cloud, and Hume are already
on the platform. Try it today at the
SambaNova dashboard. The link is in the
show notes.
&gt;&gt; Yeah, very important, you know, uh
advanced packaging is
basically what drives AI chips these
days and it's a such a bottleneck and
TSMC has been the typical provider of
advanced packaging.
Now, we have news that like Intel is
getting in some orders for their
EMIB processing,
uh which is also advanced packaging and
I should just expand it right up front.
Embedded multi-die interconnect bridge.
EMIB, right? That's EMIB.
Uh which is a way of connecting
different chips together on some kind of
a substrate. We'll talk about all the
differences between
um what TSMC's chip on wafer on
substrate is
and within chip on wafer on substrate,
which we will refer to as CoWoS,
uh there are many variations and flavors
of that and so we should, you know,
bring all those fine details to light
and then we'll talk about EMIB. What's
different from that? And then really at
the end we should hit on the whole
Google's commitment to EMIB technology
going forward. It's very interesting. So
yeah, that that's going to come in the
end so stick around for that one.
&gt;&gt; Perfect. So friends, you might first
want to start actually with advanced
packaging. What does that even mean?
What What is advanced about packaging?
And what even is un- not advanced
packaging? What is like simple
packaging? Um so let's let's start just
at the at the at the at the very basic.
So packaging So you know, we talk a lot
about wafers, TSMC making wafers and
making logic chips on wafers. Um and
we've talked about you know, the size of
these wafers and being like dinner
plates and it's these big silicon wafers
and everything gets patterned. We've
talked about lithography before, but
interestingly
when you think about your computer or
your phone, like there's not necessarily
like an exposed piece of silicon that
people see, right? You the the the
silicon that gets made on this wafer has
to get diced into individual chips and
then they need to be packaged, which is
basically everything that happens to the
wafer after it leaves the fab. Um
you you need connections
from the die to the outside world for
power, for signals, to get the heat out.
You need mechanical protection, plastic
or ceramic or something so that the die
actually survives the real world. So if
you like break open your phone, you
don't just see like this beautiful
silicon thing sitting there, you got
packaging and you know, you'd have to
like cut off the packaging to actually
get to the silicon. Um so
at the highest level, you know,
packaging is take af- like taking the
wafer, dicing it up, taking individual
die and then actually connecting them to
the surrounding environment, whether
it's a a PCB or whatever. Um anything
else in your experience as electrical
engineer to say very high level about
packaging?
&gt;&gt; The silicon itself actually, apart from
its interconnectivity to the outside
world, needs to be protected from the
elements.
And it also needs to be protected from
like electrostatic discharge and things
like this. All of this means that
packaging is important. You need to
protect a chip inside.
And while doing so, also be able to
connect to it because you just can't put
a piece of silicon in a phone and expect
it to do anything. So, the leads or the
connection points into the chip are all
done through packaging. So, it's an
essential step that has been around for
a very long time, right? So, the
earliest simple packaging approach was
wire bonding, which is just like a piece
of metal that comes from your PCB, uh,
maybe to the chip that is sitting on the
PCB. It's a very crude example. But,
yeah, it's just a metal wire that goes
up and over and connects into the chip.
Uh, this has been around for very long
time, and believe me, even in the age of
AI and all of this, wire bonds do exist.
Okay? They're still being used for a
whole variety of products
uh, because not all this advanced
packaging can handle things like, I
don't know, power chips. Power chips
require wire bonds because they need to
carry a lot of current. And so, there's
like big honking wires that are like old
school still work well. So, simple
packaging isn't dead. It's not like
something that's in the past and it's
like we've forgotten about it. Oh, those
were the days. No, it's still there
today.
Uh, which some applications require. So,
the other way to do this simple
packaging is like you flip the chip
upside down
and put solder balls there. And then you
put it onto a PCB, and, you know, you
melt the solder balls a little and so
that it sticks.
That is the flip chip approach. That was
a game changer in, I'd say, the '90s uh,
because
the connection distance between the the
chip and the external world just got a
whole lot shorter.
Using those wires are like so long, but
if you can put a solder ball and flip
the chip upside down,
it was amazing. Like it changed it blew
people's minds and it was like a
revolution in packaging in the '90s.
Because uh now performance and the
parasitics
the resistances and the capacitances all
got lower and the chips could work so
much better.
And everybody was like, "Oh yeah, flip
chip is the best."
And then ultimately it comes down, you
know, to you know, there are variations
of that in the future as it improved.
They made the distance between these
solder balls closer and closer and
closer. So you could put like more
connections into the chip. Like if you
wanted to put a thousand connections
into a chip, then you need the the
solder balls to have like a short
distance between them so that you could,
you know, put a lot of
uh wires into the chip like that. So
that became a big thing for how to make
these things smaller and smaller. So
that is the evolution of basically wire
bonding and flip chips. So just for
somebody who's never seen the world of
packaging before or anything like that.
&gt;&gt; Yes, totally. And so again, just hitting
it again, you know, wire bonding think
like the simplest thing is if someone
literally like if you're in just a lab
trying to build something for a class
and you had a wafer, you would probably
just literally like glue it onto a PCB
and then attach wires like from the die
like, you know, at the leads the edges
of the die or something to your PCB and
you can imagine that is both both very
labor intensive, it's very error prone,
and then you kind of have these weird
like exposed wires and like Vic said
they're long and they have resistance
and it just feels fragile, doesn't it?
And so of course, um this flip chip is
nice because now instead of having the
the top of the wafer where you have to
attach wires, you just turn that upside
down and you just have these short
direct connections. And now it's
actually the back of the wafer that's
kind of exposed to the elements, if you
will, and and the connections are made
by sandwiching these together and you
have these little micro bumps. Uh
and so you have like still uh electrical
conductors to to sort of help you attach
and connect the the die to the PCB below
it. But you can just see how ultimately
once you figure out how to do that with
high yield and at scale, then that is a
little bit less labor intensive, more
complex, but less labor intensive, and
also like more reliable.
Um and so you know, but for those early
decades, this the packaging is sort of
like the unglamorous part, like the the
manufacturing, the logic chip and
everything, that's like the the
front end of the process and it's it's
like where the value was captured and
and is complicated and very capex
intensive. And uh this packaging is
really like mechanical assembly and even
some like human assembly. Uh it's capex
light, but it's also like lower margin,
sort of lower value add. And and so
actually
the industry structure, you know, way
back in the day people used to
manufacture their own wafers and then
they used to some would do their own
packaging. But eventually actually some
of that packaging got outsourced to
OSATs, which literally stands for, I
think, you have to double-check this,
outsourced semiconductor assembly and
test. So if you ever hear the word OSAT,
that's what that stands for or the the
term OSAT. And these think of the
companies like Amkor, ASE, Spil,
Powertech, I think. Um so so
the foundry would ship finish wafers,
the OSAT dices them, wire bonds or flip
chips it, um molds it, you know, puts it
in its protective casing or whatever,
and then usually they do the testing as
well to to show that the final package
still works, works as as you would
expect. So, yeah, that's just for people
like rule of thumb to know like fabless
companies design it, a foundry fabs it,
and OSAT packages it. But, of course,
you could also have companies like Intel
and IBM where they do some or all of it
in house.
&gt;&gt; Yeah, so that's the whole uh
the basic coverage of what packaging is.
And this has been a very been around a
very long time. As a personal anecdote,
you know, even when I started working, I
did run into a lot of the packaging
guys.
Those were just like uh and it seemed
like it was a necessary evil. Oh, yeah,
we got to send it for packaging. You
know, there's nothing fancy about it.
There is nothing. It's just a grunt and
boring work because you got to make sure
that the package is designed well enough
so the chip can sit inside it, and they
do all these tests like uh whether it
survives the heat and it survives the
temperature, you know. It's like dotting
the i's and crossing the t's of the
semiconductor world. It
it did become a performance
limiter at some point
even in my own work that I have you know
early in my career itself because these
parasitics when it's becomes a flip
chips became lesser and like it it was
important for the RF work I was doing.
Those things matter. Wire bonds are
still terrible. So, because my work was
so parasitic sensitive and RF and all
that,
uh it was important. And flip chip saved
a lot of design work because
when you design the chip, it works just
as is. You don't have to
account for the package as much if it's
a flip chip.
However, as things got more complicated,
it became a part of the design process
itself.
It eventually became part of the chip or
an extension of the chip. And
throughout time now, you know, if you
look at all the AI chips and all that,
it is the chip.
There without advanced packaging as we
would call it now,
it is the chip. So, I think now there is
no chip without the packaging and it's
good to define now how we transition
into advanced packaging, right?
&gt;&gt; Yes. Yes, totally. So, if what we talked
about was simple packaging, then what is
advanced packaging? What puts the
advanced in advanced packaging? Well,
ultimately, now So, the goal is always
in a dream world, we would just have
huge monolithic silicon chips. And
because you would have like the fastest
communication and the lowest latency
between, you know,
dies or whatever. But as we've talked
about before and we can hit on again,
there's something called a reticle
limit. And so, you can only make silicon
dies so big. Then we probably talked
about it in the past, too, and we can
talk more again. There's also this
concept of chiplets, which is like, wait
a minute, some things don't scale when
you make transistors smaller like SRAM
or or maybe even like IO doesn't improve
as much. And oh yeah, we talked about
this last week on our Intel as we talked
about Clearwater Forest where um Intel
says, "Hey, yes, let's make the compute
dies using 18A with our smallest
transistors possible, but let's have
other Intel 3 dies and Intel 7 dies for
IO and memory and whatnot. Ultimately,
those need to get connected together.
Um and even if you're Nvidia making GPUs
where your GPU is the reticle limit,
they make it as big as they possibly can
and they actually want even more
compute, so they take two of those. With
Grace Blackwell, there's two GPUs and
they actually have two huge reticle size
GPU silicon die, but they want them to
behave the goal is always to can we make
this behave almost as if it's still just
one big piece of silicon. So that's
ultimately the goal. And and you can't
do that with wire bonding and you can't
really
a step in the right direction would be
would be flip chip but ultimately can we
do even better? And so advanced
packaging is saying, "Hey, could we
actually use the same semiconductor
processes as the chip it's the logic
chip itself? Can we use things like
deposition, etching, lithography to
actually pattern metal interconnect at
like micron scale pitches instead of big
old wires? And could that help us get
you know
a lower latency, smaller resistance and
going back to tau, like tau being the
time delay of signals communicating
resistance times capacitance, could we
try to shrink features even with the
packaging as much as possible to you
know, limit tau
and and really just all make it seem as
if these dies that are being stitched
together are are more like as if they're
on one piece of silicon.
&gt;&gt; Okay, yeah. So that's the fundamental
basis for the two technologies we
mentioned in the beginning, which is
like TSMC's CoWoS and Intel's EMIB.
These are technologies designed to hold
multiple chips together
whether they're memory like HBM and the
GPU or like multiple GPUs like you were
saying
on some of these other chip platforms
like the Blackwels or the Rubins, they
have multiple chips.
&gt;&gt; [snorts]
&gt;&gt; And those chips are really huge chips.
So since you can't make one infinitely
large GPU die, you have to stay to the
reticle limit, which is actually 858
mm squared.
It's a 26 mm by a 33 mm reticle. That's
about as big as you can make a chip. So,
the GPUs are at that limit and
to make it any bigger and put more
transistors and have more compute,
you've got to put multiple such
reticle-limited GPUs
into one substrate, which we will see
Let's just generically call it substrate
for now. And then you hook them up. You
hook them up with very, very, very fine
wires because the number of connections
going between either the GPU to GPU or
GPU to memory are way too many. There
are like just an incredible number of
wires. So, the connection that happens
between them also is not just on a
single level. It's usually multiple
levels. So, whatever the interconnecting
mechanism is underneath these chips have
to has to support pretty complex routing
that are all very finely featured,
right? That is the key that makes this
advanced packaging. These are not like
crude traces like a PCB is. These are
almost
chip level features that are being
printed on substrates so that you can
almost make one die an ex- extension of
the other.
&gt;&gt; Yes. Yes. You make a really good point
about the
wiring interconnect geometry. And so,
HBM 3, I think it had something like
1,024
signals coming out or something There's
a lot. And you So, you're obviously
having to route all of these to the GPU
and you're trying to do it in small
dimensions. And so, yes, this it would
you know, think of it as like a ultra
mini PCB, but you're you're right.
You're like in as small as possible.
You're wiring all this and you're you
know, you're needing to route around
things. It's It's non-trivial at this
point.
&gt;&gt; Yeah. And HBM 4 took it to 2,048
parallel lanes. So, that's an example of
why you need a very, very fine
interconnects, very fine metal lines
that go between these chips on this
interconnection substrate. And that has
become
pretty much the stronghold of maybe one
company, maybe two.
In the world today,
&gt;&gt; Right? Yes.
&gt;&gt; the TSMC dominates the CoWoS packaging
that require is required for all AI
chips today. And they are extremely
capacity limited because
uh there are It is actually the way TSMC
does it is actually uh
it's a wafer fab process. It's not
something you can do in an external
third-party uh
factory of some kind. You need
sophisticated fab equipment to be able
to make these things happen. And so
that's where the whole advancedness of
it comes in and that's why somebody like
a TSMC who knows how to make this with
high yields uh and have a you know, long
history of making chips and uh you know,
running a foundry comes in. And that's
why not everybody can get into this
game.
&gt;&gt; Yes, yes. So this is a really
interesting point. Let's talk about this
for a second.
It you know, going back in history we
talked about, okay, everyone used to be
their own IDM and then eventually there
were like
people said, "Oh, let's outsource the
back end of this and let these OSATs do
some of the processing and and along the
way foundries came up." And so even
TSMC, which was a foundry, said, "We
deliver the wafer and someone else can
package it for us. Not not huge value
there." But now we're talking about
advanced packaging and it takes the same
know-how as a foundry. It takes the same
tooling, the same know-how. Um and and
so now all of a sudden it's like, "Wait
a minute. The simple packaging is still
totally used high volume whether it's
from cheap components to expensive
components." But there's this advanced
packaging bit and that's actually um
these fabs that can make logic chips or
make memory chips are actually capable
of doing the advanced packaging. And so
so TSMC actually entered advanced
packaging, you know, I think in like the
late 2000s, maybe 2010s or so, um where
they started looking ahead and saying,
"Oh, this advanced packaging will be a
thing, and this is something we could
do." So, that it could actually either
create a new market, if you want to
think about it that way, or or like
um maybe bookend what OSATs can do. And,
you know, so it's like TSMC, there's
OSATs, but now there's this advanced
packaging that TSMC could do again. And,
so TSMC started doing R&amp;D and they you
know, came up with CoWoS, which we'll
talk about. They also, um I think
did some early work on info integrated
fan-out packaging, which we we probably
won't talk about much today. Um
but, I just wanted to point out that
actually now OSATs are trying to say,
"We want to get into advanced
packaging." So, OSATs are trying to
expand beyond the simple packaging and
actually move their way into advanced
packaging. So, for example, you can go
listen to Amkor's earnings call, and
you'll hear about this, um because
that's where a lot of the value is
accruing and is going to be more and
more and more important in the years
going forward. So, if you're a
forward-thinking OSAT, you're saying,
like, "Hey, I don't want to be left out.
I actually want to try to get into the
advanced packaging game, too."
&gt;&gt; Yeah, that's amazing, right? Now, what
happens is that once advanced packaging
has gone into a fab and, you know, these
traditional OSAT packaging houses, like
Amkor, want to get a piece of the bigger
pie by going and become doing what a fab
does and doing advanced packaging.
You start Anybody doing this now starts
to run into the same limitations
uh of wafer fab manufacturing and or
chip making, right? So, to put this in
perspective, I think we should just
quickly step back and see, okay, we
spoke about the reticle limit being 858
mm squared. Now, the H100 was already at
that limit really, right? And you
mentioned that the Blackwell die
is basically two reticle size die
stitched into one GPU using CoWoS,
right? So,
what's the next one?
How many chips are we going to put in
next?
Like we got two already.
&gt;&gt; Yeah, I believe for Rubin, they're
supposed to be four die, four GPU die
stitched together.
&gt;&gt; So, now what happens? Yeah, so with the
four die thing,
it starts getting complicated because
remember that
the manufacturing process for the
packaging that holds these die together
is the same thing that
was used for the chip itself, right?
So, what that means is now you couldn't
make chips that are bigger than the
reticle limit, which is why it was it
stopped there.
But now you need to make packages that
are bigger than the reticle limit.
Otherwise, how are we going to put two
GPUs into one and stitch them together?
These packages that you are running in a
wafer fab process
uh now need to be, let's say, two
reticle size to hold two chips. Uh
usually more, right? Because you need to
put HBM, you need to put other stuff.
So, maybe three, you know, so
the first generation of CoWoS was
actually something like this. It was
maybe 3.3x the reticle size that you
could make.
And and so that somehow started becoming
the limiting factor now. And the
question is, how come you can make
packaging substrates that are like
bigger than reticle limits,
uh but not ICs themselves?
Think
I'm I'm not entirely sure of the right
answer, but I'm going to take a educated
guess because
these wafer fabs that run packaging
substrates are actually much simpler.
You don't actually make transistors. And
so that
means that you can probably stitch
together a few reticle shots worth and
make a larger reticle
uh substrate that can hold maybe two or
four GPUs at one time. Right? So, that's
where it comes from. Uh what do you
think? Is that Do you think that's the
right answer as to why you can make
advanced packaging that's 3x reticle
size?
&gt;&gt; Yeah, yeah. Well, which by definition
advanced packaging has to be bigger than
reticle size cuz like you said, you're
taking reticle size like dies and
rewiring them together. So, I think
that's just the key is that ultimately
advanced packaging is still just drawing
wires. So, you're not
trying to in one shot draw a bunch of
tiny resistors. And you're not
necessarily using um this like 18A
style like
pitch and tools. You're using
semiconductor tools, but it's still
bigger. You're still drawing wires
ultimately um like like metal wires, if
you will. Um so, I think conceptually
it's more about you're taking these dies
and you're able to
pattern use lithography and pattern, but
you're you're drawing wires. Now, I
don't I don't think you're necessarily
We should I I need to learn this. It's a
great question. You're I don't think
you're drawing all the wires in one
shot, you know? So, you're probably like
putting the wires in over here and over
there and over here and over here still.
Like kind of like stepping around.
&gt;&gt; Yeah.
So, this whole chip on wafer on
substrate or CoWoS technology and we
will get right now very quickly we're
going to get into what the wafer and
substrate is, but it's typically
referred to as a 2.5D packaging
technology. It's only 2.5D because
uh
you have a
a uh
active piece of silicon that is with
transistors packaged over
let's say a passive piece of silicon
without transistors, but it's still
silicon.
Right?
So, uh that is the chip on wafer
process.
So, the chip with active elements like
transistors is packaged over silicon on
wafer, so chip on wafer.
And that is 2.5D.
Right? Now, if you the 3D version of
this would be uh stacking a logic chip
on top of a logic chip or active on
active. So, 2.5D is active on passive,
3D is active on active.
So, that is a packaging technology that
is around uh in all of these fabs, too.
But, we won't get into it too much today
because that is really not a advanced
packaging technique. It's a method of
stacking active circuits together.
&gt;&gt; Yes. So, let me I'm going to say it
again because it's like a marking
terminology, and people will get weirded
out by it, but this is just industry
standard. So, there's 2D, 2.5D, and 3D.
And um yeah, three the 3D is really
cool, and we should talk about it
sometime. Um
stacking logic chips, but we won't talk
about it a ton today. But, just to
define these things cuz people are you
know, in your brain, you're probably
thinking like two two dimensions I Okay,
I get it. Like maybe it's like a piece
of paper, like the surface of it. And
three dimensions like I get that. We
live in a three-dimensional world. What
the heck is 2.5D? And again, just
industry conventions. Sorry,
semiconductor industry is weird. Just
like we talked about 18A doesn't mean
things are 1.8 nanometers or 18
nanometers or whatever. Uh or 18
angstroms, 1.8 nanometers. Um that's
kind of a lie, and 2.5D is also a lie,
but it's just the naming convention. So,
engineers don't overthink this. Um so,
basically, think of when we talked about
um flip chip or hybrid bonding, just
think of that is like 2D. Like you've
got a die, and you slap it on substrate,
and you wire it together. And just think
like the die is sort of like 2D. It's
just a die. Like you're looking at the
surface of it. Whatever. 2D. 3D is is
what Vic said is the far other end of
the spectrum, which is like you're
trying to stack things, right? You know,
this is like you're building the
skyscraper, whatever. It has multiple
stories, if you will. So, that would be
3D. And then 2.5D is like, "Hey, um
we're going to increase the size of this
house, but instead of building many
stories, we're just going to put a bunch
of little houses next to each other, and
then we're going to like build a hallway
that connects them all, right? So, so
this is a 2.5D. So, think of like you
know, you've got a compute die, and
you've got another compute die, uh like
two GPUs, for example, and then you're
stitching them together. That would be
2.5D. Or even technically HBM memory
connected to a GPU is also considered
2.5D, which can get a little confusing
because technically internally within
HBM, it is actually 3D. It is stacked,
right? Like these uh HBM uh can be like
12 high or eight high or whatever. But,
now I'm getting way too I'm giving you
way too much information cuz you're
probably getting confused. But, but
generally, when you think about 2.5D,
just think that like it's one story, but
it's like chips next to each other, and
they're connected. And like Vic said,
there's a key point, which is in 2.5D
and we're going to get into the details
where we're fi- we've buried the lead.
We will finally explain to you what
CoWoS is. But, when you connect these
things, there's usually a passive
interposer, as we'll talk about in 2.5D.
So, okay, Vic, let's talk about chip on
wafer on substrate.
&gt;&gt; Okay, yeah. We've got to get to it,
right? At some point. But, all this
background is important because
otherwise, if we just dive right into
it, CoWoS is this and that, it's just
like it loses it People who are not
familiar with this stuff just like lose
context immediately. And I felt it in
the background so far was useful, and I
hope everybody feels the same way.
Chip on wafer on substrate. okay. Chip
is the GPU, right?
It's sitting on a wafer.
The wafer in this case could be a piece
of silicon, right? It's a silicon wafer,
but it doesn't have any transistors on
it. It just has metal lines
that can connect to another chip name
sitting nearby. So, that's the chip on
wafer.
And this stack of this chip sitting on a
piece of silicon
now sits on top of a wafer. So, it's
like a
three-layer stack, right?
And that is what is COWoS.
And that is the
big thing that
uh TSMC
made
you know, go into production around the
early 2010s
uh with FPGAs, I think, initially.
&gt;&gt; Mhm.
&gt;&gt; But, it actually enabled the stitching
together of multiple active pieces of
silicon. Now, the question is it's
obvious to ask at this point. So, why do
you need this like wafer in between? Why
don't you just put chip and put it on
the substrate? You you've been saying
you know, you're just going to connect
the chip via substrate so far. What is
What is this interposer? What is this
uh intermediate wafer W you talk about
that you also call an interposer
sometimes, and then you also call it a
piece of passive silicon wafer. Yeah,
these are all These all mean the same
thing, actually. And um
why that is required is because
on a substrate, when you call it a
substrate, it's something like a PCB or
is something like uh a different
material that's not silicon.
Also sometimes called organic substrates
because of the kind of materials they're
made of. They're made of organic
materials.
And so, you can't pattern fine lines on
them.
And that's the whole problem. So, the
the CoWoS
solution was like, "Okay, we don't need
to pattern the fine stuff on the
substrate. We'll just do the coarse
stuff on the substrate. Like, maybe we
only need like a couple of power lines,
right? To come into the chip. Let's just
make that on the substrate, right? And
hook it up to the outside world. But,
the connections between the chips needs
its own separate layer,
which requires a foundry class
technology to connect those things
together. And that's why you need a
silicon interposer to connect these two
two things together. And that's what the
chip on wafer does.
&gt;&gt; Yes, exactly. It's about
that intermediate layers, so you can
have very fine-pitched routing, lots of
wires, lots of signals. So, so TSMC
started with CoWoS-S.
So, there's different flavors of CoWoS,
and we'll talk about three of them. In
CoWoS-S,
chip on wafer on substrate with silicon
interposer, which means that that middle
layer of the sandwich, where the routing
happens, is a big silicon interposer.
Um the nice thing about silicon is it's
great you can route through it really
great. It has good, you know, it it's
it's good for um fine-pitched metal.
Um
And then you just have TSV TSVs, through
silicon vias, that come up to the chips.
Um the downside of it is that
it's expensive in that now you have it
you're you're using silicon wafers for
routing. Ideally, we would use the world
supply of silicon wafers for logic. But,
now you're using silicon wafers for
routing. And which is fine, but it can
be expensive. And so, naturally, there's
a question, "Oh, could that intermediate
layer be something cheaper? Like, do I
have to have silicon? Or could there be
something cheaper?" And so, there is
TSMC came out with something called
CoWoS-R,
where you have an organic RDL
redistribution layer interposer. So,
here we have an acronym within an
acronym. CoWoS-R, R stands for RDL, but
an organic RDL interposer. And so now
this routing layer is a cheaper organic
material, not necessarily the same
material as a substrate, um but a
cheaper material. Um and you can route
through that. Now, if you were paying
attention, you're going to say, "But Vic
literally just said organic materials
are not good for fine pitch routing."
And that is the trade-off, like
if you have this
middle layer, maybe it's ABF or
something, um
you can't get as fine of pitch of
routing as you can with silicon. And
then also, there's something uh
stability dimensional stability. Um this
these organic materials,
they can shrink when they're heated up,
they can absorb moisture, they can warp.
Um and so you can have lot your routing
connections move around or disconnect or
short circuit or whatever. And so that
because you have to account for this
error, that again limits how closely you
can put the wires. Um so
or uh chip on wafer on substrate R, so
CoWoS R, cannot support GPU
accelerators. But it can be a still a
nice advanced packaging path for
anything that and could be a little bit
cheaper, maybe
lower-end smartphones or or automotive
chips or something. I'm not I'm not
sure. Um but it's it's not what we need
for
um AI accelerators. And so then the
question is like, "Okay, well, do we
just have to use CoWoS [clears throat]
uh S with the silicon expensive silicon
if we can't use CoWoS R?" And no,
there's another next step from TSMC,
which tries to use the best of both of
those worlds. Hey, can we get the
routing density of silicon,
but more of the cost like the organic
substrate. And this is where Co-WoS L
comes in. L stands for local silicon
bridges in an interposer. And so, the
idea is, "Hey, what if
we let that middle
section of the sandwich be the organic
material that's cheap, but then wherever
we And And And let it route the big
signals through there, like the big
power signals that Vic talked about,
whatever. If they don't have to be
small, route them through the the cheap
stuff. But, in the areas where we do
need really dense, really finely
pitched, like close closely spaced,
bunched together wires connecting, could
we have silicon? And these are silicon
bridges. So, the idea is And it's
complicated, but this is uh just making
engineering trade-offs and saying, "How
can we get a little bit of best of both
worlds?" The idea is, again, you have a
big cheap bulk subs- organic substrate,
but then in certain places you put the
local little tiny silicon bridges, and
you route through that. So, I'll pause
there. Uh
any thoughts on Co-WoS L, Vic?
&gt;&gt; Yeah, so I wanted to let you finish to
go through the three kinds of Co-WoS,
because
if I interrupt the flow of the
trade-offs, uh you know, it's gets very
hard to follow. So, that was good,
actually. It's a good explanation. The
one thing I wanted to mention is that
the one problem with the first one,
which is the Co-WoS S on silicon
interposer, is that
uh you are essentially making
uh
a foundry class packaging technology,
which means that the reticle slice size
is inherently limited. There's only this
much you can do
to make really large Co-WoS S packages,
because
you can only make them What was it? Like
3.3x the reticle size or something?
Like, yeah. It's very difficult to go
past this. And so, the early early
generations of accelerators did use COAS
in spite of the cost or whatever, but uh
and uh
it did did kind of the industry grew out
of it because the chips got so much
larger, it just didn't work anymore.
Like, then comes the COAS R that you
mentioned, and I wanted to expand the
word R here. You said it's RDL
interposer.
RDL is an acronym an acronym which
stands for redistribution layer, right?
And the thing with redistribution layer
is
it's usually a a thin layer of polyimide
uh dielectric. And within the polyimide
dielectric, you can pattern about two or
three levels of metal layers. Uh so,
this is usually, even in the chips I've
worked with, RDL layers come in much
above the chip. So, it's outside the
chip, really. Even you can even deposit
RDL layers on top of a chip and route
connections out of the chip via RDL.
Okay, that's a fan-out technology. It's
called a fan-out technology cuz you can
take one connection and fan it out into
you know
greater reaches that you can't get out
of a chip cuz chip is so small, you want
to connect it to a PCB that's big. So,
you have to fan it out. So,
redistribution layer has been around a
long time. So, the idea was that why
don't we use spin this same polyimide
onto the wafer uh on you know, and then
make the pattern pattern on that
instead. And you're not
restricted by reticle sizes as much
because it's a different process
technology. It's not a fab-based
technology. It's not that kind of
lithography. So, it's a different
approach. So, you could actually make
like stuff bigger, but like you say, it
is not nearly fine enough to connect AI
accelerators together. It It never ended
up being used for that.
So, the final thing was obviously, like
you mentioned, the best of both worlds.
You take an organic substrate, stuff
that you can't make really fine
connections on, but then wherever you
need the connections, just between the
two chips that you have to connect, you
put in just the piece of silicon that
you need, right? There is a very unique
aspect to using these silicon bridges
only where you need them.
And that is now you're not restricted by
reticle size, even though you're using
silicon interconnects between the chips,
right? Because you need to make these
tiny bridges, of which you can get
thousands in a wafer, no problem. But
then you just band-aid many chips
together,
you like connect them together with
bridges, and now you're good. And you
got like silicon class interconnect
performance, but without the reticle
size limitations. So, you have that
benefit from the CoWoS-S world, where
you could connect it with this fine
interconnect, but now you're like you're
breaking the reticle size limitation,
which is amazing,
&gt;&gt; right? That's the whole point of
bridges.
&gt;&gt; Yes, totally. Yes, exactly. So,
conceptually, you know, zooming out,
when you have CoWoS-S, if you want to
have a ton of GPU dies stitched
together, you have to have a huge piece
of silicon to go under it, right? So,
could you have like 20 dies? I don't
know. Can you have a crazy massive piece
of silicon, right? And And to Vic's
point, you you have the same lithography
reticles stuff, so you'd have to like
step all over the place to draw all
these wires. Um, but when you're talking
about bridges, it's like, "Oh, okay, I
could just have some big cheap
substrate, and then I only need to take
the silicon and put it just in the
little areas where I'm connecting dies."
And And so, like, um,
with with CoWoS-L, and so, like, one
analogy that came to mind to me before,
um, is like,
um, in Iowa, where I live, you know,
there's it's actually very it's actually
very rural. I'm sure you all know. It's
mostly corn fields. And we have roads
that go all over the state. There's 99
counties in Iowa. So, it's kind of like
a grid. And this is kind of because of
the corn fields, you know. It's just
like everyone gets like a square mile by
mile or whatever, 40-acre type um farm.
So, we have all these roads, um but we
would never make all of those roads
asphalt or pavement. Pavement is the
best driving experience, but it's also
very expensive. And we're not going to
cover the state with all especially when
there's just like one random farmer that
lives out there. You're not going to
like put pavement everywhere, right? So,
what we do is we say, "Okay. Okay, let's
put gravel everywhere. Gravel's way
cheap." It's like gravel's like So,
pavement would be like silicon. Like
it's the best, but it's expensive. And
gravel is like the organic substrate,
which is like whatever. Just throw it
out there over the dirt to give you a
little bit more traction and so it
doesn't wash out, but it's cheap. Now,
we don't want to Now, yes, we live in
Iowa and maybe, you know, you call us
hicks or something, but we're not going
to we don't want gravel everywhere. So,
in town, we don't use gravel. We still
use asphalt. So, this would be like
CoWoS-L, where it's just like use the
cheap stuff to cover most of the state,
the big areas that aren't as traveled
and whatever. But then like by my house,
I want asphalt, right? And so, CoWoS-L.
So, that's my poor man's analogy to show
that like, you know, you can have the
best of both worlds.
&gt;&gt; Yeah. Only Austin can connect corn
fields and chips like this. Amazing.
Corn chips
&gt;&gt; or worse.
&gt;&gt; Corn chips are a thing, right?
&gt;&gt; Corn chips. There you go.
&gt;&gt; [laughter]
&gt;&gt; Uh yeah, that's great. Yeah. So, the
whole idea of putting localized
interconnects actually, by the way, fun
fact, didn't actually come from TSMC
because it was Intel who initially
developed this uh
bridge concept. It was
before CoWoS-L. So,
there was this whole thing of that, you
know, uh TSMC copied Intel or something
and then
there were somebody people said, "Oh, we
should we should file a lawsuit because
they copied us or something." But, yeah,
the EMIB predates CoWoS-L. And [snorts]
the whole idea of EMIB was that
um
they eliminate the silicon interposer
entirely. That was the idea for EMIB,
right?
What
TSMC did with CoWoS-L, which is local
silicon interconnect,
uh was, you know, after they found the
same problem that they can't go to
bigger and bigger chips uh or packages
anymore because they're limited in size.
So, Intel's foresight was that, "Okay,
how about we just skip this entirely?"
So, even today they they skip the middle
layer. They skip the interposer
entirely. So, they just take the chip
and put it on a substrate.
Bam, done. Like gravel road all around,
no problem. And wherever required, they
just put in uh these
multi-die bridges, right? And embedded.
And what they actually do is they embed
this thing into the substrate. So, it is
like
I don't know, I think of, you know,
pushing a piece of like a cracker or
something into Jell-O. You know,
[clears throat] it feels like you're
pushing some crackers into Jell-O.
That's the feeling I have when I think
about EMIB. And then you hook up uh dies
like this.
Uh but, yeah, so
the benefit of doing this is that you
know, obviously the bridges themselves
are really tiny. You could make tens of
thousands of them
um or at least thousand per wafer. But,
the the substrate itself
is not limited by the reticle size
because it's not even one made in a fab.
The second thing is that it's not even
in a circular wafer format. It is made
on like square panels.
&gt;&gt; Mhm. Mhm.
&gt;&gt; Because if you can make these substrates
on square panels, it's amazing because
there's no wastage. Like if you're
trying to cut out square shapes from a
from a circle, you know, you always got
wastage. And the bigger you make this
square shape that you cut out, you know,
the fewer you can circles you the fewer
you can cut out from the circle. So
there's so much wastage, especially as
package sizes go up from the wafer. So
to your original point, these silicon
wafers are already uh you know,
difficult to come by. But then you make
these gigantic packages on them and then
you throw out half the wafer because
it's no more it's no more useful. You
know, it's like the example is like, you
know, my kids when I make pancakes,
my kids are always like, I want sh- I
want shapes, you know, we have these
like cookie cutter shapes on pancakes.
So we take them and we press them down
and it you get a deer and a squirrel and
whatever. And they're like happy about
it, right?
&gt;&gt; That's awesome.
&gt;&gt; And then they're like
uh oh, but I want the this squirrel and
that squirrel. But there is no more
pancake left for me to squeeze out a
squirrel from it.
&gt;&gt; Yeah, yeah.
&gt;&gt; So now I have to make another pancake
just so that I can cut out the squirrel
uh because the moose already took up the
that the last pancake and I couldn't cut
out a squirrel and a moose. And now I
have I'm left with all these carcasses
of pancakes that I end up eating. But
that's exactly what happens with
with packaging, right? Like you make
these packages out of wafers, but the
rest what do you do with the rest of
them? You know, they're they're
wasteful. So but if you can now that you
know you're not cutting out a moose
shape on a on a package, you're cutting
out rectangles. And so if you have a
panel like that is already square, you
can cut them out. And there's like
wastage is very little. And these panels
are not the size of a wafer like 300 mm
diameter wafers. These panels are like
500 by 500 or something like that, you
know, it's much bigger than a wafer is
by a factor of
you know, an order of magnitude uh maybe
like a five five, six times more.
So it's much much bigger.
&gt;&gt; Totally. And and the the point you make
is very key, which is ultimately these
little bridges these they're just little
rectangles. They're you think the the
die is like, you know, big big
rectangles and then a little bridge in
between them is a little rectangle. And
so, as we've always talked about with
yield, the smaller things are, the
better your yield will be intrinsically
because there's just less surface area
for a random defect to pop up. So, EMIB
can actually have good yield, too. So,
again, zooming way back out, back to the
original problem of like, "Oh, yeah, we
did wire bonding, we did flip chip.
What's next? We want to draw connections
between between things." And we said,
"Oh, this the substrate's not a great
place to do it." Um Intel had the
foresight to just say, "Oh, yes, why why
not just embed little bridges into the
substrate." So, when you think EMIB,
embedded bridge embedded bridge, that's
how I used to remember EMIB. Um embedded
bridge, and that's all they're doing is
they're just taking that little
high-yield bridge that they can easily
make, and um they're just embedding it
down in there and connecting the die.
So,
that would be the progression of TSMC
getting to bridges. And again, so not so
Okay, let's say this. What's the
difference then between EMIB and
CoWoS-L? As a reminder, you said both of
them have bridges. And so, again, just
as a reminder, CoWoS-L is three-layer
sandwich, and the bridges are in the
middle the middle layer organic material
with the bridges inside of it. And EMIB
is just two layers. It's just the dies
and the substrate, and those bridges are
embedded into the bottom layer there.
So, just like a quick reminder.
&gt;&gt; Yeah. So,
EMIB itself has just two versions. You
will see this if you look up EMIB is
like EMIB-D, which means there are
through silicon vias through the bridge.
And this is quite important for
use in AI accelerators because you do
need access to power and high-speed
signals through the chip. So, the
through-silicon vias are important. So,
the EMIB-T stands for TSV. And there's
another version called EMIB-M,
which stands for
metal-insulator-metal
capacitors. So, those are MIM
capacitors. They are just
basically capacitors that are built into
this bridge, which are useful for like
power delivery. Because whenever you put
a power signal, you want to have a what
is called a bypass cap,
so that if there are any fluctuations,
they go they get rid rid of those power
supply fluctuations through the through
the capacitor. So, those are the
function of bypass capacitors are
usually quite important in power
delivery. So, it's very useful to have
them embedded into that because you can
provide a clean power signal to
whatever's on the chip. So, some the
variant of that is EMIB-M, actually.
&gt;&gt; Mhm. And Intel has been doing EMIB for
like a decade now with their own
products
um
from way back in early FPGAs to
uh their
uh CPU SOCs and obviously still using it
now. Over time as technology has
progressed, as transistors have gotten
smaller, density has increased, the
routing has increased, um Intel needed
to move beyond the original EMIB and
that's kind of where they came to EMIB-T
and EMIB-M. I'm sure they're just
solving problems with EMIB along the way
and thinking, "Oh, there's there's
better ways to improve it so that we can
continue to have higher bandwidth
signals, by the way, in even tighter
density and smaller smaller spaces,
smaller footprint, let's say.
&gt;&gt; Awesome. Now, uh I think we should
quickly Now that we have described all
the technology, do you want to quickly
hit upon the the value propositions of
EMIB versus Co-EMIB?
&gt;&gt; Sure, sure. So, like
ultimately like you're saying like the
pros and cons between EMIB and CoWoS?
&gt;&gt; Yeah, like yeah, but let's go through
the pros first and then we can try to
argue why EMIB is bad.
&gt;&gt; Okay, okay, sure. So, EMIB So, pros, you
So, you've got two layers instead of
three layers. So, obviously from a cost
perspective, you don't have to
deal with the cost of the separate
interposer, whether that's silicon or
organic substrate with local silicon in
it. Um
that reduces process steps, that reduces
material costs, that reduces interposer
dicing, that reduces inter- the waste
that Vic talked about from interposers.
Um
Those are some cost things that come to
mind. You talked about the panel
utilization, how um
the
embedded die can ultimately come on It's
like a geometric benefit. It could come
on a rectangle panel and then you can
dice that up and have less waste.
Um
&gt;&gt; Yeah, because now you know that actually
directly translates to, you know,
capacity.
Because not only is just that the
panel's bigger,
uh but also utilization rates are very
high compared to circular wafers.
And on top of that, I just want to
mention it briefly here. We won't really
get into it, but TSMC has the idea of
going what is called chip on panel on
substrate. And I thought now is a good
time to at least briefly mention it
because they do plan to go panel level
soon. Uh by soon, I mean 2028, 2029, I
believe is the time frame. So, they do
have this
uh in mind as well.
&gt;&gt; I guess uh
scalability past the reticle limit. You
kind of hit on this already. Obviously,
if you were going to have like a silicon
interposer and you wanted to make it so
big so you could put like a ton of GPU
die on it. Literally, it could start to
get like
back to what Vic was saying earlier. If
we've got like a dinner plate wafer and
we take like a big brick rectangle shape
out of the middle of it and that's all
the bigger it can get. Like, you know,
basically like the diameter of the
wafer, then you're going to leave all
this all that area that's like on top
and on the sides and on the bottom with
the curved edge that's going to all be
waste. So, obviously, the cost like EMIB
has cost benefits even from from that.
And then, um
whereas, obviously, for EMIB, which is
the embedded bridges, you're just taking
these little pieces and you can sort of
imagine scaling up to very, very large
um size packages because, like, let's
say you have a 3 by 3 grid, just
conceptually, of um
GPU die, let's say. Well, now you just
have to put little um EMIB bridges in
between all of them. And so, you can see
like, "Oh, why 3 by 3? Why not 4 by 4?"
Like, you can conceptually see like, as
far as the embedded bridge is concerned,
it's just little bridges inside dies. It
sort of feels infinitely scalable. Now,
there are limits, of course, but but you
can see how that's very scalable. And
and uh then again, you know, we talked
about yield already as well, which is
you're just making these little small
pieces. Yes, it's um there's
manufacturing that has to happen,
advanced packaging, obviously, that has
to happen to embed those in the right
place and route through them. So, it's
still complicated, um but naturally,
like, the yield is pretty good. So,
those would be some pros that come to
mind. Yeah. Now, you take the you take
the other side. What are some cons of
EMIB?
&gt;&gt; Uh EMIB, though though, I think the
couple of arguments against it are like,
one, it's never proven at scale.
Okay, like, TSMC has run a lot of volume
on um
CoWoS. There's there's of history with
the AI accelerators. All the customers
are very familiar with it.
There is a risk going to EMIB.
Although it does look like from the last
Intel earnings call, they have a lot of
advanced packaging orders in already. So
&gt;&gt; I'm going [clears throat] to push back
on your push back.
Intel's been using it for a decade and
they ship millions of chips every year.
&gt;&gt; Okay.
&gt;&gt; So so so they have internally EMIB
itself has a ton of reps.
&gt;&gt; Okay.
&gt;&gt; So but to to put a to to put a fine
point though on your argument, you could
say
it doesn't have a lot of experience in
other people's
packages.
&gt;&gt; I see. Okay, so it's not So Nvidia has
never built one with EMIB. Although I
think they're considering it.
&gt;&gt; Right right right right. Folks are
considering it. And so in in so Intel
Foundry will tell you like, "Hey,
we'll take your die. It can be from TSMC
and we will
use EMIB and just do the packaging for
you. So like you don't have to commit to
build your GPU with Intel Foundry and do
just to unlock EMIB. Like you in fact
you can
build your dies wherever and Intel will
just package it." But but yes, there
isn't a lot of
examples of that yet. In theory it
should be no different than whether it's
an Intel CPU that's stitched together
with EMIB or a
I don't know, a Qualcomm CPU from TSMC
stitched together with EMIB or an Nvidia
GPU stitched together with EMIB. In
theory it should work.
&gt;&gt; Or a Google TPU. Which which we'll get
there. But in practice, someone's got to
go first at scale.
&gt;&gt; Yeah, yeah.
They I always kept seeing this and we
posted this on the Semi Dope Daily
newsletter we write as well. And that is
that the yield of EMIB is crossing 90%
to some I read somewhere that it's 95%.
So, if EMIB has been shipping for that
long and even internally, do they
already have the yield at scale? Is Is
yield something to even worry about?
&gt;&gt; Uh I wouldn't think so. I mean, EMIB-T
and EMIB-M are newer and so, you know, I
don't know. Let me see if I have any
notes somewhere. Like, it's obviously in
um
like Clearwater Forest
um
I'm not I don't have a note anywhere. I
don't know, you know,
which chip was the first to use EMIB-T
or EMIB-M, but all the those Sapphire
Rapids, Granite Rapids, these all used
EMIB as well. So, at least the original
EMIB, it's definitely at at scale
manufacturing. So, the yield should
totally fine.
&gt;&gt; See, that's the argument because
somebody uh
was saying I I don't know where I read
it, but somebody's like, "Oh, if the the
yield of EMIB is only 90%, that's not
good enough because the packaging yield
has to be 100% because you're putting a
GPU on it. You're burning a whole
reticle's worth of 2 3 nanometer
technology chip just for packaging. And
what do you mean you I can't lose like
one chip out of every 10 chips? That's
just not acceptable." When I saw that, I
was like, "Okay, I buy that. Nobody
wants to lose one GPU out of 10 GPUs
just to advance packaging. So, 90% isn't
good enough." So, then I was wondering,
what is TSMC's packaging yield? Is it
99%? Like, you you lose one in a in a in
a 100? Or is it 99.9? You lose one in a
1,000? You know, so
I mean, every process has a has a yield.
I mean, nothing is 100%. So, the higher
the yield, obviously the better. But, I
was a little surprised with all this
about 90% EMIB yield because if you have
products shipping in Intel internally,
like you said, it's a good reminder. Now
that you mention it, I just
the dots are connecting.
Why Why is the EMIB
yield 90%? I mean, is it not 99.9%
already?
&gt;&gt; Yeah,
I would guess it is. I have no idea, but
when I hear EMIB is 90%, then my
question is which EMIB? And my question
is who says that, right? Because
&gt;&gt; [laughter]
&gt;&gt; uh some sell-side reports that might
report this stuff probably don't know
the history of EMIB deeply and aren't
thinking about it. They're probably just
thinking like, "Oh, yeah. Every new
process node has a yield. Everyone has
to ramp from zero." So, you know,
&gt;&gt; Yeah. Oh, interesting. EMIB, it must
have to ramp from zero. Uh but I I I
find it
a little hard to believe. But, it is a
really interesting question that you
asked with it which is what is CoWoS
S R and L yields um from TSMC? I don't
know if that's ever been published, but
that would be just a nice data data
point to know in the industry.
Obviously, it must be insanely high
because everyone uses it. Literally,
everyone uses it. That's why that's why
EMIB is interesting, right? That's why
there's news recently that other people
are considering EMIB. Um it's not
necessarily because CoWoS is bad or
because it's too expensive or because
the the because yields are low. It's
because there is only a fixed capacity
of these interposers and of all that
advanced packaging.
&gt;&gt; And there's been a slew of uh you know,
news around this because uh the
apparently the Google TPU order uh seems
to be booking 3 million TPUs to be
packaged with the Intel EMIB.
Uh and
uh that's going to be like what? 2028?
And apparently, SK Hynix is testing EMIB
uh for HBM integration as well.
And um if you're talking about the
Google TPUs, actually, remember it's
actually going through MediaTek who is
then using EMIB.
Uh MediaTek is becoming an increasing
threat to Broadcom's custom ASIC model,
especially with Google TPUs.
And uh something to really watch out for
and that that's why in the recent
earnings call and all that people
realize that this
uh is this this tide is shifting from
Broadcom and going to MediaTek and
that's why all this Broadcom stock has
been like low off late.
But yeah, so it's interesting that
Google through MediaTek is going through
EMIB as well. And I wanted to mention
one more very interesting thing that
very few people like I think pay
attention to
is that Intel actually has an extremely
good optics process. And technically
with their
ability to package this stuff, they
could use EMIB and their optical engines
to make some really cool CPO stuff. Just
saying. Like Intel has that ability to
make CPO.
&gt;&gt; Yes.
We should have a podcast on sometime.
Intel has a history of optics and
photonics. Not well known, some stuff
has gotten sold off and whatever, but
the foundry has the capabilities um that
opens up interesting doors in the
future. Now, of course, obviously Lip-Bu
here, they're laser focused on
customers, they're laser focused on 18A
P as a better version of 18A, working
toward 14A. They're trying to win
customers. It seems that it's working
both from a packaging perspective. Uh
hey, they have a lot of advanced
packaging capacity in New Mexico. You
want to do EMIB? No problem. MediaTek,
you know, get your
um TPUs fabricated with TSMC, send them
to us, we will stitch them together, no
problem. They're everyone's very focused
on that.
All of that is good. EMIB like the
advanced packaging business is growing
and we're talking and yeah, um
uh David Zinsner, the CFO, said, "Don't
forget that's advanced packaging alone.
These are These are billions of dollars
worth of commitments that we're getting.
So, it's it's no joke." Of course,
they're trying to win customers actually
build logic chips with Intel foundry.
Um, but if they have a little bit of
bandwidth somewhere, if they can hire I
mean, I know they have teams already on
this, but if they can if the business
can get a little bit of focus, like they
ought to be um, throwing their weight a
little bit towards CPO,
&gt;&gt; Mhm.
&gt;&gt; optics, photonics. Can they make lasers?
Can they take buy lasers and package
them? We'd have to go into exactly what
their capabilities are, but it could be
a really interesting opportunity for
Intel Foundry.
&gt;&gt; Absolutely. And so, just in terms of
sizes, I think we should just quickly
summarize where we are right now,
because the first generation of CoWoS
was like a 3.3x reticle size. Uh, I
think currently the Blackwell
ultra class and the Rubin class chips
are all like at the 5.5x reticle
packaging that TSMC CoWoS is capable of
today.
The next generation that is planned, I
believe will take it to 9.5x reticle
size.
Um, that should be about it, and then
they start talking about what is called
a system on wafer,
which uh, targets something like 40x.
Uh, that I'm I'm not sure when that is
going to come out or anything, but even
uh, the 7x thing is not, I think,
towards the latter half of uh, next few
years anyway.
&gt;&gt; It's all right.
&gt;&gt; Yeah.
&gt;&gt; It'll make make for good launch
events, you know, instead of holding up
the It used to be you'd hold up a chip,
and now it's like hold up an SOC, and
eventually they're going to hold up like
this, you know, 7x big thing, and then
someday, maybe when our kids are doing
this, you know, are they holding up
whole wafers? I mean, Cerebras is
already.
&gt;&gt; Yeah, yeah, Cerebras is already.
&gt;&gt; And maybe
COPOS, CoWoS, or whatever, would would
circumvent needing system on a wafer. I
don't know, we'll save that for another
episode.
&gt;&gt; Yeah, yeah, yeah. We we we are not going
to do that. But, what is the size of
EMIB panel EMIB right now? Like, what is
the biggest reticle they can do?
&gt;&gt; Yeah, I don't know what it is today. I
know that they're going to I think with
EMIB-T, they're going to get to 8x
reticle size. Maybe that's where they're
at today, 8x reticle size. And then, I
think in just 2 years, they're going to
get to greater than 12x reticle size by
2028. And it's rectangular, like 120 by
180. If you go Google it, it's cool
because you'll see they they'll show
like a 2 by 4 grid of dies, and then all
these little like
rectangles that are the bridges to kind
of
conceptually show you how the bridges
are connecting essentially on the
perimeter of all the die, and then in
between all the die. So, your 2 by 4
grid, you can picture all these little
bridges on the outside connecting to
other things, maybe HBM or whatever, and
then also in between them, like
stitching them together, so to speak.
Um so, yes. Uh
CoWoS is good, EMIB is also good. They
have their pros and cons. I hope you
learned a lot about packaging, about
advanced packaging, about CoWoS and
EMIB. And thank you for listening. Um
thank you to everyone who's listening on
&gt;&gt; [laughter]
&gt;&gt; Yes, yes, very long episode. Um maybe
we'll edit it down a tiny bit. We'll
see. But, uh
hope you enjoyed this. And uh to our
YouTube listeners, thank you so much. We
had so many YouTube listeners listen to
our last one on towel scaling. We had
tons of comments, tons of engagement.
Really appreciate that. We read all of
them. Um it's super enlightening, and
it's just fun to see you guys learning
and engaging. Thanks for everyone who
downloads the podcast and shares it with
their friends. Uh people who watch on X,
also cool. Um good luck with the SpaceX
IPO, and uh that's it. So, if you're
enjoying Semi Doped, share it with your
friends. Subscribe to our newsletters.
If you like us, we have little takes
daily at semidoped.com. It's totally
free. Check it out. Share it with your
friends, as well. And with that, we'll
wrap it here.
