import pygame
import physics
import math
import numpy as np

def drawObjects(screen, centreCoord):
    
    for ball in physics.balls:
        
        coordinate = (ball.position[0] + centreCoord[0], centreCoord[1] - ball.position[1])
        radius = ball.size
        colour = ball.color
        
        pygame.draw.circle(screen, colour, coordinate, radius)
    
    for link in physics.links:
        
        coordinate1 = (link.ball1.position[0] + centreCoord[0], centreCoord[1] - link.ball1.position[1])
        coordinate2 = (link.ball2.position[0] + centreCoord[0], centreCoord[1] - link.ball2.position[1])
        thickness = link.thickness
        colour = link.colour
        
        pygame.draw.line(screen, colour, coordinate1, coordinate2, width=thickness)

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
        ballCount = len(physics.balls)
    textSurface1 = font.render("FPS:" + str(fps), False, (255, 255, 255))
    screen.blit(textSurface1, (0,0))
    
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