# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import gettext_lazy as _, gettext as __
from django.core.urlresolvers import reverse
from django.conf import settings

class Order(models.Model):
    no_order = models.IntegerField(_('Número Ordem'))
    client = models.ForeignKey('Client', related_name='Cliente')
    services = models.ManyToManyField('Service', related_name='Ordem de Servico')
    related_parts = models.ManyToManyField("OrderPart", related_name='Peças ordem')
    quant = models.IntegerField(_('Quantidade'))
    discount = models.IntegerField(_('Desconto'), blank=True, null=True)
    date = models.DateField(_('Data de Entrada'), auto_now_add=True)
    
    def total_order(self):
        total = 0
        try:
            for part in self.related_parts.all():
                total += part.total()
            for service in self.services.all():
                total += service.final_price
        except Exception as e:
            print e
            pass
        return total
        
    def total_service(self):
        service_total = 0
        try:
            for service in self.services.all():
                    service_total += service.final_price
        except Exception as e:
            print 'error no total_service'
            print e
        return service_total
    
    def total_part(self):
        part_total = 0
        for part in self.related_parts.all():
                part_total += part.total()
        return part_total
    
    class Meta:
        verbose_name = __('Ordem de Serviço')
        verbose_name_plural = __('Ordens de Serviço')
        ordering = ('date', 'no_order', )

    def __unicode__(self):
        return '%s , client: %s' % (self.no_order, self.client.name)
    
    def get_absolute_url(self):
        return reverse('order.views.order',
                kwargs={'id': self.id})
        
class OrderPart(models.Model):
    part = models.ForeignKey('Part')
    quant = models.IntegerField(_('Quantidade'))
    price = models.DecimalField(_('Valor'), max_digits=6, decimal_places=2)
    
    def total(self):
        return self.quant * self.price
    
    class Meta:
        verbose_name = __('Peça da ordem')
        verbose_name_plural = __('Peças da ordem')

    def __unicode__(self):
        return self.description
    
class Service(models.Model):
    no_service = models.IntegerField(_('Número Servico'), unique=True)
    description = models.CharField(_('Descrição'), max_length=200)
    cost_price = models.DecimalField(_('Valor de Custo'), max_digits=6, decimal_places=2)
    final_price = models.DecimalField(_('Valor'), max_digits=6, decimal_places=2)
    related_parts = models.ManyToManyField("Part", related_name='Peças')
    
    class Meta:
        verbose_name = __('Serviço')
        verbose_name_plural = __('Serviços',)

    def __unicode__(self):
        return self.description
    
class Part(models.Model):
    description = models.CharField(_('Descrição'), max_length=200)
    cost_price = models.DecimalField(_('Valor de Custo'), max_digits=6, decimal_places=2)
    final_price = models.DecimalField(_('Valor'), max_digits=6, decimal_places=2)
    
    class Meta:
        verbose_name = __('Peça')
        verbose_name_plural = __('Peças')

    def __unicode__(self):
        return self.description
    
class Car(models.Model):
    model = models.CharField(_('Modelo'), max_length=100)
    license_plate = models.CharField(_('Placa'), max_length=100)
    year = models.CharField(_('Ano'), max_length=4)
    
    def __unicode__(self):
        return '%s, %s, %s' % (self.model, self.license_plate, self.year)
    
class Client(models.Model):
    name = models.CharField(_('Nome'), max_length=100)
    email = models.EmailField(max_length=75)
    address = models.ForeignKey('Address')
    phone = models.ForeignKey('Phone')
    car = models.ForeignKey('Car')
    
    class Meta:
        verbose_name = __('Cliente')
        verbose_name_plural = __('Clientes')
        ordering = ('name', )

    def __unicode__(self):
        return self.name

class Address(models.Model):
    street = models.CharField(_('Rua'), max_length=200)
    complement = models.CharField(_('Complemento'), max_length=100, blank=True)
    neighborhood = models.CharField(_('Bairro'), max_length=100)
    zip = models.CharField(_('CEP'), max_length=10)
    
    def save_address(self, street, complement, neighborhood, zip):
        self.street = street
        self.complement = complement
        self.neighborhood = neighborhood
        self.zip = zip
        self.save()
    
    def __unicode__(self):
        return self.street

class Phone(models.Model):
    number = models.CharField(_('Telefone'), max_length=15)
    
    def __unicode__(self):
        return self.number