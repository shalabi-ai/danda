from danda.configuration.config_section import ConfigSection
from dataclasses import dataclass


@dataclass
class CleaningConfig(ConfigSection):
    remove_duplicates: bool = True
    strip_whitespace: bool = True
    remove_empty_rows: bool = True