from .model import my_function

__app_name__ = "lkmap_to_ifc_cli"
__version__ = "0.1.0"

(
    SUCCESS,
    DIR_ERROR,
    FILE_ERROR
) = range(3)

ERRORS = {
    DIR_ERROR: "config directory error",
    FILE_ERROR: "config file error",
}
