from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout ,authenticate
from django.db import IntegrityError
from .forms import ElementoForm, EquipoForm
from .models import Elemento, Equipo
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
        return render(request, 'create_elemento.html',{
            'form': ElementoForm
        })
    else:
        try:
            form = ElementoForm(request.POST)
            new_elemento = form.save(commit=False)
            new_elemento.user = request.user
            new_elemento.save()
            return redirect('elementos')
        except:
            return render(request,'create_elemento.html',{
                'form': ElementoForm,
                'error': 'Por favor ingrese datos validos'
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
            'equipo':equipo,
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
                    'equipo':equipo,
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
        
        # Verifica si el equipo con el serial ya existe (para evitar duplicados)
        if Equipo.objects.filter(serial=serial).exists():
            return render(request, 'crear_equipo.html', {'error': 'Ya existe un equipo con ese serial.'})
        
        # Crea una nueva instancia del equipo y la guarda
        equipo = Equipo(
            serial=serial,
            marca=marca,
            ubicacion=ubicacion,
            estado=estado,
            tipo=int(tipo),  # Convertimos el tipo a un número entero
            user=request.user  # Asumimos que el usuario actual es el que crea el equipo
        )
        equipo.save()

        # Redirige a la página de equipos o donde desees
        return redirect('equipos')  # Asegúrate de que la URL 'equipos' esté configurada correctamente

    return render(request, 'crear_equipo.html') 