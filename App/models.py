from django.db import models

# Create your models here.


class ContenidoTraducido(models.Model):
    idioma = models.CharField(max_length=30,null=False,blank=False,unique=True)
    contenido = models.TextField()