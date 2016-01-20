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

## @package enduser_api_messages
# @brief This files contains all Proto-RPC message definitions for end users
# @author Bruno Hautzenberger



from protorpc import messages

from common_api_messages import GeoPointMessage

### CONTENT

class EndUserContentBlock(messages.Message):

    content_block_type = messages.IntegerField(1,required=True)

    public = messages.StringField(2,required=True)

    title = messages.StringField(3)

    text = messages.StringField(4)

    artists = messages.StringField(5)

    file_id = messages.StringField(6)

    youtube_url = messages.StringField(7)

    soundcloud_url = messages.StringField(8)

    link_type = messages.IntegerField(9)

    link_url = messages.StringField(10)

    content_id = messages.StringField(11)

    download_type = messages.IntegerField(12)

    spot_map_tag = messages.StringField(13)

    scale_x = messages.FloatField(14)

    video_url = messages.StringField(15)

    spot_map_show_content = messages.StringField(16)
    
    alt_text = messages.StringField(17)

class EndUserContentResponseMessage(messages.Message):

    ## the language of this localized information
    # Type Language
    language = messages.StringField(1,required=True)

    ## the content's display name
    title = messages.StringField(2,required=True)

    ## the content's description
    description = messages.StringField(3,required=True)

    ## the spot's image (as publich url) - not present if content has no image
    image_public_url = messages.StringField(4)

    ## content blocks
    content_blocks = messages.MessageField(EndUserContentBlock, 5, repeated=True)

    #system name
    system_name = messages.StringField(6)

    #content id
    content_id = messages.StringField(7,required=True)

    #category
    category = messages.IntegerField(8)

### STYLE

class EndUserSystemStyleMessage(messages.Message):

    ## the system's foreground color
    fg_color = messages.StringField(1,required=True)

    ## the system's background color
    bg_color = messages.StringField(2,required=True)

    ## the system's highlight color
    hl_color = messages.StringField(3,required=True)

    ## the system's icon
    icon = messages.BytesField(4,required=True)

    ## Chrome Header Color
    ch_color = messages.StringField(5)

    ## custom_marker
    custom_marker = messages.BytesField(6)

### MENU

## Message definition of a MenuItem (a content key)
class EndUserMenuItemMessage(messages.Message):

    ## content_id
    content_id = messages.StringField(1,required=True)

    ## content name
    item_label = messages.StringField(2,required=True)
    
    ## category
    category = messages.IntegerField(3)

## Message definition of a list of menu items
class EndUserMenuItemsMessage(messages.Message):

    ## menu items
    items = messages.MessageField(EndUserMenuItemMessage, 1, repeated=True)

### SCAN

class EndUserScanRequestMessage(messages.Message):

    ## the location identifier of the current scan
    location_identifier = messages.StringField(1,required=True)

    ## iBeacon Major (if this scan was caused by an ibeacon)
    ibeacon_major = messages.StringField(2)

    ## True / False
    include_style = messages.StringField(3,required=True)

    ## True / False
    include_menu = messages.StringField(4,required=True)

    ## Language
    language = messages.StringField(5,required=True)

class EndUserContentRequestMessage(messages.Message):

    ##content id
    content_id = messages.StringField(1,required=True)

    ## True / False
    include_style = messages.StringField(2,required=True)

    ## True / False
    include_menu = messages.StringField(3,required=True)

    ## Language
    language = messages.StringField(4,required=True)

    ## Geofencing
    is_geofencing = messages.StringField(5)

    ## full (only for apps in get_content_by_content_id_full)
    full = messages.StringField(6)

    preview = messages.StringField(7)

class EndUserSignleContentResponseMessage(messages.Message):

    ## style
    style = messages.MessageField(EndUserSystemStyleMessage, 3)

    ## menu
    menu = messages.MessageField(EndUserMenuItemsMessage, 4)

    ## content
    content = messages.MessageField(EndUserContentResponseMessage, 5)

    #system name
    system_name = messages.StringField(6)

    #system base_url
    system_url = messages.StringField(7)

    system_id = messages.IntegerField(8)

    #system is demo
    is_demo = messages.StringField(9)
    
    #app_id_google_play
    app_id_google_play = messages.StringField(10)
    
    #app_id_itunes
    app_id_itunes = messages.StringField(11)

