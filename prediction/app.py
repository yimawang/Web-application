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
    'server.socket_port' : 8080,
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
  '/prediction.html':
  { 'tools.staticfile.on':True,
    'tools.staticfile.filename':os.path.join(os.path.dirname(os.path.abspath(__file__)), 'prediction.html')
  },
  '/top10.js':
  { 'tools.staticfile.on':True,
    'tools.staticfile.filename':os.path.join(os.path.dirname(os.path.abspath(__file__)), 'top10.js')
  }
}

class App:

  @cherrypy.expose
  def index(self):
    return serve_file(os.path.join(path, 'prediction.html'))

  @cherrypy.expose
  @cherrypy.tools.json_out()
  def getData(self,date="123",hour="25", loc_id ="1", ne_id = "1"):
    no_dash = ""
    for c in date:
        if c == "-":
            continue
        no_dash += c

    weekdays=['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    weekday=weekdays[datetime.datetime.strptime(no_dash, "%Y%m%d").weekday()]

    one = int(hour) + 1
    if one >= 24:
      one = one - 24
      weekday=weekdays[datetime.datetime.strptime(str(int(no_dash)+1), "%Y%m%d").weekday()]
    hour_one = "%02d" % (one, )

    two = int(hour_one) + 1
    if two >= 24:
      two = two - 24
      weekday=weekdays[datetime.datetime.strptime(str(int(no_dash)+1), "%Y%m%d").weekday()]
    hour_two = "%02d" % (two, )

    three = int(hour_two) + 1
    if three >= 24:
      three = three - 24
      weekday=weekdays[datetime.datetime.strptime(str(int(no_dash)+1), "%Y%m%d").weekday()]
    hour_three = "%02d" % (three, )

    four = int(hour_three) + 1
    if four >= 24:
      four = four - 24
      weekday=weekdays[datetime.datetime.strptime(str(int(no_dash)+1), "%Y%m%d").weekday()]
    hour_four = "%02d" % (four, )

    five = int(hour_four) + 1
    if five >= 24:
      five = five - 24
      weekday=weekdays[datetime.datetime.strptime(str(int(no_dash)+1), "%Y%m%d").weekday()]
    hour_five = "%02d" % (five, )

    six = int(hour_five) + 1
    if six >= 24:
      six = six - 24
      weekday=weekdays[datetime.datetime.strptime(str(int(no_dash)+1), "%Y%m%d").weekday()]
    hour_six = "%02d" % (six, )

    seven = int(hour_six) + 1
    if seven >= 24:
      seven = seven - 24
      weekday=weekdays[datetime.datetime.strptime(str(int(no_dash)+1), "%Y%m%d").weekday()]
    hour_seven = "%02d" % (seven, )

    ca=holidays.Canada()
    if date in ca:
        weekday = 'Hol'

    #"-" is NE direction
    speed=es_search.movavg(weekday+hour,loc_id, "-")
    speed_one = es_search.movavg(weekday+hour_one,loc_id, "-")
    speed_two = es_search.movavg(weekday+hour_two,loc_id, "-")
    speed_three = es_search.movavg(weekday+hour_three,loc_id, "-")
    speed_four = es_search.movavg(weekday+hour_four,loc_id, "-")
    speed_five = es_search.movavg(weekday+hour_five,loc_id, "-")
    speed_six = es_search.movavg(weekday+hour_six,loc_id, "-")
    speed_seven = es_search.movavg(weekday+hour_seven,loc_id, "-")
    

    #weekdays1=['mon','tue','wed','thu','fri','sat','sun']
    #weekday1=weekdays1[datetime.datetime.strptime(no_dash, "%Y%m%d").weekday()]
    #print(weekday1)
    #if date in ca:
    #    weekday1 = 'hol'
    speed_ne=es_search.movavg_ne(weekday+hour,ne_id, "+")
    speed_ne1=es_search.movavg_ne(weekday+hour_one,ne_id, "+")
    speed_ne2=es_search.movavg_ne(weekday+hour_two,ne_id, "+")
    speed_ne3=es_search.movavg_ne(weekday+hour_three,ne_id, "+")
    speed_ne4=es_search.movavg_ne(weekday+hour_four,ne_id, "+")
    speed_ne5=es_search.movavg_ne(weekday+hour_five,ne_id, "+")
    speed_ne6=es_search.movavg_ne(weekday+hour_six,ne_id, "+")
    speed_ne7=es_search.movavg_ne(weekday+hour_seven,ne_id, "+")
    #print(speed_ne)
    #result = []
    #result = es_sort.highest10("-")
    print(type(speed))
    return {
      'foo' : speed+ ' km/h',
      'foo_one' : speed_one + ' km/h',
      'foo_two' : speed_two + ' km/h',
      'foo_three' : speed_three + ' km/h',
      'foo_four' : speed_four + ' km/h',
      'foo_five' : speed_five + ' km/h',
      'foo_six' : speed_six + ' km/h',
      'foo_seven' : speed_seven + ' km/h',

#      'speed_ne' : speed_ne_ + ' km/h',

      'hour' : hour+ ':00',
      'hour_one' : hour_one + ':00',
      'hour_two' : hour_two + ':00',
      'hour_three' : hour_three + ':00',
      'hour_four' : hour_four + ':00',
      'hour_five' : hour_five + ':00',
      'hour_six' : hour_six + ':00',
      'hour_seven' : hour_seven + ':00',

      #'loc1': result[0]["location"],
      'speed_ne' : speed_ne + ' km/h',
      'speed_ne1' : speed_ne1 + ' km/h',
      'speed_ne2' : speed_ne2 + ' km/h',
      'speed_ne3' : speed_ne3 + ' km/h',
      'speed_ne4' : speed_ne4 + ' km/h',
      'speed_ne5' : speed_ne5 + ' km/h',
      'speed_ne6' : speed_ne6 + ' km/h',
      'speed_ne7' : speed_ne7 + ' km/h',
    }


if __name__ == '__main__':
  from cherrypy.process.plugins import Daemonizer
  d = Daemonizer(cherrypy.engine)
  d.subscribe()
  cherrypy.quickstart(App(), '/', config)
