## Run Locally

Clone the project

```bash
  git clone https://github.com/ayyaninam/thepepin-1st
```

Go to the project directory

```bash
  cd thepepin-1st
```

New Virtual Environment

```bash
  python3 -m venv env
```

Active Virtual Environment 


Mac/Linux:

```bash
  source env/bin/activate
```

Windows:

```bash
  env\Scripts\bin\activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Make Migrations

```bash
  python3 manage.py makemigrations
```

Migrate

```bash
  python3 manage.py migrate
```

