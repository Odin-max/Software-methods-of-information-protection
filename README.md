# Project setup

The [pipenv](https://pipenv.pypa.io/en/latest/) tool is using as a dependencies tool.

```bash
pipenv shell
python authentication/manage.py runserver
```

# Other

## Pipenv commands

```bash 
# Activate the virtuan environment
pipenv shell 

# install deps
pipenv sync

# install dev deps
pipenv sync --dev

# lock dependencies. Update the Pipfile.lock
pipenv lock

```