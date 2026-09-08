---
source: https://www.youtube.com/watch?v=VcRfZKofBGo
vid: VcRfZKofBGo
title: Optical Supply Chain: What would you buy?
date: 2026-02-28
duration_sec: 3703
channel: Semi Doped
kind: transcript
---
Every stock or company on this list that
we will talk about today has gone up
over a 100% in just one year.
Hello listeners and welcome to another
semi-doped podcast. I'm Austin Lines of
Chipstrat and with me is Vic Shaker from
Vic's newsletter. So Vic, quick, let's
start with a plug for your newsletter
because I think you wrote something
really interesting this week. He wrote
about CPUs for AI and I thought it was
super timely because on Nvidia's
earnings call this week there was some
Q&amp;A talk about the Vera CPU and Jensen
talked about how it was great for post
training and had really great I think he
called out the single threaded
performance and so this reminded me of
your article because I think the
underappreciated thing everyone's been
talking about the demand for CPUs for AI
but people haven't taken it a level
deeper and said well what are those AI
workloads in which CPUs use fit the
different types of AI workloads better.
Um, so for example like having many
threads for and and cores for agentic
tool use is something that you called
out and I thought was really
interesting. So like give me your quick
thoughts on that article.
&gt;&gt; Yeah. So in that article I have like
basically a sliding scale of whether uh
any given CPU from any company whether
it's x86 or ARM can be put into more of
a reasoningheavy workload where it's
like only job is to have fast single go
performance and make sure the GPUs are
fed really quickly and that utilization
of the GPU is held high. And on the
other end of the sliding scale, I
basically have categorized what are
called actionheavy, you know, workloads
where the CPU does a bulk of the
lifting. Maybe it goes and scrapes a web
page, uh, does some API calls and looks
up a database, that kind of stuff. And
the GPU is it is being constantly used,
but the critical point is that you need
a lot of CPU cores so that you can
handle multiple agents and all these
agents are going to keep the GPU
completely fed. Uh so after that with
that framework I have like nine
different metrics you can rate a CPU on.
And so uh to follow up to that concept I
have like this yellow pages of all like
popular CPUs that are ranked on these
nine metrics and then sorted into uh
somewhere on this scale of reasoning
versus action. Uh some of them fall in
between. Some of them fall uh don't do
well either way. So it's it's a very
gray area. I'm trying to sort out uh
exactly what Agentic C AI needs in terms
of CPU. So that's the whole article.
&gt;&gt; Nice. I love it. And if you're a CPU
designer, you should read it and be
framing your portfolio in terms of AI
workloads. Like tell us, I want to hear
from companies. Tell us. This is our
skew that we think is going to be
awesome for agents, you know, like would
love to dig into that more. So anyway,
everyone go check out that article and
I'll give a quick plug for Chipstrat. Uh
I wrote I did a deep dive on Arista this
week earlier in the week uh talking
about how the Ethernet TAM is expanding
not only for scale out but for scale up
for example with EON um that Broadcom is
championing and how that can benefit
Arista. And then I also had a fun look
at a startup tackling the economics of
lithography. This is a US-based company
called Xite. super interesting business.
It they're using particle accelerators
to generate light and then you would
feed that light into ASML EUV scanners.
So instead of doing the tin droplet LPPP
light source is what it's called. You'd
actually use a particle accelerator, you
can power many scanners with one
particle accelerator. And then the
business model is super interesting too
which I dig into. You can think of as as
like photons as a service which is
really just like a utility. Like what is
our electric utility? It's nothing but
electrons as a service, right? So, this
would be a similar idea.
&gt;&gt; Um, and finally, Pat Gellzinger is the
chairman of the board on this company.
So, always interesting to see industry
luminaries helping out startups like
that.
&gt;&gt; Um, all right. So, Vic, let's get into
the podcast. Uh, what should we talk
about this week?
&gt;&gt; So, last week we spoke about all these
optical technologies because optics is
all the rage right now. But um in the
episode we actually said we'll talk
about the technologies and then the
companies but then we kind of ran out of
time and one of our you know keen
listeners commented and said hey where
are the companies you promised? So this
is like the followup to that podcast
episode. So we can dig into some names.
Obviously there are a lot of names in
the in the optical space. All of which
are very interesting and all of which
are doing like well right now. But uh
for the sake of this episode, we're
going to like limit ourselves to some of
them. And uh if we left out any, let us
know in the comments. We'll we'll talk
through them in the future because this
is how we know what to create next,
right?
&gt;&gt; Yeah, totally. Always love to hear from
our listeners.
&gt;&gt; Yeah, let's do that. Yeah, let us know.
So we will follow up with whatever
information we could uh dig up on all
the interesting stuff that's going on.
But instead of just talking about
companies, uh I propose that in this one
we play a little a little game. So the
way we'll do it is um Austin, I'll tell
you what the company does um and why it
matters, what the mode is and basically
why it wins and also what its risks are
or what the bare case might be and then
uh you can tell me if you feel like you
will buy the stock or you will not buy
the stock, why or why not. and I'll kind
of pitch in and say what I think of it
and we'll move on to the next one. Uh,
and be warned that a lot of every stock
or company on this list that we will
talk about today has gone up over 100%
in just one year. Okay? Like the first
one we will talk about has gone up
a,000%.
So that's the way it is. So, we're not
going to look at it from the point of
like price to earnings ratio and all
that that kind of stuff. It's just like
let's see the core thesis, see if it
makes sense, you know, and give it a a
thumbs up or a thumbs down or even a
maybe or maybe or not right now or
something. Doesn't matter. It doesn't
have to be binary. And then we'll take
it from there. So, it's kind of keeps it
interesting and not like drab as we go
through these companies. What do you
say?
&gt;&gt; Sure. Sure. Yeah. Sounds fun. Um, I will
say not financial advice. Do your own
due diligence. Don't invest in this be
or any of these companies because we say
so. Uh, this is just a fun way for us to
think through the company's thesis and
their modes. Totally.
&gt;&gt; Yes.
&gt;&gt; All right. Where should we start?
&gt;&gt; Uh, okay. So, I think this one I will
let you explain to me and we'll see
we'll see what I'm going to we'll see
what comes out of it. Okay, first one on
the list, AXT, Inc. So, this is a$1
billion dollar market cap company. You
would call them a micro cap really. It's
pretty small company. They make indium
phosphide substrates. So, this is the
base wafer that every EML laser and
silicon photonics component starts on.
And AXT, um, which I think they're I
don't have it written down, but I think
they're headquartered in California. um
they have 60 to 70% of global share and
I guess why we would be talking about
them right now is they would sort of be
at the very bottom of the optical supply
chain in that everyone you know
downstream depends or above them if you
will depends on indium phosphide
substrates so if you don't have the
substrates you can't make lasers can't
make lasers you can't make transceivers
can't make transceivers no AI optical
networking Um so obviously that would be
a a key you know bottleneck even if they
aren't huge they are very important. Um
so I think you know when you study AXT
the moat there would be so then you know
you might ask oh wow if they have all
this market share and they're pretty
small shouldn't couldn't other people
just jump in and also start making
indium phosphide wafers. I think that
the moat here that they can ride on is
that uh indium phosphide crystal growth
it's not trivial. It's sort of part art
and part science, part material science,
you know, decades of process knowhow. Um
and obviously
just because you make something that's
hard to make, you still have to take it
to market. And I think uh AXT and
listening to their most recent earnings
call um they have a lot of the biggest
names that are buying from them. They've
got uh massively growing backlog. You
can tell the demand is huge and and and
obviously they they should be tied with
the inflection like the optical
inflection. uh the you know again if you
start with the AI racks like the more
optical fibers and lasers that they have
a rack has as they get these data
centers get bigger and bigger and the
more maybe scale up CPO that happens
like this all sort of ties to needing
more indium phosphide
um let's see if I have to think through
risks I think um maybe one interesting
almost irony here right now with all of
our geopolitics is that this is a very
important optical supply chain component
and it's an American company but the
substrate is made exclusively in Beijing
and therefore sub subject to Chinese
export controls. So we're not talking
about American export controls into
China but actually Chinese export
controls back to the United States. So
that's obviously uh on their earnings
call they actually had um for the first
time some permits were delayed from the
Chinese government and it actually
impacted their revenue. Um so that would
be the big risk. One big risk for this
company is just
how much of their company is uh
dependent on geopolitics and maybe
things that are a lot harder to directly
control. So how about I I pause there.
How's that for like a high level
overview? Sounds good. That's a good
overview. I think it it has all the
pieces in there. I just wanted to add
like they have a significant market
share like 50 to 60% which is why
they're dominant. But the competitors
would be like Sum Sumitomo. Um I think
they have something like a 25 30% share.
uh but like the the fundamental problem
like in what you explained here was not
what you said but with the company is
that their manufacturing is subject to
Chinese export controls. It is not in
the hands of the United States even
though it's a US company and if you look
at the stock price of this company it is
uh it was about a dollar or two but
which has gone up to like 40 bucks in
the last year. So, and if you look at
the like the the earnings and the their
numbers like the the next quarter
guidance is um minus4 cents to plus 2
cents earnings per share which is like
almost I mean they're making the what's
funny about this is that I think people
who ended up buying this stock at like a
dollar and you know sold it at like4 $40
are making more money than the company
itself. So it's it's kind of funny. So
if you ask me, would I invest in this?
I'd say no. Even though the entire AI
industry hinges on this, but the fact
that it is subject to a foreign
government's whims and fancies and that
uh the earnings per share is almost zero
and the stock is at like extremely
elevated levels growing over a,000%.
puts it out of the range of risk for my
personal taste. What do you think?
&gt;&gt; Sure. Totally. Yeah. Yeah. I mean, it
feels like that's going to be the common
theme with any upand cominging component
supplier in the optics supply chain,
which is probably
as they're growing, their earnings per
shuge. Maybe they're even not making not
profitable yet because they've got to
invest into more manufacturing capacity,
for example. And yet people who have
like smart investors have already said,
"Oh, let's look up and down supply chain
and invest in these companies." So if
they've sort of inflated their price
ahead of the growth of the company, the
the the argument is probably like it's
not that it's not investable, it's just
not now. Like it's it's always a timing
game as far as like is it priced to
perfection? Now, as for the not
investable part, you know, you make a
good point that people have to be
comfortable with the risk of the Chinese
export controls. So if you're investing
that would be a risk you'd have to be
comfortable with.
&gt;&gt; Yeah. Well I mean there are people who
are going to invest in it but uh maybe
this is this is why I don't make any
money. I'm very riskaverse. So you know
be noted that whatever I say is going to
come from a background of being very
risk averse but yeah maybe we go should
we go to the next one?
&gt;&gt; Sure. Sure. Yeah. Um let's see you take
so we talked about substrates. You
should take it up a level. Let's go to
manufacturing. Why don't you talk to
semiconductor?
&gt;&gt; Okay let's do tower. So Tower
semiconductor is today the undisputed
leader in the silicon photonix foundry.
So what tower actually does is they are
like the TSMC to all the chips that the
fabas companies design. So Nvidia makes
like the GPU and they give it to TSMC.
They make the chip and they you know
give it back and then they sell it
right. Nvidia sells it. So that is the
tower equivalent for the photonix
industry. So companies can make photonic
designs which means they make these
waveguiding structures and mechender
interferometers or ring resonators for
modulation. All of this stuff happens on
the silicon photonics chip and then it's
sent off to tower semiconductor who
manufactures it and gives it back. The
thing is they also make other things.
They call themselves the specialty
analog foundry. U so they they don't
really focus on digital technologies.
They more focus on silicon germanmanium
which is very important for driver
circuits for um lasers and they also do
RF and power chips power ICE and things
like that. They are actually an Israeli
company but they have a fab in Newport
Beach also. So they have such a strong
you know hold over the silicon forronics
u wafer fabrication market that you know
they I think seven out of the 11 top
dataccom transceivers um all use uh
tower and they have a very big uh market
share in what they do so for the optical
world and when it comes to this new new
generation of 1.6 60 which is really
ramping heavily in the industry. U they
they stand to be the dominant player in
this game. I have a quote from the last
earnings call from their CEO Russell
Elwanger. He said Tower's exceptional
ability to scale the capacity flawlessly
in partnership with our customer has
made 1.6 6bps, the fastest growing
silicon photonics node in the industry
to date with tower being by far the
majority supplier of 1.60 silicon pic's
photonic integrated circuits. So that's
that's their position on this thing and
from their last earnings call right uh
their revenue has grown significantly in
this in this uh area of cipher and cyho
silicon photonics and silicon
germanmanium revenue it's grown like
75%. And if you look at cyho alone it's
grown like 115%.
So it is like a doubling every year kind
of thing and it is expected to even
continuing to double through 2026. So
that is their um stronghold over this
thing and they also announced that they
are going to 5x their silicon uh
photonics wafer capacity
by investing 9 I don't know uh something
$950 million in additional cipher
capacity. So think about that like
they're 5xing their silicon photonix
wafer capacity and this is not just like
because they feel like it because they
actually said that 70% of all the
capacity has already been reserved
through 2028
backed by customer prepayments which
means they've already paid for it and
they're using that and expanding up to
5x the silicon photonics.
&gt;&gt; Amazing. Yeah, you can get a good rate
on the debt you take out to build plants
when it's backed by customer.
&gt;&gt; Yeah, absolutely. It's significantly
risking. Yeah,
&gt;&gt; totally.
&gt;&gt; And I I believe I heard on the earnings
call that they went so far as to say
like, hey, we're not even pressuring
customers to prepay. They are offering
it up because they care so much
&gt;&gt; to kind of get in line and like reserve
that capacity.
&gt;&gt; Yeah, that's the thing. and they're like
they're all over the silicon photonics
thing because they announced some
partnership recently within the last 10
days I'd say uh with Cintel Photonix to
make these DWDM we spoke about this for
longhaul optics which is dense
wavelength division multiplexing uh but
that's going to be like used for CPO
apparently and this is like the slow and
wide approach like HBM is to a GPU like
DWDM laser is like way way to transmit
optical data where each lane isn't
really fast but you got many parallel
lanes and you can send a lot of
information just like HBM is like each
lane isn't that fast but you have so
many parallel lanes of uh electrical
connections you can send memory like
high bandwidth same idea so they're
doing it with central photonics they
also recently I think two days ago
announced some partnerships with
salience labs for optical circuit
switches you know so really this is a
foundry that is like really well
positioned to hang on to the upcoming uh
optics wave and because all the wafers
if they're actually available from China
uh from AXT
you know this is the company that would
actually process them into meaningful
circuits right so this is the next layer
of the cake
&gt;&gt; all right what's your take
&gt;&gt; yep
&gt;&gt; yeah well so
it sounds like a very
definitive business that
it's already a strong business and I
think it's fair to say we can see that
it's going to grow. Um it's not
speculative. How about that? Um you know
they're ramping up capacity 5x.
It does make you wonder like oh is are
we going to get to an overupp situation?
Um especially as we'll talk about you
know go global foundaries is going to
ramp up their capabilities as well. And
so, uh, you know, when we look at the
logic market, it's not quite a good
analogy because TSMC is kind of the
monopoly there. And so, if you look at
the logic market, you'd say like, oh,
it's just going to go up and to the
right forever like GPUs and TSMC is is
just done awesome because they're the
only one that can make it and it's so
important. Maybe when you look at this
space, you could argue like, okay, well,
it's a little bit different because
there actually is going to be a
competitor and so there could be some
price dynamics and especially as they're
both ramping up capacity. Um, on the
other hand, it takes a long time to turn
on capacity. People need all these uh
silicon photonics chips today, they they
yield matters. So as we see with like uh
you know in in logic as others Intel
foundry and Samsung are trying to catch
up you know obviously it takes time to
ramp not only to like be able to do the
process node but to be able to ramp it
to manufacturing scale where you have
really good yield. Um there's also a lot
of risk I think for people when they
switch foundaries uh or or or like dual
source is is not free right and so
there's all sorts of incentives to think
about and generally even it it your
investing timeline matters too here but
it does feel like you could safely say
like wow it looks like tower is really
well positioned for the next several
years if logic is anything and then of
course if you look Maybe a better
analogy would be a memory manufacturing
where there's three competitors um and
yet the whole pie is growing. All three
competitors are doing well. Obviously
HBM is in wafers were in high demand.
DRAM wafers high demand. Um even storage
and so on. And so if you look at those
other manufacturing markets as
analogies, it's hard to see how Tower
doesn't continue to do well here. So I
say all that to say it feels like a lock
for investing in them.
&gt;&gt; Okay, good. So I I agree with you. But I
I wanted to mention two things. The
first thing is that uh actually when it
comes to a wafer fab like this uh having
a lock in in a process technology is
actually a big deal. uh you just it's
very difficult to uh you know swap out
because if you have a legacy of products
you just iterate on them and you figure
out all the yield issues all of that
stuff you know you have a good
relationship on both the design side and
on the wafer pricing when you can
promise large quantities of wafers and
so that tends to become uh a lock in an
emote actually uh if you can be the
dominant player and people it is hard to
come in as an alternative right the same
thing that happens to TSM MC's
awesomeness in digital circuits. So it
is no competitor really although there
are like you know a a second place is
like a far away second and the other
thing is that in the world of HBM when
you have three companies then they are
like trying to all get a growing piece
of the growing pie. you know, it is
actually possible because there are
things like a Jedex Jex spec that
determines what the the connectivity
speed should be. And so, as long as any
supplier can meet those electrical
specs, um, and then you can get enough
supply and pricing, uh, companies are
willing to swap out or derisk by having
multiple suppliers and putting them
against price constraints against each
other.
It is possible to do that but it's a lot
harder when it comes to foundry
technology because like I said moving is
a difficult process and so sometimes
companies do have parallel fabs running
but it's a lot of internal work to do
that so that is actually a benefit
&gt;&gt; sure
&gt;&gt; for tower
&gt;&gt; I think you're calling out the
difference too like it's not fair it's
not apples to apples to compare to
memory because those memory
manufacturers are vertically integrated
they are IDMs they're making the end
product and then selling and competing
on that product, the actual memory,
which is a bit commoditized in the sense
that there is a spec and they can all
show that they meet the spec. And so,
yeah, it would be more uh analogous to
look toward TSMC where it's just pure
foundry, not also making the product.
&gt;&gt; Yes. Yes. All right. Now, that's uh I
agree with you. I'm very bullish. What's
Well, let's talk about global
foundaries. I'll let you take this one.
&gt;&gt; Okay. Global Foundaries. So who is
competing with tower in the uh
fabrication of silicon photonics uh
chips? Global foundaries is trying to
play there. I think most people probably
have heard of global foundaries has a
long and interesting history. You can
read about I actually touched on some of
it in a Skywater post that I wrote. Um,
Global Foundaries is a sort of
foundation node uh foundry, meaning
they're not making the leading edge 2
nanometer chips. Um, they are uh the
third largest pure play foundry and they
have more business lines than just
photonix. They do traditional analog uh
RF, CMOS. Um, but they do have GF
Photonix spelled with an F. F O T O N IX
for listeners. GF photonix. And that is
the only 300 millimeter monolithic uh
cipho plus RFCOS platform. So you can
have photonics and electronics on a
single chip. And so why do they matter?
They are the alternative to tower for
silicon photonics trying to catch up.
They do have lots of big brands uh
partners Broadcom, Cisco, Nvidia, Marll
um and let's see what other notes do I
have. Um oh it interestingly the
government is sort of putting a claim on
them and championing them there. They
got a one and a half billion dollar
chips act money um for domestic silicon
photonics.
Um they also acquired uh AMF advanced
micro foundry in Singapore which was the
world's first specialty cipho foundry.
It was a 200 nanometer uh foundry with
plans to scale to 300 nanometers. So
that was a bit of a land grab.
&gt;&gt; I think you mean millimeters.
&gt;&gt; Uh
millimeters. What did I say?
&gt;&gt; Nanometers.
&gt;&gt; Oh nanometers. Yes, millimeters. 300
millimeters. Thank you.
&gt;&gt; Tiny teeny tiny wafers. [laughter]
Um now AMF's not huge 75 million in
revenue but um it is acquiring the
knowhow and acquiring fab space. Um let
what else? So you know I think the the
300 millimeter uh global foundry thing
is very interesting. tower uh is
predominantly 200 millimeter and as we
kind of talked about in our last podcast
you know this is a difference in the
size of the wafer obviously the bigger
the wafer the more chips you can get per
wafer and so you can bring the cost per
chip down um I think there was a quote
from the global foundaries earnings call
from the CEO that said we're scaling
silicon silicon photonics in Singapore
and the US including on a 300 millimeter
platform which again we think gives us a
lot of opport opportunity to grow the
business and differentiate going
forward. So again, this is just how they
can very quickly expand capacity, not
just by building new fabs, but by having
bigger wafers.
Um,
so let me let me pause there. I guess I
I don't know if I've talked too much
about risks, so let me hit on risks
quick actually. Um, risk. So when you're
investing, if you're an investor and
you're investing in global foundry, uh
silicon phetonics is only a small part
of their revenue today. So they have
other business units. Traditionally,
it's been smartphones, which is the the
smartphone business unit I think is
shrinking. Uh or the the the total
revenue is shrinking. Um another big
business of theirs was IoT, which I
believe is shrinking. Automotive is a
big one, and that one's growing. Um and
then of course, uh silicon fetonics data
centers is growing. So if you're
investing in global foundaries sort of
like as an umbrella parent company you
have some companies that are po or some
business units that are poised to grow
rapidly but then you also have some
business units that are a drag on
corporate margins and so that's kind of
what you're have to be aware of and this
is not unlike investing in you know say
uh even like fabulous chip companies
like AMD you're not just investing in
their instinct line you're investing in
their CPUs and in their embedded
business and gaming business and so on.
So it's just something to be aware of.
So let me pause there. What what's your
reaction to global foundaries as an
investor?
&gt;&gt; Um actually this is good. So now that
you have introduced global foundaries, I
wanted to now use this to quickly hit
upon the risk to tower semiconductor
because global foundaries is a pretty
big company like you you know what what
is it like uh as a third largest pure
play foundry right that's what so that's
behind TSMC and Samsung. This is a
pretty pretty big company and it was
actually uh IBM before it was like
became global foundaries. So um and
around 2007 or something not seven 17 I
think they decided they will not do
leading edge anymore and they'll just
stick to something like you know 12
nanometers and above make what are
called like essential semiconductors and
um focus there because the cost of
running uh advanced lithography machines
was like too much even for a found a
foundry of this size. So now this
actually poses a threat to tower in a
sense. The reason is this is a big
player. This is not uh somebody you can
just like trifle with because if they do
have a good technology and that is a big
if because from what I've heard from
people who work on this and again this
is totally anecdotal and it probably has
a lot of personal opinion signed into it
but is like people don't really seem to
like the photonix platform. They prefer
the tower semiconductor. Uh I think
there's a lot of things that play into
it. The PDKs and the tools that you
design with a lot of preferences exist
in the design world. So when you size
all that in uh it does it could po pose
a big problem for Tawa Semiconductor if
Global Foundaries does pick up a
significant portion of the silicon
photonics business. And the other big
difference I would say between global
foundaries and tower is that when they
integrate silicon onto their photonic uh
on their platform uh the the cipher
platform it is actually bonded
separately and it is still on a 200 mm
process. Now in global foundaries they
actually have a monolithic which means
that there's no bonding involved. They
they they make the CMOS after the
silicon photonics together and you get
them on 300 mm wafers which is actually
also cost effective and when you have
something monolithic which means you
don't have to bond it. It is a both
simpler and it gives you better uh
electrical or photonic performance
because there are fewer parasitics when
you have to like attach two things. The
monolithic is always preferable,
&gt;&gt; but that doesn't mean it's easy to do.
Like having a monolithically grown
process on basically 300 mm wafers isn't
an easy process. So that is a challenge
for what they have. So is so finally
okay what's the verdict then?
Considering that GF is actually um
gets some aid from the US government. I
think the you know they they did get
some chips act money. So there is a
benefit there that US government would
rather bet on um GF rather than towers
is Israeli presence. Um, I think that
I would still go with Tower over Global
Foundaries when it comes to Silicon
Photonics. Um, so
&gt;&gt; it's not like it's a bad buy, but
considering that Silicon Photonix is a
very small portion, I think right now
it's only like three or three to 5% of
global GF's overall revenue. And like
you were saying, it is fast growing, but
they have they have so much stuff like
mobile and IoT that is dragging their
revenues down right now. This has to
grow to a meaningful size of the pie
before it actually makes significant
sense to go and invest in.
&gt;&gt; Right. Right. Yeah. So if you're trying
to, you know, really invest in silicon
photonics, the the more pure play would
be tower,
&gt;&gt; I think. So yes,
&gt;&gt; totally. Totally. All right. So, let's
see. Let's So, we've talked substrates,
we've talked manufacturing. Let's go up
yet another level. Um, let's talk
lasers. So, Vic, the most popular name,
Lummentum or Light is the ticker that
everyone's tracking. Give Give me a
rundown.
&gt;&gt; Yeah, I I get all the easy ones. I get
all the bulls. You get all the bears.
[laughter]
Everybody loves momentum. I mean, what's
not to love about it? the stock price
has crossed like $750
uh from I don't know $300 just a few
months ago. Uh it's like uh everybody's
favorite right now because they are the
dominant maker of laser components for
optical communications, right? And that
that's because they make these things
called um externally modulated lasers
which goes into every transceiver you
can think of whether it's 800 gig or 1.6
1.6 60 and uh so they they have a lion
share of the market. They I think they
have like a good 50 60% share of the EML
uh market and their demand is so high
that it like outpaces their supply by
about 30% according to their last
earnings call. So everybody wants these
things, right? There's and not only that
they they have uh a growing demand for
their optical circuit switches which are
purely MEMS based
&gt;&gt; that had absolutely zero backlog. Um and
now there's like in the last earnings
call there was like a 400 million
backlog on that. So it's like a market
that didn't even exist but now OCS has
become a thing for momentum and they are
in the driver's seat on OCS. So that
puts them in a very strong
position and in addition to that they
have a very good um ultra high power
laser for uh co-ackaged optics because
you need you need lasers that are like
significantly more power than you would
use in like externally modulated lasers
because the laser is going to be present
external to the rack like we spoke about
in the last episode and then the
modulation happens on the SCIO chip. So
you need like reasonably high power in
order for the light to make it well into
the chip and so you can modulate it or
what what not. So they have all these
technologies. They have EML, they have
uh CPO lasers, they also have OCS that
is like literally growing rapidly and
their um revenue growth has been short
of nothing short of exceptional really.
And they say that their 200 gig EMLs
for 1.6 Ct transceivers was about 5% of
the revenue in late 2025. But it is
expected to reach 25%
of their revenue by 2026 because you it
is significantly higher ASP and margins
for a 200 gig EML compared to a 100 gig
EML and
their performance of the EML is is
unmatched as well. Uh the it is so much
so that the next company we we're going
to talk about that also makes EMLs is
actually buying from Lumenum their EMLs
which is like weird. You're making your
own EMLs. Why would you buy from
Lumenum? You know those EMLs? It tells
you something about how good that is. So
they have a very good technology
and
I think the fundamental you know we've
gone on like long enough about why it's
so amazing and all that but really this
is something I've been looking at longer
term too as an writing an article about
because
um really at it's like 700 like when you
see the uh street estimates for the
stock price you know I even see
something as high as 900 okay like this
is a really high like Would anybody
invest in this thing at this price? Is
this something that is still
&gt;&gt; is there still room for this thing to
grow? I mean, yeah, there's a lot of
demand and all of this stuff, but what
is the fundamental mode that this
company has? And why should anybody, you
know, get into this at this price? So,
fundamentally, I think that their
knowhow about how to make a laser is
very good because it comes from the
epitaxi behind making these crystal
structures. uh to engineer these lasers
and that is very important to do and
that is not very easy. It's it's a good
mo that you know it's very hard to get
along you know get out of. So that is
one of their big big uh knowhows that is
like really good that they can do this.
But the risks I would say is that
uh if there's any kind of slowdown in
the AI capex that's going to hit them
very hard because they're all like
entirely AI dominated really this entire
thing. they don't have like other it's a
pure play laser thing really all of that
data center stuff is
for AI you know so that's a big problem
and then there's the other con
constraint is that if their competitor
comes in with a cheaper laser which is
entirely possible then they're going to
get seriously undercut because they're
still making the lasers on 3-in wafers.
So, if somebody comes in with a 6-in
wafers producing, you know, four times
as many laser chips per wafer, that's
going to drive the prices of these like
much wanted, highly backed up, high in
demand lasers down. So, at these prices,
as much as I would like to say by
Lumenum,
I don't know. Oh, I don't want to poison
you. Sorry. You're supposed to tell me
that. I didn't say that. Take it back.
[laughter]
&gt;&gt; Okay. Okay. Uh yeah. Well, I mean it
sounds like the company is very
technically adept, has good R&amp;D, and is
just crushing it. Um obviously it sounds
like a timing thing, and you know, a
year ago would have been a no-brainer.
Now I I do hear what you're saying which
is like okay are you going from like
this thing doubles annually to this
thing goes up 20% or or probably
actually just like tracks tracks the
capex growth broadly you know like oh if
capex is growing 50% or 20% from the
major players does that just mean like
okay momentum is going to grow 50 or 20%
or whatever they're going to have more
competition yeah there could be pricing
uh you know uh competition as well to
deal with. So it does feel like a
awesome company and now doesn't feel
like the right time.
&gt;&gt; Yeah, it seems that way though but you
know people have been proven wrong on
this SanDisk and Micron stocks in the
past.
Th that is a great analogy, right? Where
like you could have every month for the
past six months, you could have said,
"Oh, memory way overpriced. Now is not
the time." And it keeps going up.
&gt;&gt; So, I don't know. Hard call. Hard call.
Company has a really strong fundamental
basis for why you should invest though.
Their fundamental thesis is very strong.
&gt;&gt; There you go. All right. Let me talk
coherent.
&gt;&gt; The competitor
&gt;&gt; um
&gt;&gt; their competitor. Okay. So, Coherent I
think it's roughly the same market cap
around 50 billion or so. Um, they are a
broad photonix company. They make
everything from um indium phosphide and
gallium arsenide substrates to laser
chips to complete transceiver modules.
Um, but they also have other business
units, silicon carbide for EVs and
industrial lasers. Um, and by the way, I
listened to a
what was it? Maybe it was like a analyst
day or something. This like two-hour
presentation from Coherent and uh their
their CTO, Julie Sheridan Ing, I believe
her name was. Um, she did a really good
job. It's really worth the listen.
Julie, if you ever happen to listen to
this podcast and hear this, we'd love to
talk to you. I thought it was very
educational. I thought she was cool. Um,
so, okay, back to Coherent. Um, so they
matter because they're fully vertically
integrated from substrate all the way up
to module. They do have three different
onet transceiver approaches. So they
don't have all their eggs in one basket.
They've got ESML or sorry EML,
electroabsorption modulated lasers.
They've got silicon photonic, cipho, and
vixel uh vertical cavity surface
emitting lasers. And um so these all
have different pros and cons and they
make all of them. um as you've talked
about their moat could end up being uh 6
inch indium phosphide fabs. So making
again maybe more than 4x devices per
wafer than a 3-in u maybe only 60% of
the or like 40% of the die cost
potentially. Um
and so you know as you said just
essentially flooding the market if if
the performance is good enough they in
some respects they can sort of flood the
market with capacity with chips um from
their earnings call you know why they
said they'll win they said they have
huge demand visibility for the next
several years they they use the term
book to bill is above 4x so I think
that'd be like for you know every 25
chips they sell today they've got a
backlog of a 100 chips that are just
waiting to be fulfilled. Um their three
different onet approaches capture demand
across all link distances. So you know
they're trying to you know be positioned
for scale up scale out you know they can
they want to be able to handle it all.
Um obviously risks uh Lum is a very
strong competitor. Lumenum has better
operating margins. Um there kind of like
we talked about when we're talking about
tower versus global foundaries. This is
kind of like the global foundaries uh
analogy where there are several b
business units and the others could be a
drag on overall corporate margins. Um
and I do think that they're also priced
pretty uh premium. I think that uh
they're trading above or right at most
analyst targets. And then uh you know
maybe a talking point like you said we
could get into this is they do buy EMLs
from Lummentum. Um so there's some
interesting questions. It reminds me of
Intel um you know manufacturing some CPU
dies at TSMC as they're trying to get
their foundry going. And so when you
when you see that coherence buying EMLs
from Momentum you know you just have to
pause and dig in and ask oh like what's
the strategy behind that? Um, on the
other hand, they are securing
exceptionally large CPO purchase orders.
So, they're positioned for oncoming
inflections. Um, I think their CEO said
something on the earnings call like, "We
secured an exceptionally large purchase
order for our co- package, Optic
Silicons. We believe scaleup CPO will
dwarf scale out and be orders of
magnitude larger." So, I I think they're
trying to say there is a huge incoming
inflection. We're going to be really
well poised for that even if we're a
little bit behind today. Um, so I'll
pause there. What do you think, Vic?
What's your reaction? So, I like
Coherent for one reason, and that is
that they grow their own indium
phosphite substrates. Think about that
for a minute. because you know AXT is
subject to China's export controls
&gt;&gt; which Lummentum then needs to make their
uh lasers but coherent is so vertically
integrated that they grow their own
substrates they make their chips they
assemble the complete module if they
have to and they have everything under
their belt like they have EML they have
cipher they even have these vixels which
Lumenum doesn't have of course people
argue that vixels So they own their own
&gt;&gt; Yeah.
&gt;&gt; own their own destiny. Sorry to
interrupt but it sounds like you know
coherent is like they own their own
destiny not dependent on things outside
of their control like geopolitics not as
much
&gt;&gt; for for the Indian phosphide wafer
itself that's a big deal because you are
the the entire momentum like growth
strategy relies on getting
wafers which are subject to China export
controls which is one big
&gt;&gt; site that coherent does not have. So
geopolitics might work in coherence's
favor here because of this this fact.
And secondly, yeah, there are parts of
this that are dragging it down. But
&gt;&gt; I don't see 6-in wafer yields uh as a
fundamental physics limitation. I think
it's an engineering limitation. And this
problem has been solved over the years
in silicon cuz silicon was also at 6 in
at one point. it went to 8 in it's in 12
in now so uh we we can see that like the
Indian phospide industry and laser
technologies are transitioning from 3 to
4 to 6 in so it is uh you know there are
some problems associated I'm actually
currently looking into why it is so
difficult to make a 6 in wafers and what
are the yield problems it's some it
comes from having to evenly deposit over
a larger area and things like that but
again those are engineering problems and
they are eventually solvable actually I
think they said that uh I have it
written here somewhere they said that at
the end of the year 2026 50% of their
internal capacity will be 6 in so
capacity doesn't mean good lasers okay
it means that they are
&gt;&gt; making lasers okay and half of them work
oh no no not half of them work maybe
most of them work but like half the
capacity is from 6
I don't know if the laser is actually
competitive or not, but that's a
different question. So purely from the
point of wafer supply and
having 6 in that in my mind will
eventually work. The question is when
and when that comes in what is lentum's
position to defend it.
&gt;&gt; So I actually like coherent from a
certain fundamental point of view even
though all the attention is on lumenum
right now. Uh, coherent is a good good
is a good solid foundation if you ask
me.
&gt;&gt; Nice. Nice.
&gt;&gt; So, I'd be in.
&gt;&gt; Cool. He Vixen
&gt;&gt; um
I love it. Okay. Uh Fabinet, let's talk
Fabernet next. So, this is back into the
manufacturing space, but it's not a
foundry. te tell us more about what they
do and why they are part of the optics
supply chain.
&gt;&gt; Yeah, so this is uh like on the other
side of the the manufacturing of the
laser chip for example. So you know how
to was like they take the design and
they manufacture the chip uh in in a
foundry and they make all these micro
structures that make the actual silicon
photonics chip. A fabinet is on the
other side of it. So once the chip is
like made, they don't even do the
design. They don't do the chip
fabrication. So when you when all the
pieces are there together, right? They
take them all together and build they
build the transceiver and they package
the lasers. They do that kind of
assembly stuff. It's like a contract
manufacturer.
&gt;&gt; And the nice thing is that they're a
pure play manufacturer. And this is why
uh many like companies who do optics or
even uh big chip companies like Nvidia
trust uh Fabinet because they don't
compete in this space at all. All they
do is they manufacture this stuff and
you know make it ready to go.
&gt;&gt; Let me ask you a question. Would this is
is advanced packaging or like OSATs is
that kind of an analogy here from what
people are used to in logic? Yeah, I
think that's a good one. I think this is
like somehow the OSAT of the optical
world and it is a difficult space and
they have been around a long time. This
is not a new company. They have been
around like a good 25 years I would say
and they have a lot of experience in
like advanced high-speed optics which is
a difficult thing to get into for
somebody who has not been doing it for
all these years. So they are a precision
uh optics manufacturer that works by
contract. They don't design anything but
they make optical assemblies for
everybody. And they've been they're a
Thailand based I think they are based in
Thailand or at least they have their
major manufacturing in Thailand. I don't
know where they I think I remember
reading here.
&gt;&gt; I think they are based in the Cayman
Islands. Yes, they're headquartered in
the Cayman Islands which was like what?
And then all the manufacturing is
Thailand actually. Um and they haven't
&gt;&gt; Okay, interesting. So, I wonder where
their executives sit. [laughter]
&gt;&gt; Sounds I don't know. Sounds shady. Why
are you in the Cayman Islands? Uh, no,
I'm just joking. I'm sure it's perfectly
legitimate operation.
&gt;&gt; Uh, but yeah, so their one
uh major uh advantage is that they have
this really good net margin compared to
their competitor Jel who also assembles
these things. They are not uh they make
a lot more net margin than their
competitors and basically they're really
solid company in the the OSAC world of
optics and um
the risks are though
&gt;&gt; they do lidar too.
&gt;&gt; Oh yeah yeah yeah they do LAR. Yeah
interesting. Yeah like there are other
parts of the optical world that fabinet
deals in which is which is cool.
&gt;&gt; Yeah yeah sorry car. Yeah. No, that's
that's a good one because but the the
major risk is that they are the ones who
put all the optic stuff into Nvidia,
Spectrum X and uh what is the other one?
Quantum X. Uh yeah.
&gt;&gt; Mhm.
&gt;&gt; So all the photonics that went into
those network switches were all
fabricate. So Nvidia is a massive
customer concentration for them. Um but
you know like like everything if they
don't have enough EML lasers from Lum or
Coherent what what are they going to
manufacture? Because you're basically
downstream in the supply chain. If you
don't have enough wafers if you don't
have enough lasers you you're going to
be short of manufacturing, right?
&gt;&gt; So it's like really it's a it's at the
mercy of all the customers decisions and
what happens upstream in the supply
chain.
&gt;&gt; Sure. So, they're a good assembly.
They're a good assembly house, I would
say.
&gt;&gt; Uh, but yeah. What do you think?
&gt;&gt; I mean, it sounds like a solid
investment. I wouldn't expect just off
the cuff, I wouldn't expect like, you
know, this is a tanagger, right? But if
you're like, "Oh, I need a place." Let's
say your thesis is maybe some of the big
logic companies are sort of just like
tapped out and you want to invest
somewhere else. This feels like
something that's more along the lines of
TSMC where you're like, "Yeah, this is
going to grow." Might be, I don't know,
tens of percentages a year in a good
year, but it feels like essentially a
safe bet, but that still has upside,
especially if you believe in the in in
in optics in the data center and if you
believe in LAR optics, like let's say in
personal vehicles. Um, so probably some
different angles that you'd be investing
in. Of course. I'm sure you'd have to
read about if they have other Do they do
you know they have other business units?
&gt;&gt; Um Fabinet.
&gt;&gt; Yeah. Or is it pretty much just optics?
&gt;&gt; Their their specialty is optics. Uh but
they they do have nonoptical
communication parts as well.
&gt;&gt; Um
but it's like of let's say about a
fourth of the company. They do some
industrial lasers. They do some
automotive stuff. I think that's where
the LA comes in. Um
&gt;&gt; yes yes yes yes that makes sense.
&gt;&gt; I also have in my notes here that they
do some high performance computing.
That's interesting though. I never read
about that part earlier.
&gt;&gt; Oh interesting.
&gt;&gt; Oh wait I also have it here that it's um
&gt;&gt; yeah uh no that's very interesting
actually. It says yeah it might be a
wild card here. I have to look into why
they're doing high performance
computing. That's interesting though.
But no bulk of their money comes from
three4s of it comes from optical
communications. So that's their
stronghold.
&gt;&gt; Yeah. Nice. Nice. Nice, huh? Sounds I
mean if I was trying to decide where to
invest, this would be compelling as a as
a good solid investment. Also, uh maybe
we should go to Thailand and like take a
tour of their facilities.
&gt;&gt; Love to go to the Cayman Islands, too,
just to see their headquarters.
&gt;&gt; Hey, there you go. I don't even know
where those are. [laughter]
&gt;&gt; We go map it after this.
&gt;&gt; But yeah, my geography is not great.
&gt;&gt; All right, let's move on to the last one
because this one is this episode is
already getting long enough. So the last
one is uh actually a very old company.
It's been around like a hundred years
now. And it's amazing that we're still
talking about investing in this thing
which tells you imagine the bulls of
this company that were like a 100 years
ago. They had no idea that all of this
is going to end up in like optics and
data centers. But yeah, what we're going
to talk about coning coning glassware.
Uh what do you think about that? I don't
know. Maybe you want to introduce this
one.
&gt;&gt; Yeah, sure. Corning glassware. So I have
actually been to Corning, New York and
toured their facilities, not like as an
industry insider but just as a tourist.
So the parts of their, you know, museum
essentially that they let you see. But I
had a friend in college um who his folks
he's from that area kind of the
Fingerlakes area in New York. And so I
actually went and saw it and just you
know amazing. It's so fun to understand
the material science and all the
engineering um the optics and everything
behind how do you manufacture you know
these tiny strands of glass and send
light down it. Uh it super interesting.
Um so they are the dominant optical
fiber cable and connectivity company.
And so of course when we're talking
about scale out in when we're talking
about CPO and even scale up going to
optical that implies that there's fibers
connecting everything. Optical fibers
connecting everything. And of course uh
like you know you might go back to like
the 90s buildout and bust and you might
think Google fiber it's it's those
fibers but right right now obviously the
opportunity is just connecting all those
GPUs in data centers as fast as
companies can stand them up you need to
connect them. Um so every transceiver
that we've talked about needs Corning
fiber on both ends. AI data centers need
10 to almost 40x more fiber than the
traditional cloud, which is super
interesting. Um, of course, when you're
thinking about uh training runs, GPU
training runs, and you're talking about
hundreds of thousands or even with
trainium and project rainer, like a
million uh tranium 3 all connected
together, all talking that is a ton of
fiber and that is definitely very
different than than more of your
distributed cloud for just like, you
know, API serving APIs or something. Um,
so more transceivers means more corning
and the moat is kind of like with a lot
of companies we talked about like this
is deep tech. This is interesting like
materials science and fabrication and
process. So you know glass science and
fiber manufacturing knowhow built out
over decades. Um they recently t locked
in a $6 billion multi-year deal with
meta for llama for training cluster
connectivity. Um, and what else? They're
partnering with Global Foundaries on
fiber to chip connectors for CPO. So,
they're trying to go ahead and and be
very well positioned when CPO takes off,
they're going to be there. Um, I think
like with any company that has existed
for a while and has a business unit
that's in the right place in the right
time, you know, they're they're probably
all their upside is here from AI and
they're probably going to be priced for
the AI fiber buildout buildout, but of
course optical only a portion of the
revenue. I think about 40% and the rest
is other display glass. Yeah. Another
reason you might have heard of Corning
was like Gorilla Glass, you know, when
iPhones when we went from Blackberry to
iPhones having glass on them. And so,
you know, Corning plays in these spaces,
display glass, auto, life sciences,
those are not going to take off in this,
at least not right now, in the same way
that AI is. Um, so you know, you just
have to think about how is this umbrella
business priced and I'm really excited
in one business unit. uh how do I think
I should model that out? Um so let me
see any other risks.
Uh I mean obviously if there were to be
a slowdown in hyperscaler capex that
kind of
it directly would squaltch the upside
for Corning but I think I personally
don't foresee any slowdown. you might
see a deceleration over time, but but
clearly we're talking hundreds of
billions of dollars every year going
forward. Um, so with that, uh, what do
you think, Vic? Would you invest in a
glassware company?
&gt;&gt; Yeah, I would. But I have a couple of
caveats here. First of all, I like that
they have a a 100redyear mode in making
glass. I mean, about that's about as
good as MOEs get. They've been doing
this a 100red years. They know how to
make glass, you know. That's a strong a
strong statement and they you know the
$6 billion deal is a big thing because
it gives a lot of visibility uh into how
hyperscalers like Meta would want to
lock up fiber supply for the rest of the
decade. So it shows you that there is a
significant importance to this. Uh but
it it is a good business to invest in.
The only thing that would make it not
attractive so all of a sudden is if this
whole optics build out uh gets pushed
out or peters out for whatever reason
and
or hyperscalers decide copper is not yet
dead why don't we still continue with
copper why does everything have to go to
CPO maybe it's not required maybe we
just stick with copper as much as we can
um and optics only when we must you know
and when that happens uh then why do we
need all this fiber? We don't. It'll be
the demand will be significantly lower,
&gt;&gt; right?
Yeah. And so I I really think it's it's
a timing thing as all of these companies
are, which is like okay, the scale up
TAM for these optics companies is huge
and net new for them and and scale out
is always going to be optics at certain
distances, but that's pretty well known
today. And so if it's not like oh scale
up in optics actually isn't a 2027 2028
story but it's more like a 2030 or 2031
story then obviously you'd be investing
in a company and it wouldn't be
inflecting like you thought now and your
money would just sit for a long time
until it hits that curve.
&gt;&gt; Yes. Exactly. So if if if we are not in
the CPO mode immediately although it
seems like we're getting close uh I
don't know if we really know when CPO
for scale up is coming or optics for
scale up is coming. We don't really
know. So if we don't really know I don't
know how we can also model how much
demand for glass fiber there's going to
be and therefore and there in lies the
risk you know.
&gt;&gt; Yep. Yep. Yeah. It just depends on who
you ask. If it's people that are in the
copper TAM, they're going to say not
now. And if it's people that are in the
optical scale up TAM, they're going to
say 2027, 2028. Right. So, it's that's
the that's the question that people can
go dig in further, too. It's like when
when do they believe the timing is?
&gt;&gt; Yeah. Yeah.
&gt;&gt; This is cool. So, I think we shouldn't
get in any more than this. We've been at
this almost an hour now. So, uh this is
this is good for
&gt;&gt; the longest podcast.
&gt;&gt; Yeah. Totally. I hope you all listeners,
I hope you liked it. That's it for
today. Thanks for listening. If you're
enjoying semi-doped, uh we love who
gives a five star rating and a quick
review on Apple Podcast and Spotify. Um
thank you to all of our YouTube
listeners. We're seeing thousands of you
which is really cool. Subscribe,
comment, whatever. We read it all. So,
thank you in advance and we will catch
you next time.
