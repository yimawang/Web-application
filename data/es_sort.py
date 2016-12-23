from elasticsearch import Elasticsearch
import time

def highest10(direction, timeFrom, timeTo):
    client = Elasticsearch()
    result = []
    #get the newest id index
    if direction == "sw":
        direction_index = "highway_sw"
        loc_id = 0.96717
    else: 
        direction_index = "highway_ne"
        loc_id = 1.1709
    searched = client.search(index=direction_index, body={"query": {"bool": {"should":{"term": {"location_id":loc_id }}}},"size": 1,"sort": [{"timestamp": {"order": "desc"}}]})
    #index=int(searched['hits']['hits'][0]['_id'])-5

    #in milliseconds
    #timestamp_now = int(time.time())*1000
    #timestamp_previous = timestamp_now - 600000
    time1 = int(timeFrom) - 300000
    time2 = int(timeTo) + 300000

    response = client.search(
        index=direction_index,
        body= {
            "filter" : {
                "range" : {
                    "timestamp" : {
                        "gte" : time1,
                        "lte"  : time2
                    }
                }
            },
            "sort" : [
            { 
                "uncapped_speed": {"order": "desc"}
            }
          ]
        }
    )
    
    #print(response['hits']['hits'])
    if not response['hits']['hits']:
        for i in range(0,10):
            result.append({ 
                "avg_speed" : '0 km/h',
                "location" : 'Unknown'
            })
    else:
        for i in range(0,10):
            result.append({ 
                "avg_speed" : str("{0:.2f}".format(response['hits']['hits'][i]['_source']['uncapped_speed']*1.609344)) + ' km/h',
                "location" : response['hits']['hits'][i]['_source']['location_name']
            })
    #print(result)

    #print(type(ma_value))
    #print("{0:.2f}".format(ma_value))
    return result

if __name__ == '__main__':
      doit=highest10('-')
