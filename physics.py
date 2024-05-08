import numpy as np
import time
import random
from cythonized import norm

class ball:
    def __init__(self, size, position, velocity, acceleration, color, id):
        
        self.size = size
        self.position = np.array([float(position[i]) for i in range(len(position))])
        self.oldPosition = np.array(self.position) - np.array(velocity) * (1/1000)
        self.acceleration = np.array([float(acceleration[i]) for i in range(len(acceleration))])
        self.color = color
        self.id = id

    def updatePosition(self, deltaTime):
        velocity = self.position - self.oldPosition
        self.oldPosition = self.position[:]
        self.position = self.position + velocity + self.acceleration * deltaTime * deltaTime
        self.acceleration = self.acceleration * 0

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
            if ball.id not in unmovingBalls:
                ball.updatePosition(deltaTime)

    def applyGravity(self, balls):
        for ball in balls:
            if ball.id not in unmovingBalls:
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
        if self.ball1.id not in unmovingBalls:
            self.ball1.position = self.ball1.position + (normal * delta / 2)
        if self.ball2.id not in unmovingBalls:
            self.ball2.position = self.ball2.position - (normal * delta / 2)

subSteps = 3
balls = [ball(10, [0, -10*i], [(1-i)*100000, 0], [0, 0], (255, 255*i, 255*i), i)for i in range(2)]
links = [link(balls[0], balls[1], 100, 5, (255, 255, 255)) for i in range(10)]
solverVariable = solver([0, -100])
unmovingBalls = [0]
#balls.append()

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
    while True:
        main()