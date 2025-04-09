from django.shortcuts import render, redirect
from app.forms import CounterpartyForm, ContactDetailsInlineFormset

def CounterpartyView(request):
    if request.method == 'POST':
        form = CounterpartyForm(request.POST)
        if form.is_valid():
            counterparty = form.save()
            inline_formset = ContactDetailsInlineFormset(request.POST, instance=counterparty)
            if inline_formset.is_valid():
                inline_formset.save()
                return redirect('success_url')  # Заменить на URL успеха
    else:
        form = CounterpartyForm()
        inline_formset = ContactDetailsInlineFormset()

    return render(request, 'counterpartyTemplateObject.html', {'form': form, 'inline_formset': inline_formset})