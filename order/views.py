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

from decimal import Decimal

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
            
            # Car
            car = Car()
            car.model = request.POST['model']
            car.license_plate = request.POST['license_plate'].upper()
            car.year = request.POST['year']
            car.save()
            
            # Client
            client = Client()
            client.car = car
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
    clients = []
    if request.GET:
        name_search = request.GET.get('name_search')
        plate_search = request.GET.get('plate_search')
        query = Client.objects
        if name_search:
            clients = query.filter(name__icontains=name_search)
        if plate_search:
            clients = query.filter(car__license_plate=plate_search)
        
    context['clients'] = clients
    return render_to_response('order/list_client.html',
                              context,
                              context_instance=RequestContext(request))
    
@login_required
def add_order(request, client_id='0'):
    context = {}
    if request.POST:
        print request.POST
        form = AddOrderForm(request.POST)
        if form.is_valid():
            part_list = []
            pks_list = request.POST['part_pks'].split(',')
            for part_index in range(len(pks_list)):
                try:
                    if (request.POST['part_quants'].split(',')[part_index].isdigit()):
                        orderPart = OrderPart()
                        id = int(request.POST['part_pks'].split(',')[part_index])
                        orderPart.part = Part.objects.get(pk=id)
                        orderPart.quant = request.POST['part_quants'].split(',')[part_index]
                        orderPart.price = Decimal(request.POST['part_values'].split(',')[part_index])
                        orderPart.save()
                        part_list.append(orderPart)
                except ValueError:
                    pass
                
            service_list = []
            table_values_list = request.POST['table_values'].split(',')
            for index in table_values_list:
                try:
                    service_list.append(Service.objects.get(pk=index))
                except ValueError as e:
                    pass
            
            
            try:
                order = Order()
                order.no_order = request.POST['no_order']
                order.client = Client.objects.get(name=request.POST['client'])
                order.quant = 1
                if (request.POST['order_discount'].isdigit()):
                    order.discount = request.POST['order_discount']
                else:
                    order.discount = 0
                order.save()
                order.related_parts = part_list
                order.services = service_list
                order.save()
                    
                messages.success(request,
                    __('Ordem \'%s\' criada com sucesso.' % order.no_order))
            except ValueError:
                pass
            
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
    
    parts = Part.objects.all()
    context['parts'] = parts
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
                __(u'Serviço \'%s\' criado com sucesso.' % service.description))
            
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
    services = []
    if request.GET:
        code_search = request.GET.get('code_search', '')
        description_search = request.GET.get('description_search', '')
        query = Service.objects
        if code_search and code_search.isdigit():
            services = query.filter(no_service=code_search)
        if description_search:
            services = query.filter(description__icontains=description_search)
        if services:
            context['services'] = services.order_by('no_service')
    return render_to_response('order/list_service.html',
                              context,
                              context_instance=RequestContext(request))
    
@login_required
def add_part(request, template='order/add_part.html'):
    context = {}
    if request.POST:
        form = AddPartForm(request.POST)
        
        if form.is_valid():
            part = form.save()
            messages.success(request,
                __('\'%s\' cadastrado(a) com sucesso.' % part.description))
            
            form = AddPartForm()
            context['class_message'] = 'green'
        else:
            context['class_message'] = 'red'
            messages.error(request,
                __(u'Ocorreu um erro ao tentar salvar o perfil. Verifique os campos!'))
    else:
        form = AddPartForm()

    context['form'] = form
    return render_to_response(template,
                                context,
                                context_instance=RequestContext(request))
    
@login_required
def list_part(request):
    context = {}
    parts = []
    if request.GET:
        description_search = request.GET.get('description_search', '')
        query = Part.objects
        if description_search:
            parts = query.filter(description__icontains=description_search)
        if parts:
            context['parts'] = parts.order_by('description')
    return render_to_response('order/list_part.html',
                              context,
                              context_instance=RequestContext(request))
    
@login_required
def list_part_json(request, list_parts_id):
    parts = Part.objects.filter(pk__in=list_parts_id.split('i'))
    data = serializers.serialize('json', parts)
    return HttpResponse(data, mimetype='application/json')
    
    
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
    return HttpResponse(simple_dumps, mimetype='application/json')

@login_required
def list_service_json(request):
    data = serializers.serialize('json', Service.objects.all())
    return HttpResponse(data, mimetype='application/json')
    
def write_pdf(template_src, context_dict, filename):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()
    pdf = pisa.pisaDocument(StringIO.StringIO(
        html.encode("UTF-8")), result)
    if not pdf.err:
        response = http.HttpResponse(mimetype='application/pdf')
        response['Content-Disposition'] = 'attachment; filename=%s.pdf' % filename
        response.write(result.getvalue())
        return response
    return http.HttpResponse("Gremlin's ate my pdf! %s" % cgi.escape(html))

def order(request, id):
    orders = Order.objects.filter(no_order=id)
    
    return write_pdf('order/order.html',{
        'pagesize' : 'A4', 'orders' : orders}, 'servico')