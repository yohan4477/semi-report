---
source: https://www.youtube.com/watch?v=eSommbPzrIY
vid: eSommbPzrIY
title: PM technical mock interview: explain how APIs work (w/ FinTech PM)
date: 2021-02-03
duration_sec: 369
channel: RocketBlocks
kind: transcript
---
hello everyone kensingtonvestio from the
rocketblocks team here
in this mock interview video we're
sitting down with ava morgenstein who is
a product manager at jpmorgan focused on
payments products
and in this particular mock interview
we're going to sit down and ask her a
common technical question which is what
is an api
and how would you explain it to someone
that doesn't know of the concept
so let's go ahead and it
and let's go ahead and just jump into
the first question which
is focus on apis and basically what i
want to ask you is you know help me
understand
what an api is and what the purpose of
it is
and sort of to the extent possible you
know put yourself in the shoes of like
if you were explaining this concept to
someone who's never heard of it for the
first time like how would you
explain this to them you know think of
like explaining an api to your
grandfather
sure so i'll just start by telling you
what api actually stands for because
that's always a good start
but it stands for an application
programming interface okay
and from a very high level technical
perspective what it does
is it is a standard communication
contract
between two different applications or
different types of software
okay and what that actually means in
practice is that it allows two different
entities to communicate with each other
in a way that's been standardized by
whatever code the api consists of
interesting okay and to get a little bit
more into
kind of what its purpose is and why you
would use one you could use an api to
access data
that's really the most common use of it
so if you are
let's say watching the weather channel
and
the weather channel says it's 75 degrees
and sunny that
piece of information is actually coming
from an api
the weather channel is reaching out to a
data asset that has information about
the current weather and saying what's
the weather right now
that data asset is sending information
back and saying it's 75 degrees and
sunny outside
and that is then what's broadcast to you
on the weather channel so that's a data
access
api another possible use for one
and i'll take a pause there and see if
that makes sense or if i can make that
clearer anyway
yeah it does make sense i guess the
question i have maybe some naive
questions like why
why do you need an api why can't you
just
i don't know why can't you just get it
out of the database directly if you have
that data
yeah absolutely so essentially the
reason that you need an api
is you have to define what you need from
that database that database could
contain hundreds of thousands or
billions of pieces of information in it
and you just want to know what the
weather is right now and if that is
what your use case is for then you want
to write a specific query or a specific
request
or what's actually called in technical
terms a call saying i would like to know
the temperature whether it's sunny or
rainy
and the the date for right now
when the data is right now i want to
know the weather and i want to know
if it's raining if it's sunny if it's
windy etc
and that ensures that you get the exact
pieces of information you're looking for
whereas there's no way to really
communicate with the database otherwise
because there's so much information in
it that you just can't specify
got it okay and do i need to communicate
in like a very specific way
or can i just sort of ask for whatever
information i
i need how does that work so where the
the communication contract aspect of an
api comes in
is that you are essentially saying i
need exactly this piece of information
in exactly this format
and you're sending that on to the entity
that's going to return it to you so the
entity can get it
receive it reach out in itself for what
it needs for you and then send it back
got it okay and when you say something
like okay the
entity will receive it they'll they'll
find that information and send it back
like
how does that information get back to
the other entity the other sort of
you know application that made the call
as you called it
sure so that's essentially what the api
exists for they send back a message
that contains the pieces of information
that the original request had so they're
essentially sending back the original
request also with the information in it
got it okay cool um and then i think
before i
asked a few additional questions you
said you had maybe another example you
were going to share
yeah absolutely so that was a data
access use case for an api
but another possible example of an api's
use
or purpose would be something to hide
complexity
so in many cases we have applications
that operate on other applications
and a really good example of this is
your iphone so perhaps i want to open
like a photo editing application on my
iphone because i want to edit a photo
and i want to take a photo right now in
order to edit it
so in order for me to open
my camera app through that application
and take a photo
in the application it needs to access
the actual code that is written to open
the camera app on my iphone
okay in order to do that without an api
what would have to happen
is if that's 5 000 lines of code that
apple has created to allow you to open
the camera function
then that photo editing application will
have to take those 5 000 lines of code
and essentially use that to open the
camera icon
on your iphone but that's not a very
efficient process
so instead what it does is it writes an
api to say
iphone can you open this camera and
essentially
by doing that they streamline the entire
process
that they need for their application by
containing the complexity of the actual
code to open a camera
with an api got it okay so it's it's
like you said like a way to mask
all of those details and not have in
this case like an individual developer
try and
you know reinvent the wheel because
apple has sort of already
invented the wheel and made it available
exactly
got it okay cool um that sounds great
awesome
you
