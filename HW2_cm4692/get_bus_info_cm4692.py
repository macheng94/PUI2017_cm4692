import os
import json
import sys
import pandas as pd
try:
    import urllib2 as urllib
except ImportError:
    import urllib.request as urllib

url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=03bd464a-f2ac-42d7-a93b-9f28ca2f2ce4"+     "&VehicleMonitoringDetailLevel=calls&LineRef=B52"
    
response = urllib.urlopen(url)
data = response.read().decode("utf-8")
data = json.loads(data)



num = data["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"][0]["VehicleActivity"]




if not len(sys.argv) == 4:
    print ("Invalid number of arguments. Run as: python  aSimplePythonScript.py MTAKEY BUS_LINE BUS_LINE.csv")
    sys.exit()

Latitude = []
Longitude = []
Stopname = []
Status = []
for i in range(len(num)):
    stationname = data["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"][0]["VehicleActivity"][i]["MonitoredVehicleJourney"] ["OnwardCalls"]["OnwardCall"][0]["StopPointName"]
    status = data["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"][0]["VehicleActivity"][i]["MonitoredVehicleJourney"] ["OnwardCalls"]["OnwardCall"][0]["Extensions"]["Distances"]["PresentableDistance"]
    latitude = data["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"][0]["VehicleActivity"][i]["MonitoredVehicleJourney"]["VehicleLocation"]["Latitude"]
    longitude = data["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"][0]["VehicleActivity"][i]["MonitoredVehicleJourney"]["VehicleLocation"]["Longitude"]
    Latitude.append(latitude)
    Longitude.append(longitude)
    if data["Siri"]["ServiceDelivery"]["VehicleMonitoringDelivery"][0]["VehicleActivity"][i]["MonitoredVehicleJourney"]["OnwardCalls"] == {}:
        stationname.append('N/A')
        status.append('N/A')
    Stopname.append(stationname)
    Status.append(status)

output = pd.DataFrame({"Latitude":Latitude,"Longitude":Longitude,"Stop Name":Stopname,"Stop Status":Status})
print (output)

output.to_csv(sys.argv[3],index=False)
