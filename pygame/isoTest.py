import pygame
from pygame.locals import  *

import sys

#idee for das design des clients!
#https://python-forum.io/Thread-PyGame-Simple-code-for-isometric-2D-games

WINDOW_SIZE = (660,660)


TILEWIDTH = 32
TILEHEIGHT = 32

FPS = 60.0

wall = None
grass = None

# the data for the map expressed as [row[tile]].
map_data = [
    [1,1,1,0,1,1,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,0],
    [1,1,1,1,1,0,0],
    [0,0,0,1,0,0,1]
]

def draw_floor(screen):
    for row_nb,row in enumerate(map_data):
        for col_nb, tile in enumerate(row):
            #checken ob da ne Wand steht
            if tile == 1:
                tileImage = wall
            else:
                tileImage = grass
            world_x = row_nb * TILEWIDTH / 2
            world_y = col_nb * TILEHEIGHT / 2
            iso_x = (world_x - world_y)
            iso_y = (world_x + world_y) / 2
            centered_x = screen.get_rect().centerx + iso_x
            centered_y = screen.get_rect().centery / 2 + iso_y
            screen.blit(tileImage,(centered_x,centered_y))

def init():
    global wall, grass
    wall = pygame.image.load("block.png")
    grass = pygame.image.load("base.png")

def main():
    pygame.init()

    #erstelle screen
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Isometric view test")
    clock = pygame.time.Clock()

    init()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        draw_floor(screen)

        pygame.display.flip()
        clock.tick(FPS)




if __name__ == "__main__":
    main()
