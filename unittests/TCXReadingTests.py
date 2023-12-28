import sys
import unittest
sys.path.append('./')
from modules.TCXFile import TCXFile

class TCXReadingTests(unittest.TestCase):
    '''Unittests for reading TCX files'''
    @classmethod
    def setUpClass(cls) -> None:
        cls.tcx = TCXFile("./unittests/test.tcx")
        cls.activities = cls.tcx.get_activies()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tcx = None

    def test_reading_activities(self):
        self.assertEqual(len(self.activities), 3)
        self.assertEqual(self.activities[0].sport, "Walking")
        self.assertEqual(self.activities[2].starttime, "2018-04-04T14:27:51.708Z")

    def test_reading_distances(self):
        check = 108.10275268554688+366.61938285827637+1748.515429019928
        self.assertAlmostEqual(sum([x.distancemeters for x in self.activities]), check)
        self.assertAlmostEqual(self.tcx.get_total_distance_meters(), check)

    def test_reading_duration(self):
        check = 79.906+301.77+1881.131
        self.assertAlmostEqual(sum([x.totaltimeseconds for x in self.activities]), check)
        self.assertAlmostEqual(self.tcx.get_total_duration_seconds(), check)
        
