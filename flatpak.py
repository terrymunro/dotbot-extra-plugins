import dotbot
import subprocess

from pydantic import BaseModel

from typing import Optional, Literal, Union

type Setting = Union[str, dict[Literal["name", "url", "repo", "reinstall"], Union[str, bool]]]
type FlatpakSettings = dict[Literal["repos", "apps"], list[Setting]]


class Repo(BaseModel):
    name: str
    url: str


class App(BaseModel):
    name: str
    repo: Optional[str]
    reinstall: Optional[bool]


KNOWN_REPOS = {
    "flathub": "https://dl.flathub.org/repo/flathub.flatpakrepo",
    "flathub-beta": "https://flathub.org/beta-repo/flathub-beta.flatpakrepo",
    "fedora": "oci+https://registry.fedoraproject.org",
    "gnome-nightly": "https://nightly.gnome.org/gnome-nightly.flatpakrepo",
    "elementary": "https://flatpak.elementary.io/repo.flatpakrepo",
    "rhel": "https://flatpaks.redhat.io/rhel.flatpakrepo"
}


class Flatpak(dotbot.Plugin):
    """
    Install Flatpak
    """

    class Config(BaseModel):
        repos: list[Union[str, Repo]]
        apps: list[Union[str, App]]

    _directive = "flatpak"
    _default_repo = "flathub"
    _default_reinstall = False

    def can_handle(self, directive: str) -> bool:
        return self._directive == directive

    def handle(self, directive: str, data: FlatpakSettings) -> bool:
        if not self.can_handle(directive):
            raise ValueError(f"flatpak cannot handle directive {directive}")

        config = self.Config.model_validate(data, strict=True)
        self._get_defaults()
        success = True
        if config.repos:
            success = success and self._handle_repos(config.repos)
        if config.apps:
            success = success and self._handle_apps(config.apps)

        if success:
            self._log.info("All flatpak repos and apps have been installed")
        else:
            self._log.error("Not all flatpak repos and apps were successfully installed")

        return success

    def _get_defaults(self) -> None:
        """
        Gets the flatpak specific defaults from context.
        """
        defaults = self._context.defaults().get("flatpak", {})
        if "repo" in defaults:
            self._default_repo = defaults["repo"]
        if "reinstall" in defaults:
            self._default_reinstall = defaults["reinstall"]

    def _handle_repos(self, repos: list[Union[str, Repo]]) -> bool:
        """
        Add flatpak repositories
        """

        for repo in repos:
            if isinstance(repo, str) and repo in KNOWN_REPOS:
                repo = Repo(name=repo, url=KNOWN_REPOS[repo])

            try:
                subprocess.run(
                    ["flatpak", "remote-add", "--if-not-exists", repo.name, repo.url],
                    check=True
                )
            except subprocess.CalledProcessError:
                self._log.error(f"{repo.name} was not added successfully")
                return False
        return True

    def _handle_apps(self, apps: list[Union[str, App]]) -> bool:
        """
        Install flatpak apps
        """
        for app in apps:
            if isinstance(app, str):
                app = App(name=app, repo=self._default_repo, reinstall=self._default_reinstall)

            reinstall = app.reinstall if app.reinstall is not None else self._default_reinstall

            try:
                parts = [
                    "flatpak",
                    "install",
                    "--noninteractive",
                    "--reinstall" if reinstall else None,
                    app.repo or self._default_repo,
                    app.name
                ]
                subprocess.run([
                    part
                    for part in parts
                    if part is not None
                ],
                    check=True
                )
            except subprocess.CalledProcessError:
                return False
        return True
