## Run using Python 3 with the pygame and numpy packages installed. (random and time are standard libraries).

import numpy
import pygame
import random
import time
pygame.init()


map_locations=[]
f=open("map.txt")
r=f.read()
f.close()
for col in r.split("\n"):
    col_locs=[]
    for c in col:
        if c=="#":
            col_locs.append(False)
        else:
            col_locs.append(True)
    map_locations.append(col_locs)

## Note that the map will be rotated 90 degrees from what it is in the txt file.


width,height=len(map_locations),len(map_locations[0])
robot_width,robot_height=25,25
screen=pygame.display.set_mode((robot_width*width,robot_height*height))

##################################################################################

## The idea behind my C* algorithm (C* for Camacho!) is as follows:
## It goes backwards from the point we want to go to, and gives
## directions to the adjacent squares around it. Then these squares
## do the same, and so forth until much of the board is filled.
## This can take in multiple locations that you want to get to!

## It is basically a backwards breadth first search, but it computes
## the best direction for every place on the map, instead of just
## one location.s

def c_star(initial_locations,good_locations,max_depth=100):
    locations_from=initial_locations
    location_directions=[[[] for i in range(height)] for j in range(width)]
    while max_depth>0 and len(locations_from)>0:
                
        for i in range(len(locations_from)):
            loc=locations_from.pop(0)
            good_locations[loc[0]][loc[1]]=False
            location_directions[loc[0]+1][loc[1]].append([-1,0])
            location_directions[loc[0]-1][loc[1]].append([1,0])
            location_directions[loc[0]][loc[1]+1].append([0,-1])
            location_directions[loc[0]][loc[1]-1].append([0,1])
            if good_locations[loc[0]+1][loc[1]]:
                locations_from.append((loc[0]+1,loc[1]))
                good_locations[loc[0]+1][loc[1]]=False
            if good_locations[loc[0]-1][loc[1]]:
                locations_from.append((loc[0]-1,loc[1]))
                good_locations[loc[0]-1][loc[1]]=False
            if good_locations[loc[0]][loc[1]+1]:
                locations_from.append((loc[0],loc[1]+1))
                good_locations[loc[0]][loc[1]+1]=False
            if good_locations[loc[0]][loc[1]-1]:
                locations_from.append((loc[0],loc[1]-1))
                good_locations[loc[0]][loc[1]-1]=False
        max_depth-=1
    return location_directions

############################################################################################
## Gives a visual for the c_star algorithm. Uncomment the code to run it.

"""
directions=c_star([[7,19]],[i[:] for i in map_locations])
for i in range(width):
    for j in range(height):
        if map_locations[i][j]:
            screen.fill((255,255,255),(i*robot_width,j*robot_height,robot_width,robot_height))
        else:
            screen.fill((255,0,0),(i*robot_width,j*robot_height,robot_width,robot_height))


for i in range(width):
    for j in range(height):
        if directions[i][j]==[]:
            continue
        if directions[i][j][0]==[-1,0]:
            pygame.draw.polygon(screen,(0,0,0),
            (
                (int((i+0.5)*robot_width),int(j*robot_height)),
                (int((i)*robot_width),int((j+0.5)*robot_height)),
                (int((i+0.5)*robot_width),int((j+1)*robot_height))

                )
                                )
        elif directions[i][j][0]==[1,0]:
            pygame.draw.polygon(screen,(0,0,0),
            (
                (int((i+0.5)*robot_width),int(j*robot_height)),
                (int((i+1)*robot_width),int((j+0.5)*robot_height)),
                (int((i+0.5)*robot_width),int((j+1)*robot_height))

                )
                                )
        elif directions[i][j][0]==[0,-1]:
            pygame.draw.polygon(screen,(0,0,0),
            (
                (int((i)*robot_width),int((j+0.5)*robot_height)),
                (int((i+0.5)*robot_width),int((j)*robot_height)),
                (int((i+1)*robot_width),int((j+0.5)*robot_height))

                )
                                )
        elif directions[i][j][0]==[0,1]:
            pygame.draw.polygon(screen,(0,0,0),
            (
                (int((i)*robot_width),int((j+0.5)*robot_height)),
                (int((i+0.5)*robot_width),int((j+1)*robot_height)),
                (int((i+1)*robot_width),int((j+0.5)*robot_height))

                )
                                )
pygame.display.update()
"""

##################################################################################
## This swarm code uses the c_star algorithm to move the robots. It shows how
## efficient that c_star can be getting robots to a destination.

"""
robot_positions=[]
open_positions=[i[:] for i in map_locations]
goal_pos=(19,19)
directions=c_star([goal_pos],[i[:] for i in map_locations])
list_of_times=[]
while True:
    while len(robot_positions)<20:
        x=random.randint(1,20)
        y=random.randint(1,20)
        if open_positions[x][y]:
            robot_positions.append((x,y))
            open_positions[x][y]=False
    start_time=time.time()
    for num,robot_pos in enumerate(robot_positions):
        x,y=robot_pos
        if x==goal_pos[0] and y==goal_pos[1]:
            continue
        for d in directions[x][y][0:2]:
            if open_positions[x+d[0]][y+d[1]]:
                robot_positions[num]=(x+d[0],y+d[1])
                open_positions[x+d[0]][y+d[1]]=False
                open_positions[x][y]=True
                break
        open_positions[goal_pos[0]][goal_pos[1]]=True
    end_time=time.time()
    list_of_times.append((end_time-start_time)*1000000)
    print(round(sum(list_of_times)/len(list_of_times),10))
    
    for i in robot_positions:
        if i==goal_pos:
            robot_positions.remove(i)

    ## Blitting

    for i in range(width):
        for j in range(height):
            if map_locations[i][j]==False:
                screen.fill((255,0,0),(i*robot_width,j*robot_height,robot_width,robot_height))
            elif open_positions[i][j]==False:
                screen.fill((0,255,0),(i*robot_width,j*robot_height,robot_width,robot_height))
            elif i==goal_pos[0] and j==goal_pos[1]:
                screen.fill((0,0,0),(i*robot_width,j*robot_height,robot_width,robot_height))
            else:
                screen.fill((255,255,255),(i*robot_width,j*robot_height,robot_width,robot_height))
    pygame.display.update()
    pygame.event.pump()
    pygame.time.wait(100)
"""

