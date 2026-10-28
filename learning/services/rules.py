"""Central, deterministic-friendly rules for every generated question."""
from dataclasses import dataclass
from random import Random
from django.utils.translation import get_language

QUESTIONS_PER_SESSION = 10
SECONDS_BY_LEVEL = {1: 60, 2: 50, 3: 40, 4: 30, 5: 25}
OPERATIONS = {"sumar": ("Sumar", "+"), "restar": ("Restar", "−"), "multiplicar": ("Multiplicar", "×"), "dividir": ("Dividir", "÷"), "comparar": ("Comparar", "?"), "problemas": ("Problemas", "💡")}
LEVEL_NAMES = {1: "Primeros pasos", 2: "Practicamos", 3: "Avanzamos", 4: "Un buen reto", 5: "¡Experto/a!"}

@dataclass(frozen=True)
class Question:
    left: int
    right: int
    operation: str
    answer: int
    text: str

def valid_age(age): return age in range(6, 13)
def valid_level(level): return level in range(1, 6)

def _limit(age, level):
    # Each step increases range; older students begin farther along.
    return [10, 20, 50, 100, 250][level - 1] + max(age - 7, 0) * [5, 15, 30, 60, 120][level - 1]

def generate_question(age, operation, level, rng=None):
    if not valid_age(age) or operation not in OPERATIONS or not valid_level(level):
        raise ValueError("Configuración de ejercicio no válida")
    rng = rng or Random()
    limit = _limit(age, level)
    if operation == "sumar":
        left, right = rng.randint(1, limit), rng.randint(1, limit)
        answer = left + right
    elif operation == "restar":
        left, right = rng.randint(1, limit), rng.randint(1, limit)
        left, right = max(left, right), min(left, right)
        answer = left - right
    elif operation == "multiplicar":
        max_factor = min(12 + (level - 1) * 3 + max(age - 9, 0) * 2, 30)
        left, right = rng.randint(1, max_factor), rng.randint(1, max_factor)
        answer = left * right
    elif operation == "dividir":
        max_divisor = min(5 + level * 2 + max(age - 8, 0), 20)
        divisor, answer = rng.randint(2, max_divisor), rng.randint(1, max(3, limit // max_divisor))
        left, right = divisor * answer, divisor
    elif operation == "comparar":
        left, right = rng.randint(1, limit), rng.randint(1, limit)
        while left == right:
            right = rng.randint(1, limit)
        answer = max(left, right)
    else:
        left, right = rng.randint(1, limit), rng.randint(1, limit)
        answer = left + right
    symbol = OPERATIONS[operation][1]
    language = (get_language() or "es").split("-")[0]
    if operation == "comparar":
        text = (f"Which number is greater: {left} or {right}?" if language == "en" else f"Quin nombre és més gran: {left} o {right}?" if language == "ca" else f"¿Qué número es mayor: {left} o {right}?")
    elif operation == "problemas":
        text = (f"You have {left} stickers and receive {right} more. How many do you have?" if language == "en" else f"Tens {left} adhesius i en reps {right} més. Quants en tens?" if language == "ca" else f"Tienes {left} pegatinas y recibes {right} más. ¿Cuántas tienes?")
    else:
        text = f"{left} {symbol} {right}"
    return Question(left, right, operation, answer, text)

def explanation(question):
    language = (get_language() or "es").split("-")[0]
    if language == "en":
        if question.operation == "sumar": return f"{question.text} = {question.answer} because we combine both amounts."
        if question.operation == "restar": return f"{question.text} = {question.answer} because we take {question.right} away from {question.left}."
        if question.operation == "multiplicar": return f"{question.text} = {question.answer} because there are {question.left} groups of {question.right}."
        if question.operation == "dividir": return f"{question.text} = {question.answer} because we split {question.left} into groups of {question.right}."
        if question.operation == "comparar": return f"{question.answer} is greater than the other number."
        if question.operation == "problemas": return f"The answer is {question.answer}."
    if language == "ca":
        if question.operation == "sumar": return f"{question.text} = {question.answer} perquè ajuntem les dues quantitats."
        if question.operation == "restar": return f"{question.text} = {question.answer} perquè traiem {question.right} de {question.left}."
        if question.operation == "multiplicar": return f"{question.text} = {question.answer} perquè són {question.left} grups de {question.right}."
        if question.operation == "dividir": return f"{question.text} = {question.answer} perquè repartim {question.left} en grups de {question.right}."
        if question.operation == "comparar": return f"{question.answer} és més gran que l'altre nombre."
        if question.operation == "problemas": return f"La resposta és {question.answer}."
    if question.operation == "sumar": return f"{question.text} = {question.answer} porque juntamos las dos cantidades."
    if question.operation == "restar": return f"{question.text} = {question.answer} porque quitamos {question.right} de {question.left}."
    if question.operation == "multiplicar": return f"{question.text} = {question.answer} porque son {question.left} grupos de {question.right}."
    if question.operation == "dividir": return f"{question.text} = {question.answer} porque repartimos {question.left} en grupos de {question.right}."
    if question.operation == "comparar": return f"{question.answer} es mayor que el otro número."
    return f"{question.text} La respuesta es {question.answer}."
