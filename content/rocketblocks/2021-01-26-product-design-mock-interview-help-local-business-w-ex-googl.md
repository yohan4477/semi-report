---
source: https://www.youtube.com/watch?v=GvSmBETBQpQ
vid: GvSmBETBQpQ
title: Product design mock interview: help local business (w/ ex-Google PM)
date: 2021-01-26
duration_sec: 2406
channel: RocketBlocks
kind: transcript
---
hello everyone kenton kovescu from the
rocketblocks team here in this mock
interview video
we're sitting down with alan yang who is
currently the head of product management
at bubble
a popular no code development tool and
previously was a product manager at
google
where he focused on their productivity
apps including docs
sheets and slides in this mock interview
video we're going to tackle a product
design and product sense question where
allen is asked to design a new feature
to help small and local businesses cope
with the coven 19
pandemic so let's go ahead and jump in
and see how alan tackles us
i want to do sort of a product case
question
and imagine you are uh you know a pm
you you're going to have some free reign
here to pick a particular product or a
big tech company that you want to work
within that sphere but basically
we want you to think about um and work
walk us through
designing a feature that would help
local businesses
um get through copen so you've got sort
of free reign to you could pick a big
tech company and say hey i'm going to
build a new feature on top of x
or you could say hey this is just like a
new company or a new idea and we're
going to build this to help local
businesses
so okay however you would like to pursue
cool
um and i'm just going to take notes over
here um
uh could i ask a few follow-up questions
to start yeah
absolutely cool um
[Music]
so i guess from the way the question is
posed it would probably help if i chose
um like let's perhaps assume that i'm
building this feature in the context of
like google and google maps
okay um so for this particular prompt
um is there any kind of uh
maybe not like google level but like
google maps level goal that you want me
to keep in mind
or should i kind of like specify i guess
yeah no i think that's a good question i
think
um i do think having sort of a
particular goal about like how we'll
know if we're successful if this feature
has made a difference
makes sense um but we are open to you
sort of specifying hey like i'm really
going to focus on
you know uh either driving
a big revenue impact while helping small
businesses or say like you know we just
want to help the maximum number of small
businesses regardless of
revenue upside for google maps in this
case
awesome um and should i start off with
any assumptions
about the personas that google maps
already likes to work with
or should i uh propose personas relevant
to the question
uh good question i think in this case
you can propose
personas that you want to work with okay
cool um and uh
is it all right if i make certain
assumptions about
um like the kinds of data we have or
like the kinds of
uh like sources of data that google maps
might have
of course i think you know if you have
some assumption that seems crazy we
might have some questions about it but
yeah
feel free to assume certain data types
or stores of data that we might have
access to
okay awesome uh do you mind if i take a
second to
compose some thoughts no problem go
ahead thanks
okay cool um so
uh if it's all right with you um here
are some of the different
topics i thought i could walk through
and please let me know if you want me to
add anything remove anything et cetera
um so i'll start off by just kind of
like
again sort of restating the goal to make
sure we're on the same page there
and um not just to pull for the future
but possibly ties to
broader goals um i'll talk about
who some of the users involved uh seem
to be
or who they might be um then i'll
sort of propose some ideas for a
potential like v1 or even like mvp
of this then after that some perhaps
like v2 ideas
um then i'll talk a little bit more
about
metrics again um how you know we might
sort of go one level more detailed on
metrics we can track and how they tie
up to the goal okay um i'll talk a
little bit about like maybe risks or
like how we might need to engage other
functions
um and then i can close out by talking
about like where could this all be
heading like um
like what a future vision of this might
look like okay that sounds like a pretty
good plan to me
cool so in terms of the goal
to start off um so out of core
we want to design some kind of an
experience to help local businesses
in the time of covid um i think
in this particular case maybe we can
assume that the goal
is um something around
engagement uh of google maps users with
google maps uh and i propose that in
particular because i think it's kind of
a
uh like a win-win-win on all sides
actually uh where you know like if end
users are engaging with it more that
means they are finding whatever we build
useful in some way um if the
uh end users are engaging with them more
that probably means there's some value
to the local businesses
um given the future will be centered
around
uh um and um
google maps uh their revenue model
uh if you think that maybe the most of
the revenue is coming from ads like
there's of course benefit to having more
users engaged on the product um so so
that's why i
sort of choose user engagement as
kind of the overarching goal so to speak
got it okay
so user engagement is the north star yep
cool so if we think about users um
there are definitely uh the small
business that the local businesses i
should say
involved um and uh i imagine this breaks
down in a few different ways
which might become relevant um as we
sort of think about what it looks like
um i think uh one way to slice it might
be
thinking about just like the different
kinds of businesses in terms of industry
perhaps this is potentially very
relevant here because
um you know covet has had a different
effect on different kinds of companies
so like
restaurants you know have a very
different impact have felt a very
different impact
versus um i'm going to say like
a local doctor's clinic or something
which might also be this is on google
um we may also want to think at some
point about
whether there's a difference in um
called like tech savviness levels
of different businesses um
that it's something i'm sure the product
overall keeps in mind
um but uh assuming that there are
already
like ways that google maps interacts
with local businesses like perhaps
there's something we can kind of
scaffold off of here
um and why why is tech savviness in this
particular case why are you
honing in on that as something that we
would care about as we segment
businesses
yeah i think it uh it probably has more
impact when uh
i imagine we're thinking about like the
design of it like the actual like
experience the ux of it um
because you know if you have a much less
tech savvy business owner
who you know maybe they're a solo
entrepreneur
and they just don't have a lot of time
like uh
versus a very well run like fully
staffed operation which might have
somebody like dedicated to
their digital presence um like it's just
a very different
kind of user within the company
approaching the product okay
um i i again
not sure it has as much impact on like
the um
the overall thrust of what we're
designing but like you know when you
work with
uh you know the designer on the project
to think about like what exactly does
this look like
um like what are the interfaces what are
the things you want to make easier
versus tougher
um that difference might be important
fair enough
cool um
so to start off um uh oh so sorry yes so
we were segmenting businesses
um probably also useful
to briefly mention the end users as well
i imagine google maps must have known
personas for end users
but if i had to propose them i would say
there are probably
one way you can distinguish end users is
to talk about their
motivations for coming to google maps
so for example you have some users who
are probably coming to google maps who
know exactly where they want to go they
like want to type it in and get
directions and like boom
like that's it and follow directions
yeah um
there are also probably users who come
to google maps who just kind of want to
see what's around uh or um
yeah to like browse essentially a
geographic area um
there might be uh something kind of in
the middle but kind of distinct where
you have um somebody coming and they
have like a particular business in mind
like maybe a restaurant and they're like
trying to just get more information
about it
um phone number of the neighborhood
coffee shop or something
exactly yeah yeah so like something very
utilitarian like a phone number or an
address
um maybe even uh folks who like want to
like
read the description or like see the
photos or you know just like get a sense
for
the place um and so i think
uh that might also feed uh
some useful inspiration for the design
of this
in a bit um at this point it's
i also like to just at least quickly
think about like
what are these users doing um
in this particular context to solve this
pain point uh in the absence of this new
feature from google maps
so the pain point here being potentially
like you know
i want to know more information about
this business
because it's coded um from an end user's
point of view
or from a businesses point of view like
i want to publish more information
uh uh given that it's coded and you know
things are different uh
in terms of how i run the company yeah
um
so if you think about like potential
competitors here like
maybe we can use yelp as one
example to look at um they're similar in
the sense that
um you know they kind of aggregate
businesses information about business
together they have like geographic
search
things like that probably pretty
competitive with us um
they do focus a little bit more on
restaurants
you know they do other industries as
well but
they're very heavy on restaurants so
that might be kind of like one source of
competitive inspiration um from a
business's point of view
another um competitor so to speak
is uh their own website potentially so
like a lot of these companies will have
their own like you know squarespace site
or
wix site uh where they can publish
information
to the internet um so that's
uh maybe something to keep in mind that
um
you know a lot of businesses might be
turning to that uh that's sort of the
first thing
yeah um yeah or even just like their
instagram feed right
yeah especially for local businesses
that's popular these days
totally totally um and yeah from the end
user's point of view like
it's kind of interesting to maybe think
that um
a competitor to any feature we build
might be just like calling the business
like given it some unusual times people
are just like ah the internet won't be
updated so they'll just like
actually call the business um so um
yeah so some useful um just like
things to keep in mind as we start
designing
um is okay if i move on to thoughts
about mvp yeah
definitely cool so
for the mvp um you know where the goal
is to design
a feature to help local businesses
in the time of coded and
one assumption i'm going to make here is
that we
have uh at google maps we have some way
to connect with businesses already
so like basically i forget what the
project's called like google my business
maybe
um but there's already this
product within google where businesses
can like claim
their listing and like fill out certain
templated information
about it um
uh i think that does actually exist but
yeah yeah
a useful starting point fair assumption
and i'm pretty sure it exists and i have
no idea what it's no idea what it's
called yeah cool
um so um the mvp that
i'm kind of mulling over is basically
hooking into that system
and adding a few new
uh covet specific or kogit special
fields
that businesses uh can provide um
which get displayed uh kind of
prominently
in their google maps listing okay um so
what does that mean uh in a little bit
more detail um so
in the time of covid um there are
probably gonna be certain pieces of
information
that the local business wants to get out
there um that
if they can get it out there to a wide
enough audience they can you know help
um their business stay afloat hit as
hard
um so some examples here would be
maybe they have updated hours operation
or like special or changing hours of
operation over time
um there are probably specific
covet safety measures that some of them
might want to take and this is where
industry
might become a little bit more relevant
so like restaurants um like in new york
city for example
definitely will want to broadcast
whether they have outdoor dining yeah
um whereas that might not be as relevant
um
for other industries um maybe they
also want to broadcast like the number
of people capacity of their store
maybe they want to broadcast like any
special offerings um
that they have so like it could be a
special menu for
a restaurant but even like you know for
uh like a pet store like maybe
um they're offering something special
to sell um
is an interesting question like uh for
these fields like
do you just want to do sort of like open
free form text entry
or maybe some of them can be made into
structured
um multiple choice or like yes no
questions
um a little bit of research there might
be useful um
i do kind of think like if you sat down
and thought about each of the different
fields you want to ask you could
probably make a reasonable first
assumption about it
um uh or like even better maybe
if you have easy access to some of these
local businesses just like ask them like
yeah i'm curious like if you were at
google doing this and you were thinking
about that specific
problem of like okay what are maybe some
of the common
things that we would want to flag as
fields like how would you think about
trying to
to use any of the infrastructure you
have at google either people
or technology
yeah um if we have an easy way to get in
touch with
our existing like businesses who are on
google maps on this platform
um great like maybe maybe you could even
shoot them a quick email and ask them
this question
um or like a quick call um
if that's uh if that has a lot of
overhead um
depending on when this is during the
pandemic you might be able to just like
take some kind of a sampling of
businesses go to their websites and see
how they've updated their websites
um not all of them probably will have
but some of them might have and you can
kind of see
um get data on like what they they feel
is
important to put out there got it okay
cool yeah
cool um so yeah so there's
um kind of this element of augmenting
the form
that small businesses can fill out on
this small business platform um and then
there's also the element
of like showing this information on
google maps
uh on a particular listing and so this
um
is something you know you definitely
want to engage with a designer on
um this information should probably be
prominent in the sense that you don't
want to like you know have to scroll to
the very bottom for this
uh it should probably be like called out
or highlighted in some way
to specify that it is related to covid
and
like coget specific like like unusual in
a sense
um you probably don't want to
put it above like you know you don't
want to put it so high up that it's like
above
the name of the business or even above
like those shortcut buttons so like
directions or call or something like
maybe somewhere
close to but below that um
uh and so yeah like having like a new
highlighted section there where the
information is presented
in kind of like a consistent ordering um
and in a consistent format depending on
like what the type of data is
got it and tell me a little bit about
the sort of
assumptions or logic you were using
there as you were thinking about the
information hierarchy like
why wouldn't the covet information be
above say a phone number or website
yeah that that's a great question um
something i would probably want to
test and work with a designer on but my
thinking was that
um going back to like the different
um uh reasons people
users are coming to google maps um
like hypothetically uh making up numbers
if we had data to show that you know
like 70
of users coming to google maps are in
the bucket of knowing where they want to
go and just want directions
um you know like that
uh because that's like the majority of
your users you probably still want to
make it easy to fulfill that flow
uh whereas if you have data showing that
okay that's only 20 of users and
actually i don't know like
80 of users want to browse that's
that's definitely way too high but um
you know you would probably
uh be more willing to prioritize this
new code information
above some of like the key common use
cases got it okay
that makes sense yeah cool
um so uh yeah so we
i kind of touched a little bit upon what
it looks like from the
the business aside um a little bit what
it looks like in google maps so like
what an end user would experience
um there's also maybe an interesting
element with google maps
in particular around like their
recommendation algorithm
um because they're doing recommendations
both like when you search i think like
autocomplete
as well as um like they now like will
show some venues
in the map area by default yeah so there
must be some
algorithms behind that um so kind of an
interesting
question to explore whether this covet
information should influence that
uh influence the ranking in the
algorithm yeah
not something you need for the mvp
strictly speaking
but to the extent that
the product overall cares about you know
some of the metrics around
those recommendations like might be
something to bring up with the team and
talk me i think that's an interesting
point talk me through
what you think some of the trade-offs
there between say
influencing the algorithm that that
drives what shows up or the
recommendations in what order with like
whether or not
that particular listing or business has
covered relevant
info entered yeah so
so it's a good question
um because maybe the strongest counter
argument to the idea
is that um like in some sense there's
like a right answer to a recommendation
right like do people engage with the
recommendation
and whether or not people engage with a
recommendation
you might think that that's agnostic of
covet information or like covet
preparation right like if
um i'm trying to come up with an example
like
if i'm looking at an area in like
midtown manhattan
and i want to look for an italian
restaurant um
like the previous algorithm probably
incorporated you know some mix
of ratings and like
buzz of some kind and like how sure they
are of the data about a restaurant
to generate recommendations um and over
time that's
honed by people like tapping on the
actual um
restaurant um so
if it's the case that people are still
kind of
like i guess it's almost like what is
the question they're trying to answer uh
for the user with these recommendations
like if you're just looking broadly for
like
what are some italian restaurants of
interest in this area
then you're right like coveted
information might not
be as much a factor but if the question
they're trying to answer is
i want to go to an italian restaurant
what is one in this area
for me to go to um the code information
might be more relevant for an end user
yeah yeah and i think you could
certainly imagine from a user
perspective like
in this era that we live in
unfortunately like one of the most
relevant questions is like
yeah i know this is like a great spot
but like are they open do they have
outdoor dining
if they do how much they have they used
to be able to fit like 100 people but
now it might be like
20. yeah you know depending on what what
their setup is
you can see how like that relevant that
info becomes probably super relevant
potentially
totally yeah yeah and i guess that that
was an implicit assumption i was making
that i should probably state explicitly
which is uh end users
probably want and care about this data
because it influences their decisions
about where to go
um so the whole reason like businesses
want to broadcast it great
uh but end users like want this
information because like these are some
of the top questions they want answered
about a local business yeah do you think
there's like any other
impact like say you decide hey we are
going to
the the recommendation algorithm will be
influenced by the presence of some of
this covet information or not
do you think there's any other benefit
or can you think of any other way that
that
may be useful or even like is there any
ones that that may be harmful that we're
not thinking of
um i mean if you really wanted
businesses to fill this information out
you could broadcast that
you are using this as a factor uh and
that will probably
give them a little extra character yeah
a little insane
um yeah yeah and
yeah there's probably the flip side as
well which is you know is that a little
machiavellian is is the wrong word but
you know in the chaos of just trying to
survive as a local business owner
if you're now like moving down the
rankings because you haven't updated
something in google as that
yeah is that a trade-off that the google
maps feels comfortable
or the right the right product decision
totally totally
absolutely um
yeah um so those were some thoughts
about the mvp and i was starting to go a
little
maybe beyond mep there um uh
maybe i can talk a little bit about like
where this might
go in the next iteration yeah i think
that sounds good cool
um so for the like v2 uh loosely
um there might be some other uh ideas
that we kind of consider
um and this should be influenced by like
how the mmvp goes and like feedback we
get
but um some ideas that uh
feel potentially uh more high impact to
me right now
in absence of data one might be to
consider what happens if
a business doesn't have an account with
google or
doesn't have the bandwidth or desire to
update its information
um in this case uh this would be
kind of a large bolt-on feature but um
maybe you could crowdsource and
have some kind of an affordance for
users of google maps
to provide information cove covet
specific information about
business yeah um i mean you already have
the ability to leave reviews
so maybe this isn't too uh too heavy to
lift but
um this could be a way to help you patch
up um
like just missing data if that's a
concern
an interesting idea on the design side
uh could be
do you want to influence how the little
markers look on the map
based on this information um ah
interesting tell me more about that yeah
so like i think today you know you have
different little icons for
like you know restaurants versus like
other kinds of establishments
um like i almost wonder if it would be
interesting
to modify the little icon or like maybe
use a different color
or like have a badge on an icon i don't
know
to signify when a restaurant has listed
their code information
partially again it kind of feeds into
like oh this will encourage
businesses to fill it out yeah um
partially i wonder
if this helps users just like visually
get a much
faster sense of like what's on a map
yeah um i i
imagine again this is like maybe a
consideration that google maps has
thought about in the past like how
important are these icons and
um the thought behind them but um
we have all the data at that point so if
it were important and we
wanted um to drive you know some of
those uh impacts
yeah that feels like something we could
do yeah yeah it's an interesting
it's an interesting idea and also sort
of brings up something that
that as related to what we talked about
earlier that's sort of an in-between
solution of like
does the information influence the
recommendation
algorithm or not like it may not
influence say the recommendation
algorithm but give some visual
affordance
and and related to that you could
probably do like if a user cares like
let him or her filter by this place has
inputted covet-specific information yeah
totally
absolutely um like
uh slight tangent but um when we talk
about competitors like i think one thing
yelp does better than google right now
is the ability to filter
um so i would bet that if yelp started
listing code information
like the next step they're thinking of
like can you filter on the code
information so
yeah absolutely um
for uh thinking specifically on the
business side um
and this one i'm not sure about because
i'm not sure if this necessarily ties in
with some of the goals but
um there's a lot of potential like
social good that google could do
on the business side um i use that term
kind of loosely but for example
when a business is looking at the form
to fill out their code information
maybe they could include a link to the
cdc guidelines
for that industry or the state's
guidelines for that industry
it may even be interesting to show the
local business like here are what
other you know businesses of your
industry in your city are doing
mm-hmm um outsource best practices
exactly yeah um and that
i hesitate a little bit uh i'll just
bring in something like the risk section
here because
then it feels a little bit like you're
starting to get into like you know what
are the guidelines for
dealing with covid and i don't know to
what extent uh google wants to get into
that
yeah um but the data
would all be there so to speak and you
know adding a few
links and charts um is doable
yeah yeah um
so those are some potential ways uh
the team might want to iterate on this
feature um okay after the mvp
um can i move on to metrics now
yeah i think that sounds good cool so
we said earlier that the overall
business goal um
was engagement um so like engagement of
uh users so uh
there are um probably ways already to
measure
whether or not a user engages with a
particular business listing
so perhaps we can extend that to come up
with a metric for whether users engaging
with the covid
information on the business so
maybe like i think what you want to know
in
essence is like when a user has a
business listing pulled up
are they looking at the code information
maybe we have some way to measure that
already
um or it could be like um
looking at user engagement with maps as
a whole and seeing like oh okay like
users um are engaging
more with google uh when they see
businesses
with uh the covet section in the listing
or something like that um if you had
like the visual markers on the map
um like you could even see like you know
our users tapping on the
ones with coveted info more than the
others yeah
um and ultimately like uh this would
probably
uh this this could have an impact on
like high level engagement metrics so
like do people come back to google
day by day are people successful in like
their searches on google
metrics like that um
i i think it also would be important to
track the engagement of businesses with
this
and that is almost a bit easier to track
because you could just look at like
literally how many businesses
are filling this out um either in pure
numbers or like a percentage of
uh business listings you have you could
maybe even look at like our new
businesses coming onto the platform
uh because of this potentially but like
engagement on the business side
i think there are some numbers i would
want to track there
um uh
what other thoughts that i have here um
one uh i don't know if this is creepy or
not but
to the extent that google maps knows
where users are
geolocation wise like could they even
tell if the user
ends up going to a particular location
that they looked up
um that kind of gets more to like a task
success kind of a metric
um but it would be very very interesting
to see that
you know like because a business lists
this information
like their traffic is up like 10
relative to some baseline
yeah that is interesting like is this
actually driving
foot traffic yeah yeah exactly
um i don't know to what extent we
normally track
um like revenue coming from this like
advertising revenue
um if we if that was something that were
very important
to the team or the product um we
could try to like uh keep an eye on that
as well and
yeah even influence that cool yeah um
given sort of your initial idea of like
hey we're going to focus on
your driving engagement with this
feature thinking about the list of
different sort of metrics and somewhere
i think like areas of metrics you might
focus on if you had to prioritize and
pick
you know i'm not concerned about the
very specific number but one or two
of those or maybe three at most what are
like a handful of metrics you would use
to try and okay
i can look at these metrics and get a
quick read on whether this is working or
not
yeah um i would
prioritize a metric around like
engagement of the user so depending on
what we can do
this might be um like if we can do like
time
spent on uh looking at a business
listing
um uh that might be interesting as well
as like time spent
looking at google maps as a whole like
browsing uh mobile maps as a whole
um i think the third one i pick uh
is probably um uh
so sorry the first two are i'm kind of
using like placeholders for like
key engagement metric of end users with
google maps
um and the third one i would probably
say something around like task success
again so like the geolocation data if we
have it
a simpler version of task success might
be like bounce rate
or something like that like trying to
lower bounce rate um
because my hypothesis would be that uh
higher success means
more likelihood that users are getting
value out of it and would
use it again got it okay but you
wouldn't actually prioritize anything
about
percentage of businesses that have
actually inputted the information
or um you know you put those particular
flags on
safety or special hours i would
i mean that's definitely my top five but
um
yeah it's a good question definitely my
top five um
my sense a little bit is that
it's not quite a two-sided marketplace
per se but you kind of need like both of
these user groups to
engage and if you had some small number
of businesses
doing this i think you could start to
get data on whether
users are reacting
and then later on maybe if signs are
very positive
you do keep an eye on the number of
businesses you fill it out um
uh but yeah like if i if i had to
pick between the two sides i would
almost want to focus on users because
that feels like
the thing we're trying to drive got it
so the argument would sort of be
look we're not going to see the user
metrics move if no businesses are
filling it up
because then there's just not going to
be enough of this data for them to even
react to so you would expect that user
engagement is neutral
right
um i guess touching briefly on
risks um i mean one risk is that it's
this is all pretty
fast moving uh like there are lots of
developments
so like there is always a chance that
like in a month you realize that oh
there's this new factor
that's super important that hasn't been
in your little new questionnaire yet
and you kind of need to like keep
iterating so to speak
um also a possibility that in like two
months magically
you know dependent is over um vaccines
everywhere
yeah um i think uh
there's a slight risk we mentioned
around um
kind of just the the topic you were
mentioning around like okay what are the
guidelines like to what extent do you
want to like push specific guidelines
is that like is the government going to
get annoyed at us
um yeah so some kind of nebulous risk
there i think
um i think uh there
uh it could be the case that different
parts of the country just care
about this overall or about specific
factors
to different degrees yeah um which makes
i think
the overall problem a bit harder to
tackle so to speak yeah
um in terms of like other help we need
uh or other help we tap for this um like
there's definitely gonna be some
component around
um ops or or maybe it's like the
community team or the support team like
whoever's helping the businesses
maybe that's a completely separate team
within google
but like you know we need to get them on
board and then we need to kind of work
with them
to be able to support businesses as they
use that part of the product
um probably want to check in with legal
for some of like the
like guideline risks and things like
that uh also what if a restaurant lies
um yeah small risk there
um and then i would definitely want a
lot of help from marketing um
uh like this is not something to like
create a billboard campaign out of
at from the very get-go but um like
maybe they can think of some clever way
to
help us get word out there about the
future um
might be a little bit more impactful in
the short term on like getting
businesses to
um come in with symphony cool yeah
um and then the final thing i want to
touch on was just like where could this
go in the future so like
much longer term what could this look
like um
[Music]
in the concept of in the context of a
pandemic contact tracing
maybe um maybe um this is kind of like
some kind of a gateway to getting google
more information that could
make contact tracing a lot easier
legally
but there's that but in terms of like
the product like supposing we think
beyond the pandemic
maybe this is interesting model to test
out for
any kind of like a special circumstance
in the future so
it doesn't even need to be like a global
special circumstance but maybe like
a store is having a massive sale in the
middle
of april for a very personal
idiosyncratic reason
yeah um like could this be an
interesting way for businesses
uh to engage with google maps for these
like more special like one-off events
yeah not to mention of course that you
also have like
more global events or like widespread
events like black friday
or like holidays or
things like that um i imagine google
maps has some way of dealing with
holidays already
so maybe we can actually use some of
those learnings here but um
there might be something that feeds back
in uh back and over there
yeah um yeah and so i think
long term um i guess part of the
potential hope of this is that you build
the habit
in your businesses that google is the
place they want to go
when they want to like broadcast special
information
like this yeah um so yeah so
those are kind of like two potentially
longer term things yeah
that's cool i i like the longer term
idea particularly
particularly around what
unique message does this business want
to get out and potentially surface and
google like it's a little
additional piece of real estate they own
in in the digital world
and in a post-pandemic world which
hopefully we get to soon
knock on wood um i could see that being
very useful
like very useful to um
very useful to businesses um and i you
know i could see
it sort of flowing back into a bunch of
things we talked about about it if you
are
you know you were talking about users
that just want to see what's around like
that type of user like maybe you're
visiting a new city and you just want to
see what's around and like see
which local shops are having sales you
know google
now is a way where folks can say hey
we're having a sale on
you know everything in the store 50 off
tuesday through
saturday that would be kind of cool
actually
and i think it's very aligned with
certainly the small businesses
um you know own use cases and interests
cool great this is awesome
