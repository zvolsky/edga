# -*- coding: utf-8 -*-

import db_custom
import datetime

dateformat = '%d.%m.%Y'
datetimeformat = '%d.%m.%Y %H:%M'

from w2_mz import ttt  # simulace překladu T()

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

migrate = True
db = DAL('sqlite://edga.sqlite',pool_size=1,check_reserved=['all'],
      #adapter_args=dict(foreign_keys=False),
      #lazy_tables=True,   # zlikviduje odkazy ve smartgridu
      migrate=migrate)

if request.is_local:
    from gluon.custom_import import track_changes
    track_changes(True)    # auto-reload modules
    response.generic_patterns = ['*']
else:
    response.generic_patterns = []

## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud #, Service, PluginManager, prettydate
auth = Auth(db)
#crud, service, plugins = Crud(db), Service(), PluginManager()
crud = Crud(db)
crud.settings.update_deletable = False

db_custom.before(db, Field, auth)

## create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=False)
auth.settings.create_user_groups = None  # ne skupiny user_{id}

if auth.user:
    if request.controller=='default' and request.function=='logout':
        pass       # propustit odhlášení
    elif not db.auth_user[auth.user.id]:   # databáze (nebo uživatel) byla smazána,
        redirect(URL('default', 'logout'))  # vynutit odhlášení
    else:
        admin_id = auth.id_group('admin')
        if not admin_id:
            # první uživatel po založení db, kterému se povedlo přihlásit
            admin_id = auth.add_group('admin', 'admin')  # vytvoří admina
            auth.add_membership(admin_id, auth.user.id)  # a dostane jeho práva
elif not (request.controller=='default' and request.function in ('login', 'register')):
    if request.env.request_method and not request.controller=='appadmin': # ne shell a appadmin
        redirect(URL('default', 'register')) # tam další redirect(login), máme-li už >0 uživatelů
is_admin = auth.has_membership('admin')

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
#from gluon.contrib.login_methods.rpx_account import use_janrain
#use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example

db_custom.after(db, Field, auth)

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
