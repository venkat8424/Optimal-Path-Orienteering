"""
Author: Sai Venkat Kotha, sxk2606@rit.edu

This program implements A* search algorithm to find the best path in the sport
of orienteering.
"""

from PIL import Image
import math

# different types of terrains
terrainTypes = {(248,148,18):"openLand",(255,192,0):"roughMeadow",\
    (255,255,255):"easyMoveForest",(2,208,60):"slowRunForest",(2,136,40):"walkForest"\
        ,(5,73,24):"impassible",(0,0,255):"lake",(100,200,255):"ice",(71,51,3):"pavedRoad"\
            ,(0,0,0):"footpath",(205,0,101):"outOfBounds",(102,51,0):"mud"}

# speed for each terrain for all the seasons
seasonSpeeds = {"summer":{"openLand":2,"roughMeadow":0.25,"easyMoveForest":1.25,"slowRunForest":1,\
    "walkForest":0.75,"impassible":0,"lake":0,"pavedRoad":2,"footpath":2,"outOfBounds":0},\
    "fall":{"openLand":2,"roughMeadow":0.25,"easyMoveForest":0.75,"slowRunForest":1,\
        "walkForest":0.75,"impassible":0,"lake":0,"pavedRoad":2,"footpath":2,"outOfBounds":0},
    "winter":{"openLand":2,"roughMeadow":0.25,"easyMoveForest":1.25,"slowRunForest":1,\
        "walkForest":0.75,"impassible":0,"lake":0,"pavedRoad":2,"footpath":2,"outOfBounds":0,\
        "ice":0.75}, "spring":{"openLand":2,"roughMeadow":0.25,"easyMoveForest":1.25,"slowRunForest":1,\
            "walkForest":0.75,"impassible":0,"lake":0,"pavedRoad":2,"footpath":2,"outOfBounds":0,\
                "mud":0}}

path = []       #list that stores the final path

class Node:
    """
    Each pixel is represented using the Node class.
    x - x coordinate
    y - y coordinate
    type - type of terrain
    elevation - elevation of the pixel
    parent - parent for this pixel
    score - cost + heuristic for this pixel
    """

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.type = None
        self.elevation = None
        self.parent = None
        self.score = float("inf")


def calculateCost(point1, point2, direction,speed):
    """
    This function calculates the cost between two pixels
    """
    if direction == "hor":
        dist = math.sqrt((10.29**2)+(point2.elevation-point1.elevation)**2)
    else:
        dist = math.sqrt((7.55**2)+(point2.elevation-point1.elevation)**2)
    cost = dist/(speed[point1.type] + (point1.elevation-point2.elevation)/40)

    return cost

def calculateHeuristic(point, destination,speed):
    """
    This function calculates the heuristic for a pixel
    """
    return math.sqrt((point.x-destination.x)**2 + (point.y-destination.y)**2 + \
        (point.elevation-destination.elevation)**2)/2

def calculateScore(current,neighbour,destination,speed):
    """
    This function calculates the total score for the pixel.
    """
    if neighbour.x == current.x:
        totalDistance = calculateCost(current,neighbour,"hor",speed)+\
            calculateHeuristic(neighbour,destination,speed)
    else:
        totalDistance = calculateCost(current,neighbour,"ver",speed)+\
            calculateHeuristic(neighbour,destination,speed)
    return totalDistance

def getNeighbours(source,terrain,speed):
    """
    This function returns all the possible neigbours that can be reached from
    the current pixel.
    """
    possibleNeighbours = []
    x = source.x
    y = source.y

    if x == 0 and y == 0:
        if speed[terrain[x][y+1].type] != 0:
            possibleNeighbours.append(terrain[x][y+1])
        if speed[terrain[x+1][y].type] != 0:
            possibleNeighbours.append(terrain[x+1][y])
    elif x == 0 and y == 394:
        if speed[terrain[x][y-1].type] != 0:
            possibleNeighbours.append(terrain[x][y-1])
        if speed[terrain[x+1][y].type] != 0:
            possibleNeighbours.append(terrain[x+1][y])
    elif x == 499 and y == 0:
        if speed[terrain[x][y+1].type] != 0:
            possibleNeighbours.append(terrain[x][y+1])
        if speed[terrain[x-1][y].type] != 0:
            possibleNeighbours.append(terrain[x-1][y])
    elif x == 499 and y == 394:
        if speed[terrain[x][y-1].type] != 0:
            possibleNeighbours.append(terrain[x][y-1])
        if speed[terrain[x-1][y].type] != 0:
            possibleNeighbours.append(terrain[x-1][y])
    elif x == 0 and (y > 0 and y < 394):
        if speed[terrain[x][y-1].type] != 0:
            possibleNeighbours.append(terrain[x][y-1])
        if speed[terrain[x][y+1].type] != 0:
            possibleNeighbours.append(terrain[x][y+1])
        if speed[terrain[x+1][y].type] != 0:
            possibleNeighbours.append(terrain[x+1][y])
    elif x == 499 and (y > 0 and y < 394):
        if speed[terrain[x][y-1].type] != 0:
            possibleNeighbours.append(terrain[x][y-1])
        if speed[terrain[x][y+1].type] != 0:
            possibleNeighbours.append(terrain[x][y+1])
        if speed[terrain[x-1][y].type] != 0:
            possibleNeighbours.append(terrain[x-1][y])
    elif y == 0 and (x > 0  and x < 499):
        if speed[terrain[x+1][y].type] != 0:
            possibleNeighbours.append(terrain[x+1][y])
        if speed[terrain[x][y+1].type] != 0:
            possibleNeighbours.append(terrain[x][y+1])
        if speed[terrain[x-1][y].type] != 0:
            possibleNeighbours.append(terrain[x-1][y])
    elif y == 394 and (x > 0  and x < 499):
        if speed[terrain[x+1][y].type] != 0:
            possibleNeighbours.append(terrain[x+1][y])
        if speed[terrain[x][y-1].type] != 0:
            possibleNeighbours.append(terrain[x][y-1])
        if speed[terrain[x-1][y].type] != 0:
            possibleNeighbours.append(terrain[x-1][y])
    else:
        if speed[terrain[x+1][y].type] != 0:
            possibleNeighbours.append(terrain[x+1][y])
        if speed[terrain[x][y-1].type] != 0:
            possibleNeighbours.append(terrain[x][y-1])
        if speed[terrain[x-1][y].type] != 0:
            possibleNeighbours.append(terrain[x-1][y])
        if speed[terrain[x][y+1].type] != 0:
            possibleNeighbours.append(terrain[x][y+1])

    return possibleNeighbours

