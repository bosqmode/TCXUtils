from lxml import etree
from modules.Activity import Activity
from modules.TrackPoint import TrackPoint

class TCXFile:
    '''TCX file wrapper'''
    def __init__(self, filepath: str) -> None:
        '''Default ctor, filepath to .tcx'''
        self.__tree = etree.parse(filepath)
        self.__root = self.__tree.getroot()

    def get_activies(self) -> list[Activity]:
        activities = self.__root.findall('.//Activity', self.__root.nsmap)
        activityList = []

        for activity in activities:
            sport = activity.attrib['Sport']
            id = activity.find('.//Id', self.__root.nsmap).text
            starttime = activity.find('.//Lap', self.__root.nsmap).attrib['StartTime']
            totalDistance = float(activity.find('.//Lap/DistanceMeters', self.__root.nsmap).text)
            totalTime = float(activity.find('.//TotalTimeSeconds', self.__root.nsmap).text)
            calories = float(activity.find('.//Calories', self.__root.nsmap).text)
            triggerMethod = activity.find('.//TriggerMethod', self.__root.nsmap).text

            trackpointlist = []
            trackpoints = activity.findall('.//Track/Trackpoint', self.__root.nsmap)
            for trackpoint in trackpoints:
                __pos = trackpoint.find('.//Position', self.__root.nsmap)
                if __pos is None:
                    continue #skip points with no lat/lon values
                latitude = float(__pos.find('.//LatitudeDegrees', self.__root.nsmap).text)
                longitude = float(__pos.find('.//LongitudeDegrees', self.__root.nsmap).text)
                distance = float(trackpoint.find('.//DistanceMeters', self.__root.nsmap).text)
                time = trackpoint.find('.//Time', self.__root.nsmap).text
                if trackpoint.find('.//AltitudeMeters', self.__root.nsmap) is not None:
                    altitude = float(trackpoint.find('.//AltitudeMeters', self.__root.nsmap).text)
                else:
                    altitude = 0

                trackpointlist.append(TrackPoint(distance, time, latitude, longitude, altitude))

            activityList.append(Activity(sport, id, trackpointlist, totalDistance, totalTime, calories, triggerMethod, starttime))

        return activityList
    
    def get_calculated_totaldistance(self) -> float:
        '''Sums up all the distances of all the activities and their trackpoints'''
        distance = 0
        for activity in self.get_activies():
            for pt in activity.trackpoints:
                distance += pt.distance
        return distance