# coding: utf8

@auth.requires_login()
def lista():
    bv = db(db.lista_bv.lista_id==request.args[0]).select()
    form = __handleform(bv, db.lista_bv, 'lista_id')
    return dict(
        bv=bv,
        lista=db.lista[request.args[0]],
        form=form,
        info=__getinfo() 
        )

@auth.requires_login()
def pasparta():
    bv = db(db.pasparta_bv.pasparta_id==request.args[0]).select()
    form = __handleform(bv, db.pasparta_bv, 'pasparta_id')
    return dict(
        bv=bv,
        pasparta=db.pasparta[request.args[0]],
        form=form, 
        info=__getinfo() 
        )

def __getinfo():
    return ("Zadej evidenční čísla pro ty barvy, které chceš přidat do sortimentu."
        ' ' "Duplicitní číslo přidáno nebude.")
    
def __handleform(bv, bv_table, foreign_key):
    form = __getform(bv)
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
                        kwargs = {foreign_key: request.args[0]}
                        bv_table.insert(
                              cislo=nove_cislo,
                              barva_id=barva_id,
                              **kwargs
                              )
                        cisla.append(nove_cislo)
        db.commit()
        redirect(URL(args=request.args[0]))
    return form

def __getform(bv):
    bvmap = {}
    for bv1 in bv:
        bvmap[bv1.barva_id] = bv1.cislo
    barvy = db(db.barva).select()
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
