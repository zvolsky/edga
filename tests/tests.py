# coding: utf8

import os
from selenium import webdriver

# nastavení
br_all = False             # testuj ve všech browserech?
br_prefered = ('Chrome',)  # jinak jen v preferovaných

testpwd = 'testpwd'

# ostatní inicializace
br = None

def testAll():
    for wd_browser in (('Firefox', 'Chrome', 'Ie') if br_all else br_prefered):
        yield view_pages, wd_browser
        #yield nextcheck, wd_browser

def view_pages(wd_browser):
    global br
    br = getbrowser(wd_browser)
    login('http://localhost:8000/edga')
    
    assert not pages('rp_sirka',
              ('http://localhost:8000/edga/poptavka/nova',
              'http://localhost:8000/edga/poptavka/edit',
              ))
    assert not pages('main',
              ('http://localhost:8000/edga/seznam/listy',
              'http://localhost:8000/edga/seznam/pasparty',
              'http://localhost:8000/edga/seznam/podklady',
              'http://localhost:8000/edga/seznam/skla',
              'http://localhost:8000/edga/seznam/ks_doplnky',
              ))

    br.quit()

def getbrowser(wd_browser):
    return getattr(webdriver, wd_browser)()

def login(main_page):
    br.get(main_page)
    if br.current_url[-6:]==u'/login':
        assert br.find_element_by_id('auth_user_username') 
        assert br.find_element_by_id('auth_user_password')
        br.find_element_by_id('auth_user_username').send_keys('zvolsky')  
        br.find_element_by_id('auth_user_password').send_keys(
            os.getenv(testpwd))  
        br.find_element_by_xpath('//form//input[@type="submit"]').click()
    assert not (br.current_url[-6:]==u'/login'
            or br.current_url[-7:]==u'/login#')

def pages(required_id, urls):
    for url in urls:
        br.get(url)
        assert br.find_element_by_id(required_id)
