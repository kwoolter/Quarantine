import pandas as pd
import logging
from pathlib import Path

class QObject():
    def __init__(self, name:str):
        self.name = name
        self.properties = {}
        self.contents = []

    def add_properties(self, new_properties: dict):
        self.properties.update(new_properties)

    def get_property(self, property_name : str):
        return self.properties.get(property_name)
    
    def set_property(self, property_name:str, property_value, increment:bool = False):
        if increment is True:
            property_value += self.properties[property_name]

        self.properties[property_name] = property_value

    def add_content(self, new_object):
        if self.get_property("IsContainer") == False:
            raise Exception("This is not a container!!")

        self.contents.append(new_object)
        new_object.set_property("Location", self.get_property("Location"))

    def get_content(self):
        return self.contents

    def __str__(self):
        text =f'{self.name}:'
        for k,v in self.properties.items():
            text+=f'{k}={v},'
        if len(self.contents)>0:
            text+="Contents:"
            for o in self.contents:
                text+=str(o)+","
        return text

class QObjectFactory():

    qobjects = {}

    def __init__(self):
        pass

    @staticmethod
    def load(file_name: str):

        # Create path for the file that we are going to load
        data_folder = Path(__file__).resolve().parent
        file_to_open = data_folder / "data" / file_name

        # Read in the csv file
        objs = pd.read_csv(file_to_open)
        objs.set_index("Name", drop=True, inplace=True)

        # Build dictionary of objects from the data
        for index, row in objs.iterrows():
            e = QObject(index)
            e.add_properties(row.iloc[:].to_dict())
            QObjectFactory.qobjects[index] = e


    @staticmethod
    def get_available_objects()->list:
        return list(QObjectFactory.qobjects.keys())

    @staticmethod
    def get_object_by_name(name: str) -> QObject:

        e = QObjectFactory.qobjects.get(name)
        if e is None:
            logging.warning(f"Can't find QObject {name} in factory!")

        return e

    @staticmethod
    def get_objects_by_location(location_name: str) -> list:
        matching_objs = []
        for o in QObjectFactory.qobjects.values():
            if o.get_property("Location") == location_name:
                matching_objs.append(o)

        return matching_objs




if __name__ == "__main__":

    QObjectFactory.load("objects.csv")

    names = QObjectFactory.get_available_objects()
    for name in names:
        r = QObjectFactory.get_object_by_name(name)
        print(f"\t{r}")

    loc_name = "Pantry"
    print(f"\n\nLooking for objects at {loc_name}")

    matches = QObjectFactory.get_objects_by_location(loc_name)
    for o in matches:
        print(f"\t{o}")