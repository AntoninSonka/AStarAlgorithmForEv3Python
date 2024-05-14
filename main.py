#!/usr/bin/env pybricks-micropython
import os
import time
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile



SIZE_Y = 4
SIZE_X = 4


def is_wall(walls, button, sensor, neighborY, neighborX):
    while button.pressed() == False:
        x = 1
    if sensor.distance(False) <= 100:
        walls[neighborY][neighborX] = 1
        return True
    return False


def calculate_h_cost(currentY, currentX, finishY, finishX):
    y = (finishY - currentY)
    x = (finishX - currentX)

    if y < 0:
        y *= -1
    if x < 0:
        x *= -1

    return y + x


def calculate_g_cost(currentY, currentX, parentListY, parentListX, startY, startX):
    gCost = 0

    while currentY != startY or currentX != startX:
        oldCurrentY = currentY
        oldCurrentX = currentX
        currentY = parentListY[oldCurrentY][oldCurrentX]
        currentX = parentListX[oldCurrentY][oldCurrentX]
        gCost += 1
    return gCost


def is_in_list(currentY, currentX, listY, listX):
    for i in range(0, len(listY)):
        if currentY == listY[i] and currentX == listX[i]:
            return i
    return -1


def get_lowest_f_y(openY, openX, fCostList, finishY, finishX):
    lowestF = 2000
    returnY = 0
    for i in range(0, len(openY)):
        if fCostList[openY[i]][openX[i]] < lowestF:
            lowestF = fCostList[openY[i]][openX[i]]
            returnY = openY[i]
    lowestH = 2000
    for i in range(0, len(openY)):
        if fCostList[openY[i]][openX[i]] == lowestF:
            h = calculate_h_cost(openY[i], openX[i], finishY, finishX)
            if h < lowestH:
                lowestH = h
                returnY = openY[i]
    return returnY


def get_lowest_f_x(openY, openX, fCostList, finishY, finishX):
    lowestF = 2000
    returnX = 0
    for i in range(0, len(openX)):
        if fCostList[openY[i]][openX[i]] < lowestF:
            lowestF = fCostList[openY[i]][openX[i]]
            returnX = openX[i]
    lowestH = 2000
    for i in range(0, len(openX)):
        if fCostList[openY[i]][openX[i]] == lowestF:
            h = calculate_h_cost(openY[i], openX[i], finishY, finishX)
            if h < lowestH:
                lowestH = h
                returnX = openX[i]
    return returnX


def calculate_neighbour(currentY, currentX, neighborY, neighborX, openY, openX, closedY, closedX, walls, parentListY, parentListX, fCostList, startY, startX, finishY, finishX, button, button2, sensor, skipRide, ev3):
    if neighborY < 0 or neighborY >= SIZE_Y:
        return
    if neighborX < 0 or neighborX >= SIZE_X:
        return
    if is_in_list(neighborY, neighborX, closedY, closedX) != -1:
        return
    if skipRide == False:
        ev3.speaker.beep(523.25, 250)
        ev3.speaker.beep(392.00, 250)
        ev3.speaker.beep(329.63, 250)
        ev3.speaker.beep(261.63, 250)  # checking for walls
        if is_wall(walls, button, sensor, neighborY, neighborX):
            ev3.speaker.beep(261.63, 500)
            ev3.speaker.beep(523.25, 500)  # there is a wall
            return
        else:
            ev3.speaker.beep(523.25, 500)
            ev3.speaker.beep(261.63, 500)  # there isn't a wall
            while button.pressed() == False:
                if button2.pressed() == True:
                    ev3.speaker.beep(392.00, 250)
                    return
    else:
        if walls[neighborY][neighborX]:
            return
    if is_in_list(neighborY, neighborX, openY, openX) == -1:
        parentListY[neighborY][neighborX] = currentY
        parentListX[neighborY][neighborX] = currentX
        thisH = calculate_h_cost(neighborY, neighborX, finishY, finishX)
        thisG = calculate_g_cost(neighborY, neighborX, parentListY, parentListX, startY, startX)
        fCostList[neighborY][neighborX] = thisH + thisG
        if is_in_list(neighborY, neighborX, openY, openX) == -1:
            openY.append(neighborY)
            openX.append(neighborX)


