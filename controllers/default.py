# -*- coding: utf-8 -*-

def index():
    return dict()

def login():
    return dict(form=auth.login())

def logout():
    return dict(form=auth.logout())

#def profile():
#    return dict(form=auth.profile())
    
def register():
    uzivatelu = db(db.auth_user).count()
    if uzivatelu:     # další uživatelé se nikdy neregistrují, přidávají se přes správu uživatelů
        redirect(URL('login'))
    # jsme v kontoléru formuláře, toto tedy běží 2 a vícekrát (při vystavení, neúspěš.validaci, uložení),
    #  ale vystavení může být i mnohokrát, když se nezaregistruje - init_db() ošetřit proti opakování!
    from edga import init_db            # inicializuje hodnoty do databáze
    init_db(db)
    auth.settings.login_after_registration = True
    return dict(form=auth.register())   # registrace prvního uživatele

def change_password():
    return dict(form=auth.change_password())

def not_authorized():
    return dict(form=auth.not_authorized())

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in 
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    if request.args(0)=='not_authorized':
        return dict(form=auth())
    else:
        redirect(URL('index'))

@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
