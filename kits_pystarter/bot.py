from kit import Agent, Team, Direction, apply_direction
import math
import random 
import sys

# gets the distance between two points on the map
# x1, y1 the x and y coordinates of the first point
# x2, y2 the x and y coordinatex of the second point
# returns the distance between the two points
def getDistance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

# determine if unit is next to the wall
# returns true if it is
def isAtWall(unit, map):
    (x, y) = apply_direction(unit.x, unit.y, Direction.NORTH.value)
    if(x<0 or y<0 or x>=len(map[0]) or y >= len(map)):
        return True
    (x, y) = apply_direction(unit.x, unit.y, Direction.EAST.value)
    if(x<0 or y<0 or x>=len(map[0]) or y >= len(map)):
        return True
    (x, y) = apply_direction(unit.x, unit.y, Direction.SOUTH.value)
    if(x<0 or y<0 or x>=len(map[0]) or y >= len(map)):
        return True
    (x, y) = apply_direction(unit.x, unit.y, Direction.WEST.value)
    if(x<0 or y<0 or x>=len(map[0]) or y >= len(map)):
        return True
    return False

# chooses a random legal direction given the unit and map
# returns a direction that the unit can legally move in
def chooseRandom(unit, map):
    direction = Direction.STILL
    (x, y) = (unit.x, unit.y)
    # keep choosing a random direction until the direction is legal
    # also prevents unit from standing still
    while(direction==Direction.STILL or 
        x<0 or y<0 or x>=len(map[0]) or y >= len(map) or
        map[y][x]!=0):
        direction = random.choice(list(Direction))
        (x, y) = apply_direction(unit.x, unit.y, direction.value)
    return direction

# implementation of greedy algorithm for seeker to chase hider
# given the current seeker unit, its target, and the map
# returns the direction that will move the seeker closest to the hider
def greedy(current, target, map):
    bestDirection = None
    closestDistance = math.inf
    # for each possible direction, figure out its distance to the target
    for direction in Direction:
        (x, y) = apply_direction(current.x, current.y, direction.value)
        # if direction is still or not legal, continue with the loop
        if(direction==Direction.STILL or 
            x<0 or y<0 or x>=len(map[0]) or y >= len(map) or
            map[y][x]!=0):
            continue
        # figure out the shortest distance
        distance = getDistance(x, y, target.x, target.y)
        if (distance < closestDistance):
            bestDirection = direction
            closestDistance = distance
    # return the best direction
    return bestDirection
    # possibleDirections = {}
    # for direction in Direction:
    #     (x, y) = apply_direction(current.x, current.y, direction.value)
    #     #discount illegal directions
    #     if(direction==Direction.STILL or 
    #         x<0 or y<0 or x>=len(map[0]) or y >= len(map) or
    #         map[y][x]!=0):
    #         pass
    #     # map distances to each direction
    #     else:
    #         possibleDirections[direction] = getDistance(x, y, target.x, target.y)
    # # return direction that is shortest
    # return min(possibleDirections, key=possibleDirections.get)

def antiGreedy(current, enemy, map):
    bestDirection = None
    farthestDistance = 0
    # for each possible direction, figure out its distance to the target
    for direction in Direction:
        (x, y) = apply_direction(current.x, current.y, direction.value)
        # if direction is still or not legal, continue with the loop
        if(direction==Direction.STILL or 
            x<0 or y<0 or x>=len(map[0]) or y >= len(map) or
            map[y][x]!=0):
            continue
        # figure out the farthest distance
        distance = getDistance(x, y, enemy.x, enemy.y)
        if (distance > farthestDistance):
            bestDirection = direction
            farthestDistance = distance
    # return the best direction
    return bestDirection

# to keep track of the directions that each unit is "facing"
currentDirections = {}

# keep track of when unit reaches wall if it was initially heading there
reachedWall = {}

