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

## @package static_types
# @brief static types and constants
# @author Bruno Hautzenberger
# @copyright xamoom GmbH, 2015. All rights reserved.

## Available AccessInterfaceTypes
class AccessInterfaceType:
    NFC = "NFC"
    QR = "QR"
    EDDYSTONE = "EDDYSTONE"
    IBEACON = "IBEACON"

## Available Content Status values.
class ContentLinkTypes:
    FACEBOOK = 0
    TWITTER = 1
    WEB = 2
    AMAZON = 3
    WIKIPEDIA = 4
    LINKEDIN = 5
    FLICKR = 6
    SOUNDCLOUD = 7
    ITUNES = 8
    YOUTUBE = 9
    GOOGLEPLUS = 10
    TEL = 11
    EMAIL = 12
    SPOTIFY = 13
    GOOGLE_MAPS = 14
    ITUNES_APP = 15
    GOOGLE_PLAY = 16
    WINDOWS_STORE = 17

class ContentBlockTypes:
    TEXT = 0
    AUDIO = 1
    VIDEO = 2
    IMAGE = 3
    LINK = 4
    EBOOK = 5
    CONTENT = 6
    SOUNDCLOUD = 7
    DOWNLOAD = 8
    SPOTMAP = 9

class ContentDownloadTypes:
    VCF = 0
    ICAL = 1
