---
source: https://www.youtube.com/watch?v=LC92F0nUOV0
vid: LC92F0nUOV0
title: Product execution mock interview: falling metrics (w/ Amazon PM)
date: 2021-03-25
duration_sec: 1595
channel: RocketBlocks
kind: transcript
---
hello everyone kenton covestro from the
rocketblocks team here
in this mock interview video we're
sitting down with jesse lau who's a
senior product manager
at amazon focused on the kindle product
and in this particular interview we're
going to be doing a product execution
question
focused on the popular grocery delivery
app instacart and they're
seeing a decline in one of their core
metrics so let's go ahead and jump in
and see how jesse walks through this
okay so let's imagine you are a product
manager working on
instacart the grocery delivery app and
uh you walk in one day and your manager
pulls you aside and says hey
uh order deliveries uh you know the
number of orders placed
on a day-to-day basis is down four
percent
week over week from where it was last
week
and we don't know what's going on we
need you to help us figure it out so my
question to you is
how would you figure out what's going on
and sort of walk me through that process
and you know feel free to ask any
clarifying questions or
you know um ask for more info if you
need it
yeah so the first thing i would do is
ask
um is this a real problem or a not real
problem
is more what do you mean by that yeah or
not
yeah like is the is is is four percent
a normal fluctuation that you might see
week over week
especially if it if it fits inside of a
of a normally understandable seasonal
pattern
so shopping goes up before thanksgiving
and and things like that so if last week
was thanksgiving for instance
then perhaps this week is down because
last week was was normally high good
point so you're basically like is this
normal or
is there like a really high comp the
week before that makes this look like
we're down but we're just going we're
just reverting to the meat
yeah yeah fair question so the normal
sort of
week to week fluctuation is about
one percent one and a half percent so
four percent does seem high
which is why it caught caught our
attention
uh and then to your question about you
know
is this a high comp issue like it was
thanksgiving last week or something like
that that spiked orders up
that is not the case it you know we're
mid-june so it doesn't seem like there's
sort of any obvious
um you know reason why it would have
spiked up last week
got it got it okay so so it is
it is a it is a real problem so okay
let's go work on it you know one of the
things i
i've um we do i've done in my past
is um we will set up predictive alarms
against some of our metrics
so they'll actually you know um they'll
notice when there is higher variability
in our data
over time and the alarms will expand
their allowable range of variance in
those periods
so it's good to know that this is this
would have triggered that alarm
okay cool um the so the second thing i
want to know then is
um what's the geography we're talking
about here so i presume we're primarily
focused on the us
yeah so fair point so uh right now we're
100 operating in u.s markets so you're
dealing with just
uh your one country um and
happy to answer any sort of other
geography questions you have beyond that
too
yeah i'm curious um is that four percent
consistent across the us or do we see
variants
um in different regions um so good
question
um one question back for you is like
what type of cuts would you want to see
or you know if you if you could sort of
make wave your magic wand like how would
you want to grab
uh yeah to answer your own question
there
um you know i'm not exactly certain yet
but i mean typical cuts i might make in
it at a time like this where i'm just
initiating an investigation would be
you know one would be geographical yeah
um
in terms of regions right that's what i
was asking you just cut it by some
regions
yeah i mean that's one way another way i
would think about is urban versus
suburban versus rural
um and then i don't know like if i knew
this industry better i might
um instead of cutting by region i might
cut by like
um who our key partners are
right like okay so i don't know partners
yeah like if albert if there was some if
we had some change in our relationship
with albertsons or something like that
that might
yeah yeah okay so that's that's fair so
those are three interesting ways to cut
it i can
i can go retrieve that data for you um
the first one which was geographic
regions uh
so we've returned basically western us
the midwest the northeast and the
southeast
uh and it does look like the four
percent is basically down across the
board i guess
it's down across like 3.8 and the west
and 4.5 in the northeast whatever it's
like are
all around the same hovering around that
same four percent
okay um the second uh cut that you
mentioned
around rural urban same thing there
there there's a little bit of variance
um but we're not seeing that like rural
is up and urban is down
or anything like that they're both sort
of down around four percent
okay and then the last one you mentioned
a similar story there like if you cut it
by
grocery partner uh which is an
interesting idea we don't see any
you know there's no like obvious smoking
gun that like hey
uh albertson's fusion example is you
know falling off a cliff for some reason
got it so it feels pretty evenly
dispersed
across the country yeah um what about
what about competition have um have
any has anything changed in the
competitive landscape yep
oh good question so in terms of major
stuff happening
in the marketplace right now i mean uh
this is not new but so
for the last couple of years instacart
has been competing against amazon
and amazon's line of grocery delivery
stuff which i think is called
amazon fresh and you know that's like
evolved and changed a little bit over
the years but nothing
to our knowledge has changed in the last
week with that
uh we haven't seen anything there there
have been some rumblings like if you you
know read like tech crunch that type of
stuff that that uber
is considering getting into grocery
delivery uh in a bigger business
obviously they they operate in this
tangential space with ubereats you know
there are some polarities there um and
clearly they know a little bit about
logistics but
there's no um you know as far as we know
they're
they don't have any material presence
they're not actually testing it it's
just sort of like
brokers um at this point interesting
i'm um to know if there's any way that
i'm just thinking out loud here but i'm
curious to know if there's any way that
though just rumblings about uber could
have driven some sort of impact um
sorry it seems like you have something
you're going to say go ahead yeah i mean
i think
um hard to know for sure from
from my perspective i mean certainly you
know consumers might have heard
something
my i guess is it seems unlikely
um but yeah i have a specific idea of
how that
that might translate into something like
this i'd be curious to hear it for sure
oh i don't think this is a very good
idea but i'll i'll share it is
you know i've known
uh uber to be pretty competitive
so i could envision a world where they
might
um especially competitive on the on the
on the supply side
so i could i mean this seems almost
nonsensical to me or certainly not a not
a sustainable business strategy but
i could i could imagine them starting to
hire
uh delivery people um in in preparation
for a launch or something like that but
i couldn't imagine that that would
lead to such a large impact on this that
is that is interesting and so take me to
like
if if uber were doing that or
some other competitor out there was
doing the same thing
what's the logical chain of how that
would uh affect
the overall sort of decline in orders
we're seeing
yeah for sure i mean i think that what
would happen is
um your uh our delivery windows
would um either uh shrink
or um they would
they would shrink or they would get
further out and so
as a customer i mean this has happened
to me several times in the last
um uh with with with amazon in the last
uh
year where during moments of what feel
like more of
like a crisis um the delivery windows
become less and less available
and in that case i presume it's because
the orders are up
but um but in general if there's less
labor supply
um from from instacart to go pick the
groceries and bring them by
then that becomes a less interesting
option for me as a customer and i
probably get somewhere else to order it
just do it
okay interesting that is that is a fair
point um
so um i could see that happening
and i know you're talking about
certainly in periods of spike demand
those delivery windows increase but the
the sort of logic of like hey if our
if our essentially drivers and
shopper agents were getting poached and
then the delivery times
um you know spiked up uh
i could see you know losers bulking and
basically not placing orders so that's
interesting um let me ask you this like
if you wanted to try and prove or
disprove
uh whether that was going on and again
you can wave your back
on and pull some data what type of data
would you want to see whether
that hypothesis holds holds water
um so i think let me think about this
for a second
i'll just go ahead and think out loud um
so
i suppose one thing we could we could
look at is
um the whether the gap
for for those who did submit orders
whether the gap
in time order is placed until time
delivery is made
um has increased okay um
i think we could also look at um in the
in the in the click streams data i
imagine we could look at
um at the point of purchase when you're
told when your delivery window is
if if we're seeing extra drop off there
or somewhere else
okay um so those are the two ideas that
pop off the top of my stuff
okay you want to look at essentially the
first thing you mentioned was
average delivery like how long does it
take to get the delivery
yeah the second thing you want to look
at is
are we seeing a bigger drop-off from
when you first see the window to
to placing an order then we typically
say
um okay sounds good so um we can look
those both up
uh average delivery time is
um on par no no material changes that
that seem outside of um regular standard
deviation
uh and some similar with the drop-off
rate we're not seeing like a spike in
drop-off rates so it doesn't sound
like um it doesn't seem like that might
be the case
yeah this it didn't feel like a
super strong hypothesis to me but um
since you brought up the uber
um the uber thing i i wanted to i wanted
to check in on it
you know i wonder if
um this might be uh potentially a
self-inflicted wound
where we've um or we've done some we've
changed something about our either our
recommendation or sorting algorithms for
shoppers
that um they're not they're just
purchasing their average card is less
than it was
um before okay um so what um
what information would you like to know
or sort of
what's um
yeah what's what would you i guess ask
your fellow pms or
what type of information would you try
and gather there yeah i mean the easiest
thing would be to look and see if there
were any
um any a b tests run or changes made
to um to the shopping uh
to the shopping site to
um that that may have had a negative
impact
got it um yeah makes sense so
um i can retrieve some of that info for
you here
uh essentially um there are three
main experiments running right now i
like the experiments going on
uh the first is there's an experiment
that um
you're playing around with the logic
that the plays
displays the suggested items
that show up on the home screen of the
app when you're in order so when you log
into instacart
uh as a as a user instacart will suggest
items that you've purchased in the past
to put to put back in your cart this
time yeah
and this experiment is essentially
changing the logic of
how those suggestions work yeah that's
the first thing
uh the second thing that your teammates
mention is there's
another experiment going on where some
users uh
this 30 of users are receiving new push
notifications
which are alerting them about deals
happening
in their local area for the grocery
stores that are supported on instacart
so for example this would be like
you know if if i actually don't know if
albertsons is in seattle but like
uh if albertsons were having a special
instacart might notice
you as an instant notify you as an
instagram customer like hey
you know if you shop at albertsons this
week you'll get 10 off all your
stuff okay can i can i can i
dive into that one uh really quickly and
then i i do want to get back to the
third one but i want to ask a couple of
questions on that one
um so this is a new push notification
strategy that didn't exist before
correct entirely new we didn't do this
in the past okay
and then um and then the
um and and what those push notifications
do is they alert customers to
specific deals in their local area yeah
okay um i have one other follow-up
question on the prompt
to make sure i didn't misunderstand the
prompt at the beginning yeah
we said orders are down four percent do
we mean
the like average order size or do we
mean the total amount of orders
that's a good question we mean the total
amount of orders okay
because um my initial instinct was if
we're push notifying
on on discounted deals um maybe we're
having
more more and more orders but the
average ticket on those orders is lower
but it sounds like that's not the case
so that's a good question and good
clarification the four percent down is
definitely on the absolute number of
orders placed not the average order size
got it great okay thank you yep um
and and the third experiment running is
that there is an
update to essentially the color palette
that's been used
and the layout of the um
two parts of the checkout flow basically
the checkout overall and the part that
comes right before the checkout which is
when the user
has selected the items that they want in
their cart
and they go to check out there's a
screen right before that that basically
says you know
if this order is or sorry if this good
is not there how do you want you want us
to just not deliver it or you want us to
replace it with something else there's
basically this ui that lets
people make a decision so the color
palette and the layout
of those screens has been adjusted to
match
um some redesign that happened to the
general instacart
app about three months ago but this was
done last it was sort of
the last video got it got it
okay well um i will
um so taking those i'm gonna i'm gonna
break those down into four parts
okay i recognize that the color and
layout are
one and the same but i'm going to split
those two things apart
okay and and say that my so i'm going to
go ahead and say that my hypothesis
is that the the two most important
things for us to dig into here
are the logic of suggested items okay
and and the layout of the checkout flow
okay
and why do you say those two things out
of the four that i mentioned
you know i mean it's it's it's well
established now
that um that the algorithmic
recommendations work
and home page is a good place to put
algorithmic recommendations
so my instinct is very very small
changes
on um on algorithms uh recommending what
you buy
when you open an app could have really
big impacts on our business
so that's that's the one i would
investigate really deeply
i would guess whoever made that change
is watching that closely i would hope
so um and then on the layout i think you
know the color i think is a
is a uh is important and it is
you know we've i've worked in places
where i've made a button blue and made
more money because of it so
i know that that's that can happen um
it's just less likely than a layout
change
and i could envision a world here where
like um a layout change
on especially on the replace item flow
is has
has um has changed in such a way that
previously
we were getting like lots of
replacements and now
the the decision is um that instead of
getting a replacement we're just you
know removing an item from an order
um which which could have had a negative
impact
um i'll give an example for me
personally actually pretty recently in
this exact experience
is um for a long time um
when i ordered on amazon um they would
recommend a replacement only if there
was a close replacement
okay and so like i guess i never
remember which one's type one and which
one's type two error
but i might they would default to a
smaller cart because
you know if they couldn't find something
that was pretty close
they would get rid of it the last time i
ordered and there wasn't a replacement
they just like the shopper just threw
some random thing in there
that um had was nothing like what i
wanted and so i had to actively go in
and say like no thank you i do not want
that
yeah and so they just there they have an
error of inclusion rather an error of
exclusion
and i could i'd be pretty concerned
about that potentially happening over
here as well
and so your hypothesis there is just to
make sure i understand
you're saying that that behavior of like
then getting the wrong items
might frustrate people and they might
just place less orders
in the future and that would that would
lead to the ordering decrease that we're
seeing or
am i misunderstood um
it is uh either
like i i'm i'm yeah so i
am thank you for clarifying i am
considering i suppose two things like
one
is that that that that would
throw off a customer they may not want
to place an order in the future that
could certainly happen
another could just be as simple as
layout change
especially i mean adding the color
change to it would exacerbate this
it's just it's just unfamiliar for the
customer and there may even just be
you know it's not that hard to engender
like a one or two percentage points of
mistakes of people accidentally
canceling orders and that would from my
perspective like
i've had experiences where i've put like
37 items into a cart
and then the them not get purchased and
i'm like forget it i'm just going to the
store
yeah so um i could i could also see that
happening
okay cool um well let's so thank you for
clarifying why you sort of highlighted
those
two things out of the the four as you
sort of broke it down
um starting at sort of the the top of
those uh the first one was you talk
about sort of the algorithmic changes on
the logic there
um if you you could you know grab
the pm that's running that experiment
what would you want to ask
kim or her to see if it feels like maybe
that's having an impact or what
oh i would hope that they ran an ap test
and i would hope i could look at the
results of their a b test
okay um you know yeah got it so they did
run
an a b test um and they did look
at uh you know for the the folks in the
new variant
um how many of those sort of suggested
items did they end up placing into their
cart
first you know how many on average
versus the the old variant
and what was the average cart size
versus the old
cart size and what was the average
likelihood of
opening the app to placing an order so
it was the drop-off for folks in both
variants
and they found that um basically across
the board they saw about a one to two
percent
increase in those metrics so about one
percent
to two percent more items from the
suggested list were getting added
um slightly higher performance of
actually
completing the actual order and slightly
higher order value
great so now we've got to find like
negative six percent on sales loss
um well good well let's dial that one up
and then we won't
we won't uh we will be down to just
negative one i suppose
okay um okay yeah let's let's let's keep
going maybe jump to three and then
we can if three doesn't feel like the
um the right one then we can go back to
push notifications
cool um so we'll skip push notifications
on the third
um you know again just if you could wave
your magic wand what type of metrics and
there there is an a b test running on
this but what type of metrics would you
ideally want to see
for this third experiment about yeah
changes
yeah i mean you know i think
in commerce my experience is
it's super important to always
measure the purchase
um if you can right like get to as close
to measuring the purchase as possible
against every single a b test so like
the one there should be a metric um of
aggregate both total orders and
aggregate purchase value
on both this a b test and the first one
we described um
so i want that one but you can also look
at other pieces of data too
and in particular we can look at um just
that
especially in the both the pre-checkout
page and the checkout page
hopefully we can maybe test the number
of um the number of uh
like dropped shopping carts that happen
at each of those stages okay
and that should give us a much more
direct um sense as to
um whether this was the cause of the
reduction in orders
sounds good so the information we've got
is that this experiment
was running on 30 of
of live customers so 70 were in the
defaults
experience 30 were running in this this
new variant
um average order value for the customers
in the 30 percent was actually up
about one and a half percent uh and
the number of orders placed relative to
control
um was down about 21
whoops
yeah so clearly um this is a problem
i would agree uh so first of all
i mean just in general i'd be pretty you
know it's what it sounds like to me
is that this um this change
was more oriented around
the brand than it was around um
improved business improvement and that
that the rest of the brand had
changed its um color palette and layout
before um before this one and that we
wanted to
um make this one um match that
and that's okay that's important brand
value is important and it's much harder
to a b
test but it's important it is not
to my in my mind an acceptable
thing to do to compromise uh financial
performance
um for uh for improving the consistency
of a brand
uh to this level and i think it was to
be honest kind of careless
to have dialed this experiment all the
way up to 30 when you didn't have a
hypothesis
about um or when the initiating
hypothesis for doing it
was not growing revenue um my hunch
based on the fact that average order
value
is up but the total number of orders is
down is
um either customers are
probably either or both customers are
just getting confused and exiting the
app because they're confused
or we're asking them to do a lot more
work
um in order to like select which
products they're keeping and not keeping
and
either making them do it or or something
like that and so
the folks who do decide to do it are
buying more
but way way more folks are just choosing
not to buy and
and that's a pretty unacceptable outcome
so i'd immediately dial this experiment
down and go back to the drawing board
with the design
and orient the design first around um
certainly acknowledging the color
palette and
layout specifications that we want to
consider but orienting the experiment
around
growing or at least maintaining our our
our order levels
got it okay sounds good well i think you
did a good job at identifying
i agree with the recommendations that
you know brand is important but we need
to make sure that
it uh you know can be uh holistically
sort of incorporated without you know
driving a material decline in our
business metrics cool thank you
