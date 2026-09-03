---
source: https://daily.semidoped.com/p/semi-doped-qualcomms-hbc-memory-alphawave
title: 🎙️ Semi Doped: Qualcomm's HBC Memory, Alphawave, Modular, and more
kind: transcript
---

🎙️ Semi Doped: Qualcomm's HBC Memory, Alphawave, Modular, and more

Austin Lyons and Vik Sekar break down Qualcomm’s recent Investor Day, where the company unveiled an ambitious strategy to diversify beyond its traditional communications business. They dive into the technical details of Qualcomm’s High Bandwidth Compute (HBC) architecture, its new C1000 data center CPU, and the strategic acquisitions of Alpha Wave Semi and Modular. The hosts explore the challenges and opportunities as Qualcomm aims for two-thirds of its revenue to come from automotive, IoT, and data centers by fiscal year 2029.

Things we cover:

High Bandwidth Compute: stacking LPDDR on logic instead of HBM on the side

High Bandwidth Compute: stacking LPDDR on logic instead of HBM on the side

Why disaggregated inference opens the door for latecomers

Why disaggregated inference opens the door for latecomers

The AI 200 / 250 / 300 accelerator roadmap

The AI 200 / 250 / 300 accelerator roadmap

Alphawave as Qualcomm’s Mellanox, plus the Modular software stack

Alphawave as Qualcomm’s Mellanox, plus the Modular software stack

The C1000 data center CPU, with Meta as a customer

The C1000 data center CPU, with Meta as a customer

Edge AI, AI-defined vehicles, and the robotics endgame

Edge AI, AI-defined vehicles, and the robotics endgame

This podcast is lightly edited for clarity.

Cold Open and Catching Up

Austin: Qualcomm’s main point is that they’re diversifying their businesses, and the majority of their business in the long run will be non-communications. I thought this was interesting because the name of the company and the legacy of the company is communications. Quality communications. Qualcomm. But the crazy thing is the data center business could inflect so much that what Qualcomm makes from their new businesses, data center and automotive, could ultimately dwarf what they’ve made in the aggregate of the company’s history as a communications player.

So that’s something big to wrap your head around: Qualcomm being a communications player could just be the start of their story.

Austin: All right, hello, welcome listeners. Welcome to another Semi Doped podcast. I’m Austin Lyons with Chipstrat, and with me is Vik from Vik’s Newsletter. Hey Vik, what’s up, man? It’s been a while since we chatted.

Vik: Yeah, it’s been a while. I’ve been traveling, you’ve been traveling. Finally we’re back at the home studio, so it’s time to do something now.

Austin: Totally. So you were in the UK and it was hot?

Vik: It was crazy. I thought I ran away from India to get away from the heat and feel some cool air in the UK, because everybody says, oh, it rains all the time. So I was hoping to get rained upon a little bit. But anybody listening from the UK will be like, no, no, you never wish for that stuff. We like a little bit of sun once in a while. I know it’s a lot of sun right now in Europe, but it’s okay, maybe for a week or two.

Austin: Yeah, totally. I saw it was like 110 degrees Fahrenheit or something in France. When you said it was hot, I was like, oh yeah, it’s UK hot. But no, dude, it was hot, hot.

Vik: It was hot, hot. And the other thing is, in the UK they’re just not equipped to deal with this stuff. In India there’s AC in some places. If not, if you go by buses, for example, there are windows, sometimes there are no windows. So you always feel the breeze. It’s not cool breeze, but at least there’s movement of air. In the buses in the UK, it’s just sealed. There’s no air movement, the windows don’t open out or slide out or anything like that. And you’re just trapped, with a bus full of people just sweating. It’s a sweat lodge.

Austin: Just suffocating. Brutal. Well, I was in New York City. Qualcomm flew me out for their investor day event. And the weather was really nice in New York City. It was very beautiful. I woke up early, the sun’s out for a long time right now, and I ran in Central Park. I ran one day to the west side along the Hudson River. I saw crazy huge yachts. I have never seen such big boats in my life.

I don’t know if it’s someone who lives there’s yacht, or if it had to do with the World Cup, because there were a bunch of people in town for the World Cup. But I was like, dude, you need a whole staff to run this thing. This is crazy. And here it is, and I’m just right by it. I was going to take a selfie in front of it, but I thought, I don’t know, that seems kind of touristy.

Vik: I mean, all the investment bankers live there, right? Half the people who listen to our show must be on their yachts. Maybe they should let us know. Hey Austin, you saw our yacht.

Austin: That’s true. Hey, live Semi Doped podcast from your yacht. Send me an email and we can chat.

Vik: Okay, okay. So wait, wait, wait. You were in New York for the Qualcomm investor day then.

Austin: Yes, Qualcomm investor day. I was there. They hosted it in New York City because the audience is the sell-side analysts and the financial community, but they brought out industry analysts as well, because they had a lot to talk about.

Qualcomm’s Diversification Bet

Austin: Really, the story we’ll walk through, and I want to talk through the technical bits and hear your take on some of it, the story that Cristiano Amon and Qualcomm were trying to communicate was all about their diversification away from handsets. Qualcomm has always been a communications company, a big smartphone business.

Everyone is seeing the writing on the wall with smartphones: we’re at the top of the S-curve. Everyone has a smartphone. There’s lots of competition in the space. Qualcomm has been moving into automotive, and that business has been growing, and it’s a proof point that they can use M&A to get into a new business, build the technology, use their channel and their manufacturing scale to grow that business and take it to market.

