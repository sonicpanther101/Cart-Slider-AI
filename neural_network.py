import numpy as np
import random, copy, math
import physics

class node:
    def __init__(self, id, type="hidden"):
        self.id = id
        #self.bias = random.uniform(-1, 1) # not sure on this one
        self.parents = []
        self.children = []
        self.connectionWeights = []  # This will be initialized separately based on children
        self.value = 0
        self.type = type
    
    def calculate(self, nodes):
        #self.value += self.bias
        
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
    tempNodesLength = len(tempNodes)
    
    sortedNodes = []
    offset = 0
    x = 0
    
    #print("started sorting")
    while tempNodesLength > 0:
        x+=1
        print(f"round {x}")
        nodesToProcess = []
        nodeIndexesToRemove = []
        
        for i in range(tempNodesLength):
            if len(tempNodes[i].parents) == 0:
                print(i+offset)
                nodesToProcess.append(nodes[i+offset])
                nodeIndexesToRemove.append(i)
        
        nodeIndexesToRemove.sort(reverse=True)
        for nodeIndex in nodeIndexesToRemove:
            tempNodes = removeNode(tempNodes, nodeIndex)
            tempNodesLength -= 1
        
        for node in nodesToProcess:
            offset += 1
            sortedNodes.append(node)
            
    #print("finished sorting")
    
    printNodesInfo(nodes)
    print("vs")
    printNodesInfo(sortedNodes)
    
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

def calculateNodes(nodes):
    for node in nodes:
        node.calculate(nodes)
    
    return nodes

def resetNodes(nodes):
    for node in nodes:
        node.value = 0
    return nodes

def stepForwardOneFrame(subGeneration, offset, resultQueue):
    for agentID, agent in enumerate(subGeneration):
        agentID += offset
        
        # Update Physics frame
                
        physics.main(agent["environment"])
        
        # get NN output
        
        position = agent["environment"]["balls"][0].position[0]
        xDirection = agent["environment"]["balls"][0].position[0] - agent["environment"]["balls"][1].position[0]
        yDirection = agent["environment"]["balls"][0].position[1] - agent["environment"]["balls"][1].position[1]
        angularVelocity = agent["environment"]["balls"][1].angularVelocity
        
        
        agent["brain"][0].value = position
        agent["brain"][1].value = xDirection
        agent["brain"][2].value = yDirection
        agent["brain"][3].value = angularVelocity
        
        agent["brain"] = calculateNodes(agent["brain"])
        
        output = agent["brain"][-1].value
        
        agent["brain"] = resetNodes(agent["brain"])
        
        if agent["frames alive"] % 100 == 0:
            pass#(f'agent {agentID}\ny of pendulum: {agent["environment"]["balls"][1].position[1]}\noutput: {output}')
        
        agent["environment"]["cartVelocity"] = np.array([output,0])
        
        # update fitness
        
        agent["fitness"] += fitness(agent["environment"]["balls"][1].position[1])
        
        agent["frames alive"] += 1
        
        resultQueue.put(subGeneration)

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
    
    for agentIndex, agentTemp in enumerate(agentsToMutate):
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
                    
                    print("NEW NODE")
                    # Break the old connection
                    print(randomNode1Index, agent["brain"][randomNode1Index].children)
                    print(randomNode2Index, agent["brain"][randomNode2Index].parents)
                    agent["brain"][randomNode1Index].children.remove(randomNode2ID)
                    agent["brain"][randomNode2Index].parents.remove(randomNode1ID)
                    
                    # Add the new connection
                    agent["brain"][randomNode1Index].children.append(newNodeID)
                    agent["brain"][randomNode1Index].connectionWeights.append(random.uniform(-1, 1))
                    agent["brain"][randomNode2Index].parents.append(newNodeID)
                    
                    # Add the new node of the connection
                    agent["brain"].append(node(newNodeID))
                    agent["brain"][-1].parents.append(randomNode1ID)
                    agent["brain"][-1].children.append(randomNode2ID)
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

nodes = [node(i, type="input") for i in range(4)]
nodes.append(node(4, type="output"))
nodes[4].parents.append(5)
nodes[0].children.append(5)
nodes.append(node(5))
nodes[5].parents.append(0)
nodes[5].children.append(4)

nodes = sortNodes(nodes)

generation = [{"brain" : copy.deepcopy(nodes),
               "environment":copy.deepcopy(physics.environment),
               "fitness":0,
               "frames alive": 0,
               "most recent mutation":0} for i in range(10)]
generationLength = 100 # in frames of environment 100 fps for 100s so 10000

nextGeneration = []