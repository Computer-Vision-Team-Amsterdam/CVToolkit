# CVToolkit
CVToolkit is a collection of essential utilities for computer vision team projects, enhancing reusability and boosting productivity across multiple projects.

## Installation

#### 1. Clone the code

```bash
git clone git@github.com:Computer-Vision-Team-Amsterdam/CVToolkit.git
```

#### 2. Install Poetry
If you don't have it yet, follow the instructions [here](https://python-poetry.org/docs/#installation) to install the package manager Poetry.


#### 3. Init submodules
You need to initialize the content of the submodules so git clones the latest version.
```bash
git submodule update --init --recursive
```

#### 4. Install dependencies
In the terminal, navigate to the project root (the folder containing `pyproject.toml`), then use Poetry to create a new virtual environment and install the dependencies.

```bash
poetry install
```
    
#### 5. Install pre-commit hooks
The pre-commit hooks help to ensure that all committed code is valid and consistently formatted.

```bash
poetry run pre-commit install
```