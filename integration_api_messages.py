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

## @package admin_auth_messages
# @brief This files contains all Proto-RPC message definitions for XamoomCustomerApi.
# @author Bruno Hautzenberger

from protorpc import messages

from common_api_messages import GeoPointMessage


## Message definition for a System entity
class IntegrationSystemResponseMessage(messages.Message):

    ## the user's internal id
    # None for new users
    id = messages.IntegerField(1)

    ## the system's username
    name = messages.StringField(2,required=True)

    ## the system's base url
    base_url = messages.StringField(3,required=True)

    ## the system's country
    # Type Countries
    country = messages.IntegerField(4,required=True)

    ## the system's "home" location
    location = messages.MessageField(GeoPointMessage, 5)

    ## the system's primary language
    # Type Language
    language = messages.StringField(6,required=True)

## Message definition for a System's Style Information
class IntegrationSystemStyleMessage(messages.Message):

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

class IntegrationContentMessage(messages.Message):

    ## the content's id
    content_id = messages.StringField(1, required=True)

    ## the content's name
    name = messages.StringField(2, required=True)

    ## languages of this content
    languages = messages.StringField(5, repeated=True)

## Message definition of a list of contents 
class IntegrationContentListResponseMessage(messages.Message):

    ## List of CustomerContentMessage
    items = messages.MessageField(IntegrationContentMessage, 1, repeated=True)

    ## Cursor
    # resume cursor
    cursor = messages.StringField(2, required=True)

    ## has more
    has_more = messages.StringField(3, required=True)

class IntegrationContentBlock(messages.Message):

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
    
    alt_text = messages.StringField(16)

class IntegrationContentResponseMessage(messages.Message):

    ## the content's display name
    title = messages.StringField(1,required=True)

    ## the content's excerpt
    description = messages.StringField(2,required=True)

    ## the spot's image (as publich url) - not present if content has no image
    image_public_url = messages.StringField(3)

    ## content blocks
    content_blocks = messages.MessageField(IntegrationContentBlock, 4, repeated=True)

    #system id
    system_id = messages.IntegerField(6,required=True)

    ## content blocks
    system_style = messages.MessageField(IntegrationSystemStyleMessage, 7, required=False)

class IntegrationSpotMessage(messages.Message):

    display_name = messages.StringField(1,required=True)
    description = messages.StringField(2)
    location = messages.MessageField(GeoPointMessage, 3)
    image = messages.StringField(4)

class IntegrationSpotMapResponseMessage(messages.Message):

    items = messages.MessageField(IntegrationSpotMessage, 1, repeated=True)
