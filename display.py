#import pygame
import physics
import neural_network as nn
import random
import pickle
import copy
import time
import threading

def drawObjects(screen, centreCoord):
    
    for link in physics.links:
        
        coordinate1 = (link.ball1.position[0] + centreCoord[0], centreCoord[1] - link.ball1.position[1])
        coordinate2 = (link.ball2.position[0] + centreCoord[0], centreCoord[1] - link.ball2.position[1])
        thickness = link.thickness
        colour = link.colour
        
        pygame.draw.line(screen, colour, coordinate1, coordinate2, width=thickness)
        
    for ball in physics.balls:
        if ball.id == 0:
            
            width, height = ball.size, ball.size
            left, top = ball.position[0] + centreCoord[0] - width / 2, centreCoord[1] - ball.position[1] - height / 2
            colour = ball.color
            
            pygame.draw.rect(screen, colour, (left, top, width, height))

i = 0
fps = 0
ballCount = 0
def updateFrame(screen, centreCoord, font):
    global i, fps, ballCount
    i+=1

    screen.fill((0, 0, 0))
    
    drawObjects(screen,centreCoord)
    
    if i % 50 == 0:
        fps = int(1/physics.deltaTime if physics.deltaTime != 0 else fps)
    textSurface1 = font.render("FPS:" + str(fps), False, (255, 255, 255))
    screen.blit(textSurface1, (0,0))
    
    pygame.display.flip()


keyboard = {}

def get_key(key):
    try:
        return keyboard[key]
    except KeyError:
        return False

previousTime = 0
startTime = time.time()
deltaTime = 0
threadsToUse = 10

def main():
    
    """pygame.init()

    screen = pygame.display.set_mode((860, 640), pygame.RESIZABLE)
    
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    
    drawObjects(screen, (screen.get_width()/2, screen.get_height()/2))

    pygame.display.flip()"""

    while True:
        
        global previousTime, startTime, deltaTime

        #               centreCoord = (screen.get_width()/2, screen.get_height()/2)
        
        # Update Objects
        
        threads = []
        step = int(len(physics.environments)/threadsToUse)
        
        for i in range(threadsToUse):
            threads.append(threading.Thread(target=nn.stepForwardOneFrame, args=(physics.environments[step*i:step*(i+1)], step*i)))
            threads[-1].start()
            
        for thread in threads:
            thread.join()
        
        # Reset Objects for new generation

        if physics.environments[0]["frames"] % nn.generationLength == 0:
            
            deltaTime = time.time() - previousTime
            previousTime = time.time()
            
            if physics.environments[0]["frames"]/nn.generationLength == 5:
                exit()
            
            print(f'Generation {physics.environments[0]["frames"]/nn.generationLength:.0f}')
            print(f"generation took {(deltaTime):.2f} seconds")
            
            nn.generation = nn.sortGenerationByFitness(nn.generation)
            
            print(f"fitness: {(nn.generation[0]["fitness"]/100000)*100:.2f}%")
            print("most recent mutation:", nn.generation[0]["most recent mutation"])
            nn.printNodesInfo(nn.generation[0]["agent"])
            
            if physics.environments[0]["frames"]/nn.generationLength != 1:
                # Open a file for writing in binary mode
                with open(f'generation.txt', 'wb') as file:#{int(physics.environments[0]["frames"]/nn.generationLength)}.txt', 'wb') as file:
                    # Pickle the list and write it to the file
                    pickle.dump(nn.generation, file)
            
            nn.nextGeneration = copy.deepcopy(nn.generation[:int(len(nn.generation) * 0.3)])
            
            agentsToMutate = random.choices(copy.deepcopy(nn.generation), weights=[agent["fitness"] for agent in nn.generation],k= int(len(nn.generation) * 0.7))
            
            mutatedAgents = nn.mutateAgents(agentsToMutate)
            
            nn.nextGeneration.extend(mutatedAgents)
            
            for agent in nn.nextGeneration:
                print(agent["agent"][-1].id, agent["agent"][-1].parents)
                                        
            nn.generation[i] = copy.deepcopy(nn.nextGeneration[i])
            
            """for i, agent in enumerate(nn.generation):
                if any(any(node.parents) in node.children for node in agent["agent"]):
                    print("ERROR: CYCLE DETECTED IN AGENT", i)
                    print(agent["most recent mutation"])
                    nn.printNodesInfo(agent["agent"])"""
            
            for agent in nn.generation:
                agent["agent"] = nn.sortNodes(agent["agent"])
                agent["fitness"] = 0
                #print(agent["agent"][-1].id, agent["agent"][-1].parents)

        # Update Screen
        #                       updateFrame(screen,centreCoord, font)
        
        # Check if user has quit
        """for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                keyboard[event.key] = True
            elif event.type == pygame.KEYUP:
                keyboard[event.key] = False"""
                
if __name__ == "__main__":
    main()