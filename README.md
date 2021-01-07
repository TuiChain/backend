
# TuiChain: Backend

[![Build status](https://github.com/TuiChain/backend/workflows/build/badge.svg?branch=main)](https://github.com/TuiChain/backend/actions)

Repository for the backend component of the TuiChain application.

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

# test api using HTTPie

## signup

```bash
http post http://127.0.0.1:8000/api/auth/signup/ username="henrique" email="henrique@mail.com" password="soulindo!" first_name="Henrique" last_name="Pereira"
```

This route will return a token which you need to save to use the other endpoints.

## login

```bash
http post http://127.0.0.1:8000/api/auth/login/ username="henrique" password="soulindo!"
```

This route will return a token which you need to save to use the other endpoints.

## create loan request
```bash
http post http://127.0.0.1:8000/api/loanrequests/new/ "Authorization: Token <token_gotten_from_login>" school="Escola da Vida" course="Tráfico de Gomitas" amount=420.69
```

## create investment
```bash
http post http://127.0.0.1:8000/api/investments/new/ "Authorization: Token <token_gotten_from_login>" request=1 amount=69.420
```
