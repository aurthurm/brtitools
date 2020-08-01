from django.db import models
from django.utils.translation import gettext_lazy as _


class DateCreateUpdateMixin(models.Model):
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("Date Updated"), auto_now=True)

    class Meta:
        abstract=True