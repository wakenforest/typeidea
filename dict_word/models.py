from django.db import models

# Create your models here.

class ContList(models.Model):
    text_cj = models.CharField(max_length=255, verbose_name="中日")

    class Meta:
        verbose_name = verbose_name_plural='翻译条目'
    
    def __str__(self):
        return self.text_cj
    
    @classmethod
    def get_all(cls):
        return cls.objects.all()


class YoudaoResult(models.Model):
    word = models.CharField(max_length=50, verbose_name="单词")
    text_ec = models.CharField(max_length=255, verbose_name="英中")
    text_ce = models.CharField(max_length=255, verbose_name="中英")
    text_jc = models.CharField(max_length=255, verbose_name="日中")
    text_cj = models.CharField(max_length=255, verbose_name="中日")
    # text_ec = models.CharField(max_length=255, default='na', verbose_name="英中")
    # text_ce = models.CharField(max_length=255, default='na', verbose_name="中英")
    # text_jc = models.CharField(max_length=255, default='na', verbose_name="日中")
    # text_cj = models.CharField(max_length=255, default='na', verbose_name="中日")
    #text_cj_list = models.ForeignKey(ContList, default='0', verbose_name="中日list" ,on_delete=models.CASCADE)

    class Meta:
        verbose_name = verbose_name_plural='有道'

    def __str__(self):
        return self.word
    
    @classmethod
    def get_all(cls):
        return cls.objects.all()

