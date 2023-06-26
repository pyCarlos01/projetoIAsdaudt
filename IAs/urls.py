from django.urls import path, include
from .views import *
from django.contrib.auth import views as auth_view

app_name = 'IAs'

urlpatterns = [
    path('', Homepage.as_view(), name = 'homepage'),
    path('criarconta/', Criarconta.as_view(), name = 'criarconta'),
    path('homefrotas/', Homefrotas.as_view(), name = 'homefrotas'),
    # path('homefrotas/escala/remessa/', Remessas.as_view(), name='remessa'),
    path('homefrotas/disponibilidade/<int:pk>', Detalhesfrotas.as_view(), name = 'detalhesfrotas'),
    path('login/', auth_view.LoginView.as_view(template_name = 'login.html'), name = 'login'),
    path('logout', auth_view.LogoutView.as_view(template_name = 'logout.html'), name = 'logout'),
    path('homefrotas/disponibilidade/', disponibilidade, name='disponibilidade'),
    path('homefrotas/escala/', escala, name = 'escala'),
    path('homefrotas/escala/download/', download_escala, name='downloadescala'),
    path('homefrotas/relatorios/download/', Relatorios.as_view(), name='relatorios'),
    path('homefrotas/colaboradores/', controle_func, name='colaboradores'),
    # path('homefrotas/escala/remessa/', import_csv, name='remessa'),
    path('import/', import_view, name='remessa'),
]
