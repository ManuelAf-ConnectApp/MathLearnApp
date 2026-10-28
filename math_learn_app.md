# MathLearnApp — Prompt maestro de implementación para Codex

> **Rol:** actúa como ingeniero/a de software sénior especializado/a en Django, diseño de experiencias educativas infantiles, accesibilidad web, seguridad y pruebas automatizadas. Tu objetivo es construir una aplicación web funcional, mantenible y visualmente atractiva, no únicamente un prototipo estático.
>
> **Idioma:** la interfaz, los ejercicios, los mensajes y la documentación funcional estarán inicialmente en **español**. Prepara la aplicación para internacionalización futura mediante el sistema de traducciones de Django.
>
> **Instrucción principal:** analiza primero el repositorio y sus convenciones. Reutiliza y adapta el código existente; no sobrescribas funcionalidades ni archivos sin necesidad. Si el repositorio está vacío, crea el proyecto desde cero. Implementa, verifica con pruebas y documenta lo realizado. No declares terminado lo que no hayas ejecutado o comprobado.

---

## 1. Visión y propósito

**Nombre del producto:** MathLearnApp.

**Tipo:** aplicación web educativa desarrollada con **Python y Django**, dirigida a alumnado de **6 a 12 años**, para practicar y reforzar de manera entretenida las cuatro operaciones aritméticas:

1. Sumar.
2. Restar.
3. Multiplicar.
4. Dividir.

La experiencia ha de ser **simple, positiva, intuitiva, responsiva y adecuada para menores**. El recorrido básico debe funcionar sin cuentas, correo electrónico ni suministro de datos personales. Evita publicidad, enlaces externos innecesarios, rankings públicos y mecánicas que penalicen emocionalmente los errores.

### Objetivos del producto

- Adaptar el contenido a la edad seleccionada, sin confundir edad con capacidad individual.
- Ofrecer cinco niveles progresivos para cada tipo de operación.
- Resolver ejercicios dentro de un tiempo límite visible y comprensible.
- Dar retroalimentación inmediata y pedagógica.
- Permitir repetir ejercicios y mejorar progresivamente.
- Funcionar en móviles, tabletas y ordenadores con teclado o pantalla táctil.

## 2. Stack técnico

**Obligatorio:** Python + Django, plantillas HTML de Django, CSS moderno y JavaScript ligero. Mantén el proyecto compatible con una versión estable y soportada de Django al momento de implementarlo; documenta las versiones efectivamente utilizadas.

**Preferencias:**

- Arquitectura Django convencional, clara y modular (por ejemplo, proyecto `config`, aplicación `learning`; usa nombres distintos solo si el repositorio existente lo justifica).
- Django Templates para vistas del servidor; JavaScript solo para el temporizador y los comportamientos interactivos necesarios. Evita incorporar React/Vue o una API separada sin razón técnica demostrable.
- SQLite para el MVP y configuración preparada para otro motor mediante variables de entorno, sin forzar complejidad prematura.
- Estilos propios usando CSS custom properties; evita dependencias pesadas y recursos CDN obligatorios.
- Generación de operaciones y corrección autoritativas en el servidor; **no exponer las respuestas correctas en HTML, URLs ni JavaScript**.
- No introducir servicios de terceros ni analíticas de seguimiento de menores por defecto.

## 3. Flujo funcional y pantallas

### 3.1. Pantalla inicial: selección de edad

Es la primera pantalla al abrir la aplicación.

- Mostrar logotipo/título **MathLearnApp**, una bienvenida breve (p. ej. «¡Vamos a aprender matemáticas!») y la pregunta **«¿Cuántos años tienes?»**.
- Ofrecer botones grandes y accesibles para las edades **6, 7, 8, 9, 10, 11 y 12 años**.
- No solicitar fecha de nacimiento, nombre real, correo ni otros datos de identificación.
- Validar en servidor que la edad esté dentro de 6–12; no confiar solo en la interfaz.
- Guardar la edad elegida en una sesión de Django, sin asociarla a una identidad.
- Botón claro para confirmar y pasar a operaciones; si la selección ya actúa como confirmación, hacerlo evidente y consistente.
- Proporcionar acceso posterior a **«Cambiar edad»** sin reiniciar la aplicación.