And the whole point of this was Qualcomm trying to say, we are going to do that with data center as well, and here’s our plan. There was, and we’ll include the image, but they had this one money slide, I think from the CFO’s presentation, where there were three circles. It was a donut ring slide, and they were showing: okay, in fiscal year 25, handsets were two-thirds of our business, automotive and IoT is one-third. Our goal for 2027 is roughly half and half, half handsets, half other, which now starts to include data center.

And then fiscal year 29, the goal is actually two-thirds of the business is automotive, IoT, and data center, and only one-third is handsets. So they’re trying to move beyond their legacy communications-only business into these other new businesses. Last point and then I’ll let you chime in: obviously communications is part of all of these businesses. The IP and the technology is still important to the other businesses. It’s just that they’re going to have to build more and do more than just handsets.

Vik: I saw the whole investor day talk. I wasn’t there, but I saw it on YouTube. It was interesting because Cristiano Amon said that for the 40th anniversary of Qualcomm they had the founder over, Irwin Jacobs. And during that talk he mentioned that he made one mistake in naming the company Quality Communications. He said, I should have just stopped with one M in the com, because now it could be quality compute.

But now it’s a problem, so they couldn’t. In my opinion, they should rebrand it and drop one M.

Austin: Totally. Oh yeah, if only he had the foresight to think 40 years ahead, right? That’s so funny. So true.

Vik: Yeah. So that’s the big deal. What you say is actually a big deal, because this company from the get-go has always been about communications. They have a rich history. It started with satellite communications. When I joined there in 2018, they had a tour of the museum within the campus that showed the entire history of all their devices made from the beginning. It’s really nice, it’s part of the orientation, they take you to the museum. It’s a very inspiring way to start working there.

But that’s the legacy. They’ve been through 3G and 4G and 5G. They’re also on the 6G train, we’ll talk a little bit about that. But now they’re saying that only one-third of the business is going to be handset-based, which is a way of saying that’s the communications business. Two-thirds will be IoT and data centers. It’s a big shift.

Austin: Indeed. It is a big shift. So let’s start with maybe the confidence question: do you think Qualcomm can get into new businesses? Maybe we’ll start there, strategically, high level. Do you think they can build a real data center business? I’m going to let you have your take, and then maybe I’ll provide some color on what they said as well.

Vik: They can, because there’s no reason a company like Qualcomm cannot get into the data center business. They have compute. They have the CPU business, they have NPUs, which they use for graphics acceleration on their SoCs and mobile handsets anyway. They have all kinds of IP now through the Alphawave acquisition. I was looking at what all they got through that, and it’s quite a lot, because they have SerDes IP in copper and optical.

They have PCIe Gen 6, CXL for servers and storage. They have Ethernet IP, 800 gig, 1.6T, for switches, routers, DPUs, NICs. And they have HBM and DRAM IP for GPUs, which is very important. We’ll talk about that, because that’s one of their key technological innovations in the era of AI and the way they’re doing inferencing chips. And they also have chiplet IP through the Alphawave acquisition, through UCIe and a bunch of other standards.

So they’re very well positioned as a company that has also shipped billions of devices into the handset world. It’s not like they’re new to doing this. I could argue that if OpenAI says, I’m now a chip company, or Anthropic wants to be a chip company, they’ve never been a chip company. It takes experience to be one, which Qualcomm has. So yeah, they’re well positioned to do so, although one could argue that they’re a bit late to the scene.

Austin: Yes. Okay, so let’s get into that. In the grand arc of things, late and timing is interesting, because obviously this has been going on since late 2022. It’s only 2026, and this is the type of technology that will be here for the next 30, 40 years, whatever, forever. So being late now feels like a big deal in the grand arc of time, but it won’t be. It’ll just be a little blip.

But the question is, what does it take to succeed? Which I think you hit on nicely: you need IP, you need talent, you need manufacturing prowess, and you need technological differentiation. It can’t just be a me-too fast follower, like, oh great, a company did this, I’ll build the same thing and sell it to a different market. That’s not going to work. There has to be a reason for a customer to choose you. And to the point of being late, you especially have to differentiate on some vector.

I think of Nvidia’s Hopper-era GPUs, and then eventually AMD came in with Instinct, and what was nice was they made a different decision about the amount of HBM capacity on a single chip. That small decision on one vector opened up some particular workloads that could run on eight Instinct 300s, I think, or maybe it was 350, I can’t remember off the top of my head, but it took 16 Nvidia GPUs, because they just didn’t have enough memory capacity on each GPU. That illustrated for me that even if you come in late, if you make some sort of different technological bet, it might unlock a certain set of customers, which can help you get your foot in the door and grow from there.

So to your point, Qualcomm checks a lot of the boxes: they’re a big company, they have experience, they have IP. And by the way, they were able to use M&A to get IP they didn’t have, get talent they didn’t have, and fill those gaps, which is something we’ve seen them do before in their automotive business. But there still needs to be something different, so that at the end of the day a customer like a hyperscaler or an AI lab will know why they want to choose Qualcomm. And it’s not just because it’s cheaper, or because everyone’s out of supply and Qualcomm happens to have some. None of those are sustainable, those are temporary. There has to be technological differentiation that really impacts TCO for a particular workload. This is even why we saw the Groqs and the Cerebras have success: they made design decisions with lots of negative consequences, but for a particular workload, high interactivity, it was much better than GPUs could do. So obviously Qualcomm had to come out swinging and say, we think we can do something different here.

