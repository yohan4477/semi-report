---
source: https://daily.semidoped.com/p/new-episode-every-muse-user-gets
title: 🎙️ NEW EPISODE: Every Muse User Gets 2 CPUs and 8GB in Meta's Cloud. Your Phone Already Has That
date: 2026-10-01
kind: clipping
genre: etc
audience: everyone
subtitle: Meta's Muse and the push to edge inference, Qualcomm's Snapdragon and Modular acquisition, the end of apps as we know them, and more
---
Austin and Vik explore where AI agents will ultimately live: in the cloud or on our devices. They break down Qualcomm’s vision for agents running everywhere on its Snapdragon platform, unveiled at its recent summit. With the rise of expensive cloud-based agents like Meta’s Muse, there’s a powerful new incentive to push inference to the edge to save on cloud costs, potentially spelling the end for traditional apps.

This episode is presented by Crusoe. Try Crusoe’s managed inference for open models with $5 in free credits: <https://semidoped.com/crusoe>

**Things we cover:**

  * Qualcomm’s vision for agents on the edge

  * Meta’s Muse and the business model for local AI

  * The end of apps and the future of user interfaces

  * Modular’s role in running AI on diverse hardware

  * Why Google is lagging in the agent race

  * Using AI tools like Suno and Opus for creative work




 _This podcast is lightly edited for clarity._

**Last week, Qualcomm said agents will run on your phone, your glasses and your earbuds. But chip companies don’t decide where inference runs, app companies do. And the biggest app companies of our time right now, OpenAI and Anthropic, well, they only get paid when it runs in their cloud. So who will actually make local AI happen?**

**Maybe the company that makes its money on ads and already ships Snapdragon in its glasses, like Meta. Or Google. But do they have the moxy? Let’s get into it.**

## New AI-Generated Intro

**Hello everyone. I’m Austin Lyons. Welcome to another Semi Doped episode. I write Chipstrat, a semiconductor and AI infrastructure newsletter for investors and tech executives.**

**Vik** : Hey, I’m Vik Sekar. I’ve worked in the semiconductor industry for about 20 years, mostly on engineering. I’m the founder of Semi Exponent where I do independent semiconductor research, mostly focused on AI and infrastructure. And I also write Vik’s newsletter on Substack where I just explain how things work and what matters to the markets. So that’s what we bring to the newsletter. Check us out on our substacks where we write a whole lot of stuff every week.

**Yes, totally. Vik, I know you wrote some stuff last week, but let’s not talk about that. Let’s talk about our new intro. Tell me about our sick new intro.**

**Vik** : Yeah, that was, by the way, all done with Opus 5.5. We have our podcast brand document. And all I did was I gave it a brand document PDF and was like, just make me a motion graphics intro. And our branding document has basically the theme it’s based off of, like the field and the single point of singularity, and our designer put in these phrases in there.

So it just used that and built the whole thing out. And I was like, this is insane. And I told it a few other things, like make it six seconds, make it 30 seconds, and I tried different things. And I was like, wait, wait, the logo stays for too long. Make the logo stay for lesser time, make the animation slower. It’s insane. That’s what it came up with. That’s pretty crazy. And then I used Suno AI, which is a music generation thing.

If you get the paid subscription to the tool, you can actually generate commercial music. You can use that in podcasts and other things to make money off of. Not as a sponsor, but they could very well be, I suppose. Really, it’s so cool. I kept trying different things. I said, hey, make some jazz fusion. I’m like, nah, this sounds like elevator music.

And I’m like, I don’t know, I want something exciting. And I told it, build it up and give it something in the beginning that’s repetitive, but I want a climax finish and then goes to slower things where we can talk over it and things like that. I don’t know, it all works just fine. And then our editor takes it and runs with it with the magic there. So all this is really nice. AI.

**Pro AI. Dude, so good, so amazing. I love that the Suno, you still had to have taste. You’re able to use Suno to generate the music, which is incredible, and really speed things up as opposed to what you would have to do previously, contact someone who knows how to do this or figure out how to make music yourself with your computer.**

**But you had the taste to say, oh, here’s what I’m listening for. I need it to build. I want there to be a hook. I need it to be catchy.**

**Vik** : Yeah, so, yeah, clearly I am a musician and I have recorded music and I kind of know what to say to it. So that little bit of domain expertise actually helps to tell it what to do. Otherwise, it’s very impressive. I think most people can do something with it.

**Awesome. I love it. Okay, so let’s talk about what else is new in this episode. So we have a presenting sponsor.**

**Vik** : Yes. Awesome. We have Crusoe. This is our first episode with a presenting sponsor. We’re very excited.

**Very excited, really stoked to partner with them and hang tight and you’ll hear our first ad read and you’ll get to learn more about them. But it’s going to be fun and you’re going to learn a lot about them. There’s so much to learn about Crusoe and we’re going to do fun ad reads every single week and they’ll be different. So stay tuned, listen to them, check them out. They sat down with us and we spent a lot of time talking about all their value props and their interesting technology from top to bottom.**

**So you’ll get to learn about that too over the next couple months. But with that, let’s get into it.**

## Qualcomm’s Vision for Agents on the Edge