### 3.2. Pantalla de operaciones: cuatro BOX

Una vez seleccionada la edad, mostrar exactamente cuatro tarjetas principales:

1. **Sumar** (`+`)
2. **Restar** (`−`)
3. **Multiplicar** (`×`)
4. **Dividir** (`÷`)

Requisitos:

- BOX grandes, con **esquinas redondeadas** y **fondo azul muy claro**.
- Cada BOX debe contener nombre, símbolo fácilmente reconocible y descripción opcional breve.
- Efectos **hover**, **focus** y **pressed/active** diferenciados, suaves y rápidos; el funcionamiento **no debe depender del hover** en móviles.
- Área táctil amplia, alto contraste y espaciado cómodo.
- Distribución en cuadrícula adaptable: preferentemente 2 × 2 en pantallas medianas y grandes, 1 columna en móviles estrechos si mejora la lectura.
- Enlace de regreso a selección de edad.

### 3.3. Pantalla de selección de nivel

Al elegir operación, mostrar **cinco tarjetas de nivel**, de dificultad creciente, para esa operación y edad:

- **Nivel 1 — Primeros pasos**.
- **Nivel 2 — Practicamos**.
- **Nivel 3 — Avanzamos**.
- **Nivel 4 — Un buen reto**.
- **Nivel 5 — ¡Experto/a!**.

Requisitos visuales:

- Tarjetas con **bordes redondeados**, tamaño considerable y **fondo verde muy claro**.
- Efectos hover/focus/pressed, equivalentes a los BOX de operaciones.
- Cada tarjeta debe indicar nivel, breve descripción, cantidad de preguntas y tiempo disponible de forma comprensible.
- Puede haber un icono sencillo o estrellas decorativas, sin convertir el aprendizaje en una comparación entre niños.
- Permitir acceder a cualquier nivel directamente; **no bloquear niveles de inicio**.

### 3.4. Pantalla de ejercicio

- Mostrar claramente **edad, operación, nivel, ejercicio actual y progreso** (por ejemplo, «Pregunta 2 de 10»).
- Una única operación aritmética principal por pantalla, en tipografía muy visible.
- Respuesta mediante campo numérico grande, teclado numérico del dispositivo cuando sea viable y botón **«Comprobar»**.
- Permitir enviar con Enter cuando sea apropiado y evitar doble envío.
- Temporizador **visible**, con indicación comprensible de tiempo restante; aviso perceptible al quedar poco tiempo, nunca únicamente mediante color o sonido.
- Al responder, mostrar resultado **correcto/incorrecto**, solución y explicación corta adaptada a la edad (p. ej. «8 + 3 = 11 porque contamos tres más desde ocho»), con opción **«Siguiente»**.
- Si vence el plazo, registrar el ejercicio como **sin responder** y mostrar la solución de manera amable. No generar repetidamente múltiples correcciones por expiración y clic simultáneo.
- Facilitar navegación hacia niveles, con confirmación si abandonar descarta una sesión activa.

### 3.5. Pantalla de resultados

Al finalizar la sesión, mostrar:

- Número de respuestas correctas, incorrectas y agotadas por tiempo.
- Total de preguntas respondidas y porcentaje de aciertos cuando tenga sentido.
- Mensaje de ánimo neutral y positivo, evitando lenguaje de fracaso o comparaciones.
- Acciones **«Repetir nivel»**, **«Elegir otro nivel»** y **«Volver a operaciones»**.
- Historial solo durante la sesión actual en el MVP. No crear cuentas ni almacenar perfiles persistentes de menores sin que se solicite expresamente.

## 4. Reglas de dificultad por edad y nivel

La selección de edad debe modificar de verdad la generación de ejercicios. Implementa la lógica como **configuración centralizada y testeable** (no una colección de condiciones dispersas en las vistas).

Utiliza estos **criterios iniciales orientativos** y ajusta los rangos específicos para que la progresión sea consistente en cada edad:

