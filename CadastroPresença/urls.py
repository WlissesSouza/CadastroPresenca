from django.contrib import admin
from django.urls import path, include  # O include é para ao entrar no uri selecionada '' (home) ir para a urls do App
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Presenca.urls')),
    path('user/', include('Conta.urls')),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
