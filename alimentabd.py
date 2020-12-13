def handle(self, *args, **kwargs):
    path = kwargs['path']
    with open(path, 'rt') as f:
        reader = csv.reader(f, dialect='excel')
        for row in reader:
            disciplina = Disciplina.objects.create(
                sigla=row[0],
                cred_aula=row[1],
                cred_trabalho=row[2],
                ch_total=row[3],
            )
