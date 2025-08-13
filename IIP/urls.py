"""
URL configuration for IIP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core.views import HomeView, gerenciar_politico, deletar_politico

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('politico/novo/', gerenciar_politico, name='novo_politico'),
    path('politico/<int:politico_id>/editar/', gerenciar_politico, name='editar_politico'),
    path('politico/<int:politico_id>/deletar/', deletar_politico, name='deletar_politico'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),

]

# Servir arquivos de mídia durante o desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
