from django.shortcuts import render, redirect, get_object_or_404
from .models import Profesor, Curso, Estudiante, Inscripcion, Calificacion, Asistencia
from django.urls import reverse
from datetime import date

# 14. Funciones solicitadas para el CRUD de Profesor

def inicio_profesor(request):
    """Muestra la lista de todos los profesores."""
    profesores = Profesor.objects.all()
    context = {'profesores': profesores}
    return render(request, 'profesor/ver_profesor.html', context)

def agregar_profesor(request):
    """Gestiona la adición de un nuevo profesor."""
    if request.method == 'POST':
        # No hay validación de datos (Punto 30)
        nombre = request.POST.get('nombre_profesor')
        apellido = request.POST.get('apellido_profesor')
        correo = request.POST.get('correo_profesor')
        telefono = request.POST.get('telefono')
        especialidad = request.POST.get('especialidad')
        # La fecha de contratación se añade automáticamente
        
        # Crear y guardar el objeto Profesor
        Profesor.objects.create(
            nombre_profesor=nombre,
            apellido_profesor=apellido,
            correo_profesor=correo,
            telefono=telefono,
            especialidad=especialidad
        )
        return redirect('ver_profesor') # Redirige a la lista después de guardar

    return render(request, 'profesor/agregar_profesor.html')

def actualizar_profesor(request, profesor_id):
    """Muestra el formulario para editar un profesor."""
    profesor = get_object_or_404(Profesor, pk=profesor_id)
    context = {'profesor': profesor}
    return render(request, 'profesor/actualizar_profesor.html', context)

def realizar_actualizacion_profesor(request, profesor_id):
    """Procesa el formulario de actualización de un profesor."""
    profesor = get_object_or_404(Profesor, pk=profesor_id)
    if request.method == 'POST':
        # No hay validación de datos (Punto 30)
        profesor.nombre_profesor = request.POST.get('nombre_profesor')
        profesor.apellido_profesor = request.POST.get('apellido_profesor')
        profesor.correo_profesor = request.POST.get('correo_profesor')
        profesor.telefono = request.POST.get('telefono')
        profesor.especialidad = request.POST.get('especialidad')
        # El campo 'activo' se maneja con un checkbox
        profesor.activo = request.POST.get('activo') == 'on'
        
        profesor.save()
        return redirect('ver_profesor')

    # Si por alguna razón no es POST, redirige al formulario de actualización
    return redirect('actualizar_profesor', profesor_id=profesor_id)


def borrar_profesor(request, profesor_id):
    """Gestiona la eliminación de un profesor."""
    profesor = get_object_or_404(Profesor, pk=profesor_id)
    if request.method == 'POST':
        profesor.delete()
        return redirect('ver_profesor')
        
    # El archivo borrar_profesor.html debe ser una página de confirmación
    context = {'profesor': profesor}
    return render(request, 'profesor/borrar_profesor.html', context)

def inicio_sistema(request):
    """Vista para la página de inicio general del sistema."""
    return render(request, 'inicio.html')

# ... (otras funciones existentes)

def ver_detalle_profesor(request, profesor_id):
    """Muestra los detalles de un profesor específico."""
    profesor = get_object_or_404(Profesor, pk=profesor_id)
    context = {'profesor': profesor}
    # Renderizar un nuevo HTML para el detalle
    return render(request, 'profesor/detalle_profesor.html', context)

def inicio_curso(request):
    """Muestra la lista de todos los cursos, incluyendo el profesor asociado."""
    # Usamos select_related para optimizar la consulta y obtener el nombre del profesor
    cursos = Curso.objects.all().select_related('profesor')
    context = {'cursos': cursos}
    return render(request, 'curso/ver_curso.html', context)

def agregar_curso(request):
    """Gestiona la adición de un nuevo curso con selección de profesor."""
    # Solo mostrar profesores activos para la selección
    profesores = Profesor.objects.filter(activo=True) 
    
    if request.method == 'POST':
        # Extracción de datos (sin validación)
        nombre = request.POST.get('nombre_curso')
        codigo = request.POST.get('codigo')
        descripcion = request.POST.get('descripcion')
        creditos = request.POST.get('creditos')
        horario = request.POST.get('horario')
        aula = request.POST.get('aula')
        profesor_id = request.POST.get('profesor')
        
        # Obtener la instancia del Profesor
        profesor_obj = get_object_or_404(Profesor, pk=profesor_id)
        
        Curso.objects.create(
            nombre_curso=nombre,
            codigo=codigo,
            descripcion=descripcion,
            creditos=creditos,
            horario=horario,
            aula=aula,
            profesor=profesor_obj # Asignar el objeto profesor
        )
        return redirect('ver_curso') 

    context = {'profesores': profesores}
    return render(request, 'curso/agregar_curso.html', context)

