# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Order'
        db.create_table('order_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('no_order', self.gf('django.db.models.fields.IntegerField')()),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Cliente', to=orm['order.Client'])),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(related_name='Ordem de Servico', to=orm['order.Service'])),
            ('discount', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('order', ['Order'])

        # Adding model 'Service'
        db.create_table('order_service', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('no_service', self.gf('django.db.models.fields.IntegerField')()),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=6, decimal_places=2)),
        ))
        db.send_create_signal('order', ['Service'])

        # Adding model 'Client'
        db.create_table('order_client', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['order.Address'])),
            ('phone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['order.Phone'])),
        ))
        db.send_create_signal('order', ['Client'])

        # Adding model 'Address'
        db.create_table('order_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('street', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('complement', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('neighborhood', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('order', ['Address'])

        # Adding model 'Phone'
        db.create_table('order_phone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('order', ['Phone'])


    def backwards(self, orm):
        
        # Deleting model 'Order'
        db.delete_table('order_order')

        # Deleting model 'Service'
        db.delete_table('order_service')

        # Deleting model 'Client'
        db.delete_table('order_client')

        # Deleting model 'Address'
        db.delete_table('order_address')

        # Deleting model 'Phone'
        db.delete_table('order_phone')


    models = {
        'order.address': {
            'Meta': {'object_name': 'Address'},
            'complement': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'order.client': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Client'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['order.Address']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['order.Phone']"})
        },
        'order.order': {
            'Meta': {'ordering': "('date', 'no_order')", 'object_name': 'Order'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Cliente'", 'to': "orm['order.Client']"}),
            'date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'discount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_order': ('django.db.models.fields.IntegerField', [], {}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'Ordem de Servico'", 'to': "orm['order.Service']"})
        },
        'order.phone': {
            'Meta': {'object_name': 'Phone'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'order.service': {
            'Meta': {'object_name': 'Service'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'no_service': ('django.db.models.fields.IntegerField', [], {}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '6', 'decimal_places': '2'})
        }
    }

    complete_apps = ['order']
