from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout ,authenticate
from django.db import IntegrityError
from .forms import ElementoForm, EquipoForm, EmpleadoForm, AsignacionForm
from .models import Elemento, Equipo , Empleado, Asignacion
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')
# REGISTRARSE
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {
            'form': UserCreationForm
        })
    else:
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if not username or not password1 or not password2:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                "error": 'Todos los campos son obligatorios'
            })
            
        if password1 == password2:
            # Registrar Usuario
            try:
                user = User.objects.create_user(username=username, password=password1)
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    "error": 'El nombre de usuario ya está en uso'
                })
        else:
            return render(request, 'signup.html', {
                'form': UserCreationForm,
                "error": 'Las contraseñas no coinciden'
            })

#ELEMENTOS 
@login_required      
def elementos(request):
    elementos = Elemento.objects.all()
    
    return render(request, 'elementos.html',{'elementos':elementos})

@login_required
def crear_elemento(request):
    if request.method == 'GET':
        return render(request, 'create_elemento.html', {
            'form': ElementoForm()
        })
    else:
        try:
            form = ElementoForm(request.POST)
            new_elemento = form.save(commit=False)
            new_elemento.user = request.user
            new_elemento.save()
            return redirect('elementos')
        except:
            return render(request, 'create_elemento.html', {
                'form': form,  # Aquí pasamos el formulario con los datos ya ingresados
                'error': 'Por favor ingrese datos válidos'
            })

@login_required
def elemento_detail(request,elemento_id):
    if request.method == 'GET':
        elemento = get_object_or_404(Elemento, pk=elemento_id)
        form = ElementoForm(instance=elemento)
        return render(request,'elemento_detail.html',{
            'elemento':elemento,
            'form': form
        })
    else:
       try:
            elemento = get_object_or_404(Elemento,pk=elemento_id)
            form = ElementoForm(request.POST, instance=elemento)
            form.save()
            return redirect('elementos')
       except ValueError:
           return render(request,'elemento_detail.html',{
                    'elemento':elemento,
                    'form': form,
                    'error': 'Error al Actualizar Registro'
                })
@login_required          
def delete_elemento(request, elemento_id):
    elemento = get_object_or_404(Elemento, pk=elemento_id)
    
    if request.method == 'POST':  
        elemento.delete()
        return redirect('elementos')  
    return render(request, 'delete_elemento.html', {'elemento': elemento})

#CERRAR SESIÓN
@login_required
def logout_confirm(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home') 
    return render(request, 'logout_confirm.html')
    
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form':AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
            'form':AuthenticationForm,
            'error': 'Usuario o Contraseña es Incorrecta'
            })   
        else:
            login(request,user)
            return redirect('home')

#EQUIPOS
@login_required      
def equipos(request):
    equipos = Equipo.objects.all()
    
    return render(request, 'equipos.html',{'equipos':equipos})


@login_required
def equipo_detail(request,serial):
    if request.method == 'GET':
        equipo = get_object_or_404(Equipo, pk=serial)
        form = EquipoForm(instance=equipo)
        return render(request,'equipo_detail.html',{
            'equipo': equipo,
            'form': form
        })
    else:
       try:
            equipo = get_object_or_404(Equipo,pk=serial)
            form = EquipoForm(request.POST, instance=equipo)
            form.save()
            return redirect('equipos')
       except ValueError:
           return render(request,'equipo_detail.html',{
                    'equipo': equipo,
                    'form': form,
                    'error': 'Error al Actualizar Registro'
                })
