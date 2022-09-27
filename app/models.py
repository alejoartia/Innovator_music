from django.db import models


# Create your models here.

class UploadSync(models.Model):
    images = models.FileField()

