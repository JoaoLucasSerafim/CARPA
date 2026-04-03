"""
URL configuration for CARPA project.

Cadastro Ambiental Rural Popular Avançado do Pará
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Página inicial
    path('', views.pagina_inicial, name='inicio'),
    
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Cadastro de agricultor
    path('cadastro/agricultor/', views.cadastro_agricultor, name='cadastro_agricultor'),
    
    # Área do Agricultor (requer login como agricultor)
    path('agricultor/dashboard/', views.dashboard_agricultor, name='dashboard_agricultor'),
    path('agricultor/editar/', views.editar_perfil_agricultor, name='editar_perfil_agricultor'),
    
    # Área do Técnico (requer login como técnico)
    path('tecnico/dashboard/', views.dashboard_tecnico, name='dashboard_tecnico'),
    path('tecnico/agricultor/<int:pk>/', views.detalhe_agricultor, name='detalhe_agricultor'),
    path('tecnico/agricultor/<int:pk>/validar/', views.validar_cadastro, name='validar_cadastro'),
]

# Servir arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
