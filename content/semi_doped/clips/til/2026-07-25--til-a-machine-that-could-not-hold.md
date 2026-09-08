---
source: https://daily.semidoped.com/p/til-a-machine-that-could-not-hold
title: TIL: A Machine That Could Not Hold a Thought, and the Man Who Gave It a Longer Memory 
date: 2026-07-25
kind: clipping
genre: til
audience: everyone
subtitle: The story (thus far) of Zhilin Yang.
---
Whether it is Jensen’s leather jacket, or Zhilin Yang’s drumkit on the homepage of his personal website… something there is about a man who is a computer nerd by day and rockstar by night. 

[](https://substackcdn.com/image/fetch/$s_!fvxB!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F4c3b605e-6eee-47b0-9bd1-179e969aefd9_2660x1332.png)

Every language model of the late 2010s was haunted by the same minor calamity: it could read, but it could not hold on. Give it a paragraph long enough and the opening lines wandered off before it reached the end, the way your long-winded uncle loses the plot of his anecdote. Fluent and forgetful at once, they lived inside a narrow present.

Thanks for reading! Subscribe for free to receive new posts and support our work.

Subscribe

In 2019 a graduate student at Carnegie Mellon appointed himself to the problem. [Zhilin Yang](https://en.wikipedia.org/wiki/Yang_Zhilin), born in Shantou in 1992, came to programming with no background at all, and after a single year of training won first prize in the National Olympiad in Informatics, which secured him a place at Tsinghua University. 

[](https://substackcdn.com/image/fetch/$s_!jQxl!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F9a2dd4e2-32c4-4bd6-a6a1-da321b3b34f8_416x416.jpeg)Source: Forbes

At Pittsburgh he put his name to a paper of almost heroic dullness: [Transformer-XL](https://arxiv.org/abs/1901.02860), where the XL, we regret to report, stood for Extra Long. It let a machine hold the thread across far longer stretches, so the beginning of a thought no longer abandoned its end. Months later he was lead author on [XLNet](https://arxiv.org/abs/1906.08237), which strolled past Google’s much-garlanded [BERT](https://en.wikipedia.org/wiki/BERT_\(language_model\)) on twenty tasks, and finished his doctorate in four years.

Then he went home, and here the story acquires a small controversy. One telling is that America’s immigration apparatus shooed a brilliant foreigner out the door. Another one comes from the man best placed to know: his advisor [Ruslan Salakhutdinov](https://en.wikipedia.org/wiki/Ruslan_Salakhutdinov). Once head of AI research at Apple, Salakhutdinov broke a diplomatic silence recently to clear up what he called the confusion. Apple wanted him; when he said he would rather be in China, they offered a desk in Beijing. He turned down the opportunity; he had told Salakhutdinov he would regret it forever if he never tried building something of his own. Startups are not easy for immigrants in the US, so perhaps his hesitation was well-founded.

Trying new things was not a passing mood. As a boy Yang wanted to be a rock star or a wandering poet. He came to Tsinghua for thermal engineering, switched to computer science after a [Haruki Murakami](https://en.wikipedia.org/wiki/Haruki_Murakami) novel, then drummed and wrote songs for a campus band called Splay. Splay was named with an engineer’s idea of a joke - after the [splay tree](https://en.wikipedia.org/wiki/Splay_tree) \- the data structure that keeps whatever you use most within reach. So in 2023, fifty years after [Pink Floyd](https://en.wikipedia.org/wiki/Pink_Floyd) pressed [The Dark Side of the Moon](https://en.wikipedia.org/wiki/The_Dark_Side_of_the_Moon) (his favorite album), he named the company for it, because of course he did! In Chinese, Moonshot AI is the dark side of the moon - 月之暗面. He has said he is in it for the long haul toward general intelligence, not building an app to be sold off and forgotten by Tuesday.

[](https://substackcdn.com/image/fetch/$s_!jZT0!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff4f293dd-a3ef-4159-8fb5-62947254e11b_398x112.png)

Moonshot’s first product — Kimi — arrived in October 2023 with one preposterous boast: it could swallow two hundred thousand Chinese characters at once and misplace not one of them, the longest memory anyone had yet shipped. 

Keeping that promise is the hard part: more context means more key-value cache, which swells with every token until it strains the memory it runs on. Within months he stretched it to two million; the crowds broke the servers, and the company apologized for being wanted too much. Kimi K2 followed in 2025 wearing a trillion parameters, given to whoever fancied it. In July 2026 came Kimi K3: near three trillion parameters, the largest open model yet, built in a country rationed on the very chips it needs. 

Silicon Valley, not easily startled, looked up.

FYI: On July 27, Kimi K3 is slated for open-weight release. 

If you want to read more about context and storage and KV$ and other fun things:

[ChipstratRight Systems for Agentic WorkloadsBack in October, I argued that AI labs and hyperscalers should run a portfolio of inference systems, each tuned to a specific class of work. I called it right-sized AI infrastructure. This week, Sachin Katti used nearly identical language when describing…Read more8 months ago · 13 likes · Austin Lyons](https://www.chipstrat.com/p/right-systems-for-agentic-workloads?utm_source=substack&utm_campaign=post_embed&utm_medium=web&embedding_publication_id=8781267)

[ChipstratThe Agentic Computer: New S-Curve or Another iPad? The client computing industry has been chasing the next big form factor for a long time. The PC and the smartphone were massive markets, but both have scaled their S-curves. The tablet was supposed to be next but never achieved escape velocity. Smartwatches, same story…Read more5 months ago · 18 likes · Austin Lyons](https://www.chipstrat.com/p/the-agentic-computer-new-s-curve?utm_source=substack&utm_campaign=post_embed&utm_medium=web&embedding_publication_id=8781267)

[ChipstratHigh Bandwidth Flash: The Full ReportThere’s been a lot of chatter about High Bandwidth Flash (HBF) recently…Read more2 months ago · 25 likes · Austin Lyons](https://www.chipstrat.com/p/high-bandwidth-flash-the-full-report?utm_source=substack&utm_campaign=post_embed&utm_medium=web&embedding_publication_id=8781267)

[Vik's NewsletterContext Memory Storage Systems, Disruption of Agentic AI Tokenomics, and Memory Pooling Flash vs DRAMSpecial thanks to Val Bercovici, Chief AI Officer, WEKA (LinkedIn, X) for reading draft versions of this post and providing detailed feedback. The quality of the article is much higher as a result. All mistakes are mine…Read more8 months ago · 45 likes · 3 comments · Vikram Sekar](https://www.viksnewsletter.com/p/context-memory-storage-tokenomics?utm_source=substack&utm_campaign=post_embed&utm_medium=web&embedding_publication_id=8781267)

[Vik's NewsletterWhat AI Inference Actually Demands From a NAND SSDEarlier, we have covered NAND as a storage tier, and what its importance is in an AI datacenter. It was a broad post introducing various technologies in use for those not familiar with storage technologies. You can read that below as a precursor to this article…Read more2 months ago · 28 likes · Vikram Sekar](https://www.viksnewsletter.com/p/what-ai-inference-actually-demands?utm_source=substack&utm_campaign=post_embed&utm_medium=web&embedding_publication_id=8781267)

Thanks for reading! Subscribe for free to receive new posts and support our work.

Subscribe
