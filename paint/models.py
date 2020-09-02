from django.db import models

import django.utils.timezone as timezone

# Create your models here.

class ImgModel(models.Model):
    author=models.CharField(max_length=255, default="格格")
    title= models.CharField(max_length=255, default="画画")
    category=models.CharField(max_length=255, default="油画，油画棒，丙烯，彩铅")
    comment=models.TextField(default="一句话想法")

    add_date = models.DateTimeField('save_date',default = timezone.now)
    mod_date = models.DateTimeField('last_modified', auto_now = True)
    datas=models.ImageField(upload_to='imgs/%Y/%m')

    def __str__(self):
        return self.title
