import graphene
from graphene_django import DjangoObjectType
from activos.models import Departamento, Depreciacion, Ubicacion, Fabricante, Categoria, Modelo, Persona, Activos 

class DepartamentoType(DjangoObjectType):
    class Meta:
        model = Departamento
        fields = ("id", "nombre", "descripcion") 

class DepreciacionType(DjangoObjectType):
    class Meta:
        model = Depreciacion
        fields = ("id", "nombre", "meses", "valorMinimo") 

class UbicacionType(DjangoObjectType):
    class Meta:
        model = Ubicacion
        fields = ("id", "nombre", "direccion")

class FabricanteType(DjangoObjectType):
    class Meta:
        model = Fabricante
        fields = ("id", "nombre", "descripcion") 

class CategoriaType(DjangoObjectType):
    class Meta:
        model = Categoria
        fields = ("id", "nombre", "descripcion")  

class ModeloType(DjangoObjectType):
    class Meta:
        model = Modelo
        fields = ("id", "nombre", "fabricante", "Categoria")

class PersonaType(DjangoObjectType):
    class Meta:
        model = Persona
        fields = ("id", "nombre", "email", "telefono", "ci","departamento")

class ActivoType(DjangoObjectType):
    class Meta:
        model = Activos
        fields = ("nombre", "serial", "estado", "fechaCompra", "valorCompra", "valorActual", "persona", "modelo", "depreciacion", "ubicacion") 

class CreateDepartamentoMutation(graphene.Mutation):
    # Inputs que espera recibir
    class Arguments:
        nombre = graphene.String()
        descripcion = graphene.String()

    departamento = graphene.Field(DepartamentoType)

    # Datos que espera devolver
    def mutate(self, info, nombre, descripcion):
        departamento = Departamento(nombre = nombre, descripcion = descripcion)
        departamento.save()
        return CreateDepartamentoMutation(departamento = departamento)
    
class CreateDepreciacionMutation(graphene.Mutation):
    # Inputs que espera recibir
    class Arguments:
        nombre = graphene.String()
        meses = graphene.Int()
        valorMinimo = graphene.Float()

    depreciacion = graphene.Field(DepreciacionType)

    # Datos que espera devolver
    def mutate(self, info, nombre, meses, valorMinimo):
        depreciacion = Depreciacion(nombre = nombre, meses = meses, valorMinimo = valorMinimo)
        depreciacion.save()
        return CreateDepreciacionMutation(depreciacion = depreciacion)
    
class CreateUbicacionMutation(graphene.Mutation):
    # Inputs que espera recibir
    class Arguments:
        nombre = graphene.String()
        direccion = graphene.String()

    Ubicacion = graphene.Field(UbicacionType)

    # Datos que espera devolver
    def mutate(self, info, nombre, direccion):
        ubicacion = Ubicacion(nombre = nombre, direccion = direccion)
        ubicacion.save()
        return CreateUbicacionMutation(ubicacion = ubicacion)
    
class CreateFabricanteMutation(graphene.Mutation):
    # Inputs que espera recibir
    class Arguments:
        nombre = graphene.String()
        descripcion = graphene.String()

    fabricante = graphene.Field(FabricanteType)

    # Datos que espera devolver
    def mutate(self, info, nombre, descripcion):
        fabricante = Fabricante(nombre = nombre, descripcion = descripcion)
        fabricante.save()
        return CreateFabricanteMutation(fabricante = fabricante)
    
class CreateCategoriaMutation(graphene.Mutation):
    # Inputs que espera recibir
    class Arguments:
        nombre = graphene.String()
        descripcion = graphene.String()

    categoria = graphene.Field(CategoriaType)

    # Datos que espera devolver
    def mutate(self, info, nombre, descripcion):
        categoria = Categoria(nombre = nombre, descripcion = descripcion)
        categoria.save()
        return CreateCategoriaMutation(categoria = categoria)
    
class FabricanteInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    nombre = graphene.String()
    descripcion = graphene.String()

class CategoriaInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    nombre = graphene.String()
    descripcion = graphene.String()

