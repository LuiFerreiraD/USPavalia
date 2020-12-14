from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count
# open file & create csvreader
import csv


path = r"/Users/luiferreira/Desktop/Sistemas de Informacao/USPavalia/uspavalia/base_dados.csv"


# Create your models here.
class Disciplina(models.Model):
    nome = models.CharField(max_length=100)
    sigla = models.CharField(max_length=7)
    cred_aula = models.IntegerField()
    cred_trabalho = models.IntegerField()
    ch_total = models.IntegerField()
    descricao = models.TextField(max_length=5000)  # programacao
    programa_resumido = models.TextField(max_length=5000)
    bibliografia = models.TextField(max_length=10000)
    met_avaliacao = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.nome


class Comentario(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField(max_length=1000)
    downVote = models.ManyToManyField(
        User, blank=True, related_name="downvote")
    upVote = models.ManyToManyField(User, blank=True, related_name="upvote")

    def __str__(self):
        return self.user.username


class Avaliacao(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notageral = models.FloatField(default=0)
    notaCrit1 = models.FloatField(default=0)
    notaCrit2 = models.FloatField(default=0)
    notaCrit3 = models.FloatField(default=0)
    notaCrit4 = models.FloatField(default=0)

    def __str__(self):
        return self.user.username
