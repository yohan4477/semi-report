---
source: https://daily.semidoped.com/p/til-bob-proved-it-was-impossible
title: TIL: Bob Proved It Was Impossible. Two Months Later He Shipped It.
date: 2026-07-11
kind: clipping
genre: til
audience: everyone
subtitle: Bob Widlar, a sheep, and the small accounting insight sitting inside every analog chip you own
---
Walter Widlar of Cleveland was a self-taught radio engineer who worked at the WGAR station and built pioneering ultra-high-frequency transmitters, and he was clearly a man who could not leave anything alone, because when a baby arrived in the house he wired it up. 

Bo Lojek, the historian of semiconductor engineering, records that one of the Widlar boys became the first baby monitored by wireless radio in the 1930s. The child in question was Bob Widlar’s brother, and one has to assume that growing up in that house did something to a person.

It certainly did something to [Robert John Widlar](https://en.wikipedia.org/wiki/Bob_Widlar), who was the sort of engineer that companies hire against their own better judgement, and then spend twenty years telling stories about. 

[](https://substackcdn.com/image/fetch/$s_!79Yt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Facffb33a-405b-41f7-8629-cc545ee90e7c_288x346.jpeg)By Lojek, Bo (2006). History of semiconductor engineering. Springer. ISBN 3540342575. p. 312., Fair use, https://en.wikipedia.org/w/index.php?curid=28213719

There is an unwritten rule in the components trade, and it is the sort of rule that does not need writing down, which is that you do not steal engineers from the people you sell to. You take their money. You take them to lunch. You do not take their best man.

In late 1963, [Fairchild Semiconductor](https://en.wikipedia.org/wiki/Fairchild_Semiconductor) took [Ball Brothers Research](https://en.wikipedia.org/wiki/Ball_Aerospace_%26_Technologies)’s best man. Widlar was in Boulder then, building instruments for NASA, and Ball bought its parts from Fairchild, and a Fairchild salesman called [Jerry Sanders](https://en.wikipedia.org/wiki/Jerry_Sanders_\(businessman\)) (yes, the [AMD](https://en.wikipedia.org/wiki/AMD) one) noticed how good he was. Historians have been very delicate about what followed. Thomas Lee of Stanford calls it a breach of protocol. [Wikipedia](https://en.wikipedia.org/wiki/Bob_Widlar), following Lojek, calls it a breach of professional ethics. Both are polite ways of saying that the supplier walked into the customer’s lab and left with the furniture.

Having gone to all that trouble to acquire him, Fairchild then had to survive the interview. Lojek’s account is that Widlar fortified himself with a few drinks beforehand and informed the head of R&D that what Fairchild was doing with analog circuits was bullshit. They hired him anyway, into a different department, presumably one staffed by people with stronger nerves.

The insult, you will be sorry to hear, was accurate.

Everyone in 1963 designed integrated circuits the way they had always designed circuits, which is to say, you draw the thing you want, then you build the parts. On a chip this is madness. A diffused resistor of any useful value eats up an enormous amount of silicon, and silicon is money, and it is also stray capacitance and dead yield and general grief. A transistor, meanwhile, costs almost nothing. The process makes them by the thousand whether you ask it to or not.

[](https://substackcdn.com/image/fetch/$s_!C9f5!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F90bcfb28-b4a4-41f5-8849-33720b3aedbd_1667x1892.png)By RJ Widlar - US Patent Office patent number 3,320,439, Public Domain, https://commons.wikimedia.org/w/index.php?curid=4290422

So Widlar simply turned the rule around, and wrote it down as a maxim: do not attempt to replicate discrete designs in integrated circuit form. The Widlar current source, which every analog student still meets in a textbook and mostly resents, produces a tiny, very stable current by exploiting the small difference between two base-emitter voltages, rather than by using a resistor the size of a parking lot. 

Meanwhile Gordon Moore, running R&D, had decided the company’s future was digital, because digital was simpler and shipped in volume. Widlar’s view of digital electronics is preserved: _every idiot can count to one._

[](https://substackcdn.com/image/fetch/$s_!nctt!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Ff2f5cd01-3d2a-44a6-b6ce-047783db05a9_1075x1600.webp) Memes with this run amok on Reddit threads.

He then went and proved it. With a process engineer named Dave Talbert, who pushed his experimental wafer lots through the fab in two weeks instead of six, he shipped the µA702 in 1964, the world’s first op-amp on a chip, while Fairchild management looked on with visible indifference. [Jack Gifford](https://en.wikipedia.org/wiki/Jack_Gifford) said the top brass only learned Widlar existed after the market started writing them letters. The 702 was a compromise. The 1965 µA709 was not. [Don Valentine](https://en.wikipedia.org/wiki/Don_Valentine), who was there, later reckoned that at one point Widlar and Talbert between them were responsible for more than eighty percent of the linear circuits made and sold in the world. One designed them; one made them.

Naturally, Fairchild’s founders had no intention of sharing the windfall with the men who created it. So in November 1965 Widlar and Talbert left for [National Semiconductor](https://en.wikipedia.org/wiki/National_Semiconductor), and Widlar declined to fill in his exit interview form, writing across it a single line, capitalised exactly as follows: “I want to be RICH!”

Thanks for reading! We want you to be RICH too, so subscribe for FREE to receive new posts and support our work.

Subscribe

He had earlier told his boss that the only thing that would keep him was one million dollars, tax free, by whatever route Fairchild cared to choose. Fairchild declined. Fairchild then, for reasons nobody has ever satisfactorily explained, kept paying his salary until April 1966. Widlar’s assessment: maybe they did not believe he was actually leaving, and some people are really a little slow.

At National, he became fully himself.

The con he ran on the industry is still told in labs. In the autumn of 1967 the trade magazines were having a proper argument about whether a high-power voltage regulator could be built on a single monolithic chip, letters to the editor, pro and con, the works. [Bob Pease](https://en.wikipedia.org/wiki/Bob_Pease), who worked beside him, tells what happened next: Widlar ended the debate by writing an authoritative-sounding letter explaining that thermal gradients across the die made the thing impossible. Everybody shut up, because obviously Widlar knew what he was talking about. Two months later he introduced the twenty-watt LM109, containing every single feature he had just declared impossible, and stood back to enjoy the view.

The con he ran on his own employer involved livestock. A downturn came, the groundskeeping budget was cut, the lawns grew shaggy, and Widlar drove out to Morgan Hill with his colleague Bob Dobkin and came back with a sheep in the back of his Mercedes convertible. They tied her to a tree outside headquarters, and the photographers took twenty minutes to arrive, which tells you something about news in Santa Clara. The groundskeepers were quietly rehired. 

[](https://substackcdn.com/image/fetch/$s_!4rhD!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fcec216b1-5c22-49aa-9292-bfca96072762_1210x802.png)Pic Credit: EDN from [Paul Rako’s piece on Bob Widlar](https://www.edn.com/bob-widlar-cherry-bombs-the-intercom-speaker/#google_vignette).

Pease says Widlar took the sheep to a bar that evening and left her with the bartender. Lojek says she was mysteriously stolen. The _New York Times_ , in his obituary, said it was a goat, which is the sort of thing that would have delighted him enormously.

He did not stay to invent a third prank. On 21 December 1970, at about half past ten in the morning, three weeks after his thirty-third birthday, he and Talbert resigned. He cashed his options for a million dollars and drove the Mercedes to Puerto Vallarta, and when he crossed the border and truthfully told the guards _I don’t work_ , legend has it that he ran into so much difficulty that he eventually had fake business cards printed, describing himself as a road agent for Morgan Associates. 

[Share](https://daily.semidoped.com/p/til-bob-proved-it-was-impossible?utm_source=substack&utm_medium=email&utm_content=share&action=share)

He kept designing on contract, gave up the drink in his last years, took up running. The obituaries said he died jogging on a beach. Pease corrected them: it was a steep hilly section of Puerto Vallarta, and he was working at it, and he did not die drunk, which may have amazed a number of his colleagues. February 1991. He was fifty-three.

The industry he left behind is now unfathomably large, and it still turns on a small observation made by a twenty-six-year-old who was quite certain that everybody else was doing it wrong. Transistors are cheaper than resistors. Silicon was always cheaper than copper. He noticed first, and then spent the rest of his life being completely insufferable about it, which, on the evidence, he had earned.

This was an extremely fun piece to write. Yet, there are still so many untold stories! Like the one where he cherry bombed the intercom speaker.
