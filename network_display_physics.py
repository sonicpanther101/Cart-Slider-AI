import numpy as np
import time
from cythonized import norm
import math
import pickle

def getIndexFromID(nodes, id):
    for i, node in enumerate(nodes):
        if node.id == id:
            return i

def calculateAngle(coord):
    """
    Calculates the angle (in radians) of a line from the horizontal to the right
    in the clockwise direction, given one point as (0, 0) and the other point
    as (x, y).
    """
    x, y = coord
    if x == 0 and y == 0:
        return 0  # Handle the case where both points are at the origin

    if x == 0:
        if y > 0:
            return math.pi / 2  # 90 degrees
        else:
            return 3 * math.pi / 2  # 270 degrees

    if y == 0:
        if x > 0:
            return 0  # 0 degrees
        else:
            return math.pi  # 180 degrees

    angle = math.atan2(y , x)

    if angle < 0:
        angle += 2 * math.pi

    return angle

class ball:
    def __init__(self, size, position, velocity, acceleration, colour, id):
        
        self.size = size
        self.position = np.array([float(position[i]) for i in range(len(position))])
        self.oldPosition = np.array(self.position) - np.array(velocity) * (1/1000)
        self.acceleration = np.array([float(acceleration[i]) for i in range(len(acceleration))])
        self.colour = colour
        self.id = id
        self.angularVelocity = 0

    def updatePosition(self, deltaTime):
        if self.id not in unmovingBallIDs:
            velocity = self.position - self.oldPosition
            self.oldPosition = self.position[:]
            self.position = self.position + velocity + self.acceleration * deltaTime * deltaTime

    def accelerate(self, acc):
        self.acceleration = self.acceleration + acc

class solver:
    def __init__(self, gravity):
        self.gravity = np.array(gravity)

    def update(self, links, balls, deltaTime):
        self.applyGravity(balls)
        self.solveLinks(links)
        self.updatePositions(balls, deltaTime)

    def updatePositions(self, balls, deltaTime):
        for ball in balls:
            ball.updatePosition(deltaTime)

    def applyGravity(self, balls):
        for ball in balls:
            ball.accelerate(self.gravity)

    def solveLinks(self, links):
        for link in links:
            link.apply()

class link:
    def __init__(self, ball1, ball2, targetDistance, thickness, colour):
        self.ball1 = ball1
        self.ball2 = ball2
        self.targetDistance = targetDistance
        self.thickness = thickness
        self.colour = colour
    
    def apply(self):
        axis = self.ball1.position - self.ball2.position
        distance = norm(axis)
        normal = axis / distance
        delta = self.targetDistance - distance

        if self.ball2.id not in unmovingBallIDs:
            self.ball2.position = self.ball2.position - (normal * delta/ 2)
        if self.ball1.id not in unmovingBallIDs:
            self.ball1.position = self.ball1.position + (normal * delta / 2)

subSteps = 1
solverVariable = solver([0, 0])
balls = []
links = []
unmovingBallIDs = []

def getNewNetwork():
    global balls, links, unmovingBallIDs
    balls = []
    links = []
    unmovingBallIDs = []

    with open('.generation.txt', 'rb') as file:
        
        nn = pickle.load(file)

    # get number of input/output nodes
    inputNodes = len([node for node in nn if node.type == "input"]) - 1
    outputNodes = len([node for node in nn if node.type == "output"]) - 1

    inputNodeSeperation = 600 / inputNodes if inputNodes > 0 else 0
    outputNodeSeperation = 600 / outputNodes if outputNodes > 0 else 300

    inputNodesAdded = 0
    outputNodesAdded = 1

    for node in nn:
        match node.type:
            case "input":
                balls.append(ball(13, [-400,300 - inputNodeSeperation * inputNodesAdded], [0,0], [0,0], (255, 0, 0), node.id))
                unmovingBallIDs.append(node.id)
                inputNodesAdded += 1
            case "output":
                balls.append(ball(13, [400,300 - outputNodeSeperation * outputNodesAdded], [0,0], [0,0], (0, 0, 255), node.id))
                unmovingBallIDs.append(node.id)
                outputNodesAdded += 1
            case "hidden":
                balls.append(ball(10, [0,0], [0,0], [0,0], (0, 255, 0), node.id))

    for node in nn:
        
        for childID in node.children:
            links.append(link(balls[getIndexFromID(balls, node.id)], balls[getIndexFromID(balls, childID)], 0, 2, (255, 255, 0)))

previousTime = 0
startTime = time.time()
deltaTime = 0

def main():
    global previousTime, startTime, deltaTime
    
    if previousTime == 0:
        previousTime = time.time()
    deltaTime = time.time() - previousTime
    previousTime = time.time()
    
    if deltaTime != 0:

        for _ in range(subSteps):
            solverVariable.update(links, balls, deltaTime/subSteps)