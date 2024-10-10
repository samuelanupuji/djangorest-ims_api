from django.db import models

# Create your models here.\

class Items(models.Model):
    name= models.CharField(max_length=255, unique=True)
    description= models.TextField(blank=True)
    quantity= models.IntegerField(default=0)

    def __str__(self):
        return self.name

