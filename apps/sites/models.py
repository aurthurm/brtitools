from django.db import models
from django.utils.translation import gettext_lazy as _


class Site(models.Model):
    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"))

    class Meta:
        verbose_name = _("site")
        verbose_name_plural = _("sites")

    def __str__(self):
        return self.name