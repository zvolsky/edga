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
def sady_barev():
    return _grid(db.sada_barev, linked_tables=['barva'])

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

def _grid(tbl, linked_tables=None):
    from gluon.sqlhtml import ExporterCSV, ExporterXML 
    return dict(grid=SQLFORM.smartgrid(tbl,
              deletable=False,
              editable=auth.has_membership('admin'),
              create=auth.has_membership('admin'),
              csv=auth.has_membership('admin'),
              linked_tables=linked_tables,
              exportclasses=dict(html=False,csv_with_hidden_cols=False,
                                tsv=False,tsv_with_hidden_cols=False,),
              paginate=100,
              ))
              #fields=(db.auth_user.vs, ...),
              #orderby=db.auth_user.nick.lower(),
              #maxtextlengths={'auth_user.email' : 30}
