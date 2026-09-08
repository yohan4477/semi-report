---
source: https://www.youtube.com/watch?v=ID8YTF100A0
vid: ID8YTF100A0
title: Product execution mock interview: user engagement (w/ Microsoft PM)
date: 2020-08-18
duration_sec: 1979
channel: RocketBlocks
kind: transcript
---
hey everyone kenton kovesky here founder
of rocketblocks in today's rocketblocks
video
we're doing a full product management
interview focused on a facebook
style product execution question
these come up all the time in facebook's
process it's a key part of their product
management interview process
and playing the role of the candidate in
today's mock interview is
angkor bishwas he is a product manager
at microsoft currently
and he's a member of the product folks
community which is a online community
for product management enthusiasts based
out of india and we did
this video in collaboration with that so
let's go ahead and jump
so thank you so much for joining us
ankur um it's great to have you
here for this mock interview today and
what we're going to do is we're just
going to
go ahead and jump right in and we're
going to be doing
a facebook style product management
execution question
okay so the question that we've got for
you today is
if you you are a pm working on instagram
specifically on the stories team
and you walk in and notice sort of
immediately in the morning
that engagement with stories is down
how would you think about investigating
this problem
okay yeah first of all uh thank you very
much for having me it's uh
good to be here and uh thinking about
instagram stories itself uh and
engagement being done i guess the way
i'd like to
tackle the the question or the problem
at hand is to
dig a little bit deeper into the problem
first of all to kind of figure out what
engagement means to us
and kind of what metrics we're looking
at to quantify this engagement
um and then we can dig a little deeper
into reasons why that might be done kind
of figuring out the root cause
uh for the problem and then we can
investigate potentially brainstorm
solutions uh from there does that sound
like a good way to approach this
yeah that sounds like uh that sounds
like a good approach all right awesome
so i guess the first thing i want to do
and i'm just taking notes here
uh for my own benefit um i want to kind
of
dig a little deeper as to what i mean by
by engagement
so different teams uh in measure
engagement for different products in
different ways
it's uh and i want to drill a little bit
more into that so
there's direct ways in which i can i can
measure it so
the number of stories uploaded uh the
number of views on stories
um maybe a composite measure that's kind
of a weighted average of of the numbers
we get on these
um and there's also user-focused ones so
we have
uh the number of sessions uh the number
of seconds in a session the number of
daily active users or monthly active
users over time
uh kind of is there a specific one of
these that have that we've noticed in
the morning
uh is drastically different yeah so
that's um
that's a very good question so i think
you you hit on a lot of metrics that we
obviously do pay attention to
uh the number of stories posted in any
given day the number of you know unique
users posting those stories a number of
views on all those stories
um average session lengths all of those
metrics are great things to highlight
and we
do keep track of all them the specific
metric that that we noticed was actually
sort of
an aggregation of a few which is
basically looking at
all of the unique users that engage with
stories
in any way at all whether they either
posted a story or
viewed a story in a given day and so
basically how we
think of that as we call that stories
dau so the
the daily active users of the stories
okay awesome so if we're talking about
daily active users then
um then i can kind of ignore my uh
for the purposes of this problem at
least assumptions about some of the
other things and
drill down a little bit into that yeah
so when we're talking about uh
daily active users um is that a specific
time period for which i've noticed we've
noticed this go down
um is it maybe a week a month a couple
days
yeah so um the specific metric that
we're looking at here
is that um what we've been alerted to is
that daily active users is actually down
5.5 week over week
meaning if you look at dau uh
today or sorry yesterday for the full
day and compare it to
that same day a week ago that number has
declined
5.5 percent and that's sort of the the
red flag that the team has noticed and
wants to investigate
and and is this just over the last
couple of weeks has this been happening
for a little while
uh very good question so it's it's
sudden like if you look at the day
before
that that uh delta was i don't remember
it off the top of my head but it was
like
plus or minus you know point uh
two five percent or something which is
like that's pretty normal for us
so this this drop is is sudden
okay so i've noted that it's uh that
it's a sudden drop and that's obviously
something i'm going to keep at the back
of my mind when when i continue
uh with this investigation uh let's try
and narrow this down together a little
bit further
um do we have any i want to try some
segmentation
information um are there any specific
locations in the world i know
stories is a global product uh have we
narrowed this the lack of this
engagement down to maybe you know
america's or europe or maybe even a
specific country something like that
yeah so that's that's a very good
question uh
the way we have caught it like the the
dashboard gives you access to
what's going on in key regions so you
can look at north america
you can look at mia you can look at apla
and
right now all of those they're down
equally so it doesn't
you know we haven't seen anything um
divergent there
all right and before i go to the root
cause i'm sure there's a lot more things
we could consider but one thing that's
really important
instagram being a mobile as well a
mobile platform there's
loads of differences between mobile
architectures themselves
so is this something we've narrowed down
to maybe symbian os versus
android versus ios windows um any any
device related things that we can we can
look at flag immediately
yep that's another good question um on
the dashboard you can segment by
os you know you see you look at ios
versus android um etc
and uh you can cut it that way
um there are some you know minor
differences like
5.6 versus 5.45 down but
you know it looks basically pretty
consistent across the board regardless
of what
os um you cut it by all right awesome
all right i think this is kind i think
this is
for now enough information and and if i
if i need anything
uh more from you i'll i'll drill into
that as well
the way i wanna think about this problem
is
to look at kind of uh different ways in
which this this engagement
uh problem might have occurred okay so
um
would you kind of want me to to just
explain my thoughts to you just
across the board yeah it would be you'd
be helpful to sort of know how you're
how you're thinking about it for sure
the way i want to think about the
problem just so i can in my mind
uh check at least be as exhaustive as
possible in the in the list of reasons
uh i want to think of things that may be
something that we have done
uh so as the stories product team we've
done something internally
with for the product itself that's
causing uh this issue
or something that's outside of us an
externality maybe customer behavior
something that the product itself is not
responsible for the drop in engagement
so that's kind of broadly
uh the two buckets that i'm gonna that i
want to think through this question
okay um so i'll i'll tackle the let's
say
the product focus metrics first and the
assumption i'm going by there
is that it's unlikely to be any unlikely
but we drill into that as well
external behavior because i it's a it's
a sudden drop that doesn't have
any uh preferences on on geo
or or the device that's being used so it
seems
to me that it's more likely that it's
that it's a product related book so i'm
gonna dig
there uh first so yeah tell me just a
little bit about that assumption be
because it's sudden drop you don't think
it
is due to something external like give
me a little more unpack some of that
thinking for me there a little bit
yeah if it's if if it so the reason i i
think about external and we talked about
a large number of geos uh
for me external primarily is concerned
with with customer behavior and maybe
competition a little bit
uh so i would think something like a
natural disaster would cause engagement
to go
down because people suddenly have other
priorities uh it's unlikely then that
something drastic like that and i think
five percent drop in engagement is quite
high
can happen globally across all devices
at the same time um at least that's what
i was thinking of when i talked about
external problems there's of course
a larger list of problems but that's the
assumption under which i went with
product focus things first got it okay
makes sense
all right cool so let's internally then
if we're looking at the product i have
um i have through experience known that
that when something looks wrong on the
dashboard
uh do not always trust the dashboard
uh so i wanted to look at the dashboard
itself a little bit about the data
quality that we have
yeah um is there any chance we were
getting bad data
is that is there something wrong with
the telemetry are we measuring it wrong
when we parse it in the in the
in the reporting layer um are we dealing
with legacy data is is that something
we've we've checked and kind of ironed
out already
yep it's a very good first question uh
unfortunately in this case we can't
point to like a broken etl or anything
like that
we have uh you can sort of trust that
your
lead analyst on the team has gone
through and looked at the whole pipeline
and assured that yes like
all the other metrics are right and
everything checks out this one does
appear to just be
down okay cool uh so i'm gonna then
kind of rule out in my mind uh just
issues with data quality so we don't
have to go down the data analyst track
uh for why the why these numbers might
be wrong um in that case then if we
dig core into the into the features into
stories itself into the product
um i think there's there's a few issues
that that may be happening
uh the first could be we broke something
uh so
in releasing a patch or a bug fix
uh we just made the feature inaccessible
across the board to
to some group of users uh that's one
thing the second thing
that i can think of is we may have made
the feature just a lot worse to use
uh so something that went into the that
was deployed to production recently
uh made the experience of completing
whatever
uh workflow it is on the app with
stories difficult to do so maybe
starting to to upload a story would go
fine but it didn't actually upload
the the views may may not have been may
not have been a great experience
uh which means that you know maybe 95 of
the people stuck through with it and
tried repeatedly
but for the other five percent they just
kind of stopped stop working with it
because it was annoying
or there's there's an access issue uh
there so
we're not authenticating correctly
people are unable to get to the stories
feature to begin with
which is why it's not working um so kind
of
i want to kind of talk through those
obviously a little deeper do you have a
direction in which you prefer to go
yeah um i think those uh
those two additional buckets you
mentioned under internal sort of product
issues like either one
you know a particular bug or a
particular release like we just
changed something intentionally are both
good things to look into
um i do have some additional information
i can provide in terms of
uh releases uh so the first is that a
team that looks after
uh notifications recently pushed an
experiment that bundles push
notifications
to mobile devices about their friends
stories
when their friends post so um
that that experiment is running there
was also a release that adjusted what we
call
internally at the the story bar so
just to make sure you're sort of
familiar with that if you open instagram
uh and you know are looking at the at
the core feed
you will see like this bar uh usually at
the very top of the app and then
sometimes
interspersed in the core feed as well
which shows you the stories that you
have access to
um and there was a release that adjusted
sort of the mechanics of where the story
bar shows up uh
and then the last thing in terms of uh
launches from facebook itself is was
that there was a launch
from the messenger team uh that updated
their story creation tools
so the actual tools that if you are
making a story as opposed to viewing it
um the the tools that you would use as a
creator
perfect right that seems like again a
big company huge
product with with a lot of releases
going through um
that that any of these could be the
issue
so going back to um the the data we had
from a little earlier
being that it's pretty cons it's down
equally across all regions
uh i'm gonna assume that these were
released
globally at about the same time that
there's no difference between these
three releases
yep so all three of the releases i just
mentioned actually
all did release uh the day in question
i mean they all are global global
features and releases
awesome uh and they were released across
all devices so
i guess it's something to do with the
experience of using
uh of using the stories itself of using
the stories tool that's that's been
changed
as a result of this now we're talking
about daily active users
about people that are engaging with the
stories feature so i actually want to
to um investigate
for me in my mind that affects that
feature the the instagram stories
feature most closely
and to me that would be the mechanics of
the story bar
because i would assume that the the
messenger team when they release the
story making tools
uh that provides kind of a of an
infrastructure layer on top of which we
build specific things that are related
to
the instagram stories uh and if that's
working properly i want to investigate
core to the to the stories tool itself
if there's anything
uh there so can you tell me a little bit
about the uh about the
story bar mechanics that that were
adjusted kind of what did we expect from
that
yeah absolutely so the story bar
mechanics the way to the way to think
about this release is that the default
before the release was any user when
they log into their app
their their instagram app they would see
the story bar sort of pinned to the top
of the
core news feed and as they scroll
through uh their newsfeed if they scroll
down
they would not see the story bar again
so that that's the default behavior
before this launch
and then post launch with the story bar
uh what's going on is that um
it is the story bar is still pinned to
the top
but intermittently it is also uh
interspersed in the feed as you scroll
down so
i forget the specific number off top my
head but you'd see the story bar at the
very top and you might see it after you
see
the first 12 uh posts in your feed and
then
after 24 posts you'd see it again if you
scroll down etc
okay um and this is of course just in my
mind judging by
if this were to to do its best job and
if it were to be working properly
then we would see an increase of
engagement right because the number of
times in which you have the ability to
look at a story or create a story
uh is increasing by by the amount that
you're scrolling does that does that
sound right
yeah i think that's the right intuition
if you were trying to sort of confirm
that
internally at the company like what what
might you think about doing or
who would you talk to i think i would
want to talk to
two people the the pm in charge as well
as the release manager
of this particular feature uh one the
the pm in charge to look at the the
metrics that they were
targeting uh for the success of this
feature if they wanted to see an
increase in a specific behavior with
stories or with just
engagement as we with daily active users
as a whole
and with the release manager to know if
there were any technical issues they ran
into
or anything they suspect technically
going wrong when the feature was
released
uh to the public okay um great
those sound like good people to talk to
let's say you wave your magic wand and
you're able to talk to those people
uh what you learned from the release
manager is that
uh technically things seem fine they
haven't seen any major
glitches bugs like that anything
preventing people from accessing stories
from any of the new storybar placements
and the product manager when you reach
out to her says
that the experiments they ran with this
new feature um
as you sort of intuited actually drove
engagement with stories up so they saw a
2.3 percent
increase in stories dau with the new
story bar
uh the multiple insertions
right so looks like this particular
feature itself was successful in in
maintaining kind of
what they wanted to do uh which again
if this feature has succeeded but the uh
overall engagement of stories has failed
probably points to maybe not
this feature itself but maybe i'd like
to then push my focus
towards the notification bundle or the
messenger teams tools
in creating stories okay um so
let's let's look at the again my
my determination of bit of going between
the two
um since the push notifications again is
directly related to instagram and one of
the ways in which
people often view stories at least
that's the way i view stories from my
friends is when i know
my friend has uploaded a new story and
and i click on that notification
uh so i would like if i could wave my
magic wand again
uh to talk to the pm uh who is in charge
of
who's in charge of the notification
bundle uh to see whether there was a
specific stories component to that
release whether
uh stories were showing up in a
different format whether the call to
action
uh message notification text that you
saw on screen had changed in any way
and what that expected behavior was when
a notification with a store
regarding a story came onto a person's
device yeah
got it makes sense those are all good
questions and we will let you wave your
magic wand again
um so uh this pm when you reach out to
him and he he lets you know that
essentially
um what this experiment is doing is it's
not changing
the call to action um in any of the text
message like the copy is
sorry not text message push
notifications the copy is staying the
same
uh really what is being tested in this
experiment
is the frequency with which the push
notifications are actually
sent to devices so the current default
behavior
uh which 33 percent of users are still
in uh is that
anytime a friend
a close friend as determined by facebook
instagram
post a story you will receive a push
notification instantly as
another instagram um the first
experiment variant that they ran which
has another 33
of users basically
has two bundled um push notifications
that they will now get a day so rather
than instantly getting a push
notification anyone posts
depending on when their friends post
they will get one in the morning and one
in the evening that sort of
bundles together the notifications about
their friends posting stories
so that's the second variant and then
the third variant was
one midday bundle that encompasses
any notifications about a story that's
been posted
by their friends their close friends in
the last 24 hours
okay sorry can you just repeat that so
we have one notification per day and you
said that's around midday
yes that one is midday so the three
variants are there's just default which
is the normal experience
push notifications go instantly the the
second variant
is there's two daily bundles one is sent
in the morning
and one is evening and the third variant
is
one bundle that goes essentially midday
i think it's
3pm all right and from my understanding
of instagram stories the stories
themselves
has any behavior on that on how the
stories once you click on the
notification
has that changed it all so i know for
example uh that the stories go inactive
after 24 hours i believe it is
uh is that behavior still persisting
with the stories uh that behavior is
is still the same okay so all the
product mostly the the way in which you
experience stories
once you click on the notification it
remains the same yes so that yeah the
core
functionality of stories their
expiration dates how you page through
them how you
interact with them respond to them has
not changed
okay so immediately i see uh a couple of
things in ways this might change user
behavior
okay so if i if i go back to something
that we did and we
uh and i talked about feature quality so
so nothing broke
per se things are behaving as they
should uh but we might have
made the feature a little more difficult
to to interact with and this is kind of
where i see this this going through um
as a user
of of instagram one of the let's say
we're
just you know people who have certain
amount of free time during the day
um we would like
or when we are talking especially about
our close friends
when we have a close connection with
them uh online
we want to know what's happening with
them uh as soon as it does because we
may be with them
uh we might want to see the engagement
and likes from other friends
uh we want to know what they're doing
what they're up to whether it's a fear
of missing out or knowing that you were
there sharing that moment with them
that's right immediate gratification
is something that's really important to
social media engagement that's something
specifically
as a value proposition i guess if we're
talking about in a business sense
uh that instagram stories provide you
you know immediately about about when
something is happening
i see uh variant one and variant two
uh when we're talking about having one
at one in the morning one at night or
just one per day at
noon being particularly kind of
detrimental to that
from that need of of the user and the
second one
uh being that if the experience of using
stories hasn't changed at all
um that if we have just one bundle
coming in every day at noon and you kind
of miss that bundle because you're busy
people have work you know during the
work week especially people might be
busy at noon
time zone changes all of that you might
actually miss an entire set of stories
and might not be able to view them even
if you wanted to
even if you would have considering the
code product has not changed
um so i'd like to to and i see that is
the more likely thing because people's
behavior
when they've been using it for a long
time and it's minimalistically impactful
to them
isn't more likely going to change so i'm
going to this is my hypothesis kind of
going in
is that people want to see stories uh
but haven't been able to because they
might be expiring or because they don't
have access to those
uh anymore um is there a way we can kind
of talk to the person releasing variant
two of this to see
how engagement with stories the number
of views has gone down
or up uh as a result of this particular
experiment
yeah so uh this this pm did share some
data about the experiment that's running
so
um what you know is that there are three
variants
uh each variant has 33 of the
global user base in this case in it
so evenly distributed and um
the analysis so far on the on the second
variant
is that the amount of
of users opening the app in response to
one of these notifications
is down 10 relative to the default group
the default variant
and for the the third variant which is
the one with
one bundled notification sent midday
is down 15 relative to
uh
all right so i think that that might be
again
this might be the cause of the of the uh
drop in inactive users if we're talking
about 66 percent
of the user base in total uh having kind
of
a massive drop 10 and 15 respectively uh
of of users that actually might then
contribute to the overall number
of the 5.5 degrees i think is what you
said yeah whereas
we did release a bunch of other features
uh that increased viewership so
on on net net i think that's probably
what's what's causing this
uh this drop so i guess digging into the
the root cause a little bit further then
um when we're talking about the 10
decrease or the 15 percent decrease
we can go with either one of them uh do
we know from that pm
whether it was because they didn't
whether the number of clicks viewing
into stories was less overall
or the stories were not available when
they went to click on that so
uh did user behavior change in any way
or did the product
the way in which the product behaves
with the customer change at all
so yeah so that is a good that is a good
question and what they
found was not that like users weren't
getting to see stories they wanted but
just that the number of users clicking
in
was was down
so the stories were there for folks that
wanted to see yeah
but the amount of people just simply
responding to the notifications itself
okay so i think then uh i'm going to say
um i guess retracting a step from where
we began this conversation about the
variance
uh is this is is kind of dictated by the
way in which people
could want to consume instagram stories
um
when i see a story come up i want to see
that immediately because of the
relevance it has
from the person posting it especially
again as it as it comes from a close
friend
and i want to see and consume that
immediately uh i'm going to say
that if that then occurs maybe towards
the end of the day
or in or in the case of the third
variant at some point the next day
that gratification that you might have
wanted a may not be relevant anymore
because
you you you're not thinking about that
moment anymore movements have passed
or that gratification has been achieved
through a different way so that same
moment
you could have seen through a snapchat
you could have exchanged through
imessage you could have exchanged
through whatsapp
so the benefit the core benefit that
that we're providing with the instagram
story of that lends into that person's
life
and what they're doing that core benefit
doesn't exist anymore because
you can kind of get that through through
other ways uh to kind of test that
theory i guess
i know facebook is is a large company we
have access to facebook stories as well
as as well as whatsapp
i'd like to see if the engagement on
those because the behavior there hasn't
changed at all
may have gone up at all uh that might be
kind of the first way to investigate
whether this gratification is coming in
uh from anywhere else uh and then i'd
like to also i guess kind of behave
clicking into
that user behavior uh whether the uh
the engagement has changed in from the
default category at all so from the
control group
are we seeing the same numbers that
we've seen before that that'll kind of
help me
look at the consumer behavior a little
better um
can you clarify that that last question
so
the last question is we have 33 percent
of people across the world
having access to stories with
notifications as they were before yeah
yeah
uh so and we have a bunch of other
features that that increased uh
engagement there um so has that
engagement gone up or is that one gone
down as well
ah yes so that's a good question so um
in the default variant that group
is seeing a slight engagement lift
sort of in line with um what we would
expect from the storybar
feature that also went awesome uh so
in that case i believe that the the way
in which we're manifesting these
notifications
uh to the large number of people has
kind of taken away the the major value
proposition i guess that the stories is
providing
um and in the case that that were not
present
the users are behaving as they generally
would so so the numbers are the same
uh so i guess uh that's what i would
attribute to to the to the
uh to the decreased engagement um so
overall we've kind of investigated that
we didn't mess anything up and and the
data was right
uh there was an experiment being done in
another team with an instagram that
surfaced
different ways of notification sending
around stories to 66
of the global uh users and the results
of that experiment
are that if you surface notifications
not in a just-in-time manner but on a
on a kind of repetitive morning evening
or just afternoon basis
that the way in which people consume
stories then changes and engagement or
the number of users
interested in stories goes down um and
that's how i would kind of
wrap up my investigation and dig into
the experiment a little more awesome
great that sounds good i've got uh one
last question for you which is
uh knowing that you know say let's that
summary that you just provided will wave
our magic wand again we provide that to
the pm that ran this
uh notifications experiment um
as you're sitting there and you're
trying to wrap up this investigation
what would what would either uh
help sort of um
reduce your fears that this is like a
catastrophic issue for instagram overall
so if you expand your scope a little bit
versus going the flip direction saying
like
hey this is a really bad deal for
instagram overall and we need to turn
off
the experiment asap like how would you
think about that what's the last thing
you would
look at there what is some data you
would check to make that decision i
think
a number of daily active users is just
one way of looking at story engagement
okay however there's there's multiple
ways of doing so
uh so if we see um there's a couple of
things to it
uh number one notifications can be
intrusive that happen all the time
uh so maybe having less interruptions to
their day from instagram is actually
helped uh users in in some way or the
other
so i look at things like nps and nsat
score as a result of this experiment
to see whether instagram as a service is
now being is now being looked upon more
favorably
what that would mean to instagram as a
group overall
is that maybe the number of maybe the
engagement in stories
is is is down a little bit but when they
do click on that notification they spend
a lot more time on the instagram
product as a whole as a result of which
we're getting a lot more a lot higher
session times
uh the other ways in which i would look
at it and it's unlikely to be the case
because this is so user focused
is that probably leads to an increase in
ad revenue because if the session time
increases if you're just
if you have a dedicated amount of time
say at midday when it's lunch hour you
look at instagram for half an hour
instead of looking at it you know for a
minute and five times throughout the day
maybe you're looking at more ads and
you're clicking on more things yeah
so those are two ways in which i would
see that that can
be a silver lining or even kind of a net
benefit to instagram as a product
even though the engagement the stories
itself might be down a little bit
and then we can kind of compare and
contrast the two and if
overall the engagement for or for
instagram or the favorability of
instagram
or the revenue of instagram has gone up
then we'd still say that this experiment
is quite successful yeah yeah i mean i
think that where you ended is sort of
what i was thinking about which is if
stories dau is down but say
instagram engagement overall or
instagram dau is still
neutral or up and certainly you know
monetization which you mentioned if
monetization is up because the
accessions do expand
then yeah that could be a very uh could
be an interesting experiment that does
have some true benefits and it's a
trade-off
but um i think you did a good job
diagnosing the
root cause of that client all right
awesome thank you thank you for your
time
good work
thanks for watching i hope you enjoyed
that video if you haven't subscribed yet
already we've got a ton of great content
coming
out on both the consulting and the
product management career paths
on a weekly basis so go ahead and
subscribe and that means you'll get all
of our videos
as soon as they come up thanks again for
watching and have a great day
you
