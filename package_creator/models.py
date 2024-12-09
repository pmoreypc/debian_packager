from django.db import models

# Create your models here.
class Package(models.Model):
    username = models.CharField(max_length=100)
    public_key = models.TextField()
    private_key = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
