# coding: utf8

@auth.requires_login()
def lista():
    bv = db(db.lista_bv.lista_id==request.args[0]).select()
    form = __handleform(bv, db.lista_bv, db.barva_list, 'lista_id',
            'barva_list_id')
    return dict(
        bv=bv,
        lista=db.lista[request.args[0]],
        form=form,
        info=__getinfo() 
        )

@auth.requires_login()
def pasparta():
    bv = db(db.pasparta_bv.pasparta_id==request.args[0]).select()
    form = __handleform(bv, db.pasparta_bv, db.barva_paspart, 'pasparta_id',
            'barva_paspart_id')
    return dict(
        bv=bv,
        pasparta=db.pasparta[request.args[0]],
        form=form, 
        info=__getinfo() 
        )

def __getinfo():
    return ("Zadej evidenční čísla pro ty barvy, které chceš přidat do sortimentu."
        ' ' "Duplicitní číslo přidáno nebude.")
    
def __handleform(bv, bv_table, barvy_table, foreign_key, barva_id_fld):
    form = __getform(bv, barvy_table, barva_id_fld)
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
        db.commit()
        redirect(URL(args=request.args[0]))
    return form

def __getform(bv, barvy_table, barva_id_fld):
    bvmap = {}
    for bv1 in bv:
        bvmap[bv1.get(barva_id_fld)] = bv1.cislo
    barvy = db(barvy_table).select()
    radky = []
    for barva in barvy:
        cislo = bvmap.get(barva.id) 
        radky.append((
              TD(barva.barva),
              TD(cislo or INPUT(_name='barva_%s'%barva.id, _class="nove_cislo"))
              ))
    form_parts = [TABLE(*radky)]
    form_parts.append(INPUT(_type='submit'))
    return FORM(*form_parts, _id="add_bv")
