#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

## @package models
# @brief xamoom core data models
# @author xamoom GmbH, Bruno Hautzenberger

import endpoints

import random
import string
import logging
import base64

from util import string_to_bool
from util import bool_to_string

from config import file_dir

from static_types import ContentBlockTypes, ContentLinkTypes

from enduser_api_messages import EndUserContentResponseMessage
from enduser_api_messages import EndUserContentBlock

from enduser_api_messages import EnduserSpotMessage
from enduser_api_messages import EndUserMenuItemsMessage
from enduser_api_messages import EndUserSystemStyleMessage
from enduser_api_messages import EndUserMenuItemMessage

from integration_api_messages import IntegrationContentResponseMessage
from integration_api_messages import IntegrationContentBlock
from integration_api_messages import IntegrationContentMessage
from integration_api_messages import IntegrationSpotMessage
from integration_api_messages import IntegrationSystemStyleMessage

## model to store nested localized information of a customer system
class LocalizedSystemInformation(object):

    def __init__(self):
        #language identifier (de,en,...)
        self.language = None
    
        ## the system's display name
        self.display_name = ""
    
        ## the system's description
        self.description = ""
    
        ## the system's long description
        self.long_description = ""

## model to store a customer system
class System(object):

    def __init__(self):
        ## internal name
        self.name = ""
        
        ## API KEY
        self.api_key = ""

        ## information about this system in different languages
        self.localized_information = []
        
        ## base url
        self.base_url = ""

## model to store a customer system style information
class SystemStyle(object):

    def __init__(self):
        self.fg_color = ""
        self.bg_color = ""
        self.hl_color = ""
        self.ch_color = ""
        self.icon = ""
        self.custom_marker = ""

    def to_enduser_message(self):

        message = EndUserSystemStyleMessage(fg_color=self.fg_color,
                                        bg_color=self.bg_color,
                                        hl_color=self.hl_color,
                                        icon=base64.b64decode(self.icon),
                                        custom_marker=base64.b64decode(self.custom_marker),
                                        ch_color=self.ch_color)

        return message
    
    def to_integration_message(self):

        message = IntegrationSystemStyleMessage(fg_color=self.fg_color,
                                        bg_color=self.bg_color,
                                        hl_color=self.hl_color,
                                        icon=base64.b64decode(self.icon),
                                        custom_marker=base64.b64decode(self.custom_marker),
                                        ch_color=self.ch_color)

        return message

## model to store a marker which connects physical things to spots
class Marker(object):
    spot_id = None
    qr = None
    nfc = None
    eddystone = None
    ibeacon_region_uid = None
    ibeacon_major = None
    ibeacon_minor = None

## model to store nested localized information of a customer spot
class LocalizedSpotInformation(object):

    def __init__(self):
        self.spot_id = ""
        self.language = ""
        self.display_name = ""
        self.description = ""

## model to store a customer spot
class Spot(object):
    
    def __init__(self):
        self.spot_id = ""
        self.name = ""
        self.image = ""
        self.category = 0
        self.location = (46,14)
        self.localized_information = {}
        self.content = ""
        self.tags = []
    
    def to_enduser_message(self, lang, system, include_content=False):
        message = EnduserSpotMessage()
        
        display_name = ""
        description = ""

        found_lang = False
        for l_info in self.localized_information.values():
            if l_info.language == lang:
                display_name = l_info.display_name
                description = l_info.description
                found_lang = True

        if found_lang == False: #requested lang not found
            l_info = self.localized_information.values()[0]
            display_name = l_info.display_name
            description = l_info.description

        message.display_name = display_name
        message.description = description

        message.location=location_message_from_geopoint(self.location)

        message.image = file_dir + self.image

        if include_content:
            message.content_id = self.content
            
        message.category = self.category

        return message
    
    def to_integration_message(self, lang):
        message = IntegrationSpotMessage()

        display_name = ""
        description = ""

        found_lang = False
        for l_info in self.localized_information.values():
            if l_info.language == lang:
                display_name = l_info.display_name
                description = l_info.description
                found_lang = True

        if found_lang == False: #requested lang not found
            l_info = self.localized_information.values()[0]
            display_name = l_info.display_name
            description = l_info.description

        message.display_name = display_name
        message.description = description
        
        message.location=location_message_from_geopoint(self.location)

        message.image = file_dir + self.image

        return message

