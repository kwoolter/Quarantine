

class QPuzzle:

    INPUT_TIME = "CURRENT TIME"
    INPUT_LOCATION = "CURRENT LOCATION"
    INPUT_OBJECT = "OBJECT NAME"
    INPUT_ACTION = "OBJECT ACTION"
    INPUT_PLATER_STATE = "PLAYER STATE"

    INPUTS = (INPUT_TIME, INPUT_PLATER_STATE, INPUT_ACTION, INPUT_OBJECT, INPUT_LOCATION)


    ACTION_USE = "USE"
    ACTION_OPEN = "OPEN"
    ACTION_CLOSE = "CLOSE"
    ACTION_EAT = "EAT"
    ACTION_DRINK = "DRINK"
    ACTION_TAKE = "TAKE"
    ACTION_DROP = "DROP"

    ACTIONS = (ACTION_USE, ACTION_DRINK, ACTION_EAT, ACTION_OPEN, ACTION_CLOSE, ACTION_TAKE, ACTION_DROP)

    OUTPUT_SUCCESS = "OUTPUT SUCCESS"

    def __init__(self, name:str):
        self.name = name
        self.outputs = {}

    def evaluate(self, inputs:dict):

        self.inputs = inputs.copy()

        success = self.is_success()

        if success is True:
            self.outputs[QPuzzle.OUTPUT_SUCCESS] = True
        else:
            self.outputs[QPuzzle.OUTPUT_SUCCESS] = False

        return success

    def is_success(self):

        assert False, f"No is_success override for puzzle {self.name}"

        return False

class QPuzzleManager:

    def __init__(self):

        self.puzzles = []
        self.outputs = []

    def add_puzzle(self, new_puzzle:QPuzzle):

        self.puzzles.append(new_puzzle)

    def evaluate_puzzles(self, inputs:dict):

        overall_success = False

        self.outputs=[]

        for puzzle in self.puzzles:
            success = puzzle.evaluate(inputs)
            overall_success = overall_success or success
            if success is True:
                self.outputs.append(puzzle.outputs.copy())
                print(f"Puzzle {puzzle.name} succeeded")

        return overall_success

if __name__ == "__main__":
    pm = QPuzzleManager()

    inputs = {}
    inputs[QPuzzle.INPUT_LOCATION] = "Desk"

    p1 = QPuzzle("Test1")

    pm.add_puzzle(p1)

    pm.evaluate_puzzles(inputs)

