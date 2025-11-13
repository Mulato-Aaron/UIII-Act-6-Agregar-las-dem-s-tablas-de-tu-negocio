from django.db import models
from datetime import date # Necesario para Asistencia

# ==========================================
# MODELO: PROFESOR (7 campos existentes)
# ==========================================
class Profesor(models.Model):
    nombre_profesor = models.CharField(max_length=50)
    apellido_profesor = models.CharField(max_length=50)
    correo_profesor = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=15)
    especialidad = models.CharField(max_length=50, default="")
    fecha_contratacion = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre_profesor} {self.apellido_profesor}"

# ==========================================
# MODELO: CURSO (7 campos existentes)
# ==========================================
class Curso(models.Model):
    nombre_curso = models.CharField(max_length=50)
    codigo = models.CharField(max_length=10, unique=True)
    descripcion = models.TextField(max_length=100)
    creditos = models.PositiveIntegerField()
    horario = models.CharField(max_length=50)
    aula = models.CharField(max_length=20)
    profesor = models.ForeignKey(Profesor, related_name="cursos", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre_curso} ({self.codigo})"

# ==========================================
# MODELO: ESTUDIANTE (7 campos existentes)
# ==========================================
class Estudiante(models.Model):
    nombre_estudiante = models.CharField(max_length=50)
    apellido_estudiante = models.CharField(max_length=50)
    matricula = models.CharField(max_length=10, unique=True)
    correo_estudiante = models.EmailField(max_length=100)
    fecha_nacimiento = models.DateField()
    fecha_inscripcion = models.DateField(auto_now_add=True)
    # Cambiamos la relación para usar Inscripcion como tabla intermedia
    cursos = models.ManyToManyField(Curso, through='Inscripcion', related_name="estudiantes_inscritos")

    def __str__(self):
        return f"{self.nombre_estudiante} {self.apellido_estudiante}"
    
# ------------------------------------------
# MODELO: INSCRIPCION (7 campos) 🚀
# ------------------------------------------
class Inscripcion(models.Model):
    """Modelo que representa la inscripción de un Estudiante en un Curso."""
    # 1. Foreign Key a Estudiante
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    # 2. Foreign Key a Curso
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    
    # 3. Fecha de inicio
    fecha_inscripcion_curso = models.DateField(auto_now_add=True)
    # 4. Fecha de finalización
    fecha_finalizacion = models.DateField(null=True, blank=True)
    # 5. Estado
    esta_activo = models.BooleanField(default=True)
    
    # 6. Semestre o Periodo
    periodo_academico = models.CharField(max_length=50, default="2025-2") # Campo nuevo
    # 7. Requerido (Indica si el curso es obligatorio)
    es_obligatorio = models.BooleanField(default=True) # Campo nuevo

    class Meta:
        unique_together = ('estudiante', 'curso', 'periodo_academico') # Ajuste para permitir reinscripción en otro periodo

    def __str__(self):
        return f"Inscripción: {self.estudiante.matricula} en {self.curso.codigo} ({self.periodo_academico})"


# ------------------------------------------
# MODELO: CALIFICACION (7 campos) 🚀
# ------------------------------------------
class Calificacion(models.Model):
    """Modelo que guarda una calificación específica para una Inscripción."""
    # 1. Foreign Key a Inscripcion
    inscripcion = models.ForeignKey('Inscripcion', on_delete=models.CASCADE, related_name='calificaciones')
    
    # 2. Tipo de Evaluación
    tipo_evaluacion = models.CharField(
        max_length=50, 
        choices=[
            ('PARCIAL_1', 'Examen Parcial 1'),
            ('PARCIAL_2', 'Examen Parcial 2'),
            ('PROYECTO', 'Proyecto Final'),
            ('FINAL', 'Calificación Final'),
            ('OTRO', 'Otro')
        ],
        default='OTRO'
    )
    
    # 3. Puntaje
    puntaje = models.DecimalField(max_digits=5, decimal_places=2) 
    # 4. Fecha de Evaluación
    fecha_evaluacion = models.DateField(default=date.today) # Usamos default en lugar de auto_now_add
    # 5. Comentarios
    comentarios = models.TextField(null=True, blank=True)

    # 6. Peso de la calificación (para el promedio)
    porcentaje_peso = models.PositiveIntegerField(default=100) # Campo nuevo
    # 7. Profesor que asignó la nota
    profesor_asignador = models.ForeignKey(
        Profesor, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='notas_asignadas'
    ) # Campo nuevo

    def __str__(self):
        return f"{self.get_tipo_evaluacion_display()} ({self.puntaje}) para {self.inscripcion.estudiante.matricula}"
    
# ------------------------------------------
# MODELO: ASISTENCIA (7 campos) 🚀
# ------------------------------------------
class Asistencia(models.Model):
    """Registro de asistencia diaria para un estudiante en un curso específico (Inscripción)."""
    # 1. Foreign Key a Inscripcion
    inscripcion = models.ForeignKey('Inscripcion', on_delete=models.CASCADE, related_name='asistencias')
    # 2. Fecha
    fecha = models.DateField(default=date.today)
    # 3. Estado
    presente = models.BooleanField(default=True)
    # 4. Observaciones
    observaciones = models.TextField(blank=True, null=True)

    # 5. Hora de Registro
    hora_registro = models.TimeField(auto_now_add=True) # Campo nuevo
    # 6. Justificación (Si es Ausente)
    justificacion_aprobada = models.BooleanField(default=False) # Campo nuevo
    # 7. Tipo de Sesión (Ej: Clase, Laboratorio, Examen)
    tipo_sesion = models.CharField(
        max_length=20, 
        choices=[
            ('CLASE', 'Clase Regular'),
            ('LAB', 'Laboratorio'),
            ('EXAMEN', 'Examen')
        ],
        default='CLASE'
    ) # Campo nuevo

    class Meta:
        # Asegura que solo haya un registro de asistencia por inscripción por día
        unique_together = ('inscripcion', 'fecha')

    def __str__(self):
        return f"Asistencia de {self.inscripcion.estudiante.matricula} - {self.fecha} ({'Presente' if self.presente else 'Ausente'})"