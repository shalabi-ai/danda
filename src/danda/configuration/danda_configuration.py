from danda.configuration.clean_configuration import CleaningConfig
from danda.configuration.config_section import ConfigSection
from dataclasses import dataclass, field

from danda.configuration.type_configuration import TypeConfig


@dataclass
class DandaConfig(ConfigSection):
    cleaning: CleaningConfig = field(default_factory=CleaningConfig)
    types: TypeConfig = field(default_factory=TypeConfig)

    def show(self) -> str:
        return "\n\n".join([
            self.types.show(),
            self.cleaning.show(),
        ])
