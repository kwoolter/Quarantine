import pandas as pd
import logging
from pathlib import Path

class QLocation():
    def __init__(self, name:str):
        self.name = name
        self.properties = {}
        self.linked_locations = {}

    def add_properties(self, new_properties: dict):
        self.properties.update(new_properties)

    def add_linked_location(self, new_link):
        self.linked_locations[new_link.name] = new_link

    def get_property(self, property_name : str):
        return self.properties.get(property_name)

    def __str__(self):
        text =f'{self.name}:'
        for k,v in self.properties.items():
            text+=f'{k}={v},'
        if len(self.linked_locations) >0:
            text+="Links:"
            for k in self.linked_locations.keys():
                text += f'{k},'
        return text


class QLocationFactory():

    qlocations = {}

    def __init__(self):
        pass

    @staticmethod
    def load(file_name: str):

        # Create path for the file that we are going to load
        data_folder = Path(__file__).resolve().parent
        file_to_open = data_folder / "data" / file_name

        # Read in the csv file
        locs = pd.read_csv(file_to_open)
        locs.set_index("Name", drop=True, inplace=True)

        # Build dictionary of objects from the data
        for index, row in locs.iterrows():
            e = QLocation(index)
            e.add_properties(row.iloc[:].to_dict())
            QLocationFactory.qlocations[index] = e

    @staticmethod
    def get_available_objects()->list:
        return list(QLocationFactory.qlocations.keys())

    @staticmethod
    def get_object_by_name(name: str) -> QLocation:
        return QLocationFactory.qlocations.get(name)

if __name__ == "__main__":

    QLocationFactory.load("locations.csv")

    names = QLocationFactory.get_available_objects()
    for name in names:
        r = QLocationFactory.get_object_by_name(name)
        print(r)