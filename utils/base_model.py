from django.db import models


class BaseModel(models.Model):

    id = models.AutoField(primary_key=True, verbose_name='主键', help_text='主键')
    create_time = models.DateTimeField(verbose_name='创建时间', help_text='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', help_text='更新时间', auto_now=True)

    class Meta:

        abstract = True
        verbose_name = "公共字段表"
        db_table = "BaseModel"