from pygame.locals import *
import pygame
from time import sleep
import sys
from typing import List

def isSafe(row: int, col: int, 
           m: List[List[int]],co:int, ro: int,
           visited: List[List[bool]]) -> bool:

    if (row == -1 or row == ro or 
        col == -1 or col == co or 
        visited[row][col] or m[row][col] == 0):
        return False

    return True

def printPathUtil(row: int, col: int, 
                  m: List[List[int]], co: int,
                  ro: int, path: str,
                  possiblePaths: List[str], 
                  visited: List[List[bool]]) -> None:

    if (row == -1 or row == ro or 
        col == -1 or col == co or
        visited[row][col] or m[row][col] == 0):
        return

    if (row == ro - 1 and col == co - 1):
        possiblePaths.append(path)
        return

    visited[row][col] = True

    if (isSafe(row + 1, col, m, co, ro, visited)):
        path += 'D'
        printPathUtil(row + 1, col, m, co, ro, 
                      path, possiblePaths, visited)
        path = path[:-1]

    if (isSafe(row, col - 1, m, co, ro, visited)):
        path += 'L'
        printPathUtil(row, col - 1, m, co, ro, 
                      path, possiblePaths, visited)
        path = path[:-1]

    if (isSafe(row, col + 1, m, co, ro, visited)):
        path += 'R'
        printPathUtil(row, col + 1, m,co, ro,
                      path, possiblePaths, visited)
        path = path[:-1]

    if (isSafe(row - 1, col, m, co, ro, visited)):
        path += 'U'
        printPathUtil(row - 1, col, m, co, ro,
                      path, possiblePaths, visited)
        path = path[:-1]

    visited[row][col] = False

def printPath(m: List[List[int]], ro: int) -> None:

    co = len(m[0])
    possiblePaths = []
    path = ""
    visited = [[False for _ in range(co)] for _ in range(ro)]
                   
    printPathUtil(0, 0, m, co, ro, path, 
                  possiblePaths, visited)

    return possiblePaths

class Config:
    def __init__(self, file):
        self.maze = self.bacaFile(file)
        self.lebar = len(self.maze[0])
        self.tinggi = len(self.maze)
    
    def bacaFile(self, file):
        i = []
        try:
            with open(file) as f:
                for l in f:
                    j = []
                    for c in l:
                        if c!='\n':
                            j.append(int(c))
                    i.append(j)
        except FileNotFoundError:
            print("File tidak ditemukan!")
            exit()
        return i

class Player:
    x = 0
    y = 0
    speed = 44
 
    def moveRight(self):
        self.x = self.x + self.speed
 
    def moveLeft(self):
        self.x = self.x - self.speed
 
    def moveUp(self):
        self.y = self.y - self.speed
 
    def moveDown(self):
        self.y = self.y + self.speed
 
class Maze:
    def __init__(self, maze):
       self.maze = maze
    
    def draw(self,display_surf,image_surf):
        
        for i in range(len(self.maze)):
            for j in range(len(self.maze[i])):
                if self.maze[i][j] == 0:
                    display_surf.blit(image_surf,( (j*44 , i*44)))

class App:
 
    def __init__(self, maze, lebar, tinggi, sol):
        self._running = True
        self._display_surf = None
        self._image_surf = None
        self._block_surf = None
        self.windowWidth = lebar*44
        self.windowHeight = tinggi*44
        self.player = Player()
        self.maze = Maze(maze)
        self.solusi = sol[0]
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode((self.windowWidth,self.windowHeight), pygame.HWSURFACE)
        
        pygame.display.set_caption('Maze')
        self._running = True
        self._image_surf = pygame.image.load("player.png").convert()
        self._block_surf = pygame.image.load("block.png").convert()
 
    def on_event(self, event):
        if event.type == QUIT:
            self._running = False
    
    def on_render(self):
        self._display_surf.fill((0,0,0))
        self._display_surf.blit(self._image_surf,(self.player.x,self.player.y))
        self.maze.draw(self._display_surf, self._block_surf)
        pygame.display.flip()
 
    def on_cleanup(self):
        pygame.quit()
    
    def run(self):
        for i in self.solusi:
            pygame.event.pump()
            sleep(2)
            if i == 'R':
                self.player.moveRight()
            elif i == 'L':
                self.player.moveLeft()
            elif i == 'U':
                self.player.moveUp()
            elif i == 'D':
                self.player.moveDown()
            self.on_render()
            
        
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
        #self.on_init()
        print("-----------------------------")
        print("|  TEKAN SPASI UNTUK MULAI  |")
        print("|  TEKAN ESC UNTUK KELUAR   |")
        print("-----------------------------")
        while(self._running):
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[K_ESCAPE]):
                self._running = False
            
            if (keys[K_SPACE]):
                self.run()

            #for event in pygame.event.get():
            #    if event.type == pygame.QUIT:
            #        sys.exit()

            self.on_render()
        self.on_cleanup()
 
if __name__ == "__main__" :
    name = input("Input nama file matrix dari maze:")
    conf = Config(name)
    statespacetree = printPath(conf.maze, len(conf.maze))
    if not statespacetree:
        print("Maze tidak memiliki solusi!")
    else:
        theApp = App(conf.maze, conf.lebar, conf.tinggi, statespacetree)
        theApp.on_execute()
