import physics_parallel as physics
import copy, time, gnumpy

solverVariable = physics.solver()

numOfAgents = 1000
subSteps = 1
framesPerGen = 10000 # in frames of environment 100 fps for 100s so 10000

cartPosX = gnumpy.zeros((numOfAgents,))
cartVelX = copy.deepcopy(cartPosX)
cartAccX = copy.deepcopy(cartPosX)

stickPosX = copy.deepcopy(cartPosX)
stickPosY = gnumpy.full((numOfAgents,), -100.)
oldStickPosX = copy.deepcopy(stickPosX)
oldStickPosY = copy.deepcopy(stickPosY)
stickAccX = copy.deepcopy(stickPosX)
stickAccY = copy.deepcopy(stickPosY)

fitness = copy.deepcopy(cartPosX)
mostRecentMutation = ["" for _ in range(numOfAgents)]

previousTime = 0
startTime = time.time()
deltaTime = 0

def main():
    global previousTime, startTime, deltaTime
    
    if previousTime == 0:
        previousTime = time.time()
    deltaTime = 1/100#time.time() - previousTime
    previousTime = time.time()
    
    for _ in range(subSteps):
        solverVariable.update(deltaTime)