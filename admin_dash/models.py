from django.db import models


# Create your models here.
class BurnedTokens(models.Model):
    token = models.CharField(max_length=255, editable=False, unique=True)
