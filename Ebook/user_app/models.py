from django.db import models

# Create your models here.
class User(models.Model) :
    user_id = models.CharField(max_length=255)
    user_name = models.CharField(max_length = 10)
    user_pwd = models.CharField(max_length=20)
    birthday = models.DateField()
    join_date = models.DateTimeField(auto_now_add=True)