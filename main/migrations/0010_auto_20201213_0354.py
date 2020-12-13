# Generated by Django 3.1.4 on 2020-12-13 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_delete_vote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='disciplina',
            name='crit_avaliacao',
        ),
        migrations.RemoveField(
            model_name='disciplina',
            name='met_avaliacao',
        ),
        migrations.RemoveField(
            model_name='disciplina',
            name='recup_avaliacao',
        ),
        migrations.AlterField(
            model_name='disciplina',
            name='bibliografia',
            field=models.TextField(max_length=10000),
        ),
        migrations.AlterField(
            model_name='disciplina',
            name='descricao',
            field=models.TextField(max_length=5000),
        ),
        migrations.AlterField(
            model_name='disciplina',
            name='programa_resumido',
            field=models.TextField(max_length=5000),
        ),
    ]
