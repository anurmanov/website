from django.db import models
from tinymce import HTMLField

class CompanyInfo(models.Model):
    class Meta:
        verbose_name = 'информация о компании'
        verbose_name_plural = 'информация о компании'
        ordering = ['name']
    code = models.CharField(max_length = 50, verbose_name = 'код параметра')
    name = models.CharField(max_length = 50, verbose_name = 'название параметра')
    value = HTMLField('Значение параметра')
    def __str__(self):
        return self.name
