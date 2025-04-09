import json
import phonenumbers
from django.db import models
from django.db import connection
from urllib.parse import urlparse
from .counterparty import Counterparty
from email_validator import validate_email, EmailNotValidError


class ContactDetailsType(models.TextChoices):
    ADDRESS = "address"
    PHONE = "phone"
    EMAIL = "email"
    TEXT = "text"
    WEB = "web"


class ContactDetails(models.Model):

    class Meta:
        indexes = [
            models.Index(fields=["counterparty"]),
            models.Index(fields=["counterparty", "type"])
        ]
        ordering = ["counterparty", "type"]
        verbose_name = "Контактная информация контрагента"
        verbose_name_plural = "Контактная информация контрагентов"

    counterparty = models.ForeignKey(
        Counterparty,
        on_delete=models.CASCADE,
        blank=False,
        verbose_name="Контрагент"
    )

    type = models.CharField(
        max_length=20,
        choices=ContactDetailsType.choices,
        blank=False,
        verbose_name="Тип"
    )

    country = models.CharField(
        max_length=100,
        default="",
        blank=True,
        verbose_name="Страна"
    )

    region = models.CharField(
        max_length=255,
        default="",
        blank=True,
        verbose_name="Регион"
    )

    сity = models.CharField(
        max_length=255,
        default="",
        blank=True,
        verbose_name="Город"
    )

    place = models.CharField(
        max_length=255,
        default="",
        blank=True,
        verbose_name="Населенный пункт"
    )

    if connection.vendor == "postgresql":
        json = models.JSONField(
            blank=False,
            verbose_name="Информация в JSON-е"
        )
    else:
        json = models.TextField(
            default="",
            blank=False,
            verbose_name="Информация в JSON-е"
        )
    
    repr = models.CharField(
        max_length=1024,
        default="",
        blank=True,
        verbose_name="Контактная информация контрагента"
    )

    def __str__(self):
        return self.repr

    def __repr__(self):
        return self.repr

    def __eq__(self, value):
        if isinstance(value, str):
            return self.repr == value
        return super().__eq__(value)

    def clean(self):
        super().clean()
        if connection.vendor == "postgresql":
            json_data = self.json
        else:
            json_data = json.loads(self.json)
        match self.type:
            case ContactDetailsType.ADDRESS:
                pass
            case ContactDetailsType.PHONE:
                self.check_json_phone(json_data)
            case ContactDetailsType.EMAIL:
                self.check_json_email(json_data)
            case ContactDetailsType.WEB:
                self.check_json_web(json_data)
        self.json = json.dumps(json_data, ensure_ascii=False, indent=4)
        self.repr = json_data.get("repr")

    def check_json_address(self, json_data):
        self.check_json_keys(self, json_data, ["repr"])
        self.country = json_data.get("country", "")
        self.region = json_data.get("region", "")
        self.сity = json_data.get("сity", "")
        self.place = json_data.get("place", "")
    
    def check_json_phone(self, json_data):
        self.check_json_keys(self, json_data, ["country_code", "operator_code", "number"])
        phone_number = "".join([json_data.country_code, json_data.operator_code, json_data.number])
        try:
            parsed_number = phonenumbers.parse(phone_number)
        except phonenumbers.NumberParseException:
            raise ValueError(f"В поле JSON не корректно указаны данные в свойства country_code или operator_code или number.")
        json_data["repr"] = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

    def check_json_email(self, json_data):
        self.check_json_keys(self, json_data, ["username", "domain"])
        email = f"{json_data.get("username")}@{json_data.get("domain")}"
        try:
            validate_email(email)
        except EmailNotValidError as e:
            ValueError(f"Email {email} не является валидным: {str(e)}")
        json_data["repr"] = email

    def check_json_web(self, json_data):
        self.check_json_keys(self, json_data, ["repr"])
        uri = json_data.get("repr")
        try:
            result = urlparse(uri)
            return all([result.scheme, result.netloc])
        except AttributeError as e:
            ValueError(f"Web ресурс {uri} не является валидным: {str(e)}")
    
    def check_json_keys(self, json_data, keys: list):
        if not isinstance(json_data, map):
            raise ValueError(f"Поле JSON не корректно. Должен быть объект.")
        for key in keys:
            if not json_data.get(key):
                raise ValueError(f"В поле JSON отсутствует обязательное свойство: {key}")
