from django.db import models

# Create your models here.
class Departamento(models.Model):
    nombre = models.CharField(max_length=50, null=False, unique=True,verbose_name="Nombre")
    descripcion = models.CharField(max_length=255, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre

class Depreciacion(models.Model):
    nombre = models.CharField(max_length=50, null=False, unique=True,verbose_name="Nombre")
    meses = models.SmallIntegerField(verbose_name="Meses")
    valorMinimo = models.FloatField(verbose_name="Valor Mínimo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
class Ubicacion(models.Model):
    nombre = models.CharField(max_length=50, null=False, unique=True,verbose_name="Nombre")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
class Fabricante(models.Model):
    nombre = models.CharField(max_length=50, null=False, unique=True,verbose_name="Nombre")
    descripcion = models.CharField(max_length=255, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
class Categoria(models.Model):
    nombre = models.CharField(max_length=50, null=False, unique=True,verbose_name="Nombre")
    descripcion = models.CharField(max_length=255, verbose_name="Descripción")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
class Modelo(models.Model):
    nombre = models.CharField(max_length=50)
    fabricante = models.ForeignKey(Fabricante, on_delete=models.CASCADE, null=True, blank=True)
    Categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
class Persona(models.Model):
    nombre = models.CharField(max_length=50, null=False, unique=True,verbose_name="Nombre")
    email = models.CharField(max_length=50, verbose_name="Email")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    departamento = models.ForeignKey(Departamento, on_delete=models.CASCADE, null=True, blank=True)
    ci = models.CharField(max_length=20, verbose_name="Ci")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
class Activos(models.Model):
    nombre = models.CharField(max_length=100, null=False,verbose_name="Nombre")
    serial = models.CharField(max_length=50, verbose_name="Serial")
    estado = models.CharField(max_length=20, verbose_name="Estado")
    ultimaAsignacion = models.DateField(verbose_name="Ultima Asignación")
    ultimaDesignacion = models.DateField(verbose_name="Ultima Designación")
    fechaCompra = models.DateField(verbose_name="Fecha de Compra")
    valorCompra = models.FloatField(verbose_name="Valor de Compra")
    valorActual = models.FloatField(verbose_name="Valor Actual")
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True, blank=True)
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, null=True, blank=True)
    depreciacion = models.ForeignKey(Depreciacion, on_delete=models.CASCADE, null=True, blank=True)
    ubicacion = models.ForeignKey(Ubicacion, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre