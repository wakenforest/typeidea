from django.db import models

# Create your models here.

class YoudaoResult(models.Model):
    word = models.CharField(max_length=50, verbose_name="单词")
    text = models.CharField(max_length=255, verbose_name="文本")

    class Meta:
        verbose_name = verbose_name_plural='有道'

    def __str__(self):
        return self.word
    
    @classmethod
    def get_all(cls):
        return cls.objects.all()