| Edad | Suma y resta | Multiplicación | División |
|---|---|---|---|
| 6–7 | Cantidades pequeñas, sin/luego con llevadas sencillas | Grupos repetidos y tablas iniciales | Repartos exactos muy sencillos |
| 8–9 | Dos y tres cifras, llevadas progresivas | Tablas y factores moderados | Divisiones exactas de complejidad creciente |
| 10–12 | Cifras mayores y más pasos | Factores de una/dos cifras según nivel | Divisiones exactas con divisores mayores |

Reglas obligatorias:

- **Cinco niveles diferentes para cada operación y edad**. Un nivel superior debe aumentar al menos una dimensión de complejidad: rango de operandos, número de cifras, llevadas, tablas, divisor o tiempo, sin saltos arbitrarios.
- Para el MVP, **todas las respuestas son números enteros**. En restas evita resultados negativos; en divisiones utiliza dividendos generados desde `divisor × cociente` para garantizar **cocientes exactos** y divisores no nulos.
- Permite niveles básicos de multiplicación/división a los 6 años, pero utiliza ejemplos adecuados (grupos y repartos), sin afirmar que se exige dominar todo el currículo a esa edad.
- Evita operaciones absurdas, fuera de rango o repetidas consecutivamente; usa aleatoriedad controlable por semilla en pruebas.
- Define una interfaz para el generador (por ejemplo, `generate_question(age, operation, level)`), con tests que validen corrección, rangos y progresión.
- Mantén separadas la **generación**, la **evaluación** y la **presentación** de ejercicios.

## 5. Duración y temporizador

Cada nivel tiene **tiempo máximo por pregunta**. Valores iniciales propuestos (configurables desde un único módulo):

| Nivel | Tiempo por pregunta |
|---|---:|
| 1 | 60 segundos |
| 2 | 50 segundos |
| 3 | 40 segundos |
| 4 | 30 segundos |
| 5 | 25 segundos |

La duración puede ajustarse posteriormente por operación y edad. No la codifiques de forma dispersa. Para esta primera versión, fija **10 preguntas por sesión de nivel** (también configurable).

**Integridad del tiempo:** el servidor registrará la hora de emisión y la caducidad de cada pregunta usando tiempos fiables; JavaScript muestra la cuenta atrás como apoyo visual. El servidor verifica el plazo al corregir y no acepta respuestas fuera de tiempo. Ten en cuenta latencia razonable y accesibilidad; evita errores por zona horaria usando fechas con zona horaria y compara instantes, no relojes visuales.

**Necesidades infantiles:** incorpora un modo opcional **«Sin límite de tiempo»** o **«Tiempo ampliado»**, claramente presentado como ajuste de accesibilidad y disponible sin penalización ni estigmatización; si está activado, la aplicación debe reflejarlo también en las reglas del servidor. Guarda únicamente la preferencia en sesión.

## 6. Diseño visual / UI

Construye una estética educativa, cálida y moderna, sin sobrecarga visual ni apariencia infantil excesiva para los estudiantes mayores.

### Paleta orientativa

- Fondo principal: blanco roto o muy claro.
- BOX de operaciones: azul muy claro (referencia orientativa `#E8F4FF`).
- BOX de niveles: verde muy claro (referencia orientativa `#E8F8EC`).
- Texto: azul marino/gris muy oscuro, con contraste legible.
- Color de acción principal: azul intenso accesible.
- Estados de acierto/error: color + icono + mensaje textual, no solo color.

Ajusta los tonos para cumplir **WCAG 2.2 AA** en contraste donde sea aplicable, especialmente texto, foco y controles. Define los colores en variables CSS para permitir evolución visual.

### Interacciones y accesibilidad

- Bordes redondeados generosos y sombra discreta en tarjetas.
- Efectos hover y active visibles pero suaves; transición corta y alternativa compatible con `prefers-reduced-motion`.
- Estados `:focus-visible` claros, navegación totalmente utilizable con teclado y controles con etiquetas semánticas.
- Tipografía clara, buen espaciado y botones táctiles de al menos 44 × 44 px como objetivo de diseño.
- Mensajes de validación junto al campo y anuncio accesible de correcciones/resultados mediante regiones de estado cuando corresponda, sin saturar lectores de pantalla.
- Temporizador comprensible para lectores de pantalla sin anunciar cada segundo.
- Diseña primero para dispositivos móviles y garantiza adaptación a tabletas y escritorio.