def actualizar_curso(request, curso_id):
    """Muestra el formulario para editar un curso."""
    curso = get_object_or_404(Curso, pk=curso_id)
    profesores = Profesor.objects.filter(activo=True)
    context = {'curso': curso, 'profesores': profesores}
    return render(request, 'curso/actualizar_curso.html', context)

def realizar_actualizacion_curso(request, curso_id):
    """Procesa el formulario de actualización de un curso."""
    curso = get_object_or_404(Curso, pk=curso_id)
    if request.method == 'POST':
        # Actualización de campos
        curso.nombre_curso = request.POST.get('nombre_curso')
        curso.codigo = request.POST.get('codigo')
        curso.descripcion = request.POST.get('descripcion')
        curso.creditos = request.POST.get('creditos')
        curso.horario = request.POST.get('horario')
        curso.aula = request.POST.get('aula')
        profesor_id = request.POST.get('profesor')
        
        curso.profesor = get_object_or_404(Profesor, pk=profesor_id)
        
        curso.save()
        return redirect('ver_curso')

    return redirect('actualizar_curso', curso_id=curso_id)

def borrar_curso(request, curso_id):
    """Gestiona la eliminación de un curso."""
    curso = get_object_or_404(Curso, pk=curso_id)
    if request.method == 'POST':
        curso.delete()
        return redirect('ver_curso')
        
    # Página de confirmación
    context = {'curso': curso}
    return render(request, 'curso/borrar_curso.html', context)

def ver_detalle_curso(request, curso_id):
    """Muestra los detalles completos de un curso específico."""
    # Usamos select_related para obtener el profesor asociado
    curso = get_object_or_404(Curso.objects.select_related('profesor'), pk=curso_id)
    context = {'curso': curso}
    return render(request, 'curso/ver_detalle_curso.html', context)


def inicio_estudiante(request):
    """Muestra la lista de todos los estudiantes."""
    estudiantes = Estudiante.objects.all()
    context = {'estudiantes': estudiantes}
    return render(request, 'estudiante/ver_estudiante.html', context)

def ver_detalle_estudiante(request, estudiante_id):
    """Muestra los detalles completos de un estudiante específico."""
    estudiante = get_object_or_404(Estudiante.objects.prefetch_related('cursos'), pk=estudiante_id)
    context = {'estudiante': estudiante}
    return render(request, 'estudiante/ver_detalle_estudiante.html', context)

def agregar_estudiante(request):
    """Gestiona la adición de un nuevo estudiante con asignación de cursos."""
    cursos = Curso.objects.all()
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre_estudiante')
        apellido = request.POST.get('apellido_estudiante')
        matricula = request.POST.get('matricula')
        correo = request.POST.get('correo_estudiante')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        cursos_seleccionados = request.POST.getlist('cursos') # Obtiene una lista de IDs

        # Crear y guardar el objeto Estudiante
        nuevo_estudiante = Estudiante.objects.create(
            nombre_estudiante=nombre,
            apellido_estudiante=apellido,
            matricula=matricula,
            correo_estudiante=correo,
            # Aseguramos que la fecha esté en formato YYYY-MM-DD
            fecha_nacimiento=fecha_nacimiento 
        )
        # Asignar los cursos ManyToMany
        nuevo_estudiante.cursos.set(cursos_seleccionados) 
        
        return redirect('ver_estudiante')

    context = {'cursos': cursos}
    return render(request, 'estudiante/agregar_estudiante.html', context)

def actualizar_estudiante(request, estudiante_id):
    """Muestra el formulario para editar un estudiante."""
    estudiante = get_object_or_404(Estudiante.objects.prefetch_related('cursos'), pk=estudiante_id)
    cursos = Curso.objects.all()
    
    # Obtener los IDs de los cursos actualmente asignados
    cursos_actuales_ids = list(estudiante.cursos.values_list('id', flat=True))
    
    context = {
        'estudiante': estudiante,
        'cursos': cursos,
        'cursos_actuales_ids': cursos_actuales_ids
    }
    return render(request, 'estudiante/actualizar_estudiante.html', context)

