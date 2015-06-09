from django.db import models

class Permalinkable(models.Model):
    slug = models.SlugField()

    class Meta:
        abstract = True
