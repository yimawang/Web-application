import holidays
import data 
import datetime
from data import data_retriving
from data import formatData

from elasticsearch import Elasticsearch
import datetime
import time

list_of_NE_id = []
list_of_SW_id = []

index = 0

def get_NE_data(url):
	resp = data_retriving(url)
	raw_data = resp.json()

	HW_data = raw_data[0]["data"]
	ca_holidays = holidays.Canada()

	highway_list = ["HWY-401 Express","HWY-401 Collectors"," HWY-407 Etr","HWY-404", "HWY-427", "QEW", "Gardiner Expy", "Don Valley Pky","HWY-400"]
	
	list_of_NE_id = [0.04214, 0.11947, 0.24033, 0.25462, 0.2692, 0.29286, 0.29333, 0.32613, 0.3366, 0.35391, 0.37027, 0.37538, 0.38728, 0.39482, 0.4028, 0.45234, 0.45414, 0.46537, 0.47681, 0.48186, 0.48202, 0.5291, 0.54835, 0.5503, 0.55438, 0.57247, 0.58036, 0.59942, 0.61795, 0.63905, 0.64071, 0.66999, 0.67059, 0.68821, 0.68888, 0.70454, 0.70827, 0.72451, 0.73241, 0.73859, 0.79105, 0.80008, 0.81212, 0.82364, 0.83072, 0.83211, 0.83218, 0.83218, 0.83296, 0.84449, 0.85259, 0.86824, 0.88199, 0.88791, 0.90311, 0.90619, 0.9117, 0.91469, 0.9196, 0.92247, 0.92622, 0.9263, 0.95116, 0.95487, 0.95892, 0.96717, 0.96717, 0.97455, 0.97891, 0.98513, 0.99111, 1.00087, 1.0121, 1.01376, 1.03736, 1.04851, 1.05016, 1.05548, 1.06029, 1.07234, 1.08435, 1.10302, 1.12735, 1.19169, 1.19569, 1.21382, 1.22413, 1.22654, 1.23478, 1.23525, 1.23879, 1.26175, 1.27064, 1.27455, 1.2847, 1.28672, 1.28931, 1.29862, 1.30271, 1.32559, 1.33443, 1.33999, 1.34022, 1.34022, 1.34454, 1.34907, 1.3691, 1.37458, 1.385, 1.40316, 1.42031, 1.42748, 1.45801, 1.46279, 1.46679, 1.46744, 1.46983, 1.46983, 1.54029, 1.54405, 1.59703, 1.63465, 1.65197, 1.67345, 1.71843, 1.733, 1.82976, 1.82976, 1.89295, 1.94644, 2.01923, 2.26437, 2.55565, 2.60908, 2.78309, 3.76202, 3.85968, 3.9684, 5.30822]
	#parser = formatData()
	#list_of_NE_id = parser.get_NE_direction_id()
	#print (list_of_NE_id)

	NE_direction_data = []
	#ordered_NE_direction_data = []

	#print(raw_data[0]["timestamp"])

	#check holliday and convert to Mon00 format
	date_string= datetime.datetime.fromtimestamp(int(raw_data[0]["timestamp"])).strftime('%A')
	day = date_string[0:3]
	hour = datetime.datetime.fromtimestamp(int(raw_data[0]["timestamp"])).strftime('%H')
	if (int(raw_data[0]["timestamp"])) in ca_holidays:
		day_hour = "Hol" +hour
	else:
		day_hour =  day + hour
	#print (day_hour)
	#d = "Hol" +hour
	#print (d)


	for a in HW_data:
		if (a["sensor_location_ID"] in list_of_NE_id) and (a["main_road_name"] in highway_list):
			NE_direction_data.append({
				"location_name": a["main_road_name"] + '@' + a["ref_road_name"], 
            	"uncapped_speed": a["avg_speed_uncapped"],    
            	"location_ID": a["sensor_location_ID"],
            	"timestamp": raw_data[0]["timestamp"],
            	"hour": day_hour,
				"direction": "NE"
            	})

    #print(NE_direction_data)
	## create the location list for NE direction
	#ordered_NE_direction_data = sorted(NE_direction_data)
	#print(ordered_NE_direction_data)

	##insert elasticsearch
	for b in NE_direction_data:
		if b["uncapped_speed"] == "NULL":
			#print("found!!!!!!!!!!!!!!!!!!!")
			#print(b["location_ID"])
			#print(b["timestamp"])
			b["uncapped_speed"] = "60.0001"
		#print(b["location_ID"])
		doc = {
			"location_name": str(b["location_name"]), 
			"uncapped_speed": float(b["uncapped_speed"]),
			"location_id": str(b["location_ID"]),
			"timestamp": b["timestamp"]*1000,
			"hour": str(b["hour"]),
	 		"direction": str(b["direction"])
		}
		insert_elasticsearch(doc)

	return NE_direction_data

