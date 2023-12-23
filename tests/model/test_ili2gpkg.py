from model.ili2gpkg import Ili2gpkg


def test_ili2gpkg_conversion_schema_import():
    valid = Ili2gpkg.convert2GPKG(
        '--schemaimport --dbfile MeilenLKMAP.gpkg --defaultSrsCode 2056 C:\\Users\\jamie\\SA\\Meilen\\SIA405_LKMap_LV95.ili')
    assert valid
