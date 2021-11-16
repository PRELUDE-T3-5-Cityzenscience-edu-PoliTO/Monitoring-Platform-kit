# Monitoring-Platform-kit

![](http://www.politocomunica.polito.it/var/politocomunica/storage/images/media/images/marchio_logotipo_politecnico/1371-1-ita-IT/marchio_logotipo_politecnico_large.jpg) 

> **Master course in ICT FOR SMART SOCIETIES**

> **Interdisciplinary projects 2020-2021**

*Considering the high price solutions for indoor thermal comfort monitoring, this project proposes a low-cost IoT sensor network (exploiting Raspberry Pi and Arduino platforms) for collecting real-time data and evaluating specific thermal comfort indicators (PMV and PPD). The overall architecture was accordingly designed, implementing the hardware setup, the back-end and the Android user interface. Eventually, three distinct platforms were deployed for testing the general system and analyzing the obtained results in different places and seasons, based on collected data and users’ preferences.*

This repository can be used to setup a new platform hardware kit.

The main repostiory for the initial set up and the monitoring platform back-end is retrievable here:

> [https://github.com/AndreaAvignone/PMV-Monitoring-Platform](url)

The source code for the Android Application:

> [https://github.com/AndreaAvignone/myComfort](url)


## Hardware kit architecture overview
The main functionality of the hardware kit is to collect raw data from sensors. The system is implemented to be flexible and capable of supporting different types of sensors which are handled by a Raspbery Pi and an Arduino module. Furthermore, the former is in charge of the communications with the server while the latter is used as an ADC for supporting analog devices. 
The parameters required for an accurate functioning of the platform are:
* Air Temperature
* Relative Humidity
* Globe Temperature
* Air velocity

In addition to sensors needed for providing the described parameters and the Raspberry and Arduino modules, a breadboard kit is required to handle the connections and a display to visualize real-time metrics. 

## Tested configuration
A possible implementation of the kit is shown in the figure below and it is composed by:
* Sensors:

<table>
  <tr>
    <th>Sensor</th>
    <th>Measured Parameter</th>
  </tr>
  <tr>
    <td>DS18B20</td>
    <td>Air temperature</td>
  </tr>
  <tr>
    <td>DHT22</td>
    <td>Relative Humidity</td>
  </tr>
  <tr>
    <td>MAX6675</td>
    <td>Globe temperature</td>
  </tr>
  <tr>
    <td>Rev-C</td>
    <td>Air Velocity</td>
  </tr>
</table>

* Raspberry Pi 3B
* Arduino One
* Display OLED 0.96''
* Breadboard kit


<img src="https://github.com/AndreaAvignone/Monitoring-Platform-kit/blob/main/IP_kit_circuit_bb.png" alt="SensorKit_scheme" width="700"/>


## Getting Started

In order to correctly install a new platform, it is necessary to have a unique platform ID:

> MP-A000xx

### Configuration of the central HUB
Open the terminal and rename the Rasperry Pi:

```
sudo nano /etc/hostname
```

Save with:
> ctrl+x 

Then reboot:
> reboot

### Check platform ID

```
hostname
```

### Clone the repository

```
git clone https://github.com/AndreaAvignone/Monitoring-Platform-kit.git
```

### Setup

Entering the correct path:

```
cd Monitoring-Platform-kit
```

Run the installation:

```
python3 install.py
```

### Registration
Open the application, fill the form and sign-in. Use >Add Platform button.

### Final association
Reboot the Rasperry Pi (within 5 minutes) and the association will be automatically completed without additional steps.

If the association fails, run: 
> autorun 

or 
> reboot

## Description

### Associate a new platform

When all services are up, new platforms can be installed. Each platform is composed by a **central HUB**, locally exposed for the REST communication with present rooms. It actually ping the back-end to be added to the catalog. Then, a room can be configured.

**IMPORTANT**: the idea is that a virtual instance is created from the client (i.e. the mobile application), appended to the *profiles catalog* of the specific platform with:
``
connection_flag=False. 
``

When the physical room is plugged, it retrieves information about *service catalog* from the *central HUB*, then it sends a put request to *profiles catalog*.\
In this way, the server check if there is any room previously created, with *connection_flag equal* to false and a timestamp less than 1 minute. Association is therefore performed. 

Moreover, for each profile, a room counter is set. In fact, room is "blind" also about itself, avoiding needs for any kind of a-priori identification. It just knows the IP address of the central HUB, and the *basic room_ID* it is expected to assume (e.g. room_X). When the association is correclty performed, *profiles service* returns the complete configuration, including the ID based on counter (e.g. room_X2 if it is the second associated room) and name set by client. Room updates its own configuration file so that connected sensors can retrieve all information.

### Sensor network
For the **sensor installation**, main.py script is used, independently on the sensor. In fact, when main script is run, it automatically imports the class according to sensor_ID. Sensor_ID is specified as argument, toghether with the room configuration file and the related pin:
```
python3 main.py room_setup.json dht11 17 
```

Again, the sensor requests configuration drivers from *central HUB* with a GET request. If central HUB has not already the drivers inside its own memory, it contacts the **drivers service** to download. Sensor can now be configured, publishing on the broker messages. Eventually, subscriber collects information among all sensors and continusoly updates stored information inside the *server catalog*.