class CreateModeloMutation(graphene.Mutation):
    # Inputs que espera recibir
    class Arguments:
        nombre = graphene.String(required=True)
        fabricante = graphene.Argument(FabricanteInput, required=True)
        categoria = graphene.Argument(CategoriaInput, required=True)

    modelo = graphene.Field(ModeloType)

    def mutate(self, info, nombre, fabricante, categoria):
        fabricante_instance = Fabricante.objects.create(**fabricante)
        categoria_instance = Categoria.objects.create(**categoria)

        modelo = Modelo.objects.create(nombre=nombre, fabricante=fabricante_instance, categoria=categoria_instance)

        return CreateModeloMutation(modelo=modelo)

class DepartamentoInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    nombre = graphene.String()
    descripcion = graphene.String()

class CreatePersonaMutation(graphene.Mutation):
    # Inputs que espera recibir
    class Arguments:
        ci = graphene.String(required=True)
        departamento = graphene.Argument(DepartamentoInput, required=True)
        email = graphene.String(required=True)
        nombre = graphene.String(required=True)
        telefono = graphene.String(required=True)

    persona = graphene.Field(PersonaType)

    def mutate(self, info, ci, departamento, email, nombre, telefono):
        departamento_instance, _ = Departamento.objects.update_or_create(id=departamento.id, defaults=departamento.__dict__)

        persona = Persona.objects.create(ci=ci, departamento=departamento_instance, email=email, nombre=nombre, telefono=telefono)

        return CreatePersonaMutation(persona=persona)

class PersonaInput(graphene.InputObjectType):
    ci = graphene.String()
    departamento = graphene.String()
    email = graphene.String()
    id = graphene.ID(required=True)
    nombre = graphene.String()
    telefono = graphene.String()

class DepreciacionInput(graphene.InputObjectType):
    id = graphene.ID(required=True)
    meses = graphene.String()
    nombre = graphene.String()
    valor_minimo = graphene.Float()

class CategoriaInput(graphene.InputObjectType):
    descripcion = graphene.String()
    id = graphene.ID(required=True)
    nombre = graphene.String()

class FabricanteInput(graphene.InputObjectType):
    descripcion = graphene.String()
    id = graphene.ID(required=True)
    nombre = graphene.String()

class ModeloInput(graphene.InputObjectType):
    categoria = graphene.Argument(CategoriaInput, required=True)
    fabricante = graphene.Argument(FabricanteInput, required=True)
    id = graphene.ID(required=True)
    nombre = graphene.String()

class UbicacionInput(graphene.InputObjectType):
    direccion = graphene.String()
    id = graphene.ID(required=True)
    nombre = graphene.String()

class ActivoInput(graphene.InputObjectType):
    persona = graphene.Argument(PersonaInput, required=True)
    depreciacion = graphene.Argument(DepreciacionInput, required=True)
    estado = graphene.String(required=True)
    etiqueta = graphene.String(required=True)
    fecha_compra = graphene.String(required=True)
    id = graphene.ID()
    image = graphene.String(required=True)
    modelo = graphene.Argument(ModeloInput, required=True)
    nombre = graphene.String(required=True)
    serial = graphene.String(required=True)
    ubicacion = graphene.Argument(UbicacionInput, required=True)
    ultima_asignacion = graphene.String(required=True)
    ultima_desasignacion = graphene.String(required=True)
    valor_actual = graphene.Float(required=True)
    valor_compra = graphene.Float(required=True)

