from modules.TCXFile import TCXFile
import argparse
from lxml import etree
from termcolor import colored
import os

def get_gpx_type(sport: str):
    if "run" in sport.lower():
        return "Running"
    elif "walk" in sport.lower():
        return "Walking"
    return sport

def convert_to_gpx(tcx: TCXFile, filename: str) -> None:
    '''Converts TCXFile to GPX XML'''
    NSMAP = {
        "xmlns": "http://www.topografix.com/GPX/1/1",
        "gpxtpx": "http://www.garmin.com/xmlschemas/TrackPointExtension/v1",
        "gpxx": "http://www.garmin.com/xmlschemas/GpxExtensions/v3",
        "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        "schemaLocation": "http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd",
    }

    activities = tcx.get_activies()

    if len(activities) > 1:
        print(colored('Encountered more than one activity... combining with some assumptions...', 'red'))

    document = etree.Element('gpx', nsmap=NSMAP)
    document.attrib["creator"] = "--No GPS SELECTED--"
    document.attrib["version"] = "1.1"

    metadata = etree.SubElement(document, 'metadata')
    link = etree.SubElement(metadata, 'link')
    etree.SubElement(metadata, 'desc').text = "https://en.wikipedia.org/wiki/GPS_Exchange_Format"
    etree.SubElement(metadata, 'time').text = activities[0].starttime
    text = etree.SubElement(link, 'text')
    text.text = "Bosqmode's TCX2GPX converter"

    trk = etree.SubElement(document, 'trk')
    etree.SubElement(trk, 'name').text = "Converter Export"
    etree.SubElement(trk, 'type').text = get_gpx_type(activities[0].sport)
    trkseg = etree.SubElement(trk, 'trkseg')
    
    for activity in activities:
        for point in activity.trackpoints:
            trkpt = etree.SubElement(trkseg, 'trkpt')
            trkpt.attrib['lon'] = str(point.longitude)
            trkpt.attrib['lat'] = str(point.latitude)
            etree.SubElement(trkpt, 'ele').text = str(point.altitude)
            etree.SubElement(trkpt, 'time').text = str(point.time)

    tree = etree.ElementTree(document)
    tree.write(filename, pretty_print=True, xml_declaration=True, encoding="utf-8")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-ip", "--inpath", type=str, help="Path to the file or files. Can be a single file ending in .tcx or directory")
    parser.add_argument("-op", "--outpath", type=str, help="Output directory path")

    args = parser.parse_args()

    inpath = args.inpath
    outpath = args.outpath
    singlefile = inpath.endswith(".tcx")

    if singlefile:
        print(colored(f'Converting: {inpath}', 'green'))
        tcx = TCXFile(inpath)
        filename = os.path.normpath(inpath)
        filename = inpath.split(os.sep)[-1]
        filename = filename.replace('.tcx', '.gpx')
        convert_to_gpx(tcx, os.path.join(outpath, filename))
    else:
        files = os.listdir(inpath)
        if not os.path.exists(outpath):
            os.mkdir(outpath)
        for file in files:
            print(colored(f'Converting: {file}', 'green'))
            tcx = TCXFile(os.path.join(inpath, file))
            filename = file.replace('.tcx', '.gpx')
            convert_to_gpx(tcx, os.path.join(outpath, filename))