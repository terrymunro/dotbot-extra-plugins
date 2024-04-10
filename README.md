# Dotbot extra plugins

A small collection of extra plugins for [dotbot](https://github.com/anishathalye/dotbot).

* [Installation](#installation)
* [dnf](#dnf)
* [flatpak](#flatpak)
* [haskell](#haskell)
* [rust](#rust)
* [scala](#scala)
* [Write Files](#write-files)
* [Rational](#rational)

## Requirements

* Python >= 3.9

## Installation

Add it as a submodule of your dotfiles repository.

```sh
git submodule add https://github.com/terrymunro/dotbot-extra-plugins.git
```

Modify your `install` script, to enable all the plugins:

> TODO: Adjust install file to also install `requirements.txt`

```sh
"${BASEDIR}/${DOTBOT_DIR}/${DOTBOT_BIN}" \
    --package-dir dotbot-extra-plugins \
    -d "${BASEDIR}" \
    -c "${CONFIG}" \
    "${@}"
```

## TODO

This repository is a work-in-progress the following still needs to be done:

* [-] `dnf` plugin
    * [ ] Implementation
    * [-] Documentation
    * [ ] Tests
* [-] `flatpak` plugin
    * [x] Implementation
    * [x] Documentation
    * [ ] Tests
* [ ] `haskell` plugin
    * [ ] Implementation
    * [ ] Documentation
    * [ ] Tests
* [ ] `rust` plugin
    * [ ] Implementation
    * [ ] Documentation
    * [ ] Tests
* [ ] `scala` plugin
    * [ ] Implementation
    * [ ] Documentation
    * [ ] Tests
* [ ] `write_files` plugin
    * [ ] Implementation
    * [ ] Documentation
    * [ ] Tests

Please feel free to open an issue, or create pull requests to help out <3

## dnf

# Dotbot `dnf` plugin

Adds `dnf`, `rpm` and `yum_repos` directives, to allow you to install dnf packages and add new yum repos.

### Full example

```yaml
- defaults:
    yum_repos:
        enabled: true
        gpgcheck: true
        failovermethod: priority

- dnf:
    - at
    - cronie
    - cronie-anacron
    - ripgrep

# These will generate files under /etc/yum.repos.d/<name>.repo
- yum_repos: 
    vscode:                                         # The <name> of the repository
        # Any repository configuration options
        # See: man dnf.conf or man yum.conf
        name: Visual Studio Code
        baseurl: https://packages.microsoft.com/yumrepos/vscode  # This property is required!
        gpgkey: https://packages.microsoft.com/keys/microsoft.asc
        enabled: true
        gpgcheck: true
        failovermethod: priority
```

### Minimal example

```yaml
- dnf:
    - at
    - cronie
    - cronie-anacron
    - ripgrep
```


## flatpak

Adds the `flatpak` directive, allowing you to add remote repos and install flatpak apps.

### Full example

```yaml
- defaults:
    flatpak:
        repo: flathub           # Default repository that will be used for apps
        reinstall: false        # Default for reinstall or if-not-exists

# Every setting is optional
- flatpak:
    repos:                      # Enable various repositories
        - flathub
        - fedora
        - name: flathub-beta
          url: https://flathub.org/beta-repo/flathub-beta.flatpakrepo
        - name: elementary
          url: https://flatpak.elementary.io/repo.flatpakrepo
    apps:                       # Flatpak apps to install
        - com.slack.Slack
        - org.telegram.desktop
        - name: com.discordapp.Discord
          repo: flathub
        - name: io.elementary.calendar
          repo: appcenter-elementary
        - name: com.spotify.Client
          reinstall: true
```

### Minimal example

```yaml
- flatpak:
    apps:
        - com.slack.Slack
        - org.telegram.desktop
        - com.discordapp.Discord
```


## Haskell

> TODO: Install [GHCup](https://www.haskell.org/ghcup/) and [Haskell](https://www.haskell.org/)

## Rust

> TODO: Install [Rustup](https://rustup.rs/) add toolchains, components, targets

* rustup
    * toolchains
    * targets
    * components
* cargo
    * binaries

### Full example

```yaml

```

### Minimal example

```yaml
- rustup:
    install: true
```

## Scala

> TODO: Install [Coursier](https://get-coursier.io/) and [Scala](https://www.scala-lang.org/)

## Write files

Write arbitrary files. Inspired by [cloud-init write_files](https://cloudinit.readthedocs.io/en/latest/reference/modules.html#write-files)

> TODO: Implement this

## Rational

Rational for why a single repository rather than one per plugin.

1. Share common utilities
2. I was getting sick of having so many submodules
3. Why not? Even if you don't use the other plugins, they're only a few python files, its not a big difference.

Feel free to open issues if you wish to discuss.
