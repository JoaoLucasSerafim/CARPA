from django.db import models

# Create your models here.
class CriarModel(models.Model):
    class agriinfo(models.Model):
        nome = models.CharField(max_length=100)
        cpf = models.CharField(max_length=14)
        rg = models.CharField(max_length=12)
    class geospace(models.Model):
        cep = models.CharField(max_length=9)
        docposse = models.BooleanField()
        vizinhos = models.CharField()
        Total_ha = models.FloatField()
        property_name = models.CharField()
        reservalegal_ha = models.FloatField()
        app_ha = models.FloatField()
        uso_ha = models.FloatField()
        consolidada_ha = models.FloatField()
        corposHidricos = models.IntegerField()
        nascentes = models.IntegerField()