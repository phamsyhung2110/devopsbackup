from django.db import models

class contactForm(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    def __str__(self) -> str:
        return self.username