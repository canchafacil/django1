from django.shortcuts import render, redirect
from .models import Usuario

def registro(request):

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        rol='CLIENTE'

        if password != confirm_password:
            return render(
                request,
                'usuarios/registro.html',
                {'error': 'Las contraseñas no coinciden'}
            )

        if Usuario.objects.filter(email=email).exists():
            return render(
            request,
            'usuarios/registro.html',
            {'error': 'Este correo ya está registrado'}
    )

        Usuario.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password,
            rol=rol
        )

        return redirect('login')

    return render(request, 'usuarios/registro.html')

def registro_admin(request):

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        rol='ADMIN'

        if password != confirm_password:
            return render(
                request,
                'usuarios/registro_admin.html',
                {'error': 'Las contraseñas no coinciden'}
            )

        if Usuario.objects.filter(email=email).exists():
            return render(
            request,
            'usuarios/registro_admin.html',
            {'error': 'Este correo ya está registrado'}
    )

        Usuario.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            password=password,
            rol=rol
        )

        return redirect('login')

    return render(request, 'usuarios/registro_admin.html')

def login_view(request):
    """Renderiza la pantalla de inicio de sesión."""
    return render(request, 'usuarios/login.html')

def login_admin(request):

    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            usuario = Usuario.objects.get(
                email=email,
                password=password
            )

            if usuario.rol == 'ADMIN':
                return redirect('panel_principal')

            return redirect('inicio')

        except Usuario.DoesNotExist:
            return render(
                request,
                'usuarios/login_admin.html',
                {'error': 'Correo o contraseña incorrectos'}
            )

    return render(request, 'usuarios/login_admin.html')

def lista_usuarios(request):

    usuarios = Usuario.objects.all()

    return render(
        request,
        'usuarios/lista_usuarios.html',
        {'usuarios': usuarios}
    )

def eliminar_usuario(request, id):

    usuario = Usuario.objects.get(id=id)
    usuario.delete()

    return redirect('lista_usuarios')

def editar_usuario(request, id):

    usuario = Usuario.objects.get(id=id)

    if request.method == 'POST':

        usuario.first_name = request.POST.get('first_name')
        usuario.email = request.POST.get('email')
        usuario.phone = request.POST.get('phone')
        usuario.password = request.POST.get('password')

        usuario.save()

        return redirect('lista_usuarios')

    return render(
        request,
        'usuarios/editar_usuarios.html',
        {'usuario': usuario}
    )
