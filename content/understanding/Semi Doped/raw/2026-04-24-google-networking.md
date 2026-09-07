---
source: https://daily.semidoped.com/p/googles-networking-innovations
title: 🎧 Google’s Networking Innovations
kind: transcript
---

Hi everyone! Austin and Vik plan to write regular short commentaries on industry news here. We’ll also post the podcast episodes for convenience. Here’s an episode to kick things off.

Google’s Cloud Next 2026 keynote? Fire. 🔥

The TPU is now two chips instead of one, but more interestingly, it’s two scale-up networking topologies too.

Copper? Yep. Optics? Yep.

Things we cover:

TPU 8t vs 8i: Google splits training and inference into two chips

Why the inference chip has 3x the SRAM (and more HBM than the training chip)

Virgo: Google’s new scale-out fabric, built entirely on optical circuit switching (OCS)

3D torus scale-up for dense training (picture a Rubik’s Cube)

Boardfly: new scale-up topology for MoE inference — copper PCB + AECs within racks, OCS between groups, 16 hops down to 7

Axion CPU head nodes, TPU Direct RDMA, and the Collective Acceleration Engine

This podcast is lightly edited for clarity.

Subscribe now

Two TPUs for Two Workloads

Austin: Hello everyone, welcome to another Semi Doped podcast. I’m Austin Lyons of Chipstrat and with me is Vik Sekar from Vik’s Newsletter. Today we’re gonna talk all things Google — TPUs, networking, silicon. Yes, and Vik is going to try sharing his screen. So if you’re listening to this, you might want to watch it on YouTube.

Vik: Yeah, this is our first attempt at sharing video, because there’s so much developments on networking in the Google announcements recently, in their whole TPU architecture and how they deal with training and inference differently — not just from a chip side, which we’ll talk about, but also from the networking side.

It’s easy to talk about chips in the sense of, look, it has so much RAM, it has so many flops. It’s very difficult to talk about networking without showing a picture. So I’ve pasted a bunch of pictures on Google Slides. I’m just going to share that. It’s very rough. This is not going to be seriously edited or professional. Yet. Maybe we’ll get there one day. But anyway, I think it’s useful to show some pictures. So definitely watch it on YouTube if you can.

Austin: Yes, so I’m excited. I think there’s a lot to learn there. I’ll set the stage for listeners. Google had their Google Cloud Next 2026 keynote yesterday, and in it they announced the next version of the TPU. And of course, the most exciting thing that most listeners probably have heard is that there’s not just one TPU, there’s actually two. TPU version eight — there’s 8T, which is the training chip, and 8I, which is the inference chip.

This is interesting in that historically, for quite some time with the TPU, there’s just been one chip. V1 was an inference-only chip. Then V2 was training and serving. V3, V4 was training and serving. V5, they split out this efficiency chip versus a performance chip. V6 was back to one chip. V7 was one chip, kind of marketed very heavily as an inference chip. But here we are, now we’ve got a specific training chip or training system, as we’ll get into, and a specific inference chip.

HBM, SRAM, and Axion CPUs

Vik: Maybe I should point out the elephant in the room right away. The TPU 8I has like 384 MB of SRAM, which is three times as much as the 8T, which is for training. It makes sense. Why not put SRAM? You know, Groq LPUs that Nvidia is now integrating into their platform is basically SRAM. And why not do that right now in the TPU 8I? Because you put in as much SRAM as you can so that you can get your low-latency inferencing from SRAM right there. You get high throughput, faster tokens. So that’s one obvious thing to do, which is put in more SRAM. So it’s a good decision. But it’s explicit right now after seeing how we’re going for fast decoding.

Austin: Yes, yes. And this aligns with when I talked to Reiner Pope from MatX — he talked about how they do weights in SRAM and KV cache in HBM, and these are architectural decisions to try to get both really fast decode but also all the context you need. So we see Google going this direction with three times as much SRAM, but then also 288 gigs of HBM on the inference chip.

And I will point out one thing that I thought was interesting, which is the training chip has less HBM. It’s 216 gigs. And by the way, listeners and people watching, Google has amazing technical blogs for these chips and they talked a lot about it. They kind of talk about why they made these trade-offs. But I think it was interesting because right away in my head I’m saying, for training, if you’re going to have less HBM, you could sort of frame that as “why overpay for HBM you don’t need?” So for example, if someone’s just selling one chip, like a GPU that’s one size fits all — use it for training, use it for inference — you could say, well, hey, look what Google’s doing. Maybe am I overpaying for expensive HBM on a training chip? Maybe I don’t actually need it.

