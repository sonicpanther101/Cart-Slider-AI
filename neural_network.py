import numpy as np
import random, copy, math

class node:
    def __init__(self, id, parents=[], children=[], type="hidden"):
        self.id = id
        self.bias = random.uniform(-1, 1) # not sure on this one
        self.parents = parents
        self.children = children
        self.connectionWeights = [random.uniform(-1, 1) for i in range(len(self.children))]
        self.value = 0
        self.type = type
    
    def calculate(self, nodes):
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
    tempNodes = copy.deepcopy(nodes)
    
    sortedNodes = []
    
    while len(tempNodes) > 0:
        nodesToProcess = []
        
        for node in tempNodes:
            if len(node.parents) == 0:
                nodesToProcess.append(node)
                tempNodes = removeNode(tempNodes, getIndexFromID(tempNodes, node.id))
        
        for node in nodesToProcess:
            sortedNodes.append(node)
    
    return sortedNodes

def removeNode(nodes, nodeIndex):
    tempNodes = copy.deepcopy(nodes)
    tempNodes.pop(nodeIndex)
    
    for childID in nodes[nodeIndex].children:

        for childNode in tempNodes:
            if childNode.id == childID:
                childNode.parents.remove(nodes[nodeIndex].id)

    return tempNodes

def printNodesInfo(nodes):
    for node in nodes:
        print(node.id, node.parents, node.children, node.connectionWeights, node.value, node.type)
    
def printNodesOrder(nodes):
    output = []
    for node in nodes:
        output.append(str(node.id))
    print(", ".join(output))
    
def printNodeInfo(node):
    print(node.id, node.parents, node.children, node.connectionWeights, node.value)

def calculateNodes(nodes):
    for node in nodes:
        node.calculate(nodes)
    
    return nodes

def resetNodes(nodes):
    for node in nodes:
        node.value = 0
    return nodes

def sortGenerationByFitness(generation):
    return sorted(generation, key=lambda x: x["fitness"], reverse=True)

def getIndexFromID(nodes, id):
    for i, node in enumerate(nodes):
        if node.id == id:
            return i

def getIDFromIndex(nodes, index):
    return nodes[index].id

def fitness(x):
    return 100 * math.exp(3 * (x/100 - 1))

def mutateAgents(agentsToMutate):
    print("mutating")
    
    for i in range(len(agentsToMutate)):
        print("agent:", i)
        printNodesInfo(agentsToMutate[i]["agent"]) 
        print("-"*30)
    
    mutatedAgents = []
    
    for agentIndex, agentTemp in enumerate(agentsToMutate):
        agent = copy.deepcopy(agentTemp)
        print("pre mutation agent:", agentIndex)
        printNodesInfo(agent["agent"])
        print("-"*30)
        
        options = [0,1]
        
        if any(len(agent["agent"][i].children) > 0 for i in range(len(agent["agent"]))):
            options.append(2)
            options.append(3)
        
        match random.choice(options):
            case 0: # Nothing
                print("Nothing")
                pass
            case 1: # New Connection
                print("New Connection")
                errorCounter = 0
                while True:
                    if errorCounter > 100:
                        print("error")
                        break
                    node1Index = random.randint(0,len(agent["agent"])-1)
                    node2Index = random.randint(0,len(agent["agent"])-1)
                                        
                    if node1Index < node2Index and \
((agent["agent"][node1Index].type == "input") + (agent["agent"][node2Index].type == "input") <=1 ) and \
((agent["agent"][node1Index].type == "output") + (agent["agent"][node2Index].type == "output") <=1 ) and \
(agent["agent"][node2Index].id not in agent["agent"][node1Index].children) and \
(agent["agent"][node1Index].id not in agent["agent"][node2Index].parents):
                        break
                    errorCounter += 1
                try:
                    agent["agent"][node1Index].children.append(agent["agent"][node2Index].id)
                    agent["agent"][node1Index].connectionWeights.append(random.uniform(-1, 1))
                    agent["agent"][node2Index].parents.append(agent["agent"][node1Index].id)
                    print(agent["agent"][node2Index].parents, agent["agent"][node1Index].children)
                except:...
                
            case 2: # New Node
                print("New Node")
                randomNode1Index = random.randint(0, len(agent["agent"])-2) # -2 to avoid output node
                randomNode2ID = random.choice(agent["agent"][randomNode1Index].children)
                randomNode2Index = getIndexFromID(agent["agent"], randomNode2ID)
                randomNode1ID = getIDFromIndex(agent["agent"], randomNode1Index)
                newNodeID = len(agent["agent"])
                
                # Break the old connection
                agent["agent"][randomNode1Index].children.remove(randomNode2ID)
                agent["agent"][randomNode2Index].parents.remove(randomNode1ID)
                
                # Add the new connection
                agent["agent"][randomNode1Index].children.append(newNodeID)
                agent["agent"][randomNode1Index].connectionWeights.append(random.uniform(-1, 1))
                agent["agent"][randomNode2Index].parents.append(newNodeID)
                
                # Add the new node of the connection
                agent["agent"].append(node(newNodeID, [randomNode1ID], [randomNode2ID]))
                
            case 3: # Weight Modification
                print("Weight Modification")              
                randomNodeIndex = random.randint(0, len(agent["agent"])-2) # -2 to avoid output node
                
                randomWeightIndex = random.randint(0, len(agent["agent"][randomNodeIndex].connectionWeights)-1)
            
                agent["agent"][randomNodeIndex].connectionWeights[randomWeightIndex] = random.uniform(-1, 1)
        
        print("post mutation agent:", agentIndex)
        printNodesInfo(agent["agent"])
        print("-"*30)
        mutatedAgents.append(agent)

nodes = [node(i, type="input") for i in range(4)]
nodes.append(node(4, type="output"))

nodes = sortNodes(nodes)

generation = [{"agent" : nodes,
               "fitness":0} for i in range(10)]
generationLength = 10000 # in frames of environment

nextGeneration = []