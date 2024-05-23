import pygame
import asyncio
import network_display_physics as network_display_physics

def drawObjects(screen, centreCoord):
    
    for link in network_display_physics.links:
        
        coordinate1 = (link.ball1.position[0] + centreCoord[0], centreCoord[1] - link.ball1.position[1])
        coordinate2 = (link.ball2.position[0] + centreCoord[0], centreCoord[1] - link.ball2.position[1])
        thickness = link.thickness
        colour = link.colour
        
        pygame.draw.line(screen, colour, coordinate1, coordinate2, width=thickness)
        
    for ball in network_display_physics.balls:
        
        coordinate = (ball.position[0] + centreCoord[0], centreCoord[1] - ball.position[1])
        radius = ball.size
        colour = ball.colour
        
        pygame.draw.circle(screen, colour, coordinate, radius)

i = 0
fps = 0
networkScreen = 0

def updateFrame(screen, centreCoord):
    global i, fps
    i+=1

    screen.fill((0, 0, 0))
    
    drawObjects(screen,centreCoord)
    
    pygame.display.flip()

def init():
    
    pygame.init()

    screen = pygame.display.set_mode((860, 640), pygame.RESIZABLE)
    
    
    drawObjects(screen, (screen.get_width()/2, screen.get_height()/2))

    pygame.display.flip()
        
    return screen
    
def main(screen):
    
    network_display_physics.getNewNetwork()

    for i in range(10):
        centreCoord = (screen.get_width()/2, screen.get_height()/2)
        
        # Update Objects
        network_display_physics.main()

        # Update Screen
        updateFrame(screen,centreCoord)
                
#main(screen)

"""while True:
    # Check if user has quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()"""