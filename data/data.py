import json
from urllib2 import urlopen
import urllib2
from time import time,mktime,strptime, strftime
import schedule
import time
import requests
import unittest
import os

from apscheduler.schedulers.blocking import BlockingScheduler
from elasticsearch import Elasticsearch
import datetime
import sched
from datetime import datetime

import pickle

USERNAME = "sam"
PASSWORD = "616961127"
TOKEN_URL ="http://portal.cvst.ca/api/token/"

s = sched.scheduler(time.time, time.sleep)
url_border = "http://portal.cvst.ca/api/0.1/border"

url1 = 'http://portal.cvst.ca/api/0.1/HW_speed';
url2 = 'http://portal.cvst.ca/api/0.1/HW_speed/street_name';

full_loc_name_NE = []
full_loc_name_SW = []

location_id_list_SW = []
location_id_list_NE = []

NE_direction_data = []
ordered_NE_direction_data = []

#later will have more HW
highway_list = ["HWY-401 Express","HWY-401 Collectors"," HWY-407 Etr","HWY-404", "HWY-427", "QEW", "Gardiner Expy", "Don Valley Pky","HWY-400"]

##getting token
def authenticate():
    global token
    resp = requests.get(url = TOKEN_URL, auth = (USERNAME,PASSWORD))
    assert resp.ok, "Request Failed with error code %r" %resp.status_code
    token = resp.json()['token']
    #print(token)

##this is for highway speed
def data_retriving(url):
    #later use for authentication
    #response = urllib2.urlopen(url)
    #data = json.load(response)   
    #print data
    resp = requests.get(url=url)
    #print(resp.ok)
    #putting json data into a file
    if resp.ok is not True:
        delta_time = 1
        while resp.ok is not True:
            # exponentional backoff
            print('error '+str(resp.status_code)+'. Backing off for '+str(delta_time)+' seconds')
            delta_time = delta_time
            time.sleep(delta_time)
            authenticate()
            resp = requests.get(url=url, auth=(token,""))
    return resp

def insert_elasticsearch():
    es = Elasticsearch()
    doc = {
    'author': 'kimchy',
    'text': 'Elasticsearch: cool. bonsai cool.',
    'timestamp': datetime.now(),
    'id': 'abc',
    }
    #the id can be acquired from the search 

    res = es.index(index="test-index", doc_type='tweet', id=1, body=doc)
    print(res['created'])
    index = es.count(index="test-index", doc_type='tweet')
    new_index = index['count']
    print(index['count'])
    print(url)
    #document = data_retriving(url)

    with open('favs.json') as data_file:    
        data = json.load(data_file)
        #print data
    res = es.get(index="test-index", doc_type='tweet', id=1)
    print(res['_source'])

    es.indices.refresh(index="test-index")
    res = es.search(index="test-index", body={"query": {"match_all": {}}})
    print("Got %d Hits:" % res['hits']['total'])

#simple data retriving function for border
def get_borderDataONLY(url):
    #later use for authentication
    #NOTE: if border has authentication, then use the same 
    #data_retriving function as HW_speed
    response = urllib2.urlopen(url)
    data = json.load(response)   

##used for HW_speed
def get_allData():
    resp = data_retriving(url1)
    #print(resp.json())
    data = resp.json()
    #finding the length of our list of dictionaies
    length = len(data[0]["data"])
    #print(length)
    #print(data[0]["data"][0])
    return data

def get_locationInfo():
    resp = data_retriving(url2)
    locationInfo = resp.json()
    length = len(locationInfo[0]["data"])
    #print(length)
    #print(locationInfo[0]["data"][0])
    print("-------------------------------------------------")
    return locationInfo[0]["data"]

def get_valid_HW():
    resp = data_retriving(url1)
    data = resp.json()


