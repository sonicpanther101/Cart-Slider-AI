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
    
    mutatedAgents = []
    
    for agent in agentsToMutate:
        
        match random.choice([0,1,2,3]):
            case 0: # Nothing
                pass
            case 1: # New Connection
                while True:
                    node1Index = random.randint(0,len(agent["agent"])-1)
                    node2Index = random.randint(0,len(agent["agent"])-1)
                    
                    if node1Index < node2Index and \
((len(agent["agent"][node1Index].parents) == 0) + (len(agent["agent"][node2Index].parents) == 0) <=1 ) and \
((len(agent["agent"][node1Index].children) == 0) + (len(agent["agent"][node2Index].children) == 0) <=1 ) and \
(agent["agent"][node2Index].id not in agent["agent"][node1Index].children) and \
(agent["agent"][node1Index].id not in agent["agent"][node2Index].parents):
                        break
                    
                agent["agent"][node1Index].children.append(agent["agent"][node2Index].id)
                agent["agent"][node1Index].connectionWeights.append(random.uniform(-1, 1))
                agent["agent"][node2Index].parents.append(agent["agent"][node1Index].id)
                
            case 2: # New Node
                randomNodeIndex = random.randint(0, len(agent["agent"])-2) # -2 to avoid output node
                
                
                
            case 3: # Weight Modification
                
                randomNodeIndex = random.randint(0, len(agent["agent"])-2) # -2 to avoid output node
                
                randomWeightIndex = random.randint(0, len(agent["agent"][randomNodeIndex].connectionWeights)-1)
                
                agent["agent"][randomNodeIndex].connectionWeights[randomWeightIndex] = random.uniform(-1, 1)
                
        mutatedAgents.append(agent)

nodes = [
node(0,[],[5,7]),  node(1,[],[7]),  node(2,[],[8]),          node(3,[],[7,8]), node(4,[5,6,8],[]), 
node(5,[0,7],[4]), node(6,[7],[4]), node(7,[0,1,3],[5,6,8]), node(8,[2,3,7],[4])]

nodes = sortNodes(nodes)

generation = [{"agent" : nodes,
               "fitness":0} for i in range(10)]

nextGeneration = []