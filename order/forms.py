# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import gettext_lazy as _, gettext as __
from django.core.urlresolvers import reverse
from django.conf import settings

from models import *

class AddClientForm(forms.Form):
    textClass = forms.TextInput(attrs={'class':'text'})
    name = forms.CharField(label=_('Nome'), max_length=100)
    email = forms.EmailField(max_length=75)
    phone = forms.CharField(label=_('Telefone'), max_length=15)
    street = forms.CharField(label=_('Rua'), max_length=200)
    complement = forms.CharField(label=_('Complemento'), max_length=200, required=False)
    neighborhood = forms.CharField(label=_('Bairro'), max_length=200)
    zip = forms.CharField(label=_('CEP'), max_length=15)
        
class AddOrderForm(forms.Form):
    service_id = forms.CharField(widget=forms.HiddenInput)
    no_order = forms.IntegerField(label=_('Numero Ordem'))
    client = forms.CharField(label=_('Cliente'), max_length=200)
    service = forms.CharField(label=_('Servico'), max_length=100)

class AddServiceForm(forms.ModelForm):

    class Meta:
        model = Service