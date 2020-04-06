import logging
import pygame

import view.ViewSettings as props
from view.BasicView import BasicView
from view.IsoElements import Block, BlockGroup, Camera
from view.ViewSettings import ViewSettings
from controller.ControllerView import ControllerGameView
from util.Transforms import Transformations


def create_playing_field(group: BlockGroup, window: pygame.display) -> None:
    """
    Methode used for testing, generates basic field to test transformations and so on
    :todo can be deleted as soon as scenario files can be read in
    :param group:
    :param window:
    :return:
    """
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

    def __init__(self, window: pygame.display, controller: ControllerGameView, settings: ViewSettings) -> None:
        super().__init__(window, controller, settings)
        self.window_width, self.window_height = pygame.display.get_surface().get_size()

        self.block_group = BlockGroup()
        create_playing_field(self.block_group, self.window)
        self.camera = Camera(camera_speed=.5)

    def draw(self) -> None:
        self.window.fill((50, 50, 50))

        self.camera.move_camera(pygame.key.get_pressed(), self.block_group)

        self.block_group.highlight_block_in_focus(self.camera.getTrans())
        self.block_group.draw(window=self.window)
        pygame.display.update()
        pygame.display.flip()

    def receive_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.camera.center(self.block_group)

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            offsetX, offsetY = self.camera.getTrans()
            xTrans, yTrans = Transformations.trafo_window_to_world_coords(pos[0], pos[1], offsetX, offsetY)
            logging.info("Pos: " + str(pos) + " OffsetX= " + str(offsetX) + " OffsetY= " + str(offsetY))
            logging.info("XTrans= " + str(xTrans) + " YTrans= " + str(yTrans))