class formatData():

    def get_NE_direction_id(self):
        count = 0
        all_location = get_locationInfo()
        #highway_list = ["HWY-401 Express","HWY-401 Collectors"]
        
        for a in all_location:
            if a["direction ('+':N/E,'-':S/W)"] == "+" and (a["main_road_name"] in highway_list):
                NE_direction_data.append({
                    "direction ('+':N/E,'-':S/W)": a["direction ('+':N/E,'-':S/W)"],
                    "main_road_name": a["main_road_name"], 
                    "ref_road_name": a["ref_road_name"], 
                    "location_name": a["main_road_name"] + '@' + a["ref_road_name"],
                    "location_ID": a["sensor_location_ID"]
                    })
                #print(NE_direction_data)
                full_loc_name_NE.append(a["main_road_name"] + '@' + a["ref_road_name"] + ' wtih ID = ' + str(a["sensor_location_ID"]))
       
        ## create the location list for NE direction
        ordered_NE_direction_data = sorted(NE_direction_data)
        #print(ordered_NE_direction_data)
        for b in ordered_NE_direction_data:
            location_id_list_NE.append(b["location_ID"])
        #print location_id_list_NE
        return location_id_list_NE


    def get_SW_direction_id(self):
        count = 0
        all_location = get_locationInfo()
        #highway_list = ["HWY-401 Express","HWY-401 Collectors"]
        SW_direction_data = []
        ordered_SW_direction_data = []
        
        for a in all_location:
            if a["direction ('+':N/E,'-':S/W)"] == "-" and (a["main_road_name"] in highway_list):
                SW_direction_data.append({
                    "direction ('+':N/E,'-':S/W)": a["direction ('+':N/E,'-':S/W)"],
                    "main_road_name": a["main_road_name"], 
                    "ref_road_name": a["ref_road_name"], 
                    "location_ID": a["sensor_location_ID"]
                    })
                #print(SW_direction_data)
                full_loc_name_SW.append(a["main_road_name"] + '@' + a["ref_road_name"] + ' wtih ID = ' + str(a["sensor_location_ID"]))

        ## create the location list for SW direction
        ordered_SW_direction_data = sorted(SW_direction_data)
        for b in ordered_SW_direction_data:
            location_id_list_SW.append(b["location_ID"])
        #print location_id_list_SW

        #print(full_loc_name)
        return location_id_list_SW

    # sort the list and output to a file
    def create_alphabetical_names(self, name_list):
        #this also remove duplicates if there is any
        alphabetical_names = sorted(set(name_list))
        thefile = open('total_ne.txt', 'w')
        for item in alphabetical_names:
            print>>thefile, item
        thefile.close()
        #print(alphabetical_names)
        return alphabetical_names

##since two directions have diff id, we can get second id from full location name
def find_id_from_neName(name):
    #print(NE_direction_data)
    for item in NE_direction_data:
        #print(fullname)
        if name == item["location_name"]:
            #(item["location_ID"])
            loc_id = item["location_ID"]
    return loc_id


def print_time(): 
    print "From print_time", time.time()

def top_10_busy(url):
    SW_direction_data = []
    highway_list = ["HWY-401 Express","HWY-401 Collectors"]

    resp = data_retriving(url)
    raw_data = resp.json()
    HW_data = raw_data[0]["data"]
    parser = formatData()
    list_of_SW_id = parser.get_SW_direction_id()
    result = []

    for a in HW_data:
        if (a["sensor_location_ID"] in list_of_SW_id) and (a["main_road_name"] in highway_list):
            SW_direction_data.append({
                "location_name": a["main_road_name"] + '@' + a["ref_road_name"], 
                "avg_uncapped_speed": a["avg_speed_uncapped"], 
                "location_ID": a["sensor_location_ID"],
                "timestamp": raw_data[0]["timestamp"],
                "direction": "SW"
                })
    #newlist = sorted(list_to_be_sorted, key=lambda k: k['name']) 
    sorted_SW = sorted(SW_direction_data, key=lambda k: k['avg_uncapped_speed'], reverse=True)
    for b in sorted_SW[:10]:
        result.append({
        "location":b["location_name"],
        "avge_speed":b["avg_uncapped_speed"]
        })
    return result

def main():
    parser = formatData()
   # get_allData()
    #get_locationInfo()
    es = Elasticsearch()
    #parser.get_NE_direction_id()
#    parser.get_SW_direction()
    #parser.create_alphabetical_names(full_loc_name_NE)


######## working scheduler##################
#    scheduler = BlockingScheduler()
#    print_time()
#    scheduler.add_job(print_time, 'interval', seconds=15)
    #print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

#    try:
#        scheduler.start()
#    except (KeyboardInterrupt, SystemExit):
#        pass
####################################################

if __name__ == '__main__':
    #print(1)

    #result = []
    #url = "http://portal.cvst.ca/api/0.1/HW_speed"
    #result = top_10_busy(url)

    #print(result[0]["location"])
    main()
    exit(0)