from lxml import etree
from modules.TCXFile import TCXFile
from termcolor import colored

def get_gpx_type(sport: str):
    if "run" in sport.lower():
        return "Running"
    elif "walk" in sport.lower():
        return "Walking"
    return sport

def __convert_to_gpx(tcx: TCXFile) -> etree.ElementTree:
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
    etree.SubElement(metadata, 'desc').text = "https://github.com/bosqmode/TCXUtils"
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

    return etree.ElementTree(document)

def convert_to_gpx_file(tcx: TCXFile, filename: str) -> None:
    '''Converts TCXFile to GPX XML and writes it to filename'''
    tree = __convert_to_gpx(tcx)
    tree.write(filename, pretty_print=True, xml_declaration=True, encoding="utf-8")

def convert_to_gpx_text(tcx: TCXFile) -> str:
    '''Converts TCXFile to GPX XML and returns GPX as str'''
    tree = __convert_to_gpx(tcx)
    return str(etree.tostring(tree, encoding='utf8'))