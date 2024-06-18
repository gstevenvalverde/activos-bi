from itertools import count
import graphene
from graphene_django import DjangoObjectType
from activos.models import Activos 
from django.db.models import Count
from django.db.models import Sum


class ActivoType(DjangoObjectType):
    class Meta:
        model = Activos
        fields = ("nombre", "serial", "estado", "fechaCompra", "valorCompra", "valorActual", "persona", "modelo", "depreciacion", "ubicacion","categoria", "fabricante", "etiqueta", "ultimaAsignacion", "ultimaDesasignacion") 

class CategoriaCount(graphene.ObjectType):
    name = graphene.String()
    y = graphene.Int()
    drilldown = graphene.String()
    
    
# Define un objeto GraphQL para representar cada activo con su cantidad en una categoría
class ActivoCantidad(graphene.ObjectType):
    name = graphene.String()
    cantidad = graphene.Int()

# Define un objeto GraphQL para representar cada categoría con sus activos y cantidades
class CategoriaActivos(graphene.ObjectType):
    id = graphene.String()
    name = graphene.String()
    type = graphene.String()
    data = graphene.List(graphene.List(graphene.String, graphene.Int))
    
    
class PersonaCantidadActivos(graphene.ObjectType):
    name = graphene.String()
    y = graphene.Int()
    drilldown = graphene.String()
    
class ModeloCantPersonas(graphene.ObjectType):
    name = graphene.String()
    y = graphene.Int()
    drilldown = graphene.String()
    
class Estadisticas(graphene.ObjectType):
    total_personas = graphene.Int()
    total_activos = graphene.Int()
    total_modelos = graphene.Int()
    
class TotalValoresPorModeloType(graphene.ObjectType):
    modelo = graphene.String()
    valorCompraTotal = graphene.Float()
    valorActualTotal = graphene.Float()

class ActivoInput(graphene.InputObjectType):
    persona = graphene.String(required=False)
    depreciacion = graphene.String(required=False)
    categoria = graphene.String(required=False)
    fabricante = graphene.String(required=False)
    estado = graphene.String(required=False)
    etiqueta = graphene.String(required=False)
    fechaCompra = graphene.String(required=False)
    id = graphene.ID()
    modelo = graphene.String(required=False)
    nombre = graphene.String(required=False)
    serial = graphene.String(required=False)
    ubicacion = graphene.String(required=False)
    ultimaAsignacion = graphene.String(required=False)
    ultimaDesasignacion = graphene.String(required=False)
    valorActual = graphene.String(required=False)
    valorCompra = graphene.String(required=False)

class CreateActivosMutation(graphene.Mutation):
    # Inputs que espera recibir
    class Arguments:
        activo = graphene.Argument(ActivoInput, required=False)

    persona = graphene.String()
    depreciacion = graphene.String()
    estado = graphene.String()
    etiqueta = graphene.String()
    fechaCompra = graphene.String()
    id = graphene.ID()
    modelo = graphene.String()
    nombre = graphene.String()
    serial = graphene.String()
    ubicacion = graphene.String()
    categoria = graphene.String()
    fabricante = graphene.String()
    ultimaAsignacion = graphene.String()
    ultimaDesasignacion = graphene.String()
    valorActual = graphene.String()
    valorCompra = graphene.String()

    def mutate(self, info, activo):
        """ persona_data = activo.pop('persona', None)
        depreciacion_data = activo.pop('depreciacion', None)
        modelo_data = activo.pop('modelo', None)
        ubicacion_data = activo.pop('ubicacion', None)

        persona_instance = Persona.objects.create(**persona_data)
        depreciacion_instance = Depreciacion.objects.create(**depreciacion_data)
        modelo_instance = Modelo.objects.create(**modelo_data)
        ubicacion_instance = Ubicacion.objects.create(**ubicacion_data) """

        activo_instance = Activos.objects.create(
            **activo
        )

        return CreateActivosMutation(
            persona=activo_instance.persona,
            depreciacion=activo_instance.depreciacion,
            estado=activo_instance.estado,
            etiqueta=activo_instance.etiqueta,
            fechaCompra=activo_instance.fechaCompra,
            id=activo_instance.id,
            modelo=activo_instance.modelo,
            nombre=activo_instance.nombre,
            serial=activo_instance.serial,
            ubicacion=activo_instance.ubicacion,
            categoria=activo_instance.categoria,
            fabricante=activo_instance.fabricante,
            ultimaAsignacion=activo_instance.ultimaAsignacion,
            ultimaDesasignacion=activo_instance.ultimaDesasignacion,
            valorActual=activo_instance.valorActual,
            valorCompra=activo_instance.valorCompra,
        )
    



    
