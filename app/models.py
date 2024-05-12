from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['complete']