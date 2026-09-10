---
title: "Where Does a Robot Think – On-Device vs Datacenter Inference"
source: "https://newsletter.semianalysis.com/p/where-does-a-robot-think-on-device"
author:
  - "[[IVAN CHIAM]]"
  - "[[ZANE FONG]]"
  - "[[BRYAN SHAN]]"
published: 2026-09-09
created: 2026-09-10
description: "The Embodiment Problem, Planning vs Action Layers, Glass-To-Glass Budgets, Wafers & DRAM Constraints, One B300 vs 56 Thors TCO, Factories To Caves"
tags:
  - "clippings"
---
For most of its short history, AI lived behind a screen. That’s starting to change.

First came chatbots, good for answering a question or drafting an email. Then agentic AI, models that don’t just respond but do real work on a computer: navigating software, calling tools, finishing multi-step tasks on their own. Now the frontier is physical AI, intelligence that reaches past the screen to perceive the world and act on it. The biggest piece is robots, and it is still early: the hardware, the models, and the economics are all being worked out right now.

## **The Embodiment Problem**

With LLMs, the hardware bends to the model. For hyperscalers and AI labs, there’s no hard latency requirement and a very high spending ceiling, so the process is simple: pour in as much data and compute as possible at training, then figure out how to serve the model that comes out. The model comes first; the hardware serves it. Robotics inverts this. Tighter constraints flip the order of design: you first work out what it takes to serve a model on the robot, then build a model that fits. Two constraints drive this.

The first is time. A robot runs real-time control loops and can’t miss a deadline. An LLM can be slow without affecting the final output. If a robot is slow, the world changes around it, and then the action is obsolete by the time it needs to enact it.

The second is cost. When you use an LLM, it lives behind a screen provided by the user. In robotics, the manufacturer has to build both the compute and the robot itself and pay for it upfront, on every unit, and the capital expenditure can be immense. At scale, this upfront cost can be billions and even in the trillions if we do eventually get to a billion robots.

Because of these two constraints, in robotics the on-robot hardware is fixed, and the model is designed to fit it. Even at hyperscaler funding levels, most of the capital will have to go into the robots and factories themselves, not into compute. Model capability is therefore capped by what can run on affordable, real-time hardware on the robot, and intelligence becomes something you ration against latency and unit economics.

## **Robot Models Are Still Small…**

This is why frontier robot models remain far smaller than frontier LLMs, which have already pushed into the trillions of parameters. Today most frontier robot models sit between roughly 5 and 14 billion parameters: Physical Intelligence’s π0.7 at 5 billion, and NVIDIA’s DreamZero at 14 billion.

