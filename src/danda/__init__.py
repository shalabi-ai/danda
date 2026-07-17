from .io import read_csv
from .io import read_excel
from .accessor import DandaAccessor

__all__ = [
    "read_csv",
    "read_excel",
    "DandaAccessor",
    "clean",
   # "optimize",
   # "report",
]

clean_plugin = "clean"