## 7. Rutas y organización sugeridas

Adapta estos nombres a las convenciones actuales del repositorio:

- `/` → selección de edad.
- `/operaciones/` → tarjetas de operaciones.
- `/operaciones/<operacion>/niveles/` → selección de nivel.
- `/jugar/<operacion>/<nivel>/` → sesión de ejercicios.
- `/resultados/` → resumen de sesión.

**Seguridad de flujo:** si no hay edad seleccionada, redirigir a inicio; validar `operacion` contra una lista cerrada y `nivel` en 1–5; proteger peticiones que modifican estado con CSRF y métodos HTTP adecuados. Evitar que recargar o volver atrás duplique respuestas o avance preguntas.

Organiza responsabilidades, por ejemplo:

```text
MathLearnApp/
├── config/                  # Configuración Django, URL y WSGI/ASGI
├── learning/                # Vistas, rutas, servicios y tests
│   ├── services/            # Generación, evaluación, tiempos, reglas
│   └── tests/               # Pruebas unitarias y de integración
├── templates/               # Plantillas base y pantallas
├── static/                  # CSS, JavaScript, iconos propios
├── .env.example             # Variables documentadas sin secretos
├── .gitignore
├── requirements.txt         # O pyproject.toml, según repositorio
└── README.md
```

No impongas esta estructura si la base existente ya dispone de una equivalente correcta.

## 8. Modelo de estado y datos

Para el **MVP no hace falta persistir perfiles infantiles**. Utiliza las sesiones de Django para edad, configuración de accesibilidad y estado mínimo del ejercicio, protegiendo los datos frente a manipulaciones del cliente. Evalúa críticamente el tamaño de sesión y no guardes historiales innecesarios.

El servidor debe controlar qué pregunta está activa, su respuesta correcta, el identificador de pregunta, el plazo y si ya fue corregida. La sesión de juego debe tener una única ruta segura de transición: `creada → pregunta activa → respondida/caducada → siguiente → completada`.

Si las sesiones están basadas en cookies firmadas, **no almacenes respuestas correctas o datos que deban permanecer secretos** dentro de ellas: Django firma pero no cifra necesariamente su contenido. Prefiere almacenamiento de sesión del lado servidor (base de datos o caché gestionada) para proteger las respuestas.

## 9. Seguridad, privacidad y resiliencia

- No solicitar información personal ni registrar analítica identificable del alumnado.
- Configuración segura de Django: `DEBUG=False` en producción, `SECRET_KEY` desde entorno, `ALLOWED_HOSTS`, cookies y HTTPS según entorno, protección CSRF, cabeceras pertinentes.
- Validar todo en servidor, escapar salidas con Django Templates y evitar inserción insegura de HTML.
- No exponer secretos ni configuraciones sensibles en el repositorio.
- Gestionar errores de forma comprensible para estudiantes; mostrar estados vacíos y alternativas de reintento.
- Evitar cookies de terceros, tipografías remotas obligatorias o transferencias de datos a servicios externos.
- Documentar qué datos técnicos almacena Django para que el despliegue pueda ajustarse a las obligaciones legales aplicables cuando hay menores.

## 10. Pruebas y criterios de aceptación

Implementa pruebas automatizadas como mínimo para:

1. Selección de edad válida, edad fuera del rango y acceso directo sin edad.
2. Acceso a las cuatro operaciones y exactamente cinco niveles por cada una.
3. Generación válida por edad, operación y nivel; restas no negativas, divisiones exactas y ausencia de división por cero.
4. Progresión razonable de dificultad y tiempos configurados.
5. Evaluación de respuesta correcta/incorrecta y respuesta fuera de plazo.
6. Protección frente a doble envío, recarga y avance indebido.
7. Cierre de una sesión de 10 preguntas, cómputos correctos y pantalla de resultados.
8. Comportamiento del ajuste sin límite/ampliación de tiempo también en el servidor.
9. CSRF y control de operaciones/niveles manipulados en URL o formulario.
10. Comprobación de plantillas sin respuestas expuestas y ejecución del chequeo de Django.

