from django.db import models


class EnumOrganizationsLegalType(models.Model):

    class Meta:
        indexes = [
            models.Index(fields=["name"])
        ]
        ordering = ["name"]
        verbose_name = "Тип правовой формы организации"
        verbose_name_plural = "Типы правовых форм организаций"

    name = models.CharField(
        max_length=50,
        default="",
        blank=False,
        unique=True,
        verbose_name="Имя"
    )

    repr = models.CharField(
        max_length=255,
        default="",
        blank=False,
        verbose_name="Типы правовых форм организаций"
    )

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr

    def __eq__(self, value):
        if isinstance(value, str):
            return self.name == value
        return super().__eq__(value)
