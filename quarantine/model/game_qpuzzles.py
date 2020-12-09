from quarantine.model.qpuzzles import *
from quarantine.model.qplayer import QPlayer

class TestPuzzle(QPuzzle):
    def __init__(self):
        super().__init__(__class__)

    def is_success(self):
        return True

class TestPuzzle2(QPuzzle):
    def __init__(self):
        super().__init__(__class__)

    def is_success(self):
        success = True

        loc = self.inputs.get(QPuzzle.INPUT_LOCATION)

        if loc == "Desk":
            success = False

        return success

class TakeShower(QPuzzle):
    def __init__(self):
        super().__init__(__class__)

    def is_success(self):
        success = False

        loc = self.inputs.get(QPuzzle.INPUT_LOCATION)
        obj = self.inputs.get(QPuzzle.INPUT_OBJECT)
        action = self.inputs.get(QPuzzle.INPUT_ACTION)

        if loc == "Shower" and obj == "Shampoo" and action == "use":
            success = True

        return success


if __name__ == "__main__":
    pm = QPuzzleManager()

    inputs = {}

    inputs[QPuzzle.INPUT_OBJECT] = "Shampoo"
    inputs[QPuzzle.INPUT_ACTION] = "use"
    inputs[QPuzzle.INPUT_LOCATION] = "Shower"


    p = TestPuzzle()
    pm.add_puzzle(p)

    p = TestPuzzle2()
    pm.add_puzzle(p)

    p = TakeShower()
    pm.add_puzzle(p)

    pm.evaluate_puzzles(inputs)


class QGamePuzzleManager(QPuzzleManager):
    def __init__(self):
        super().__init__()

    def evaluate_puzzles(self, inputs: dict):

        overall_success = False

        self.outputs = {}

        loc = inputs.get(QPuzzle.INPUT_LOCATION)
        o = inputs.get(QPuzzle.INPUT_OBJECT)
        action = inputs.get(QPuzzle.INPUT_ACTION)

        puzzle_name = "Take Shower"
        if loc == "Shower" and o == "Shampoo" and action == QPuzzle.ACTION_USE:
            outputs = {QPlayer.PROPERTY_TIREDNESS: -10, QPlayer.PROPERTY_ENERGY: 10,
                       QPuzzle.OUTPUT_TIME_DELTA:30,
                       QPuzzle.OUTPUT_OBJECT: o,
                       QPuzzle.OUTPUT_OBJECT_PROPERTY: "Location",
                       QPuzzle.OUTPUT_OBJECT_PROPERTY_VALUE: "VOID"
                       }
            overall_success = True
            self.outputs[puzzle_name]=outputs
            print(f"Puzzle {puzzle_name} succeeded")

        puzzle_name = "Drink Coffee"
        if o == "Coffee" and action == QPuzzle.ACTION_USE:
            outputs = {QPlayer.PROPERTY_TIREDNESS: -10,
                       QPuzzle.OUTPUT_TIME_DELTA: 15,
                       QPuzzle.OUTPUT_OBJECT:o,
                       QPuzzle.OUTPUT_OBJECT_PROPERTY:"Location",
                       QPuzzle.OUTPUT_OBJECT_PROPERTY_VALUE:"VOID"}
            overall_success = True
            self.outputs[puzzle_name] = outputs
            print(f"Puzzle {puzzle_name} succeeded")

        return overall_success