# chooses a direction for the given unit to move
# based on how an ant explores a new area
# basically it moves in a straight line until it encounters an obstacle
# then it chooses a random direction to continue in
# i̶n̶d̶e̶x̶ i̶s̶ t̶h̶e̶ i̶n̶d̶e̶x̶ o̶f̶ t̶h̶e̶ u̶n̶i̶t̶ i̶n̶ t̶h̶e̶ c̶u̶r̶r̶e̶n̶t̶D̶i̶r̶e̶c̶t̶i̶o̶n̶s̶ l̶i̶s̶t̶
# index has been deprecated :)
# returns the direction the unit must continue in
def chooseAntDirection(unit, map):
    if unit.id not in currentDirections:
        currentDirections[unit.id] = Direction.STILL
                
    (x, y) = apply_direction(unit.x, unit.y, currentDirections[unit.id].value)
    # if unit hits a wall or has no assigned direction            
    if(currentDirections[unit.id]==Direction.STILL or
        x<0 or y<0 or x>=len(map[0]) or y >= len(map) or
        map[y][x]!=0):
        # assign a random direction for it            
        currentDirections[unit.id] = chooseRandom(unit, map)
        direction = currentDirections[unit.id]
    # otherwise, continue in its current direction                
    else:
        direction = currentDirections[unit.id]

    return direction

# determines which wall is closest to the unit
# returns the point on the closest wall
# that is closest to the unit in the form (x, y)
def getClosestWall(unit, map):
    # Dictionary with the points on each wall
    # that are closest to the unit
    distances = {
        (unit.x, -1) : math.inf,            # North wall
        (unit.x, len(map)) : math.inf,     # South wall
        (-1, unit.y) : math.inf,            # West wall
        (len(map[0]), unit.y) : math.inf   # East wall
    }
    # map each key (point on the walls) to the distance that the unit is from that point
    distances[(unit.x, -1)] = getDistance(unit.x, unit.y, unit.x, -1)
    distances[(unit.x, len(map))] = getDistance(unit.x, unit.y, unit.x, len(map))
    distances[(-1, unit.y)] = getDistance(unit.x, unit.y, -1, unit.y)
    distances[(len(map[0]), unit.y)] = getDistance(unit.x, unit.y, len(map[0]), unit.y)

    return min(distances, key=distances.get)    # return key of smallest value in Dictionary

# returns direction that is closest to nearest wall
def goToWall(unit, map):
    # gets closest point to the closest wall
    (targetx, targety) = getClosestWall(unit, map)
    # a Dictionary to keep track of possible directions to move
    possibleDirections = {}
    for direction in Direction:
        (x, y) = apply_direction(unit.x, unit.y, direction.value)
        #discount illegal directions
        if(direction==Direction.STILL or 
            x<0 or y<0 or x>=len(map[0]) or y >= len(map) or
            map[y][x]!=0):
            pass
        # map distances to each direction
        else:
            possibleDirections[direction] = getDistance(x, y, targetx, targety)
    # return direction that is shortest
    return min(possibleDirections, key=possibleDirections.get)

# sticks to the right wall on the edge of the map
# returns the proper direction for sticking to the right wall
def followRightWall(unit, map):
    
    if unit.id not in currentDirections:
        currentDirections[unit.id] = goToWall(unit, map)
    
    (x, y) = apply_direction(unit.x, unit.y, currentDirections[unit.id].value)
    
    if((x<0 or y<0 or x>=len(map[0]) or y >= len(map))
        and (currentDirections[unit.id].value % 2)==0):
        currentDirections[unit.id] = Direction((currentDirections[unit.id].value - 2) % 8)
    
    i = 2
    (x, y) = apply_direction(unit.x, unit.y, (currentDirections[unit.id].value + i) % 8)
    direction = Direction((currentDirections[unit.id].value + i) % 8)
    # starts at direction right to current direction
    # and checks if it as a valid location to move to
    # then sequentially points counter-clockwise until a valid direction is found
    while(x<0 or y<0 or x>=len(map[0]) or y >= len(map) or 
        map[y][x]!=0):
        i -= 1
        direction = Direction((currentDirections[unit.id].value + i) % 8)
        (x, y) = apply_direction(unit.x, unit.y, direction.value)
    # update current facing direction and return direction to move
    currentDirections[unit.id] = direction
    return direction