**I was at Snapdragon Summit last week in Maui, in Hawaii. It was awesome. There was a tropical storm incoming, which I didn’t even know, but some other analysts are like, hey, my mom or my wife called and said they saw on the news that there’s a tropical storm that’s going to hit Hawaii. I was like, oh man, really? I’m just too busy enjoying the beach to even notice.**

**But we got out before it was a problem. But yeah, let’s talk about Qualcomm. So I think that of course everyone may have seen I did an interview with Durga, which was really interesting and talked about high bandwidth compute. And that was mostly because Durga was there and I was super excited to talk about it. But the name of the game for Snapdragon Summit, my takeaway was Qualcomm really talking about a vision for agents running anywhere.**

**And the fact that their Snapdragon SOC, they have different flavors of it that can run in watches, in augmented reality glasses, on your phone, on your car, in your laptop. And so naturally, Qualcomm as a hardware vendor, their vision is agents that can run anywhere.**

**Vik** : Sometime ago, if you had told me agents are going to run on the edge, I think the perception I would have had is LLMs are too big. How are you going to run a frontier LLM that is intelligent on your phone? And clearly we will never have, I don’t know, a terabyte of memory on the phone to run a trillion parameter model.

And clearly scaling laws still hold, which means the bigger you make a model in terms of its parameters, the smarter it seems to get and we still haven’t seen the end of that. So I would have laughed at the idea of what’s no way we can have that running on our phones, right? But in talking with you just before the show and also reading a little bit about this stuff and the event that Qualcomm just had, it seems like there is a different way to think about it.

Agents could be a portal into our world of AI and we’ll clarify what that means. It’s very interesting.

**Yeah, you know, you make a really interesting point, which go back a couple years. Remember Intel, Pat Gelsinger, he talked a lot about AIPCs and there’s this big push. Yeah, we’re going to have these AIPCs. They’ve got NPUs and everyone’s like, oh, how many tops does your NPU have? Mine has 35, mine has 45, mine has 55. And it was all about the idea was running AI locally.**

**But at the time, it was LLMs. And first of all, there were barely any open source LLMs when that started. And then when they came out, it’s a 70 billion parameter and it barely fits on your laptop and your NPU really can’t chug along and do too much. And so everyone’s like, dude, what are we doing here? This is going to be slow. What’s the use case? And ultimately, AIPCs were kind of a dud. Everyone just ran their AI in the cloud.**

**And I think now we are getting closer to a world where there will be useful AI and we can get into this that could run at the edge and it doesn’t have to be an LLM. It doesn’t have to be a frontier trillion parameter LLM. But we can get into that. I will say, we’re still in this transitory world where and and we’ll get into this where you can see a world that we’ll run AI at the edge and yet there’s still talk about, oh yeah, we can run all of this agentic AI, for example, Claude and Codex and, you know, Open Claude, Perplexity, and a lot of that is still running in the cloud.**

**So there’s still a little bit of, we’re envisioning a world to come, but we’re still talking about apps that actually run in the cloud. But obviously I think Muse comes to mind as truly agentic AI and then where that could go is pretty interesting. But yeah, I’ll hand it over to you.**

## The Business Case for Edge AI

**Vik** : The app thing is very interesting. So recently I have gotten very much, let’s say AI pilled, not that I wasn’t already. But the reason is given the substack and now I’m running, I’ve been talking to prospective clients about Semi Exponent and institutional research for financial firms and things like that. And then we have the podcast, right? And then we have so many podcast briefings and recordings and back and forth of documents. It’s a large universe that we deal with, really. And so I have been thinking, this needs to be more agentic AI for me. I really need the help. I could go off and hire people and all that, but I was like, okay, let me see what parts of this. It’s not like human taste isn’t important. It is. And we do have people who work with us on the podcast. We do need people. I’m not saying we’re going to replace everything.

But I’m like, just what can AI take care of for me? Because there’s a minimum requirement for some things, the MVP in my life. What can it do? So the app itself, the phone has become a very big part of my day. And the reason is, I have ChatGPT, I have Claude too. So, when I’m making coffee, literally, ChatGPT reads out to me whatever has come to me. Or I read it out or whatever. It doesn’t matter, but it’s all in one place. It’s become an integral part of my morning. And so, yes, AI doesn’t run on my device, but it’s become a portal for me to handle tasks during the day. And this is what Qualcomm has been saying, except that their view is that a lot more inference runs on the device.

Maybe we are not just there yet, but I can see where we are headed. Because it’s become so important for me that every hour, right? I don’t want to miss emails and all that, because some emails require me to respond immediately. So, I have another scheduled task that reads my emails and tells me every hour. So, a notification comes up on my phone. Hey, somebody’s asking you to do this. Here’s another great example. I messed up and I always get time zones wrong.

And anybody who’s worked with me on this, I always get rescheduling invites for my calendars and I always get, I can’t do math in my head, I guess. So it sent me a notification and says, hey, your email says that you’re going to meet with this person at this time, but your scheduled meeting is one hour late. Are you sure this is what you want to do? Or do you want to move it? I’m like, oh my God, I told ChatGPT, remember to put that on my to-do list and put it on my task calendar.

Because it’s hooked up to Google, right? And so it made it, so it’s put on my to-do list and I just have to go and send, reschedule it. I could ask it to do that too, but I’m just not interfacing with other people yet, because I don’t want it to keep sending stuff to other people. Could be done automatically, but you see where this is going, right? I know inference doesn’t run on the device yet, but on the cloud, it’s still useful.