class CreateActivosMutation(graphene.Mutation):
    # Inputs que espera recibir
    class Arguments:
        activo = graphene.Argument(ActivoInput, required=True)

    persona = graphene.Field(PersonaType)
    depreciacion = graphene.Field(DepreciacionType)
    estado = graphene.String()
    etiqueta = graphene.String()
    fecha_compra = graphene.String()
    id = graphene.ID()
    image = graphene.String()
    modelo = graphene.Field(ModeloType)
    nombre = graphene.String()
    serial = graphene.String()
    ubicacion = graphene.Field(UbicacionType)
    ultima_asignacion = graphene.String()
    ultima_desasignacion = graphene.String()
    valor_actual = graphene.Float()
    valor_compra = graphene.Float()

    def mutate(self, info, activo):
        persona_data = activo.pop('persona', None)
        depreciacion_data = activo.pop('depreciacion', None)
        modelo_data = activo.pop('modelo', None)
        ubicacion_data = activo.pop('ubicacion', None)

        persona_instance = Persona.objects.create(**persona_data)
        depreciacion_instance = Depreciacion.objects.create(**depreciacion_data)
        modelo_instance = Modelo.objects.create(**modelo_data)
        ubicacion_instance = Ubicacion.objects.create(**ubicacion_data)

        activo_instance = Activos.objects.create(
            persona=persona_instance,
            depreciacion=depreciacion_instance,
            modelo=modelo_instance,
            ubicacion=ubicacion_instance,
            **activo
        )

        return CreateActivosMutation(
            persona=persona_instance,
            depreciacion=depreciacion_instance,
            estado=activo_instance.estado,
            etiqueta=activo_instance.etiqueta,
            fecha_compra=activo_instance.fecha_compra,
            id=activo_instance.id,
            image=activo_instance.image,
            modelo=modelo_instance,
            nombre=activo_instance.nombre,
            serial=activo_instance.serial,
            ubicacion=ubicacion_instance,
            ultima_asignacion=activo_instance.ultima_asignacion,
            ultima_desasignacion=activo_instance.ultima_desasignacion,
            valor_actual=activo_instance.valor_actual,
            valor_compra=activo_instance.valor_compra,
        )
    
class UpdateDepartamentoMutation(graphene.Mutation):
    # Inputs que espera recibir
    class Arguments:
        id = graphene.ID(required = True)
        nombre = graphene.String()
        descripcion = graphene.String()

    departamento = graphene.Field(DepartamentoType)

    # Datos que espera devolver
    def mutate(self, info, id, nombre, descripcion):
        departamento = Departamento.objects.get(pk = id)
        departamento.nombre = nombre
        departamento.descripcion = descripcion
        departamento.save()
        return UpdateDepartamentoMutation(departamento = departamento)

class UpdateDepreciacionMutation(graphene.Mutation):
    # Inputs que espera recibir
    class Arguments:
        id = graphene.ID(required = True)
        nombre = graphene.String()
        meses = graphene.Int()
        valorMinimo = graphene.Float()

    depreciacion = graphene.Field(DepreciacionType)

    # Datos que espera devolver
    def mutate(self, info, id, nombre, meses, valorMinimo):
        depreciacion = Depreciacion.objects.get(pk = id)
        depreciacion.nombre = nombre
        depreciacion.meses = meses
        depreciacion.valorMinimo = valorMinimo
        depreciacion.save()
        return UpdateDepreciacionMutation(depreciacion = depreciacion)
    
class UpdateUbicacionMutation(graphene.Mutation):
    # Inputs que espera recibir
    class Arguments:
        id = graphene.ID(required = True)
        nombre = graphene.String()
        direccion = graphene.String()

    Ubicacion = graphene.Field(UbicacionType)

    # Datos que espera devolver
    def mutate(self, info, id, nombre, direccion):
        ubicacion = Ubicacion.objects.get(pk = id)
        ubicacion.nombre = nombre
        ubicacion.direccion = direccion
        ubicacion.save()
        return UpdateUbicacionMutation(ubicacion = ubicacion)

class UpdateFabricanteMutation(graphene.Mutation):
    # Inputs que espera recibir
    class Arguments:
        id = graphene.ID(required = True)
        nombre = graphene.String()
        descripcion = graphene.String()

    fabricante = graphene.Field(FabricanteType)

    # Datos que espera devolver
    def mutate(self, info, id, nombre, descripcion):
        fabricante = Fabricante.objects.get(pk = id)
        fabricante.nombre = nombre
        fabricante.descripcion = descripcion
        fabricante.save()
        return UpdateFabricanteMutation(fabricante = fabricante)
    
