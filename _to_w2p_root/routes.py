#!/usr/bin/python
# -*- coding: utf-8 -*-

default_application = 'edga'    # ordinarily set in base routes.py
default_controller = 'default'  # ordinarily set in app-specific routes.py
default_function = 'index'      # ordinarily set in app-specific routes.py

routes_in = (
  ('/$anything', '/edga/$anything'),
  ('*./favicon.ico', '/edga/static/images/favicon.ico'),
  ('*./favicon.png', '/edga/static/images/favicon.png'),
  ('*./robots.txt', '/edga/static/robots.txt'),
  )

routes_out = [(x, y) for (y, x) in routes_in[:-3]]
