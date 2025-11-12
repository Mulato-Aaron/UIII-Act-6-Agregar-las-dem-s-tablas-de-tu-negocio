from django.db import models

# ==========================================
# MODELO: PROFESOR
# ==========================================
class Profesor(models.Model):
    nombre_profesor = models.CharField(max_length=50, unique=True)
    apellido_profesor = models.CharField(max_length=50, unique=True)
    correo_profesor = models.EmailField(max_length=100)
    telefono = models.CharField(max_length=15)
    especialidad = models.CharField(max_length=50, default="")
    fecha_contratacion = models.DateField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre_profesor} {self.apellido_profesor}"

# ==========================================
# MODELO: CURSO
# ==========================================
class Curso(models.Model):
    nombre_curso = models.CharField(max_length=50)
    codigo = models.CharField(max_length=10)
    descripcion = models.TextField(max_length=100)
    creditos = models.PositiveIntegerField()
    horario = models.CharField(max_length=50)
    aula = models.CharField(max_length=20)
    profesor = models.ForeignKey(Profesor, related_name="cursos", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre_curso} ({self.codigo})"

# ==========================================
# MODELO: ESTUDIANTE
# ==========================================
class Estudiante(models.Model):
    nombre_estudiante = models.CharField(max_length=50)
    apellido_estudiante = models.CharField(max_length=50)
    matricula = models.CharField(max_length=10, unique=True)
    correo_estudiante = models.EmailField(max_length=100)
    fecha_nacimiento = models.DateField()
    fecha_inscripcion = models.DateField(auto_now_add=True)
    cursos = models.ManyToManyField(Curso, related_name="estudiantes")

    def __str__(self):
        return f"{self.nombre_estudiante} {self.apellido_estudiante}"
    
# ------------------------------------------
# MODELO NUEVO: INSCRIPCION (Tabla Intermedia)
# ------------------------------------------
class Inscripcion(models.Model):
    """Modelo que representa la inscripción de un Estudiante en un Curso."""
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    
    fecha_inscripcion_curso = models.DateField(auto_now_add=True)
    fecha_finalizacion = models.DateField(null=True, blank=True)
    esta_activo = models.BooleanField(default=True)

    class Meta:
        # Evita que un estudiante se inscriba dos veces en el mismo curso
        unique_together = ('estudiante', 'curso')

    def __str__(self):
        return f"Inscripción: {self.estudiante.matricula} en {self.curso.codigo}"


# ------------------------------------------
# MODELO NUEVO: CALIFICACION
# ------------------------------------------
class Calificacion(models.Model):
    """Modelo que guarda una calificación específica para una Inscripción."""
    # Relación a la Inscripción (el evento de que el Estudiante está en el Curso)
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE, related_name='calificaciones')
    
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
    
    puntaje = models.DecimalField(max_digits=5, decimal_places=2) 
    fecha_evaluacion = models.DateField(auto_now_add=True)
    comentarios = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.get_tipo_evaluacion_display()} ({self.puntaje}) para {self.inscripcion.estudiante.matricula}"
    
# ------------------------------------------
# MODELO NUEVO: ASISTENCIA
# ------------------------------------------
class Asistencia(models.Model):
    inscripcion = models.ForeignKey(Inscripcion, on_delete=models.CASCADE, related_name='asistencias')
    fecha = models.DateField(auto_now_add=True)
    presente = models.BooleanField(default=True)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Asistencia de {self.inscripcion.estudiante.matricula} - {self.fecha}"