Vik: Yeah, I was wondering about why the training chip has lower HBM. And I think the inference part of it is obviously now so memory hungry that you want to put in as many fast memory tiers and as much of it as you possibly can, because the decoding and inference gets so much faster with much better memory throughput. The inference chip is peaked. It’s maxed out with the best memory you can ever put down in the current scenario. This is what you can do.

Why is HBM lower in training? I guess you could always put more chips together if you don’t have enough memory. You could just add more GPUs, and your cluster total GPU memory in the cluster gets bigger. So I guess that’s the solution to it. But in inference, it only makes sense to max out every tier. Remember Nvidia’s memory tier, where you have SRAM right up — they don’t actually mention SRAM, it should have been there, but it should have been tier zero, and HBM was tier one, and DRAM was tier two. An effort at maximizing the fastest memory. Makes sense.

Austin: Okay, what else was interesting? Both chips do use the ARM Axion, so Google’s ARM-based custom CPU, as the head node CPU. And I think there was a quote here, I’ll read it.

It said in the announcement blog: “TPU introduces two distinct systems, TPU 8T and 8I. These new systems are key components of Google Cloud’s AI hypercomputer.” So yet another interesting marketing name. Of course, again, it hints that it’s a whole data center these days. You’re not just thinking the chip level. “An integrated supercomputing architecture that combines hardware, software, and networking to power the full AI lifecycle. While both systems share the core DNA of Google’s AI stack and support the full AI lifecycle, each is built to address distinct bottlenecks and optimize efficiency for critical stages of development. Additionally, by integrating ARM-based Axion CPU headers across our 8th Gen TPU system, we’ve removed the host bottleneck caused by data preparation latency. Axion provides the compute headroom to handle complex data pre-processing and orchestration so that TPUs stay fed and don’t stall.”

So they’re really framing these as the CPUs to feed the TPUs.

Vik: Yeah, that’s what is important. Never let the GPU stay idle.

Austin: Yes, yes.

Vik: That also points out that ARM is a very viable alternative to any x86 CPUs, not to be ruled out at all in terms of architecture. So yeah, I think they’re all equal fair game now. And like we mentioned in an earlier episode, the best CPU is the one you can lay your hands on. So just whoever can deliver most of them, they’ll make it work — ARM or x86.

Austin: Totally.

Why Networking Is Now the Bottleneck

Austin: Okay, now let’s talk networking. Where should we start? I noticed that they’ve got this nice little table and they’re showing 8T uses a 3D torus network topology, but 8I uses the Boardfly topology. So this is interesting because not only are we now starting to make different SKUs for different workloads, but we’re starting to have different network topologies for different workloads. So that’s super interesting. Take us there.

Vik: Yeah, so in terms of the chips that we just spoke about themselves, they’re cool. I mean, they’re good chips. They have HBM, they have SRAM. This is all standard stuff in some sense. Now, I think the real innovation here — and it is a tectonic shift in how networking is implemented in the future of Google data centers. There is a big change, and this is a change that happens once in a decade kind of a change.

And so I’ll explain what that is, but for that I need to explain what was there before. So the fundamental assumption and the basic need for scaling AI today is to realize that the constraint is no longer compute, but it is instead the networking that underlies all of compute today. That is the bottleneck that needs to be solved, and that is what Google’s innovations now address. Google has now reimagined the data center in a sense, and as we talk about it, we’ll kind of break down why that is. Because they have different chips, as we just mentioned, for training and inference, they have different networking architectures for training and inference as well. And we’ll talk about why that is.

And what is most interesting is that a lot of this networking is going towards optics. You will hear me talk about OCS a lot, which stands for optical circuit switching. And I want to explain what that is right up front, so that when I keep saying this word while talking about networking — and I will say it a lot — people understand what this actually is.

So optical circuit switching is a way to redirect light from one port in a switch to another port in a switch, so that you can connect one GPU here to another GPU here, or TPUs in this case. And you do it entirely in the optical domain. The idea is very simple. It’s just like holding up a mirror and reflecting the sunlight coming in from your window. You know how you can point it to different spots on your wall or something? That’s exactly the theory, the concept behind OCS. Why convert optics to electronics and do silicon packet switching like all the Tomahawk switches do? Just stay in light. You’re already in the optical domain, stay in light. So that’s what OCS is.

You can simply connect one port to another by changing how you shine light into different ports. So that’s what OCS is. And that’s becoming the substrate on which Google’s networking is built today. And I’ll explain what parts of the network do what.

