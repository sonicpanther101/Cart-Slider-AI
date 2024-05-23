import neural_network as nn
import random
import pickle
import copy
import time
import threading
import queue
import network_display as display

previousTime = 0
startTime = time.time()
deltaTime = 0
threadsToUse = 1
step = int(len(nn.generation)/threadsToUse)
resultQueue = queue.Queue()
framesRun = 0

def threadedUpdateEnv(generation):

    global threadsToUse, step, resultQueue
    threads = []
    
    for i in range(threadsToUse):
        
        startIndex = step * i
        end = step * (i + 1)
        subGeneration = generation[startIndex:end]
        
        thread = threading.Thread(target=nn.stepForwardOneFrame, args=(subGeneration, startIndex, resultQueue))
        
        threads.append(thread)
        thread.start()
        
    for thread in threads:
        thread.join()
    
    results = []
    while not resultQueue.empty():
        results.append(resultQueue.get())
    
    generation = copy.deepcopy(results[0])
    
    assert len(generation) == len(nn.generation), f"The number of agents has changed unexpectedly, {len(generation)} vs {len(nn.generation)}"
                
    return generation

def main():
    global previousTime, startTime, deltaTime, framesRun

    previousTime = time.time()
    
    while True:
        
        # Update Objects
        nn.generation = threadedUpdateEnv(nn.generation)
        
        framesRun += 1
        if framesRun % 100 == 0:
            print(framesRun)
            
        if framesRun % 50 == 0 and framesRun/nn.generationLength > 1:
            display.pygame.event.pump()
            
        # Reset everything for new generation

        if framesRun % nn.generationLength == 0:
            print("new generation")
            
            deltaTime = time.time() - previousTime
            previousTime = time.time()
            
            """if framesRun/nn.generationLength == 5:
                exit()"""
            
            print(f'Generation {framesRun/nn.generationLength:.0f}')
            print(f"generation took {(deltaTime):.2f} seconds")
            
            nn.generation = nn.sortGenerationByFitness(nn.generation)
            
            print(f"fitness: {(nn.generation[0]["fitness"]/100000)*100:.2f}%")
            print("most recent mutation:", nn.generation[0]["most recent mutation"])
            nn.printNodesInfo(nn.generation[0]["brain"])
            
            if framesRun/nn.generationLength != 1:
                # Open a file for writing in binary mode
                with open(f'.generation.txt', 'wb') as file:
                    test = copy.deepcopy(nn.generation[0]["brain"])
                    from neural_network import node
                    network = [node(i) for i in range(len(test))]
                    
                    for i in range(len(test)):
                        network[i].id = test[i].id
                        network[i].type = test[i].type
                        network[i].parents = copy.copy(test[i].parents)
                        network[i].children = copy.copy(test[i].children)
                        network[i].connectionWeights = copy.copy(test[i].connectionWeights)
                    
                    print("dumping")
                    pickle.dump(network, file)
                    print("dumped")
            
            if framesRun/nn.generationLength == 1:
                display.networkScreen = display.init()
            print("updating screen")
            display.main(display.networkScreen)
            
            nn.nextGeneration = copy.deepcopy(nn.generation[:int(len(nn.generation) * 0.3)])
            
            agentsToMutate = random.choices(copy.deepcopy(nn.generation), weights=[agent["fitness"] if agent["fitness"] > 1 else 1 for agent in nn.generation],k= int(len(nn.generation) * 0.7))
            
            mutatedAgents = nn.mutateAgents(agentsToMutate)
            
            nn.nextGeneration.extend(mutatedAgents)
                                        
            nn.generation = copy.deepcopy(nn.nextGeneration)
            
            for agent in nn.generation:
                agent["brain"] = nn.sortNodes(agent["brain"])
                agent["fitness"] = 0
                agent["environment"] = copy.deepcopy(nn.physics.environment)
                
            print("new generation created")
                
if __name__ == "__main__":
    main()