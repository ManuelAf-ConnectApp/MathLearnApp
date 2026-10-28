# MathLearnApp

MathLearnApp is a Spanish-language Django application that helps children aged 6 to 12 practise addition, subtraction, multiplication, and division. It does not require accounts or personal information. Each operation includes five levels, ten-question sessions, instructional feedback, and a server-validated timer.

## Requirements

- Python 3.10 or newer
- Django 5.2 through 6.0 (as declared in `requirements.txt`)

## Getting started

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Visit <http://127.0.0.1:8000/>. Run checks with `python manage.py test` and `python manage.py check`.

## How it works

- `learning/services/rules.py` centralizes rules, time limits, and testable question generation. Subtractions never produce negative results and divisions always have exact results.
- `learning/views.py` manages session state: active question, answered or expired question, next question, then completion. Django database-backed sessions keep the solution out of the client.
- `templates/` and `static/` contain Django templates, responsive CSS, and JavaScript used only for the visible countdown. The server always validates timeouts.

The **extended time** mode doubles the time available. **Untimed** mode disables expiry both in the user interface and on the server. The application has no analytics or child profiles. It keeps aggregate completed-session counts and best scores only in the browser's Django session, without tying them to a child identity; a short review session is offered after answers that need more practice.

## Production

Before deployment, configure `SECRET_KEY`, set `DEBUG=False`, restrict `ALLOWED_HOSTS`, enable HTTPS, and use an appropriate production database.

## License

MathLearnApp is licensed under the [Apache License 2.0](LICENSE). See [NOTICE](NOTICE) for attribution notices. Spanish documentation: [README.es.md](README.es.md).