Además, verifica manualmente, cuando dispongas de navegador o herramientas adecuadas, el diseño responsivo, teclado, estados de foco y temporizador con y sin JavaScript. Si algún paso no puede probarse en el entorno de Codex, **indícalo expresamente** y proporciona el procedimiento exacto para verificarlo.

### Definición de terminado (DoD)

- El usuario puede completar el flujo **edad → operación → nivel → ejercicios → resultados**.
- Las cuatro operaciones funcionan para cualquier edad entre 6 y 12, con cinco niveles cada una.
- El temporizador se aplica correctamente en servidor, sin depender de JavaScript.
- El rediseño visual y los estados hover, focus y pressed funcionan en dispositivos apropiados.
- La aplicación es utilizable desde móvil y por teclado.
- No se muestran respuestas correctas antes de corregir.
- Pruebas relevantes y `python manage.py check` pasan (o las limitaciones se reportan).
- README y comandos de arranque están actualizados.

## 11. README.md y documentación

Crea o actualiza un **README.md** profesional que incluya:

- Descripción, público objetivo y funcionalidades reales.
- Capturas solo si pueden producirse; no inventes imágenes ni marques como implementado lo pendiente.
- Requisitos y versiones de Python/Django utilizadas.
- Instalación local y creación de entorno virtual.
- Configuración de variables de entorno, migraciones si existen y ejecución del servidor.
- Comandos para ejecutar pruebas y comprobaciones.
- Organización del proyecto y explicación de reglas de niveles/tiempos.
- Ajustes de accesibilidad, privacidad y consideraciones para producción.
- Limitaciones conocidas y mejoras futuras.

**No asumas una licencia Open Source concreta sin autorización.** Si no existe un archivo LICENSE, señálalo como decisión pendiente; no asignes derechos ni titularidades inexistentes.

## 12. Plan de ejecución exigido a Codex

Trabaja de manera autónoma dentro de los límites del repositorio y sigue este orden:

**Fase 1 — Inspección.** Examina la estructura, dependencias, funcionalidades existentes y pruebas. Resume hallazgos en pocas líneas e identifica incompatibilidades con estos requisitos.

**Fase 2 — Diseño de la solución.** Define rutas, servicios, configuración de dificultad, flujo de estados, gestión de sesiones y decisión técnica del temporizador. Resuelve ambigüedades menores con criterios simples y documentados; pregunta solo si hay una decisión bloqueante o con impacto irreversible.

**Fase 3 — Implementación.** Construye las pantallas, estilos responsivos, lógica matemática, sesiones, temporizador fiable y resultados. Mantén el código claro, desacoplado y sin complejidad artificial.

**Fase 4 — Calidad.** Añade y ejecuta las pruebas disponibles, corrige fallos, ejecuta comprobaciones Django y revisa accesibilidad básica.

**Fase 5 — Documentación y entrega.** Actualiza README, muestra los archivos principales modificados, comandos ejecutados con sus resultados, decisiones de diseño, limitaciones pendientes y siguientes mejoras sugeridas.

## 13. Restricciones y prioridades

1. **Primero corrección pedagógica y matemática; después estética.** Ambas deben formar parte de la entrega.
2. No reemplazar la aplicación existente sin inspeccionarla.
3. No añadir cuentas de menores, gamificación competitiva ni servicios externos no solicitados.
4. No utilizar un temporizador solo cliente como mecanismo fiable para aceptar respuestas.
5. No introducir preguntas con resultados decimales, divisiones por cero o restas negativas en el MVP.
6. No exponer soluciones anticipadamente ni aceptar respuestas duplicadas.
7. Mantener los **cuatro BOX azules** y los **cinco BOX verdes por operación** como requisito visual central.
8. Usar textos claros y positivos adecuados para niños de 6 a 12 años.
9. Priorizar una **primera versión plenamente ejecutable** frente a características secundarias.

---

## 14. Resultado que debes entregar

Una **MathLearnApp funcional en Django**, con código fuente organizado, interfaz atractiva y responsiva, flujo educativo completo, dificultad real ajustada por edad, cinco niveles por operación, temporización robusta, feedback pedagógico, pruebas y documentación suficiente para instalar y ejecutar el proyecto.

**Comienza inspeccionando el repositorio. Luego implementa la aplicación; no te limites a explicar cómo se desarrollaría.**
