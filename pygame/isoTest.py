import pygame
from pygame.locals import *

import sys

#todo introduce layers!

# idee for das design des clients!
# https://python-forum.io/Thread-PyGame-Simple-code-for-isometric-2D-games

WINDOW_SIZE = (660, 660)
TILEWIDTH = 32
TILEHEIGHT = 32

FPS = 60.0

block = None
base = None

# the data for the map expressed as [row[tile]].
map_data = [
    [1, 1, 1, 0, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 1]
]

class Block:
    def __init__(self,x,y):
        self.block = pygame.image.load("block.png")
        self.base = pygame.image.load("base.png")
        self.x = x
        self.y = y

    def draw_block(self,screen,tileImage):
        world_x = self.x * TILEWIDTH/2
        world_y = self.y * TILEHEIGHT/2
        iso_x = (world_x - world_y)
        iso_y = (world_x + world_y) / 2
        centered_x = screen.get_rect().centerx + iso_x
        centered_y = screen.get_rect().centery /2 + iso_y
        screen.blit(tileImage,(centered_x,centered_y))


class BlockGroup:
    def __init__(self):
        self.list = []

    def add(self,block):
        self.list.append(block)

    def translation(self,x,y):
        for _,block in enumerate(self.list):
            block.x += x
            block.y += y

    def draw(self,screen):
        for _,block in enumerate(self.list):
            block.draw_block(screen,block.block)


def draw_floor(screen):
    for row_nb, row in enumerate(map_data):
        for col_nb, tile in enumerate(row):
            # checken ob da ne Wand steht
            if tile == 1:
                tileImage = block
            else:
                tileImage = base
            world_x = row_nb * TILEWIDTH / 2
            world_y = col_nb * TILEHEIGHT / 2
            iso_x = (world_x - world_y)
            iso_y = (world_x + world_y) / 2
            centered_x = screen.get_rect().centerx + iso_x
            centered_y = screen.get_rect().centery / 2 + iso_y
            screen.blit(tileImage, (centered_x, centered_y))



class Camera:

    def __init__(self,camera_speed=1,x_factor=.5,y_factor=1):
        self.__xTrans__ = 0
        self.__yTrans__ = 0
        self.__xFactor__ = x_factor
        self.__yFactor__ = y_factor
        self.camera_speed = camera_speed


    def move_camera(self, keys, blockGroup):
        vx = self.camera_speed * self.__xFactor__
        vy = self.camera_speed * self.__yFactor__

        if keys[pygame.K_a]:
            blockGroup.translation(-vx, vx)
            self.__xTrans__ -= vx
            self.__yTrans__ += vx
        if keys[pygame.K_d]:
            blockGroup.translation(vx, -vx)
            self.__xTrans__ += vx
            self.__yTrans__ -= vx
        if keys[pygame.K_w]:
            blockGroup.translation(-vy, -vy)
            self.__xTrans__ -= vy
            self.__yTrans__ -= vy
        if keys[pygame.K_s]:
            blockGroup.translation(vy, vy)
            self.__xTrans__ += vy
            self.__yTrans__ += vy

    def center(self,blockgroup):
        blockgroup.translation(-self.__xTrans__,-self.__yTrans__)
        self.__xTrans__ = 0
        self.__yTrans__ = 0


def main():
    pygame.init()

    # erstelle screen
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Isometric view test")
    clock = pygame.time.Clock()

    blockGroup = BlockGroup()
    blockGroup.add(Block(25,25))
    blockGroup.add(Block(24, 26))
    blockGroup.add(Block(25, 26))
    blockGroup.add(Block(24, 25))

    cam = Camera(camera_speed=.5)



    while True:
        #clear screen
        screen.fill((0,0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    cam.center(blockGroup)

        #naive kamera
        cam.move_camera(pygame.key.get_pressed(), blockGroup)

        #draw_floor(screen)
        #szene muss immer von oben an gezeichnet werden, damit nur dinge sichtbar sind, die man auch sehen kann!
        blockGroup.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()

