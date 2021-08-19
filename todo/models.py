from django.db import models
from django.utils import timezone

# Create your models here.
class Todo(models.Model):
  todo = models.CharField('ToDo', max_length=100, blank=False)
  created_at = models.DateTimeField('作成日時', auto_now_add=True)
  updated_at = models.DateTimeField('更新日時',auto_now=True)
  adress = models.CharField('住所', max_length=100, blank=False)
  lat = models.DecimalField('緯度', max_digits=9, decimal_places=6, default=0)
  lng = models.DecimalField('経度', max_digits=9, decimal_places=6, default=0)

  def __str__(self):
    return self.todo