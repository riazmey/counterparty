from django.db import models
from django.utils import timezone
from .enumOrganizationsLegalType import EnumOrganizationsLegalType


class Counterparty(models.Model):

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["ogrn"]),
            models.Index(fields=["inn"]),
            models.Index(fields=["inn", "kpp"])
        ]
        unique_together = ("inn", "kpp")
        ordering = ["name"]
        verbose_name = "Контрагент"
        verbose_name_plural = "Контрагенты"

    type = models.ForeignKey(
        EnumOrganizationsLegalType,
        on_delete=models.PROTECT,
        blank=False,
        verbose_name="Форма организации"
    )

    name = models.CharField(
        max_length=128,
        default="",
        blank=False,
        verbose_name="Наименование (для поиска)"
    )

    name_short = models.CharField(
        max_length=255,
        default="",
        blank=False,
        verbose_name="Наименование (сокращенное)"
    )

    name_full = models.CharField(
        max_length=255,
        default="",
        blank=False,
        verbose_name="Наименование (полное)"
    )

    ogrn = models.CharField(
        max_length=13,
        default="",
        blank=True,
        verbose_name="ОГРН"
    )

    ogrn_date = models.DateField(
        default=None,
        blank=True,
        null=True,
        verbose_name="Дата ОГРН (дата регистрации)"
    )

    inn = models.CharField(
        max_length=12,
        default="",
        blank=False,
        verbose_name="ИНН"
    )

    kpp = models.CharField(
        max_length=9,
        default="",
        blank=True,
        verbose_name="КПП"
    )

    okpo = models.CharField(
        max_length=10,
        default="",
        blank=True,
        verbose_name="ОКПО"
    )
    
    repr = models.CharField(
        max_length=255,
        default="",
        blank=True,
        verbose_name="Контрагент"
    )

    def clean(self):
        super().clean()
        if self.inn and self.kpp:
            self.repr = f"{self.name} ({self.inn}/{self.kpp})"
        elif self.inn:
            self.repr = f"{self.name} ({self.inn})"
        else:
            self.repr = self.name

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr

    def __eq__(self, value):
        if isinstance(value, str):
            return self.name == value
        return super().__eq__(value)
