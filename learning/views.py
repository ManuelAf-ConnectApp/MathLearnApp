from datetime import datetime, timedelta
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_http_methods, require_POST
from .services.rules import (LEVEL_NAMES, OPERATIONS, QUESTIONS_PER_SESSION, SECONDS_BY_LEVEL,
                             explanation, generate_question, valid_age, valid_level)

def _age(request):
    age = request.session.get("age")
    return age if isinstance(age, int) and valid_age(age) else None

def _needs_age(request):
    return None if _age(request) else redirect("age")

def _questions_total(game):
    return game.get("questions_total", QUESTIONS_PER_SESSION)

def _progress(request):
    return request.session.get("progress", {})

def _recommended_level(progress, operation):
    """Advance only after a strong result; otherwise reinforce the current level."""
    level_progress = progress.get(operation, {}).get("levels", {})
    for level in range(1, 6):
        if level_progress.get(str(level), {}).get("best_percent", 0) < 80:
            return level
    return 5

def _record_progress(request, game):
    """Store aggregate progress in the browser session only, never by child identity."""
    if game.get("progress_recorded"):
        return
    answers = game["answers"]
    correct = sum(answer["outcome"] == "correct" for answer in answers)
    percent = round(correct * 100 / len(answers)) if answers else 0
    progress = _progress(request)
    operation = progress.get(game["operation"], {})
    operation["completed"] = operation.get("completed", 0) + 1
    operation["best_percent"] = max(operation.get("best_percent", 0), percent)
    operation["last_percent"] = percent
    level_progress = operation.setdefault("levels", {})
    level = level_progress.setdefault(str(game["level"]), {"completed": 0, "best_percent": 0})
    level["completed"] += 1
    level["best_percent"] = max(level["best_percent"], percent)
    progress[game["operation"]] = operation
    request.session["progress"] = progress
    game["progress_recorded"] = True

def _new_question(game):
    question = generate_question(game["age"], game["operation"], game["level"])
    # Do not present exactly the same operation twice in a row.
    for _ in range(8):
        if question.text != game.get("last_question"):
            break
        question = generate_question(game["age"], game["operation"], game["level"])
    game["last_question"] = question.text
    game["question"] = {"left": question.left, "right": question.right, "operation": question.operation,
                        "answer": question.answer, "text": question.text}
    game["state"] = "active"
    game["issued_at"] = timezone.now().isoformat()
    if game["time_mode"] != "untimed":
        seconds = SECONDS_BY_LEVEL[game["level"]] * (2 if game["time_mode"] == "extended" else 1)
        game["expires_at"] = (timezone.now() + timedelta(seconds=seconds)).isoformat()
    else:
        game["expires_at"] = None

@require_http_methods(["GET", "POST"])
def age(request):
    if request.method == "POST":
        try: chosen = int(request.POST.get("age", ""))
        except ValueError: chosen = 0
        mode = request.POST.get("time_mode", "normal")
        if valid_age(chosen) and mode in {"normal", "extended", "untimed"}:
            request.session["age"] = chosen
            request.session["time_mode"] = mode
            request.session["high_contrast"] = request.POST.get("high_contrast") == "true"
            request.session["sound_enabled"] = request.POST.get("sound_enabled") == "true"
            request.session["narration_enabled"] = request.POST.get("narration_enabled") == "true"
            request.session.pop("game", None)
            return redirect("operations")
        return render(request, "learning/age.html", {"error": "Elige una edad entre 6 y 12 años."}, status=400)
    return render(request, "learning/age.html", {"age": _age(request), "time_mode": request.session.get("time_mode", "normal"), "high_contrast": request.session.get("high_contrast", False)})

def operations(request):
    if (go := _needs_age(request)): return go
    progress = _progress(request)
    operations_data = [{"key": key, "name": item[0], "symbol": item[1], "progress": progress.get(key),
                        "recommended_level": _recommended_level(progress, key)}
                       for key, item in OPERATIONS.items()]
    return render(request, "learning/operations.html", {"operations": operations_data, "age": _age(request)})

def dashboard(request):
    if (go := _needs_age(request)): return go
    progress = _progress(request)
    rows = []
    for key, (name, symbol) in OPERATIONS.items():
        stat = progress.get(key)
        if stat:
            rows.append({"name": name, "symbol": symbol, "completed": stat["completed"],
                         "best_percent": stat["best_percent"], "recommended_level": _recommended_level(progress, key)})
    return render(request, "learning/dashboard.html", {"rows": rows, "age": _age(request)})

@require_POST
def reset_progress(request):
    if (go := _needs_age(request)): return go
    request.session.pop("progress", None)
    request.session.pop("game", None)
    return redirect("dashboard")

