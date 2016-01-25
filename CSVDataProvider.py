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

## @package enduser_data_access
# @brief This files shows what your specific backend has to deliver in terms of data.
# This example uses static CSV files to read the data from. Just replace this (keepin the methods and types)
# with a data provider for your targeted CMS.
# @author Bruno Hautzenberger

import endpoints
import logging
import csv
import urllib2
import base64

from models import System, LocalizedSystemInformation, Content, LocalizedContentInformation, ContentBlock, Spot, LocalizedSpotInformation, SystemStyle, Menu, Marker
from config import data_dir
from util import string_to_bool
from static_types import ContentBlockTypes
from math import radians, cos, sin, asin, sqrt
from util import location_message_from_geopoint 

class CSVDataProvider():

    def __init__(self):
        self.system = None
        self.marker = None
        self.spots = None
        self.content = None
        self.menu = None
        self.settings = None
        
    def get_system_by_api_key(self,api_key):
        if self.system == None: self.load_system()
        #CHECK API KEY
        if self.system.api_key != api_key:
            raise endpoints.UnauthorizedException('Invalid API Key!')
        
        return self.system
    
    def get_menu(self):
        if self.menu == None: self.load_menu()
        return self.menu
    
    def get_settings(self):
        if self.settings == None: self.load_settings()
        return self.settings
    
    def get_style(self):
        style = SystemStyle()
        style_sys_data = self.__read_csv("system_style")[0]
        self.__fill_members_with_csv_data(style,('fg_color','bg_color','hl_color','ch_color','icon','custom_marker'),style_sys_data)
        return style
    
    def get_marker(self,uid):
        if self.marker == None: self.load_markers()
        
        for m in self.marker:
            if m.qr == uid or m.nfc == uid or m.eddystone == uid or m.ibeacon_minor == uid:
                return m
            
        raise endpoints.NotFoundException("Marker with uid " + uid + " does not exist!")
    
    def get_spot(self,spot_id):
        if self.spots == None: self.load_spots()

        for s in self.spots.values():
            if s.spot_id == spot_id:
                return s
            
        raise endpoints.NotFoundException("Spot with id " + spot_id + " does not exist!")
    
    def get_content_by_id(self,content_id):
        if self.content == None: self.load_content()
        
        result = [c for c in self.content.values() if content_id in c.content_id]
        
        if len(result) == 0:
            raise endpoints.NotFoundException("Content with content_id " + content_id + " does not exist!")
        else:
            return result[0]
        
    def query_content(self,ft_query,cursor,page_size,sort_direction):
        if self.content == None: self.load_content()
        
        #sort direction
        reverse = (sort_direction == "DESC")
        
        #filter
        if ft_query != None:
            result = [c for c in self.content.values() if ft_query.upper() in c.name.upper()]
        else:
            result = self.content.values()
            
        #sort      
        result.sort(key=lambda c: c.name, reverse=reverse)
        
        #cut page
        start = cursor * page_size
        start = start if start < len(result) else len(result)
        
        end = start + page_size
        end = end if end < len(result) else len(result)
        
        next_cursor = cursor + 1
        has_more = end < (len(result) - 1)
        
        return result[start:end], next_cursor, has_more
    
    def query_content_by_tags(self,tags,cursor,page_size):
        if self.content == None: self.load_content()
                
        #filter
        if tags != None:
            tags = tags.split(',')
            result = []
            for c in self.content.values():
                for t in tags:
                    if t in c.tags:
                        result.append(c)            
        
        #cut page
        start = cursor * page_size
        start = start if start < len(result) else len(result)
        
        end = start + page_size
        end = end if end < len(result) else len(result)
        
        next_cursor = cursor + 1
        has_more = end < (len(result) - 1)
        
        return result[start:end], next_cursor, has_more
    
    def get_spot_map(self,map_tag):
        if self.spots == None: self.load_spots()
        
        result = self.spots.values()
        if map_tag != "showAllTheSpots":
            result = [s for s in self.spots.values() if map_tag in s.tags]
                
        return result
    
    def get_spots_in_radius(self,lat,lon,radius,sort=False,limit=None):
        if self.spots == None: self.load_spots()
        
        result = [s for s in self.spots.values() if self.get_distance(float(lat),float(lon),float(s.location[0]),float(s.location[1])) <= radius]
        
        if sort:
            result.sort(key=lambda s: self.get_distance(float(lat),float(lon),float(s.location[0]),float(s.location[1])), reverse=False)
            
        if limit != None and limit < len(result):
            result = result[0:limit]
        
        return result
    
    def load_system(self):
        sys_data = self.__read_csv("system")[0]
        localized_sys_data = self.__read_csv("system_localized")
        
        ## READ SYSTEM
        #system csv structure: name;api_key
        self.system = System()
        self.__fill_members_with_csv_data(self.system,('name','api_key','base_url'),sys_data)
        
        ## READ LOCALIZED SYSTEM DATA
        # localized system csv structure lang;display_name;description;long_description
        for item in localized_sys_data:
            lang = LocalizedSystemInformation()
            self.__fill_members_with_csv_data(lang,('lang','display_name','description','long_description'),item)
            self.system.localized_information.append(lang)
            
    def load_menu(self):
        menu_data = self.__read_csv("menu")[0]
        self.menu = Menu()
        self.menu.keys = menu_data
        
    def load_settings(self):
        self.settings = self.__read_csv("settings")[0]
        
    def load_content(self):
        content_data = self.__read_csv("content")
        localized_content_data = self.__read_csv("content_localized")
        contentblocks_data = self.__read_csv("content_blocks")
        style_sys_data = self.__read_csv("system_style")[0]
        
        #load style
        ## READ STYLE
        style = SystemStyle()
        self.__fill_members_with_csv_data(style,('fg_color','bg_color','hl_color','ch_color','icon','custom_marker'),style_sys_data)
        
        #load content
        self.content = {}
        for item in content_data:
            c = Content()
            self.__fill_members_with_csv_data(c,('content_id','name','image_name','tags','category'),item)
            c.tags = c.tags.split(',') #split tags
            c.category = int(c.category) #parse category to int
            c.style = style
        
            self.content[c.content_id] = c #add to content items
        
        #load localized info
        for item in localized_content_data:
            lang = LocalizedContentInformation()
            self.__fill_members_with_csv_data(lang,('content_id','language','title','description'),item)
            
            #add to right content
            if self.content.has_key(item[0]):
                self.content[item[0]].localized_content_information[item[1]] = lang
            else:
                logging.warn("Localized Content Data with invalid content id: " + item[0])
                
        #load content blocks
        for item in contentblocks_data:
            #they have to be parsed in a special way,because they vary in terms of fields
            b = ContentBlock()
            b.content_id = item[0]
            b.content_block_type = int(item[2])
            b.public = string_to_bool(item[3])
            
            if b.content_block_type == ContentBlockTypes.TEXT:
                b.title = item[4]
                b.text = item[5]
            elif b.content_block_type == ContentBlockTypes.AUDIO:
                b.title = item[4]
                b.artists = item[5]
                b.file_id = item[6]
            elif b.content_block_type == ContentBlockTypes.VIDEO:
                b.title = item[4]
                b.youtube_url = item[5]
            elif b.content_block_type == ContentBlockTypes.IMAGE:
                b.title = item[4]
                b.file_id = item[5]
                b.scale_x = float(item[6])
                b.alt_text = item[7]
            elif b.content_block_type == ContentBlockTypes.LINK:
                b.title = item[4]
                b.text = item[5]
                b.link_type = int(item[6])
                b.link_url = item[7]
            elif b.content_block_type == ContentBlockTypes.EBOOK:
                b.title = item[4]
                b.artists = item[5]
                b.file_id = item[6]
            elif b.content_block_type == ContentBlockTypes.CONTENT:
                b.title = item[4]
                b.content_id = item[5]
            elif b.content_block_type == ContentBlockTypes.SOUNDCLOUD:
                b.title = item[4]
                b.soundcloud_url = item[5]
            elif b.content_block_type == ContentBlockTypes.DOWNLOAD:
                b.title = item[4]
                b.text = item[5]
                b.download_type = int(item[6])
                b.file_id = item[7]
            elif b.content_block_type == ContentBlockTypes.SPOTMAP:
                b.title = item[4]
                b.spot_map_tag = item[5]
            else:
                raise Exception("Unknown Content Block Type: " + str(b.content_block_type))
                
            #add to right content and lang
            if self.content.has_key(item[0]):
                if self.content[item[0]].localized_content_information.has_key(item[1]):
                    self.content[item[0]].localized_content_information[item[1]].content_blocks.append(b)
                else:
                    logging.warn("Content Block Data with invalid lang: " + item[0] + "/" + item[1])
            else:
                logging.warn("Content Block Data with invalid content id: " + item[0])
        
    def load_spots(self):
        spots_data = self.__read_csv("spots")
        localized_spots_data = self.__read_csv("spots_localized")
        
        #load content
        self.spots = {}
        for item in spots_data:
            s = Spot()
            self.__fill_members_with_csv_data(s,('spot_id','name','image','category','location','content','tags'),item)
            s.tags = s.tags.split(',') #split tags
            s.location = s.location.split(',') #split location
            s.category = int(s.category) #parse category to int        
            self.spots[s.spot_id] = s #add to spots
        
        #load localized info
        for item in localized_spots_data:
            lang = LocalizedSpotInformation()
            self.__fill_members_with_csv_data(lang,('spot_id','language','display_name','description'),item)
            
            #add to right content
            if self.spots.has_key(item[0]):
                self.spots[item[0]].localized_information[item[1]] = lang
            else:
                logging.warn("Localized Spot Data with invalid spot id: " + item[0])
                
    def load_markers(self):
        marker_data = self.__read_csv("marker")
        
        #load marker
        self.marker = []
        for item in marker_data:
            m = Marker()
            self.__fill_members_with_csv_data(m,('spot_id','qr','nfc','eddystone','ibeacon_region_uid','ibeacon_major','ibeacon_minor'),item)       
            self.marker.append(m)
        
        
    def __fill_members_with_csv_data(self,obj, sorted_members, csv_data):
        if len(sorted_members) == len(csv_data):
            i = 0
            while i < len(sorted_members):
                setattr(obj, sorted_members[i], csv_data[i].decode('utf-8'))
                i = i + 1
        else:
            logging.error("CSV data does not match object members!")
            raise Exception("CSV data does not match object members!")
        
    def __read_csv(self,name):
        url = data_dir + name + '.csv'
        response = urllib2.urlopen(url)
        reader = csv.reader(response, delimiter=';', quotechar='|')
        
        data = []
        for row in reader:
            data.append(row)
            
        return data
           
    def get_distance(self, lon1, lat1, lon2, lat2):
        # convert decimal degrees to radians 
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
        # haversine formula 
        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371 # Radius of earth in kilometers.
        
        logging.info("DISTANCE: " + str((c * r) * 1000))
        
        return (c * r) * 1000 #in meters