# .tcx utils

This repo provides a wrapper for .tcx files (modules/TCXFile.py),
and a way to convert .tcx files to .gpx files (TCX2GPX.py),
making it easy to migrate Google Fit data to Strava.

## Requirements

[Python 3.11.](https://www.python.org/downloads/release/python-3115/)

```
pip3 install -r requirements.txt
```

### Converting .tcx to .gpx

One can either supply a single file:
```
TCX2GPX.py --inpath test.tcx --outpath ./
```

or a directory of files to be converted:
```
TCX2GPX.py --inpath F:\dir1 --outpath F:\dir2
```