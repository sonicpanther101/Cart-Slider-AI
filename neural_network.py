import numpy as np
import random

class node:
    def __init__(self, id, parents=[], children=[]):
        self.id = id
        self.bias = random.uniform(-1, 1)
        self.parents = parents
        self.children = children
        self.connectionWeights = [random.uniform(-1, 1) for i in range(len(self.children))]
        self.value = 0
    
    def calculate(self):
        global nodes
        self.value += self.bias
        
        if len(self.children) == 0:
            self.value = tanh(self.value)
        elif len(self.parents) > 0:
            self.value = relu(self.value)
        
        for childID in self.children:
            for childNode in nodes:
                if childNode.id == childID:
                    childNode.value += self.value * self.connectionWeights[self.children.index(childID)]

def relu(x):
	return max(0.0, x)

def tanh(x):
    return np.tanh(x)

def sortNodes(nodes):
    tempNodes = nodes.copy()
    
    sortedNodes = []
    
    while len(tempNodes) > 0:
        nodesToProcess = []
        
        for node in tempNodes:
            if len(node.parents) == 0:
                nodesToProcess.append(node)
                tempNodes = removeNode(tempNodes, node)
        
        for node in nodesToProcess:
            sortedNodes.append(node)
    
    return sortedNodes

def removeNode(nodes, node):
    tempNodes = nodes.copy()
    tempNodes.remove(node)
    
    for childID in node.children:

        for childNode in tempNodes:
            if childNode.id == childID:
                childNode.parents.remove(node.id)

    return tempNodes

def printNodesInfo(nodes):
    for node in nodes:
        print(node.id, node.parents, node.children, node.connectionWeights, node.value)
    
def printNodesOrder(nodes):
    output = []
    for node in nodes:
        output.append(str(node.id))
    print(", ".join(output))
    
def printNodeInfo(node):
    print(node.id, node.parents, node.children, node.connectionWeights, node.value)

def calculateNodes(nodes):
    for node in nodes:
        node.calculate()
    
    return nodes

def resetNodes(nodes):
    for node in nodes:
        node.value = 0
    return nodes

def sortGenerationByFitness(generation):
    return sorted(generation, key=lambda x: x["fitness"], reverse=True)

def mutateAgents(agentsToMutate):
    for agent in agentsToMutate:
        
        match random.choice([0,1,2,3]):
            case 0: # Nothing
                pass
            case 1: # New Connection
                
                
            case 2: # New Node
                pass
            case 3: # Weight Modification
                
                weightIndex = random.randint(0, len(random.choice(agent["agent"]).connectionWeights) - 1)
                
                random.choice(agent["agent"]).connectionWeights[weightIndex] = random.uniform(-1, 1)

nodes = [
node(0,[],[6,8]),  node(1,[],[8]),  node(2,[],[9]),          node(3,[],[8,9]), node(4,[6,7,9],[]), 
node(6,[0,8],[4]), node(7,[8],[4]), node(8,[0,1,3],[6,7,9]), node(9,[2,3,8],[4])]

nodes = sortNodes(nodes)

generation = [{"agent" : nodes,
               "fitness":0} for i in range(10)]

nextGeneration = []