Disaggregated Inference

Vik: Yeah. Their key differentiator here, apart from their memory architecture, which we’ll discuss, is basically the fact that inference now is getting disaggregated. This was their key theme that went through the whole talk, they kept saying this is now disaggregated, which means you can actually develop hardware to do a particular task. So you could put in a Qualcomm rack along with some other racks. It doesn’t mean you have to fill Nvidia racks with all these Blackwell GPUs along with their Vera CPUs. You don’t have to do that. Now you can put a rack full of CPUs separately. You can put a rack full of low-latency decode, like you were saying, the Cerebras or the Groq LPUs. And now you can put maybe a rack of Qualcomm inference chips just to do that one portion of it. If they have high memory bandwidth, you could just do decode on that, and still continue to use Nvidia GPUs for the prefill part. So the disaggregation across the whole inference space is becoming more and more a theme, because one size does not fit all. You’ve spoken about this in your Substack as well, there’s a right-sized hardware for the right-sized workload. So that’s increasingly becoming a theme, which is why you can run different kinds of hardware along a common software platform, which Qualcomm also wants to have, open and developer-friendly for everybody to work with.

Austin: Yes, you’re totally right: disaggregation has really opened the door to everyone. Once we started to break the workload down for inference, today LLM inference is obviously the defining workload, and the value is actually all being created by agentic inference workloads, reasoning models, but in breaking up that workload into prefill and decode, then people could say, okay, I’m late to the market, I’m just going to focus on decode. I’m going to do something very decode-specific and very different, and that will help me get my foot in the door. Again, it worked for the AI ASIC startups, and this will have to be the mindset that Qualcomm has.

Because ultimately, yes, would they like to sell data centers full of Qualcomm Dragonfly, which, by the way, that’s what they branded it, for anyone who’s not watching. Dragonfly is their data center brand. Would they ultimately like to sell, and the branding was white and gold, by the way, so it looks very nice, would they like a data center full of white racks, so that whenever on FinTwit you see a picture of someone saying, look, I built a data center and all the racks are white, everyone can go, whoa, Qualcomm to the moon? Yes, they want to do that. But the reality, which I think they’re fully aware of, is they need to sell a few racks into the existing data center that’s full of Nvidia GPUs. So focusing in on decode, for example, would be one way to get there. But okay, take us further. Do you want to talk about the memory, the HBC? That was sort of the big star of the show.

High Bandwidth Compute

Vik: Yeah, let’s go to HBC, because that’s an underlying technology that’s very useful regardless of whether they want to use it in data center hardware or IoT or automotive or robotics, because this is going to be the platform that lays the foundation for all of their businesses going forward, in my opinion. At least that’s the way it seemed from what I heard.

So high bandwidth compute is their way of getting better memory-bandwidth hardware packaged right next to an XPU, so that you can get a really fast inference bandwidth like you’d get with Cerebras or Groq LPUs. Those things can do, a SRAM bandwidth is in the range of 100 terabytes per second, and right now HBM bandwidth is about a tenth of that, about eight terabytes per second. So they want to break through this eight-terabyte barrier, which currently involves an HBM stack sitting next to a GPU or XPU and connected with maybe 2,000 lanes of interconnect between the memory and the GPU chips, packaged with an advanced packaging substrate like TSMC CoWoS.

So their idea with high bandwidth compute is that you take the memory and you put it on top of the XPU die. Instead of connecting the memory through the side, using shoreline density as it’s called, on one edge of the GPU die you can only put so many lanes before you run into advanced packaging limits, if you put the memory on top of the XPU, you expose the entire face of the chip between the XPU compute and the memory to have interconnects. So now, instead of 2,000 lanes going between these chips, you can have, I don’t know, tens of thousands or even 100,000 different lanes. What that does is increase your bandwidth, if you increase your number of lanes by 100x, you’ll get 100x more bandwidth. So this is their main idea, what they call high bandwidth compute.

Austin: Yes. Okay, there’s so much to unpack here. I’m going to walk through it again for people at a high level in case they didn’t catch it the first time, because, I’ll be honest, one, the naming might not do it justice, although I don’t have a better name, because HBC, HBM, it feels very similar, but there’s actually a lot of differences going on. And two, there are some nuances that weren’t obvious to me the very first time it came across, but as I looked back at it again preparing for this episode, some things stood out.

So, one of the problems: everyone knows the way GPUs and HBM work today. You’ve got the HBM, it sits next to the GPU, and you’ve got things like weights or activations, KV cache, sitting in this HBM. During decode especially, that stuff just has to fly back and forth. It’s like if you separated your kitchen and put your fridge in the garage, and you just had to walk to the garage and get something, bring it back, chop it up, walk to the garage, get the next thing, bring it back, chop it up, walk to the garage. Obviously it’s like, dude, what are you doing? Why are you spending all this time walking back and forth to your garage? Just put your ingredients right next to your chopping block. Because of course there’s lots of power loss, lots of latency, that kind of thing.

And to your point, the analogy breaks down, but you can’t get as many lanes and as high bandwidth. So one point is: how do we bring the compute as close to the memory as possible? Other people have called this near-memory compute, processing in memory, stuff like this. There are lots of startups doing this. I think it was d-Matrix doing something like this?

Vik: Yeah, yeah. This is d-Matrix’s approach, what they call in-memory compute.

Austin: In-memory.

Vik: So d-Matrix also puts memory on top of logic. So there’s a question of, really, is the Qualcomm innovation all that different? That’s another question to ask.