def getBestNode(toExplore):
    """
    This function returns the pixel with the lowest total score
    """
    bestNode = None
    minScore = float("inf")
    for node in toExplore:
        if node.score < minScore:
            minScore = node.score
            bestNode = node
    return bestNode

def aStar(source,destination,terrain,speed):
    """
    This function performs the A* search on the input
    """
    if(speed[source.type] == 0):
        print("not a valid source")
        return
    if(speed[destination.type] == 0):
        print("not a valid destination")
        return
    visited = []    # pixels that have been visited
    toExplore = []  # pixels that have to be visited (frontier)
    source.score = 0
    current = source    # current pixel
    toExplore.append(current)
    while len(toExplore) != 0:
        # as long as the frontier is not empty
        current = getBestNode(toExplore)
        if current == destination:
            # if a path is found
            while current.parent:
                # compute the path
                point = []
                point.append(current.x)
                point.append(current.y)
                path.append(point)
                current = current.parent
            point = []
            point.append(current.x)
            point.append(current.y)
            path.append(point)
            return path
        toExplore.remove(current)
        visited.append(current)
        neighbours = getNeighbours(current,terrain,speed)
        for neighbour in neighbours:
            # coputing the scores for each neighbour
            if neighbour not in visited:
                if neighbour in toExplore:
                    # if the neighbour has been seen before
                    score = calculateScore(current,neighbour,destination,speed)
                    if score < neighbour.score:
                        neighbour.score = score
                        neighbour.parent = current
                else:
                    # if the neighbour has not been seen before
                    neighbour.score = calculateScore(current,neighbour,destination,speed)
                    neighbour.parent = current
                    toExplore.append(neighbour)
    print("no path found")

def buildTerrain(terrainArray,elevations,season):
    """
    This function uses the terrain data from image, the elevations data
    and combines both the data into a single data structure
    """
    terrain = []
    for row in range(500):
        line = []
        for col in range(395):
            temp = Node(row,col)
            temp.type = terrainTypes[terrainArray[row][col][:3]]
            temp.elevation = elevations[row][col]
            line.append(temp)
        terrain.append(line)
    return terrain

def buildWinterImage():
    """
    This function build the terrain map for winter
    """
    img = Image.open("terrain.png")
    terrainImage = list(Image.open("terrain.png").getdata())
    terrainArray = []
    cols = 0
    row = []
    for pixel in terrainImage:
        row.append(pixel)
        cols += 1
        if cols == 395:
            cols = 0
            terrainArray.append(row)
            row = []
    for row in range(500):
        for col in range(395):
            # checking if the pixel is in water
            if terrainTypes[terrainArray[row][col][:3]] == "lake" or \
                terrainTypes[terrainArray[row][col][:3]] == "ice":
                edge = False
                # checking if this is the edge of the water body
                if col+1 < 395 and (terrainTypes[terrainArray[row][col+1][:3]] != "lake"\
                    and terrainTypes[terrainArray[row][col+1][:3]] != "ice"):
                    edge = True
                elif col-1 >= 0 and (terrainTypes[terrainArray[row][col-1][:3]] != "lake"\
                    and terrainTypes[terrainArray[row][col-1][:3]] != "ice"):
                    edge = True
                elif row+1 < 500 and (terrainTypes[terrainArray[row+1][col][:3]] != "lake"\
                    and terrainTypes[terrainArray[row+1][col][:3]] != "ice"):
                    edge = True
                elif row-1 >= 0 and (terrainTypes[terrainArray[row-1][col][:3]] != "lake"\
                    and terrainTypes[terrainArray[row-1][col][:3]] != "ice"):
                    edge = True
                if edge:
                    # converting water to ice
                    for i in range(7):
                        if col+i > 394 or (terrainTypes[terrainArray[row][col+i][:3]] != "lake"\
                            and terrainTypes[terrainArray[row][col+i][:3]] != "ice"):
                            break
                        else:
                            img.putpixel((col+i,row),(100,200,255))
                    for i in range(7):
                        if col-i < 0 or (terrainTypes[terrainArray[row][col-i][:3]] != "lake"\
                            and terrainTypes[terrainArray[row][col-i][:3]] != "ice"):
                            break
                        else:
                            img.putpixel((col-i,row),(100,200,255))
                    for i in range(7):
                        if row+i > 499 or (terrainTypes[terrainArray[row+i][col][:3]] != "lake"\
                            and terrainTypes[terrainArray[row+i][col][:3]] != "ice"):
                            break
                        else:
                            img.putpixel((col,row+i),(100,200,255))
                        if row-i < 0 or (terrainTypes[terrainArray[row-i][col][:3]] != "lake"\
                            and terrainTypes[terrainArray[row-i][col][:3]] != "ice"):
                            break
                        else:
                            img.putpixel((col,row-i),(100,200,255))
    return img

