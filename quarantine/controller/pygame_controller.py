import os
import pygame
import sys
from pygame.locals import *

import quarantine.model as model
import quarantine.view as view


class QController:

    GAME_MODE_START = "start"
    GAME_MODE_INVENTORY = "inventory"
    GAME_MODE_PLAYING = "playing"
    GAME_MODE_PAUSED = "paused"
    GAME_MODE_GAME_OVER = "game over"


    def __init__(self):

        # Properties
        self._state = QController.GAME_MODE_START
        self.mode = QController.GAME_MODE_START

        # Components
        self.model = None
        self.view = None
        self.events = None

    def initialise(self):
        view.View.image_manager.initialise()
        self.model = model.QModel("Quarantine")
        self.view = view.QMainFrame(self.model)

        self.model.initialise()
        self.view.initialise()

        self.events = self.model.events
        
        self.set_mode(QController.GAME_MODE_START)

    def end(self):
        self.model.end()
        self.view.end()

    def run(self):

        os.environ["SDL_VIDEO_CENTERED"] = "1"

        FPSCLOCK = pygame.time.Clock()

        # Model tick timer
        pygame.time.set_timer(USEREVENT + 1, 1000)

        pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP, USEREVENT])

        loop = True

        while loop is True:

            self.view.draw()
            self.view.update()

            # Loop to process Quarantine game events
            event = self.model.get_next_event()
            while event is not None:

                try:
                    self.model.process_event(event)
                    self.view.process_event(event)

                except Exception as err:
                    print("Caught exception {0}".format(str(err)))

                if event.type == model.Event.QUIT:
                    loop = False
                    break

                event = self.model.get_next_event()


            # Loop to process pygame events
            for event in pygame.event.get():

                # Timer events for the model to process
                if event.type == USEREVENT + 1:
                    self.model.tick()

                # Quit event
                if event.type == QUIT:
                    loop = False

                self.process_event(event)

            FPSCLOCK.tick(60)

        self.end()


    def process_event(self, new_event):

        if self.mode == QController.GAME_MODE_START:
            action = self.process_playing_events(new_event)

            # Game playing actions
            pause = action.get('pause')

            if pause:
                self.set_mode(QController.GAME_MODE_PLAYING)

        elif self.mode == QController.GAME_MODE_PLAYING:
            action = self.process_playing_events(new_event)

            # Game playing actions
            pause = action.get('pause')

            if pause:
                self.set_mode(QController.GAME_MODE_PAUSED)
        
        elif self.mode == QController.GAME_MODE_PAUSED:
            action = self.process_paused_events(new_event)

            # Game playing actions
            pause = action.get('pause')

            if pause:
                self.set_mode(QController.GAME_MODE_PLAYING)


    def process_start_events(self, new_event):
        action = {}
        # Key UP events - less time critical actions
        if new_event.type == KEYUP:
            if new_event.key == K_SPACE:
                action = {"pause":True}

        return action

    def process_playing_events(self, new_event):
        action = {}
        # Key UP events - less time critical actions
        if new_event.type == KEYUP:
            if new_event.key == K_SPACE:
                action = {"pause":True}

        return action

    def process_paused_events(self, new_event):
        action = {}
        # Key UP events - less time critical actions
        if new_event.type == KEYUP:
            if new_event.key == K_SPACE:
                action = {"pause": True}
        return action

    def set_mode(self, new_mode):

        if new_mode != self.mode:

            self.last_mode = self.mode
            self.mode = new_mode

            if new_mode == QController.GAME_MODE_START:
                self.view.set_mode(view.QMainFrame.MODE_READY)
                self.model.set_mode(model.QModel.STATE_PAUSED)

            elif new_mode == QController.GAME_MODE_PLAYING:
                self.view.set_mode(view.QMainFrame.MODE_PLAYING)
                self.model.set_mode(model.QModel.STATE_PLAYING)

            elif new_mode == QController.GAME_MODE_PAUSED:
                self.view.set_mode(view.QMainFrame.MODE_PAUSED)
                self.model.set_mode(model.QModel.STATE_PAUSED)

            elif new_mode == QController.GAME_MODE_GAME_OVER:
                self.view.set_mode(view.QMainFrame.MODE_GAME_OVER)
                self.model.set_mode(model.QModel.STATE_PAUSED)

            if self.last_mode is not None:
                self.events.add_event(model.Event(type=model.Event.CONTROL,
                                                  name=model.Event.GAME_MODE_CHANGED,
                                                  description=f'Game mode changed from {self.last_mode.upper()} to {self.mode.upper()}'))