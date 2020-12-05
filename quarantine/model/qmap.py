import pandas as pd
import logging
from pathlib import Path

from quarantine.model.qobject import *
from quarantine.model.qlocation import *

class QMapFactory():

    def __init__(self):
        pass

    @staticmethod
    def load(file_name: str):

        # Create path for the file that we are going to load
        data_folder = Path(__file__).resolve().parent
        file_to_open = data_folder / "data" / file_name

        # Read in the csv file
        location_links = pd.read_csv(file_to_open)
        location_links.set_index("Location", drop=True, inplace=True)

        for index, row in location_links.iterrows():
            loc = QLocationFactory.get_object_by_name(index)
            col = row["VisibleLocations"]
            for link in col.split(","):
                link_loc = QLocationFactory.get_object_by_name(link.strip())
                if link_loc is not None:
                    loc.add_linked_location(link_loc)
                else:
                    print(f"Failed to get link {link}")

if __name__ == "__main__":

    QObjectFactory.load("objects.csv")
    QLocationFactory.load("locations.csv")
    QMapFactory.load("map.csv")

    names = QLocationFactory.get_available_objects()
    for name in names:
        r = QLocationFactory.get_object_by_name(name)
        print(r)
        os = QObjectFactory.get_objects_by_location(r.name)
        for o in os:
            print(f"\t{o}")
            cos = QObjectFactory.get_objects_by_location(o.name)
            for co in cos:
                print(f"\t\t{co}")

