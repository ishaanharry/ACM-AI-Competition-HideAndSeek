This is the bot I made to compete in ACM@UCSD's first AI Competition.  The challenge is presented [here](https://ai.acmucsd.com/).  It is a game of ~~Hide and Seek~~ Cops vs. Citizens where seekers have to find and tag all the hiders and the hiders have to not get tagged within the given time frame.  A bot that is entered in the competition may either be the seeker team or the hider team in any given match.  "kits_pystarter/bot.py" is the main program for the bot.


## Expected behavior of my bot

###### Seeker
My seeker has two different methods of searching the map until a hider comes into range:
1. If the obstacle density of the map is less than 0.35, each seeker randomly moves in straight lines.  When it hits an obstacle or wall, it chooses a new direction and continues moving in a straight line (in my code I called this function "chooseAntDirection" because this is roughly how a colony of ants explore a new area to find food).
2. If the obstacle density is higher than that, the seekers navigate to the nearest wall and begin moving along the wall counter-clockwise around the map.

Once a hider comes into range of the seekers, each seeker employs a greedy algorithm to move towards one of the hiders.

###### Hider
When the match starts, my hiders navigate to the nearest wall and follow the wall counter-clockwise around the map.  Once they find a nook in which they are surrounded by obstacles on at least 6 sides, it stays where it is and hopes that seekers won't see it.


## Improvements
Well the competition ended and I didn't have enough time to implement everything that I was thinking about implementing.  After all, I am taking MMW this summer (and doing other things) so the time I had to work on the competition was limited.  Here are some of the improvements that I could have made if I had more time:

###### Seeker
I definitely didn't spend enough time on the seeker, seeing as a well-coded seeker is more likely to win than a well-coded hider.  When I initally programmed the Seeker to chase after Hiders once they got in view, I used a simple greedy algorithm thinking I might implement A-star or something later on but I never got to it.  That was the first thing I could've improved.  Another thing is that each unit, regardless of whether or not the enemy units are in range, has a field that tells the distance it is to the nearest enemy unit.  I didn't make use of this, but it would have been useful for hiders to navigate closer to the seekers rather than just attempting to sweep the map.  Finally (after the competition ended), a fellow competitor showed me a [Python pathfinding library](https://pypi.org/project/pathfinding/) that already has an implementation of A-star and a number of other pathfinding algorithms.  If I had taken a few minutes on Google I might have found this site and implemented A-star from the beginning.  It would've been faster to code and it would probably work better than if I tried to implement it myself.  This was kind of a bruh moment. :trollface:

###### Hider
As I said before, ~~the Hider is less likely to win~~ the Citizens have no chance against the highly militarized poice force, so spending as much time as I did coding the Hider was probably not super benficial.  I would still try to improve the Hider though.  One thing that I started trying to do (a day or two before the deadline to submit) was to make the hiders move away from the seekers if they got too close.  If you look in the code, I have written an "antiGreedy" method that I never use.  It was meant for this purpose.  Additionally, my check to determine if a hider was sufficiently surrounded by obstacles is very basic.  It only looks at adjacent tiles and is not smart enough to know if there is a very clear exposed line of sight.  A more complex implementation would check if the hider is "boxed in" by following the unit's lines of sight in all directions.  I haven't thought about how I could implement this but I'm sure it can be done.


## Final thoughts
This was a pretty fun competition, even though I didn't win :cry:.  It was certainly better than the MMW that I still have to do.  (I think) I learned a thing or two about pathfinding algorithms, and I gave it my best shot.  I'll be on the lookout for more of these competitions in the future.

:trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface::trollface:
