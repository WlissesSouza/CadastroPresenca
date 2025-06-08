from functools import wraps
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime as dt_datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages


def confirmar_senha_required(view_func):
    """
    Decorador que exige confirmação de usuario e senha a cada 15 minutos para acessos a url privados,
    usando o fuso horario para a confirmação definido em settings.py que foi o (America/Sao_Paulo).
    """

    @wraps(view_func)
    @login_required(login_url='login')
    def wrapper(request, *args, **kwargs):

        # 1) Tenta recuperar a última confirmação
        last_ts = request.session.get('last_confirmation')
        try:
            last_ts = float(last_ts)
        except (ValueError, TypeError):
            last_ts = None

        if last_ts is not None:
            # (America/Sao_Paulo)
            tz_padrao = timezone.get_default_timezone()

            # Reconstrói o datetime com fuso selecionado a partir do timestamp
            ultima_confirmacao = dt_datetime.fromtimestamp(last_ts, tz=tz_padrao)

            # “Agora” em SP
            hora_atual = timezone.localtime()  # equivale a timezone.now().astimezone(tz_padrao)

            # Se já tiver confirmado há menos de 15 minutos (em SP), libera a view
            if hora_atual - ultima_confirmacao <= timedelta(minutes=15):
                return view_func(request, *args, **kwargs)

        # 2) Se chegou via POST no formulário de confirmação de senha:
        if request.method == 'POST' and request.POST.get('confirmar_senha'):
            senha = request.POST['confirmar_senha']
            user = authenticate(
                username=request.user.username,
                password=senha
            )
            if user is not None:
                # Se a senha for correta:
                #  -Atualiza o timestamp atual (Com o fuso horario selecionado no settings).
                request.session['last_confirmation'] = timezone.now().timestamp()

                next_url = request.POST.get('next_url', request.get_full_path())
                return redirect(next_url)
            else:
                messages.error(request, 'Senha incorreta!')

        # 3) Se não confirmou ou se a senha estiver errada,
        return render(request, 'controle/confirmar_senha.html', {
            'next_url': request.get_full_path(),
        })

    return wrapper
