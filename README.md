# Chai aur Tweet

A small Twitter-like Django app.

Local setup

1. Create a virtualenv and install dependencies

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

2. Run migrations and create a superuser

```bash
python chaiheadq/manage.py migrate
python chaiheadq/manage.py createsuperuser
```

3. Run server

```bash
python chaiheadq/manage.py runserver
```

Development notes

- AJAX posting is supported on the tweet creation form.
- Tailwind is included via CDN for quick UI polish; for a production Tailwind build, run the django-tailwind workflow and npm build in the `theme` app.
- Dockerfile and docker-compose are included for containerized runs.
- CI workflow in .github/workflows/ci.yml runs tests.

