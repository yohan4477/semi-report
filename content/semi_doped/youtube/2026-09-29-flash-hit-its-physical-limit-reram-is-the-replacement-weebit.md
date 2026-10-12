---
source: https://www.youtube.com/watch?v=3444zi04g98
vid: 3444zi04g98
title: Flash Hit Its Physical Limit. ReRAM Is the Replacement: WeeBit Nano's Ilan Sever
date: 2026-09-29
duration_sec: 3413
channel: Semi Doped
kind: transcript
---
There is a memory in almost every chip
that nobody talks about and it holds a
few kilobytes to a few megabytes. It has
no like spot price or a super cycle but
without it most chips analog especially
can't work or even meet the specs on its
data sheet. So for 30 years that memory
has been embedded flash but as we get to
smaller technology nodes it really stops
working. So today's guest designed
embedded flash and then spent the rest
of his career on what comes after it.
Hey, welcome to another episode of
Semi-oped podcast. I am Vic Shaker, the
founder of Semiexponent, where I do
boutique research on semiconductors and
AI infrastructure. I also write Vick's
newsletter on Substack, one of the top
20 technology newsletters on the
platform covering AI and semis. I come
from two decades of working in the
semiconductor industry and my work now
is taking that engineering background
and explaining what matters in the
technology and why it matters to the
markets. Check out Vick's newsletter on
Substack and uh for technology research
reach out to me at semi-exponent. And
our guest today is uh Elan Se chief
memory architect at Weebit Nano. He has
spent over 30 years in non-volletile
memory semiconductor IP and SOC design.
He was previously group CTO at Dolphin
Design, director of IP and libraries at
Tower Semi and design manager of flash
memory at SD Micro Electronics. Elan,
welcome to the podcast.
&gt;&gt; Happy to be here, Vick.
&gt;&gt; Awesome. So uh I guess one of the things
that we don't often talk about uh is uh
what exactly are nonvolatile memories
because when I mentioned flash memory
that's there pretty much everywhere but
it is so ubiquitous that people have
even you know stopped thinking about it
in the mainstream. It is assumed to be
there but it's still a very important
part of all of our electronics. uh and
it's not just like DRAM and SRAMM that's
the whole problem right so you've worked
on this stuff before so let me start by
u going through your journey uh what
what made you get started on working on
flash memory
&gt;&gt; yes thanks P so yes nonvolatile
[clears throat]
memory is basically fundamental element
of any electronic system it's where you
store your software code and your
parameters and anything that you would
like to stay even when the power goes
away. So um we all have systems in which
the battery can run out or we turn shut
it down but when we power it back up
everything goes back to life. So where
is this stored? Uh all this information
is stored in nonvolatile memory meaning
a memory that doesn't need the power in
order to retain the data. So uh you
mentioned flash memory in the technology
of choice uh even today in what we call
N storage like your uh phone storage is
um is what we call n flesh I'm not
talking about this technology we are now
referring to technologies which are
embedded within system on chips on
silicon
and this was previously
um served with um embedded flesh which
is a n type flesh.
Basically flesh technology is storing
charge on some floating gates. So there
is some um
capacitors which is charged and it
remains there even if you shut uh the
power down and that's how flesh works.
As you mentioned flesh doesn't scale
well. So in geometries below 28 or 22
nanometer
flesh reached its uh physical limit
actually. So physically you cannot
implement embedded flesh anymore and the
industry had been looking for
alternative technologies for few decades
now and um we will talk today about one
of these technologies that is now
gaining really market and acceptance
which is resistive run.
&gt;&gt; Awesome that's a great introduction. Uh
so for people listening we always talk
about static RAM SRAMM uh which you know
holds the state but it holds information
without having to be refreshed. However,
if you turn off the power to that uh
SRAMM, uh you're going to lose
everything in the SRAM. Like you switch
off your computer, you know, your OS is
removed from the SRAM and all of that
stuff, right? Um so on dynamic RAM, I
think it's more like you have to keep
refreshing it. Uh but of course, you
take power out that goes out too.
nonvolatile memory that you know Elan
that you were mentioning is that it it's
the stuff that stays all the time you
know on and it even if you turn off your
phone it holds information and that's
very important because you your your
devices just can't forget stuff all the
time. So we'll definitely get to why
Elash stopped scaling as we went to
smaller nodes and what resistive RAM
means. But I just want to like step back
just a little bit and say like exactly
what is the role of nonvolatile memory
in a device could it could be an
embedded uh device in or a sensor or a
power controller or an automotive chip
whatever it is like what is the role of
uh this nonvolatile memory? What does it
actually hold?
Yeah, that's a very good question, Vic.
So fundamentally I would say uh the the
base usage or the most wide usage is for
any embedded MCU or um
microprocessor
it has it it software and and if you
want to have a really embedded whether
it's an IoT device a medical device your
hearing aid or or whatever device that
needs to be compact, low power, fully
embedded uh without additional uh
external chips. You would like to have
your code inside the same system on
chip. uh you have an MCU whether it's
you know uh one of uh any MCU
architecture it would need to run some
firmware which is software
&gt;&gt; like a microcontroller right like MCU is
a microcontroller unit and it has to
have it has to run some code the
question is where does it get this code
from
&gt;&gt; so of course if you want the code to be
there even when someone is replacing
batteries or maybe the battery uh is out
or even applications that don't have um
power all the time. You know there are
applications today which do energy
harvesting and they just get energy from
uh ambient uh sources and they are not
always connected to any power source. So
in any of these cases you want the
software stored. So the the main usage
or the first usage I would say is to
store your software but then in addition
just think about sensors. So you have
some IoT device or medical device. It is
logging maybe the temperature maybe your
heart beat maybe some ambient data from
some sensors and you want to to have a
logging of this data. So think about a
sensor. It's logging what happened and
maybe after a while it is transmitting
um the information to some system
whether it's an industrial sensor,
medical sensor any type of these
devices. So they always need in addition
to the code storage that we discussed
before also some data logging storage.
Moreover,
most of these systems, these mix signal
embedded system, they have also some
analog parts. And for the analog parts,
uh usually you would need to have some
kind of trimming. So these are a kind of
a normally one-time programmed data that
you do upon production to just put all
the analog values in place. So you use
trimming.
&gt;&gt; That's another usage for nonvolatile
memory. So you just want to to kind of
burn these this data into the chip so it
returns throughout the lifetime of the
chip. And last but not least uh on
security applications there is always
storage of some secret key. So
encryption keys um uh are normally
stored on some kind of nonvolatile
memory on uh security applications.
Awesome. Yeah, that's a good that's a
great introduction because I think what
what most people don't realize is take
the example of the analog part you
mentioned. You know, my own background
is in analog semiconductors. So it's
like it's amazing that you know when
you're making a billion of these little
analog sensors or any analog you know
power supply unit or a or a power
distribution chip or whatever it is uh
you know as you manufacture a billion of
them right what you're saying is like
not all of them are going to come out
the same no way because there is process
variation and if you say that this thing
has to output like 1 volt it's going to
output 1.02 02 the next chip will
output.99.
You know this is not usable because you
let's say you want to power a GPU with
this power controller chip. It can't be
putting out these random variables of
voltages. And so the trimming aspect is
just a an electronic knob that is inside
the chip that when you can write in
something like a code like hey adjust
the voltage by 0.02 02 volts down and
know you can write you know code that in
in a one-time fashion and then center
everything like the alternative in the
digital world is you have to kind of
keep binning chips like Intel will take
oh these are the fastest chips I'll sell
them as i9 these are the slowest chips
I'll sell them as i5 you know but in the
analog world they don't do that they
just they just trim and calibrate things
so that they all work the same so this
is like a very unspoken part of the
analog world which is extremely
important
Yes, this is correct and this is again
one of the use cases. In this case, we
are talking about a very small amount of
data that needs to re retained
throughout the lifetime and it also is
programmed only once or maybe very few
times. So when we discuss nonvolatile
memory, it's important to state one very
important term which is what we call
endurance or programming cycles.
&gt;&gt; So for example, if you program a
software, then yes, you would need to
change it, right? The software versions
people do even what is called photo
firmware update over the air today. So
your system can update code uh even in
the field or over the air. Uh so all
this requires reprogramming of of the
data unlike this streaming data or what
we just mentioned that is more like
production data that you stored once. In
any case or any type of nonvolatile
memory is able to reprogram data
uh not as many times as you can write to
SRAMM or DM uh which are the volatile
technologies that you mentioned that
obviously you can
&gt;&gt; uh read and write to them almost
infinitely.
&gt;&gt; Exactly. Okay. This is great because
you're setting this nonvolatile memory
to be a kind of memory that you mostly
write one time or a few times and read
many many times uh in its lifetime.
&gt;&gt; Um yes. So any type of nonvolatile
memory will need to be reprogrammed. And
one of um the parameters that we look at
when we uh look at NVM technology is the
number of cycles, the endurance of this
memory. So some technologies can only
work up to 10k 10,000 uh reprogramming
cycles. advanced and nonvolatile memory
is expected to already allow in the
order of 100k 100,000 to a million
reprogramming cycles and this means it's
a very uh good technology that allows
a wide usage for many types of
applications.
&gt;&gt; Awesome. That's helpful to know because
we will obviously talk about like
endurance and reprogrammability when we
actually talk about what resistive RAM
is. One other important point that you
mentioned I think we should touch on is
the capacity of this thing. When you
talk about you mentioned NAND in the
beginning you can you have you can store
terabytes on NAND flash and in DAM you
can store gigabytes in SRAM you can
store hundreds of megabytes. So what is
the range of nonvolatile memory in terms
of storage capacity? The capacity of the
nonvolatile memory depends on the
application obviously. So we mentioned
embedded MCUs having some firmware. This
is normally counted in kilobytes but I
would say um tens hundreds of kilobytes
to single megabytes. Uh so maybe um one
two or 4 mgabytes is a large uh NVM
capacity for embedded MCU
maybe maybe uh 4 megabytes. So um so
we're talking about singledigit megabits
right like 1 8 maybe 16 megabits 32
megabits uh for code storage of course
all the other use cases like uh data
logging or trimming that I mentioned
&gt;&gt; are much smaller we're talking about
kilobytes
now in in more advanced MCUs so maybe um
some um
in in lower geometries where people
embed
nonvolatile memory with high performance
microprocessors
uh for any type of applications
automotive industrial it can reach to um
I would say ranges of 16 32 megabytes
but we are definitely still not in the
gigabit or gigabyte
terrain that that is implemented in
other type of
technologies like the ones you mentioned
DRAM or N flesh.
Yeah. So that's that's also very
important to understand about these
nonvolatile memories because you want to
essentially let's say reprogram them
over the air. uh what you're actually
reprogramming is only a few megabits
bytes or a few kilobits kilobytes. And
when you drive your Tesla into your
driveway and it wirelessly connects and
updates its firmware, this is where it
is actually stored. It is stored in a
nonvolatile memory probably on the
larger capacity side than you would have
in a little sensor. I would assume an
automotive
NVME
uh nonvolatile memory NVM with like
embedded flash or whatever is like a
larger capacity than a sensor which
would or you for the trimming uh
applications it's going to be really
small because you only need to correct
for like you know put in a code that's
it. So it has to store very little
amount of memory compared to what um you
know an automotive application would use
but it's definitely not in the gigabits
gigabytes range and all that right so
that's that's the that's the whole thing
here so typically we've used e flash for
doing this um and
now it seems like el has hit some kind
of a limitation as we go to smaller
nodes uh what what exactly is e flash
and why does it it not scale to lower
technology nodes say below 22
nanometers?
&gt;&gt; That's a good uh question. So embedded
flesh um basically flash memory uh is
storing some charge
um in an insulated floating gate. So
it's like a transistor in which the the
gate has some charge stored or a
floating gate and it changes the
conductance or the threshold of the
transistor. That's the way the data is
stored. So you can have charge stored on
that floating gate or uh taken away and
it [clears throat] changes the behavior
of the transistor. Now the amount of
charge that you store there uh when the
technology scales to low geometries like
uh 28 nanometer 22 and I'm not even
talking about a singledigit nanometer
technologies that are available today.
The the the dimensions of this
transistor and the dimension of this
so-called floating gate are so tiny and
the amount of charge that is stored
there is just moving physically to
almost single electrons.
You know a very small amount of charge
and this is just a physical limit. So um
and of course holding this charge over
there without any leakage without the
charge going away by all kinds of
physical mechanisms is becoming really
impossible in the smallest geometries
and that's why flesh cannot scale to
these smaller geometries.
&gt;&gt; Okay. Yeah. Yeah. That's very helpful.
Actually I wanted to compare this to
what uh like for example DM looks like
you know a modern DM actually uses the
equivalent of let's say a 10 nanometer
transistor but the trans the charge that
is stored is never stored within the the
transistor itself because there is a
capacitor on top of the DM that actually
stores the charge and the whole problem
of DM and capacity and DM density is how
to get as much capacity by digging a
deep trench in the in the silicon and
connecting a transistor to it and how to
maximize that capacitance uh without
having to rely on the transistor to hold
that charge. But what you're saying is
like in the in the flash world the
transistor has to hold a charge and then
you make the transistor so small that uh
you you can hold basically you know a
few electrons of charge in it and that's
about it because it's so small it
physically stops scaling you you need to
hold more charge than that for which you
need larger transistors period. Um and
that's why flash does not scale beyond
22 nanometers. So there's no flash
memory in finfet transistors or below.
&gt;&gt; Yeah, this is a very good point because
you mentioned all kinds of vertical
capacitors and um trench into the
silicon the tardana in in discrete DM
chips. When we are uh talking about the
embedded world, it's very important to
note that the whole idea of embedding a
system on chip with memories and with
analog is that you would like to keep a
plain SIMOS technology that allows to
integrate on the same uh chip with the
same uh basic technology features. You
would like to have analog
components. You would like to have
digital components. You would like to
have SRAMM because there was will always
be SRAMM and you would like to have an
NVM. But you will never invest a a
special trench capacitor or you will
never invest a lot of um special
technology
uh because it be will make the whole
system on chip too expensive. So another
key parameter that we look when
selecting a nonvolatile technology
I mentioned before endurance and the
performance of the memory is h how much
does it interfere how much does it add
on top of the baseline simos technology
in the end of the day uh semiconductors
is very cost sensitive so uh it doesn't
seem seems like that but just imagine
uh how much um is the selling price for
such an embedded MCU. If one would need
to add too many processing uh layers
which eventually translate to money and
to time of manufacturing the silicon
wafer that will make the whole system on
chip too expensive. Imagine there is a
large system on chip that has everything
I mentioned digital analog and it has
one NVM component one NVM code storage.
If you add more uh layers of processing
special uh structures
you pay this additional cost over the
whole area of the chip which is making
the whole system on chip more expensive.
So a key parameter in adding any
technology is how many masks we count
basically in semiconductor processing we
count masks.
So how many mask does the technology add
on top of the plain SIMOS
uh you know plain vanilla technology and
that's another key element because in
the end of the day this means how much
are you paying premium for having a
system on chip with embedded NVM so when
you mention for example in in nan flash
that's a totally tech different
technology with you know 3D integration
and many levels and when you mentioned
for example discrete DM with the trench
capacitors there are these are expensive
technologies but they are optimized for
a single use case which is an NF flash
chip or a DM chip in embedded you need
to have a plain vanilla technology with
the minimum additional layers to support
all the type of memories that you
Yes. Okay. It's very important
because you're saying that look the the
cost of these microcontroller chips that
require these uh nonvolatile memories is
already very low. Now, if you want to
add like a whole lot of masks into the
semiconductor process just because you
have to implement this nonvolatile
technology, it better be very
inexpensive because otherwise you can't
have the the whole bill of materials for
the chip go up just because you want to
add NVM materials inside. So,
nonvolatile memories should come with as
few masks as possible. So with that
being said, how many masks does a
typical uh NVM embedded flash process
add? Yes. So important to to mention. So
embedded flash adds another I would say
polysilicon layer, a floating gate layer
on top of the transistor. In some cases
there is a split gate technologies.
There all kind of flavors of that but
they add a lot of processing and this
processing is done in what we call the
front end of life. So in the transistor
very close to the silicon substrate
where you actually implement your
transistor.
And for making that we are talking about
in the range of 10 additional masks
maybe eight to 10 additional masks just
to process these additional features
required for embedded flesh.
Okay, that's uh what percentage of the
total mask count would you think that is
a typical CMOS process has would you say
like 70 80 masks uh even less I mean
typical SIMOS will have even less masks
and uh so yeah this can add 25 30%
add-on and it can become very
significant in the cost
&gt;&gt; that's a problem that's that's what
we're actually trying to solve here and
uh when you're trying to go to smaller
transistor nodes anyway, you can't store
enough charge and you can't add so many
layers. If you have to add 30% more
layers, uh that's not a cost optimal
feature. So I think this is a good time
to get into we've set the stage exactly
as to what is nonvolatile memory, why is
it used, where is it used, what are its
features, um and what what is required
from a nonvolatile memory in terms of
cost, simplicity of implementation,
capacity and everything. So I think we
have set the foundation of nonvolatile
memory and where it lies. I think the
next interesting step is to go into what
we bit nano actually does which is
resistive RAM. like this is a nice time
to get into what that is and how it
solves many of these problems that we
just talked about.
&gt;&gt; So indeed resistive RAM is a technology
that uh is aiming at replacing embedded
flesh. Um it has uh several key benefits
related to our previous discussion.
First of all
um it is very low cost. It is adding
just two additional masks uh to the
technology.
Um it is embedded only in the what we
call the back end of line. So we
actually build the structures between
the meta layers above way above uh the
silicon substrate and transistors. Now
why is this important?
uh we mentioned before um all kind of
mix signal chips, analog chips that
require some nonvolatile memory.
These technologies have passed through a
lot of optimizations of their unique
analog characteristics.
For example, some technologies have BCD
transistors which are high voltage
transistors.
uh and when you invested so much in an
alert technology to have the the perfect
analog properties and for power
management and other type of
applications.
If you had to now embed what we call a
front end ofline technology, a
technology that sits at the transistor
level, it would interfere with the other
analog transistor that you spend years
optimizing.
So another key importance of a
technology um that you would like to add
on top of an existing let's say analog
or mix signal platform
is that putting it in the back end of
line means it is totally decoupled from
the transistors.
So you are not impacting the transistor
behavior and you are not impacting any
analog characteristics because the
memory uh processing is done actually
after way after you finished processing
all your SIMOS technology. It is
actually done in the top layers uh top
rooting layers uh meta layers above uh
the the silicon. One second. I just
wanted to that is a very that's a very
interesting point that you mentioned
here. Uh that's because I think people
need to understand where resistive RAM
sits inside the stack of a silicon chip.
What you were saying is that back end of
line means that it is sitting like very
way on top of the chip where if you
think the transistors are way below the
substrate is way below this is all the
way on the top. So it's actually
processed almost very much at the end of
the chip processing. And so it's very
decoupled from what is happening in the
transistor world downstairs. Uh and so
you also mentioned BCD technology. So
for those who have not heard of this, it
stands for bicos, cos and demos. Uh and
this is a specific technology that is
good for high voltage transistors. It's
used a lot in automotive you know
applications uh because it can withstand
a lot of voltage like tens of volts. So
these transistors are unique to what
they do like they are used in like power
conversion circuits and things like
that. Uh you you don't want to go and
put a a storage and nonvolatile memory
storage technology that messes with the
transistor structure.
So that would make the whole BCD
transistor which is so well optimized
for power performance or like whatever
that is supposed to do at high voltage
performance is going to mess up because
the nonvolatile memory is like
interfering with that. So the best place
to put it is like really far away and
process it really after all the silicon
is done at the back end of line right on
top of the chip. Right? So that is what
uh resistive RAM does with just one or
two added masks which makes it very
inexpensive. That's that's a right on.
So what is resistive RAM? So basically
as opposed to flash that we said is
storing charge resistive RAM the type of
resistive RAM that we bit nano is doing
uh which is called oxm. So oxygen
vacancy based resistive RAM is actually
implementing
a resistive element
which you can change between uh two
states a low resistive state and a high
resistive state by applying a voltage.
[snorts]
H so I will try to explain it with this
demo that we have here. Let's see if it
works.
&gt;&gt; Yeah. Uh if you're listening to this,
this is a time good time to switch to
YouTube because Elan has like a a nice
3D model of a uh the internal structure
of a resistive RAM cell. And I'm just
describing what I'm looking at here with
changes between its low resistance and
high resistance states. Resistive RAM is
actually a resistor that can switch
between two states, a high resistive
state and a low resistive state. What we
do, we take an insulating layer like a
capacitor that has a very high
resistance and by applying electrical
voltage and current we actually create
these oxygen vacancies
uh that are that you can see here that
are actually forming this filament that
is a conduct conductive filament. So
with oxygen vacancies charge can go
through and this is becoming conductive.
Uh conductive mean lower resistance. So
when the memory has this filament built
the resistance is low and we are storing
the value of one. Then by applying
voltage in the opposite direction what
we can do is actually dissolve this
filament. So in this side in the high
resistive state we dissolve the filament
it goes back to an insulating layer that
has a high resistance. So a current can
not longer go through or the resistance
is high. So we have these two states
either the filament is created and we
are in the low resistive state or the
filament is dissolved and we are in the
high resistive state.
So these two states we then read them
with some uh sense amplifier which is a
typical uh circuit that is used to read
any type of memory uh whether it's flash
dram
uh so we can actually sense whether the
filament is there and then we read a one
or the filament is dissolved and we read
a zero. So that's basically the way
resistive RAM is programmed by applying
voltage that will create the filament or
voltage in the opposite direction that
will dissolve it and it is read by
reading or sensing the resistance
whether it's a high resistance or a low
resistance. Okay, this is fascinating.
Usually these are not the kind of
devices that we see inside a typical
CMOS technology process. So what I what
I find fascinating about this is that
clearly you can't use any kind of a
dialectric material that creates oxygen
vacancies right there's like ser there
should be something that is different
now I know we bit nano would probably
have its proprietary materials but would
you be able to broadly explain
uh what what is the property that causes
these oxygen vacancies uh what kind of
materials do this and how is it
compatible with the CMOS process flow?
&gt;&gt; Yeah. So we'll not dive into the whole
physics of resistive RAM. Uh but
basically um I mentioned that we have an
insulating layer. Uh but on top of
bottom of it and there are two
electrodes.
So there is a bottom electrode that is
built from some kind of inert material.
And there is a top electrode that is
built from what we call a scavenging
layer. So the scavenging layer is the
layer that can actually uh kind of store
oxygen or give it back.
&gt;&gt; Mhm. So according to the uh electrical
field this governing layer either will
take away oxy oxygen from uh the the
electric material or will um give back
oxygen
uh to it. So by applying the electrical
fields in opposite directions, we can
either have oxygen vacancies inserted
into the the material or oxygen going
away and creating vacancies. All the
opposite
uh contribute back um oxygen
to um dissolve the vacancies.
&gt;&gt; Awesome. Okay, that's that's unique like
so this pro this material is actually uh
compatible with CMOS uh foundaries.
&gt;&gt; So maybe the most important and
overwhelming property of resistive RAM
is that to generate it we at webit nano
use only fab friendly material.
So we use materials
that are available in any SIMOS
technology.
We don't use any rare earth material. Uh
we don't use any expensive and we don't
use any contaminating
materials. So some technology that maybe
we'll not discuss in this podcast like
magnetic RAM and ferro electric RAM.
These are competing technologies that
are also nonvolatile.
&gt;&gt; But to actually manufacture them, you
would need um several
uh rare contaminating and expensive
materials that are uh not available in
normal production lines. And in many
cases
to just be able to process with these
materials, you need totally separate
rooms, separate chambers, separate
machines to make sure you do you don't
have any contamination of these
materials. So in the resistive ram um
here at Weebit, we use only fab friendly
materials, very basic materials that you
would know. Of course, I cannot
&gt;&gt; uh tell you the secret. source of course
of the we bit technology in this podcast
for decades now this technology was
developed um so we is over a decade now
and even before that um our technology
partner CA Leti in France had been
developed this technologies for
many years before together with our
partners we reach this technology
that is as I said not using any
contaminating
materials and is performing with the
best-in-class NVM
performance and features. Yeah, that's
that's resistive RAM itself is like not
an idea that is like new, right? Uh you
mentioned we bit nano has been doing
this for 10 years. Um but why why now
what is what has changed now about
resistive RAM that we should you know
people have been trying this since
Panasonic
uh have have tried it, Samsung has tried
it. Uh what's what's the need now? Why
what has changed? So I think it's a it's
a combination of many elements. One is
what we mentioned before that you know
flesh is hitting the physical limit and
cost is you know uh we know that the
cost pressure and semiconductor is
always growing. There is the more law
and there is you know a lot of pressure
to reduce cost. Moreover, I think one of
the
driving application driving is a good
word here is automotive. You mentioned
it before.
So uh we at Weebit um were able to
demonstrate that this technology is not
only low cost and has a very good
performance
but it can actually serve h this very
challenging market of automotive. So we
all know that in our cars today
everything is electronic. there are you
know hundreds of chips and um many of
them require nonvolatile today
resistive ramp technology can serve the
automotive market and I think it's a
major breakthrough
so it's nice uh you mentioned that the
competitors to this technology are MR
RAM magneettoresistive RAM and
ferroelectric RAM both of which are
alternative material s and not really
well suited to be integrated into a a
cos fab. So those are those those are
like technologies are ruled out but then
there's an also I think another
alternative technology called like phase
change memory which you know alters the
its physical crystal structure with
voltages. Uh so like this is a resistive
RAM is an other application where
automotive is driving uh a lot of uh
requirement here especially as we go to
smaller technology nodes where flash
stops working resistive RAM is really
well suited to automotive and so has
this technology been qualified already
for automotive cuz I know that uh
there's a standard called the AECQ 100
which is like a very hard automotive
standard to pass. Does Weebit Nano
already pass this uh standard?
&gt;&gt; Yes. Uh so indeed
our technology is now qualified for ACQ
100 automotive
and uh we are continuing this
with
additional customers. So we recently
announced
two um I would say um leading uh IDMs
that are both active in the automotive
space uh that license our technologies
for automotive platforms. So the way
that um this resistive RAM technology
works from we bit nano is that you guys
have the secret recipe uh that explains
how resistive RAM can be made in a fab
and a fab would license it from you. Is
that how this whole thing works?
Yes.
But that's where when you ask me why
resistive RAM is now becoming um
available,
it's because it's not all about the
secret sauce. So the secret sauce for
sure it was developed throughout decades
and we have now
all the recipe for the the exact
dialectric structure and the exact
electrodes that are needed to to you
know do the scavenging of the oxygen and
all of that and we really have you know
tens of PhDs in webit working on this
part along with our partners
as I mentioned, but that's not enough.
If you are an embedded,
I would say MCU, let's say a system on
chip architect,
what you need is a full-blown memory
module that you can just commission a a
read command, a write command. That's
it. All the rest is done. You don't work
with the bit cell. you don't work with
physics. You you need to write a a 32 or
64bit word onto the memory and re be
able to read it back when you need it.
And that's where WeIT Nano is today the
only fully um vertically integrated and
fully independent IP provider because
with Weebit we have all the pillars that
are needed to build such a technology.
So yes, you need the bit cell that I
showed and the physics around it and the
secret source, but around it, you need
to build the design and the layout of
the full memory array. You need to
design the the and lay out all the
peripheral circuits like the the
decoders and the drivers and the sense
amplifiers that I mentioned before which
are basically of analog nature that are
able to sense these exact resistances.
Um and for programming the resistive RAM
we need to apply as I mentioned uh
electrical field which is actually
voltages and currents that needs to be
controlled very precisely. So for that
you need a whole
analog design and layout team. And then
on top of it
the programming sequence of resistive
RAM [snorts] is done using a proprietary
smart algorithm.
&gt;&gt; So not only that we did an analog
capabilities,
we also need a very strong algorithm
team. We need a very strong digital
design and verification team. So
basically what I'm telling you is that
the resistive RAM module that our
customer actually embeds into the SOC is
comprised not only of the physical
bitel. It has a lot of analog design,
memory architecture,
layout,
digital design, algorithms
and and even software is developed at
webit in order to have a full offering
of a embedded
resistive RAM uh IP. So yeah, it's much
more it's much more than just making the
physical transistor. Like a user of
resistive RAM would rather just get the
whole black box with all the layouts
inside with all the sense amplifiers and
all the voltage controls wired up, place
it into their design and then you have
the software that controls uh that
aspect of the algorithm. So it's all
it's all done for you approach. It's not
like somebody has to go and place these
uh physical structures in their layout
and struggle with it. So all a user has
to do is like license it, dump it in, go
ahead and do the rest of your chip. So
nothing everything is like handled uh by
Weebit Nano for the customer using this
IP.
&gt;&gt; Yeah, it sounds easy but actually what
is unique at Weebit Nano
&gt;&gt; is that all these teams are sitting
together. So when there is a discussion
of let's say a performance that needs to
be met or automotive let's say meeting
automotive qualification you mentioned
before you know uh it requires very
meeting very high temperature profiles
and high endurance and in order to meet
this you cannot do it by just the bit
cell you cannot do it by just some
analog design you need a fully
multi-isiplinary
approach that
&gt;&gt; takes the best of the device physics and
the process, the best of the analog
design, the best of the digital and the
algorithm and wraps everything together
uh into this uh product and and
that's the main strength of WeIT Nano
and that's the main um the the probably
the only way that you can have any NVM
technology
uh be commercially viable.
It was done before in flash memory. It
is mostly done in other technologies. Uh
but for the resistive RAM today um we
are doing it uh and all these
capabilities
exist inside the team at webit.
So you mentioned endurance was one of
the like the factors that you have to
really design in as well. It's not as
easy as it seems. Uh what in the rough
ranges uh is the endurance of resistive
RAM like what and how does it compared
to like let's say flash memory or any
other alternatives if you have the
numbers off the top of your head. I'm
trying to place like is it more
endurance more endurance or less
endurance or where does it fit?
I would say uh typically um a med flashh
is 10k cycles. It depends of course
there are some technologies that are
more but I would say 10k cycles
typically.
And for our resistive RAM we have some
um products that are 10k. We already
demonstrated and qualified 100k cycles
uh which is opening
the market for additional applications
automotive and others and um we are um
working on extending it be beyond the
the 100k into the million cycles in the
near future.
&gt;&gt; Okay. Awesome. So it's going to be quite
performant in spite of the treacherous
conditions that automotive applications
want from I don't know from driving cars
in Alaska to the Sahara desert uh you
have to support all temperatures and so
it's usually a very challenging
qualification to pass and uh and
especially the life the lifetime of
memory used in automotive is also should
be pretty high. So all of these things
should fit broadly into that umbrella.
Where do you see uh resistive RAM going
next? So what's next? So you know we
already spoke about microcontrollers.
What's the next big thing?
&gt;&gt; Yes, that that's a very good question
Vic. Uh so we all know that uh the next
big thing or the existing big thing is
AI. So um
resistive RAM or I would say in the
academic
um naming is called memory stores that's
kind of how the academy wants to to name
it had been um
studied in
multiple academic researchers
um for what we call inmemory compute or
IMC. Wee bit is also very active in this
field. Probably a good topic that we can
discuss in one of the the next podcasts.
&gt;&gt; Yeah. But the basically the idea is that
resistive RAM a a different type of
resistive RAM array can actually
create AI calculation inside the memory
by just combining
a resistive elements
and um this had been demonstrated in the
academy and commercializing it. I would
say is one of the next big things for
resistivity.
&gt;&gt; Amazing. That's that's would be very
interesting to hear. Analog in-memory
compute has uh been around as a concept
for a long time and as we have like the
AI era coming up and GPUs sucking
like,000 to 2,000 watts per GPU. Uh
maybe the future lies somewhere where we
can do it differently. But that is a big
topic and a topic for another day. All
right. Uh Elan before we wrap up this I
want to hear like what is the one story
of innovation that you faced or came
across while developing this technology
within we nano? That's a good story to
tell for the whole audience.
&gt;&gt; Yeah, I can think about such a story. Um
you know we mentioned analog dreaming
before, right? So
uh embedded system on chip mix chips
will always have some analog but I also
mentioned that we have our own piece of
analog within our memory. So obviously
we need also to trim that part. So we
came up with the idea hey we have
nonvolatile memory and we need to do
trimming. So let's just take you know
some part of the nonvolatile memory just
some additional row store our own um
data owning values there read them and
we can just use it to trim our own
system
and then we when we went to to our lead
customers
h and we explained to them and they
asked us how do you do this and we said
yeah we have our own mechanism that we
use our on nonvolatile memory to trim
our system. They say why uh we want to
use that as well. So can you grant us
access? we would like to trim our own
system and it it just saves us having
additional NVM uh for trimming our
system and today it became a standard
feature in all our models in which we
let uh the end customer get his own um
uh user data uh his own trimming data
and write out out of the NVM
and uh this is done automatically and
became a a lead feature.
&gt;&gt; That's amazing. So the key takeaway I'm
getting from all of this is that it is
important that you solve problems. It
doesn't have to be the customer's
problems. Even if you solve your own
problems that you come up, sometimes you
just have like a new product on your
hands or a new problem you solved for
someone else and you can turn around and
sell your own solution to your problem
to solve someone else's problem. It's
like a perfectly viable business model.
&gt;&gt; I guess that's what you call
engineering, right?
&gt;&gt; Yeah, that's that's amazing. It's a nice
story. Awesome. Thanks, Elan, for coming
on Semi-Doped. Uh it's glad to have you
here. Uh I know we don't often talk
about things like resistive RAM but
that's what semi-doped is for that we
sometimes try to go outside of the
normal narrative of AI semiconductors
memory optics you know we talk about all
this stuff but every once in a while we
like to throw a curveball and have
someone like you explain what resistive
RAM is to us. So thank you for coming on
the podcast.
&gt;&gt; Thank you for having me Vic.
&gt;&gt; All right so that's the end of the
podcast. So, please check us out um on
all the podcast platforms if you haven't
already. Apple really likes it. If you
give us five stars, they push us up the
technology rankings and it's always a
competition as to who gets to the top.
So, if you can go press the like uh star
five star review thing that really help
us out. And as usual, uh check us out um
uh on our daily newsletter which is
daily.
com and my newsletter is on
vixnewsletter.com
and Austin who was not on this episode
but is usually on the podcast with me
also has chipstrap.com. All right, see
you on the next one.
