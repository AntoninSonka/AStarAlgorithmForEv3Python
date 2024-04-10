import os
import time


# startY = 0
# startX = 0

# finishY = 3
# finishX = 3

SIZE_Y = 4
SIZE_X = 4


def print_grid(walls, currentY, currentX, startY, startX, finishY, finishX):
    print()
    os.system('clear')
    for i in range(0, SIZE_Y):
        for j in range(0, SIZE_X):
            if walls[i][j]:
                print("X", end="")
            elif i == currentY and j == currentX:
                print("P", end="")
            elif i == startY and j == startX:
                print("S", end="")
            elif i == finishY and j == finishX:
                print("F", end="")
            else:
                print("0", end="")
        print()
    return


def calculate_h_cost(currentY, currentX, finishY, finishX):
    y = (finishY - currentY)
    x = (finishX - currentX)

    if y < 0:
        y *= -1
    if x < 0:
        x += -1

    return y + x


def calculate_g_cost(currentY, currentX, parentListY, parentListX, startY, startX):
    gCost = 0

    while currentY != startY or currentX != startX:
        oldCurrentY = currentY
        oldCurrentX = currentX
        # print("FROM G COST")
        # print("current")
        # print(currentY)
        # print(currentX)
        currentY = parentListY[oldCurrentY][oldCurrentX]
        currentX = parentListX[oldCurrentY][oldCurrentX]
        gCost += 1
    # print("gCost: ", gCost)
    # time.sleep(1)
    return gCost


def compare_g_costs(currentY, currentX, parentListY, parentListX, newParentY, newParentX, startY, startX):
    oldGCost = calculate_g_cost(currentY, currentX, parentListY, parentListX, startY, startX)
    oldParentY = parentListY[currentY][currentX]
    oldParentX = parentListX[currentY][currentX]
    parentListY[currentY][currentX] = newParentY
    parentListX[currentY][currentX] = newParentX
    newGCost = calculate_g_cost(currentY, currentX, parentListY, parentListX, startY, startX)
    parentListY[currentY][currentX] = oldParentY
    parentListX[currentY][currentX] = oldParentX
    if oldGCost < newGCost:
        return False
    return True


def is_in_list(currentY, currentX, listY, listX):
    for i in range(0, len(listY)):
        if currentY == listY[i] and currentX == listX[i]:
            return i
    return -1

def get_lowest_f_y(openY, openX, fCostList):
    lowestF = 2000
    returnY = 0
    for i in range(0, len(openY)):
        if fCostList[openY[i]][openX[i]] < lowestF:
            lowestF = fCostList[openY[i]][openX[i]]
            returnY = openY[i]
    return returnY


def get_lowest_f_x(openY, openX, fCostList):
    lowestF = 2000
    returnX = 0
    for i in range(0, len(openY)):
        if fCostList[openY[i]][openX[i]] < lowestF:
            lowestF = fCostList[openY[i]][openX[i]]
            returnX = openX[i]
    return returnX


def calculate_neighbour(currentY, currentX, neighborY, neighborX, openY, openX, closedY, closedX, walls, parentListY, parentListX, fCostList, startY, startX, finishY, finishX):
    if neighborY < 0 or neighborY >= SIZE_Y:
        # print("SIZE ISSUE IN calculate_heighbor")
        return
    if neighborX < 0 or neighborX >= SIZE_X:
        # print("SIZE ISSUE IN calculate_heighbor")
        return
    if is_in_list(neighborY, neighborX, closedY, closedX) != -1:
        # print("IS IN CLOSED ISSUE IN calculate_heighbor")
        return
    if walls[neighborY][neighborX]:
        # print("IS WALL ISSUE IN calculate_heighbor")
        return
    # print("PASSED ELIMINATION")
    isShorter = False
    # print("open FROM calculate_neighbor: ")
    # print(openY)
    # print(openX)
    if is_in_list(neighborY, neighborX, openY, openX) != -1:
        # print("COMPARING G COST IN PROCESS")
        isShorter = False # compare_g_costs(neighborY, neighborY, parentListY, parentListX, currentY, currentX, startY, startX)
        # print("COMPARING G COST HAPPEND")
    if isShorter or is_in_list(neighborY, neighborX, openY, openX) == -1:
        # print("IS SHORTER OR IS NOT IN OPEN")
        # print("GRID: ")
        # print_grid(walls, neighborY, neighborX, startY, startX, finishY, finishX)
        parentListY[neighborY][neighborX] = currentY
        parentListX[neighborY][neighborX] = currentX
        thisH = calculate_h_cost(neighborY, neighborX, finishY, finishX)
        thisG = calculate_g_cost(neighborY, neighborX, parentListY, parentListX, startY, startX)
        fCostList[neighborY][neighborX] = thisH + thisG
        if is_in_list(neighborY, neighborX, openY, openX) == -1:
            openY.append(neighborY)
            openX.append(neighborX)
            # print("APPENDED FROM calculate_neighbor")
            # print("open:")
            # print(openY)
            # print(openX)