class UpdateCategoriaMutation(graphene.Mutation):
    # Inputs que espera recibir
    class Arguments:
        id = graphene.ID(required = True)
        nombre = graphene.String()
        descripcion = graphene.String()

    categoria = graphene.Field(CategoriaType)

    # Datos que espera devolver
    def mutate(self, info, id, nombre, descripcion):
        categoria = Categoria.objects.get(pk = id)
        categoria.nombre = nombre
        categoria.descripcion = descripcion
        categoria.save()
        return UpdateCategoriaMutation(categoria = categoria)
    
class UpdateModeloMutation(graphene.Mutation):
    # Inputs que espera recibir
    class Arguments:
        id = graphene.ID(required = True)
        nombre = graphene.String()
        fabricante = graphene.Int()
        Categoria = graphene.Int()

    modelo = graphene.Field(ModeloType)

    # Datos que espera devolver
    def mutate(self, info, nombre, fabricante, categoria):
        modelo = Modelo.objects.get(pk = id)
        modelo.nombre = nombre
        modelo.fabricante = fabricante
        modelo.Categoria = categoria
        modelo.save()
        return UpdateModeloMutation(modelo = modelo)
    
class UpdatePersonaMutation(graphene.Mutation):
    # Inputs que espera recibir
    class Arguments:
        id = graphene.ID(required = True)
        nombre = graphene.String()
        email = graphene.String()
        telefono = graphene.String()
        departamento = graphene.Int()
        ci = graphene.String()

    persona = graphene.Field(PersonaType)

    # Datos que espera devolver
    def mutate(self, info, id, nombre, email, telefono, departamento, ci):
        persona = Persona.objects.get(pk = id)
        persona.nombre = nombre
        persona.email = email
        persona.telefono = telefono
        persona.departamento = departamento
        persona.ci = ci
        persona.save()
        return UpdatePersonaMutation(persona = persona)
    
class UpdateActivosMutation(graphene.Mutation):
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
        return UpdateActivosMutation(activo = activo)

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello!!!")
    departamentos = graphene.List(DepartamentoType)
    depreciaciones = graphene.List(DepreciacionType)
    ubicaciones = graphene.List(UbicacionType)
    fabricantes = graphene.List(FabricanteType)
    categorias = graphene.List(CategoriaType)
    modelos = graphene.List(ModeloType)
    personas = graphene.List(PersonaType)
    activos = graphene.List(ActivoType)

    def resolve_departamentos(self, info):
        return Departamento.objects.all()
    
    def resolve_depreciaciones(self, info):
        return Depreciacion.objects.all()
    
    def resolve_ubicaciones(self, info):
        return Ubicacion.objects.all()
    
    def resolve_fabricantes(self, info):
        return Fabricante.objects.all()
    
    def resolve_categorias(self, info):
        return Categoria.objects.all()
    
    def resolve_modelos(self, info):
        return Modelo.objects.all()
    
    def resolve_personas(self, info):
        return Persona.objects.all()
    
    def resolve_activos(self, info):
        return Activos.objects.all()

class Mutation(graphene.ObjectType):
    create_departamento = CreateDepartamentoMutation.Field()
    create_depreciacion = CreateDepreciacionMutation.Field()
    create_ubicacion = CreateUbicacionMutation.Field()
    create_fabricante = CreateFabricanteMutation.Field()
    create_categoria = CreateCategoriaMutation.Field()
    create_modelo = CreateModeloMutation.Field()
    create_persona = CreatePersonaMutation.Field()
    create_activo = CreateActivosMutation.Field()
    update_departamento = UpdateDepartamentoMutation.Field()
    update_depreciacion = UpdateDepreciacionMutation.Field()
    update_ubicacion = UpdateUbicacionMutation.Field()
    update_fabricante = UpdateFabricanteMutation.Field()
    update_categoria = UpdateCategoriaMutation.Field()
    update_modelo = UpdateModeloMutation.Field()
    update_persona = UpdatePersonaMutation.Field()
    update_activo = UpdateActivosMutation.Field()
    


schema = graphene.Schema(query=Query, mutation=Mutation)