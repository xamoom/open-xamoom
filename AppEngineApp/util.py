#!/usr/bin/env python

## @package util
# @brief This files contains helper methods and constants for all kinds of tasks
# @author Bruno Hautzenberger
# @copyright xamoom GmbH, 2014. All rights reserved.


import logging

from common_api_messages import GeoPointMessage

## converts strings like 'True' or 'False' to boolean
# @param theString ('True' or 'False')
# @return boolean
def string_to_bool(theString):
    return theString[0].upper()=='T'

## converts a boolean to 'True' or 'False' strings
# @param theBool boolean
# @return 'True' or 'False'
def bool_to_string(theBool):
    if theBool:
        return 'True'
    else:
        return 'False'

## converts a List to a GeoPointMessage
def location_message_from_geopoint(geopoint):
    return GeoPointMessage(lat = float(geopoint[0]), lon = float(geopoint[1]))