Edge devices have been useful to me already.

**Yeah, yeah, I love that use case. Good job, ChatGPT, by the way, for keeping things straight and figuring it out.**

**Vik** : I wouldn’t even have showed up to this podcast on time. I would have been one hour late.

## Sponsored by Crusoe

**Vik** : This episode of Semi Doped is presented by Crusoe. Crusoe builds AI infrastructure from the ground up. Power, data centers, and the cloud on top. Crusoe Intelligence Foundry is their managed AI platform. And a nice feature in there is serverless inference. Now, if you’re going what in Jensen’s name is that, it means that there are no GPUs for you to provision and no clusters to manage. You simply pay per token.

If you’re running open models, like GLM, DeepSeek, Kimmy, O, Crusoe’s managed inference is fast, nearly 10x faster, time to first token, and 5x the throughput of vLLM. Their memory alloy caching layer routes requests to maximize cache hits. Since it works with OpenAI SDK, switching over to Crusoe’s API is quick and easy to get it running. All you have to do is pick a model, grab an API key, and start sending requests.

If you sign up with the link in the show notes, you get $5 in free credits to try Crusoe Intelligence Foundry. Think of it, five whole bucks, so you can just burn some tokens just for fun. And some of these open models are quite inexpensive, so you’ll actually have a ton of fun with it. Check out Crusoe and see their serverless inference on their managed AI platform. You really got to find out this for yourself. There are a whole lot of more features in this that I want to try out for myself.

But serverless inference I’ve found is the best place to get started. It’s a great way to support the show and try out Crusoe’s Intelligence Foundry. The link is in the show notes, and now back to the show.

## The End of Apps and the Future of UI

**Previously, when everything was just running ChatGPT, chatting with ChatGPT, or chatting with Codex, still everyone is still focused on, oh, it’s got to be Fable, it’s got to be the frontier model. What I think has been really interesting lately is Muse and Instinct, GrokBot, and these agents where you realize, one, I could see this going to actual normal consumer adoption, because it’s so simple to use, you can, there’s billions of people that have Meta’s family of apps installed.**

**And it’s very simple for them to get up and running with Muse. And by the way, when they sign up for Muse, they get a dedicated, what is it? Like two CPUs, a dedicated cloud VPN. It’s like two CPUs, eight gigabytes of RAM. I think I even saw maybe 100 gigabyte of storage. Or maybe that was Tom’s Hardware speculating or something, but clearly quite a beefy computer for every single person.**

**And so on the one hand, this is crazy powerful that all these people can spin up agents that can actually go do useful stuff. And by the way, my use case for Muse, because I was like, okay, I want to try this out, what am I going to do? And I’ve got all this electronics and old recording equipment and stuff like this sitting just next to me in my office, and it kills my wife because she’s a minimalist and she’s like, this junk is sitting here, do something about it. I’m like, literally, she’s like, it has so much value, it’s just sitting there.**

**Just sell it on Facebook marketplace. I’m like, I just don’t have time. I just don’t have time to take pictures, write out all the listings, look up how much everything should cost. And then I was like, wait a minute, this is perfect for Muse. I’m just going to take pictures of everything and tell it, bro, just post this on Facebook marketplace. I don’t care what the price is, you pick a good price. You make a nice listing and I just gave it a bunch of pictures. And it actually did an awesome job. It looked up what everything was called and wrote really great descriptions, figured out the prices and posted it and everything.**

**And so I’m like, dude, that is truly useful work for me. And I even may make some money out of it. And but even more importantly, of course, I’m going to make my wife happy. So, happy wife, happy life. But, here’s an interesting thing. I was like, oh man, I’m using all this stuff that was provisioned for me in the cloud, but then I stopped using it and so I’m like, is it just sitting there? Are they sharing it with other people? But I was thinking, man, if I get this just cranking all the time for me, Muse is so handy, so convenient because it’s on my phone.**

**And so I was actually checking it when I was in Hawaii, people are responding like, hey, can I buy this? So I tell Muse like, tell everyone, no, I’ll get back to you when I’m back from vacation, but don’t tell them I’m gone. I don’t want to rob my house. So just tell them, I’ll get back to you this weekend. And so Muse is doing that for me. And I just thought, again, hey, some of that stuff, it’s here’s my phone right here and it’s pretty simple. They’re paying a lot of money in the cloud to reserve this infrastructure and use it for me.**

**But couldn’t some of this very simple stuff like sending someone a message, couldn’t that actually happen on my phone? So, it just got me thinking, hey, maybe app companies who end up spending a ton of money in the cloud, like maybe Meta, maybe they will be the ones who are incentivized to actually push a model down to my phone and try to orchestrate and have some of it run locally when it can.**

**Vik** : Yeah, that’s very interesting. The fact that you mentioned that everybody gets a virtual machine in some cloud instance somewhere. Actually, I sat down, the Substack post this week was all about estimating how many CPUs are going to be deployed assuming, I don’t know, a billion VMs being in the cloud, like how many CPUs do you need? Because I think there’s a lot of excitement about CPU requirements. So, I calculated all this out.

