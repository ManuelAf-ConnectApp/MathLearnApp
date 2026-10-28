"""Small translation layer for the existing child-facing Spanish copy."""
from django.utils.translation import get_language


COPY = {
    "en": {
        "Saltar al contenido": "Skip to content", "Edad:": "Age:", "Mi progreso": "My progress",
        "Cambiar edad": "Change age", "Idioma": "Language", "Matemáticas para explorar": "Maths to explore",
        "¡Vamos a aprender matemáticas!": "Let's learn maths!", "Elige tu edad. No necesitamos tu nombre ni ningún dato personal.": "Choose your age. We do not need your name or any personal information.",
        "¿Cuántos años tienes?": "How old are you?", "Tiempo para responder": "Time to answer",
        "Tiempo normal": "Standard time", "Tiempo ampliado": "Extra time", "Sin límite de tiempo": "No time limit",
        "Usar modo de alto contraste": "Use high contrast mode", "Leer los ejercicios en voz alta": "Read exercises aloud",
        "Usar sonidos de respuesta": "Use answer sounds", "Estos ajustes son para aprender a tu ritmo y se pueden cambiar después.": "These settings help you learn at your own pace and can be changed later.",
        "Elige una aventura": "Choose an adventure", "¿Qué quieres practicar?": "What would you like to practise?",
        "Practica paso a paso.": "Practise step by step.", "sesiones · mejor resultado:": "sessions · best score:",
        "Siguiente sugerido: nivel": "Suggested next: level", "← Operaciones": "← Operations", "Elige tu nivel": "Choose your level",
        "Nivel": "Level", "recomendado": "recommended", "preguntas ·": "questions ·", "sin límite": "no limit",
        "segundos por pregunta": "seconds per question", "← Niveles": "← Levels", "Repaso recomendado": "Recommended review",
        "Pregunta": "Question", "de": "of", "Tiempo:": "Time:", "Escuchar ejercicio": "Listen to exercise",
        "Tu respuesta": "Your answer", "Comprobar": "Check", "Ver resultados": "See results", "Siguiente": "Next",
        "Repaso terminado": "Review complete", "Sesión terminada": "Session complete", "¡Buen trabajo!": "Great work!",
        "Practicar es una forma estupenda de aprender.": "Practising is a great way to learn.", "correctas": "correct",
        "para seguir practicando": "to keep practising", "sin responder": "unanswered", "Has acertado el": "You got",
        "% de las preguntas.": "% of the questions right.", "has completado": "you have completed", "sesiones. Tu mejor resultado es": "sessions. Your best score is",
        "Repasar lo que cuesta": "Review what is difficult", "Repetir nivel": "Repeat level", "Elegir otro nivel": "Choose another level",
        "Solo en este navegador": "Only in this browser", "Aún no has terminado una sesión. Cuando lo hagas, verás aquí tus mejores resultados.": "You have not finished a session yet. Once you do, you will see your best scores here.",
        "Empezar a practicar": "Start practising", "Reiniciar mi progreso": "Reset my progress", "Sumar": "Addition",
        "Restar": "Subtraction", "Multiplicar": "Multiplication", "Dividir": "Division", "Comparar": "Compare", "Problemas": "Word problems",
        "Primeros pasos": "First steps", "Practicamos": "Let's practise", "Avanzamos": "Moving forward", "Un buen reto": "A good challenge", "¡Experto/a!": "Expert!",
        "Elige una edad entre 6 y 12 años.": "Choose an age between 6 and 12.", "Se acabó el tiempo. ¡La siguiente también cuenta!": "Time is up. The next one counts too!",
        "Escribe un número para comprobar tu respuesta.": "Enter a number to check your answer.", "¡Muy bien! Has encontrado la respuesta.": "Well done! You found the answer.", "Casi. Aprendemos también al intentarlo.": "Almost. We learn by trying too.",
    },
    "ca": {
        "Saltar al contenido": "Vés al contingut", "Edad:": "Edat:", "Mi progreso": "El meu progrés", "Cambiar edad": "Canvia l'edat", "Idioma": "Idioma", "Matemáticas para explorar": "Matemàtiques per explorar", "¡Vamos a aprender matemáticas!": "Aprenem matemàtiques!", "Elige tu edad. No necesitamos tu nombre ni ningún dato personal.": "Tria la teva edat. No necessitem el teu nom ni cap dada personal.", "¿Cuántos años tienes?": "Quants anys tens?", "Tiempo para responder": "Temps per respondre", "Tiempo normal": "Temps normal", "Tiempo ampliado": "Temps ampliat", "Sin límite de tiempo": "Sense límit de temps", "Usar modo de alto contraste": "Utilitza el mode d'alt contrast", "Leer los ejercicios en voz alta": "Llegeix els exercicis en veu alta", "Usar sonidos de respuesta": "Utilitza sons de resposta", "Elige una aventura": "Tria una aventura", "¿Qué quieres practicar?": "Què vols practicar?", "Practica paso a paso.": "Practica pas a pas.", "Nivel": "Nivell", "preguntas ·": "preguntes ·", "sin límite": "sense límit", "segundos por pregunta": "segons per pregunta", "Pregunta": "Pregunta", "Tiempo:": "Temps:", "Tu respuesta": "La teva resposta", "Comprobar": "Comprova", "Ver resultados": "Veure resultats", "Siguiente": "Següent", "Sesión terminada": "Sessió acabada", "¡Buen trabajo!": "Bona feina!", "correctas": "correctes", "sin responder": "sense respondre", "Repetir nivel": "Repeteix el nivell", "Elegir otro nivel": "Tria un altre nivell", "Operaciones": "Operacions", "Sumar": "Suma", "Restar": "Resta", "Multiplicar": "Multiplicació", "Dividir": "Divisió", "Comparar": "Compara", "Problemas": "Problemes", "Primeros pasos": "Primers passos", "Practicamos": "Practiquem", "Avanzamos": "Avancem", "Un buen reto": "Un bon repte", "¡Experto/a!": "Expert/a!", "Elige una edad entre 6 y 12 años.": "Tria una edat entre 6 i 12 anys.", "¡Muy bien! Has encontrado la respuesta.": "Molt bé! Has trobat la resposta.", "Casi. Aprendemos también al intentarlo.": "Gairebé. També aprenem quan ho intentem.",
    },
}


class ChildFacingTranslationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        language = (get_language() or "es").split("-")[0]
        if language not in COPY or not response.get("Content-Type", "").startswith("text/html"):
            return response
        content = response.content.decode(response.charset or "utf-8")
        for source, translated in sorted(COPY[language].items(), key=lambda item: len(item[0]), reverse=True):
            content = content.replace(source, translated)
        response.content = content.encode(response.charset or "utf-8")
        response.headers.pop("Content-Length", None)
        return response
