========================
django-zoo-project
========================

1.Create new virtualenv
=============================

In development:

    $ mkvirtualenv zoo-env

    $ cd zoo-env

=============================

2.Installation of Dependencies
=============================

Depending on where you are installing dependencies:

In development::

    $ pip install -r requirements/local.txt

For production::

    $ pip install -r requirements.txt

*note: We install production requirements this way because many Platforms as a
Services expect a requirements.txt file in the root of projects.*

========================

3.install Custom apps in site_packages
=============================

'gallery_orders'
'add_vid'

*note: These apps are located in the git repository zoo/custom_apps they need to be moved to site_packages for installation .*

========================

4. Sync Database
=============================

In development:

    $ cd zoo

    $ cd zoo

    $ python manage.py syncdb --settings=zoo.settings.local

========================

5.Migrate
=============================

    $ python manage.py migrate photologue

    $ python manage.py migrate add_vid

========================

6.Start Dev server
=============================

In development:

    $ python manage.py runserver --settings=zoo.settings.local




