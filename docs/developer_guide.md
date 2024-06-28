# Developer Guide

## Setup

### Set up the environmental variables
1. copy and rename `.env.template` to `.env` in the same folder
1. open `.env` with a text editor and fill in your API key in the `INVENIORDM_API_KEY` variable
1. fill in the InvenioRDM base URL in the `INVENIORDM_BASE_URL` variable
    - in case of Zenodo Sandbox: use `https://sandbox.zenodo.org/`
    - in case of TU Wien test instance: use `https://test.researchdata.tuwien.ac.at/`
1. Run `source .env` to set the environment variables for the session

If you prefer to set the environment variables `INVENIORDM_API_KEY` and `INVENIORDM_BASE_URL` another way (e.g. in `~/.bashrc`), you can do that instead. However, the `.env` file must also be configured as it is used by `pytest`.

### Set up the Python environment

If you do not already have `poetry` installed, install it following the [Poetry installation documentation](https://python-poetry.org/docs/#installation).

Then install dependencies from `poetry.lock`:

```bash
cd ro-crate-inveniordm
poetry install
```

Activate the virtual environment:
```bash
poetry shell
```

## Run tests

Beware that tests can make Zenodo uploads using your access token.

In the root directory:
```bash
pytest
```

## Publish a release

1. Update the version in `pyproject.toml`
2. Make a git tag for the release and push it to GitHub
3. Run `poetry build`
4. Run `poetry publish -u <username> -p <password_or_api_key>`
5. Create a release on GitHub, including the build artifacts

## Project structure

The project consists of the following structure:

- `/src/rocrate_inveniordm/`: Source code for the package
  - `mapping/`: Contains code for the mapping process
    - `converter.py`: Python script used to map between RO-Crates and DataCite. Not to be called by the user.
    - `mapping.json`: Encodes the mapping between RO-Crates and DataCite. See [Mapping](docs/mapping.md) for more. 
    - `condition_functions.py`: Defines functions used for the mapping. See [Conditon Functions](docs/mapping.md#condition-functions) for more.
    - `processing_functions.py`: Defines functions used for the mapping. See [Processing Functions](docs/mapping.md#processing-functions) for more.
  - `upload/`: Contains code for the upload process
    - `uploader.py`: Python script used to upload the files to the InvenioRDM. Not to be called by the user.
  - `deposit.py`: Starting point. Used to map and upload the RO-Crate directory.
- `.env.template`: Template file for the environment variables.
- `/docs`: contains documentation
- `/test`: contains tests and test data
