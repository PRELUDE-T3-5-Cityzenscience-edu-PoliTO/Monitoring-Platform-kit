import cherrypy
import json
import socket
import sys
import time
import os
import requests
from urllib.parse import urlparse

class HUB():
    def __init__(self,db_filename,IP):
        self.db_filename=db_filename
        self.hubContent=json.load(open(self.db_filename,"r"))
        self.service=self.hubContent['service']
        self.serviceCatalogAddress=self.hubContent['service_catalog']
        self.hub_ID=self.hubContent['hub_ID']
        self.port=self.hubContent["IP_port"]
        self.rooms=self.hubContent['rooms']
        self.retrieveBroker()
        time.sleep(0.5)
        self.setup(IP)


    def retrieveBroker(self):
        print("Retrieving broker information...")
        try:
            requestBroker=requests.get(self.serviceCatalogAddress+'/public/broker').json()
            port=urlparse(requestBroker.get('IP_address')).port
            IP=urlparse(requestBroker.get('IP_address')).netloc.replace(":"+str(port),"")
            msg={"IP_address":IP,"port":port}
            self.hubContent["broker"].append(msg)
            print("Broker info obtained.")
        except IndexError as e:
            print("Broker info not obtained.")
            
    def setup(self,hub_IP):
        print("Connecting...")
        try:
            requestResourcesCatalog=requests.get(self.serviceCatalogAddress+'/public/server_catalog').json()
            IP=requestResourcesCatalog.get('IP_address')
            service=requestResourcesCatalog.get('service')
            self.hubContent['server_catalog']=self.buildAddress(IP,service)
            json_body={"platform_ID":self.hub_ID,"rooms":self.rooms,'local_IP':"http://"+hub_IP+":"+str(self.port)+self.service}
            requests.put(self.hubContent['server_catalog']+'/insertPlatform',json=json_body)
            print("Connection performed")
        except:
            print("Connection failed.")
            return False


    def retrieveInfo(self,parameter):
        try:
            result= self.hubContent[parameter]
        except:
            result=False
        return result

    def retrieveDrivers(self,device_ID):
        notFound=1
        try:
            drivers_list=self.hubContent['drivers']
            for drivers in drivers_list:
                if drivers['device_ID']==device_ID:
                    notFound=0
                    return drivers
            if notFound==1:
                print(f'Drivers for device {device_ID} not found. Downloading...')
                drivers=self.downloadDrivers(device_ID)
                self.hubContent['drivers'].append(drivers)
                print(f'Drivers for device {device_ID} installed.')
                return drivers
        except:
            return False

    def downloadDrivers(self,device_ID):
        try:
            requestDriversCatalog=requests.get(self.serviceCatalogAddress+'/public/drivers_catalog').json()
            IP=requestDriversCatalog.get('IP_address')
            service=requestDriversCatalog.get('service')
            drivers=requests.get(self.buildAddress(IP,service)+'/drivers_list/'+device_ID).json()
            return drivers
        except:
            return False



    def buildAddress(self,IP, service):
        finalAddress=IP+service
        return finalAddress


class HUB_REST():
    exposed=True
    def __init__(self,db_filename,IP):
        self.IP=IP
        self.hubCatalog=HUB(db_filename,self.IP)
        self.port=self.hubCatalog.port

    def GET(self, *uri):
        if len(uri)>0:
            parameter=uri[0]
            info=self.hubCatalog.retrieveInfo(parameter)
            if len(uri)>1 and uri[0]=='drivers':
                    device_ID=uri[1]
                    drivers= self.hubCatalog.retrieveDrivers(device_ID)
                    if drivers is not False:
                        output=drivers
                    else:
                        raise cherrypy.HTTPError(404,"Drivers Not found")


            elif len(uri)==1 and uri[0]=='drivers':
                raise cherrypy.HTTPError(405,"You can't!")

            elif len(uri)==1 and uri[0]=='reboot':
                print("Rebooting...")
                time.sleep(2.5)
                os.system("sudo reboot")
                output=True
            elif len(uri)==1 and uri[0]=='poweroff':
                print("Shutdown...")
                time.sleep(2.5)
                os.system("sudo poweroff")
                output=True
            else:
                if info is not False:
                    output=info
                else:
                    raise cherrypy.HTTPError(404,"Information Not found")

        else:
            output=self.hubCatalog.retrieveInfo('description')
        return json.dumps(output)

def get_ip_address():
     ip_address = '';
     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
     s.connect(("8.8.8.8",80))
     ip_address = s.getsockname()[0]
     s.close()
     return ip_address

if __name__ == '__main__':
    db=sys.argv[1]
    IP=get_ip_address()
    hub=HUB_REST(db,IP)
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True
        }
    }
    cherrypy.tree.mount(hub, hub.hubCatalog.service, conf)
    cherrypy.config.update({'server.socket_host': hub.IP})
    cherrypy.config.update({'server.socket_port': hub.port})
    cherrypy.engine.start()
    while True:
        time.sleep(1)
    cherrypy.engine.block()