Austin: Totally. Okay, so that’s the first problem, how can we bring the compute as close to the memory as possible? And what you said is, well, the closest thing is to stack the memory on top of the compute and literally have it as close as possible. Now, there are obviously thermal concerns there. These GPUs, XPUs are crazy hot. So can you actually put memory on top of the XPU?

As I looked closer, and we’ll try to include some pictures as well, my understanding is they’re not actually stacking the memory on the XPU, but they’re putting a logic chip under it, and putting it close to the XPU, and they’re actually offloading some of the workload to live on that logic chip. I don’t even think it’s necessarily a programmable logic chip. I have a feeling it’s almost more of a true accelerator, in the sense of accelerator. So for example, maybe you have during inference some sort of primitive, some function that’s run all the time, like softmax, or something in attention. Can you actually take that off the XPU, put it in the logic that’s right under the memory, and the idea is: fetch what you need from the memory, do those primitives right there, and then send the result back? That would help you solve the thermal issue, you’re not actually putting the memory on top of this crazy hot XPU, but you’re still using advanced-node logic and putting the memory on top of it, and accelerating an even finer-grained piece of the workload.

This would be the name we’ve always used before AI, which is an accelerator. Like a camera, an image-sensing processor, or any other little acceleration we’ve done in the past, like with graphics, you’re like, dude, we just keep doing this particular loop over and over on a CPU, why not build a little thing to do it? Qualcomm does this all the time in their Snapdragon SoCs, build a little thing to do some image processing that’s dedicated for that. My understanding is it felt conceptually like they’re saying, take a tiny piece of the inference primitives, move it off, but also it’s very important that it’s very close to memory, because it’s very memory-bandwidth intensive. So I’ll pause there. What’s your reaction?

Vik: When I saw this announced on the talk, it was very confusing the way it was drawn out. In the first example, where they show how the current solution works, they had a GPU and an HBM, and there was this gold-colored back-and-forth happening. It was very beautiful to look at, you could see the gold data going up and down the HBM stack and going around into the GPU. So that’s how it works today. But then when they put in their solution, their high bandwidth compute, they still showed a stack of LPDDR. And then they said something about an XPU. And sitting next to it was an SoC. And then they were showing the same gold thing, presumably data, going between the SoC and the LPDDR stack.

So for somebody looking at this, it looks very similar to the HBM one. I’m like, what’s different? And then they go on to mention that, no, you don’t need advanced packaging anymore, you could do standard packaging, because you don’t need that bandwidth anymore. So my interpretation is that the logic die under this memory is not any simplistic logic die of any kind. It is a full-up XPU. Because that’s the only way you will not need advanced packaging to make this work, you have to do the full thing there. And that’s what d-Matrix is doing: they do all their compute right under memory.

Austin: Okay, so when you say XPU, what’s your definition of XPU in this particular use case?

Vik: This is the thing that does matrix multiplications. That’s what I call an XPU.

Austin: Yeah. So do you think they’ll do any matrix multiplication anywhere in the workload right there under the LPDDR?

Vik: Yes, I think so. To me it looks very similar to what d-Matrix is doing, because d-Matrix, digital in-memory compute, and their Raptor, which is the next generation of 3D DRAM, those slides are out there, they previously announced this stuff. So it’s nothing unannounced. They actually have a full-up XPU chip that does all the compute under the DRAM die. That’s their Raptor chip. So this has to be something like that. This SoC sitting next to it is doing something else. It could be a mobile SoC, if you’re using AI on a phone. It could be an automotive SoC, if you’re using AI in a car. But it’s not doing matrix multiplications, it’s doing SoC stuff.

Austin: Sure. I agree with you. Conceptually I like the idea of essentially a tensor core coming over and doing all the matrix multiplication. I totally agree that’s what makes sense, get all of this multi-dimensional data, put it right down into some sort of tensor-core-type thing, and have it do all the matmuls. It would be nice to understand what else is in this SoC. Obviously there’s die-to-die communication, there’s orchestration of the whole workload, there’s communication with CPUs, all these other blocks that don’t need to live right there. But I do agree that conceptually, anything in the workload related to the specific matrix multiplication would live under the memory.

Vik: Yes.

Austin: And you mentioned earlier that this technology could come to the edge, to phones, to auto, wherever. I think that’s also a key point: if people are thinking GPU with LPDDR stacked on top, that might be confusing, because it’s like, oh, are we putting big GPUs into a car now? But the point is the concept of the technology: if your car’s going to run neural nets, wouldn’t it be nice to have the matrix multiplication under a big stack of, not HBM, but LPDDR, something lower power, cheaper, higher capacity, that would still let you do generative AI at the edge, presumably with even bigger models?

The Hard Part: Thermals, Stacking, and TSV Density

Vik: Yeah. I want to talk about this memory-stacking part first, because we’ll definitely talk about the automotive, IoT, and robotics aspects, which they really want to get into in the future, and I think they’re well positioned to do it. But there are several issues with the way this memory works to begin with.

First of all, you already mentioned the thermal aspect. It is pretty challenging to stack logic on top of GPUs or XPUs like this. The second thing is that there’s a fundamental size mismatch. These XPUs that sit under any form of memory, even when d-Matrix does their Raptor, they’re pretty big dies, because they’re reticle-sized GPUs that sit there. Nvidia even packages multiple GPUs in a single Rubin or whatever nowadays. So it’s easy and okay to assume the XPU will be a reticle-sized compute unit, which means it’s like 850 square millimeters, anyway, above 800 mm². Now, if you have to stack DRAM on top of that, can you imagine how big a DRAM die you need? And can you imagine the planarity requirements of actually hooking this up and keeping it planar in a thermal environment? Stuff is heating up, and the planarity between the top die and the bottom die needs to be maintained without having the bumps rip off each other. This is a challenging problem.

