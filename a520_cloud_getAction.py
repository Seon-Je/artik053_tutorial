#/****************************************************************************
#*
#* Copyright 2018 Primesoft All Rights Reserved.
#*
#* Filename: 663_getAction.py
#* Author: enj.park, yr.kim
#* Release date: 2018/05/02
#* Version: 2.1
#* Modified date : 2018/05/23 by sj.yang
#*
#****************************************************************************/

import artikcloud
from artikcloud.rest import ApiException
import sys, getopt
import time, json
from pprint import pprint

# For LED
ledPin = 135
path_export = '/sys/class/gpio/export'
path_unexport = '/sys/class/gpio/unexport'
path_dir = '/sys/class/gpio/gpio%d/direction' % ledPin
path_val = '/sys/class/gpio/gpio%d/value' % ledPin


def main(argv):
	DEFAULT_CONFIG_PATH = 'config.json'
	
	with open(DEFAULT_CONFIG_PATH, 'r') as config_file:
		config = json.load(config_file)
#	print(config)

	artikcloud.configuration = artikcloud.Configuration();
	artikcloud.configuration.access_token = config['device_token']

	# create an instance of the API class
	api_instance = artikcloud.MessagesApi()
	count = 1
	start_date = int(time.time()*1000) - 86400000   # 24 hours ago
	end_date = int(time.time()*1000) 		# current
	order = 'desc'

	try: 
		# Get Normalized Actions
		api_response = api_instance.get_normalized_actions(count=count, end_date = end_date, start_date = start_date, order = order)
#		pprint(api_response)
		actionName = api_response.data[0].data.actions[0].name;
		if actionName == "setOnLED":
			pinVAL = open(path_val, "wb", 0)
			pinVAL.write(str(1))
			pinVAL.close()		
#			ff = open('led_state.txt','w')
#           ff.write('1')
#           ff.close()
			print('[RECEIVED] LED Turned On')
		else:
			pinVAL = open(path_val, "wb", 0)
			pinVAL.write(str(0))
			pinVAL.close()
#			ff = open('led_state.txt','w')
#           ff.write('0')
#           ff.close()
			print('[RECEIVED] LED Turned Off')
				
	except ApiException as e:
		print("Exception when calling MessagesApi->get_normalized_actions: %s\n" % e)


if __name__ == "__main__":
	# export
	pinCTL = open(path_export, "wb", 0)
	try:
		pinCTL.write(str(ledPin))
		print "Exported pin", str(ledPin)
	except:
		print "Pin ", str(ledPin), "has been exported"
	pinCTL.close()
	
	# direction
	pinDIR = open(path_dir, "wb", 0)
	try:
		pinDIR.write("out")
		print "Set pin ", str(ledPin), "as digital output"
	except:
		print "Failed to set pin direction"
	pinDIR.close()


	# value & unexport
	while True:
		main(sys.argv[1:])
		time.sleep(5)
