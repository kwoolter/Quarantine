class Event():

    # Event Types
    DEBUG = "debug"
    QUIT = "quit"
    DEFAULT = "default"
    STATE = "state"
    GAME = "game"
    WORLD = "world"
    EFFECT = "effect"

    # Define states
    STATE_LOADED = "Game Loaded"
    STATE_READY = "Game Ready"
    STATE_PLAYING = "Game Playing"
    STATE_PAUSED = "Game Paused"
    STATE_GAME_OVER = "Game Over"
    STATE_WORLD_COMPLETE = "Game World Complete"

    # Event Names
    TICK = "Tick"
    EFFECT_START = "Effect Start"
    EFFECT_END = "Effect End"
    HELP = "Help"
    ACTION_FAILED = "action failed"
    ACTION_SUCCEEDED = "action succeeded"

    def __init__(self, name: str, description: str = None, type: str = DEFAULT):
        self.name = name
        self.description = description
        self.type = type

    def __str__(self):
        return "{0}:{1} ({2})".format(self.name, self.description, self.type)