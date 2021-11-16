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


## Features

## Description

## Configuration

## Links

## License

