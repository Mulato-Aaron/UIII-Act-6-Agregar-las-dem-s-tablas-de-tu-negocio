from django.urls import path
from . import views

urlpatterns = [
    # Rutas generales
    path('', views.inicio_sistema, name='inicio_sistema'),
    
    # Rutas para el modelo PROFESOR
    path('profesor/', views.inicio_profesor, name='ver_profesor'),
    path('profesor/agregar/', views.agregar_profesor, name='agregar_profesor'),
    path('profesor/actualizar/<int:profesor_id>/', views.actualizar_profesor, name='actualizar_profesor'),
    path('profesor/actualizar_guardar/<int:profesor_id>/', views.realizar_actualizacion_profesor, name='realizar_actualizacion_profesor'),
    path('profesor/borrar/<int:profesor_id>/', views.borrar_profesor, name='borrar_profesor'),
    path('profesor/detalle/<int:profesor_id>/', views.ver_detalle_profesor, name='ver_detalle_profesor'),

    # Rutas para el modelo CURSO (NUEVAS)
    path('curso/', views.inicio_curso, name='ver_curso'),
    path('curso/detalle/<int:curso_id>/', views.ver_detalle_curso, name='ver_detalle_curso'),
    path('curso/agregar/', views.agregar_curso, name='agregar_curso'),
    path('curso/actualizar/<int:curso_id>/', views.actualizar_curso, name='actualizar_curso'),
    path('curso/actualizar_guardar/<int:curso_id>/', views.realizar_actualizacion_curso, name='realizar_actualizacion_curso'),
    path('curso/borrar/<int:curso_id>/', views.borrar_curso, name='borrar_curso'),

    # Rutas para el modelo ESTUDIANTE (NUEVAS)
    path('estudiante/', views.inicio_estudiante, name='ver_estudiante'),
    path('estudiante/detalle/<int:estudiante_id>/', views.ver_detalle_estudiante, name='ver_detalle_estudiante'),
    path('estudiante/agregar/', views.agregar_estudiante, name='agregar_estudiante'),
    path('estudiante/actualizar/<int:estudiante_id>/', views.actualizar_estudiante, name='actualizar_estudiante'),
    path('estudiante/actualizar_guardar/<int:estudiante_id>/', views.realizar_actualizacion_estudiante, name='realizar_actualizacion_estudiante'),
    path('estudiante/borrar/<int:estudiante_id>/', views.borrar_estudiante, name='borrar_estudiante'),

    # app_Preparatoria/urls.py (Fragmento - Añadir a las rutas existentes)

    # ... (Rutas de Profesor, Curso, Estudiante ya existentes) ...
    
    # Rutas para el modelo INSCRIPCION (NUEVAS)
    path('inscripcion/', views.ver_inscripciones, name='ver_inscripciones'),
    path('inscripcion/agregar/', views.agregar_inscripcion, name='agregar_inscripcion'),
    path('inscripcion/finalizar/<int:inscripcion_id>/', views.finalizar_inscripcion, name='finalizar_inscripcion'),
    path('inscripcion/actualizar/<int:inscripcion_id>/', views.actualizar_inscripcion, name='actualizar_inscripcion'),
    
    # Rutas para el modelo CALIFICACION (NUEVAS)
    path('calificacion/', views.ver_calificaciones_curso, name='ver_calificaciones_curso'),
    path('calificacion/gestionar/<int:curso_id>/', views.ver_calificaciones_por_curso, name='ver_calificaciones_por_curso'),
    path('calificacion/agregar/<int:inscripcion_id>/', views.agregar_calificacion, name='agregar_calificacion'),
    path('inscripcion/actualizar_guardar/<int:inscripcion_id>/', views.realizar_actualizacion_inscripcion, name='realizar_actualizacion_inscripcion'),

    # Rutas para el modelo ASISTENCIA (NUEVAS)
    path('asistencia/', views.seleccionar_curso_asistencia, name='seleccionar_curso_asistencia'),
    path('asistencia/gestionar/<int:curso_id>/', views.gestionar_asistencia, name='gestionar_asistencia'),
    path('asistencia/historial/<int:inscripcion_id>/', views.ver_historial_asistencia_estudiante, name='ver_historial_asistencia_estudiante'),
]