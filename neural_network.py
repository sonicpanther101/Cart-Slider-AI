import numpy as np
import random, copy, math
import physics

class node:
    def __init__(self, id, type="hidden"):
        self.id = id
        self.bias = random.uniform(-1, 1) # not sure on this one
        self.parents = []
        self.children = []
        self.connectionWeights = []  # This will be initialized separately based on children
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
    
    #print("started sorting")
    while len(tempNodes) > 0:
        nodesToProcess = []
        
        for i, node in enumerate(tempNodes):
            if len(node.parents) == 0:
                nodesToProcess.append(nodes[i])
                tempNodes = removeNode(tempNodes, getIndexFromID(tempNodes, node.id))
        
        for node in nodesToProcess:
            sortedNodes.append(node)
    #print("finished sorting")
    
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

def stepForwardOneFrame(environments, offset):
    for agentID, environment in enumerate(environments):
        global generation
        agentID += offset
        
        # Update Physics frame
                
        physics.main(environment)
        
        # get NN output
        
        position = physics.environment["balls"][0].position[0]
        xDirection = physics.environment["balls"][0].position[0] - physics.environment["balls"][1].position[0]
        yDirection = physics.environment["balls"][0].position[1] - physics.environment["balls"][1].position[1]
        angularVelocity = physics.environment["balls"][1].angularVelocity
        
        
        generation[agentID]["agent"][0].value = position
        generation[agentID]["agent"][1].value = xDirection
        generation[agentID]["agent"][2].value = yDirection
        generation[agentID]["agent"][3].value = angularVelocity
        
        generation[agentID]["agent"] = calculateNodes(generation[agentID]["agent"])
        
        output = generation[agentID]["agent"][-1].value
        
        generation[agentID]["agent"] = resetNodes(generation[agentID]["agent"])
        
        if environment["frames"] % 100 == 0:
            pass#(f'agent {agentID}\ny of pendulum: {physics.environment["balls"][1].position[1]}\noutput: {output}')
        
        environment["cartVelocity"] = np.array([output,0])
        
        # update fitness
        
        generation[agentID]["fitness"] += fitness(physics.environment["balls"][1].position[1])

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
    #print("mutating")
    
    for i in range(len(agentsToMutate)):
        """print("agent:", i)
        printNodesInfo(agentsToMutate[i]["agent"]) 
        print("-"*30)"""
    
    mutatedAgents = []
    
    for agentIndex, agentTemp in enumerate(agentsToMutate):
        agent = copy.deepcopy(agentTemp)
        """print("pre mutation agent:", agentIndex)
        printNodesInfo(agent["agent"])
        print("-"*30)"""
        
        options = [0,1]
        
        if any(len(agent["agent"][i].children) > 0 for i in range(len(agent["agent"]))):
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

                    node1Index = random.randint(0,len(agent["agent"])-1)
                    node2Index = random.randint(0,len(agent["agent"])-1)
                                        
                    if node1Index < node2Index and \
((agent["agent"][node1Index].type == "input") + (agent["agent"][node2Index].type == "input") <=1 ) and \
((agent["agent"][node1Index].type == "output") + (agent["agent"][node2Index].type == "output") <=1 ) and \
(agent["agent"][node2Index].id not in agent["agent"][node1Index].children) and \
(agent["agent"][node1Index].id not in agent["agent"][node2Index].parents):
                        break
                    
                try:
                    if tries != 100:
                        agent["agent"][node1Index].children.append(agent["agent"][node2Index].id)
                        agent["agent"][node1Index].connectionWeights.append(random.uniform(-1, 1))
                        #print("pre:",agent["agent"][node2Index].id,agent["agent"][node2Index].parents)
                        agent["agent"][node2Index].parents.append(agent["agent"][node1Index].id)
                        #print(agent["agent"][node2Index].id,agent["agent"][node2Index].parents)
                        agent["most recent mutation"] = f"New Connection between nodes {getIDFromIndex(agent['agent'],node1Index)} and {getIDFromIndex(agent['agent'],node2Index)}"
                except:...

            case 2: # New Node
                #print("New Node")
                unusableNodes = []
                tries = 0
                while len(unusableNodes) != len(agent["agent"]) and tries < 100:
                    tries += 1
                
                    randomNode1Index = random.randint(0, len(agent["agent"])-1) # -2 to avoid output node
                    
                    if len(agent["agent"][randomNode1Index].children) == 0:
                        unusableNodes.append(randomNode1Index)
                        continue
                    #else:
                        #print(agent["agent"][randomNode1Index].id, agent["agent"][randomNode1Index].children)
                    
                    randomNode2ID = random.choice(agent["agent"][randomNode1Index].children)
                    randomNode2Index = getIndexFromID(agent["agent"], randomNode2ID)
                    randomNode1ID = getIDFromIndex(agent["agent"], randomNode1Index)
                    newNodeID = len(agent["agent"])
                    #print(randomNode2ID, agent["agent"][randomNode2Index].parents)
                    
                    # check if nodes are connected
                    if randomNode1ID not in agent["agent"][randomNode2Index].parents or randomNode2ID not in agent["agent"][randomNode1Index].children:
                        continue
                    
                    print("NEW NODE")
                    # Break the old connection
                    print(randomNode1Index, agent["agent"][randomNode1Index].children)
                    print(randomNode2Index, agent["agent"][randomNode2Index].parents)
                    agent["agent"][randomNode1Index].children.remove(randomNode2ID)
                    agent["agent"][randomNode2Index].parents.remove(randomNode1ID)
                    
                    # Add the new connection
                    agent["agent"][randomNode1Index].children.append(newNodeID)
                    agent["agent"][randomNode1Index].connectionWeights.append(random.uniform(-1, 1))
                    agent["agent"][randomNode2Index].parents.append(newNodeID)
                    
                    # Add the new node of the connection
                    agent["agent"].append(node(newNodeID))
                    agent["agent"][-1].parents.append(randomNode1ID)
                    agent["agent"][-1].children.append(randomNode2ID)
                    agent["most recent mutation"] = f"New Node {newNodeID} between {randomNode1ID} and {randomNode2ID}"
                    
                    break
                
            case 3: # Weight Modification
                #print("Weight Modification")
                unusableNodes = []
                tries = 0
                
                while len(unusableNodes) != len(agent["agent"]) and tries < 100:
                    tries += 1
                    
                    randomNodeIndex = random.randint(0, len(agent["agent"])-2) # -2 to avoid output node
                    
                    if len(agent["agent"][randomNodeIndex].connectionWeights) == 0:
                        unusableNodes.append(randomNodeIndex)
                        continue
                    
                    randomWeightIndex = random.randint(0, len(agent["agent"][randomNodeIndex].connectionWeights)-1)
                
                    agent["agent"][randomNodeIndex].connectionWeights[randomWeightIndex] = random.uniform(-1, 1)
                    agent["most recent mutation"] = f"Weight Modification of node {getIDFromIndex(agent["agent"],randomNodeIndex)} connection {getIDFromIndex(agent["agent"],randomWeightIndex)}"
                    break
                #print("weight modified")
        
        """print("post mutation agent:", agentIndex)
        printNodesInfo(agent["agent"])
        print("-"*30)"""
        mutatedAgents.append(agent)
    
    return mutatedAgents

nodes = [node(i, type="input") for i in range(4)]
nodes.append(node(4, type="output"))

nodes = sortNodes(nodes)

generation = [{"agent" : copy.deepcopy(nodes),
               "fitness":0,
               "most recent mutation":0} for i in range(100)]
generationLength = 100 # in frames of environment 100 fps for 100s so 10000

nextGeneration = []