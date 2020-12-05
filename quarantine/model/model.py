from quarantine.model.events import Event
import collections

class QModel:
    def __init__(self, name : str):

        # Model properties
        self.name = name
        self._state = None


        # Model Components
        self.events = EventQueue()

        self.state = Event.STATE_LOADED

    def initialise(self):
        self.state = Event.STATE_READY

    def end(self):
        pass

    def tick(self):
        self.events.add_event(Event(type=Event.GAME,
                                    name=Event.TICK,
                                    description=f"Game model ticked state({self.state})"))

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
