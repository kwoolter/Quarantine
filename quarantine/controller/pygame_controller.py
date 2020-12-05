import os
import pygame
import sys
from pygame.locals import *

import quarantine.model as model
import quarantine.view as view


class QController:
    def __init__(self):
        self.model = None
        self.view = None

    def initialise(self):
        view.View.image_manager.initialise()
        self.model = model.QModel("Quarantine")
        self.view = view.QMainFrame(self.model)

        self.model.initialise()
        self.view.initialise()

    def end(self):
        self.model.end()
        self.view.end()


    def run(self):

        os.environ["SDL_VIDEO_CENTERED"] = "1"

        FPSCLOCK = pygame.time.Clock()

        # Model tick timer
        pygame.time.set_timer(USEREVENT + 1, 15)

        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, USEREVENT])

        loop = True

        while loop is True:

            self.model.tick()
            self.view.draw()
            self.view.update()

            # Loop to process pygame events
            for event in pygame.event.get():

                # Timer events for the model to process
                if event.type == USEREVENT + 1:
                    pass

                # Quit event
                if event.type == QUIT:
                    loop = False

            FPSCLOCK.tick(60)

        self.end()