So the first thing we should talk about was what Google called their Virgo networking solution. Their previous network was actually called Jupiter. This is from 2015, and was at that time the industry’s first petabit-scale network. Nobody had ever seen anything before that at that scale. It was pretty fantastic because it was built primarily for the internet era, because that’s what was driving everything. And data centers relied on a Clos network, which is basically — have these racks and you can have different levels of networking switches. This is where I have to kind of experiment with a picture, because I actually have a picture of what a Clos network looks like. And yeah, so I hope this works.

Austin: While he’s pulling that up, for people listening, Clos is spelled C-L-O-S. You might not know that when you’re listening if you’re trying to Google it yourself.

Vik: Yes, it is. Yes, so Clos, Clos network, it looks something like this. So basically there are these racks, and then you have the first layer called a leaf switch that the racks hook up to. At the next layer is what is called a spine switch. Then you have another layer on top called a super spine switch. And so what ends up happening is that if you have to go from one rack to another rack, or one GPU to another GPU between different parts or whatever — you can see this picture. If you’re looking at it on YouTube, you’ll see there are two parts. And basically you have to go through a lot of network hops. Think about it. You have to go from the GPU in the rack to the leaf switch. From the leaf switch, you go one higher level to the spine switch. The spine switch, you go to the super spine switch. And then you’ll get switched into the right super spine switch, and then you come back all the way down the hierarchy.

This is too many hops. And when you have to go from one GPU at one end of the data center to the other end of the data center, it is too much. So that’s the whole thing here, and that’s why it doesn’t work for the AI era.

Austin: Right, right. This was definitely designed and made a lot of sense in the cloud server web app era. You’re hitting a database over here, you’re hitting an API over there. But it’s not that you need every leaf talking to all the other leaves and having to hop way up and way back down to do that.

Vik: Yeah, it happens sometimes and the latency is kind of undeterministic. It happens. Latency is what it is. And the problem is training networks don’t like that. AI does not like random latencies and all that.

And another reason — I think this is very important — that this Clos network has so many hops and you need so many layers of networking switches, is because each switch does not have enough ports. In networking terminology, that is called the switch radix. So when you say a switch doesn’t have enough ports, it’s just another way of saying it’s a low-radix switch. So when you have a low-radix switch, you need to multiply the number of ports by adding layers on top. That’s why you need so many layers. Now that problem has changed. We have really high-radix switches, and we’ll come into why that is. All of this communication was managed in a data center in the Jupiter network — Google’s Jupiter network — by their software layer called Orion.

As this internet era grew, really in the 2020, around 2022, Google introduced optical circuit switching into the data center, because it actually has a large switch radix. If you see Lumentum’s OCS switch, and even Coherent, you’ll see they have like 300 by 300 ports. It’s a high-radix switch. And so these were also switched to optics. It’s not doing silicon switching anymore. So when they started doing optical switching, and they also started doing wavelength division multiplexing, which means they sent multiple wavelengths — all that increased the bandwidth. Around 2022, it was like six petabit per second speeds. So six petabits. A peta is like 1000 tera. So we are talking about like 6000 terabits per second. That was 2022. And then they went to faster networking speeds, like going to 400 gig networking, made it a staggering 13.1 petabits per second. That’s 13,100 terabits per second. That’s a lot.

Remember this number, 13.1 petabits, because later when I tell you about Virgo, I’m going to tell you what the number is, and you’ll see how amazing that is. From 2015 to 2023, it’s grown 13 times. That’s pretty cool. They’ve been growing it pretty quickly.

So this was great. It worked great for internet, YouTube videos, web search. It’s great. But when AI showed up, when you’re training a trillion-parameter model with highly synchronous traffic — see, the internet does not work that way. Internet is like, I don’t know, Austin is checking it in his time zone, I’m losing the internet in my time zone. Maybe there are spikes because everybody’s watching a sporting event at some particular time, but those tend to be regional.

Vik: It’s okay. It’s kind of an asynchronous thing really. Internet is asynchronous for the most part. AI does not like that. When all of it hits AI at the same time, the latencies go crazy, and it’s always limited by the slowest deer in the pack. The highest latency is what is going to cause problems, and that is what is called tail latency. The highest latency is the limiting factor. So that is the Jupiter network. That is the status of the world — until Google changes everything.

Austin: Yeah, so okay, so they had a network and it was made more for the previous era — cloud, unpredictable network. And by the way, it’s not all just one big job, like AI training where you’re running one job across the network. It’s coordination. It’s all the machines are contributing to one big job. But obviously the Jupiter network was not designed for that era. It was highly distributed, tons of jobs running at the same time, even if there was some pattern to the traffic — it’s just highly distributed. And then to your point, with training, not only is it all coordinated, but it’s coordinated in such a way that there’s this tail latency concept where everyone has to do work and update everyone else. And if there’s a straggler, the whole bus has to wait for that one straggler.

