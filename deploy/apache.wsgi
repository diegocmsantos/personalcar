Alias /static/ "/var/www/personalcar/static/"
<Directory "/var/www/personalcar/static">
        Order allow,deny
        Options Indexes
        Allow from all
        IndexOptions FancyIndexing
</Directory>

Alias /media/ "/usr/lib/python2.5/site-packages/django/contrib/admin/media/"
<Directory "/usr/lib/python2.5/site-packages/django/contrib/admin/media">
        Order allow,deny
        Options Indexes
        Allow from all
        IndexOptions FancyIndexing
</Directory>


WSGIDaemonProcess personalcar python-path=/var/envs/personalcar/lib/python2.6/site-packages
WSGIProcessGroup personalcar
WSGIScriptAlias / "/var/www/personalcar/deploy/script.wsgi"
WSGIPassAuthorization On


<Directory "/var/www/personalcar/deploy">
        Allow from all
</Directory>

ErrorLog /var/log/apache2/personalcar_error.log
CustomLog /var/log/apache2/personalcar_access.log combined
LogLevel warn