""" class UpdateActivosMutation(graphene.Mutation):
    # Inputs que espera recibir
    class Arguments:
        id = graphene.ID(required = True)
        nombre = graphene.String()
        serial = graphene.String()
        estado = graphene.String()
        ultimaAsignacion = graphene.Date()
        ultimaDesignacion = graphene.Date()
        fechaCompra = graphene.Date()
        valorCompra = graphene.Float()
        valorActual = graphene.Float()
        persona = graphene.Int()
        modelo = graphene.Int()
        depreciacion = graphene.Int()
        ubicacion = graphene.Int()

    activo = graphene.Field(ActivoType)

    # Datos que espera devolver
    def mutate(self, info, id, nombre, serial, estado, ultimaAsignacion, ultimaDesignacion, fechaCompra, valorCompra, valorActual, persona, modelo, depreciacion, ubicacion):
        activo = Activos.objects.get(pk = id)
        activo.nombre =nombre
        activo.serial = serial
        activo.estado = estado
        activo.ultimaAsignacion = ultimaAsignacion
        activo.ultimaDesignacion = ultimaDesignacion
        activo.fechaCompra = fechaCompra
        activo.valorCompra = valorCompra
        activo.valorActual = valorActual
        activo.persona = persona
        activo.modelo = modelo
        activo.depreciacion = depreciacion
        activo.ubicacion = ubicacion
        activo.save()
        return UpdateActivosMutation(activo = activo) """

class Query(graphene.ObjectType):
   
    activos = graphene.List(ActivoType)
    
    categorias_con_activos = graphene.List(CategoriaCount)
    
    categoria_activos = graphene.List(CategoriaActivos)
    
    personas_cantidad_activos = graphene.List(PersonaCantidadActivos)
    
    modelos_cantidad_personas = graphene.List(ModeloCantPersonas)
    
    estadisticas = graphene.Field(Estadisticas)
    
    total_valores_por_modelo = graphene.List(TotalValoresPorModeloType)
    def resolve_activos(self, info):
        return Activos.objects.all()
    
    def resolve_categorias_con_activos(self, info):
        categorias = Activos.objects.values('categoria').annotate(count=Count('categoria'))
        result = []
        for categoria in categorias:
            result.append({
                'name': categoria['categoria'],
                'y': categoria['count'],
                'drilldown': categoria['categoria']  # Opcional: Convertir el nombre a minúsculas
            })
        return result
    
    def resolve_categoria_activos(self, info):
        # Realiza la consulta a la base de datos para agrupar los activos por categoría y nombre de activo
        categorias = Activos.objects.values('categoria').annotate(
            activos_data=Count('nombre')
        )

        # Preparar la estructura de datos para cada categoría
        resultado = []
        for categoria in categorias:
            activos_en_categoria = Activos.objects.filter(categoria=categoria['categoria']).values('nombre').annotate(
                cantidad=Count('id')
            )
            activos_data = [[activo['nombre'],  int(activo['cantidad'])] for activo in activos_en_categoria]
            resultado.append(CategoriaActivos(
                id=categoria['categoria'],
                name="cantidad",
                type="column",
                data=activos_data
            ))

        return resultado
    

    def resolve_personas_cantidad_activos(self, info):
        activos_por_persona = Activos.objects.values('persona').annotate(cantidad=Count('id'))
        return [
            PersonaCantidadActivos(name=activo['persona'], y=activo['cantidad'], drilldown=activo['persona'])
            for activo in activos_por_persona
        ]
    
    def resolve_modelos_cantidad_personas(self, info):
        activos_por_modelo = Activos.objects.values('modelo').annotate(cantidad=Count('persona', distinct=True))
        return [
            ModeloCantPersonas(name=activo['modelo'], y=activo['cantidad'], drilldown=activo['modelo'])
            for activo in activos_por_modelo
        ]
        
    def resolve_estadisticas(self, info):
        total_personas = Activos.objects.values('persona').distinct().count()
        total_activos = Activos.objects.count()
        total_modelos = Activos.objects.values('modelo').distinct().count()
        return Estadisticas(
            total_personas=total_personas,
            total_activos=total_activos,
            total_modelos=total_modelos
        )
        
    def resolve_total_valores_por_modelo(self, info):
        from django.db.models import F
        resultados = Activos.objects.values('modelo').annotate(
            valorCompraTotal=Sum(F('valorCompra')),
            valorActualTotal=Sum(F('valorActual'))
        )
        return [
            TotalValoresPorModeloType(
                modelo=result['modelo'],
                valorCompraTotal=result['valorCompraTotal'],
                valorActualTotal=result['valorActualTotal']
            ) for result in resultados
        ]

class Mutation(graphene.ObjectType):
    """ update_activo = UpdateActivosMutation.Field() """
    create_activo = CreateActivosMutation.Field()
    


schema = graphene.Schema(query=Query, mutation=Mutation)