Austin: Yes. You’re saying that things move and warp when it’s hot, but obviously you need physical connections, wires, pipes, so to speak, going up and down. So you can’t have all this moving around. It needs to be rigid, stable, heat up together, cool off together, or dissipate all the heat so it doesn’t move around.

Vik: Yes. So it’s a challenging problem. And as much as they say, oh, we don’t need advanced CoWoS packaging anymore, yay, we solved packaging, it’s enough to use a standard-pitch package for this, they have not really solved the packaging problem. They moved it to a different place.

Austin: From next to the XPU to on top of it, which is even harder. And one more thing I want to point out: the picture deceivingly shows multiple LPDDR stacks. It’s not that easy, because even the Raptor first generation is probably going to have one die layer. The expansion is going to happen later, people want to stack more DDR die on top of each other, but it’s not simple by any means, because as it is, it’s hard enough to stack one memory chip on top of logic like this. This is logic-on-logic stacking, in a sense, if you think of it that way. It’s like stacking SRAM on top of compute, like AMD did with its V-Cache. Similar stuff.

Vik: Right. Well, talk to me about this then. Obviously Qualcomm’s going to need to work with the memory vendor, but then there’s a logic accelerator under it. So they obviously have to work with the logic foundry as well, TSMC.

Austin: TSMC, yeah.

Vik: TSMC, exactly. Then, as far as the thermals and the stacking and making the logic and the memory behave nicely, ultimately, who does that fall on? HBM4 has, or maybe it’s HBM4E, memory stacked on top of a custom logic die now. So I’m wondering if some of these thermal problems are already being solved for HBM4, the HBM stacked onto a custom base logic die, and if there are any learnings that can be applied here. So it’s like, oh, the industry has already solved this, or is it, no, no, we’re talking about different memories and a different level of compute under the memory?

Austin: I don’t think the logic die and the HBM die sizes are as big as a GPU die. They’re smaller.

Vik: True. Yes.

Austin: So that’s what I was pointing out earlier, it’s not as easy as that. If you want to stack something the size of a GPU die, that’s difficult. The logic dies under HBM4 are smaller, and they don’t nearly do as much work as something doing matrix multiplications to infinity, which is what XPUs really do. They do a lot of matrix multiplications. So it’s a computationally much heavier workload when you try to do it under.

Vik: So presumably running hotter, more often.

Austin: Yeah. There’s another catch to this. When you do DDR7 on top, let’s say LPDDR on top of LPDDR, the whole idea was that DDR has more capacity than HBM per layer, and therefore you’re getting more capacity. But now, when you stack DDR on top of DDR, that’s pretty much HBM. Now what you’re doing is stacking HBM on top of compute, in my opinion. And the reason HBM per layer does not have that density, that memory density, is because there are through-silicon vias. When you have through-silicon vias, you can’t put as many memory cells around them. There’s a keep-out zone: if you put a through-silicon via here, you can’t put memory cells around it for some distance. So per die, your memory capacity drops.

You get high density if you stack only one layer, because you don’t have to put vias through that memory layer. The moment you start stacking two or more, you have to put vias through the layer, which means the capacity per layer starts to drop, let’s say by half. So you need to stack four to make it even useful. You can’t stack two, because you lose it on density and keep-out regions. So you see the complexities here that nobody ever talks about. They just say, look at this, yay, high bandwidth compute, let’s go. And that’s it.

Vik: Totally. On that point, this was obviously an investor day, so they teased some technology, but they didn’t get into the technology weeds. I would love to see Qualcomm have a data center day or something focused on the technical architecture and all the technical details. Or ultimately just publish some papers on this, show it at Hot Chips, whatever, because there are lots of technical questions. But if they can answer them confidently, then it gives a lot more credence to what they tried to say at investor day, which is: we’re late, we’ve got a new approach, we think it can ultimately be competitive, it’s HBC, and we’ve shown you all the technical bits and answered all your questions with satisfaction. So you can believe that it’s possible, it’ll work, and it’ll scale.

The Roadmap: Accelerators, Alphawave, and the C1000 CPU

Austin: Yeah. So I think we’ve spoken about the technical complexities of HBC. We don’t know any more details, like you say, unless they publish something. But the first HBC-based chip is expected in 2027, that’s what they said. And then they showed a chart that they’ll do the AI 300 in 2028, and they’ll use UALink and E-sun for scale-up fabrics. And then somebody in the audience asked, when are you doing scale-up CPO? They said, yeah, it’s going to be after that. So maybe a 2029 thing would be CPO. It’s interesting that this is in the works, but we really have to see the silicon show up to understand anything more than what’s already been announced here.

Vik: Totally. So on the accelerator roadmap, they said, yes, we’ve got a multi-generation accelerator roadmap. Historically they had the AI 100, that was a long time ago. I’m sure they learned some lessons, but you could argue it doesn’t really count. The AI 200 is sampling in 2026, and it does not have this HBC we’re talking about. It is the AI 250 that has the first generation of HBC technology, and that’s in 2027. And then, to your point, the AI 300, which isn’t until fiscal year 28. When does Qualcomm’s fiscal year start? You would know.

