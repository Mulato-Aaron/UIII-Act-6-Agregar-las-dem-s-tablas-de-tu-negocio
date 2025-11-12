# app_Preparatoria/admin.py (Ya debe estar así)
from django.contrib import admin
from .models import Profesor, Curso, Estudiante

# Registrar modelos (Punto 10)
admin.site.register(Profesor)
admin.site.register(Curso) # <-- Verificado y Registrado
admin.site.register(Estudiante)