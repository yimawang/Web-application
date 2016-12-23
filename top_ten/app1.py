#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import cherrypy
from cherrypy.lib.static import serve_file

import datetime
import holidays

import sys 
sys.path.insert(0, '/home/ubuntu/data')
import es_search
from data import find_id_from_neName
from data import top_10_busy
import es_sort


path   = os.path.abspath(os.path.dirname(__file__))
config = {
  'global' : {
    'server.socket_host' : '0.0.0.0',
    'server.socket_port' : 8081,
    'server.thread_pool' : 16,
    'tools.staticdir.root': os.path.dirname(os.path.abspath(__file__))
  },
  '/css':
  {
    'tools.staticdir.on': True,
    'tools.staticdir.dir': os.path.join(os.path.dirname(__file__), 'css'),
  },
  '/style.css':
  { 'tools.staticfile.on':True,
    'tools.staticfile.filename':os.path.join(os.path.dirname(os.path.abspath(__file__)), 'style.css')
  },
  '/top_ten.html':
  { 'tools.staticfile.on':True,
    'tools.staticfile.filename':os.path.join(os.path.dirname(os.path.abspath(__file__)), 'top_ten.html')
  },
  '/top10.js':
  { 'tools.staticfile.on':True,
    'tools.staticfile.filename':os.path.join(os.path.dirname(os.path.abspath(__file__)), 'top10.js')
  }
}

class App:

  @cherrypy.expose
  def index(self):
    return serve_file(os.path.join(path, 'top_ten.html'))

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def getTopTen(self, timeFrom="1",timeTo="2", direction ="1"):
    #getting current top 10 busy location
    result = []
    result_ne = []
    result = es_sort.highest10("sw", timeFrom, timeTo)
    result_ne = es_sort.highest10("ne", timeFrom, timeTo)
    #'loc1': result[0]["location"]
    #value = result[0]["location"]
    return {
      'result': result,
      'result_ne': result_ne,
    }

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def getPast(self):
    return{

    }

if __name__ == '__main__':
  from cherrypy.process.plugins import Daemonizer
  d = Daemonizer(cherrypy.engine)
  d.subscribe()
  cherrypy.quickstart(App(), '/', config)
