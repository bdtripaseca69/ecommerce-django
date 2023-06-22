from django.db import models

# Create your models here.
'''class contact_model(models.Model):
    nameP = models.CharField(max_length=60)
    contentP = models.TextField(max_length=500)
    imagenProduct = models.ImageField(upload_to="processor")
    imagenSPECS = models.ImageField(blank=True, upload_to="processor", null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    precioP = models.IntegerField(blank=True, null=True)
    cantidadP = models.IntegerField(blank=True, null=True)
    marcaP = models.CharField(max_length=20)

    class Meta: #representacion en la db, encontrara el modelo(tabla) segun la informacion proporcionada
        verbose_name = 'processor'
        verbose_name_plural = 'processors'
    
    def __str__(self) -> str:
        return self.nameP  '''