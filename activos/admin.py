from django.contrib import admin
from .models import Departamento, Depreciacion, Ubicacion, Fabricante, Categoria, Modelo, Persona, Activos 

# Register your models here.
admin.site.register(Departamento)
admin.site.register(Depreciacion)
admin.site.register(Ubicacion)
admin.site.register(Fabricante)
admin.site.register(Categoria)
admin.site.register(Modelo)
admin.site.register(Persona)
admin.site.register(Activos)