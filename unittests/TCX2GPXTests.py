import sys
import unittest
sys.path.append('./')
from modules.TCXFile import TCXFile
from modules.TCX2GPXConverter import convert_to_gpx_text

class TCX2GPXTests(unittest.TestCase):
    '''TCX to GPX conversion tests'''
    @classmethod
    def setUpClass(cls) -> None:
        cls.tcx = TCXFile("./unittests/test.tcx")
        cls.gpx = convert_to_gpx_text(cls.tcx)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.tcx = None
        cls.gpx = None

    def test_points_count(self):
        tcxpointscount = sum([len(x.trackpoints) for x in self.tcx.get_activies()])
        gpxpointscount = self.gpx.count('</trkpt>')
        self.assertEqual(tcxpointscount, gpxpointscount)

    def test_element(self):
        elementexists = '<trkpt lon="24.942840576171875" lat="60.166439056396484"><ele>31.5</ele><time>2018-04-04T14:38:15.336Z</time></trkpt>' in self.gpx
        self.assertTrue(elementexists)