# -*- coding: utf-8 -*-

from django import forms
from django.utils.translation import gettext_lazy as _, gettext as __
from django import template
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.conf import settings

from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

class LoginForm(forms.ModelForm):
    username = forms.CharField(label=_('Usuario'), max_length=100)
    password = forms.CharField(
        label=_('Senha'), 
        max_length=100,
        widget=forms.PasswordInput(render_value=True),
    )
    email = forms.EmailField(label=_('E-mail'))

    class Meta:
        model = User
        
    def clean_username(self):
        data = self.cleaned_data['username']
        
        if len(data) < 4:
            raise forms.ValidationError(
                __(u'O usuario precisa ser maior que 3 caracteres')
            )

        try:
            user = User.objects.get(username=data)
        except:
            return data
        else:
            raise forms.ValidationError(__(u'Este usuario ja existe'))
            
    def clean_password(self):
        data = self.cleaned_data['password']
        
        if len(data) < 6:
            raise forms.ValidationError(
                __(u'A senha precisa ser maior que 5 caracteres')
            )
            
        if self.cleaned_data.has_key('username'):
            if self.cleaned_data['username'] == data:
                raise forms.ValidationError(
                    __(u'Usuario e senha nao podem ser iguais')
                )
                        
        return data

    def clean_email(self):
        data = self.cleaned_data['email']

        try:
            user = User.objects.get(email=data)
        except:
            return data
        else:
            raise forms.ValidationError(__(u'Este e-mail ja existe'))