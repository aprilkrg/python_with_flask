## Create virtual environment:
We'll use the command `python3 -m venv` to create the environment, and provide the argument `env` to name it. 
```bash
python3 -m venv env
```
Enter the environment with the `source` command, and provide the relative path to the environment created from the previous command.
```bash
source env/bin/activate
```

## Install migration manager:
This will add a `lib` directory to our `env` directory, which will be the equivalent of the `node_modules` directory in node projects.
```bash
pip3 install alembic
```
Next we'll initialize the migrations using alembic. It will create a `migrations` directory and file called `alembic.ini`.
```bash
alembic init migrations
```
Before we can migrate using the `alembic upgrade head` command, we need to set some environment variables.

## Config for alembic
Install `python-dotenv` package using pip3. This will create a `env.py` file in the `migrations` directory.
```bash
pip3 install python-dotenv
```
Add the following lines to the top of the newly created `env.py`:
```python
from dotenv import load_dotenv load_dotenv() 
import os
```
Further down in the same file look for the line `config = context.config`. Add the following lines directly after to modify the config dictionary, we'll also add a print line to show the url in the terminal.
```python
config.set_main_option('sqlalchemy.url', os.environ.get('DATABASE_URL'))
print("DATABASE URL \n", os.environ.get('DATABASE_URL'), "\n")
```
We need a hidden  file to save our database url to, so run the command:
```bash
touch .env
```
Add the following line to the newly created `.env` file
```
DATABASE_URL=postgresql://localhost:5432/python_craigs
```