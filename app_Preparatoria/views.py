from django.shortcuts import render, redirect, get_object_or_404
from .models import Profesor, Curso, Estudiante, Inscripcion, Calificacion, Asistencia
from django.urls import reverse
from datetime import date, datetime # Importar datetime para el manejo de fechas
from django.db.models import Sum, Count, F, Case, When, FloatField # Importar elementos de agregación

# --------------------------------------------------------------------------
# 1. FUNCIÓN AUXILIAR: GENERACIÓN DINÁMICA DE PERIODOS (CORREGIDA)
# --------------------------------------------------------------------------

def get_periodos_disponibles(duracion_ciclo=4):
    """
    Genera una lista de periodos académicos en formato de RANGO DE AÑOS (YYYY-YYYY).
    'duracion_ciclo' define cuántos años dura el ciclo escolar (ej: 3 o 4 años).
    """
    current_year = date.today().year
    periods = []
    
    # Generamos 5 rangos posibles empezando desde el año actual
    # Esto asegura que siempre haya opciones futuras disponibles en el select.
    for start_year in range(current_year, current_year + 5):
        end_year = start_year + duracion_ciclo
        periods.append(f'{start_year}-{end_year}')
             
    return periods

# --------------------------------------------------------------------------
# 2. VISTAS GENERALES Y PROFESOR (CRUD)
# --------------------------------------------------------------------------

def inicio_sistema(request):
# ... (vistas de profesor sin cambios)
# ...
    return render(request, 'inicio.html')

def inicio_profesor(request):
    """Muestra la lista de todos los profesores."""
    profesores = Profesor.objects.all()
    context = {'profesores': profesores}
    return render(request, 'profesor/ver_profesor.html', context)

def agregar_profesor(request):
    """Gestiona la adición de un nuevo profesor."""
    if request.method == 'POST':
        nombre = request.POST.get('nombre_profesor')
        apellido = request.POST.get('apellido_profesor')
        correo = request.POST.get('correo_profesor')
        telefono = request.POST.get('telefono')
        especialidad = request.POST.get('especialidad')
        
        Profesor.objects.create(
            nombre_profesor=nombre,
            apellido_profesor=apellido,
            correo_profesor=correo,
            telefono=telefono,
            especialidad=especialidad
        )
        return redirect('ver_profesor') 
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
        profesor.nombre_profesor = request.POST.get('nombre_profesor')
        profesor.apellido_profesor = request.POST.get('apellido_profesor')
        profesor.correo_profesor = request.POST.get('correo_profesor')
        profesor.telefono = request.POST.get('telefono')
        profesor.especialidad = request.POST.get('especialidad')
        profesor.activo = request.POST.get('activo') == 'on'
        
        profesor.save()
        return redirect('ver_profesor')
    return redirect('actualizar_profesor', profesor_id=profesor_id)

def borrar_profesor(request, profesor_id):
    """Gestiona la eliminación de un profesor."""
    profesor = get_object_or_404(Profesor, pk=profesor_id)
    if request.method == 'POST':
        profesor.delete()
        return redirect('ver_profesor')
    context = {'profesor': profesor}
    return render(request, 'profesor/borrar_profesor.html', context)

def ver_detalle_profesor(request, profesor_id):
    """Muestra los detalles de un profesor específico."""
    profesor = get_object_or_404(Profesor, pk=profesor_id)
    context = {'profesor': profesor}
    return render(request, 'profesor/detalle_profesor.html', context)

# --------------------------------------------------------------------------
# 3. VISTAS CURSO (CRUD)
# --------------------------------------------------------------------------

def inicio_curso(request):
# ... (vistas de curso sin cambios)
# ...
    """Muestra la lista de todos los cursos, incluyendo el profesor asociado."""
    cursos = Curso.objects.all().select_related('profesor')
    context = {'cursos': cursos}
    return render(request, 'curso/ver_curso.html', context)