def isSufficientlySurrounded(unit, map):
    surroundingObstacles = 0
    for direction in Direction:
        if(direction==Direction.STILL):
            continue
        (x, y) = apply_direction(unit.x, unit.y, direction.value)
        if(x<0 or y<0 or x>=len(map[0]) or y >= len(map) or map[y][x]==1):
            surroundingObstacles += 1
    if(surroundingObstacles >= 6):
        return True
    else:
        return False
    
# Create new agent
agent = Agent()

# initialize agent
agent.initialize()

numObstacles = 0
for i in range(len(agent.map)):
    for j in range(len(agent.map[i])):
        if(agent.map[i][j]==1):
            numObstacles += 1
obstacleDensity = numObstacles/(len(agent.map) * len(agent.map[0]))

while True:

    commands = []
    units = agent.units # list of units you own
    opposingUnits = agent.opposingUnits # list of units on other team that you can see
    game_map = agent.map # the map
    round_num = agent.round_num # the round number
    # unit.id is id of the unit
    # unit.x unit.y are its coordinates, unit.distance is distance away from nearest opponent
    # game_map is the 2D map of what you can see. 
    # game_map[i][j] returns whats on that tile, 0 = empty, 1 = wall, 
    # anything else is then the id of a unit which can be yours or the opponents
    
    if (agent.team == Team.SEEKER):
        # AI Code for seeker goes here

        index = 0       #index f̶o̶r̶ k̶e̶e̶p̶i̶n̶g̶ t̶r̶a̶c̶k̶ o̶f̶ u̶n̶i̶t̶s̶ i̶n̶ c̶u̶r̶r̶e̶n̶t̶D̶i̶r̶e̶c̶t̶i̶o̶n̶s̶ l̶i̶s̶t̶ is deprecated
        for _, unit in enumerate(units):
            if unit.id not in reachedWall:
                reachedWall[unit.id] = False

            # if no hiders seen, move like an ant exploring a new area
            if(len(opposingUnits)==0):
                if(obstacleDensity < 0.35):
                    direction = chooseAntDirection(unit, game_map)
                else:
                    if (not reachedWall[unit.id]) and (isAtWall(unit, game_map) or isSufficientlySurrounded(unit, game_map)):
                        reachedWall[unit.id] = True

                    if not reachedWall[unit.id]:
                        direction = goToWall(unit, game_map)
                        currentDirections[unit.id] = direction

                    else:
                        direction = followRightWall(unit, game_map)

            # if hiders seen, apply basic greedy alorithm to move closer to it
            else:
                reachedWall[unit.id] = False
                closestEnemy = opposingUnits[0]
                direction = greedy(unit, closestEnemy, game_map)
                currentDirections[unit.id] = direction
            
            # apply direction to current unit's position to check if that new position is on the game map
            (x, y) = apply_direction(unit.x, unit.y, direction.value)
            if (x < 0 or y < 0 or x >= len(game_map[0]) or y >= len(game_map)):
                # we do nothing if the new position is not in the map
                pass
            else:
                commands.append(unit.move(direction.value))

            index += 1
        
    else:
        index = 0
        for _, unit in enumerate(units):
            if unit.id not in reachedWall:
                reachedWall[unit.id] = False

            if (not reachedWall[unit.id]) and isAtWall(unit, game_map):
                reachedWall[unit.id] = True
                #currentDirections[unit.id] = Direction((goToWall(unit, game_map).value - 2) % 8)

            # if(len(opposingUnits)!=0):
            #     direction = antiGreedy(unit,)

            if isSufficientlySurrounded(unit, game_map):
                direction = Direction.STILL

            # if initially not at wall, call goToWall until wall reached
            elif not reachedWall[unit.id]:
                direction = goToWall(unit, game_map)
                currentDirections[unit.id] = direction

            # otherwise, procede with skrrrting around the edge of the map
            else:
                direction = followRightWall(unit, game_map)            

            # apply direction to current unit's position to check if that new position is on the game map
            (x, y) = apply_direction(unit.x, unit.y, direction.value)
            if (x < 0 or y < 0 or x >= len(game_map[0]) or y >= len(game_map)):
                # we do nothing if the new position is not in the map
                pass
            else:
                commands.append(unit.move(direction.value))
            
            index += 1



    # submit commands to the engine
    print(','.join(commands))

    # now we end our turn
    agent.end_turn()

    # wait for update from match engine
    agent.update()



