---
source: https://www.youtube.com/watch?v=a8wrV3ISon4
vid: a8wrV3ISon4
title: PM product execution interview: Build an ad platform (w/ Google Global Product Lead and ex-eBay PM)
date: 2024-03-20
duration_sec: 2233
channel: RocketBlocks
kind: transcript
---
[Music]
today we'll focus on product execution
and how you would build and scale
different product systems uh but before
that you know I'll pause share about
myself and and love to turn it over to
you that's good uh awesome yeah so by
way of background my name is sta
Jovovich and I'm a global product lead
here at Google and we focus on building
and scaling data products uh at Google
we have nine core product areas and one
of the core ones is advertising and the
ads business is still uh I'd say north
of 60% of the overall revenue and it's
the whole ecosystem and data products
for us mean a lot of different things it
means uh zero to one it means uh
refactoring it means Tech enablement it
means change management and and the
products could be anything from uh
metrics and dashboards to chatbots to um
actual uh rules and policies with our
stakeholders and and my focus is around
data intelligence products it's ensuring
that um we can we can successfully
acquire and onboard different steps of
the ad platform uh and I really enjoy
the work uh here at Google because it's
it's incredible that you can make one
change or one refactor and a billion
users uh are impacted or one small
increment of like
0.1% change in a in a metric could could
save or generate millions of dollars and
so there's this outsized impact um by
building our life's work at Google and
and for me that's it's very meaningful I
just wanted to share that to give you
some context of why I enjoy uh working
here um prior to that I worked in a
variety of startups building and scaling
different data products um in the
private markets uh and had a background
in statistics so happy to be here and
happy to support you um I'll turn over
to you love to learn more about
yourself all right that was a great
introduction thank you um I understand
your role like Google and I understand
that you love it so clearly it's the
right place to interview with um I uh am
a product manager I've been a product
manager for several years uh I've done a
whole variety of different types of
product management you know b2c B2B and
I honestly really enjoy the B2B aspect
but I know Google um scale and the
ability for Google to bring together
large forms of information and really
make it accessible to everybody is what
Google really believes in and that's the
reason why I'm I'm interviewing for this
position you know I think all of our our
interviews are think about it like a
process as if you're working and we're
peers in the industry and and that's how
I like to think about the co-creation
and collaboration in each of our um
processes and so you know where you're
at today um in your stages is you've
already had um a phone screen with your
uh HR coordinator uh and you then
connected with uh our hiring manager
who's who's my boss right and and so now
where you're at is you're having like
one of these peer interviews where
you're speaking with a peer like myself
who could be a uh product manager
product lead who collaborates with you
on different work streams and different
elements of the product development um
throughout your interview process you'll
also be speaking with perhaps data
Engineers or software Engineers to see
what that collaboration would look like
on the engineering front um but today
we'll be um focusing on the product font
seeing a little bit about your thought
process and and so today's interview is
going to be a case study it's about
product execution there's no right or
wrong answer it's very much like a
hypothetical to see how you would
approach to solve a problem and we'll
we'll go down different um levels of
thinking uh throughout the
problem uh so here I'll give you the
highle prompt but before I just want to
check in uh any questions you have
before we get started no I'm ready to
jump in okay awesome we're excited to
have you here uh so our high level
prompt so today's uh case study is going
to be about of course ad platform so uh
as mentioned at the start of our our
conversation ads is still the the
largest um driver of of both product and
revenue and growth at Google uh but
we've been seeing in the last few years
a lot of changes in the ad
ecosystem um ad platforms today are
encountering a lot of um challenges from
from policy uh from from different
platforms and advertisers today have a
lot of different Cho CH uh to to engage
with their audiences and it's becoming
even more challenging to explore how do
you Target and retarget an audience how
do you um offer those advertisers the
right control um around data privacy
around ad creative and development to
ensure that just this whole endtoend
process about data collection is secure
safe and you know putting the advertiser
in control
so with that prompt in mind the question
is if you could share with us to start
how would you think about maybe
executing or or building a a a roll out
of some update to the ad platform that
would enable the advertisers with this
type of data privacy and control perfect
so when I look at an ad platform and let
me just say that clearly it's top
priority for Google because 60% of the
revenue comes from there and you
mentioned that that that's still the
case so when I think about an ad
platform I typically see view it as a
two-sided ecosystem uh actually
three-sided but two-sided which is
really the advertisers just like you
mentioned and the people who are
actually seeing the advertisement and
reacting to that or doing something with
that
ad uh of course it's a Google platform
which allows that interaction but I'm
mainly going to focus on these two
portions does that sound like a good
plan for you right now or did you want
me to consider some other
um uh people or um people in the
ecosystem that I might have
missed I I think you're thinking about
it just right and and for the case study
I think those two sided would be a great
uh Focus for today okay fantastic so
because the revenue is primarily coming
from the advertisers because they're
bidding on an ad and they're showing how
to surface that ad to a certain kind of
person um typically mindset would be to
prioritize them but I believe that the
priority should run and stay with the
people who are actually consuming the ad
because in the end more consumption of
ads results in the overall higher
revenue for the advertisers so I'm
actually going to focus on both sides
let's talk about both sides but I want
to start more with the people and the
demograph Graphics or uh special
parameters that this adds are targeted
towards because it really is dependent
on how much they react to that ad right
and most of the times the way people pay
for this is based on the number of
clicks based on the number of Interest
based on the time spent you know those
are the kind of parameters that you look
at so um let's talk about initially like
what would that look like right so I'm
going to split it up in kind of two
things one is a process of on wording
and one is kind of the tools that make
this happen right so so uh let's talk
about the process first right so let's
talk about the process for the um
advertisers and then we'll talk about
the process for uh the people who are
consuming this ad so let's talk about
advertisers so advertisers what do they
do what is top priority for them and I
think I always as a product manager look
at pain points first so the pain point
is I want to create an ad that is more
most effective and if I were to look at
a notstar metric the ad that actually
someone create clicks on and looks at
right
um so I would need to create an ad there
needs to be a workflow that actually
allows me to create an ad and then also
incorporate a review that is very very
fast so whether it's a manual review and
I'm also going to break out the review
process into two pieces one is automated
and one is manual right so there are
tools related to both of them and
there's a process related to both both
of them so an ability to create an ad
use a tool that will review the ad for
you
automatically uh also uh manually and
have the quickest turnaround in order
for you to be able to publish that ad
right so I can think of two things one
is there they could be a scoring system
right for the ad that really looks for
these safe words like maybe it's you
know uh it's politically charged content
or it's child pornography or something
like that and um this uh tool
automatically tags it and says well this
this is not going to work or it needs
further review you know that sort of
thing or there'd be a manual review
where someone actually looks at it and
says well does it go with my branding
does it like does it fit it Etc and kind
of approve that that approval process
has to be the minimal in addition at the
end once the review is done you want to
probably have Predictive Analytics to
say similar ads how are they successful
before and what was the click-through
rate right so that that's the first step
the Second Step would be uh there is a
compliance part and we'll talk about
that later but I want to keep the
solution a little simpler than including
compliance right now so that's the
advertiser processes and tools and then
think about what the viewer is seeing
right so there's a process for the
viewer tool so you surface a certain ad
to the viewer they look at it and they
say oh it's offensive to me or it's I it
doesn't you know it doesn't align with
my interest or whatever it is so they
could say I don't like this ad so that's
kind of manual there's a second piece of
manual process which is I actually don't
want to see it at all like there's a
preference dashboard per user that the
user can go to it should be really easy
no legal jargon like a Yola or something
like that just very easy flow to say I
don't like certain kinds of things or I
like certain kind of things or I'm okay
with certain kind of things right so um
that would be something that I would
focus on uh in terms of the automated
part uh the preferences will eventually
lead to automation because like I
mentioned every process and Tool has an
automated piece and a manual piece the
two manual pieces are in flow where the
ad doesn't pertain to me out of flow
which is the preference dashboard both
are manual and then eventually PR
dashboard leads to automation so that's
that's the flow that I'm thinking about
I'm going to take a pause here did I
miss anything and does it feel like it
resonates with
you I like what you're you're sharing um
pavi talking about like customer user
journey I think that's something that
I'm I'm hearing you're talking about
like all the steps through your
workflows so that's really great to see
both the manual processes where often
you know Google will have a trust and
safety team that will need to uh have
human ERS to to review and ensure that
um everything is is factual or just for
compliance standpoint so I like that
you're thinking about both keeping the
human in the loop as well as of course
the automated processes thinking about
at scale so I think that's highly
effective um I I'll let you continue for
now okay great so in terms of drilling
one step down which is just like I
talked about automated versus
verification manual verification so in
terms of AD review
verification um and following the whole
workflow there are of course AI models
hot right now so I'm going to talk about
that first which is we utilize a AI
models to decide on what violations have
happened in the past what does the
system know already and how can it
predict to say but it's inappropriate
imagery or copyright or whatever the
case may be right so you could use that
that's solution number one solution
number two is actually something that
people don't necessarily think about but
it's very valuable which is uh you can
actually have third party people do this
for you you can pay them and they do
have Specialists and experts actually
review this for you because they are
trained in in such a way that they can
actually figure it out faster so if the
success criteria is to make the review
process shorter and the publishing times
shorter that is a very good way and you
could have a REV share model with these
Partners to say um if we are mitigating
certain threats and copyrights or PR
issues they could get a cut from there
so that's second the third one is really
the feedback mechanisms that um users
provide to you and keep a track of that
so I hadn't talked about that earlier
which is the user actually says that
it's inappropriate or doesn't like or
reports it back you probably track it
very closely to say per week or per
month how many people are reporting and
that kind of goes into the Quality
Control process and that kind of feeds
into the overall model that says next
time we probably won't surface these ads
to these type of people right so that we
hadn't we hadn't talked about that we
had talked it at a per user level but we
didn't talk about the broader ecosystem
right so I'd say that would be important
um it's a part of data and data
collection so I thought I'll make sure
that I say that um in addition I would
also say that if we were to execute it
faster and let's say we've come up with
these Solutions and these Solutions are
okay with us which is the AI modeling
with the third party review with user
feedback and user preferences there are
probably four solutions that I just
talked about I would like to prioritize
two of them because I think for this
interview I don't think we'll be able to
figure out like everything so um I would
like to prioritize the uh AI model for
advertisement review and the preference
dashboard for the users because
eventually preference dashboards would
make it automated because let's let's be
real the biggest pain point for users
today is my data is being used somewhere
that I don't like and there is no
transparency of that right so users
don't know what did I choose what did I
don't choose did my did I sign my life
away really why am I seeing this ad it's
irritating versus whatever so um if you
think about it it's really dependent on
what you've done in the past and also
your preferences so I'm going to focus
on the preference dashboard and I'm work
going to work on the AI tools uh part
for advertisement
review all right so let's talk great and
I think what I hear from here is that um
this like AI uh uh tools will be focused
more on the advertiser side and is the
preference dashboard is it also the
advertiser side or is it more like you
or I if we have the ads like would I
sign in and view my dashboard and toggle
on and off different ad preferences just
love to see um if that's what what you
meant there yeah that's what I meant so
I wanted to have a solution for both
sides of the ecosystem maybe I should
prioritize one of the other but I think
both are equally important in this
situation even if advertisers are the
actual Revenue generators so what I'm
talking about here is the users the end
users who are actually viewing the ad
their preferences because one you're
mandated by compliance right CPA
California privacy act as well as gdpr
requires you to do that you're you're
supposed to provide a preferences
dashboard where the user can actually
toggle on and off to say I want to share
my data I don't want to share uh this
typee of data I don't want to share my
name or I want to share my age you know
that sort of thing and kind of make it
simpler say about me about my
information about my interest like there
are different categories that you could
think of where you provide them that a
way of easily giving them the option of
opting out or opting in actually you
know and I have some ideas around
optigan so uh we can talk about that so
let's first talk about the AI model
which is question I'd love to check in
on um before we dive into it so I think
P you hinted at that you wanted to
prioritize uh these two ideas the AI
model uh and um the focus on this this
uh preference dashboard out of the four
um could you tell me a little bit about
your your process and how you would um
prioritize these two or stack rank
against the four total ideas that you
suggested yeah uh the reason why I chose
these two ideas is because typically I
prioritize ideas impact times reach
right it's a very simple equation I
that's the framework I typically use um
and pain the depth of the pain okay so
as we are going along in this AI world
and advertising world people have
stopped trusting ads as much and
typically people will skip ads like if
you look at the number of people who
Skip ads in YouTube or you know people
who do who scroll through it's becoming
higher and higher because people feel
like they're their data is being used to
their disadvantage and not to their
advantage right and there's a lot of
pain around this like people are more
vocal about it people are
also feeling a little distance and that
which is the reason why social media is
losing its losing its star power pretty
much so um I want that's why I wanted to
prioritize a preference dashboard
because the users want more transparency
and it the fact that they want more
transparency is not just because they
don't want to see something it because
they want to probably be compensated for
the data that they've been sharing right
so I think that the landscape has
changed significantly just in the last
two years and which is the reason why I
was prioritizing that also the pain is
also increased like there's a lot of
talk and why did gdpr even come into
place right because because of the
discontent of of users right so that's
one and also concerns about privacy like
everyone wanted to share everything on
social media 12 years ago and now that's
not true true okay so that's one the
second piece is the advertiser piece
which
is advertisers just want to sell their
product they want to get to the maximum
number of people and they want the
largest amount of
conversion they don't want to review
their ads they don't want to review and
make sure that okay oh my god did I
violate something and they didn't they
don't really know even some of the ad
makers don't really know that like
they're just bidding for an ad but
they're not they're not really they
don't know about all compliance stuff
they don't know everything about
everything really they expect machines
to help them out right to make their ad
the best that's out there to get the
most views that are out there which is
why I focused on the AI model for the
advertisers but more human accessible
model for uh for the
viewers got it that that makes a lot of
sense and so um so with that in mind you
know taking these two ideas uh I'm sure
this is where where you are going to
towards but like let's let's describe
your your execution plan like what would
that look like for building out these
systems uh for the data and AD
preferences for the accounts and and as
you go about that how would you balance
that transparency and control I think
you've hinted at it earlier but to build
that smooth user onboarding and user
experience during implementation perfect
I don't have the perfect design because
the designs vary quite a bit um I can I
can only speculate and which I think I
hinted at earlier which is better uh
compartmentalization of what type of
data is being shared on the preference
dashboard as well as probably giving
hints along the way about what other
people of their mindset have chosen
based on their previous usage that would
be really that would be something we
should think about but more importantly
the way to execute it would be one to do
ab testing that's what I've always done
as a PM right so I would choose certain
set of users and surface some this
preference dashboard in flow when
they're actually interacting with your
system and say that well we have new
preferences for you which will give you
either better ads or give you other
options related to ads and I'm thinking
of ads also the way they impact people
in multiple ways one i' I see a category
of people who want to see relevant ads
who actually want to use that for
discoverability right so for those type
of people your preference dashboards
looks slightly different than some
preferences above the four looks
slightly different right the second
category I don't want to see ads at all
and in that situation obviously there's
a balance right like you are charging
your advertisers to show ads and if
someone doesn't want to see ads at all
that model doesn't work for you as a
business so in that situation if someone
really chooses that they don't have any
other option but to say I'm going to pay
for your platform to even view right
that's option number one option number
two is I'm okay with seeing the ads but
I I need to know where my data is going
or the advertisers need to pay me
directly if they want to see my data
that would be a really big win-win
situation yes Google or another ad
platform may not make all the money that
they make today but even providing a
little cut for the person who sharing
the data is quite valuable uh so I would
say that might be a good win-win
solution for both in the preference
dashboard saying that I don't want it at
all and I'm going to pay for the
platform or share a piece of the pie
with me and you know let's take it from
there so um I think that's a pretty good
model we could test it with different
types of users again AB testing so for a
period of time for example for three
months for a quarter I would share it
with the first type of people who want
to see ad but want to see relevant ads
and tailor the preference dashboard
based on that next step would be for
people who don't want to see ads at all
what would they do if I give them that
option maybe we will we have to we have
to make be aware that they might leave
our platform alog together and the
leaving of the platform might be of
concern so you you probably tried out
for Le less number of people um even
before you get to the AB testing what we
used to do in eBay while I was a PM
there uh we would actually test it on
focus groups focus groups tend to be a
little not the most accurate way of
predicting predicting the outcome and
the reason is because it's so dependent
geographically the mindset of the people
and the sample size is very very small
right so I like AB testing better than
focus groups but focus groups could give
us an early indicator of what that might
look like so that would be the execution
plan for the preference dashboard for
the advertisers um I have a slightly
different approach which which I've
tried before and has
succeeded so because advertisers tend to
be businesses and they are a little bit
more open for training I would do a lot
of webinars or have these seller
conferences or Advertiser conferences
that I host as a platform and train them
on what these tools might look like and
how these tools work in the background
right we explained to them that you can
just create the ad we're going to make
it super easy for you but here is the
workflow that you'll have to do and
here's the turnaround time that you'll
have to wait for it'll be an AI model
but eventually you will have to do your
own review if you want to pay for a
manual review later we'll take extra
payment for you you know that sort of
thing so there has to be some sort of
training for them and typically they are
open to training because they want best
outcome and the best success
rate
it's really it's really interesting how
you've you know described both of these
these uh Solutions pav I think you
brought up a lot of really strong merits
around uh I think granularity uh of
toggling different um uh features right
for both advertisers and users and and
different ways of collecting your data I
think that's one of the core elements to
ensure that the data is not simply uh as
a PM based on our thought process but
more so driven by data so I think I
think that's really commendable that you
brought that approach uh um to the
interview um uh but some thoughts I have
in addition to that as as you're
describing this is uh you made a couple
call outs that I'm curious and I want to
get some more thoughts from you on this
um one of them was about uh paying for
manual review so um you know I think
generally in the Google EOS system our
goal is to um gather the world's
information and make it accessible for
all um so uh can you share more about
like um this idea or or where would that
um be would that be Google paying for
this manual review with advertisers how
would you see that uh that's a very good
question so I do have two ideas around
that uh the first idea in order to
maximize benefit would be the third
party manual reviewers they actually pay
Google
if if their manual review succeeded and
uh there's a certain threshold of money
to be made from that ad for the
advertiser itself or The Advertiser
decides to pay them a cut right so that
would happen the other way to do it
would be actually crowdsourcing Google
could pay um certain set of agencies
like three or four agencies a very
minimal amount to do this because they
can eventually further their ads later a
business so I would I would look at two
different ways of doing
that yeah and I I I like how you just
called out blav about crowdsourcing as
you may know historically um Google is a
big proponent of crowd sourcing through
its products of course we know in like
Google Maps reviews where you'll be able
to you know get surface better insights
based on the content and the the up
worthiness of reviews uh so that I think
could be a um
an aligned idea ac across the business
um one other uh call out that you
mentioned was about uh there could be a
a potential risk uh of Google losing
money with some of these Solutions so I
was curious um perhaps if you had a a
creative solution around how to or align
with what you shared about continuing to
preserve the data privacy but without
Google losing money because that's
definitely you know as as a a core
driver of our business we always are
trying to make Google ads grow in
Revenue as opposed to losing to
competitors so I think the cost then
would have to be forced back to the
advertisers to say you will have to pay
the end user for the data if you really
wanted the better ad so Google
essentially would still be a platform
they aren't they aren't really losing
very much they are they're directly
getting revenue from The Advertiser
themselves but the costs are passed back
to the advertisers uh I don't know the
so as over time if you're going to see
less advertisers because of that reason
uh that's one potential that'll have to
be tracked year over year I think
short-term metrics will not drive that
um there is another way to look at it
which is over time with the amount of
data that you have if you're still able
to do predictive and get better and
better outcomes and show the advertisers
that you're getting better and better
outcomes just with predictive and
analytics and AI models that might still
work out in your favor in the long
term that's great and I appreciate the
additional context you shared there
about um looking at different approaches
and identifying the trade-offs right we
don't know in in this case study today
which one's right but I'm sure with some
data and further analysis you you would
drive that home and and and have that as
part of maybe your your PRD and and some
of that to share uh with with your team
members there's one more thing I'd like
to mention sorry uh there one more thing
I'd like to mention which is like I me I
I did mention it earlier but I think it
kind of got lost in the overall
conversation so I apologize for that
which is you do ask the users to pay for
using your platform so if you really if
they don't really want to share the data
Google still makes money in the end
because the users are saying I don't
want to share my data but I'll pay to
use your platform and that's really been
actually that's been mentioned many
times over the years over the last last
10 years or so uh and no one has had
[Music]
the uh mental strength to try it no
business has had that strength to try it
and it might be something that the the
world is ready for right
now that's right and I think pav you're
you're mentioning a good call out to one
of our other products um as we may have
seen in the last year or two YouTube has
rolled out a very interesting pricing
model where you know you could um
subscribe without ad
uh and so it sounds like you're hinting
to our other product lines that are you
know giving users that choice though
through through a paying to to not have
those at surface that's a great uh call
out and thanks for noticing that in our
other
offerings um so let's go let's go into
one more final section I know we're
we're getting tight on time but it's
been really helpful um this one we can
keep a little short but from everything
you've you've synthesized and brought
together on these can you share a little
bit about what the go to market strategy
would be then for rolling out either or
both of these features yeah so the way
I've done it in the past and I've come
from a very B2B background so please
excuse me uh the biggest thing that I
always do is beta testing right that is
a true qualifier of what this is going
to look like how people are going to
receive it and do the whole iterative
development process so I have a
specialized team that I'll typically set
up for beta testing there's an engineer
who's who's completely dedicated to the
beta testing
piece for each of the Fe feature sets
that we roll off we start we first start
with figuring out who those people are
that we are going to surface this test
to and then um add these two different
types of formats or different types of
things that we have allowed for
review um in different environments and
test it week over week and track our
metrics week over week and the metrics
for advertisement review could be very
simple thing like I mentioned which is
the quickest way of revieww either AI or
manual um and GA feedback from the
advertisers in the end to say okay
here's a survey for you you participated
in our beta test one what did you like
or dislike of other product and then
secondly really did it meet your needs
do you feel like this is this is going
to work for you so beta testing is one
option and the second option is to do
itera development as they're going
through the product as they're going to
the usage of the product either
preference dashboard or um the review
process you take feedback from them on
an ongoing basis so it's a research
search slba testing
effort I think that's so important right
I always think about uh the the
different levels of a roll out right it
could start with as you're saying this
like pilot where you're Gathering that
feedback and and um and I guess the
question I'd be curious about is is why
is this so important you gather this
feedback but but then what let's say uh
some users or Enterprise customers come
back and say um you know laa you got
eight out of the 10 but but we you know
we got this data issue or we're we're
missing this other requirement now what
what what happens next I think it's
that's also another very important point
it depends on how far or deviated from
the original predicted metrics you are
okay so typically you will you do the
020 rule if it's meing 80% of the
customers's needs you do end up rolling
it out with the contra
knowledge that n amount of dollars are
going to be lost because 20% of the
people aren't really happy the second
piece of that is really if the 20% isn't
the happy why aren't they happy and what
can we do about it what could what could
The Tweak in the existing design be that
could meet maybe five additional percent
of of these users Your solution will
never meet 100% of the users I mean
that's just the reality you know so you
basically launch and have the best
intent and provide a way to onboard the
20% who didn't really agree with the
solution so that's that's really how I
approach any business problem and again
metric say it all it has to be year-over
year it has to be a long-term indicator
versus a short-term indicator change is
never good for anyone uh nobody really
adapts to change that quickly so and
understanding that change management
takes time also is a very important
piece of
business H yeah I think you did really
well here um pavi talking about the
endtoend process from you know the early
parts of our our case study today about
Gathering the the general requirements
and thinking about this holistic problem
of data privacy from the two-sided
Marketplace then you uh prompted or
suggested four different solutions where
you stack ranked and prioritize down to
two that you'd like to focus for both
The Advertiser and the end user um you
then share with us perhaps what some of
those features and and product updates
would look like and the data components
that would measure privacy and then um
you covered trade-offs like what could
an alternative universe or products be
if there were additional expansion
opportunities or more engineering
resources to further build and
complement um Your solution uh in fact
you spoke about uh one of the core areas
of product management which is feedback
and constant
Gathering that and and knowing that no
product is is finished on day one and
even on launch day right but we're we're
constantly launching and landing and
shipping and and making those
adjustments and as long as as as you
suggested Gathering that feedback that's
that's a great way to ensure you uh
build consensus and broader alignment
with your stakeholders um yeah I'd like
to pause there check in um see if you
had any concluding remarks or additional
comments
thank you it was such a fun interview I
I really love interviewing with Google
because of that reason because the
problem statements tend to be really
Broad and to break them down um it's a
it's a skill set uh and and a PM is
essentially expected to have that skill
set so just in terms of closing remarks
I wanted to mention that you don't even
have to prioritize both Solutions or
really both both sides of the equation
at all uh based on the LI resources
based on how how much bud
you're you're planning to spend on this
you could easily prioritize one or the
other and see how it goes so I
prioritize both because I feel like both
sides of the ecosystem are really
important and to be very fair if I
really had a choice because I'm very
geared towards a consumer I'd probably
go towards the preference dashboard
because it's just much easier to roll
out it's not in your face all the time
people have to go there to actually
access the preference dashboard and um
surfacing that is a much easier cell
because form design is much better
better than AI modeling so I I in terms
of closing remarks I would choose
that and and I like how you spoke to
that because sometimes it's about
getting those quick wins or building
broader consensus and Alignment um
perhaps over multi- quarters you'll
build all for Solutions but we have to
see um how you can hit the ground
running so um P thank you so much for
your time this is our our interview on a
peer product management you know I'll be
uh connecting with our team to to share
some notes and they'll get back to you
on next steps with the process thank you
David it was a
pleasure oh thanks so much have a great
day hey everyone it's Kenton gaves here
the founder of Rocket blocks thank you
so much for watching this mock interview
video I hope you found it informative
and helpful as you are getting ready to
prepare for your own interviews and
hopefully Landing that job offer you are
excited about we have a ton of great
content on the rocket blocks Channel
coming out on a weekly basis mock
interviews mini lessons and chats with
our rocket block expert so if you
haven't subscribed yet already please do
so there is a big red button below and
if you hit that you'll get all of our
content as soon as it comes out thanks
for watching and have a great
day
