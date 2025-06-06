from django.contrib import admin
from django.urls import path, include  # O include é para ao entrar no uri selecionada '' (home) ir para a urls do App

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Presenca.urls')),
    path('user/', include('Conta.urls')),

]
