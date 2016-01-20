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

## @package xamoom_admin_api
# @brief This files contains a class XamoomAdminApi and the helper method check_user
# @todo check_user should be moved to another module with helper methods.
# @author Bruno Hautzenberger
# @copyright xamoom GmbH, 2014. All rights reserved.


import logging
import endpoints
import os
from datetime import datetime

from protorpc import messages
from protorpc import message_types
from protorpc import remote

#utils
from util import bool_to_string

from integration_api_messages import IntegrationContentListResponseMessage
from integration_api_messages import IntegrationContentResponseMessage
from integration_api_messages import IntegrationSpotMapResponseMessage

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

## Contains all integration API methods.
@endpoints.api(name='xamoomIntegrationApi', version='v1', description='xamoom Integration API')
class XamoomIntegrationApi(remote.Service):

    @endpoints.method(endpoints.ResourceContainer(
                                                    message_types.VoidMessage,
                                                    ft_query=messages.StringField(1),
                                                    cursor=messages.StringField(2),
                                                    page_size=messages.IntegerField(3),
                                                    sort_direction=messages.StringField(4)
                                                ),
                                                IntegrationContentListResponseMessage,path='content',
                                                http_method='GET',name='integration.content_query')
    def query_content(self, request):
        db = CSVDataProvider()
        system = check_auth(self,request,db)

        cursor = int(request.cursor) if hasattr(request, 'cursor') and request.cursor != None else 0
        page_size = int(request.page_size) if hasattr(request, 'page_size') and request.page_size != None and request.page_size <= 100 else 10
        sort_direction = request.sort_direction if hasattr(request, 'sort_direction') and request.sort_direction != None else 'ASC'

        contents, next_curs, more = db.query_content(request.ft_query,cursor,page_size,sort_direction)
        
        content_items = [content_item.to_integration_message(system) for content_item in contents]

        return IntegrationContentListResponseMessage(items=content_items, cursor=str(next_curs), has_more=bool_to_string(more))


    @endpoints.method(endpoints.ResourceContainer(
                                                    message_types.VoidMessage,
                                                    content_id=messages.StringField(1,required=True),
                                                    language=messages.StringField(2,required=True)
                                                ),
                                                IntegrationContentResponseMessage,path='content/{content_id}/{language}',
                                                http_method='GET',name='integration.content_by_id')
    def get_content_by_content_id(self, request):
        db = CSVDataProvider()
        system = check_auth(self,request,db)

        request.language = request.language.split('-')[0]

        content_id = request.content_id

        #get Content
        content = db.get_content_by_id(content_id)

        response = content.to_full_integration_message(request.language,system)

        return response


    @endpoints.method(endpoints.ResourceContainer(
                                                    message_types.VoidMessage,
                                                    map_tag=messages.StringField(1,required=True),
                                                    language=messages.StringField(2,required=True)
                                                ),
                                                IntegrationSpotMapResponseMessage,path='spotmap',
                                                http_method='GET',name='enduser.get_spot_map')
    def get_spot_map(self, request):
        db = CSVDataProvider()
        system = check_auth(self,request,db)
        
        language = request.language.split('-')[0]

        spots = db.get_spot_map(request.map_tag)

        items = [s.to_integration_message(language) for s in spots]
        
        return IntegrationSpotMapResponseMessage(items=items)