It’s very interesting actually, because people can share CPUs. Everybody doesn’t need to get a dedicated VM. When it’s not posting your Facebook marketplace ad, it could go and help Vik get his calendar right, right? The same CPUs. Why should it just chill out? So, this kind of stuff is there. So, the second thing is, what we don’t have yet, I think, is, we’ve got 8 GB of RAM on this thing, right?

And we’ve got some computing power, like two vCPUs worth of computing power is right here. We’ve got some storage. I mean, I don’t know how much is in this thing. Maybe not 100 gigabytes. I need space for apps. Or do I? We’ll get to that soon. Do I really need apps anymore? Is a big question. So, although there’s all these CPU deployments on the cloud and everybody’s excited about the prospect of CPU, I’m like, look, my phone is already my portal to the AI world.

It’s happening right now. It keeps buzzing about all those scheduled tasks I have. You’re putting up stuff for sale. Everybody’s happy. Things are getting done. You’re making money. But then what’s my CPU doing here? Nothing. So, I’m like, why don’t we now start using this as our edge computing device where your two VMs and 8 GB of RAM live, so that you can just talk to this device and it has everything. It knows everything about you. It knows where you are. It knows how much you’ve walked in a day.

It could even listen to you. It knows who you’re talking to. All your devices connect to this. Your watch can connect to it. Your AirPods can connect to it.

## The Edge Device as a Context Hub

**Yes, yes, I totally agree. It and it’s all about all that context too. And that’s kind of the point you’re making. It’s like, you’ve got your watch, it’s got your health data, your steps data, maybe for me it logs my Strava, whatever. You’ve got your microphones, you’ve got your phone, which has not only of course your calendar and whatever, but it’s got the pictures that you’ve taken.**

**So there’s all this just local context on your watch, and your glasses, and your earbuds, and your phone. And so again, the idea, let’s say it’s just OpenAI and Anthropic. The idea that you would take everything local, send it up to the cloud, have it compute in the cloud, send it back down, feels a little crazy. And of course, in their world, and remember, OpenAI and Anthropic, these are two of the fastest growing companies ever, great companies, amazing app companies, whether they meant to become that or not in the first place because they’re both kind of research companies.**

**Their business model is we make money when we do inference in the cloud. And yet we are saying, actually, there’s a world where we would really like to just run this stuff locally because all of our context is here. You could have of course there’s privacy if you can just filter through things and take only what you need here and not don’t send up all my photos to the cloud, don’t send all this information to the cloud just so that you can compute it there and send it back down.**

**Like, why not do it here? And what’s interesting again is Meta stands out as a company who their business model is ads. It’s they just want to help me and have the opportunity to show me ads and just be part of my life essentially. Now, whether you like ads or not is a whole another conversation.**

**I think it can be useful. But there’s a disincentive of course for the model labs to want to come help me at the edge, but Meta’s like, bro, I want to help you at the edge. You’ve already got our apps installed, let me help you. And so Meta has already made open models. Meta has, I think they released Muse Glimmer, which is in this direction of running things locally, orchestrating, running on the edge.**

**So it’s very natural actually for Meta to say, hey, I’ve made Muse. It’s super helpful for you. It’s really expensive. You’ve got this cloud or this little VM here with these CPUs and the 8 gigs of memory, which is a very great point. It’s just sitting idle. We can give you more Muse if we can just run some of it locally.**

**I can imagine I hit my token limit and they’re like, yeah, didn’t that suck? We can make your tokens go farther. Let us run some, give us permission to run it on your phone when possible. And I would say totally. And this doesn’t even necessarily mean that it has to be the stuff like you said that requires that sort of system to deep thinking, deep research, you need a frontier model.**

**There’s lots of stuff that can be done at the edge that aligns with just helping my little agent, making some quick decisions and helping me with my life, looking through my context or whatever, before deciding what needs to go to the cloud.**

**Vik** : Yeah. So that’s the whole point because look at the app like you mentioned the Strava thing, and you run a lot and you keep track of your steps. You even post it on X and all that and you were like, when you were in Hawaii, you were like, look at this, I have 20,000 steps today, all that stuff.

Clearly it all runs on an app, but do you really need that app? There’s a fitness app sitting on your home screen, occupying the space and I have to find where it is or you have to type fitness and then you have to click on the app and it shows you the steps. Why do you need that? All you have to do is ask it how many steps and it has a screen.

That’s all it needs. It’s just a screen. Everything that happens on a phone can just happen. You don’t need an app for it. And this is a point that Ben Thompson recently made on Stratechery, which we are both big fans of that newsletter. He’s like the OG newsletter guy. I think at some point everybody who started a newsletter wanted to be like Ben.

So he made the point that there is no need for apps anymore because everything can be built and destroyed on demand. It’s very simple to do. Anybody can build an app for their own use cases and change it out if they don’t want to. Some things may not even need an app, like this fitness example, right?

So, where are we going in this world of devices? What do devices need to have? Do we need to think of them as computers or what is its function in the world of AI? Are really deep questions that we have to think about because that defines what AI is. Another point that Ben made, I want to mention this and I’ll ask you what you think because it’s a very important point.

He’s like, look, now there is no reason for anybody to code. There’s literally no purpose. It is a syntax that nobody understands with this braces and colons and indenting or whatever. We don’t need to deal with that mess, okay? You just ask it, it writes the code, it gives you, you don’t worry what happens in the background.