class EndUserScanResponseMessage(messages.Message):

    ## marker initialized
    has_spot = messages.StringField(1,required=True)

    ## content assigned
    has_content = messages.StringField(2,required=True)

    ## style
    style = messages.MessageField(EndUserSystemStyleMessage, 3)

    ## menu
    menu = messages.MessageField(EndUserMenuItemsMessage, 4)

    ## content
    content = messages.MessageField(EndUserContentResponseMessage, 5)

    #system name
    system_name = messages.StringField(6)

    #system base_url
    system_url = messages.StringField(7)

    system_id = messages.IntegerField(8)

    #system is demo
    is_demo = messages.StringField(9)
    
    #app_id_google_play
    app_id_google_play = messages.StringField(10)
    
    #app_id_itunes
    app_id_itunes = messages.StringField(11)

### Geo Result

class EndUserGeoScanRequestMessage(messages.Message):

    location = messages.MessageField(GeoPointMessage, 1, required=True)

    language = messages.StringField(2,required=True)

    #just used for get_closest_spots
    radius = messages.IntegerField(3)
    limit = messages.IntegerField(4)

class GeofenceContentResponseMessage(messages.Message):

    language = messages.StringField(1,required=True)

    title = messages.StringField(2,required=True)

    description = messages.StringField(3,required=True)

    image_public_url = messages.StringField(4)

    content_id = messages.StringField(5, required=True)

    ## Latitude
    lat = messages.FloatField(6, required=True)

    ## Longitude
    lon = messages.FloatField(7, required=True)

    system_name = messages.StringField(8, required=True)

    #system base_url
    system_url = messages.StringField(9)

    ## the system's foreground color
    style_fg_color = messages.StringField(10,required=True)

    ## the system's background color
    style_bg_color = messages.StringField(11,required=True)

    ## the system's highlight color
    style_hl_color = messages.StringField(12,required=True)

    ## the system's icon
    style_icon = messages.BytesField(13,required=True)

    system_id = messages.IntegerField(14)

    #BEGIN new ones for analytics on geofences

    spot_id = messages.IntegerField(16)

    spot_name = messages.StringField(17)

    content_name = messages.StringField(18)

    #system is demo
    is_demo = messages.StringField(19)

class GeofenceAnalyticsMessage(messages.Message):
    requested_language = messages.StringField(1,required=True)
    delivered_language = messages.StringField(2,required=True)
    system_id = messages.IntegerField(3,required=True)
    system_name = messages.StringField(4, required=True)
    content_id = messages.StringField(5, required=True)
    content_name = messages.StringField(6, required=True)
    spot_id = messages.IntegerField(7, required=True)
    spot_name = messages.StringField(8, required=True)

class GeofenceResponseMessage(messages.Message):

    items = messages.MessageField(GeofenceContentResponseMessage, 1, repeated=True)

### SPOT

class EnduserSpotMessage(messages.Message):

    display_name = messages.StringField(1,required=True)
    description = messages.StringField(2)
    location = messages.MessageField(GeoPointMessage, 3)
    image = messages.StringField(4)
    content_id = messages.StringField(5)
    category = messages.IntegerField(6)

class EnduserSpotMapResponseMessage(messages.Message):

    items = messages.MessageField(EnduserSpotMessage, 1, repeated=True)
    style = messages.MessageField(EndUserSystemStyleMessage, 2)

    #just used for get_closest_spots
    radius = messages.IntegerField(3)
    limit = messages.IntegerField(4)

### APPS CONTENT LIST

class EnduserContentListResponseMessage(messages.Message):

    items = messages.MessageField(EndUserContentResponseMessage, 1, repeated=True)
    cursor = messages.StringField(2,required=True)
    more = messages.StringField(3,required=True)