@login_required
def crear_equipo(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        serial = request.POST.get('serial')
        marca = request.POST.get('marca')
        ubicacion = request.POST.get('ubicacion')
        estado = request.POST.get('estado')
        tipo = request.POST.get('tipo')
        
        # Verificar si el campo 'serial' está vacío
        if not serial:
            return render(request, 'create_equipo.html', {'error': 'Es obligatorio el serial del equipo.',
                                                          'serial': serial, 'marca': marca, 'ubicacion': ubicacion,
                                                          'estado': estado, 'tipo': tipo})
        
        # Verifica si el equipo con el serial ya existe
        if Equipo.objects.filter(serial=serial).exists():
            return render(request, 'create_equipo.html', {'error': 'Ya existe un equipo con ese serial.',
                                                          'serial': serial, 'marca': marca, 'ubicacion': ubicacion,
                                                          'estado': estado, 'tipo': tipo})
        
        # Verificar si el campo 'marca' está vacío
        if not marca:
            return render(request, 'create_equipo.html', {'error': 'Es obligatorio la marca del equipo.',
                                                          'serial': serial, 'marca': marca, 'ubicacion': ubicacion,
                                                          'estado': estado, 'tipo': tipo})
        
        # Crea una nueva instancia y la guarda
        equipo = Equipo(
            serial=serial,
            marca=marca,
            ubicacion=ubicacion,
            estado=estado,
            tipo=tipo,  
        )
        equipo.save()

        # Redirige a la página de equipos
        return redirect('equipos') 

    return render(request, 'create_equipo.html') 

@login_required          
def delete_equipo(request, serial):
    equipo = get_object_or_404(Equipo, pk=serial)
    
    if request.method == 'POST':  
        equipo.delete()
        return redirect('equipos')  
    return render(request, 'delete_equipo.html', {'equipo': equipo})

#EMPLEADOS
@login_required      
def empleados(request):
    empleados = Empleado.objects.all()
    
    return render(request, 'empleados.html',{'empleados': empleados})


@login_required
def empleado_detail(request,codigo):
    if request.method == 'GET':
        empleado = get_object_or_404(Empleado, pk=codigo)
        form = EmpleadoForm(instance=empleado)
        return render(request,'empleado_detail.html',{
            'empleado': empleado,
            'form': form
        })
    else:
       try:
            empleado = get_object_or_404(Empleado,pk=codigo)
            form = EmpleadoForm(request.POST, instance=empleado)
            form.save()
            return redirect('empleados')
       except ValueError:
           return render(request,'empleado_detail.html',{
                    'empleado': empleado,
                    'form': form,
                    'error': 'Error al Actualizar Registro'
                })
@login_required
def crear_empleado(request):
    if request.method == 'POST':
        # Obtener los datos del formulario
        codigo = request.POST.get('codigo')
        nombre = request.POST.get('nombre')
        cargo = request.POST.get('cargo')

        # Verificar si el campo 'codigo' está vacío
        if not codigo:
            return render(request, 'create_empleado.html', {'error': 'Es obligatorio el código del empleado.',
                                                            'codigo': codigo, 'nombre': nombre, 'cargo': cargo})
        
        # Verificar si el campo 'nombre' está vacío
        if not nombre:
            return render(request, 'create_empleado.html', {'error': 'Es obligatorio el nombre del empleado.',
                                                            'codigo': codigo, 'nombre': nombre, 'cargo': cargo})
        
        # Verificar si el campo 'cargo' está vacío
        if not cargo:
            return render(request, 'create_empleado.html', {'error': 'Es obligatorio el área del empleado.',
                                                            'codigo': codigo, 'nombre': nombre, 'cargo': cargo})
        
        # Verificar si ya existe un empleado con el mismo código
        if Empleado.objects.filter(codigo=codigo).exists():
            return render(request, 'create_empleado.html', {'error': 'Ya existe un empleado con ese código.',
                                                            'codigo': codigo, 'nombre': nombre, 'cargo': cargo})
        
        # Crear la nueva instancia y guardarla
        empleado = Empleado(
            codigo=codigo,
            nombre=nombre,
            cargo=cargo 
        )
        empleado.save()

        # Redirigir a la página de empleados
        return redirect('empleados') 

    return render(request, 'create_empleado.html')


@login_required          
def delete_empleado(request, codigo):
    empleado = get_object_or_404(Empleado, pk=codigo)
    
    if request.method == 'POST':  
        empleado.delete()
        return redirect('empleados')  
    return render(request, 'delete_empleado.html', {'empleado': empleado})

#ASIGNACIONES
@login_required
def asignaciones(request):
    asignaciones = Asignacion.objects.all()
    return render(request, 'asignaciones.html', {'asignaciones': asignaciones})

@login_required
def asignacion_detail(request, pk):
    # Obtén la asignación específica
    asignacion = get_object_or_404(Asignacion, pk=pk)

    if request.method == 'POST':
        # Si la solicitud es POST, procesamos el formulario
        form = AsignacionForm(request.POST, instance=asignacion)
        
        if form.is_valid():
            # Guardamos la asignación con los nuevos elementos seleccionados
            form.save()  # Django maneja la relación ManyToMany por ti
            return redirect('asignaciones')  # Redirige a la lista de asignaciones
        else:
            # Si el formulario no es válido, mostramos el error
            return render(request, 'asignacion_detail.html', {
                'form': form,
                'asignacion': asignacion,
                'empleados': Empleado.objects.all(),
                'elementos': Elemento.objects.all(),
                'error': 'Hubo un error al intentar actualizar la asignación'
            })
    else:
        # Si la solicitud es GET, pre-poblamos el formulario con la asignación actual
        form = AsignacionForm(instance=asignacion)
        empleados = Empleado.objects.all()
        elementos = Elemento.objects.all()

        return render(request, 'asignacion_detail.html', {
            'form': form,
            'asignacion': asignacion,
            'empleados': empleados,
            'elementos': elementos,
        })

@login_required
def crear_asignacion(request):
    if request.method == 'POST':
        # Obtén los valores enviados por el formulario
        empleado_id = request.POST.get('empleado')
        elementos_ids = request.POST.getlist('elementos')  # Lista de ids de los elementos seleccionados
        computador = request.POST.get('computador')

        # Validación: Verificar que los campos requeridos no estén vacíos
        if not empleado_id or not elementos_ids or not computador:
            return render(request, 'create_asignacion.html', {
                'error': 'Todos los campos son obligatorios.',
                'empleados': Empleado.objects.all(),
                'elementos': Elemento.objects.all().distinct(),
                'empleado_id': empleado_id,
                'elementos_ids': elementos_ids,
                'computador': computador
            })

        # Obtén el empleado y los elementos correspondientes
        try:
            empleado = Empleado.objects.get(codigo=empleado_id)
        except Empleado.DoesNotExist:
            return render(request, 'create_asignacion.html', {
                'error': 'Empleado no encontrado.',
                'empleados': Empleado.objects.all(),
                'elementos': Elemento.objects.all().distinct(),
                'empleado_id': empleado_id,
                'elementos_ids': elementos_ids,
                'computador': computador
            })
        
        elementos = Elemento.objects.filter(id__in=elementos_ids)

        # Crea la asignación
        asignacion = Asignacion.objects.create(
            empleado=empleado,
            computador=computador
        )
        asignacion.elementos.set(elementos)  # Establece la relación ManyToMany

        return redirect('asignaciones')
    
    # Si la solicitud es GET, pasamos los empleados y elementos al contexto
    empleados = Empleado.objects.all()

    # Filtramos los elementos para que solo se muestren una vez por nombre (puedes hacerlo también por otro campo)
    elementos = Elemento.objects.all()
    # Agrupamos por el nombre del elemento (sin importar la marca o id)
    elementos_unicos = {e.nombre: e for e in elementos}.values()

    return render(request, 'create_asignacion.html', {
        'empleados': empleados,
        'elementos': elementos_unicos  
    })

@login_required
def delete_asignacion(request, pk):
    asignacion = get_object_or_404(Asignacion, pk=pk)
    
    if request.method == 'POST':
        asignacion.delete()
        return redirect('asignaciones')
    
    return render(request, 'delete_asignacion.html', {'asignacion': asignacion})


def custom_404(request, exception):
    return render(request, '404.html', {}, status=404)