Now we have Muse and we have these CPUs and all that. These agents can even control your computer, like ChatGPT has a computer use. So now agents control your computer too. So you don’t need to even use your computer. Your computer is meant for your AI to use, not for you. Right? So you see where I’m going with this.

Yeah, yeah, yeah. So what is the device supposed to do now?

## The Software Layer: Modular and Mojo

**Oh, good. Okay. So this is a great setup. I have lots of thoughts. So the idea that we don’t need to code, I would say baloney to that, although many people don’t need to learn. But and by the way, I got that, Ben lives in Wisconsin right now and I was listening to this Guy Raz How I Built This with the guy who started Culver’s, which is if anyone knows, it’s a fast food restaurant.**

**It started in Wisconsin and it’s so funny because the guy’s so Wisconsin and instead of swearing on the episode, when he was really angry, he said, baloney to that. And I was like, oh, that’s so good. I have to use that. I wanted to. Yeah, thank you. So thank you. I wanted to swear, but I don’t want to get that explicit rating on our podcast with our sponsor.**

**But, okay, so as you said earlier, why could you make such a great little hook and little jingle with AI using Suno? It’s because you had domain expertise, because you’ve made music manually the hard way. Therefore, you knew how to prompt the AI. I think obviously with the best coding, it’s still going to be people who have written code and understand how to write good code and what good code looks like.**

**And and actually, and we’ll get into this a little bit later. There’s this new model that came out recently, Jev. And I won’t get into it right now because then I’ll get too distracted from the point that you were trying to make. But Jev, what’s really cool is it can you can use it to take in the world’s input.**

**So you could give it free form text or you could give it a chatbot conversation or a phone call or whatever. And then you can have it do simple things like classification, like, oh, here’s what I, I’m a bank, here’s what the person said. Should it go to fraud department, should it go to the payment department, whatever.**

**It’s literally just like a little, these are little classifiers or little switch statements or if statements if you will. But it can work crazy fast and it’s trained like an LLM on the internet’s corpus. So it’s very intelligent. And anyway, these are like new programming constructs that will actually go into code.**

**And if you zoom out and you think, wait a minute, today we’re in a world where the LLM just writes all the code end to end, but if you actually try to stick an LLM call in your code, it gets really funky because these LLM calls are they take a long time potentially, they’re not very bounded, they’re not typed, so you don’t quite know what’s going to come back.**

**It’s just a string that comes back and you have to parse it and figure out. And even if you ask for structured output, so it comes back as a JSON or something, it’s still very slow and it’s inefficient. So anyway, I say all this to say, there’s going to actually be new ways of programming, which the models aren’t even trained on yet.**

**So I think there’s all sorts of reasons why having domain experience as a programmer, sure for the Ben Thompsons, they don’t need to learn how to code. But for folks like you and I, knowing how to write RTL or knowing how to code will help you obviously be able to prompt it better. And then again, as we continue to even invent new ways of programming, someone’s got to prompt the AI to do that to train it on it.**

**But to the question of do we even need apps? Okay, this is actually really interesting. And I won’t bear the lead. I agree with you that we don’t need apps. And let’s think from first principles, why do we have user interfaces in the first place? At the end of the day, let’s take Excel for an example. Dude, at the end of the day, you could just have a database and a prompt and store data in a database and prompt use SQL and just say, hey, whatever, I’m trying to calculate my mortgage.**

**Like you could put you could either write all this stuff in the command line or put a bunch of data in the database and pull extract it out and make calculations.**

**But obviously, that’s a very difficult thing for people to learn. So we make these user interfaces like Excel where it’s very visual and you can have little if statements and summing and stuff like that and it’s super simple. But the problem with all user interfaces is someone has to decide what the rest of us are going to be forced to use.**

**And that’s why user interface designers are amazing because they’re almost like psychologists. They can think really well about what’s the best experience and what are people going to try to do and what are they going to expect? Are they going to expect this button and that button? But still, there’s that new level. Yes, you didn’t have to learn how to code, but you had to learn how to use the UI. So you still have to learn this paradigm that’s forced upon you.**

**And we’ve all been in UIs that are terrible where you’re just like, dude, what the heck? Why is this button here or whatever. And it just sucks. And ultimately, what that user interface is a slightly simpler way for us to tell a machine what to do, right? And so, if it’s not telling it with programming, it’s telling it with some user interface that someone created. And by the way, it’s never perfect.**

**For me, I’ve got this very niche thing where I have hearing aids and I can connect them via Bluetooth, but it’s not normal Bluetooth, it’s this other thing. And for me to access it, I’ve got to go into the accessibility menu on Mac and scroll down and click on this thing and do this pairing. And then there’s not an easy disconnect if I want to switch to headphones, I just have to forget it every time.**

**Super cumbersome, but Apple has given me no other simpler way. And they don’t give me the ability to make my own little app on top of it where I could just I literally just want to push a button and say connect or disconnect, right? So I’m forced to live inside the paradigm that Apple made. And hey, I’m glad they made it a couple clicks instead of having to write code, but it still sucks.**

**I would love to just use human language and say disconnect my hearing aids, right? And I think that’s the point you’re making and that Ben Thompson is making too, which is at the end of the day, we all just want to talk to the machine, to the agent, to the computer, to the phone, tell it what we want, have it give it back. And of course, the beautiful thing and Ben Thompson talks about this about generating UI too is, if it gives it back to you in text or in speech, but you’re like, I’m visual, create a nice visualization for me.**

