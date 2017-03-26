# apiai-flightassistant-webhook-sample
Webhook project for Flydubai Developer API

# Api.ai - sample webhook implementation in Python

This is a really simple webhook implementation that gets Api.ai classification JSON (i.e. a JSON output of Api.ai /query endpoint) and returns a fulfillment response.

More info about Api.ai webhooks could be found here:
[Api.ai Webhook](https://docs.api.ai/docs/webhook)

# Deploy to:
[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

# What does the service do?
It's a flight information fulfillment service that uses[Flydubai Developer API](https://devapi.flydubai.com/res/v3). 
The services takes the `geo-city`,`geo-time`, parameters from the action, performs geolocation for the city and requests flight information from Flydubai Developer public API. 

The service packs the result in the Api.ai webhook-compatible response JSON and returns it to Api.ai.