## model to store a nested content block
class ContentBlock(object):

    def __init__(self):
        ## the content block's type
        # Type ContentBlockTypes
        self.content_block_type = 0
    
        ## public flag
        self.public = True
    
        self.title = ""
    
        self.text = ""
    
        self.artists = ""
    
        self.file_id = ""
    
        self.youtube_url = ""
    
        self.soundcloud_url = ""
    
        self.link_type = 0
        
        self.link_url = ""
    
        self.content_id = ""
    
        self.download_type = 0
    
        self.spot_map_tag = ""
    
        self.spot_map_show_content = ""
    
        self.scale_x = 100
        
        self.alt_text = ""


    def to_enduser_message(self):
        message = EndUserContentBlock()

        if self.content_block_type == ContentBlockTypes.TEXT:
            message.title = self.title
            message.text = self.text
        elif self.content_block_type == ContentBlockTypes.AUDIO:
            message.title = self.title
            message.artists = self.artists
            message.file_id = file_dir + self.file_id

        elif self.content_block_type == ContentBlockTypes.VIDEO:
            message.title = self.title
            message.video_url = self.youtube_url
        elif self.content_block_type == ContentBlockTypes.IMAGE:
            message.title = self.title
            message.file_id = file_dir + self.file_id

            if self.link_url == None:
                message.link_url = ""
            else:
                if self.link_url.startswith('http://') == False and self.link_url.startswith('https://') == False:
                    message.link_url = "http://" + self.link_url
                else:
                    message.link_url = self.link_url

            if hasattr(self,"scale_x") and self.scale_x != None:
                message.scale_x = self.scale_x
                
            if hasattr(self,"alt_text") and self.alt_text != None:
                message.alt_text = self.alt_text

        elif self.content_block_type == ContentBlockTypes.LINK:
            message.title = self.title
            message.text = self.text
            message.link_type = self.link_type

            #add special link type prefixes
            if self.link_type == ContentLinkTypes.EMAIL and self.link_url.startswith('mailto:') == False:
                message.link_url = "mailto:" + self.link_url
            elif self.link_type == ContentLinkTypes.TEL and self.link_url.startswith('tel:') == False:
                message.link_url = "tel:" + self.link_url
            elif self.link_type != ContentLinkTypes.TEL and self.link_type != ContentLinkTypes.EMAIL:
                if self.link_url.startswith('http://') == False and self.link_url.startswith('https://') == False:
                    message.link_url = "http://" + self.link_url
                else:
                    message.link_url = self.link_url
            else:
                message.link_url = self.link_url

        elif self.content_block_type == ContentBlockTypes.EBOOK:
            message.title = self.title
            message.artists = self.artists
            message.file_id = file_dir + self.file_id
        elif self.content_block_type == ContentBlockTypes.CONTENT:
            message.title = self.title
            message.content_id = self.content_id
        elif self.content_block_type == ContentBlockTypes.SOUNDCLOUD:
            message.title = self.title
            message.soundcloud_url = self.soundcloud_url
        elif self.content_block_type == ContentBlockTypes.DOWNLOAD:
            message.title = self.title
            message.text = self.text
            message.download_type = self.download_type
            message.file_id = file_dir + self.file_id
        elif self.content_block_type == ContentBlockTypes.SPOTMAP:
            message.title = self.title
            message.spot_map_tag = self.spot_map_tag
        else:
            logging.error('Invalid Content Block Type in Entity! ' + str(self.content_block_type))

        message.content_block_type = self.content_block_type
        message.public = bool_to_string(self.public)

        return message
    
    def to_integration_message(self):
        message = IntegrationContentBlock()

        if self.content_block_type == ContentBlockTypes.TEXT:
            message.title = self.title
            message.text = self.text
        elif self.content_block_type == ContentBlockTypes.AUDIO:
            message.title = self.title
            message.artists = self.artists
            message.file_id = file_dir + self.file_id

        elif self.content_block_type == ContentBlockTypes.VIDEO:
            message.title = self.title
            message.video_url = self.youtube_url
        elif self.content_block_type == ContentBlockTypes.IMAGE:
            message.title = self.title
            message.file_id = file_dir + self.file_id

            if self.link_url == None:
                message.link_url = ""
            else:
                if self.link_url.startswith('http://') == False and self.link_url.startswith('https://') == False:
                    message.link_url = "http://" + self.link_url
                else:
                    message.link_url = self.link_url

            if hasattr(self,"scale_x") and self.scale_x != None:
                message.scale_x = self.scale_x
                
            if hasattr(self,"alt_text") and self.alt_text != None:
                message.alt_text = self.alt_text

        elif self.content_block_type == ContentBlockTypes.LINK:
            message.title = self.title
            message.text = self.text
            message.link_type = self.link_type

            #add special link type prefixes
            if self.link_type == ContentLinkTypes.EMAIL and self.link_url.startswith('mailto:') == False:
                message.link_url = "mailto:" + self.link_url
            elif self.link_type == ContentLinkTypes.TEL and self.link_url.startswith('tel:') == False:
                message.link_url = "tel:" + self.link_url
            elif self.link_type != ContentLinkTypes.TEL and self.link_type != ContentLinkTypes.EMAIL:
                if self.link_url.startswith('http://') == False and self.link_url.startswith('https://') == False:
                    message.link_url = "http://" + self.link_url
                else:
                    message.link_url = self.link_url
            else:
                message.link_url = self.link_url

        elif self.content_block_type == ContentBlockTypes.EBOOK:
            message.title = self.title
            message.artists = self.artists
            message.file_id = file_dir + self.file_id
        elif self.content_block_type == ContentBlockTypes.CONTENT:
            message.title = self.title
            message.content_id = self.content_id
        elif self.content_block_type == ContentBlockTypes.SOUNDCLOUD:
            message.title = self.title
            message.soundcloud_url = self.soundcloud_url
        elif self.content_block_type == ContentBlockTypes.DOWNLOAD:
            message.title = self.title
            message.text = self.text
            message.download_type = self.download_type
            message.file_id = file_dir + self.file_id
        elif self.content_block_type == ContentBlockTypes.SPOTMAP:
            message.title = self.title
            message.spot_map_tag = self.spot_map_tag
        else:
            logging.error('Invalid Content Block Type in Entity! ' + str(self.content_block_type))

        message.content_block_type = self.content_block_type
        message.public = bool_to_string(self.public)

        return message