##################################################################################
## This utilizes the A* algorithm. The "guessed" distance between two
## points is just the taxicab distance (also known as Manhattan distance).

def taxicab_distance(start_position,end_position):
    return abs(start_position[0]-end_position[0])+abs(start_position[1]-end_position[1])

def a_star(initial_location, end_location, good_positions, max_depth=1000):
    open_set=[initial_location]
    came_from=[[[None,None] for j in i] for i in good_positions]
    gscore=[[1000 for j in i] for i in good_positions]
    gscore[initial_location[0]][initial_location[1]]=0
    fscore=[[1000 for j in i] for i in good_positions]
    fscore[initial_location[0]][initial_location[1]]=taxicab_distance(initial_location,end_location)
    while len(open_set)>0:
        if max_depth==0:
            return None
        max_depth-=1
        smallest_pos=open_set[0]
        smallest_f=fscore[open_set[0][0]][open_set[0][1]]
        for pos in open_set:
            f=fscore[pos[0]][pos[1]]
            if f<smallest_f:
                smallest_f=f
                smallest_pos=pos
        good_positions[smallest_pos[0]][smallest_pos[1]]=False
        open_set.remove(smallest_pos)
        for direction in [(-1,0),(1,0),(0,-1),(0,1)]:
            pos=(smallest_pos[0]+direction[0],smallest_pos[1]+direction[1])
            tentative_gscore=gscore[smallest_pos[0]][smallest_pos[1]]+1
            if good_positions[pos[0]][pos[1]]:
                if not pos in open_set:
                    open_set.append(pos)
                if tentative_gscore<gscore[pos[0]][pos[1]]:
                    came_from[pos[0]][pos[1]]=smallest_pos
                    gscore[pos[0]][pos[1]]=tentative_gscore
                    fscore[pos[0]][pos[1]]=gscore[pos[0]][pos[1]]+taxicab_distance(pos,end_location)
    
    
    if came_from[end_location[0]][end_location[1]]==[None,None]:
        return None
    path=[]
    loc=end_location
    while loc!=initial_location:
        path.append(loc)
        loc=came_from[loc[0]][loc[1]]
    path=path[::-1]
    return path

##################################################################################
## This gives a visual for the A* algorithm. To run, uncomment the code.

"""
robot_positions=[]
open_positions=[i[:] for i in map_locations]
goal_pos=(19,19)
list_of_times=[]
while True:
    while len(robot_positions)<20:
        x=random.randint(1,20)
        y=random.randint(1,20)
        if open_positions[x][y]:
            robot_positions.append((x,y))
            open_positions[x][y]=False
    start_time=time.time()
    for num,robot_pos in enumerate(robot_positions):
        if robot_pos==goal_pos:
            continue
        path=a_star(robot_pos,goal_pos,[i[:] for i in open_positions])
        if path!=None:
            pos=path[0]
            robot_positions[num]=pos
            open_positions[pos[0]][pos[1]]=False
            open_positions[robot_pos[0]][robot_pos[1]]=True
            open_positions[goal_pos[0]][goal_pos[1]]=True
            continue
        path=a_star(robot_pos,goal_pos,[i[:] for i in map_locations])
        if path!=None:
            pos=path[0]
            if open_positions[pos[0]][pos[1]]:
                robot_positions[num]=pos
                open_positions[pos[0]][pos[1]]=False
                open_positions[robot_pos[0]][robot_pos[1]]=True
                open_positions[goal_pos[0]][goal_pos[1]]=True
    end_time=time.time()
    list_of_times.append(int((end_time-start_time)*1000))
    print(round(sum(list_of_times)/len(list_of_times),2))
    for i in robot_positions:
        if i[0]==goal_pos[0] and i[1]==goal_pos[1]:
            robot_positions.remove(i)

    ## Blitting

    for i in range(width):
        for j in range(height):
            if map_locations[i][j]==False:
                screen.fill((255,0,0),(i*robot_width,j*robot_height,robot_width,robot_height))
            elif open_positions[i][j]==False:
                screen.fill((0,255,0),(i*robot_width,j*robot_height,robot_width,robot_height))
            elif i==goal_pos[0] and j==goal_pos[1]:
                screen.fill((0,0,0),(i*robot_width,j*robot_height,robot_width,robot_height))
            else:
                screen.fill((255,255,255),(i*robot_width,j*robot_height,robot_width,robot_height))
    pygame.display.update()
    pygame.event.pump()
    pygame.time.wait(50)
"""

##################################################################################
