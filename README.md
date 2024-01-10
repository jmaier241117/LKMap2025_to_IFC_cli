
LKMap2025 to IFC Converter - a CLI to convert LKMap 2025 data to an IFC 4.3 file
===================
 
Prerequisites
===================
For the current version, you will need a JRE (Java Runtime Environment) installed on your system, version 1.8 or later.

Additionally, Python 3.7 or higher is needed.


Installing 
=================
```
$ pip install -r requirements.txt
```


Running the Converter
=================
```
python convertLKMap2IFC.py 'POINT(2691039.8 1236160.3 420.0)' path/to/INTERLISdatafile.xtf
```

Options:

Option | Description | Format | Example
--- | --- | --- | --- 
--clip_src | Polygon representing bbox of elements to be considered | LV95 WKT Polygon | 'POLYGON((2691019.5 1236189.3, 2691079.8 1236187.8, 2691075.5 1236126.3, 2691009.0 1236129.3, 2691019.5 1236189.3))'
--export_path | The path to where you would like your IFC file to be generated | Path | path/to/IFC.ifc
--show_height_uncertainty | Flag if height uncertainties should be shown | Boolean | default = True
--show_position_uncertainty | Flag if position uncertainties should be shown | Boolean | default = True

