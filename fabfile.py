# -*- coding: utf-8 -*-
"""
Fabfile template for deploying django apps on webfaction using gunicorn,
and supervisor.

# TODO:
 -- currently only for single-app websites.
 -- if an app with our app name already exists, we use it without checking its structure..
 -- we take the first listed IP address. I only have one so it's not an issue for me...
"""


from fabric.api import *
from fabric.contrib.files import upload_template, exists, append
import xmlrpclib
import sys

import string, random

try:
    from fabsettings import DOMAIN_NAME, APPLICATION_NAME, WEBSITE_NAME, APPLICATION_PATH, SUBDOMAIN_PREFIX
#    from fabsettings import WF_HOST, PROJECT_NAME, REPOSITORY, USER, PASSWORD, VIRTUALENVS, SETTINGS_SUBDIR
    from fabsettings import CONTROL_PANEL_USER, CONTROL_PANEL_PASSWORD
except ImportError:
    print("ImportError: Couldn't find fabsettings.py, it either does not exist or giving import problems (missing settings)")
    sys.exit(1)

## env.hosts           = [WF_HOST]
## env.user            = USER
## env.password        = PASSWORD
## env.home            = "/home/%s" % USER
## env.project         = PROJECT_NAME
## env.repo            = REPOSITORY
## env.project_dir     = env.home + '/webapps/' + PROJECT_NAME
## env.settings_dir    = env.project_dir + '/' + SETTINGS_SUBDIR
## env.supervisor_dir  = env.home + '/webapps/supervisor'
## env.virtualenv_dir  = VIRTUALENVS
## env.supervisor_ve_dir = env.virtualenv_dir + '/supervisor'
## env.template_dir    = 'fabric_templates'

env.website_name = WEBSITE_NAME
env.domain_name = DOMAIN_NAME
env.subdomain_prefix = SUBDOMAIN_PREFIX
env.application_name = APPLICATION_NAME
env.application_path = APPLICATION_PATH


def subdomain_exists(domain_name):
    """Return True if domain name (or subdomain) exists, False if it doesn't"""

    # the API returns subdomain prefixes along with domains - we want a single list of
    # domains and subdomains to check against, so let's create it.

    api_response = list_domains()
    all_domains_and_subdomains = []
    for domain in api_response:
        all_domains_and_subdomains.append(domain['domain'])
        for subdomain in domain:
            all_domains_and_subdomains.append('.'.join([subdomain, domain['domain']]))
    return (domain_name in all_domains_and_subdomains)

def get_website_data(website_name):
    """Get the webfaction website data for website_name."""
    
    api_response = list_websites()
    website_data = None
    for website in api_response:
        if website['name'] == website_name:
            website_data = website
    return website_data

def website_exists(website_name):
    """Check whether webfation website with specified name exists."""

    website_data = get_website_data(website_name)   
    return (website_data is not None)

def process_subdomain(domain_name, subdomain_prefix):
    if subdomain_prefix:
        subdomain = '.'.join([subdomain_prefix, domain_name])
    else:
        subdomain = domain_name
    return subdomain

def check_website_structure(website_name, domain_name, subdomain_prefix, application_name, application_path):
    """raise exception if website doesn't use the specified domain and app."""

    website_data = get_website_data(website_name)
    subdomain = process_subdomain(domain_name, subdomain_prefix)
    if website_data is None:
        raise Exception('Cannot find data for website "%s"' % website_name)
    if subdomain not in website_data['subdomains']:
        raise Exception('Domain name "%s" is not configured for website "%s"' % (domain_name, website_name))
    if [application_name, application_path] not in website_data['website_apps']:
        raise Exception('App ["%s", "%s"] not configured for website "%s"' % (application_name, application_path, website_name))

def get_app_data(app_name):
    """Get the webfaction app data for app_name."""
    
    api_response = list_apps()
    app_data = None
    for app in api_response:
        if app['name'] == app_name:
            app_data = app
    return app_data
    
def app_exists(app_name):
    app_data = get_app_data(app_name)
    return (app_data is not None)
    
    
def setup_website():
    """..."""
    
    if website_exists(env.website_name):
        print("website exists")
        check_website_structure(env.website_name, env.domain_name, env.subdomain_prefix, env.application_name, env.application_path)
    else:
        print("creating website")
        subdomain = process_subdomain(env.domain_name, env.subdomain_prefix)
        if not subdomain_exists(subdomain):
            create_domain(env.domain_name, env.subdomain_prefix)
        if not app_exists(env.application_name):
            create_app(env.application_name, 'custom_app_with_port', False, '')
        ip_address = get_webfaction_ip()
        
        create_website(env.website_name, ip_address, True, [subdomain], [env.application_name, env.application_path])