Vik: Yes, that’s exactly the word they use in their blog post too. Stragglers. Yeah.

Virgo: Rebuilding Scale-Out on Optics

Vik: All right. So let’s now talk about their new network called Virgo. They call it Virgo mega scale network, so fancy. It is actually a mega scale network, and you’ll see why.

So Virgo is basically designed for AI. They saw the network like, this internet era stuff doesn’t work anymore. We need to redesign this to actually make it work. And the biggest change here is that they re-imagined each part of the network for what it is. And this is why I need a picture again from their blog, which I am going to put up if you’re watching it on YouTube. It really helps, but I will try to explain it without having the visuals as well.

So essentially what happens is that you have three layers of their networking stack. The first one is the scale up. We’ll talk about scale up a little separately. But you’ve got the scale-up network within a pod, and however the pod is hooked up. The Virgo fabric itself, where the interconnect happens, is in the scale out, also called the backend network. So this is where it’s an east-west connection, where you hook up all the racks in the data center, these TPUs, to act as one big AI hypercomputer. And so that’s the whole scale-out network.

Austin: Yes, a tiny bit of nuance there for people listening. Scale up — you’re trying to make all the TPUs act as one, and they’re sharing their memory. So it’s like memory coherence. It’s like they’re all talking at as fast a latency that it seems like all their HBM is shared. And then with scale out, from a training perspective, we’re still trying to make one massive training computer, but everything on the scale-out network is not sharing memory. They’re talking as a big coordinated system, but not as tightly coupled.

And I know that when it comes to GPUs, everyone thinks scale up is within the rack and scale out is many racks. And that’s mostly the case, although you can have scale up in between side-by-side racks. But TPUs are a bit of a different beast, because even on their scale-up domain, they’ll have lots and lots of TPUs, more than just a rack. Did I get that right?

Vik: Yes, TPUs go to thousands actually. But in terms of memory coherency, there are some improvements that I will mention next. And that is, it’s a combination of how the latency between memory can actually be reduced as well. And that’s an innovation here.

Yeah, actually that brings me to pretty much explaining the last part of this networking thing we hear, which is that front-end network. The front-end network is simply, I don’t know, compute and storage or connecting to the internet. This is not fancy networking. So you can use the Jupiter network for this. You can use the leaf-spine topology, the Clos networking thing that we spoke about. That’s fine. Don’t need to reinvent every part of the network stack. Just reinvent what is required.

So that’s how this basically looks. So the Virgo network — this is what we should talk about now. They collapse it entirely to a two-layer network, because they have these high-radix switches, which are all OCS by the way. And they have, I think 300 by 300 ports if they are using Lumentum’s OCS. The future of OCS is going to scale to 1,000 by 1,000 ports. So you can imagine, you can even flatten the network further. But regardless — I don’t know if Coherent is an OCS provider to Google as well. Things I don’t really know. But anyway, all this technology exists from these companies and they are viable users in these data centers. So OCS used to be optional before, but now it has become an integral part of Google’s data center networking approach.

And the way you can connect with OCS, because it has so many ports and you can connect it in simply two layers, means you don’t have all those hops. You can get from one TPU to another TPU going across two network layers. That makes it really, really fast. And not only that, because you have these high-radix switches, you can connect 134,000 TPUs to all act as one in the data center. That’s insane. So they call it “campus as a computer.” It’s crazy.

Austin: That’s crazy.

Vik: The whole campus is a computer. You’ll be staring at a whole computer. And you want to know what the aggregate bandwidth of this whole network now is?

Austin: What was it before? Like 13 petabits or something? You told us to remember and I don’t remember. Okay, okay, okay. And now?

Vik: Yes, 13.1 petabits per second. Now it’s 47 petabits per second. That’s like 4x faster.

Austin: Wow, wow, yeah.

Vik: So that’s one reason — it’s optics entirely, no silicon-based switching really in the backend network. And they’ve re-architected a bunch of things that makes this happen. So it’s really amazing. And now, you know, what happens when you put 134,000 chips together in a campus as a computer is that stuff breaks all the time. And so they have an enormous amount of telemetry built in so that they can continuously monitor these things and keep their goodput high.

Goodput is like all the stuff when it’s actually working. It’s not just throughput. Throughput — when you say throughput, it’s just like yeah, the CPU is capable of making flops, but does that actually generate enough tokens or do what it’s supposed to? The goodput terminology nowadays is to be like, okay, the working throughput.