## model to store nested localized information of a customer content
class LocalizedContentInformation(object):

    def __init__(self):
        ## the id of the content this item belongs to
        self.content_id = ""
        
        ## the language of this localized information
        self.language = ""
    
        ## the content's display name
        self.title = ""
    
        ## the content's description
        self.description = ""
    
        ## the content blocks
        self.content_blocks = []

## model to store a content
class Content(object):

    def __init__(self):
        ## the content's id
        self.content_id = ""
    
        ## the content's internal name (for search)
        self.name = ""

        ## the content's cover Image
        self.image_name = None
   
        ## Search tags of this content
        self.tags = []
        
        self.category = 0
        
        self.localized_content_information = {}
        
        self.style = None
    
    def to_enduser_message(self, lang, system, full=True):
        localized_content = None
        if self.localized_content_information.has_key(lang):
            localized_content = self.localized_content_information[lang]
        else: #default to first
            localized_content = self.localized_content_information[self.localized_content_information.keys()[0]]
            lang = localized_content.language

        message = EndUserContentResponseMessage(
            language = lang,
            title = localized_content.title,
            description = localized_content.description
        )

        if self.image_name != None:
            message.image_public_url = file_dir + self.image_name

        content_blocks = [block.to_integration_message() for block in localized_content.content_blocks]

        #add category
        if hasattr(self, 'category') and self.category != None:
            message.category = self.category

        if full == True:
            message.content_blocks = [block.to_enduser_message() for block in localized_content.content_blocks]
        else:
            raw_blocks = [block.to_enduser_message() for block in localized_content.content_blocks]
            message.content_blocks = []

            for block in raw_blocks:
                if block.public == "True":
                    message.content_blocks.append(block)

        message.content_id = self.content_id

        return message
    
    def to_integration_message(self,system):

        message = IntegrationContentMessage(content_id=self.content_id,
                                            name=self.name,
                                            languages=self.localized_content_information.keys())

        return message
    

    def to_full_integration_message(self,lang,system):
        
        if self.localized_content_information.has_key(lang):
            localized_content = self.localized_content_information[lang]
        else: #default to first
            localized_content = self.localized_content_information[self.localized_content_information.keys()[0]]

        message = IntegrationContentResponseMessage(
            system_id = 1, #always 1 since this isn't multitenant
            title = localized_content.title,
            description = localized_content.description
        )

        if self.image_name != None:
            message.image_public_url = file_dir + self.image_name

        content_blocks = [block.to_integration_message() for block in localized_content.content_blocks]

        #clean content block - remove not public
        clean_content_blocks = []
        for block in content_blocks:
            if block.public == 'True':
                clean_content_blocks.append(block)

        message.content_blocks = clean_content_blocks

        #get style
        message.system_style = self.style.to_integration_message()

        return message

## model to store a menu which is just a list of content ids
class Menu(object):

    ## the content keys
    keys = []

    def to_enduser_message(self, lang, system, db):
        message = EndUserMenuItemsMessage(items=[])

        i = 0
        while i < len(self.keys):
            content = db.get_content_by_id(self.keys[i])
            
            title = ""
            
            localized_content = None
            if content.localized_content_information.has_key(lang):
                localized_content = content.localized_content_information[lang]
            else: #default to first
                localized_content = content.localized_content_information[content.localized_content_information.keys()[0]]
            
            title = localized_content.title
                    
            item = EndUserMenuItemMessage(content_id=content.content_id,item_label=title)
            item.category = content.category

            message.items.append(item)

            i = i + 1

        return message
