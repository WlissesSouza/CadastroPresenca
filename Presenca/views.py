from django.shortcuts import render, redirect, get_object_or_404
from .forms import PessoaForm
from .models import Pessoas
from django.core.files.storage import default_storage
from django.contrib import messages
from django.http import JsonResponse

from Conta.decorators import confirmar_senha_required


def home(request):
    return render(request, 'home.html')


@confirmar_senha_required
def gerenciar_membro(request, id=None):
    """
    :param request: Request do objeto
    :param id: Id  para edição do cadastro caso nao tenha é um novo cadastro

    Se id for None, cria um novo registro. Caso contrário, edita o registro existente.
    Requer confirmação de senha a cada 15 minutos para ser acessada.
    """
    pessoa = get_object_or_404(Pessoas, pk=id) if id else None

    if request.method == 'POST':
        # Cria o form, com ou sem instância, dependendo de `id`
        if id is None:
            form = PessoaForm(request.POST, request.FILES)
        else:
            form = PessoaForm(request.POST, request.FILES, instance=pessoa)

        if form.is_valid():
            membro = form.save(commit=False)

            # Detecta se há pedido de remoção de imagem
            remover_imagem = request.POST.get('remover_imagem') == '1'
            nova_imagem = request.FILES.get('imagem')

            # 1) Se enviou nova imagem apaga a antiga (se existir)
            if nova_imagem and pessoa and pessoa.imagem:
                if default_storage.exists(pessoa.imagem.name):
                    default_storage.delete(pessoa.imagem.name)

            # 2) Se pediu para remover imagem e NÃO enviou nova
            if remover_imagem and not nova_imagem and pessoa and pessoa.imagem:
                if default_storage.exists(pessoa.imagem.name):
                    default_storage.delete(pessoa.imagem.name)
                membro.imagem = None
            membro.save()

            # Usei operação tenaria para faciliar na resposta
            messages.success(request, f'Cadastro {"criado" if id is None else "editado"} com sucesso!')

            return redirect('lista_membros')
        else:
            messages.error(request, 'Verifique os dados digitados!')

    else:
        # Form vazio se for criar ou com instance se for editar
        if id is None:
            form = PessoaForm()
        else:
            form = PessoaForm(instance=pessoa)

    return render(request, 'gerenciar_membros.html', {'form': form})


from django.views.decorators.http import require_POST

@confirmar_senha_required
def lista_membros(request):
    membros = Pessoas.objects.all()

    return render(request, 'lista_membros.html', {'membros': membros})


@require_POST
@confirmar_senha_required
def deletar_membro(request, id):
    try:
        membro = Pessoas.objects.get(pk=id)
        membro.delete()
        return JsonResponse({'success': True, 'message': 'Membro deletado com sucesso.'})
    except Pessoas.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Membro não encontrado.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)