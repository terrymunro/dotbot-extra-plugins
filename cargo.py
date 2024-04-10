import dotbot
import subprocess

from pydantic import BaseModel


class Cargo(dotbot.Plugin):
    """
    Install cargo binaries
    """

    class Config(BaseModel):
        # TODO: implement config
        pass

    _directive = "cargo"

    def can_handle(self, directive: str) -> bool:
        return self._directive == directive

    def handle(self, directive: str, data: dict) -> bool:
        if not self.can_handle(directive):
            raise ValueError(f"{self._directive} cannot handle directive {directive}")

        config = self.Config.model_validate(data)

        # TODO: implement
        try:
            subprocess.run([], check=True)
        except subprocess.CalledProcessError:
            return False

        return True
