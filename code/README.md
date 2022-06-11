# FAST API
 
Rest api made with fast api, links:

 - /
 - /clientes/
 - /clientes/{id}

to be able to run uvicorn server you have to run this command in the same path where the main python file is located

    uvicorn main:app --reload

> The command uvicorn main:app refers to:
> - main: the file main.py (the Python "module").
> - app: the object created inside of main.py with the line app = FastAPI().
> - --reload: make the server restart after code changes. Only do this for development.

also you can review all the current links available at http://localhost:8000/docs

You can check  [The official documentation of FAST API](https://fastapi.tiangolo.com/) for more commands and examples.

### Antoher libs used here:

#### Pydantic 

Data validation and settings management using python type annotations. pydantic enforces type hints at runtime, and provides user friendly errors when data is invalid. Define how data should be in pure, canonical python; validate it with pydantic, You can consult [The official documentation of Pydantic.](https://pydantic-docs.helpmanual.io/)

#### Typing

This module provides runtime support for type hints. The most fundamental support consists of the types Any, Union, Callable, TypeVar, and Generic, You can consult [The official documentation of Typing.](https://docs.python.org/3/library/typing.html) 

# PYTEST

run the next command to verify all link made it work as we expected

    pytest -v

> Note: all functions and file name must start with `test` and followed with a `_`

You can consult [The official documentation of Pytest](https://docs.pytest.org/en/7.1.x/) for more commands and examples.