# Generated by Django 3.1.4 on 2020-12-12 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_avaliacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='disciplina',
            name='notaCrit1',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='disciplina',
            name='notaCrit2',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='disciplina',
            name='notaCrit3',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='disciplina',
            name='notaCrit4',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='disciplina',
            name='notageral',
            field=models.FloatField(default=0),
        ),
    ]
