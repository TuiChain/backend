# backend
Backend Repository for the TuiChain Application

## startup

If virtual environment not set yet:
```bash
python -m venv venv
```

Before anything, activate virtual environment.

MacOS / Linux:
```bash
source venv/bin/activate
```
Windows:
```bash
\venv\Scritps\activate
```

Install packages from requirements.txt:
```bash
pip install -r requirements.txt
```

## create user
```bash
python manage.py createsuperuser --email mail@example.com --username yourusername
```

## run server
```bash
python manage.py runserver <ip>:<port>
```