def find_path(walls, parentListY, parentListX, fCostList, startY, startX, finishY, finishX, skipRide, motors, ev3, button, button2, sensor):
    openY = []
    openX = []
    closedY = []
    closedX = []
    openY.append(startY)
    openX.append(startX)
    thisH = calculate_h_cost(startY, startX, finishY, finishX)
    thisG = calculate_g_cost(startY, startX, parentListY, parentListX, startY, startX)
    fCostList[startY][startX] = thisH + thisG
    counter = 0
    oldCurrentY = startY
    oldCurrentX = startX
    while True:
        counter += 1
        currentY = get_lowest_f_y(openY, openX, fCostList, finishY, finishX)
        currentX = get_lowest_f_x(openY, openX, fCostList, finishY, finishX)
        if skipRide == False:
            ride_to_tile(openY, openX, closedY, closedX, currentY, currentX, oldCurrentY, oldCurrentX, motors, ev3, button, button2, sensor)
        index = is_in_list(currentY, currentX, openY, openX)
        openY.pop(index)           
        openX.pop(index)
        closedY.append(currentY)
        closedX.append(currentX)
        if currentY == finishY and currentX == finishX:
            break
        # ev3.speaker.beep(261.63, 250)
        # ev3.speaker.beep(329.63, 250)
        # ev3.speaker.beep(392.00, 250)
        # ev3.speaker.beep(523.25, 250)
        neighborY = currentY - 1
        neighborX = currentX
        calculate_neighbour(currentY, currentX, neighborY, neighborX, openY, openX, closedY, closedX, walls, parentListY, parentListX, fCostList, startY, startX, finishY, finishX, button, button2, sensor, skipRide, ev3)
        if skipRide == False:
            motors.turn(90)
        neighborY = currentY
        neighborX = currentX + 1
        calculate_neighbour(currentY, currentX, neighborY, neighborX, openY, openX, closedY, closedX, walls, parentListY, parentListX, fCostList, startY, startX, finishY, finishX, button, button2, sensor, skipRide, ev3)
        if skipRide == False:
            motors.turn(90)
        neighborY = currentY + 1
        neighborX = currentX
        calculate_neighbour(currentY, currentX, neighborY, neighborX, openY, openX, closedY, closedX, walls, parentListY, parentListX, fCostList, startY, startX, finishY, finishX, button, button2, sensor, skipRide, ev3)
        if skipRide == False:
            motors.turn(90)
        neighborY = currentY
        neighborX = currentX - 1
        calculate_neighbour(currentY, currentX, neighborY, neighborX, openY, openX, closedY, closedX, walls, parentListY, parentListX, fCostList, startY, startX, finishY, finishX, button, button2, sensor, skipRide, ev3)
        if skipRide == False:
            motors.turn(90)
        oldCurrentY = currentY
        oldCurrentX = currentX

    currentY = finishY
    currentX = finishX

    while currentY != startY or currentX != startX:
        originalY = currentY
        originalX = currentX
        currentY = parentListY[originalY][originalX]
        currentX = parentListX[originalY][originalX]

        if currentY < originalY:
            # ev3.speaker.beep(261.63, 250)
            motors.straight(270)
        if currentX > originalX:
            # ev3.speaker.beep(329.63, 250)
            motors.turn(90)
            motors.straight(270)
            motors.turn(-90)
        if currentY > originalY:
            # ev3.speaker.beep(392.00, 250)
            motors.turn(180)
            motors.straight(270)
            motors.turn(-180)
        if currentX < originalX:
            # ev3.speaker.beep(523.25, 250)
            motors.turn(-90)
            motors.straight(270)
            motors.turn(90)
       
        ev3.speaker.beep(130.81, 500)
        while(button.pressed() == False):
            b = 1


def ride_to_tile(openY, openX, closedY, closedX, newStartY, newStartX, newFinishY, newFinishX, motors, ev3, button, button2, sensor):
    walls = [
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1]
            ]
    parentListY = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
            ]
    parentListX = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
            ]
    fCostList = [
            [2000, 2000, 2000, 2000],
            [2000, 2000, 2000, 2000],
            [2000, 2000, 2000, 2000],
            [2000, 2000, 2000, 2000]
            ]
    for i in range(0, len(openY)):
        walls[openY[i]][openX[i]] = False
    for i in range(0, len(closedY)):
        walls[closedY[i]][closedX[i]] = False
    walls[newStartY][newStartX] = False
    walls[newFinishY][newFinishX] = False
    find_path(walls, parentListY, parentListX, fCostList, newStartY, newStartX, newFinishY, newFinishX, 1, motors, ev3, button, button2, sensor)


walls = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ]
parentListY = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ]
parentListX = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]
        ]
fCostList = [
        [2000, 2000, 2000, 2000],
        [2000, 2000, 2000, 2000],
        [2000, 2000, 2000, 2000],
        [2000, 2000, 2000, 2000]
        ]


levy = Motor(Port.A)
pravy = Motor(Port.D)

motors = DriveBase(levy, pravy, 45, 270)
motors.settings(900, 300, 80, 60)
ev3 = EV3Brick()

button = TouchSensor(Port.S2)
button2 = TouchSensor(Port.S3)

sensor = UltrasonicSensor(Port.S1)


ev3.speaker.beep(130.81, 500)  # code upload done
while(button.pressed() == False):
    x = 1
ev3.speaker.beep(523.25, 500) # program start


startY = 0
startX = 2

finishY = 3
finishX = 2

find_path(walls, parentListY, parentListX, fCostList, startY, startX, finishY, finishX, 0, motors, ev3, button, button2, sensor)

ev3.speaker.beep(261.63, 250)
ev3.speaker.beep(329.63, 250)
ev3.speaker.beep(392.00, 250)
ev3.speaker.beep(523.25, 250)