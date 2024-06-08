import cupy, time
from cythonized import norm

class solver:
    
    def __init__(self):
        pass

    def update(self, deltaTime, cartPosX, stickPosX, stickPosY, cartVelX, oldStickPosX, oldStickPosY, stickAccX, stickAccY):
        stickPosX, stickPosY = applyLinks(cartPosX, stickPosX, stickPosY)
        cartPosX = updateCartPositions(deltaTime, cartVelX, cartPosX)
        stickPosX, stickPosY, angularVelocity, oldStickPosX, oldStickPosY = updateStickPositions(deltaTime, stickPosX, stickPosY, oldStickPosX, oldStickPosY, stickAccX, stickAccY, cartPosX)
        return stickPosX, stickPosY, angularVelocity, cartPosX, oldStickPosX, oldStickPosY

def applyLinks(cartPosX, stickPosX, stickPosY):
    axisX = cartPosX - stickPosX
    axisY = - stickPosY
    distance = cupy.sqrt(axisX**2 + axisY**2)
    normalX = axisX / distance
    normalY = axisY / distance
    delta = 100 - distance
        
    stickPosX = stickPosX - (normalX * delta)
    stickPosY = stickPosY - (normalY * delta)
        
    return stickPosX, stickPosY
    
    
def updateCartPositions(deltaTime, cartVelocity, cartPosX):
    cartPosX = cartPosX + cartVelocity * deltaTime
    cartPosX = cupy.clip(cartPosX, -250, 250)
    
    return cartPosX

def updateStickPositions(deltaTime, stickPosX, stickPosY, oldStickPosX, oldStickPosY, stickAccX, stickAccY, cartPosX):
    velocityX = stickPosX - oldStickPosX
    velocityY = stickPosY - oldStickPosY
    
    oldStickPosX = stickPosX[:]
    oldStickPosY = stickPosY[:]
    
    stickPosX = stickPosX + velocityX + stickAccX * deltaTime * deltaTime
    stickPosY = stickPosY + velocityY + stickAccY * deltaTime * deltaTime
    
    linearVelocityX = velocityX / deltaTime
    linearVelocityY = velocityY / deltaTime
    
    theta = (cupy.pi-calculateAngle(stickPosX - cartPosX, stickPosY))-(cupy.pi-calculateAngle(linearVelocityX, linearVelocityY))
    velocityTangential = cupy.sin(theta) * cupy.sqrt(linearVelocityX**2 + linearVelocityY**2)
    
    angularVelocity = velocityTangential / cupy.sqrt((stickPosX - cartPosX)**2 + stickPosY**2)
    
    return stickPosX, stickPosY, angularVelocity, oldStickPosX, oldStickPosY

def calculateAngle(listOfCoordX, listOfCoordY):
    
    # Allocate space for angles
    angle = cupy.zeros_like(listOfCoordX)
    
    mask = (listOfCoordX != 0) & (listOfCoordY != 0)
    angle[mask] = cupy.arctan2(listOfCoordY[mask], listOfCoordX[mask])
    
    mask = (listOfCoordX == 0) & (listOfCoordY != 0)
    angle[mask] = cupy.where(listOfCoordY > 0, cupy.pi / 2, 3 * cupy.pi / 2)
    
    mask = (listOfCoordY == 0) & (listOfCoordX != 0)
    angle[mask] = cupy.where(listOfCoordX > 0, 0, cupy.pi)
    
    angle = cupy.where(angle < 0, angle + 2 * cupy.pi, angle)
    
    return angle


previousTime = 0
startTime = time.time()
deltaTime = 0

def main(cartPosX, stickPosX, stickPosY, cartVelX, oldStickPosX, oldStickPosY, stickAccX, stickAccY, subSteps, solverVariable):
    global previousTime, startTime, deltaTime
    
    if previousTime == 0:
        previousTime = time.time()
    deltaTime = time.time() - previousTime #1/1000
    previousTime = time.time()
        
    for _ in range(subSteps):
        stickPosX, stickPosY, angularVelocity, cartPosX, oldStickPosX, oldStickPosY = solverVariable.update(deltaTime/subSteps, cartPosX, stickPosX, stickPosY, cartVelX, oldStickPosX, oldStickPosY, stickAccX, stickAccY)
        
    return stickPosX, stickPosY, angularVelocity, cartPosX, oldStickPosX, oldStickPosY