from quarantine.model.events import Event
from quarantine.model.qtime import QTimer
from quarantine.model.qobject import *
from quarantine.model.qlocation import *
from quarantine.model.qmap import *
from quarantine.model.qpuzzles import *
from quarantine.model.game_qpuzzles import *
from quarantine.model.qplayer import *
import collections

class QModel:

    # Define states
    STATE_LOADED = "Game Loaded"
    STATE_READY = "Game Ready"
    STATE_PLAYING = "Game Playing"
    STATE_PAUSED = "Game Paused"
    STATE_GAME_OVER = "Game Over"

    def __init__(self, name : str):

        # Model properties
        self.name = name
        self._state = None
        self.timer = None

        # Model Components
        self.player = None
        self.events = EventQueue()
        self.current_location = None
        self.puzzles = None

        self.state = QModel.STATE_LOADED

    def print(self):
        print(f"Game:{self.name}")
        print(f"Player:{self.player}")
        self.puzzles.print()

    def initialise(self):
        self.state = QModel.STATE_READY
        self.timer = QTimer()

        # Initialise components
        self.player = QPlayer("Me")
        self.player.roll()

        QLocationFactory.load("locations.csv")
        QObjectFactory.load("objects.csv")
        QMapFactory.load("map.csv")
        self.puzzles = QGamePuzzleManager(self.player)

        start_location = "Doorway"

        self.current_location = QLocationFactory.get_object_by_name(start_location)

        self.events.add_event(Event(type=Event.GAME,
                                    name=Event.STATE_LOADED,
                                    description=f"Welcome {self.player.name} to {self.name}"))

    def pause(self):
        if self.state == QModel.STATE_PLAYING:
            self.state = QModel.STATE_PAUSED
        elif self.state == QModel.STATE_PAUSED:
            self.state = QModel.STATE_PLAYING

    def end(self):
        self.state = QModel.STATE_GAME_OVER

    def tick(self, increment:int = 1):

        if self.state == QModel.STATE_PLAYING:

            for i in range(increment):
                self.timer.tick()
                self.player.tick()
                self.perform_action("Game", "TICK")

            self.events.add_event(Event(type=Event.GAME,
                                        name=Event.TICK,
                                        description=f"Game model ticked by {increment}: Day {self.timer.day:02} {self.timer.hour:02}:{self.timer.minutes:02} state({self.state})"))

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        if new_state != self._state:
            self._old_state = self._state
            self._state = new_state
            self.events.add_event(Event(type=Event.STATE,
                                        name=self.state,
                                        description="Game state changed to {0}".format(self.state)))

    def set_mode(self, new_mode):
        self.state = new_mode

    def get_next_event(self):
        next_event = None
        if self.events.size() > 0:
            next_event = self.events.pop_event()

        return next_event

    def process_event(self, new_event):
        print("Default Game event process:{0}".format(new_event))

    def get_light_at_location(self, location_name:str = None):

        if location_name is None:
            location = self.current_location
        else:
            location = QLocationFactory.get_object_by_name(location_name)

        alpha = 255

        is_light = location.get_property("IsLight")
        hour = self.timer.hour

        if is_light is False:
            alpha = int(255 * (1 - abs(1 - (hour/12))))

        alpha = max(min(alpha, 255),10)

        #print(f"{location.name}:light={is_light}, time={hour}, alpha = {alpha}")

        return alpha

    def get_objects_at_location(self, location_name:str = None):
        if location_name is None:
            location_name = self.current_location.name

        return QObjectFactory.get_objects_by_location(location_name)

    def perform_action(self, obj:str, action:str):

        inputs = {}

        inputs[QPuzzle.INPUT_LOCATION] = self.current_location.name
        inputs[QPuzzle.INPUT_HOUR] = self.timer.hour
        inputs[QPuzzle.INPUT_DAY] = self.timer.day
        inputs[QPuzzle.INPUT_PLAYER_STATE] = self.player.state
        inputs[QPuzzle.INPUT_OBJECT] = obj
        inputs[QPuzzle.INPUT_ACTION] = action

        success = self.puzzles.evaluate_puzzles(inputs)

        if success is False:
            for puzzle, output in self.puzzles.errors.items():
                print(f"{puzzle}:{output}")
            # self.events.add_event(Event(type=Event.GAME,
            #                             name=Event.ACTION_FAILED,
            #                             description=f"Nothing happens when you {action} {obj}"))
        else:
            for puzzle, output in self.puzzles.outputs.items():
                print(f"{puzzle}:{output}")
                for k,v in output.items():
                    if k in QPlayer.PROPERTIES:
                        self.player.set_property(k, v, increment=True)

                    elif k == QPuzzle.OUTPUT_TIME_DELTA:
                        self.tick(v)
                        #self.timer.tick(v)

                    elif k == QPuzzle.OUTPUT_OBJECT:
                        object_property = output.get(QPuzzle.OUTPUT_OBJECT_PROPERTY)
                        object_property_delta = output.get(QPuzzle.OUTPUT_OBJECT_PROPERTY_DELTA)
                        object_property_value = output.get(QPuzzle.OUTPUT_OBJECT_PROPERTY_VALUE)
                        selected_object = QObjectFactory.get_object_by_name(v)
                        if object_property_delta is not None:
                            selected_object.set_property(object_property, object_property_delta, increment=False)
                        else:
                            selected_object.set_property(object_property, object_property_value)

            self.events.add_event(Event(type=Event.GAME,
                                        name=Event.GAME_MODEL_CHANGED,
                                        description=f"Something happened when you {action} {obj}"))

        return success


class EventQueue():
    def __init__(self):
        self.events = collections.deque()

    def add_event(self, new_event: Event):
        self.events.append(new_event)

    def pop_event(self):
        return self.events.pop()

    def size(self):
        return len(self.events)

    def print(self):
        for event in self.events:
            print(event)
