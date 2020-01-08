import pygame
from pygame.locals import *

import sys

#todo introduce layers!

# idee for das design des clients!
# https://python-forum.io/Thread-PyGame-Simple-code-for-isometric-2D-games

WINDOW_SIZE = (660, 660)


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
    def __init__(self,x,y,z):
        self.block = pygame.image.load("block.png")
        self.base = pygame.image.load("base.png")
        self.x = x
        self.y = y
        self.z = z
        self.__TILEWIDTH = 32
        self.__TILEHEIGHT = 32

    def draw_block(self,screen,tileImage):
        m_x = screen.get_rect().centerx
        m_y = screen.get_rect().centery
        v_x = self.x * self.__TILEWIDTH / 2 - self.y * self.__TILEHEIGHT / 2 + m_x
        v_y = self.x * self.__TILEWIDTH / 4 + self.y * self.__TILEHEIGHT / 4 - self.z * self.__TILEHEIGHT / 2 + m_y / 2
        screen.blit(tileImage,(v_x,v_y))


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





class Camera:

    def __init__(self,camera_speed=1.0,x_factor=.5,y_factor=1):
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


def getPlayingField(group):
    for i in range(0,10,1):
        for j in range(0,10,1):
            group.add(Block(i,j,0))
    for i in range(0,10,1):
        for j in range(0,10,1):
            group.add(Block(i,j,1))

    for i in range(2,6,1):
        group.add(Block(0,0,i))
        group.add(Block(9, 0, i))
        group.add(Block(0, 9, i))
        group.add(Block(9, 9, i))



def main():
    pygame.init()

    # erstelle screen
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Isometric view test")
    clock = pygame.time.Clock()

    blockGroup = BlockGroup()
    getPlayingField(blockGroup)

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

