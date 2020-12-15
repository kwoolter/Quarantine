import pygame
import os
import quarantine.model as model
from .game_views import *
from .graphics import *
import logging

class QMainFrame(View):

    MODE_READY = "ready"
    MODE_PLAYING = "playing"
    MODE_PLAYER = "player"
    MODE_PAUSED = "game paused"
    MODE_GAME_OVER = "game over"

    MODE_VISIBLE_OBJECTS = "visible objects"
    MODE_OBJECT_CONTENTS = "object contents"
    VIEW_OPTIONS = (MODE_VISIBLE_OBJECTS, MODE_OBJECT_CONTENTS)

    RESOURCES_DIR = os.path.dirname(__file__) + "\\resources\\"

    TRANSPARENT = (0, 255, 0)

    INVENTORY_SIZE = (140,140)

    def __init__(self, model: model.QModel):

        super().__init__()

        # Properties
        self.model = model
        self.surface = None
        self.width = 800
        self.height = 800
        self.mode = None
        self._debug = False

        # Components
        self.location_view = LocationView(model, width=self.width,height=self.height)
        self.player_view = PlayerView(model.player, width=100,height=100)

        inv_w, inv_h = QMainFrame.INVENTORY_SIZE
        self.left_hand_view = ObjectsView("Left Hand", width=inv_w, height=inv_h)
        self.right_hand_view = ObjectsView("Right Hand", width=inv_w, height=inv_h)

        self.set_mode(QMainFrame.MODE_READY)


    def initialise(self):

        super().initialise()

        self.location_view.initialise()
        self.player_view.initialise()

        left_hand_objects = self.model.get_objects_at_location("Left Hand")
        self.left_hand_view.initialise(left_hand_objects)

        right_hand_objects = self.model.get_objects_at_location("Right Hand")
        self.right_hand_view.initialise(right_hand_objects)


        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        pygame.display.set_caption(self.model.name)

        self.surface = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF | pygame.HWACCEL)

        filename = QMainFrame.RESOURCES_DIR + "icon.png"

        try:
            image = pygame.image.load(filename)
            image = pygame.transform.scale(image, (32,32))
            pygame.display.set_icon(image)
        except Exception as err:
            print(str(err))

    def print(self):

        print("Printing Quarantine view...")

    def draw(self):
        
        self.surface.fill(Colours.RED)
        self.surface.fill((0, 255, 0))

        pane_rect = self.surface.get_rect()

        x = 0
        y = 0

        if self.mode == QMainFrame.MODE_PLAYING:
            self.location_view.draw()
            self.surface.blit(self.location_view.surface, (0,0))

        elif self.mode == QMainFrame.MODE_PLAYER:
            self.player_view.draw()
            self.surface.blit(self.player_view.surface, (0,0))

        else:
            x = pane_rect.centerx
            y = pane_rect.centery
            draw_text(self.surface,
                      msg=f"{self.mode:^40}",
                      size=40,
                      x=x,
                      y=y)

        y = 400

        if self.mode == QMainFrame.MODE_PLAYING:
            self.left_hand_view.draw()
            self.surface.blit(self.left_hand_view.surface, (0, y))
            self.right_hand_view.draw()
            rh_rect = self.right_hand_view.surface.get_rect()
            rh_rect.right = pane_rect.right
            rh_rect.top = y
            self.surface.blit(self.right_hand_view.surface, rh_rect.topleft)

            self.player_view.draw()
            rect = self.player_view.surface.get_rect()
            rect.topright = pane_rect.topright
            self.surface.blit(self.player_view.surface, rect.topleft)

    def update(self):
        pygame.display.update()

    def end(self):
        pygame.quit()
        print("Ending {0}".format(__class__))

    def tick(self):
        super().tick()

    def process_event(self, new_event: model.Event):
        self.location_view.process_event(new_event)

        if new_event.name == model.Event.GAME_MODEL_CHANGED:
            self.initialise()

    def set_mode(self, new_mode: str):

        if new_mode in QMainFrame.VIEW_OPTIONS:
            self.location_view.set_mode((new_mode))
        else:
            self.mode = new_mode

    def set_option(self, new_option:str, option_value):
        self.options[new_option] = option_value