Austin: That’s a good question. I never followed the financial side of things when I was at Qualcomm, I was doing engineering work. But I think it starts in 2027 actually. The reason I say that is, at the end, when the CFO was talking about FY 2027, he mentioned, hey, FYI, that’s actually in calendar year 26.

Vik: Yeah, right. Exactly. Well, I don’t know if it’s a full year, but it probably starts in June or something.

Austin: Which is actually one year earlier, yeah.

Vik: Qualcomm fiscal year start, I’m Googling it, audience. According to the AI overview, Qualcomm’s fiscal year begins on the last Sunday of September. So they pull it forward by a quarter, essentially.

Austin: Right. So I did pay attention a little bit.

Vik: So the AI 300, that’s when they get the second generation of this HBC. That’s also when they add scale-up, UALink or E-sun, and copper and optical scale-out. So they started to have the buzzwords. I think this is a nice transition to talk a little bit about Alphawave Semi. One of the things nowadays, if you’re coming to compete in the data center accelerator market, you can no longer say, I have a chip. You have to say, I have a rack-scale solution, which not only means the accelerator chip, but the interconnect.

Going all the way back, Nvidia bought Mellanox, and that was their way of using M&A to say, we want to be more than just the GPU, we want to do the whole system, and Mellanox gives us all the networking, scale-up, scale-out, switches, all the good stuff. So the question is, what is Qualcomm’s Mellanox? And Alphawave is an acquisition they made, I think about a year ago, maybe a little less. Alphawave historically is well regarded for their IP, a lot of communication IP, from SerDes and essentially taking an accelerator and making it able to talk at high enough bandwidth, getting data in and out, communicating with industry-standard networks, talking to a Broadcom switch on the other end, or whatever.

I’ll also mention that Alphawave Semi brings custom silicon customers to Qualcomm, because Alphawave was pretty smart: hey, if we’re good at the hard part, SerDes and IO, we can help people do custom XPUs. That’s essentially what Marvell does, what Broadcom does, we could license you the hard part, or we could also do the so-called easier part, like the front-end RTL stuff. So Alphawave Semi was actually also in the game of custom XPUs. Not only did Qualcomm acquire the IP and the talent, but they also acquired customer relationships and roadmaps that Alphawave Semi had with these huge hyperscalers. They didn’t name them, they said there are two. And then separately on the call, Satya Nadella spoke and Mark Zuckerberg spoke, so that implies Meta and Microsoft are working with Qualcomm on data center. But they specifically called out two custom silicon customers, which are presumably heritage, legacy Alphawave ones. I didn’t think about this until just now, but Alphawave was public, so a person could probably go back and figure out who those customers are.

The CFO also said they expect $1 billion of revenue in 2028, I think, where total revenue would be $5 billion. But $1 billion will come from each of these hyperscalers, so $2 billion is already spoken for. I don’t think it’s actually Alphawave’s customers, because he said that on top of this, we have the Alphawave business as well that will add on top. So he says things are looking very good, that was the CFO’s whole thing.

But in terms of acquisitions, their Modular acquisition that was recently announced is very interesting too, because you can’t build a rack-scale solution without providing a software layer to go with it. That’s exactly what Modular brings to the table. They have something called Mojo, which is somewhat equivalent to Nvidia CUDA in the programming layer. They also have something called MAX, which is the equivalent of Triton or TRT-LLM, for model serving. And they have the cloud product, which is distributed, it’s like Nvidia’s Dynamo, it handles KV cache offloading and data movements and all of that. So Modular basically lets you use this software layer to run what they call multi-silicon token factories, which means this software layer will tie together hardware from multiple vendors in a single solution, so you can mix and match. That’s a powerful thing, a Qualcomm solution can be slotted in with others and still work.

Austin: Nice. Right. So this is the unicorn that everyone’s always talked about: write it once and run it everywhere. But when you peel it back, there are always trade-offs, you’re writing at some high-level abstraction, and then it’s trying to translate it down to something that runs, and usually what happens is things are unoptimized. There’s a translation layer higher up, and it’s unoptimized. So the natural question is, is this different?

This was a very surprising and strategically good decision by Qualcomm, because Modular is started by Chris Lattner, he’s one of the co-founders, and he’s a legend in the space of compilers and programming languages. In his PhD, I think he created the Clang compiler and LLVM. At Apple, he invented the Swift programming language. And he also has history with MLIR. At the end of the day, what Chris and team did is make it so you can build in, I think if you use their language, it’s like a superset of Python, but they have the hooks to go all the way down to MLIR, multi-level intermediate representation, to go way down the stack and hook in there.

So at the highest conceptual level, I’d think of it as: other approaches would say, yeah, write using our software and it’ll run on Nvidia’s and ours, but they’d have to do some translation at a much higher level, and it was unoptimized. Lattner’s team is able to go much further down the stack. So in the data center, this would be great, because you could say, hey, use Mojo, use Modular’s tools, write it for Qualcomm, and it will also run on Nvidia. Chris has said before that they can actually squeeze more performance out of Nvidia’s chips than Nvidia. So it’s like, we can also make sure you’re getting as much as possible out of your existing Nvidia infrastructure, potentially even more, that’s compelling.