def buildSpringImage(elevations):
    """
    This function builds the terrain map for spring
    """
    img = Image.open("terrain.png")
    terrainImage = list(Image.open("terrain.png").getdata())
    terrainArray = []
    cols = 0
    row = []
    for pixel in terrainImage:
        row.append(pixel)
        cols += 1
        if cols == 395:
            cols = 0
            terrainArray.append(row)
            row = []
    for row in range(500):
        for col in range(395):
            # checking if the pixel is in water
            if terrainTypes[terrainArray[row][col][:3]] == "lake":
                # checking if this is the edge of the water body
                edge = False
                if col+1 < 395 and terrainTypes[terrainArray[row][col+1][:3]] != "lake":
                    edge = True
                elif col-1 >= 0 and terrainTypes[terrainArray[row][col-1][:3]] != "lake":
                    edge = True
                elif row+1 < 500 and terrainTypes[terrainArray[row+1][col][:3]] != "lake":
                    edge = True
                elif row-1 >= 0 and terrainTypes[terrainArray[row-1][col][:3]] != "lake":
                    edge = True
                if edge:
                    # converting land to mud
                    for i in range(15):
                        if col+i > 394 or terrainTypes[terrainArray[row][col+i][:3]] == "lake"\
                            or (elevations[row][col+i] - elevations[row][col])>1:
                            break
                        else:
                            img.putpixel((col+i,row),(102,51,0))
                    for i in range(7):
                        if col-i < 0 or terrainTypes[terrainArray[row][col-i][:3]] != "lake"\
                            or (elevations[row][col-i] - elevations[row][col])>1:
                            break
                        else:
                            img.putpixel((col-i,row),(102,51,0))
                    for i in range(7):
                        if row+i > 499 or terrainTypes[terrainArray[row+i][col][:3]] != "lake"\
                            or (elevations[row+i][col] - elevations[row][col])>1:
                            break
                        else:
                            img.putpixel((col,row+i),(102,51,0))
                        if row-i < 0 or terrainTypes[terrainArray[row-i][col][:3]] != "lake"\
                            or (elevations[row-i][col] - elevations[row][col])>1:
                            break
                        else:
                            img.putpixel((col,row-i),(102,51,0))
    return img

def main():
    """
    This is the main program that reads in the data from the user and invokes
    the respective functions
    """
    season = input("enter a season: 'summer','fall','winter','spring'\n")
    speed = seasonSpeeds[season]
    elevations = []
    with open("elevationsFile.txt") as f:
        # reading the elevations data
        for line in f:
            line = line.strip()
            temp = line.split()
            for i in range(len(temp)):
                temp[i] = float(temp[i])
            elevations.append(temp)

    # loading the respective map
    if season == "winter":
        img = buildWinterImage()
    elif season == "spring":
        img = buildSpringImage(elevations)
    else:
        img = Image.open("terrain.png")

    terrainImage = list(img.getdata())
    terrainArray = []
    cols = 0
    row = []
    for pixel in terrainImage:
        row.append(pixel)
        cols += 1
        if cols == 395:
            cols = 0
            terrainArray.append(row)
            row = []

    ipFileName = input("enter the input file with controls\n")
    inputFile = []
    with open(ipFileName) as inp:
        for line in inp:
            point = []
            line = line.strip()
            temp = line.split()
            point.append(int(temp[1]))
            point.append(int(temp[0]))
            inputFile.append(point)

    for i in range(len(inputFile)-1):
        terrain = buildTerrain(terrainArray,elevations,season)
        source = inputFile[i]
        destination = inputFile[i+1]
        aStar(terrain[source[0]][source[1]],terrain[destination[0]][destination[1]],terrain,speed)

    for coord in path:
        img.putpixel((coord[1],coord[0]),(255,0,127))
    img.save("path.png")

main()
