from django.urls import path
from . import views

urlpatterns = [
    path("", views.age, name="age"), path("service-worker.js", views.service_worker, name="service_worker"), path("operaciones/", views.operations, name="operations"),
    path("progreso/", views.dashboard, name="dashboard"), path("progreso/reiniciar/", views.reset_progress, name="reset_progress"),
    path("operaciones/<slug:operation>/niveles/", views.levels, name="levels"),
    path("jugar/<slug:operation>/<int:level>/", views.play, name="play"),
    path("jugar/siguiente/", views.next_question, name="next_question"),
    path("repasar/", views.review, name="review"),
    path("resultados/", views.results, name="results"),
]