Austin: That’s actually good. Yes. It’s not just the theoretical max. It’s what actually happens in practice.

Vik: Yes. Now I should quickly hit upon the memory thing you mentioned. They have this thing called TPU Direct now. What that is, is basically Remote Direct Memory Access, or RDMA. RDMA as a technology has been around for a while, and in Nvidia land it has also been called GPU Direct. So TPU Direct is like an evolution of that concept, I suppose. But the idea is fairly simple, and honestly this is not a fantastic innovation or anything. It’s been around for a while. So it’s not new, but it’s been implemented in TPUs now.

So what this is is that before, if TPU 1 had to access the memory of TPU 2, TPU 1 has to go through the host CPU of the neighboring TPU. And then it has to — the host CPU will interact with the DRAM and with the network interface card, the networking stack, and all of them will have conversations. Like, what do you want to access the memory? Cool, which address in memory do you want? And the CPU is involved and all this stuff. And then it’ll go and tell the destination TPU — the CPU of that TPU — like, hey, this guy wants to access your memory. Would you allow me to do this? And the destination CPU would be like, yeah, yeah, fine. Let’s do this. Let’s make it happen. And then finally you get to the HBM of the destination TPU. So the memory coherency, like you’re saying, has so many handshakes. It’s so many middlemen ruining the organization. So they’re like…

Austin: Exactly.

Vik: Take it out. Let’s get the middleman out of this thing and remove the host CPU from the picture. And that is what is called Remote Direct Memory Access. So TPU 1 will talk to TPU 2 directly through the network interface. No host CPU involved. And so GPU Direct has also been there. Nvidia does this too.

Austin: Mm-hmm. And this is how GPUs do it too, right? Yep, yep.

Vik: Yeah, this is how. So this significantly speeds things up. Memory coherency speed and latency increases as well.

3D Torus: Rubik’s Cube Scale-Up for Training

Vik: And now we should go to — so that was all about scale out. This is where we are, the TPU Direct thing. So now at some point, we should get into talking about scale up. Because scale-up networks in this TPU V8 thing come in two flavors. It comes with the 3D torus approach, which everybody is well familiar with, which is like the picture on the screen if you’re watching it on YouTube. And then now they have something called the Boardfly. Have you heard of any of these things?

Austin: Mm-hmm. So I remember hearing about the torus topology. Semi-Analysis — I don’t know if this is from Semi-Analysis — okay, perfect, yeah, they had some nice diagrams showing how it works. Is that historically, this is historically how the TPUs have done scale up, is through the torus?

Vik: This picture is from Semi-Analysis, yeah. Yes.

I’m going to very briefly try to explain a complicated 3D picture with words. Follow this carefully if you’re listening and not watching. So think about them. I was going to say Rubik’s Cube. I was so going to say Rubik’s Cube.

Austin: Yes, picture a Rubik’s Cube in your brain. I’m sorry, I interrupted.

Vik: No, no, no, that is perfect. That is perfect. So this is a very large Rubik’s Cube. But you know what? Think of it like the regular 3 by 3 one. It’s okay. 3 by 3 by 3. So the Rubik’s Cube has all its inner faces, right? You don’t see the inner faces of a Rubik’s Cube really. So all of those are connected to each other with cables. Let’s just say each movable cube of a Rubik’s Cube here we’re thinking about is a TPU. And the TPUs are connected through each other in cubes like the Rubik’s Cube. And the inner faces are connected with copper cables all around the Rubik’s Cube. So it’s like every face is connected to every other face with copper.

But now, you also want to connect the outside faces of the same row and the outside faces of the same column to each other. That’s what makes it the torus. And that is done with optics, because clearly you have to go a longer distance to connect the faces of the Rubik’s Cube of the same row or same column, but on the opposite ends together. That has to be connected with optics. So this is how the 3D torus works.

And it has a problem when used for inference, actually. Because in training it’s fine. All of these GPUs are working together and whatever, it’s fine. But the hardest distance that any GPU-to-GPU communication will happen in a Rubik’s Cube — you have to think about this one carefully — is actually from the edge of the Rubik’s Cube. Think about one very edge. But if you think the farthest edge is the other edge of the Rubik’s Cube, you would be wrong, because you can always use the outside optical cable to reach the other end. So that’s not the hardest portion to get to.

In a torus, in a 3D torus, the hardest position to get to is the middle of the torus. The middle of the Rubik’s Cube is the hardest, and requires the most number of hops to get to in a 3D torus.

Austin: Ooh, interesting.

