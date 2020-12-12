"""uspavalia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('',views.home,name="home"),
    path('disciplina/<int:id>/', views.pagina_disciplina, name = "disciplina"),
    path('add_comentario/<int:id>', views.add_comentario, name = "add_comentario"),
    path('editarcomentario/<int:disciplina_id>/<int:comentario_id>', views.edit_comment, name = "edit_comment"),
    path('deletarcomentario/<int:disciplina_id>/<int:comentario_id>', views.delete_comment, name = "delete_comment"),
]
