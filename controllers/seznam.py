# coding: utf8

from gluon.sqlhtml import ExporterCSV, ExporterXML

@auth.requires_login()
def listy():
    retval = {
        'caste_form': _caste('lista', 'lista_bv.lista_id', 'lista_id', db.lista_bv, db.barva_list, 'barva_list_id'),
        'akce_caste': 'barvy_list',
        }
    db.lista.id.readable = False
    db.lista_bv.id.readable = False
    db.lista_bv.cislo.readable = False
    retval.update(_grid(db.lista))  # grid později, protože _dopln_caste může obsahovat redirect po přidání nových častých barev
    return retval

@auth.requires_login()
def pasparty():
    retval = {
        'caste_form': _caste('pasparta', 'pasparta_bv.pasparta_id', 'pasparta_id', db.pasparta_bv, db.barva_paspart, 'barva_paspart_id'),
        'akce_caste': 'barvy_paspart',
        }
    db.pasparta.id.readable = False
    db.pasparta_bv.id.readable = False
    db.pasparta_bv.cislo.readable = False
    retval.update(_grid(db.pasparta))  # grid později, protože _dopln_caste může obsahovat redirect po přidání nových častých barev
    return retval

@auth.requires_login()
def listy_bv():
    return _vypis(db.lista_bv, db.lista_bv.lista_id)

@auth.requires_login()
def pasparty_bv():
    return _vypis(db.pasparta_bv, db.pasparta_bv.pasparta_id)

@auth.requires_login()
def rozmery():
    db.rozmer.id.readable = False
    db.pasparta_rozmer.id.readable = False
    return _grid(db.rozmer, linked_tables=['pasparta_rozmer'], add_empty_form=True)

@auth.requires_login()
def barvy_list():
    db.barva_list.id.readable = False
    return _grid(db.barva_list, add_empty_form=True)

@auth.requires_login()
def barvy_paspart():
    db.barva_paspart.id.readable = False
    return _grid(db.barva_paspart, add_empty_form=True)

@auth.requires_login()
def podklady():
    db.podklad.id.readable = False
    return _grid(db.podklad, add_empty_form=True)

@auth.requires_login()
def skla():
    db.sklo.id.readable = False
    return _grid(db.sklo, add_empty_form=True)

@auth.requires_login()
def blintramy():
    db.blintram.id.readable = False
    return _grid(db.blintram, add_empty_form=True)
    
@auth.requires_login()
def platna():
    db.platno.id.readable = False
    return _grid(db.platno, add_empty_form=True)

'''
@auth.requires_login()
def ks_pasp():
    return _grid(db.kspasp)
'''

@auth.requires_login()
def zaveseni():
    db.zaves.id.readable = False
    return _grid(db.zaves, add_empty_form=True)

@auth.requires_login()
def ks_doplnky():
    db.ksmat.id.readable = False
    return _grid(db.ksmat, add_empty_form=True)


def _grid(tbl, linked_tables=None, add_empty_form=False):
    response.view = 'seznam/seznam.html'
    render = dict(
          grid=SQLFORM.smartgrid(tbl,
              #fields = [item[1] for item in tbl.iteritems() if isinstance(item[1], Field) and not item[0] in ('_id', 'id')], 
              deletable=False,
              editable=auth.has_membership('admin'),
              create=auth.has_membership('admin'),
              csv=auth.has_membership('admin'),
              linked_tables=linked_tables,
              exportclasses=dict(html=False,csv_with_hidden_cols=False,
                                tsv=False,tsv_with_hidden_cols=False,),
              paginate=100,
              maxtextlength=30,
              showbuttontext=False,
              ),
              #fields=(db.auth_user.vs, ...),
              #orderby=db.auth_user.nick.lower(),
              #maxtextlengths={'auth_user.email' : 30}
          pocet_variant = False,
          )
    if len(request.args)==4 and request.args[1]=='edit':
        if request.args[0]=='lista' and request.args[2]=='lista':
            render['pocet_variant'] = db(
                  db.lista_bv.lista_id==int(request.args[3])).count()
        elif request.args[0]=='pasparta' and request.args[2]=='pasparta':
            render['pocet_variant'] = db(
                  db.pasparta_bv.pasparta_id==int(request.args[3])).count()

    if add_empty_form:
        render.update({'caste_form': None})
    return render

def _vypis(tbl, prvek):
    response.view = 'seznam/vypis.html'
    render = dict(
            grid=SQLFORM.grid(tbl,                                  
                fields=[tbl.skladem, tbl.cislo_sort, prvek, tbl.barva],
                deletable=False,
                editable=False,
                create=False,
                csv=auth.has_membership('admin'),
                exportclasses=dict(html=False,csv_with_hidden_cols=False,
                                  tsv=False,tsv_with_hidden_cols=False,),
                paginate=100,
                orderby=tbl.cislo_sort,
                showbuttontext=False,
                maxtextlength=60,
                ),
            )
    return render

def _caste(parent_name, foreign_key_full, foreign_key_fld, tbl_bv, tbl_caste, barva_id_fld):
    '''jen právě při zobrazení barevných variant jednoho typu lišty/pasparty
    přidá možnost přidat časté barvy pouhým zadáním výrobních čísel

    příklad parametrů: 'lista', 'lista_bv.lista_id', 'lista_id', db.lista_bv, db.barva_list, 'barva_list_id'
    příklad argumentů url: lista/lista_bv.lista_id/2 (a při přidání následuje: new)
    '''
    caste_form = None
    if len(request.args)==3 and request.args[0]==parent_name and request.args[1]==foreign_key_full:
        bv = db(tbl_bv[foreign_key_fld]==request.args[2]).select()
        bvmap = {}
        for bv1 in bv:
            bvmap[bv1.get(barva_id_fld)] = bv1.cislo
        caste = db(tbl_caste).select()
        radky = []
        for barva in caste:
            cislo = bvmap.get(barva.id)
            if not cislo:
                radky.append(TR(
                    TD(barva.barva),
                    TD(INPUT(_name='barva_%s'%barva.id, _class="nove_cislo"))
                    ))
        if radky:
            form_parts = [TABLE(*radky)]
            form_parts.append(INPUT(_type='submit'))
            caste_form = FORM(*form_parts, _id="add_bv")

            if caste_form.process().accepted:
                bv_all = db(tbl_bv).select(tbl_bv.cislo)
                cisla = [bv1.cislo for bv1 in bv_all]
                for var in caste_form.vars:
                    if var[:6]=='barva_':
                        barva_id = int(var[6:])
                        try:
                            nove_cislo = caste_form.vars['barva_%s'%barva_id].strip()
                        except ValueError:
                            nove_cislo = None
                        if nove_cislo and nove_cislo not in cisla:
                            kwargs = {foreign_key_fld: request.args[2],
                                  barva_id_fld: barva_id}
                            barva = db(tbl_caste.id==barva_id).select().first().barva
                            tbl_bv.insert(
                                  cislo=nove_cislo,
                                  barva=barva,
                                  **kwargs
                                  )
                            cisla.append(nove_cislo)
                redirect(URL(args=request.args, user_signature=True))
    return caste_form
