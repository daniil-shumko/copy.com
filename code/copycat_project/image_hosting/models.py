from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __unicode__(self):  #For Python 2, use __str__ on Python 3
        return self.name

class Image(models.Model):
    category = models.ForeignKey(Category)
    caption = models.CharField(max_length=128)
    url_image_name = models.CharField(max_length=128, unique=True)
    timestamp = models.DateTimeField()
    views = models.IntegerField(default=0)
    up_votes = models.IntegerField(default=0)
    down_votes = models.IntegerField(default=0)

    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.url_image_name