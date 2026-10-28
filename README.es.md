# MathLearnApp

Aplicación Django en español para que alumnado de 6 a 12 años practique suma, resta, multiplicación y división sin crear cuentas ni aportar datos personales. Incluye cinco niveles por operación, diez preguntas por sesión, corrección pedagógica y un temporizador validado por el servidor.

## Requisitos y arranque

Requiere Python 3.10+ y Django 5.2–6.0 (declarado en `requirements.txt`). Cree un entorno virtual e instale dependencias:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Abra <http://127.0.0.1:8000/>. Ejecute `python manage.py test` y `python manage.py check` para probar el proyecto.

## Diseño técnico

- `learning/services/rules.py`: reglas centralizadas, tiempos y generación testeable. Restas sin negativos y divisiones exactas.
- `learning/views.py`: flujo de estado en sesión: pregunta activa → respondida/caducada → siguiente → completa. Las sesiones de base de datos de Django mantienen la solución fuera del cliente.
- `templates/` y `static/`: plantillas Django, CSS responsive y JavaScript limitado a la cuenta atrás visual. El servidor comprueba siempre la caducidad.

El modo **tiempo ampliado** duplica el tiempo y **sin límite** elimina el vencimiento también en servidor. No hay analítica ni perfiles infantiles. Los recuentos de sesiones completadas y la mejor marca se guardan únicamente en la sesión de Django del navegador, sin vincularlos a una identidad; tras los errores se ofrece un repaso breve.

## Producción

Antes del despliegue configure `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`, HTTPS y una base de datos apropiada.

## Licencia

MathLearnApp se distribuye bajo la [licencia Apache 2.0](LICENSE). Consulte [NOTICE](NOTICE) para los avisos de atribución. Documentación inglesa: [README.md](README.md).
