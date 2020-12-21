from quarantine.model.qpuzzles import *
from quarantine.model.qplayer import QPlayer
from quarantine.model.qobject import QObjectFactory
from quarantine.model.qlocation import QLocationFactory


class QGamePuzzleManager(QPuzzleManager):
    # Which locations get lit by which switches...
    LIGHT_SWITCHES = {"Master Light Switch": ("Doorway", "Main Room"),
                      "Bathroom Light Switch": ("Bathroom", "Shower"),
                      "Main Room Switch": ("Main Room", "Pantry", "Desk", "TV Area", "Snug"),
                      "Bed Switch 1": ("Main Room"),
                      "Bed Switch 2": ("Bed")}

    def __init__(self, player: QPlayer):
        super().__init__()
        self.player = player
        self.puzzle_tracker_by_day = {}
        self.puzzle_tracker_total = {}
        self.outputs = {}
        self.errors = {}

    def evaluate_puzzles(self, inputs: dict):

        overall_success = False

        # An empty dictionary for collating the results of the puzzles
        self.outputs = {}
        self.errors = {}

        # Collect all of the inputs that will be useful for evaluating the puzzles
        day = inputs.get(QPuzzle.INPUT_DAY)
        hour = inputs.get(QPuzzle.INPUT_HOUR)
        loc = inputs.get(QPuzzle.INPUT_LOCATION)
        loc_obj = QLocationFactory.get_object_by_name(loc)
        o = inputs.get(QPuzzle.INPUT_OBJECT)
        obj = QObjectFactory.get_object_by_name(o)
        action = inputs.get(QPuzzle.INPUT_ACTION)
        is_power_on = self.puzzle_tracker_total.get("Power On",0) > 0

        # Check all of the puzzles....
        if action == "DROP":
            obj.set_property("Location", loc)
            overall_success = True

        if action in ("TAKE", "TAKE LEFT", "TAKE RIGHT"):
            if obj.get_property("IsMovable") is True:
                is_taken = False

                if action in ("TAKE", "TAKE RIGHT"):
                    hand = "Right Hand"
                    right_obj = QObjectFactory.get_objects_by_location(hand)
                    if len(right_obj) == 0:
                        obj.set_property("Location", hand)
                        is_taken = True

                if action == "TAKE LEFT" or is_taken is False:
                    hand = "Left Hand"
                    right_obj = QObjectFactory.get_objects_by_location(hand)
                    if len(right_obj) == 0:
                        obj.set_property("Location", hand)
                        is_taken = True

                overall_success = is_taken

            else:
                self.errors[action] = f"You can't take {o.title()}"

        puzzle_name = "Time is Up!"
        if day >=1:
            outputs = {
                QPuzzle.OUTPUT_PLAYER_STATE: QPlayer.STATE_DEAD
            }
            overall_success = True
            self.outputs[puzzle_name] = outputs


        puzzle_name = "Power On"
        if is_power_on is False and o == "Room Key" and loc == "Doorway" and action == QPuzzle.ACTION_USE:
            outputs = {}
            obj.set_property("Location", "Key Card Slot")
            overall_success = True
            self.outputs[puzzle_name] = outputs

        puzzle_name = "Room Service"
        count = self.get_day_puzzle_count(puzzle_name=puzzle_name, day=day)
        if count == 0 and day == 0 and hour == 1:

            outputs = {
                QPuzzle.OUTPUT_OBJECT: "Coffee",
                QPuzzle.OUTPUT_OBJECT_PROPERTY: "Location",
                QPuzzle.OUTPUT_OBJECT_PROPERTY_VALUE: "Pantry"}

            overall_success = True
            self.outputs[puzzle_name] = outputs

        puzzle_name = "Busted"
        if loc == "Corridor" and (day > 0 or hour > 0):

            outputs = {
                QPuzzle.OUTPUT_PLAYER_STATE: QPlayer.STATE_DEAD
            }
            overall_success = True
            self.outputs[puzzle_name] = outputs


        puzzle_name = "Sleep"
        count = self.get_day_puzzle_count(puzzle_name=puzzle_name, day=day)
        if o == "Single Bed" and action == QPuzzle.ACTION_USE:
            if count > 1:
                outputs = {QPlayer.PROPERTY_TIREDNESS: -80, QPlayer.PROPERTY_ENERGY: 50,
                           QPuzzle.OUTPUT_TIME_DELTA: (60 * 6),
                           }
                overall_success = True
                self.outputs[puzzle_name] = outputs
            else:
                self.errors[puzzle_name] = "You have already slept today"

        puzzle_name = "Lights On or Off"
        if is_power_on is True and o in QGamePuzzleManager.LIGHT_SWITCHES.keys() and action == QPuzzle.ACTION_USE:
            affected_rooms = QGamePuzzleManager.LIGHT_SWITCHES.get(o)
            current_state = obj.get_property("State")
            new_state = "ON" if current_state == "OFF" else "OFF"
            obj.set_property("State", new_state)

            if type(affected_rooms) is tuple:
                for room in affected_rooms:
                    loc_obj = QLocationFactory.get_object_by_name(room)
                    loc_obj.set_property("IsLight", new_state == "ON")
            else:
                loc_obj = QLocationFactory.get_object_by_name(affected_rooms)
                assert loc_obj is not None, f"Location {affected_rooms} does not exist"
                loc_obj.set_property("IsLight", new_state == "ON")

            outputs = {}
            self.outputs[puzzle_name] = outputs
            overall_success = True

        puzzle_name = "Take Shower"
        count = self.get_day_puzzle_count(puzzle_name=puzzle_name, day=day)
        if loc == "Shower" and o == "Shampoo" and action == QPuzzle.ACTION_USE:
            if count < 2:
                outputs = {QPlayer.PROPERTY_TIREDNESS: -10,
                           QPlayer.PROPERTY_ENERGY: 10,
                           QPuzzle.OUTPUT_TIME_DELTA: 30
                           }

                obj.set_property("Location", "VOID")
                overall_success = True
                self.outputs[puzzle_name] = outputs

            else:
                self.errors[puzzle_name] = "You have already had {count} showers today"

        puzzle_name = "Drink Coffee"
        if o == "Coffee" and action == QPuzzle.ACTION_USE:
            outputs = {QPlayer.PROPERTY_TIREDNESS: -10,
                       QPuzzle.OUTPUT_TIME_DELTA: 15
                        }

            obj.set_property("Location", "VOID")
            overall_success = True
            self.outputs[puzzle_name] = outputs

        puzzle_name = "Drink Red Wine"
        if o == "Red Wine" and action == QPuzzle.ACTION_USE:
            outputs = {QPlayer.PROPERTY_TIREDNESS: 15,
                       QPuzzle.OUTPUT_TIME_DELTA: 15}
            obj.set_property("Location", "VOID")
            overall_success = True
            self.outputs[puzzle_name] = outputs

        # Finished checking all of the puzzles

        # Update the number of times the player has completed a puzzle on a given day
        puzzles_today = self.puzzle_tracker_by_day.get(day, {})

        for puzzle_name in self.outputs.keys():
            current_count = puzzles_today.get(puzzle_name, 0)
            current_count += 1
            puzzles_today[puzzle_name] = current_count
            print(f"Puzzle {puzzle_name} succeeded")

        self.puzzle_tracker_by_day[day] = puzzles_today


        # Update the number of times the player has completed a puzzle in total
        for puzzle_name in self.outputs.keys():
            puzzles_total = self.puzzle_tracker_total.get(puzzle_name, 0)
            self.puzzle_tracker_total[puzzle_name] = puzzles_total + 1

        return overall_success

    def get_day_puzzle_count(self, day: int, puzzle_name: str):

        puzzles_for_day = self.puzzle_tracker_by_day.get(day, {})
        count = puzzles_for_day.get(puzzle_name, 0)

        return count

    def print(self):
        print(str(self.puzzle_tracker_by_day))
        print(self.puzzle_tracker_total)
