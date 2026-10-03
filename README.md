# pr-showcase

<p align="center">
  <a href="https://github.com/Aayushyaash/pr-showcase/actions"><img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white" alt="GitHub Actions" /></a>
  <a href="https://pypi.org/project/pr-showcase/"><img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.9+" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-green?style=flat-square" alt="MIT License" /></a>
  <img src="https://img.shields.io/badge/dependencies-0-brightgreen?style=flat-square" alt="Zero Dependencies" />
</p>

<p align="center">
  <strong>Turn your upstream pull requests into an automated, visual open-source portfolio directly inside your GitHub Profile README.</strong>
</p>

---

## ⚡ Highlights

- 🚀 **Single-Query GraphQL Engine**: Collapses all PR, repository, star count, and owner avatar lookups into a single network roundtrip with automated REST fallback.
- 🎨 **Visual Portfolio**: Renders upstream organization avatars (`github.com/<owner>.png`), repository descriptions, and Shields.io live star counts.
- 📂 **Interactive Drawers**: Features recent high-impact merged PRs while gracefully tucking older and in-review contributions into collapsible `<details>` accordions.
- 🛡️ **Zero Dependencies**: Pure Python standard library (`urllib`, `json`, `re`, `argparse`). No `pip install` required for CI runners, zero supply-chain risk.
- 📦 **Dual Modality**: Usable both as a drop-in **GitHub Action** (`uses: Aayushyaash/pr-showcase@v1`) and as a standalone **CLI tool** (`python scripts/update_contributions.py`).

---

## 🚀 Quickstart

### Option A: GitHub Action (Recommended)

In your profile repository (`<username>/<username>`), create `.github/workflows/update-contributions.yml`:

```yaml
name: Update Open Source Contributions

on:
  schedule:
    - cron: '17 2 * * *' # Nightly off-peak run
  workflow_dispatch:      # Manual trigger

permissions:
  contents: write

jobs:
  showcase:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Update Showcase
        uses: Aayushyaash/pr-showcase@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          username: ${{ github.repository_owner }}

      - name: Commit and push changes
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add README.md
          git diff --quiet && git diff --staged --quiet || (git commit -m "chore(readme): auto-update open-source showcase" && git push)
```

> **Important**: Ensure your repository workflow permissions are set to **"Read and write permissions"** under **Settings &rarr; Actions &rarr; General**. See the [Setup Guide](docs/SETUP_GUIDE.md) for details.

### Option B: Local CLI

```bash
# Preview without modifying files
python scripts/update_contributions.py --username <USERNAME> --dry-run

# Update target file directly
python scripts/update_contributions.py --username <USERNAME> --target-file README.md
```

---

## 📖 Documentation

Detailed documentation and technical specifications are available in the [`docs/`](docs/) directory:

- 🛠️ **[Setup & Deployment Guide](docs/SETUP_GUIDE.md)**: Step-by-step setup, workflow permissions, and GitHub Actions cron guidance.
- ⚙️ **[Configuration Reference](docs/CONFIGURATION.md)**: Full parameters table, visibility flags, modular sub-markers, and conflict resolution rules.
- 🏗️ **[Technical Architecture](docs/ARCHITECTURE.md)**: Single-query GraphQL engine, claimed section injection, and atomic marker replacement.

---

## 🌟 Live Demonstration

Below is an example of the standard full showcase rendered by `pr-showcase`:

<!-- CONTRIB:START -->
<p align="center">
  <img src="https://img.shields.io/badge/pull_requests-12-1f6feb?style=flat-square&labelColor=161b22&logo=git&logoColor=white" alt="PRs" />
  <img src="https://img.shields.io/badge/merged-8-8957e5?style=flat-square&labelColor=161b22&logo=github&logoColor=white" alt="Merged" />
  <img src="https://img.shields.io/badge/in_review-4-2da44e?style=flat-square&labelColor=161b22&logo=githubactions&logoColor=white" alt="In Review" />
  <img src="https://img.shields.io/badge/projects-3-f78166?style=flat-square&labelColor=161b22&logo=opensourceinitiative&logoColor=white" alt="Projects" />
