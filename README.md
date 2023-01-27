# Example using Cerbos as Authorization Service + SqlAlchemy/FastAPI

Forked from https://github.com/cerbos/cerbos-sdk-python.

It's highly recommend to have a look first at the [Original README](README.original.md).

This fork has the following purposes:

- Implement unit tests with `pytest`
- Refactor the endpoints moving away the implementation details of the authorization service to its own package
- Extend the policies with some more advanced attributes

## Development

1. Install pdm with pipx

```sh
pipx install pdm
```

2. Install dependencies

```sh
pdm install
```

3. Activate virtualenv

```sh
source (pdm venv activate | awk '{print $2}')
```

### Running the tests

1. Start the Cerbos service: `docker compose up -d`
2. With the virtualenv enabled run: `pytest`

## Example requests

Besides the [original requests](https://github.com/cerbos/python-sqlalchemy-cerbos#example-requests), more examples can be found [here](EXAMPLES.md).
