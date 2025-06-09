from django.urls import path
from .views import *

urlpatterns = [
    path("", home, name="home"),

    path("membros", lista_membros, name="lista_membros"),

    path("membros/novo", gerenciar_membro, name="cadastro"),

    path("membros/<int:id>", gerenciar_membro, name="editar_membro"),

    path('membros/deletar/<int:id>/', deletar_membro, name='deletar_membro'),
]
