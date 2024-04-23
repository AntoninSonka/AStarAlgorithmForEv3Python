# #!/usr/bin/env pybricks-micropython
# import os
# import time
# from pybricks.hubs import EV3Brick
# from pybricks.ev3devices import (Motor, TouchSensor, UltrasonicSensor)
# from pybricks.parameters import Port, Stop, Direction, Button, Color
# from pybricks.tools import wait, StopWatch, DataLog
# from pybricks.robotics import DriveBase
# from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

SIZE_Y = 4
SIZE_X = 4


def calculate_h(startY, startX, finishY, finishX):
    hY = finishY - startY
    hX = finishX - startX
    if hY < 0:
        hY *= -1
    if hX < 0:
        hX *= -1
    return hY + hX


def calculate_g(currentY, currentX, parentListY, parentListX, startY, startX):
    g = 0
    while currentY != startY or currentX != startX:
        oldCurrentY = currentY
        oldCurrentX = currentX
        currentY = parentListY[oldCurrentY][oldCurrentX]
        currentX = parentListX[oldCurrentY][oldCurrentX]
        g += 1
    return g


def get_lowest_f_y(openY, openX, fList):
    lowestF = 2000
    returnY = 0
    for i in range(0, len(openY)):
        if fList[openY[i]][openX[i]] < lowestF:
            lowestF = fList[openY[i]][openX[i]]
            returnY = openY[i]
    return returnY


def get_lowest_f_x(openY, openX, fList):
    lowestF = 2000
    returnX = 0
    for i in range(0, len(openY)):
        if fList[openY[i]][openX[i]] < lowestF:
            lowestF = fList[openY[i]][openX[i]]
            returnX = openX[i]
    return returnX


def find_path(startY, startX, finishY, finishX, parentListY, parentListX, fList, skipRide):
    openY = []
    openX = []
    closedY = []
    closedX = []
    openY.append(startY)
    openX.append(startX)
    h = calculate_h(startY, startX, finishY, finishX)
    g = calculate_g(startY, startX, parentListY, parentListX, finishY, finishX)
    fList[startY][startX] = h + g
    while True:
        currentY = get_lowest_f_y(openY, openX, fList)
        currentX = get_lowest_f_x(openY, openX, fList)
        if skipRide == False:
