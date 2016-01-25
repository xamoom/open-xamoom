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

## @package xamoom_enduser_api
# @brief This files contains a class XamoomEndUserApi
# @author Bruno Hautzenberger
# @copyright xamoom GmbH, 2014. All rights reserved.



import logging
import endpoints
import os
import base64
from protorpc import messages
from protorpc import message_types
from protorpc import remote

from util import string_to_bool
from util import bool_to_string


from enduser_api_messages import EndUserScanRequestMessage
from enduser_api_messages import EndUserContentRequestMessage
from enduser_api_messages import EndUserScanResponseMessage
from enduser_api_messages import EndUserSignleContentResponseMessage
from enduser_api_messages import EndUserGeoScanRequestMessage
from enduser_api_messages import GeofenceContentResponseMessage
from enduser_api_messages import GeofenceResponseMessage
from enduser_api_messages import EnduserSpotMapResponseMessage
from enduser_api_messages import EnduserSpotMessage
from enduser_api_messages import GeofenceAnalyticsMessage
from enduser_api_messages import EnduserContentListResponseMessage

#Data Access REPLACE THIS WITH THE DATA ACCESS OBJECT TO YOUR CMS DATABASE
from CSVDataProvider import CSVDataProvider

#Data Access REPLACE THIS WITH THE DATA ACCESS OBJECT TO YOUR CMS DATABASE
from CSVDataProvider import CSVDataProvider

def check_auth(request,msg,db):
    #get API Key from Header
    api_key = ""
    try:
        api_key = request.request_state.headers['Authorization']
        if api_key == None:
            if hasattr(msg,'api_key') and msg.api_key != None:
                api_key = msg.api_key
            else:
                raise endpoints.UnauthorizedException('No API Key!')
    except:
        if hasattr(msg,'api_key') and msg.api_key != None:
            api_key = msg.api_key
        else:
            raise endpoints.UnauthorizedException('No Authorization Header!')

    logging.info("API KEY:" + api_key)

    #Load System by API Key
    system = db.get_system_by_api_key(api_key)

    logging.info("INTEGRATION API CALL: SystemName[" + system.name + "]")

    return system

