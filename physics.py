import numpy as np
import time
import random
from cythonized import norm
import copy

import math

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
    def __init__(self, size, position, velocity, acceleration, color, id):
        
        self.size = size
        self.position = np.array([float(position[i]) for i in range(len(position))])
        self.oldPosition = np.array(self.position) - np.array(velocity) * (1/1000)
        self.acceleration = np.array([float(acceleration[i]) for i in range(len(acceleration))])
        self.color = color
        self.id = id
        self.angularVelocity = 0

    def updatePosition(self, deltaTime, cart, cartVelocity):
        velocity = self.position - self.oldPosition
        self.oldPosition = self.position[:]
        if self.id == 0:
            self.position = self.position + cartVelocity * deltaTime
            if -250 > self.position[0]:
                self.position[0] = -250
            elif self.position[0] > 250:
                self.position[0] = 250

        if self.id == 1:
            self.position = self.position + velocity + self.acceleration * deltaTime * deltaTime
            linearVelocity = velocity / deltaTime
            theta = (math.pi-calculateAngle(self.position-cart.position))-(math.pi-calculateAngle(linearVelocity))
            velocityTangential = math.sin(theta) * norm(linearVelocity)
            self.angularVelocity = velocityTangential / norm(self.position-cart.position)

    def accelerate(self, acc):
        self.acceleration = self.acceleration + acc

class solver:
    def __init__(self, gravity):
        self.gravity = np.array(gravity)

    def update(self, links, balls, deltaTime, cartVelocity):
        self.applyGravity(balls)
        self.solveLinks(links)
        self.updatePositions(balls, deltaTime, cartVelocity)

    def updatePositions(self, balls, deltaTime, cartVelocity):
        for ball in balls:
            ball.updatePosition(deltaTime, balls[0], cartVelocity)

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

        # uncomment to have stick momentum to pull cart
        self.ball2.position = self.ball2.position - (normal * delta) #/ 2)
        #self.ball1.position = self.ball1.position + (normal * delta / 2) * np.array([1, 0])

subSteps = 1
balls = [ball(50, [0, -100*i], [0, 0], [0, 0], (255, 255*i, 255*i), i)for i in range(2)]
links = [link(balls[0], balls[1], 100, 5, (255, 255, 255))]
solverVariable = solver([0, -100])
cartVelocity = 0

environment = {
    "balls": balls,
    "links": links,
    "solver": solverVariable,
    "cartVelocity": cartVelocity
}

previousTime = 0
startTime = time.time()
deltaTime = 0

def main(environment):
    global previousTime, startTime, deltaTime
    
    if previousTime == 0:
        previousTime = time.time()
    deltaTime = 1/100#time.time() - previousTime
    previousTime = time.time()
    
    if deltaTime != 0:

        for i in range(subSteps):
            environment["solver"].update(environment["links"], environment["balls"], deltaTime/subSteps, environment["cartVelocity"])
            
if __name__ == "__main__":
    main(environment)