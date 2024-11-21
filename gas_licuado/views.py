from django.shortcuts import render, redirect, get_object_or_404
from .models import Solicitud
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:  
            return redirect('home')  
        return view_func(request, *args, **kwargs)  
    return wrapper
def home(request):
    return render(request, 'home.html', {
        'username': request.user.username if request.user.is_authenticated else None
    })

def crear_solicitud(request):
    if request.method == 'POST':
        rut = request.POST['rut']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        direccion = request.POST['direccion']
        telefono = request.POST['telefono']
        comuna = request.POST['comuna']
        

        solicitud = Solicitud(
            rut=rut,
            nombre=nombre,
            apellido=apellido,
            direccion=direccion,
            telefono=telefono,
            comuna=comuna
        )
        solicitud.save()
        
        messages.success(request, "Solicitud creada exitosamente.")
        return redirect('home')
    
    return render(request, 'solicitud.html')

@login_required
def listar_solicitudes(request):
    if request.user.is_superuser:  # Verifica si el usuario es un superusuario
        solicitudes = Solicitud.objects.all()
        return render(request, 'listar.html', {'solicitudes': solicitudes})
    else:
        return redirect('home')  # Cambia 'home' al nombre correcto de tu URL de inicio

@admin_required
@login_required
def cambiar_estado(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        solicitud.cambiar_estado(nuevo_estado)  
        return redirect('listar_solicitudes')
    
    return render(request, 'cambiar_estado.html', {'solicitud': solicitud})

@login_required
def buscar_solicitud(request):
    resultados = []  

    if request.method == 'POST':
        rut = request.POST.get('rut')
        resultados = Solicitud.objects.filter(rut=rut)  

    return render(request, 'buscar.html', {'resultados': resultados})

@login_required
def request_detail(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    return render(request, 'detalle_solicitud.html', {'solicitud': solicitud})

@admin_required
def delete_request(request, id):
    solicitud = get_object_or_404(Solicitud, id=id)
    if request.method == 'POST':
        solicitud.delete()
        return redirect('listar_solicitudes')
    return render(request, 'confirm_delete.html', {'solicitud': solicitud})


def iniciar_sesion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'iniciar_sesion.html', {'error': 'Credenciales incorrectas'})
    return render(request, 'iniciar_sesion.html')

@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('home')


@admin_required
@login_required
def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()  # Limpia espacios en blanco
        password = request.POST.get('password')
        rol = request.POST.get('rol')

        # Verificar si el nombre de usuario ya existe
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return render(request, 'crear_usuario.html')

        # Validar que el nombre de usuario no esté vacío después de eliminar espacios
        if not username:
            messages.error(request, "El nombre de usuario no puede estar vacío.")
            return render(request, 'crear_usuario.html')

        try:
            # Determina si es superusuario o no según el rol
            is_superuser = True if rol == 'administrador' else False

            # Crear el usuario
            user = User.objects.create_user(
                username=username,
                password=password,
                is_superuser=is_superuser,
                is_staff=is_superuser  # Necesario para que acceda al panel de admin
            )
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('home')  # Cambiar 'home' por la URL correspondiente
        except Exception as e:
            messages.error(request, f'Ocurrió un error: {str(e)}')
            return render(request, 'crear_usuario.html')

    return render(request, 'crear_usuario.html')

@admin_required
@login_required
def listar_usuarios(request):
    if request.user.is_superuser:
        users = User.objects.all()
        return render(request, 'listar_usuarios.html', {'users': users})
    else:
        return redirect('home')


@login_required
def ver_perfil(request, id):
    selected_user = get_object_or_404(User, id=id)  # Cambia "user" a "selected_user"
    return render(request, 'ver_perfil.html', {'selected_user': selected_user})


@login_required
def cambiar_contrasena(request, id):
    user = get_object_or_404(User, id=id)

    # Verificar si el usuario no es superusuario y está intentando cambiar la contraseña de otro perfil
    if not request.user.is_superuser and request.user != user:
        return redirect('ver_perfil', id=request.user.id)

    if request.method == 'POST':
        new_password = request.POST['new_password']

        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)  # Mantener la sesión activa tras cambiar la contraseña

        messages.success(request, "Contraseña cambiada exitosamente.")

        return redirect('ver_perfil', id=user.id)

    return render(request, 'cambiar_contrasena.html', {'user': user})

@admin_required
@login_required
def confirm_delete_user(request, id):
    user_to_delete = get_object_or_404(User, id=id)  # Cambiamos 'user' por 'user_to_delete'
    
    if request.method == 'POST':
        if request.user == user_to_delete:  # Verifica si el usuario actual está eliminando su propia cuenta
            user_to_delete.delete()
            logout(request)  # Cierra la sesión
            messages.success(request, "Tu cuenta ha sido eliminada exitosamente.")
            return redirect('home')  # Redirige al inicio (ajusta 'home' según tu URL de inicio)
        else:
            user_to_delete.delete()
            messages.success(request, "Usuario eliminado exitosamente.")
            return redirect('listar_usuarios')
    
    return render(request, 'confirm_delete_user.html', {'user_to_delete': user_to_delete})