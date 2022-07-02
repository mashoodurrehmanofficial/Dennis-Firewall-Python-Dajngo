from django.db import models 

# Create your models here.



class IPTable(models.Model):
    ip = models.CharField(max_length=100, null=True,blank=True)
    allowed  = models.BooleanField(default=False)
    waiting  = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.ip} - {self.allowed} - {self.waiting}"
