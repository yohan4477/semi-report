---
source: https://www.youtube.com/watch?v=fPp8GQnGUg8
vid: fPp8GQnGUg8
title: OpenClaw Makes AI Agents and CPUs Get Real
date: 2026-02-03
duration_sec: 2854
channel: Semi Doped
kind: transcript
---
just tell cloud code your problem.
That's how I started. I was like, look,
&gt;&gt; I have a lot of newsletter emails. I I
read a lot of news sources. So, what do
I do with all of this? Give me a
workflow that, you know, sorts all this
out. So, it said like, yeah, I'll give
you a slash news skill. All you have to
do is run / news and it'll create the
digest for you. I'm like, yeah, yeah,
awesome. Do that.
Hello listeners and welcome to another
semi-doped podcast. I'm Austin Lines of
Chipstrat and with me is Vic Shaker from
Vick's newsletter. Today we're going to
talk about agents. Um, so the framing
for this is I feel like 2026 is actually
going to be the year of agents. I think
even as far back as 2024, there started
to be some marketing speak where lots of
companies said agent AI is all the all
the rage and it's the thing and everyone
should get on the bandwagon. And I think
a lot of that was very aspirational and
visionary, but it feels like now, as
we'll get into with things like Cloud
Code, Cloudbot, and so on, I'm actually
seeing lots of people tinkering with
agents. So, more than just marketing on
a PowerPoint, but I'm actually seeing
people play with this stuff. So I
thought Vic and I we could kick off the
conversation chatting about agents and
then we will get into like what are some
of the implications u for CPUs for GPUs
and so on from an in infra
infrastructure perspective. So, okay,
enough of an intro. Vic, let's start
with you. Uh, agents, what's top of mind
for you?
&gt;&gt; Yeah, so the agent thing has become
quite a revolution on X. Like, everybody
has declared that it's over and now the
age of a agents
is upon us. And also, I'm not sure what
we should call this tool that is now
this great agent that everybody's
talking about because it started off as
Claudebot, but then Claude decided it
sounds too similar to their product and
uh then they changed it to mold bot and
then now it's again changed to open
claw. I think this is what the final
product is going to be called. So maybe
we should refer to it as like open claw
so that this podcast makes some sense
even like a few months down the line.
&gt;&gt; Yes, totally. Okay, we'll call it open
claw today. We'll see what if it
changes.
&gt;&gt; Yeah. Yeah. Yeah. Yeah. So this I saw
this really funny YouTube video. Um
uh he's he's a software programmer. I've
seen his YouTube video for years and he
calls himself the primogen. So, you
know, if anybody's watching this, you
should go and like pause this for a
moment and see his claude code. Uh, not
his Claude code, his his open claw video
that he has. It's like really funny. Uh,
but uh, essentially, it's just like all
these agents are like doing random
things like it went and lost money on
the crypto market and then posted on
LinkedIn, I lost $1,600 in the crypto
market and here's what I learned.
[laughter]
&gt;&gt; Oh man.
&gt;&gt; So, it's ridiculous. So, this kind of
stuff is like really hilarious. The last
week has been awesome. Just simply
awesome in the world of technology and
LLMs and AI. [laughter]
&gt;&gt; That's good. It's uh it it's so like
LinkedIn clickbay type sounding, you
know, like I did a thing and now I'm an
expert. Let me tell you about it. That
it's it's like almost mockery. It's
hilarious.
&gt;&gt; Yeah. Yeah. And it's it uh was all
posted on this like Reddit uh equivalent
for agents called mold book. So these
like agents go and they post on mold
book uh like humans do like they're
writing a LinkedIn post. It's just a
mess. I'm like why are we why are we
spending all this infrastructure in GPUs
and burning down a few rainforests so
agents can like get on social media like
as if it weren't bad enough for humans.
&gt;&gt; Right. [laughter] Right. Totally. Yes.
uh the experimental stage we'll say that
&gt;&gt; yes indeed indeed. So let's start with
cloud code which when I think of like
agentic AI coding I think of cloud code.
Um tell me are you using cloud code? How
are you using it?
&gt;&gt; Yeah so the thing is with cloud code for
the longest time I never gave it a whirl
because I don't do programming for a
living and so I was like what I mean I
guess it's a coding tool whatever I
don't need it because I'm not coding
anything. And I know programmers have
been using it for a long time and doing
it's been doing a lot of good stuff for
them. So I was like I don't know I never
use it. But then recently I saw videos
of stuff and people talking about how
cloud code is so much more than just
coding and then people use it for other
things. And the creator of Cloud Code
himself said this on an interview. So I
was like okay maybe now is the time to
do this and I'm not scared away by like
a Linux terminal or whatever. I'm okay
with terminal. So I was like, fine,
let's let's fire this up. It's pretty
easy. So I all I did was like, you know,
installed cloud code based on the
instructions on the website. It works
right off the bat. So it's on my Mac,
you know, I installed it on my Mac
terminal and I use it on that. So it's
it's pretty neat actually. Um, so I have
the $20 subscription and I've been using
it fairly extensively even based on
that. I at one point I like got locked
out of Claude Opus. Uh and I've been
using Opus the whole time. I could have
used Haiko or Sonnet. I didn't. I was
like I just want the best model. Let's
see how much it goes. So almost for a
week's worth of work for my use case, I
think the $20 was enough, right? So I I
got some use of it. Like I've been
starting to create some
skills and like running it and helping
it do some of my research. um it gives
me information quickly. So yeah, it's
pretty cool.
&gt;&gt; Okay, say more about how you're using it
and which let let me pause really quick
and say that it's you point out like a a
funny like branding problem. It's like
called claude code. So you're just like
ah I'm not coding so I don't need this
thing and they're it's kind of like no
no no wait it can do more which I know
that uh anthropic has kind of tried to
get past that with clawed co-work I
think it's called putting into the guey
where you know normal people live let's
say you know and giving it a lot of the
same
&gt;&gt; uh tools have you and and so I guess
another question too so tell me more
about how you use cloud code but have
you thought about also using that in
cloud co-work or do you just stick with
cloud code because Do you like the
terminal command line feel versus a
guey?
&gt;&gt; Uh I'm okay with the command line feel
actually. I like it. So I'm so I
actually use that. The cowork aspect of
it I have not yet gotten into because a
lot of the files that I work with at
least for the newsletter and stuff is on
Google workspace uh and Google drive. So
I don't really need to access local
files as much. But I can see if like
cowork you know if you give it some
control over your computer you know it
could reorganize files on your computer
this and that kind of stuff.
&gt;&gt; But that being said I really don't like
giving machines control over my
computer. I just
&gt;&gt; Yes.
&gt;&gt; Because you know this thing is watching
me. I I feel like I'm being watched
&gt;&gt; and I have my password manager which has
like a master code
&gt;&gt; and like everything in my life is past
that. Totally.
&gt;&gt; I'm like, I I'm not going to type uh
anything while my agents are watching
me.
&gt;&gt; Yeah, totally. I mean, think about it.
If you hired interns to offload work,
you're not going to let them use your
computer, right? You're going to give
them their own computer.
&gt;&gt; Yeah. Yeah. A cloud code isn't uh
running, you know, it's it's within the
the terminal window that I'm using it,
but it doesn't have general access to my
computer. If I kill the terminal
session, it's it's out, right? like now
no more.
&gt;&gt; So for you it's almost like a sandbox
thing too. It's like hey it just lives
in the terminal. It can't see
everything. It does its thing there and
then I can kill it when I'm done.
&gt;&gt; Yeah. So the way I'm using it is
actually uh I have hooked it up with a
Google Drive MCP server. So I run that
and on a local Docker container on my
Mac. So you can get download Docker for
desktop. I think it's there for Windows,
Mac or whatever it is. And then you can
get the Google MCP container from the
Docker registry and you can just like
run it. And what that does is it creates
a link between the
uh Google Drive on you know Google
server and your local cloud code session
and MCP if people haven't heard about is
model context protocol. So it's kind of
like an API for LLMs that you can like
plug into. So with this thing, I can
actually look at my emails. I can look
at my uh files on Google Drive and I can
look at my calendar. So I can ask cloud
code, tell me what my week looks like.
It'll look at my calendar and give me
an, you know, something like that. I I
could go look at it, you know, whatever.
But I could also never leave Terminal
and be like, hey Claude, you know, can
you add this appointment at this time?
And it I don't have to switch windows at
all, right? So it just goes and adds a
&gt;&gt; Okay, interesting. So yeah, I was going
to ask like, oh, why are you connecting
to Google Drive when you could just put
files locally, but it's not just Google
Drive, but you're accessing your
calendar and your Gmail. So that that's
pretty awesome.
&gt;&gt; Yeah. So that's a very good point.
Actually one thing that I ran out of
tokens doing is trying to put the files
uh that claude code creates like let's
say I ask it to research something for
me and create a report or something just
so that I can read it and understand all
the news of the week. I have a skill
like that.
&gt;&gt; But then what it does is it spends all
this token authenticating with the MCP
and I have to copy paste this thing into
a browser and I have to click okay
there.
Then I was like, "Oh man, I'm just like
dumb." Like Austin figured it out in
like 1 second. I should just save it to
my local Google Drive folder and then
that will sync. So that's then I asked
Cloud Code like, "Hey Cloud Code, don't
sync it to the online version. Here is
the folder locally. Just put it there
and it'll sync on its own." So it does
it like it it then takes care of the
changes, right?
&gt;&gt; Nice. Yes.
&gt;&gt; Yeah.
&gt;&gt; Good. Good. So you you mentioned you've
got like a skill for reading the news or
summarizing.
&gt;&gt; Yeah. Yeah. So what I told it is like I
have all these Substack publications
that come through. By the way, when I
say this, people are going to do this to
our our publications. So it's probably
not a good thing, but it helps, you
know, it helps. The reason it helps is
that I just want to get a sense of what
the article covers uh without having to
open all of the Substack publication
emails I get and then have a quick
summary of what is in there and then I
can go and read the whole thing if I
find that it's relevant or what because
I store it on a Google doc or a Google
file drive uh all these news summaries
it now becomes searchable because
Substack search is so terrible. So if I
just go and ask claude, hey, look in my
news folder and tell me the substack
that I remember seeing sometime in the
last couple of weeks that spoke about
this particular thing and it will
surface it for me and there is the you
know it short summaries there too and
now I can go read the original thing. So
it's kind of a note takingaking thing.
So what I asked um Claude code to do was
I have all the Substack emails coming
into my Gmail folder labeled like
newsletter and then I asked it to go
read all the emails tagged newsletter
and then it automatically decided to tag
them as newsletter processed you know
and it tag tags it another tag yeah it
says like I'm going to tag it process
because if I do this next time I will
not you know resurface this because it's
already summarized for you, right? So,
it's very clever that way. And it said
like, look, I'm going to put this
newsletter process tag as hidden in your
Gmail uh so that you don't always see it
because not relevant really. So, it put
it it created a new tag label and hid
it. It's very beautiful. It makes really
good choices.
&gt;&gt; Yeah, it's really thinking deeply for
you.
&gt;&gt; Yeah.
&gt;&gt; Okay. Interesting. So, it's reading your
email to get access to all your
Substack, which is good because I was
thinking like, oh, do you have it
authenticated to Substack? How does this
work? Um, technically, it can only read
the entire email. So, for all of the
Substack newsletters that are too long
and get truncated, uh, it's obviously
going to only read what's in the email,
but then it's it's even cleaning up
after itself for you and and tagging it
as processed and hiding it. That's
pretty amazing.
&gt;&gt; Yeah, it's pretty great. And now the
thing that you mentioned about
authentication is interesting. This is
kind of unsafe what I'm doing here. But
I have certain new subscriptions uh that
I pay for and those things I I just gave
cloud code like the login and password
and be like log in on the website and
then get me all [clears throat] the
information on the paid articles
because you know digit times is one
example right because if you go to digit
times and you don't have a pay
subscription a lot of the articles are
just completely payw wall like there's
not even a single sentence over there
&gt;&gt; so this thing goes logs in and then
reads
Wow.
&gt;&gt; And then summarizes it for me.
&gt;&gt; Amazing. And it and it and it works.
&gt;&gt; It works great. Yeah. And I told it like
what I'm interested in too because I
don't want all kinds of news articles.
So I said, "Hey, in the following areas
like like I like photonics, I like uh
memory. I like interconnects. Whatever
that I think like semiconductor like
capex like semicap stuff uh ASML that
kind of news foundry stuff. So it made
it, you know, you can tell it like here
are the topics I'm interested in and
then it goes and creates its own files
and keeps it all uh organized and
deletes lines and adds lines whatever
and keeps it all like great. Yeah. So it
only surfaces the kind of information I
want, not everything because then it
becomes useless, right?
&gt;&gt; Yeah. Yeah. Yeah. And so is it writing
all these summaries locally? It's like a
markdown file or something.
&gt;&gt; Yes, exactly. It writes it in a markdown
file on my local uh Google Drive folder
which is which I read with VS Code.
Maybe I should find a better markdown
here but I just read it in VS Code.
&gt;&gt; Uh but you know if you go to Google
Drive it doesn't maybe I don't know
there's like a plugin I try to install
that reads markdown but it's just
cumbersome because it's not a Google doc
file and you can open a markdown file as
a Google doc file but it's just too much
work. I mean it's already on my
computer. But I just like open it and
I'm okay.
&gt;&gt; Totally. Yeah. I use some app locally
called Bear, I think, uh to to view
markdown. But m hey, maybe maybe uh a
agents will drive markdown to get better
support in like Google and whatnot.
Become a first class citizen if you
will.
&gt;&gt; Yeah. Yeah. I mean it's fine. And then I
told it like one, you know, all these
like small optimizations I did later
because I was like it tries to go
through the it creates the entire digest
and then it realizes it can't connect to
the Google uh MCP server and then it's
like I don't know like it's just hanging
out and did write any files and so I
told it next time make sure you can
authenticate first before you start
doing anything. If nothing happens let
me know. I'll fix the authentication
then you can go read my substack emails
you know so I save tokens otherwise I
like I just waste time with token like
thinking through all this stuff and then
it can't write the file you know
&gt;&gt; totally totally so it's both a genius
but also can't think for itself and you
have to tell it like hey
&gt;&gt; you're optimizing for tokens here
&gt;&gt; yeah sometimes it's really smart
sometimes it's like ah why didn't you do
the obvious thing but for somebody who's
thinking of like doing this kind of
stuff I would not even re recommend like
going through any guide just ask just
tell cloud code your problem that's how
I started I was like look I have a lot
of newsletter emails I I read a lot of
news sources so what do I do with all of
this give me a workflow that you know
sorts all this out so it said like yeah
I'll give you a slashnew skill all you
have to do is run slashnews and it'll
create a digest for you I'm like yeah
yeah awesome do that [laughter]
&gt;&gt; nice amazing that's pretty awesome I
&gt;&gt; it's interesting because to you to
generally today or yesterday it used to
be you know anytime you want to start on
something you like look for the tutorial
and you hope someone wrote a good
tutorial otherwise you're fumbling
around and now you can just ask claude
and let it essentially guide you
&gt;&gt; yeah having been trained on all sorts of
previous tutorials it's a probably a
good teacher at how to walk through and
do this stuff
&gt;&gt; yeah I also created a couple of other
skills I said like I have a slash topic
skill so what it does is it looks
through all my news articles and looks
at all the stuff I've written and if
there's any possible extensions so it
gives me a few suggestions like hey you
should look at this look at this has
happened in the news you kind of looked
at your newsletter because it can go
read at least the uh article top you
know whatever is before the payw wall on
my you know newsletter itself on
substack right uh that part is open so
it goes and reads substack and it reads
the news folder on my Google drive and
tries to form some links and stuff like
that playing with that it's not really
useful in a sense because it's very it
gives me very obtuse ideas. I don't
know. So maybe I have to work on this a
little bit. It's not as good as I would
like it to be.
&gt;&gt; Gotcha. And uh
how do you decide how much time to kind
of sink into this and if it's worth it?
&gt;&gt; Yeah, that's a good point. I have uh
spent time on these kinds of things and
it goes nowhere. uh like in the initial
GPT days I tried creating various like
what was it called? It is like a skill
but uh it's like your own subgp so to
speak. [clears throat]
&gt;&gt; Yeah, I tried making those but then you
know I couldn't keep them up because
each one had a system level instruction
and then it didn't evolve with my style
or anything like that. So here I like
this because it's like an all-in-one
thing and I improve it as I go. like I
don't spend too much time on it. Like if
I'm doing something and it's coming up
that I'm doing the same thing a few
times and I ask Lord Code to go make
that a skill or something and then it
doesn't maybe do a great job of it which
is fine because at least it got the job
done for now and later on I'll kind of
add skills or tweak the skill and all of
it happens like I'm telling like telling
you you know like oh you know I don't
like this do that you know change this
change that so it goes and fixes it.
Yeah.
&gt;&gt; Yeah. So because you've been tinkering
from the early days of making like
custom GPTs or whatever they called it
to now with cloud code and it it sounds
like now you feel like you can talk to
it more in natural language
&gt;&gt; and it's mostly helpful and sometimes it
burns tokens but generally speaking you
can actually start to like automate some
workflows. Um do you feel like we're
starting it back to the year of agents
theme? I mean, do you feel like we're
starting to get closer to a place where
people who want either are less
techsavvy or don't want to invest so
much time tinkering, you think we're
getting to a place where they can
actually start to create agents and tool
around and experiment and find value?
&gt;&gt; Yeah. Yeah. So, yes and no, right?
Because right now you have these things
like um open claw which takes clawed
code to the next level right and it is
not as simple as people think if you're
not used to like uh do dealing with a
little command line stuff here and there
and the only reason I say that and let's
go into open claw for a little bit now
because first of all anybody listening
to this don't try open claw on your
laptop because literally when you see
the website, it tells you all the stuff
it can do and it's terrible. Like it's
like handing uh you know unlocking your
laptop with a password or your Touch ID
and handing it to somebody else. Would
you ever do that in real life? You
would. So that's that's actually what
OpenClaw does, you know. So don't unlock
your computer and give it to an LLM.
It's crazy to do that. Uh because it has
everything like on your laptop. So the
way people have been doing this is
they've been buying these Mac minis
because they're kind of powerful
machines. They have fairly large number
of resources and maybe you could even
run a local LLM on it. And we'll come to
why that is a little bit later. But then
if you don't want to spend like I don't
know like hundreds of dollars on a Mac
Mini. I don't know what kind of Mac
minis these people are specking up on
it. Could get expensive. But the
simplest way to begin is to go and get a
virtual private server, a VPS. You can
get those like for like $5ish
and you'll get a like a little Ubuntu
terminal and there you can go and you
know claw code uh or not cloud code open
claw and install that and get going
there. Right? So that's that way you on
a virtual machine somewhere in the you
know cloud at least you don't have all
the stuff that you have on your laptop
and it's a little better off.
&gt;&gt; Yeah. So yeah it sounds like you're
saying basically again security comes to
mind and sort of sandboxing. You don't
want to run it on your local computer.
So why not either run it on a local
server people are buying Mac minis or
just run it on a cloud server as like a
safe environment. So I would say that
the Mac Mini has another advantage which
is that um
you are really not
exposed to the outside world if you
choose to not be out you know if you
choose it to not be so because that's
your entire uh entirely in your control.
And what I mean by that is when you put
up a a virtual machine on a cloud server
and you run it and those machines unless
secured properly are accessible to
anyone because you can SSH into these
virtual machines. You can hack virtual
machines because they're on a cloud.
They're exposed to the internet. So
unless you have proper hardening
practices even those are unsafe, right?
So you have to be very careful like how
people can get into your open claw
instance and that's something you have
to look into. I found one suggestion I
can give anybody who wants to try this.
It's little bit expensive and then I'll
tell you how I do it. I' I've been
messing around with it. I'm not really
using it that much but I'll tell you the
way people might want to look at it if
they're serious. And that is Digital
Ocean has a a preconfigured droplet you
can get uh which is called Moltbot. Stay
still using the middle name here. U but
yeah essentially you can pay them I
think $24 a month and you can provision
this machine that they tell you is safe
to use. It's hardened for like internet
access. So that's a good way to do it.
But the costs don't end there, right?
because you will hook up this thing to
some form of LLM and uh you can pay
anthropic to do this and you will pay
API costs and so that's the thing here
uh if you are paying $24 a month already
for this droplet on digital ocean that
is like uh secure and then you're paying
API cost like another 50 75 bucks a
month it comes up to $100 a month which
is of course like for the capabilities
that you have out of this thing is
actually very cheap. But uh you know
maybe not everybody needs this like
people like me are like still happy with
cloud code unless you need some kind of
massive automation that agents have to
do this stuff you know you can get by
with claw code for now like I'd say
&gt;&gt; so so clawed bot or open claw or
whatever open claw um the the benefit is
as a pair compos or compared to cloud
code is it just that you can run like
lots of agents simult simultaneously
&gt;&gt; or what's kind of like the main value
prop?
&gt;&gt; Yeah, so you can run a lot of agents and
you I have seen people propose that like
various agents spin up do a particular
task spin down then two hours later and
different task spins up does something
spins down.
&gt;&gt; This kind of stuff is better than
keeping an always on agent which sucking
up uh tokens.
&gt;&gt; So you wake them up and make them to
work and put them back to bed. you know
that kind of thing is better.
&gt;&gt; Yeah.
&gt;&gt; So you can have sub agents doing a lot
of stuff. So I have seen some people's
like ideas of doing this where they have
like a manager for their business. This
is their manager agent and under that
manager uh the manager agent takes care
of all the input from the sub agents
like you know a social media expert, a
content analyst or an SEO expert. All
these people report report to the
general manager who runs as an agent and
yeah this kind of stuff is like fancy
actually. So the question is how much do
you personally need that stuff but if
you're running a business that makes
sense. Yeah I can totally see why people
would want to do this. Right.
&gt;&gt; Sure. Sure. Interesting. Fascinating.
But but for you today do you feel like
cloudbot's worth it? I think it's worth
playing around with. And the way I set
it openclaw,
&gt;&gt; the way I set it up is uh I have my own
like home uh server. I run a little
server with with with all my I run my
little cloud storage here for like
family photos and such because I have a
lot of them. Uh so I spun up a virtual
machine there and it doesn't have access
to the outside world at all because you
have to VPN to get into the home server
network. So it's all like not exposed to
the outside world in the sense nobody
can get into it. Uh but it does have
access internally uh to the internet. So
I I have been playing around with this.
I want to see what it's capable of
because what I feel right now is that I
am only limited by uh by imagination
here because honestly for what I do like
clot code is just something I'm even
starting to use now. it. I can see how
it's helpful. I don't have the sense of
imagination to see what I can do with a
tool as powerful as like setting up a
virtual company of agents that runs my
business.
&gt;&gt; I I have to think about this. I think
everybody needs to have that like
vision. What do I really automate
&gt;&gt; and you know what kind of work do agents
need to do? And then you can kind of go
off and like figure out how to get it
done. That's the easy part. Yeah.
figuring out what you wanted to do is
the hard part.
&gt;&gt; Yeah. Yeah. I mean, I think that's going
to be a a new muscle for a lot of people
to develop, which is thinking like a
manager. You know, how
&gt;&gt; what are the outcomes I'm trying to
accomplish and how can I create tasks
that can be delegated so that I can
accomplish my outcome.
&gt;&gt; Yeah. Exactly. You got to have like some
amount of self-awareness of what it is
that you are doing.
&gt;&gt; Yeah. and how to agentify it.
&gt;&gt; Totally. Totally. So,
I like the idea of having like a local
AI server that you can run a lot of this
stuff on that's you can control how
exposed to the outside world it is. Now,
at the end of the day though, everything
is an API call to claude and it's
consuming all these tokens and you use
Opus. um it's only 20 bucks a month, but
on the other hand, it's and it's the
best model, but you you are running out
of tokens and presumably if you're like
a gentifying your business and you're
running tons of tokens,
maybe it's going to get expensive. Um do
you ever see a world in which the some
of the AI is actually like the lighterw
weight tasks are actually offloaded and
run locally on an AI server or do you
think this is always going to go to the
cloud? No, you can do it locally like
like the Mac Mini approach or like you
mentioned earlier the DJX Spark which is
a better inference system you can run on
your local premises. Um yeah those kinds
of things are great like what's what's a
few thousand to somebody who's running I
don't know a million dollar business
right?
&gt;&gt; A few thousand for a DJX Spark um I
don't know how how is that how much it
costs? Well, the the um the Station is
like $4,000. I think the Spark the
Station has like a GB10 in it. The
Spark, which is supposed to have like a
GB300, I think those they haven't said,
but it's probably be like 50,000 bucks
or more.
&gt;&gt; Okay. So, yeah. So, you can get the
small one or the big one depending on
your needs, I suppose. But yeah, in
either case, if your business is running
like several million, which is still a
small businessish, you know, it's not a
billion dollar business. Even a small
business, a medium-sized business, can
get one of these $50,000 machines and
kind of run a bunch of agents because
how much would an employee how much
would a bunch of employees cost? Way
more than $50,000, right?
&gt;&gt; Totally. If you were going to hire
someone, somebody like this should look
at really buying one of these computers,
putting it on premises, and running your
uh inferencing on it if you don't want
to pay the API costs. So, it all depends
on your use case. If you have enough
load and enough token usage, go get the
API or this one depending on
&gt;&gt; Yeah,
&gt;&gt; totally. And I'm I'm very convinced like
I know that for AI labs it's always
about like unlocking the next level of
intelligence and increasing the IQ and
stuff and and therefore that would be
the argument like no no you should
always want the frontier IQ and then you
should keep using our API. Um, on the
other hand, if you were to just run all
this stuff on your own machine using
some like open- source models, which are
always getting better, too. They might
just be like two or three years behind,
like I have a feeling for a lot of this
stuff, like a lot of your use cases,
it's probably good enough like reading
the news and summarizing it, you know,
surfacing ideas in front of you, things
like that. Like, probably good enough to
just do the open source stuff. And then
I think you could totally control your
cost because you're like, "Oh, I
invested five grand up front or 50 grand
upfront and now I can experiment and go
crazy and generate all the tokens
possible and that's it." You know, I'm
just paying whatever some small monthly
fees are for various cloud services.
&gt;&gt; Yeah, there's another in between option
actually between running it locally
versus a frontier model. I for my own
cloud uh bot open claw experiments uh I
went and got an open router account
which allows you to get a whole lot of
other models like deepseek and you know
all of the quen stuff you know there
like a whole lot of other models that
are like not ultra expensive and then I
got like $5 in credit just to try this
out and I also limited how much this can
use. So, I put like upper limits in case
I charge like a hundred bucks. I'm like,
you know, I have $100 in credit, but I'm
like, use only $10 a week, okay? Like,
don't use all the hundred in the first
week. And so, the first thing I did was
I set API limits uh before I go ex get
all excited in agentic world and like
blow all my credits in like one day. So,
the first thing I did was set limits. I
think something that people should keep
in mind as well. Uh but yeah, you can
get other models at various price points
per token. You don't have to go frontier
or local, you know, you have a whole
range here.
&gt;&gt; So, you're saying the advantage for open
router is you could sort of cost
optimize and and try to play around with
like maybe telling your agents, you
know, hey, use these models for these
tasks only use this frontier model for
this type of difficult task.
&gt;&gt; Yeah. Yeah, you can do that. You can
even give it a preferred hierarchy of
models to go through and say like you
know for some things like this use this
model and that model. So within open
claw you can give it a hierarchy of
models to go through. So you can really
finally control how you spend in
inferencing.
&gt;&gt; Interesting. Yeah. This will be a story
we'll have to watch because if if 2026
is the year of the agents, meaning
people are starting to actually do
useful stuff, pretty quickly behind will
come lots of cost optimization of like,
cool,
&gt;&gt; I this is awesome. I'm spending a ton of
money, so maybe I need to play around
with like, yeah, stack ranking models by
performance and price and thinking about
local versus uh, you know, cloud compute
and so on. Um, before we get to talking
about the implications from an
infrastructure perspective more deeply,
I I wanted to ask really quick, one of
the things you said earlier was um, you
know, oh, I've got, you know, I'm using
cloud code and I've got it reading my
substacks by going to my Gmail and
summarizing them for me and then now I'm
just referencing this summarized file.
You also talked about being able to have
it go into websites like Digi Times and
kind of same thing uh reading it on your
behalf. So, let me ask you as a Substack
writer, have you put much thought into
there's there's sort of two things that
came to mind there. One is from an
analytics perspective,
it's sort of obfiscating
analytics a little bit because now you
have your bot just like reading
everything but only reading it once and
then just summarizing it for you. uh as
opposed to like a human having to like
go in a couple times, read it, think
about it, that kind of thing or not read
it at all. Um and then two, all of a
sudden now also your AI is becoming your
primary user interface and so is the
markdown and and so arguably you might
end up spending less time in your Gmail
or on your Substack app or on the Digit
Times website. a lot of these uh
companies, you know, they obviously
prefer users to be on their platform,
whether that's so they can sell more ads
or just try to put more things in front
of you. So, I guess the the two
questions from an analytics perspective
as a Substack creator, have you much
thought into that? And then secondly,
like do you feel like there's going to
be push back to this idea of the actual
spending less time in applications and
just more time in front of your AI?
&gt;&gt; Yeah. So that I can see what you say is
a very real thing actually because you
can bring everything to my cloud code
terminal or you can bring it to the
anthropic app uh on my computer and you
could do it with co-work
even you can do cloud code even on the
app by the way it's not like you have to
do it terminal I do it terminal but you
can do it on the app uh so yes so if
everything is coming here and it's being
pushed to markdown or Google docs or
this why would you go to the website? So
what immediately, you know, the old web
approach of having banner ads, those
things are going to be dead. I mean, why
on earth would anyone go to a website
with like like ugly banner ads and try
to pass through the text, you know, you
have all these like cookie blocking, you
know, plugins in the Chrome thing and
all of that is like useless when you
have to you have the information being
given to you. I am in a sense maybe a
minority. I can't tell because I don't
have the data, but I actually use this
only for surfacing the content because I
actually go read the original thing and
then think about it cuz that's where I
think the human element still lives
because
&gt;&gt; the information is being sent to me and
process the processing and the insights
comes from the human mind
&gt;&gt; and I don't think that AI is there yet
and the speed of things you never know
We maybe we won't be writing substacks
next year. I can't tell. [laughter] It's
crazy.
&gt;&gt; Maybe it'll have better insights than
than what we can generate. I don't know.
But for now, uh it's not that insightful
to me. I still appreciate all the people
who actually write um articles on their
own. And you know it's you can kind of
tell because even however sophisticated
these tools are uh it has its footprint
the AI footprint is there. So
&gt;&gt; totally.
&gt;&gt; Yeah. So I don't really use it for
writing but in terms of like a
aggregation tool and bringing things to
me where I can see them all in one place
is a fantastic tool for that kind of
stuff.
&gt;&gt; Yes. So the analogy that comes to mind
for me is I get the print Wall Street
Journal because I prefer the user
experience of flipping through a paper
as opposed to hoping the algorithm
surfaces the right things to me. And
anyway, and the you know scrolling I
spend enough time on the computer I want
to be as analog as possible. Um in the
print Wall Street Journal the lefth hand
sidebar on the homepage is always like
these it's like a a bunch of little tiny
summaries of like what they think are
like some of the most important topics.
and you look at those and you read like
a sentence and then you're like oh
that's interesting I want to go read the
article and I feel like what you've
created for yourself is very uh similar
which is like hey
&gt;&gt; help point me in the direction and then
I will still go read the whole article.
&gt;&gt; Yes that's a great analogy that's
exactly what it is I I do not have the
print edition of Wall Street Journal but
yes that is exactly what I'm I'm doing
here. Yeah.
&gt;&gt; Yeah. Yeah. So
&gt;&gt; and it's searchable and it's searchable.
&gt;&gt; Yeah. Which is nice. So, and so
ultimately, even though you're using
your AI to help like point you in the
right direction, get you started faster,
uh you still think that you'll spend a
lot of time on the actual apps or
reading the actual content from from
users thinking beyond just Substack, but
anything else in your life that you
might try to speed up using AI? I I can
I think I personally would but I don't
think I can generalize that to a lot of
people you know because the summaries it
gives are actually pretty insightful in
the sense that it is able to collect
most of the information rather quickly
and give you the gist of it and people
are quite happy with that you know it
depends on the use case for me I I write
very long form stuff I read long form
stuff that's the way I operate but for a
lot of busy people who don't have the
need for this kind of stuff like
earnings call highlights you know
&gt;&gt; just run it you can you can create a
skill for that like
&gt;&gt; you can say slash earnings MSFT
Microsoft you know and it'll go and look
up all of the stuff and give you the key
highlights you know that's a perfectly
good use case because sometimes I don't
want all the earnings call stuff too you
know the summary is enough yeah
&gt;&gt; yes yeah actually I need to try that
because I always like to I listen to the
earnings calls when I run because then I
can form my own like interesting
insights, but there's always so many
that are simultaneous like having a
skill that would nicely summarize them
and not put the necessarily the spin
that you get from like when I see the
earnings report in the Wall Street
Journal, sometimes they don't know,
they're not super technical and don't
know how to explain the story. So, I do
like the idea of having my own AI that I
could maybe kind of tune to look for
particular things as it reports out the
summary to me. The the the other thing I
think that you and I do when we listen
to earnings calls is u we kind of are
able to tell based on what somebody said
and read between the lines.
&gt;&gt; Yes.
&gt;&gt; And the reason is like, oh, why did you
say that? Oh, that's because you don't
really know this or you're not
committing to this. Why are you not
committing to that? So it's like so many
like levels above what AI can tell you,
right? AI will not spot those things.
Like why did you say that? Is it because
you know
&gt;&gt; that is a that is a really good insight,
right? What happens a lot is someone
asks a question and then a different
question is answered and it's because
they didn't want to answer that
question. But AI isn't trained to see
that, right? Because like the in the
training data, I'm sure it obviously
it's just predicting things and it's
just like it's very causal like I I read
the sentence and therefore this thing
but it's probably not being trained on.
You read the sentence was was that
actually answering the question if not
surmise why it wasn't you know.
&gt;&gt; Yes. That's because humans are trained
to think of what wasn't said. [laughter]
&gt;&gt; Yes. Totally. Well, so there's some RL
that uh you know these AI labs should go
do. So let me uh ask you so what
&gt;&gt; what's going to be the impact as you've
been playing around with agents if if
this is the year of agents obviously we
talked about like local servers Mac
minis that kind of thing but generally
speaking all this is still running in
the cloud for the most part what are you
seeing from like a demand and supply
perspective and how might that continue
in 2026 2027 and beyond
&gt;&gt; so the whole agentic AI world is causing
a crunch of CPUs and there's like
shortages. And in fact, when listening
to the Intel earnings call, it turns out
Intel was actually uh surprised by the
sudden surge in CPUs uh and the demand
for it. And they did not anticipate this
uh and they're kind of like in in in
short supply now and in not exactly a
position to meet the supply even because
of the way they chose their
architectures which is most becoming
more and more monolithic.
um in the last couple of generations at
least compared to how AMD does it you
know AMD is chipletized everything and
they can reuse their consumer uh cores
along with their server grade cores and
it's like interchangeable you know Ryzen
and Epic have interchangeable chiplets
things like that so now everybody's like
oh wait we need a whole lot of CPUs now
because agents not just you know need to
inference LLMs in GPUs, but they need to
uh send various tasks out. They need to
read a database. They need to read an
Excel file. They need to decide, oh,
what should I do next? You know, get
some information from the LLMs. So, CPU
load is getting a lot more relevant in
the age of uh AI agents. And I'm going
to look into a bit more depth here than
what I'm talking about as to exactly why
that is and uh why it's different from
the CPU use from servers before. Like I
don't entirely understand for myself why
AI agents need specifically high number
of CPUs. Uh so that's something I'm
going to look at but clearly the crunch
is here.
&gt;&gt; Yeah, totally. Yeah, I look forward to
seeing what you come up with. I mean, at
the end of the day, my thoughts are like
GPUs should be doing matrix
multiplications as much as possible.
Anything that gets in the way of matrix
multiplications should run on the CPU,
right? Especially to your point, if it's
waiting on an API call, if it's making a
database call, right? like
obviously rag type stuff any sort of
pre-processing post-processing
it's a lot cheaper to run it on a CPU
than to use mat holes on a GPU now
interestingly we've also talked a lot on
this about security authentication
sandboxing stuff like that
all of that should come into play when
you're thinking about agents which by
the way Microsoft AWS Google everyone
has these agent AD or SDKs that they're
making and they're trying to wrap in
things like okay if enterprises are
letting their individuals create a bunch
of agents where you know how do we wrap
like enterprisegrade security and things
along with this to say like yes um VIX
agent should be able to access the HR
database or no VIX agent should not be
able to access the internal HR database.
Obviously, a lot of this type of stuff
should run on CPUs, not on GPUs. And a
conversation for another day, but you
could see how this could even get
offloaded into DPUs, which are basically
CPUs and and switches, kind of
integrated networking in the network to
to even try to stop this stuff before it
even gets to the CPUs and just say like,
oh, wait, this is a network request and
it's from Vic and he doesn't have
access. Don't even let this happen. And
so I think we'll over the next year or
two at one I think we'll see a lot of
software that comes into play to say
like agent orchestration, user security,
user management, like where is the right
place for all this to happen? How do we
make it as simple as possible? Um but
two, I think we'll see as much get
offloaded out of GPUs onto CPUs as
possible and maybe get offloaded into
these kind of like network co companion
processors, if you will, DPUs.
&gt;&gt; Yeah. And uh even in Nvidia's CES
announcement, one of the things that
might have relatively gone unnoticed is
the fact that they now have uh this kind
of like what can I security features I
think is encryption things like that
because when you're inferencing on
common hardware and so many people are
doing it like hospitals and uh
military equipments I don't so sensitive
sensitive applications
&gt;&gt; you got to make sure that even during
the inference process process these
weights are not shared or there is no
way that this is going to leak. So like
you mentioned there needs to be identity
management like who is the user that is
accessing what information and whether
they are allowed or not. Then you also
have to have like actual encryption
which all of this runs on the CPU.
&gt;&gt; Yes. Exactly. Yeah. Encryption. Totally.
&gt;&gt; So you know this is probably a good
place for us to stop. I think this is a
super fun chat into agents from a
early adopter tinker perspective all the
way through to like just a hint at maybe
some of the themes for 2026 from uh uh
compute and infrastructure demand. Um
we'll leave it there. Vic, thank you for
sharing us uh with us all of your
personal journeys with cloud code and uh
open claw. And uh that's it listeners.
Thanks for listening. If you're enjoying
Semi-Doped, we'd love if you give us a
fivestar rating and a quick review in
Apple Podcast, Spotify, or wherever you
listen to this. Thank you.
