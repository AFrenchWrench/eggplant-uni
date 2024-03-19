from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    user_id = models.CharField(max_length=8, primary_key=True, unique=True, editable=False)
    type = models.CharField(max_length=1,
                            choices=(('s', 'student'), ('i', 'it manager'), ('p', 'professor'), ('a', 'assistant')))

    def save(self, *args, **kwargs):
        if not self.user_id:
            if self.type == 's':
                id_increment = 100000
                self.user_id = str(id_increment)
                id_increment += 1
            elif self.type == 'p':
                id_increment = 200000
                self.user_id = str(id_increment)
                id_increment += 1
            elif self.type == 'a':
                id_increment = 300000
                self.user_id = str(id_increment)
                id_increment += 1
            elif self.type == 'i':
                id_increment = 400000
                self.user_id = str(id_increment)
                id_increment += 1
        super().save(*args, **kwargs)

    phone = models.CharField(max_length=11, unique=True)
