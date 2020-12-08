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
        self.puzzles = QGamePuzzleManager()

        self.state = QModel.STATE_LOADED

    def initialise(self):
        self.state = QModel.STATE_READY
        self.timer = QTimer()

        # Initialise components
        self.player = QPlayer("Me")
        self.player.roll()
        print(f"{self.player}")

        QLocationFactory.load("locations.csv")
        QObjectFactory.load("objects.csv")
        QMapFactory.load("map.csv")

        start_location = "Pantry"
        start_location = "Main Room"

        self.current_location = QLocationFactory.get_object_by_name(start_location)

        self.events.add_event(Event(type=Event.GAME,
                                    name=Event.ACTION_SUCCEEDED,
                                    description=f"Welcome {self.player.name} to {self.name}"))

    def pause(self):
        if self.state == QModel.STATE_PLAYING:
            self.state = QModel.STATE_PAUSED
        elif self.state == QModel.STATE_PAUSED:
            self.state = QModel.STATE_PLAYING

    def end(self):
        self.state = QModel.STATE_GAME_OVER

    def tick(self):

        if self.state == QModel.STATE_PLAYING:

            self.timer.tick()

            self.events.add_event(Event(type=Event.GAME,
                                        name=Event.TICK,
                                        description=f"Game model ticked: Day {self.timer.day:02} {self.timer.hour:02}:{self.timer.minutes:02} state({self.state})"))

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


    def get_objects_at_location(self):
        return QObjectFactory.get_objects_by_location(self.current_location.name)

    def perform_action(self, obj:str, action:str):

        inputs = {}

        inputs[QPuzzle.INPUT_LOCATION] = self.current_location.name
        inputs[QPuzzle.INPUT_TIME] = str(self.timer)
        inputs[QPuzzle.INPUT_PLATER_STATE] = self.player.state
        inputs[QPuzzle.INPUT_OBJECT] = obj
        inputs[QPuzzle.INPUT_ACTION] = action

        self.events.add_event(Event(type=Event.GAME,
                                    name=Event.ACTION_SUCCEEDED,
                                    description=f"Trying to {action} {obj}"))

        success = self.puzzles.evaluate_puzzles(inputs)

        if success is False:
            self.events.add_event(Event(type=Event.GAME,
                                        name=Event.ACTION_FAILED,
                                        description=f"Nothing happens when you {action} {obj}"))
        else:
            for puzzle, output in self.puzzles.outputs.items():
                print(f"{puzzle}:{output}")

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
