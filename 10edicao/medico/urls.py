from django.urls import path
from medico import views

app_name = 'medicos'

urlpatterns = [
    path('cadastro_medico/', views.cadastro_medico, name="cadastro_medico"),
    path('abrir_horario/', views.abrir_horario, name="abrir_horario"),
]