from django import forms
from app.models import Counterparty
from app.models import ContactDetails
from app.models import EnumOrganizationsLegalType
from django.forms import inlineformset_factory


class ContactDetailsForm(forms.ModelForm):
    class Meta:
        model = ContactDetails
        fields = '__all__'


class CounterpartyForm(forms.ModelForm):
    class Meta:
        model = Counterparty
        fields = [
            'type',
            'name',
            'name_short',
            'name_full',
            'ogrn',
            'ogrn_date',
            'inn',
            'kpp',
            'okpo',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].queryset = EnumOrganizationsLegalType.objects.all()

# Создание inline-формы для ContactDetails
ContactDetailsInlineFormset = inlineformset_factory(
    Counterparty,
    ContactDetails,
    form=ContactDetailsForm,
    extra=1,  # Количество дополнительных форм
)


