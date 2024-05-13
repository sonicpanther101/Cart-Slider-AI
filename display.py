import pygame
import physics
import neural_network as nn
import numpy as np
import random
import pickle
import copy

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

def main():
    
    """pygame.init()

    screen = pygame.display.set_mode((860, 640), pygame.RESIZABLE)
    
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    
    drawObjects(screen, (screen.get_width()/2, screen.get_height()/2))

    pygame.display.flip()"""

    while True:

        #               centreCoord = (screen.get_width()/2, screen.get_height()/2)
        
        # Update Objects
        
        for agentID, environment in enumerate(physics.environments):
            
            # Update Physics frame
            
            physics.main(environment)
            
            # get NN output
            
            position = physics.environment["balls"][0].position[0]
            xDirection = physics.environment["balls"][0].position[0] - physics.environment["balls"][1].position[0]
            yDirection = physics.environment["balls"][0].position[1] - physics.environment["balls"][1].position[1]
            angularVelocity = physics.environment["balls"][1].angularVelocity
            
            nn.generation[agentID]["agent"][0].value = position
            nn.generation[agentID]["agent"][1].value = xDirection
            nn.generation[agentID]["agent"][2].value = yDirection
            nn.generation[agentID]["agent"][3].value = angularVelocity
            
            nn.generation[agentID]["agent"] = nn.calculateNodes(nn.generation[agentID]["agent"])
            
            output = nn.generation[agentID]["agent"][-1].value
            
            nn.generation[agentID]["agent"] = nn.resetNodes(nn.generation[agentID]["agent"])
            
            if physics.j % 100 == 0:
                pass#print(f'agent {agentID}\ny of pendulum: {physics.environment["balls"][1].position[1]}\noutput: {output}')
            
            environment["extraForce"] = output
            
            # update fitness
            
            nn.generation[agentID]["fitness"] += nn.fitness(physics.environment["balls"][1].position[1])
        
        # Reset Objects for new generation

        if physics.j % nn.generationLength == 0:
            
            print(f'Generation {physics.j/nn.generationLength}')
            
            if physics.j/nn.generationLength != 1:
                # Open a file for writing in binary mode
                with open(f'generation{int(physics.j/nn.generationLength)}.txt', 'wb') as file:
                    # Pickle the list and write it to the file
                    pickle.dump(nn.generation, file)
            
            nn.nextGeneration = copy.deepcopy(nn.generation[:int(len(nn.generation) * 0.3)])
            
            agentsToMutate = random.choices(copy.deepcopy(nn.generation), weights=[agent["fitness"] for agent in nn.generation],k= int(len(nn.generation) * 0.7))
            
            mutatedAgents = nn.mutateAgents(agentsToMutate)
            
            nn.nextGeneration.extend(mutatedAgents)
            
            nn.generation = copy.deepcopy(nn.nextGeneration)
            
            nn.generation = nn.sortGenerationByFitness(nn.generation)

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