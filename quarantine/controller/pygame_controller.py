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
    GAME_MODE_PLAYER = "player"
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
        self.model.initialise()

        self.view = view.QMainFrame(self.model)
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
            action = self.process_start_events(new_event)

            # Game playing actions
            pause = action.get('pause')

            if pause:
                self.set_mode(QController.GAME_MODE_PLAYING)

        elif self.mode == QController.GAME_MODE_PLAYING:
            action = self.process_playing_events(new_event)

            # Game playing actions
            select = action.get('select')
            pause = action.get('pause')
            number_selection = action.get("select_number")
            f_number_selection = action.get("select_F_number")
            view_selection = action.get("view selection")
            object_action = action.get("action")
            debug = action.get("debug")
            new_mode = action.get("new mode")


            if select:
                new_loc = self.view.location_view.get_selected_new_location()
                self.model.current_location = new_loc
                self.view.location_view.initialise()
            elif object_action:

                obj = None

                if object_action == "USE":
                    obj = self.view.location_view.get_selected_object()
                elif object_action == "USE LEFT":
                    objs = self.model.get_objects_at_location("Left Hand")
                    if len(objs) >= 1:
                        obj = objs[0]
                        object_action = "USE"
                elif object_action == "USE RIGHT":
                    objs = self.model.get_objects_at_location("Right Hand")
                    if len(objs) >= 1:
                        obj = objs[0]
                        object_action = "USE"

                if obj is not None:
                    self.model.perform_action(obj.name, object_action)

            elif pause:
                self.set_mode(QController.GAME_MODE_PAUSED)
            elif number_selection:
                self.view.location_view.set_next_location(number_selection)
            elif f_number_selection:
                self.view.location_view.set_selected_object(f_number_selection)
            elif view_selection:
                self.view.location_view.set_location_image(view_selection, increment=True)
            elif new_mode:
                self.set_mode(new_mode)
            elif debug:
                self.model.print()
        
        elif self.mode == QController.GAME_MODE_PAUSED:
            action = self.process_paused_events(new_event)

            # Game playing actions
            pause = action.get('pause')

            if pause:
                self.set_mode(QController.GAME_MODE_PLAYING)

        elif self.mode == QController.GAME_MODE_PLAYER:
            action = self.process_player_events(new_event)
            new_mode = action.get("new mode")
            if new_mode:
                self.set_mode(new_mode)

    def process_start_events(self, new_event):
        action = {}
        # Key UP events - less time critical actions
        if new_event.type == KEYUP:
            if new_event.key == K_SPACE:
                action = {"pause":True}
            elif new_event.key == K_RETURN:
                action = {"select":True}
            elif new_event.key >= K_1 and new_event.key <= K_9:
                action = {"select_number":new_event.key - K_1 + 1}
            elif new_event.key >= K_F1 and new_event.key <= K_F12:
                action = {"select_F_number":new_event.key - K_F1 + 1}


        return action

    def process_playing_events(self, new_event):
        action = {}
        # Key UP events - less time critical actions
        if new_event.type == KEYUP:
            if new_event.key == K_ESCAPE:
                action = {"pause":True}
            elif new_event.key == K_SPACE:
                action = {"action":"USE"}
            elif new_event.key == K_LSHIFT:
                action = {"action":"USE LEFT"}
            elif new_event.key == K_RSHIFT:
                action = {"action":"USE RIGHT"}
            elif new_event.key == K_RETURN:
                action = {"select":True}
            elif new_event.key >= K_1 and new_event.key <= K_9:
                action = {"select_number":new_event.key - K_1 + 1}
            elif new_event.key >= K_F1 and new_event.key <= K_F11:
                action = {"select_F_number":new_event.key - K_F1 + 1}
            elif new_event.key == K_LEFT:
                action = {"view selection": -1}
            elif new_event.key == K_RIGHT:
                action = {"view selection": 1}
            elif new_event.key == K_F12:
                action = {"debug": True}
            elif new_event.key == K_c:
                action = {"new mode": QController.GAME_MODE_PLAYER}


        return action

    def process_paused_events(self, new_event):
        action = {}
        # Key UP events - less time critical actions
        if new_event.type == KEYUP:
            if new_event.key == K_SPACE:
                action = {"pause": True}
        return action

    def process_player_events(self, new_event):
        action = {}
        # Key UP events - less time critical actions
        if new_event.type == KEYUP:
            if new_event.key == K_c:
                action = {"new mode": QController.GAME_MODE_PLAYING}

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

            elif new_mode == QController.GAME_MODE_PLAYER:
                self.view.set_mode(view.QMainFrame.MODE_PLAYER)
                self.model.set_mode(model.QModel.STATE_PAUSED)

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