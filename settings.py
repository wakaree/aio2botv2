
from dataclasses import dataclass


@dataclass
class Settings:
    API_TOKEN: str

    @classmethod
    def load(cls, filename: str) -> "Settings":
        from yaml import full_load

        with open(filename) as yaml:
            return cls(**full_load(yaml))
