---
source: https://www.youtube.com/watch?v=Y9WNNsX6lyk
vid: Y9WNNsX6lyk
title: Huawei's Tau Scaling Law: Is the "EUV Killer" Real?
date: 2026-05-29
duration_sec: 2331
channel: Semi Doped
kind: transcript
---
The fact that we are stacking logic on
logic has two implications. The first
one is it is entirely centered around
hybrid bonding because that is the
secret sauce that allows them to
increase transistor density.
&gt;&gt; Welcome to another semi-doped episode.
I'm Austin Lines with Chip Strat and
with me is Vic Shaker from Vick's
newsletter. Hey Vic, what's up?
&gt;&gt; Yeah, how's it going?
&gt;&gt; It's going well.
Yeah, it's a nice time to chat. We we
usually do this later in the week. So,
usually we record on a Thursday, but
today we're like doing Tuesday. And it's
perfect because we were actually going
to talk about something else, but then
there is this paper that dropped from
Huawei that said something to the effect
of, "Oh, we're bypassing EUV. We're
going to be in like TSMC's 14 anstrom
equivalent by 2031 and everything online
is all at once. Uh this is hitting
hitting me in my face saying Huawei has
you know circumvented EUV ASML is dead
in the water. US dominance is gone and
leading edge nodes. I mean at least
that's the sentiment I get and
considering we recorded the deep dive on
lithography last week. So, I know I I
texted you and be like, "Okay, like, can
we just talk about this early this week
because it's so fresh in my mind, we
should just do this."
&gt;&gt; Yes. Yes. So, this is perfect. Let's
talk about it. And in fact, it was
Memorial Day in the United States
yesterday, so I was like hardly even
online, but the internet was blowing up.
So, I'm I'm glad that you text me. I'm
glad that you read it. I look forward to
learning from you through this
conversation. And I will say I wonder
how um the United States government,
anyone in those circles, like the uh
commerce department stuff, how they're
feeling because of course lithography is
e EUV lithography is the big
geopolitical chip on the table. Um and I
bet some of them have to be freaking out
if they heard or saw an X like, "Oh
yeah, that you know what you used for uh
controls is now rendered useless." They
have to be also like, "Wait a minute. Is
this real or is this marketing? So
that's the goal of this is to unpack
what actually
did Huawei announce and was the
marketing speak and the interpretation
different than the technical paper and
the and the technical innovations here.
&gt;&gt; Yeah. So uh we wrote this down um in the
semi-doped uh newsletter. Uh this is
kind of where our first reactions go. So
if you're not signed up to that, you
know, uh as the listener, you should.
It's it's free on Substack. You should
just go to semi-dop.com and just like
sign up because whatever news comes our
way, we just try to like write up
quickly the first thought that comes to
mind. Usually it's the most natural
response. But uh yeah, after that um I
think I got a few questions saying,
"Hey, what do you think of this piece of
news?" Uh and then I responded and said,
"Yeah, um this is really interesting
that you know Huawei is has this
approach of trying to improve
performance of chips overall but without
trying to go to the you know the fancy
machines which they can't get a hold of
because they're all under export
control. So without much ado, I think we
should first explain what the whole
claim was. So there is this conference
uh called ISCAS 2026 that I believe is
being held in Shanghai uh this week and
um Hey Tingbo who is like a Huawei
director and the head of high silicon
which is the chip arm of Huawei uh he I
think gave a talk. So was that I did not
hear the talk. Do you know if hating is
a he or a she? Because I might totally
get this wrong.
&gt;&gt; Um I saw a picture of a woman. So
&gt;&gt; okay
&gt;&gt; I think the she gave whoever gave the
talk was a woman I'm pretty sure.
&gt;&gt; Okay. Okay. I'm glad I asked but uh
anyway the point is the whole idea is
that um there is this new guiding
principle called the toao scaling law
and
this the spiel is at least that it's
going to replace m's law because you
know time the the whole um over time m's
law has stopped scaling and it's we've
been you know squeaking along ever since
we hit kind of the EUV nodes below 7
nanometer and the whole idea is like
okay let's look at something else and so
this is where I actually like this
framing actually the toao scaling law
has a much more fundamental scaling that
I truly appreciate and I need to explain
why why this toao thing first of all to
is a measure of delay uh it could be
delay on the chip it could be delay
through the interconnect it could be
delay between racks it could be delay I
don't know on the between entire data
centers or anything so The whole idea of
basically going to smaller transistors
was essentially to minimize this delay.
The smaller you made a transistor, the
delay got you know lesser from the input
to the output of the transistor and that
only meant it went faster. So for the
longest time the only way to make things
go faster was to reduce the delay. So
Huawei's interpretation is to stop
thinking about dimensions of the
transistor which they really can't scale
without EUV machines. Uh but why not go
down one further level and ask what was
the transistor solving anyway? And the
answer was delay. So then the next
logical question is okay we can't
improve the transistor delay anymore
because we don't have the machines. So
where else can we improve the delay?
Because it's not like delay comes only
from the chip or the GPU or the CPU
whatever it is delay is everywhere.
Delay is in software. Delay is in
interconnects and how you hook up
memory. What memory protocols and
handshakes you do. So they were like
okay let's reinvent everything and think
of this from a whole system perspective.
So this is what they call their tow
scaling law. We will now scale down TOAO
at the system level. Not so much at the
transistor level that has been done
historically but over the entire system.
It could be a phone to begin with or an
entire AI data center. We are now
scaling down delay. Okay. Yeah, that
makes sense. I mean, so so summarizing
it, they're basically saying, hey, uh,
Moore's law is dead. And by the way,
even if it's not dead, we can't shrink
transistors anyway because we can't get
our hands on EUV tools. So if we want to
continue to increase performance and we
can't reduce the geometric footprint of
each transistor, how can we increase
performance? And so they zoomed out and
said, well, wait a minute, m maybe the
geometric scaling of transistors was
actually ultimately about reducing
delay. And so then they're trying to
reorient around tow this time delay
resistance capacitance uh product and
say okay fine we we don't have the we
have one knob that we can't turn but
what are all the other knobs that we
could turn to continue to reduce delay
and I do like the point of not just
delay at the transistor level but
extreme co-op optimization or STCO DTCO
which we could talk about um I saw you
had a tweet about this um which is just
saying how can we look up and down the
whole stack from transistors and devices
to circuits to systems to racks to
interconnects to the whole data center
to software on top of it and how can we
try to co-optimize amongst all of those.
Yeah. So whenever they say this is kind
of a law uh it's always nice to see some
equation and I read the whole paper
actually uh it's an easy read for a
paper actually and they had this nice
equation which says the toao of the
transistor toao of the system is
basically the delay through the
transistor delay through the circuit uh
delay through the chip and delay through
the system right and what they want to
do at every subsequent generation like
the tow of the next generation is the
tow at this generation divided by some
factor alpha where they think that that
alpha factor is like um 1.3x
uh a year for mobile and 1.5x for auto
and maybe even 10x for AI workloads. So
think about that like optimizing across
the system. They are
thinking that they can reduce the delay
by 10x for AI workloads. That is a
significant improvement and that is why
they feel like um they can get a 1.4
nanometer class performance by tweaking
other parts of the system not just the
transistor.
&gt;&gt; Okay. So this law like you know most of
these laws are not actual physical laws
but they're observations. So they must
have had in their paper were they
showing just like chips that they
created and measured these constants and
and that's where they're seeing the
scaling or where where did this data
come from in this like observ empirical
observation?
It's not anywhere I think. So they have
some silicon. Okay. So let's get to that
in a bit. But their optimizations were
interesting because they happen
basically across what from what I could
tell across three dimensions. The first
dimension was that they just want to
make transistor density more, right?
That's the whole thing that EUV does.
EUV lets you pack in more transistors
per unit area of the chip by making
transistors smaller. So they stepped
back and like asked, okay, we can't make
transistors smaller. So, how do we scale
up the number of transistors in a chip?
So, they decided, okay, fine. We'll just
take two chips and stack them one on top
of the other
&gt;&gt; and like hybrid bond it. Hybrid bonding
is a packaging technique that's very
interesting because you can have like
millions of connections between these
two logic chips and uh the way it works
is that you just heat them and like put
pressure and they literally stick to
each other in the most simplest way.
That's what hybrid bonding is. So you
can have like very very very fine uh
connections that are like closely spaced
like the pitch between connections is
something like 1.5 micron across a
massive area of a chip. Think about that
right. So hybrid bonding is a very fine
uh pitch packaging technology which is
probably the most advanced packaging
technology you can get. So their first
dimension was okay let's just stack two
chips together. So in the space of one
chip we get now two chips. Hooray. You
know, that's one way to get transistor
density. H that's a kind of cheating
because now you also use two times the
silicon area because you got to sandwich
two wafers together, but you know,
considering the cost of EUV, which we
discussed in the last podcast episode,
uh maybe it's not a big deal. Just
saying.
&gt;&gt; Yeah. Yeah. Yeah. Totally. Okay. So
there, so you're saying they can't so
they've got a chip, they can't increase
the transistor density because they're
at their fundamental limits with DUV and
multiattering and whatnot. And and
historically, by the way, how um the
industry is kind of quoteunquote getting
around Moors law is like systems of
chips, you know, so it's like, oh,
whether you're using chiplets or
whatever, so it's like, okay, well,
let's use like 2.5D integration. Let's
put chips next to each other and then
we'll have coas, you know, or
interposers and connecting things. Um
but but you're saying that Huawei said,
"Oh, no, wait a minute. Well, what if we
like instead of putting those
transistors far apart and have increased
delay because now you we've got to route
between them. What if we just try to
decrease the delay by stacking them in
three dimensions to sort of increase the
the density if you will in a unit volume
really?
&gt;&gt; Yeah, they call it logic folding.
&gt;&gt; Okay. uh which is a nice name but it's
really if you think of it no different I
feel compared to what Intel foros is
&gt;&gt; or how uh AMD stacked SRAMM with vcash I
guess it's not technically you know
logic tologic stacking when you're
talking about AMD's vcash because they
put SRAM on top of a logic wafer to
boost like L3 cache on it but in
principle yeah they hybrid bonded a
SRAMM wafer onto a ch a logic chip and
that's kind of what this is all about.
So logic to logic stacking is is not not
easy right because what how we going to
get heat out of this thing that's one
one example like thermals are quite
challenging so there are a lot of
challenges to doing this stuff actually
&gt;&gt; and you know you got to align it like
think about it like the the connections
are like 1.5 micron pitch actually is
ridiculously tiny and so the alignment
between the bonds needs to be perfect
and hybrid bonding itself isn't is a
crazy packaging technology because the
surface Notice that your bonding needs
to be very flat and defect free and all
that because when you squeeze it
together there's like a dust particle
between the two of them or whatever like
you know what happens like now you've
got an open connection
&gt;&gt; between the two you know sandwich chips
and that's bad. So it's it's a
challenging process and that's the whole
question is like
&gt;&gt; does um China actually have the
equipment to do this? Yeah funnily they
do. do they do because for two reasons.
One they do have this expertise because
they have been doing uh memory stacking
for NAND at YMTC using waferto- wafer
stacking and hybrid bonding of chips.
That's how NAND chips work. They have
even done hundreds of layers of NAND. Um
so they are familiar with it but memory
is little bit of an easier problem
because
memory has so much redundancy that you
can kind of route around stuff like have
uh failovers in the memory architecture
and stuff like that. So stacking is a
different problem in memory than it is
for logic. Stacking two GPUs on top of
each other is a significantly harder
problem than trying to stack 400 layers
of NAND memory you know. [laughter]
&gt;&gt; Totally totally. So okay so you're
saying historically
stacking things is not a new concept.
Even stacking logic is not necessarily a
new concept but normally when we're
stacking first like let's say logic on
an interposer that interposer is
passive. Um so it's it's not as big of a
deal. You're just routing through it.
And then even if you're stacking like
memory on logic, um that's a little or
and of course memory and NAND and HBM, a
lot of these things are already
three-dimensional. So we're already used
to figuring out how to create things in
three dimensions and stack them. But it
is a bit of a different beast when we
stack logic on top of logic because
they're both active, they're both
powered, they're both giving off
thermals, and you have to make sure all
the connections are correct. And there's
like today the way these things are
built there's not this built-in
redundancy where like oh if something
fails just route around it. Um but
conceptually it's still to the industry
logic on logic is not a new thing that
Huawei has invented.
&gt;&gt; No it's not and it's been around in in
in principle. Uh so that's what makes it
interesting like it's a challenging
problem and it's it's impressive that
they do have silicon that uh they it's
called the kirin 2026 this is a mobile
SOC processor uh and they actually have
this implemented um and they have plans
to keep going uh in the future so
they've already you know let's say I
don't know how the paper has all these
numbers oh yeah here I have them I think
yeah they they've managed to like double
their transition account. Yeah,
obviously by stacking and uh so they
they kind of jump nodes in in principle
because you know we spoke about this
there is no such thing as like five
nanometers or two nanometers anymore
because the transistor architectures
have changed. So this is just a
nomenclature now anyway. So you can go
to the same class node by doing other
things like gate all around was one of
those other things like you could do to
go to two nanometers.
So Huawei's approach is like yeah we'll
just stack transistors and we'll get the
same transistor you know density. Um, in
principle this is like you know C FET
maybe like a complimentary FET where
people were like why should I put an N
MOS and a COS NOS and a POS transistor
next to each other
&gt;&gt; cuz for a for a COS a complimentary MOS
you require PT type and N type
transistors what if I put them on top of
each other you know I can save space so
this is along the same inspired lines
not exactly the same thing but basically
you can why don't why not put a whole
transistor wafer on top and stack them
like that and you can jump generations
forward. So this is they've done it
actually and this is very impressive
engineering. All kudos to them. I'm not
going to take away from their
engineering achievement here. So that is
the whole logic stacking aspect of it.
There are two more things that I think
are very useful but I want to get to
that after you ask me this question.
&gt;&gt; Yes,
thank you for letting me graciously
interrupt. Um, so on the logic stacking,
so one of the things this reminds me of,
of course, is DeepSeek in that they
could not get enough compute. They could
not get enough compute and enough like
memory bandwidth with the chips that
they were given. Allegedly, okay, maybe
they did find their way to some H100s,
but allegedly they had these strip down
which caused um the Deep Seek team to
have to innovate in other dimensions
because they were constrained on one.
And so then they got to be the first to
think deeply about other things like you
know how do we offload some
communication overlap some communication
and compute do other little tricks so
that we still unlock the right
performance and so what I'm thinking
about is okay if Huawei is constrained
to not use um EUV and therefore they're
thinking about like okay how can we
reduce delay in other parts of our
system and one of them is it's forcing
them to go to logic to logic stack
hacking maybe sooner than the rest of
the industry feels that they have to. My
question is who is manufacturing it and
is this giving them an advantage in just
getting more practice manufacturing
logic on logic? Like will they be able
to sort of run ahead a little bit
because they are forced to build this
for their customer sooner than say a
TSMC?
&gt;&gt; Yes. Um, this brings actually it's a
good question and I'm glad you asked
this now before I went on to talk about
something else because the fact that we
are stacking logic on logic has two
implications. The first one is it is
entirely centered around hybrid bonding
because that is the secret sauce that
allows them to increase transistor
density. Um, so you can increase the
density two times. Can you stack it
three times? I don't know. Can you stack
it four times? I don't know. Like, so
what is the limit on hybrid bonding
here? How many layers? That's something
I don't know. But remember, it gets like
extremely difficult because
um if you are stacking logic on logic,
you would I think you would want to do
die to wafer stacking, not wafer to
wafer stacking because you will get
wrecked on yield. you know as it is
these logic chips are kind of big and
yield is such an important thing because
you know you don't get all that much um
as people imagine especially at the very
cutting edge but maybe 7 nanometer nodes
is okay so that is one aspect of it that
it's entirely based on hybrid bonding
and the question is are they capable of
it and the answer to that is at this
point uh memory to memory wafer was all
like so memory stacking is all like
wafer to wafer but logic needs die to
wafer and that is kind of new even to
like bezi and these companies that
specialize in hybrid bonding and even
they have pro product releases that are
like very recent okay so die to wafer
bonding in logic chips is very cutting
edge and luckily from what I was looking
at this there is no export restriction
uh on bond hybrid bonding machines you
have extremely high limitations on what
you can do in EUV but not so much on
hybrid bonding machines so that's that's
that's one thing so they do have the
machines that they can do this with and
if you look at like Bezy's business 35%
of all their business is actually China
based if you see the last quarter so
that is actually a a large fraction of
their machines actually do go to China
so I'm pretty sure they've stacked up on
some bezy machines before they let this
cat out of the bag. Because if you
already has a have a silicon piece of
silicon that's stacked up you and and
working as in the Kirin mobile SOC's,
you can believe that they've been
working on this for years. Okay. This is
not an overnight achievement.
&gt;&gt; Sure. Sure. So, you're saying Smick is
the manufacturer here and they can't get
EUV machines, but they can get hybrid
bonding machines and hybrid bonding is
the secret sauce here to logic stacking.
So, do you think that someone's going to
try to go say now you can't buy hybrid
bonding equipment anymore?
&gt;&gt; So, Huawei never said it's smick by the
way. Everybody assumed it is. [laughter]
&gt;&gt; Okay. Okay. because it's a reasonable
assumption and the stock went up and all
that which is cool but uh and I don't
think it's smick who will do the
stacking aspect of it either because
there are specialized people uh in
packaging in China um who's whose names
we don't have we shouldn't get into I I
I'm writing an article on Substack on
this so all those details will be on
there but that there is another company
that will do this the hybrid bonding
because there is a whole learning curve
on learning to do hybrid bonding. So
there are companies who have patents
just on hybrid bonding and that is
something that is not easy to do. So
that's a separate skill set. China is
working on that as well.
&gt;&gt; So that's the one important thing is
that
&gt;&gt; it's all hybrid bonding based and uh the
next question is like okay does China
have any local hybrid bonding machines?
The answer is uh yes they do uh but I
don't think that they are in the same
level of sophistication there is um for
you know in their wafer to wafer bonding
for example so that is something they
still rely on bezi and to answer your
question yes so they they can impose
restrictions on it on China I I presume
um but
it really comes down that if they can
get to do EV group uh wafer to wafer
bonding there is a company called EV
group which is in an Austria based
company and they are not in this this
axis of like export restrictions that
you know Bezi is in because Bezi is an
is a Netherlands-based company and you
know they're in the same boat as ASML
and stuff like that. So this these
countries have a lot of export
restrictions, but if they can do wafer
to wafer bonding, who knows? Maybe they
don't are not subject to export
restrictions because Austria is not part
of this thing. [laughter]
&gt;&gt; Yeah. Well, so okay, I did not expect
that this conversation would get so much
into hybrid bonding. So that's cool. And
I'm like, I need to go learn more about
hybrid bonding in the market and who all
the competitors are. Um, and then two,
yes, these poor European countries,
they're like, we invented something.
we're awesome at wait for wait for
hybrid bonding and then you know they're
going to get caught up in the crossfire
of geopolitics. You know the one thing
is I got I anticipate is like oh wait if
if China can't do EUV is AML ASML
affected by this and this news of to
scaling no because first of all they
were never buying EUV machines from ASML
they can't okay so there's never a
business to begin with secondly I will
argue that this is actually good for
ASML because remember now they have to
make two wafers using deep ultraviolet
uh you know DUV for every transistor. So
they need more DUV machines which is a
positive for I would say SML, right?
&gt;&gt; There you go. I like it. That's a
positive spin.
&gt;&gt; Yeah, that's a positive spin on it. Uh
so so that's the whole thing about uh
you know how this whole logic thing
works.
&gt;&gt; Okay, so then really quick logic to
logic. Maybe last thing we're talking
about uh companies who build the die and
other companies that package them. It's
kind of like the front end and the back
end. Um, of course, Intel Foundry can do
both. So, they can make the wafers, they
can also do the advanced packaging. And
you mentioned Intel Faros Direct. Um, so
could you say like 10 more seconds on
Faros and if this is a direction that
Intel foundry could support with the
logic on logic stacking and packaging.
&gt;&gt; Yeah. Uh, I don't see why not. That is
essentially what Intel for is as far as
I understand it. And what this shows is
that
this is the other thing I wanted to
mention. Um it comes to me now that you
asked the question. uh is basically
there is no reason that any US fab like
Intel or anybody else like TSMC
shouldn't start stacking wafers now
because if you stack a 7 nanometer wafer
and then you get to scaling to work
imagine what will happen when you stack
a 5 nanometer wafer or a 3 nanometer
process node or a 2 nanometer process
node you're going to you know leapfrog
past what uh China can do with Tao
scaling. So they may be able to catch up
but what this will do now is drive the
ability to do hybrid bonding uh in the
advanced EUV nodes because why not it
it's not an overnight thing. It's a very
complicated thing to do and but it you
know think of it long term if you can
stack two nanometer node wafers that is
an an amazing amount of compute in a
small area and uh we may get to see FET
before that maybe we don't need it we
may do hybrid bonding of gate around
FETSS before CfET shows up don't know or
we may hybrid bond CF fet wafers
together ultimate the ultimate density
move. [laughter]
&gt;&gt; Totally. We should do it all, right?
Like the front-end folks should keep
working on the transistor innovations
and the packaging folks should keep
improving stacking and hybrid bonding
and then slam it all together. And but I
do agree with your point, which is like,
okay, let's say I'm like, oh, I can do a
billion transistors in this little area
now. I can stack them so I get two
billion. And then you're like, oh, well,
I'm on an advanced node and I can do 1.5
billion transistors in the same area.
And now I stack it. Now I have three
billion transistors. Right. So it
compounds totally. Yeah. So the whole
tow scaling thing is not a I will
replace EUV technology and leapfrog
around you without the right tools. It
is a temporary measure where yes you can
bump up the performance of silicon uh
with this technique. But if the people
who are EUVabled
do start doing the same thing and they
will because that's how the industry
works. they're going to sit down and not
do something about it. Uh then you know
the gap widens. It doesn't narrow. The
gap widens. That's a good thing.
&gt;&gt; Yes. And maybe to make the point yet a
third time if someone after Huawei's big
tow scaling announcement if someone came
to that to their silicon manufacturer
whoever that is and said would you like
EUV as well? I'm sure Huawei would say
sounds great.
&gt;&gt; Let's have that and to scaling.
&gt;&gt; Yes. Exactly. That's what you do right.
that's the logical thing to do. So yeah,
absolutely. So that's the whole that's
the whole aspect about logic uh folding
and that is mostly the discussion that
is going on here. But there uh their
paper actually talks about a few other
dimensions that at least is worth
mentioning. Um and that is basically
what they call uh the unified bus for
memory. So because they say that look if
you have all these different memory
standards talking to each other and then
you have to have all these handshakes
and converters and gearboxes and all of
this stuff that adds latency uh then you
know you're wasting cycles here. Okay,
you're wasting towel. Don't waste what
we will do is we'll have a universal
language
which everything in the rack or the
system or the data center I don't know
the earth if you could will all speak
the same language so that there's no
like translations happening and so that
is one way to scale down the entire
thing uh the delay and speed up stuff.
It's a very good one. I mean I love it
right. It's a it's a very good thing to
do anyway regardless of whether you have
EOE or not.
&gt;&gt; Totally. Totally. So, I mean, isn't that
ultimately like weren't we trying to do
that with like RDMA and things and just
say like how do we make it so that GPUs
can communicate with other GPUs to talk
share their memory directly without so
many handshakes? I mean, was the
industry already on this path and does
this just speed it up and say, "Hey,
there's more latency to get rid of."
&gt;&gt; Exactly. That's that's the whole point.
The industry has been there already.
Again, this is not a new concept,
&gt;&gt; you know.
&gt;&gt; Mhm. Just a different prioritization.
&gt;&gt; Yeah. Exactly. When Jensen talks about
extreme code design, I mean, what do you
think he's thinking about? He This is
what he's saying, right? Don't uh just
think about one thing like memory in
isolation and work with your own
standard and when you try to plug it
into a system, it has to talk a
different language and now everybody's
like, "Oh, can you convert this language
to that language?" And don't do that.
Let's look at the whole thing as one
picture and then optimize everything for
that you know system level optimization.
So this is this is the you know STCO
argument or you can call it extreme code
design whatever fancy word you you you
want to use to scaling seems like the
fanciest word I've heard yet.
&gt;&gt; Yeah, very good. Yeah, their marketing
folks did great. So yes, you may have
heard the term STCO system technology
co-optimization. Jensen took it up a
notch with extreme code design and now
Huawei is trying to one up with tow
scaling which I mean it does sound
pretty sweet.
&gt;&gt; It is pretty sweet. It is pretty sweet.
&gt;&gt; Yeah. You know one other thing they want
to save tow on is uh networking
because they are like why don't I just
do near packaged optics
and eliminate DSPs from the entire
system if possible. DSPs are terrible
for latency. They are towel killers, you
know. DSP is the towiller. Like, you
know, like fear is the mind killer in
Dune. If you've ever read the books,
&gt;&gt; DSP is the towiller. Uh yeah, because
you know, you have to wait for all the
bits to arrive and then you have to wait
for the parity bits to come and then
DSPs look at it and like, oh, are these
bits correct? Oh, they're not correct.
Cool. Then I have to correct for the
error and then does all this
computation. You need like a leading
edge node to do this DSP stuff. Sucks
power. sucks latency and they want to do
away with it. They're like just get rid
of, you know, DSPs. Don't use all this
pluggable stuff. Use as much as close as
you can to CPO, which is like maybe near
packaged optics. Maybe you don't. Maybe
they'll they'll try to package the
optical engine right on top of this
[laughter]
stack.
&gt;&gt; Stack it up.
&gt;&gt; Let's go.
&gt;&gt; Logic folded logic, whatever. Yeah, I
don't know. But anyway, at least in the
near term, they can put the optical
engine as close as possible to the
actual compute silicon. That's one way
to reduce cycles. So they're looking at
all of this stuff. Obviously, you can do
software optimizations, all that kind of
stuff. So at the system level, they want
to squeeze as much performance as
possible, which is the only logical
thing you do when you don't have access
to leading edge silicon. What do you do?
You do everything else.
&gt;&gt; Exactly.
&gt;&gt; That's what scaling is.
&gt;&gt; Okay. Gotcha. Gotcha. Okay. Yeah. I
mean, yeah. Of course, you know, NPO and
CPO make a ton of sense. Everything
comes with trade-offs, though. So,
there's the the whole like, does the uh
supply chain support these things? Are
they ready for it? Can they build it
reliably? Do you have multiple sources?
So, I think that's, you know, it it
feels a little bit academic in that on
one hand, like anyone could sit down and
look at a system and just say, what are
all the different ways we could wave a
magic wand to reduce towel? Um I don't
know if they talked about like all the
practical bits in the paper or or if
this was more of just like whiteboarding
out where the bottom
&gt;&gt; very high level. It is interesting that
they have some silicon to show for it
which I love but it's also a lot of like
highlevel handwavy equationy stuff. It's
not very complicated equations. You can
read the paper. It's it's online you
know you can find it. It's not a very
complex paper. It's very marketing like,
but uh it's just it's a good read cuz I
think
&gt;&gt; it is a it's another knob the industry
hasn't entirely [snorts] paid attention
to. I think we're getting there and this
is one of those signs, right? We we
realize that we need more speed. We
realize co-ackaged optics is coming
along. We realize that memory
bottlenecks are the biggest problem.
It's not compute flops. its memory and
the interconnect that is really holding
back everything now and this is the next
step like okay how do we squeeze and
make uh you know active silicon in CPUs
GPUs or whatever that is more dense and
that the insane way to do it is like
start stacking them and hybrid bonding
them but you know this whole thing is
insane so what's new AI is insane to
begin with so what's new
&gt;&gt; totally totally yes never before right
have we tried to co-optimize on such a
grand scale and such a miniature scale
and so I do like looking at a different
constraint to optimize around up and
down. So I guess maybe final takeaways
like what does this mean and you kind of
alluded to it before like what does this
mean for everyone else for TSMC for ASML
are are there other than the fact that
they're not dead and EUV is not going
away um are there any other takeaways?
I don't have too many unless there is
something that comes up that I haven't
thought about but whatever I thought
about I already said in the sense as a
broad summary it's just like I think
going to stacking chips is a positive
for ASML because you need more machines
to make more uh chips for the same you
know product need to make two times as
many wafers which is a good thing. The
other thing is that you will see most of
the industry now starting to optimize
across the entire stack. That's already
happening. Nothing new about that. Uh
and then you I'm guessing that we will
start seeing some activity around
stacking up wafers. Maybe somebody's
going to try to, you know, use Intel for
kind of try to stack GPUs, stack GPUs. I
don't know. That's just a guess. But
yeah, I think you know once Huawei talks
about this logic folding idea, more
people are going to do it and that's a
good thing. Got to try more complicated
stuff. That's how we move ahead.
&gt;&gt; Totally.
&gt;&gt; I guess what's coming to mind to me for
obviously this is bullish advanced
packaging because it's just more
complicated connections [clears throat]
&gt;&gt; and then um also maybe bullish EDA and
like multifysics. Oh my god, great
point. Actually, that's a great
takeaway. Yeah.
&gt;&gt; Yep. So, we we're basically at time, so
I won't get into it too much, but really
quick at a high level, I guess where I'm
thinking is like, okay, now this is a
threedimensional problem that involves
thermals, it involves mechanical stress,
it involves electricity, it involves
optics potentially if you're talking
near uh NPO, CPO. And so, this becomes
more and more of a challenge. I think
this of course reminds me of like
synopsis and sits multifysics engine of
just like
it's going to be less and less of like
the silicon guy does this thing and the
packaging guy does that thing and the
thermals guy does that thing but all of
it needs to be brought together to
figure out how do we stack logic on
logic and remove the heat and still meet
time enclosure and still have
reliability and so on.
&gt;&gt; Yes, it is hard enough. EDA is a hard
enough problem already where we are on
single layer transistors and you know
how you scale them up uh to make the
GPUs they are today there's a lot of
advancements in the use of AI for EDA
and um the whole uh EDA industry is
actually very bullish right now because
you can basically sell licenses per
agent rather than per person and it can
do a lot of stuff now and what this adds
is a level of complexity that is you
know we haven't seen so far in the
transistor world when you start stacking
you know entire wafers and running
complete logic you know across uh two
wafers stacked of maybe four wafers
stacked in the future that's crazy so
there's going to be a lot of challenges
there and the paper actually does
mention that this is a challenge so yeah
that's that's very much a good point to
bring up
&gt;&gt; nice cool all right well folks with that
we hope you liked
this episode. Um, check out, of course,
our substacks. Also, go to semi-dop.com.
You can sign up for our free newsletter
if you like Vic and I and our takes. We
try to give takes there every single
day. And, uh, sometimes I come in later
than Vic, so I just get to take a take
on his take and he doesn't get to
respond before I hit send. So, uh, we
try to keep it light-hearted and fun,
too. But, thanks for listening and we'll
catch you guys next time.
