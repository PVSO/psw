from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.messages import constants


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        users = User.objects.filter(username=username)

        if users.exists():
            messages.add_message(
                request,
                constants.ERROR,
                'Já existe um usuário com esse nome',
            )
            return redirect('usuarios:cadastro')

        if senha != confirmar_senha:
            messages.add_message(
                request, constants.ERROR, 'As senhas não coincídem'
            )
            return redirect('usuarios:cadastro')

        if len(senha) < 8:
            messages.add_message(
                request, constants.ERROR,
                'A senha deve possuir pelo menos 8 caracteres'
            )
            return redirect('usuarios:cadastro')

        try:
            User.objects.create_user(
                username=username,
                email=email,
                password=senha
            )

            return redirect('usuarios:login')

        except:
            print('Erro 4')
            return redirect('usuarios:cadastro')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get("senha")

        user = auth.authenticate(request, username=username, password=senha)

        if user:
            auth.login(request, user)
            return redirect('/pacientes/home')

        messages.add_message(request, constants.ERROR, 'Usuário ou senha incorretos')
        return redirect('/usuarios/login')


def logout(request):
    auth.logout(request)
    return redirect('usuarios:login')