def realizar_actualizacion_estudiante(request, estudiante_id):
    """Procesa el formulario de actualización de un estudiante."""
    estudiante = get_object_or_404(Estudiante, pk=estudiante_id)
    if request.method == 'POST':
        estudiante.nombre_estudiante = request.POST.get('nombre_estudiante')
        estudiante.apellido_estudiante = request.POST.get('apellido_estudiante')
        estudiante.matricula = request.POST.get('matricula')
        estudiante.correo_estudiante = request.POST.get('correo_estudiante')
        estudiante.fecha_nacimiento = request.POST.get('fecha_nacimiento')
        cursos_seleccionados = request.POST.getlist('cursos')
        
        estudiante.save()
        # Actualizar la relación ManyToMany
        estudiante.cursos.set(cursos_seleccionados)
        
        return redirect('ver_estudiante')

    return redirect('actualizar_estudiante', estudiante_id=estudiante_id)

def borrar_estudiante(request, estudiante_id):
    """Gestiona la eliminación de un estudiante."""
    estudiante = get_object_or_404(Estudiante, pk=estudiante_id)
    if request.method == 'POST':
        estudiante.delete()
        return redirect('ver_estudiante')
        
    context = {'estudiante': estudiante}
    return render(request, 'estudiante/borrar_estudiante.html', context)

# app_Preparatoria/views.py (Fragmento - Añadir a las funciones existentes)

# ==========================================
# INSCRIPCION MANAGEMENT FUNCTIONS (CORREGIDAS)
# ==========================================

def ver_inscripciones(request):
    """Muestra la lista de todas las inscripciones activas."""
    inscripciones = Inscripcion.objects.filter(esta_activo=True).select_related('estudiante', 'curso')
    context = {'inscripciones': inscripciones}
    return render(request, 'inscripcion/ver_inscripciones.html', context)

def agregar_inscripcion(request):
    """Permite inscribir un estudiante en uno o varios cursos."""
    estudiantes = Estudiante.objects.all()
    cursos = Curso.objects.all()
    
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante_id')
        cursos_seleccionados = request.POST.getlist('cursos')
        
        estudiante = get_object_or_404(Estudiante, pk=estudiante_id)
        
        # Asumimos el periodo por defecto del modelo si no se pasa por POST
        periodo_default = '2025-2'
        
        for curso_id in cursos_seleccionados:
            curso = get_object_or_404(Curso, pk=curso_id)
            
            # CORRECCIÓN: Usar get_or_create con el periodo para respetar la nueva clave única
            Inscripcion.objects.get_or_create(
                estudiante=estudiante,
                curso=curso,
                periodo_academico=periodo_default, # Usar el campo clave
                defaults={
                    # Asignamos el campo booleano, si se llegara a crear
                    'es_obligatorio': True 
                }
            )
        
        return redirect('ver_inscripciones')

    context = {'estudiantes': estudiantes, 'cursos': cursos}
    return render(request, 'inscripcion/agregar_inscripcion.html', context)

def finalizar_inscripcion(request, inscripcion_id):
    """Marca una inscripción como inactiva (finalizada)."""
    inscripcion = get_object_or_404(Inscripcion, pk=inscripcion_id)
    
    if request.method == 'POST':
        inscripcion.esta_activo = False
        inscripcion.fecha_finalizacion = date.today()
        inscripcion.save()
        return redirect('ver_inscripciones')
    
    context = {'inscripcion': inscripcion}
    return render(request, 'inscripcion/finalizar_inscripcion.html', context)

# ==========================================
# CALIFICACION MANAGEMENT FUNCTIONS (CORREGIDAS)
# ==========================================

def ver_calificaciones_curso(request):
    """Muestra un resumen de cursos para seleccionar y ver calificaciones."""
    cursos = Curso.objects.all().select_related('profesor')
    context = {'cursos': cursos}
    return render(request, 'calificacion/ver_cursos_calificar.html', context)

