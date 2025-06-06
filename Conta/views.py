from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login realizado com sucesso')  # Mensagem de sucesso
            return redirect('home')  # Rota de retorno (pagina principal)
        else:
            messages.error(request, 'Usuário ou senha incorretos.')  # Mensagem de erro
            return render(request, 'registration/login.html')

    return render(request, 'registration/login.html')
