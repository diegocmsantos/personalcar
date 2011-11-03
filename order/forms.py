# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import gettext_lazy as _, gettext as __
from django.core.urlresolvers import reverse
from django.conf import settings

from uni_form import helpers

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
    
    model = forms.CharField(label=_('Modelo'), max_length=100)
    license_plate = forms.CharField(label=_('Placa'), max_length=8)
    year = forms.CharField(label=_('Ano'), max_length=4)
        
class AddOrderForm(forms.Form):
    service_id = forms.CharField(widget=forms.HiddenInput)
    no_order = forms.IntegerField(label=_('Numero Ordem'))
    client = forms.CharField(label=_('Cliente'), max_length=200)
    service = forms.CharField(label=_('Servico'), max_length=100)

class AddServiceForm(forms.ModelForm):

    class Meta:
        model = Service
        
    @property
    def helper(self):
        """ We call this as a method/property so we don't make the form helper a singleton. """

        # instantiate the form helper object
        helper = helpers.FormHelper()

        # add in some input controls (a.k.a. buttons)
        submit = helpers.Submit('submit','Submit')
        helper.add_input(submit)
        reset = helpers.Reset('reset','Reset')
        helper.add_input(reset)

        # define the form action
        helper.form_action = reverse('awesome-form-action')
        helper.form_method = 'POST'
        # helper.form_class = 'awesomeness'
        # helper.form_id = 'form-100'
        return helper