**It can just on demand create a visualization for you. And so I definitely think that’s the world where apps are going, but I think to your point, that can impact how we interact with things at the edge and make the edge much more interesting if we sort of expand our mind to say, how could we interact with AI? How could we control computers? How could we re-visualize and rethink things?**

**Vik** : Yeah, so the edge device is inherently a multimodal device, right? It does video, it does text, it does audio, everything. And so technically, you could use it in any way that is most useful to you. And you could ask AI to give you the format that suits you best as well.

And one thing I’ll tell you I tried to do for this episode. So I was looking through some briefing notes for preparing for this podcast and I was like, wait, Austin just got back from Hawaii. I’m going to see if I can make him a MP3 file that you can use while you go on your run in the morning so that you come back in the morning from your run to the podcast and you’re like, I’m briefed.

Right? So if you look in the Google Drive folder, you’ll actually find an MP3 file there. It didn’t really work out. It’s a little bit robotic. I have to figure out how to fix that, but you see what I was trying to do here is give you a format that will suit you better. So you don’t have to sit at the computer and read the text PDF file I created for this podcast, right?

You could just go on a run and get your information and how did that happen with AI, right? I mean, you could read out, obviously, you have dictation apps that just read stuff to you and they do pretty well too. But that’s another app, okay? I just want AI to give you the format you wanted best.

**Dude, Vik, this is such a great example. Vik is my ideal agent. He knows all about me. He has the context. He knows that I run, he knows that I like to listen to information. He knows that there’s something on my calendar called our podcast recording that I need to prepare for. And he went so far as to put everything together in MP3, which I totally didn’t even see.**

**My apologies, but I love the heart behind it. But of course, this is the future. And then of course, maybe someday it’s not you doing this for me, but it’s an AI knowing so much about me and then preparing me in the way that best suits me.**

**Vik** : Yeah, and it’s your edge devices that know you the best, right? Your watch knows how long you run. I don’t know how long you run. I don’t know where you run. Right? I don’t know so many things about it. I don’t have entire context. I have some context because I generally know what you’re up to. You’re like, hey, I just got back from my run. I’ll see you in a bit.

Is what you texted me before the show. So I generally know what’s going on, but your devices know way more than me about you.

**Yeah, yeah, yeah, that’s true. And and that doesn’t necessarily mean that it all even has to run at the edge, but they obviously have all that context and could recognize like, oh, generating this piece of actually generating the MP3, that’s big, go run that in the cloud somewhere. Or or who knows, man, my phone could probably do it just fine if it’s by the way, I’m just running, so it’s just chilling, not doing anything.**

**It’s fine if it’s slow to process that.**

**Vik** : Yeah, exactly. So it knows that hey, your phone is not going to be really useful right now. You’re not browsing on it or anything. You’re not gaming on it. Maybe you do before you go to bed or when you want to relax, you just game on your phone and that time you’re like, okay, let’s not run some agentic stuff now. He’s gaming, okay? Austin usually plays on his phone from 7:00 to 7:30 p.m.

And maybe then he grabs dinner and goes to bed or whatever. So that information it knows. So the role of the edge device now is a context translation layer. So it takes the inputs it knows about you, when you run, what you do, when you play, when you sleep, and then it manages its own workloads and decides what can happen locally. Maybe a simple translation to an MP3 file from text can happen locally.

Why does it need a frontier model? It’s a rather simple task, right? Or maybe it needs to be in a different language to somebody else. Maybe that translation of a document can happen easily. Those are simple tasks. Just run them on the phone. It’s not something frontier. I’m not asking you to find some hard problem to solve like maybe it can run on the device and the rest of it send it to the cloud.

And decide when to send it to the cloud. Maybe some answers you don’t need. Like I have a podcast recording in the next few days. I’ve actually lined up a couple of them. So my agent already knows that this podcast is only three days away. So it doesn’t need to make the briefing document now. It just needs to handle that in two days.

So my edge device can find out when’s the best time to get this done because all the context lives on it. So that’s a re-imagination of the edge in the sense.

**Yeah, yeah, I love it. And so I’m going to take it back to that. I mentioned Jev, the sort of fast thinking system one model from Type Safe AI, which people if you haven’t heard of it, you should go look it up, check it out. I wrote an article about it as well this past week. And this type of model is really good for just making fast decisions.**

**And what is a lot of what we’re talking about? A lot of it’s just little fast decisions, like looking at context, deciding if something needs to be done, looking at the time of day, deciding what needs to be done. Large language models are great at prose, they’re writing natural language, they’re doing that decode loop over and over and predicting the next token and it takes a long time. Sometimes you just need a fast decision.**

**Now, the ironic thing is Jev launched their fast thinking model as a cloud offering. I think that’s the wrong place. I think it should live on the edge. I think of course, I don’t know how they would make money that way. So I think that this might be one of those use cases where they made really good technology and now everyone’s going to take it and go make edge versions. So I hope they get acquired and get some sort of upside out of all the good work that they did.**

**But I don’t think, again, just making the same point over and over that it has to be the big, I take in English and I write back out English massive models. I think there could be lots of little models that help with all of these little decisions at the edge.**

