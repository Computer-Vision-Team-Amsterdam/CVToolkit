# CVToolkit
CVToolkit is a collection of essential utilities for computer vision team projects, enhancing reusability and boosting productivity across multiple projects.

## Installation

#### 1. Clone the code

```bash
git clone git@github.com:Computer-Vision-Team-Amsterdam/CVToolkit.git
```

#### 2. Init submodules
You need to initialize the content of the submodules so git clones the latest version.
```bash
git submodule update --init --recursive
```

### 3. Install UV
We use UV as package manager, which can be installed using any method mentioned on [the UV webpage](https://docs.astral.sh/uv/getting-started/installation/).

The easiest option is to use their installer:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

It is also possible to use pip:
```bash
pipx install uv
```

Afterwards, uv can be updated using `uv self update`.

#### 4. Install dependencies
In the terminal, navigate to the project root (the folder containing `pyproject.toml`), then use UV to create a new virtual environment and install the dependencies.

```bash
cd CVToolkit

# Create the environment locally in the folder .venv, for example with python 3.11
uv venv --python 3.11

# Activate the environment
source .venv/bin/activate 

# Install dependencies
uv pip install -r pyproject.toml --extra dev
```

To update dependencies (e.g. when pyproject.toml dependencies change):

```bash
uv lock --upgrade
uv sync --extra dev
```
    
#### 5. Install pre-commit hooks
The pre-commit hooks help to ensure that all committed code is valid and consistently formatted.

```bash
uv tool install pre-commit --with pre-commit-uv --force-reinstall

# Install pre-commit hooks
uv run pre-commit install

# Optional: update pre-commit hooks
uv run pre-commit autoupdate

# Run pre-commit hooks using
uv run .git/hooks/pre-commit
```

#### 6. Run pytest

Tests are included in `tests/`. To run pytest using UV:

```bash
uv run pytest
```