Another really compelling angle is just Qualcomm infrastructure: what you deploy in the cloud on Qualcomm hardware or someone else’s hardware, you could also deploy on premises, on your desk, on your phone. That’s interesting too. It’s not just cloud multi-vendor silicon you could deploy across, in theory, you could easily deploy from cloud all the way to edge. Nvidia’s doing that too, with their laptop and stuff they’ve come out with recently, where you can write CUDA and it can run in the cloud, or on the DGX little box on your desk, or even on your laptop. But that’s still a proprietary environment. If you use Mojo and Modular, you’d get all those same benefits, but in a true open, modular, hence the name, environment.

Vik: Okay, so that’s good. We should move on and quickly mention what they called their CPUs for data centers, the C1000. It’s supposedly 5 GHz per core and 250-plus core count, runs a lot of PCIe Gen 7 with LPDDR and all of this. I think they have three different versions: one for agentic CPUs, one for general purpose, and one for AI head nodes, which is nice. And it looks like they had Mark Zuckerberg come in and do a video clip saying Meta is planning to deploy the C1000 in the data center, and that they have a multi-generational agreement to supply to Meta. So they already have a business customer there in Meta.

But the one question from the audience at the end on this topic was really funny. That analyst asks, hey, your CPU is for 2028 or something, it’s not this year. So the analyst asks, you say 5 GHz, but is your CPU any good in 2028? Now, everybody knows there’s an agentic AI CPU shortage now, but you don’t have a product for two years, what’s with that? And for that, the Alphawave CEO, Tony Pialis, right, his name was?

Austin: Yes, yeah.

Vik: Yeah, he was like, oh yeah, Qualcomm has the best engineers, and when they design stuff from the ground up, it doesn’t matter when it hits the market, it’s still going to be the best. I’m like, dude, I thought Amon was the bullish Qualcomm guy, which makes sense, because he’s been a Qualcomm guy since he was an engineer and now he’s CEO. But Tony Pialis showed up six months ago with the Alphawave acquisition, and I’m like, what’s with the bullishness about CPUs? I can’t be that bullish. I’m going to take that with a grain of salt. It’s good, maybe we still need CPUs. I don’t think we’re anywhere near the peak of what hardware is required for AI, agentic AI, and all that. Maybe CPUs will be required for another five years, because if you see AMD’s forecasts, there’s a massive growth of the CPU industry all the way to 2030, 2031. So in a sense, yeah, I buy that Qualcomm is not really late to the CPU game. But it’s not that easy to just say, yeah, we’re going to be the best. It’ll be one of the CPUs. And if they can provide it at scale and volume, with sufficient supply chain capacity, then people will buy it. So that’s the level take on it.

Austin: Yeah, to your point, there is a wave happening right now, and they’re missing that wave. It’s just like, we need all the CPUs we can get, they’re missing it. So what happens when they come back in? Well, if CPU capacity is a lot higher, then you’re going to have to compete more on performance or power or cost. So it’s good, if you know you’re going to be late, make sure you feel very confident that you know where it slots in. Which, by the way, I appreciate them calling out the difference in the type of workload and requirements you need from the head node versus general purpose, which is just running more of your SQL databases, because now your agents are pummeling them, versus the agentic rack running a lot of VMs with little agents spinning up tools, some making web requests, some compiling code. So I appreciate that they spelled that out. But if they’re going to compete at that agentic layer, they need to think really hard about the specs they want and make sure they get it right. It’s too bad they couldn’t have brought it in a year earlier, but it is what it is.

Edge AI and Robotics

Vik: There are reasons for that, which we won’t get into. But I want to quickly mention their other big angle, which is the edge AI thing, because Qualcomm is one of the biggest proponents of edge AI, other than maybe NXP, since it’s very important to their whole IoT and automotive business, which they’ve been doing for the longest time. They expect that what they call the software-defined vehicle is now going to be called the AI-defined vehicle. They gave a really interesting example: a car drives into a parking lot, sees a QR code, looks at it, identifies what it is, and then pays for it. You don’t get parking tickets, if time runs out, it can renew it, or get a notification on your phone, and take care of it all by itself. I thought that was a nice example, and apparently that’s already in deployment.

So this is one use case they’re looking at, and they want to couple these high bandwidth compute units we spoke about into automotive SoCs, which means you can put AI into a car so it can think for itself and look at QR codes and identify this and that.

And they want to put vision as a primary driver for their whole edge inference play, because they say vision is the biggest way to get information, if humans can do most things with vision, AI should be able to. So they’re heavily centered on vision as a major unlock for industrial AI.

All of this was really cool, because they’re talking about converting cars into basically token generators. If you have this high bandwidth compute unit in a car, it’s actually using local AI inference, connectivity may exist, yes, but you can use local AI to do a lot of stuff, and it’s really fun. I think this concept is really nice. I don’t know whether it’ll materialize, but it’s fun to hear about all these applications.

Austin: It’s how do they. And the nuance I’ll add is that many cars are already token generators, but they’re captive. It’s for ADAS and autonomy. So your Rivian, your Tesla, your whoever, you’re running end-to-end neural nets these days on potentially Nvidia chips, or custom chips in the case of Rivian. But it’s captive, that is for essentially driving the car.

So what’s cool is, if you can enable the cockpit, the user experience, the user interface, to have AI and enough compute headroom to go experiment and do very interesting things, whether it’s just, hey, next song please, and you don’t have to take your hands off and it actually works, or the car itself doing interesting things for you.

Vik: Yeah. A lot of these edge IoT things are really fun, because, if you remember, they recently acquired Arduino too, and they have the Dragonwing platform, which I believe they’re launching later this summer. So what you can actually do is buy an AI card off of Amazon and use that to run Claude locally.

