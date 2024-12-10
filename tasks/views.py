from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout ,authenticate
from django.db import IntegrityError
from .forms import ElementoForm
from .models import Elemento
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

def signup(request):

    if request.method == 'GET':
        return render(request, 'signup.html',{
            'form': UserCreationForm
         })
    else:
        if request.POST['password1'] == request.POST['password2']:
            #Registrar Usuario
            try:
                user = User.objects.create_user(username=request.POST['username'],
                password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    "error": 'Usuario existente'
                })
        return render(request, 'signup.html',{
                    'form': UserCreationForm,
                    "error": 'Las Contraseñas no coinciden'
                })

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
    
    if request.method == 'POST':  # Si la solicitud es POST, eliminamos el elemento
        elemento.delete()
        return redirect('elementos')  # Redirigimos a la lista de elementos

    # Si la solicitud es GET, mostramos una página de confirmación
    return render(request, 'delete_elemento.html', {'elemento': elemento})

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('home')

    
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

