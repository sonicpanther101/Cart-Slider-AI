import neural_network_parallel as nn
import copy
import cupy
import random
import pygame

solverVariable = nn.physics.solver()

subSteps = 10
framesPerGen = 10000 # in frames of environment 100 fps for 100s so 10000
numOfAgents = 10
initialNodesPerAgent = 5
emptyArray = cupy.zeros((numOfAgents,))

cartPosX = copy.deepcopy(emptyArray)
cartVelX = copy.deepcopy(emptyArray)

stickPosX = copy.deepcopy(emptyArray)
stickPosY = cupy.full((numOfAgents,), -100.)
oldStickPosX = copy.deepcopy(emptyArray)
oldStickPosY = copy.deepcopy(stickPosY)
stickAccX = copy.deepcopy(emptyArray)
stickAccY = cupy.full((numOfAgents,), -100)
angularVelocity = copy.deepcopy(emptyArray)

nodesPerAgent = cupy.full((numOfAgents,), initialNodesPerAgent)

nodeIDs = cupy.arange(numOfAgents*initialNodesPerAgent)
nodeBiases = cupy.full((numOfAgents*initialNodesPerAgent,), random.uniform(-1, 1))
nodeParents = cupy.full((numOfAgents*initialNodesPerAgent,), [])
nodeChildren = cupy.full((numOfAgents*initialNodesPerAgent,), [])
nodeConnectionWeights = cupy.full((numOfAgents*initialNodesPerAgent,), [])
nodeValues = cupy.full((numOfAgents*initialNodesPerAgent,), 0)
nodeType = cupy.tile((cupy.array(["input"] * (initialNodesPerAgent-1) + ["output"])), numOfAgents)
nodeColour = cupy.tile((cupy.array(["blue"] * (initialNodesPerAgent-1) + ["red"])), numOfAgents)

fitness = copy.deepcopy(emptyArray)
mostRecentMutation = ["" for _ in range(numOfAgents)]

def main(cartPosX, stickPosX, stickPosY, cartVelX, oldStickPosX, oldStickPosY, stickAccX, stickAccY, subSteps, solverVariable):
    
    while True:
        
        stickPosX, stickPosY, angularVelocity, cartPosX, oldStickPosX, oldStickPosY = nn.physics.main(cartPosX, stickPosX, stickPosY, cartVelX, oldStickPosX, oldStickPosY, stickAccX, stickAccY, subSteps, solverVariable)
                
if __name__ == "__main__":
    main(cartPosX, stickPosX, stickPosY, cartVelX, oldStickPosX, oldStickPosY, stickAccX, stickAccY, subSteps, solverVariable)