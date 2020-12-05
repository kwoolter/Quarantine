from quarantine.model.events import Event
from quarantine.model.qtime import QTimer
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
        self.events = EventQueue()

        self.state = QModel.STATE_LOADED

    def initialise(self):
        self.state = QModel.STATE_READY
        self.timer = QTimer()

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