[![](https://substackcdn.com/image/fetch/$s_!F5RL!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b08ff38-9526-460d-b73f-fed4cf64f380_2176x1144.png)](https://substackcdn.com/image/fetch/$s_!F5RL!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4b08ff38-9526-460d-b73f-fed4cf64f380_2176x1144.png)Source: SemiAnalysis

In LLMs, scaling laws have held, scaling has consistently broadened the range of problems a single model can solve. Early results show robotics might work the same way. Data has been a constraint but that is now scaling with World Models and Embodied human data collection. Embodied AI faces limits language models never did, like scarce data and the cost of real-world interaction, so whether scaling pays off the same way is genuinely an open question.

If robot models do continue to scale, the question becomes where should all that compute run, given the latency, cost and model limits mentioned above. The field is genuinely split, with different companies making diverging bets. Figure runs its in-house Helix model entirely onboard the robot. Physical Intelligence’s π0.7 model goes the other way and runs its policy off-robot on a single H100. NVIDIA’s DreamZero, a 14-billion-parameter “world action model” built on a video-diffusion backbone, needs two GB200 GPUs off-robot just to run in real time.

Our view is that a cascade is inevitable. Some robots will run cognition on-board, while others will offload it to GPUs sitting in a datacenter. The biggest robot model builders today, like NVIDIA and Google DeepMind, will lean toward this cloud approach, running the heavy cognition on cloud GPUs, with only a small edge model on the robot for low-level control and safety.

Smaller builders, such as Dyna and Sunday, may initially favor models that fit on a Jetson or consumer GPUs because their early deployments operate within narrow, controllable environments where onboard inference is sufficient. As deployments scale, however, they will converge on whichever mix of onboard and off-robot compute delivers the best performance and economics for their business model.

Moving the GPU off the robot brings real benefits, but also real challenges. Chief among them is latency, and it doesn’t work everywhere. In environments with poor connectivity, cloud deployment isn’t an option at all. Despite these difficulties, off-robot compute remains beneficial, and in some cases necessary, as the following sections show.

## Models in Robots

Before we get into why the robot model should run in an off-robot datacenter, here’s a quick primer on how robot models work, and which ones we’re talking about.

Robot control is a broad space. Hard-coded control, where engineers write out the rules and math for every movement, has run factories for decades on embedded compute, and small task-specific policies fit onboard just fine. That’s not our subject. We’re talking about data-driven generalist robotics, robots run by large foundation models, because that’s where the frontier is.

Even within data-driven generalist robot models, architectures vary. Some are monolithic: one model that goes straight from what the camera sees to how the motors move. Many are hierarchical: a big, slow model decides what to do, and a small, fast one turns that into movement, hundreds of times a second. Our argument for off-robot datacenter compute is about these hierarchical models, where the brain separates into two or more layers, most often a planning layer and an action layer.

The planning layer is the slow, high-level one: it perceives the scene, reasons about space, and plans the task. The action layer is the fast, low-level one: it turns those plans into motor commands. The planning layer, which is also the heavy part of the model, is the more forgiving: it updates only a few times a second and runs asynchronously from the control loop, so the action layer keeps acting on the most recent plan while the next one is still in flight. That decoupling lets planning absorb the delay, and even the jitter, of a wireless round trip, while the action layer runs at hundreds of Hz and can tolerate none of it. So planning is the natural candidate to move into the datacenter, while the fast control loop stays local.

[![](https://substackcdn.com/image/fetch/$s_!ChJt!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff393990c-76fa-43af-ab99-dc4f50c08a4f_2152x1092.png)](https://substackcdn.com/image/fetch/$s_!ChJt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff393990c-76fa-43af-ab99-dc4f50c08a4f_2152x1092.png)Source: SemiAnalysis

The amount of planning scales with how general the robot’s job is. A generalist built to handle open-ended tasks needs a large planning model doing genuine reasoning, and those models are heavy. That reasoning is exactly what gets pushed to the datacenter. A specialist is the opposite case: a narrow policy doing one repetitive job carries little high-level planning, so the whole model is small enough to stay on the robot.

## Why DC GPUs are better suited…

Specialist robots are for the most part solved: factories have run on them for many years now using hard-coded automation, but not modern AI. But a specialist is rigid, one task at one station, idle when the bottleneck moves. Generalists are the frontier because one flexible robot can cover many jobs, redeploy to wherever is bottlenecked, a changing product mix, and the long tail of unstructured work. This aligns with some of the many lessons of the Toyota Production System, where we learned that multi-skilled workers can reduce waste and improve economic efficiency. As a result, the TAM for generalist robotics is huge, not just in manufacturing and warehousing but also in homes and other places.

The more generality you demand, the more you lean toward FLOP-hungry foundation models and datacenter-scale compute. Not every robot needs maximal generality, and many tasks are served well by smaller models, but the frontier of flexible, general-purpose robots is where datacenter-scale compute becomes necessary.

## **LLMs vs Robot Models Token Flow**

An LLM ingests and emits huge, bursty token counts: a long prompt to prefill, then a long generation, with a KV cache that grows the whole time. That is the memory wall, the capacity to hold that cache and the bandwidth to stream the weights and cache on every token, and it makes LLM serving bandwidth-bound.

A robot model is the opposite, a smaller steady stream, more metronome-like rather than a burst. It never stops, because a robot is not answering one question and halting; it is locked in a closed loop with a moving world, taking in a fresh frame and emitting a short action chunk a few times a second. Each frame is compressed in dedicated hardware (the ISP and video-codec ASICs) into a fixed, compact token budget of tens to a few hundred tokens. So robot models are not as memory capacity and bandwidth bound in the same way that LLMs are.

[![](https://substackcdn.com/image/fetch/$s_!WVGn!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcc9f1f18-6d66-45b3-bb44-7abc9b8ee910_1792x1112.png)](https://substackcdn.com/image/fetch/$s_!WVGn!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcc9f1f18-6d66-45b3-bb44-7abc9b8ee910_1792x1112.png)Source: SemiAnalysis

## **Frontier Robot Models are FLOPs hungry**

What binds a frontier robot model sometimes memory, but often it is the FLOPs to run it.

These are FLOP-hungry workloads: a VLA (Vision Language Action model) is a multi-billion-parameter model, orders of magnitude larger than the specialist policies before it, and its vision and language stages, which are the bulk of the work, are compute-bound on any capable GPU. A WAM (World Action Model) is heavier still. Instead of naming an action, it generates video of the predicted future and derives the action from it, through iterative denoising, meaning one action could take multiple full forward passes through a model.

Edge silicon cannot keep up. Nvidia’s latest Jetson Thor, the best-in-class robot brain, has only about a tenth of a single B200’s compute, and roughly a fourteenth of a B300’s. DreamZero (a 14B WAM) needed two GB200 GPUs just to reach ~7Hz, which is on the order of twenty times the compute a single Thor can muster. Run the same model on a Thor and it would fall to a fraction of 1Hz, far too slow for real-time control.

[![](https://substackcdn.com/image/fetch/$s_!s1nK!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb14e5b6e-f670-4adb-aafd-a1a5159dcf19_2702x1186.png)](https://substackcdn.com/image/fetch/$s_!s1nK!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb14e5b6e-f670-4adb-aafd-a1a5159dcf19_2702x1186.png)Source: SemiAnalysis

[![](https://substackcdn.com/image/fetch/$s_!EbLA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fabefc74a-e5e4-4fd1-b144-e049be2658cd_1686x1072.png)](https://substackcdn.com/image/fetch/$s_!EbLA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fabefc74a-e5e4-4fd1-b144-e049be2658cd_1686x1072.png)Source: SemiAnalysis

## **Shipping the Robot Model Off Device**

If a Jetson Thor can’t keep up, and we off-load the heavy, compute-intensive part of the workload to datacenters, it means optimizing local compute for safety loops and high-frequency control loops, and doubling-down on network interfacing.

The primary consideration is the glass-to-glass latency budget we need to hit, and hit reliably. The network will produce issues with bandwidth and stability, and we will feel this the most when transmitting image data.

Transmitting image data quickly and reliably is more than just a dedicated compression ASIC on-device and calling it a day; the entire upstream image processing pipeline must be optimized. Noise is the enemy of compression, the less spatiotemporal structure an image has, the harder it is to compress. So a good local compute system optimized for networking will prioritize the components that keep noise out of the image in the first place: optics, low-light sensor performance, sensor SnR, thermal management, and the image signal processor (ISP).

ISPs turn messy analog signals into digital ones, but can ruin compression efficiency when not optimized for compression directly. And when we consider the imaging pipeline as a whole, we are optimizing for the model, not for human viewing. This is similar to how WAMs do not require the extra denoising steps that typical video diffusion models use; they solve a different task. The same principle applies here: we care about good model outputs and a low bitrate, not necessarily beautiful images (see below).

[![](https://substackcdn.com/image/fetch/$s_!1ltz!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2611c6e0-8bb2-49ab-99be-1100b09c914e_1672x826.png)](https://substackcdn.com/image/fetch/$s_!1ltz!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2611c6e0-8bb2-49ab-99be-1100b09c914e_1672x826.png)Left image is more pleasing to the eye, but the right image has a higher SnR. Source: [NASA](https://ntrs.nasa.gov/api/citations/20170000636/downloads/20170000636.pdf)

Network conditions introduce a lot of variability, so local compute must also incorporate dynamic, real-time adaptation of both the ISP and the compression bitrate, similar to WebRTC, to gracefully handle constantly fluctuating network conditions and do so without adversely affecting model performance.

A pipeline that produces a clean, adaptable stream also needs hardware explicitly tuned for offloading – getting the bits off-device and on-schedule. Historically, mobile chipsets prioritized downlink speeds, but robotics requires massive uplink capacity to stream out high-fidelity telemetry. The download can be relatively small. This means multiple transmit antennas with proper placement, since the environment and robot itself can block signals. It also means support for a wider array of RF bands to allow multiple channels for higher throughput and less congestion – especially with factory conditions in mind. Optimizing hardware and embedded firmware for fast handovers between access points and between WiFi and 5G is critical since the typical handover time will temporarily kill the latency budget. Jitter is the biggest enemy.

The end goal is a highly coordinated hybrid architecture that maintains a healthy, but not overly indulgent, amount of FLOPs locally for safety and high-frequency control and can reliably off-load the “foundation” part of a foundation model. It’s not a perfect system: simple control loop fallbacks are still required the moment the network connection diminishes or is completely lost. We require latency watchdogs, heartbeat timeouts, and staleness bounds on remote actions.

## **Power**

Datacenter GPUs have to run off the robot, because the battery can’t feed them. A single Blackwell GPU draws ~1.2-1.4 kW and has to be liquid-cooled, built to sit in a rack. A humanoid, by contrast, stores only about 2 kWh in its battery and draws a few hundred watts in normal motion, a kilowatt or two at peak, everything included, which is why its onboard brain is a 40 to 130 W Jetson Thor. Put a datacenter GPU on the robot and the chip alone would out-draw the whole machine, demand cooling it can’t carry, and flatten the battery in minutes. Offloading sidesteps the power constraint. The robot carries only a 20 to 30 W perception compute + wireless board to reach the datacenter GPU, comfortably within budget.

## The Supply-Chain Wall

Nvidia’s accelerator output is almost entirely datacenter silicon: a long Hopper ramp through 2023 and 2024 handing off to Blackwell, which scales sharply across 2025 and 2026 to dominate the mix. Jetson, the line used in robots, is the thin red sliver along the bottom, barely visible even in 2026. This is because the robotics market is nascent, real volume is years out, and there is next to nothing to build for.

[![](https://substackcdn.com/image/fetch/$s_!KqPD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F16d7f8da-1f57-413f-aa67-a9428c06a6d3_1362x938.png)](https://substackcdn.com/image/fetch/$s_!KqPD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F16d7f8da-1f57-413f-aa67-a9428c06a6d3_1362x938.png)Source: [SemiAnalysis Accelerator Model](https://semianalysis.com/accelerator-hbm-model/), we withheld Rubin shipments on this chart, buy the data

Margins tell a similar story. Demand isn’t there yet, but when it arrives, pricing will go up and Jetson margins will inflect. But for now, a Blackwell datacenter GPU earns far higher gross margins than a Jetson module, on the order of mid-to-high 70s percent versus mid-60s, so NVIDIA has every incentive to point its scarce leading-edge wafer capacity at the datacenter and little reason to ramp edge silicon while the robotics market stays small. Robotics chips like Jetson Thor also require a lot more memory per unit of compute which is a major roadblock.

[![](https://substackcdn.com/image/fetch/$s_!pP39!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F29e76318-982e-4731-a1f7-3e2b88f22e41_1212x850.png)](https://substackcdn.com/image/fetch/$s_!pP39!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F29e76318-982e-4731-a1f7-3e2b88f22e41_1212x850.png)Source: [SemiAnalysis Accelerator Model](https://semianalysis.com/accelerator-hbm-model/)

Worse, robot silicon is converging onto the exact nodes the datacenter is fighting over. Nvidia’s Jetson line used to be insulated: the previous generation, Orin, ran on Samsung’s SF8 process. The current generation, Thor, has closed that gap onto TSMC N4, which Blackwell uses, and as robots run on more capable models their silicon has to stay on the leading edge: the generation after Thor likely moves to N3 alongside Rubin, then N2 alongside Feynman, exactly the nodes the entire AI-accelerator roadmap is fighting over. So a low-volume, lower-margin Jetson will always be competing for advanced-node wafers from the back of the queue.

[![](https://substackcdn.com/image/fetch/$s_!o0_d!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d3a7504-6aed-4c0a-917f-dfd935c8611f_1362x990.png)](https://substackcdn.com/image/fetch/$s_!o0_d!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F0d3a7504-6aed-4c0a-917f-dfd935c8611f_1362x990.png)Source: [SemiAnalysis Accelerator Model](https://semianalysis.com/accelerator-hbm-model/)

[![](https://substackcdn.com/image/fetch/$s_!HNJN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a4cc3df-cb9e-4089-afe4-d317b49272ea_1364x990.png)](https://substackcdn.com/image/fetch/$s_!HNJN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F3a4cc3df-cb9e-4089-afe4-d317b49272ea_1364x990.png)Source: [SemiAnalysis Accelerator Model](https://semianalysis.com/accelerator-hbm-model/)

But the wafer demand from robots is not where the strain is. A million Jetson-class chips in 2030, each around 400mm², is only about ten thousand wafers for the year, a rounding error next to the datacenter GPU ramp, because Thor’s die is barely half a reticle size chip, and there simply aren’t many robots yet. Supply only tightens once robots need tens of millions of chips a year, well beyond 2030. So the real question is not whether robots can get wafers. It is silicon efficiency: for a given fleet of robots, which approach consumes less leading-edge silicon? Putting a chip in every robot, or serving their cognition from shared datacenter GPUs.

[![](https://substackcdn.com/image/fetch/$s_!yaj3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8bdb2a2b-3a60-404e-a670-fbf411c98dd6_1368x992.png)](https://substackcdn.com/image/fetch/$s_!yaj3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8bdb2a2b-3a60-404e-a670-fbf411c98dd6_1368x992.png)Source: [SemiAnalysis Accelerator Model](https://semianalysis.com/accelerator-hbm-model/)

If you look at silicon efficiency as wafers per robot, the onboard chip and the shared datacenter GPU cross over at around 7 robots per GPU. Beyond that, serving cognition from a shared GPU takes less silicon per robot than putting a chip in every machine. And that’s what really matters here, because when fab supply is scarce, the approach that uses less silicon per robot is the one that scales.

[![](https://substackcdn.com/image/fetch/$s_!KZer!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a2d80ff-e70c-4437-90e2-8315440c759b_1356x982.png)](https://substackcdn.com/image/fetch/$s_!KZer!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F7a2d80ff-e70c-4437-90e2-8315440c759b_1356x982.png)Source: SemiAnalysis

Another major bottleneck is memory. Each Jetson generation has carried more DRAM than the last: Jetson Xavier used 32GB, AGX Orin 64GB, and Jetson Thor now uses 128GB of LPDDR5X, with future generations set to keep climbing. Although total DRAM wafer capacity continues to grow, most of the incremental capacity is being absorbed by HBM for AI accelerators. 

That leaves the commodity and LPDDR supply that robot brains depend on competing for a shrinking pool of non-HBM wafers. Similarly, when DRAM is the scarce resource, the approach that uses less DRAM per robot is the one that scales. The LPDDR is better off being allocated to Vera GPUs or wafers to HBM.

[![](https://substackcdn.com/image/fetch/$s_!Bwbm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05f82ac7-8b85-49d0-8925-bb2cab6cd725_1270x896.png)](https://substackcdn.com/image/fetch/$s_!Bwbm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F05f82ac7-8b85-49d0-8925-bb2cab6cd725_1270x896.png)Source: [SemiAnalysis Memory Model](https://semianalysis.com/memory-model/)

Memory tells a similar story, the onboard chip and the shared datacenter GPU cross over at around 5 robots per GPU. Beyond that, serving cognition from a shared GPU takes less DRAM per robot than putting a chip in every machine.

[![](https://substackcdn.com/image/fetch/$s_!Z5BS!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74cf355c-15ef-48ad-8ea2-39bca79ed103_1168x854.png)](https://substackcdn.com/image/fetch/$s_!Z5BS!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F74cf355c-15ef-48ad-8ea2-39bca79ed103_1168x854.png)Source: SemiAnalysis

## The TCO Verdict: One B300 server vs. 56 Thors

We ran DreamZero, current leader on RoboArena, on a real B300, using the inference optimizations from NVIDIA’s WAM paper (CUDA graphs, DiT caching, NVFP4 quantization, moving the scheduler onto the GPU). We also ran a single denoising step to match the DreamZero-Flash setup, though without Flash’s retraining recipe, so task quality is unvalidated.

DreamZero’s serving profile is prefill-shaped: each inference pushes a full chunk of video latents (thousands of tokens) through the 14B DiT in parallel, so a B300 is compute-bound at batch size 1. Batching therefore buys nothing: FLOPs scale one-for-one with batch size, and every robot just waits longer. Instead, we time-multiplex, with the B300 serving each robot sequentially. This is specific to video-generating WAMs. A VLA like π0 or GR00T flips the roofline: a few hundred tokens through a small backbone leaves the GPU memory-bandwidth-bound, so batching amortizes the same weight reads across robots and throughput scales nearly linearly with batch size. Serve a VLA fleet with continuous batching; serve a video WAM one robot at a time.

A key assumption we made is that Network RTT is 10ms, meaning the GPU sits on-prem near the robots. Each inference buys the robot its next 1.6 seconds of motion, which makes 1.6 seconds our latency budget: the total time a request gets to spend across network, queueing, and compute before the robot runs out of instructions and stalls mid-motion.

[![](https://substackcdn.com/image/fetch/$s_!xNF4!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d7f24de-6676-4e95-965b-40f5b1e91b93_956x648.png)](https://substackcdn.com/image/fetch/$s_!xNF4!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4d7f24de-6676-4e95-965b-40f5b1e91b93_956x648.png)Source: [Nvidia](https://arxiv.org/html/2602.15922v1)

We read the chart below on p99 latency (blue line), the 99th percentile response time. 99 out of 100 requests come back faster than this, so it’s effectively the worst case. It matters more than the median (green line) here because a robot stalls the moment any single chunk shows up late. We see that the maximum number of robots we can process on 1 B300 GPU is 7 robots. At 7 robots, p99 is 1.16 seconds, still under the wall, with zero missed chunks over the run.

[![](https://substackcdn.com/image/fetch/$s_!kftX!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F11ee04d9-e49a-4c50-b190-159dfaef8249_1508x910.png)](https://substackcdn.com/image/fetch/$s_!kftX!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F11ee04d9-e49a-4c50-b190-159dfaef8249_1508x910.png)Source: SemiAnalysis

Now that we know we can time-multiplex 7 robots per GPU, the fundamental TCO question stands: 

## Is it cheaper to offload compute to a B300 server, or to run inference on-device in a Jetson Thor?

We build up two scenarios: the offload scenario assumes one Blackwell-class server which can serve 7 robots (i.e. one B300 NVL8 server serving 56 robots), and an on-robot scenario of the same 56 robots each carrying its own Jetson Thor. In both scenarios, common parts across both cases (i.e. mechanical components, robot shells) are not included in the BOM cost calculation.

We also discuss the biggest challenge with this deployment mechanism.

The offload scenario is one B300 NVL8 plus 56 wireless boards (one per robot) to connect the robot to the GPU cluster in the datacenter. That brings all-in capex to ~$542K, which, including operating costs like colocation and power, leads us to a TCO of $18.32/hr in the offload scenario.

[![](https://substackcdn.com/image/fetch/$s_!5sI0!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa1078a13-ffbd-47c1-a1e3-ea5e59ed6c30_1584x1022.png)](https://substackcdn.com/image/fetch/$s_!5sI0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fa1078a13-ffbd-47c1-a1e3-ea5e59ed6c30_1584x1022.png)Source: [SemiAnalysis AI TCO Model](https://semianalysis.com/ai-cloud-tco-model/)

The on-robot scenario is 56 Thor modules at $3,500 per unit, each with its own baseboard, storage, cooling, incremental battery, and onboard radio connectivity, landing at ~$230K. Accounting for the above, along with power costs for the Thor modules, leads us to a TCO of $6.58/hr for the 56-chip deployment.

[![](https://substackcdn.com/image/fetch/$s_!DX0r!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff3afcbc5-ac57-4aa7-b50d-a8a29bdd1ad7_1606x1024.png)](https://substackcdn.com/image/fetch/$s_!DX0r!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff3afcbc5-ac57-4aa7-b50d-a8a29bdd1ad7_1606x1024.png)Source: [SemiAnalysis AI TCO Model](https://semianalysis.com/ai-cloud-tco-model/)

Before accounting for utilization, the two cases are close on TCO per FP4 dense FLOPs: $0.15/hr/PFLOP in the offload scenario, and $0.11/hr/PFLOP in the on-robot scenario.

[![](https://substackcdn.com/image/fetch/$s_!FEs-!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7f45bdd-c292-4a68-96fe-071c25f3a7d2_1982x644.png)](https://substackcdn.com/image/fetch/$s_!FEs-!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fd7f45bdd-c292-4a68-96fe-071c25f3a7d2_1982x644.png)Source: [SemiAnalysis AI TCO Model](https://semianalysis.com/ai-cloud-tco-model/)

However, utilization is the swing factor in TCO. A robot and the GPU behind it are almost entirely fixed capital, so the bill is the same whether the asset runs or sits idle, and cost per productive hour scales inversely with how much it works.

On-robot chip utilization today is highly deployment-dependent. In the home, one company that has deployed robots in volume told us its robots run just 1-2 hours a day, only 4-8% of the clock, because chores are bursty and current models still cap what can run unsupervised. That figure is trending up, toward 4-5 hours (17-21%), as capability improves and new features drive engagement. But the home has a hard ceiling: eventually the chores run out. Industrial demand is continuous and should clear a higher bar. Figure’s BMW deployment is an anchor we have: roughly 1,250 operational hours over about 11 months of weekday shifts, working around 10 hours a day at 40% utilization. As model capability improves, industrial utilization should climb well beyond that.

[![](https://substackcdn.com/image/fetch/$s_!sqTD!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F47898ba3-e527-4304-a972-55c3d3d80aeb_1966x634.png)](https://substackcdn.com/image/fetch/$s_!sqTD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F47898ba3-e527-4304-a972-55c3d3d80aeb_1966x634.png)Source: [SemiAnalysis AI TCO Model](https://semianalysis.com/ai-cloud-tco-model/)

We conservatively model ~40% utilization as our base case for on-robot chip utilization, which is factored into the table below. Net of utilization, the offload scenario reaches a TCO per FP4 dense FLOPs of $0.17/hr/PFLOP, while the on-robot scenario reaches a TCO per FP4 dense FLOPs of $0.28/hr/PFLOP. Here, the offload scenario reaches a mere ~60% of the on-robot scenario.

[![](https://substackcdn.com/image/fetch/$s_!bpU2!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8c547c11-845f-412b-9306-33dd2e2125f0_1914x1076.png)](https://substackcdn.com/image/fetch/$s_!bpU2!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8c547c11-845f-412b-9306-33dd2e2125f0_1914x1076.png)Source: [SemiAnalysis AI TCO Model](https://semianalysis.com/ai-cloud-tco-model/)

The shared GPU server often runs the other way, as its compute resources are pooled across the fleet and busy around the clock. Given that, in the scenario above, one B300 GPU can serve 7 robots within the latency budget, we model ~90% utilization of the GPU server.

Towards the top right corner of the sensitivity analysis below, high GPU server utilization and low chip on-device utilization swings the TCO per PFLOP massively in favor of the offloaded scenario. The offload scenario for current industrial deployments reaches ~60% the TCO per PFLOP of the on-robot scenario, reaching an even lower ~15% for home deployments.

It is only in several cases towards the bottom right corner wherein low GPU server utilization and high on-device utilization swings the TCO per PFLOP in favor of on-device inference.

[![](https://substackcdn.com/image/fetch/$s_!BWsj!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa54cf98-4f8b-4534-9496-01695fbf2fac_2018x918.png)](https://substackcdn.com/image/fetch/$s_!BWsj!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Faa54cf98-4f8b-4534-9496-01695fbf2fac_2018x918.png)Source: [SemiAnalysis AI TCO Model](https://semianalysis.com/ai-cloud-tco-model/)

The question arises naturally: How many robots have to be batched in order for such TCO per PFLOP savings to come through in favor of the offload scenario? Varying our batching assumptions below, for a standard industrial deployment, we see that anywhere from 4 robots per GPU and upwards, the TCO per PFLOP shifts in favor of the offloaded scenario.

On the whole, we find that offloading inference to a GPU server is a compelling case, except for cases with very small robot deployments with one on-site server sitting mostly idle - though even then, one could make the argument for renting compute as needed rather than owning an entire server to serve a few robots.

[![](https://substackcdn.com/image/fetch/$s_!xfaN!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83da760f-eb1d-417d-abed-ef77ae76eed5_1608x1046.png)](https://substackcdn.com/image/fetch/$s_!xfaN!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F83da760f-eb1d-417d-abed-ef77ae76eed5_1608x1046.png)Source: [SemiAnalysis AI TCO Model](https://semianalysis.com/ai-cloud-tco-model/)

## Where it works and where it doesn’t - the network layer

There are obvious issues with running the heavy part of your model off-device (see image below). We aren’t arguing that it will be easy; we are just arguing that it will be more practical than local compute for some applications.

[![](https://substackcdn.com/image/fetch/$s_!c6mQ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe8f82647-9803-47a3-b3b2-3508d115dbb0_1290x1676.png)](https://substackcdn.com/image/fetch/$s_!c6mQ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fe8f82647-9803-47a3-b3b2-3508d115dbb0_1290x1676.png)Source: X

Certain settings will be impossible to run off-device compute; caves, ruins, and disaster sites for example. Settings that are unpredictably occluded, dynamic, and with none of the wireless conditions correctly configured will rely on local compute options because the network cannot exist reliably, if at all.

Open agriculture and remote fields will be conditional on the latency budget of the model, since services like Starlink cover these areas but have higher latency and jitter. Properly managing this is difficult because we can only control some parts of the setup. We imagine that these settings would utilize a mix of on-device and off-device options, and the model’s latency budget will dictate the choice.

The home is easier, but not ideal. Walls and other obstacles create weak and dead zones, and the typical home router is not optimized for handoffs. Wireless conditions are often good, but congestion is a factor: homes typically run on shared fiber, so neighboring homes and apartments can degrade conditions. Making this work in the home under a tight latency budget would require specialized routers, as well as characterizing performance during peak WiFi utilization hours when the shared fiber link is loaded.

Factories and warehouses are extremely difficult because they are massive labyrinths of moving metal and heavy machinery that create a worst-case scenario for RF propagation. They suffer severe multipath interference, electromagnetic noise, and constant line-of-sight occlusion. But factories and warehouses are also where we have the most control. URLLC protocols and private 5G bands mean factories can achieve sub-10ms wireless latency when optimized. We can eliminate the internet transit layer entirely by placing the GPUs a few hundred feet away in the same building. Routers can use beamforming to maximize signal to robots on the floor. Factories and warehouses require the most work to be functional, but they can become the most optimized deployments as a result. The investment required depends on the latency budget, and whether the juice is worth the squeeze depends on whether this setup is cheaper than hundreds of robots with local GPUs. 

These deployments already exist, and off-device compute in factories and warehouses will be able to lean on existing infrastructure in some cases. And when the latency budget is generous, the in-building buildout may not be needed at all: one robot foundation model developer we know already serves production inference for an automaker and a industrial manufacturer from a cloud availability zone in the local metro, with no GPUs on site, because the control loop is able to tolerate a good amount of latency. These robots already talk to the cloud for data upload and tele-op, so inference rides on infrastructure that exists anyway. The only new cost is compute.

The country and regulatory environment in which the robot operates also has a significant impact. Certain nations employ national firewalls that perform deep packet inspection, which can severely degrade latency and jitter. Ultimately, once data is transmitted through the network, the host country exerts a degree of control that can directly compromise wireless conditions. This means that how countries react to robotics in the future will shape the on-device versus off-device tradeoff on a per-country basis. Speculatively, countries like the US will offer excellent wireless conditions for off-device robotics, while China and other countries that perform deeper packet inspection may end up pushing harder toward on-device compute.

Key to all of this is specifically architecting for safety, low-level control, and fallbacks for when the network inevitably fails. The robot needs to be able to run an extremely low-level local policy that returns it to a safe zone on failure. Think Figure’s policy that allows the robot to return for maintenance when an actuator fails, automatically accommodating a modified embodiment. In this case, it’s a modified brain; the fallback is a simple control loop that is 100% safety focused. Network uptime needs to hit 99.99%, so we need reliability first and this fallback second. Without both, there will be no off-device deployments. This failure mode is already the norm in today’s warehouses: AGVs trigger a safety stop and freeze in place when wireless drops.

## Conclusion

For a large and growing share of robot deployments, the brain belongs in the datacenter. The barrier to mass adoption is price: an expensive humanoid has no mass market, and prices have to come down for adoption to grow. That makes cost the battleground, and pulling compute out of every robot to share GPUs in a datacenter is a strong lever. It also fixes the worst part of being a robotics company: chips bought months before robots sell are dead capital, and ten thousand staged robots is $30M depreciating in a warehouse, whereas offloaded compute is a shared GPU that is already earning its keep.

Supply points the same way: leading-edge wafers and DRAM are largely allocated for, and NVIDIA has little reason to divert them while LLMs eat the supply, so offloading rides that buildout instead of fighting it.

None of this makes offloading universal. It depends on a network that holds up, and the environments vary widely: factories can be engineered for low latency, homes are workable with the right hardware, open fields are conditional on the latency budget, and some settings, like caves and disaster sites, rule it out entirely. A safety-focused local fallback is non-negotiable everywhere. But where the network can be made reliable, the economics win out, and the gap only grows as fleets scale and robots work more hours. What remains is execution, and the winners will be the few teams that can make the datacenter feel local.
