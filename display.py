import neural_network as nn
import random
import pickle
import copy
import time
import threading
import queue

previousTime = 0
startTime = time.time()
deltaTime = 0
threadsToUse = 10
step = int(len(nn.generation)/threadsToUse)
resultQueue = queue.Queue()

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
        
    results = []
    for thread in threads:
        thread.join()
    
    while not resultQueue.empty():
        results.append(resultQueue.get())
        
    generation = []
    for subList in results:
        generation.extend(subList)
        
    return generation

def main():

    while True:
        
        global previousTime, startTime, deltaTime
        
        # Update Objects
        
        nn.generation = threadedUpdateEnv(nn.generation)
            
        print(nn.generation[0]["frames alive"])
        
        # Reset everything for new generation

        if nn.generation[0]["frames alive"] % nn.generationLength == 0:
            
            deltaTime = time.time() - previousTime
            previousTime = time.time()
            
            if nn.generation[0]["frames alive"]/nn.generationLength == 5:
                exit()
            
            print(f'Generation {nn.generation[0]["frames alive"]/nn.generationLength:.0f}')
            print(f"generation took {(deltaTime):.2f} seconds")
            
            nn.generation = nn.sortGenerationByFitness(nn.generation)
            
            print(f"fitness: {(nn.generation[0]["fitness"]/100000)*100:.2f}%")
            print("most recent mutation:", nn.generation[0]["most recent mutation"])
            nn.printNodesInfo(nn.generation[0]["agent"])
            
            if nn.generation[0]["frames alive"]/nn.generationLength != 1:
                # Open a file for writing in binary mode
                with open(f'generation.txt', 'wb') as file:#{int(nn.generation[0]["frames alive"]/nn.generationLength)}.txt', 'wb') as file:
                    # Pickle the list and write it to the file
                    pickle.dump(nn.generation[0], file)
            
            nn.nextGeneration = copy.deepcopy(nn.generation[:int(len(nn.generation) * 0.3)])
            
            agentsToMutate = random.choices(copy.deepcopy(nn.generation), weights=[agent["fitness"] if agent["fitness"] > 1 else 1 for agent in nn.generation],k= int(len(nn.generation) * 0.7))
            
            mutatedAgents = nn.mutateAgents(agentsToMutate)
            
            nn.nextGeneration.extend(mutatedAgents)
                                        
            nn.generation = copy.deepcopy(nn.nextGeneration)
            
            """for agent in nn.generation:
                print(agent["agent"][-1].id, agent["agent"][-1].parents)"""
            
            """for i, agent in enumerate(nn.generation):
                if any(any(node.parents) in node.children for node in agent["agent"]):
                    print("ERROR: CYCLE DETECTED IN AGENT", i)
                    print(agent["most recent mutation"])
                    nn.printNodesInfo(agent["agent"])"""
            
            for agent in nn.generation:
                agent["agent"] = nn.sortNodes(agent["agent"])
                print(agent["agent"][-1].id, agent["agent"][-1].parents)
                agent["fitness"] = 0
                
if __name__ == "__main__":
    main()