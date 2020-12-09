class Event():

    # Event Types
    DEBUG = "debug"
    QUIT = "quit"
    DEFAULT = "default"
    STATE = "state"
    GAME = "game"
    WORLD = "world"
    EFFECT = "effect"
    CONTROL = "control"

    # Define states
    STATE_LOADED = "Game Loaded"
    STATE_READY = "Game Ready"
    STATE_PLAYING = "Game Playing"
    STATE_PAUSED = "Game Paused"
    STATE_GAME_OVER = "Game Over"
    STATE_WORLD_COMPLETE = "Game World Complete"

    # Game events
    GAME_NEW_PLAYER = "new player"
    GAME_SAVED = "game saved"
    GAME_LOADED = "game loaded"
    GAME_MODE_CHANGED = "mode changed"
    GAME_MODEL_CHANGED = "model changed"

    TICK = "Tick"
    HELP = "Help"
    ACTION_FAILED = "action failed"
    ACTION_SUCCEEDED = "action succeeded"

    def __init__(self, name: str, description: str = None, type: str = DEFAULT):
        self.name = name
        self.description = description
        self.type = type

    def __str__(self):
        return "{0}:{1} ({2})".format(self.name, self.description, self.type)