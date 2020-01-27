class GpsLocationEntries:
    lat = "lat"
    lng = "lng"
    time = "time"


class GpsLocation(object):
    def __init__(self, lat, lng, time):
        self.lat = lat
        self.lng = lng
        self.time = time

    @classmethod
    def fromDict(cls, input_dict: dict):
        return cls(
            input_dict[GpsLocationEntries.lat],
            input_dict[GpsLocationEntries.lng],
            input_dict[GpsLocationEntries.time]
        )

    def toDict(self):
        return {
            GpsLocationEntries.lat: self.lat,
            GpsLocationEntries.lng: self.lng,
            GpsLocationEntries.time: self.time
        }
