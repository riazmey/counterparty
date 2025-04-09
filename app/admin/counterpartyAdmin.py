from django.contrib import admin
from app.models import Counterparty


class CounterpartyAdmin(admin.ModelAdmin):
    fields = [
        "type",
        "name",
        "name_short",
        "name_full",
        ("ogrn", "ogrn_date"),
        ("inn", "kpp"),
        "okpo"
    ]
    list_display = ["name", "type", "inn", "kpp"]
    search_fields = ["name", "inn", "ogrn"]
    ordering = ["name"]


admin.site.register(Counterparty, CounterpartyAdmin)
