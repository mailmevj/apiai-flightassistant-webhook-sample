#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
#    if req.get("result").get("action") == "searchFlights":
#	    baseurl = "https://devapi.flydubai.com/res/v3/flights/1"

#    if req.get("result").get("action") == "optionalExtras":
#	    baseurl = "https://devapi.flydubai.com/res/v3/optional/extras"
    
    if req.get("result").get("action") == "flightdetails":
    	baseurl = "https://devapi.flydubai.com/ops/v3/flightinfo"

#    else:
#        return{}
    
    yql_query = makeYqlQuery(req)
    print(yql_query)
#    if yql_query is None:
#        return {}
#    yql_url = baseurl + urlencode(yql_query)
#    print("URL data: \n "+yql_url)

    data = urllib.parse.urlencode(yql_query)
    data = data.encode('ascii') # data should be bytes
    req = urllib.request.Request(baseurl, data)

    result = urlopen(req).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    flightNumber = paramters.get("flightNumber")
#    if city is None:
#        return None
    return {
	"{ 'carrierCode' : 'FZ', 'flightNumber': '"+flightNumber+"', 'flightDate': '20-10-2017', 'origin': 'DXB', 'destination':'DOH' }"
   }


def makeWebhookResult(data):
#    {
#      "carrierCode": "FZ",
#      "flightNumber": "24",
#      "flightDate": "20-10-2017",
#      "origin": "DXB",
#      "destination": "DOH",
#      "status": "FO",
#      "gateNumber": 228,
#      "terminal": "T2"
#    }
    print(data)

#    query = data.get('query')
#    if query is None:
#        return {}

#    result = query.get('results')
#    if result is None:
#        return {}

#    channel = result.get('channel')
#    if channel is None:
#        return {}

#    item = channel.get('item')
#    location = channel.get('location')
#    units = channel.get('units')
#    if (location is None) or (item is None) or (units is None):
#        return {}

#    condition = item.get('condition')
#    if condition is None:
#        return {}

    # print(json.dumps(item, indent=4))
	
    speech = "The flight is in "+data.get('status')+" status, and you can see it at Gate number "+data.get('gateNumber')+" of the "+data.get('terminal')+" Terminal."
#    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
#             ", the temperature is " + condition.get('temp') + " " + units.get('temperature')

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
    
