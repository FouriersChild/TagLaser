import numpy as np
import pygame

def generateMaze(width, height):
    #input type: int, int
    #output type: list

    grids = width * height
    maze = []
    visited = []
    toVisit = []

    visited.append(0)
    toVisit.append((0,1))
    toVisit.append((0, width))

    while len(toVisit) > 0:
        randomIndex = np.random.randint(len(toVisit))
        nextPath = toVisit.pop(randomIndex)

        if nextPath[1] in visited:
            continue
        if nextPath[0] > nextPath[1]:
            maze.append((nextPath[1], nextPath[0]))
        else:
            maze.append(nextPath)
        
        visited.append(nextPath[1])

        above = nextPath[1] - width
        if above > 0 and not above in visited:
            toVisit.append((nextPath[1], above))

        left = nextPath[1] - 1
        if left % width != width - 1 and not left in visited:
            toVisit.append((nextPath[1], left))

        right = nextPath[1] + 1
        if right % width != 0 and not right in visited:
            toVisit.append((nextPath[1], right))

        below = nextPath[1] + width
        if below < grids and not below in visited:
            toVisit.append((nextPath[1], below))
    return maze

def getWallsFromMaze(maze, width, height, probMirror):
    final = np.zeros((2*width+1, 2*height + 1))
    final[0,0] = 3
    for x in range(width):
        final[0,1+2*x] = randMirror(probMirror)
    for x in range(width):
        final[0,2+2*x] = 3
    for x in range(height):
        final[1+2*x,0] = randMirror(probMirror)
    for x in range(height):
        final[2+2*x,0] = 3

    for y in range(height):
        for x in range(width):
            pos = np.array([1,1])+ 2* np.array([x,y])
            current = y*width + x
            lower = ((y+1)* width) + x
            if not (current, lower) in maze:
                final[pos[0],pos[1]+1] = 1
            if not (current, current + 1) in maze:
                final[pos[0]+1,pos[1]] = 1
            final[pos[0]+1, pos[1]+1] = 3
    return final

def randMirror(probMirror):
    randNum = np.random.rand()
    if randNum <= probMirror:
        return 1
    else: 
        return 2

def getRectWallsFromMaze(maze, width, height, wallwidth, wallheight, probMirror):
    maze = getWallsFromMaze(maze, width, height, probMirror)
    final = []
    yPos = 0
    xPos = 0
    for y in range(len(maze)):
        currHeight = maze[y][0]
        for x in range(len(maze[0])):
            
            current = maze[y][x]
            if current == 0:
                if x % 2 ==0:
                    xPos += wallwidth
                else:
                    xPos += wallheight

            elif current == 1 or current == 2:
                if currHeight == 3:
                    rect = pygame.Rect((xPos,yPos),(wallheight, wallwidth))
                    final.append(rect)
                    xPos += wallheight
                elif currHeight == 1 or currHeight == 2:
                    rect = pygame.Rect((xPos,yPos),(wallwidth, wallheight))
                    final.append(rect)
                    xPos += wallwidth
            else:
                rect = pygame.Rect((xPos,yPos),(wallwidth, wallwidth))
                final.append(rect)
                xPos += wallwidth
        
        if currHeight == 3:
            yPos += wallwidth
        else:
            yPos += wallheight
        if y != len(maze) -1:
            xPos = 0
    xPos += wallwidth
    return final, (xPos, yPos)