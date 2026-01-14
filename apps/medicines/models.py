from django.db import models

class Medicine(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    strength = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.strength})"
