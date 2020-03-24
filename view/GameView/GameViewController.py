import logging
import pygame

# from view.GameView.GameView import GameView
from view.GameView.Drawable import DrawableGroup, Drawable, Block
from view.GameView.Camera import Camera
from util.Transforms import Transformations
from util.Coordinates import WorldPoint


def create_playing_field(group: DrawableGroup, window: pygame.display) -> None:
    """
    Methode used for testing, generates basic field to test transformations and so on
    :todo can be deleted as soon as scenario files can be read in
    :param group:
    :param window:
    :return:
    """
    for i in range(0, 10, 1):
        for j in range(0, 10, 1):
            group.add(Block(window, WorldPoint(i, j, 0)))

    for i in range(1, 6, 1):
        group.add(Block(window, WorldPoint(0, 0, i)))
        group.add(Block(window, WorldPoint(9, 0, i)))
        group.add(Block(window, WorldPoint(0, 9, i)))
        group.add(Block(window, WorldPoint(9, 9, i)))

    for i in range(1, 9, 1):
        group.add(Block(window, WorldPoint(i, 0, 4)))
        group.add(Block(window, WorldPoint(i, 9, 4)))
        group.add(Block(window, WorldPoint(0, i, 4)))
        group.add(Block(window, WorldPoint(9, i, 4)))


class GameViewController:
    def __init__(self, view):
        self.view = view
        self.camera = self.camera = Camera(camera_speed=.5)
        self.drawable_group = DrawableGroup()

        create_playing_field(self.drawable_group, self.view.window)

    def draw(self):
        self.camera.move_camera(pygame.key.get_pressed())
        self.drawable_group.highlight_drawable_in_focus(self.camera.getTrans())
        self.drawable_group.draw(self.view.window, self.camera.getTrans())

    def receive_event(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.camera.center()

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            offsetX, offsetY = self.camera.getTrans()
            xTrans, yTrans = Transformations.trafo_window_to_world_coords(pos[0], pos[1], offsetX, offsetY)
            logging.info("Pos: (%d,%d) OffsetX: %f OffsetY: %f" % (pos[0], pos[1], offsetX, offsetY))
            logging.info("XTrans: %d YTrans: %d" % (xTrans, yTrans))
