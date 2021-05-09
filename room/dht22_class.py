from conf.Generic_Sensor import *
import time
import Adafruit_DHT

class dht22(SensorPublisher):
    def __init__(self,configuration_filename,device_ID='dht22',pin=17):
        SensorPublisher.__init__(self,configuration_filename,device_ID)
        self.DHT22 = Adafruit_DHT.DHT22                              
        self.DHT22_PIN = pin
                    
    def retrieveData(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.DHT22, self.DHT22_PIN, retries=2, delay_seconds=3)
        #outputResult=[{'parameter':'humidity','value':humidity},{'parameter':'temperature','value':temperature}]
        if humidity is not None:
            if (humidity<=100):
                outputResult=[{'parameter':'humidity','value':humidity}]
                return outputResult
            
