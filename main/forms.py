from django import forms
from .models import *

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ("texto",)

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ("notageral",
                "notaCrit1",
                "notaCrit2",
                "notaCrit3",
                "notaCrit4",)