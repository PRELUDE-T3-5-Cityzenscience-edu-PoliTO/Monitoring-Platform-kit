import os
import time
import json
import socket

hub_folder="central Hub"
hubContent=json.load(open(hub_folder+"/etc/hub_db.json","r"))
hub_ID=socket.gethostname().replace("Monitoring-hub-","")
hubContent["hub_ID"]=hub_ID
hubContent["client_ID"]=hub_ID
with open(hub_folder+"/etc/hub_db.json",'w') as file:
    json.dump(hubContent,file,indent=4)
os.system("chmod 745 autorun")
time.sleep(.1)
os.chdir("central Hub")
time.sleep(.1)
os.system("chmod 745 hub_autorun")
time.sleep(.1)
os.chdir("../room")
time.sleep(.1)
os.system("chmod 745 room_autorun")
os.system("chmod 745 sensors_autorun")
time.sleep(.1)
#print("Installation completed")

