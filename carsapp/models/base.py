from __future__ import unicode_literals

from django.db import models
from django.utils import timezone


class BaseModel(models.Model):

    class Meta:
        abstract = True

    created_at = models.DateTimeField(null=True)
    updated_at = models.DateTimeField(null=True)

    def before_save(self):
        pass

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        self.before_save()
        return super(BaseModel, self).save(*args, **kwargs)

    @classmethod
    def save_with(cls, **kwargs):
        kwargs = cls._validate_kwargs(kwargs)
        obj = cls(**kwargs)
        obj.save()
        return obj

    def update_with(self, **kwargs):
        kwargs = self._validate_kwargs(kwargs)
        for field_name, value in kwargs.iteritems():
            setattr(self, field_name, value)
        self.save()

    @classmethod
    def _validate_kwargs(cls, kwargs):
        field_names = [field.name for field in cls._meta.get_fields()]
        return { k: v for k,v in kwargs.iteritems() if k in field_names}
