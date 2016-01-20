#!/usr/bin/env python

"""
open xamoom cloud backend
Copyright (C) 2015  xamoom GmbH

This file is part of open xamoom

open xamoom is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

xamoom-wordpress is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with open xamoom.  If not, see <http://www.gnu.org/licenses/>.
"""

## @package util
# @brief This files contains helper methods and constants for all kinds of tasks
# @author Bruno Hautzenberger
# @copyright xamoom GmbH, 2014. All rights reserved.


import logging

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
