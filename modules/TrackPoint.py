class TrackPoint:
    '''Dataobject for a trackpoint'''
    def __init__(self, distance: float, time: str, latitude: float, longitude: float, altitude: float) -> None:
        self.distance = distance
        self.time = time
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude