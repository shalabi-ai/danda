from danda.configuration.config_section import ConfigSection
from dataclasses import dataclass


@dataclass
class TypeConfig(ConfigSection):
    category_threshold: float = 0.10
    numeric_threshold: float = 0.95
    datetime_threshold: float = 0.95
    boolean_threshold: float = 1.0