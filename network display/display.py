import pygame
from neural_network import node, printNodesInfo
import physics
import math
import numpy as np

def drawObjects(screen, centreCoord):
    
    for link in physics.links:
        
        coordinate1 = (link.ball1.position[0] + centreCoord[0], centreCoord[1] - link.ball1.position[1])
        coordinate2 = (link.ball2.position[0] + centreCoord[0], centreCoord[1] - link.ball2.position[1])
        thickness = link.thickness
        colour = link.colour
        
        pygame.draw.line(screen, colour, coordinate1, coordinate2, width=thickness)
        
    for object in physics.balls:
        
        coordinate = (object.position[0] + centreCoord[0], centreCoord[1] - object.position[1])
        radius = object.size
        colour = object.colour
        
        pygame.draw.circle(screen, colour, coordinate, radius)

i = 0
fps = 0
def updateFrame(screen, centreCoord, font):
    global i, fps
    i+=1

    screen.fill((0, 0, 0))
    
    drawObjects(screen,centreCoord)
    
    pygame.display.flip()

def main():
    
    pygame.init()

    screen = pygame.display.set_mode((860, 640), pygame.RESIZABLE)
    
    pygame.font.init()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    
    drawObjects(screen, (screen.get_width()/2, screen.get_height()/2))

    pygame.display.flip()

    while True:

        centreCoord = (screen.get_width()/2, screen.get_height()/2)
        
        # Update Objects
        physics.main()

        # Update Screen
        updateFrame(screen,centreCoord, font)
        
        # Check if user has quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
if __name__ == "__main__":
    main()