def find_path(walls, parentListY, parentListX, fCostList, startY, startX, finishY, finishX, skipRide):
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
    # print("+++++++++++++++++++++++++++++++")
    # if skipRide:
        # print("IS IN RIDE")
    # else:
        # print("NORMAL")
    # print(openY)
    # print(openX)
    while True:
        # print("counter: ", counter)
        counter += 1
        currentY = get_lowest_f_y(openY, openX, fCostList)
        currentX = get_lowest_f_x(openY, openX, fCostList)
        # print("\ncurrentY: ", currentY)
        # print("currentX: ", currentX)
        # print_grid(walls, currentY, currentX, startY, startX, finishY, finishX)
        if skipRide == False:
            ride_to_tile(openY, openX, closedY, closedX, currentY, currentX, oldCurrentY, oldCurrentX)
        index = is_in_list(currentY, currentX, openY, openX)
        # print("open FROM MAIN WHILE")
        # print(openY)
        # print(openX)
        #time.sleep(1)
        openY.pop(index)
        openX.pop(index)
        closedY.append(currentY)
        closedX.append(currentX)
        if currentY == finishY and currentX == finishX:
            print("PATH FOUND")
            break
        neighborY = currentY - 1
        neighborX = currentX
        calculate_neighbour(currentY, currentX, neighborY, neighborX, openY, openX, closedY, closedX, walls, parentListY, parentListX, fCostList, startY, startX, finishY, finishX)
        neighborY = currentY + 1
        neighborX = currentX
        calculate_neighbour(currentY, currentX, neighborY, neighborX, openY, openX, closedY, closedX, walls, parentListY, parentListX, fCostList, startY, startX, finishY, finishX)
        neighborY = currentY
        neighborX = currentX - 1
        calculate_neighbour(currentY, currentX, neighborY, neighborX, openY, openX, closedY, closedX, walls, parentListY, parentListX, fCostList, startY, startX, finishY, finishX)
        neighborY = currentY
        neighborX = currentX + 1
        calculate_neighbour(currentY, currentX, neighborY, neighborX, openY, openX, closedY, closedX, walls, parentListY, parentListX, fCostList, startY, startX, finishY, finishX)
        oldCurrentY = currentY
        oldCurrentX = currentX

    # print("=========================")

    currentY = finishY
    currentX = finishX

    print_grid(walls, currentY, currentX, startY, startX, finishY, finishX)
    time.sleep(1)

    while currentY != startY or currentX != startX:
        originalY = currentY
        originalX = currentX
        currentY = parentListY[originalY][originalX]
        currentX = parentListX[originalY][originalX]
        print_grid(walls, currentY, currentX, startY, startX, finishY, finishX)
        time.sleep(1)
    # print("END OF find_path")
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")


def ride_to_tile(openY, openX, closedY, closedX, newStartY, newStartX, newFinishY, newFinishX):
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
    # print("closed:")
    # print(closedY)
    # print(closedX)
    # print(len(closedY))
    for i in range(0, len(closedY)):
        walls[closedY[i]][closedX[i]] = False
    walls[newStartY][newStartX] = False
    walls[newFinishY][newFinishX] = False
    # print("GRID FROM ride_to_tile")
    # print_grid(walls, SIZE_Y, SIZE_X, newStartY, newStartX, newFinishY, newFinishX)
    find_path(walls, parentListY, parentListX, fCostList, newStartY, newStartX, newFinishY, newFinishX, 1)


walls = [
        [0, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 0, 1],
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

startY = 0
startX = 0

finishY = 3
finishX = 3

find_path(walls, parentListY, parentListX, fCostList, startY, startX, finishY, finishX, 0)
