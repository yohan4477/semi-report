---
source: https://www.youtube.com/watch?v=tieu3xhnoEA
vid: tieu3xhnoEA
title: Every Muse User Gets 2 CPUs and 8GB in Meta's Cloud. Your Phone Already Has That
date: 2026-10-01
duration_sec: 3051
channel: Semi Doped
kind: transcript
---
Last week Qualcomm said agents will run
on your phone, your glasses, and your
earbuds. But chip companies don't decide
where inference runs, app companies do.
And the biggest app companies of our
time right now, OpenAI and Anthropic,
well, they only get paid when it runs in
their cloud. So who will actually make
local AI happen?
Maybe the company that makes its money
on ads and already ships Snapdragon in
its glasses,
&gt;&gt; [music]
&gt;&gt; like Meta.
Or Google. But do they have the moxie?
Let's get into it.
Hello everyone. I'm Austin Lyons.
Welcome to another Semi Duck episode. I
write Chip Strat, a semiconductor and AI
infrastructure newsletter for investors
and tech executives.
&gt;&gt; Hey, I'm Vic Shayko. I've worked in the
semiconductor industry for about 20
years, mostly on engineering. I'm the
founder of Semi Exponent, where I do
independent semiconductor research,
mostly focused on AI and infrastructure.
And I also write Vic's newsletter on
Substack, where I just explain how
things work and what matters to the
markets. Um so that's what we bring to
the newsletter. Check us out on our
substacks,
uh where we write like whole lot of
stuff every week.
&gt;&gt; Yes, totally. Uh
Vic, I know you wrote some stuff last
week, but let's not talk about that. Um
let's talk about our new intro. Tell me
about our sick new intro.
&gt;&gt; Yeah, that was uh by the way, uh all
done with um
Opus 5.5. And you know, uh I we have our
podcast brand document. And all I did
was I like I gave it a brand document uh
PDF and was like,
"Just make me a motion graphics intro."
And our branding document has basically
the the theme it's based off of, like uh
the field and the single point of
singularity. And our designer put in
these like like phrases in there. So it
just used that and built the whole thing
out. And I was like, "Ah, this is
insane." And I told it like a few other
things like make it 6 seconds, make it
like 30 seconds, and we I tried
different things. I was like, "Wait,
wait, the logo stays for too long. Make
the logo stay for lesser time. Make the
animation slower." It's insane. That's
That's what it came up with. That's
pretty crazy. And then uh I used uh
you know, Suno AI, which is like a music
generation thing. Uh and if you get the
paid subscription uh to the
tool, you can actually generate
commercial uh music. You can use that in
podcasts and you know, other things to
make money off of.
Uh not as not a sponsor, but they could
very well be, I suppose. Uh really, like
it's it's so so cool. Like I keep kept
trying different things. I said, "Hey,
make some like jazz fusion." I'm like,
"Nah, this sounds like elevator music."
And I'm like, "I don't know. Like I want
something exciting." And I told it like,
"Build it up and like give it something
in the beginning that's repetitive, but
like I want a climax finish, and then
goes to slower things where you know, we
can talk over it and things like that."
I don't know, it all works just fine.
And then our editor took it takes it and
you know, runs with it or uh with with
the magic there. So all this is really
nice. AI.
&gt;&gt; Pro AI.
So so good. So amazing. I love that the
the Suno like you still had to have
taste. Like you're able to use Suno to
generate the music, which is incredible.
Um and and really speed things up
opposed to you know, what would you have
to do
previously? Contact someone who knows
how to do this or figure out how to make
music yourself, you know, with your
computer. Um but you had the taste to
say, "Oh, you know, here's what I'm
listening for. I need it to build. I
want there to be a hook. I need it to be
catchy."
Yeah, so yeah, clearly I am a musician
and like I have recorded music, and I
kind of know
what to say to it. So that little bit of
domain expertise actually helps uh to
tell it what to do. Otherwise, it's very
impressive. I think most people can do
something with it.
&gt;&gt; Awesome. I love it. Okay, so let's talk
about what else is new in this episode.
So, we have a presenting sponsor.
&gt;&gt; Yes. Awesome. We have Crusoe. This is
like our first episode with a presenting
sponsor. We are very excited.
&gt;&gt; Very excited. Really stoked to partner
with them and hang tight and you'll hear
our first ad read and you'll get to
learn more about them. But, it's going
to be fun and you're going to learn a
lot about them. There's so much to learn
about Crusoe and we're going to do fun
ad reads every single week and they'll
be different. So, stay tuned, listen to
them, check them out. And you know, they
sat down with us and we spent a lot of
time talking about all their value props
in their interesting technology from top
to bottom. So, you'll get to learn about
that too over the next couple months.
But, with that let's let's get into it.
So, I was at Snapdragon Summit last week
in Maui in Hawaii. It was awesome. There
was a tropical storm coming which I
didn't even know, but some other
analysts were like, "Hey, like my mom or
my wife called and said they saw on the
news that there's a tropical storm
that's going to hit Hawaii." I was like,
"Oh man, really? I'm just too busy
enjoying the beach to even notice." But,
we got we got out before it it was a
problem.
But yeah, let's talk about Qualcomm. So,
I think you know Of course, everyone may
have seen I did an interview with Durgo
which was really interesting and talked
about high bandwidth compute and that
was mostly because Durgo was there and I
was super excited to talk about it.
But, the name of the game for Snapdragon
Summit my takeaway was Qualcomm really
talking about a vision for agents
running anywhere and the fact that their
Snapdragon SOC they have different sort
of flavors of it that can run in
watches, in augmented reality glasses,
on your phone, on your car, in your
laptop. And so, naturally Qualcomm as a
hardware vendor, their vision is agents
that can run anywhere.
&gt;&gt; Uh sometime ago, if you had told me like
agents
were are going to run on the edge, I
think the perception I would have had is
LLMs are too big. Like, how are you
going to run a frontier like LLM uh that
is intelligent on your phone, and
clearly we will never have
I don't know, like
a terabyte of memory on the phone to run
a
trillion parameter model, and clearly
scaling laws still hold, which means the
bigger you make a model in terms of its
parameters, the smarter it seems to get,
and it's still haven't We still haven't
seen the end of that. So, I would have
laughed at the idea of
what's no way we can have that running
on our phones, right?
But, in talking with you just before the
show, and also uh reading a little bit
about the stuff in the event uh that
Qualcomm just had, it seems like there
is a different way to think about it. Um
agents
could be a portal into our world of AI,
and we'll clarify what that means. It's
very interesting.
&gt;&gt; Yeah. You know, you make a really
interesting point, which is like
go back a couple years. Uh remember like
Intel uh Pat Gelsinger, he talked a lot
about AI PCs, and there's this big push.
Yeah, we're going to have these AI PCs.
They've got NPUs, and everyone's like,
"Oh, how many tops does your NPU have?
Mine has 35. Mine has 45. Mine has 55."
And it was all about like um the idea
was running AI locally. But at the time,
it was LLMs, and first of all, there
were barely any open-source LLMs when
that started. Um and then, you know,
when they came out, it's a 70 billion
parameter, and it barely fits on your
laptop, and your NPU really can't chug
along and do too much. And so,
everyone's like, "Dude, what are we
doing here? Like, this this is going to
be slow. What's the use case?" Um and
ultimately, AI PCs were kind of a dud.
Everyone just ran their AI in the cloud.
Um, and I think now we are getting
closer to a world where there will be
useful AI and we can get into this that
could run at the edge and it doesn't
have to be an LLM. It doesn't have to be
a frontier trillion parameter LLM.
Um,
but we can get into that. I will say
uh
you know, we're we're still in this
transitory world where
and and we'll get into this where you
can see a world that will run AI at the
edge and yet there's still talk about
like, oh yeah, we we can run all of this
uh agentic AI for example, Claude and
co- codex and you know, open Claude,
perplexity, uh you know, and a lot of
that is still running in the cloud. So
there's there's still a little bit of,
you know, we're envisioning a world to
come but we're still talking about apps
that actually run in the cloud. But um,
you know, obviously I think Muse comes
to mind uh as
a truly agentic AI and and then where
that could go is pretty interesting. But
yeah, I'll hand it over to you.
&gt;&gt; The app thing is very interesting. So
recently I have gotten
uh very much let's say AI built to say,
not that I wasn't already. But the
reason is
given the Substack and now I'm, you
know, running I've been talking to
prospective clients about semi-exponent
and institutional research for financial
firms and things like that. And then we
have the podcast, right? And then we
have so many like podcast briefings and
recordings and back and forth of
documents. It's a large universe that we
deal with, really, you know? And so
I have been thinking this needs to be
more agentic AI for me. I I really need
the help. Like
uh I could go off and hire people and
all that but I was like, okay, let me
see what parts of this. It's not like
human taste isn't important. It is and
we do have people who work with us on
the podcast. We do need people. I'm not
saying we're going to replace
everything, but I'm like just let's what
can I what can AI take care of for me?
Because there's like a minimum
requirement for some things the MVP in
my life. What can it do?
So, the app itself the phone has become
a very big part of my day. And the
reason is
I have chat GPT. I have I have Claude 2
and this happens both places really. But
in chat GPT I have now scheduled tasks.
So, what it does is like every morning
it it reads all the emails and because
I'm on a different time zone it gives me
a briefing as soon as I wake up in the
morning. So, when I'm making coffee
literally chat GPT reads out to me like
whatever has come to me or I read it out
or whatever doesn't matter, but it's all
in one place. It's become an integral
part of my morning. And so, yes AI
doesn't run on my device, but it's
become a portal for me to handle tasks
during the day. And this is
kind of what Qualcomm has been saying
except that their view is that lot more
inference runs on the device.
Maybe we are not just there yet, but I
can see where we are headed. Because
it's become so important for me that
every hour, right? I don't want to miss
emails and all that because some emails
require me to respond immediately. So, I
have another scheduled task that
you know, reads my emails and tells me
every hour. So, it a notification comes
up on my phone. Hey, somebody is asking
you to do this.
Here's another great example. I
messed up and I always get time zones
wrong and anybody who's like worked with
me on this always gets rescheduling
invites from the calendars and I always
get I can't do math in my head I guess.
Um so, it it sent me a notification it
says, "Hey, your email says that you're
going to meet with this person at this
time, but your scheduled
you know, meeting is 1 hour late.
Are you sure this is what you want to
do? Like or do you want to move it? I'm
like, "Oh my god." Like I told chat GPT
like remember to put that on my to-do
list and put it on my task calendar."
Cuz it's hooked up to Google, right? And
so, it made it uh you know, so it's put
on my to-do list and I you know, I just
have to go and send you know, reschedule
it. I could ask it to do that, too, but
I'm just not interfacing with other
people yet because I don't want it to
like keep sending stuff to other people.
Could be done
automatically, but you see where this is
going, right? Like, I know inference
doesn't run on the device yet, but on
the cloud, it's still useful. Edge
devices have been useful to me already.
&gt;&gt; Yeah. Yeah, I love that use case. Good
job, Chat GPT, by the way, for keeping
Vic straight and figuring it out.
&gt;&gt; I wouldn't even have showed up to this
podcast on time. I would have been 1
hour late.
&gt;&gt; That's hilarious. [laughter]
&gt;&gt; This episode of Semi Dope is presented
by Crusoe. Crusoe builds AI
infrastructure from the ground up,
power,
data centers, and the cloud on top.
Crusoe Intelligence Foundry is their
managed AI platform. And the nice
feature in there is serverless
inference. Now, if you're going, "What
in Jensen's name is that?" It means that
there are no GPUs for you to provision
and no clusters to manage. You simply
pay per token.
If you're running open models like GLM,
Deep Seek, Kimmy, or Gwen, Crusoe's
managed inference is fast, nearly 10x
faster time to first token, and 5x the
throughput of VLLM. Their memory alloy
caching layer routes requests to
maximize cache hits.
Since it works with OpenAI SDK,
switching over to Crusoe's API is quick
and easy to get it running. All you have
to do is pick a model, grab an API key,
and start sending requests.
If you sign up with the link in the show
notes, you get $5 in free credits to try
Crusoe Intelligence Foundry. Think of
it, five whole bucks so you can just
burn some tokens just for fun. And some
of these open models are quite
inexpensive, so you'll actually have a
ton of fun with it. Check out Crusoe and
see their serverless inference on their
managed AI platform. You really got to
find out this for yourself.
There are a whole lot of more features
in this that I want to try out for
myself, but serverless inference I found
is the best place to get started. It's a
great way to support the show and try
out Crusoe's Intelligence Foundry. The
link is in the show notes, and now back
to the show.
&gt;&gt; Previously, when everything was just all
running chat GPT, chatting with chat
GPT, or chatting with Codex, still
everyone is still focused on like, "Oh,
it's got to be Fable. It's got to be the
Frontier model." Um what I think has
been really interesting lately is Muse
and Instinct, like we've talked about,
Grok by, and these agents where you
realize one, I could see this going to
actual like normal consumer adoption
because it's so simple to use, you know,
you can there's billions of people that
have um Meta's family of apps installed,
and it's very simple for them to get up
and running with Muse. And um by the
way, when they when they sign up for
Muse, they get a dedicated uh what is
it, like two CPUs, a dedicated cloud
VPN. It's like two CPUs, 8 GB of RAM. Um
I think I even saw maybe like 100 GB of
storage, or maybe that was Tom's
Hardware speculating or something, but
clearly like quite a beefy computer for
every single person. And and so on the
one hand, this is like crazy powerful
that all these people can spin up agents
that can actually go do useful stuff.
And by the way, um my use case for Muse,
cuz I was like, "Okay, I want to try
this out. What am I going to do?" And
I've got all this like electronics and
old recording equipment and stuff like
this sitting just next to me in my
office, and it kills my wife because
she's kind of a minimalist, and she's
like, "This junk is sitting here. Do
something about it." I'm like,
literally, I She's like, "It has so much
value. It's just sitting there. Just
sell it on Facebook Marketplace, you
know?" I'm like, "I just don't have
time. I just don't have time to take
pictures, write out all the listings,
look up how much everything should cost.
And then I was like, wait a minute, this
is perfect for Muse. I'm just going to
take pictures of everything and tell it,
bro,
just post this on Facebook Marketplace.
I don't care what the price is. You pick
a good price. You You make a nice
listing. And I just took gave it a bunch
of pictures. And it actually did an
awesome job. It like looked up what
everything was called and wrote like
really great descriptions, figured out
the prices, and posted it and
everything. And so I'm like, dude, that
is like truly useful work for me. And I
even may make some money out of it. And
but even more importantly, of course,
I'm going to make my wife happy. Uh so,
you know, happy wife, happy life. Um
but,
The more it So I was like, oh man, I'm
I'm using those uh
you know,
all this stuff that was provisioned for
me in the cloud. But then I stopped
using it. And so I'm like, is it just
sitting there? Are they sharing it with
other people? But I was thinking like,
if man, if I get this just cranking all
the time for me, Muse is so handy, so
convenient because because it's on my
phone. And so I was actually checking it
when I was in Hawaii. You know, people
are responding like, hey, can I buy
this? So tell Muse like, tell everyone
like, no, I'll get back to you when I'm
back from vacation. But don't tell them
I'm gone. I don't want them to rob my
house, you know. So just tell them like,
I'll get back to you this weekend, you
know. And so Muse is doing that for me.
And I just thought like, again, hey,
some of that stuff, it's Here's my phone
right here. And it's pretty simple. Like
they're paying a lot of money in the
cloud to reserve this infrastructure and
use it for me. But like, couldn't some
of this very simple stuff like sending
someone a message, like couldn't that
actually happen on my phone? So it just
got me thinking like, hey,
maybe app companies who end up spending
a ton of money in the cloud, like maybe
Meta, maybe they will be the ones who
are incentivized to actually push a
model down to my phone and try to
orchestrate and have some of it run
locally when it can.
&gt;&gt; Yeah, that's very interesting that the
fact that, you know, you mentioned that
they everybody gets a virtual machine in
some cloud instance somewhere.
Actually, I sat down the Substack post
this week was all about estimating how
many CPUs are going to be deployed
assuming, I don't know, a billion VMs
being in the cloud. Like how many CPUs
do you need? Cuz I think there's like a
lot of like excitement about CPU
requirements. So, I calculated all this
out. It's very interesting actually
because
people can share CPUs. You know,
everybody doesn't need to get a
dedicated VM. Like, you know, when it's
not posting your
Facebook Marketplace ad, like it could
go and help Vic like get his calendar
right, right? Like the same CPUs. Why
should it like just chill out? So,
this kind of stuff is there. So, the
second thing is like
what we don't have yet, I think, is
uh we've got 8 GB of RAM on this thing,
right?
And we've got uh some computing power,
like two VCPUs worth of computing powers
right here. Got some storage. I mean, I
don't know how much is in this thing.
Maybe not 100 GB. Like, I need space for
apps.
Or do I? We'll get to that soon. Do I
really need apps anymore? It's a big
question. So, yeah, like
although there's like all these CPU
deployments on the cloud and everybody's
excited about the prospect of CPU, I'm
like, "Look, my phone is already
my portal to the AI world. It's
happening right now. Keeps buzzing about
all the schedule tasks I have. You're
putting up stuff for sale. Everybody's
happy. Things are getting done. You're
making money."
But then what's my CPU doing here?
Nothing. So, I'm like, "Why don't we now
start using this as our edge computing
device where your two VMs and 8 GB of
RAM live? So that, you know, you can
just talk to this device and it has
everything it knows everything about
you. It knows where you are. It knows
how much how much you've walked in a
day. It could even listen to you. It
knows who you're talking to.
All your devices connect to this. Like
your watch can connect to it. Your you
know, your your AirPods can connect to
it. Everything is phone-centric. So, we
have to reimagine the AI
on the edge world in this framing.
&gt;&gt; Yes. Yes. I totally agree. It In it's
all about all that context, too. And
that's kind of the point you're making
is like I you you've got your watch.
It's got your health data, your steps
data. Maybe for me it logs my Strava,
whatever. Um you've got your
microphones. You've got your phone,
which has not only of course your
calendar and whatever, but it's got like
the pictures that you've taken. So,
there's all this just local context on
your watch and your glasses and your
earbuds and your phone. And so again, um
the idea Let's Let's say it's just
Claude and OpenAI. The idea that you
would take everything local, send it up
to the cloud, have it compute in the
cloud, send it back down, feels a little
crazy. And of course in their world, and
remember, uh OpenAI and Claude uh OpenAI
and Anthropic, these are like two of the
fastest growing companies ever. Great
companies, uh amazing app companies,
whether they meant to become that or not
in the first place cuz they're both kind
of research companies. Um
they their business model is we make
money when we do inference in the cloud.
And yet we are saying, "Actually,
there's a world where we would really
like to just run this stuff locally
because all of our context is here. You
could have Of course there's privacy. If
you can just
filter through things and and take only
what you need here and not don't send up
all my photos to the cloud. Don't send
all this information to the cloud just
so that you can compute it there and
send it back down. Like why not do it
here?" And what's interesting again is
Meta stands out as a company who their
business model is ads. It's they just
want to help me and have the opportunity
to show me ads and just be part of my
life essentially. Now, whether you like
ads or not is a whole 'nother
conversation. I think it can be useful.
Um but there's a disincentive of course
for the model labs to want to come help
me at the edge, but Meta's like, "Bro, I
want to help you at the edge. You've
already got our apps installed. Like,
let me help you." And so, Meta has
already made open models. Meta has um I
think they released Muse glimmer, which
is in this uh direction of running
things locally, orchestrating, running
on the edge. So, it's very natural,
actually, for Meta to say, "Hey, I've
made Muse. It's super helpful for you.
It's really expensive. You've got this
um clap this little VM here with these
CPUs in the 8 gigs of memory, which is
very great point. It's just sitting
idle.
We can give you more Muse if we can just
run some of it locally. I can imagine I
hit my token limit, and they're like,
"Yeah, didn't that suck? We can make
your tokens go farther. Let us run some
We give us permission to run it on your
phone when possible." And I would say,
"Totally." And this doesn't even
necessarily mean that it has to be the
stuff, like you said, that requires that
sort of system to deep thinking, deep
research. You need a frontier model.
There's lots of stuff that can be done
at the edge that aligns with just
helping my little agent making some
quick decisions and helping me with my
life, looking through my contacts or
whatever, before deciding what needs to
go to the cloud.
&gt;&gt; Yeah.
&gt;&gt; [clears throat]
&gt;&gt; So, that's the that's the whole point
because look at the like the app like
you mentioned the Strava thing um and
you you run a lot, and uh you keep track
of your steps. You even post it on X and
all that, and you were like uh when you
were in Hawaii, you were like, "Look at
this. I have 20,000 steps today." You
know, all that stuff. Clearly, it all
runs on an app, but do you really need
that app? You know, there's a fitness
app sitting on your home screen
occupying like the space, and I will
have to find where it is, or you have to
type fitness, and then you have to click
on the app, and it shows you the steps.
And why do you need that? All you have
to do is ask it, "How many steps?" And
it it it has a screen. That's all it
needs. It's just a screen. Everything
that happens on a phone
can just happen. You don't need an app
for it. Like And this is a point that
Ben Thompson recently made on
Stratechery,
which if we are both big fans of that
newsletter, he's like the OG newsletter
guy. I think at some point everybody who
started a newsletter wanted to be like
Ben. So
&gt;&gt; exactly
&gt;&gt; [laughter]
&gt;&gt; So
he made the point that
there is no need for apps anymore
because
on everything can be built and destroyed
on demand.
It's very simple to do.
Anybody can like build an app for their
own use cases
and change it out if they don't want to.
Some things may not even need an app,
like this fitness example, right? So,
where are we going in in this world of
like
devices? Like what do devices need to
have?
Do we need to think of them as computers
or
what is its function in the world of AI?
Are really deep questions that we have
to think about because that defines what
AGI is.
Another point that Ben made, I want to
mention this and I'll ask you what you
think because it's a very important
point. He's like, "Look,
now there is no reason for anybody to
code. There's like literally no purpose.
It is a syntax that nobody understands
with this like braces and like colons
and like indenting or whatever.
We don't need to deal with that mess,
okay? Like you just ask it, it writes
the code, it gives you you don't worry
what happens in the background.
Now we have news and we have these CPUs
and all that. These
agents can even control your computer.
Like ChatGPT has a computer use.
So now agents control your computer,
too. Like So you don't need to even use
your computer. Your computer is meant
for your AI to use, not for you.
Right? So you see where I'm going with
this?
&gt;&gt; Yeah, yeah, yeah.
&gt;&gt; So what is the device supposed to do
now?
&gt;&gt; [laughter]
&gt;&gt; Oh good. Okay. So this is a great setup.
I have lots of thought. So the idea that
we don't need to code, I would say
baloney to that, although many people
don't need to learn. But in in By the
way, I got that um Ben lives in
Wisconsin right now, and I was listening
to this Guy Raz How I Built This with
the the guy who started Culver's, which
is like a
you know, if anyone knows, it's like a
fast-food restaurant. It started in
Wisconsin, and it's so funny cuz the
guy's so Wisconsin, and instead of
swearing on the episode, when he was
like really angry, he said, "Baloney to
that." And I was like, "Oh, that's so
good. I have to use that."
&gt;&gt; I'm [laughter] ready to get this done.
&gt;&gt; Yeah. Thank you. So, thank you. I wanted
to swear, but I you know, I don't want
to get that explicit rating on our
podcast with our sponsor. Um
&gt;&gt; [laughter]
&gt;&gt; but okay. So, as you [snorts] said
earlier, why could you make such a great
little hook and little jingle with AI
using Suno? It's because you had domain
expertise, because you've made music
manually the hard way. Therefore, you
knew how to prompt the AI. I think
obviously, with the best coding, um it's
still going to be people who have
written code and understand how to uh
write good code and what good code looks
like. And And actually, and we'll get
into this a little bit later, there's
this new model that came out recently,
Jev.
And I won't get into it right now
because then I'll get too distracted
from the point that you were trying to
make. Um but Jev, what what's really
cool is it can you can use it to take in
like the world's input. Um so, you could
give it free-form text or you could give
it a a chatbot conversation or a phone
call or whatever. And then you can have
it do simple things like classification.
Like, "Oh, here's what I I'm a bank.
Here's what the person said. Should it
go to fraud department? Should it go to
the payment department?" Whatever. It's
literally just like a little These are
little like classifiers or little switch
statements or if statements, if you
will. Um but it can work crazy fast, and
it's trained like an LLM on the on the
world's um the internet's corpus. Um so,
it's very intelligent. And anyway, these
These are like new programming
constructs that will actually go into
code. And if you like zoom out and you
think like, "Wait a minute, today we're
in a world where the LLM just writes all
the code end-to-end, but if you actually
try to stick an LLM call in your code,
it gets really funky because these LLM
calls are like they take a long time
potentially, they're not very bounded,
they're not typed, so you don't quite
know what's going to come back. It's
just a string that comes back and you
have to parse it and figure out and if
you even if you ask for structured
output, so it comes back as like a JSON
or something, it still like very slow
and it's inefficient. So, anyway, I say
all this to say there's going to
actually be new ways of programming
which the models aren't even trained on
yet. So, I think there's all sorts of
reasons why having domain experience as
a programmer, sure for the Ben
Thompsons, they don't need to learn how
to code, um but for folks like you and
I, like knowing how to write RTL or
knowing how to code will help you
obviously be able to prompt it better.
And then again, as we continue to even
invent new ways of programming,
someone's got to prompt the AI to do
that to train it on it. But, to the
question of do we even need apps? So,
yes, we need to program. We need people
who have domain experience in
programming so they can they can do it
better and more efficiently. Do we need
apps? Okay, this is actually really
interesting and I won't bury the lead. I
agree with you that we don't need apps.
And let's think from first principles,
why do we have user interfaces in the
first place? At the end of the day,
let's take Excel for an example. Dude,
at the end of the day,
you could just have a database and a
prompt and like store data in a database
and prompt use SQL and just say like,
"Hey,
uh whatever, I'm trying to um calculate
my mortgage." Like you could put you
could either write all this stuff in the
command line or, you know, put a bunch
of data in a database and pull extract
it out and make calculations and
everything could be the command line.
But, obviously,
that's like a a very difficult thing for
people to learn, so we make these user
interfaces like Excel where it's like,
"Oh, it's very visual and you can, you
know,
um have little if statements and summing
and stuff like that." And it's super
simple. But, the problem with all user
interfaces is someone has to decide what
the rest of us are going to be forced to
use. And that's why user interface
designers are amazing because they're
almost like psychologists. They can
think really well about like what's the
best experience and what are people
going to try to do and what are they
going to expect? Are they going to
expect this button and that button? But
still
there's that new level Yes, you didn't
have to learn how to code, but you had
to learn how to use the UI. So you still
have to learn this paradigm that's
forced upon you. And we've all been in
UIs that are terrible where you're just
like, "Dude, what the heck? This Why is
this button here? Why or whatever." And
it just sucks. And ultimately, what that
user interface is a slightly simpler way
for us to tell a machine what to do,
right? And so, if it's not telling it
with programming, it's telling it with
some user interface that someone
created. And by the way, it's never
perfect. Like, um for me, I I've got
this like um very niche thing where I
have hearing aids and I and I can
connect them via Bluetooth, but it's not
normal Bluetooth. It's this other thing.
And for me to access it, I have to go
into the accessibility menu on Mac and
scroll down and click on this thing and
do this pairing. And then there's not
like an easy disconnect if I want to
switch to headphones. I just have to
forget it every time. Super cumbersome.
But Apple has given me no other simpler
way. And they don't give me the ability
to make my own little like app on top of
it where I could just I literally just
want to push a button and say connect or
disconnect, right? So I'm forced to live
inside the paradigm that Apple made. And
I Hey, I'm glad they made it a couple
clicks instead of having to write code,
but it still sucks. I would love to just
use human language and say "Disconnect
my hearing aids," right? And I think
that's the point you're making and that
Ben Thompson is making too, which is
like at the end of the day, we all just
want to talk to the machine, to the
agent, to the computer, to the phone,
tell it what we want, have it give it
back. And of course, the beautiful thing
and and Ben Thompson talks about this
about like generating UI too is like if
it gives it back to you in text or in uh
speech, but you're like, "I'm visual,
create a nice visualization for me. It
can just on demand create a
visualization for you. And so, I you
know, I definitely think that's the
world where apps are going, but I think
to your point that can impact like how
we interact with things at the edge and
make the edge much more interesting if
we sort of expand our mind to say,
how could we interact with AI? How could
we control computers? How could we
re-visualize and rethink things?
&gt;&gt; Yeah, so the edge device is inherently a
multimodal device, right? It does video,
it does text, it does audio, everything.
And so, technically, you could uh
use it in any way that is most useful to
you. And you could ask AI to give you
the format that suits you best as well.
And one thing I'll tell you I tried to
do for this episode, so I was looking
through some briefing notes for
preparing for this podcast and I was
like,
wait,
Austin just got back from Hawaii.
I'm going to see if I can make him a MP3
file that you can use while you go on
your run in the morning so that you go
come back in the morning from your run
to the podcast and you're like, oh, I'm
briefed, right? So, if you look in the
Google Drive folder, you'll actually
find an MP3 file there. It didn't really
work out just like a little bit robotic,
so I have to figure out how to fix that,
but you see what I was trying to do here
is give you a format that will suit you
better. So, you don't have to sit at
the, you know, computer and like read
the text like PDF file I created for
this podcast, right? You could just go
on a run and get your information. And
how did that happen? With AI, right? I
mean, you could you could read out,
obviously you could you have dictation
apps that just read stuff to you and
they do pretty well, too. But like it's
another app, okay? Like I just want AI
like give you the format you wanted
best.
&gt;&gt; Dude, Vic, this is such a great example.
Vic is my ideal agent. He knows all
about me. He has the context. He knows
that I run. He knows that I like to
listen to information. He knows that
there's something on my calendar called
our podcast recording that I need to
prepare for. And he went so far as to
put everything together in MP3, which I
totally didn't even see. My apologies,
but I love the heart behind it. Um but
of course, this is the future. And then
of course, maybe someday it's not you
doing this for me, but it's an AI
knowing so much about me and then
preparing me in the way that best suits
me.
&gt;&gt; Yeah, and it's your edge devices that
know you with the best, right? Your your
watch knows how long you run. I don't
know how long you run. I don't know
where you run.
&gt;&gt; Yeah, that's [laughter] true.
&gt;&gt; know so many things about it. Like
I don't have entire context. I have some
context because like I generally know
what you're up to. You're like, "Hey,
I'm I just got back from my run. I'll
see you in a bit." is what you were like
texted me before the show. So I
generally know what's going on, but your
devices know way more than me about you.
&gt;&gt; [laughter]
&gt;&gt; Yeah, yeah, yeah, that's true. And And
that doesn't necessarily mean that it
all even has to run at the edge, but
they obviously have all that context and
could recognize like, "Oh, generating
this piece of actually generating the
MP3, that's big. Go run that in the
cloud somewhere." Or Or who knows, man?
My phone could probably do it just fine
if it's By the way, I'm just running, so
it's just chilling, not doing anything.
It's fine if it's slow, you know, to
process that.
&gt;&gt; So it knows that hey, you know, what
your phone is not going to be really
useful right now. You're not like
browsing on it or anything. You're not
gaming on it. Uh maybe you do before you
go to bed or when you want to relax, you
just like game on your phone. And that
time you're like, "Okay, let's not run
some agentic stuff now. He's gaming,
okay?" Like Austin usually plays on his
phone from like 7:00 to 7:30 p.m. And
maybe then he grabs dinner and goes to
bed or whatever. So that information it
knows. So the role of the edge device
now is a context translation layer. So
it takes the inputs it knows about you,
when you run, what you do, when you
play, when you sleep, and then it
manages its own workloads and decides
what can happen locally.
Maybe a simple translation to an MP3
file from text can happen locally. Why
does it need a frontier model? It's a
It's a rather simple task, right? Or
maybe
it needs to be in a different language
to somebody else. Maybe that translation
of a document can happen easily. Those
are simple tasks. Just run them on the
phone. It's not like it's something
frontier. I'm not asking you to, you
know, you know, find some hard problem
to solve. Like, maybe it can run on the
device and the rest of it send it to the
cloud and decide when to send it to the
cloud. Maybe some answers you don't
need. Like, I have a podcast recording,
uh, you know, then in the next few days
I've actually lined up a couple of them.
Um, you know, so my agent already knows
that this podcast is only 3 days away.
So, it doesn't need to make make the
briefing document now. It It just needs
to handle that in 2 days. So, my edge
device can find out when's the best time
to get this done cuz all the context
lives on it. So, that's the That's the
reimagination of the edge in the sense.
&gt;&gt; Yeah. Yeah, I love it. And, uh, so I'm
going to take it back to that I
mentioned Jev, the sort of fast-thinking
system one model from Type Safe AI,
which people if you haven't heard about
it, you should go look it up, check it
out. I wrote an article about it as
well, um, this past week. And this type
of model is really good for just making
fast decisions. And what is a lot of
what we're talking about? A lot of it's
just little fast decisions, like looking
at context, deciding if something needs
to be done, looking at the time of day,
deciding what needs to be done. Large
language models are great at prose.
They're writing natural language.
They're doing that decode loop over and
over and predicting the next token and
it takes a long time. Sometimes you just
need a fast decision. Now, the ironic
thing is Jev launched their fast
thinking model as a cloud offering.
I think that's the wrong place. I think
it should live on the edge. I think it
Of course, I don't know how they would
make money that way. So, I think that
this might be one of those use cases
where they made really good technology
and now everyone's going to take it and
go make edge versions. So, I hope they
get acquired and and have you know, get
some sort of upside out of all the good
work that they did. Um but I don't think
again just making the same point over
and over that like it has to be the big
um I take in English and I write back
out English massive models. I think
there could be lots of little models
that help with all of these little
decisions at the edge.
&gt;&gt; And there are so many modes of operating
this edge device that I feel like we
haven't actually explored all of them
yet.
In my own mind, what I'm doing with all
these things is very limited context.
Like I'm not doing anything dramatically
different from what I have done in the
past. I am only adapting my existing way
of working somehow into the world of AI,
but it doesn't have to be that way.
There could be a complete reimagination
of how we do all of this. Before the
show, I was thinking, what do I really
need in my laptop, really? Is it all
that I Let's assume bulk of the
inference happens in the cloud just for
a minute. Do I even need a keyboard?
Like is a screen with a speaker enough
as a device? Like what is the simplest
device that could be useful for an edge
device? Like literally
like a very few in inference chips, a
screen, and a microphone.
That's it. And the radio communication
device. Don't forget. Like it has to be
wireless. Nobody wants to be connected
with wires. So, a radio device, a
microphone,
a speaker, and a screen. That should
take care of everything for you.
&gt;&gt; So good, man. Um I I totally agree. And
Okay, so that makes me want to go to
wearables and to how do you orchestrate
across all this and we'll get there in a
second, but I do want to go back. You
were kind of breaking things down and
going up from first principles, which is
like, what is just the the basic things
that I need? And so, you were talking
about you're forcing AI into your
existing workflow and you're saying,
wait a minute, no, no, I should build my
workflow around AI. And that reminds me
of two things. One, it reminds me of
that transition from the horse-drawn
carriage to the automobile, where the
automobile was literally a horse-drawn
carriage with an engine. Basically, it's
like it didn't have It was like open air
and it had the wooden wheels and
everything and clearly they kind of like
just bolted on an engine. Only much
later do we you know, reimagine. I mean,
you could argue that even it's really
like the robo-taxis also reimagining
things of like, guys, what if it's just
a car and you don't even have to drive
it and should even have a steering
wheel, you know, so there's obviously
ways to reimagine something once the
technology is there. And then and of
course, it reminds me even also of like
when electricity first happened, you
know, it's like
taking existing um manufacturing
workflows and saying like, ah, how do we
stick like some sort of engine or you
know, conveyor belt or something in here
instead of reimagining the whole
manufacturing line around electricity,
right? And so, this is what we need to
do with AI. Um this is what we're trying
to do with our
uh you know, podcast, too. And
everything you've talked about about
thinking how do we prep and how do we
manage this, you know, is like how do we
put AI at the center and build our
podcast around of it instead of our the
way we've been doing our podcast and
inserting AI. Hopefully, we'll have more
anecdotes to share with people over
time. Uh you know, victory stories
there. But, here's one question.
Okay, so you built up um saying like,
hey, really all I need is like I just
need context. That's all I really need
is be able to give context to the AI and
then to somehow receive context back.
Maybe it's I hear it, maybe it's I see
it on a screen. And you're even saying
maybe I don't need a keyboard because
keyboards are a slow way to give
context. I just want to speak it now. Um
okay, so then the question is like
that's obviously very promising for what
Qualcomm was saying because they're
literally saying we've taken our
Snapdragon processor and we've made it a
little so like different little form
factors so you can have a Snapdragon
wear and make wearables or you know,
make earbuds or make glasses or watches
or whatever. All that's very promising.
And of course you could do it on the
phone, you could do it in the car, that
kind of thing. Um, so then the next
natural question is like and and and and
then I I posited that maybe someone like
Meta who has the correct business model
and is incentivized to today both
subsidize agentic AI in the cloud, but
then eventually optimize and bring those
costs down and make it more affordable
by pushing more and more stuff to the
edge. So then the question is
oh man, this could be lots of different
hardware, lots of different little
interfaces. Yes, lots of it's
Snapdragon, but lots of it isn't. So how
do you ideally make sure that stuff can
run everywhere? You let's say you're
Meta.
Ideally, you're you're not going to want
to write an Android app and an iPhone
app and all these different things
everywhere. And so then where my head
went is
when I was at Snapdragon Summit, I had
the fortune of having dinner with Chris
Lattner, CEO of Modular, and he's famous
for creating the Swift programming
language, creating VLLM. Um, you know,
he worked at Google on their TPUs. I
think he had he had a stint um, at Tesla
even. And I got to sit across from him
and ask him a lot about Modular and his
vision. And Mojo is their programming
language and it's like Python but
better. It's it's statically typed. Um,
it has like safe memory access and stuff
like that.
And he using Mojo and then they have Max
which is like an LLM serving layer. Um,
and they had already they actually
started by showing that using Mojo you
could run models on CPUs. It could be an
Intel CPU, could be an AMD CPU. Now
they've also showed that um, you know,
they can
you can use their software and their
technology to run models on Nvidia and
on AMD and maybe even like Google TPUs,
I can't remember, but like on lots of
different accelerators. And so,
naturally where my head goes is like, oh
wow, Qualcomm bought Modular. Mojo could
be a great way for someone like Meta to
say, let's use one programming language
and one tool chain to the extent
possible and write kind of orchestration
software to make sure that these models
could run anywhere.
And so, I'll be very interested to see
if that actually happens, but it's quite
promising for Qualcomm that not only do
they have the hardware platform, but
they have the right software, which is
being open sourced because as a hardware
merchant vendor, they don't need to make
money, they don't need to like try to
keep it as a proprietary thing like CUDA
where it's like, no, no, we want you to
get accustomed to our software so that
you buy our hardware. But instead,
they're just say, hey, our hardware's
here, let it compete on its own merits,
but by the way, here's this open source
software that we've bought and are
providing and you could use it to write
it and run it anywhere.
&gt;&gt; So, your point is like, I like how
you're bringing all these things
together. You're bringing Look, Qualcomm
is always has been at the edge. They've
had their moments of trying to go into
servers and all that. They may still do
it. But their strength really lies at
the edge.
Then they have Modular, which is a
software platform, for lack of a better
word,
to
run literally different pieces of
hardware.
Uh, and this software platform is the
glue that puts all of that together and
you can run like inference based on
that. And then, you've got somebody like
Meta who is incentivized to bring all of
that into the edge device. So, now you
you see all these things kind of align.
And uh,
in my own simplification of what a
fundamental AI interface device should
look like.
It seems like Qualcomm's radios and
their modems for their wireless
connectivity, their NPOs,
their CPUs because like, you know, you
could this could be your agentic VM,
your little iPad-like device. That's all
you need. And now you have your
microphone and your Bluetooth
connections and all of this stuff. All
of that ecosystem fits into Qualcomm's
product line today, right? And I think
that is their vision. And I was reading
their blog post about this and they
said, "This is the ecosystem of you."
The idea is that you are in the center.
It's not like the device is in the
center. No. It's not like the cloud
server is in the center of all of this
AI. It's you and like what you interact
with your outside world and what
gets taken care of by the edge device is
not your problem. When you ask a
question, it is not your problem whether
it's handled within the device on the
edge or it goes to the cloud. You don't
need to know. Right? That's where we
want to get to eventually with this edge
AI stuff. That's the vision I think
that's coming out of what Qualcomm is
saying.
Um
I I'm kind of starting to warm up to the
idea that this is interesting.
Uh but the question is like
what I'm waiting for, what I want to see
next is a clear definition of how any
kind of computing and what kind of
computing gives benefit at the edge. I
don't think I can answer that clearly.
I want to see that happen. Right?
&gt;&gt; Yes. Yes.
Yeah. And so I think you you captured
correctly that Qualcomm is making the
hardware that involves the radios and
the CPUs and the NPOs and GPUs available
everywhere. And it used to feel a little
self-serving because they came as a
radio company already at the edge. And
so like in the AI PC world, right? When
they're like, "Everything's going to run
the edge." And we're like, "Dudes, right
now only everything runs in the cloud.
It feels like you're just saying
everything's going to run on the edge
because you're a radio company and a SOC
company and you know, a smartphone
company, you want it to run at the edge.
But, we've seen so much progression with
first reasoning models which opened the
door to agentic AI and finally the
consumerification,
there's probably a better word, um of
agentic AI with Muse, with Grok Bot,
with Instinct. Muse definitely leading
the way
&gt;&gt; [snorts]
&gt;&gt; to all of a sudden it's like, "Whoa, I
can actually see a lot of people wanting
to run this at the edge." And then the
question is, "Well, why Qualcomm, why
not someone else at the edge?" Uh
there's lots of other CPU companies,
right? And I think um interestingly,
Qualcomm's advantage is having the full
stack, so having the radio and the
compute is is going to be an an
important part. Obviously, other people
can put it together, um but it it's
pretty advantageous for for Qualcomm.
Meta is a Yeah, you're going to say
something.
&gt;&gt; I have a I have a counter to that. What
about Huawei?
&gt;&gt; Well, there you go.
&gt;&gt; right? They have the whole stack.
&gt;&gt; Okay, so Huawei has the whole stack and
I'd love to talk to Huawei sometime. I
think this is totally exactly what they
can do, you know, they will probably be
banned from doing this in the United
States.
Um so, that's probably the only other
advantage that American companies have.
But yeah, Huawei totally has the whole
stack and could do this too.
&gt;&gt; MediaTek.
&gt;&gt; [laughter]
&gt;&gt; Yeah, MediaTek. Yeah, no no, MediaTek.
No, yeah, exactly. Yeah, MediaTek
&gt;&gt; These names are just coming to me. I'm
like, "Look, I think a bunch of these
companies can actually benefit out of
this this movement because I think a lot
of them have this
Think of all the companies that make
like phones. All these companies now
open to this. Like if they have a
CPU-like device and a radio-like device,
you're basically set.
&gt;&gt; [laughter]
&gt;&gt; Exactly. And microphones and screens,
yeah, totally. And this is why also,
listeners, we try to differentiate from
other podcasts because I'm very American
egocentric and Vic is uh you know, a
world traveler and uh so he's thinking
about all the companies in the rest of
the world. So I appreciate that. Um
So yes, phone companies will do well. Um
you know who else has a phone and who
could potentially play in all of this
space? Google. Google Pixel. Google has
a phone. Google has a watch. Google's
the original Google Glasses. Um they've
got the business model. Of course, the
question is do they have the moxie?
Clearly, um
Zuck and Alex Wang are just going after
it and taking advantage of this world
that we live in and making news happen.
Um
it just doesn't I don't see Google could
they've got everything they've got the
business model. They've got the hardware
from the TPUs in the cloud so they can,
you know, be vertically integrated and
have cost efficiencies there when they
run things in the cloud all the way to
the edge they've got all the brilliant
people all the models they've got
everything. They just don't seem to have
the product wherewithal and the courage
to just get out there and do it. Please
tell me I'm wrong, but um Google this is
your space to play in too. You can make
an amazing agent. You can make it run
everywhere. You can cost optimize it and
bring it all to the edge. But right now,
I say Meta's in the lead.
&gt;&gt; Yeah, so many things can happen. So many
things. Like this is an exciting time
because AI with agents and with these
personal assistants that we are seeing,
AI has finally come to the user and
we've said this in the
podcast before. Like the regular person
can now use it because everybody uses
messaging apps. If you can message
somebody and it gives you an answer,
which is what a lot of these apps can
do,
you are now in the masses. Like the
everybody has access to AI now.
Don't give somebody a chatbot they don't
know what to ask it. Like literally, I'm
not joking. Like there's like a barrier
to this. Like it's like the Google
search bar when it first came out.
They're like, "Okay, what do I type in
it?" Whatever you want.
I don't want anything. Like so that's
not the way to do it, right? And that
was a problem even in the Google era
when it came out. But like chatbot is
the initial like that this this whole
like open claw was like is totally for
the hacker types, okay? Like who the
hell knows how to spin up like a VM and
you know, install, give API keys and do
some command line stuff. Nobody knows
that.
Now we are in the consumer layer and
what's going to happen is very exciting.
&gt;&gt; Indeed. Indeed. And it it will have all
sorts of implications for the AI
infrastructure trade, which I know lots
of you listeners are here for. Um but
we're at the end of today's episode. So
that's your homework is to go think
about this and then, you know, write
comments on YouTube, send us emails,
follow us uh
daily.semidope.com. We have a daily
newsletter and go check out our
sponsors. So thank you for listening,
guys.
&gt;&gt; [music]
[music]
