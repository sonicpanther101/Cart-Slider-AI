import numpy as np
import time
import random
from cythonized import norm

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

    def updatePosition(self, deltaTime, cart):
        velocity = self.position - self.oldPosition
        self.oldPosition = self.position[:]
        self.position = self.position + velocity + self.acceleration * deltaTime * deltaTime
        if self.id == 0:
            if -250 > self.position[0]:
                self.position[0] = -250
            elif self.position[0] > 250:
                self.position[0] = 250
        self.acceleration = self.acceleration * 0
        if self.id != 0:
            linearVelocity = velocity / deltaTime
            theta = (math.pi-calculateAngle(self.position-cart.position))-(math.pi-calculateAngle(linearVelocity))
            velocityTangential = math.sin(theta) * norm(linearVelocity)
            self.angularVelocity = velocityTangential / norm(self.position-cart.position)

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
            ball.updatePosition(deltaTime, balls[0])

    def applyGravity(self, balls):
        global extraForce
        for ball in balls:
            if ball.id != 0:
                ball.accelerate(self.gravity)
            else:
                ball.accelerate([extraForce, 0])

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
balls = [ball(50, [0, -10*i], [0, 0], [0, 0], (255, 255*i, 255*i), i)for i in range(2)]
links = [link(balls[0], balls[1], 100, 5, (255, 255, 255))]
solverVariable = solver([0, -100])
extraForce = 0

previousTime = 0
startTime = time.time()
deltaTime = 0

j=0
s=0
def main():
    global previousTime, startTime, deltaTime, j,s
    
    if previousTime == 0:
        previousTime = time.time()
    deltaTime = time.time() - previousTime
    previousTime = time.time()
    
    if deltaTime != 0:
        j+=1
        for i in range(subSteps):
            solverVariable.update(links, balls, deltaTime/subSteps)
        
if __name__ == "__main__":
    #while True:
        #main()
    pass