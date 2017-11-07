# Optimal-Path-Orienteering

In the sport of orienteering, you are given a map with terrain information, elevation contours, and a set or sequence of 
locations to visit ("controls"). There is a combination of athletic skills and planning skills required to succeed - a smarter 
competitor who can figure out the best way to get from point to point may beat out a more athletic competitor who makes poor 
choices! In this project, I have developed a program that uses A* search algorithm to determine the optimal path that goes 
through all the controls.

In an ordinary orienteering event, the map you get will be quite detailed. Different background colors show the type of 
terrain, while buildings, boulders, man-made objects and other notable features are shown with different symbols. For this 
project, I have used two separate inputs, both representing Mendon Ponds Park: a text representation of the 
elevations within an area (500 lines of 400 double values, each representing an elevation in meters) and a 395x500 simplified 
color-only terrain map (color legend below). The last five values on each line of the elevation file can be ignored. Also, 
the real-world pixel size is determined by that of the National Elevation Dataset, which in our area is one third of an 
arc-second, equivalent to 10.29 m in longitude (X) and 7.55 m in latitude (Y).

As for the points a player will need to go visit, those will come in a simple text file, two integers per line, representing 
the (x,y) pixel (origin at upper left) in the terrain map containing the location. In the classic event type that we are 
considering, the sequence of points must be visited in the order given. One such classic event was the World Deaf Orienteering 
Championships, held in Mendon Ponds Park.

## Planning and implementation

So, the player has to get to some controls. However, going in a straight line, even if possible, is often not advisable. First 
of all, the player will be able to proceed at different speeds through different terrains. Rather than telling how fast, 
the algorithm needs to decide based on some representative photos how fast the player can travel through these terrains. The 
different types of terrains and their representation on the map is described in the table present in the file "terrainTypes.jpg".

In addition, you will probably go slower uphill, and even slower up steeper hills. As you may have noticed, the landscape 
changes significantly throughout the year. This can have a big impact on orienteering, as the map itself indicates a sort of 
default terrain, but may have been made at a different time of year than the competition. (For example, this past spring, a 
local meet was held in which some "open land" and "slow run forest" was in fact six inches or more underwater.) So, for this 
part of the project, the algorithm will need to adapt the search process as follows:

**Summer**: The photos above were taken during summer, so we can assume the map and photos to be accurate for this season.

**Fall**: In the fall, leaves fall. In the park, what happens is that paths through the woods can become covered and hard to 
follow. So, for fall, the algorithm should increase the time for any paths through (that is, adjacent to) easy movement forest 
(but only those paths).

**Winter**: In winter, the waters can freeze. For this particular assignment, we will assume that any water within seven pixels
of non-water is safe to walk on.

**Spring**: aka "mud season". Any pixels within fifteen pixels of water that can be reached from a water pixel without gaining 
more than one meter of elevation (total) are now underwater. (Note that the water pixels represent different ponds and are 
therefore at different heights.)

The algorithm considers different speeds for different terrains based on the season. Initially, the algorithm reads the image
file that represents the map and creates a 2D array that represents this map based on the type of the season. For all the controls
(points that have to be visited), A* search algorithm is invoked on every pair of consecutive controls. The optimal path
through all the controls is determined after the A* is completed for all the pairs of consecutive controls.

## Running the program
Run the python program present in the file titled "aStar.py". The program then asks for a type of season, enter one of the seasons
and provide the name of the file that contains the controls. The program then generates a file titled "path.png" which contains
an image of the map with the optimal path highlighted.
