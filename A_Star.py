#!usr/bin/env python

from tkinter import *
import time
import random


#Mahatan
def heuristic(a,b):
    dist = abs(b.i-a.i)+abs(b.j-a.j)
    return dist


class Spot: #Point
    def __init__(self,i,j):
        self.i = i
        self.j = j
        self.neighbors = list([])
        self.previous = 0 #tìm path
        self.f = 0 #tiêu chí lựa chọn điểm kế
        self.g = 0 #khoảng cách so với nhà
        self.h = 0 #khoảng cách so với đích
        self.wall=0

    def show(self,color):
        c.create_rectangle(self.i*w,self.j*h,self.i*w+w,self.j*h+h,fill=color)

    def addneighbors(self,grid):
        if (self.i<cols-1): self.neighbors.append(grid[self.i+1][self.j])
        if (self.i>0):  self.neighbors.append(grid[self.i-1][self.j])
        if (self.j<rows-1): self.neighbors.append(grid[self.i][self.j+1])
        if (self.j>0): self.neighbors.append(grid[self.i][self.j-1])
        # đường chéo
        if (self.i>0 and self.j>0): self.neighbors.append(grid[self.i-1][self.j-1])
        if (self.i < cols-1 and self.j>0): self.neighbors.append(grid[self.i+1][self.j-1])
        if (self.i>0 and self.j<rows-1): self.neighbors.append(grid[self.i-1][self.j+1])
        if (self.i < cols-1 and self.j<rows-1): self.neighbors.append(grid[self.i+1][self.j+1])



cols = 25
rows = 25
width = 400
height = 400
grid = [[0 for x in range(cols)] for y in range(rows)]
w = width / cols   # chiều rộng của pixel
h = height / rows  # chiều dài của pixel
root = Tk()
size = str(width)+'x'+str(height)
root.geometry(size) # "widthxheigh"
c = Canvas(root, height=400, width=400, bg='gray')
c.pack()
openset = []
closedset = [] # dùng để không xét trùng
path = []
# Making a 2D array
for i in range (rows):
    for j in range (cols):
        grid[i][j] = Spot(i,j)
# add All the neighbors
for i in range(rows):
    for j in range(cols):
        grid[i][j].addneighbors(grid)
# start and end
start = grid[0][0]
end = grid[cols-1][rows-1]
# openset starts with beginning only
openset.append(start)


def a_star_algorithm():
    if len(openset)>0:
        'We can keep going'
        winner=0
        while openset:
            for i in range(len(openset)):
                if(openset[i].f<openset[winner].f):
                    winner=i
            current = openset[winner]
            if current==end:
                print("DONE!") # console.log("DONE!")
                # Find the path
                path = []
                temp = current
                path.append(temp)
                while (temp.previous):
                    path.append(temp.previous)
                    temp = temp.previous
                return path
            openset.remove(current)
            closedset.append(current)
            neighbors = current.neighbors
            for i in range(len(neighbors)):
                neighbor = neighbors[i]
                if (neighbor not in closedset) and (neighbor.wall==0):
                    tempG = current.g+1
                    if neighbor in openset:
                        if tempG < neighbor.g:
                            neighbor.g = tempG
                    else:
                        neighbor.g = tempG
                        openset.append(neighbor)
                    neighbor.h=heuristic(neighbor,end)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.previous=current
    else:
        'no solution'
        path = []
        return path



def obstacle(startX,startY,width,height):
    for i in range(startX,startX+width):
        for j in range(startY,startY+height):
            if(startX+width<=cols-1 and startY+height<=rows-1):
                grid[i][j].wall=1
                grid[i][j].show('orange')
                c.update()

def draw_obstacle():
    number_of_rectangle = int(random.uniform(15,20))
    check = 0
    while (check != number_of_rectangle):
        #i1,j1, are the coordinate of rectangle / wid,hei are the size of rectangle
        i1 = int(random.uniform(5,cols-5))
        j1 = int(random.uniform(5,rows-5))
        wid = int(random.uniform(1,5))
        hei = int(random.uniform(1,5))
        if (i1+wid) <= (cols-5) and (j1+hei) <= (rows-5):
            obstacle(i1,j1,wid,hei)
            check +=1


# Draw current state of everything
end.show('yellow')
for i in range(rows):
    for j in range(cols):
        grid[i][j].show('white')
        c.update()
        #time.sleep(0.001)
draw_obstacle()
path = a_star_algorithm()

for i in range(len(closedset)):
    closedset[i].show('red')
    c.update()
    time.sleep(0.001)

for i in range(len(openset)):
    openset[i].show('green')
    c.update()
    time.sleep(0.001)

if len(path)>0:
    for i in range(len(path)):
        path[i].show('blue')
else:
    print("No path!")
start.show('magenta')
end.show('yellow')
root.mainloop()

'''
 print array
for i in range(rows):
    print(matrix[i])

matrix[1][1]=3
print(matrix[1][1])

for i in range(rows):
    print(matrix[i])
'''