# coding: utf8

def edit():
    if not request.args(0):    # chybné volání
        redirect(URL('default', 'index'))
    form = SQLFORM(db.poptavajici, request.args(0)).process(
        next=URL('poptavka', 'hlavicka_edit', args=request.args(1))
            if request.args(1) else
            URL('poptavky', 'otevrene')
            )
    return dict(form=form)    
