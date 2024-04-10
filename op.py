import subprocess, dotbot

from typing import Any


class OnePassword(dotbot.Plugin):
    """
    Install 1Password CLI and Desktop App as well as generate templates and
    configure ssh-agent etc.
    """
    _directive = "1password"

    def can_handle(self, directive: str) -> bool:
        return self._directive == directive

    def handle(self, directive: str, data: dict[str, Any]) -> bool:
        if not self.can_handle(directive):
            raise ValueError(f"1Password plugin cannot handle directive {directive}")

        if "template" in data and not self._handle_template(data["template"]):
            raise RuntimeError("Error while generating templates")

    def _handle_template(self, templates: list[dict[str, Any]]) -> bool:
        success = True
        for template in templates:
            if not ("input" in template and "output" in template):
                self._log.warn("Templates should have an input and output")
                success = False
                continue

            try:
                subprocess.run(
                    ["op", "inject", "-i", template["input"], "-o", template["output"]],
                    check=True
                )
            except subprocess.CalledProcessError:
                self._log.error(f"{template} was not generated successfully")
                success = False

        return success