## Contains all end user API methods.
@endpoints.api(name='xamoomEndUserApi', version='v1', description='xamoom End User API')
class XamoomEndUserApi(remote.Service):

    ## Used to get content, menu and style of a scan
    # @param request as EndUserScanRequestMessage
    # @return response as EndUserScanResponseMessage
    @endpoints.method(EndUserScanRequestMessage, EndUserScanResponseMessage,path='get_content_by_location_identifier', http_method='POST',name='enduser.get_content_by_location_identifier')
    def get_content_by_location_identifier(self, request):
        db = CSVDataProvider()
        system = check_auth(self,request,db)
        
        language = request.language.split('-')[0]
        
        #initialize response
        response = EndUserScanResponseMessage()
        
        #get marker
        marker = db.get_marker(request.location_identifier)
        
        #get spot connected to marker
        spot = db.get_spot(marker.spot_id)
        
        #get content
        content = db.get_content_by_id(spot.content)
        content_message = content.to_enduser_message(language, system, full=True)
        
        #set status flags
        #on the CSV backend both always have to be true
        response.has_spot = bool_to_string(True)
        response.has_content = bool_to_string(True)
        
        #get system name
        system_name = system.name
        l_infos = system.localized_information
        for info in l_infos: #try to find selected language
            if info.language == content_message.language:
                system_name = info.display_name
        
        #get settings
        settings = db.get_settings()
        response.app_id_google_play = settings[1]
        response.app_id_itunes = settings[0]

        #render message
        response.system_name = system_name
        response.system_url = system.base_url #not needed in apps or wordpress
        response.system_id = 1 #always 1, because this is single tenant
        
        response.content = content_message
        
        #render message
        if string_to_bool(request.include_style):
            response.style = content.style.to_enduser_message()
        
        if string_to_bool(request.include_menu):
            response.menu = db.get_menu().to_enduser_message(content_message.language, system, db)

        return response
        
    ## Used to get content by location (geofencing)
    @endpoints.method(EndUserGeoScanRequestMessage, GeofenceResponseMessage,path='get_content_by_location', http_method='POST',name='enduser.get_content_by_location')
    def get_content_by_location(self, request):
        db = CSVDataProvider()
        system = check_auth(self,request,db)
        
        language = request.language.split('-')[0]
        
        #load spots in radius
        spots = db.get_spots_in_radius(request.location.lat,request.location.lon,40)
        
        ##prepare response
        response = GeofenceResponseMessage()
        response.items = []
                
        #get style
        style = db.get_style()
        
        content_ids = []
        for s in spots:
            #do not add dublicates
            if (s.content in content_ids) == False:
                #get Content
                content = db.get_content_by_id(s.content)
                content_message = content.to_enduser_message(language, system, full=True)
                
                #get system name
                system_name = system.name
                l_infos = system.localized_information
                for info in l_infos: #try to find selected language
                    if info.language == content_message.language:
                        system_name = info.display_name
                
                #render content message
                item = GeofenceContentResponseMessage(
                            language = content_message.language,
                            title = content_message.title,
                            description = content_message.description,
                            content_id = content.content_id,
                            lat = float(s.location[0]),
                            lon =float(s.location[1]),
                            system_name = system_name,
                            system_url = system.base_url,
                            style_fg_color = style.fg_color,
                            style_bg_color = style.bg_color,
                            style_hl_color = style.hl_color,
                            style_icon = base64.b64decode(style.icon),
                            system_id = 1, #always 1, because this is single tenant
                            content_name = content.name, #only for geofence analytics
                            spot_id = int(s.spot_id), #only for geofence analytics
                            spot_name = s.name, #only for geofence analytics
                            image_public_url = content_message.image_public_url
                        )

                response.items.append(item)

                content_ids.append(content.content_id)
            
        return response
    
    ## Used to queue geofence analytics
    @endpoints.method(GeofenceAnalyticsMessage, message_types.VoidMessage,path='queue_geofence_analytics', http_method='POST',name='enduser.queue_geofence_analytics')
    def queue_geofence_analytics(self, request):
        logging.warn("NOT IMPLEMENTED")
        
        #TODO Add your analytics backend here and save all the values of the incoming GeofenceAnalyticsMessage (request)

        return message_types.VoidMessage()
    
    ## Used to get content, menu and style by content id
    # @param request as EndUserContentRequestMessage
    # @return response as EndUserSignleContentResponseMessage
    @endpoints.method(EndUserContentRequestMessage, EndUserSignleContentResponseMessage,path='get_content_by_content_id', http_method='POST',name='enduser.get_content_by_content_id')
    def get_content_by_content_id(self, request):
        db = CSVDataProvider()
        system = check_auth(self,request,db)

        request.language = request.language.split('-')[0]

        content_id = request.content_id
        
        response = EndUserSignleContentResponseMessage()

        #get Content
        content = db.get_content_by_id(content_id)

        content_message = content.to_enduser_message(request.language, system, full=True)
        response.content = content_message
        
        #get system name
        system_name = system.name
        l_infos = system.localized_information
        for info in l_infos: #try to find selected language
            if info.language == content_message.language:
                system_name = info.display_name
                
        #get settings
        settings = db.get_settings()
        response.app_id_google_play = settings[1]
        response.app_id_itunes = settings[0]

        #render message
        response.system_name = system_name
        response.system_url = system.base_url #not needed in apps or wordpress
        response.system_id = 1 #always 1, because this is single tenant

        
        if string_to_bool(request.include_style):
            response.style = content.style.to_enduser_message()
        
        if string_to_bool(request.include_menu):
            response.menu = db.get_menu().to_enduser_message(content_message.language, system, db)

        return response
    
    @endpoints.method(endpoints.ResourceContainer(
                                                    message_types.VoidMessage,
                                                    system_id=messages.IntegerField(1,required=True), #always Zero for API KEY REQUESTS
                                                    map_tag=messages.StringField(2,required=True),
                                                    language=messages.StringField(3,required=True),
                                                    include_content=messages.StringField(4)
                                                ),
                                                EnduserSpotMapResponseMessage,path='spotmap/{system_id}/{map_tag}/{language}',
                                                http_method='GET',name='enduser.get_spot_map')
    def get_spot_map(self, request):
        db = CSVDataProvider()
        system = check_auth(self,request,db)
        
        language = request.language.split('-')[0]

        spots = db.get_spot_map(request.map_tag)
        
        #check if spots should also deliver content
        include_content = False
        if hasattr(request,'include_content') == True and request.include_content != None:
            include_content = string_to_bool(request.include_content)

        items = [s.to_enduser_message(language,system,include_content=include_content) for s in spots]
        
        return EnduserSpotMapResponseMessage(items=items,style=db.get_style().to_enduser_message())
        
    ## Used to get content by location (geofencing)
    @endpoints.method(EndUserGeoScanRequestMessage, EnduserSpotMapResponseMessage,path='get_closest_spots', http_method='POST',name='enduser.get_closest_spots')
    def get_closest_spots(self, request):
        db = CSVDataProvider()
        system = check_auth(self,request,db)
        
        language = request.language.split('-')[0]
        
        request.limit = 1000 if hasattr(request,'limit') == False or request.limit == None or request.limit > 1000 else request.limit
        request.radius = 10000 if hasattr(request,'radius') == False or request.radius == None or request.radius > 10000 else request.radius
        
        #load spots in radius
        spots = db.get_spots_in_radius(request.location.lat,request.location.lon,request.radius,sort=True,limit=request.limit)
        
        #convert to messages
        items = [s.to_enduser_message(language, system) for s in spots]
        
        return EnduserSpotMapResponseMessage(items=items,limit=request.limit,radius=request.radius)

    @endpoints.method(endpoints.ResourceContainer(
                                                    message_types.VoidMessage,
                                                    language=messages.StringField(1,required=True),
                                                    page_size=messages.IntegerField(2,required=True),
                                                    cursor=messages.StringField(3,required=True),
                                                    tags=messages.StringField(4)
                                                ),
                                                EnduserContentListResponseMessage,path='content_list/{language}/{page_size}/{cursor}/{tags}',
                                                http_method='GET',name='enduser.get_content_list')
    def get_content_list(self, request):
        db = CSVDataProvider()
        system = check_auth(self,request,db)
        
        request.language = request.language.split('-')[0]

        cursor = request.cursor if hasattr(request, 'cursor') and request.cursor != None else 0
        
        if cursor == 'null':
            cursor = '0'
            
        cursor = int(cursor)
        
        page_size = int(request.page_size) if hasattr(request, 'page_size') and request.page_size != None and request.page_size <= 100 else 10
        
        tags = request.tags if hasattr(request, 'tags') else None
        tags = None if tags == 'null' else tags

        contents, next_curs, more = db.query_content_by_tags(tags,cursor,page_size)
        
        content_items = [content_item.to_enduser_message(request.language, system, full=False) for content_item in contents]

        return EnduserContentListResponseMessage(items=content_items, cursor=str(next_curs), more=bool_to_string(more))
    
    @endpoints.method(EndUserContentRequestMessage, EndUserSignleContentResponseMessage,path='get_content_by_content_id_full', http_method='POST',name='enduser.get_content_by_content_id_full')
    def get_content_by_content_id_full(self, request):
        db = CSVDataProvider()
        system = check_auth(self,request,db)

        request.language = request.language.split('-')[0]

        content_id = request.content_id
        
        response = EndUserSignleContentResponseMessage()

        #get Content
        content = db.get_content_by_id(content_id)

        #deliver full content?
        full = True if hasattr(request,"full") == True and request.full != None and string_to_bool(request.full) == True else False

        content_message = content.to_enduser_message(request.language, system, full=full)
        response.content = content_message
        
        #get system name
        system_name = system.name
        l_infos = system.localized_information
        for info in l_infos: #try to find selected language
            if info.language == content_message.language:
                system_name = info.display_name
                
        #get settings
        settings = db.get_settings()
        response.app_id_google_play = settings[1]
        response.app_id_itunes = settings[0]

        #render message
        response.system_name = system_name
        response.system_url = system.base_url #not needed in apps or wordpress
        response.system_id = 1 #always 1, because this is single tenant

        
        if string_to_bool(request.include_style):
            response.style = content.style.to_enduser_message()
        
        if string_to_bool(request.include_menu):
            response.menu = db.get_menu().to_enduser_message(content_message.language, system, db)

        return response
        