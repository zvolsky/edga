# coding: utf8

def browser():
    import httpagentparser
    agent = request.env.http_user_agent
    return BEAUTIFY(httpagentparser.simple_detect(agent))
def browser2():
    import httpagentparser
    agent = request.env.http_user_agent
    return BEAUTIFY(httpagentparser.detect(agent))

@auth.requires_membership('admin')
def listy_unique():
    root = [0]
    smazano = 0
    predchozi = []
    for lista in db().select(db.lista.ALL):
        if [lista.vyrobce, lista.typ, lista.cena, lista.tovarni, lista.sirka]==predchozi:
            root[1] = max(root[1], lista.nakupni)
            del db.lista[lista.id]
            smazano += 1
        else:
            if root[0]:
                db.lista[root[0]] = {'nakupni': root[1]}
            predchozi = [lista.vyrobce, lista.typ, lista.cena, lista.tovarni, lista.sirka]
            root = [lista.id, lista.nakupni]
        db.lista_bv.insert(barva=lista.nazev or lista.barva, cislo=lista.cislo, lista_id=root[0])
    return 'smazano : %s' % smazano