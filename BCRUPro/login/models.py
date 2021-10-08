from django.db import models

# Create your models here.


class User(models.Model):
    gender = (
        ('male', 'male'),
        ('female', 'female'),
    )
    
    role_choice = (
        ('customer', 'customer'),
        ('csp', 'csp'),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=32, choices=role_choice, default='customer')
    sex = models.CharField(max_length=32, choices=gender, default='male')
    c_time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_threader():
        return ["Name", "Email"]

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['c_time']
