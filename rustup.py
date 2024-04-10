import dotbot
import subprocess
import requests

from pydantic import BaseModel

# curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh


class RustUp(dotbot.Plugin):
    """
    Install Rust Up and Toolchains
    """

    class Config(BaseModel):
        pass

    _directive = "rustup"

    def can_handle(self, directive: str) -> bool:
        return self._directive == directive

    def handle(self, directive: str, data: dict) -> bool:
        if not self.can_handle(directive):
            raise ValueError(f"{self._directive} cannot handle directive {directive}")

        config = self.Config.model_validate(data)

        resp = requests.get("https://sh.rustup.rs", allow_redirects=True)
        print(resp.text)
        return False
        try:
            subprocess.run([], check=True)
        except subprocess.CalledProcessError:
            return False

        return True
