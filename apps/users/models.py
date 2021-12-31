from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Users(AbstractUser):

    class Meta:
        db_table = "tb_users"
        verbose_name = "用户表"
        verbose_name_plural = "用户表"

    def __str__(self):
        return self.username