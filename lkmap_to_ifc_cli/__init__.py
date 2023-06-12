__app_name__ = "lkmap_to_ifc_cli"
__version__ = "0.1.0"

(
    SUCCESS,
    CONFIG_ERROR,
    GPKG_ERROR,
    IFC_ERROR,

) = range(4)

ERRORS = {
    CONFIG_ERROR: "config error",
    GPKG_ERROR: "geopackage error",
    IFC_ERROR: "IFC error"
}