Vik: If you think about how you’re going to get from one very, very edge of the Rubik’s Cube to the middle of the Rubik’s Cube, you’re going to hop halfway along one dimension, halfway along another dimension, and halfway along the third dimension. That will get you to the middle, right?

Austin: Mm-hmm.

Vik: So what happens is, when you have a 4 by 4 by 8 Rubik’s Cube, which is I think what is on the screen — this is a TPU V7 configuration — when you have a 4 by 4 by 8, you’re going to hop two hops in one direction, two hops in the other direction, and four hops in the third direction. So you’re going to have 2 plus 2, plus 4 — 8 hops in this thing. So that’s how you calculate for any 3D torus topology. Which doesn’t have to be 4 by 4 by 8, it could be 8 by 8 by 16, which means you have 4 plus 4 is 8, plus another 16 by 2 is 8. So you have 16 hops.

So if you see the Google blog, that’s the example they use. They use an 8 by 8 by 16 topology, which means you need a maximum of 16 hops to get from one point of the Rubik’s Cube to the farthest point in the Rubik’s Cube, which is the middle.

Austin: Let me interject here really quick and reflect it back, because we’re going really deep and I want to make sure everyone’s tracking. So we were talking about scale out, kind of just connecting pods to each other, and now we’re talking about connecting individual TPUs to each other. And we don’t want to use a Clos network, because if you have these neighbor TPUs in training, you’ve got — with dense models — just neighbors talking to each other. Think of different layers of the network and you just want GPU 1 to talk to GPU 2, or TPU 2 to talk to TPU 3 to TPU 4. They talk to their neighbors a lot. And so we don’t want a world where they have to hop up and hop back down just to talk to their neighbor.

So the traditional way to lay out for training is, how can we densely pack as many TPUs to have as many neighbors that are close by as possible, that we could connect with copper, just really easily? And so Vik has this picture here of this Rubik’s Cube just showing this is actually pretty optimal to think about connecting these in three dimensions. If I’m in the bottom left corner, if that’s my little block or TPU — I’ve got a TPU to my right (call it the X axis), a TPU to my left (call that the Y axis), and then a TPU right above me (call that the Z axis). So I’ve got all these neighbors really close to me.

And then Vik was also pointing out that if I’m in that bottom left corner and I want to connect to anyone else on my X axis row, it’s one neighbor or two neighbors or three neighbors, or you can put optical to connect me from zero all the way to the other end, let’s call it three. So actually it’s pretty easy to talk to my neighbor’s neighbor. But the hardest one to talk to is the one right in the middle, because I have to traverse through neighbors in every dimension — down the X and the Y and the Z — to get to there. So I’ll hand it back to you.

Vik: Yeah, thanks. That’s a good summary. That is important. That is what a 3D torus is.

Now, in the 8 by 8 by 16, I showed you how you need half the hops in each direction. And anybody listening to this might want to pause and think about, okay, what is he saying? How many hops? But yeah, this is how this networking is serious business. The 16 hops is what was mentioned in the Google blog. And so 16 hops is a lot. This is a good architecture for training, because all of these TPUs are talking to each other all the time.

In inference, it is not a good architecture. And why is that? The reason is because not all GPUs or TPUs are activated all the time. When you have a mixture-of-experts model, only some of them are going to be active, depending on which parameters are getting activated. And so all the GPUs don’t function all the time together. And they do traverse a lot more hops. And you want that hop latency to be minimized, because otherwise it adds to the inference time and performance. You don’t want that.

So the question is, how do you architect 3D torus for the world of inferencing with mixture-of-experts models? And this is why we come to the concept of Boardfly.

Austin: Yes. So let me reflect it back really quick for people. For training, we want all this neighbor-to-neighbor communication. And what Vik was saying is, if you’ve got a mixture of experts when you’re doing inference, there’s not necessarily going to be all this neighbor-to-neighbor communication. Because it might just be like, hey, for this token, I want this expert, expert 21 over there, and for this token, I want that expert, expert 4 over there. So it’s not the same communication patterns every time — just neighbor-to-neighbor, layer to layer to layer. But now it’s this routing, which actually kind of reminds me back to what we were talking about earlier — that sort of non-deterministic era that we were living in.

So all this is to say the workload communication pattern is different for training than it is for inference. So that raises the point: why not design the interconnect for the workload, which in this case is mixture of experts? Which by the way, if you go listen to the Reiner Pope talk, he actually talked about how they’re thinking about this as well — designing the interconnect specifically for mixture of experts. But okay, carry on, Vik.

Google Boardfly: Scale-Up Networking for MoE Inference

Vik: Awesome. Yeah, good context, good context, because we need that. We need to always take a break and think about and say to ourselves what networking is. That’s the only way you learn networking. You have to say it out loud, you know? So pause the video and say whatever we’ve spoken out loud so far.

