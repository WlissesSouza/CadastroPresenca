from django.urls import path, include
from .views import *

urlpatterns = [
    # Fazer login/logout
    path('accounts/', include('django.contrib.auth.urls')),

    path('login/', login_view, name='login'),

]
