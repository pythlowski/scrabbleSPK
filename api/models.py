from django.db import models
import string
import random

def generate_random_code():
    length = 6

    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k=length))
        if Room.objects.filter(code=code).count() == 0:
            return code


# Create your models here.
class Room(models.Model):
    code = models.CharField(max_length=8, default=generate_random_code, unique=True)
    host = models.CharField(max_length=50, unique=True)
    is_public = models.BooleanField(null=False, default=True)
    created_at = models.DateTimeField(auto_now_add=True)
