+++
date = '2025-11-29T20:58:52+02:00'
draft = false
title = 'Beleaf Csaw19 Ctf'
+++
# Beleaf CSAW 19 ctf
## category : crackmes/RE
## difficulty : beginners
## url to challenge : https://github.com/osirislab/CSAW-CTF-2019-Quals/tree/master/rev/beleaf 
### how i solved it : 


We begin with a basic executable we try to run it and see it asks for a code of somekind,
i tried entering several inputs but to no avail , we need to dig deeper , 
using bininja i located the main function we can see that it performs some kind of a check for the right input
![mainfunc](/study-blog/images/csawbeleaf-1.png)

some constraints we see are that our input must be at least 0x20 and that it checks with some encoding function
that performs some kind of actions lets dig in and find something interesting,
![indexfunc](/study-blog/images/csawbeleaf-2.png)

this function appears to be finding the index of something inside the data array, 
inside the main function we see the following : 
![encodefunc](/study-blog/images/csawbeleaf-3.png)

if the comparison is wrong, it puts out incorrect therefore it must be true, a comparison between the input string encoded by the function and a certain array-like structure that jumps 8 bytes lets see what it must be equal to,
![memfunc](/study-blog/images/csawbeleaf-4.png)
so , 1 - 9 - 11 - 27... you get the idea , how do we do that ?

inside the encoding function we see that we recieve some kind of an index so.. in other words we have to match an index that gets returned from the encoding function to the tagert array, first number we need is 1 so index 1 needs to be returned from the index array which as we see here
![idkfunc](/study-blog/images/csawbeleaf-5.png)
the first letter we need is 'f' since the target array requests 1 so our encoding function needs to return 1 which is the index where 'f' is.
we continute and get flag...
you do the rest !
good luck and thank you for reading this.
