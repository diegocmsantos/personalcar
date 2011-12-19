# -*- coding: utf-8 -*-

from django.core.context_processors import csrf
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.translation import gettext as __
from django.core.urlresolvers import reverse
from django.db.models import Q

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from forms import LoginForm

from django.contrib.auth import authenticate, login

@login_required
def office(request, template="index.html"):
        return render_to_response(template,
                                {},
                                context_instance=RequestContext(request))
        
def www(request, template="index_accordion.html"):
    return render_to_response(template,
        {},
        context_instance=RequestContext(request))

def make_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                if request.POST['next']:
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return HttpResponseRedirect('/office')
                # return render_to_response('index.html')
            else:
                # Return a 'disabled account' error message
                messages.error(request, 
                    __(u'Conta desativada. Por favor, contacte o adminstrador'))
        else:
            # Return an 'invalid login' error message.
            messages.error(request, 
                    __(u'Usuario ou senha invalidos. Por favor, tente novamente'))
        
    form = LoginForm()
    return render_to_response('login/login.html',
                                {'form': form},
                                context_instance=RequestContext(request))
    
@login_required
def about(request):
    return render_to_response('first_page.html')