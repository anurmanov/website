from django.db import models
from django.urls import reverse

class Service(models.Model):
    class Meta:
        verbose_name = 'услуга'
        verbose_name_plural = 'услуги'
        ordering = ['name']
    name = models.CharField(max_length = 50, verbose_name = 'Название')
    description = models.TextField(max_length = 1000, verbose_name = 'Описание', blank = True)
    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('services')


