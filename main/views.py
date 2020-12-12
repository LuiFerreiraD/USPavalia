from django.shortcuts import render, redirect
#from django.http import HttpResponse
from .models import *
from .forms import *
from django.db.models import Avg

# Create your views here.
def home(request):
    disciplinas = pesquisa_disciplina(request)

    contexto = {
        "disciplinas": disciplinas,
    }
    return render(request, 'main/index.html', contexto)

    
#pagina da disciplina
def pagina_disciplina(request, id):
    disciplina = Disciplina.objects.get(id=id)
    #comentarios = Comentario.objects.filter(disciplina=id).order_by()

    comentarios =  Comentario.objects.filter(disciplina=id).annotate(
    total_votes=Count('upVote')-Count('downVote')
    ).order_by('total_votes')

    avaliacoes = Avaliacao.objects.filter(disciplina=id)
    mediaGeral = avaliacoes.aggregate(Avg("notageral"))["notageral__avg"]
    mediaCrit1 = avaliacoes.aggregate(Avg("notaCrit1"))["notaCrit1__avg"]
    mediaCrit2 = avaliacoes.aggregate(Avg("notaCrit2"))["notaCrit2__avg"]
    mediaCrit3 = avaliacoes.aggregate(Avg("notaCrit3"))["notaCrit3__avg"]
    mediaCrit4 = avaliacoes.aggregate(Avg("notaCrit4"))["notaCrit4__avg"]

    medias = [
        mediaGeral, mediaCrit1, mediaCrit2, mediaCrit3, mediaCrit4
    ]
    averages = []
    for media in medias:
        if media == None:
            averages.append(0)
        else:
            averages.append(int(round(media)))
    
    print(averages[0], averages[1])

    ranges = [
        range(averages[0]), range(averages[1]), range(averages[2]), range(averages[3]), range(averages[4])
    ]

    contexto = {
        "disciplina": disciplina,
        "comentarios": comentarios,
        "ranges": ranges
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
        return render(request, "main:home", {"form": form})
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

def add_review(request, disciplina_id):
    if request.user.is_authenticated:
        disciplina = Disciplina.objects.get(id=disciplina_id)
        if request.method == "POST":
            form = AvaliacaoForm(request.POST or None)
            if form.is_valid():
                data = form.save(commit=False)
                data.user = request.user
                data.notageral = request.POST["notageral"]
                data.notaCrit1 = request.POST["notaCrit1"]
                data.notaCrit2 = request.POST["notaCrit2"]
                data.notaCrit3 = request.POST["notaCrit3"]
                data.notaCrit4 = request.POST["notaCrit4"]

                data.disciplina = disciplina
                data.save()
                return redirect("main:disciplina", disciplina_id)
        else:
            form = AvaliacaoForm()
        return redirect("main:disciplina", disciplina_id)
    else:
        return redirect("accounts:login")


def pesquisa_disciplina(request):
    #função auxiliar para a barra de pesquisa
    query = request.GET.get("barra_de_pesquisa")
    disciplinas = None

    if query:
        disciplinas = Disciplina.objects.filter(name__icontains=query)
    else:
        disciplinas = Disciplina.objects.all()
    return disciplinas