def get_SW_data(url):
	resp = data_retriving(url)
	raw_data = resp.json()

	HW_data = raw_data[0]["data"]
	ca_holidays = holidays.Canada()

	highway_list = ["HWY-401 Express","HWY-401 Collectors"," HWY-407 Etr","HWY-404", "HWY-427", "QEW", "Gardiner Expy", "Don Valley Pky","HWY-400"]
	#parser = formatData()
	list_of_SW_id = [0.01308, 0.10924, 0.12855, 0.20785, 0.22805, 0.28442, 0.30675, 0.31229, 0.31433, 0.34143, 0.34896, 0.3588, 0.36296, 0.3737, 0.41098, 0.41776, 0.41776, 0.42642, 0.43479, 0.45464, 0.48621, 0.49675, 0.50391, 0.53617, 0.54539, 0.55767, 0.56606, 0.5788, 0.58192, 0.58389, 0.60035, 0.63276, 0.66536, 0.67913, 0.68054, 0.68847, 0.70182, 0.7126, 0.71387, 0.7303, 0.75949, 0.77108, 0.78187, 0.78324, 0.78888, 0.79767, 0.79795, 0.80995, 0.82872, 0.83326, 0.84422, 0.85398, 0.86913, 0.91469, 0.92776, 0.93493, 0.94602, 0.95295, 0.955, 0.95635, 0.9567, 0.97388, 0.97742, 0.97888, 0.97888, 0.98112, 0.99866, 1.01753, 1.02575, 1.03214, 1.03885, 1.0532, 1.05634, 1.05951, 1.08014, 1.097, 1.10453, 1.15526, 1.15947, 1.16416, 1.16936, 1.1709, 1.1709, 1.1889, 1.19626, 1.19626, 1.20979, 1.21778, 1.22501, 1.22858, 1.23091, 1.24136, 1.24244, 1.25958, 1.26175, 1.26428, 1.27186, 1.29574, 1.30271, 1.30421, 1.30446, 1.30666, 1.30666, 1.31322, 1.32119, 1.32586, 1.32925, 1.3943, 1.40298, 1.40969, 1.42031, 1.42748, 1.44636, 1.44819, 1.46581, 1.48245, 1.50276, 1.55153, 1.63225, 1.66558, 1.67041, 1.68571, 1.75128, 1.81648, 1.84253, 1.94879, 2.03004, 2.25879, 2.25879, 2.54174, 2.60175, 2.73766, 2.84931, 3.45504, 3.85466, 3.85574, 3.93032, 6.05438]
	#list_of_SW_id = parser.get_SW_direction_id()
	#print (list_of_SW_id)

	SW_direction_data = []
	#ordered_SW_direction_data = []

	#check holliday and convert to Mon00 format
	date_string= datetime.datetime.fromtimestamp(int(raw_data[0]["timestamp"])).strftime('%A')
	day = date_string[0:3]
	hour = datetime.datetime.fromtimestamp(int(raw_data[0]["timestamp"])).strftime('%H')
	if (int(raw_data[0]["timestamp"])) in ca_holidays:
		day_hour = "Hol" +hour
	else:
		day_hour =  day + hour

	for a in HW_data:
		if (a["sensor_location_ID"] in list_of_SW_id) and (a["main_road_name"] in highway_list):
			SW_direction_data.append({
				"location_name": a["main_road_name"] + '@' + a["ref_road_name"], 
            	"uncapped_speed": a["avg_speed_uncapped"], 
            	"location_ID": a["sensor_location_ID"],
            	"timestamp": raw_data[0]["timestamp"],
            	"hour": day_hour,
            	"direction": "SW"
            	})
    
	## create the location list for NE direction
	#ordered_SW_direction_data = sorted(SW_direction_data)
	#print(ordered_SW_direction_data)

	#insert in elasticsearch
	for b in SW_direction_data:
		if b["uncapped_speed"] == "NULL":
			#print("found!!!!!!!!!!!!!!!!!!!")
			#print(b["location_ID"])
			#print(b["timestamp"])
			b["uncapped_speed"] = "60.0001"
		doc = {
			"location_name": str(b["location_name"]),
			"uncapped_speed": float(b["uncapped_speed"]),
			"location_id": str(b["location_ID"]),
			"timestamp": b["timestamp"]*1000,
			"hour": str(b["hour"]),
	 		"direction": str(b["direction"])
		}
		insert_elasticsearch(doc)

	return SW_direction_data

