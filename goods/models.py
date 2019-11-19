from tinymce import HTMLField
from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from visits.tasks import remove_redis_key

def validate_price(value):
    try:
        f = float(value)
    except:
        raise ValidationError('%(value)s is not an even number', params={'value' : value})

class Country(models.Model):
    class Meta:
        verbose_name = 'страна'
        verbose_name_plural = 'страны'
        ordering = ['name']
    name = models.CharField(max_length = 50, verbose_name = 'Название', unique = True)
    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    class Meta:
        verbose_name = 'производитель'
        verbose_name_plural = 'производители'
        ordering = ['name']
    name = models.CharField(max_length = 50, verbose_name = 'Название', unique = True)
    country = models.ForeignKey(Country, on_delete = models.PROTECT, verbose_name = 'Страна происхождения', default = None)
    logo_image = models.ImageField(upload_to = 'manufacturers/images', verbose_name = 'Логотип', default = None, null = True, blank = True)
    def __str__(self):
        return self.name + ' (' +str(self.country) + ')'

class Category(models.Model):
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['level_index_field','name']
    name = models.CharField(max_length = 50, verbose_name = 'Название', unique = True)
    parent_category = models.ForeignKey('self', on_delete = models.PROTECT, verbose_name = 'Родительская категория', default = None, null = True, blank = True)
    image = models.ImageField(upload_to = 'categories/images', verbose_name = 'Изображение', default = None, null = True, blank = True)
    level_index_field = models.CharField(max_length = 500, verbose_name = 'Индекс вложенности', default = None, editable = False, null = True)
    def __str__(self):
        return '.  '*(self.level() - 1) + self.name
    def get_absolute_url(self):
        return reverse("goods", kwargs = {"pk": self.pk})
    def level(self):
        lvl = 1
        if self.parent_category:
            lvl += self.parent_category.level()
        return lvl
    def level_index(self):
        lvl_ind = str(self.pk)
        if self.parent_category:
            lvl_ind = self.parent_category.level_index() + lvl_ind
        else:
            lvl_ind = '_' + lvl_ind
        return lvl_ind
    def recalc_level_index(self):
        cats = Category.objects.filter(parent_category = self)
        if cats:
            for cat in cats:
                obj = Category.objects.get(pk = cat.pk)
                obj.save(force_update = True)
    def ancestors(self):
        ancs = list()
        if self.parent_category:
            ancs.append(self.parent_category)
            ancs = self.parent_category.ancestors() + ancs
        else:
            ancs.append(None)
        return ancs
    def childs(self):
        cats = Category.objects.all()
        childs = []
        for cat in cats:
            if cat.parent_category == self:
                childs.append(cat)
        return childs
    def build_child_tree(self):
        d = {}
        d[self.name] = []
        childs = self.childs()
        for kid in childs:
            d[self.name].append(kid.build_child_tree())
        return d    

    def save(self, *args, **kwargs):
        if None == self.level_index_field:
            self.level_index_field = self.level_index()
            super(Category, self).save(*args, **kwargs)
        else:
            obj = Category.objects.get(pk = self.pk)
            force_update = kwargs.get('force_update', False)
            if obj.parent_category != self.parent_category or force_update:
                if self.parent_category:
                    if self in self.parent_category.ancestors():
                        raise ValidationError('Циклическая ссылка в родительской категории!')
                self.level_index_field = self.level_index()
                super(Category, self).save(*args, **kwargs)
                self.recalc_level_index()
                return
        super(Category, self).save(*args, **kwargs)

class Good(models.Model):
    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ['name']
    name = models.CharField(max_length = 50, verbose_name = 'Название')
    category = models.ForeignKey(Category, on_delete = models.PROTECT, verbose_name = 'Категория', default = None)
    content = HTMLField('Content')
    manufacturer = models.ForeignKey(Manufacturer, on_delete = models.PROTECT, verbose_name = 'Производитель', default = None)
    featured = models.BooleanField(default = False, db_index = True, verbose_name = 'Рекомендуемый товар')
    image = models.ImageField(upload_to = 'goods/images', verbose_name = 'Изображение', default = None, null = True)
    reg_number = models.CharField(max_length = 50, verbose_name = 'Регистрационное свидетельство', default = None, null = True)
    reg_exp_date = models.DateField(verbose_name = 'Дата окончания регистрации', default = None, null = True)
    def __str__(self):
        return self.name  + ' (' + str(self.category) + ')'
    def save(self, *args, **kwargs):
        try:
            this_record = Good.objects.get(pk = self.pk)
            if this_record.image != self.image:
                this_record.image.delete(save = False)
        except:
            pass
        super(Good, self).save(*args, **kwargs)
    def delete(self, *args, **kwargs):
        """Method of deleting model record.

        Before totaly removing model record we must delete image file
        associated with record and then asynchronously remove 
        visits key from redis cache.
        """
        self.image.delete(save = False)
        path = self.get_absolute_url()
        remove_redis_key.apply_async(args = [path],
        retry = True,
        retry_policy =
        {'max_retries': 20,
        'interval_start': 0.01,
        'interval_step': 0.3,
        'interval_max': 6,})
        super(Good, self).delete(*args, **kwargs)
    def get_absolute_url(self):
        return reverse("goods_detail", kwargs = {"pk": self.pk})
