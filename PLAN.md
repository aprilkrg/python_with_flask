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

## Config for alembic: `dotenv`
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
We'll create that `DATABASE_URL` variable mentioned in `env.py`. First, specify the diaclect as postgresql, and end the url with the name of your database, in this case our database is called python_flask. 

Add the following line to the newly created `.env` file
```
DATABASE_URL=postgresql://localhost:5432/python_flask
```
Now install the `psycopg2` package.

Note: if you get errors about `psycopg2`, try installing `psycopg2-binary` or `wheel`.
```bash
pip3 install psycopg2
```
At this point, we've installed the following packages:
```bash
pip3 list

Package       Version
------------- -------
alembic       1.7.5
greenlet      1.1.2
Mako          1.1.6
MarkupSafe    2.0.1
pip           21.2.4
psycopg2      2.9.3
python-dotenv 0.19.2
setuptools    57.4.0
SQLAlchemy    1.4.29
```
### Create or check database 
You can confirm it has already been created by connecting to the psql shell and listing your databases.
```bash
psql
```
List all the psql databases you have with this command:
```psql
macuser=# \l
```
If the database `python_flask` is listed, then you can skip to the migration step next.

If the database is not listed, you can create it with the `createdb` bash command:
```bash
createdb python_flask
```
or from the psql shell:
```psql
macuser=# CREATE DATABASE python_flask;
```
### Start migration

Let's tell alembic that it's time to make a migration, run:
```bash
alembic upgrade head
```
Which returns,
```bash
DATABASE URL 
 postgresql://localhost:5432/python_flask 

INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
```
When we see our database url printed in the console, and the alembic INFO messages, then we know the migration is ready. 

Next, we need to make the migration with the `alembic revision -m` command, and provide an argument that is our migration message - this argument will be added to the file name created in `migrations/versions`.
```bash
alembic revision -m initial-migration
```
Which returns,
```bash
  Generating /Users/macuser/r-sei/seir-1011/unit-4/python_flask/migrations/version
  s/64d16607c8b6_initial_migration.py ...  done
```
Open the file created at the above path, and we'll add to the `upgrade` and `downgrade` functions, to create and drop the table. We'll fill out the function with the alembic command `create_table`, then call on the sqlalchemy library for the `Column` construct and datatypes.  
```python
def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String, nullable=False, unique=True),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP, server_default=sa.func.now())
    )

def downgrade():
    op.drop_table(
        'users'
    )
```
Now that we've filled out our migration file, time to run the command to send it to the database.
```bash
alembic upgrade head
```
To confirm the migration worked, connect to the database with the `psql` command and provide the database name as an argument. Once inside the psql shell, list related tables.
```bash
psql python_flask

python_flask=# \d
               List of relations
 Schema |      Name       |   Type   |  Owner  
--------+-----------------+----------+---------
 public | alembic_version | table    | macuser
 public | users           | table    | macuser
 public | users_id_seq    | sequence | macuser
(3 rows)
```
A query of the users table will show the anticipated columns,
```psql
python_flask=# SELECT * FROM users;
 id | email | password | timestamp 
----+-------+----------+-----------
(0 rows)
```
So, the steps to complete a migration are: 
<!-- - prepare the migration with `alembic upgrade head` -->
- create the migration version file with `alembic revisions -m ARGUMENT_TACO`
- fill out the file that was created from the previous step with any change you want to make to the database
- migrate the changes with the command `alembic upgrade head`


Now we have a way to connect with our database, which we will use to create our CRUD-able RESTful API. We can test our routes and controllers by creating rows in our users table.


Plan out our next steps,
- we'll need an app.py to run
- we could immediately seperate out the routes and functions into other directories, and import into app.py to test the file connection