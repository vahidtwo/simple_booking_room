from django.db import models


class AbstractBaseModel(models.Model):
    is_active = models.BooleanField('active', default=True)
    priority = models.IntegerField(default=1000000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
