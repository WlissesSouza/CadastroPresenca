from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),
    path("membros", lista_membros, name="lista_membros"),
    path("membros/novo", gerenciar_membro, name="cadastro"),
    path("membros/<int:id>", gerenciar_membro, name="editar_membro"),
    # Toggle de telefone: exibe/bloqueia a visualização do telefone
    path('membros/<int:id>/exibir', exibir_membro, name='exibir'),

    # Marcar presença: /membros/ID/presenca/
    # path('membros/<int:id>/presenca/', marcar_presenca, name='marcar_presenca'),
]
