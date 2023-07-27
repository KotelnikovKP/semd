# ONCOR Structured Electronic Medical Document
Application for working with ONCOR Structured Electronic Medical Document

## Table of Contents

- [Backend](#Backend)
- [Frontend](#Frontend)

## Backend

REST API interface

---

### How to run Locally?

#### Cloning a project from a repository

```bash
git clone https://github.com/KotelnikovKP/semd.git
```

#### Setting up python environment

Run the following to create a virtual environment for the project. (Assuming you have python installed on local machine)

```bash
# Windows
python -m venv venv

# MacOs + Linux
python3 -m venv venv

```

#### Activating virtual environment

```bash
# Windows
venv/Scripts/activate

# MacOs + Linux
source venv/bin/activate
```

#### Copying the config file `.env`

Assuming you are in the base directory.

```bash
# Windows
copy .env.template .env

# MacOs + Linux
cp .env.template .env
```

#### Installing dependencies

Assuming you are in the base directory.

```bash
pip install -r requirements.txt
```

#### Creating database

Assuming you have PostgreSQL Server installed on local machine. If it is not, then use [PostgreSQL Server Downloads](https://www.postgresql.org/download/)

Run the following to create a schema and user and to grant privileges in `MySQL Command Line Client`

NOTICE! Come up with your own password and substitute it in the command below instead of `password`

```bash
CREATE DATABASE "semd";

CREATE USER "semd" WITH PASSWORD 'password';

ALTER ROLE "semd" SET client_encoding TO 'utf8';
ALTER ROLE "semd" SET default_transaction_isolation TO 'read committed';
ALTER ROLE "semd" SET timezone TO 'UTC';

GRANT ALL PRIVILEGES ON DATABASE "semd" TO "semd";
GRANT ALL ON SCHEMA public TO "semd";
```

#### Changing the .env file

Replace `<password>` with "semd" user password came up above in following line of the `.env` file.

```text
DATABASE_PASSWORD=<password>
```

#### Creating models in the database (run the migration)

```bash
python manage.py migrate 
```

#### Creating an application administrator user

NOTICE! Remember the administrator login and password for further use in the application

```bash
python manage.py createsuperuser
```

#### Running the backend

```bash
python manage.py runserver 
```

---

#### Using Equipment REST API interface

Find out a description of API methods at http://127.0.0.1:8000/api/docs

#### Using Django administration UI for the application

Administration UI is available at http://127.0.0.1:8000/admin/

---

## Frontend

Application web interface 

---

### How to run Locally?

#### Install dependencies

Assuming you have [Node.js](https://nodejs.org/) and [npm](https://www.npmjs.com/) installed on local machine

Go to frontend directory

```bash
cd fronted
```

Run the following

```bash
npm install
```

#### Running the frontend (in dev mode)

```bash
npm run dev
```

#### Using Equipment web interface

Web client is available at http://localhost:3000/

---
