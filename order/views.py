# -*- coding: utf-8 -*-

from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.translation import gettext as __
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils import simplejson
from django.core.paginator import Paginator
from django.core import serializers

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django import http
from django.template.loader import get_template
from django.template import Context
import ho.pisa as pisa
import cStringIO as StringIO
import cgi

from forms import *
from models import *

@login_required
def add_client(request):
    context = {}
    if request.POST:
        form = AddClientForm(request.POST)
        
        if form.is_valid():
            # Address
            address = Address()
            address.street = request.POST['street']
            address.complement = request.POST['complement']
            address.neighborhood = request.POST['neighborhood']
            address.zip = request.POST['zip']
            address.save()
            
            # Phone
            phone = Phone()
            phone.number = request.POST['phone']
            phone.save()
            
            # Client
            client = Client()
            client.name = request.POST['name']
            client.email = request.POST['email']
            client.address = address
            client.phone = phone
            client.save()
            
            messages.success(request,
                __('Cliente \'%s\' criado com sucesso.' % client.name))
            
            form = AddClientForm()
            context['class_message'] = 'green'
        else:
            context['class_message'] = 'red'
            messages.error(request,
                __(u'Ocorreu um erro ao tentar salvar o perfil. Verifique os campos!'))
    else:
        form = AddClientForm()

    context['form'] = form
    return render_to_response('order/add_client.html',
                                context,
                                context_instance=RequestContext(request))

@login_required
def list_client(request):
    context = {}
    clients = Client.objects.all()
    context['clients'] = clients
    return render_to_response('order/list_client.html',
                              context,
                              context_instance=RequestContext(request))
    
@login_required
def add_order(request, client_id='0'):
    print 'CLIENT_ID: %s' % (client_id,)
    context = {}
    if request.POST:
        form = AddOrderForm(request.POST)
        print request.POST
        if form.is_valid():
            for id in request.POST['table_values']:
                try:
                    int(id)
                    order = Order()
                    order.no_order = request.POST['no_order']
                    order.client = Client.objects.get(name=request.POST['client'])
                    order.service = Service.objects.get(pk=id)
                    order.save()
                except ValueError:
                    pass
            
            messages.success(request,
                __('Ordem \'%s\' criada com sucesso.' % order.no_order))
            
            form = AddOrderForm()
            context['class_message'] = 'green'
        else:
            context['class_message'] = 'red'
            messages.error(request,
                __(u'Ocorreu um erro ao tentar salvar o perfil. Verifique os campos!'))
    else:
        form = AddOrderForm()
        client = Client.objects.get(pk=client_id)
        context['client'] = client
        try:
            latest_order = Order.objects.latest('pk')
            context['order_id'] = latest_order.pk + 1
        except:
            context['order_id'] = 1
        

    context['form'] = form
    return render_to_response('order/add_order.html',
                                context,
                                context_instance=RequestContext(request))
    
@login_required
def list_order(request):
    context = {}
    orders = Order.objects.all()
    context['orders'] = orders
    return render_to_response('order/list_order.html',
                              context,
                              context_instance=RequestContext(request))
    
@login_required
def add_service(request, template='order/add_service.html'):
    context = {}
    if request.POST:
        form = AddServiceForm(request.POST)
        
        if form.is_valid():
            service = form.save()
            messages.success(request,
                __('Servico \'%s\' criado com sucesso.' % service.no_service))
            
            form = AddServiceForm()
            context['class_message'] = 'green'
        else:
            context['class_message'] = 'red'
            messages.error(request,
                __(u'Ocorreu um erro ao tentar salvar o perfil. Verifique os campos!'))
    else:
        form = AddServiceForm()

    context['form'] = form
    return render_to_response(template,
                                context,
                                context_instance=RequestContext(request))
    
@login_required
def list_service(request):
    context = {}
    services = Service.objects.all()
    context['services'] = services
    return render_to_response('order/list_service.html',
                              context,
                              context_instance=RequestContext(request))
    
@login_required
def list_service_json(request):
    page = request.GET.get('page','')
    print 'Page: %s' % (page,)
    limit = request.GET.get('rows', '')
    print 'Limit: %s' % (limit,)
    sidx = request.GET.get('sidx', '')
    print 'Sidx: %s' % (sidx,)
    sord = request.GET.get('sord', '')
    print 'Sord: %s' % (sord,)
    search = request.GET.get('_search','')
    print 'Search: %s' % (search,)
    
    if sord == 'asc':
        sord = '-'
    else:
        sord = ''

    services = Service.objects.all()
    
    if search == 'true':
        searchField = request.GET.get('searchField','')
        print 'SearchField: %s' % (searchField,)
        searchOper = request.GET.get('searchOper','')
        print 'SearchOper: %s' % (searchOper,)
        searchString = request.GET.get('searchString','')
        print 'SearchString: %s' % (searchString,)
        
    services_result = services.order_by(str(sord) + str(sidx))
    n_services = services_result.count()
    print 'Numero de serviços: %s' % (n_services,)
    paginator = Paginator(services_result, int(limit))
    
    try:
        page = request.GET.get('page', '1')
    except ValueError:
        page = 1
    
    try:
        resultados = paginator.page(page)
    except (EmptyPage, InvalidPage):
        resultados = paginator.page(paginator.num_pages)
    
    rows = []
    i = 1
    for service in resultados.object_list:
        row = {"id": service.id, "cell": [service.no_service, service.description, str(service.price)]}
        rows.append(row)
        i += 1
    results = {"page": page, "total": paginator.num_pages, "records": n_services, "rows": rows}
    simple_dumps = simplejson.dumps(results)
    print simple_dumps
    return HttpResponse(simple_dumps, mimetype='application/json')

@login_required
def list_service_json(request):
    data = serializers.serialize('json', Service.objects.all())
    return HttpResponse(data, mimetype='application/json')
    
def write_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(
        html.encode("UTF-8")), result)
    if not pdf.err:
        return http.HttpResponse(result.getvalue(), \
             mimetype='application/pdf')
    return http.HttpResponse("Gremlin's ate your pdf! %s" % cgi.escape(html))

def order(request, id):
    order = get_object_or_404(Order, pk=id)

    return write_pdf('order/order.html',{
        'pagesize' : 'A4',
        'order' : order})