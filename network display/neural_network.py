import numpy as np
import random, copy, math
import pickle

class node:
    def __init__(self, id, type="hidden"):
        self.id = id
        #self.bias = random.uniform(-1, 1) # not sure on this one
        self.parents = []
        self.children = []
        self.connectionWeights = []  # This will be initialized separately based on children
        self.value = 0
        self.type = type
        match type:
            case "input":
                self.colour = "blue"
            case "output":
                self.colour = "red"
            case "hidden":
                self.colour = "green"

def sortNodes(nodes):
    
    tempNodes = copy.deepcopy(nodes)
    
    sortedNodes = []
    
    while len(tempNodes) > 0:

        nodesToProcess = []
        nodeIndexesToRemove = []
        
        for i in range(len(tempNodes)):
            if len(tempNodes[i].parents) == 0:
                realIndex = getIndexFromID(nodes, tempNodes[i].id)
                nodesToProcess.append(nodes[realIndex])
                nodeIndexesToRemove.append(i)
        
        nodeIndexesToRemove.sort(reverse=True)
        for nodeIndex in nodeIndexesToRemove:
            tempNodes = removeNode(tempNodes, nodeIndex)
        
        for node in nodesToProcess:
            sortedNodes.append(node)
                    
    return sortedNodes

def removeNode(nodes, nodeIndex):
    tempNodes = copy.deepcopy(nodes)
    tempNodes.pop(nodeIndex)
    
    for childID in nodes[nodeIndex].children:

        for childNode in tempNodes:
            if childNode.id == childID:
                try:
                    childNode.parents.remove(nodes[nodeIndex].id)
                except:
                    pass#print("wtf")

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
    print(node.id, node.parents, node.children, node.connectionWeights, node.value, node.type)

def sortGenerationByFitness(generation):
    return sorted(generation, key=lambda agent: agent["fitness"], reverse=True)

def getIndexFromID(nodes, id):
    for i, node in enumerate(nodes):
        if node.id == id:
            return i

def getIDFromIndex(nodes, index):
    return nodes[index].id

def fitness(x):
    return 100 * math.exp(3 * (x/100 - 1))

def mutateAgents(agentsToMutate):
    #print("mutating")
    
    for i in range(len(agentsToMutate)):
        """print("agent:", i)
        printNodesInfo(agentsToMutate[i]["brain"]) 
        print("-"*30)"""
    
    mutatedAgents = []
    
    for agentTemp in agentsToMutate:
        agent = copy.deepcopy(agentTemp)
        """print("pre mutation agent:", agentIndex)
        printNodesInfo(agent["brain"])
        print("-"*30)"""
        
        options = [0,1]
        
        if any(len(agent["brain"][i].children) > 0 for i in range(len(agent["brain"]))):
            options.append(2)
            options.append(3)
        
        match random.choice(options):
            case 0: # Nothing
                agent["most recent mutation"] = "Nothing"
                #print("Nothing")
                pass
            case 1: # New Connection
                #print("New Connection")
                tries = 0
                while tries < 100:
                    tries += 1

                    node1Index = random.randint(0,len(agent["brain"])-1)
                    node2Index = random.randint(0,len(agent["brain"])-1)
                                        
                    if node1Index < node2Index and \
((agent["brain"][node1Index].type == "input") + (agent["brain"][node2Index].type == "input") <=1 ) and \
((agent["brain"][node1Index].type == "output") + (agent["brain"][node2Index].type == "output") <=1 ) and \
(agent["brain"][node2Index].id not in agent["brain"][node1Index].children) and \
(agent["brain"][node1Index].id not in agent["brain"][node2Index].parents):
                        break
                    
                try:
                    if tries != 100:
                        agent["brain"][node1Index].children.append(agent["brain"][node2Index].id)
                        agent["brain"][node1Index].connectionWeights.append(random.uniform(-1, 1))
                        #print("pre:",agent["brain"][node2Index].id,agent["brain"][node2Index].parents)
                        agent["brain"][node2Index].parents.append(agent["brain"][node1Index].id)
                        #print(agent["brain"][node2Index].id,agent["brain"][node2Index].parents)
                        agent["most recent mutation"] = f"New Connection between nodes {getIDFromIndex(agent['agent'],node1Index)} and {getIDFromIndex(agent['agent'],node2Index)}"
                except:...

            case 2: # New Node
                #print("New Node")
                unusableNodes = []
                tries = 0
                while len(unusableNodes) != len(agent["brain"]) and tries < 100:
                    tries += 1
                
                    randomNode1Index = random.randint(0, len(agent["brain"])-1) # -2 to avoid output node
                    
                    if len(agent["brain"][randomNode1Index].children) == 0:
                        unusableNodes.append(randomNode1Index)
                        continue
                    
                    randomNode2ID = random.choice(agent["brain"][randomNode1Index].children)
                    randomNode2Index = getIndexFromID(agent["brain"], randomNode2ID)
                    randomNode1ID = getIDFromIndex(agent["brain"], randomNode1Index)
                    newNodeID = len(agent["brain"])
                    #print(randomNode2ID, agent["brain"][randomNode2Index].parents)
                    
                    # check if nodes are connected
                    if randomNode1ID not in agent["brain"][randomNode2Index].parents or randomNode2ID not in agent["brain"][randomNode1Index].children:
                        continue
                    
                    # Break the old connection
                    childIndex = agent["brain"][randomNode1Index].children.index(randomNode2ID)
                    agent["brain"][randomNode1Index].children.remove(randomNode2ID)
                    agent["brain"][randomNode1Index].connectionWeights.pop(childIndex)
                    agent["brain"][randomNode2Index].parents.remove(randomNode1ID)
                    
                    # Add the new connection
                    agent["brain"][randomNode1Index].children.append(newNodeID)
                    agent["brain"][randomNode1Index].connectionWeights.append(random.uniform(-1, 1))
                    agent["brain"][randomNode2Index].parents.append(newNodeID)
                    
                    # Add the new node of the connection
                    agent["brain"].append(node(newNodeID))
                    agent["brain"][-1].parents.append(randomNode1ID)
                    agent["brain"][-1].children.append(randomNode2ID)
                    agent["brain"][-1].connectionWeights.append(random.uniform(-1, 1))
                    agent["most recent mutation"] = f"New Node {newNodeID} between {randomNode1ID} and {randomNode2ID}"
                    
                    break
                
            case 3: # Weight Modification
                #print("Weight Modification")
                unusableNodes = []
                tries = 0
                
                while len(unusableNodes) != len(agent["brain"]) and tries < 100:
                    tries += 1
                    
                    randomNodeIndex = random.randint(0, len(agent["brain"])-2) # -2 to avoid output node
                    
                    if len(agent["brain"][randomNodeIndex].connectionWeights) == 0:
                        unusableNodes.append(randomNodeIndex)
                        continue
                    
                    randomWeightIndex = random.randint(0, len(agent["brain"][randomNodeIndex].connectionWeights)-1)
                
                    agent["brain"][randomNodeIndex].connectionWeights[randomWeightIndex] = random.uniform(-1, 1)
                    agent["most recent mutation"] = f"Weight Modification of node {getIDFromIndex(agent["brain"],randomNodeIndex)} connection {getIDFromIndex(agent["brain"],randomWeightIndex)}"
                    break
                #print("weight modified")
        
        """print("post mutation agent:", agentIndex)
        printNodesInfo(agent["brain"])
        print("-"*30)"""
        mutatedAgents.append(agent)
    
    return mutatedAgents