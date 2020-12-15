import random

class QPlayer:

    # The states that a player can be in
    STATE_AWAKE = "awake"
    STATE_ASLEEP = "asleep"
    STATE_DEAD = "dead"
    STATES = (STATE_AWAKE, STATE_ASLEEP)

    # The properties that a player has
    PROPERTY_HUNGER = "hunger"
    PROPERTY_TIREDNESS = "tiredness"
    PROPERTY_ENERGY = "energy"
    PROPERTY_HEALTH = "health"

    # For each state...
    # How many ticks does it take to change a property...
    # Any by how much does it change.
    STATE_TICKS_PER_CHANGE = {

        STATE_AWAKE: {
            PROPERTY_HUNGER: (5, 1),
            PROPERTY_ENERGY: (5, -1),
            PROPERTY_TIREDNESS: (5, 1)},

        STATE_ASLEEP: {
            PROPERTY_HUNGER: (5, 1),
            PROPERTY_ENERGY: (5, 1),
            PROPERTY_TIREDNESS: (5, -1)},

        STATE_DEAD: {
            PROPERTY_HUNGER: (1, 0),
            PROPERTY_ENERGY: (1, 0),
            PROPERTY_TIREDNESS: (1, 0)},
    }

    PROPERTIES = (PROPERTY_HEALTH, PROPERTY_ENERGY, PROPERTY_ENERGY, PROPERTY_TIREDNESS)

    def __init__(self, name: str):
        self.name = name
        self.state = QPlayer.STATE_AWAKE
        self.ticks = 0

        self.properties = {}

    def __str__(self):
        text = f"My name is {self.name}: "
        for property_name in QPlayer.PROPERTIES:
            text += f'{property_name}={self.properties.get(property_name)},'

        return text

    def add_properties(self, new_properties: dict):
        self.properties.update(new_properties)

    def get_property(self, property_name: str):
        return self.properties.get(property_name, 0)

    def set_property(self, property_name: str, property_value, increment: bool = False):

        if increment is True:
            property_value += self.get_property(property_name)

        property_value = max(0, min(100, property_value))
        self.properties[property_name] = property_value

    def roll(self):
        new_properties = {}
        for property in QPlayer.PROPERTIES:
            new_properties[property] = random.randint(50, 100)

        self.add_properties(new_properties)

    def tick(self, increment: int = 1):

        state_ticks = QPlayer.STATE_TICKS_PER_CHANGE.get(self.state)

        for i in range(increment):

            self.ticks += 1

            for k, v in state_ticks.items():
                ticks, delta = v
                if self.ticks % ticks == 0:
                    self.set_property(k, delta, increment=True)
