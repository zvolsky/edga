# coding: utf8

@auth.requires_login()
def lista():
    bv = db(db.lista_bv.lista_id==request.args[0]).select(orderby=db.lista_bv.cislo_sort)
    form, volne = __handleform(bv, db.lista_bv, db.barva_list, 'lista_id', 'barva_list_id')
    info_vzdy, zpet = __getvzdy('listy', 'lista', request.args[0], kterych_prvku="lišt")
    return dict(
        bv = bv,
        volne = volne,
        lista = db.lista[request.args[0]],
        form = form,
        info_volne = __getinfo_volne(),
        info_vzdy = info_vzdy,
        zpet = zpet,
        )

@auth.requires_login()
def pasparta():
    bv = db(db.pasparta_bv.pasparta_id==request.args[0]).select(orderby=db.pasparta_bv.cislo_sort)
    form, volne = __handleform(bv, db.pasparta_bv, db.barva_paspart, 'pasparta_id', 'barva_paspart_id')
    info_vzdy, zpet = __getvzdy('pasparty', 'pasparta', request.args[0], kterych_prvku="paspart")
    return dict(
        bv = bv,
        volne = volne,
        pasparta = db.pasparta[request.args[0]],
        form = form, 
        info_volne = __getinfo_volne(),
        info_vzdy = info_vzdy,
        zpet = zpet,
        )

def __getinfo_volne():
    return P(EM("Zde lze rychle doplnit barevné varianty pro časté barvy.", BR(),
        "Jednoduše zadej evidenční číslo ke každé barvě, kterou chceš přidat. (Duplicitní číslo ale přidáno nebude.)"))

def __getvzdy(akce, tbl, typ_id, kterych_prvku):
    zpet_na_typ = URL('seznam', akce, args=(tbl, '%s_bv.%s_id' % (tbl, tbl), typ_id))
    return P(EM(
        "Pro novou, nezobrazenou barvu, je potřeba se rozhodnout,",
        UL(
        LI("zda takovou barvu mají často i jiné typy %s. V tom případě si ji trvale" % kterych_prvku, ' ',
            A("doplň do seznamu častých barev", _href=URL('seznam', 'barvy_list' if tbl=='lista' else 'barvy_paspart')), '. ',
            "Taková barva se bude nadále nabízet u všech %s." % kterych_prvku),
        LI("zda je to nepříliš častá barva a", ' ',
            A("přidáš ji jen k tomuto prvku", _href=zpet_na_typ), '.'),
            ),
            )),\
        P(
            A("Zpět na seznam %s" % kterych_prvku, _href=URL('seznam', akce)), ' -- ',
            A("Zpět na tento typ", _href=zpet_na_typ),
        )

def __handleform(bv, bv_table, barvy_table, foreign_key, barva_id_fld):
    form, volne = __getform(bv, barvy_table, barva_id_fld)
    if form.process().accepted:
        bv_all = db(bv_table).select(bv_table.cislo)
        cisla = [int(bv1.cislo) for bv1 in bv_all]
        for var in form.vars:
            if var[:6]=='barva_':
                barva_id = int(var[6:])
                try:
                    nove_cislo = int(form.vars['barva_%s'%barva_id])
                except ValueError:
                    nove_cislo = None
                if nove_cislo:
                    if nove_cislo in cisla:
                        pass
                    else:
                        kwargs = {foreign_key: request.args[0],
                              barva_id_fld: barva_id}
                        barva = db(barvy_table.id==barva_id).select().first().barva
                        bv_table.insert(
                              cislo=nove_cislo,
                              barva=barva,
                              **kwargs
                              )
                        cisla.append(nove_cislo)
        #db.commit()
        redirect(URL(args=request.args[0]))
    return form, volne

def __getform(bv, barvy_table, barva_id_fld):
    bvmap = {}
    for bv1 in bv:
        bvmap[bv1.get(barva_id_fld)] = bv1.cislo
    caste = db(barvy_table).select()
    volne = False
    radky = []
    for barva in caste:
        cislo = bvmap.get(barva.id)
        if not cislo:
            radky.append(TR(
                TD(barva.barva),
                TD(INPUT(_name='barva_%s'%barva.id, _class="nove_cislo"))
                ))
            volne = True
    form_parts = [TABLE(*radky)]
    form_parts.append(INPUT(_type='submit'))
    return FORM(*form_parts, _id="add_bv"), volne