**Vik** : There are so many modes of operating this edge device that I feel like we haven’t actually explored all of them yet. In my own mind, what I’m doing with all these things is very limited context. I’m not doing anything dramatically different from what I have done in the past. I am only adapting my existing way of working somehow into the world of AI, but it doesn’t have to be that way.

There could be a complete reimagination of how we do all of this. Before the show, I was thinking, what do I really need in my laptop? Really? Is it all that I let’s assume,

## The Competitive Landscape

**So good, man. I totally agree. And okay, so that makes me want to go to wearables and to how do you orchestrate across all this and we’ll get there in a second. But I do want to go back. You were kind of breaking things down and going up from first principles, which is like, what is just the basic things that I need. And so you were talking about you’re forcing AI into your existing workflow and you’re saying, wait a minute, no, no, I should build my workflow around AI. And that reminds me of two things. One, it reminds me of that transition from the horse drawn carriage to the automobile, where the automobile was literally a horse drawn carriage with an engine basically. It’s like it didn’t have, it was open air and it had the wooden wheels and everything and clearly they kind of just bolted on an engine. Only much later do we really, you know, reimagine. I mean, you could argue that even it’s really like the robo taxis also reimagining things of like, guys, what if it’s just a car and you don’t even have to drive it and should even have a steering wheel. You know, so there’s obviously ways to reimagine something once the technology is there. And and of course, it reminds me even also of when electricity first happened, it’s like taking existing manufacturing workflows and saying, oh, how do we stick some sort of engine or conveyor belt or something in here instead of reimagining the whole manufacturing line around electricity, right? And so this is what we need to do with AI. This is what we’re trying to do with our podcast too and everything you’ve talked about about thinking how do we prep and how do we manage this, is like how do we put AI at the center and build our podcast around it instead of our the way we’ve been doing our podcast and inserting AI. Hopefully, we’ll have more anecdotes to share with people over time. Victory stories there. But here’s one question. Okay, so you built up saying, hey, really all I need is I just need context. That’s all I really need is be able to give context to the AI and then to somehow receive context back. Maybe it’s I hear it, maybe it’s I see it on a screen. And you’re even saying, maybe I don’t even need a keyboard because keyboard is a slow way to give context. I just want to speak it now. Okay, so then the question is, that’s obviously very promising for what Qualcomm was saying because they’re literally saying, we’ve taken our Snapdragon processor and we’ve made it so like different little form factors so you can have Snapdragon wear and make wearables or make earbuds or make glasses or watches or whatever. All that’s very promising. And of course, you could do it on the phone, you could do it in the car, that kind of thing. So then the next natural question is like, and and and then I posited that maybe someone like Meta who has the correct business model and is incentivized to today both subsidize agentic AI in the cloud, but then eventually optimize and bring those costs down and make it more affordable by pushing more and more stuff to the edge. So then the question is, oh man, this could be lots of different hardware, lots of different little interfaces. Yes, lots of it Snapdragon, but lots of it isn’t. So how do you ideally make sure that stuff can run everywhere? Let’s say you’re Meta. Ideally you’re not going to want to write an Android app and an iPhone app and all these different things everywhere. And so then where my head went is when I was at Snapdragon Summit, I had the fortune of having dinner with Chris Lattner, CEO of Modular, and he’s famous for creating the Swift programming language, creating LLVM. He worked at Google on their TPUs. I think he had a stint at Tesla even. And I got to sit across from him and ask him a lot about Modular and his vision. And Mojo is their programming language and it’s like Python but better. It it statically typed, it has safe memory access and stuff like that. And he using Mojo and then they have MAX, which is an LLM serving layer. And they had already so they actually started by showing that using Mojo, you could run models on CPUs. It could be an Intel CPU, it could be an AMD CPU. Now they’ve also showed that you can use their software and their technology to run models on Nvidia and on AMD and maybe even like Google TPUs, I can’t remember, but on lots of different accelerators. And so naturally where my head goes is like, oh wow, Qualcomm bought Modular. Mojo could be a great way for someone like Meta to say, let’s use one programming language and one tool chain to the extent possible and write kind of orchestration software to make sure that these models could run anywhere. And so I’ll be very interested to see if that actually happens, but it’s quite promising for Qualcomm that not only do they have the hardware platform, but they have the right software, which is being open source because as a hardware merchant vendor, they don’t need to make money, they don’t need to try to keep it as a proprietary thing like CUDA where it’s like, no, no, we want you to get accustomed to our software so that you buy our hardware. But instead, they’re just say, hey, our hardware is here, let it compete on its own merits. But by the way, here’s this open source software that we have bought and are providing and you could use it to write it and run it anywhere.**

