#!/usr/bin/env python

## @package admin_auth_messages
# @brief This files contains all Proto-RPC message definitions for XamoomAdminApi.
# @author xamoom GmbH, Bruno Hautzenberger

from protorpc import messages

## Simple Proto-RPC message for a ndb.geopoint
class GeoPointMessage(messages.Message):

    ## Latitude
    lat = messages.FloatField(1, required=True)

    ## Longitude
    lon = messages.FloatField(2, required=True)
