import neural_network_parallel as nn
import copy
import cupy
import pygame

solverVariable = nn.physics.solver()

numOfAgents = 10
subSteps = 10
framesPerGen = 10000 # in frames of environment 100 fps for 100s so 10000
emptyArray = cupy.zeros((numOfAgents,))

keyboard = {}
movementSpeed = 100

def get_key(key):
    try:
        return keyboard[key]
    except KeyError:
        return False

cartPosX = copy.deepcopy(emptyArray)
cartVelX = copy.deepcopy(emptyArray)

stickPosX = copy.deepcopy(emptyArray)
stickPosY = cupy.full((numOfAgents,), -100.)
oldStickPosX = copy.deepcopy(emptyArray)
oldStickPosY = copy.deepcopy(stickPosY)
stickAccX = copy.deepcopy(emptyArray)
stickAccY = cupy.full((numOfAgents,), -100)
angularVelocity = copy.deepcopy(emptyArray)

fitness = copy.deepcopy(emptyArray)
mostRecentMutation = ["" for _ in range(numOfAgents)]

def init(cartPosX, stickPosX, stickPosY):
    
    pygame.init()

    screen = pygame.display.set_mode((860, 640), pygame.RESIZABLE)
    
    
    drawObjects(screen, (screen.get_width()/2, screen.get_height()/2), cartPosX, stickPosX, stickPosY)

    pygame.display.flip()
        
    return screen

def updateFrame(screen, centreCoord, cartPosX, stickPosX, stickPosY):

    screen.fill((0, 0, 0))
    
    drawObjects(screen,centreCoord, cartPosX, stickPosX, stickPosY)
    
    pygame.display.flip()
    
def drawObjects(screen, centreCoord, cartPosX, stickPosX, stickPosY):

    stickCoord = (centreCoord[0] + int(stickPosX[0]), centreCoord[1] - int(stickPosY[0]))
    cartCoord = (centreCoord[0] + int(cartPosX[0]), centreCoord[1])
    
    pygame.draw.line(screen, (0, 255, 0), stickCoord, cartCoord, width=5)
    
    pygame.draw.circle(screen, (255, 0, 0), (cartCoord), 10)
            
def main(cartPosX, stickPosX, stickPosY, cartVelX, oldStickPosX, oldStickPosY, stickAccX, stickAccY, subSteps, solverVariable):
    
    screen = init(cartPosX, stickPosX, stickPosY)
    frames = 0
    
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                keyboard[event.key] = True
            elif event.type == pygame.KEYUP:
                keyboard[event.key] = False
                
        centreCoord = (screen.get_width()/2, screen.get_height()/2)
        
        if get_key(pygame.K_LEFT):
            cartVelX = cupy.full((numOfAgents,), -movementSpeed)
        elif get_key(pygame.K_RIGHT):
            cartVelX = cupy.full((numOfAgents,), movementSpeed)
        if get_key(pygame.K_LEFT) and get_key(pygame.K_RIGHT) or not get_key(pygame.K_LEFT) and not get_key(pygame.K_RIGHT):
            cartVelX = cupy.full((numOfAgents,), 0)
        
        if frames == 3:
            pass
        frames += 1
        
        stickPosX, stickPosY, angularVelocity, cartPosX, oldStickPosX, oldStickPosY = nn.physics.main(cartPosX, stickPosX, stickPosY, cartVelX, oldStickPosX, oldStickPosY, stickAccX, stickAccY, subSteps, solverVariable)
                
        updateFrame(screen,centreCoord, cartPosX, stickPosX, stickPosY)

if __name__ == "__main__":
    main(cartPosX, stickPosX, stickPosY, cartVelX, oldStickPosX, oldStickPosY, stickAccX, stickAccY, subSteps, solverVariable)