**Vik** : So your point is, I like how you’re bringing all these things together. You’re bringing look, Qualcomm has always been at the edge. They’ve had their moments of trying to go into servers and all that. They may still do it, but their strength really lies at the edge. Then they have Modular, which is a software platform for lack of a better word to run literally different pieces of hardware. And this software platform is the glue that puts all of that together and you can run inference based on that. And then you’ve got somebody like Meta who is incentivized to bring all of that into the edge device. So now you see all these things kind of align and in my own simplification of what a fundamental AI interface device should look like, it seems like Qualcomm’s radios and their modems for their wireless connectivity, their NPUs, their CPUs because you could this could be your agentic VM, your little iPad like device. That’s all you need. And all you have your microphone and your Bluetooth connections and all of this stuff. All of that ecosystem fits into Qualcomm’s product line today, right? And I think that is their vision and I was reading their blog post about this and they said, this is the ecosystem of you. The idea is that you are in the center. It’s not like the device is in the center. No, it’s not like the cloud server is in the center of all of this AI. It’s you and what you interact with your outside world and what gets taken care of by the edge device is not your problem. When you ask a question, it is not your problem whether it’s handled within the device on the edge or it goes to the cloud. You don’t need to know, right? That’s where we want to get to eventually with this edge AI stuff. That’s the vision I think that’s coming out of what Qualcomm is saying. I’m kind of starting to warm up to the idea that this is interesting. But the question is, what I’m waiting for, what I want to see next is a clear definition of how any kind of computing and what kind of computing gives benefit at the edge. I don’t think I can answer that clearly. I want to see that happen, right?

**Yes, yes. Yeah. And so I think you you captured correctly that Qualcomm is making the hardware that involves the radios and the CPUs and the NPUs and GPUs available everywhere. And it used to feel a little self-serving because they came as a radio company already at the edge. And so in the AI PC world, right, when they’re like, everything’s going to run at the edge. And we’re like, dudes, right now, only everything runs in the cloud. It feels like you’re just saying everything’s going to run at the edge because you’re a radio company and an SOC company and a smartphone company and you want it to run at the edge. But we’ve seen so much progression with first reasoning models, which opened the door to agentic AI and finally the consumerification, there’s probably a better word, of agentic AI with Muse, with GrokBot, with Instinct, Muse definitely leading the way to all of a sudden, it’s like, whoa, I can actually see a lot of people wanting to run this at the edge. And then the question is, well, why Qualcomm? Why not someone else at the edge? There’s lots of other CPU companies, right? And I think interestingly, Qualcomm’s advantage is having the full stack, so having the radio and the compute is is going to be an an important part.**

**Vik** : I have a counter to that. What about Huawei? Well, they do, right? They have

**Well, true, there you go. Obviously, other people can put it together, but it it’s pretty advantageous for for Qualcomm.**

**Vik** : I have a counter to that. What about Huawei? Huawei has the whole stack too, right? They have a whole stack.

**Well, there you go. Okay, so Huawei has the whole stack and I’d love to talk to Huawei sometime. I think this is totally exactly what they can do. They will probably be banned from doing this in the United States. So that’s probably the only other advantage that American companies have.**

**But yeah, Huawei totally has the whole stack and could do this too.**

**Vik** : MediaTek.

**Yeah, MediaTek. Exactly.**

**Vik** : I just have these names are just coming to me. I’m like, look, I think a bunch of these companies can actually benefit out of this this movement because I think a lot of them have this think of all the companies that make phones. All these companies now open to this. Like if they have a CPU like device and a radio like device, you’re basically set.

**Exactly. And microphones and screens. Yeah, totally. And this is why also listeners, we try to differentiate from other podcasts because I’m very American-egocentric and Vik is a world traveler and so he’s thinking about all the companies in the rest of the world.**

**So I appreciate that. So yes, phone companies will do well. You know who else has a phone and who could potentially play in all of this space? Google, Google Pixel. Google has a phone, Google has a watch. Google’s the original Google glasses. They’ve got the business model. Of course, the question is, do they have the moxy?**

**Clearly, Zuck and Alex Wang are just going after it and taking advantage of this world that we live in and making Muse happen. I don’t see Google could, they’ve got everything. They’ve got the business model. They’ve got the hardware from the TPUs in the cloud.**

**So they can be vertically integrated and have cost efficiencies there when they run things in the cloud. All the way to the edge. They’ve got all the brilliant people, all the models, they’ve got everything. They just don’t seem to have the product wherewithal and the courage to just get out there and do it. Please tell me I’m wrong, but Google, this is your space to play in too.**

**You can make an amazing agent, you can make it run everywhere, you can cost optimize it and bring it all to the edge. But right now, I say Meta is in the lead.**

## Conclusion

**Vik** : Yeah, so many things can happen. So many things. Like this is an exciting time because AI with agents and with these personal assistants that we are seeing, AI has finally come to the user. And we’ve said this in the podcast before, the regular person can now use it because everybody uses messaging apps.

If you can message somebody and it gives you an answer, which is what a lot of these apps can do, you are now in the masses. Everybody has access to AI now. Don’t give somebody a chatbot, they don’t know what to ask it. Literally, I’m not joking. There’s a barrier to this. It’s like the Google search bar when it first came out.

Like, okay, what do I type in it? Whatever you want. I don’t want anything. So that’s not the way to do it, right? And that was a problem even in the Google era when it came out. But chatbot is the initial, right? This whole Open Claude was totally for the hacker types, okay? Who the hell knows how to spin up a VM and install, give API keys and do some command line stuff. Nobody knows that. Now we are in the consumer layer and what’s going to happen is very exciting.

**Indeed, indeed. And it will have all sorts of implications for the AI infrastructure trade, which I know lots of you listeners are here for. But we are at the end of today’s episode. So that’s your homework is to go think about this and then write comments on YouTube, send us emails, follow us, daily.semidope.com.**

**We have a daily newsletter and go check out our sponsors. So thank you for listening, guys.**
