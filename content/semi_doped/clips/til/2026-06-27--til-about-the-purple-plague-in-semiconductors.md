---
source: https://daily.semidoped.com/p/til-about-the-purple-plague-in-semiconductors
title: TIL: About the Purple Plague in Semiconductors
date: 2026-06-27
kind: clipping
genre: til
audience: everyone
subtitle: 
---
Some of the integrated circuits being built to fly to the moon were quietly dying inside their own packages, and the failure had a color.

When engineers in the early 1960s cracked open the sealed chips and looked through a microscope, the tiny wires inside had not stayed silver and gold. The contact points had turned a deep, sickly violet. The industry called it the “purple plague,” and for a few years it was one of the most feared failures in electronics.

[](https://substackcdn.com/image/fetch/$s_!42X6!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F053b0f9b-5cdb-4e5e-99e2-3237c1bf55a2_500x300.svg)By Bondkontakt_Gold-Aluminium.svg: Cepheidenderivative work: Shoecream (talk) - Bondkontakt_Gold-Aluminium.svg, Public Domain, https://commons.wikimedia.org/w/index.php?curid=11036701

The setup looked innocent. To wire up a chip you bonded a hair-thin gold wire onto an aluminum pad on the silicon. On the bench the joints were perfect, the signals crisp, the chips passing every test. Then they ran hot - in a missile, in a spacecraft, in any sealed box that warmed up in use - and something quiet and molecular went wrong. Gold and aluminum are bad roommates. Heat them together and they diffuse into one another, forming a family of brittle gold-aluminum compounds. One of them, gold aluminide (AuAl2), happens to be a vivid purple. That purple was what engineers saw when they opened a dead chip, so the purple got the name, and the blame.

Here is the part the name gets wrong. The purple compound was mostly a bystander. AuAl2 is so stable that jewelers still sell it as “purple gold,” and it turns up in bonds that stay perfectly strong. This is because gold diffuses into the aluminum faster than the aluminum moves back, the reaction leaves rows of microscopic empty pockets along the joint — a hollowing-out called [Kirkendall voiding](https://en.wikipedia.org/wiki/Kirkendall_effect). Leftover manufacturing contaminants like fluorine and chlorine made it worse, drilling their own voids into the interface. The bond slowly turned into a purple honeycomb, and the first real vibration — a truck ride, a test firing — snapped it. The color was just the witness standing over the body.

Thanks for reading! This post is public so feel free to share it. Learn a new thing every Saturday!

[Share](https://daily.semidoped.com/p/til-about-the-purple-plague-in-semiconductors?utm_source=substack&utm_medium=email&utm_content=share&action=share)

The timing could not have been worse, because the plague hit the two most important chip projects in the country at once. The [Apollo Guidance Computer](https://en.wikipedia.org/wiki/Apollo_Guidance_Computer), the machine meant to steer astronauts to the moon, ran entirely on early Fairchild integrated circuits; its lead hardware designer, Eldon Hall, later counted the purple plague among the team’s major problems, a metal that turned brittle and cracked. At the same time the Air Force’s Minuteman II missile was being built around custom Texas Instruments chips. A single snapped wire meant a dead guidance computer, whether it was bound for the Sea of Tranquility or sitting in a silo in North Dakota.

[](https://substackcdn.com/image/fetch/$s_!3XXM!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2F24e225e9-b802-428b-bf2a-c9f13a4bd18a_788x784.png)Minuteman II Missile IC. Photo Credit: https://www.computerhistory.org/collections/catalog/102711695/

So the industry treated metallurgy with the same fear it had reserved for physics. Engineers deliberately baked wafers in hot ovens to force the reaction and find the weak joints early. They screened by the lot, and if one chip failed, the whole batch was thrown out. They scrubbed contamination out of their fabrication lines, and they redesigned the joint itself, doping the gold wire, switching to aluminum-on-aluminum, or slipping a barrier metal between the two so gold and aluminum never touched.

It is a strange thing to find at the foundation of the digital age: not a theory, not a transistor, but two common metals that could not be trusted to sit quietly together in the dark. And the most notorious villain in early chip history turned out to be named after a color that was mostly just standing at the scene.

Thanks for reading! Subscribe for free to receive new posts and support our work.

Subscribe
