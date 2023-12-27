from modules.TrackPoint import TrackPoint

class Activity:
    '''Activity dataobject'''
    def __init__(self, 
                 sport: str,
                 id: str,
                 trackpoints: list[TrackPoint],
                 distancemeters: float,
                 totaltimeseconds: float,
                 calories: float,
                 triggermethod: str,
                 starttime: str
                 ) -> None:
        
        self.sport = sport
        self.id = id
        self.trackpoints = trackpoints
        self.distancemeters = distancemeters
        self.totaltimeseconds = totaltimeseconds
        self.calories = calories
        self.triggermethod = triggermethod
        self.starttime = starttime

    def __repr__(self) -> str:
        return f'{self.sport} | {self.id} | TrackPoints: {len(self.trackpoints)} | {self.distancemeters/1000.0} km | {self.totaltimeseconds/60.0} minutes | {self.calories} calories'