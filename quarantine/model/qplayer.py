import random

class QPlayer:

    STATE_AWAKE = "awake"
    STATE_ASLEEP = "asleep"
    STATE_DEAD = "dead"

    PROPERTY_HUNGER = "hunger"
    PROPERTY_TIREDNESS = "tiredness"
    PROPERTY_ENERGY = "energy"
    PROPERTY_HEALTH = "health"

    PROPERTIES = (PROPERTY_HEALTH, PROPERTY_ENERGY, PROPERTY_ENERGY, PROPERTY_TIREDNESS)

    def __init__(self, name:str):
        self.name = name
        self.state = QPlayer.STATE_AWAKE

        self.properties = {}

    def __str__(self):
        text = f"My name is {self.name}: "
        for property_name in QPlayer.PROPERTIES:
            text += f'{property_name}={self.properties.get(property_name)},'

        return text

    def add_properties(self, new_properties: dict):
        self.properties.update(new_properties)

    def get_property(self, property_name: str):
        return self.properties.get(property_name)

    def set_property(self, property_name: str, property_value, increment:bool = False):

        if increment is True:
            property_value += self.get_property(property_name)

        property_value = max(0,min(100, property_value))
        self.properties[property_name] = property_value


    def roll(self):
        new_properties = {}
        for property in QPlayer.PROPERTIES:
            new_properties[property] = random.randint(50,100)

        self.add_properties(new_properties)


