# Contributing

Prior to contributing to this repository, please reach out to the owner of this repository to discuss the changes you wish to make either through creating an issue, emailing the owner, or any other preferred method of communication. 

## Installation
SudokuPy uses `requirements.txt` to keep track of modules used. To install the modules listed in this file, run the following command:

```sh
pip install -r requirements.txt
```
> **Note:** If your changes require additional modules, please add them to the `requirements.txt` file before raising PR. This can be done with the command `pip freeze > requirements.txt`


## Formatting
As the source code formatter, SudokuPy uses [black](https://pypi.org/project/black/). Ensure you run the following command after your changes have been implemented.
```sh
black ./src/
```

## Linting

SudokuPy follows the [PEP8](https://www.python.org/dev/peps/pep-0008/) style guide and uses [pylint](https://pypi.org/project/pylint/) to enforce this. To lint your code, run the following command:
```sh
pylint ./src/
```

## Testing 

SudokuPy uses the [pytest](https://docs.pytest.org/en/stable/) framework for testing. To test the code, run the following command: 
```sh
pytest
```