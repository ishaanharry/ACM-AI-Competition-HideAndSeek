from kit import Agent, Team, Direction, apply_direction
import math
import random 
import sys

def getDistance(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def greedy(current, target):
    bestDirection = None
    closestDistance = math.inf

    for direction in Direction:
        if(direction==Direction.STILL): continue
        (x, y) = apply_direction(current.x, current.y, direction.value)
        distance = getDistance(x, y, target.x, target.y)
        if (distance < closestDistance):
            bestDirection = direction
            closestDistance = distance
    
    return bestDirection


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

        for _, unit in enumerate(units):
            # unit.id is id of the unit
            # unit.x unit.y are its coordinates, unit.distance is distance away from nearest opponent
            # game_map is the 2D map of what you can see. 
            # game_map[i][j] returns whats on that tile, 0 = empty, 1 = wall, 
            # anything else is then the id of a unit which can be yours or the opponents

            
             # choose a random direction to move in
            direction = random.choice(list(Direction)).value
            
            
            if(len(opposingUnits)!=0):
                closestEnemy = opposingUnits[0]
                direction = greedy(unit, closestEnemy).value
            
            """
            # choose direction based on greedy algorithm
            direction = Direction.STILL.value
            if (len(opposingUnits)==0):
                direction = random.choice(list(Direction)).value
            else:
                
                closestEnemy = opposingUnits[0]
                for enemy in opposingUnits:
                    distance = getDistance(unit.x, unit,y, enemy.x, enemy.y)
                    if distance == unit.distance:
                        closestEnemy = enemy
                
                direction = greedy(unit, closestEnemy)
            """

            # apply direction to current unit's position to check if that new position is on the game map
            (x, y) = apply_direction(unit.x, unit.y, direction)
            if (x < 0 or y < 0 or x >= len(game_map[0]) or y >= len(game_map)):
                # we do nothing if the new position is not in the map
                pass
            else:
                commands.append(unit.move(direction))
        
    else:
        # AI Code for hider goes here
        # hider code, which does nothing, sits tight and hopes it doesn't get 
        # found by seekers
        pass



    # submit commands to the engine
    print(','.join(commands))

    # now we end our turn
    agent.end_turn()

    # wait for update from match engine
    agent.update()



