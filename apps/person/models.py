from django.db import models


class Person(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
