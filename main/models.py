from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count

# Create your models here.
class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=7)
    cred_aula = models.IntegerField()
    cred_trabalho = models.IntegerField()
    ch_total = models.IntegerField()
    descricao = models.TextField(max_length=500) #programacao
    programa_resumido = models.TextField(max_length=300)
    met_avaliacao = models.CharField(max_length=50)
    crit_avaliacao = models.CharField(max_length=50)
    recup_avaliacao = models.CharField(max_length=50)
    bibliografia = models.TextField(max_length=1000)

    def __str__(self):
        return self.nome


class Comentario(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField(max_length=1000)
    downVote = models.ManyToManyField(User, blank=True, related_name="downvote")
    upVote = models.ManyToManyField(User, blank=True, related_name="upvote")

    def __str__(self):
        return self.user.username