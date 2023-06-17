from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime, timedelta
# Create your models here.

class Usuario(AbstractUser):
    pass

class Frota(models.Model):
    lista = (('DISPONÍVEL', 'DISPONÍVEL'),
             ('EM ROTA', 'EM ROTA'),
             ('MANUTENÇÃO', 'MANUTENÇÃO'),
             )
    empresas = [
            ('IPIRANGA', 'IPIRANGA'),
        ('SHELL', 'SHELL'),
    ]
    numero = models.IntegerField()
    imagem = models.ImageField(upload_to = 'foto_frota', default= 'padrão.png')
    placa = models.CharField(max_length = 8)
    tipo = models.CharField(max_length = 20)
    bau = models.CharField(max_length = 20)
    capacidade = models.IntegerField()
    motorista = models.ForeignKey('Colaboradores', related_name= 'colaboradores', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=lista, default='DISPONÍVEL')
    empresa = models.CharField(max_length=10, choices=empresas, default= 'IPIRANGA' )

    def __str__(self):
        return str(self.numero)

class Colaboradores(models.Model):
    funcoes = [('OPERADOR','OPERADOR'),
              ('AJUDANTE','AJUDANTE'),
              ('MOTORISTA VUC', 'MOTORISTA VUC'),
              ('MOTORISTA MÉDIO','MOTORISTA MÉDIO'),
              ('MOTORISTA PESADO', 'MOTORISTA PESADO'),
              ('MOTORISTA MONITOR', 'MOTORISTA MONITOR'),

              ]
    lista_status = [('DISPONÍVEL', 'DISPONÍVEL'),
                    ('EM ROTA', 'EM ROTA'),
                    ('FÉRIAS', 'FÉRIAS'),
                    ('AFASTADO', 'AFASTADO'),
                    ('ATESTADO', 'ATESTADO'),
                    ('FOLGA', 'FOLGA'),
                    ]
    lista_hora = [('NULO',' NULO'),
                  ('POSITIVO', 'POSITIVO'),
                  ('NEGATIVO', 'NEGATIVO'),
                    ]
    empresas = [
        ('IPIRANGA', 'IPIRANGA'),
        ('SHELL', 'SHELL'),
    ]

    nome = models.CharField(max_length=100)
    nome_guerra = models.CharField(max_length=50)
    funcao = models.CharField(max_length=20, choices=funcoes)
    status = models.CharField(max_length=20, choices=lista_status, default='DISPONÍVEL')
    periodo = models.CharField(max_length=10, blank=True, null=True)
    horas = models.CharField(max_length=90, blank=True, null=True)
    tempo_s = models.FloatField(blank=True)
    status1 = models.CharField(max_length=20, choices=lista_hora, default='NULO')
    empresa = models.CharField(max_length=20, choices=empresas, default='IPIRANGA')
    observacoes = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        hora = int(self.horas[:2])
        minutos = int(self.horas[3:5])

        segundos = hora * 3600 + minutos * 60
        if segundos == '':
            self.status1 = 'NULO'

        if self.status1 == 'NEGATIVO':
            self.tempo_s = -segundos
        else:
            self.tempo_s = segundos
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_guerra

class Escala(models.Model):
    data = models.DateField(default= datetime.utcnow)
    remessa = models.CharField(max_length=100)
    frota = models.IntegerField()
    placa = models.CharField(max_length=10)
    tipo_carga = models.CharField(max_length=5)
    peso = models.IntegerField()
    entregas = models.IntegerField(default=0)
    distancia = models.IntegerField(default=0)
    motorista = models.CharField(max_length=30)
    ajudante = models.CharField(max_length=30)
    viagem = models.CharField(max_length=3)
    status = models.CharField(max_length=10, default ='EM ENTREGA')
    observacao = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return str(self.remessa)

class ArqRemessa(models.Model):
    arquivo = models.FileField(upload_to='/remessas')

    def __str__(self):
        return str(self.arquivo)

class Remessa(models.Model):
    remessa = models.CharField(max_length=10)
    placa = models.CharField(max_length=10)
    peso = models.IntegerField(default= 0)
    categoria = models.CharField(max_length=10, default='N/D')
    entregas = models.IntegerField(default=0)
    distancia = models.IntegerField(default=0)
    status = models.CharField(max_length=10, default= 'DISPONÍVEL')

    def __str__(self):
        return str(self.remessa)



