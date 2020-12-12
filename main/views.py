from django.shortcuts import render
#from django.http import HttpResponse
from.models import *

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

    contexto = {
        "disciplina": disciplina,
    }
    return render(request, 'main/disciplina.html', contexto)