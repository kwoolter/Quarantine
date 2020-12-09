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

    RESOURCES_DIR = os.path.dirname(__file__) + "\\resources\\"

    TRANSPARENT = (0, 255, 0)

    def __init__(self, model: model.QModel):

        super().__init__()

        self._debug = False

        self.model = model
        self.surface = None
        self.width = 800
        self.height = 800
        self._debug = False

        # Components
        self.location_view = LocationView(model, width=self.width,height=self.height)
        self.player_view = PlayerView(model.player, width=self.width,height=self.height)

        self.set_mode(QMainFrame.MODE_READY)


    def initialise(self):

        super().initialise()

        self.location_view.initialise()
        self.player_view.initialise()

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


    def update(self):
        pygame.display.update()

    def end(self):
        pygame.quit()
        print("Ending {0}".format(__class__))

    def tick(self):
        super().tick()

    def process_event(self, new_event: model.Event):
        self.location_view.process_event(new_event)

    def set_mode(self, new_mode: str):
        self.mode = new_mode

