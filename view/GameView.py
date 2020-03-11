import logging
import pygame

import view.ViewConstants as props
from view.BasicView import BasicView
from view.IsoElements import Block, BlockGroup, Camera
from controller.ControllerView import ControllerGameView


def create_playing_field(group: BlockGroup, window: pygame.display):
    for i in range(0, 10, 1):
        for j in range(0, 10, 1):
            group.add(Block(window, i, j, 0))

    for i in range(1, 6, 1):
        group.add(Block(window, 0, 0, i))
        group.add(Block(window, 9, 0, i))
        group.add(Block(window, 0, 9, i))
        group.add(Block(window, 9, 9, i))

    for i in range(1, 9, 1):
        group.add(Block(window, i, 0, 4))
        group.add(Block(window, i, 9, 4))
        group.add(Block(window, 0, i, 4))
        group.add(Block(window, 9, i, 4))


class GameView(BasicView):

    def __init__(self, window: pygame.display, controller: ControllerGameView):
        super().__init__(window, controller)
        self.window_width, self.window_height = pygame.display.get_surface().get_size()

        self.block_group = BlockGroup()
        create_playing_field(self.block_group, self.window)
        self.camera = Camera(camera_speed=.5)

    def draw(self):
        self.window.fill((50, 50, 50))

        self.camera.move_camera(pygame.key.get_pressed(), self.block_group)
        self.block_group.draw(window=self.window)
        pygame.display.update()
        pygame.display.flip()

    def receive_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.camera.center(self.block_group)

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            self.trafo_to_world_coords(pos[0], pos[1])

    def trafo_to_world_coords(self, x, y):
        # todo, sieht bisher mal ganz gut, der konstante offset muss mal noch raus
        offsetX, offsetY = self.camera.getTrans()
        # parameter for tilesize!
        b = h = 64
        #woher kommen die konstanten offset -24 und 6?
        xTrans = int(1 / b * x + 2 / b * y - offsetX) - 24
        yTrans = int(-1 / h * x + 2 / h * y - offsetY) + 6
        logging.info("xTrans= " + str(xTrans) + " yTrans= " + str(yTrans))
