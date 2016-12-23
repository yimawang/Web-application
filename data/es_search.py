from elasticsearch import Elasticsearch
from data import formatData
from data import find_id_from_neName

def movavg(hour_here,loc_id,direction):
    client = Elasticsearch()

    response = client.search(
        index="highway_sw",
        body= {
         "aggs": {
            "filter0": {
               "filter": {
                  "term": {
                     "location_id": loc_id
                  }
               },
               "aggs": {
                  "filter_first_yo": {
                     "filter": {
                        "term": {
                           "hour": hour_here
                        }
                     },
                     "aggs": {
                        "set_hour_avg": {
                           "date_histogram": {
                              "field": "timestamp",
                              "interval": "week"
                           },
                           "aggs": {
                              "hourly_sum": {
                                 "avg": {
                                    "field": "uncapped_speed"
                                 }
                              },
                              "the_movavg": {
                                 "moving_avg": {
                                    "buckets_path": "hourly_sum",
                                    "window": 14,
                                    "model": "ewma",
                                    "settings": {
                                       "alpha": 0.5
                                    }
                                 }
                              }
                           }
                        }
                     }
                  }
               }
            }
         }
      }
    )
    #print(response['aggregations']['filter_first_yo']['set_hour_avg']['buckets'])
    for tag in response['aggregations']['filter0']['filter_first_yo']['set_hour_avg']['buckets']:
        if 'the_movavg' in tag:
            ma_value = float(tag['the_movavg']['value'])*1.609344
            #print(tag['the_movavg'])


    #print(type(ma_value))
    #print("{0:.2f}".format(ma_value))
    return "{0:.2f}".format(ma_value)




def movavg_ne(hour_here,loc_id,direction):
    client = Elasticsearch()
    #parser = formatData()
    #parser.get_NE_direction_id()
    #print(loc_name)
    #print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    #loc_id = find_id_from_neName(loc_name)
    #print(loc_id)
    response = client.search(
        index="highway_ne",
        body= {
         "aggs": {
            "filter0": {
               "filter": {
                  "term": {
                     "location_id": loc_id
                  }
               },
               "aggs": {
                  "filter_first_yo": {
                     "filter": {
                        "term": {
                           "hour": hour_here
                        }
                     },
                     "aggs": {
                        "set_hour_avg": {
                           "date_histogram": {
                              "field": "timestamp",
                              "interval": "week"
                           },
                           "aggs": {
                              "hourly_sum": {
                                 "avg": {
                                    "field": "uncapped_speed"
                                 }
                              },
                              "the_movavg": {
                                 "moving_avg": {
                                    "buckets_path": "hourly_sum",
                                    "window": 14,
                                    "model": "ewma",
                                    "settings": {
                                       "alpha": 0.5
                                    }
                                 }
                              }
                           }
                        }
                     }
                  }
               }
            }
         }
      }
    )
    #print(response['aggregations']['filter_first_yo']['set_hour_avg']['buckets'])
    for tag in response['aggregations']['filter0']['filter_first_yo']['set_hour_avg']['buckets']:
        if 'the_movavg' in tag:
            ma_value = float(tag['the_movavg']['value'])*1.609344
            #print(tag['the_movavg'])


    #print(type(ma_value))
    #print("{0:.2f}".format(ma_value))
    return "{0:.2f}".format(ma_value)

if __name__ == '__main__':
    #doit=movavg_ne("Wed00","HWY-401 Collectors@Allen Road/Exit 365", '+')
    exit(0)