So what ends up happening is we need to go to the Boardfly. And this is — it is not a dramatically new invention, but it’s a modification of an existing idea. So the Boardfly approach is fundamentally to reduce the number of hops. Remember how I told you 8 by 8 by 16 has 16 hops? Now we want to get that down, and the Boardfly topology allows you to do that.

Okay, so how this works is, you have a board. And on a board you have basically four TPUs. You’ll see this picture whenever you search up TPU V8 — you’ll see a board with four TPUs on it. Those are PCB connected, and so there’s copper. There’s no optics here. It’s just a board PCB with copper connections. So that’s copper connection.

Now you take eight of these boards and you put them in a rack, and you hook them all up with active electrical cables. You see how scale up still uses active electrical cable? So it’s not like everything’s optics and copper is dead. No. So AEC is still used to connect the boards — eight boards together. And this is now called a group.

Now how they are connected is what is called the Dragonfly approach. And this has been around since the supercomputing days. Again, this has been around for decades. This is not a fantastically revolutionary idea. It was at the time, not today.

Austin: Yes, let me give you a tiny bit of trivia. I found this when I was Googling. I’ve been waiting to tell you this. I haven’t told you this before. Okay, so I was looking up Dragonfly and there was a paper from 2008 — some computer architecture paper introducing the Dragonfly network. And the authors on the paper: someone named John Kim from Northwestern; William Dally from Stanford, whom you might also know as Bill Dally, who is now at Nvidia and he’s the head of Nvidia’s research — which by the way is probably one of the coolest jobs in the world. Then another author is Steve Scott, some guy from Cray. Which of course Cray’s supercomputing, a lot of history there. And for people who don’t know, that’s in Chippewa Falls, Wisconsin, which is a town of 14,000 people. So just kind of crazy, kind of cray cray. And then the last name on it from this 2008 paper is Dennis Abts — I’m not sure how to pronounce his last name, A-B-T-S. He was at Google at the time. Then he went to Groq, and he was an early Groq engineer from like 2017 to 2022, presumably doing all of their network design and stuff. And then he went to Nvidia, and he’s been at Nvidia ever since.

So when I saw the paper, I was just like, whoa, these are some of the who’s who of networking at Nvidia. And it was just crazy to see that this traced back to them from 2008. But with that, I’ll give it back to you to keep going. I just thought it was cool.

Vik: That was great. That was great. That’s a great piece of trivia. And I want to add to the fact that Dennis Abts, when he was at Groq, and then he went to Nvidia and all that — if you look at how Groq architects their rack-scale solution, it’s also Dragonfly. They don’t hook up boards, they hook up individual LPUs in Dragonfly configuration. That is what Groq does too, by the way.

Austin: I see, I see, gotcha. Yeah, yeah, because it still reduces the amount of hops. Even if they’re not connected on boards, it’s still going from 16 hops down to something less.

Vik: Yes, exactly. So this is called Boardfly because you’re not hooking up GPUs in a Dragonfly configuration. You’re hooking up boards of four TPUs in a Dragonfly configuration. So it’s a portmanteau — Boardfly. So this is still AEC. The next level is that you connect up all of these groups together.

So remember, we had four TPUs to a board, eight boards to a rack — also you can call it a group — and then you have 36 groups connected to each other in a pod. So if you multiply 36 groups times 8 boards times 4 TPUs, you get 1,152 chips. And so 36 groups are all connected together with OCS again. So you see how OCS is the underlying substrate on which all of Google’s networking is built. It tells you how important this technology is now.

Austin: Yes, yes. So all of this scale out in Virgo or whatever it’s called — was all of that OCS?

Vik: Virgo, yes, that is all, because it is a high-radix switch that connects in two layers, that connects all of this stuff up in two layers.

Austin: Okay, so all the scale out was OCS, and then scale up: on the board, it’s PCB traces, nearby boards in a group are AECs, but then group to group is connected via OCS.

Vik: Yes, all optics. Yes, so optics.

Austin: Gotcha.

Vik: Is the primary driver in all of this networking, and all of this is OCS. And now, what is the benefit? Why do all this stuff? I promise class will end soon. All right. But I think this is fascinating. Okay, so let’s — I’ll show you a couple more pictures. If you please do watch this on YouTube.

So the Boardfly tells you why, how exactly the hops can be minimized. Only the picture can show you this. Because what you can do is you can go from board to board within the rack — you’ll have a couple of hops within the rack, and then you will make one big hop via OCS to a different group. And then you will make a couple more hops there, and ultimately you’ll reach your destination in probably six or seven hops.

