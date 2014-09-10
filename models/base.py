# -*- coding: utf-8 -*-

def script(soubor, pripona="js"):
    return SCRIPT(_src="%s" % (URL('static','js/%s.%s' % (soubor, pripona))))
