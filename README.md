# cups-filters

A dockerized version of CUPS Filters with a set of API for managing printers and print jobs

***

## How to use it

This dockerized version of CUPS Filters aims to be a good solution for those scenarios where is needed a server side rendering and a client side printing. This docker container does its work in combo with this: https://hub.docker.com/r/drcoccodrillus/cups

### Scenario

This is the typical scenario where using this image could help you out.

There is an application server which needs to process the rendering phase server side.
Application server ---> Cups Server


### Clone the repository

`git clone git@github.com:drcoccodrillus/docker-cups-filters.git`

### Build the image

`docker-compose up --build -d`

#### Default settings

Before starting the cups-filters container, remember to start this dockerized version of CUPS https://hub.docker.com/r/drcoccodrillus/cups or to have a CUPS Server running and configured for accepting print jobs from the network. As default settings, this containerized cups-filters process the encoded PDF payload received through the API using Generic-PDF_Printer-PDF.ppd then sends print jobs to a CUPS Server with IP 172.28.0.2 and listening on default 631. You can modify this default settings changing the config.py constants CUPS_HOST and PPD.

### API

A set of API is defined to make it easy sending print jobs or querying CUPS. In case you run this project dockerized use the first url to invoke the API. Instead, if you run this project directly on your host machine, use the second url.

#### [GET] api/v1/print-jobs

Returns the queue for gprinter

`http://172.28.0.3:5000/api/v1/print-jobs`

`http://localhost:5000/api/v1/print-jobs`

**Returned JSON**
```
[{"id": "gprinter-1", "owner": "thedude", "size": "182272", "date": "24 mar 2023,", "time": "11:58:29"}]
```
#### [GET] api/v1/printer-status

Returns a list of configured printers within their status

`http://172.28.0.3:5000/api/v1/printer-status`

`http://localhost:5000/api/v1/printer-status`

**Returned JSON**
```
[{"printer": "gprinter", "status": "enabled", "date": "24 mar 2023", "time": "11:58:29"}]
```

#### [GET] api/v1/printer-details

Returns a list of printers connected through USB cable

`http://172.28.0.3:5000/api/v1/printer-details`

`http://localhost:5000/api/v1/printer-details`

**Returned JSON**
```
[{"connection": "direct", "uri": "usb://Xerox/WorkCentre%20PE114%20Series?serial=3429108682......"}]
```

#### [POST] api/v1/print-base64

Receives a base64 encoded PDF

`http://172.28.0.3:5000/api/v1/print-base64`

`http://localhost:5000/api/v1/print-base64`


**Returned JSONs**

***Successful print***

```
{"message": "PDF printed"}
```

***Errors***

It didn't receive a valid base64 PDF
```
{"message": "Error: No PDF provided"}
```
