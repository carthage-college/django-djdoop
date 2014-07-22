django-djdoop
==============

Django Data quality applications for informix database 

# Apache Configuration

    # Data quality
    <Location /data-quality>
    WSGIProcessGroup djdoop
    WSGIApplicationGroup djdoop
    </Location>
    WSGIDaemonProcess djdoop user=www-data group=www-data processes=2 threads=15
    #WSGIImportScript /d2/django_projects/djforms/wsgi process-group=djdoop application-group=djdoop
    WSGIScriptAlias /data-quality "/d2/django_projects/djdoop/wsgi.py"

# Informix schemas

    /opt/carsi/schema/development/

