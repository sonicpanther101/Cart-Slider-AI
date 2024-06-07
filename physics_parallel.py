import gnumpy
import numpy as np

def applyLinks(cartPosX, stickPosX, stickPosY):
    axisX = cartPosX - stickPosX
    axisY = gnumpy.array([0, 0]) - stickPosY