def get_webfaction_ip():
    ip_list = list_ips()
    return ip_list[0]['ip']
     
def test():
    print get_webfaction_ip()

## def deploy():
##     bootstrap()
    
##     if not exists(env.supervisor_dir):
##         install_supervisor()
    
##     install_app()



## def bootstrap():
##     run('mkdir -p %s/lib/python3.3' % env.home)
##     run('easy_install-3.3 pip')
##     run('pip3.3 install --user virtualenv virtualenvwrapper')


## def install_app():
##     """Installs the django project in its own wf app and virtualenv
##     """
##     response = _webfaction_create_app(env.project)
##     env.app_port = response['port']

##     # upload template to supervisor conf
##     upload_template('%s/gunicorn.conf' % env.template_dir,
##                     '%s/conf.d/%s.conf' % (env.supervisor_dir,env.project),
##                     {
##                         'project': env.project,
##                         'project_dir': env.settings_dir,
##                         'virtualenv':'%s/%s' % (env.virtualenv_dir, env.project),
##                         'port': env.app_port,
##                         'user': env.user,
##                      }
##                     )

##     with cd(env.home + '/webapps'):
##         if not exists(env.project_dir + '/setup.py'):
##             run('git clone %s %s' % (env.repo ,env.project_dir))

##     _create_ve(env.project)
##     reload_app()
##     restart_app()

## def install_supervisor():
##     """Installs supervisor in its wf app and own virtualenv
##     """
##     response = _webfaction_create_app("supervisor")
##     env.supervisor_port = response['port']
##     _create_ve('supervisor')
##     if not exists(env.supervisor_ve_dir + 'bin/supervisord'):
##         _ve_run('supervisor','pip install supervisor')
##     # uplaod supervisor.conf template
##     upload_template('%s/supervisord.conf' % env.template_dir,
##                      '%s/supervisord.conf' % env.supervisor_dir,
##                     {
##                         'user':     env.user,
##                         'password': env.password,
##                         'port': env.supervisor_port,
##                         'dir':  env.supervisor_dir,
##                     },
##                     )

##     # upload and install crontab
##     upload_template('%s/start_supervisor.sh' % env.template_dir,
##                     '%s/start_supervisor.sh' % env.supervisor_dir,
##                      {
##                         'user':     env.user,
##                         'virtualenv': env.supervisor_ve_dir,
##                     },
##                     mode=0750,
##                     )



##     # add to crontab

##     filename = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(7))
##     run('crontab -l > /tmp/%s' % filename)
##     append('/tmp/%s' % filename, '*/10 * * * * %s/start_supervisor.sh start' % env.supervisor_dir)
##     run('crontab /tmp/%s' % filename)


##     # create supervisor/conf.d
##     with cd(env.supervisor_dir):
##         run('mkdir conf.d')

##     with cd(env.supervisor_dir):
##         with settings(warn_only=True):
##             run('./start_supervisor.sh stop && ./start_supervisor.sh start')



## def reload_app(arg=None):
##     """Pulls app and refreshes requirements"""

##     with cd(env.project_dir):
##         run('git pull')

##     if arg != "quick":
##         with cd(env.project_dir):
##             _ve_run(env.project, "pip install -r requirements/production.txt")
##             _ve_run(env.project, "manage.py syncdb")
##             _ve_run(env.project, "manage.py collectstatic")

##     restart_app()


## def restart_app():
##     """Restarts the app using supervisorctl"""

##     with cd(env.supervisor_dir):
##         _ve_run('supervisor','supervisorctl reread && supervisorctl reload')
##         _ve_run('supervisor','supervisorctl restart %s' % env.project)

### Webfaction API

def list_domains():
    """Get information about the account’s domains.
    
    returns list of dicts containing:
    id: domain ID
    domain: domain name
    subdomains: list of subdomains for the domain

    e.g.:
    [{'domain':'example.com', id:12345, subdomains:['www','media']}, { ... }, { ... }]
    """

    return _webfaction_api_call("list_domains")

def list_websites():
    """Get information about the account’s websites.

    returns list of dicts containing:
    id: website ID
    name: website name
    ip: website IP address
    https: whether the website is served over HTTPS
    subdomains: array of website’s subdomains
    website_apps: array of the website’s apps and their URL paths;
                  each item in the array is a two-item array,
                  containing an application name and URL path.
    """

    return _webfaction_api_call("list_websites")

