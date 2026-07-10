---
title: "DeepSeek Debates: Chinese Leadership On Cost, True Training Cost, Closed Model Margin Impacts"
source: "https://newsletter.semianalysis.com/p/deepseek-debates"
author:
  - "[[DYLAN PATEL]]"
  - "[[AJ]]"
  - "[[DOUG]]"
  - "[[REYK KNUHTSEN]]"
published: 2026-02-05
created: 2026-07-10
description: "H100 Pricing Soaring, Subsidized Inference Pricing, Export Controls, MLA"
tags:
  - "clippings"
---
## The DeepSeek Narrative Takes the World by Storm

DeepSeek took the world by storm. For the last week, DeepSeek has been the only topic that anyone in the world wants to talk about. As it currently stands, DeepSeek daily traffic is now much higher than Claude, Perplexity, and even Gemini.

But to close watchers of the space, this is not exactly “new” news. [We](https://x.com/dylan522p/status/1819431961368129554) [have](https://semianalysis.com/2024/05/07/openai-is-doomed-et-tu-microsoft/) [been](https://x.com/dylan522p/status/1828316816273195452) [talking](https://x.com/dylan522p/status/1875594509339521414) [about](https://x.com/dylan522p/status/1859302712803807696) DeepSeek for months (each link is an example). The company is not new, but the obsessive hype is. SemiAnalysis has long maintained that DeepSeek is extremely talented and the broader public in the United States has not cared. When the world finally paid attention, it did so in an obsessive hype that doesn’t reflect reality.

We want to highlight that the narrative has flipped from last month, when scaling laws were broken, [we dispelled this myth](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/), now algorithmic improvement is too fast and this too is somehow bad for Nvidia and GPUs.

The narrative now is that DeepSeek is so efficient that we don't need more compute, and everything has now massive overcapacity because of the model changes. While Jevons paradox too is overhyped, Jevons is closer to reality, the models have already induced demand with tangible effects to H100 and H200 pricing.

## DeepSeek and High-Flyer

High-Flyer is a Chinese Hedge fund and early adopters for using AI in their trading algorithms. They realized early the potential of AI in areas outside of finance as well as the critical insight of scaling. They have been continuously increasing their supply of GPUs as a result. After experimentation with models with clusters of thousands of GPUs, High Flyer made an investment in 10,000 A100 GPUs in 2021 _before any export restrictions._ That paid off. As High-Flyer improved, they realized that it was time to spin off “DeepSeek” in May 2023 with the goal of pursuing further AI capabilities with more focus. High-Flyer self funded the company as outside investors had little interest in AI at the time, with the lack of a business model being the main concern. High-Flyer and DeepSeek today often share resources, both human and computational.

DeepSeek now has grown into a serious, concerted effort and are by no means a “side project” as many in the media claim.  We are confident that their GPU investments account for more than $500M US dollars, even after considering export controls.

[![](https://substackcdn.com/image/fetch/$s_!rMUO!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F39cab87f-3291-4eb9-9355-c1b1eb696e79_975x368.png)](https://substackcdn.com/image/fetch/$s_!rMUO!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F39cab87f-3291-4eb9-9355-c1b1eb696e79_975x368.png)Source: SemiAnalysis, Lennart Heim

## The GPU Situation

We believe they have access to around 50,000 _Hopper GPUs_ , which is not the same as 50,000 H100, as some have claimed. There are different variations of the H100 that Nvidia made in compliance to different regulations (H800, H20), with only the H20 being currently available to Chinese model providers today. Note that H800s have the same computational power as H100s, but lower network bandwidth.

We believe DeepSeek has access to around 10,000 of these H800s and about 10,000 H100s. Furthermore they have orders for many more H20's, with Nvidia having produced over 1 million of the China specific GPU in the last 9 months. These GPUs are shared between High-Flyer and DeepSeek and geographically distributed to an extent. They are used for trading, inference, training, and research. For more specific detailed analysis, please refer to our [Accelerator Model](https://semianalysis.com/accelerator-industry-model/).

[![](https://substackcdn.com/image/fetch/$s_!yfHm!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F055c28ff-9ad9-422a-a8b5-61cbfa326e68_2196x872.png)](https://substackcdn.com/image/fetch/$s_!yfHm!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F055c28ff-9ad9-422a-a8b5-61cbfa326e68_2196x872.png)Source: SemiAnalysis

Our analysis shows that the total server CapEx for DeepSeek is ~$1.6B, with a considerable cost of $944M associated with operating such clusters. Similarly, all AI Labs and Hyperscalers have many more GPUs for various tasks including research and training then they they commit to an individual training run due to centralization of resources being a challenge. X.AI is unique as an AI lab with all their GPUs in 1 location.

DeepSeek has sourced talent exclusively from China, with no regard to previous credentials, placing a heavy focus on capability and curiosity. DeepSeek regularly runs recruitment events at top universities like PKU and Zhejiang, where many of the staff graduated from. Roles are not necessarily pre-defined and hires are [given flexibility](https://www.chinatalk.media/p/deepseek-ceo-interview-with-chinas), with jobs ads even boasting of access to 10,000s GPUs with no usage limitations. They are extremely competitive, and allegedly offer salaries of over $1.3 million dollars USD for promising candidates, well over the competing big Chinese tech companies and AI labs like Moonshot. They have ~150 employees, but are growing rapidly.

As history shows, a small well-funded and focused startup can often push the boundaries of what’s possible. DeepSeek lacks the bureaucracy of places like Google, and since they are self funded can move quickly on ideas. However, like Google, DeepSeek (for the most part) runs their own datacenters, without relying on an external party or provider. This opens up further ground for experimentation, allowing them to make innovations across the stack.

We believe they are the single best “open weights" lab today, beating out Meta’s Llama effort, Mistral, and others.

## DeepSeek’s Cost and Performance

DeepSeek’s price and efficiencies caused the frenzy this week, with the main headline being the “$6M” dollar figure training cost of DeepSeek V3. This is wrong. This akin to pointing to a specific part of a bill of materials for a product and attributing it as the entire cost. The pre-training cost is a very narrow portion of the total cost.

## Training Cost

We believe the pre-training number is nowhere the actual amount spent on the model. We are confident their hardware spend is well higher than $500M over the company history. To develop new architecture innovations, during the model development, there is a considerable spend on testing new ideas, new architecture ideas, and ablations. Multi-Head Latent Attention, a key innovation of DeepSeek, took [several months](https://www.chinatalk.media/p/deepseek-ceo-interview-with-chinas) to develop and cost a whole team of manhours and GPU hours.

The $6M cost in the paper is attributed to just the GPU cost of the pre-training run, which is only a portion of the total cost of the model. Excluded are important pieces of the puzzle like R&D and TCO of the hardware itself. For reference, Claude 3.5 Sonnet cost $10s of millions to train, and if that was the total cost Anthropic needed, then they would not raise billions from Google and tens of billions from Amazon. It's because they have to experiment, come up with new architectures, gather and clean data, pay employees, and much more.

So how was DeepSeek able to have such a large cluster? The lag in export controls is the key, and will be discussed in the export section below.

## Closing the Gap - V3’s Performance

V3 is no doubt an impressive model, but it is worth highlighting _impressive relative to what_. Many have compared V3 to GPT-4o and highlight how V3 beats the performance of 4o. That is true but GPT-4o was released in _May of 2024_. AI moves quickly and May of 2024 is another lifetime ago in algorithmic improvements. Further we are not surprised to see less compute to achieve comparable or stronger capabilities after a given amount of time. Inference cost collapsing is a hallmark of AI improvement.

[![](https://substackcdn.com/image/fetch/$s_!w9PC!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F907678eb-2886-499e-ad43-36c9fd9be879_975x459.png)](https://substackcdn.com/image/fetch/$s_!w9PC!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F907678eb-2886-499e-ad43-36c9fd9be879_975x459.png)Source: SemiAnalysis

An example is small models that can be run on laptops have comparable performance to GPT-3, which required a supercomputer to train and multiple GPUs to inference. Put differently, algorithmic improvements allow for a smaller amount of compute to train and inference models of the same capability, and this pattern plays out over and over again. This time the world took notice because it was from a lab _in China_. But smaller models getting better is not new.

[![](https://substackcdn.com/image/fetch/$s_!IXuJ!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb39c0193-339c-4e63-bb1d-55504b1e5d6e_975x554.png)](https://substackcdn.com/image/fetch/$s_!IXuJ!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fb39c0193-339c-4e63-bb1d-55504b1e5d6e_975x554.png)Source: SemiAnalysis, Artificialanalysis.ai

So far what we've witnessed with this pattern is that AI labs spend more in absolute dollars to get _even more_ intelligence for their buck. Estimates put algorithmic progress at [4x per year](https://epoch.ai/blog/algorithmic-progress-in-language-models), meaning that for every passing year, 4x less compute is needed to achieve the same capability. Dario, CEO of Anthropic argues that algorithmic advancements are even faster and can yield a [10x improvement](https://darioamodei.com/on-deepseek-and-export-controls). As far as inference pricing goes for GPT-3 quality, costs have fallen 1200x.

When investigating the cost for GPT-4, we see a similar decrease in cost, although earlier in the curve. While the decreased difference in cost across time can be explained by no longer holding the capability constant like the graph above. In this case, we see algorithmic improvements and optimizations creating a 10x decrease in cost and increase in capability.

[![](https://substackcdn.com/image/fetch/$s_!cyiw!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2c3a6b7a-93dd-4f6c-9367-b3a93146913b_1024x610.png)](https://substackcdn.com/image/fetch/$s_!cyiw!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F2c3a6b7a-93dd-4f6c-9367-b3a93146913b_1024x610.png)Source: SemiAnalysis, OpenAI, Together.ai

To be clear DeepSeek is unique in that they achieved this level of cost and capabilities first. They are unique in having released open weights, but prior Mistral and Llama models have done this in the past too. DeepSeek has achieved this level of cost but by the end of the year do not be shocked if costs fall another 5x.

## Is R1’s Performance Up to Par with o1?

On the other hand, R1 is able to achieve results comparable to o1, and o1 was only announced in September. How has DeepSeek been able to catch up so fast?

The answer is that reasoning is a new paradigm with faster iteration speeds and lower hanging fruit with meaningful gains for smaller amounts of compute than the previous paradigm. As outlined in our [scaling laws report](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/), the previous paradigm depended on pre-training, and that is becoming both more expensive and difficult to achieve robust gains with.

The new paradigm, focused on reasoning capabilities through synthetic data generation and RL in post-training on an existing model, allows for quicker gains with a lower price. The lower barrier to entry combined with the easy optimization meant that DeepSeek was able to replicate o1 methods quicker than usual. As players figure out how to scale more in this new paradigm, we expect the time gap between matching capabilities to increase.

Note that the R1 paper makes _no mention_ of the compute used. This is not an accident – a significant amount of compute is needed to generate synthetic data for post-training R1. This is not to mention RL. R1 is a very good model, we are not disputing this, and catching up to the reasoning edge this quickly is objectively impressive. The fact that DeepSeek is Chinese and caught up with less resources makes it doubly impressive.

But some of the benchmarks R1 mention are also _misleading._ Comparing R1 to o1 is tricky, because R1 specifically doesn't mention benchmarks that they are not leading in. And while R1 matches in reasoning performance, it's not a clear winner in every metric and in many cases it is worse than o1.

[![](https://substackcdn.com/image/fetch/$s_!ymND!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28789d0f-8d48-491b-af3d-2012619f5736_1020x354.png)](https://substackcdn.com/image/fetch/$s_!ymND!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F28789d0f-8d48-491b-af3d-2012619f5736_1020x354.png)Source: [(Yet) another tale of Rise and Fall: DeepSeek R1](https://x.com/JJitsev/status/1883158738661691878)

And we have not mentioned o3 yet. o3 has significantly higher capabilities than both R1 or o1. In fact, OpenAI recently shared o3’s results, and the benchmark scaling is vertical. "Deep learning has hit a wall", but of a different kind.

[![](https://substackcdn.com/image/fetch/$s_!K8M3!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91731feb-d9fd-438b-8931-447b6cf70a60_975x635.png)](https://substackcdn.com/image/fetch/$s_!K8M3!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F91731feb-d9fd-438b-8931-447b6cf70a60_975x635.png)Source: AI Action Summit

## Google’s Reasoning Model is as Good as R1

While there is a frenzy of hype for R1, a $2.5T US company released a reasoning model a month before for cheaper: Google’s Gemini Flash 2.0 Thinking. This model is available for use, and is considerably _cheaper than R1_ , even with a much larger context length for the model through API.

On reported benchmarks, Flash 2.0 Thinking beats R1, though benchmarks do not tell the whole story. Google only released 3 benchmarks so it's an incomplete picture. Still, we think Google’s model is robust, standing up to R1 in many ways while receiving none of the hype. This could be because of Google’s lackluster go to market strategy and poor user experience, but also R1 is a Chinese surprise. 

[![](https://substackcdn.com/image/fetch/$s_!DBth!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feaf6e4b3-1b75-4e21-a157-52c29add65ac_1017x1024.jpeg)](https://substackcdn.com/image/fetch/$s_!DBth!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Feaf6e4b3-1b75-4e21-a157-52c29add65ac_1017x1024.jpeg)

To be clear, none of this detracts from DeepSeek’s remarkable achievements. DeepSeek’s structure as a fast moving, well-funded, smart and focused startup is why it's beating giants like _Meta_ in releasing a reasoning model, and that's commendable.

## Technical Achievements

DeepSeek has cracked the code and unlocked innovations that leading labs have not yet been able to achieve. We expect that any published DeepSeek improvement will be copied by Western labs almost immediately.  

What are these improvements? Most of the architectural achievements specifically relate to V3, which is the base model for R1 as well. Let’s detail these innovations.

## Training (Pre and Post)

DeepSeek V3 utilizes Multi-Token Prediction (MTP) at a scale not seen before, and these are added attention modules which predict the next few tokens as opposed to a singular token. This improves model performance during training and can be discarded during inference. This is an example of an algorithmic innovation that enabled improved performance with lower compute.   

There are added considerations like doing FP8 accuracy in training, but leading US labs have been doing FP8 training for some time.

DeepSeek v3 is also a mixture of experts model, which is one large model comprised of many other smaller experts that specialize in different things, an emergent behavior. One struggle MoE models have faced has been how to determine which token goes to which sub-model, or “expert”. DeepSeek implemented a “gating network” that routed tokens to the right expert in a balanced way that did not detract from model performance. This means that routing is very efficient, and only a few parameters are changed during training per token relative to the overall size of the model. This adds to the training efficiency and to the low cost of inference.

Despite concerns that Mixture-of-Experts (MoE) efficiency gains might reduce investment, [Dario points](https://darioamodei.com/on-deepseek-and-export-controls) out that the economic benefits of more capable AI models are so substantial that any cost savings are quickly reinvested into building even larger models. Rather than decreasing overall investment, MoE's improved efficiency will accelerate AI scaling efforts. The companies are laser focused on scaling models to more compute and making them more efficient algorithmically.

In terms of R1, it benefited immensely from having a robust base model (v3). This is partially because of the Reinforcement Learning (RL). There were two focuses in RL: formatting (to ensure it provides a coherent output) and helpfulness and harmlessness (to ensure the model is useful). Reasoning capabilities emerged during the fine-tuning of the model on a synthetic dataset. This, **[as mentioned in our scaling laws article](https://semianalysis.com/2024/12/11/scaling-laws-o1-pro-architecture-reasoning-training-infrastructure-orion-and-claude-3-5-opus-failures/) , **is what happened with o1. Note that in the R1 paper no compute is mentioned, and this is because mentioning how much compute was used would show that they have more GPUs than their narrative suggests. RL at this scale requires a considerable amount of compute, especially to generate synthetic data.

Additionally a portion of the data DeepSeek used seems to be data from OpenAI’s models, and we believe that will have ramifications on policy on distilling from outputs. This is already illegal in the terms of service, but going forward a new trend might be a form of KYC (Know Your Customer) to stop distillation.

And speaking of distillation, perhaps the most interesting part of the R1 paper was being able to turn non-reasoning smaller models into reasoning ones via fine tuning them with outputs from a reasoning model. The dataset curation contained a total of 800k samples, and now anyone can use R1’s CoT outputs to make a dataset of their own and make reasoning models with the help of those outputs. We might see more smaller models showcase reasoning capabilities, bolstering performance of [small models](https://importai.substack.com/p/import-ai-397-deepseek-means-ai-proliferation).

## Multi-head Latent Attention (MLA)

MLA is a key innovation responsible for a significant reduction in the inference price for DeepSeek. The reason is MLA reduces the amount of KV Cache required per query by about _93.3%_ versus standard attention. KV Cache is a memory mechanism in transformer models that stores data representing the context of the conversation, reducing unnecessary computation.

As discussed in our scaling laws article, KV Cache grows as the context of a conversation grows, and creates considerable memory constraints. Drastically decreasing the amount of KV Cache required per query decreases the amount of hardware needed per query, which decreases the cost. However we think DeepSeek is providing inference at cost to gain market share, and not actually making any money. Google Gemini Flash 2 Thinking remains cheaper, and Google is unlikely to be offering that at cost. MLA specifically caught the eyes of many leading US labs. MLA was released in DeepSeek V2, released in May 2024. DeepSeek has also enjoyed more efficiencies for inference workloads with the H20, due to higher memory bandwidth and capacity compared to the H100. They have also announced partnerships with Huawei but very little has been done with Ascend compute so far.

We believe the most interesting implications is specifically on margins, and what that means for the entire ecosystem. Below we have a view of the future pricing structure of the entire AI industry, and we detail why we think DeepSeek is subsidizing price, as well as why we see early signs that Jevons paradox is carrying the day. We comment on the implications on export controls, how the CCP might react with added DeepSeek domninance, and more.

## Broader Implications on Margins

There is a critical observation here when it comes to margins. R1 is not a true undermining of o1’s technical progress, but rather a matching of capabilities at a much lower price. This inherently makes sense, and we want to now introduce a framework for how pricing could and should work in the future.

Pushing capabilities leads to superior margins. This analogy closely matches a very accelerated version of semiconductor fabrication. When TSMC is the first to a new node (new capability) they get meaningful pricing power because they are creating a product that didn’t exist before.

The rest of the lagging competitors (Samsung, Intel) price below the leader’s capability in order achieve parity in price to performance. Luckily for chipmakers (in this analogy AI labs) they can shift their capacity. If they can get much better price to performance on newer models, they can shift capacity to serve the newest models. Older models continue to get supported, but on smaller amounts of supply. This closely mirrors realized behavior in AI labs today and the law of the land for semiconductor fabrication.

## Commoditization of Capabilities, Endless Pursuit of Stronger

This is probably how the world of capabilities will work out. Pushing to the newest tier of capabilities will lead to meaningful pricing premium, while others who match that capability quickly will have modest profits. The lagging edge of capabilities continue to exist if they can be reserved for specific use cases. Those who can catch up to leading edge capabilities will be fewer each generation.

What we just witnessed is that R1 go to the leading edge of capabilities and priced it at 0 margins. This jarring pricing difference opens up the question – why is OpenAI so expensive? And that’s because they were pricing at the SOTA frontier and enjoyed frontier capability premiums.

What we think will happen is an even faster version of leading edge fab dynamics. Rushing to the newest capability means continued pricing power (see ChatGPT Pro) and lagging capabilities means much lower pricing that mostly accrues to the infrastructure that serves the tokens.

Given we are in a very quick technological cycle, we will see very quick product cadence to pursue this leading edge of capability. As long as you expand capability to drive new features which can create value on top of these features, then you deserve pricing power. If not – commoditization is the open model market just a generation behind.

We think that there’s a fundamental misunderstanding of what is happening given this context. What we described to you was a parallel for a hyperdrive version of chip manufacturing as an analogy, the _most capital intensive industry_ known to man. Not a single industry spends more on R&D in the world, and yet the closest realized parallel means this is somehow bad for the chips that support the model companies.

And when comparing AI tokens to Jevons paradox, there is deep historical analogy. In the beginning it wasn’t clear you could scale transistors smaller and smaller, and when it did become clear, the entire industry focused on scaling CMOS to the smallest possible dimension and built meaningful functions on top. We are in the early stages of putting together multiple CoT models and capabilities together. We are scaling models like we initially scaled transistors, and while that is likely to be a very hectic period in terms of technological progress, this is good for Nvidia.

## DeepSeek Subsidized Inference Margins

The reality is the market was looking for a reason and they chose this one. DeepSeek might be that cheap if they choose to have 0% or negative margins, but clearly the price elastic point of serving cutting edge tokens is much higher. DeepSeek has an incentive to do so given they are raising money for a new round.

DeepSeek just blew up OpenAI’s leadership margins at the critical insertion point of reasoning. Will this leadership last? We don't believe so – rather an open lab showed the capabilities of a closed lab. And while critically important, **we still note that DeepSeek is a fast follower**.

[![](https://substackcdn.com/image/fetch/$s_!U-G5!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8c87bf57-49d1-427c-99cf-07888d787059_975x675.png)](https://substackcdn.com/image/fetch/$s_!U-G5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F8c87bf57-49d1-427c-99cf-07888d787059_975x675.png)Source: SemiAnalysis

We do think that a stronger open lab (which DeepSeek is now the best) is very good for the Neoclouds and service providers. Compute concentration is still important, open or closed, but if the layer built on top gives away their products for free than the possibility of increasing the dollar of your compute increases. More total dollars go to compute rather than closed model providers which means the spend flows more to hardware than anything else. Software businesses also benefit from this hugely.

## H100 Pricing Soaring - Jevon's Paradox in Action

And we are getting early indications of this thesis. With AWS GPU pricing for H100 up across many regions since the release of V3 and R1. H200 similarly are more difficult to find.

[![](https://substackcdn.com/image/fetch/$s_!VStA!,w_1456,c_limit,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48177ead-e7e4-41ff-b365-635618ba24ff_1024x635.webp)](https://substackcdn.com/image/fetch/$s_!VStA!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F48177ead-e7e4-41ff-b365-635618ba24ff_1024x635.webp)

Source: SemiAnalysis

H100 prices exploded after the introduction of V3, as GPUs are starting to be monetized at much higher rates. More intelligence for cheaper means more demand. This is a meaningful shift to sluggish H100 spot pricing in previous months.

## Export Control Implications, DeepSeek, and The CCP

There’s another lens to think about the DeepSeek versus Western lab capability context, and that’s the lens of geopolitics. [Dario of Anthropic](https://darioamodei.com/on-deepseek-and-export-controls) is heavily supporting export controls, and we think that the East versus West debate especially in AI Models will continue. Some context is that [AI Diffusion controls](https://semianalysis.com/2025/01/15/2025-ai-diffusion-export-controls-microsoft-regulatory-capture-oracle-tears/) already are set in place and we do not think that they will be lifted.

Narratives have been flying around that the Export Controls failed because of DeepSeek’s progress, but this misunderstands how the exports worked. Initially, the H100 was banned and the H800 was allowed, which was computationally similar (but bandwidth limited). Then, the H800 was banned and now only the H20 is permissible. [We discussed a huge cancellation of H20 orders in January from Nvidia in our Accelerator Model despite huge demand, which likely preceds an upcoming US ban](https://semianalysis.com/accelerator-industry-model/).

Between the passage of these laws are grace periods and during which, it is likely DS stockpiled on orders for the chips they used. However, note that H100 have been banned since release. In that sense, the export controls came short of fully restricting capable chips. The export controls are not about cutting off China entirely, but about severely restricting the overall ecosystem. This means restricting on the order of hundreds of thousands to millions of chips, not necessarily tens of thousands.

However, we are expecting that the H20 will be banned in the future, further limiting the ability for DeepSeek to get chips.

And they want chips.

## DeepSeek Capacity Limitations

DeepSeek has struggled to serve the huge increase in demand. Despite having one of the best inference stacks in the world, doing research to identify architectural developments and training a model is a different challenge than serving tens of millions of users on a reliable basis. Signups for DeepSeek have been closed on and off, with R1 exhibiting extremely slow responses when they do go through (though it is masked well with the clever UX).

The models we see this month exhibit a lag based off the results of previous export controls, and with more time, it will be harder and harder to scale both models and serving capabilities. Scaling is needed, and China knows it too.

The Bank of China has announced a USD$140B (1 Trillion Yuan) subsidy over the next 5 years for the AI Industry Chain, 1 day after meeting the CEO and founder of DeepSeek. The goal of this subsidy is explicitly to empower China to be completely self-reliant in science and technology, including basic research as well as industrial applications and development. There are specific focus areas around AI and robotics, biotechnology, and new materials. Some additional support includes computing infrastructure and datacenters, insurance and risk management aid for first generation technical equipment as well.

We think in the future we will see the effects of export controls play out more: algorithms will progress and hardware will progress, US labs will have access to such innovations and thus be able to scale to a point where China will not be able to get to. We may still see the effect of China producing models that match US lab’s, but it will continue to be a follower.

We also think it’s plausible that DeepSeek does not continue to open source models in the long term, especially as the CCP gains more direct interest in the work and aims to protect algorithmic innovations.
