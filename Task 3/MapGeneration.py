from mazelib import Maze
from mazelib.generate.Prims import Prims
import numpy as np
import cv2 
import random
WINDOW_WIDTH = 51


def generateMap():
    m = Maze()
    m.set_seed(random.seed())
    m.generator = Prims(70,70)
    m.generate()
    
    maze_init = m.grid
    maze_init = maze_init.astype(np.float32)
    
    scale_factor = 4
    width = int(maze_init.shape[1] * scale_factor)
    height = int(maze_init.shape[0] * scale_factor)
    dim = (width, height)
    resized = cv2.resize(maze_init,dim,interpolation = cv2.INTER_NEAREST)
    
    kernel = np.ones((3, 3), np.uint8)
    resized = cv2.dilate(resized,kernel,2)
    resized = cv2.copyMakeBorder(resized,WINDOW_WIDTH//2,WINDOW_WIDTH//2,WINDOW_WIDTH//2,WINDOW_WIDTH//2,cv2.BORDER_CONSTANT)
    
    return resized

def generateRandomStart(Map):
    x=np.where(Map > 0)
    free_list = np.asarray(x).T
    start = random.choice(free_list)
    return start
    


