def agregar_curso(request):
    """Gestiona la adición de un nuevo curso con selección de profesor."""
    profesores = Profesor.objects.filter(activo=True) 
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre_curso')
        codigo = request.POST.get('codigo')
        descripcion = request.POST.get('descripcion')
        creditos = request.POST.get('creditos')
        horario = request.POST.get('horario')
        aula = request.POST.get('aula')
        profesor_id = request.POST.get('profesor')
        
        profesor_obj = get_object_or_404(Profesor, pk=profesor_id)
        
        Curso.objects.create(
            nombre_curso=nombre,
            codigo=codigo,
            descripcion=descripcion,
            creditos=creditos,
            horario=horario,
            aula=aula,
            profesor=profesor_obj
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
    context = {'curso': curso}
    return render(request, 'curso/borrar_curso.html', context)

def ver_detalle_curso(request, curso_id):
    """Muestra los detalles completos de un curso específico."""
    curso = get_object_or_404(Curso.objects.select_related('profesor'), pk=curso_id)
    context = {'curso': curso}
    return render(request, 'curso/ver_detalle_curso.html', context)

# --------------------------------------------------------------------------
# 4. VISTAS ESTUDIANTE (CRUD)
# --------------------------------------------------------------------------

def inicio_estudiante(request):
# ... (vistas de estudiante sin cambios)
# ...
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
        cursos_seleccionados = request.POST.getlist('cursos')

        nuevo_estudiante = Estudiante.objects.create(
            nombre_estudiante=nombre,
            apellido_estudiante=apellido,
            matricula=matricula,
            correo_estudiante=correo,
            fecha_nacimiento=fecha_nacimiento 
        )
        nuevo_estudiante.cursos.set(cursos_seleccionados) 
        
        return redirect('ver_estudiante')

    context = {'cursos': cursos}
    return render(request, 'estudiante/agregar_estudiante.html', context)

def actualizar_estudiante(request, estudiante_id):
    """Muestra el formulario para editar un estudiante."""
    estudiante = get_object_or_404(Estudiante.objects.prefetch_related('cursos'), pk=estudiante_id)
    cursos = Curso.objects.all()
    
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

# --------------------------------------------------------------------------
# 5. VISTAS INSCRIPCIÓN (CRUD)
# --------------------------------------------------------------------------

def ver_inscripciones(request):
    """Muestra la lista de todas las inscripciones activas."""
    inscripciones = Inscripcion.objects.filter(esta_activo=True).select_related('estudiante', 'curso')
    context = {'inscripciones': inscripciones}
    return render(request, 'inscripcion/ver_inscripciones.html', context)

def agregar_inscripcion(request):
    """Permite inscribir un estudiante en uno o varios cursos, usando periodos dinámicos."""
    estudiantes = Estudiante.objects.all()
    cursos = Curso.objects.all()
    # 🎯 Ajuste la llamada para usar 4 años de ciclo (ej: 2025-2029)
    periodos_disponibles = get_periodos_disponibles(duracion_ciclo=4) 
    
    if request.method == 'POST':
        estudiante_id = request.POST.get('estudiante_id')
        cursos_seleccionados = request.POST.getlist('cursos')
        periodo_seleccionado = request.POST.get('periodo_academico') 
        
        estudiante = get_object_or_404(Estudiante, pk=estudiante_id)
        # ⚠️ Nota: Ya no se usa f'{date.today().year}-2' como fallback.
        periodo_a_usar = periodo_seleccionado 
        
        for curso_id in cursos_seleccionados:
            curso = get_object_or_404(Curso, pk=curso_id)
            
            Inscripcion.objects.get_or_create(
                estudiante=estudiante,
                curso=curso,
                periodo_academico=periodo_a_usar,
                defaults={
                    'es_obligatorio': True 
                }
            )
        return redirect('ver_inscripciones')

    context = {
        'estudiantes': estudiantes, 
        'cursos': cursos,
        'periodos_disponibles': periodos_disponibles
    }
    return render(request, 'inscripcion/agregar_inscripcion.html', context)

def actualizar_inscripcion(request, inscripcion_id):
    """Muestra el formulario para editar una inscripción."""
    inscripcion = get_object_or_404(Inscripcion.objects.select_related('estudiante', 'curso'), pk=inscripcion_id)
    # 🎯 Ajuste la llamada para usar 4 años de ciclo (ej: 2025-2029)
    periodos_disponibles = get_periodos_disponibles(duracion_ciclo=4) 
    
    context = {
        'inscripcion': inscripcion,
        'periodos_disponibles': periodos_disponibles,
    }
    return render(request, 'inscripcion/actualizar_inscripcion.html', context)

def realizar_actualizacion_inscripcion(request, inscripcion_id):
    """Procesa el formulario de actualización de una inscripción."""
    inscripcion = get_object_or_404(Inscripcion, pk=inscripcion_id)
    
    if request.method == 'POST':
        inscripcion.periodo_academico = request.POST.get('periodo_academico')
        inscripcion.es_obligatorio = request.POST.get('es_obligatorio') == 'on'
        
        esta_activo_str = request.POST.get('esta_activo')
        inscripcion.esta_activo = esta_activo_str == 'on'
        
        if not inscripcion.esta_activo and not inscripcion.fecha_finalizacion:
             inscripcion.fecha_finalizacion = date.today()
        elif inscripcion.esta_activo:
             inscripcion.fecha_finalizacion = None

        fecha_finalizacion_str = request.POST.get('fecha_finalizacion')
        if fecha_finalizacion_str:
            try:
                # Usamos datetime.strptime para manejar la conversión de string a date
                inscripcion.fecha_finalizacion = datetime.strptime(fecha_finalizacion_str, '%Y-%m-%d').date()
            except ValueError:
                inscripcion.fecha_finalizacion = None

        inscripcion.save()
        return redirect('ver_inscripciones')

    return redirect('actualizar_inscripcion', inscripcion_id=inscripcion_id)

def finalizar_inscripcion(request, inscripcion_id):
# ... (vistas de inscripción sin cambios)
# ...
    """Marca una inscripción como inactiva (finalizada)."""
    inscripcion = get_object_or_404(Inscripcion, pk=inscripcion_id)
    
    if request.method == 'POST':
        inscripcion.esta_activo = False
        inscripcion.fecha_finalizacion = date.today()
        inscripcion.save()
        return redirect('ver_inscripciones')
    
    context = {'inscripcion': inscripcion}
    return render(request, 'inscripcion/finalizar_inscripcion.html', context)

# --------------------------------------------------------------------------
# 6. VISTAS CALIFICACIÓN (MODIFICADAS PARA CALCULAR PROMEDIO EN LA VISTA)
# --------------------------------------------------------------------------

# ... (vistas de calificación sin cambios)
# ...

def ver_calificaciones_curso(request):
    """Muestra un resumen de cursos para seleccionar y ver calificaciones."""
    cursos = Curso.objects.all().select_related('profesor')
    context = {'cursos': cursos}
    return render(request, 'calificacion/ver_cursos_calificar.html', context)

def ver_calificaciones_por_curso(request, curso_id):
    """Muestra las inscripciones activas de un curso, calcula y muestra el promedio."""
    curso = get_object_or_404(Curso, pk=curso_id)
    
    # Obtener inscripciones, prefetch calificaciones y realizar cálculos de promedio
    inscripciones = Inscripcion.objects.filter(
        curso=curso, 
        esta_activo=True
    ).select_related('estudiante').prefetch_related('calificaciones').annotate(
        # 1. Suma de todos los puntajes
        total_puntaje=Sum('calificaciones__puntaje'),
        # 2. Conteo de calificaciones
        conteo_calificaciones=Count('calificaciones'),
        # 3. Calcular el promedio, evitando división por cero con Case/When
        promedio_simple=Case(
            When(conteo_calificaciones__gt=0, 
                 then=F('total_puntaje') / F('conteo_calificaciones')),
            default=0.0,
            output_field=FloatField()
        )
    )
    
    opciones_tipo = Calificacion.tipo_evaluacion.field.choices
    
    context = {
        'curso': curso,
        # Las inscripciones ahora incluyen 'total_puntaje', 'conteo_calificaciones' y 'promedio_simple'
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
        
        Calificacion.objects.create(
            inscripcion=inscripcion,
            puntaje=puntaje,
            tipo_evaluacion=tipo_evaluacion,
            comentarios=comentarios
        )
        # Redirige de vuelta al curso
        return redirect('ver_calificaciones_por_curso', curso_id=inscripcion.curso.id)
    
    return redirect('ver_calificaciones_por_curso', curso_id=inscripcion.curso.id)

# --------------------------------------------------------------------------
# 7. VISTAS ASISTENCIA
# --------------------------------------------------------------------------

# ... (vistas de asistencia sin cambios)
# ...

def seleccionar_curso_asistencia(request):
    """Muestra la lista de cursos para que el usuario seleccione uno y registre la asistencia."""
    cursos = Curso.objects.all().select_related('profesor')
    context = {'cursos': cursos}
    return render(request, 'asistencia/seleccionar_curso_asistencia.html', context)


def gestionar_asistencia(request, curso_id):
    """Muestra y procesa el formulario para registrar la asistencia de los estudiantes de un curso
         para una fecha seleccionada o la fecha actual por defecto."""
        
    curso = get_object_or_404(Curso, pk=curso_id)
    
    # --- Lógica de la Fecha ---
    fecha_a_usar = date.today()

    if request.method == 'POST':
        fecha_registro_str = request.POST.get('fecha_registro')
        if fecha_registro_str:
            try:
                fecha_a_usar = datetime.strptime(fecha_registro_str, '%Y-%m-%d').date()
            except ValueError:
                pass
    else:
        fecha_param = request.GET.get('fecha')
        if fecha_param:
            try:
                fecha_a_usar = datetime.strptime(fecha_param, '%Y-%m-%d').date()
            except ValueError:
                pass

    if fecha_a_usar > date.today():
          fecha_a_usar = date.today() 
    
    
    # --- Obtención de Datos ---
    inscripciones = Inscripcion.objects.filter(
        curso=curso, 
        esta_activo=True
    ).select_related('estudiante')
    
    asistencias_query = Asistencia.objects.filter(
        inscripcion__in=inscripciones, 
        fecha=fecha_a_usar
    )
    asistencias_hoy = {asist.inscripcion_id: asist for asist in asistencias_query}
    
    for inscripcion in inscripciones:
        inscripcion.registro_asistencia = asistencias_hoy.get(inscripcion.id)


    # --- Procesamiento POST (Guardar datos) ---
    if request.method == 'POST':
        for inscripcion in inscripciones:
            presente = request.POST.get(f'presente_{inscripcion.id}') == 'on'
            observaciones = request.POST.get(f'observaciones_{inscripcion.id}', '')
            justificada = request.POST.get(f'justificada_{inscripcion.id}') == 'on' 
            
            asistencia_obj = inscripcion.registro_asistencia 

            if asistencia_obj:
                # Actualizar asistencia existente
                asistencia_obj.presente = presente
                asistencia_obj.observaciones = observaciones
                asistencia_obj.justificacion_aprobada = justificada
                asistencia_obj.save()
            else:
                # Crear nueva asistencia
                Asistencia.objects.create(
                    inscripcion=inscripcion,
                    fecha=fecha_a_usar,
                    presente=presente,
                    observaciones=observaciones,
                    justificacion_aprobada=justificada
                )
        
        return redirect(f"{reverse('gestionar_asistencia', args=[curso_id])}?fecha={fecha_a_usar}")


    context = {
        'curso': curso,
        'inscripciones': inscripciones,
        'fecha_hoy': fecha_a_usar,
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