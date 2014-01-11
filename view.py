# -*- coding: utf-8 -*-

import web
import db
import config
from mako.template import Template
from mako.lookup import TemplateLookup

#Carga de las plantillas Mako
mylookup = TemplateLookup(directories=['./view'],module_directory='/tmp/mako_modules',
	output_encoding='utf-8',input_encoding='utf-8',encoding_errors='replace', collection_size=500)
def serve_template(templatename, **kwargs):
    mytemplate = mylookup.get_template(templatename)
    return mytemplate.render(**kwargs)

t_globals = dict(
  datestr=web.datestr,
)

def listing(**k):
    l = db.listing(**k)
    return render.listing(l)