And so your hops have come down from 16 all the way down to seven because of this approach of architecting a Boardfly networking scheme for scale up. That is a big deal. The latency has dropped by over 50% because of this clever way of hooking stuff up.

See, that’s why the networking of a data center is vital in the performance it provides. It’s critical, right? So that’s about all the spiel I have. It’s pretty fancy. It’s very technical, I know, this episode. But essentially, to summarize, there are two major inventions. One in the scale-out network, which is pretty much all OCS. And then there is re-architecting of the scale-up network to go from 3D torus, which TPUs are typically known for, to make it inference-specific and use Boardfly topology. So that’s my long spiel.

Workload-Specific Everything

Austin: Very good, thank you Professor Vik. And yes, just as a reminder — why we wanted to spend the whole time talking about what Google introduced is, because again, we’re seeing these big shifts from one chip that does everything to two chips, training and inference. But it’s not just two chips. It’s two scale-up networks — 3D torus for training, for dense neighbor-to-neighbor communication, and then the Boardfly for inference scale up for mixture of experts.

Which is again sort of proving the point that a lot of people have been saying — it’s no longer one size fits all, not for silicon, not for networking, but actually the data centers, the complete data centers, are being architected around the workload. And so whether you’re a startup in this space or you’re tracking optics, this is a big shift that we see from Google.

And then of course there’s lots of interesting questions, like, will we start to see this level of network innovation coming from others like AWS with Trainium? Are they going to stick to the way they’ve architected things for their cloud environment? Or are they going to start designing data centers that are specifically designed for MoE inference or whatever, even if it means they have to think differently than they used to in the web server API era?

Vik: Yeah, yeah. It’s interesting, right? Now you have training and inference distinctly falling into two different camps. They have different chips. They have different networking solutions. I don’t know what’s next. Different power solutions too. Different locations based on the direction of the wind. It’s extreme co-design, man. It matters. The wind matters.

Austin: No, it definitely is extreme co-design. And then of course there’s a million other questions that I’m sure we’ll circle back to, like, is it just these two architectures forever, or are there going to be other workloads that demand something slightly different? So for inference, is this sort of one size fits all for all inference workloads, whether they’re world models or just textual inference?

Vik: Yeah. Maybe we’ll build out agentic inference data centers in the future. Somebody will figure out that agentic workloads need a different infrastructure.

Austin: Okay, I’m glad you mentioned that, because I still want to know more about where CPUs fit in this communication, this network topology. Obviously they talked about the Axion CPUs to feed the TPUs, but what about all that other — all the other agents that are just running on CPUs and virtual machines somewhere? I know that a lot of them are just kind of long-running and latency doesn’t matter, but what about the ones where latency does matter? Do those come into the networking topology somehow? I don’t know, come tell us, teach me.

Vik: There’s so much to learn here. This is just scratching the surface. We haven’t even talked about other stuff that I saw on there called CAE, which is Collective Acceleration Engine. To be frank, I don’t even know what that is. I haven’t gotten around to reading about it.

Austin: Yeah, we’ll have to follow up on that. I did a little bit of reading, and it sounded like it actually is related to networking, in that it sounded like offloading some communication stuff to a specific accelerator. So yeah, I think I have written down here the CAE, Collective Acceleration Engine. Each TPU 8I has two tensor cores and one CAE on a chiplet die. And the CAE offloads all-reduce, all-gather, all-to-all type collectives. It’s a workload-specific accelerator. It’s kind of like Nvidia’s SHARP. So it’s kind of similar to what DPUs do as well, which is how can you let GPUs just do as much matrix multiplication as possible, let CPUs not get in the way, save those for doing some AI agent stuff maybe or feeding the TPUs. But then as much of that networking stuff — you can just put it on network-specific optimized silicon. So it’s turtles all the way down, optimizing everything.

Vik: Yeah, it’s true. All right. That is too much information for anybody to process. We’re going to have to split this up into 16 clips, I think. I don’t know. It’s like a whole course on OCS and Google networking.

Austin: Yes. Totally, yes. We hope that you liked Professor Vik’s lecture in near real time after Google’s announcement yesterday. Thanks for listening. That’s it. If you’re enjoying Semi Doped, the first thing you should do is just tell your friends. We are so happy when we see people sharing our videos. Thank you so much for that word of mouth recommendation. Subscribe to our newsletters if you haven’t yet. I’m sure Vik and I will write about this more in depth. And yes, thanks, and we’ll see you next week.

Thanks for reading! Subscribe for free to receive new posts and support my work.
