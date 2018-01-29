import statistics

from influxdb import InfluxDBClient


# this method takes in an integer value that represents the hours past
# to construct an update from.
def constructUpdate(hours): 

	# Establish connection with the database for a query
	client = InfluxDBClient('localhost', 8086, 'root', 'root', 'garden')

	# Call query to get the temperature for the incubator for the specified 
	# hours
	temperatures = client.query("SELECT value,environment FROM temperature WHERE time > now() - " + str(hours) + "h")

	# Query for the relative humidity for the same criteria above 
	humidities = client.query("SELECT value,environment FROM relative_humidity WHERE time > now() - " +str(hours) + "h")

	# Create lists for each tags and measurement pair
	flower_tent_temp = map(lambda x: x['value'], temperatures.get_points(tags={"environment": "flower_tent"}))
	clone_incubator_temp = map(lambda x: x['value'], temperatures.get_points(tags={"environment": "clone_incubator"}))
	veg_tent_temp = map(lambda x: x['value'], temperatures.get_points(tags={"environment": "veg_tent"}))

	flower_tent_hum = map(lambda x: x['value'], humidities.get_points(tags={"environment": "flower_tent"})) 
	clone_incubator_hum = map(lambda x: x['value'], humidities.get_points(tags={"environment": "clone_incubator"}))
	veg_tent_hum = map(lambda x: x['value'], humidities.get_points(tags={"environment": "veg_tent"}))



	# Calculate averages
	flower_tent_temp_avg = sum(flower_tent_temp)/len(flower_tent_temp)
	clone_incubator_temp_avg = sum(clone_incubator_temp)/len(clone_incubator_temp)
	veg_tent_temp_avg = sum(veg_tent_temp)/len(veg_tent_temp)

	flower_tent_hum_avg = sum(flower_tent_hum)/len(flower_tent_hum)
	clone_incubator_hum_avg = sum(clone_incubator_hum)/len(clone_incubator_hum)
	veg_tent_hum_avg = sum(veg_tent_hum)/len(veg_tent_hum)

	# Calculate the standard deviations
	flower_tent_temp_std = statistics.stdev(flower_tent_temp)
	clone_incubator_temp_std = statistics.stdev(clone_incubator_temp)
	veg_tent_temp_std = statistics.stdev(veg_tent_hum)

	flower_tent_hum_std = statistics.stdev(flower_tent_temp)
	clone_incubator_hum_std = statistics.stdev(clone_incubator_temp)
	veg_tent_hum_std = statistics.stdev(veg_tent_hum)


	# construct string
	return_string = ("Here is the update for the past " + str(hours) 
	+ " hours. \n Average Flower Tent Stats: " + str( '{:.2f}'.format(flower_tent_temp_avg)) + "F, " 
	+ str('{:.2f}'.format(flower_tent_hum_avg)) + "RH \n Average Veg Tent Stats: " 
	+ str('{:.2f}'.format(veg_tent_temp_avg)) + "F, " + str('{:.2f}'.format(veg_tent_hum_avg)) 
	+ "RH \n Average Incubator Stats: " + str('{:.2f}'.format(clone_incubator_temp_avg)) + "F, " 
	+ str('{:.2f}'.format(clone_incubator_hum_avg)) + "RH" ) 

	return return_string