def insert_elasticsearch(doc):
	es = Elasticsearch()
	loc_id = str(doc["location_id"])
	#print(loc_id)
	if doc["direction"] == "SW":

		#res=es.index(index="highway_sw", doc_type=loc_id, id=1, body=doc)
		searched = es.search(index="highway_sw", body={"query": {"bool": {"should":{"term": {"location_id":loc_id }}}},"size": 1})
		check_zero = int(searched['hits']['total'])
		res=es.index(index="highway_sw", doc_type=loc_id, id=check_zero+1, body=doc)
		#print("1")

	if doc["direction"] == "NE":
		#res=es.index(index="highway_ne", doc_type=loc_id, id=1, body=doc)
		searched = es.search(index="highway_ne", body={"query": {"bool": {"should":{"term": {"location_id":loc_id }}}},"size": 1})
		#index=int(searched['hits']['hits'][0]['_id'])
		#new_index = index +1 
		#res=es.index(index="highway_ne", doc_type=loc_id, id=new_index, body=doc)
		check_zero = int(searched['hits']['total'])
		res=es.index(index="highway_ne", doc_type=loc_id, id=check_zero+1, body=doc)
	else:
		pass

def main():
	#date = "2016-01-23 00:00:00"
	#got 2:30 here
	#date = "2016-01-01 02:35:00"
	date = "2016-05-17 00:05:00"
	#date = "2015-07-11 00:00:00"
	start_time = time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timetuple())
	#print(start_time)
	#date2 = "2016-03-31 23:55:00"
	date2 = "2016-06-07 23:55:00"
	current_time = time.mktime(datetime.datetime.strptime(date2, "%Y-%m-%d %H:%M:%S").timetuple())
	#print(current_time)
	diff = 600
	#while start_time < current_time:
	while start_time <= current_time:
		month = datetime.datetime.fromtimestamp(start_time).strftime('%m')
		#print (month)
		day = datetime.datetime.fromtimestamp(start_time).strftime('%d')
		#print (day)
		hour = datetime.datetime.fromtimestamp(start_time).strftime('%H')
		#print (hour)
		minute = datetime.datetime.fromtimestamp(start_time).strftime('%M')
		start_url = "http://portal.cvst.ca/api/0.1/HW_speed?timestamp=2016"+ month + day + "T" + hour + minute +"EDT"
		#start_url2 = "http://portal.cvst.ca/api/0.1/HW_speed?timestamp=201601010105EDT"
		#print (start_url)
		get_SW_data(start_url)
		get_NE_data(start_url)
		#get_SW_data(start_url2)
		#get_NE_data(start_url2)
		start_time += diff

if __name__ == '__main__':
    #print(1)
    main()
    exit(0)

