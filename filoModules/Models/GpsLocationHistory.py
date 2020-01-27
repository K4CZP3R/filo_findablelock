from filoModules.Models.GpsLocation import GpsLocation
class GpsLocationHistoryEntries:
    locations = "locations"


class GpsLocationHistory(object):
    def __init__(self, locations: list):
        self.locations = locations
    
    @classmethod
    def empty(cls):
        return cls(list())

    @classmethod
    def fromDict(cls, input_dict: dict):
        locations = list()

        for i in input_dict[GpsLocationHistoryEntries.locations]:
            locations.append(GpsLocation.fromDict(i))
        return cls(locations)

    def toDict(self):
        locations = list()
        for i in self.locations:
            locations.append(i.toDict())
        return {GpsLocationHistoryEntries.locations: locations}

    def add_location(self, GpsLocation: GpsLocation):
        self.locations.append(GpsLocation)

    def get_location(self, i) -> GpsLocation:
        if i > len(self.locations):
            return None
        return self.locations[i]

    def get_location_count(self) -> int:
        return len(self.locations)