def service_worker(request):
    script = """const CACHE='mathlearnapp-v1';self.addEventListener('install',event=>event.waitUntil(caches.open(CACHE).then(cache=>cache.addAll(['/','/static/learning/app.css','/static/learning/logo.png']))));self.addEventListener('fetch',event=>{if(event.request.method!=='GET')return;event.respondWith(caches.match(event.request).then(hit=>hit||fetch(event.request).then(response=>{if(new URL(event.request.url).origin===location.origin){const copy=response.clone();caches.open(CACHE).then(cache=>cache.put(event.request,copy));}return response;})));});"""
    return HttpResponse(script, content_type="application/javascript")

def levels(request, operation):
    if (go := _needs_age(request)): return go
    if operation not in OPERATIONS: raise Http404
    recommended_level = _recommended_level(_progress(request), operation)
    levels_data = [{"number": n, "name": LEVEL_NAMES[n], "seconds": SECONDS_BY_LEVEL[n], "questions": QUESTIONS_PER_SESSION,
                    "recommended": n == recommended_level} for n in range(1, 6)]
    return render(request, "learning/levels.html", {"operation": operation, "operation_name": OPERATIONS[operation][0], "levels": levels_data, "age": _age(request), "time_mode": request.session.get("time_mode", "normal")})

@require_http_methods(["GET", "POST"])
def play(request, operation, level):
    if (go := _needs_age(request)): return go
    if operation not in OPERATIONS or not valid_level(level): raise Http404
    game = request.session.get("game")
    if not game or game.get("operation") != operation or game.get("level") != level or game.get("state") == "complete":
        game = {"age": _age(request), "operation": operation, "level": level, "index": 1, "answers": [], "questions_total": QUESTIONS_PER_SESSION, "time_mode": request.session.get("time_mode", "normal")}
        _new_question(game)
        request.session["game"] = game
    feedback = None
    if request.method == "POST":
        # A state guard makes repeated form submissions harmless.
        if game.get("state") != "active":
            return redirect(reverse("play", args=[operation, level]))
        question = game["question"]
        expired = game.get("expires_at") and timezone.now() > datetime.fromisoformat(game["expires_at"])
        raw = request.POST.get("answer", "").strip()
        try: answer = int(raw)
        except ValueError: answer = None
        if expired:
            outcome, message = "timed_out", "Se acabó el tiempo. ¡La siguiente también cuenta!"
        elif answer is None:
            outcome, message = "incorrect", "Escribe un número para comprobar tu respuesta."
        elif answer == question["answer"]:
            outcome, message = "correct", "¡Muy bien! Has encontrado la respuesta."
        else:
            outcome, message = "incorrect", "Casi. Aprendemos también al intentarlo."
        game["answers"].append({"outcome": outcome})
        game["state"] = "answered"
        request.session["game"] = game
        feedback = {"outcome": outcome, "message": message, "solution": question["answer"],
                    "explanation": explanation(type("Q", (), question)())}
    return render(request, "learning/play.html", {"game": game, "question_text": game["question"]["text"], "feedback": feedback,
        "operation_name": OPERATIONS[operation][0], "seconds": SECONDS_BY_LEVEL[level] * (2 if game["time_mode"] == "extended" else 1), "untimed": game["time_mode"] == "untimed"})

@require_POST
def next_question(request):
    if (go := _needs_age(request)): return go
    game = request.session.get("game")
    if not game or game.get("state") != "answered": return redirect("operations")
    if game["index"] >= _questions_total(game):
        game["state"] = "complete"
        _record_progress(request, game)
        request.session["game"] = game
        return redirect("results")
    game["index"] += 1
    _new_question(game)
    request.session["game"] = game
    return redirect(reverse("play", args=[game["operation"], game["level"]]))

def results(request):
    if (go := _needs_age(request)): return go
    game = request.session.get("game")
    if not game or game.get("state") != "complete": return redirect("operations")
    answers = game["answers"]
    correct = sum(a["outcome"] == "correct" for a in answers)
    timed_out = sum(a["outcome"] == "timed_out" for a in answers)
    return render(request, "learning/results.html", {"game": game, "correct": correct, "timed_out": timed_out,
        "incorrect": len(answers) - correct - timed_out, "percent": round(correct * 100 / len(answers)) if answers else 0,
        "has_mistakes": correct < len(answers), "progress": _progress(request).get(game["operation"], {}),
        "operation_name": OPERATIONS[game["operation"]][0]})

@require_POST
def review(request):
    if (go := _needs_age(request)): return go
    completed_game = request.session.get("game")
    if not completed_game or completed_game.get("state") != "complete":
        return redirect("operations")
    review_total = min(5, _questions_total(completed_game))
    game = {"age": _age(request), "operation": completed_game["operation"], "level": completed_game["level"],
            "index": 1, "answers": [], "questions_total": review_total, "is_review": True,
            "time_mode": request.session.get("time_mode", "normal")}
    _new_question(game)
    request.session["game"] = game
    return redirect(reverse("play", args=[game["operation"], game["level"]]))