Those are cool. I don’t know what kind of model sizes, but they said you can run Claude Code locally, that’s what Qualcomm said in their investor day presentation. So I assume it’s a capable model. But I think it’s nice. They showed all these applications in retail, where you can stock shelves and it automatically restocks, and you have all this intelligence within the department store. And how they use it in energy, oil, gas, everything.

But their long-term play at this moment is basically robotics, because that’s what they view as their absolute future opportunity, which they mentioned to be a $1 trillion opportunity, in 2040, though, if you see it.

Austin: Always 2040. Yeah.

Vik: It’s 2040.

Austin: So it’s like, okay, whatever, we’ll retire by then. But what do you need to do interesting robotics? You need a CPU that’s constrained by power, because it’s probably battery powered. You need accelerators, you need memory. And one of the things we don’t have today is cheap enough, high-capacity, high-bandwidth enough memory at the edge.

So we have to run these crappy little models with very little context. If HBM or other innovations can bring us much more memory and much more bandwidth, and still do it in a way that makes sense from a power-envelope perspective, that’s really compelling. What if today’s frontier-level model, not even Fable... Fable, I miss you, come back, give me a call, but, you know, Opus-level, three or four years from now, if you could get that at the edge and fit it in, I think the opportunities are very compelling.

Oh yeah, and then what else do you need? You need connectivity. So they kind of have the whole portfolio: CPU, accelerator, some memory innovations, connectivity. It’s very promising for Qualcomm. Oh, and you need the software stack, they’re acquiring that with Mojo, Modular. Wouldn’t it be interesting if they acquired it for the data center, but actually the best place for it to capture the most value was robotics, seven years from now?

Vik: That’s my whole outlook. I think we’re coming up on time anyway. So I just wanted to mention that my whole outlook on what the Qualcomm investor day came away with: their data center entry point is a little bit late, yes, but we are nowhere near the peak of what compute and AI is anyway. So maybe, like you say, it’s just a blip in the long time horizon here.

But that’s a short-to-medium-term play. I think if edge AI really becomes something widely adopted, Qualcomm has a very, very strong portfolio, and they could come up and dominate edge AI like they did communications for a good decade. So I think they have a very strong edge AI play, but whether that’s going to come next year or whatever is the question.

Austin: It’s going to take a while.

MOAR Memory

Vik: So I remember you mentioned in the beginning that you got to ask Cristiano a question. I don’t know if it was on the record or off the record, but it doesn’t matter, now I’m curious, what did you ask him?

Austin: Yes. So it was not on the recording. I was in a room with Akash, the CFO, and Cristiano, the CEO. Industry analysts had a chance to ask questions, and this one was on the record, so I can talk about it. Sometimes it’s on background, so you can’t talk about it.

I basically said, hey, you introduced HBC, which needs less HBM but more DDR. DDR uses fewer memory wafers than HBM. So on the one hand, that could shift the mix from HBM back into DDR’s favor. On the other hand, this actually opens up the opportunity to bring much more memory to the edge. So, Cristiano, from your perspective, how should we think about the memory market in 2028, 2029, and 2030, when more supply is coming on, but new innovations like this are going to shift the mix, but also just grow the pie, because the edge is going to need more? How should we think about it?

And he was like, that was very many questions, that was a big question, but it’s very good and very interesting. I think he was basically like, HBM’s not going anywhere. Don’t think HBM is dead, we’re going to need HBM. But he said what’s interesting is the amount of increased demand there will be from on-premise infrastructure, from the workstation on your desk to your laptop to your car, for LPDDR and more memory. So he was also giving the MOAR memory vibes, more memory.

Vik: Amazing. And in general, was everybody really excited about all the Qualcomm announcements, from what you could see around you?

Austin: Oh yeah. I think all the other analysts in the room were excited. Investors were excited. There are always the technical questions, some people are naturally more skeptical than others, so it’s like, okay, you introduced a lot, you talked about it, we want to see the technical proof. And some of that is just, you have to know the context of this being an investor day. What are we going to talk about, how in the weeds are we going to get? And these things take time. So I think you can give Qualcomm the benefit of the doubt, but they do eventually need to follow up with technical details, especially if stuff’s not shipping for a few years. The best thing they could do is write a paper, give a presentation, whatever, to prove that at least in the lab, it’s real and it works.

Vik: Yeah. So we still need more memory. Good to know.

Austin: Yes, totally. Okay, maybe here’s one last bonus thought, we won’t even talk about it, we’ll talk about it more some other time. If HBC can bring much more memory close to the accelerator, let’s not call it HBC, let’s just say, industry-wide, near-memory compute, what are the implications on the memory market? Obviously we’re still going to want HBM, but now all of a sudden, maybe even more DRAM. And not even from a data center perspective, but when we’re talking about bringing more data to the edge, robotics, cars, and stuff, it just feels like even more wafers are going to be needed.

Vik: More memory. MOAR. Yes.

Austin: MOAR. Exactly. Don’t let anyone DeepSeek you and tell you, oh, HBM’s dead because near-memory compute. No, MOAR, more memory.

Vik: All right, we should call it with that. Yeah.

Austin: Yeah, let’s call it there. Everyone, thanks for watching. We appreciate you curious, intelligent, interesting people who love semiconductors and listen all the way to the end. Check us out on YouTube, leave comments, check us out on Spotify, send us emails, whatever. We have a daily, if you like our takes, you can get them daily for free at semidope.com. Check it out, and thanks for listening.