</p>


### Merged upstream

**<img src="https://github.com/astral-sh.png?size=64" width="16" height="16" valign="middle" alt="astral-sh" /> [`astral-sh/uv`](https://github.com/astral-sh/uv "An extremely fast Python package and project manager, written in Rust.")**<br/><sub>An extremely fast Python package and project manager, written in Rust.</sub>
- [#4120](https://github.com/astral-sh/uv/pull/4120) feat(resolver): optimize dependency resolution with parallel SAT solver
- [#4098](https://github.com/astral-sh/uv/pull/4098) fix(cli): preserve custom index credentials on lockfile sync

**<img src="https://github.com/neovim.png?size=64" width="16" height="16" valign="middle" alt="neovim" /> [`neovim/neovim`](https://github.com/neovim/neovim "Vim-fork focused on extensibility and usability.")**<br/><sub>Vim-fork focused on extensibility and usability.</sub>
- [#28410](https://github.com/neovim/neovim/pull/28410) feat(lsp): support dynamic registration for workspace folders

**<img src="https://github.com/BurntSushi.png?size=64" width="16" height="16" valign="middle" alt="BurntSushi" /> [`BurntSushi/ripgrep`](https://github.com/BurntSushi/ripgrep "ripgrep recursively searches directories for a regex pattern while respecting your gitignore.")**<br/><sub>ripgrep recursively searches directories for a regex pattern while respecting your gitignore.</sub>
- [#2650](https://github.com/BurntSushi/ripgrep/pull/2650) fix(search): handle utf-16 surrogate pairs in binary detection


### In review

<details>
<summary><b>4 open pull requests across 2 repositories</b></summary>

**<img src="https://github.com/astral-sh.png?size=64" width="16" height="16" valign="middle" alt="astral-sh" /> [`astral-sh/uv`](https://github.com/astral-sh/uv "An extremely fast Python package and project manager, written in Rust.")**
- [#4215](https://github.com/astral-sh/uv/pull/4215) feat(build): add wheel tag validation for musllinux targets

**<img src="https://github.com/neovim.png?size=64" width="16" height="16" valign="middle" alt="neovim" /> [`neovim/neovim`](https://github.com/neovim/neovim "Vim-fork focused on extensibility and usability.")**
- [#28550](https://github.com/neovim/neovim/pull/28550) fix(ui): prevent cursor flicker during fast terminal redraw

</details>


### Contributed to

<p align="left">
  <a href="https://github.com/astral-sh/uv" title="An extremely fast Python package and project manager, written in Rust."><img alt="astral-sh/uv stars" src="https://img.shields.io/github/stars/astral-sh/uv?style=flat-square&logo=github&label=astral-sh%2Fuv&color=1f6feb&labelColor=0d1117" /></a>
  <a href="https://github.com/neovim/neovim" title="Vim-fork focused on extensibility and usability."><img alt="neovim/neovim stars" src="https://img.shields.io/github/stars/neovim/neovim?style=flat-square&logo=github&label=neovim%2Fneovim&color=1f6feb&labelColor=0d1117" /></a>
  <a href="https://github.com/BurntSushi/ripgrep" title="ripgrep recursively searches directories for a regex pattern while respecting your gitignore."><img alt="BurntSushi/ripgrep stars" src="https://img.shields.io/github/stars/BurntSushi/ripgrep?style=flat-square&logo=github&label=BurntSushi%2Fripgrep&color=1f6feb&labelColor=0d1117" /></a>
</p>
<!-- CONTRIB:END -->

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 📜 Acknowledgments

- **Concept Inspiration**: Original profile PR tracking pattern inspired by [@SajalDevX](https://github.com/SajalDevX) ([SajalDevX/SajalDevX](https://github.com/SajalDevX/SajalDevX)).
- **Architecture & Tooling**: Re-engineered by [@Aayushyaash](https://github.com/Aayushyaash) into **`pr-showcase`**, a zero-config, single-query GraphQL engine with automated repository description fetching, organization avatars, interactive drawers, and live star counts.
- **Badges**: Powered by [Shields.io](https://shields.io/).