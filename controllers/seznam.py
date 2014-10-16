# coding: utf8

@auth.requires_login()
def listy():
    return _grid(db.lista)

@auth.requires_login()
def pasparty():
    return _grid(db.pasparta)

@auth.requires_login()
def rozmery():
    return _grid(db.rozmer, linked_tables=['pasparta_rozmer'])

@auth.requires_login()
def barvy_list():
    return _grid(db.barva_list)

@auth.requires_login()
def barvy_paspart():
    return _grid(db.barva_paspart)

@auth.requires_login()
def podklady():
    return _grid(db.podklad)
    
@auth.requires_login()
def skla():
    return _grid(db.sklo)
    
@auth.requires_login()
def blintramy():
    return _grid(db.blintram)
    
@auth.requires_login()
def platna():
    return _grid(db.platno)

'''
@auth.requires_login()
def ks_pasp():
    return _grid(db.kspasp)
'''

@auth.requires_login()
def zaveseni():
    return _grid(db.zaves)

@auth.requires_login()
def ks_doplnky():
    return _grid(db.ksmat)

def _grid(tbl, linked_tables=None):
    response.view = 'seznam/seznam.html'
    from gluon.sqlhtml import ExporterCSV, ExporterXML
    render = dict(grid=SQLFORM.smartgrid(tbl,
              #fields = [eval('db.%s.%s' % (tbl._tablename, f)) for f in tbl._fields][1:],
              deletable=False,
              editable=auth.has_membership('admin'),
              create=auth.has_membership('admin'),
              csv=auth.has_membership('admin'),
              linked_tables=linked_tables,
              exportclasses=dict(html=False,csv_with_hidden_cols=False,
                                tsv=False,tsv_with_hidden_cols=False,),
              paginate=100,
              ),
              #fields=(db.auth_user.vs, ...),
              #orderby=db.auth_user.nick.lower(),
              #maxtextlengths={'auth_user.email' : 30}
              pocet_variant = False)
    if len(request.args)==4 and request.args[1]=='edit':
        if request.args[0]=='lista' and request.args[2]=='lista':
            render['pocet_variant'] = db(
                  db.lista_bv.lista_id==int(request.args[3])).count()
        elif request.args[0]=='pasparta' and request.args[2]=='pasparta':
            render['pocet_variant'] = db(
                  db.pasparta_bv.pasparta_id==int(request.args[3])).count()
    return render