from django.db import models
from tinymce import HTMLField
from django.utils import timezone
from django.urls import reverse
from taggit.managers import TaggableManager

class News(models.Model):
    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'
        ordering = ['date']
    name = models.CharField(max_length = 200, verbose_name = 'Название')
    date = models.DateTimeField(default = timezone.now)
    content = HTMLField('Content')
    tags = TaggableManager()
    def get_absolute_url(self):
        return reverse('news_detail', kwargs = {"pk": self.pk})
    def __str__(self):
        return str(self.date) + ' - ' + self.name

    