def ver_calificaciones_por_curso(request, curso_id):
    """Muestra las inscripciones activas de un curso para asignar/ver calificaciones."""
    curso = get_object_or_404(Curso, pk=curso_id)
    inscripciones = Inscripcion.objects.filter(
        curso=curso, 
        esta_activo=True
    ).select_related('estudiante').prefetch_related('calificaciones')
    
    opciones_tipo = Calificacion.tipo_evaluacion.field.choices
    
    context = {
        'curso': curso,
        'inscripciones': inscripciones,
        'opciones_tipo': opciones_tipo 
    }
    return render(request, 'calificacion/gestionar_calificaciones.html', context)

def agregar_calificacion(request, inscripcion_id):
    """Añade una calificación a una inscripción específica."""
    inscripcion = get_object_or_404(Inscripcion, pk=inscripcion_id)
    
    if request.method == 'POST':
        puntaje = request.POST.get('puntaje')
        tipo_evaluacion = request.POST.get('tipo_evaluacion')
        comentarios = request.POST.get('comentarios')
        
        # CORRECCIÓN: Usamos los valores por defecto del modelo para los nuevos campos:
        # 'porcentaje_peso' (default=100) y 'profesor_asignador' (null=True)
        Calificacion.objects.create(
            inscripcion=inscripcion,
            puntaje=puntaje,
            tipo_evaluacion=tipo_evaluacion,
            comentarios=comentarios
        )
        # NOTA: En un sistema real, se debería obtener 'porcentaje_peso' y 'profesor_asignador' del formulario.
        
        return redirect('ver_calificaciones_por_curso', curso_id=inscripcion.curso.id)
    
    return redirect('ver_calificaciones_por_curso', curso_id=inscripcion.curso.id)

# ==========================================
# ASISTENCIA CRUD FUNCTIONS (CORREGIDAS)
# ==========================================

def seleccionar_curso_asistencia(request):
    """Muestra la lista de cursos para que el usuario seleccione uno y registre la asistencia."""
    cursos = Curso.objects.all().select_related('profesor')
    context = {'cursos': cursos}
    return render(request, 'asistencia/seleccionar_curso_asistencia.html', context)

def gestionar_asistencia(request, curso_id):
    """Muestra y procesa el formulario para registrar la asistencia de los estudiantes de un curso."""
    curso = get_object_or_404(Curso, pk=curso_id)
    hoy = date.today()
    
    inscripciones = Inscripcion.objects.filter(
        curso=curso, 
        esta_activo=True
    ).select_related('estudiante')
    
    asistencias_hoy = {
        asist.inscripcion_id: asist 
        for asist in Asistencia.objects.filter(
            inscripcion__in=inscripciones, 
            fecha=hoy
        )
    }

    if request.method == 'POST':
        # Asumimos valores por defecto del modelo para los nuevos campos:
        # 'justificacion_aprobada' (default=False) y 'tipo_sesion' (default='CLASE')
        
        for inscripcion in inscripciones:
            presente = request.POST.get(f'presente_{inscripcion.id}') == 'on'
            observaciones = request.POST.get(f'observaciones_{inscripcion.id}', '')
            
            if inscripcion.id in asistencias_hoy:
                asistencia = asistencias_hoy[inscripcion.id]
                asistencia.presente = presente
                asistencia.observaciones = observaciones
                # 'justificacion_aprobada' y 'tipo_sesion' mantienen su valor o usan el default del modelo
                asistencia.save()
            else:
                # CORRECCIÓN: Al crear, 'hora_registro' se añade automáticamente (auto_now_add=True)
                Asistencia.objects.create(
                    inscripcion=inscripcion,
                    fecha=hoy, 
                    presente=presente,
                    observaciones=observaciones
                    # 'justificacion_aprobada' y 'tipo_sesion' usan el default del modelo
                )
        
        return redirect('gestionar_asistencia', curso_id=curso_id)

    context = {
        'curso': curso,
        'inscripciones': inscripciones,
        'asistencias_hoy': asistencias_hoy, 
        'fecha_hoy': hoy,
    }
    return render(request, 'asistencia/gestionar_asistencia.html', context)


def ver_historial_asistencia_estudiante(request, inscripcion_id):
    """Muestra el historial completo de asistencia para un estudiante en un curso."""
    inscripcion = get_object_or_404(Inscripcion.objects.select_related('estudiante', 'curso'), pk=inscripcion_id)
    historial = Asistencia.objects.filter(inscripcion=inscripcion).order_by('-fecha')
    
    context = {
        'inscripcion': inscripcion,
        'historial': historial
    }
    return render(request, 'asistencia/historial_asistencia_estudiante.html', context)
