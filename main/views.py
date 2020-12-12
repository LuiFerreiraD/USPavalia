from django.shortcuts import render, redirect
#from django.http import HttpResponse
from .models import *
from .forms import *

# Create your views here.
def home(request):
    todas_disciplinas = Disciplina.objects.all()
    contexto = {
        "disciplinas": todas_disciplinas,
    }
    return render(request, 'main/index.html', contexto)

#pagina da disciplina
def pagina_disciplina(request, id):
    disciplina = Disciplina.objects.get(id=id)
    #comentarios = Comentario.objects.filter(disciplina=id).order_by()

    comentarios =  Comentario.objects.filter(disciplina=id).annotate(
    total_votes=Count('upVote')-Count('downVote')
    ).order_by('total_votes')

    contexto = {
        "disciplina": disciplina,
        "comentarios": comentarios
    }

    return render(request, 'main/disciplina.html', contexto)

def add_comentario(request, id):
    if request.user.is_authenticated:
        disciplina = Disciplina.objects.get(id=id)
        if request.method == "POST":
            form = CommentForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = request.user
                data.texto = request.POST["texto"]
                data.disciplina = disciplina
                data.save()
                return redirect("main:disciplina", id)
        else:
            form = CommentForm()
        return render(request, "main/details.html", {"form": form})
    else:
        return redirect("accounts:login")

def edit_comment(request, disciplina_id, comentario_id):
    if request.user.is_authenticated:
        disciplina = Disciplina.objects.get(id=disciplina_id)
        comentario = Comentario.objects.get(disciplina=disciplina, id=comentario_id)
        
        if request.user == comentario.user:
            if request.method == "POST":
                form = CommentForm(request.POST, instance=comentario)
                if form.is_valid():
                    data = form.save(commit=False)
                    data.save()
                    return redirect("main:disciplina", disciplina_id)
            else:
                form = CommentForm(instance=comentario)
            return render(request, 'main/editarcomentario.html', {"form": form})
        else:
            return redirect("main:disciplina", disciplina_id)
    else:
        return redirect("accounts:login")


def delete_comment(request, disciplina_id, comentario_id):
    if request.user.is_authenticated:
        disciplina = Disciplina.objects.get(id=disciplina_id)
        comentario = Comentario.objects.get(disciplina=disciplina, id=comentario_id)
        
        if request.user == comentario.user:
            comentario.delete()
        return redirect("main:disciplina", disciplina_id)
    else:
        return redirect("accounts:login")