# DISTRIBUTED SYSTEMS COURSEWORK DOCUMENTATION

## Prerequisite

To run this program you will need 
* `Pyro4`; and
* `requests`

which can both be installed using `pip install <package>`.

## Setup

To setup the server, first run the command
```
pyro4-ns
```
to setup the name server.
Then run three instances of the back-end.py by running
```
python back-end.py
```
in three separate terminals, a URI should be provided for each one.
Now run the `front-end.py` via
```
python front-end.py
```
and then enter the URIs outputted by the back-end scripts delimited by line breaks.
Finally, run `client.py` via
```
python client.py
```
and copy the URI from the front end script and press enter.
Now you can use client script to access the system.

## Web service

The web service used for postcode lookup is [postcodes.io](https://postcodes.io/).
