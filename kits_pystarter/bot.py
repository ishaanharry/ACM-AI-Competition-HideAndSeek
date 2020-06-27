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

# to keep track of the directions that each unit is "facing"
currentDirections = {}

# chooses a direction for the given unit to move
# based on how an ant explores a new area
# basically it moves in a straight line until it encounters an obstacle
# then it chooses a random direction to continue in
# index is the index of the unit in the currentDirections list
# returns the direction the unit must continue in
def chooseAntDirection(unit, index, map):
    if index not in currentDirections:
        currentDirections[index] = Direction.STILL
                
    (x, y) = apply_direction(unit.x, unit.y, currentDirections[index].value)
    # if unit hits a wall or has no assigned direction            
    if(currentDirections[index]==Direction.STILL or
        x<0 or y<0 or x>=len(map[0]) or y >= len(map) or
        map[y][x]!=0):
        # assign a random direction for it            
        currentDirections[index] = chooseRandom(unit, map)
        direction = currentDirections[index]
    # otherwise, continue in its current direction                
    else:
        direction = currentDirections[index]

    return direction

# Create new agent
agent = Agent()

# initialize agent
agent.initialize()

while True:

    commands = []
    units = agent.units # list of units you own
    opposingUnits = agent.opposingUnits # list of units on other team that you can see
    game_map = agent.map # the map
    round_num = agent.round_num # the round number

    
    if (agent.team == Team.SEEKER):
        # AI Code for seeker goes here

        index = 0       #index for keeping track of units in currentDirections list
        for _, unit in enumerate(units):
            # unit.id is id of the unit
            # unit.x unit.y are its coordinates, unit.distance is distance away from nearest opponent
            # game_map is the 2D map of what you can see. 
            # game_map[i][j] returns whats on that tile, 0 = empty, 1 = wall, 
            # anything else is then the id of a unit which can be yours or the opponents

            
            # if no hiders seen, move like an ant exploring a new area
            if(len(opposingUnits)==0):
                direction = chooseAntDirection(unit, index, game_map)
            # if hiders seen, apply basic greedy alorithm to move closer to it
            else:
                closestEnemy = opposingUnits[0]
                direction = greedy(unit, closestEnemy, game_map)    
            

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
            direction = chooseRandom(unit, game_map)

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



