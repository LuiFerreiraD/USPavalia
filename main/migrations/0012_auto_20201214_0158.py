# Generated by Django 3.1.4 on 2020-12-14 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_disciplina_met_avaliacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disciplina',
            name='met_avaliacao',
            field=models.TextField(blank=True, null=True),
        ),
    ]