def create_domain(domain_name, subdomain_prefix):
    """Create a domain entry

    Parameters:
    domain (string) – a domain name in the form of example.com
    subdomain (string) – each additional parameter provided after domain: a subdomain name of domain
    
    If  domain has  already been  created, you  may supply  additional
    parameters to add subdomains.  For example, if example.com already
    exists,  create_domain  may  be  called with  four  parameters—  a
    session  ID, example.com,  www, private—to  create www.example.com
    and private.example.com.
    """
    
    return _webfaction_api_call("create_domain", domain_name, subdomain_prefix)

def list_apps():
    """Get information about the account’s applications.

    The method returns a list of dicts with the following key-value pairs:

    id: app ID
    name: app name
    type: app type
    autostart: whether the app uses autostart
    port: port number if the app listens on a port, otherwise is 0
    open_port: for applications that listen on a port, whether the port is open on shared and dedicated IP addresses (True for open ports, False for closed ports, or for applications that do not listen to a port)
    extra_info: extra info for the app if any
    machine: name of the machine where the app resides
    """

    return _webfaction_api_call("list_apps")


def create_app(app_name, app_type, autostart, extra_info, open_port):
    """Create a new application.

    Parameters:
    session_id – session ID returned by login
    name (string) – name of the application
    type (string) – type of the application
    autostart (boolean) – whether the app should restart with an autostart.cgi script (optional, default: false)
    extra_info (string) – additional information required by the application; if extra_info is not required or used by the application, it is ignored (optional, default: an empty string)
    open_port (boolean) – for applications that listen on a port, whether the port should be open on shared and dedicated IP addresses (optional, default: false)
    """

    return _webfaction_api_call("create_app", app_name, app_type, extra_info, open_port)


def create_website(website_name, ip, https, subdomains, site_apps):
    """Create a new website entry.

    Applications may  be added  to the  website entry  with additional
    parameters  supplied after  subdomains. The  additional parameters
    must be arrays  containing two elements: a  valid application name
    and a path (for example, 'htdocs' and '/').
        
    Parameters:
    website_name (string): the name of the new website entry
    ip (string): IP address of the server where the entry resides
    https (boolean): whether the website entry should use a secure connection
    subdomains (array): an array of strings of (sub)domains to be associated with the website entry
    site_apps (array): each additional parameter provided after subdomains: an array containing a valid application name (a string) and a URL path (a string)
    """

    return _webfaction_api_call("create_website", website_name, ip, https, subdomains, site_apps)
    

def list_ips():
    """Get information about all of the account’s machines and their IP addresses.

    This method returns an array of structs with the following key-value pairs:

    machine: machine name (for example, Web100)
    ip: IP address
    is_main: a boolean value indicating whether the IP address is the primary address for the server (true) or an extra IP address provisioned to the account (false)
    """

    return _webfaction_api_call("list_ips")

### Helper functions

## def _create_ve(name):
##     """creates virtualenv using virtualenvwrapper
##     """
##     if not exists(env.virtualenv_dir + '/name'):
##         with cd(env.virtualenv_dir):
##             run('mkvirtualenv -p /usr/local/bin/python3.3 --no-site-packages %s' % name)
##     else:
##         print("Virtualenv with name %s already exists. Skipping." % name)

## def _ve_run(ve,cmd):
##     """virtualenv wrapper for fabric commands
##     """
##     run("""source %s/%s/bin/activate && %s""" % (env.virtualenv_dir, ve, cmd))

def _webfaction_api_call(api_command, *args):
    """Wrapper which handles XML-RPC connection for webfaction API
    """
    server = xmlrpclib.ServerProxy('https://api.webfaction.com/')
    session_id, account = server.login(CONTROL_PANEL_USER, CONTROL_PANEL_PASSWORD)
    api_args = (session_id, ) + args
    response = getattr(server, api_command)(*api_args)
    return response

  
## def _webfaction_create_app(app):
##     """creates a "custom app with port" app on webfaction using the webfaction public API.
##     """
##     server = xmlrpclib.ServerProxy('https://api.webfaction.com/')
##     session_id, account = server.login(CONTROL_PANEL_USER, CONTROL_PANEL_PASSWORD)
##     #try:
##     response = server.create_app(session_id, app, 'custom_app_with_port', False, '')
##     print("App on webfaction created: %s" % response)
##     return response

##     #except xmlrpclib.Fault:
##     #    print("Could not create app on webfaction %s, app name maybe already in use" % app)
##     #    sys.exit(1)

