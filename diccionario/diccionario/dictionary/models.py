# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from pyuploadcare.dj.models import ImageField
from taggit_autosuggest.managers import TaggableManager

@python_2_unicode_compatible
class Word(models.Model):
    title = models.CharField(max_length=255)
    image = ImageField(blank=True, manual_crop="")
    tags = TaggableManager()

    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
